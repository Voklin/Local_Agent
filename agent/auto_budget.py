"""Read-only loaded-model discovery and optional tokenizer; never load/unload a model."""
import asyncio
from copy import deepcopy
import hashlib
import ipaddress
import json
import re
import threading
import time
from urllib.parse import urlparse
import httpx

_CACHE={}
_LOCK=threading.Lock()
INITIAL_WINDOW=32768


def local_endpoint(url):
    """Automatic local task policy applies to loopback/private self-hosted servers."""
    host=urlparse(url).hostname or ''
    if host in ('localhost','localhost.localdomain') or host.endswith('.local'):return True
    try:return ipaddress.ip_address(host).is_private or ipaddress.ip_address(host).is_loopback
    except ValueError:return False


def valid_window(value):
    """Reject booleans, training-size guesses and implausible context metadata."""
    return value if type(value) is int and 512<=value<=1048576 else None


def loaded_profile(data,model,kind):
    """Use the selected loaded instance's context, never the model's trained maximum."""
    if not isinstance(data,dict):return None
    if kind=='lmstudio':
        if not isinstance(data.get('models'),list):return None
        for entry in data.get('models',[]):
            if not isinstance(entry,dict) or entry.get('type')!='llm':continue
            instances=entry.get('loaded_instances') or []
            matches=[i for i in instances if isinstance(i,dict) and (i.get('id')==model or entry.get('key')==model)]
            windows=[valid_window((i.get('config') or {}).get('context_length')) for i in matches]
            windows=[w for w in windows if w]
            if windows:return {'window':min(windows),'source':'LM Studio · загруженная модель','provider':kind,'instances':[i['id'] for i in matches if isinstance(i.get('id'),str)]}
        return {'provider':kind,'source':'LM Studio · окно уточняется после загрузки'}
    if kind=='lmstudio-v0':
        for entry in data.get('data',[]):
            if isinstance(entry,dict) and entry.get('id')==model and entry.get('state')=='loaded':
                window=valid_window(entry.get('loaded_context_length'))
                if window:return {'window':window,'provider':'lmstudio','source':'LM Studio · загруженная модель','instances':[model]}
    if kind=='ollama':
        for entry in data.get('models',[]):
            name=entry.get('name',entry.get('model','')) if isinstance(entry,dict) else ''
            if name.removesuffix(':latest')==model.removesuffix(':latest'):
                window=valid_window(entry.get('context_length'))
                if window:return {'window':window,'provider':kind,'source':'Ollama · загруженная модель'}
        if isinstance(data.get('models'),list):return {'provider':kind,'window':4096,'source':'Ollama · осторожный начальный профиль'}
    if kind=='llama.cpp':
        window=valid_window((data.get('default_generation_settings') or {}).get('n_ctx'))
        if window:return {'window':window,'provider':kind,'source':'llama.cpp · загруженный слот'}
    return None


async def discover_profile(base_url,model,api_key='',*,force=False):
    """Bounded cached metadata GETs on the configured local origin; no inference requests."""
    if not local_endpoint(base_url):return {'source':'Профиль подключения','provider':'remote'}
    parsed=urlparse(base_url);prefix=parsed.path.rstrip('/')
    if prefix.endswith('/v1'):prefix=prefix[:-3]
    origin=f'{parsed.scheme}://{parsed.netloc}'+prefix
    key=(origin,model,hashlib.sha256(api_key.encode()).hexdigest())
    with _LOCK:
        cached=_CACHE.get(key)
        if not force and cached and time.monotonic()-cached[0]<30:return deepcopy(cached[1])
    endpoints=[('lmstudio','/api/v1/models'),('lmstudio-v0','/api/v0/models'),('llama.cpp','/props'),('ollama','/api/ps')]
    async with httpx.AsyncClient(timeout=.6,follow_redirects=False,trust_env=False) as client:
        async def read(kind,path):
            """Read small metadata only and ignore unsupported provider endpoints."""
            try:
                async with client.stream('GET',origin+path,headers={'Authorization':'Bearer '+(api_key or 'no-key')}) as response:
                    if response.status_code!=200:return None
                    raw=bytearray()
                    async for chunk in response.aiter_bytes():
                        raw.extend(chunk)
                        if len(raw)>512000:return None
                return loaded_profile(json.loads(raw),model,kind)
            except (httpx.HTTPError,ValueError,TypeError,KeyError,AttributeError):return None
        try:values=await asyncio.wait_for(asyncio.gather(*(read(*endpoint) for endpoint in endpoints)),1)
        except asyncio.TimeoutError:values=[]
    result=next((v for v in values if v and v.get('window') and not v.get('source','').endswith('начальный профиль')),None)
    result=result or next((v for v in values if v),{'source':'Сервер не сообщил загруженное окно','provider':'unknown'})
    with _LOCK:
        if len(_CACHE)>64:_CACHE.clear()
        _CACHE[key]=(time.monotonic(),deepcopy(result))
    return result


def context_rejection(error):
    """Parse only explicit context-window labels from a rejected pre-stream request."""
    status=getattr(error,'status_code',0)
    if status not in (400,413,422):return None
    body=getattr(error,'body',None)
    if isinstance(body,dict):
        details=body.get('error',body)
        if isinstance(details,dict):
            for key in ('n_ctx','context_length','max_context_length'):
                if valid_window(details.get(key)):return details[key]
    text=str(error)[:6000]
    patterns=(r'(?:maximum|max) context (?:length|size)(?: is| of|:|=)*\s*(\d+)',
        r'(?:loaded with )?context (?:length|size)(?: of| is|:|=)*(?: only)?\s*(\d+)',
        r'(?:available context size)\s*\(?(\d+)',r'\bn_ctx\s*[=:]\s*(\d+)')
    for pattern in patterns:
        match=re.search(pattern,text,re.I)
        if match and valid_window(int(match.group(1))):return int(match.group(1))
    return None


class LoadedTokenizer:
    """Optional SDK handles obtained by list_loaded only; no implicit model() loading."""
    def __init__(self,client,model,cancelled):
        self.client,self.model,self.cancelled=client,model,cancelled

    @classmethod
    def connect(cls,base_url,instances,cancelled):
        """Use the SDK solely for tokenization of an already loaded anonymous local instance."""
        parsed=urlparse(base_url)
        if not instances or parsed.scheme!='http' or parsed.path.rstrip('/') not in ('','/v1'):return None
        try:import lmstudio
        except ImportError:return None
        client=None
        try:
            lmstudio.set_sync_api_timeout(.8)
            client=lmstudio.Client(api_host=parsed.netloc)
            for model in client.llm.list_loaded():
                if model.identifier in instances:return cls(client,model,cancelled)
        except Exception:pass
        if client:client.close()
        return None

    def count(self,text):
        """Count lexical request tokens on the local server, checking cancellation around the RPC."""
        if self.cancelled.is_set():raise InterruptedError('Остановлено пользователем')
        value=self.model.count_tokens(text)
        if self.cancelled.is_set():raise InterruptedError('Остановлено пользователем')
        if type(value) is not int or value<0:raise ValueError('Некорректный token count')
        return value

    def close(self):
        """Release SDK sockets/threads at the end of the existing model client lifetime."""
        self.client.close()
