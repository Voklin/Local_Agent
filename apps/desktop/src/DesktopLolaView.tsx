import {useEffect,useRef,useState} from 'react';
import {Mic,Square,MessageCircle,Settings,MoreHorizontal,ArrowUp,PanelTop,History,Volume2} from 'lucide-react';
import {useLolaSession} from './useLolaSession';
import {ChatText} from './ChatText';
import {TaskProgress} from './TaskProgress';
import {ApprovalDialog} from './ApprovalDialog';
import {ConversationSidebar} from './ConversationSidebar';
import {DialogFocus} from './StudioControls';
import {LolaAvatar} from './LolaAvatar';
import {lolaDesktopDefaults,lolaInitialFrame,type LolaDesktopSettings,type LolaDesktopFrame} from '../shared/lolaDesktop';

export function DesktopLolaView(){
  const voice=useLolaSession();
  const [autoEnd,setAutoEnd]=useState(()=>localStorage.getItem('miya-auto-end')!=='off'),[autoSend,setAutoSend]=useState(()=>localStorage.getItem('miya-auto-send')==='on');
  const [history,setHistory]=useState(false),[rename,setRename]=useState<{id:string;title:string}|null>(null);
  const [settings,setSettings]=useState<LolaDesktopSettings>(lolaDesktopDefaults),[frame,setFrame]=useState<LolaDesktopFrame>(lolaInitialFrame);
  const [expanded,setExpanded]=useState(false),[text,setText]=useState(''),[notice,setNotice]=useState('');
  const drag=useRef<{x:number;y:number;moved:boolean}|null>(null),hover=useRef(false);
  const [motion,setMotion]=useState(()=>!matchMedia('(prefers-reduced-motion: reduce)').matches);
  useEffect(()=>{if(voice.draft){setText(voice.draft);setExpanded(true);voice.clearDraft();}},[voice.draft]);
  useEffect(()=>{if(voice.approval||voice.task?.recovery_items?.length)setExpanded(true);},[voice.approval,voice.task?.recovery_items?.length]);
  useEffect(()=>{
    const media=matchMedia('(prefers-reduced-motion: reduce)'),change=()=>setMotion(!media.matches);media.addEventListener('change',change);
    void window.lola.status().then(result=>{if(result.ok){setSettings(result.settings);setFrame(result.frame);}});
    const unsubscribe=window.lola.onState(value=>{setSettings(value.settings);setFrame(value.frame);});
    function pointer(event:MouseEvent){const hit=!!(event.target as Element)?.closest('[data-lola-hit]');if(hit!==hover.current){hover.current=hit;void window.lola.hover(hit);}}
    function leave(){hover.current=false;void window.lola.hover(false);}
    window.addEventListener('mousemove',pointer);window.addEventListener('blur',leave);
    return()=>{unsubscribe();media.removeEventListener('change',change);window.removeEventListener('mousemove',pointer);window.removeEventListener('blur',leave);};
  },[]);
  async function action(kind:'record'|'stop'|'settings'|'ask'|'speak'){
    setNotice('');const result=await window.lola.action({action:kind,...(kind==='ask'?{text}:{})});if(!result.ok)setNotice(result.error||'Действие не выполнено');else if(kind==='ask')setText('');
  }
  return <main className="desktop-lola" data-state={frame.state} style={{'--lola-size':settings.size+'px'} as React.CSSProperties}>
    {voice.engine}<DialogFocus/>
    <section className={`lola-bubble${expanded?' expanded':''}`} data-lola-hit>
      <div className="lola-bubble-heading"><b>Лола</b><span>{frame.recording?'Микрофон включён':frame.wake?'Активация голосом включена':frame.caption}</span><button aria-label="Меню Лолы" onClick={()=>void window.lola.menu()}><MoreHorizontal size={16}/></button></div>
      {history&&<div className="lola-history"><ConversationSidebar mode="voice" showWorkspace={false} root="" visible busy={voice.busy} navigating={voice.selecting} activeId={voice.chatId} refresh={voice.revision} workspaceId="" onWorkspace={async()=>false} onOpen={id=>{void voice.select(id);setHistory(false);setExpanded(true);}} onRename={setRename} onReset={()=>void voice.select()} onFork={r=>{void voice.select(r.chat.id);setText(r.prompt||'');setHistory(false);setExpanded(true);}} onError={setNotice}/></div>}
      {expanded&&<><div className="lola-conversation" aria-label="Разговор с Лолой">{voice.chat.length?voice.chat.map((message,index)=><div className={'lola-message '+message.role} key={message.id||index}><small>{message.role==='user'?'Вы':'Лола'}</small><ChatText text={message.text}/></div>):<p className="lola-reply">Я рядом. Можно написать вопрос или нажать микрофон.</p>}</div><form onSubmit={e=>{e.preventDefault();void action('ask');}}><input aria-label="Вопрос настольной Лоле" maxLength={2000} placeholder="Чем помочь?" disabled={voice.busy||voice.selecting} value={text} onChange={e=>setText(e.target.value)}/><button aria-label="Отправить Лоле" disabled={voice.busy||voice.selecting||!text.trim()}><ArrowUp size={16}/></button></form>{voice.task?.recovery_items?.length||voice.task?.recovery_error?<TaskProgress task={voice.task} busy={voice.busy||voice.recoveryBusy} onResume={()=>void voice.resume()} onResolveRecovery={(item,resolution)=>void voice.resolve(item,resolution)}/>:null}</>}
      {voice.approval&&<ApprovalDialog approval={voice.approval} deciding={voice.deciding} onLater={()=>voice.setApproval(null)} onDecide={value=>void voice.decide(value)}/>}
      {expanded&&<details className="lola-recording-options"><summary>Параметры записи</summary><label><input type="checkbox" aria-label="Завершать запись после паузы" checked={autoEnd} onChange={e=>{setAutoEnd(e.target.checked);localStorage.setItem('miya-auto-end',e.target.checked?'on':'off');window.dispatchEvent(new Event('lola-recording-preferences'));}}/>Завершать после паузы</label><label><input type="checkbox" aria-label="Сразу отправлять распознанный запрос" checked={autoSend} onChange={e=>{setAutoSend(e.target.checked);localStorage.setItem('miya-auto-send',e.target.checked?'on':'off');window.dispatchEvent(new Event('lola-recording-preferences'));}}/>Отправлять после распознавания</label></details>}
      {rename&&<form className="lola-rename" onSubmit={e=>{e.preventDefault();void window.lca.renameChat(rename.id,rename.title,'voice').then(r=>{if(r.ok){setRename(null);void voice.select(rename.id);}else setNotice(r.error);});}}><input aria-label="Название разговора Лолы" maxLength={120} value={rename.title} onChange={e=>setRename({...rename,title:e.target.value})}/><button disabled={voice.busy||!rename.title.trim()}>Сохранить</button><button type="button" onClick={()=>setRename(null)}>Отмена</button></form>}
      <div className="lola-desktop-actions"><button aria-label={frame.recording?'Завершить запись Лолы':'Говорить с Лолой'} disabled={frame.busy&&!frame.recording} onClick={()=>void action('record')}><Mic size={15}/></button><button aria-label="Озвучить ответ Лолы" disabled={voice.busy||!voice.chat.some(m=>m.role==='assistant')} onClick={()=>void action('speak')}><Volume2 size={15}/></button><button aria-label="Остановить Лолу" onClick={()=>void action('stop')}><Square size={14}/></button><button aria-label="Вопрос и ответ Лолы" aria-expanded={expanded} onClick={()=>setExpanded(!expanded)}><MessageCircle size={16}/></button><button aria-label="Открыть настройки Лолы" onClick={()=>void action('settings')}><Settings size={15}/></button><button aria-label="Открыть Лешего" onClick={()=>void window.lola.showMain()}><PanelTop size={16}/></button></div>
      <button className="lola-history-toggle" aria-label="История Лолы" aria-expanded={history} onClick={()=>setHistory(!history)}><History size={13}/>Разговоры</button>
      {(notice||voice.notice)&&<p role="status">{notice||voice.notice}</p>}
    </section>
    <div className="lola-drag-character" data-lola-hit title="Перетащите Лолу. Нажмите, чтобы открыть разговор."
      onContextMenu={e=>{e.preventDefault();void window.lola.menu();}}
      onPointerDown={e=>{if(e.button!==0)return;drag.current={x:e.screenX,y:e.screenY,moved:false};e.currentTarget.setPointerCapture(e.pointerId);}}
      onPointerMove={e=>{const previous=drag.current;if(!previous)return;const x=e.screenX-previous.x,y=e.screenY-previous.y;if(Math.abs(x)+Math.abs(y)<2)return;previous.moved=true;previous.x=e.screenX;previous.y=e.screenY;void window.lola.move(Math.max(-200,Math.min(200,x)),Math.max(-200,Math.min(200,y)));}}
      onPointerUp={e=>{if(drag.current&&!drag.current.moved)setExpanded(!expanded);drag.current=null;e.currentTarget.releasePointerCapture(e.pointerId);}}
      onPointerCancel={()=>{drag.current=null;}}>
      <LolaAvatar state={frame.state} reducedMotion={!settings.animate||!motion}/>
    </div>
  </main>;
}
