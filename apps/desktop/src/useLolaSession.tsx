import {useEffect,useRef,useState} from 'react';
import {useTaskSession} from './useTaskSession';
import {VoicePanel} from './VoicePanel';
import {isTaskEvent,type ApprovalDecision} from '../shared/protocol';
import type {LolaVoiceAction} from '../shared/lolaDesktop';
import type {TaskRecoveryItem,TaskRecoveryResolution} from './TaskProgress';

/** The floating window owns its voice conversation; the main workspace stays intact. */
export function useLolaSession(){
 const session=useTaskSession(),{chat,setChat,task,setTask,busy,setBusy,stopping,setStopping,chatId,runId,active}=session;
 const [notice,setNotice]=useState(''),[approval,setApproval]=useState<CoreEvent|null>(null),[deciding,setDeciding]=useState(false),[revision,setRevision]=useState(0),[selecting,setSelecting]=useState(false),[recoveryBusy,setRecoveryBusy]=useState(false);
 const [draft,setDraft]=useState('');
 const [desktopAction,setDesktopAction]=useState<LolaVoiceAction|null>(null);
 const startPending=useRef(false),selectionPending=useRef(false),loadId=useRef(''),events=useRef<CoreEvent[]>([]),floor=useRef(0),ready=useRef<Promise<void>|null>(null),receive=useRef<(event:CoreEvent)=>void>(()=>{}),settingsReady=useRef(false);
 async function select(id?:string){if(selectionPending.current||startPending.current)return;selectionPending.current=true;setSelecting(true);loadId.current=id||'';events.current=[];try{
  const result=id?await window.lca.loadChat(id,'voice'):await window.lca.newChat('voice');if(!result.ok)throw Error(result.error);
  chatId.current=result.chat.id;runId.current=result.active_run?.run_id||'';floor.current=result.event_seq||0;active.current=!!result.active_run;setBusy(!!result.active_run);setStopping(false);setTask(result.task);setApproval(result.approval||null);
  setChat(result.chat.messages.filter((m:any)=>['user','assistant'].includes(m.role)&&typeof m.content==='string').map((m:any)=>({role:m.role,text:m.content,id:m.message_id,streaming:m.streaming})));
  const pending=events.current;events.current=[];loadId.current='';for(const event of pending)receive.current(event);setRevision(r=>r+1);setNotice('');
 }catch(error){setNotice(String(error));}finally{selectionPending.current=false;setSelecting(false);loadId.current='';}}
 async function send(text:string,resume=false){if(startPending.current||active.current||!text.trim()&&!resume)return;await ready.current;if(selectionPending.current||active.current)return;
  if(task?.recovery_items?.length||task?.recovery_error){setNotice('Сначала проверьте прерванные действия.');return;}
  startPending.current=true;active.current=true;setBusy(true);setStopping(false);setNotice('');
  try{if(!chatId.current){active.current=false;startPending.current=false;await select();active.current=true;startPending.current=true;}runId.current=crypto.randomUUID().replaceAll('-','');floor.current=0;if(!resume)setChat(rows=>[...rows,{role:'user',text:text.trim()}]);const result=await window.lca.startTask(text.trim(),resume,'voice',undefined,runId.current);if(!result.ok)throw Error(result.error);if(active.current)runId.current=result.run_id;}catch(error){setNotice(String(error));setBusy(false);active.current=false;}finally{startPending.current=false;}
 }
 async function stop(){setDesktopAction({id:Date.now(),action:'cancel'});await window.lca.stopVoice();if(runId.current){setStopping(true);const result=await window.lca.cancelTask(runId.current);if(!result.ok){setNotice(result.error);setStopping(false);}}}
 async function decide(value:ApprovalDecision){if(!approval||deciding)return;setDeciding(true);try{const result=await window.lca.resolveApproval(approval.run_id!,approval.approval_id,value);if(!result.ok)throw Error(result.error);setApproval(null);}catch(error){setNotice(String(error));}finally{setDeciding(false);}}
 async function resolve(item:TaskRecoveryItem,resolution:TaskRecoveryResolution){if(active.current||recoveryBusy||!task?.journal_id)return;setRecoveryBusy(true);try{const result=await window.lca.resolveToolRecovery({chat_id:chatId.current,journal_id:task.journal_id,message_index:item.message_index,call_id:item.call_id,resolution});if(!result.ok)throw Error(result.error);setTask(result.task);setRevision(r=>r+1);}catch(error){setNotice(String(error));}finally{setRecoveryBusy(false);}}
 receive.current=event=>{
  if(event.event==='lola_open_chat'){void ready.current?.then(()=>select(event.chat_id));return;}
  if(event.event==='lola_action'){if(event.action==='ask')void send(event.text||'');if(event.action==='speak')setDesktopAction({id:Date.now(),action:'speak'});if(event.action==='record')setDesktopAction({id:Date.now(),action:'record'});if(event.action==='stop')void stop();return;}
  if(event.event==='backend_stopped'){setBusy(false);active.current=false;setApproval(null);setNotice('Python Core остановлен');return;}
  if(event.chat_id&&event.chat_id===loadId.current){events.current.push(event);return;}
  if(event.event==='remote_task'&&event.mode==='voice'){chatId.current=event.chat.id;runId.current=event.run_id||'';active.current=true;floor.current=0;setBusy(true);setTask(null);setChat([{role:'user',text:event.prompt}]);return;}
  if(event.chat_id!==chatId.current||(runId.current&&event.run_id!==runId.current)||event.event_seq&&event.event_seq<=floor.current)return;
  if(event.event_seq)floor.current=event.event_seq;
  if(isTaskEvent(event)&&session.accepts(event))session.reduce(event);
  if(event.event==='approval'){setApproval(event);setDeciding(false);}
  if(event.event==='task_end'){setApproval(null);setRevision(r=>r+1);}
  if(event.event==='warning'||event.event==='failed')setNotice(event.text);
  if(event.event==='handoff')void window.lola.showMain();
 };
 useEffect(()=>{const unsubscribe=window.lca.onEvent(event=>receive.current(event));
  if(!ready.current)ready.current=(async()=>{try{const list=await window.lca.listChats('voice');await select(list.ok?list.chats[0]?.id:undefined);settingsReady.current=true;}catch(error){setNotice(String(error));}})();
  void window.lola.ready();return unsubscribe;
 },[]);
 const engine=<VoicePanel headless onDraft={setDraft} attention={approval?'Нужно подтверждение':notice} desktopAction={desktopAction} task={task} recoveryBusy={recoveryBusy} onResume={()=>void send('',true)} onResolveRecovery={(item,value)=>void resolve(item,value)} activation={null} conversationKey={chatId.current} completed={task?.status==='completed'} messages={chat} busy={busy} onAsk={text=>void send(text)} onCancel={()=>void stop()} onChat={()=>void window.lola.showMain()}/>;
 return {engine,draft,clearDraft:()=>setDraft(''),chat,task,busy,stopping,notice,approval,deciding,setApproval,decide,select,selecting,chatId:chatId.current,revision,recoveryBusy,resolve,resume:()=>send('',true),ready:settingsReady.current};
}
