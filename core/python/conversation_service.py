"""User-owned chat organization: pin/archive/delete/copy/export, with scope checks."""
from copy import deepcopy
import json
import uuid
from agent import chat_store
from agent.chat_store import STORE_LOCK, create_chat, load_chat, save_chat, read_chat_catalog
from agent.task_store import clear_task


class ConversationService:
    def __init__(self, tasks):
        self.tasks=tasks

    def scoped(self, root, params):
        chat=load_chat(params.get('chat_id'))
        mode=params.get('mode','chat')
        if not chat or chat.get('mode','ide' if chat.get('project_root') else 'chat')!=mode or chat.get('project_root','')!=str(root) or chat.get('project_id','')!=self.tasks.project_id:
            raise ValueError('Чат не принадлежит выбранному пространству')
        return chat

    def update(self, root, params):
        self.tasks.idle()
        with self.tasks.lock,STORE_LOCK:
            chat=self.scoped(root,params)
            for key in ('pinned','archived'):
                if key in params:
                    if type(params[key]) is not bool:raise ValueError('Некорректный флаг чата')
                    chat[key]=params[key]
            if 'project_id' in params:
                target=self.tasks.projects.get(params['project_id'])
                if chat.get('mode')=='ide' and target.get('root') and str(target['root'])!=chat.get('project_root'):
                    raise ValueError('Этот IDE-чат связан с другой папкой. Выберите проект с той же папкой или создайте копию разговора в Chat.')
                chat['project_id']=params['project_id']
            save_chat(chat)
            if self.tasks.chat and self.tasks.chat['id']==chat['id']:
                self.tasks.chat=chat if chat.get('project_id','')==self.tasks.project_id and not chat.get('archived') else None
        return {'ok':True}

    def delete(self, root, params):
        self.tasks.idle()
        with self.tasks.lock,STORE_LOCK:
            chat=self.scoped(root,params)
            if params.get('confirmed') is not True:raise ValueError('Подтвердите удаление выбранного чата')
            if not chat_store.delete_chat(chat['id']):raise ValueError('Не удалось удалить чат')
            clear_task(chat['id'])
            if self.tasks.chat and self.tasks.chat['id']==chat['id']:self.tasks.chat=None
        return {'ok':True}

    def fork(self, root, params):
        self.tasks.idle()
        with self.tasks.lock,STORE_LOCK:
            source=self.scoped(root,params);messages=deepcopy(source['messages']);prompt=''
            if params.get('retry'):
                indexes=[i for i,m in enumerate(messages) if m.get('role')=='user' and isinstance(m.get('content'),str)]
                if not indexes:raise ValueError('Нет запроса для повторения')
                index=indexes[-1];prompt=messages[index]['content'];messages=messages[:index]
            chat=create_chat(str(root),source.get('model',''),title=(source.get('title','Разговор')+' · копия')[:120],mode=source.get('mode','chat'))
            chat.update(messages=messages,project_id=self.tasks.project_id,source_chat_id=source['id'])
            save_chat(chat);self.tasks.chat=chat
            return {'ok':True,'chat':chat,'task':None,'prompt':prompt}

    def export(self, root, params):
        with STORE_LOCK:chat=self.scoped(root,params)
        kind=params.get('format','markdown')
        if kind not in ('markdown','json'):raise ValueError('Формат экспорта: Markdown или JSON')
        public={key:chat.get(key) for key in ('id','title','mode','project_id','project_root','created_at','messages')}
        if kind=='json':content=json.dumps(public,ensure_ascii=False,indent=2)
        else:
            rows=['# '+chat.get('title','Разговор')]
            for message in chat['messages']:
                if message.get('role') in ('user','assistant') and isinstance(message.get('content'),str):
                    rows.extend(['','## '+('Вы' if message['role']=='user' else 'Ассистент'),'',message['content']])
            content='\n'.join(rows)+'\n'
        if len(content.encode('utf8'))>10_000_000:raise ValueError('Разговор слишком велик для экспорта (10 МБ)')
        return {'ok':True,'content':content,'extension':'json' if kind=='json' else 'md'}

    def search(self, root, params):
        query=params.get('query','')
        if not isinstance(query,str) or len(query)>300:raise ValueError('Поиск: до 300 символов')
        archive=params.get('archived') is True;query=query.strip().casefold()
        base=self.tasks.chats(root,params.get('mode','chat'))
        matches=[]
        for item in base['chats'][:2000]:
            if bool(item.get('archived'))!=archive:continue
            if not query or query in item['title'].casefold():matches.append(item);continue
            try:chat=load_chat(item['id'])
            except (OSError,ValueError):continue
            if not chat:continue
            if not chat:continue
            text=next((m['content'] for m in chat['messages'] if m.get('role') in ('user','assistant') and isinstance(m.get('content'),str) and query in m['content'].casefold()),None)
            if text:
                index=text.casefold().find(query);matches.append({**item,'snippet':text[max(0,index-30):index+130]})
        matches.sort(key=lambda p:(bool(p.get('pinned')),p.get('updated_at','')),reverse=True)
        return {**base,'chats':matches[:300]}
