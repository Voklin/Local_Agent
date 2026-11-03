"""Declarative readonly subagent profiles; instructions never grant capabilities."""
from copy import deepcopy
import json
import re
import threading
import uuid
from .chat_store import _atomic_write

READS = frozenset({'list_files', 'read_file', 'read_range'})
DEFAULT = {'id':'research', 'title':'Исследователь', 'summary':'Изучить выбранные файлы и вернуть факты с источниками.',
           'instructions':'Прочитай относящиеся к задаче файлы. Отделяй факты от предположений, указывай пути и строки.',
           'tools':sorted(READS), 'enabled':True, 'source':'builtin', 'version':1}
CREATE_TOOL = {'type':'function','function':{'name':'create_subagent_profile',
    'description':'Создать профиль субагента (subagent) как выключенный черновик исследователя. Пользователь просмотрит и включит его в настройках. Не сохраняй секреты. Не запускает ребёнка.',
    'parameters':{'type':'object','properties':{'title':{'type':'string','minLength':1,'maxLength':80},
      'summary':{'type':'string','minLength':1,'maxLength':300}, 'instructions':{'type':'string','minLength':10,'maxLength':4000},
      'tools':{'type':'array','items':{'type':'string','enum':sorted(READS)},'minItems':1,'maxItems':3,'uniqueItems':True}},
      'required':['title','summary','instructions','tools'],'additionalProperties':False}}}


class SubagentProfiles:
    """Atomic versioned catalog shared with extension settings, never a second executor."""
    def __init__(self, directory):
        self.path=directory/'subagents.json'; self.lock=threading.RLock()

    def load(self):
        """Fail closed on damaged catalogs instead of silently re-enabling defaults."""
        if not self.path.exists():return {'version':1,'enabled':True,'profiles':[deepcopy(DEFAULT)]}
        if self.path.stat().st_size>1_000_000:raise ValueError('Каталог субагентов слишком велик')
        value=json.loads(self.path.read_text(encoding='utf8'))
        if not isinstance(value,dict) or value.get('version')!=1 or type(value.get('enabled')) is not bool or not isinstance(value.get('profiles'),list) or len(value['profiles'])>50:
            raise ValueError('Повреждён каталог субагентов; восстановите его из резервной копии')
        ids=set()
        for item in value['profiles']:
            self.validate(item)
            if item['id'] in ids:raise ValueError('Повторяющийся профиль субагента')
            ids.add(item['id'])
        return value

    @staticmethod
    def validate(item):
        """Accept only bounded text and the three existing readonly file tools."""
        if not isinstance(item,dict) or not re.fullmatch(r'(research|user_[a-f0-9]{32})',str(item.get('id',''))):raise ValueError('Неверный ID субагента')
        if set(item)-{'id','title','summary','instructions','tools','enabled','source','version'}:raise ValueError('Профиль не может задавать модель, MCP или дополнительные права')
        for key,lo,hi in [('title',1,80),('summary',1,300),('instructions',10,4000)]:
            if not isinstance(item.get(key),str) or not lo<=len(item[key].strip())<=hi:raise ValueError('Заполните название, назначение и инструкцию субагента')
        tools=item.get('tools')
        if not isinstance(tools,list) or not tools or any(not isinstance(t,str) or t not in READS for t in tools) or len(set(tools))!=len(tools):raise ValueError('Доступны только инструменты чтения файлов')
        if type(item.get('enabled')) is not bool or item.get('source') not in ('builtin','user','model') or type(item.get('version')) is not int or item['version']<1:raise ValueError('Неверная версия профиля')

    def catalog(self):
        """Return independent data so UI/model consumers cannot mutate stored state."""
        with self.lock:return deepcopy(self.load())

    def configure(self, params, generated=False):
        """Model creation is append-only and disabled; trusted user CRUD is explicit."""
        with self.lock:
            state=self.load(); kind=params.get('kind','subagent_save')
            if kind=='subagents_toggle' and not generated:
                if type(params.get('enabled')) is not bool:raise ValueError('Укажите включить или выключить')
                state['enabled']=params['enabled']
            elif kind=='subagent_delete' and not generated:
                if params.get('id')=='research':raise ValueError('Встроенный профиль можно выключить')
                state['profiles']=[p for p in state['profiles'] if p['id']!=params.get('id')]
            else:
                if kind!='subagent_save':raise ValueError('Неизвестное действие субагента')
                if generated and (not state['enabled'] or set(params)-{'kind','title','summary','instructions','tools'}):raise ValueError('Модель может только предложить новый выключенный профиль')
                identity=params.get('id') or 'user_'+uuid.uuid4().hex
                old=next((p for p in state['profiles'] if p['id']==identity),None)
                if generated and old:raise ValueError('Модель не может менять существующий профиль')
                item={k:deepcopy(params.get(k)) for k in ('title','summary','instructions','tools')}
                item.update(id=identity,enabled=False if generated else params.get('enabled',False),
                            source='model' if generated else (old['source'] if old else 'user'),version=(old['version']+1 if old else 1))
                self.validate(item)
                if not old and len(state['profiles'])>=50:raise ValueError('Сохранено 50 профилей; удалите неиспользуемые')
                state['profiles']=[p for p in state['profiles'] if p['id']!=identity]+[item]
            _atomic_write(self.path,state)
            return deepcopy(item) if kind=='subagent_save' else deepcopy(state)

    def resolve(self, identity):
        """Check current enablement immediately before starting a child."""
        state=self.catalog()
        item=next((p for p in state['profiles'] if p['id']==identity),None)
        if not state['enabled'] or not item or not item['enabled']:raise ValueError('Профиль субагента выключен или удалён')
        return item
