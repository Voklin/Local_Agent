import { useRef,useState } from 'react';
import { isTaskEvent,type TaskLifecycleEvent } from '../shared/protocol';
import type { TaskSnapshot } from './TaskProgress';

export type SessionMessage={role:string;text:string;id?:string;streaming?:boolean};

export function useTaskSession(){
  const [chat,setChat]=useState<SessionMessage[]>([]);
  const [task,setTask]=useState<TaskSnapshot|null>(null),[busy,setBusy]=useState(false),[stopping,setStopping]=useState(false);
  const chatId=useRef(''),runId=useRef(''),active=useRef(false);
  function accepts(event:unknown):event is TaskLifecycleEvent {
    if(!active.current||!isTaskEvent(event)||event.chat_id!==chatId.current)return false;
    if(runId.current&&event.run_id!==runId.current)return false;
    // Bind before the asynchronous start response, including terminal events.
    if(active.current&&!runId.current)runId.current=event.run_id;
    return true;
  }
  function reduce(event:TaskLifecycleEvent){
    if(event.event==='text_delta')setChat(messages=>{const index=messages.findIndex(m=>m.id===event.message_id);return index<0?[...messages,{role:'assistant',text:event.text,id:event.message_id,streaming:true}]:messages.map((m,i)=>i===index?{...m,text:m.text+event.text,streaming:true}:m);});
    if(event.event==='chat')setChat(messages=>{const index=event.message_id?messages.findIndex(m=>m.id===event.message_id):-1;const message={role:event.role,text:event.text,id:event.message_id,streaming:false};return index<0?[...messages,message]:messages.map((m,i)=>i===index?message:m);});
    if(event.event==='result')setChat(messages=>messages.at(-1)?.role==='user'?[...messages,{role:'assistant',text:event.text}]:messages);
    if(event.event==='failed')setChat(messages=>[...messages,{role:'system',text:event.text}]);
    if(event.event==='task')setTask(event.task);
    if(event.event==='task_end'){active.current=false;setBusy(false);setStopping(false);runId.current='';setChat(messages=>messages.map(m=>m.streaming?{...m,streaming:false}:m));}
  }
  return {chat,setChat,task,setTask,busy,setBusy,stopping,setStopping,chatId,runId,active,accepts,reduce};
}
