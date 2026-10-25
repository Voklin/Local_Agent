"""On-demand MCP connections. Each operation owns and closes its transport."""
from __future__ import annotations
import asyncio
import json
import os
import re
import threading
from pathlib import Path
from urllib.parse import urlparse


def validate_server(value):
    """Only settings entered by a person can define executable commands/endpoints."""
    if not isinstance(value, dict):raise ValueError('Ожидаются настройки MCP сервера')
    identity=str(value.get('id','')).strip()
    if not re.fullmatch(r'[a-z0-9][a-z0-9_-]{0,39}',identity):raise ValueError('ID сервера: латинские буквы, цифры, _ и -, до 40 символов')
    transport=value.get('transport','stdio')
    if transport not in ('stdio','http'):raise ValueError('Поддерживается stdio или HTTP')
    result={'id':identity,'name':str(value.get('name') or identity)[:100], 'transport':transport,
            'enabled':value.get('enabled') is True,'confirm':value.get('confirm',True) is not False,
            'timeout':max(5,min(120,int(value.get('timeout',30))))}
    if transport=='http':
        url=str(value.get('url','')).strip();parsed=urlparse(url)
        if parsed.scheme not in ('http','https') or not parsed.hostname or parsed.username or parsed.password or parsed.fragment or parsed.query:raise ValueError('Укажите HTTP(S) адрес MCP без пароля и параметров')
        result['url']=url[:2000]
    else:
        command=str(value.get('command','')).strip()
        args=value.get('args',[])
        if not command or len(command)>2000 or not isinstance(args,list) or len(args)>50 or any(not isinstance(a,str) or len(a)>4000 for a in args):raise ValueError('Укажите команду запуска и список аргументов')
        result.update(command=command,args=args)
    return result


class MCPClient:
    def __init__(self, log_dir):
        self.log_dir=Path(log_dir)

    def operation(self, server, name=None, arguments=None, interrupted=None, token=''):
        """Bound cancellation and time; SDK exceptions never expose credentials."""
        try:return asyncio.run(self._operate(server,name,arguments,interrupted or threading.Event(),token))
        except Exception as exc:return {'ok':False,'error':'MCP: '+type(exc).__name__+'. Проверьте сервер, команду запуска и журнал.'}

    async def _operate(self, server, name, arguments, interrupted, token):
        from contextlib import AsyncExitStack
        from mcp import Client, StdioServerParameters
        from mcp.client.stdio import stdio_client
        from mcp.client.streamable_http import streamable_http_client
        async def exchange():
            async with AsyncExitStack() as stack:
                if server['transport']=='stdio':
                    self.log_dir.mkdir(parents=True,exist_ok=True)
                    log_path=self.log_dir/(server['id']+'.log')
                    if log_path.exists() and log_path.stat().st_size>1_000_000:log_path.write_text('',encoding='utf-8')
                    err=stack.enter_context(log_path.open('a',encoding='utf-8'))
                    transport=stdio_client(StdioServerParameters(command=server['command'],args=server['args']),errlog=err)
                else:
                    import httpx2
                    http=await stack.enter_async_context(httpx2.AsyncClient(headers={'Authorization':'Bearer '+token} if token else {},timeout=server['timeout'],follow_redirects=False))
                    transport=streamable_http_client(server['url'],http_client=http,max_sse_event_size=1_000_000)
                async with Client(transport,read_timeout_seconds=server['timeout']) as client:
                    if name is not None:
                        result=await client.call_tool(name,arguments or {})
                        data=result.model_dump(mode='json',by_alias=True)
                        # Images/audio remain metadata: never return unbounded base64 to a model.
                        content=[]
                        for item in data.get('content',[])[:30]:
                            if item.get('type')=='text':content.append({'type':'text','text':str(item.get('text',''))[:16000]})
                            else:content.append({'type':item.get('type'),'note':'Нетекстовое вложение MCP'})
                        return {'ok':not bool(data.get('isError',data.get('is_error',False))),'content':content,'untrusted':True}
                    tools=[];cursor=None
                    for _ in range(5):
                        page=(await client.list_tools(cursor=cursor)).model_dump(mode='json',by_alias=True)
                        for tool in page.get('tools',[]):
                            schema=tool.get('inputSchema',tool.get('input_schema',{}))
                            if len(json.dumps(schema))>30000:continue
                            tools.append({'name':str(tool['name'])[:200],'description':str(tool.get('description',''))[:1500],'parameters':schema})
                            if len(tools)>=100:break
                        cursor=page.get('nextCursor') or page.get('next_cursor')
                        if not cursor or len(tools)>=100:break
                    return {'ok':True,'tools':tools[:100]}
        operation=asyncio.create_task(exchange())
        try:
            async with asyncio.timeout(server['timeout']):
                while not operation.done():
                    if interrupted.is_set():raise asyncio.CancelledError()
                    await asyncio.sleep(.05)
                return await operation
        except asyncio.CancelledError:return {'ok':False,'error':'MCP: остановлено пользователем'}
        finally:
            operation.cancel()
            await asyncio.gather(operation,return_exceptions=True)
