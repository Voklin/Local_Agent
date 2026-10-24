"""Validated IDE role preferences, independent of Chat and companion profiles."""
from copy import deepcopy
import json
from .chat_store import APP_DIR, _atomic_write
from .model_preferences import validate_preferences

ROLES = ('conductor','coder','builder','reviewer')
ROLE_TITLES = {'conductor':'Дирижёр','coder':'Автор кода','builder':'Сборщик проекта','reviewer':'Проверяющий'}
WORKFLOW_FILE = APP_DIR / 'ide-workflow.json'
DEFAULT_WORKFLOW = {'enabled':False,'mode':'pipeline','context_length':4096,'repair_passes':1,
    'roles':{role:{'base_url':'','model':'','provider':'lmstudio','tool_protocol':'native'} for role in ROLES}}


def validate_workflow(params):
    if not isinstance(params,dict):raise ValueError('Ожидаются настройки IDE')
    result=deepcopy(DEFAULT_WORKFLOW)
    result['enabled']=params.get('enabled') is True
    result['mode']=params.get('mode','pipeline')
    if result['mode'] not in ('pipeline',*ROLES):raise ValueError('Неизвестный режим IDE')
    for key,low,high in (('context_length',2048,32768),('repair_passes',0,2)):
        value=params.get(key,result[key])
        if isinstance(value,bool) or not isinstance(value,int) or not low<=value<=high:raise ValueError(f'{key}: от {low} до {high}')
        result[key]=value
    roles=params.get('roles',{})
    if not isinstance(roles,dict):raise ValueError('Некорректные роли IDE')
    for role in ROLES:
        supplied=roles.get(role,{})
        if not isinstance(supplied,dict):raise ValueError('Некорректная роль '+role)
        model=supplied.get('model','');base=supplied.get('base_url','')
        if not isinstance(model,str) or len(model)>300 or '\0' in model:raise ValueError('Некорректный ID модели')
        if not isinstance(base,str) or len(base)>2000:raise ValueError('Некорректный адрес роли')
        validated=validate_preferences({'base_url':base.strip() or 'http://127.0.0.1:1234/v1','tool_protocol':supplied.get('tool_protocol','native')})
        provider=supplied.get('provider','lmstudio')
        if provider not in ('lmstudio','ollama','external'):raise ValueError('Неизвестный сервер роли')
        result['roles'][role]={'base_url':validated['base_url'] if base.strip() else '', 'model':model.strip(),
            'provider':provider,'tool_protocol':validated['tool_protocol']}
    return result


def load_workflow():
    try:return validate_workflow(json.loads(WORKFLOW_FILE.read_text('utf8')))
    except (OSError,ValueError,TypeError):return deepcopy(DEFAULT_WORKFLOW)


def save_workflow(params):
    result=validate_workflow(params);_atomic_write(WORKFLOW_FILE,result);return result


def resolve_roles(workflow, primary, secrets=None):
    result={}
    for role in ROLES:
        config=workflow['roles'][role]
        base=config['base_url'] or primary['base_url']
        # A main-server token is never sent to a different endpoint implicitly.
        secret=(secrets or {}).get(role,primary.get('api_key','') if base==primary['base_url'] else '')
        result[role]={**primary,**config,'base_url':base,'model':config['model'] or primary['model'],'api_key':secret}
    required=ROLES if workflow['mode']=='pipeline' else (workflow['mode'],)
    if any(not result[role]['model'] for role in required):raise ValueError('Выберите модель для каждой используемой роли IDE')
    return result
