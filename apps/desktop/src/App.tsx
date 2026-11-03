import {OrnamentFrame,WoodlandAccent} from './design/Ornaments';
import {StudioFileTree} from './StudioFileTree';
import {ContextUsage} from './ContextUsage';
import {ApprovalDialog} from './ApprovalDialog';
import {ComposerModel,DialogFocus,InlineTools,ResizeRail,useStudioLayout} from './StudioControls';
import {saveAppearance} from './AppearanceSettings';
import { OptionalIdePanel } from './OptionalIdePanel';
import { useTaskSession,type SessionMessage as Message } from './useTaskSession';
import { isTaskEvent,type ApprovalDecision } from '../shared/protocol';
import { IdeTaskOptions,defaultIdeOptions,serializeIdeOptions,type IdeOptions } from './IdeTaskOptions';
import { WorkspaceReview } from './WorkspaceReview';
import { BrandMark } from './BrandMark';
import { Welcome } from './Welcome';
import { ConversationSidebar } from './ConversationSidebar';
import {MessageSquare,PanelLeft,PanelRight,ChevronRight,Clock3} from 'lucide-react';
import { useAppearance } from './AppearanceSettings';
import { useEffect, useRef, useState } from 'react';
import {ChevronDown,Code2,FileCode2,Folder,FolderOpen,History,Plus,Search,Check,Circle,Sparkles,Settings2,Square,SquareTerminal,X} from 'lucide-react';
import { MemoryPanel } from './MemoryPanel';
import { ChatText } from './ChatText';
import { ProjectSearch } from './ProjectSearch';
import { EditorPanel, type EditorHandle } from './EditorPanel';
import { ModelSettings, defaultGeneration, type GenerationSettings } from './ModelSettings';
import { type WorkspaceMode } from './VoicePanel';
import { TaskProgress, taskStatusLabel, type TaskRecoveryItem, type TaskRecoveryResolution } from './TaskProgress';
import { NeuralAudio } from './NeuralAudio';
import { WakeListener } from './WakeListener';

type FileItem = { name: string; path: string; kind: 'file' | 'directory' };
type ChatSummary = { id: string; title: string };
const greeting: Message[] = [];

