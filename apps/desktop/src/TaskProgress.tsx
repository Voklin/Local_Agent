import { Check, Circle, LoaderCircle, Minus } from 'lucide-react';

export type TaskStage = { id: string; title: string; objective?: string; status: string };
export type ToolActivity = { id: number; tool: string; path: string; status: string; summary: string; stage: string };
export type TaskSnapshot = {
  status: string; last_event: string; stage: string; turn: number; tool_calls: number;
  stages: TaskStage[]; tool_activity?: ToolActivity[]; activity_omitted?: number;
  modified_files?: string[]; stop_reason?: string;
};

const toolNames: Record<string, string> = { list_files: 'Обзор файлов', read_file: 'Чтение файла', search_text: 'Поиск', write_file: 'Запись файла' };
const activityNames: Record<string, string> = {
  running: 'Выполняется', awaiting_approval: 'Ждёт решения', applying: 'Применяется', succeeded: 'Успешно',
  failed: 'Ошибка', rejected: 'Отклонено', cancelled: 'Отменено', interrupted: 'Прервано', unknown: 'Проверьте файл',
};
const stageNames: Record<string, string> = { active: 'Выполняется', done: 'Завершён', pending: 'Ожидает', skipped: 'Пропущен' };

export function TaskProgress({ task, busy, onResume }: { task: TaskSnapshot; busy: boolean; onResume: () => void }) {
  const activities = task.tool_activity || [];
  const waiting = activities.some(item => item.status === 'awaiting_approval');
  const status = task.status === 'paused' ? 'Приостановлена' : task.status === 'completed' ? 'Завершена' : waiting ? 'Ожидает подтверждения' : 'Выполняется';
  const modified = [...new Set(task.modified_files || [])];
  return <section className="task-card task-progress" aria-label="План задачи">
    <div className="task-progress-heading"><b>{status}</b><span>Цикл {task.turn || 0}</span></div>
    <p className="task-last-event">{task.last_event}</p>
    <details open className="task-plan">
      <summary>План задачи</summary>
      <div className="task-progress-body">
        <ol className="task-stages" aria-label="Этапы выполнения">
          {(task.stages || []).map(stage => <li key={stage.id} data-status={stage.status} aria-current={stage.status === 'active' ? 'step' : undefined}>
            {stage.status === 'done' ? <Check size={13}/> : stage.status === 'skipped' ? <Minus size={13}/> : stage.status === 'active' && task.status === 'running' ? <LoaderCircle size={13}/> : <Circle size={13}/>}
            <div><strong title={stage.objective}>{stage.title}</strong><span>{stage.status === 'active' && task.status === 'paused' ? 'Приостановлен' : stageNames[stage.status] || stage.status}</span></div>
          </li>)}
        </ol>
        <div className="task-tools-heading">Инструменты <span>{activities.length}{task.activity_omitted ? ` · ещё ${task.activity_omitted} в истории` : ''}</span></div>
        {activities.length ? <ol className="task-tools" aria-label="Журнал инструментов">
          {[...activities].reverse().map(item => <li key={item.id} data-status={item.status}>
            <div className="task-tool-title"><strong>{toolNames[item.tool] || item.tool}</strong><span>{activityNames[item.status] || item.status}</span></div>
            {item.path && <code>{item.path}</code>}
            <p>{item.summary}</p>
          </li>)}
        </ol> : <p className="task-empty">{task.status === 'running' ? 'Вызовов инструментов пока нет.' : 'Для этой задачи нет записей инструментов.'}</p>}
        {modified.length > 0 && <details className="task-files"><summary>Изменённые файлы · {modified.length}</summary><ul>{modified.map(file => <li key={file}><code>{file}</code></li>)}</ul></details>}
        <p className="task-check-note">Проверка ответа моделью не заменяет запуск тестов.</p>
      </div>
    </details>
    {task.stop_reason && <p className="task-stop-reason">{task.stop_reason}</p>}
    {task.status === 'paused' && !busy && <button className="task-resume" onClick={onResume}>Продолжить задачу</button>}
  </section>;
}
