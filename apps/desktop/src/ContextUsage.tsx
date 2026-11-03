import type { RequestBudgetSnapshot,ModelUsageSnapshot } from '../shared/contextTypes';
export type { RequestBudgetSnapshot,ModelUsageSnapshot } from '../shared/contextTypes';
export function ContextUsage({budget,usage}:{budget?:RequestBudgetSnapshot;usage?:ModelUsageSnapshot}) {
  if(!budget)return null;
  const number=(value:number)=>value.toLocaleString('ru');
  return <details className="context-usage" open={budget.status==='blocked'?true:undefined} aria-label="Контекст и расход">
    <summary>{budget.mode==='auto'?'Контекст · автоматически':'Контекст'} · ≈ {number(budget.input_tokens_estimate)} / {number(budget.window_tokens)} токенов{budget.status==='blocked'?' · не помещается':''}</summary>
    {budget.mode==='auto'&&<p>{budget.context_source}. Ответ и история подстраиваются автоматически.{budget.tools_deferred?` Редкие инструменты в каталоге: ${budget.tools_deferred}.`:''}</p>}
    <p>Ответ: до {number(budget.output_tokens_reserved)} · запас: {number(budget.safety_tokens)} · свободно: {number(Math.max(0,budget.remaining_tokens))}</p>
    <dl>{Object.entries(budget.components).map(([key,value])=><div key={key}><dt>{{instructions:'Инструкции',history:'История и результаты',tools:'Схемы инструментов',protocol:'Формат запроса'}[key]}</dt><dd>≈ {number(value)}</dd></div>)}</dl>
    <p>Оценка с запасом по окончательному запросу. Точное число токенов зависит от модели.</p>
    {(budget.reasons||[]).map(reason=><p key={reason}>{reason}</p>)}
    {!!budget.mcp_available&&<p>Схемы MCP: подключено {budget.mcp_loaded||0} из {budget.mcp_available}. Остальные доступны через поиск инструментов.</p>}
    {usage?.reported?<p>Сервер сообщил: вход {number(usage.input_tokens||0)}, выход {number(usage.output_tokens||0)} токенов · по {usage.requests_reported} из {usage.requests} запросов.</p>:<p>Сервер пока не сообщил фактический расход токенов.</p>}
  </details>;
}
