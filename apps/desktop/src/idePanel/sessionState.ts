import type {TaskSnapshot} from '../../shared/taskTypes';
import type {TaskLifecycleEvent} from '../../shared/protocol';
import type {GenerationSettings} from '../GenerationFields';

export type Line={role:string;text:string;id?:string};
export type Reference={path:string;start:number;end:number};
export type SessionIdentity={chat:string;run:string;seq:number};
export type PanelApproval=Extract<TaskLifecycleEvent,{event:'approval'}>;
export type ModelConnection={ok:boolean;base_url:string;model:string;api_key?:string;api_protocol:'chat'|'responses';tool_protocol:'native'|'json';settings:GenerationSettings};
export type ChatSummary={id:string;title:string};
export type ChatSelection={ok:boolean;error?:string;chat:ChatSummary&{messages?:{role:string;content:unknown;message_id?:string}[]};task?:TaskSnapshot;approval?:PanelApproval;active_run?:{run_id:string};event_seq?:number};
export type SessionUpdate={identity:SessionIdentity;messages?:Line[];task?:TaskSnapshot;approval?:PanelApproval|null;fileEvent?:string;error?:string;ended?:boolean};

export function projectTaskEvent(identity:SessionIdentity,lines:Line[],event:TaskLifecycleEvent):SessionUpdate|null {
 if(!identity.run||event.chat_id!==identity.chat||event.run_id!==identity.run)return null;
 if(event.event_seq!==undefined&&(!Number.isSafeInteger(event.event_seq)||event.event_seq<0))return null;
 if(typeof event.event_seq==='number'&&event.event_seq<=identity.seq)return null;
 const next:SessionUpdate={identity:{...identity,seq:event.event_seq??identity.seq}};
 if(event.event==='text_delta'){
  const at=lines.findIndex(line=>line.id===event.message_id);
  next.messages=at<0?[...lines,{role:'assistant',text:event.text,id:event.message_id}]:lines.map((line,i)=>i===at?{...line,text:line.text+event.text}:line);
 }
 if(event.event==='chat'){
  const at=event.message_id?lines.findIndex(line=>line.id===event.message_id):-1;
  const line={role:event.role,text:event.text,id:event.message_id};next.messages=at<0?[...lines,line]:lines.map((old,i)=>i===at?line:old);
 }
 if(event.event==='result'&&lines.at(-1)?.role==='user')next.messages=[...lines,{role:'assistant',text:event.text}];
 if(event.event==='failed')next.error=event.text;
 if(event.event==='task')next.task=event.task;
 if(event.event==='approval')next.approval=event;
 if(event.event==='change'||event.event==='file_change')next.fileEvent=`${event.change.path}: ${event.change.status}`;
 if(event.event==='task_end'){next.identity.run='';next.approval=null;next.ended=true;}
 return next;
}
