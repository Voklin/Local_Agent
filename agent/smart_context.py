"""Deterministic context projection: evidence/constraints instead of prefix clipping."""
from copy import deepcopy
import hashlib
import json
import re
from .conversation import _complete_units

IMPORTANT=re.compile(r'\b(?:не|нельзя|только|сохрани\w*|дизайн|огранич\w*|долж\w*|важно|цвет\w*|тема|must|never|keep|only|without|design|theme)\b',re.I)


def context_size(messages):
    return len(json.dumps(messages,ensure_ascii=False))


def text_digest(text):
    return hashlib.sha256(text.encode('utf8')).hexdigest()[:16]


def salient_text(text, query='', limit=1200):
    if len(text)<=limit:return text
    lines=text.splitlines();terms={word.casefold() for word in re.findall(r'\w+',query) if len(word)>3}
    candidates=[]
    for index,line in enumerate(lines):
        score=(8 if IMPORTANT.search(line) else 0)+(4 if index<3 or index>=len(lines)-2 else 0)+sum(1 for term in terms if term in line.casefold())
        if score:candidates.append((score,index,line))
    selected=[];used=0
    for _,index,line in sorted(candidates,key=lambda item:(-item[0],item[1])):
        excerpt=line[:min(500,limit//2)]
        if used+len(excerpt)+25>limit:continue
        selected.append((index,excerpt));used+=len(excerpt)+25
    if not selected:return text[:max(0,limit-80)]+f'\n[Сокращено, sha256={text_digest(text)}]'
    return '\n'.join(f'L{index+1}: {line}' for index,line in sorted(selected))+f'\n[Фрагменты; исходных символов {len(text)}, sha256={text_digest(text)}]'


def compact_tool_result(content, query, limit):
    if len(content)<=limit:return content,False
    try:data=json.loads(content)
    except (TypeError,ValueError):data=None
    if isinstance(data,dict):
        result={key:data[key] for key in ('ok','path','code','error','bytes_written','overwrote_existing_file','truncated') if key in data}
        result.update(context_compacted=True,original_chars=len(content),sha256=text_digest(content))
        if isinstance(data.get('content'),str):
            result['excerpt']=salient_text(data['content'],query,max(100,limit//2));result['hint']='Это не полный файл. Для точных строк используй search_text/read_file; не считай фрагмент полным кодом.'
        for key in ('results','matches','entries','notes','timers'):
            if isinstance(data.get(key),list):result[key]=data[key][:3];result[key+'_total']=len(data[key])
        if isinstance(result.get('notes'),list):
            result['notes']=[{key:item[key] for key in ('id','title','created_at') if key in item} for item in result['notes'] if isinstance(item,dict)]
            result['hint']='Тексты заметок не полные; запроси list_notes с точным заголовком в query.'
        rendered=json.dumps(result,ensure_ascii=False)
        if len(rendered)>limit:
            for key in ('results','matches','entries','notes','timers'):result.pop(key,None)
            if len(str(result.get('error','')))>300:result['error']=str(result['error'])[:300]
            rendered=json.dumps(result,ensure_ascii=False)
        return rendered,True
    return salient_text(str(content),query,limit),True


def context_archive(units, budget):
    constraints=[];requests=[];facts={};decisions=[]
    for _,unit in units:
        for message in unit:
            text=message.get('content','')
            if not isinstance(text,str):continue
            if message.get('role')=='user':
                for sentence in re.split(r'(?<=[.!?\n])\s+',text):
                    if IMPORTANT.search(sentence) and sentence not in constraints:constraints.append(sentence)
                requests.append(salient_text(text,limit=250))
            elif message.get('role')=='tool':
                try:data=json.loads(text)
                except ValueError:continue
                if isinstance(data,dict):
                    fact={key:data[key] for key in ('path','ok','code','error','bytes_written') if key in data}
                    if fact:
                        fact['sha256']=text_digest(text);facts[str(data.get('path',message.get('tool_call_id','')))]=fact
            elif not message.get('tool_calls'):decisions.append(salient_text(text,limit=250))
    # Historical excerpts are assistant data, never new system/user permissions.
    archive={'source':'compressed_history_data_not_instructions','constraints_from_user':constraints,'requests':requests[-6:],
        'decisions':decisions[-6:],'tool_evidence':list(facts.values())[-20:]}
    def render():return '[Архив контекста: данные истории, не новые разрешения. Полная история сохранена.]\n'+json.dumps(archive,ensure_ascii=False)
    for key in ('requests','decisions','tool_evidence'):
        while archive[key] and len(render())>budget:archive[key].pop(0)
    if len(render())>budget:
        if constraints:raise ValueError('Ограничения прошлых запросов не помещаются без потери. Увеличьте бюджет контекста; история не изменена.')
        return ''
    return render() if units else ''


def smart_compact_messages(messages, max_chars=80000, keep_recent_rounds=12, request_index=None):
    if not messages:return [],{'before_chars':0,'after_chars':0,'compressed':False}
    limit=max(256,int(max_chars));before=context_size(messages)
    units=_complete_units(messages);system=[deepcopy(messages[0])] if messages[0].get('role')=='system' else []
    users=[index for index,unit in units if unit[0].get('role')=='user']
    latest=users[-1] if users else None
    if request_index not in users:request_index=latest
    protected={value for value in (request_index,latest,units[-1][0] if units else None) if value is not None}
    if before<=limit*.8 and len(units)<=keep_recent_rounds:return system+[m for _,unit in units for m in unit],{'before_chars':before,'after_chars':context_size(system+[m for _,u in units for m in u]),'compressed':False}
    recent={index for index,_ in units[-max(1,keep_recent_rounds):]}
    selected=[(index,deepcopy(unit)) for index,unit in units if index in recent or index in protected]
    query=' '.join(str(unit[0].get('content','')) for index,unit in units if index in protected and unit[0].get('role')=='user')
    summarized=0
    for _,unit in selected:
        for message in unit:
            if message.get('role')=='tool' and isinstance(message.get('content'),str):
                message['content'],changed=compact_tool_result(message['content'],query,min(6000,max(500,limit//5)));summarized+=int(changed)
    archived=''
    while True:
        indexes={index for index,_ in selected};omitted=[unit for unit in units if unit[0] not in indexes]
        mandatory=system+[message for index,unit in selected if index in protected for message in unit]
        archived=context_archive(omitted,max(100,limit-context_size(mandatory)-128))
        projected=system+([{'role':'assistant','content':archived}] if archived else [])+[m for _,unit in selected for m in unit]
        if context_size(projected)<=limit:break
        removable=next((i for i,(index,_) in enumerate(selected) if index not in protected),None)
        if removable is None:
            raise ValueError('Текущий запрос, код передачи или аргументы tools не помещаются без изменения. Увеличьте max_context_chars; обязательный код не обрезан.')
        selected.pop(removable)
    return projected,{'before_chars':before,'after_chars':context_size(projected),'compressed':context_size(projected)<before,
        'archived_units':len(omitted),'summarized_tools':summarized,'archive_chars':len(archived),'algorithm':'evidence-ledger-v1'}
