export type GenerationSettings = {
  temperature: number; top_p: number; max_tokens: number; max_context_chars: number;
  request_timeout: number; max_agent_turns: number; max_runtime_minutes: number;
};
export const defaultGeneration: GenerationSettings = {
  temperature: 0.2, top_p: 1, max_tokens: 8192, max_context_chars: 80000,
  request_timeout: 180, max_agent_turns: 200, max_runtime_minutes: 180,
};
export const generationFields: { key: keyof GenerationSettings; label: string; min: number; max: number; step: number; hint: string }[] = [
  {key:'temperature', label:'Temperature', min:0, max:2, step:0.05, hint:'Ниже — более предсказуемый ответ. Для кода начните с 0.2.'},
  {key:'top_p', label:'Top P', min:0.01, max:1, step:0.01, hint:'Ограничивает выбор вероятных токенов. 1 оставляет полный диапазон.'},
  {key:'max_tokens', label:'Максимум токенов ответа', min:64, max:32768, step:1, hint:'Общий бюджет генерации. У reasoning-моделей часть бюджета может уйти на рассуждения.'},
  {key:'max_context_chars', label:'Бюджет контекста, символов', min:12000, max:500000, step:1, hint:'Ограничение сообщений приложения, а не размер контекстного окна модели в токенах.'},
  {key:'request_timeout', label:'Ожидание HTTP, секунд', min:5, max:600, step:1, hint:'Тайм-аут сетевой операции. Медленный ответ может требовать большего значения.'},
  {key:'max_agent_turns', label:'Максимум циклов агента', min:1, max:500, step:1, hint:'Количество обращений в основном цикле, включая повтор пустого ответа.'},
  {key:'max_runtime_minutes', label:'Время задачи, минут', min:1, max:1440, step:1, hint:'Проверяется между циклами. Активный HTTP ограничен отдельным тайм-аутом.'},
];

export function GenerationFields({value,locked,onChange}:{value:GenerationSettings;locked:boolean;onChange:(settings:GenerationSettings)=>void}) {
  return <div className="generation-grid">{generationFields.map(field=><label key={field.key}>{field.label}<input name={field.key} type="number" min={field.min} max={field.max} step={field.step} value={Number.isFinite(value[field.key])?value[field.key]:''} disabled={locked} onChange={event=>onChange({...value,[field.key]:event.target.value===''?NaN:Number(event.target.value)})}/><small>{field.hint}</small></label>)}</div>;
}
