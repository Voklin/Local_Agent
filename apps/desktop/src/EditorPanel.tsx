import { forwardRef, useEffect, useImperativeHandle, useRef, useState } from 'react';
import { Code2, FileCode2, FolderOpen, RotateCcw, Save, Search, Settings2, ShieldCheck, WrapText, X } from 'lucide-react';

export type EditorDocument = {path:string; content:string; original:string; revision:{path:string; sha256:string}; newline:string};
export type EditorHandle = {
  open: (path:string, line?:number) => Promise<string | undefined>;
  refresh: (path:string) => Promise<void>;
  reset: () => void;
  hasDirty: () => boolean;
};
type EditorProps = {root:string; busy:boolean; visible:boolean; onActive:(path:string)=>void;
  onDirty:(dirty:boolean)=>void; onProject:()=>void; onModels:()=>void; onLog:(text:string)=>void};

export const EditorPanel = forwardRef<EditorHandle,EditorProps>(function EditorPanel(props, ref) {
  const [tabs, setTabs] = useState<EditorDocument[]>([]);
  const [activePath, setActivePath] = useState('');
  const [notice, setNotice] = useState('');
  const [saving, setSaving] = useState(false);
  const [proposal, setProposal] = useState<{proposal_id:string;path:string;diff:string}|null>(null);
  const [wrap, setWrap] = useState(false);
  const [findOpen, setFindOpen] = useState(false);
  const [query, setQuery] = useState('');
  const [lineInput, setLineInput] = useState('1');
  const [position, setPosition] = useState({line:1,column:1});
  const [scrollTop, setScrollTop] = useState(0);
  const input = useRef<HTMLTextAreaElement>(null);
  const findInput = useRef<HTMLInputElement>(null);
  const jumpInput = useRef<HTMLInputElement>(null);
  const tabsRef = useRef(tabs); tabsRef.current = tabs;
  const rootRef = useRef(props.root); rootRef.current = props.root;
  const previousRoot = useRef(props.root);
  const dirtySent = useRef(false);
  const targetLine = useRef<{path:string;line:number}|null>(null);
  const current = tabs.find(tab=>tab.path===activePath);
  const dirty = tabs.some(tab=>tab.content!==tab.original);
  const lineCount = (current?.content.match(/\n/g)?.length || 0) + 1;
  const gutterStart = Math.max(0, Math.floor(scrollTop / 21) - 1);

  useEffect(()=>{
    if (dirty !== dirtySent.current) { dirtySent.current=dirty; props.onDirty(dirty); }
  }, [dirty]);
  useEffect(()=>{
    if (!props.root) return; // Keep local drafts if Core stops; reconnect can reuse the same root.
    if (previousRoot.current && previousRoot.current!==props.root) reset();
    previousRoot.current=props.root;
  }, [props.root]);
  useEffect(()=>{
    props.onActive(activePath);
    setPosition({line:1,column:1}); setScrollTop(0);
  }, [activePath]);
  useEffect(()=>{
    if (targetLine.current?.path===activePath && current) {
      const line=targetLine.current.line; targetLine.current=null;
      moveToLine(line);
    }
  }, [activePath,tabs]);

  function reset() {
    setTabs([]); setActivePath(''); setProposal(null); setNotice(''); targetLine.current=null;
  }
  function selectDocument(document:EditorDocument) {
    setTabs(items=>items.some(tab=>tab.path===document.path)
      ? items.map(tab=>tab.path===document.path?document:tab) : [...items,document]);
    setActivePath(document.path);
  }
  async function read(path:string) {
    const requestedRoot=props.root;
    const result=await window.lca.editorRead(path);
    if (rootRef.current!==requestedRoot) return;
    if (!result.ok) throw new Error(result.error);
    return {...result, original:result.content} as EditorDocument;
  }
  async function open(path:string, line?:number) {
    if (saving || proposal) return;
    try {
      const existing=tabsRef.current.find(tab=>tab.path===path);
      if (line) targetLine.current={path,line};
      if (existing) { setActivePath(path); if(line) moveToLine(line); return path; }
      const document=await read(path);
      if (document) {
        if (line) targetLine.current={path:document.path,line};
        selectDocument(document); setNotice(''); return document.path;
      }
    } catch(error) { setNotice(String(error)); props.onLog(String(error)); }
  }
  async function refresh(path:string) {
    const tab=tabsRef.current.find(item=>item.path===path);
    if (!tab) return;
    if (tab.content!==tab.original) { setNotice(`${path}: версия на диске изменилась. Ваш черновик сохранён; перечитайте файл или скопируйте свой текст.`); return; }
    try {
      const document=await read(path);
      if (document) setTabs(items=>items.map(item=>item.path===path && item.content===item.original?document:item));
    } catch(error) { setNotice(String(error)); }
  }
  useImperativeHandle(ref,()=>({open,refresh,reset,hasDirty:()=>tabsRef.current.some(tab=>tab.content!==tab.original)}));

  async function closeTab(path:string) {
    if (saving || proposal) return;
    const tab=tabsRef.current.find(item=>item.path===path);
    if (tab && tab.content!==tab.original && !(await window.lca.confirmEditorDiscard()).discard) return;
    const remaining=tabsRef.current.filter(item=>item.path!==path);
    setTabs(remaining);
    if (activePath===path) setActivePath(remaining.at(-1)?.path || '');
  }
  async function reload() {
    if (!current || saving) return;
    if (current.content!==current.original && !(await window.lca.confirmEditorDiscard()).discard) return;
    try { const document=await read(current.path); if(document) {selectDocument(document);setNotice('Файл перечитан с диска');} }
    catch(error) { setNotice(String(error)); }
  }
  async function save() {
    if (!current || props.busy || saving || proposal || !props.root) return;
    setSaving(true);
    try {
      const result=await window.lca.editorPreview(current.path,current.content,current.revision);
      if (!result.ok) throw new Error(result.error);
      if (result.unchanged) {selectDocument({...result.file,original:result.file.content});setNotice('Изменений нет');}
      else setProposal(result);
    } catch(error) { setNotice(String(error)); }
    finally {setSaving(false);}
  }
  async function decide(decision:string) {
    if (!proposal || saving) return;
    setSaving(true);
    try {
      const result=await window.lca.editorResolve(proposal.proposal_id,decision);
      setProposal(null);
      if (!result.ok) throw new Error(result.error);
      if (result.applied && result.file) {
        selectDocument({...result.file,original:result.file.content});
        setNotice(`Сохранено: ${result.path}`); props.onLog(`Редактор: сохранён ${result.path}`);
      } else setNotice(result.warning || 'Запись отклонена; черновик остался в редакторе');
    } catch(error) {setNotice(String(error));}
    finally {setSaving(false);}
  }
  function updatePosition() {
    const element=input.current;
    if (!element) return;
    const before=element.value.slice(0,element.selectionStart);
    const lines=before.split('\n'); setPosition({line:lines.length,column:lines.at(-1)!.length+1});
  }
  function moveToLine(line:number) {
    const element=input.current;
    if (!element) return;
    const lines=element.value.split('\n');
    const index=Math.max(0,Math.min(lines.length-1,Math.floor(line)-1));
    const offset=lines.slice(0,index).reduce((sum,text)=>sum+text.length+1,0);
    element.focus(); element.setSelectionRange(offset,offset);
    element.scrollTop=Math.max(0,(index-3)*21); updatePosition();
  }
  function findNext() {
    const element=input.current;
    if (!element || !query) return;
    const text=element.value.toLocaleLowerCase(), needle=query.toLocaleLowerCase();
    let offset=text.indexOf(needle,element.selectionEnd);
    if (offset<0) offset=text.indexOf(needle);
    if (offset<0) {setNotice('Совпадений в файле нет');return;}
    moveToLine(element.value.slice(0,offset).split('\n').length);
    element.setSelectionRange(offset,offset+query.length); updatePosition();
  }
  useEffect(()=>{
    function shortcuts(event:KeyboardEvent) {
      if (!props.visible || !current || document.querySelector('[role="dialog"]') || !(event.ctrlKey||event.metaKey)) return;
      if(event.key.toLowerCase()==='s') {event.preventDefault();void save();}
      if(event.key.toLowerCase()==='f') {event.preventDefault();setFindOpen(true);setTimeout(()=>findInput.current?.focus(),0);}
      if(event.key.toLowerCase()==='g') {event.preventDefault();setFindOpen(true);setLineInput(String(position.line));setTimeout(()=>{jumpInput.current?.focus();jumpInput.current?.select();},0);}
      if(event.shiftKey && event.key.toLowerCase()==='r') {event.preventDefault();void reload();}
    }
    window.addEventListener('keydown',shortcuts); return()=>window.removeEventListener('keydown',shortcuts);
  }, [props.visible,props.busy,current,saving,proposal,position.line]);

  return <>
    <div className="editor-tabs" role="tablist" aria-label="Открытые файлы">
      {tabs.length?tabs.map(tab=><div className={`tab ${activePath===tab.path?'active':''}`} key={tab.path}>
        <button role="tab" aria-selected={activePath===tab.path} onClick={()=>setActivePath(tab.path)} title={tab.path}><FileCode2 size={14}/>{tab.path.split('/').pop()}{tab.content!==tab.original&&<span className="editor-dirty" aria-label="Есть несохранённые изменения">●</span>}</button>
        <button className="close-editor-tab" title={`Закрыть ${tab.path}`} onClick={()=>void closeTab(tab.path)}><X size={12}/></button>
      </div>):<div className="tab active"><FileCode2 size={14}/>Welcome</div>}
    </div>
    <div className="editor-area">
      {current?<div className="document-editor">
        <div className="editor-toolbar"><span className="breadcrumbs">{current.path}</span><button title="Сохранить · Ctrl+S" disabled={props.busy||saving||!props.root||current.content===current.original} onClick={()=>void save()}><Save size={15}/></button><button title="Перечитать · Ctrl+Shift+R" disabled={saving||!props.root} onClick={()=>void reload()}><RotateCcw size={15}/></button><button title="Найти · Ctrl+F" onClick={()=>{setFindOpen(!findOpen);setTimeout(()=>findInput.current?.focus(),0);}}><Search size={15}/></button><button title="Перенос строк" aria-pressed={wrap} onClick={()=>setWrap(!wrap)}><WrapText size={15}/></button></div>
        {findOpen&&<div className="editor-find"><input ref={findInput} aria-label="Поиск в файле" value={query} onChange={event=>setQuery(event.target.value)} onKeyDown={event=>{if(event.key==='Enter')findNext();}} placeholder="Найти текст…"/><button onClick={findNext}>Далее</button><input ref={jumpInput} onKeyDown={event=>{if(event.key==='Enter')moveToLine(Number(lineInput)||1);}} aria-label="Номер строки" type="number" min={1} value={lineInput} onChange={event=>setLineInput(event.target.value)}/><button onClick={()=>moveToLine(Number(lineInput)||1)}>К строке</button><button title="Закрыть поиск" onClick={()=>setFindOpen(false)}><X size={13}/></button></div>}
        <div className={`editor-code ${wrap?'wrapped':''}`}>
          {!wrap&&<div className="editor-gutter" aria-hidden="true"><pre style={{transform:`translateY(${12+gutterStart*21-scrollTop}px)`}}>{Array.from({length:Math.min(120,Math.max(0,lineCount-gutterStart))},(_,index)=>gutterStart+index+1).join('\n')}</pre></div>}
          <textarea ref={input} className="editor-input" aria-label={`Редактор ${current.path}`} disabled={saving||!!proposal} spellCheck={false} autoCapitalize="off" autoCorrect="off" wrap={wrap?'soft':'off'} value={current.content} onChange={event=>{const content=event.target.value;setTabs(items=>items.map(tab=>tab.path===activePath?{...tab,content}:tab));}} onClick={updatePosition} onKeyUp={updatePosition} onSelect={updatePosition} onScroll={event=>setScrollTop(event.currentTarget.scrollTop)}/>
        </div>
        <div className="editor-status"><span>Ln {position.line}, Col {position.column}</span><span>UTF-8 · {current.newline.toUpperCase()}</span><span>{current.content!==current.original?'Несохранённые изменения · агент видит версию на диске':'Изменений нет'}</span></div>
      </div>:<div className="welcome"><div className="welcome-logo"><Code2 size={28}/></div><h1>Agent Studio</h1><p>Рабочее пространство LocalAgent</p><div className="welcome-actions"><button onClick={props.onProject} disabled={props.busy}><FolderOpen size={16}/>Открыть проект</button><button onClick={props.onModels}><Settings2 size={16}/>Настроить модель</button></div><div className="migration-note"><ShieldCheck size={17}/><span><b>Изменения под вашим контролем</b><br/>Редактируйте файлы во вкладках. Сохранение проходит через diff и повторную проверку файла.</span></div></div>}
      {notice&&<div className="editor-notice" role="status">{notice}<button title="Скрыть уведомление" onClick={()=>setNotice('')}><X size={12}/></button></div>}
    </div>
    {proposal&&<div className="modal-backdrop editor-approval"><section className="approval-dialog" role="dialog" aria-modal="true" aria-labelledby="editor-approval-title"><h2 id="editor-approval-title">Сохранение: {proposal.path}</h2><p>Подтверждение относится только к этому diff. Черновик не записан до применения.</p><pre>{proposal.diff}</pre><div className="approval-actions"><button disabled={saving} onClick={()=>void decide('cancel')}>Отмена</button><button disabled={saving} onClick={()=>void decide('reject')}>Отклонить</button><button className="primary-button" disabled={saving||props.busy} onClick={()=>void decide('apply')}>Применить и сохранить</button></div></section></div>}
  </>;
});
