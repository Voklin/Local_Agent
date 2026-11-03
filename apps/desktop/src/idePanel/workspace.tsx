import {ForestSpot} from '../design/ForestSpot';
import {Plus,Settings2,ArrowUp,Square,ChevronDown,ArrowUpRight} from 'lucide-react';
import {OrnamentFrame,OrnamentDivider,WoodlandAccent} from '../design/Ornaments';
import {BrandMark} from '../BrandMark';
import {useEffect,useRef,useState} from 'react';
import {RunActivity} from './runActivity';

import type {TaskSnapshot} from '../../shared/taskTypes';
import {isTaskEvent} from '../../shared/protocol';
import {projectTaskEvent} from './sessionState';
import type {Line,Reference,SessionIdentity,PanelApproval,ModelConnection,ChatSummary,ChatSelection} from './sessionState';
import {hasRecoveryBlockers,recoveryDiagnostics} from './recoveryDiagnostics';
import {ConnectionSettings} from './connectionSettings';
import {AcceptanceSettings} from './acceptanceSettings';
import {emptyAcceptanceOptions,prepareAcceptanceOptions,acceptanceDraftForChat,canResumeInMode} from './acceptanceChecks';
import type {IdeOptions} from '../../shared/ideTypes';
type Page='conversation'|'history'|'activity'|'settings'|'checks';
const api=()=>window.lca;
function checked<T extends {ok:boolean;error?:string}>(result:T):T{if(!result.ok)throw Error(result.error||'Операция не выполнена');return result;}
function Content({text}:{text:string}){return <>{text.split(/(```[\s\S]*?```)/g).map((part,index)=>part.startsWith('```')?<pre key={index}><code>{part.replace(/^```[^\n]*\n?/,'').replace(/```$/,'')}</code></pre>:<p key={index}>{part}</p>)}</>;}

