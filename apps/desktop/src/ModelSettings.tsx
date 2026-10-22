import { useEffect, useRef, useState } from 'react';
import { CheckCircle2, Eye, EyeOff, RotateCcw, Server, Settings2, X } from 'lucide-react';

export type GenerationSettings = {
  temperature: number; top_p: number; max_tokens: number; max_context_chars: number;
  request_timeout: number; max_agent_turns: number; max_runtime_minutes: number;
};
export type ModelConfig = { base_url: string; model: string; api_key: string; settings: GenerationSettings };
export const defaultGeneration: GenerationSettings = {
  temperature: 0.2, top_p: 1, max_tokens: 8192, max_context_chars: 80000,
  request_timeout: 180, max_agent_turns: 200, max_runtime_minutes: 180,
};
const fields: { key: keyof GenerationSettings; label: string; min: number; max: number; step: number; hint: string }[] = [
  {key:'temperature', label:'Temperature', min:0, max:2, step:0.05, hint:'Ниже — более предсказуемый ответ. Для кода начните с 0.2.'},
  {key:'top_p', label:'Top P', min:0.01, max:1, step:0.01, hint:'Ограничивает выбор вероятных токенов. 1 оставляет полный диапазон.'},
  {key:'max_tokens', label:'Максимум токенов ответа', min:64, max:32768, step:1, hint:'Общий бюджет генерации. У reasoning-моделей часть бюджета может уйти на рассуждения.'},
  {key:'max_context_chars', label:'Бюджет контекста, символов', min:12000, max:500000, step:1, hint:'Ограничение сообщений приложения, а не размер контекстного окна модели в токенах.'},
  {key:'request_timeout', label:'Ожидание HTTP, секунд', min:5, max:600, step:1, hint:'Тайм-аут сетевой операции. Медленный ответ может требовать большего значения.'},
  {key:'max_agent_turns', label:'Максимум циклов агента', min:1, max:500, step:1, hint:'Количество обращений в основном цикле, включая повтор пустого ответа.'},
  {key:'max_runtime_minutes', label:'Время задачи, минут', min:1, max:1440, step:1, hint:'Проверяется между циклами. Активный HTTP ограничен отдельным тайм-аутом.'},
];

