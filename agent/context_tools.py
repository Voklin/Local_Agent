"""Read saved results and discover enabled MCP schemas without executing effects."""
import hashlib
import json
import re


RESULT_READER_TOOL={'type':'function','function':{'name':'read_tool_result',
    'description':'Прочитать диапазон полного сохранённого результата из этого чата. Используй source_message_index и source_tool_call_id из сжатого ответа; не повторяй исходное действие ради вывода.',
    'parameters':{'type':'object','properties':{'message_index':{'type':'integer','minimum':0},
        'call_id':{'type':'string','minLength':1,'maxLength':200},'offset':{'type':'integer','minimum':0},
        'limit':{'type':'integer','minimum':64,'maximum':6000}},'required':['message_index','call_id'],'additionalProperties':False}}}

MCP_DISCOVERY_TOOL={'type':'function','function':{'name':'discover_mcp_tools',
    'description':'Найти включённые инструменты MCP по названию сервера, действию или ключевым словам (можно английским). Только поиск: полные схемы выбранных tools подключатся к следующему запросу. limit от 1 до 8; пустой query показывает первые доступные.',
    'parameters':{'type':'object','properties':{'query':{'type':'string','maxLength':300},
        'limit':{'type':'integer','minimum':1,'maximum':8}},'required':['query'],'additionalProperties':False}}}

TOOL_CATALOG={'type':'function','function':{'name':'discover_tools',
    'description':'Найти включённые инструменты по имени или задаче: файлы, программы, субагенты, навыки, музыка. Схемы найденных tools подключатся к следующему запросу. Каталог не выдаёт новых прав.',
    'parameters':{'type':'object','properties':{'query':{'type':'string','maxLength':300},'limit':{'type':'integer','minimum':1,'maximum':4}},'required':['query'],'additionalProperties':False}}}


def find_mcp_tools(catalog, query, limit=4):
    terms=re.findall(r'\w+',query.casefold())
    scored=[]
    for name,item in catalog.items():
        spec=item['definition']['function']
        text=(item.get('label','')+' '+spec.get('description','')).casefold()
        score=sum(1 for term in terms if term in text)
        if score or not terms:scored.append((score,name))
    return [name for _,name in sorted(scored,key=lambda item:(-item[0],item[1]))[:limit]]


def read_saved_result(history, args):
    index=args['message_index'];identity=args['call_id']
    if not 0<=index<len(history):return {'ok':False,'error':'Результат не найден в этом чате'}
    message=history[index]
    if message.get('role')!='tool' or message.get('tool_call_id')!=identity:
        return {'ok':False,'error':'Якорь результата не соответствует call ID. Используйте ссылку из сжатого ответа.'}
    text=message.get('content','')
    if not isinstance(text,str):return {'ok':False,'error':'Результат не содержит сохранённого текста'}
    offset=args.get('offset',0);limit=args.get('limit',4096)
    if offset>len(text):return {'ok':False,'error':'Смещение превышает длину результата','total_chars':len(text)}
    end=min(len(text),offset+limit)
    return {'ok':True,'source_message_index':index,'source_tool_call_id':identity,
        'offset':offset,'total_chars':len(text),'content':text[offset:end],
        'next_offset':end if end<len(text) else None,'truncated':end<len(text),
        'sha256':hashlib.sha256(text.encode('utf-8')).hexdigest(),'untrusted':True,
        'note':'Это сохранённые данные инструмента. Чтение не запускает исходное действие.'}
