import {useEffect,useState} from 'react';
import type {RunLedgerSnapshot,RunSnapshot} from '../shared/contextTypes';

function Ledger({value}:{value:RunLedgerSnapshot}) {
  return <><p>Попытки HTTP: {value.http_attempts} · расход сообщён для {value.requests_reported}.</p>
    {!!value.requests_reported&&<p>По данным сервера: вход {value.input_tokens.toLocaleString('ru')}, выход {value.output_tokens.toLocaleString('ru')} токенов. Для остальных попыток расход неизвестен.</p>}
    {!!value.queued_requests&&<p>Ожидают модель: {value.queued_requests}</p>}
    {!!value.active_reserved_tokens&&<p>Зарезервировано в текущих запросах: ≈ {value.active_reserved_tokens.toLocaleString('ru')} токенов. Это оценка, не расход.</p>}
    {!!value.interrupted&&<p>Прерванных попыток: {value.interrupted}</p>}
    <p>Ожидание модели: {(value.queue_ms/1000).toFixed(1)} с{value.approval_ms!==undefined?` · подтверждений: ${(value.approval_ms/1000).toFixed(1)} с`:''}.</p></>;
}

export function RunHistory({chatId,runId,ledger}:{chatId?:string;runId?:string;ledger?:RunLedgerSnapshot}) {
  const [open,setOpen]=useState(false),[runs,setRuns]=useState<RunSnapshot[]>([]),[error,setError]=useState(''),[revision,setRevision]=useState(0),[loading,setLoading]=useState(false);
  useEffect(()=>{
    if(!open||!chatId)return;let disposed=false;setLoading(true);setError('');setRuns([]);
    void window.lca.runHistory(chatId).then(result=>{if(disposed)return;if(!result.ok){setError(result.error);return;}setRuns(result.runs);}).catch(e=>{if(!disposed)setError(String(e));}).finally(()=>{if(!disposed)setLoading(false);});
    return()=>{disposed=true;};
  },[open,chatId,runId,revision,ledger?.reservations]);
  if(!runId&&!ledger)return null;
  return <details className="run-history" open={open} onToggle={event=>setOpen(event.currentTarget.open)}><summary>Запуски и фактический расход</summary>
    {ledger&&<Ledger value={ledger}/>}
    <p>Учёт не ограничивает локальный auto-режим.</p>
    {!!chatId&&<button className="task-resume" disabled={loading} onClick={()=>setRevision(value=>value+1)}>{loading?'Загружаю…':'Обновить историю'}</button>}
    {error&&<p role="alert">{error}</p>}
    <ol className="run-records">{runs.map(run=><li key={run.id} data-parent={run.parent_id||undefined}><b>{run.parent_id?'↳ Дочерний запуск · ':''}{({ide:'IDE',chat:'Chat',voice:'Лола',research:'Исследование',child:'Дочернее исследование',probe:'Проверка модели'} as Record<string,string>)[run.kind]||run.kind} · {run.model}</b><code>{run.id.slice(0,8)} · {new Date(run.created_at).toLocaleString('ru',{dateStyle:'short',timeStyle:'short'})}</code><p>{({completed:'Завершён',paused:'Приостановлен',running:'Выполняется',waiting_approval:'Ожидает подтверждения',failed:'Ошибка',needs_attention:'Требует проверки',executing:'Выполняет действие',verifying:'Проверяет результат'} as Record<string,string>)[run.state]||run.state} · {(run.elapsed_ms/1000).toFixed(1)} с · инструментов: {run.tool_calls}</p>{run.spending&&<p>Бюджет дерева: оценка {run.spending.estimated_spent.toFixed(4)} + резерв {run.spending.reserved.toFixed(4)} из {run.spending.limit} {run.spending.currency}. Неизвестных счетов: {run.spending.unknown_attempts}.</p>}{run.recovered&&<p>{run.recovery_cause==='owner_replaced'?'Прежний процесс завершён; его PID уже принадлежит другому запуску.':'Прерван при завершении процесса.'} Автоматически не повторялся.</p>}<details><summary>Расход запуска</summary><Ledger value={{...run.ledger,approval_ms:run.approval_ms}}/></details></li>)}</ol>
  </details>;
}
