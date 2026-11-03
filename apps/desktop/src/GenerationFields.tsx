export type GenerationSettings = {
  temperature: number; top_p: number; max_tokens: number; max_context_chars: number;
  request_timeout: number; max_agent_turns: number; max_runtime_minutes: number;
  context_window:number; context_reserve_tokens:number; memory_updates:'off'|'on_change'|'always';
  budget_mode:'auto'|'manual';
  paid_budget?:{enabled:boolean;amount:number;input_per_million:number;output_per_million:number;currency:'USD'|'EUR'|'RUB'};
};
export const defaultGeneration: GenerationSettings = {
  temperature: 0.2, top_p: 1, max_tokens: 8192, max_context_chars: 80000,
  request_timeout: 180, max_agent_turns: 200, max_runtime_minutes: 180,
  context_window:32768, context_reserve_tokens:512, memory_updates:'on_change',
  budget_mode:'auto',
};
export const generationFields: { key: Exclude<keyof GenerationSettings,'memory_updates'|'budget_mode'|'paid_budget'>; label: string; min: number; max: number; step: number; hint: string }[] = [
  {key:'temperature', label:'Temperature', min:0, max:2, step:0.05, hint:'Ниже — более предсказуемый ответ. Для кода начните с 0.2.'},
  {key:'top_p', label:'Top P', min:0.01, max:1, step:0.01, hint:'Ограничивает выбор вероятных токенов. 1 оставляет полный диапазон.'},
  {key:'max_tokens', label:'Максимум токенов ответа', min:64, max:32768, step:1, hint:'Общий бюджет генерации. У reasoning-моделей часть бюджета может уйти на рассуждения.'},
  {key:'max_context_chars', label:'Бюджет контекста, символов', min:12000, max:500000, step:1, hint:'Ограничение сообщений приложения, а не размер контекстного окна модели в токенах.'},
  {key:'context_window',label:'Окно загруженной модели, токенов',min:512,max:1048576,step:1,hint:'Укажите окно, с которым модель реально загружена в LM Studio или на сервере. Леший проверяет весь запрос со схемами и резервом ответа.'},
  {key:'context_reserve_tokens',label:'Дополнительный запас, токенов',min:128,max:8192,step:1,hint:'Запас на формат чата и неточность оценки. Он оставляется сверх максимума ответа.'},
  {key:'request_timeout', label:'Ожидание HTTP, секунд', min:5, max:600, step:1, hint:'Тайм-аут сетевой операции. Медленный ответ может требовать большего значения.'},
  {key:'max_agent_turns', label:'Максимум циклов агента', min:1, max:500, step:1, hint:'Количество обращений в основном цикле, включая повтор пустого ответа.'},
  {key:'max_runtime_minutes', label:'Время задачи, минут', min:1, max:1440, step:1, hint:'Проверяется между циклами. Активный HTTP ограничен отдельным тайм-аутом.'},
];

export function GenerationFields({value,locked,onChange}:{value:GenerationSettings;locked:boolean;onChange:(settings:GenerationSettings)=>void}) {
  const automatic=value.budget_mode!=='manual';
  const paid=value.paid_budget||{enabled:false,amount:1,input_per_million:0,output_per_million:0,currency:'USD' as const};
  return <><details className="paid-budget"><summary>Добровольный бюджет внешнего API</summary><label><input type="checkbox" checked={paid.enabled} disabled={locked} onChange={e=>onChange({...value,paid_budget:{...paid,enabled:e.target.checked}})}/>Ограничить планируемые расходы на задачу и её детей</label><p className="settings-help">На локальный auto-режим не влияет. Цены вводятся вручную; это оценка, фактический счёт провайдера может отличаться. При неизвестном usage оценка сохраняется.</p>{paid.enabled&&<><label>Валюта<select value={paid.currency} disabled={locked} onChange={e=>onChange({...value,paid_budget:{...paid,currency:e.target.value as typeof paid.currency}})}>{['USD','EUR','RUB'].map(c=><option key={c}>{c}</option>)}</select></label>{([{key:'amount',label:'Бюджет на задачу'},{key:'input_per_million',label:'Цена 1 млн входных токенов'},{key:'output_per_million',label:'Цена 1 млн выходных токенов'}] as const).map(field=><label key={field.key}>{field.label}<input type="number" min={0} max={1000000} step="any" disabled={locked} value={paid[field.key]} onChange={e=>onChange({...value,paid_budget:{...paid,[field.key]:Number(e.target.value)}})}/></label>)}</>}</details><label>Управление лимитами<select aria-label="Управление лимитами" disabled={locked} value={automatic?'auto':'manual'} onChange={e=>onChange({...value,budget_mode:e.target.value as GenerationSettings['budget_mode']})}><option value="auto">Автоматически · рекомендуется</option><option value="manual">Вручную · дополнительные параметры</option></select></label>
    {automatic&&<p className="settings-help auto-budget-help">Выберите модель — Леший подберёт размер ответа и рабочий контекст, сожмёт старую историю и подключит нужные инструменты. У локальных моделей нет суммарного ограничения циклов и времени задачи; остановить работу можно кнопкой Stop. Обнаружение окна не меняет загрузку модели и настройки видеопамяти в LM Studio.</p>}
    {!automatic&&<div className="generation-presets" aria-label="Размер окна модели">{[4096,8192,32768].map(size=><button type="button" className="secondary-button" disabled={locked} key={size} onClick={()=>onChange({...value,context_window:size,max_tokens:Math.min(value.max_tokens,Math.floor(size/4)),context_reserve_tokens:Math.min(value.context_reserve_tokens,512)})}>{size/1024}K</button>)}</div>}
    <div className="generation-grid">{generationFields.filter(field=>!automatic||['temperature','top_p'].includes(field.key)).map(field=><label key={field.key}>{field.label}<input name={field.key} type="number" min={field.min} max={field.max} step={field.step} value={Number.isFinite(value[field.key])?value[field.key]:''} disabled={locked} onChange={event=>onChange({...value,[field.key]:event.target.value===''?NaN:Number(event.target.value)})}/><small>{field.hint}</small></label>)}</div><label>Память проекта<select aria-label="Обновление памяти проекта" value={value.memory_updates} disabled={locked} onChange={event=>onChange({...value,memory_updates:event.target.value as GenerationSettings['memory_updates']})}><option value="on_change">После изменений или просьбы запомнить</option><option value="off">Не обновлять автоматически</option><option value="always">После каждого успешного задания</option></select><small>Обновление памяти — отдельный запрос к модели. В обычном разговоре и при просмотре проекта он по умолчанию не нужен.</small></label></>;
}
