"""OpenAI Responses translated into the existing canonical conversation protocol."""
from types import SimpleNamespace as NS


def response_request(params,cache=None):
    cache=cache or {};inputs=[];instructions=[]
    for message in params.get('messages',[]):
        role=message.get('role');content=message.get('content')
        if role=='system':instructions.append(str(content or ''));continue
        calls=message.get('tool_calls',[])
        cached=cache.get(calls[0]['id']) if calls else None
        if cached:
            inputs.extend(cached);continue
        if role=='tool':inputs.append({'type':'function_call_output','call_id':message['tool_call_id'],'output':str(content or '')});continue
        if role in ('user','assistant') and content:inputs.append({'role':role,'content':str(content)})
        for call in calls:inputs.append({'type':'function_call','call_id':call['id'],'name':call['function']['name'],'arguments':call['function']['arguments']})
    result={'model':params['model'],'input':inputs,'instructions':'\n\n'.join(instructions),
            'stream':params.get('stream',False),'store':False,'include':['reasoning.encrypted_content'],
            'max_output_tokens':params.get('max_tokens',8192)}
    if params.get('tools'):
        result['tools']=[{'type':'function',**tool['function'],'strict':False} for tool in params['tools']]
        choice=params.get('tool_choice','auto')
        result['tool_choice']={'type':'function','name':choice['function']['name']} if isinstance(choice,dict) else choice
    if params.get('response_format'):result['text']={'format':params['response_format']}
    return result


def chat_chunk(content=None,calls=None,finish=None):
    return NS(choices=[NS(delta=NS(content=content,tool_calls=calls or []),finish_reason=finish)])


class ResponseEvents:
    def __init__(self,cache):
        self.cache=cache;self.started=set();self.arguments=set()

    def translate(self,event):
        kind=event.type
        if kind in ('response.output_text.delta','response.refusal.delta'):return chat_chunk(content=event.delta)
        if kind=='response.output_item.added' and event.item.type=='function_call':
            self.started.add(event.output_index)
            return chat_chunk(calls=[NS(index=event.output_index,id=event.item.call_id,function=NS(name=event.item.name,arguments=''))])
        if kind=='response.function_call_arguments.delta':
            self.arguments.add(event.output_index)
            return chat_chunk(calls=[NS(index=event.output_index,id=None,function=NS(name=None,arguments=event.delta))])
        if kind=='response.output_item.done' and event.item.type=='function_call':
            item=event.item;index=event.output_index
            if index not in self.started:return chat_chunk(calls=[NS(index=index,id=item.call_id,function=NS(name=item.name,arguments=item.arguments))])
            if index not in self.arguments:return chat_chunk(calls=[NS(index=index,id=None,function=NS(name=None,arguments=item.arguments))])
        if kind in ('error','response.failed'):
            raise RuntimeError('OpenAI Responses: сервер завершил запрос с ошибкой. Проверьте доступ к модели и настройки подключения.')
        if kind in ('response.completed','response.incomplete'):
            output=[item.model_dump(mode='json',exclude_none=True) for item in event.response.output]
            for item in output:
                if item['type']=='function_call':self.cache[item['call_id']]=output
            return chat_chunk(finish='length' if kind=='response.incomplete' else 'stop')
        return None


def response_completion(response):
    text=response.output_text
    return NS(choices=[NS(message=NS(content=text),finish_reason='stop')])
