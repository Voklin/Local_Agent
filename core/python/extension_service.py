"""Declarative capabilities, progressive skills and user-configured MCP servers."""
from __future__ import annotations
from copy import deepcopy
import hashlib
import json
import re
import threading
import uuid
from pathlib import Path
from agent.chat_store import APP_DIR, _atomic_write
from agent.skills import SkillManager
from agent.mcp_client import MCPClient, validate_server
from agent.project_command import COMMAND_TOOL

GROUPS=[{'id':'memory','name':'Память проекта','description':'Решения, гипотезы и наблюдения с проверяемыми источниками; автоматический контекст IDE.'},{'id':'commands','name':'Проверки и команды проекта','description':'Тесты и сборки в IDE с отдельным подтверждением каждого запуска. Выполняют локальный код с вашими правами.'},{'id':'project','name':'Файлы проекта','description':'Просмотр, поиск и изменения с предварительным diff.'},
        {'id':'assistant','name':'Повседневные задачи','description':'Время, расчёты, заметки, таймеры и музыка.'},
        {'id':'desktop','name':'Компьютер и браузер','description':'Разрешённые приложения, поиск и снимки экрана.'},
        {'id':'skills','name':'Навыки и опыт','description':'Пошаговые инструкции, которые агент читает по необходимости.'}]

def function(name,description,properties,required=()):
    return {'type':'function','function':{'name':name,'description':description,'parameters':{'type':'object','properties':properties,'required':list(required),'additionalProperties':False}}}

SKILL_TOOLS=[function('skills_list','Список включённых навыков. Сначала найди подходящий, затем прочитай skill_view.',{}),
             function('skill_view','Прочитать полную инструкцию включённого навыка.',{'id':{'type':'string'}},['id']),
             function('create_skill','Сохранить полезный повторяемый опыт как черновик навыка. Пользователь включит его в настройках. Не сохраняй секреты или одноразовый ответ.',{'title':{'type':'string'},'summary':{'type':'string'},'content':{'type':'string'}},['title','summary','content'])]


def mcp_alias(server, name):
    """Provider-safe alias bound to the full server endpoint and original tool name."""
    identity={key:server.get(key) for key in ('id','transport','command','args','url')}
    digest=hashlib.sha256(json.dumps([identity,name],sort_keys=True,ensure_ascii=False).encode('utf8')).hexdigest()[:24]
    return 'mcp_'+server['id'][:20]+'_'+digest

