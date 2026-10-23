import { useEffect, useRef, useState } from 'react';

export function LocalRuntimePanel({locked,onUse}:{locked:boolean;onUse:(url:string,model:string)=>void}) {
  const [runtime,setRuntime]=useState('');
  const [model,setModel]=useState('');
  const [context,setContext]=useState(4096);
  const [gpu,setGpu]=useState(0);
  const [threads,setThreads]=useState(3);
  const [cacheK,setCacheK]=useState('f16');
  const [cacheV,setCacheV]=useState('f16');
  const [status,setStatus]=useState<any>({state:'stopped'});
  const [notice,setNotice]=useState('');
  const [working,setWorking]=useState(false);
  const alive=useRef(true);
  const initialized=useRef(false);
  useEffect(()=>{
    alive.current=true;
    async function refresh() {
      try {const result=await window.lca.runtimeStatus();if(alive.current&&result.ok){setStatus(result);if(!initialized.current){initialized.current=true;setCacheK(result.cache_type_k||'f16');setCacheV(result.cache_type_v||'f16');setContext(result.ctx_size||4096);setGpu(result.gpu_layers??0);setThreads(result.threads||3);}}}
      catch(error){if(alive.current)setNotice(String(error));}
    }
    void refresh();const timer=setInterval(()=>void refresh(),1000);
    return ()=>{alive.current=false;clearInterval(timer);};
  },[]);
  async function pick(kind:'model'|'runtime') {
    try {const result=await window.lca.pickRuntimeFile(kind);if(result.ok)(kind==='model'?setModel:setRuntime)(result.path);else if(!result.canceled)setNotice(result.error);}
    catch(error){setNotice(String(error));}
  }
  async function control(start:boolean) {
    setWorking(true);setNotice('');
    try {
      const result=start?await window.lca.startRuntime({ctx_size:context,gpu_layers:gpu,threads,cache_type_k:cacheK,cache_type_v:cacheV}):await window.lca.stopRuntime();
      if(!result.ok)throw new Error(result.error);
      setStatus(result);
    }catch(error){setNotice(String(error));}finally{setWorking(false);}
  }
  const active=['starting','running','stopping'].includes(status.state);
  const unavailable=locked||working;
  return <section className="settings-section local-runtime"><h3>GGUF внутри LocalAgent</h3>
    <p className="settings-help">CPU-сервер llama.cpp включён в установщик. Выберите файл GGUF. Приложение запустит отдельный сервер на localhost. Файлы не копируются; загрузки из сети нет. По умолчанию CPU, GPU-слои требуют подходящей сборки сервера.</p>
    <button type="button" className="secondary-button pick-runtime" disabled={unavailable||active} onClick={()=>void pick('runtime')}>Другой llama-server</button><small className="runtime-path">{runtime||status.bundled_runtime||'Сервер не выбран'}</small>
    <button type="button" className="secondary-button pick-gguf" disabled={unavailable||active} onClick={()=>void pick('model')}>Выбрать GGUF</button><small className="runtime-path">{model||status.model?.path||'Модель не выбрана'}</small>
    <div className="generation-grid"><label>Контекст сервера, токенов<input aria-label="Контекст GGUF" type="number" min={512} max={32768} value={context} disabled={unavailable||active} onChange={e=>setContext(Number(e.target.value))}/></label><label>GPU-слои (-1 = все, 0 = CPU)<input aria-label="GPU-слои GGUF" type="number" min={-1} max={256} value={gpu} disabled={unavailable||active} onChange={e=>setGpu(Number(e.target.value))}/></label></div>
    <label>Потоки CPU<input aria-label="Потоки CPU" type="number" min={1} max={128} disabled={unavailable||active} value={threads} onChange={e=>setThreads(Number(e.target.value))}/></label><div className="generation-grid">{(['K','V'] as const).map(kind=><label key={kind}>KV-кеш {kind}<select aria-label={`KV-кеш ${kind}`} disabled={unavailable||active} value={kind==='K'?cacheK:cacheV} onChange={e=>(kind==='K'?setCacheK:setCacheV)(e.target.value)}>{['f16','q8_0','q4_0'].map(value=><option key={value}>{value}</option>)}</select></label>)}</div><small>Квантование уменьшает память кеша. Для V-кеша включается Flash Attention; поддержка зависит от сборки сервера. Для внешнего LM Studio меняйте KV-кеш в самом LM Studio.</small>
    <div className="connection-actions"><button type="button" className="secondary-button start-runtime" disabled={unavailable||active||!(runtime||status.bundled_runtime)||!model} onClick={()=>void control(true)}>Запустить GGUF</button><button type="button" className="secondary-button stop-runtime" disabled={unavailable||!active||status.state==='stopping'} onClick={()=>void control(false)}>{status.state==='starting'?'Отменить загрузку':'Остановить свой сервер'}</button></div>
    <p className="runtime-status" role="status">{({stopped:'Остановлен',starting:'Загрузка модели…',running:'Готов',stopping:'Остановка…',error:'Ошибка'} as Record<string,string>)[status.state]}{status.pid?` · PID ${status.pid}`:''}{status.base_url?` · ${status.base_url}`:''}</p>
    {status.state==='running'&&<button type="button" className="secondary-button use-runtime" disabled={unavailable} onClick={()=>{onUse(status.base_url,status.model.name);setNotice('Адрес и модель перенесены в черновик. Проверьте ответ и сохраните настройки.');}}>Использовать в настройках</button>}
    {(notice||status.error)&&<p className="settings-notice" role="alert">{notice||status.error}</p>}
    {!!status.logs&&<details><summary>Последний вывод сервера</summary><pre className="runtime-logs">{status.logs}</pre></details>}
  </section>;
}
