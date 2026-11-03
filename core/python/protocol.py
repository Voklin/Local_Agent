"""Versioned, validated critical RPC envelope. No executable names come from routing."""
import re
from agent.task_contract import validate_options

PROTOCOL_VERSION=1


def require_text(params,key,limit=200):
    value=params.get(key)
    if not isinstance(value,str) or not value or len(value)>limit or '\x00' in value:raise ValueError('Некорректное поле '+key)
    return value


def validate_request(request):
    if not isinstance(request,dict) or not isinstance(request.get('params',{}),dict):raise ValueError('Ожидается JSON-объект запроса и параметров')
    if request.get('id') is not None and type(request['id']) not in (int,str):raise ValueError('Некорректный id запроса')
    version=request.get('protocol_version',PROTOCOL_VERSION)
    if type(version) is not int or version!=PROTOCOL_VERSION:raise ValueError('Несовместимая версия протокола Neutral; перезапустите приложение с соответствующим Core')
    method=require_text(request,'method',100);params=request.get('params') or {}
    if method in ('start_task','new_chat','load_chat','list_chats','rename_chat'):
        if params.get('mode','ide') not in ('chat','ide','voice'):raise ValueError('Неизвестный режим')
    if method=='start_task':
        if type(params.get('resume',False)) is not bool:raise ValueError('Некорректный флаг resume')
        prompt=params.get('prompt','')
        if not isinstance(prompt,str) or len(prompt)>50000 or '\x00' in prompt:raise ValueError('Некорректный запрос задачи')
        if params.get('run_id') is not None and not re.fullmatch(r'[a-f0-9]{32}',str(params['run_id'])):raise ValueError('Некорректный run_id')
        if params.get('task_options') is not None:validate_options(params['task_options'])
    if method=='cancel_task' and params.get('run_id') is not None and not re.fullmatch(r'[a-f0-9]{32}',str(params['run_id'])):
        raise ValueError('Некорректный run_id')
    if method in ('resolve_approval','resolve_tool_recovery'):
        for field in (('run_id','approval_id') if method=='resolve_approval' else ('chat_id','journal_id','call_id')):require_text(params,field)
        if method=='resolve_approval' and params.get('decision') not in ('apply','reject','cancel'):raise ValueError('Некорректное решение')
        if method=='resolve_tool_recovery':
            index=params.get('message_index')
            if type(index) is not int or index<0:raise ValueError('Некорректный индекс сообщения')
            if params.get('resolution') not in ('completed','not_executed'):raise ValueError('Некорректное наблюдение')
    if method.startswith('snapshot_') and method!='snapshot_checkpoint_cancel':
        require_text(params,'chat_id')
        if method in ('snapshot_preview','snapshot_review'):require_text(params,'group_id')
        if method=='snapshot_apply':require_text(params,'proposal_id')
        if method in ('snapshot_apply','snapshot_review') and params.get('confirmed') is not True:raise ValueError('Нужно явное подтверждение')
    return method,params