class ExtensionService:
    def __init__(self,directory=None,bundled=None):
        self.directory=Path(directory) if directory else APP_DIR/'extensions'
        self.file=self.directory/'registry.json'
        from agent.subagent_profiles import SubagentProfiles
        self.subagents=SubagentProfiles(self.directory)
        self.user_dir=self.directory/'skills'
        self.bundled=SkillManager(bundled)
        self.lock=threading.RLock()
        self.tokens={}
        self.discoveries={}
        self.closed=False
        self.mcp=MCPClient(self.directory/'logs')
        self.state={'groups':{},'tools':{},'skills':{},'servers':[],'plugins':[],'learn':True}
        if self.file.exists() and self.file.stat().st_size<=2_000_000:
            try:
                data=json.loads(self.file.read_text(encoding='utf-8'))
                if isinstance(data,dict):self.state.update({k:v for k,v in data.items() if k in self.state})
            except (OSError,ValueError):pass
        self._migrate_aliases()

    def _migrate_aliases(self):
        """Project legacy aliases to endpoint identities, preserving every explicit denial."""
        renamed={}
        for server in self.state['servers']:
            seen=set()
            for tool in server.get('tools',[]):
                old=tool['id'];alias=mcp_alias(server,tool['name'])
                if alias in seen:raise ValueError('Сервер содержит повторяющееся имя инструмента MCP')
                seen.add(alias);tool['id']=alias
                if old!=alias:renamed.setdefault(old,set()).add(alias)
        for old,aliases in renamed.items():
            if old in self.state['tools']:
                for alias in aliases:
                    self.state['tools'][alias]=self.state['tools'].get(alias,True) and self.state['tools'][old]
                self.state['tools'].pop(old,None)
        for plugin in self.state['plugins']:
            plugin['tools']=list(dict.fromkeys(alias for old in plugin.get('tools',[]) for alias in sorted(renamed.get(old,{old}))))
        # Persist with the next normal save; merely opening settings does not write.

    def save(self):
        _atomic_write(self.file,self.state)

    def skills(self):
        records=[]
        for item in self.bundled.discover():
            records.append({**item,'source':'bundled','enabled':self.state['skills'].get(item['id'],True)})
        if self.user_dir.exists():
            for path in sorted(self.user_dir.glob('*.json'))[:200]:
                if path.stat().st_size>50000:continue
                try:
                    value=json.loads(path.read_text(encoding='utf-8'))
                    records.append({**value,'source':'agent' if value.get('generated') else 'user','enabled':self.state['skills'].get(value['id'],False)})
                except (ValueError,OSError,KeyError):continue
        return records

    def catalog(self):
        with self.lock:
            from agent.tools import TOOL_DEFINITIONS
            from agent.project_knowledge import TOOLS as MEMORY_TOOLS
            from agent.diagnostics_evidence import DIAGNOSTICS_TOOL
            from core.python.assistant_service import ASSISTANT_TOOLS
            from core.python.desktop_service import DESKTOP_TOOLS
            tools=[]
            for group,definitions in [('memory',MEMORY_TOOLS),('commands',[COMMAND_TOOL,DIAGNOSTICS_TOOL]),('project',TOOL_DEFINITIONS),('assistant',ASSISTANT_TOOLS),('desktop',DESKTOP_TOOLS),('skills',SKILL_TOOLS)]:
                for tool in definitions:
                    item=tool['function'];tools.append({'id':item['name'],'name':item['name'],'description':item.get('description',''),'group':group,'enabled':self.state['tools'].get(item['name'],True)})
            for server in self.state['servers']:
                for tool in server.get('tools',[]):tools.append({'id':tool['id'],'name':tool['name'],'description':tool['description'],'group':'mcp:'+server['id'],'enabled':self.state['tools'].get(tool['id'],True)})
            return {'ok':True,'groups':[{**g,'enabled':self.state['groups'].get(g['id'],g['id']!='commands')} for g in GROUPS],
                    'tools':tools,'skills':[{k:v for k,v in item.items() if k!='path'} for item in self.skills()],
                    'servers':[{**s,'has_token':bool(self.tokens.get(s['id']))} for s in self.state['servers']],
                    'subagents':self.subagents.catalog(),'plugins':self.state['plugins'],'learn':self.state['learn'],'mcp_sessions':self.mcp.pool.status()}

    def configure(self,params):
        with self.lock:
            kind=params.get('kind');identity=str(params.get('id',''))
            if kind in ('subagent_save','subagent_delete','subagents_toggle'):
                self.subagents.configure(params)
            elif kind in ('groups','tools','skills'):
                if type(params.get('enabled')) is not bool:raise ValueError('Укажите включить или выключить')
                allowed={x['id'] for x in self.catalog()[kind]}
                if identity not in allowed:raise ValueError('Расширение не найдено')
                self.state[kind][identity]=params['enabled']
            elif kind=='learn':
                if type(params.get('enabled')) is not bool:raise ValueError('Укажите включить или выключить')
                self.state['learn']=params['enabled']
            elif kind=='skill_read':
                skill=next((s for s in self.skills() if s['id']==identity),None)
                if not skill:raise ValueError('Навык не найден')
                return {'ok':True,'content':skill.get('content') or self.bundled.load(identity)}
            elif kind=='skill_save':self._save_skill(params,generated=False)
            elif kind=='skill_delete':
                if not re.fullmatch(r'user_[a-f0-9]{32}',identity):raise ValueError('Можно удалить только пользовательский навык')
                (self.user_dir/(identity+'.json')).unlink(missing_ok=True);self.state['skills'].pop(identity,None)
            elif kind=='close_sessions':
                self.mcp.pool.invalidate()
            elif kind=='server_save':
                server=validate_server(params.get('server'))
                self.mcp.pool.invalidate(server['id'])
                previous=next((s for s in self.state['servers'] if s['id']==server['id']),None)
                # Changing a command/URL invalidates the discovered capabilities.
                connection=('transport','command','args','url')
                if previous and all(previous.get(k)==server.get(k) for k in connection) and ('token' not in params or params['token']==self.tokens.get(server['id'],'')):server['tools']=previous.get('tools',[])
                elif previous:
                    self.tokens.pop(server['id'],None)
                    self.cancel_discovery(server['id'])
                self.state['servers']=[s for s in self.state['servers'] if s['id']!=server['id']]
                if len(self.state['servers'])>=20:raise ValueError('Максимум 20 MCP серверов')
                self.state['servers'].append(server)
                token=params.get('token')
                if isinstance(token,str):self.tokens[server['id']]=token[:4000]
            elif kind=='server_delete':
                self.mcp.pool.invalidate(identity)
                self.cancel_discovery(identity)
                self.state['servers']=[s for s in self.state['servers'] if s['id']!=identity];self.tokens.pop(identity,None)
            elif kind=='plugin_toggle':
                plugin=next((p for p in self.state['plugins'] if p['id']==identity),None)
                if not plugin:raise ValueError('Плагин не найден')
                plugin['enabled']=params.get('enabled') is True
                for skill_id in plugin.get('skills',[]):self.state['skills'][skill_id]=plugin['enabled']
                for server in self.state['servers']:
                    if server['id'] in plugin.get('servers',[]):
                        server['enabled']=plugin['enabled']
                        if not server['enabled']:self.mcp.pool.invalidate(server['id'])
                for name in plugin.get('tools',[]):self.state['tools'][name]=plugin['enabled']
            else:raise ValueError('Неизвестное действие расширений')
            self.save();return self.catalog()

    def _save_skill(self,params,generated=False):
        title=str(params.get('title','')).strip();summary=str(params.get('summary','')).strip();content=str(params.get('content','')).strip()
        if not 1<=len(title)<=100 or not 1<=len(summary)<=300 or not 10<=len(content)<=16000:raise ValueError('Навык: название до 100, описание до 300 и инструкция от 10 до 16000 символов')
        identity=str(params.get('id') or 'user_'+uuid.uuid4().hex)
        if not re.fullmatch(r'user_[a-f0-9]{32}',identity):raise ValueError('Встроенный навык нельзя перезаписать; создайте копию')
        path=self.user_dir/(identity+'.json')
        if generated and path.exists():raise ValueError('Модель может создавать только новый черновик')
        if not path.exists() and self.user_dir.exists() and len(list(self.user_dir.glob('*.json')))>=200:raise ValueError('Достигнут лимит 200 навыков')
        record={'id':identity,'title':title,'summary':summary,'content':content,'generated':generated}
        _atomic_write(path,record)
        if identity not in self.state['skills']:self.state['skills'][identity]=False
        return record

    def import_plugin(self,manifest):
        with self.lock:
            if not isinstance(manifest,dict) or manifest.get('version')!=1:raise ValueError('Ожидается JSON манифест плагина версии 1')
            if len(json.dumps(manifest))>200000:raise ValueError('Манифест слишком большой')
            name=str(manifest.get('name','')).strip()
            if not 1<=len(name)<=100:raise ValueError('Укажите название плагина')
            if len(self.state['plugins'])>=40:raise ValueError('Максимум 40 плагинов')
            skills=manifest.get('skills',[]);servers=manifest.get('servers',[]);tools=manifest.get('tools',[])
            if not all(isinstance(x,list) for x in (skills,servers,tools)) or len(skills)>10 or len(servers)>5:raise ValueError('Проверьте списки навыков и серверов')
            known={t['id'] for t in self.catalog()['tools']}
            if any(t not in known for t in tools):raise ValueError('Плагин ссылается на неизвестный инструмент')
            validated=[validate_server({**s,'enabled':False}) for s in servers]
            existing={s['id'] for s in self.state['servers']}
            if len(self.state['servers'])+len(validated)>20 or len({s['id'] for s in validated})!=len(validated) or any(s['id'] in existing for s in validated):raise ValueError('ID серверов должны быть уникальны; максимум 20 серверов')
            # Validate all skills before writing any part of the package.
            for skill in skills:
                if not isinstance(skill,dict) or not 1<=len(str(skill.get('title','')).strip())<=100 or not 1<=len(str(skill.get('summary','')).strip())<=300 or not 10<=len(str(skill.get('content','')).strip())<=16000:raise ValueError('Неполное описание навыка в плагине')
            if len(self.skills())+len(skills)>200:raise ValueError('Достигнут лимит навыков')
            created=[self._save_skill({k:v for k,v in s.items() if k!='id'})['id'] for s in skills]
            plugin={'id':'plugin_'+uuid.uuid4().hex,'name':name,'description':str(manifest.get('description',''))[:500],'skills':created,'servers':[s['id'] for s in validated],'tools':tools,'enabled':False}
            self.state['servers'].extend(validated);self.state['plugins'].append(plugin);self.save()
            return self.catalog()

    def _reserve_discovery(self,identity):
        with self.lock:
            if self.closed:raise ValueError('Проверки MCP завершаются вместе с приложением')
            if identity in self.discoveries:raise ValueError('Проверка этого MCP сервера уже выполняется')
            server=next((deepcopy(s) for s in self.state['servers'] if s['id']==identity),None)
            if not server:raise ValueError('MCP сервер не найден')
            token=self.tokens.get(identity,'')
            record={'cancel':threading.Event(),'thread':None}
            self.discoveries[identity]=record
            return server,token,record

    def _release_discovery(self,identity,record):
        with self.lock:
            if self.discoveries.get(identity) is record:self.discoveries.pop(identity,None)

    def discover_server(self,identity):
        server,token,record=self._reserve_discovery(identity)
        try:return self._discover_server(server,token,record['cancel'])
        finally:self._release_discovery(identity,record)

    def start_discovery(self,identity,respond):
        """Reserve before spawning so repeated requests never create another worker."""
        server,token,record=self._reserve_discovery(identity)
        def run_discovery():
            try:
                try:result=self._discover_server(server,token,record['cancel'])
                except Exception as exc:result={'ok':False,'error':str(exc)[:300]}
            finally:self._release_discovery(identity,record)
            respond(result)
        worker=threading.Thread(target=run_discovery,daemon=True,name='mcp-discover-'+identity)
        try:
            with self.lock:
                if self.closed:raise ValueError('Приложение завершает проверки MCP')
                record['thread']=worker
                worker.start()
        except Exception:
            self._release_discovery(identity,record)
            raise

    def cancel_discovery(self,identity=None):
        with self.lock:
            records=[self.discoveries[identity]] if identity in self.discoveries else []
            if identity is None:records=list(self.discoveries.values())
            for record in records:record['cancel'].set()
        return {'ok':True,'cancelled':len(records)}

    def shutdown(self):
        self.mcp.shutdown()
        with self.lock:
            self.closed=True
            records=list(self.discoveries.values())
            for record in records:record['cancel'].set()
        for record in records:
            worker=record['thread']
            if worker and worker is not threading.current_thread():worker.join(timeout=2)

    def _discover_server(self,server,token,cancelled):
        identity=server['id']
        result=self.mcp.operation(server,token=token,interrupted=cancelled)
        if cancelled.is_set():return {'ok':False,'canceled':True,'error':'Проверка MCP отменена'}
        if not result['ok']:return result
        tools=[];seen=set()
        for tool in result['tools']:
            alias=mcp_alias(server,tool['name'])
            if alias in seen:raise ValueError('Сервер вернул повторяющееся имя инструмента MCP')
            seen.add(alias)
            tools.append({**tool,'id':alias})
        with self.lock:
            if cancelled.is_set():return {'ok':False,'canceled':True,'error':'Проверка MCP отменена'}
            current=next((s for s in self.state['servers'] if s['id']==identity),None)
            if not current or any(current.get(k)!=server.get(k) for k in ('transport','command','args','url')):raise ValueError('Настройки сервера изменились во время проверки')
            current['tools']=tools;self.save()
        return {'ok':True,'count':len(tools),'tools':tools}

    def snapshot(self,groups):
        """Freeze all permission choices for one run, independent of later GUI changes."""
        with self.lock:
            definitions=[]
            for group,items in groups:
                if self.state['groups'].get(group,group!='commands'):definitions.extend(t for t in items if self.state['tools'].get(t['function']['name'],True))
            skills=[s for s in self.skills() if s['enabled']] if self.state['groups'].get('skills',True) else []
            if self.state['groups'].get('skills',True):definitions.extend(t for t in SKILL_TOOLS if self.state['tools'].get(t['function']['name'],True) and (t['function']['name']!='create_skill' or self.state['learn']))
            external={}
            for server in self.state['servers']:
                if not server['enabled']:continue
                for tool in server.get('tools',[]):
                    if self.state['tools'].get(tool['id'],True):
                        if tool['id'] in external or any(t['function']['name']==tool['id'] for t in definitions):raise ValueError('Обнаружен конфликт инструментов MCP; повторите проверку сервера')
                        definitions.append({'type':'function','function':{'name':tool['id'],'description':'MCP '+server['name']+': '+tool['description'],'parameters':tool['parameters']}})
                        external[tool['id']]={'server':dict(server),'tool':tool,'token':self.tokens.get(server['id'],'')}
            allowed={t['function']['name'] for t in definitions}
            catalog='\n'.join(s['id']+': '+s['title']+' — '+s['summary'] for s in skills)[:12000]
            hint=('Доступные навыки (полный текст читай через skill_view):\n'+catalog if catalog else '')
            if 'create_skill' in allowed:hint+='\nПосле сложной успешно проверенной работы сохрани повторяемый метод через create_skill, если такого навыка ещё нет. Это только черновик: секреты, данные пользователя и разовые ответы в него не включай.'
            return {'definitions':definitions,'allowed':allowed,'skills':skills,'external':external,'hint':hint}

    def execute(self,snapshot,name,args,interrupted,approve):
        if name not in snapshot['allowed']:return {'ok':False,'error':'Инструмент выключен в настройках'}
        if name=='skills_list':return {'ok':True,'skills':[{k:s[k] for k in ('id','title','summary')} for s in snapshot['skills']]}
        if name=='skill_view':
            skill=next((s for s in snapshot['skills'] if s['id']==args.get('id')),None)
            if not skill:return {'ok':False,'error':'Навык не включён или не найден'}
            return {'ok':True,'content':skill.get('content') or self.bundled.load(skill['id']),'instructions_only':True}
        if name=='create_skill':
            with self.lock:
                skill=self._save_skill(args,generated=True);self.save()
            return {'ok':True,'id':skill['id'],'status':'draft','message':'Черновик навыка создан. Его можно просмотреть и включить в настройках → Расширения → Навыки.'}
        item=snapshot['external'].get(name)
        if item:
            from jsonschema import Draft202012Validator
            errors=list(Draft202012Validator(item['tool']['parameters']).iter_errors(args))
            if errors:return {'ok':False,'error':'Аргументы MCP не соответствуют схеме: '+errors[0].message[:300]}
            if item['server']['confirm'] and not approve(item['server']['name']+' / '+item['tool']['name'],json.dumps(args,ensure_ascii=False,indent=2)[:12000]):return {'ok':False,'error':'Вызов MCP отклонён пользователем'}
            return self.mcp.operation(item['server'],item['tool']['name'],args,interrupted,item['token'])
        return None
