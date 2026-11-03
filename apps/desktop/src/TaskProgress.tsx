import { Check, Circle, LoaderCircle, Minus } from 'lucide-react';
import { useState } from 'react';
import { ContextUsage } from './ContextUsage';
import {TaskGraphPanel} from './TaskGraphPanel';
import { RunHistory } from './RunHistory';

import type {TaskSnapshot,TaskRecoveryItem,TaskRecoveryResolution} from '../shared/taskTypes';
export type {TaskStage,ToolActivity,TaskSnapshot,TaskRecoveryItem,TaskRecoveryResolution} from '../shared/taskTypes';

const toolNames: Record<string, string> = { list_files: 'Обзор файлов', read_file: 'Чтение файла', search_text: 'Поиск', write_file: 'Запись файла',patch_file:'Точечная правка',create_directory:'Создание каталогов',rename_file:'Перемещение файла',delete_file:'Удаление файла',glob_files:'Поиск файлов',read_range:'Чтение строк',get_project_instructions:'Инструкции проекта' };
const activityNames: Record<string, string> = {
  running: 'Выполняется', awaiting_approval: 'Ждёт решения', applying: 'Применяется', succeeded: 'Успешно',
  failed: 'Ошибка', rejected: 'Отклонено', cancelled: 'Отменено', interrupted: 'Прервано', unknown: 'Результат неизвестен',
  not_executed: 'Не выполнено', confirmed: 'Подтверждено вами',
  instructions_required: 'Правила подключены',
};
const stageNames: Record<string, string> = { active: 'Выполняется', done: 'Завершён', pending: 'Ожидает', skipped: 'Пропущен' };

export function taskStatusLabel(task: TaskSnapshot) {
  const state = task.run_state || task.status;
  if(task.snapshot_attention?.length)return 'Проверьте прерванный откат';
  if(task.workspace_reverted)return 'Изменения отменены';
  if(task.workspace_reviewed)return 'Файлы проверены вручную';
  if (state === 'needs_attention' || task.recovery_items?.length || task.recovery_error) return 'Требует проверки';
  if (state === 'failed') return 'Ошибка выполнения';
  if (state === 'paused') return 'Приостановлена';
  if (state === 'completed') return task.verification?.status === 'scoped_passed' ? 'Проверены выбранные файлы' : task.verification?.status === 'failed' ? 'Проверка не пройдена' : ['not_run','stale','incomplete'].includes(task.verification?.status||'') ? 'Ответ получен' : 'Завершена';
  if (state === 'waiting_approval' || task.tool_activity?.some(item => item.status === 'awaiting_approval')) return 'Ожидает подтверждения';
  if (state === 'executing') return 'Выполняет действие';
  if (state === 'verifying') return 'Проверяет результат';
  return 'Выполняется';
}