export default function App() {
  const appearance=useAppearance();
  const studio=useStudioLayout();
  const [showHistory,setShowHistory]=useState(false);
  const historyToggle=useRef<HTMLButtonElement>(null);

  const [assistantNotices,setAssistantNotices]=useState<{id:number;title:string;text:string}[]>([]);
  const [workspaceId,setWorkspaceId]=useState('');
  const [apiProtocol,setApiProtocol]=useState('chat');
  const [mode, setMode] = useState<WorkspaceMode>(window.neutralIdeHost?'ide':'chat');
  const modeRef = useRef<WorkspaceMode>(window.neutralIdeHost?'ide':'chat');
  const [showProgress, setShowProgress] = useState(false);
  const [progressTab,setProgressTab]=useState('overview');
  const progressToggle=useRef<HTMLButtonElement>(null);
  const progressDrawer=useRef<HTMLDivElement>(null);
  const [project, setProject] = useState('Выберите проект');
  const [root, setRoot] = useState('');
  const [, setDirectory] = useState('.');
  const directoryRef=useRef('.');
  const [files, setFiles] = useState<FileItem[]>([]);
  const [selectedFile, setSelectedFile] = useState('');
  const editorRef = useRef<EditorHandle>(null);
  const [nativeDefault,setNativeDefault]=useState(false);
  const [health, setHealth] = useState('Подключение к Python Core…');
  const [agentMode,setAgentMode]=useState<'agent'|'ask'|'plan'>('agent');
  const [editorContext,setEditorContext]=useState<{path:string;start:number;end:number}[]>([]);
  async function attachEditorContext(){const result=await window.lca.ideEditorContext();if(!result.ok){showWarning(result.error||'Не удалось добавить файл');return;}setEditorContext(items=>[...items.filter(item=>item.path!==result.path),{path:result.path!,start:result.start!,end:result.end!}].slice(-8));}
  const [prompt, setPrompt] = useState(window.neutralIdeDraft||'');
  useEffect(()=>{if(!window.neutralIdeHost)return;const take=async()=>{const r=await window.lca.ideEditDraft();if(r.draft){setPrompt(r.draft.prompt);setEditorContext([r.draft.context]);setAgentMode('agent');document.querySelector<HTMLTextAreaElement>('.composer textarea')?.focus();}};void take();return window.lca.onEvent(e=>{if(e.event==='ide_edit_ready')void take();});},[]);
  useEffect(()=>{if(window.neutralIdeHost)window.dispatchEvent(new CustomEvent('neutral-draft',{detail:prompt}));},[prompt]);
  const [memoryOpen,setMemoryOpen]=useState(false);
  const [renaming,setRenaming]=useState<{id:string;title:string}|null>(null);
  const [renameNotice,setRenameNotice]=useState('');
  const [renameWorking,setRenameWorking]=useState(false);
  const [atBottom,setAtBottom]=useState(true);
  const followChat=useRef(true);
  const [quickOpen,setQuickOpen]=useState(false);
  const [searchFocus,setSearchFocus]=useState(0);
  const [nav, setNav] = useState(window.neutralIdeHost?'Explorer':'History');
  useEffect(()=>{if(mode==='ide'&&nav==='History'){setNav('Explorer');setShowHistory(true);}},[mode,nav]);
  useEffect(()=>{if(!showHistory)return;const frame=requestAnimationFrame(()=>document.querySelector<HTMLInputElement>('.studio-history #conversation-search')?.focus());const dismiss=(e:KeyboardEvent)=>{if(e.key==='Escape'&&!e.defaultPrevented&&!document.querySelector('[aria-modal="true"],dialog[open]')){e.preventDefault();setShowHistory(false);historyToggle.current?.focus();}};document.addEventListener('keydown',dismiss);return()=>{cancelAnimationFrame(frame);document.removeEventListener('keydown',dismiss);};},[showHistory]);
  const session=useTaskSession();
  const {chat,setChat,task,setTask,busy,setBusy,stopping,setStopping,chatId,runId,active}=session;
  const [chats, setChats] = useState<ChatSummary[]>([]);
  const [approval, setApproval] = useState<CoreEvent | null>(null);
  const [deciding, setDeciding] = useState(false);
  const [optionalOpen,setOptionalOpen]=useState(false);
  const [ideOptions,setIdeOptions]=useState<IdeOptions>({...defaultIdeOptions});
  const [workspaceWorking,setWorkspaceWorking]=useState(false);
  const [editorDirty,setEditorDirty]=useState(false);
  const [recoveryWorking, setRecoveryWorking] = useState(false);
  const recoveryPending = useRef(false);
  const [logs, setLogs] = useState<string[]>([]);
  const [baseUrl, setBaseUrl] = useState('http://127.0.0.1:1234/v1');
  const [model, setModel] = useState('');
  const [handoffResult,setHandoffResult]=useState('');
  const [desktopImage,setDesktopImage]=useState('');
  const [handoff,setHandoff]=useState<any>(null);
  const handoffWorking=useRef(false);
  const [toolProtocol,setToolProtocol]=useState('native');
  const [apiKey, setApiKey] = useState('');
  const [generation, setGeneration] = useState<GenerationSettings>({...defaultGeneration});
  const [settingsOpen, setSettingsOpen] = useState(false);
  const [settingsSection,setSettingsSection]=useState('connection');
  const [settingsReady, setSettingsReady] = useState(false);
  const [backgroundRuns,setBackgroundRuns]=useState<any[]>([]);
  const [selectionBusy,setSelectionBusy]=useState(false),[starting,setStarting]=useState(false);
  const selectionPending=useRef(false),startingPending=useRef(false);
  const endedRuns=useRef(new Set<string>());
  const loadingChat=useRef(''),queuedEvents=useRef<any[]>([]),eventFloor=useRef(0);
  const receiveEvent=useRef<(event:any)=>void>(()=>{});
  const anyRunning=backgroundRuns.length>0||busy;
  const navigationBusy=selectionBusy||starting||workspaceWorking||recoveryWorking;
  const selectedRef = useRef('');
  const messagesEnd = useRef<HTMLDivElement>(null);

  function restoreBackgroundRuns(runs:any[]) {
    setBackgroundRuns(rows=>Array.from(new Map([...runs,...rows].filter(r=>!endedRuns.current.has(r.run_id)).map(r=>[r.run_id,r])).values()));
  }
  function report(text: string) { setLogs(l => [...l.slice(-99), text]); }
  function showWarning(text: string) {
    report(text);
    setChat(c => c.some(m => m.role === 'system' && m.text === text) ? c : [...c, {role: 'system', text}]);
  }
  async function refreshChats(scope = modeRef.current) {
    const r = await window.lca.listChats(scope);
    if (scope !== modeRef.current) return;
    if (r.ok) { setChats(r.chats); (r.warnings || []).forEach(showWarning); }
    else showWarning(r.error);
  }
  useEffect(() => {
    window.lca.health().then(r => {setHealth(r.ok ? 'Python Core подключён' : r.error);if(window.neutralIdeHost&&r.ok){setRoot(r.project||'');setProject((r.project||'').split(/[\\/]/).pop()||'Проект');setWorkspaceId(r.project_id||'');if(r.chat_id)void selectChat(r.chat_id);}}).catch(e => setHealth(String(e)));
    window.lca.getModelSettings().then(r => {
      if (r.ok) { setApiProtocol(r.api_protocol||'chat'); setBaseUrl(r.base_url); setModel(r.model); setToolProtocol(r.tool_protocol||'native'); setGeneration({...defaultGeneration, ...r.settings}); }
      else report(r.error);
    }).catch(e => report(String(e))).finally(() => setSettingsReady(true));
    void window.lca.ideShell().then(r=>setNativeDefault(r.native_default===true));
    void refreshChats();
    void window.lca.activeRuns().then(r=>{if(r.ok)restoreBackgroundRuns(r.runs);});
    const unsubscribe=window.lca.onEvent(e=>receiveEvent.current(e));
    return unsubscribe;
  }, []);
  receiveEvent.current=e=>{
      if(window.neutralIdeHost&&['handoff','handoff_result','lola_action','lola_microphone'].includes(e.event))return;
      if(e.chat_id&&loadingChat.current===e.chat_id){queuedEvents.current.push(e);return;}
      if(e.event==='task')setBackgroundRuns(rows=>[...rows.filter(r=>r.run_id!==e.run_id),{chat_id:e.chat_id,run_id:e.run_id,title:e.task.prompt?.slice(0,65)||'Задача',mode:e.mode|| (e.task.project_root?'ide':'chat'),state:e.task.run_state,approval:e.task.run_state==='waiting_approval'}]);
      if(e.event==='task_end'){endedRuns.current.add(e.run_id);setBackgroundRuns(rows=>rows.filter(r=>r.run_id!==e.run_id));}
      if(e.event==='approval')setBackgroundRuns(rows=>rows.map(r=>r.run_id===e.run_id?{...r,approval:true}:r));
      if(e.event==='lola_microphone'){window.dispatchEvent(new CustomEvent('manual-microphone',{detail:e.active}));return;}
      if(e.event==='lola_action'){if(e.action==='settings'){setSettingsSection('voice');setSettingsOpen(true);}return;}
      if(e.event==='workspace_evidence'){if(!active.current&&e.chat_id===chatId.current&&e.task?.chat_id===chatId.current)setTask(e.task);return;}
      if(e.event==='assistant_notice'){setAssistantNotices(items=>[...items.slice(-19),{id:Date.now()+Math.random(),title:String(e.title||'Лола'),text:String(e.text||'')}]);report(String(e.title)+': '+String(e.text));return;}
      if(e.event==='change'&&e.change.status==='applied'&&e.project_root===root){void refreshFiles(directoryRef.current);if(e.change.path===selectedRef.current)void editorRef.current?.refresh(selectedRef.current);}
      if(e.event==='handoff_result'){setHandoffResult(e.source_chat);return;}
      if(e.event==='remote_error'){if(e.run_id===runId.current){setBusy(false);active.current=false;runId.current='';}report(e.text);return;}
      if(e.event==='handoff'){setHandoff(e.handoff);return;}
      if(e.event==='remote_task'&&e.mode==='voice')return;
      if(e.event==='remote_task'&&e.mode==='ide'){if(window.neutralIdeHost){void selectChat(e.chat.id,'ide');return;}if(nativeDefault)return;}
      if(e.event==='remote_task'){modeRef.current=e.mode;setMode(e.mode);setNav('History');chatId.current=e.chat.id;runId.current=e.run_id||'';setTask(null);setChat([...(e.resume?e.chat.messages.filter((m:any)=>typeof m.content==='string'&&['user','assistant'].includes(m.role)).map((m:any)=>({role:m.role,text:m.content})):[]),{role:'user',text:e.prompt}]);active.current=true;setBusy(true);return;}
      if(e.event==='desktop_artifact'){setDesktopImage(e.image);return;}
      if (e.event === 'backend_stopped') {
        setHealth('Python Core остановлен. Выберите проект заново.');
        setBackgroundRuns([]);setBusy(false); setStopping(false); active.current = false; setApproval(null); setWorkspaceId(''); setRoot(''); setFiles([]);
        setSelectedFile(''); selectedRef.current = ''; setProject('Выберите проект');
        chatId.current = ''; runId.current = ''; setTask(null); setChats([]); return;
      }
      if (e.chat_id !== chatId.current || (runId.current && e.run_id !== runId.current)) return;
      if(e.event_seq&&e.event_seq<=eventFloor.current)return;
      if(e.event_seq)eventFloor.current=e.event_seq;
      if(isTaskEvent(e)){if(!session.accepts(e))return;session.reduce(e);}

      if (e.event === 'log') report(e.text);
      if (e.event === 'warning') showWarning(e.text);
      if(e.event==='failed')report(e.text);
      if (e.event === 'progress') setHealth(`Агент работает · инструменты ${e.count}${e.maximum?'/'+e.maximum:''}`);
      if (e.event === 'approval') { setApproval(e); setDeciding(false); }
      if (e.event === 'change') {
        report(`${e.change.status}: ${e.change.path}${e.change.error ? ': ' + e.change.error : ''}`);
        if (e.change.status === 'error') setChat(c => [...c, {role: 'system', text: `${e.change.path}: ${e.change.error}`}]);
      }
      if (e.event === 'task_end') {
        setApproval(null);
        setHealth('Python Core подключён'); void refreshChats();
      }
    };
  useEffect(() => { if(followChat.current) messagesEnd.current?.scrollIntoView({behavior:'instant'}); }, [chat]);

  function closeProgress(restoreFocus=false) {
    setShowProgress(false);
    if(restoreFocus)progressToggle.current?.focus();
  }
  useEffect(()=>{
    if(!showProgress)return;
    function dismissProgress(event:KeyboardEvent|PointerEvent) {
      if(event.defaultPrevented)return;
      if(document.querySelector('[aria-modal="true"],dialog[open]'))return;
      if(event instanceof KeyboardEvent){
        if(event.key==='Escape'){event.preventDefault();closeProgress(true);}
        return;
      }
      if(event.target instanceof Node&&!progressDrawer.current?.contains(event.target)&&!progressToggle.current?.contains(event.target))closeProgress();
    }
    document.addEventListener('keydown',dismissProgress);
    document.addEventListener('pointerdown',dismissProgress);
    return()=>{document.removeEventListener('keydown',dismissProgress);document.removeEventListener('pointerdown',dismissProgress);};
  },[showProgress]);

  useEffect(()=>{
    function shortcuts(event:KeyboardEvent) {
      if (!(event.ctrlKey||event.metaKey) || document.querySelector('[aria-modal="true"],dialog[open]')) return;
      if(event.key.toLowerCase()==='n'){event.preventDefault();if(!navigationBusy&&(mode!=='ide'||root))void selectChat();return;}
      if(event.key.toLowerCase()==='k'){event.preventDefault();if(mode==='ide'){studio.update({agentVisible:true});setShowProgress(false);setShowHistory(true);}else setNav('History');setTimeout(()=>document.getElementById('conversation-search')?.focus(),0);return;}
      if(event.key.toLowerCase()==='b'){event.preventDefault();saveAppearance({...appearance,sidebar:!appearance.sidebar});return;}
      if(event.key.toLowerCase()==='p' || (event.shiftKey&&event.key.toLowerCase()==='f')) {
        event.preventDefault();
        const quick=event.key.toLowerCase()==='p';
        setQuickOpen(quick); setNav('Search');setSearchFocus(n=>n+1);
      }
    }
    window.addEventListener('keydown',shortcuts);
    return ()=>window.removeEventListener('keydown',shortcuts);
  },[mode,root,navigationBusy,appearance,studio]);
  useEffect(()=>{const clearSources=()=>setTask(current=>current?{...current,context_pack:undefined}:current);window.addEventListener('workspace-access-changed',clearSources);return()=>window.removeEventListener('workspace-access-changed',clearSources);},[]);
  function resetConversation(){chatId.current='';runId.current='';setChat([]);setTask(null);setApproval(null);setPrompt('');}
  async function switchWorkspace(id:string){
    if(anyRunning||navigationBusy||selectionPending.current||startingPending.current)return false;
    if(editorRef.current?.hasDirty()&&!(await window.lca.confirmEditorDiscard()).discard)return false;
    const result=await window.lca.selectWorkspace({id});
    if(!result.ok){report(result.error);return false;}
    editorRef.current?.reset();setWorkspaceId(id);setRoot(result.root);setProject(result.project.name);setSelectedFile('');selectedRef.current='';resetConversation();setMemoryOpen(false);setRenaming(null);setFiles([]);setDirectory('.');
    if(result.root)await refreshFiles('.');await refreshChats();return true;
  }
  function openFork(result:any){chatId.current=result.chat.id;runId.current='';setChat(result.chat.messages.filter((m:any)=>['user','assistant'].includes(m.role)&&typeof m.content==='string').map((m:any)=>({role:m.role,text:m.content})));setTask(null);setPrompt(result.prompt||'');void refreshChats();}
  async function openSearchFile(path:string,line:number) {
    setQuickOpen(false);
    if(window.neutralIdeHost){await window.lca.ideOpenFile(path,line);return;}
    if(modeRef.current!=='ide') await switchMode('ide');
    setNav('Search');
    const opened=await editorRef.current?.open(path,line);
    if(opened){setSelectedFile(opened);selectedRef.current=opened;}
  }
  async function refreshFiles(path = '.') {
    const r = await window.lca.listFiles(path);
    if (r.ok) { setFiles(r.items); setDirectory(path); directoryRef.current=path; } else report(r.error);
  }
  async function launchNativeIde(){
    const result=await window.lca.openNeutralIde();if(!result.ok)showWarning(result.error);
  }
  async function chooseProject() {
    if (anyRunning||navigationBusy||selectionPending.current||startingPending.current) return;
    if (editorRef.current?.hasDirty() && !(await window.lca.confirmEditorDiscard()).discard) return;
    const r = await window.lca.chooseProject();
    if (r.canceled) return;
    if(window.neutralIdeHost&&r.ok)return;
    if (!r.ok) { report(r.error); return; }
    if(nativeDefault&&!window.neutralIdeHost){setRoot(r.root);setProject(r.name);if(workspaceId)await window.lca.saveWorkspace({id:workspaceId,root:r.root});resetConversation();const opened=await window.lca.openNeutralIde();if(!opened.ok)showWarning(opened.error);return;}
    followChat.current=true;setAtBottom(true);setMemoryOpen(false);setRenaming(null);
    setMode('ide'); modeRef.current = 'ide'; setNav('Explorer');
    editorRef.current?.reset();
    if(workspaceId)await window.lca.saveWorkspace({id:workspaceId,root:r.root});
    setRoot(r.root); setProject(r.name); setSelectedFile(''); selectedRef.current = '';
    setChat(greeting); chatId.current = ''; setTask(null); setShowProgress(false);
    await refreshFiles('.'); await refreshChats();
  }
  async function openWorktree(id:string) {
    if(active.current||editorDirty)return;
    setWorkspaceWorking(true);
    try{const r=await window.lca.openManagedWorktree(id);if(!r.ok){report(r.error);return;}if(window.neutralIdeHost)return;
      editorRef.current?.reset();setRoot(r.root);setProject(r.name);setSelectedFile('');selectedRef.current='';
      resetConversation();setShowProgress(false);setNav('Explorer');await refreshFiles('.');await refreshChats();
    }finally{setWorkspaceWorking(false);}
  }
  async function switchMode(next: WorkspaceMode) {
    if(next==='voice'){await window.lca.openLola();return;}
    setShowHistory(false);
    if (navigationBusy || selectionPending.current || startingPending.current || next === modeRef.current) return;
    followChat.current=true;setAtBottom(true);setMemoryOpen(false);setRenaming(null);
    modeRef.current = next; setMode(next); setNav(next === 'ide' ? 'Explorer' : 'History');
    chatId.current = ''; runId.current = '';eventFloor.current=0;active.current=false;setBusy(false);setStopping(false); setTask(null); setApproval(null); setShowProgress(false);
    setChat([]);
    setChats([]);
    if (next !== 'ide' || root) await refreshChats(next);
  }
  async function activateMiya(text:string,send:boolean){const r=await window.lca.openLola(undefined,text?{action:'ask',text}:send?{action:'record'}:undefined);if(!r.ok)report(r.error||'Лола недоступна');}
  async function openFile(item: FileItem) {
    if(window.neutralIdeHost){await window.lca.ideOpenFile(item.path);return;}
    if (item.kind === 'directory') { await refreshFiles(item.path); return; }
    const path = await editorRef.current?.open(item.path);
    if (path) { setSelectedFile(path); selectedRef.current=path; }
  }
  async function selectChat(id?: string, scope=modeRef.current) {
    if (navigationBusy||selectionPending.current||startingPending.current) return;
    selectionPending.current=true;setSelectionBusy(true);loadingChat.current=id||'';queuedEvents.current=[];
    try {
      const r=id?await window.lca.loadChat(id,scope):await window.lca.newChat(scope);
      if(!r.ok){report(r.error);return;}
      followChat.current=true;setAtBottom(true);
      chatId.current=r.chat.id;runId.current=r.active_run?.run_id||'';
      eventFloor.current=r.event_seq||0;active.current=!!r.active_run;setBusy(!!r.active_run);setStopping(false);
      restoreBackgroundRuns(r.active_runs||[]);setTask(r.task);setApproval(r.approval||null);setDeciding(false);setPrompt('');
      setIdeOptions(r.task?.options?{...defaultIdeOptions,...r.task.options}:structuredClone(defaultIdeOptions));
      setChat(r.chat.messages.filter((m:any)=>typeof m.content==='string'&&['user','assistant'].includes(m.role)).map((m:any)=>({role:m.role,text:m.content,id:m.message_id,streaming:m.streaming})));
      (r.warnings||[]).forEach(showWarning);
      const pending=queuedEvents.current;queuedEvents.current=[];loadingChat.current='';
      for(const event of pending)if(!event.event_seq||event.event_seq>eventFloor.current)receiveEvent.current(event);
      await refreshChats(scope);
      return r.chat.id as string;
    } finally {loadingChat.current='';queuedEvents.current=[];selectionPending.current=false;setSelectionBusy(false);}
  }
  async function openBackgroundRun(run:any) {
    if(run.mode==='voice'){await window.lca.openLola(run.chat_id);return;}
    if(navigationBusy)return;
    if(run.mode!==modeRef.current)await switchMode(run.mode);
    await selectChat(run.chat_id,run.mode);
  }
  async function resolveToolRecovery(item: TaskRecoveryItem, resolution: TaskRecoveryResolution) {
    if (active.current || recoveryPending.current || !task?.journal_id || !chatId.current) return;
    const selectedChat = chatId.current, selectedMode = modeRef.current;
    recoveryPending.current = true; setRecoveryWorking(true);
    try {
      const result = await window.lca.resolveToolRecovery({chat_id:selectedChat, journal_id:task.journal_id, message_index:item.message_index, call_id:item.call_id, resolution});
      if (!result.ok) throw new Error(result.error || 'Не удалось сохранить результат проверки');
      if (chatId.current !== selectedChat || modeRef.current !== selectedMode) return;
      setTask(result.task);
      setChat(result.chat.messages.filter((m:any) => typeof m.content === 'string' && ['user','assistant'].includes(m.role)).map((m:any) => ({role:m.role, text:m.content})));
      (result.warnings || []).forEach(showWarning);
      await refreshChats(selectedMode);
    } catch (error) {
      if (chatId.current === selectedChat && modeRef.current === selectedMode) showWarning(String(error));
      else report(String(error));
    } finally { recoveryPending.current = false; setRecoveryWorking(false); }
  }
  async function returnToMiya(){if(!handoffResult)return;const r=await window.lca.openLola(handoffResult);if(r.ok)setHandoffResult('');else report(r.error||'Не удалось открыть Лолу');}
  async function declineHandoff() {
    if(!handoff||active.current)return;
    try{const result=await window.lca.cancelHandoff(handoff.id);if(!result.ok)throw Error(result.error);setHandoff(null);}
    catch(error){report(String(error));}
  }
  async function acceptHandoff() {
    if(active.current||!handoff||handoffWorking.current)return;
    handoffWorking.current=true;
    try {
      const result=await window.lca.prepareHandoff(handoff.id);if(!result.ok)throw Error(result.error);
      const target=result.handoff.target as WorkspaceMode;
      setMode(target);modeRef.current=target;setNav('History');setChat([]);setTask(null);
      chatId.current=result.chat.id;runId.current='';setHandoff(null);
      active.current=true;eventFloor.current=0;setBusy(true);setStopping(false);
      setChat([{role:'user',text:result.handoff.prompt}]);
      runId.current=crypto.randomUUID().replaceAll('-','');
      const started=await window.lca.startTask(result.handoff.prompt,false,target,undefined,runId.current);
      if(!started.ok)throw Error(started.error);if(active.current)runId.current=started.run_id;
      await refreshChats(target);
    }catch(error){report(String(error));setBusy(false);active.current=false;}finally{handoffWorking.current=false;}
  }
  useEffect(()=>{if(handoff&&!busy)void window.lca.getCompanionSettings().then(profile=>{if(profile.ok&&profile.auto_delegate!==false)void acceptHandoff();});},[handoff,busy]);
  async function renameChat() {
    if(!renaming||busy||renameWorking)return;
    setRenameWorking(true);setRenameNotice('');
    try {
      const result=await window.lca.renameChat(renaming.id,renaming.title,mode);
      if(!result.ok)throw new Error(result.error);
      (result.warnings||[]).forEach(showWarning);setRenaming(null);await refreshChats();
    }catch(error){setRenameNotice(String(error));}finally{setRenameWorking(false);}
  }
  async function configure() {
    const r = await window.lca.configureModel({base_url: baseUrl, model, api_key: apiKey, api_protocol:apiProtocol, tool_protocol:toolProtocol, settings:generation});
    if (!r.ok) throw new Error(r.error);
  }
  async function sendPrompt(resume = false, voiceText?:string,checksOnly=false) {
    let value = checksOnly?'Выполнить заданные проверки проекта':(voiceText??prompt).trim();
    if (active.current || selectionPending.current || navigationBusy || workspaceWorking || recoveryPending.current || !settingsReady || (mode === 'ide' && !root) || (!resume && mode === 'voice' && voiceText===undefined) || (mode!=='voice'&&!model&&!checksOnly) || (!resume && !value)) return;
    if (task?.recovery_items?.length || task?.recovery_error || task?.snapshot_attention?.length) {setShowProgress(true);showWarning('Сначала проверьте прерванные действия в карточке восстановления.');return;}
    // Block repeated clicks before the first IPC round trip.
    active.current = true;startingPending.current=true;setStarting(true);eventFloor.current=0; setBusy(true); setStopping(false);
    try {
      if(!checksOnly)await configure();
      if(nativeDefault&&!window.neutralIdeHost&&chatId.current){const selected=await window.lca.loadChat(chatId.current,mode);if(!selected.ok)throw Error(selected.error);}
      if(mode==='voice')setHandoff(null);
      if (!chatId.current) {
        const r = await window.lca.newChat(mode);
        if (!r.ok) throw new Error(r.error);
        chatId.current = r.chat.id;
        (r.warnings || []).forEach(showWarning);
      }
      runId.current = '';
      setChat(c => [...c, {role:'user', text: resume ? 'Продолжить приостановленную задачу' : value}]);
      runId.current=crypto.randomUUID().replaceAll('-','');
      const options=window.neutralIdeHost&&agentMode!=='agent'?{...ideOptions,read_only:true,auto_checks:false}:ideOptions;
      if(window.neutralIdeHost&&!resume&&!checksOnly){
        if(agentMode==='plan')value='Составь план реализации: исследуй проект, опиши шаги, затронутые файлы и проверки. Не выполняй изменения.\n\n'+value;
        if(editorContext.length)value+='\n\nКонтекст из редактора (ссылки на сохранённые файлы; прочитай их инструментами при необходимости):\n'+editorContext.map(item=>`${item.path}:${item.start}-${item.end}`).join('\n');
      }
      const r = await window.lca.startTask(value, resume, mode,mode==='ide'?serializeIdeOptions(options,checksOnly):undefined,runId.current);
      if (!r.ok) throw new Error(r.error);
      // Events can arrive before the start response, including task_end.
      if (active.current) runId.current = r.run_id;
      setPrompt('');setEditorContext([]);
    } catch (e) {
      report(String(e)); setChat(c => [...c, {role:'system', text:String(e)}]);
      setBusy(false); active.current = false;
    } finally {startingPending.current=false;setStarting(false);}
  }
  async function decide(decision: ApprovalDecision) {
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
    const r = await window.lca.cancelTask(runId.current||undefined);
    if (r.ok) { setApproval(null); report('Остановка запрошена'); }
    else { report(r.error); setStopping(false); }
  }
  const sidebarWidth=Math.min(studio.layout.sidebar,Math.max(180,studio.viewport-(mode==='ide'&&studio.layout.agentVisible?300:mode==='chat'&&studio.layout.contextVisible?200:0)-340));
  const agentWidth=Math.min(studio.layout.agent,Math.max(300,studio.viewport-(appearance.sidebar?sidebarWidth:0)-340));
  const contextWidth=Math.min(studio.layout.context,Math.max(200,studio.viewport-(appearance.sidebar?sidebarWidth:0)-360));
  const sidebarProps={mode,root,busy:anyRunning,navigating:navigationBusy,activeId:chatId.current,refresh:chats,workspaceId,onWorkspace:switchWorkspace,onRename:(c:ChatSummary)=>{setRenaming({id:c.id,title:c.title});setRenameNotice('');},onReset:resetConversation,onFork:openFork,onError:report};
  const contextFiles=files.filter(f=>f.kind==='file').slice(0,12);
  return <div className={`app-shell studio-shell ${window.neutralIdeHost?'native-ide':''} mode-${mode}${appearance.sidebar?'':' sidebar-hidden'}${appearance.statusbar?'':' statusbar-hidden'}${appearance.output?'':' output-hidden'}`} data-theme={appearance.theme==='parchment'?'light':'dark'} data-leshy-theme={appearance.theme} data-accent={appearance.accent} data-density={appearance.density} style={{'--studio-sidebar':sidebarWidth+'px','--studio-agent':agentWidth+'px','--studio-context':contextWidth+'px','--studio-settings':studio.layout.settings+'px'} as React.CSSProperties}>
    <DialogFocus/>{!window.neutralIdeHost&&<NeuralAudio/>}
    <OptionalIdePanel visible={optionalOpen} root={root} path={selectedFile} busy={busy||recoveryWorking} dirty={editorDirty} onClose={()=>setOptionalOpen(false)} onWorking={setWorkspaceWorking} onOpen={(path,line)=>void openSearchFile(path,line)} onUse={text=>setPrompt(previous=>(previous?previous+'\n\n':'')+text)} onWorktree={openWorktree}/>
    {quickOpen&&<div className="search-overlay" onMouseDown={e=>{if(e.target===e.currentTarget)setQuickOpen(false);}}><ProjectSearch root={root} visible quick focus={searchFocus} onClose={()=>setQuickOpen(false)} onOpen={(path,line)=>void openSearchFile(path,line)}/></div>}
    {!window.neutralIdeHost&&<header className="topbar"><div className="brand"><BrandMark size={23}/><strong>ЛЕШИЙ <small>/ LESHY</small></strong></div><div className="mode-tabs" role="tablist" aria-label="Режим работы">{([{id:'ide',label:nativeDefault?'Открыть IDE':'Код',icon:Code2},{id:'chat',label:'Чат',icon:MessageSquare}] as const).map(item=><button role="tab" key={item.id} aria-selected={mode===item.id} disabled={navigationBusy} className={mode===item.id?'selected':''} onClick={()=>{if(item.id==='ide'&&nativeDefault&&!window.neutralIdeHost)void launchNativeIde();else void switchMode(item.id);}}><item.icon size={16}/>{item.label}</button>)}</div><button className="icon-button leshy-new-chat" title="Новый разговор" aria-label="Новый разговор" disabled={navigationBusy} onClick={()=>void selectChat()}><Plus size={18}/></button><div className="top-spacer"/><button className="icon-button" title="Поиск по проекту" aria-label="Поиск по проекту" disabled={!root} onClick={()=>{setQuickOpen(true);setSearchFocus(x=>x+1);}}><Search size={18}/></button>{!window.neutralIdeHost&&<div className="studio-lola-controls"><button className="lola-open" onClick={()=>void window.lca.openLola().then(r=>{if(!r.ok)showWarning(r.error||'Не удалось открыть Лолу');})}>Лола <MessageSquare size={14}/></button><details><summary aria-label="Голосовая активация Лолы"><ChevronDown size={13}/></summary><div><WakeListener busy={busy} onWake={activateMiya}/></div></details></div>}<button className="icon-button" title="Показать или скрыть боковую панель" aria-label="Боковая панель" aria-pressed={appearance.sidebar} onClick={()=>saveAppearance({...appearance,sidebar:!appearance.sidebar})}><PanelLeft size={17}/></button><button className="icon-button" title="Показать или скрыть правую панель" aria-label="Правая панель" aria-pressed={mode==='ide'?studio.layout.agentVisible:studio.layout.contextVisible} onClick={()=>mode==='ide'?studio.update({agentVisible:!studio.layout.agentVisible}):studio.update({contextVisible:!studio.layout.contextVisible})}><PanelRight size={17}/></button><button className="icon-button" title="Настройки Лешего" aria-label="Настройки Лешего" onClick={()=>{setSettingsSection('connection');setSettingsOpen(true);}}><Settings2 size={18}/></button></header>}
    <div className="workarea">
      <aside className="sidebar"><OrnamentFrame/><ResizeRail name="sidebar"/><ConversationSidebar {...sidebarProps} visible={mode==='chat'} onOpen={id=>void selectChat(id)}/>
        {mode==='ide'&&<><div className="side-heading"><span>ФАЙЛЫ ПРОЕКТА</span><button title="Открыть в LESHY IDE · прототип Code-OSS" aria-label="Открыть в LESHY IDE" disabled={!root||editorDirty||navigationBusy} onClick={()=>void window.lca.openNeutralIde().then(r=>{if(!r.ok)showWarning(r.error||'Не удалось открыть LESHY IDE');else report('Открыта отдельная LESHY IDE · прототип. Агент и подтверждение правок пока доступны в этом окне.');})}><Code2 size={15}/></button><button className="studio-optional-open" title="Дополнительные возможности IDE" onClick={()=>setOptionalOpen(true)}><SquareTerminal size={14}/></button><button onClick={()=>void chooseProject()} title="Выбрать папку проекта" disabled={anyRunning||navigationBusy}><FolderOpen size={15}/></button></div><nav className="sidebar-views" aria-label="Области проекта">{[{id:'Explorer',label:'Файлы',title:'Файлы проекта'},{id:'Search',label:'Поиск',title:'Поиск по проекту'},{id:'Memory',label:'Память',title:'Память проекта'}].map(item=><button key={item.id} title={item.title} aria-pressed={nav===item.id} disabled={item.id==='Memory'&&!root} onClick={()=>item.id==='Memory'?setMemoryOpen(true):setNav(item.id)}>{item.label}</button>)}</nav><ProjectSearch root={root} visible={nav==='Search'&&!quickOpen} quick={false} focus={searchFocus} onClose={()=>setNav('Explorer')} onOpen={(path,line)=>void openSearchFile(path,line)}/>{nav==='Explorer'&&<StudioFileTree root={root} selected={selectedFile} refresh={files} onFile={f=>void openFile(f)} onProject={()=>void chooseProject()} onError={report}/>}</>}
        {mode==='chat'&&root&&<details className="leshy-project-tree"><summary><Folder size={14}/>Файлы проекта</summary><StudioFileTree root={root} selected={selectedFile} refresh={files} onFile={f=>void openSearchFile(f.path,1)} onProject={()=>void chooseProject()} onError={report}/></details>}<WoodlandAccent className="sidebar-woodland"/><div className="sidebar-footer"><Folder size={13}/><button className="project-pill" title={root||'Выбрать папку проекта'} onClick={()=>void chooseProject()} disabled={anyRunning||navigationBusy}>{root?project:'Открыть папку'}</button><small>{root?'локально':''}</small></div>
      </aside>
      <div className={`studio-workspace ${studio.layout.contextSide==='left'?'context-left':''}`}>
        <main className={mode==='ide'?'main-panel':'editor-hidden'}>{!window.neutralIdeHost&&<EditorPanel ref={editorRef} root={root} busy={busy||workspaceWorking} visible={mode==='ide'} onActive={path=>{setSelectedFile(path);selectedRef.current=path;}} onDirty={dirty=>{setEditorDirty(dirty);void window.lca.setEditorDirty(dirty);}} onProject={()=>void chooseProject()} onModels={()=>{setSettingsSection('connection');setSettingsOpen(true);}} onLog={report}/>}<div className="bottom-panel"><div className="bottom-tabs"><span className="bottom-tab active"><SquareTerminal size={14}/>Вывод</span><button className="icon-button" aria-label="Закрыть вывод" onClick={()=>saveAppearance({...appearance,output:false})}><X size={13}/></button></div><div className="output-log">{logs.length?logs.map((l,i)=><pre key={i}>{l}</pre>):<p className="output-line dim">События агента появятся здесь.</p>}</div></div></main>
        {(window.neutralIdeHost||mode!=='ide'||studio.layout.agentVisible)&&<aside className="agent-panel">
          {mode==='ide'&&<ResizeRail name="agent" edge="left"/>}
          {window.neutralIdeHost&&<div className="native-project-context"><span title={root}><Folder size={13}/>{project}</span><button title="Память и инструкции проекта" onClick={()=>setMemoryOpen(true)}>Правила</button><button className="icon-button" aria-label="Настройки агента" onClick={()=>{setSettingsSection('connection');setSettingsOpen(true);}}><Settings2 size={15}/></button></div>}
          <header className="agent-heading"><h1>{mode==='ide'?(chats.find(c=>c.id===chatId.current)?.title||'Новая задача'):chats.find(c=>c.id===chatId.current)?.title||'Новый разговор'}</h1>{backgroundRuns.length>0&&<details className="studio-runs"><summary title="Фоновые задачи" aria-label={`Фоновые задачи: ${backgroundRuns.length}`}><Clock3 size={12}/>{backgroundRuns.length}</summary><div className="background-runs" aria-label="Фоновые задачи">{backgroundRuns.map(run=><button key={run.run_id} disabled={navigationBusy} className={run.chat_id===chatId.current?'selected':''} onClick={()=>void openBackgroundRun(run)}><span>{run.title}</span><small>{run.approval?'Нужно решение':run.chat_id===chatId.current?'Открыта':'Открыть задачу'}</small></button>)}</div></details>}{mode==='ide'&&<button ref={historyToggle} className="studio-panel-button history-toggle" aria-expanded={showHistory} aria-controls="ide-agent-history" onClick={()=>{setShowHistory(!showHistory);setShowProgress(false);}}><History size={14}/><span>История</span></button>}<button ref={progressToggle} className="progress-toggle studio-panel-button" aria-controls="model-progress-details" aria-expanded={showProgress} disabled={!task} onClick={()=>{setShowHistory(false);setShowProgress(!showProgress);}}><PanelRight size={14}/><span>Действия</span></button><button className="icon-button" title="Новый чат" disabled={(mode==='ide'&&!root)||navigationBusy} onClick={()=>void selectChat()}><Plus size={15}/></button></header>
          {window.neutralIdeHost&&task&&<button className="native-review" onClick={()=>{setShowHistory(false);setProgressTab('overview');setShowProgress(true);}}>Изменения и проверки <ChevronRight size={13}/></button>}
          {showHistory&&mode==='ide'&&<section id="ide-agent-history" className="studio-history" role="region" aria-label="Разговоры с агентом"><ResizeRail name="agent" edge="left"/><header><strong>Разговоры с агентом</strong><button className="icon-button" aria-label="Закрыть разговоры" onClick={()=>{setShowHistory(false);historyToggle.current?.focus();}}><X size={16}/></button></header><ConversationSidebar {...sidebarProps} showWorkspace={false} visible onOpen={id=>{setShowHistory(false);void selectChat(id);}}/></section>}
          {showProgress&&task&&<div ref={progressDrawer} id="model-progress-details" className="progress-drawer" role="region" aria-label="Подробности работы модели"><ResizeRail name="agent" edge="left"/><header className="progress-drawer-header"><strong>Задача · {taskStatusLabel(task)}</strong><button className="icon-button" aria-label="Закрыть подробности работы модели" title="Закрыть · Esc" onClick={()=>closeProgress(true)}><X size={17}/></button></header><nav className="progress-tabs" aria-label="Раздел подробностей"><button onClick={()=>setProgressTab('overview')} aria-pressed={progressTab==='overview'}>Обзор и субагенты</button><button onClick={()=>setProgressTab('tools')} aria-pressed={progressTab==='tools'}>Инструменты</button></nav>{progressTab==='tools'&&<InlineTools task={task}/>}<div hidden={progressTab!=='overview'}><TaskProgress task={task} onTask={mode==='ide'?updated=>{if(updated.chat_id===chatId.current)setTask(updated);}:undefined} busy={busy||recoveryWorking} onResume={()=>void sendPrompt(true)} onResolveRecovery={(item,resolution)=>void resolveToolRecovery(item,resolution)}/>{mode==='ide'&&<WorkspaceReview key={chatId.current+root} onWorking={setWorkspaceWorking} chatId={chatId.current} root={root} busy={busy||recoveryWorking} dirty={editorDirty} revision={task.workspace_generation||0} onTask={setTask} onRestored={()=>{void selectChat(chatId.current);void refreshFiles(directoryRef.current);if(selectedRef.current)void editorRef.current?.refresh(selectedRef.current);}}/>}</div></div>}
          <div className="chat-messages" inert={showHistory||showProgress} onScroll={event=>{const node=event.currentTarget;const bottom=node.scrollHeight-node.scrollTop-node.clientHeight<80;followChat.current=bottom;setAtBottom(bottom);}}>{!chat.some(m=>m.role==='user')&&<Welcome mode={mode} onStart={()=>document.querySelector<HTMLTextAreaElement>('.composer textarea')?.focus()} onPrompt={text=>{setPrompt(text);document.querySelector<HTMLTextAreaElement>('.composer textarea')?.focus();}}/ >}{chat.filter(m=>chat.some(x=>x.role==='user')||m.role==='system').map((m,i)=><div className={`message ${m.role}`} key={m.id||i}><div className="message-content"><div className="message-meta">{m.role==='assistant'&&<BrandMark size={19}/>}<span>{m.role==='user'?'ВЫ':m.role==='assistant'?'ЛЕШИЙ':'СООБЩЕНИЕ СИСТЕМЫ'}</span></div><ChatText text={m.text}/>{m.streaming&&<span className="streaming-caret" aria-label="Ответ генерируется">▍</span>}</div></div>)}<div ref={messagesEnd}/></div>
          {!atBottom&&<button className="follow-chat" onClick={()=>{followChat.current=true;setAtBottom(true);messagesEnd.current?.scrollIntoView({behavior:'instant'});}}>К последнему сообщению ↓</button>}
          <div className="composer-area" inert={showHistory||showProgress}>{mode==='ide'&&<IdeTaskOptions value={ideOptions} onChange={setIdeOptions} busy={busy||recoveryWorking||workspaceWorking} onRunChecks={()=>void sendPrompt(false,undefined,true)}/>}<div className="composer"><OrnamentFrame/>{window.neutralIdeHost&&<><div className="native-composer-tools"><select aria-label="Режим агента" value={agentMode} disabled={busy} onChange={e=>setAgentMode(e.target.value as typeof agentMode)}><option value="agent">Agent</option><option value="ask">Ask</option><option value="plan">Plan</option></select><button disabled={busy} onClick={()=>void attachEditorContext()} title="Добавить активный сохранённый файл или выделенные строки">+ Контекст</button></div><div className="native-context-chips">{editorContext.map(item=><button key={item.path} disabled={busy} title="Убрать из запроса" onClick={()=>setEditorContext(items=>items.filter(i=>i.path!==item.path))}>{item.path}:{item.start} <X size={12}/></button>)}</div></>}<textarea aria-label="Задача агенту" value={prompt} disabled={busy} onChange={e=>setPrompt(e.target.value)} onKeyDown={e=>{if(e.key==='Enter'&&!e.shiftKey&&!e.nativeEvent.isComposing&&e.keyCode!==229){e.preventDefault();void sendPrompt();}}} placeholder={mode==='ide'&&!root?'Сначала выберите проект':!model?'Выберите модель ниже':'Опишите задачу…'}/><div className="composer-footer"><ComposerModel config={{api_protocol:apiProtocol,base_url:baseUrl,model,api_key:apiKey,tool_protocol:toolProtocol,settings:generation}} busy={anyRunning||workspaceWorking} onSelected={setModel} onSettings={()=>{setSettingsSection('connection');setSettingsOpen(true);}}/>{busy?<button className="send-button" title="Остановить" disabled={stopping} onClick={()=>void cancel()}><Square size={14}/><span>{stopping?'Остановка…':'Остановить'}</span></button>:<button className="send-button" title="Отправить" onClick={()=>void sendPrompt()} disabled={workspaceWorking||!prompt.trim()||(mode==='ide'&&!root)||!model||!settingsReady}><ChevronRight size={14}/><span>Отправить</span></button>}</div></div><div className="agent-foot">{busy?'Агент работает…':window.neutralIdeHost&&agentMode!=='agent'?'Только чтение · без изменений и команд':mode==='ide'?'Изменения файлов — после подтверждения':'История сохраняется на этом ПК'}</div></div>
        </aside>}
        {mode==='chat'&&studio.layout.contextVisible&&<aside className="studio-context"><OrnamentFrame/><ResizeRail name="context" edge={studio.layout.contextSide==='left'?'right':'left'}/><header><div><span className="eyebrow">КОНТЕКСТ</span><h2>Проект</h2></div><button className="icon-button" aria-label="Закрыть контекст" onClick={()=>studio.update({contextVisible:false})}><X size={15}/></button></header><section><span className="eyebrow">РАБОЧЕЕ ПРОСТРАНСТВО</span><p><Folder size={15}/><strong>{workspaceId?project:'Личное пространство'}</strong></p><small>{root||'Папка проекта не выбрана'}</small></section>{contextFiles.length>0&&<section><span className="eyebrow">ФАЙЛЫ</span>{contextFiles.map(f=><button className="context-file" key={f.path} onClick={()=>void openSearchFile(f.path,1)}><FileCode2 size={14}/>{f.name}</button>)}</section>}<section className="leshy-agent-card"><span className="eyebrow">АКТИВНЫЙ АГЕНТ</span><div className="leshy-agent-identity"><Sparkles size={24}/><div><strong>{model||'Агент'}</strong><small><i className={busy?'working':''}/>{busy?'Выполняет задачу':model?'Готов к задачам':'Выберите модель'}</small></div><button className="icon-button" aria-label="Настроить модель агента" onClick={()=>{setSettingsSection('connection');setSettingsOpen(true);}}><ChevronDown size={16}/></button></div></section><section className="leshy-context-tasks"><span className="eyebrow">ЗАДАЧИ</span>{task?<><p>{taskStatusLabel(task)}</p><ul aria-label="Этапы текущей задачи">{(task.stages||[]).map(stage=><li key={stage.id} data-status={stage.status}>{stage.status==='done'?<Check size={15}/>:<Circle size={15}/>}<span>{stage.title}<small>{stage.status==='done'?'Завершено':stage.status==='active'?'Текущий этап':stage.status==='skipped'?'Пропущено':'Ожидает'}</small></span></li>)}</ul><ContextUsage budget={task.budget} usage={task.usage}/></>:<p className="leshy-no-task">Опишите задачу — здесь появится ход работы.</p>}</section><section><span className="eyebrow">ИНСТРУМЕНТЫ</span><div className="leshy-tool-grid"><button disabled={navigationBusy} onClick={()=>nativeDefault?void launchNativeIde():void switchMode('ide')}><Code2 size={17}/>Код</button><button disabled={!root} onClick={()=>{setQuickOpen(true);setSearchFocus(x=>x+1);}}><Search size={17}/>Поиск</button><button disabled={anyRunning||navigationBusy} onClick={()=>void chooseProject()}><FolderOpen size={17}/>Проект</button><button onClick={()=>setOptionalOpen(true)}><SquareTerminal size={17}/>Инструменты</button></div></section><WoodlandAccent className="context-woodland"/></aside>}
      </div>
    </div>
    {!window.neutralIdeHost&&<footer className="statusbar"><span className="status" title={health}><i/>{health.includes('подключён')?'Готов к работе':health}</span><span>{mode==='ide'?'IDE':'Chat'} · {workspaceId?project:root?project:'Личное пространство'}</span><button className="statusbar-right" onClick={()=>saveAppearance({...appearance,output:!appearance.output})}>Журнал событий <SquareTerminal size={12}/></button></footer>}
    {handoffResult&&!busy&&<button className="handoff-return" onClick={()=>void returnToMiya()}>Результат готов · открыть Лолу</button>}
    {desktopImage&&<div className="desktop-artifact"><button onClick={()=>setDesktopImage('')}>Закрыть скриншот</button><img src={desktopImage} alt="Скриншот по запросу пользователя"/></div>}
    {handoff&&<div className="handoff-card"><b>Лола передаёт задачу в {handoff.target.toUpperCase()}</b><p>{handoff.prompt}</p><button disabled={busy} onClick={()=>void acceptHandoff()}>Выполнить основной моделью</button><button disabled={busy} onClick={()=>void declineHandoff()}>Не выполнять</button></div>}
    <div className="assistant-notices" aria-live="polite">{assistantNotices.map(item=><div className="assistant-notice" role="status" key={item.id}><b>{item.title}</b><p>{item.text}</p><button className="secondary-button" aria-label="Закрыть напоминание" onClick={()=>setAssistantNotices(items=>items.filter(value=>value.id!==item.id))}>Закрыть</button></div>)}</div>
    {memoryOpen&&root&&<MemoryPanel key={root} root={root} busy={busy} onClose={()=>setMemoryOpen(false)}/>}
    {renaming&&<div className="modal-backdrop"><section className="rename-dialog" role="dialog" aria-modal="true" aria-labelledby="rename-title"><h2 id="rename-title">Название чата</h2><form onSubmit={event=>{event.preventDefault();void renameChat();}}><input autoFocus aria-label="Название чата" value={renaming.title} maxLength={120} disabled={renameWorking} onChange={event=>setRenaming({...renaming,title:event.target.value})}/><p role="status">{renameNotice}</p><div className="settings-actions"><button type="button" disabled={renameWorking} onClick={()=>setRenaming(null)}>Отмена</button><button className="primary-button" type="submit" disabled={busy||renameWorking||!renaming.title.trim()}>Переименовать</button></div></form></section></div>}
    {settingsOpen&&settingsReady&&<ModelSettings onIde={()=>{setSettingsOpen(false);if(nativeDefault&&!window.neutralIdeHost)void launchNativeIde();else setOptionalOpen(true);}} initialSection={settingsSection} initial={{api_protocol:apiProtocol,base_url:baseUrl,model,api_key:apiKey,tool_protocol:toolProtocol,settings:generation}} busy={anyRunning} onClose={()=>setSettingsOpen(false)} onSaved={config=>{setApiProtocol(config.api_protocol||'chat');setBaseUrl(config.base_url);setModel(config.model);setToolProtocol(config.tool_protocol||'native');setApiKey(config.api_key);setGeneration(config.settings);report('Настройки модели сохранены');}}/>}
    {approval&&<ApprovalDialog approval={approval} deciding={deciding} onLater={()=>setApproval(null)} onDecide={value=>void decide(value)}/>}
  </div>;
}
