import {ForestSpot} from './design/ForestSpot';
import {useEffect,useRef,useState} from 'react';
import {X,Search,Stethoscope,GitBranch,Box,Square} from 'lucide-react';
import type {OptionalSettings,OptionalRequest,OptionalResult,ManagedWorktree} from '../shared/optionalTypes';
import {ChatText} from './ChatText';
import {WorkspaceAccessSettings} from './WorkspaceAccessSettings';

export function OptionalIdePanel({visible,root,path,busy,dirty,onClose,onWorking,onOpen,onUse,onWorktree}:{visible:boolean;root:string;path:string;busy:boolean;dirty:boolean;onClose:()=>void;onWorking:(value:boolean)=>void;onOpen:(path:string,line:number)=>void;onUse:(text:string)=>void;onWorktree:(id:string)=>Promise<void>}) {
  const dialog=useRef<HTMLDialogElement>(null),locked=useRef(false);
  const [settings,setSettings]=useState<OptionalSettings|null>(null),[tab,setTab]=useState<'research'|'lsp'|'worktrees'|'container'>('research');
  const [working,setWorking]=useState(false),[notice,setNotice]=useState(''),[question,setQuestion]=useState('');
  const [result,setResult]=useState<OptionalResult|null>(null),[trees,setTrees]=useState<ManagedWorktree[]>([]),[name,setName]=useState('Пробная задача');
  const [confirmation,setConfirmation]=useState<{kind:'create'|'remove';id?:string}|null>(null),[saved,setSaved]=useState('');
  useEffect(()=>{if(visible){dialog.current?.showModal();void window.lca.optionalSettings().then(r=>{if(r.ok){setSettings(r.settings);setSaved(JSON.stringify(r.settings));if(r.warning)setNotice(r.warning);}else setNotice(r.error);});}else dialog.current?.close();},[visible]);
  useEffect(()=>{setResult(null);setTrees([]);setConfirmation(null);},[root]);
  const changed=!!settings&&JSON.stringify(settings)!==saved;
  async function save() {
    if(!settings||locked.current)return;locked.current=true;setWorking(true);onWorking(true);
    try{const r=await window.lca.configureOptionalIde(settings);if(!r.ok)throw Error(r.error);setSaved(JSON.stringify(r.settings));setNotice('Настройки сохранены. Возможности запускаются только по вашему действию.');}
    catch(e){setNotice(String(e instanceof Error?e.message:e));}
    finally{locked.current=false;setWorking(false);onWorking(false);}
  }
  async function run(request:OptionalRequest) {
    if(locked.current||busy||!root)return null;
    locked.current=true;setWorking(true);onWorking(true);setNotice('');setResult(null);
    try{const r=await window.lca.runOptionalIde(request);setResult(r);if(!r.ok){setNotice(r.error);return null;}if(r.root!==root){setNotice('Проект изменился; результат относится к другой папке.');return null;}if(r.worktrees)setTrees(r.worktrees);if(r.notice)setNotice(r.notice);return r;}
    catch(e){setNotice(String(e instanceof Error?e.message:e));return null;}
    finally{locked.current=false;setWorking(false);onWorking(false);}
  }
  async function confirm() {
    if(!confirmation)return;
    const request:OptionalRequest=confirmation.kind==='create'?{action:'worktree_create',name,confirmed:true}:{action:'worktree_remove',id:confirmation.id!,confirmed:true};
    setConfirmation(null);if(await run(request))await run({action:'worktree_list'});
  }
  const disabled=busy||working,ready=!!root&&!changed&&!disabled;
  const tabs=[{id:'research',name:'Исследователь',icon:Search},{id:'lsp',name:'Диагностика',icon:Stethoscope},{id:'worktrees',name:'Рабочие копии',icon:GitBranch},{id:'container',name:'Изоляция',icon:Box}] as const;
  return <dialog ref={dialog} className="optional-ide-dialog" aria-label="Дополнительные возможности IDE" onCancel={e=>{e.preventDefault();onClose();}}>
    <header><div><span className="eyebrow">LESHY · IDE</span><h2>Инструменты для сложных задач</h2><p>Выберите нужное. По умолчанию всё выключено.</p></div><ForestSpot kind={tab==='research'?'archive':tab==='lsp'?'birch':tab==='worktrees'?'fern':'mushrooms'}/><button className="icon-button" aria-label="Закрыть возможности IDE" onClick={onClose}><X size={18}/></button></header>
    <nav className="extension-tabs" aria-label="Дополнительные инструменты">{tabs.map(item=><button key={item.id} aria-pressed={tab===item.id} onClick={()=>{setTab(item.id);setResult(null);setConfirmation(null);}} disabled={working}><item.icon size={16}/>{item.name}</button>)}</nav>
    <div className="optional-ide-content">
    <WorkspaceAccessSettings root={root} busy={disabled}/>
    {!root&&<p role="status">Сначала выберите папку проекта.</p>}
    {notice&&<p className="settings-notice" role="status">{notice}</p>}
    {!settings?<p>Загружаем настройки…</p>:<>
      <label className="check-row"><input type="checkbox" aria-label={`Включить ${tab}`} disabled={disabled} checked={settings[tab].enabled} onChange={e=>setSettings({...settings,[tab]:{...settings[tab],enabled:e.target.checked}})}/>Включить: {tabs.find(t=>t.id===tab)?.name}</label>
      {tab==='research'&&<>
        <p className="settings-help">Отдельный взгляд на код без записи и команд. Основная модель делает один запрос по 6 фрагментам, максимум 12 000 символов. История чата не отправляется. Исследование занимает общий слот модели.</p>
        <div className="field-grid"><label>Предел времени, секунд<input aria-label="Время исследователя" type="number" min={10} max={120} disabled={disabled} value={settings.research.seconds} onChange={e=>setSettings({...settings,research:{...settings.research,seconds:Number(e.target.value)}})}/></label><label>Предел ответа, токенов<input aria-label="Токены исследователя" type="number" min={256} max={2048} step={256} disabled={disabled} value={settings.research.max_tokens} onChange={e=>setSettings({...settings,research:{...settings.research,max_tokens:Number(e.target.value)}})}/></label></div>
        <label>Что изучить?<textarea aria-label="Вопрос исследователю" rows={3} maxLength={2000} value={question} disabled={disabled} onChange={e=>setQuestion(e.target.value)} placeholder="Например: где формируется ответ агента и что мешает отмене?"/></label>
        <button disabled={!ready||!settings.research.enabled||!question.trim()} onClick={()=>void run({action:'research',query:question})}>Исследовать · один запрос</button>
        {result?.ok&&result.text&&<section className="optional-result"><b>{result.complete?'Отчёт исследователя':'Ответ ограничен — исследование неполное'}</b><ChatText text={result.text}/><small>Запросов: {result.requests} · источники: {result.source_chars} символов · {result.elapsed_ms} мс {result.usage&&Object.keys(result.usage).length>0?'· usage: '+JSON.stringify(result.usage):''}</small><div className="optional-sources">{result.sources?.map(s=><button key={s.path} onClick={()=>{onClose();onOpen(s.path,s.start_line);}}>{s.path}:{s.start_line}–{s.end_line}</button>)}</div><button onClick={()=>{onUse('Исследование (перепроверь перед изменениями):\n'+result.text);onClose();}}>Добавить вывод к задаче</button></section>}
      </>}
      {tab==='lsp'&&<>
        <p className="settings-help">Используется установленный вами языковой сервер. Укажите его исполняемый файл и аргументы. Запуск сервера выполняется с вашими правами. Леший принимает только диагностику; запросы правок и команд от сервера отклоняются.</p>
        <label>Программа LSP<input aria-label="Программа LSP" disabled={disabled} value={settings.lsp.program} placeholder="pyright-langserver или node" onChange={e=>setSettings({...settings,lsp:{...settings.lsp,program:e.target.value}})}/></label>
        <label>Аргументы · каждый с новой строки<textarea aria-label="Аргументы LSP" rows={3} disabled={disabled} value={settings.lsp.arguments.join('\n')} onChange={e=>setSettings({...settings,lsp:{...settings.lsp,arguments:e.target.value?e.target.value.split('\n'):[]}})}/></label>
        <div className="field-grid"><label>Язык<input aria-label="Язык LSP" disabled={disabled} value={settings.lsp.language} onChange={e=>setSettings({...settings,lsp:{...settings.lsp,language:e.target.value}})}/></label><label>Ожидать до, секунд<input aria-label="Время LSP" type="number" min={2} max={60} disabled={disabled} value={settings.lsp.seconds} onChange={e=>setSettings({...settings,lsp:{...settings.lsp,seconds:Number(e.target.value)}})}/></label></div>
        <p>Выбранный файл: <code>{path||'откройте файл в редакторе'}</code>{dirty?' · есть несохранённые правки':''}</p><button disabled={!ready||!settings.lsp.enabled||!path||dirty} onClick={()=>void run({action:'diagnostics',path})}>Проверить сохранённый файл</button>
        {result?.ok&&result.diagnostics&&<section className="optional-result"><b>{result.stale?'Файл изменился — повторите диагностику':`Диагностик: ${result.diagnostics.length}`}</b><small>{result.elapsed_ms} мс {result.truncated?'· показаны первые 200':''}</small>{!result.diagnostics.length&&<p>Сервер прислал пустой список. Это диагностика одного файла, а не тестирование проекта.</p>}{result.diagnostics.map((d,i)=><button className="optional-diagnostic" key={i} onClick={()=>{onClose();onOpen(path,d.line);}}><span>{d.severity===1?'Ошибка':d.severity===2?'Предупреждение':'Сообщение'} · {d.line}:{d.column}</span>{d.message}</button>)}</section>}
      </>}
      {tab==='worktrees'&&<>
        <p className="settings-help">Отдельная папка из текущего commit HEAD, без незакоммиченных правок и без смены ветки основной копии. До 8 копий на репозиторий. Они остаются на диске после закрытия приложения.</p>
        <label>Название новой копии<input aria-label="Название рабочей копии" maxLength={80} disabled={disabled} value={name} onChange={e=>setName(e.target.value)}/></label><div className="section-actions"><button disabled={!ready||!settings.worktrees.enabled||!name.trim()} onClick={()=>setConfirmation({kind:'create'})}>Создать рабочую копию</button><button disabled={!ready||!settings.worktrees.enabled} onClick={()=>void run({action:'worktree_list'})}>Обновить копии</button></div>
        {trees.map(tree=><section className="optional-result" key={tree.id}><b>{tree.name} · {tree.status}</b><code>{tree.path}</code><div className="section-actions"><button disabled={!ready||!settings.worktrees.enabled||tree.status!=='ready'} onClick={()=>{onClose();void onWorktree(tree.id);}}>Открыть в IDE</button><button disabled={!ready||!settings.worktrees.enabled} onClick={()=>void run({action:'worktree_diff',id:tree.id})}>Изменения</button><button disabled={!ready||!settings.worktrees.enabled} onClick={()=>setConfirmation({kind:'remove',id:tree.id})}>Удалить чистую копию</button></div></section>)}
        {result?.ok&&typeof result.diff==='string'&&<section className="optional-result"><b>Изменения {result.worktree?.name}</b><pre>{result.status||'Рабочая папка чистая'}{'\n'}{result.diff}</pre></section>}
        {confirmation&&<div className="inline-confirm" role="alert"><p>{confirmation.kind==='create'?'Создать отдельную папку из HEAD? Текущие несохранённые и незакоммиченные изменения в неё не попадут.':'Удалить эту копию? При новых файлах, правках, commits, ignored-файлах или блокировке Git откажет. Принудительного удаления нет.'}</p><button disabled={disabled} onClick={()=>void confirm()}>Подтвердить {confirmation.kind==='create'?'создание':'удаление'}</button><button disabled={disabled} onClick={()=>setConfirmation(null)}>Отмена</button></div>}
      </>}
      {tab==='container'&&<>
        <p className="settings-help">После включения все команды агента в IDE выполняются в Linux-контейнере: проект только для чтения, сеть выключена, 1 CPU, до 64 процессов. Перед каждой командой остаётся подтверждение. Команды, которым нужна запись в проект, завершатся ошибкой.</p>
        <label>Уже загруженный образ<input aria-label="Образ контейнера" disabled={disabled} value={settings.container.image} onChange={e=>setSettings({...settings,container:{...settings.container,image:e.target.value}})}/></label><label>Предел памяти, МБ<input aria-label="Память контейнера" type="number" min={128} max={2048} step={128} disabled={disabled} value={settings.container.memory_mb} onChange={e=>setSettings({...settings,container:{...settings.container,memory_mb:Number(e.target.value)}})}/></label>
        <button disabled={!ready} onClick={()=>void run({action:'container_status'})}>Проверить Docker</button><p className="settings-help">Нужен Docker с Linux containers, например через WSL2 backend. Установка, загрузка образов и включение компонентов Windows выполняются вами. WSL без контейнера не ограничивает доступ к файлам Windows. MCP и LSP запускаются отдельно от этого режима.</p>
      </>}
    </>}
    </div><footer><span>{working?'Выполняется… Закрытие панели не останавливает операцию.':changed?'Сохраните изменения перед запуском.':'Дополнительного расхода модели без запуска исследования нет.'}</span>{working&&<button onClick={()=>void window.lca.cancelOptionalIde()}><Square size={14}/>Остановить операцию</button>}<button className="primary-button" disabled={disabled||!changed} onClick={()=>void save()}>Сохранить возможности</button></footer>
  </dialog>;
}