export function ModelSettings({ initial, busy, onSaved, onClose }: {
  initial: ModelConfig; busy: boolean; onSaved: (config: ModelConfig) => void; onClose: () => void;
}) {
  const [draft, setDraft] = useState<ModelConfig>(() => ({...initial, settings:{...initial.settings}}));
  const [models, setModels] = useState<string[]>([]);
  const [visibleKey, setVisibleKey] = useState(false);
  const [operation, setOperation] = useState('');
  const [notice, setNotice] = useState({kind:'info', text:'Сначала проверьте сервер и выберите модель. Проверки не сохраняют изменения.'});
  const dialog = useRef<HTMLElement>(null);
  const locked = busy || !!operation;
  useEffect(() => {
    const previous = document.activeElement as HTMLElement | null;
    dialog.current?.querySelector<HTMLInputElement>('input')?.focus();
    return () => previous?.focus();
  }, []);

  function change<K extends keyof ModelConfig>(key: K, value: ModelConfig[K]) {
    setDraft(current => ({...current, [key]:value}));
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
      const value = draft.settings[field.key];
      if (!Number.isFinite(value) || value < field.min || value > field.max || (field.step === 1 && !Number.isInteger(value)))
        throw new Error(`${field.label}: ${field.step === 1 ? 'целое число' : 'число'} от ${field.min} до ${field.max}.`);
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

  return <div className="modal-backdrop settings-backdrop">
    <section ref={dialog} className="settings-dialog" role="dialog" aria-modal="true" aria-labelledby="model-settings-title" onKeyDown={handleKeys}>
      <header className="settings-header"><div><Settings2 size={20}/><div><h2 id="model-settings-title">Модель и подключение</h2><p>Одна конфигурация для Chat и IDE</p></div></div><button className="icon-button" title="Закрыть настройки" disabled={!!operation} onClick={onClose}><X size={20}/></button></header>
      <form className="model-settings" onSubmit={event => {event.preventDefault(); void perform('save');}} noValidate>
        <div className="settings-scroll">
          {busy&&<div className="settings-notice">Дождитесь завершения задачи, чтобы менять настройки.</div>}
          <section className="settings-section"><h3><Server size={16}/>Подключение</h3>
            <div className="endpoint-presets"><span>Быстрый адрес</span><button type="button" disabled={locked} onClick={()=>change('base_url','http://127.0.0.1:1234/v1')}>LM Studio</button><button type="button" disabled={locked} onClick={()=>change('base_url','http://127.0.0.1:11434/v1')}>Ollama</button></div>
            <label>URL сервера<input name="base_url" maxLength={2000} value={draft.base_url} disabled={locked} onChange={event=>change('base_url',event.target.value)} placeholder="http://127.0.0.1:1234/v1"/><small>Адрес OpenAI-совместимого API с /v1. Сервер должен быть запущен отдельно.</small></label>
            <label>API-ключ <span className="field-optional">если требуется сервером</span><div className="key-input"><input name="api_key" maxLength={4000} type={visibleKey?'text':'password'} autoComplete="off" value={draft.api_key} disabled={locked} onChange={event=>change('api_key',event.target.value)}/><button type="button" className="icon-button" title={visibleKey?'Скрыть ключ':'Показать ключ'} onClick={()=>setVisibleKey(!visibleKey)}>{visibleKey?<EyeOff size={16}/>:<Eye size={16}/>}</button></div><small>Ключ не сохраняется на диск. Для локального сервера обычно не нужен.</small></label>
            <div className="connection-actions"><button type="button" className="secondary-button discover-models" disabled={locked} onClick={()=>void perform('discover')}>{operation==='discover'?'Получаю список…':'Проверить сервер и загрузить модели'}</button></div>
            <label>ID модели<input name="model" maxLength={300} list="model-names" value={draft.model} disabled={locked} onChange={event=>change('model',event.target.value)} placeholder="Выберите из списка или введите ID"/><datalist id="model-names">{models.map(model=><option value={model} key={model}/>)}</datalist></label>
            {!!models.length&&<div className="model-picker" aria-label="Модели сервера">{models.map(model=><button type="button" key={model} disabled={locked} className={draft.model===model?'selected':''} onClick={()=>change('model',model)}><span>{model}</span>{draft.model===model&&<CheckCircle2 size={14}/>}</button>)}</div>}
            <button type="button" className="secondary-button probe-model" disabled={locked||!draft.model.trim()} onClick={()=>void perform('probe')}>{operation==='probe'?'Проверяю ответ…':'Проверить ответ модели'}</button><small>Короткий запрос без файлов и истории, до 30 секунд, с выбранным ниже бюджетом токенов. Сервер может автоматически загрузить выбранную модель.</small>
          </section>
          <section className="settings-section"><div className="settings-section-heading"><h3>Генерация и лимиты</h3><button type="button" className="reset-generation" disabled={locked} onClick={resetGeneration}><RotateCcw size={13}/>Сбросить параметры</button></div>
            <div className="generation-grid">{fields.map(field=><label key={field.key}>{field.label}<input name={field.key} type="number" min={field.min} max={field.max} step={field.step} value={Number.isFinite(draft.settings[field.key])?draft.settings[field.key]:''} disabled={locked} onChange={event=>change('settings',{...draft.settings,[field.key]:event.target.value===''?NaN:Number(event.target.value)})}/><small>{field.hint}</small></label>)}</div>
            <p className="settings-help">Размер контекста, GPU-слои, квантование и chat template настраиваются в LM Studio или другом сервере. Эти поля управляют запросами LocalAgent.</p>
          </section>
        </div>
        <footer className="settings-footer"><div className={`settings-feedback ${notice.kind}`} role={notice.kind==='error'?'alert':'status'}>{notice.text}</div><div className="settings-actions">{operation&&operation!=='save'&&<button type="button" className="secondary-button" onClick={()=>void window.lca.cancelModelSetup()}>Отменить проверку</button>}<button type="button" className="secondary-button" disabled={!!operation} onClick={onClose}>Закрыть</button><button type="submit" className="primary-button save-model-settings" disabled={locked}>{operation==='save'?'Сохраняю…':'Сохранить настройки'}</button></div></footer>
      </form>
    </section>
  </div>;
}
