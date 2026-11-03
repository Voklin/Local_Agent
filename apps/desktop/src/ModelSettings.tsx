import {ResizeRail} from './StudioControls';
import { StorageSettings } from './StorageSettings';
import { ExtensionsSettings } from './ExtensionsSettings';
import { ConnectionProfiles } from './ConnectionProfiles';
import { VoiceSettings } from './VoiceSettings';
import { BrandMark } from './BrandMark';
import { AppearanceSettings } from './AppearanceSettings';
import { GenerationFields, generationFields as fields, defaultGeneration, type GenerationSettings } from './GenerationFields';
export { defaultGeneration, type GenerationSettings } from './GenerationFields';
import { ConnectionsSettings } from './ConnectionsSettings';
import { LocalRuntimePanel } from './LocalRuntimePanel';
import { useEffect, useRef, useState } from 'react';
import { CheckCircle2, Eye, EyeOff, RotateCcw, Server, X } from 'lucide-react';

export type ModelConfig = { api_protocol?:string; tool_protocol?: string; base_url: string; model: string; api_key: string; settings: GenerationSettings };
export function ModelSettings({ initial, busy, onSaved, onClose, onIde, initialSection='connection' }: {
  initial: ModelConfig; busy: boolean; onSaved: (config: ModelConfig) => void; onClose: () => void;onIde?:()=>void;initialSection?:string;
}) {
  const [draft, setDraft] = useState<ModelConfig>(() => ({...initial, settings:{...initial.settings}}));
  const [models, setModels] = useState<string[]>([]);
  const [visibleKey, setVisibleKey] = useState(false);
  const [operation, setOperation] = useState('');
  const [section,setSection]=useState(initialSection);
  const [query,setQuery]=useState('');
  const [notice, setNotice] = useState({kind:'info', text:'Сначала проверьте сервер и выберите модель. Проверки не сохраняют изменения.'});
  const dialog = useRef<HTMLElement>(null);
  const locked = busy || !!operation;
  useEffect(() => {
    const previous = document.activeElement as HTMLElement | null;
    dialog.current?.querySelector<HTMLInputElement>('input')?.focus();
    return () => previous?.focus();
  }, []);

  function change<K extends keyof ModelConfig>(key: K, value: ModelConfig[K]) {
    setDraft(current => ({...current, ...(key==='base_url'&&value!==current.base_url?{api_key:''}:{}), [key]:value}));
    if (key === 'base_url') setModels([]);
    setNotice({kind:'info', text:'Есть несохранённые изменения. Проверка и список моделей относятся к полям в этом окне.'});
  }
  function validate() {
    let url: URL;
    try { url = new URL(draft.base_url.trim()); }
    catch { throw new Error('Укажите полный адрес API, например http://127.0.0.1:1234/v1.'); }
    if (!['http:','https:'].includes(url.protocol) || !url.hostname || url.username || url.password || url.search || url.hash)
      throw new Error('Нужен HTTP(S) адрес API без ключа, пароля и параметров в URL.');
    for (const field of fields) {
      if(draft.settings.budget_mode!=='manual'&&!['temperature','top_p'].includes(field.key))continue;
      const value = draft.settings[field.key];
      if (!Number.isFinite(value) || value < field.min || value > field.max || (field.step === 1 && !Number.isInteger(value))) {
        setSection('generation');
        throw new Error(`${field.label}: ${field.step === 1 ? 'целое число' : 'число'} от ${field.min} до ${field.max}.`);
      }
    }
    if(draft.settings.budget_mode==='manual'&&draft.settings.max_tokens+draft.settings.context_reserve_tokens>=draft.settings.context_window){
      setSection('generation');throw new Error('Максимум ответа и запас должны быть меньше окна загруженной модели.');
    }
  }
  async function perform(action: 'discover' | 'probe' | 'save') {
    if (locked) return;
    setOperation(action);
    try {
      validate();
      if (action !== 'discover' && !draft.model.trim()) throw new Error('Выберите модель из списка или введите её ID.');
      if (action === 'discover') {
        const response = await window.lca.listModels(draft);
        if (!response.ok) throw new Error(response.error);
        setModels(response.models);
        if (!draft.model.trim() && response.models.length) change('model', response.models[0]);
        setNotice({kind:'success', text:response.models.length ? `Сервер доступен. Найдено моделей: ${response.models.length}. Список не означает, что модель уже загружена.` : 'Сервер доступен, но список пуст. Можно ввести ID модели вручную.'});
      } else if (action === 'probe') {
        const response = await window.lca.testModel(draft);
        if (!response.ok) throw new Error(response.error);
        setNotice({kind:'success', text:`Модель ответила за ${response.elapsed_ms} мс: ${response.text}`});
      } else {
        const response = await window.lca.configureModel(draft);
        if (!response.ok) throw new Error(response.error);
        const saved = {...draft, base_url:response.base_url, model:response.model, settings:response.settings};
        setDraft(saved); onSaved(saved);
        setNotice({kind:'success', text:'Настройки сохранены. Они применятся к следующему запросу. API-ключ остаётся только в памяти до закрытия приложения.'});
      }
    } catch (error) {
      setNotice({kind:'error', text:String(error instanceof Error ? error.message : error)});
    } finally { setOperation(''); }
  }
  function resetGeneration() {
    change('settings', {...defaultGeneration});
  }
  function handleKeys(event: React.KeyboardEvent<HTMLElement>) {
    if (event.key === 'Escape' && !operation) { event.preventDefault(); onClose(); }
    if (event.key !== 'Tab') return;
    const controls = dialog.current?.querySelectorAll<HTMLElement>('button:not(:disabled), input:not(:disabled), select:not(:disabled), [tabindex="0"]');
    if (!controls?.length) return;
    const first = controls[0], last = controls[controls.length - 1];
    if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
    else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
  }

  const filteredTabs=[{id:'connection',label:'Модели'},{id:'voice',label:'Голос и Лола'},{id:'extensions',label:'Расширения'},{id:'connections',label:'Компьютер и Telegram'},{id:'appearance',label:'Оформление'},{id:'generation',label:'Контекст и лимиты'},{id:'runtime',label:'Локальный запуск'},{id:'storage',label:'История и копии'},...(onIde?[{id:'ide',label:'Возможности IDE'}]:[])].filter(tab=>!window.neutralIdeHost||!['voice','connections'].includes(tab.id)).filter(tab=>tab.label.toLocaleLowerCase('ru').includes(query.toLocaleLowerCase('ru')));
  return <div className="modal-backdrop settings-backdrop">
    <section ref={dialog} className="settings-dialog" data-settings-section={section} role="dialog" aria-modal="true" aria-labelledby="model-settings-title" onKeyDown={handleKeys}>
      <header className="settings-header"><div><BrandMark size={27}/><div><h2 id="model-settings-title">Настройки Лешего</h2><p>Подключение, инструменты и рабочее пространство</p></div></div><button className="icon-button" title="Закрыть настройки" disabled={!!operation} onClick={onClose}><X size={20}/></button></header>
      <nav className="settings-tabs" aria-label="Разделы настроек"><ResizeRail name="settings"/><label className="studio-settings-search"><input value={query} aria-label="Поиск настроек" placeholder="Поиск настроек…" onChange={e=>setQuery(e.target.value)}/></label>{filteredTabs.map(tab=><button type="button" key={tab.id} aria-pressed={section===tab.id} disabled={!!operation} onClick={()=>tab.id==='ide'?onIde?.():setSection(tab.id)}>{tab.label}</button>)}{query&&!filteredTabs.length&&<p className="settings-help">Разделы не найдены</p>}</nav>
      <form className="model-settings" onSubmit={event => {event.preventDefault();if(['connection','generation'].includes(section))void perform('save');}} noValidate>
        <div className="settings-scroll">
          {busy&&<div className="settings-notice">Дождитесь завершения задачи, чтобы менять настройки.</div>}
          <section hidden={section!=='connection'} className="settings-section"><div className="section-intro"><span className="eyebrow">ПОДКЛЮЧЕНИЕ</span><h3>Подключение модели</h3><p>Локальный сервер или внешний API — выберите удобный способ.</p></div><ConnectionProfiles value={draft} locked={locked} onSelect={config=>{setDraft(config);setModels([]);}}/><h3><Server size={16}/>Сервер и модель</h3>
            <div className="endpoint-presets"><span>Быстрый адрес</span><button type="button" disabled={locked} onClick={()=>{change('base_url','http://127.0.0.1:1234/v1');change('api_protocol','chat');}}>LM Studio</button><button type="button" disabled={locked} onClick={()=>{change('base_url','http://127.0.0.1:11434/v1');change('api_protocol','chat');}}>Ollama</button><button type="button" disabled={locked} onClick={()=>{change('base_url','https://api.openai.com/v1');change('api_protocol','responses');change('tool_protocol','native');change('model','');}}>OpenAI API</button></div>
            <label>Тип API<select aria-label="Тип API" value={draft.api_protocol||'chat'} disabled={locked} onChange={e=>change('api_protocol',e.target.value)}><option value="chat">OpenAI-совместимый · LM Studio / Ollama</option><option value="responses">OpenAI · Responses API</option></select><small>{draft.api_protocol==='responses'?'Нужен ключ OpenAI API. Подписка ChatGPT не подключает API автоматически. Параметры случайности выбирает сервер; бюджет ответа задаётся в лимитах.':'Подходит для локальных и совместимых облачных серверов.'}</small></label>
            <label>Протокол инструментов<select aria-label="Протокол инструментов" value={draft.tool_protocol||'native'} disabled={locked} onChange={e=>change('tool_protocol',e.target.value)}><option value="native">Native tools API</option><option value="json">JSON в тексте · Qwen 2.5 Coder</option></select><small>JSON не требует нативной поддержки tools у модели. Вызовы выполняются через обычные проверки и подтверждения.</small></label>
            <label>URL сервера<input name="base_url" maxLength={2000} value={draft.base_url} disabled={locked} onChange={event=>change('base_url',event.target.value)} placeholder="http://127.0.0.1:1234/v1"/><small>Адрес OpenAI-совместимого API с /v1. Для внешнего сервера запустите его отдельно; GGUF можно запустить ниже.</small></label>
            <label>API-ключ <span className="field-optional">если требуется сервером</span><div className="key-input"><input name="api_key" maxLength={4000} type={visibleKey?'text':'password'} autoComplete="off" value={draft.api_key} disabled={locked} onChange={event=>change('api_key',event.target.value)}/><button type="button" className="icon-button" title={visibleKey?'Скрыть ключ':'Показать ключ'} onClick={()=>setVisibleKey(!visibleKey)}>{visibleKey?<EyeOff size={16}/>:<Eye size={16}/>}</button></div><small>Ключ не сохраняется на диск. Для локального сервера обычно не нужен.</small></label>
            <div className="connection-actions"><button type="button" className="secondary-button discover-models" disabled={locked} onClick={()=>void perform('discover')}>{operation==='discover'?'Получаю список…':'Получить список моделей'}</button></div>
            <label>ID модели<input name="model" maxLength={300} list="model-names" value={draft.model} disabled={locked} onChange={event=>change('model',event.target.value)} placeholder="Выберите из списка или введите ID"/><datalist id="model-names">{models.map(model=><option value={model} key={model}/>)}</datalist></label>
            {!!models.length&&<div className="model-picker" aria-label="Модели сервера">{models.map(model=><button type="button" key={model} disabled={locked} className={draft.model===model?'selected':''} onClick={()=>change('model',model)}><span>{model}</span>{draft.model===model&&<CheckCircle2 size={14}/>}</button>)}</div>}
            <button type="button" className="secondary-button probe-model" disabled={locked||!draft.model.trim()} onClick={()=>void perform('probe')}>{operation==='probe'?'Проверяю ответ…':'Проверить ответ модели'}</button><small>Короткий запрос без файлов и истории, до 30 секунд. Сервер может автоматически загрузить выбранную модель.</small>
          </section>
          <div hidden={section!=='voice'}><VoiceSettings busy={locked}/></div><div hidden={section!=='extensions'}><ExtensionsSettings busy={locked}/></div>
          <div hidden={section!=='connections'}><ConnectionsSettings busy={locked}/></div><div hidden={section!=='runtime'}><LocalRuntimePanel locked={locked} onUse={(url,model,context)=>{setDraft(current=>({...current,base_url:url,model,api_key:'',api_protocol:'chat',settings:{...current.settings,context_window:context,max_tokens:Math.min(current.settings.max_tokens,Math.floor(context/4)),context_reserve_tokens:Math.min(current.settings.context_reserve_tokens,Math.max(128,Math.floor(context/8)))}}));setModels([]);setSection('connection');}}/></div>
          <section hidden={section!=='generation'} className="settings-section"><div className="section-intro"><span className="eyebrow">ПАРАМЕТРЫ</span><div className="settings-section-heading"><h3>Генерация и лимиты</h3><button type="button" className="reset-generation" disabled={locked} onClick={resetGeneration}><RotateCcw size={13}/>Сбросить параметры</button></div><p>Настройте ответы модели и расход контекста.</p></div>
            {draft.settings.budget_mode==='manual'&&<div className="generation-presets">{[{label:'Точный код',temperature:0.2,max_tokens:8192},{label:'Разговор',temperature:0.5,max_tokens:4096},{label:'Короткий ответ',temperature:0.3,max_tokens:1024}].map(preset=><button type="button" className="secondary-button" disabled={locked} key={preset.label} onClick={()=>change('settings',{...draft.settings,temperature:preset.temperature,top_p:1,max_tokens:preset.max_tokens})}>{preset.label}</button>)}</div>}
            <GenerationFields value={draft.settings} locked={locked} onChange={settings=>change('settings',settings)}/>
            <p className="settings-help">Для внешнего сервера контекст, GPU и chat template настраиваются в LM Studio/Ollama. Для собственного GGUF контекст и GPU-слои задаются в разделе выше. Эти поля управляют запросами Лешего.</p>
          </section>
          {section==='storage'&&<StorageSettings busy={locked}/>}
          <div hidden={section!=='appearance'}><AppearanceSettings/></div>
        </div>
        <footer className="settings-footer"><div className={`settings-feedback ${notice.kind}`} role={notice.kind==='error'?'alert':'status'}>{notice.text}</div><div className="settings-actions">{operation&&operation!=='save'&&<button type="button" className="secondary-button" onClick={()=>void window.lca.cancelModelSetup()}>Отменить проверку</button>}<button type="button" className="secondary-button" disabled={!!operation} onClick={onClose}>Закрыть</button>{['connection','generation'].includes(section)&&<button type="submit" className="primary-button save-model-settings" disabled={locked}>{operation==='save'?'Сохраняю…':'Сохранить настройки'}</button>}</div></footer>
      </form>
    </section>
  </div>;
}
