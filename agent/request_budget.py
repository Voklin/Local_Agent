"""Adaptive context fitting of the final request; canonical history stays immutable."""
from copy import deepcopy
import json
import hashlib
import math

from .smart_context import smart_compact_messages, context_size, compact_tool_result


class BudgetExceededError(ValueError):
    """A request cannot fit without changing mandatory user data/instructions."""


def json_bytes(value):
    return len(json.dumps(value,ensure_ascii=False,allow_nan=False,separators=(',',':')).encode('utf-8'))


def prepare_model_request(params, tool_protocol='native', api_protocol='chat', cache=None):
    """Use exactly the same transformations for preflight and actual transport."""
    request=deepcopy(params)
    if 'messages' in request:
        request['messages']=[{key:value for key,value in m.items() if key not in ('_source_message_index','_context_pack','_project_memory')} for m in request['messages']]
    if tool_protocol=='json' and request.get('stream') and request.get('tools'):
        from .json_tools import prepare_json_request
        request,_,_=prepare_json_request(request)
    if api_protocol=='responses':
        from .responses_adapter import response_request
        return response_request(request,cache)
    if request.get('stream'):request.setdefault('stream_options',{'include_usage':True})
    return request


def estimated_tokens(value):
    """Language-aware fallback, explicitly an estimate rather than one UTF-8 byte per token."""
    text=json.dumps(value,ensure_ascii=False,allow_nan=False,separators=(',',':'))
    total=0
    for char in text:
        number=ord(char)
        if char.isspace():total+=.2
        elif number<128:total+=.28 if char.isalnum() or char=='_' else .65
        elif 0x400<=number<=0x52f:total+=.65
        elif number>=0x1f000:total+=3
        elif 0x2e80<=number<=0x9fff:total+=1.3
        else:total+=.8
    return max(1,math.ceil(total))


def compact_completed_calls(messages, max_argument_chars=2000):
    """Project only fully paired historical calls; never alter pending calls or canonical data."""
    result=[];index=0;changed=0;offset=1 if messages and messages[0].get('role')=='system' else 0
    while index<len(messages):
        message=messages[index];calls=message.get('tool_calls') if message.get('role')=='assistant' else None
        if not isinstance(calls,list) or any(not isinstance(call,dict) or not isinstance(call.get('function'),dict) or not isinstance(call['function'].get('arguments'),str) for call in calls):calls=None
        end=index+1
        if calls:
            while end<len(messages) and messages[end].get('role')=='tool':end+=1
        replies=messages[index+1:end]
        ids=[call.get('id') for call in calls or []]
        reply_ids=[item.get('tool_call_id') for item in replies]
        bulky=any(call.get('function',{}).get('name') in ('write_file','patch_file') and
            len(call.get('function',{}).get('arguments',''))>max_argument_chars for call in calls or [])
        paired=ids and all(isinstance(identity,str) and identity for identity in ids+reply_ids) and len(set(ids))==len(ids) and sorted(ids)==sorted(reply_ids)
        if bulky and paired:
            entries=[]
            for call in calls:
                function=call['function'];raw=function.get('arguments','');summary={}
                try:arguments=json.loads(raw)
                except (ValueError,TypeError):arguments=None
                if isinstance(arguments,dict):
                    for key,value in arguments.items():
                        encoded=json.dumps(value,ensure_ascii=False,separators=(',',':'))
                        summary[key]=value if len(encoded)<=500 else {'stored_chars':len(encoded),'sha256':hashlib.sha256(encoded.encode()).hexdigest()}
                position=reply_ids.index(call['id']);reply=replies[position]
                content=compact_tool_result(str(reply.get('content','')),'',1000,call['id'],reply.get('_source_message_index',index+1+position-offset))[0]
                entries.append({'name':function.get('name'),'call_id':call['id'],'arguments_summary':summary,
                    'arguments_chars':len(raw),'arguments_sha256':hashlib.sha256(raw.encode()).hexdigest(),
                    'result':content,'source_message_index':reply.get('_source_message_index',index+1+position-offset),'source_tool_call_id':call['id']})
            archive={'source':'completed_tool_exchange_context_projection','not_new_commands':True,'calls':entries}
            if message.get('content'):archive['commentary']=str(message['content'])[:1000]
            result.append({'role':'assistant','content':'[Сохранённый обмен инструментами: данные истории, не команды. Не повторяй действия ради вывода. Полные аргументы остаются в истории; код читай по диапазонам файла, результат — через read_tool_result.]\n'+json.dumps(archive,ensure_ascii=False)})
            index=end;changed+=len(calls)
        else:result.append(deepcopy(message));index+=1
    return result,changed