export function TaskProgress({ task, busy, onResume, onResolveRecovery,onTask }: { task: TaskSnapshot; busy: boolean; onTask?:(task:TaskSnapshot)=>void; onResume: () => void; onResolveRecovery?: (item: TaskRecoveryItem, resolution: TaskRecoveryResolution) => void }) {
  const [review, setReview] = useState<{key: string; resolution: TaskRecoveryResolution} | null>(null);
  const recovery = task.recovery_items || [];
  const state = task.run_state || task.status;
  const status = taskStatusLabel(task);
  const modified = [...new Set(task.modified_files || [])];
  return <section className="task-card task-progress" aria-label="План задачи">
    <div className="task-progress-heading"><b>{status}</b><span>Цикл {task.turn || 0}</span></div>
    <p className="task-last-event">{task.last_event}</p>
    {task.verification&&<p className="task-check-note" data-verification={task.verification.status}>{task.verification.summary}</p>}
    {task.options?.read_only&&<p className="task-check-note">Режим агента: только чтение</p>}
    {(!!task.plan_steps?.length||onTask)&&<TaskGraphPanel task={task} busy={busy} onTask={onTask}/>}
    {!!task.acceptance_evidence?.length&&<details open className="task-criteria"><summary>Критерии готовности</summary><ul>{task.acceptance_evidence.map(item=><li key={item.id} data-criterion-status={item.status}>{item.description}<span>{({checks_passed:'Связанные проверки прошли',scoped_checks_passed:'Проверка выбранных файлов прошла',failed:'Проверка не пройдена',stale:'Результат устарел',unverified:'Не подтверждено'} as Record<string,string>)[item.status]||item.status}</span></li>)}</ul></details>}
    {!!task.test_results?.length&&<details open className="task-checks"><summary>Проверки проекта</summary>{task.test_results.map(check=><div key={check.id} data-check-status={!check.ok?'failed':check.evidence_status==='current'?(check.coverage?.project_complete?'passed':'scoped'):check.evidence_status||'unverified'}><b>{check.purpose||'Назначение не задано'}</b><code>{check.program} {(check.arguments||[]).join(' ')}</code><span>{check.kind==='diagnostics'?`LSP: ${check.ok?'полный ответ без ошибок':'не подтверждён'}`:`Команда: ${check.ok?'выполнена успешно':'не подтверждена'} · код выхода: ${check.exit_code??'нет'}`}</span>{check.diagnostics?.map((d,index)=><p key={index}>Строка {d.line}:{d.column} · {d.severity===1?'Ошибка':'Замечание'}: {d.message}</p>)}<span>{check.evidence_summary||'Актуальность исходников не подтверждена.'}</span>{check.coverage?.kind==='files'&&<span>Область: {[...(check.coverage.files||[]),...(check.coverage.dependencies||[])].join(', ')}. Остальной проект не сверялся.</span>}</div>)}</details>}
    {task.checks_notice&&<p className="task-check-note">{task.checks_notice}</p>}
    <ContextUsage budget={task.budget} usage={task.usage}/>
    {!!task.children?.length&&<details open className="child-runs"><summary>Дочерние исследования · {task.children.length}</summary><p className="task-check-note">Та же модель · только чтение. Stop родителя отменяет всё дерево.</p><ol>{task.children.map(child=><li key={child.id}><b>{child.profile?.title||'Исследователь'}</b> · <code>{child.id.slice(0,8)}</code> · {({completed:'Завершён',running:'Исследует',executing:'Читает файлы',paused:'Приостановлен',failed:'Ошибка',needs_attention:'Нужна проверка'} as Record<string,string>)[child.state]||child.state}<p>{child.event}</p><details><summary>Ход работы · цикл {child.turn||0} · вызовов {child.tool_calls||0}</summary><ol>{child.activity?.map((item,index)=><li key={item.id??index}><strong>{toolNames[item.tool||'']||item.tool}</strong> · {activityNames[item.status||'']||item.status}{item.path&&<code>{item.path}</code>}<p>{item.summary}</p></li>)}</ol>{!child.activity?.length&&<p>Вызовов пока нет.</p>}</details></li>)}</ol></details>}
    <RunHistory chatId={task.chat_id} runId={task.run_id} ledger={task.run_ledger}/>
    {!!task.context_pack?.sources.length&&<details className="task-files context-sources"><summary>Источники контекста · {task.context_pack.sources.length}</summary><p className="task-check-note">Выбраны сохранённые фрагменты, покрытие проекта частичное. {task.context_pack.status==='waiting_approval'?'Ожидают разрешения на передачу.':task.context_pack.status==='rejected'?'Передача отклонена.':''}</p><ul>{task.context_pack.sources.map(source=><li key={`${source.path}:${source.start_line}`}><code>{source.path}:{source.start_line}–{source.end_line}</code><span>{source.reason}</span></li>)}</ul>{!!task.context_pack.budget_omitted&&<p className="task-check-note">Фрагментов убрано под окно модели: {task.context_pack.budget_omitted}</p>}</details>}
    {task.context?.compressed&&<p className="task-check-note">Контекст уплотнён: {task.context.before_chars.toLocaleString('ru')} → {task.context.after_chars.toLocaleString('ru')} символов. Полная история сохранена.</p>}
    <details open className="task-plan">
      <summary>План задачи</summary>
      <div className="task-progress-body">
        <ol className="task-stages" aria-label="Этапы выполнения">
          {(task.stages || []).map(stage => <li key={stage.id} data-status={stage.status} aria-current={stage.status === 'active' ? 'step' : undefined}>
            {stage.status === 'done' ? <Check size={13}/> : stage.status === 'skipped' ? <Minus size={13}/> : stage.status === 'active' && ['running', 'executing', 'verifying'].includes(state) ? <LoaderCircle size={13}/> : <Circle size={13}/>}
            <div><strong title={stage.objective}>{stage.title}</strong><span>{stage.status === 'active' && state === 'paused' ? 'Приостановлен' : stage.status === 'active' && state === 'needs_attention' ? 'Требует проверки' : stage.status === 'active' && state === 'failed' ? 'Ошибка' : stageNames[stage.status] || stage.status}</span></div>
          </li>)}
        </ol>
        {recovery.length > 0 && <section className="task-recovery" aria-label="Проверка прерванных действий">
          <div className="task-tools-heading">Проверьте прерванные действия · {recovery.length}</div>
          <p className="task-check-note">Перед выбором проверьте фактический файл или внешний сервис. Сохранится только результат вашей проверки, действие не запускается. Для повторного выполнения действуют обычные подтверждения.</p>
          <ol className="task-tools task-recovery-items">{recovery.map(item => {
            const key = `${task.journal_id}:${item.message_index}:${item.call_id}`;
            const selected = review?.key === key ? review.resolution : null;
            return <li key={key} data-status="unknown">
              <div className="task-tool-title"><strong>{toolNames[item.tool] || item.tool}</strong><span>Нужна ваша проверка</span></div>
              {item.path && <code>{item.path}</code>}{item.summary && <p>{item.summary}</p>}
              {onResolveRecovery && (selected ? <div role="group" aria-label="Подтвердите результат проверки">
                <p>{selected === 'completed' ? 'Вы проверили: действие уже выполнено.' : 'Вы проверили: действие не выполнялось.'}</p>
                <button className="task-resume" disabled={busy} onClick={() => { onResolveRecovery(item, selected); setReview(null); }}>Подтвердить результат</button>
                <button className="task-resume" disabled={busy} onClick={() => setReview(null)}>Назад</button>
              </div> : <div role="group" aria-label="Результат проверки действия">
                <button className="task-resume" disabled={busy} onClick={() => setReview({key, resolution:'completed'})}>Действие уже выполнено</button>
                <button className="task-resume" disabled={busy} onClick={() => setReview({key, resolution:'not_executed'})}>Действие не выполнялось</button>
              </div>)}
            </li>;
          })}</ol>
        </section>}
        {!!task.workspace_changes?.length&&<details className="task-files"><summary>Операции с проектом · {task.workspace_changes.length}</summary><ul>{task.workspace_changes.map(change=><li key={change.id}>{toolNames[change.operation]||change.operation}: <code>{change.path}</code>{change.destination&&<> → <code>{change.destination}</code></>}</li>)}</ul></details>}
        {!!task.project_instructions?.length&&<details className="task-files"><summary>Инструкции проекта · {task.project_instructions.length}</summary><ul>{task.project_instructions.map(rule=><li key={rule.path}><code>{rule.path}</code> · папка {rule.scope}</li>)}</ul></details>}
        {modified.length > 0 && <details className="task-files"><summary>Изменённые файлы · {modified.length}</summary><ul>{modified.map(file => <li key={file}><code>{file}</code></li>)}</ul></details>}
        <p className="task-check-note">Проверка ответа моделью не заменяет запуск тестов.</p>
      </div>
    </details>
    {task.stop_reason && <p className="task-stop-reason">{task.stop_reason}</p>}
    {task.recovery_error && <p role="alert" className="task-stop-reason">{task.recovery_error}</p>}
    {(state === 'paused' || state === 'failed' || state === 'needs_attention' || recovery.length > 0) && <button className="task-resume" disabled={busy || recovery.length > 0 || !!task.recovery_error} title={recovery.length || task.recovery_error ? 'Сначала проверьте все прерванные действия' : undefined} onClick={onResume}>Продолжить задачу</button>}
  </section>;
}
