"""Bounded MCP actors: a transport's enter/use/exit always share one asyncio task."""
import asyncio
import hashlib
import json
import threading
from .operation_context import OperationContext


class MCPSessionPool:
    def __init__(self,connect,exchange,*,idle_seconds=45,max_sessions=4):
        self.connect,self.exchange=connect,exchange
        self.idle_seconds,self.max_sessions=idle_seconds,max_sessions
        self.lock=threading.RLock();self.loop=None;self.thread=None;self.actors={};self.closed=False

    def _start(self):
        with self.lock:
            if self.closed:raise ValueError('MCP manager закрыт')
            if self.loop is None:
                self.loop=asyncio.new_event_loop()
                self.thread=threading.Thread(target=self.loop.run_forever,daemon=True,name='mcp-session-manager')
                self.thread.start()

    def operation(self,server,name,args,cancelled,token):
        self._start()
        endpoint={key:server.get(key) for key in ('id','transport','command','args','url','timeout')}
        key=hashlib.sha256(json.dumps([endpoint,token],sort_keys=True,ensure_ascii=False).encode()).hexdigest()
        context=OperationContext(server['timeout'],cancelled)
        future=asyncio.run_coroutine_threadsafe(self._submit(key,server,name,args,context,token),self.loop)
        try:return future.result(timeout=server['timeout']+5)
        except Exception:
            context.set();future.cancel()
            return {'ok':False,'code':'OUTCOME_UNKNOWN' if name else 'MCP_ERROR','error':'MCP: время ожидания или соединение прервано; действие не повторялось.'}

    async def _submit(self,key,server,name,args,context,token):
        reply=self.loop.create_future()
        with self.lock:
            actor=self.actors.get(key)
            if actor is None:
                if len(self.actors)>=self.max_sessions:return {'ok':False,'code':'MCP_BUSY','error':'Все MCP-сессии заняты. Закройте соединения или дождитесь их освобождения.'}
                actor={'id':server['id'],'queue':asyncio.Queue(),'stop':threading.Event(),'calls':0,'current':reply}
                self.actors[key]=actor
                actor['task']=asyncio.create_task(self._actor(key,actor,server,token))
        await actor['queue'].put((name,args,context,reply))
        while not reply.done():
            if context.is_set() or actor['stop'].is_set():
                if actor.get('current') is reply or actor.get('current') is None:
                    actor['stop'].set();actor['task'].cancel()
                if not reply.done():reply.set_result(self._failure(name,asyncio.CancelledError()))
                break
            await asyncio.sleep(.025)
        return await reply

    async def _actor(self,key,actor,server,token):
        current=None
        try:
            async with self.connect(server,token) as client:
                while not actor['stop'].is_set():
                    try:current=await asyncio.wait_for(actor['queue'].get(),self.idle_seconds)
                    except asyncio.TimeoutError:break
                    if current is None:break
                    name,args,context,reply=current
                    if reply.done():continue
                    actor['current']=reply
                    if context.is_set():
                        reply.set_result(self._failure(name,asyncio.CancelledError()));continue
                    operation=asyncio.create_task(self.exchange(client,name,args))
                    try:
                        while not operation.done():
                            if context.is_set() or actor['stop'].is_set():raise asyncio.CancelledError()
                            await asyncio.sleep(.025)
                        result=await operation
                        actor['calls']+=1
                        if not reply.done():reply.set_result(result)
                    except BaseException as exc:
                        operation.cancel();await asyncio.gather(operation,return_exceptions=True)
                        if not reply.done():reply.set_result(self._failure(name,exc))
                        break  # Never reuse a transport with an uncertain in-flight request.
                    finally:current=None;actor['current']=None
        except BaseException as exc:
            if current and not current[3].done():current[3].set_result(self._failure(current[0],exc))
        finally:
            while not actor['queue'].empty():
                item=actor['queue'].get_nowait()
                if item and not item[3].done():item[3].set_result(self._failure(item[0],RuntimeError()))
            with self.lock:
                if self.actors.get(key) is actor:self.actors.pop(key,None)

    @staticmethod
    def _failure(name,error):
        return {'ok':False,'code':'OUTCOME_UNKNOWN' if name is not None else 'MCP_ERROR','error':'MCP: '+type(error).__name__+'. Соединение закрыто; автоматического повтора нет.'}

    def invalidate(self,identity=None):
        with self.lock:
            for actor in list(self.actors.values()):
                if identity is None or actor['id']==identity:
                    actor['stop'].set()
                    if self.loop:self.loop.call_soon_threadsafe(actor['queue'].put_nowait,None)

    def status(self):
        with self.lock:return {'active':len(self.actors),'limit':self.max_sessions,'idle_seconds':self.idle_seconds,
            'sessions':[{'id':a['id'],'calls':a['calls']} for a in self.actors.values()]}

    def shutdown(self):
        with self.lock:
            if self.closed:return
            self.closed=True
        self.invalidate()
        if self.loop:
            future=asyncio.run_coroutine_threadsafe(self._close(),self.loop)
            try:future.result(timeout=5)
            except Exception:pass
            self.loop.call_soon_threadsafe(self.loop.stop)
            self.thread.join(timeout=2)
            if not self.thread.is_alive():self.loop.close()

    async def _close(self):
        with self.lock:tasks=[a['task'] for a in self.actors.values()]
        if tasks:await asyncio.gather(*tasks,return_exceptions=True)
