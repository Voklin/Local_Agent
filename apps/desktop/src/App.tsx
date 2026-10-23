import { useEffect, useRef, useState } from 'react';
import { Bot, ChevronDown, Code2, FileCode2, Folder, FolderOpen, GitBranch, History, Play, Plus, Settings2, ShieldCheck, Square, SquareTerminal, Search, Brain, Pencil } from 'lucide-react';
import { MemoryPanel } from './MemoryPanel';
import { ChatText } from './ChatText';
import { ProjectSearch } from './ProjectSearch';
import { EditorPanel, type EditorHandle } from './EditorPanel';
import { ModelSettings, defaultGeneration, type GenerationSettings } from './ModelSettings';
import { VoicePanel, type WorkspaceMode } from './VoicePanel';
import { TaskProgress, type TaskSnapshot } from './TaskProgress';

type FileItem = { name: string; path: string; kind: 'file' | 'directory' };
type Message = { role: string; text: string; id?: string; streaming?: boolean };
type ChatSummary = { id: string; title: string };
const greeting: Message[] = [{role: 'assistant', text: 'Выберите папку проекта, укажите сервер и модель. Я могу изучать и изменять файлы проекта. Перед записью каждого файла вы увидите diff для подтверждения.'}];

export default function App() {
  const [mode, setMode] = useState<WorkspaceMode>('chat');
  const modeRef = useRef<WorkspaceMode>('chat');
  const [showProgress, setShowProgress] = useState(false);
  const [project, setProject] = useState('Выберите проект');
  const [root, setRoot] = useState('');
  const [directory, setDirectory] = useState('.');
  const [files, setFiles] = useState<FileItem[]>([]);
  const [selectedFile, setSelectedFile] = useState('');
  const editorRef = useRef<EditorHandle>(null);
  const [health, setHealth] = useState('Подключение к Python Core…');
  const [prompt, setPrompt] = useState('');
  const [memoryOpen,setMemoryOpen]=useState(false);
  const [renaming,setRenaming]=useState<{id:string;title:string}|null>(null);
  const [renameNotice,setRenameNotice]=useState('');
  const [renameWorking,setRenameWorking]=useState(false);
  const [atBottom,setAtBottom]=useState(true);
  const followChat=useRef(true);
  const [quickOpen,setQuickOpen]=useState(false);
  const [searchFocus,setSearchFocus]=useState(0);
  const [nav, setNav] = useState('History');
  const [chat, setChat] = useState<Message[]>([{role:'assistant', text:'Чем займёмся? Здесь можно общаться с локальной моделью без подключения папки. Для работы с проектом переключитесь в IDE.'}]);
  const [chats, setChats] = useState<ChatSummary[]>([]);
  const [busy, setBusy] = useState(false);
  const [approval, setApproval] = useState<CoreEvent | null>(null);
  const [deciding, setDeciding] = useState(false);
  const [task, setTask] = useState<TaskSnapshot | null>(null);
  const [logs, setLogs] = useState<string[]>([]);
  const [baseUrl, setBaseUrl] = useState('http://127.0.0.1:1234/v1');
  const [model, setModel] = useState('');
  const [apiKey, setApiKey] = useState('');
  const [generation, setGeneration] = useState<GenerationSettings>({...defaultGeneration});
  const [settingsOpen, setSettingsOpen] = useState(false);
  const [settingsReady, setSettingsReady] = useState(false);
  const [stopping, setStopping] = useState(false);
  const chatId = useRef('');
  const runId = useRef('');
  const active = useRef(false);
  const selectedRef = useRef('');
  const messagesEnd = useRef<HTMLDivElement>(null);

  function report(text: string) { setLogs(l => [...l.slice(-99), text]); }
  function showWarning(text: string) {
    report(text);
    setChat(c => c.some(m => m.role === 'system' && m.text === text) ? c : [...c, {role: 'system', text}]);
  }
  async function refreshChats(scope = modeRef.current) {
    const r = await window.lca.listChats(scope === 'voice' ? 'chat' : scope);
    if (scope !== modeRef.current) return;
    if (r.ok) { setChats(r.chats); (r.warnings || []).forEach(showWarning); }
    else showWarning(r.error);
  }
  useEffect(() => {
    window.lca.health().then(r => setHealth(r.ok ? 'Python Core подключён' : r.error)).catch(e => setHealth(String(e)));
    window.lca.getModelSettings().then(r => {
      if (r.ok) { setBaseUrl(r.base_url); setModel(r.model); setGeneration({...defaultGeneration, ...r.settings}); }
      else report(r.error);
    }).catch(e => report(String(e))).finally(() => setSettingsReady(true));
    void refreshChats();
    return window.lca.onEvent(e => {
      if (e.event === 'backend_stopped') {
        setHealth('Python Core остановлен. Выберите проект заново.');
        setBusy(false); setStopping(false); active.current = false; setApproval(null); setRoot(''); setFiles([]);
        setSelectedFile(''); selectedRef.current = ''; setProject('Выберите проект');
        chatId.current = ''; runId.current = ''; setTask(null); setChats([]); return;
      }
      if (e.chat_id !== chatId.current || (runId.current && e.run_id !== runId.current)) return;
      if (e.event === 'text_delta') setChat(c => {
        const index = c.findIndex(m => m.id === e.message_id);
        if (index < 0) return [...c, {role:'assistant', text:e.text, id:e.message_id, streaming:true}];
        return c.map((m, i) => i === index ? {...m, text:m.text + e.text, streaming:true} : m);
      });
      if (e.event === 'chat') setChat(c => {
        const index = e.message_id ? c.findIndex(m => m.id === e.message_id) : -1;
        const message = {role:e.role, text:e.text, id:e.message_id, streaming:false};
        return index < 0 ? [...c, message] : c.map((m, i) => i === index ? message : m);
      });
      if (e.event === 'result') setChat(c => c.at(-1)?.role === 'user' ? [...c, {role:'assistant', text:e.text}] : c);
      if (e.event === 'log') report(e.text);
      if (e.event === 'warning') showWarning(e.text);
      if (e.event === 'failed') { setChat(c => [...c, {role: 'system', text: e.text}]); report(e.text); }
      if (e.event === 'task') setTask(e.task);
      if (e.event === 'progress') setHealth(`Агент работает · инструменты ${e.count}/${e.maximum}`);
      if (e.event === 'approval') { setApproval(e); setDeciding(false); }
      if (e.event === 'change') {
        report(`${e.change.status}: ${e.change.path}${e.change.error ? ': ' + e.change.error : ''}`);
        if (e.change.status === 'error') setChat(c => [...c, {role: 'system', text: `${e.change.path}: ${e.change.error}`}]);
        if (e.change.status === 'applied' && e.change.path === selectedRef.current)
          void editorRef.current?.refresh(selectedRef.current);
      }
      if (e.event === 'task_end') {
        setBusy(false); setStopping(false); active.current = false; setApproval(null); runId.current = '';
        setChat(c => c.map(m => m.streaming ? {...m, streaming:false} : m));
        setHealth('Python Core подключён'); void refreshChats();
      }
    });
  }, []);
  useEffect(() => { if(followChat.current) messagesEnd.current?.scrollIntoView({behavior:'instant'}); }, [chat]);

  useEffect(()=>{
    function shortcuts(event:KeyboardEvent) {
      if (!(event.ctrlKey||event.metaKey) || document.querySelector('[role="dialog"]')) return;
      if(event.key.toLowerCase()==='p' || (event.shiftKey&&event.key.toLowerCase()==='f')) {
        event.preventDefault();
        const quick=event.key.toLowerCase()==='p';
        setQuickOpen(quick); setNav('Search');setSearchFocus(n=>n+1);
      }
    }
    window.addEventListener('keydown',shortcuts);
    return ()=>window.removeEventListener('keydown',shortcuts);
  },[]);
  async function openSearchFile(path:string,line:number) {
    setQuickOpen(false);
    if(modeRef.current!=='ide') await switchMode('ide');
    setNav('Search');
    const opened=await editorRef.current?.open(path,line);
    if(opened){setSelectedFile(opened);selectedRef.current=opened;}
  }
  async function refreshFiles(path = '.') {
    const r = await window.lca.listFiles(path);
    if (r.ok) { setFiles(r.items); setDirectory(path); } else report(r.error);
  }
  async function chooseProject() {
    if (active.current) return;
    if (editorRef.current?.hasDirty() && !(await window.lca.confirmEditorDiscard()).discard) return;
    const r = await window.lca.chooseProject();
    if (r.canceled) return;
    if (!r.ok) { report(r.error); return; }
    followChat.current=true;setAtBottom(true);setMemoryOpen(false);setRenaming(null);
    setMode('ide'); modeRef.current = 'ide'; setNav('Explorer');
    editorRef.current?.reset();
    setRoot(r.root); setProject(r.name); setSelectedFile(''); selectedRef.current = '';
    setChat(greeting); chatId.current = ''; setTask(null); setShowProgress(false);
    await refreshFiles('.'); await refreshChats();
  }
  async function switchMode(next: WorkspaceMode) {
    if (active.current || next === mode) return;
    followChat.current=true;setAtBottom(true);setMemoryOpen(false);setRenaming(null);
    modeRef.current = next; setMode(next); setNav(next === 'ide' ? 'Explorer' : 'History');
    chatId.current = ''; runId.current = ''; setTask(null); setApproval(null); setShowProgress(false);
    setChat(next === 'ide' ? greeting : [{role:'assistant', text:next==='voice'?'Я Мия, ваш локальный ассистент. Напишите сообщение, затем можно озвучить мой ответ.':'Новый разговор. Чем могу помочь?'}]);
    setChats([]);
    if (next !== 'voice' && (next === 'chat' || root)) await refreshChats(next);
  }
  async function openFile(item: FileItem) {
    if (item.kind === 'directory') { await refreshFiles(item.path); return; }
    const path = await editorRef.current?.open(item.path);
    if (path) { setSelectedFile(path); selectedRef.current=path; }
  }
  async function selectChat(id?: string) {
    if (active.current) return;
    const r = id ? await window.lca.loadChat(id, mode) : await window.lca.newChat(mode);
    if (!r.ok) { report(r.error); return; }
    followChat.current=true;setAtBottom(true);
    chatId.current = r.chat.id; runId.current = ''; setTask(r.task);
    setChat(r.chat.messages.filter((m: any) => typeof m.content === 'string' && ['user','assistant'].includes(m.role)).map((m: any) => ({role:m.role, text:m.content})));
    (r.warnings || []).forEach(showWarning);
    await refreshChats();
    return r.chat.id as string;
  }
  async function renameChat() {
    if(!renaming||busy||renameWorking)return;
    setRenameWorking(true);setRenameNotice('');
    try {
      const result=await window.lca.renameChat(renaming.id,renaming.title,mode==='voice'?'chat':mode);
      if(!result.ok)throw new Error(result.error);
      (result.warnings||[]).forEach(showWarning);setRenaming(null);await refreshChats();
    }catch(error){setRenameNotice(String(error));}finally{setRenameWorking(false);}
  }
  async function configure() {
    const r = await window.lca.configureModel({base_url: baseUrl, model, api_key: apiKey, settings:generation});
    if (!r.ok) throw new Error(r.error);
  }
  async function sendPrompt(resume = false, voiceText?:string) {
    const value = (voiceText??prompt).trim();
    if (active.current || !settingsReady || (mode === 'ide' && !root) || (mode === 'voice' && voiceText===undefined) || !model || (!resume && !value)) return;
    // Block repeated clicks before the first IPC round trip.
    active.current = true; setBusy(true); setStopping(false);
    try {
      await configure();
      if (!chatId.current) {
        const r = await window.lca.newChat(mode);
        if (!r.ok) throw new Error(r.error);
        chatId.current = r.chat.id;
        (r.warnings || []).forEach(showWarning);
      }
      runId.current = '';
      setChat(c => [...c, {role:'user', text: resume ? 'Продолжить приостановленную задачу' : value}]);
      const r = await window.lca.startTask(value, resume, mode);
      if (!r.ok) throw new Error(r.error);
      // Events can arrive before the start response, including task_end.
      if (active.current) runId.current = r.run_id;
      setPrompt('');
    } catch (e) {
      report(String(e)); setChat(c => [...c, {role:'system', text:String(e)}]);
      setBusy(false); active.current = false;
    }
  }
  async function decide(decision: string) {
    if (!approval || deciding) return;
    setDeciding(true);
    try {
      const r = await window.lca.resolveApproval(approval.run_id!, approval.approval_id, decision);
      if (!r.ok) report(r.error);
      else setApproval(null);
    } finally { setDeciding(false); }
  }
  async function cancel() {
    setStopping(true);
    const r = await window.lca.cancelTask();
    if (r.ok) { setApproval(null); report('Остановка запрошена'); }
    else { report(r.error); setStopping(false); }
  }
  const parent = directory.split(/[\\/]/).slice(0, -1).join('/') || '.';
  return <div className={`app-shell mode-${mode}`}>
    {quickOpen&&<div className="search-overlay" onMouseDown={e=>{if(e.target===e.currentTarget)setQuickOpen(false);}}><ProjectSearch root={root} visible quick focus={searchFocus} onClose={()=>setQuickOpen(false)} onOpen={(path,line)=>void openSearchFile(path,line)}/></div>}
    <header className="topbar"><div className="brand"><div className="brand-mark"><Code2 size={18}/></div><span>LOCAL<b>AGENT</b></span><span className="version">v6.0</span></div><button className="project-pill" onClick={chooseProject} disabled={busy}><FolderOpen size={15}/>{project}<ChevronDown size={14}/></button><div className="mode-tabs" role="tablist" aria-label="Режим работы">{(['chat','ide','voice'] as WorkspaceMode[]).map(m=><button role="tab" aria-selected={mode===m} disabled={busy} className={mode===m?'selected':''} key={m} onClick={()=>void switchMode(m)}>{m==='chat'?'Chat':m==='ide'?'IDE':'Ассистент'}</button>)}</div><div className="top-spacer"/><span className="status">{health}</span><button className="icon-button" title="Настройки модели" onClick={()=>setSettingsOpen(true)}><Settings2 size={17}/></button></header>
    <div className="workarea">
      <nav className="activity-bar">{[{id:'Explorer',icon:Folder},{id:'Search',icon:Search},{id:'History',icon:History},{id:'Memory',icon:Brain},{id:'Models',icon:Settings2}].map(x=><button key={x.id} className={(x.id==='Models'?settingsOpen:nav===x.id)?'active':''} disabled={x.id==='Memory'&&(!root||mode!=='ide')} onClick={()=>x.id==='Models'?setSettingsOpen(true):x.id==='Memory'?setMemoryOpen(true):setNav(x.id)} title={x.id==='Memory'?'Память проекта':x.id}><x.icon size={19}/></button>)}</nav>
      <aside className="sidebar"><div className="side-heading"><span>{nav==='History'?'ИСТОРИЯ ЧАТОВ':nav==='Search'?'ПОИСК ПО ПРОЕКТУ':nav==='Models'?'НАСТРОЙКИ МОДЕЛИ':'ФАЙЛЫ ПРОЕКТА'}</span><button onClick={()=>nav==='History'?refreshChats():refreshFiles(directory)} title="Обновить"><ChevronDown size={15}/></button></div>
        <ProjectSearch root={root} visible={nav==='Search'&&!quickOpen} quick={false} focus={searchFocus} onClose={()=>setNav('Explorer')} onOpen={(path,line)=>void openSearchFile(path,line)}/>
        {nav==='Explorer' && <div className="file-list">{directory!=='.'&&<button className="file-row" onClick={()=>refreshFiles(parent)}>..</button>}{files.map(f=><button key={f.path} className={`file-row ${selectedFile===f.path?'selected':''}`} onClick={()=>openFile(f)}>{f.kind==='directory'?<Folder size={15}/>:<FileCode2 size={15}/>}<span>{f.name}</span></button>)}{!root&&<div className="empty-small">Выберите папку проекта</div>}</div>}
        {nav==='History' && <div className="file-list"><button className="file-row" disabled={(mode==='ide'&&!root)||busy} onClick={()=>selectChat()}><Plus size={15}/>Новый чат</button>{chats.map(c=><div className="chat-history-row" key={c.id}><button className="file-row" disabled={busy} onClick={()=>selectChat(c.id)}><History size={15}/><span>{c.title}</span></button><button className="rename-chat icon-button" title="Переименовать чат" disabled={busy} onClick={()=>{setRenaming({id:c.id,title:c.title});setRenameNotice('');}}><Pencil size={13}/></button></div>)}</div>}
        <div className="sidebar-footer"><div className="project-status"><GitBranch size={14}/><span>{root?'Локальный проект':'Проект не выбран'}</span></div></div>
      </aside>
      <main className={mode==='ide'?'main-panel':'editor-hidden'}><EditorPanel ref={editorRef} root={root} busy={busy} visible={mode==='ide'} onActive={path=>{setSelectedFile(path);selectedRef.current=path;}} onDirty={dirty=>{void window.lca.setEditorDirty(dirty);}} onProject={()=>void chooseProject()} onModels={()=>setSettingsOpen(true)} onLog={report}/>
        <div className="bottom-panel"><div className="bottom-tabs"><span className="bottom-tab active"><SquareTerminal size={14}/>ВЫВОД</span></div><div className="output-log">{logs.length?logs.map((l,i)=><pre key={i}>{l}</pre>):<div className="output-line dim">События агента появятся здесь.</div>}</div></div>
      </main>
      {mode==='voice'?<VoicePanel conversationKey={chatId.current} completed={task?.status==='completed'} model={model} messages={chat} busy={busy} onAsk={text=>void sendPrompt(false,text)} onCancel={()=>void cancel()} onChat={()=>void switchMode('chat')}/>:<aside className="agent-panel"><div className="agent-heading"><div><Bot size={17}/><b>{mode==='chat'?'Разговор с моделью':'Агент проекта'}</b></div><button className="icon-button" title="Новый чат" disabled={(mode==='ide'&&!root)||busy} onClick={()=>selectChat()}><Plus size={16}/></button></div><div className="agent-context"><span className="context-chip"><Folder size={13}/>{mode==='chat'?'Личный чат · без файловых инструментов':project}</span><span className="context-chip">Модель: {model||'не выбрана'}</span>{task&&<button className="progress-toggle" aria-expanded={showProgress} onClick={()=>setShowProgress(!showProgress)}>Ход задачи · {task.status==='completed'?'завершена':task.status==='paused'?'приостановлена':'в работе'} <ChevronDown size={13}/></button>}</div>
        {showProgress&&task&&<div className="progress-drawer"><TaskProgress task={task} busy={busy} onResume={()=>void sendPrompt(true)}/></div>}<div className="chat-messages" onScroll={event=>{const node=event.currentTarget;const bottom=node.scrollHeight-node.scrollTop-node.clientHeight<80;followChat.current=bottom;setAtBottom(bottom);}}>{chat.map((m,i)=><div className={`message ${m.role}`} key={i}>{m.role==='assistant'&&<div className="avatar"><Bot size={14}/></div>}<div className="message-content"><ChatText text={m.text}/>{m.streaming&&<span className="streaming-caret" aria-label="Ответ генерируется">▍</span>}</div></div>)}<div ref={messagesEnd}/></div>
        {!atBottom&&<button className="follow-chat" onClick={()=>{followChat.current=true;setAtBottom(true);messagesEnd.current?.scrollIntoView({behavior:'instant'});}}>К последнему сообщению ↓</button>}
        <div className="composer"><textarea aria-label="Задача агенту" value={prompt} disabled={busy} onChange={e=>setPrompt(e.target.value)} onKeyDown={e=>{if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();void sendPrompt();}}} placeholder={mode==='ide'&&!root?'Сначала выберите проект':!model?'Укажите модель в настройках':'Опишите задачу…'}/><div className="composer-footer"><span>{stopping?'Останавливаем…':busy?'Агент работает…':'Enter для отправки'}</span>{busy?<button className="send-button" title="Остановить" disabled={stopping} onClick={cancel}><Square size={14}/></button>:<button className="send-button" title="Отправить" onClick={()=>sendPrompt()} disabled={!prompt.trim()||(mode==='ide'&&!root)||!model||!settingsReady}><Play size={14}/></button>}</div></div><div className="agent-foot"><ShieldCheck size={13}/> {mode==='ide'?'Подтверждение перед записью':'Локальная модель · история сохраняется на этом ПК'}</div>
      </aside>}
    </div><footer className="statusbar"><span><GitBranch size={12}/>{project}</span><span><ShieldCheck size={12}/>{mode==='ide'?'Файлы ограничены папкой проекта':mode==='chat'?'Chat · файловые инструменты отключены':'Ассистент · локальная озвучка'}</span><span className="statusbar-right">Electron · React · Python</span></footer>
    {memoryOpen&&root&&<MemoryPanel key={root} root={root} busy={busy} onClose={()=>setMemoryOpen(false)}/>}
    {renaming&&<div className="modal-backdrop"><section className="rename-dialog" role="dialog" aria-modal="true" aria-labelledby="rename-title"><h2 id="rename-title">Название чата</h2><form onSubmit={event=>{event.preventDefault();void renameChat();}}><input autoFocus aria-label="Название чата" value={renaming.title} maxLength={120} disabled={renameWorking} onChange={event=>setRenaming({...renaming,title:event.target.value})}/><p role="status">{renameNotice}</p><div className="settings-actions"><button type="button" disabled={renameWorking} onClick={()=>setRenaming(null)}>Отмена</button><button className="primary-button" type="submit" disabled={busy||renameWorking||!renaming.title.trim()}>Переименовать</button></div></form></section></div>}
    {settingsOpen&&settingsReady&&<ModelSettings initial={{base_url:baseUrl,model,api_key:apiKey,settings:generation}} busy={busy} onClose={()=>setSettingsOpen(false)} onSaved={config=>{setBaseUrl(config.base_url);setModel(config.model);setApiKey(config.api_key);setGeneration(config.settings);report('Настройки модели сохранены');}}/>}
    {approval&&<div className="modal-backdrop"><section className="approval-dialog" role="dialog" aria-modal="true" aria-labelledby="approval-title"><h2 id="approval-title">{approval.exists?'Изменение файла':'Новый файл'}: {approval.path}</h2><p>Проверьте изменения перед записью.</p><pre>{approval.diff||'Текстовых изменений нет'}</pre><div className="approval-actions"><button disabled={deciding} onClick={()=>decide('cancel')}>Отменить задачу</button><button disabled={deciding} onClick={()=>decide('reject')}>Отклонить изменение</button><button className="primary-button" disabled={deciding} onClick={()=>decide('apply')}>Применить изменение</button></div></section></div>}
  </div>;
}