export function AgentWorkspace(){
 const [page,setPage]=useState<Page>('conversation'),[root,setRoot]=useState(''),[title,setTitle]=useState('Новая задача');
 const [messages,setMessageState]=useState<Line[]>([]),[draft,setDraft]=useState(window.neutralIdeDraft||'');
 const [references,setReferences]=useState<Reference[]>([]),[mode,setMode]=useState('agent');
 const [savedConfig,setSavedConfig]=useState<ModelConnection|null>(null);
 const [rename,setRename]=useState<{id:string;title:string}|null>(null),[deleting,setDeleting]=useState('');
 const [config,setConfig]=useState<ModelConnection|null>(null),[models,setModels]=useState<string[]>([]);
 const [history,setHistory]=useState<ChatSummary[]>([]),[filter,setFilter]=useState('');
 const [checkOptions,setCheckOptions]=useState<IdeOptions>(emptyAcceptanceOptions);
 const checkDrafts=useRef(new Map<string,IdeOptions>()),checkRef=useRef(checkOptions);
 const [busy,setBusy]=useState(false),[working,setWorking]=useState(false),[error,setError]=useState(''),[connected,setConnected]=useState(false);
 const [task,setTask]=useState<TaskSnapshot|null>(null),[approval,setApproval]=useState<PanelApproval|null>(null),[events,setEvents]=useState<string[]>([]);
 const transcript=useRef<Line[]>([]),identity=useRef<SessionIdentity>({chat:'',run:'',seq:0}),starting=useRef(false),lock=useRef(false),tail=useRef<HTMLDivElement>(null),input=useRef<HTMLTextAreaElement>(null),follow=useRef(true);
 function setMessages(next:Line[]|((current:Line[])=>Line[])){transcript.current=typeof next==='function'?next(transcript.current):next;setMessageState(transcript.current);}
 function changeChecks(value:IdeOptions){checkRef.current=value;checkDrafts.current.set(identity.current.chat,value);setCheckOptions(value);}
 async function act(work:()=>Promise<void>,propagate=false){if(lock.current){if(propagate)throw Error('Дождитесь текущего действия');return;}lock.current=true;setWorking(true);setError('');try{await work();}catch(e){setError(String(e));if(propagate)throw e;}finally{lock.current=false;setWorking(false);}}
 async function refresh(){const result:{ok:boolean;error?:string;chats:ChatSummary[]}=checked(await api().listChats('ide'));setHistory(result.chats||[]);const current=(result.chats||[]).find(chat=>chat.id===identity.current.chat);if(current)setTitle(current.title);}
 async function select(id?:string){
  const result:ChatSelection=checked(id?await api().loadChat(id,'ide'):await api().newChat('ide'));
  identity.current={chat:result.chat.id,run:result.active_run?.run_id||'',seq:result.event_seq||0};
  const local=checkDrafts.current.get(result.chat.id);changeChecks(acceptanceDraftForChat(result.chat.id,result.task?.options,local?{chatId:result.chat.id,options:local}:window.neutralIdeCheckDraft));
  setTitle(result.chat.title||'Новая задача');setMessages((result.chat.messages||[]).filter(m=>['user','assistant'].includes(m.role)&&typeof m.content==='string').map(m=>({role:m.role,text:m.content as string,id:m.message_id})));
  setMode(result.task?.options?.read_only?'ask':'agent');setTask(result.task||null);setApproval(result.approval||null);setBusy(!!result.active_run);setDraft('');setReferences([]);setEvents([]);setPage('conversation');await refresh();
 }
 async function takeEdit(){const result=checked(await api().ideEditDraft());if(result.draft){setDraft(result.draft.prompt);setReferences([result.draft.context]);setMode('agent');setPage('conversation');input.current?.focus();}}
 useEffect(()=>{
  const unsubscribe=api().onEvent(event=>{
   if(event.event==='backend_stopped'){setConnected(false);setError('Соединение с Лешим потеряно. Перезапустите Лешего и обновите панель.');return;}
   if(event.event==='ide_edit_ready'){void act(takeEdit);return;}
   if(!isTaskEvent(event))return;
   const update=projectTaskEvent(identity.current,transcript.current,event);if(!update)return;
   identity.current=update.identity;
   if(update.messages)setMessages(update.messages);
   if(update.task)setTask(update.task);
   if(update.approval!==undefined)setApproval(update.approval);
   if(update.error)setError(update.error);
   if(update.fileEvent)setEvents(lines=>[...lines,update.fileEvent!].slice(-100));
   if(update.ended){setBusy(false);void refresh().catch(e=>setError(String(e)));}
  });
  void act(async()=>{const health=checked(await api().health());setRoot(health.project||'');{const settings=checked(await api().getModelSettings());setConfig(settings);setSavedConfig(settings);}if(health.chat_id)await select(health.chat_id);else{await refresh();changeChecks(acceptanceDraftForChat('',undefined,window.neutralIdeCheckDraft));}setDraft(window.neutralIdeDraft||'');await takeEdit();setConnected(true);});
  return unsubscribe;
 },[]);
 useEffect(()=>{if(!approval)return;const previous=document.activeElement as HTMLElement|null;const node=document.querySelector<HTMLElement>('.nw-approval');node?.querySelector<HTMLButtonElement>('button')?.focus();const trap=(event:KeyboardEvent)=>{if(event.key!=='Tab')return;const buttons=[...(node?.querySelectorAll<HTMLButtonElement>('button:not(:disabled)')||[])];if(!buttons.length)return;const index=buttons.indexOf(document.activeElement as HTMLButtonElement);if(event.shiftKey&&index<=0){event.preventDefault();buttons.at(-1)?.focus();}else if(!event.shiftKey&&index===buttons.length-1){event.preventDefault();buttons[0].focus();}};document.addEventListener('keydown',trap);return()=>{document.removeEventListener('keydown',trap);previous?.focus();};},[approval]);
 useEffect(()=>{window.dispatchEvent(new CustomEvent('neutral-draft',{detail:draft}));},[draft]);
 useEffect(()=>{if(connected)window.dispatchEvent(new CustomEvent('neutral-check-draft',{detail:{chatId:identity.current.chat,options:checkOptions}}));},[checkOptions,connected]);
 useEffect(()=>{if(follow.current)tail.current?.scrollIntoView({block:'end'});},[messages]);
 useEffect(()=>{const escape=(event:KeyboardEvent)=>{if(event.key==='Escape'&&!approval)setPage('conversation');};window.addEventListener('keydown',escape);return()=>window.removeEventListener('keydown',escape);},[approval]);
 async function send(resume=false,checksOnly=false){const effectiveChecksOnly=checksOnly||(resume&&task?.options?.checks_only===true);if(starting.current||busy||working||!connected||(!effectiveChecksOnly&&!savedConfig?.model)||(!resume&&!checksOnly&&!draft.trim()))return;
  if(hasRecoveryBlockers(task)){setPage('activity');setError('Сначала проверьте незавершённые действия.');return;}
  if(resume&&!canResumeInMode(task?.options,mode)){setPage('activity');setError('Для продолжения этой задачи переключитесь в Agent: её сохранённые проверки могут запускать команды.');return;}
  let options;try{options=resume?undefined:prepareAcceptanceOptions(checkRef.current,mode,checksOnly);}catch(e){setError(String(e));setPage('checks');return;}
  starting.current=true;setBusy(true);setError('');
  try{
   if(!identity.current.chat){const result=checked(await api().newChat('ide'));identity.current.chat=result.chat.id;checkDrafts.current.delete('');changeChecks({...checkRef.current});}
   const run=crypto.randomUUID().replaceAll('-','');identity.current.run=run;identity.current.seq=0;
   const text=draft.trim();let prompt=checksOnly?'Выполнить заданные проверки проекта':mode==='plan'?'Исследуй проект и составь план реализации с файлами и проверками. Не выполняй изменения.\n\n'+text:text;
   if(!checksOnly&&references.length)prompt+='\n\nКонтекст редактора: '+references.map(ref=>`${ref.path}:${ref.start}-${ref.end}`).join(', ');
   setMessages(lines=>[...lines,{role:'user',text:resume?'Продолжить задачу':checksOnly?'Выполнить заданные проверки проекта':text}]);setPage(checksOnly?'activity':'conversation');
   checked(await api().startTask(prompt,resume,'ide',options,run));if(!checksOnly&&!resume){setDraft('');setReferences([]);}
  }catch(e){setError(String(e));setBusy(false);identity.current.run='';}finally{starting.current=false;}
 }
 async function decide(decision:'apply'|'reject'|'cancel'){const current=approval;if(!current)return;await act(async()=>{checked(await api().resolveApproval(current.run_id,current.approval_id,decision));setApproval(null);});}
 async function attach(){await act(async()=>{const ref=checked(await api().ideEditorContext());setReferences(items=>[...items.filter(item=>item.path!==ref.path),{path:ref.path!,start:ref.start!,end:ref.end!}].slice(-8));});}
 return <main className="nw" data-testid="new-agent-workspace">
  <header className="nw-header"><BrandMark size={28}/><div><span className="nw-kicker">ЛЕШИЙ / LESHY</span><strong title={root}>{root.split(/[\\/]/).pop()||'Редактор'}</strong></div><button aria-label="Новая задача" disabled={busy||working} onClick={()=>void act(()=>select())}><Plus size={18}/></button><button aria-label="Настройки подключения" aria-pressed={page==='settings'} onClick={()=>setPage(page==='settings'?'conversation':'settings')}><Settings2 size={18}/></button></header>
  <nav className="nw-nav" aria-label="Разделы агента">{([['conversation','Диалог'],['history','История'],['activity','Работа']] as [Page,string][]).map(([value,label])=><button key={value} aria-current={page===value?'page':undefined} onClick={()=>setPage(value)}>{label}{value==='activity'&&busy&&<i/>}</button>)}</nav>
  {error&&<div className="nw-error" role="alert"><span>{error}</span><button aria-label="Закрыть сообщение" onClick={()=>setError('')}>×</button></div>}
  {page==='conversation'&&<><section className="nw-transcript" aria-label="Переписка" onScroll={e=>{const n=e.currentTarget;follow.current=n.scrollHeight-n.scrollTop-n.clientHeight<80;}}>
   {messages.length===0?<div className="nw-start"><WoodlandAccent className="nw-woodland"/><BrandMark size={40}/><h1>ЛЕШИЙ</h1><span className="nw-wordmark">LESHY</span><OrnamentDivider/><p>Агент работает с папкой этого окна. Опишите результат или добавьте файл из редактора.</p><div>{['Объясни устройство проекта','Найди возможные ошибки','Предложи план изменений'].map(text=><button key={text} onClick={()=>{setDraft(text);input.current?.focus();}}>{text}<ArrowUpRight size={15} aria-hidden="true"/></button>)}</div></div>:<><h1 className="nw-title">{title}</h1>{messages.map((line,index)=><article className={'nw-message '+line.role} key={line.id||index}><small>{line.role==='user'?'ВЫ':'LESHY'}</small><Content text={line.text}/></article>)}</>}
   <div ref={tail}/></section>
   <section className="nw-compose" aria-label="Новый запрос"><OrnamentFrame/><div className="nw-context">{references.map(ref=><button key={ref.path} title="Удалить ссылку из запроса" onClick={()=>setReferences(items=>items.filter(item=>item!==ref))}>{ref.path}:{ref.start} ×</button>)}</div><textarea ref={input} aria-label="Задача агенту" value={draft} disabled={busy||working||!connected} placeholder="Опишите задачу…" onChange={e=>setDraft(e.target.value)} onKeyDown={e=>{if(e.key==='Enter'&&!e.shiftKey&&!e.nativeEvent.isComposing){e.preventDefault();void send();}}}/><div className="nw-compose-actions"><select aria-label="Режим агента" disabled={busy} value={mode} onChange={e=>setMode(e.target.value)}><option value="agent">Agent</option><option value="ask">Ask</option><option value="plan">Plan</option></select><button disabled={busy||working} onClick={()=>void attach()} title="Ссылка на активный файл и выделение">+ Файл</button><button className="nw-send" aria-label={busy?'Остановить':'Отправить'} disabled={working||!connected||(!busy&&(!draft.trim()||!savedConfig?.model))} onClick={()=>busy?void act(async()=>{checked(await api().cancelTask(identity.current.run));}):void send()}>{busy?<Square size={15}/>:<ArrowUp size={18}/>} </button></div><button className="nw-model" onClick={()=>setPage('settings')}><span title={savedConfig?.model}>{savedConfig?.model||'Подключить модель'}</span><ChevronDown size={14} aria-hidden="true"/></button><button className="nw-checks-trigger" aria-label="Настроить проверки" onClick={()=>setPage('checks')}>Проверки результата{checkOptions.checks.length?` · ${checkOptions.checks.length}`:''}{checkOptions.auto_checks&&checkOptions.checks.length?' · авто':''}</button></section></>}
  {page==='history'&&<section className="nw-page"><header className="nw-page-heading"><h1>Разговоры проекта</h1><ForestSpot kind="archive"/></header><input aria-label="Найти разговор" placeholder="Поиск по названию" value={filter} onChange={e=>setFilter(e.target.value)}/>{history.filter(item=>(item.title||'').toLowerCase().includes(filter.toLowerCase())).map(item=><div className="nw-history-row" key={item.id}><button className="nw-history-item" disabled={busy||working} onClick={()=>void act(()=>select(item.id))}><strong>{item.title||'Без названия'}</strong><span>{item.id===identity.current.chat?'Текущий':'Открыть →'}</span></button><div className="nw-row-actions"><button disabled={busy||working} onClick={()=>{setRename({id:item.id,title:item.title});setDeleting('');}}>Название</button><button disabled={busy||working} onClick={()=>{setDeleting(item.id);setRename(null);}}>Удалить</button></div>{rename&&rename.id===item.id&&<form onSubmit={e=>{e.preventDefault();void act(async()=>{checked(await api().renameChat(item.id,rename.title,'ide'));setRename(null);await refresh();});}}><input aria-label="Новое название" autoFocus value={rename.title} maxLength={120} onChange={e=>setRename({...rename,title:e.target.value})}/><button type="submit" disabled={working||!rename.title.trim()}>Сохранить название</button><button type="button" onClick={()=>setRename(null)}>Отмена</button></form>}{deleting===item.id&&<div className="nw-confirm"><p>Удалить «{item.title}»? Переписка будет удалена. Файлы проекта останутся.</p><button disabled={working} onClick={()=>void act(async()=>{checked(await api().deleteChat({chat_id:item.id,mode:'ide',confirmed:true}));checkDrafts.current.delete(item.id);setDeleting('');if(identity.current.chat===item.id){identity.current={chat:'',run:'',seq:0};changeChecks(emptyAcceptanceOptions());setMessages([]);setTask(null);setTitle('Новая задача');}await refresh();})}>Подтвердить удаление</button><button onClick={()=>setDeleting('')}>Отмена</button></div>}</div>)}{!history.length&&<div className="nw-empty"><ForestSpot kind="mushrooms"/><OrnamentDivider/><p>Здесь появятся сохранённые задачи этой папки.</p></div>}{history.length>0&&!history.some(item=>(item.title||'').toLowerCase().includes(filter.toLowerCase()))&&<p role="status">По этому названию ничего не найдено.</p>}</section>}
  {page==='activity'&&<RunActivity task={task} busy={busy||working} events={events} onConfigureChecks={()=>setPage('checks')} onCopy={()=>api().copyTaskDiagnostics(JSON.stringify(recoveryDiagnostics(task),null,2)).then(result=>{checked(result);})} onResume={()=>void send(true)} onOpen={path=>void act(async()=>{checked(await api().ideOpenFile(path));})} onResolve={(item,resolution)=>act(async()=>{if(!task?.journal_id)throw Error('Журнал задачи недоступен; скопируйте диагностику');const result=checked(await api().resolveToolRecovery({chat_id:identity.current.chat,journal_id:task.journal_id,message_index:item.message_index,call_id:item.call_id,resolution}));setTask(result.task||task);},true)}/>}
  {page==='settings'&&<ConnectionSettings config={config} savedConfig={savedConfig} models={models} locked={working||busy} onChange={setConfig} onSave={()=>void act(async()=>{if(!config)return;const next={...config};if(!next.api_key)delete next.api_key;checked(await api().configureModel(next));const settings=checked(await api().getModelSettings());setConfig(settings);setSavedConfig(settings);setPage('conversation');})} onList={()=>void act(async()=>{const result:{ok:boolean;error?:string;models:(string|{id:string})[]}=checked(await api().listModels(config));setModels((result.models||[]).map(model=>typeof model==='string'?model:model.id));})}/>}
  {page==='checks'&&<AcceptanceSettings value={checkOptions} mode={mode} busy={busy||working} connected={connected} onChange={changeChecks} onRun={()=>void send(false,true)} onBack={()=>setPage('conversation')}/>}
  <footer className="nw-footer"><i className={connected?'online':''}/>{busy?'Работаю':!connected?'Нет соединения':mode==='agent'?'Правки — с подтверждением':'Только чтение'}<button onClick={()=>setPage('activity')}>Действия ↗</button></footer>
  {approval&&<div className="nw-approval" role="dialog" aria-modal="true" aria-label="Подтверждение действия"><h2>{approval.kind==='context'?'Отправка исходников':'Подтверждение действия'}</h2><p>{approval.path||approval.kind}</p>{error&&<p role="alert" className="nw-error">{error}</p>}<pre className="nw-diff">{approval.diff?approval.diff.split('\n').map((line:string,index:number)=><span key={index} className={line.startsWith('+++')||line.startsWith('---')||line.startsWith('@@')?'nw-diff-heading':line.startsWith('+')?'nw-diff-add':line.startsWith('-')?'nw-diff-remove':''}>{line+'\n'}</span>):JSON.stringify(approval,null,2)}</pre><div>{approval.path&&!['context','mcp','command'].includes(approval.kind||'')&&<button disabled={working} onClick={()=>void act(async()=>{checked(await api().idePreviewDiff(approval.path));})}>Diff в редакторе</button>}<button disabled={working} onClick={()=>void decide('reject')}>Отклонить</button><button disabled={working} onClick={()=>void decide('cancel')}>Остановить задачу</button><button className="nw-primary" disabled={working} onClick={()=>void decide('apply')}>Применить</button></div></div>}
 </main>;
}
