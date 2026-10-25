import { GenerationFields, defaultGeneration } from './GenerationFields';
import { useEffect, useState } from 'react';

export function CompanionSettings({profile,busy,onSaved}:{profile:any;busy:boolean;onSaved:(profile:any)=>void}) {
  const [draft,setDraft]=useState({...profile});
  const [notice,setNotice]=useState('');
  const [working,setWorking]=useState(false);
  const [models,setModels]=useState<string[]>([]);
  useEffect(()=>{setDraft({...profile});},[profile.tts_provider]);
  async function save() {
    setWorking(true);setNotice('');
    try {
      const result=await window.lca.configureCompanion({...draft,voice:profile.voice,rate:profile.rate,volume:profile.volume,auto_speak:profile.auto_speak});
      if(!result.ok)throw Error(result.error);
      onSaved(result);setDraft(result);window.dispatchEvent(new Event('companion-profile'));setNotice('Профиль Лолы сохранён. Ключи остаются только в памяти.');
    }catch(error){setNotice(String(error));}finally{setWorking(false);}
  }
  async function discover() {
    setWorking(true);setNotice('');
    try{const result=await window.lca.listModels(draft);if(!result.ok)throw Error(result.error);setModels(result.models);}
    catch(error){setNotice(String(error));}finally{setWorking(false);}
  }
  return <details className="settings-section companion-settings"><summary>Характер, отдельная модель и распознавание</summary>
    <details><summary>Что умеет Лола</summary><p className="settings-help">«Посчитай 125 × 8», «Запомни заметку…», «Поставь таймер на 5 минут», «Покажи таймеры», «Который час?». Таймеры работают, пока Neutral открыт. Для «Найди музыку…», открытия трека и локального аудио включите инструменты ПК в общих настройках. Папку музыки указывайте полным путём в кавычках. Браузер может потребовать нажать Play.</p></details>
    <label>Характер Лолы<textarea maxLength={6000} value={draft.persona||''} disabled={busy||working} onChange={e=>setDraft({...draft,persona:e.target.value})}/></label>
    <label>Тип API Лолы<select aria-label="Тип API Лолы" value={draft.api_protocol||'chat'} disabled={busy||working} onChange={e=>setDraft({...draft,api_protocol:e.target.value,...(e.target.value==='responses'&&draft.base_url!=='https://api.openai.com/v1'?{base_url:'https://api.openai.com/v1',api_key:''}:{})})}><option value="chat">Совместимый сервер · LM Studio / Ollama</option><option value="responses">OpenAI · Responses API</option></select></label>
    <label>API отдельной модели<input value={draft.base_url||''} disabled={busy||working} onChange={e=>setDraft({...draft,base_url:e.target.value,api_key:''})}/></label>
    <label>Модель Лолы<input list="companion-models" value={draft.model||''} disabled={busy||working} onChange={e=>setDraft({...draft,model:e.target.value})}/><datalist id="companion-models">{models.map(model=><option key={model}>{model}</option>)}</datalist></label>
    <button className="secondary-button" disabled={busy||working} onClick={()=>void discover()}>Загрузить модели Лолы</button>
    <label>API-ключ модели<input type="password" autoComplete="off" value={draft.api_key||''} onChange={e=>setDraft({...draft,api_key:e.target.value})}/></label>
    <details><summary>Генерация модели Лолы</summary><GenerationFields value={{...defaultGeneration,...draft.settings}} locked={busy||working} onChange={settings=>setDraft({...draft,settings})}/></details>
    <label>Tool calling<select value={draft.tool_protocol||'native'} onChange={e=>setDraft({...draft,tool_protocol:e.target.value})}><option value="native">Native</option><option value="json">JSON</option></select></label>
    <label className="auto-speak"><input type="checkbox" checked={draft.auto_delegate!==false} onChange={e=>setDraft({...draft,auto_delegate:e.target.checked})}/>Автоматически передавать задачи программирования основной модели</label>
    <details><summary>Дополнительные параметры озвучки</summary>
    {draft.tts_provider!=='windows'&&<label>Адрес сервера озвучки<input value={draft.tts_url||''} onChange={e=>setDraft({...draft,tts_url:e.target.value})}/></label>}
    {draft.tts_provider==='qwen3'&&<>
      <label>Тембр и манера речи<textarea maxLength={1500} value={draft.tts_style||''} onChange={e=>setDraft({...draft,tts_style:e.target.value})}/></label>
      <p className="settings-help">Qwen3-TTS VoiceDesign создаёт русский голос по описанию. Для локального сервера откройте папку и запустите start-tts.ps1. Первый запуск скачает зависимости и модель — несколько ГБ; нужен Python 3.12. На CPU синтез может быть медленным. Качество и постоянство тембра зависят от модели.</p>
      <button type="button" className="secondary-button" onClick={()=>void window.lca.openTtsFolder()}>Открыть папку установки TTS</button>
    </>}
    {draft.tts_provider==='piper'&&<><p className="settings-help">Serena — обученный голос Лолы. Работает на процессоре, видеопамять не занимает. Если модель отсутствует, выберите её ONNX-файл; соответствующий JSON должен находиться рядом.</p><button type="button" className="secondary-button" onClick={()=>void window.lca.speechRuntime('install').then(result=>setNotice(result.ok?'Голос установлен':result.error))}>Указать файлы Serena</button><button type="button" className="secondary-button" onClick={()=>void window.lca.openTtsFolder()}>Открыть папку компонентов</button></>}
    </details>
    <label>Фраза активации<input maxLength={80} value={draft.wake_phrase||''} onChange={e=>setDraft({...draft,wake_phrase:e.target.value})}/></label>
    <label className="auto-speak"><input type="checkbox" checked={draft.wake_auto_send===true} onChange={e=>setDraft({...draft,wake_auto_send:e.target.checked})}/>Отправлять голосовую команду сразу после фразы</label>
    <p className="settings-help">Сохраните профиль и включите «Активация голосом» в верхней панели. Микрофон слушает во всех режимах, пока приложение открыто. Распознавание использует STT URL ниже; передаются только фрагменты с обнаруженной речью. Скажите фразу и команду либо произнесите команду следующим фрагментом.</p>
    <label>STT URL<input value={draft.stt_url||''} onChange={e=>setDraft({...draft,stt_url:e.target.value})}/><small>whisper.cpp: http://127.0.0.1:8080/inference; OpenAI-совместимый сервер: полный URL /v1/audio/transcriptions.</small></label>
    <label>STT модель<input value={draft.stt_model||''} onChange={e=>setDraft({...draft,stt_model:e.target.value})}/></label>
    <label>Язык STT<input maxLength={16} value={draft.stt_language||''} onChange={e=>setDraft({...draft,stt_language:e.target.value})}/></label>
    <label>STT API-ключ<input type="password" autoComplete="off" value={draft.stt_api_key||''} onChange={e=>setDraft({...draft,stt_api_key:e.target.value})}/></label>
    <button className="primary-button" disabled={busy||working} onClick={()=>void save()}>Сохранить профиль Лолы</button><p role="status">{notice}</p>
  </details>;
}
