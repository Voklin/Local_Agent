import { useEffect, useRef, useState } from 'react';
import { Bot, ChevronDown, Code2, FileCode2, Folder, FolderOpen, GitBranch, History, Play, Plus, Settings2, ShieldCheck, Square, SquareTerminal } from 'lucide-react';

type FileItem = { name: string; path: string; kind: 'file' | 'directory' };
type Message = { role: string; text: string };
type ChatSummary = { id: string; title: string };
const greeting: Message[] = [{role: 'assistant', text: 'Выберите папку проекта, укажите сервер и модель. Я могу изучать и изменять файлы проекта. Перед записью каждого файла вы увидите diff для подтверждения.'}];

export default function App() {
  const [project, setProject] = useState('Выберите проект');
  const [root, setRoot] = useState('');
  const [directory, setDirectory] = useState('.');
  const [files, setFiles] = useState<FileItem[]>([]);
  const [selectedFile, setSelectedFile] = useState('');
  const [fileText, setFileText] = useState('');
  const [health, setHealth] = useState('Подключение к Python Core…');
  const [prompt, setPrompt] = useState('');
  const [nav, setNav] = useState('Explorer');
  const [chat, setChat] = useState<Message[]>(greeting);
  const [chats, setChats] = useState<ChatSummary[]>([]);
  const [busy, setBusy] = useState(false);
  const [approval, setApproval] = useState<CoreEvent | null>(null);
  const [deciding, setDeciding] = useState(false);
  const [task, setTask] = useState<any>(null);
  const [logs, setLogs] = useState<string[]>([]);
  const [baseUrl, setBaseUrl] = useState('http://127.0.0.1:1234/v1');
  const [model, setModel] = useState('');
  const [apiKey, setApiKey] = useState('');
  const [models, setModels] = useState<string[]>([]);
  const [configuring, setConfiguring] = useState(false);
  const chatId = useRef('');
  const runId = useRef('');
  const active = useRef(false);
  const selectedRef = useRef('');
  const messagesEnd = useRef<HTMLDivElement>(null);

  function report(text: string) { setLogs(l => [...l.slice(-99), text]); }
  async function refreshChats() {
    const r = await window.lca.listChats();
    if (r.ok) setChats(r.chats);
  }
  useEffect(() => {
    window.lca.health().then(r => setHealth(r.ok ? 'Python Core подключён' : r.error)).catch(e => setHealth(String(e)));
    return window.lca.onEvent(e => {
      if (e.event === 'backend_stopped') {
        setHealth('Python Core остановлен. Выберите проект заново.');
        setBusy(false); active.current = false; setApproval(null); setRoot(''); setFiles([]);
        setSelectedFile(''); selectedRef.current = ''; setProject('Выберите проект');
        chatId.current = ''; runId.current = ''; setTask(null); setChats([]); return;
      }
      if (e.chat_id !== chatId.current || (runId.current && e.run_id !== runId.current)) return;
      if (e.event === 'chat') setChat(c => [...c, {role: e.role, text: e.text}]);
      if (e.event === 'result') setChat(c => c.at(-1)?.role === 'user' ? [...c, {role:'assistant', text:e.text}] : c);
      if (e.event === 'log') report(e.text);
      if (e.event === 'failed') { setChat(c => [...c, {role: 'system', text: e.text}]); report(e.text); }
      if (e.event === 'task') setTask(e.task);
      if (e.event === 'progress') setHealth(`Агент работает · инструменты ${e.count}/${e.maximum}`);
      if (e.event === 'approval') { setApproval(e); setDeciding(false); }
      if (e.event === 'change') {
        report(`${e.change.status}: ${e.change.path}`);
        if (e.change.status === 'applied' && e.change.path === selectedRef.current)
          void window.lca.readFile(selectedRef.current).then(r => { if (r.ok) setFileText(r.content); });
      }
      if (e.event === 'task_end') {
        setBusy(false); active.current = false; setApproval(null); runId.current = '';
        setHealth('Python Core подключён'); void refreshChats();
      }
    });
  }, []);
  useEffect(() => { messagesEnd.current?.scrollIntoView({behavior: 'smooth'}); }, [chat]);

  async function refreshFiles(path = '.') {
    const r = await window.lca.listFiles(path);
    if (r.ok) { setFiles(r.items); setDirectory(path); } else report(r.error);
  }
  async function chooseProject() {
    if (active.current) return;
    const r = await window.lca.chooseProject();
    if (r.canceled) return;
    if (!r.ok) { report(r.error); return; }
    setRoot(r.root); setProject(r.name); setSelectedFile(''); selectedRef.current = '';
    setChat(greeting); chatId.current = ''; setTask(null);
    await refreshFiles('.'); await refreshChats();
  }
  async function openFile(item: FileItem) {
    if (item.kind === 'directory') { await refreshFiles(item.path); return; }
    const r = await window.lca.readFile(item.path);
    if (r.ok) { setSelectedFile(item.path); selectedRef.current = item.path; setFileText(r.content); }
    else report(r.error);
  }
  async function selectChat(id?: string) {
    if (active.current) return;
    const r = id ? await window.lca.loadChat(id) : await window.lca.newChat();
    if (!r.ok) { report(r.error); return; }
    chatId.current = r.chat.id; runId.current = ''; setTask(r.task);
    setChat(r.chat.messages.filter((m: any) => typeof m.content === 'string' && ['user','assistant'].includes(m.role)).map((m: any) => ({role:m.role, text:m.content})));
    await refreshChats();
    return r.chat.id as string;
  }
  async function configure() {
    const r = await window.lca.configureModel({base_url: baseUrl, model, api_key: apiKey});
    if (!r.ok) throw new Error(r.error);
  }
  async function discoverModels() {
    setConfiguring(true);
    try {
      await configure();
      const r = await window.lca.listModels();
      if (!r.ok) throw new Error(r.error);
      setModels(r.models);
      if (!r.models.includes(model)) setModel(r.models[0] || '');
      report(r.models.length ? `Найдено моделей: ${r.models.length}` : 'Сервер доступен, но список моделей пуст');
    } catch (e) { report(String(e)); }
    finally { setConfiguring(false); }
  }
  async function sendPrompt(resume = false) {
    const value = prompt.trim();
    if (active.current || !root || !model || (!resume && !value)) return;
    // Block repeated clicks before the first IPC round trip.
    active.current = true; setBusy(true);
    try {
      await configure();
      if (!chatId.current) {
        const r = await window.lca.newChat();
        if (!r.ok) throw new Error(r.error);
        chatId.current = r.chat.id;
      }
      runId.current = '';
      setChat(c => [...c, {role:'user', text: resume ? 'Продолжить приостановленную задачу' : value}]);
      const r = await window.lca.startTask(value, resume);
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
    const r = await window.lca.cancelTask();
    if (r.ok) { setApproval(null); report('Остановка запрошена. Ожидаем завершения запроса модели.'); }
    else report(r.error);
  }
  const parent = directory.split(/[\\/]/).slice(0, -1).join('/') || '.';
  return <div className="app-shell">
    <header className="topbar"><div className="brand"><div className="brand-mark"><Code2 size={18}/></div><span>LOCAL <b>CODING AGENT</b></span><span className="version">v6.0</span></div><button className="project-pill" onClick={chooseProject} disabled={busy}><FolderOpen size={15}/>{project}<ChevronDown size={14}/></button><div className="top-spacer"/><span className="status">{health}</span><button className="icon-button" title="Настройки модели" onClick={()=>setNav('Models')}><Settings2 size={17}/></button></header>
    <div className="workarea">
      <nav className="activity-bar">{[{id:'Explorer',icon:Folder},{id:'History',icon:History},{id:'Models',icon:Settings2}].map(x=><button key={x.id} className={nav===x.id?'active':''} onClick={()=>setNav(x.id)} title={x.id}><x.icon size={19}/></button>)}</nav>
      <aside className="sidebar"><div className="side-heading"><span>{nav==='History'?'ИСТОРИЯ ЧАТОВ':nav==='Models'?'НАСТРОЙКИ МОДЕЛИ':'ФАЙЛЫ ПРОЕКТА'}</span><button onClick={()=>nav==='History'?refreshChats():refreshFiles(directory)} title="Обновить"><ChevronDown size={15}/></button></div>
        {nav==='Explorer' && <div className="file-list">{directory!=='.'&&<button className="file-row" onClick={()=>refreshFiles(parent)}>..</button>}{files.map(f=><button key={f.path} className={`file-row ${selectedFile===f.path?'selected':''}`} onClick={()=>openFile(f)}>{f.kind==='directory'?<Folder size={15}/>:<FileCode2 size={15}/>}<span>{f.name}</span></button>)}{!root&&<div className="empty-small">Выберите папку проекта</div>}</div>}
        {nav==='History' && <div className="file-list"><button className="file-row" disabled={!root||busy} onClick={()=>selectChat()}><Plus size={15}/>Новый чат</button>{chats.map(c=><button className="file-row" key={c.id} disabled={busy} onClick={()=>selectChat(c.id)}><History size={15}/><span>{c.title}</span></button>)}</div>}
        {nav==='Models' && <form className="model-settings" onSubmit={e=>{e.preventDefault();void discoverModels();}}>
          <label>URL сервера<input value={baseUrl} disabled={busy||configuring} onChange={e=>setBaseUrl(e.target.value)} placeholder="http://127.0.0.1:1234/v1"/></label>
          <label>API-ключ (если требуется)<input type="password" autoComplete="off" value={apiKey} disabled={busy||configuring} onChange={e=>setApiKey(e.target.value)}/></label>
          <button className="primary-button" disabled={busy||configuring}>{configuring?'Подключение…':'Загрузить модели'}</button>
          <label>Имя модели<input list="model-names" value={model} disabled={busy||configuring} onChange={e=>setModel(e.target.value)} placeholder="Выберите или введите ID"/><datalist id="model-names">{models.map(m=><option value={m} key={m}/>)}</datalist></label>
          <p>Настройки действуют в текущем сеансе. Ключ остаётся в памяти приложения.</p>
        </form>}
        <div className="sidebar-footer"><div className="project-status"><GitBranch size={14}/><span>{root?'Локальный проект':'Проект не выбран'}</span></div></div>
      </aside>
      <main className="main-panel"><div className="editor-tabs"><div className="tab active"><FileCode2 size={14}/>{selectedFile.split(/[\\/]/).pop()||'Welcome'}</div></div><div className="editor-area">{selectedFile?<><div className="breadcrumbs">{selectedFile}</div><pre className="code-view">{fileText}</pre></>:<div className="welcome"><div className="welcome-logo"><Code2 size={28}/></div><h1>Agent Studio</h1><p>Рабочее пространство Local Coding Agent</p><div className="welcome-actions"><button onClick={chooseProject} disabled={busy}><FolderOpen size={16}/>Открыть проект</button><button onClick={()=>setNav('Models')}><Settings2 size={16}/>Настроить модель</button></div><div className="migration-note"><ShieldCheck size={17}/><span><b>Контроль изменений</b><br/>Агент покажет diff и запросит разрешение перед записью каждого файла.</span></div></div>}</div>
        <div className="bottom-panel"><div className="bottom-tabs"><span className="bottom-tab active"><SquareTerminal size={14}/>ВЫВОД</span></div><div className="output-log">{logs.length?logs.map((l,i)=><pre key={i}>{l}</pre>):<div className="output-line dim">События агента появятся здесь.</div>}</div></div>
      </main>
      <aside className="agent-panel"><div className="agent-heading"><div><Bot size={17}/><b>AI Agent</b></div><button className="icon-button" title="Новый чат" disabled={!root||busy} onClick={()=>selectChat()}><Plus size={16}/></button></div><div className="agent-context"><span className="context-chip"><Folder size={13}/>{project}</span><span className="context-chip">Модель: {model||'не выбрана'}</span>{task&&<div className="task-card"><b>{task.status==='paused'?'Приостановлена':task.status==='completed'?'Завершена':'Выполняется'}</b><span>{task.last_event}</span>{task.status==='paused'&&!busy&&<button onClick={()=>sendPrompt(true)}>Продолжить задачу</button>}</div>}</div>
        <div className="chat-messages">{chat.map((m,i)=><div className={`message ${m.role}`} key={i}>{m.role==='assistant'&&<div className="avatar"><Bot size={14}/></div>}<div className="message-content">{m.text}</div></div>)}<div ref={messagesEnd}/></div>
        <div className="composer"><textarea aria-label="Задача агенту" value={prompt} disabled={busy} onChange={e=>setPrompt(e.target.value)} onKeyDown={e=>{if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();void sendPrompt();}}} placeholder={!root?'Сначала выберите проект':!model?'Укажите модель в настройках':'Опишите задачу…'}/><div className="composer-footer"><span>{busy?'Агент работает…':'Enter для отправки'}</span>{busy?<button className="send-button" title="Остановить" onClick={cancel}><Square size={14}/></button>:<button className="send-button" title="Отправить" onClick={()=>sendPrompt()} disabled={!prompt.trim()||!root||!model||configuring}><Play size={14}/></button>}</div></div><div className="agent-foot"><ShieldCheck size={13}/> Подтверждение перед записью</div>
      </aside>
    </div><footer className="statusbar"><span><GitBranch size={12}/>{project}</span><span><ShieldCheck size={12}/>Файлы ограничены папкой проекта</span><span className="statusbar-right">Electron · React · Python</span></footer>
    {approval&&<div className="modal-backdrop"><section className="approval-dialog" role="dialog" aria-modal="true" aria-labelledby="approval-title"><h2 id="approval-title">{approval.exists?'Изменение файла':'Новый файл'}: {approval.path}</h2><p>Проверьте изменения перед записью.</p><pre>{approval.diff||'Текстовых изменений нет'}</pre><div className="approval-actions"><button disabled={deciding} onClick={()=>decide('cancel')}>Отменить задачу</button><button disabled={deciding} onClick={()=>decide('reject')}>Отклонить изменение</button><button className="primary-button" disabled={deciding} onClick={()=>decide('apply')}>Применить изменение</button></div></section></div>}
  </div>;
}
