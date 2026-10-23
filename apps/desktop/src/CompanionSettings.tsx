import { useState } from 'react';

export function CompanionSettings({profile,busy,onSaved}:{profile:any;busy:boolean;onSaved:(profile:any)=>void}) {
  const [draft,setDraft]=useState({...profile});
  const [notice,setNotice]=useState('');
  const [working,setWorking]=useState(false);
  const [models,setModels]=useState<string[]>([]);
  async function save() {
    setWorking(true);setNotice('');
    try {
      const result=await window.lca.configureCompanion({...draft,voice:profile.voice,rate:profile.rate,volume:profile.volume,auto_speak:profile.auto_speak});
      if(!result.ok)throw Error(result.error);
      onSaved(result);setDraft(result);setNotice('Профиль Мии сохранён. Ключи остаются только в памяти.');
    }catch(error){setNotice(String(error));}finally{setWorking(false);}
  }
  async function discover() {
    setWorking(true);setNotice('');
    try{const result=await window.lca.listModels(draft);if(!result.ok)throw Error(result.error);setModels(result.models);}
    catch(error){setNotice(String(error));}finally{setWorking(false);}
  }
  return <details className="settings-section companion-settings"><summary>Характер, отдельная модель и распознавание</summary>
    <label>Характер Мии<textarea maxLength={6000} value={draft.persona||''} disabled={busy||working} onChange={e=>setDraft({...draft,persona:e.target.value})}/></label>
    <label>API отдельной модели<input value={draft.base_url||''} disabled={busy||working} onChange={e=>setDraft({...draft,base_url:e.target.value})}/></label>
    <label>Модель Мии<input list="companion-models" value={draft.model||''} disabled={busy||working} onChange={e=>setDraft({...draft,model:e.target.value})}/><datalist id="companion-models">{models.map(model=><option key={model}>{model}</option>)}</datalist></label>
    <button className="secondary-button" disabled={busy||working} onClick={()=>void discover()}>Загрузить модели Мии</button>
    <label>API-ключ модели<input type="password" autoComplete="off" value={draft.api_key||''} onChange={e=>setDraft({...draft,api_key:e.target.value})}/></label>
    <details><summary>Генерация модели Мии</summary>{[
      {key:'temperature',label:'Temperature',min:0,max:2,step:0.05},
      {key:'top_p',label:'Top P',min:0.01,max:1,step:0.01},
      {key:'max_tokens',label:'Токены ответа',min:64,max:32768,step:1},
      {key:'max_context_chars',label:'Контекст, символов',min:12000,max:500000,step:1000},
      {key:'request_timeout',label:'HTTP ожидание, секунд',min:5,max:600,step:1},
      {key:'max_agent_turns',label:'Циклы агента',min:1,max:500,step:1},
      {key:'max_runtime_minutes',label:'Время задачи, минут',min:1,max:1440,step:1},
    ].map(field=><label key={field.key}>{field.label}<input type="number" min={field.min} max={field.max} step={field.step} value={draft.settings?.[field.key]??''} onChange={e=>setDraft({...draft,settings:{...draft.settings,[field.key]:Number(e.target.value)}})}/></label>)}</details>
    <label>Tool calling<select value={draft.tool_protocol||'native'} onChange={e=>setDraft({...draft,tool_protocol:e.target.value})}><option value="native">Native</option><option value="json">JSON</option></select></label>
    <label className="auto-speak"><input type="checkbox" checked={draft.auto_delegate!==false} onChange={e=>setDraft({...draft,auto_delegate:e.target.checked})}/>Автоматически передавать сложные задачи основной модели</label>
    <label>STT URL<input value={draft.stt_url||''} onChange={e=>setDraft({...draft,stt_url:e.target.value})}/><small>whisper.cpp: http://127.0.0.1:8080/inference; OpenAI-совместимый сервер: полный URL /v1/audio/transcriptions.</small></label>
    <label>STT модель<input value={draft.stt_model||''} onChange={e=>setDraft({...draft,stt_model:e.target.value})}/></label>
    <label>Язык STT<input maxLength={16} value={draft.stt_language||''} onChange={e=>setDraft({...draft,stt_language:e.target.value})}/></label>
    <label>STT API-ключ<input type="password" autoComplete="off" value={draft.stt_api_key||''} onChange={e=>setDraft({...draft,stt_api_key:e.target.value})}/></label>
    <button className="primary-button" disabled={busy||working} onClick={()=>void save()}>Сохранить профиль Мии</button><p role="status">{notice}</p>
  </details>;
}
