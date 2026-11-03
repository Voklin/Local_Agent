import { useEffect, useRef, useState } from 'react';
import { Search, X } from 'lucide-react';

type Match = {path:string; line:number; text:string};
type Props = {root:string; visible:boolean; quick:boolean; focus:number; onClose:()=>void; onOpen:(path:string,line:number)=>void};

export function ProjectSearch({root, visible, quick, focus, onClose, onOpen}:Props) {
  const [query,setQuery]=useState('');
  const [pattern,setPattern]=useState('');
  const [caseSensitive,setCaseSensitive]=useState(false);
  const [matches,setMatches]=useState<Match[]>([]);
  const [notice,setNotice]=useState('');
  const [busy,setBusy]=useState(false);
  const [selected,setSelected]=useState(0);
  const [kind,setKind]=useState('text');
  const [index,setIndex]=useState<any>(null);
  const input=useRef<HTMLInputElement>(null);
  const serial=useRef(0);
  const pending=useRef<Promise<unknown>|null>(null);
  const scope=useRef({root,visible,quick}); scope.current={root,visible,quick};

  async function search() {
    const ticket=++serial.current;
    const snapshot={root,visible,quick};
    setBusy(true); setNotice('Поиск…');
    try {
      if (pending.current) { await window.lca.cancelProjectSearch(); await pending.current; }
      if (ticket!==serial.current || !snapshot.root || !snapshot.visible) return;
      const request=window.lca.searchProject({mode:snapshot.quick?'files':kind,query,pattern:snapshot.quick?'':pattern,case_sensitive:caseSensitive,limit:snapshot.quick?1000:200});
      pending.current=request;
      const result=await request;
      if (ticket!==serial.current || scope.current.root!==snapshot.root || !scope.current.visible) return;
      setMatches(result.ok?result.matches:[]); setSelected(0);
      setNotice(result.ok?`${result.matches.length} результатов · ${result.backend==='project-index'?'по индексу':'обычный поиск'} · проверено файлов: ${result.scanned_files}${result.precision==='text'&&kind==='symbols'?' · текстовый fallback, точность определений не подтверждена':''}${result.truncated?' · Показана часть проекта ('+result.reason+')':''}`:result.error);
    } catch (error) { if (ticket===serial.current) setNotice(String(error)); }
    finally { if (ticket===serial.current) {pending.current=null;setBusy(false);} }
  }
  function cancel() {
    ++serial.current; setBusy(false); setNotice('Поиск отменён');
    void window.lca.cancelProjectSearch();
  }
  useEffect(()=>{
    ++serial.current; setMatches([]); setNotice(''); setBusy(false);
    void window.lca.cancelProjectSearch();
    if (visible) input.current?.focus();
    return ()=>{++serial.current;void window.lca.cancelProjectSearch();};
  },[root,visible,quick]);
  useEffect(()=>{if(visible) input.current?.focus();},[focus]);
  useEffect(()=>{
    let stopped=false;setIndex(null);
    if(!visible||!root)return;
    async function refresh(){try{const result=await window.lca.projectIndex({action:'status'});if(!stopped)setIndex(result);}catch{if(!stopped)setIndex({state:'degraded',reason:'Индекс недоступен; обычный поиск работает'});}}
    void refresh();const timer=setInterval(()=>void refresh(),1500);
    return ()=>{stopped=true;clearInterval(timer);};
  },[root,visible]);
  async function indexAction(action:string){try{setIndex(await window.lca.projectIndex({action}));}catch(error){setNotice(String(error));}}
  useEffect(()=>{
    if (!quick || !visible || !root) return;
    const timer=setTimeout(()=>void search(),250);
    return ()=>clearTimeout(timer);
  },[query,quick,visible,root]);
  if (!visible) return null;
  return <section className={quick?'project-search quick-open':'project-search'} aria-label={quick?'Быстрое открытие':'Поиск по проекту'}>
    {index&&<div className="index-status" data-index-state={index.state}><span>{({ready:'Индекс готов',building:'Создание индекса',updating:'Индекс обновляется',needs_rebuild:'Нужна пересборка индекса',degraded:'Поиск без индекса'} as Record<string,string>)[index.state]||'Индекс'} · {index.files||0} файлов</span><small>{index.reason}</small>{['building','updating'].includes(index.state)?<button type="button" onClick={()=>void indexAction('cancel')}>Остановить индексацию</button>:<button type="button" onClick={()=>void indexAction('rebuild')}>Пересобрать индекс</button>}</div>}
    {index?.parser_errors>0&&<p className="search-notice">Не все файлы распознаны. Для них используйте текстовый поиск.</p>}
    {quick&&<div className="search-heading"><b>Быстрое открытие</b><button onClick={onClose} title="Закрыть"><X size={16}/></button></div>}
    <form onSubmit={e=>{e.preventDefault();if(quick&&matches[selected])onOpen(matches[selected].path,1);else void search();}}>
      {!quick&&<select aria-label="Тип поиска по проекту" value={kind} onChange={event=>setKind(event.target.value)}><option value="text">Текст</option><option value="symbols">Определения символов</option></select>}
      <input ref={input} aria-label={quick?'Имя файла':'Текст поиска по проекту'} placeholder={quick?'Имя или часть пути…':'Найти текст…'} value={query} maxLength={200} disabled={!root} onChange={e=>setQuery(e.target.value)} onKeyDown={e=>{
        if(e.key==='Escape'){e.preventDefault();cancel();if(quick)onClose();}
        if(quick&&['ArrowDown','ArrowUp'].includes(e.key)){e.preventDefault();setSelected(n=>Math.max(0,Math.min(matches.length-1,n+(e.key==='ArrowDown'?1:-1))));}
      }}/>
      {!quick&&<><input aria-label="Маска файлов" placeholder="Маска файлов, например *.py" value={pattern} maxLength={120} onChange={e=>setPattern(e.target.value)}/><label><input type="checkbox" checked={caseSensitive} onChange={e=>setCaseSensitive(e.target.checked)}/>Учитывать регистр</label><button type="submit" disabled={!root||!query.trim()}><Search size={14}/>Найти</button></>}
      {busy&&<button type="button" onClick={cancel}>Отменить поиск</button>}
    </form>
    <p className="search-notice" role="status">{root?notice:'Выберите папку проекта'}</p>
    <div className="search-results">{matches.map((match,index)=><button className={quick&&index===selected?'selected':''} key={`${match.path}:${match.line}:${index}`} onClick={()=>onOpen(match.path,match.line)}><b>{match.path}{!quick&&`:${match.line}`}</b>{!quick&&<span>{match.text}</span>}</button>)}</div>
  </section>;
}
