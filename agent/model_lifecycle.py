"""Sequential, cancellable LM Studio/Ollama model lifecycle. No process killing."""
import asyncio
from urllib.parse import urlsplit, urlunsplit
import httpx
from .model_client import ModelCancelled


class ModelLifecycle:
    def __init__(self, roles, interrupted, context_length=4096, notify=None):
        self.roles=roles;self.interrupted=interrupted;self.context_length=context_length
        self.notify=notify or (lambda text:None);self.active=None

    @staticmethod
    def origin(config):
        url=urlsplit(config['base_url'])
        if url.path.rstrip('/') not in ('','/v1'):raise ValueError('Автозагрузка требует адрес сервера без префикса, например http://127.0.0.1:1234/v1')
        return urlunsplit((url.scheme,url.netloc,'','',''))

    def request(self, config, method, route, payload=None, cleanup=False):
        async def run():
            async def fetch():
                headers={'Authorization':'Bearer '+config['api_key']} if config.get('api_key') else {}
                async with httpx.AsyncClient(timeout=httpx.Timeout(20 if cleanup else 180,connect=5),trust_env=False,follow_redirects=False) as client:
                    async with client.stream(method,self.origin(config)+route,headers=headers,json=payload) as response:
                        if response.status_code>=400:
                            detail='Проверьте токен сервера.' if response.status_code in (401,403) else 'Нужен API управления LM Studio 0.4+ или совместимой Ollama.' if response.status_code==404 else 'Сервер не выполнил операцию. Проверьте его журнал, наличие и совместимость весов и свободную память.'
                            raise RuntimeError(f"{config['provider']}: HTTP {response.status_code}. {detail}")
                        raw=bytearray()
                        async for chunk in response.aiter_bytes():
                            raw.extend(chunk)
                            if len(raw)>2_000_000:raise ValueError('Слишком большой ответ сервера моделей')
                    import json
                    return json.loads(raw)
            worker=asyncio.create_task(fetch())
            try:
                while not worker.done():
                    if not cleanup and self.interrupted.is_set():raise ModelCancelled('Переключение модели отменено; проверьте незавершённую загрузку на сервере')
                    await asyncio.wait({worker},timeout=.05)
                return await worker
            finally:
                worker.cancel();await asyncio.gather(worker,return_exceptions=True)
        return asyncio.run(run())

    def catalog(self, config):
        if config['provider']=='lmstudio':
            data=self.request(config,'GET','/api/v1/models')
            return [{'id':item['key'],'loaded':[v['id'] for v in item.get('loaded_instances',[]) if isinstance(v.get('id'),str)]}
                for item in data.get('models',[]) if item.get('type')=='llm' and isinstance(item.get('key'),str)]
        if config['provider']=='ollama':
            tags=self.request(config,'GET','/api/tags');running=self.request(config,'GET','/api/ps')
            loaded={item.get('name') for item in running.get('models',[])}
            return [{'id':item['name'],'loaded':[item['name']] if item['name'] in loaded else []} for item in tags.get('models',[]) if isinstance(item.get('name'),str)]
        data=self.request(config,'GET','/v1/models')
        return [{'id':item['id'],'loaded':[]} for item in data.get('data',[]) if isinstance(item.get('id'),str)]

    def unload(self, config, instance, cleanup=False):
        self.notify('Выгрузка модели '+instance)
        if config['provider']=='lmstudio':
            result=self.request(config,'POST','/api/v1/models/unload',{'instance_id':instance},cleanup)
            if result.get('instance_id')!=instance:raise ValueError('Сервер не подтвердил выгрузку нужного instance_id')
        elif config['provider']=='ollama':
            result=self.request(config,'POST','/api/generate',{'model':instance,'keep_alive':0,'stream':False},cleanup)
            if result.get('done') is not True:raise ValueError('Ollama не подтвердила выгрузку')

    def release(self):
        if self.active:
            config,instance=self.active
            self.unload(config,instance,cleanup=True)
            self.active=None
            self.notify('Модель выгружена')

    def acquire(self, config):
        if self.interrupted.is_set():raise ModelCancelled('Остановлено пользователем')
        if self.active and all(self.active[0][key]==config[key] for key in ('base_url','model','provider','api_key')):return self.active[1]
        self.release()
        if config['provider']=='external':return config['model']
        catalog=self.catalog(config)
        selected={c['model'] for c in self.roles.values() if c['base_url']==config['base_url'] and c['provider']==config['provider']}
        if config['provider']=='ollama':
            selected|={name+':latest' for name in selected if ':' not in name}
        target=config['model']
        if config['provider']=='ollama' and ':' not in target:target+=':latest'
        found=next((item for item in catalog if item['id']==target),None)
        if not found:raise ValueError('Модель не найдена на сервере: '+target+'. Загрузите её веса и выберите точный ID из списка.')
        if any(item['loaded'] and item['id'] not in selected for item in catalog):
            raise ValueError('На сервере загружена модель вне ролей IDE. Выгрузите её вручную, чтобы освободить память перед циклом.')
        # Only explicitly configured role models may be evicted.
        for item in catalog:
            for instance in item['loaded']:
                if item['id'] in selected:self.unload(config,instance)
        self.notify('Загрузка модели '+target)
        if config['provider']=='lmstudio':
            result=self.request(config,'POST','/api/v1/models/load',{'model':target,'context_length':self.context_length,'eval_batch_size':128,'flash_attention':True,'offload_kv_cache_to_gpu':False})
            instance=result.get('instance_id')
            if not isinstance(instance,str) or not instance or result.get('status')!='loaded':raise ValueError('Сервер не подтвердил загрузку модели')
        else:
            self.active=(config,target)
            result=self.request(config,'POST','/api/generate',{'model':target,'stream':False,'keep_alive':'10m','options':{'num_ctx':self.context_length,'num_batch':128}})
            if result.get('done') is not True:raise ValueError('Ollama не подтвердила загрузку')
            instance=target
        self.active=(config,instance)
        self.notify('Модель готова: '+instance)
        return instance
