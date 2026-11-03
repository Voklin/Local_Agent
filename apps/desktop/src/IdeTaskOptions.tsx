import { Plus, Trash2 } from 'lucide-react';

import type {ValidationCommand,IdeOptions} from '../shared/ideTypes';
export type {ValidationCommand,IdeOptions} from '../shared/ideTypes';
export const defaultIdeOptions:IdeOptions={read_only:false,auto_checks:false,criteria:[],criteria_links:{},checks:[]};

export function serializeIdeOptions(value:IdeOptions,checks_only=false){
  const selected=value.criteria.map((text,index)=>({text:text.trim(),index})).filter(item=>item.text);
  return {...value,checks_only,checks:value.checks.map(check=>({...check,evidence_scope:check.evidence_scope?.kind==='files'?{kind:'files' as const,files:check.evidence_scope.files.map(p=>p.trim()).filter(Boolean),dependencies:check.evidence_scope.dependencies.map(p=>p.trim()).filter(Boolean)}:check.evidence_scope})),criteria:selected.map(item=>item.text),criteria_links:Object.fromEntries(selected.map((item,index)=>[index,value.criteria_links[String(item.index)]||[]]))};
}

export function IdeTaskOptions({value,onChange,busy,onRunChecks}:{value:IdeOptions;onChange:(value:IdeOptions)=>void;busy:boolean;onRunChecks:()=>void}) {
  function updateCheck(id:string,values:Partial<ValidationCommand>){onChange({...value,checks:value.checks.map(check=>check.id===id?{...check,...values}:check)});}
  function removeCheck(id:string){onChange({...value,checks:value.checks.filter(c=>c.id!==id),criteria_links:Object.fromEntries(Object.entries(value.criteria_links).map(([key,ids])=>[key,ids.filter(i=>i!==id)]))});}
  return <details className="ide-task-options"><summary>План и проверки{value.read_only?' · Только чтение':''}{value.checks.length?` · ${value.checks.length} проверок`:''}</summary>
    <div className="ide-options-body">
      <label className="check-row"><input type="checkbox" aria-label="Агент только читает" disabled={busy} checked={value.read_only} onChange={event=>onChange({...value,read_only:event.target.checked,auto_checks:event.target.checked?false:value.auto_checks})}/>Агент только читает и объясняет</label>
      <p className="settings-help">В этом режиме агент не изменяет файлы, не запускает программы и не вызывает внешние действия.</p>
      <label>Критерии готовности · по одному на строке<textarea aria-label="Критерии готовности" disabled={busy} rows={3} value={value.criteria.join('\n')} onChange={event=>onChange({...value,criteria:event.target.value.split('\n'),criteria_links:{}})} placeholder="Например: файл проходит проверку синтаксиса"/></label>
      {value.criteria.map((text,index)=>text.trim()&&<label key={index} className="criterion-link">Чем проверить: {text}<select aria-label={`Проверка критерия ${index+1}`} disabled={busy} value={value.criteria_links[String(index)]?.[0]||''} onChange={event=>onChange({...value,criteria_links:{...value.criteria_links,[index]:event.target.value?[event.target.value]:[]}})}><option value="">Нужна ручная проверка</option>{value.checks.map(check=><option key={check.id} value={check.id}>{check.purpose||'Проверка без названия'}</option>)}</select></label>)}
      <p className="settings-help">Успех команды подтверждает связанную проверку, но не заменяет вашу оценку результата.</p>
      {value.checks.map(check=><section className="ide-check-editor" key={check.id}>
        <div className="section-actions"><b>Проверка</b><button type="button" title="Удалить проверку" disabled={busy} onClick={()=>removeCheck(check.id)}><Trash2 size={13}/></button></div>
        <label>Тип проверки<select aria-label="Тип проверки" disabled={busy} value={check.kind||'custom'} onChange={event=>updateCheck(check.id,event.target.value==='diagnostics'?{kind:'diagnostics',program:'lsp',arguments:['src/main.py'],cwd:'.',evidence_scope:{kind:'files',files:['src/main.py'],dependencies:[]}}:{kind:event.target.value as ValidationCommand['kind'],...(check.kind==='diagnostics'?{program:'node',arguments:['--check','src/main.js']}: {})})}><option value="test">Тесты</option><option value="lint">Линтер</option><option value="types">Типы</option><option value="syntax">Синтаксис</option><option value="custom">Своя команда</option><option value="diagnostics">LSP · сохранённый файл</option></select></label>
        <label>Когда применять · шаблоны путей, по одному на строку<textarea aria-label="Шаблоны затронутых файлов" disabled={busy} rows={2} value={(check.applies_to||[]).join('\n')} onChange={event=>updateCheck(check.id,{applies_to:event.target.value.split('\n').filter(Boolean)})} placeholder={'src/*.py\nsrc/**/*.py'}/><small>Пусто — проверять всегда. Привязанный критерий готовности требует проверку независимо от шаблона. Ручной запуск выполняет все проверки.</small></label>
        <label>Что проверяем<input aria-label="Назначение проверки" disabled={busy} value={check.purpose} onChange={event=>updateCheck(check.id,{purpose:event.target.value})} placeholder="Например: синтаксис JavaScript"/></label>
        {check.kind!=='diagnostics'&&<>
        <label>Программа<input aria-label="Программа проверки" disabled={busy} value={check.program} onChange={event=>updateCheck(check.id,{program:event.target.value})} placeholder="node"/></label>
        <label>Аргументы · каждый с новой строки<textarea aria-label="Аргументы проверки" disabled={busy} rows={2} value={check.arguments.join('\n')} onChange={event=>updateCheck(check.id,{arguments:event.target.value?event.target.value.split('\n'):[]})} placeholder={'--check\nsrc/main.js'}/></label>
        <label>Папка внутри проекта<input aria-label="Папка проверки" disabled={busy} value={check.cwd} onChange={event=>updateCheck(check.id,{cwd:event.target.value})}/></label>
        </>}
        {check.kind==='diagnostics'&&<label>Сохранённый файл для LSP<input aria-label="Файл проверки LSP" disabled={busy} value={check.arguments[0]||''} onChange={e=>updateCheck(check.id,{arguments:[e.target.value],evidence_scope:{kind:'files',files:[e.target.value],dependencies:check.evidence_scope?.kind==='files'?check.evidence_scope.dependencies:[]}})}/><small>Настройте сервер в дополнительных возможностях IDE. Только полный ответ LSP без ошибок подтверждает эту проверку.</small></label>}
        <label>Область подтверждения<select aria-label="Область подтверждения проверки" disabled={busy||check.kind==='diagnostics'} value={check.evidence_scope?.kind||'workspace'} onChange={event=>updateCheck(check.id,{evidence_scope:event.target.value==='files'?{kind:'files',files:[],dependencies:[]}:{kind:'workspace'}})}><option value="workspace">Весь проект</option><option value="files">Выбранные файлы и зависимости</option></select></label>
        {check.evidence_scope?.kind==='files'&&<>
          <label>Файлы проверки · по одному пути от корня проекта<textarea aria-label="Файлы области проверки" disabled={busy} rows={2} value={check.evidence_scope.files.join('\n')} onChange={event=>updateCheck(check.id,{evidence_scope:{kind:'files',files:event.target.value.split('\n'),dependencies:check.evidence_scope?.kind==='files'?check.evidence_scope.dependencies:[]}})} placeholder="src/main.js"/></label>
          <label>Зависимости · тесты, настройки, импортируемые файлы<textarea aria-label="Зависимости области проверки" disabled={busy} rows={2} value={check.evidence_scope.dependencies.join('\n')} onChange={event=>updateCheck(check.id,{evidence_scope:{kind:'files',files:check.evidence_scope?.kind==='files'?check.evidence_scope.files:[],dependencies:event.target.value?event.target.value.split('\n'):[]}})} placeholder={'tests/main.test.js\npackage.json'}/></label>
          <p className="settings-help">Укажите все известные зависимости этой проверки. Будет подтверждён только снимок этих файлов. Остальной проект не сверяется. Это область доказательств, а не ограничение доступа запускаемой программы.</p>
        </>}
        <label>Лимит времени, секунд<input type="number" aria-label="Время проверки" min={1} max={120} disabled={busy} value={check.timeout} onChange={event=>updateCheck(check.id,{timeout:Number(event.target.value)})}/></label>
      </section>)}
      <button type="button" className="secondary-button" disabled={busy||value.checks.length>=8} onClick={()=>onChange({...value,checks:[...value.checks,{id:crypto.randomUUID(),purpose:'Проверка синтаксиса',program:'node',arguments:['--check','src/main.js'],cwd:'.',timeout:60}]})}><Plus size={13}/>Добавить проверку</button>
      <label className="check-row"><input type="checkbox" aria-label="Проверки после правок" disabled={busy||value.read_only||!value.checks.length} checked={value.auto_checks} onChange={event=>onChange({...value,auto_checks:event.target.checked})}/>Предлагать проверки перед завершением</label>
      <button type="button" className="secondary-button" disabled={busy||value.read_only||!value.checks.length} onClick={onRunChecks}>Запустить проверки без модели</button>
      <p className="settings-help">Нужно включённое расширение команд проекта. Каждый запуск потребует обычного подтверждения программы, аргументов и назначения.</p>
    </div>
  </details>;
}