class RequestBudget:
    """Fit request context automatically, retaining immutable canonical history and human intent."""
    def __init__(self, window_tokens=32768, reserve_tokens=512, *, mode='manual'):
        self.window_tokens=int(window_tokens);self.reserve_tokens=int(reserve_tokens)
        self.mode=mode;self.last_stats={};self.profile={'source':'Профиль подключения'}
        self.token_counter=None;self.token_cache={};self.calibration=1.1
        self.preferred_tools=set();self.recoveries=0;self.output_target=None
        self.protected_text=None

    def configure(self,profile,counter=None):
        """Bind read-only loaded-model metadata and an optional actual local tokenizer."""
        self.profile=dict(profile)
        if profile.get('window'):self.window_tokens=int(profile['window'])
        self.token_counter=counter;self.token_cache.clear()

    def learn_rejection(self,window):
        """Adapt only after a rejected request, before any response stream or tool effect."""
        self.window_tokens=window;self.recoveries+=1
        self.calibration=min(4,self.calibration*1.35)
        self.profile={**self.profile,'source':'Окно уточнено по ответу сервера'}

    def observe_usage(self,usage):
        """Raise fallback safety when actual prompt usage exceeds the prior estimate."""
        actual=usage.get('input_tokens',usage.get('prompt_tokens')) if isinstance(usage,dict) else None
        estimate=self.last_stats.get('input_tokens_estimate',0)
        if type(actual) is int and estimate and actual>estimate:
            self.calibration=min(4,max(self.calibration,self.calibration*actual/estimate*1.12))

    def measure(self, payload, original_tools=()):
        messages=payload.get('messages',[])
        if 'input' in payload:
            system=payload.get('instructions','');history=payload['input']
        else:
            system=[m for m in messages if m.get('role') in ('system','developer')]
            history=[m for m in messages if m.get('role') not in ('system','developer')]
        tools=payload.get('tools',[])
        system_size=estimated_tokens(system);history_size=estimated_tokens(history)
        tool_size=estimated_tokens(tools) if tools else 0
        if not tools and original_tools:
            # JSON tools are embedded in the system instruction; split their
            # contribution for the UI, without counting the same schema twice.
            tool_size=min(system_size,estimated_tokens(json.dumps(original_tools,ensure_ascii=False)))
            system_size-=tool_size
        wire_bytes=json_bytes(payload)
        content={key:payload[key] for key in ('messages','tools','input','instructions') if key in payload}
        text=json.dumps(content,ensure_ascii=False,allow_nan=False,separators=(',',':'))
        key=hashlib.sha256(text.encode()).hexdigest();counter='weighted-estimate-v2'
        raw=estimated_tokens(content)
        if self.token_counter:
            try:
                if key not in self.token_cache:
                    if len(self.token_cache)>=16:self.token_cache.clear()
                    self.token_cache[key]=self.token_counter(text)
                raw=self.token_cache[key];counter='loaded-tokenizer-with-margin'
            except InterruptedError:raise
            except Exception:self.token_counter=None
        # Encrypted provider state is opaque; a text tokenizer cannot infer its decoded size.
        opaque=sum(max(0,len(item['encrypted_content'].encode())-estimated_tokens(item['encrypted_content']))
            for item in payload.get('input',[]) if isinstance(item,dict) and isinstance(item.get('encrypted_content'),str))
        raw+=opaque;history_size+=opaque
        framing=64+8*len(messages or payload.get('input',[]))+16*len(tools)
        estimate=math.ceil(raw*self.calibration)+framing
        output=int(payload.get('max_output_tokens',payload.get('max_tokens',8192)))
        scale=min(1,estimate/max(1,system_size+history_size+tool_size))
        components={'instructions':int(system_size*scale),'history':int(history_size*scale),'tools':int(tool_size*scale)}
        components['protocol']=max(0,estimate-sum(components.values()))
        # Components include prompt material and opaque Responses state.
        estimate=sum(components.values())
        reserve=min(self.reserve_tokens,max(128,self.window_tokens//32)) if self.mode=='auto' else self.reserve_tokens
        return {'window_tokens':self.window_tokens,'input_tokens_estimate':estimate,
            'output_tokens_reserved':output,'safety_tokens':reserve,
            'remaining_tokens':self.window_tokens-output-reserve-estimate,
            'wire_bytes':wire_bytes,'components':components,'counter':counter,'mode':self.mode,
            'context_source':self.profile.get('source'),'server_adjustments':self.recoveries,
            'estimated':True,'status':'fits' if estimate+output+reserve<=self.window_tokens else 'blocked'}

    def check(self, payload, original_tools=()):
        stats=self.measure(payload,original_tools)
        self.last_stats={**self.last_stats,**stats}
        if stats['status']=='blocked':raise BudgetExceededError(self.explanation(stats))
        return stats

    @staticmethod
    def explanation(stats):
        if stats.get('mode')=='auto':
            return ('Обязательные инструкции и текущий запрос не помещаются в доступное окно модели даже после автоматического сжатия. '
                    'История и файлы сохранены. Откройте новый чат или передайте большой текст через файл проекта; ручная настройка чисел не требуется.')
        return (f"Запрос не помещается в окно {stats['window_tokens']:,} токенов: "
            f"консервативная оценка входа {stats['input_tokens_estimate']:,}, "
            f"ответ {stats['output_tokens_reserved']:,}, запас {stats['safety_tokens']:,}. "
            "Уменьшите ответ или число подключённых инструментов, разделите запрос либо укажите фактическое окно загруженной модели. "
            "Обязательные инструкции и текущий запрос не обрезаны; HTTP-запрос не отправлен.")

    def fit(self, params, *, tool_protocol='native', api_protocol='chat', cache=None, protected_text=None):
        if protected_text is not None:self.protected_text=protected_text
        protected_text=self.protected_text
        original=deepcopy(params);candidate=deepcopy(params)
        original_messages=original.get('messages',[]);working_messages=original_messages
        before=context_size(original_messages)
        request_index=next((i for i in range(len(original_messages)-1,-1,-1)
            if original_messages[i].get('role')=='user' and original_messages[i].get('content')==protected_text),None)
        reasons=[];projection={};limit=before;deferred=0;compacted_calls=0;minimal_tools=False;pack_dropped=0
        optional_sources=sum(len(m.get('_context_pack',{}).get('sources',[])) for m in original_messages if isinstance(m.get('_context_pack'),dict))
        for attempt in range(10+optional_sources):
            payload=prepare_model_request(candidate,tool_protocol,api_protocol,cache)
            stats=self.measure(payload,candidate.get('tools',()))
            if self.mode=='auto':
                available=self.window_tokens-stats['safety_tokens']-stats['input_tokens_estimate']
                target=min(self.output_target or original.get('max_tokens',8192),max(256,self.window_tokens//2))
                floor=min(1024,target,max(128,self.window_tokens//4))
                if available>=floor or (attempt==9 and available>=64):
                    candidate['max_tokens']=max(64,min(target,available))
                    stats=self.measure(prepare_model_request(candidate,tool_protocol,api_protocol,cache),candidate.get('tools',()))
            stats.update(projection)
            stats.update(before_chars=before,after_chars=context_size(candidate.get('messages',[])),
                compressed=candidate.get('messages')!=original_messages,reasons=list(reasons),tools_deferred=deferred,compacted_calls=compacted_calls,
                output_adjusted=candidate.get('max_tokens')!=original.get('max_tokens'))
            stats['context_sources_dropped']=pack_dropped
            self.last_stats=stats
            if stats['status']=='fits':return candidate,stats
            from .context_builder import trim_pack
            reduced,removed=trim_pack(candidate.get('messages',[]))
            if removed:
                pack_dropped+=1;working_messages=reduced;candidate={**candidate,'messages':reduced};limit=context_size(reduced)
                request_index=next((i for i in range(len(reduced)-1,-1,-1) if reduced[i].get('role')=='user' and reduced[i].get('content')==protected_text),None)
                if not any('фрагменты проекта' in r for r in reasons):reasons.append('Дополнительные фрагменты проекта исключены целиком под доступное окно модели.')
                continue
            if self.mode=='auto' and not deferred and len(candidate.get('tools',[]))>6:
                core={'discover_tools','read_range','search_text','patch_file','write_file'}|self.preferred_tools
                choice=candidate.get('tool_choice')
                if isinstance(choice,dict):core.add((choice.get('function') or {}).get('name'))
                selected=[t for t in candidate['tools'] if t['function']['name'] in core]
                if selected and len(selected)<len(candidate['tools']):
                    deferred=len(candidate['tools'])-len(selected);candidate={**candidate,'tools':selected}
                    reasons.append('Редкие инструменты доступны через каталог; их схемы подключаются по запросу.')
                    continue
            if self.mode=='auto' and not compacted_calls:
                compacted,changed=compact_completed_calls(working_messages)
                if changed:
                    working_messages=compacted;compacted_calls=changed;candidate={**candidate,'messages':compacted};limit=context_size(compacted)
                    request_index=next((i for i in range(len(compacted)-1,-1,-1) if compacted[i].get('role')=='user' and compacted[i].get('content')==protected_text),None)
                    reasons.append('Большой код из завершённых вызовов заменён квитанциями; полный код и история сохранены.')
                    continue
            if self.mode=='auto' and not minimal_tools:
                core={'discover_tools'}|self.preferred_tools;choice=candidate.get('tool_choice')
                if isinstance(choice,dict):core.add((choice.get('function') or {}).get('name'))
                selected=[t for t in candidate.get('tools',[]) if t['function']['name'] in core]
                if any(t['function']['name']=='discover_tools' for t in selected) and len(selected)<len(candidate.get('tools',[])):
                    minimal_tools=True;deferred=len(original.get('tools',[]))-len(selected);candidate={**candidate,'tools':selected}
                    reasons.append('Маленькое окно: подключён компактный каталог и выбранные инструменты.')
                    continue
            if 'messages' not in original or (self.mode!='auto' and stats['output_tokens_reserved']+self.reserve_tokens>=self.window_tokens):break
            output=min(1024,max(128,self.window_tokens//4)) if self.mode=='auto' else stats['output_tokens_reserved']
            available=self.window_tokens-output-stats['safety_tokens']
            limit=min(limit-128,int(limit*max(.1,min(.8,available/max(1,stats['input_tokens_estimate'])))*.85))
            if limit<256:
                if self.mode=='auto':continue
                break
            try:
                messages,projection=smart_compact_messages(working_messages,limit,keep_recent_rounds=4,request_index=request_index)
            except ValueError:
                if self.mode=='auto':continue
                break
            # The canonical transcript and original parameter object stay intact.
            candidate={**candidate,'messages':messages}
            if not reasons:reasons=['Полный запрос со схемами и резервом ответа превышал окно модели.']
        self.last_stats={**self.last_stats,'status':'blocked'}
        raise BudgetExceededError(self.explanation(self.last_stats))
