import type { TaskSnapshot,TaskRecoveryResolution } from './taskTypes';
import type { IdeOptions } from './ideTypes';

export const PROTOCOL_VERSION=1;
export type AgentMode='chat'|'ide'|'voice';
export type RpcFailure={ok:false;error:string;code?:string};
export type RpcResult<T extends object=Record<string,never>>=({ok:true}&T)|RpcFailure;
export type StartTaskOptions=IdeOptions&{checks_only?:boolean};
export type StartTaskResult=RpcResult<{run_id:string;chat_id:string}>;
export type ApprovalDecision='apply'|'reject'|'cancel';
export type RecoveryRequest={chat_id:string;journal_id:string;message_index:number;call_id:string;resolution:TaskRecoveryResolution};
export type SnapshotSummary={id:string;status:string;paths:string[];operations:string[];journal_id?:string};
export type SnapshotScope={chat_id:string};
export type SnapshotPreview={id:string;group_id:string;paths:string[];diff:string;truncated:boolean};
export type SnapshotListResult=RpcResult<{snapshots:SnapshotSummary[];task:TaskSnapshot|null}>;
export type SnapshotApplyResult=({ok:true;snapshots:SnapshotSummary[];task:TaskSnapshot|null;changed_paths?:string[]})|(RpcFailure&{snapshots?:SnapshotSummary[];task?:TaskSnapshot|null;changed_paths?:string[]});
export type TaskEventBase={protocol_version?:number;chat_id:string;run_id:string;event_seq?:number};
export type TaskLifecycleEvent=TaskEventBase&(
  {event:'task';task:TaskSnapshot}|{event:'task_end'}|{event:'text_delta';message_id:string;text:string}|
  {event:'chat';message_id?:string;role:string;text:string}|{event:'failed'|'result'|'warning'|'log';text:string}|
  {event:'progress';count:number;maximum:number}|
  {event:'approval';approval_id:string;path:string;diff:string;exists:boolean;kind?:string;title?:string}|
  {event:'change'|'file_change';change:{status:string;path:string;error?:string;[key:string]:unknown}}
);
export const TASK_EVENTS=new Set(['task','task_end','text_delta','chat','failed','result','warning','log','progress','approval','change','file_change']);
export function isTaskEvent(value:unknown):value is TaskLifecycleEvent {
  if(!value||typeof value!=='object')return false;
  const event=value as Record<string,unknown>;
  if(!TASK_EVENTS.has(String(event.event))||typeof event.chat_id!=='string'||typeof event.run_id!=='string')return false;
  if(event.event==='task')return !!event.task&&typeof event.task==='object';
  if(event.event==='text_delta'&&typeof event.message_id!=='string')return false;
  if(['text_delta','chat','failed','result','warning','log'].includes(String(event.event)))return typeof event.text==='string';
  if(event.event==='approval')return typeof event.approval_id==='string'&&typeof event.diff==='string';
  if(event.event==='change'||event.event==='file_change')return !!event.change&&typeof event.change==='object';
  return true;
}
export function rpcTimeout(method:string){
  const timeouts:Record<string,number>={optional_run:130000,snapshot_apply:120000,snapshot_preview:120000,storage_backup:300000,storage_status:60000,mcp_discover:125000,transcribe:95000,test_model:35000};
  return timeouts[method]||10000;
}
export function rpcCancellation(method:string):{method:string;params?:Record<string,unknown>}|null {
  const methods:Record<string,string>={storage_backup:'storage_cancel',storage_status:'storage_cancel',optional_run:'optional_cancel',transcribe:'cancel_transcription',list_models:'cancel_model_setup',test_model:'cancel_model_setup',search_project:'cancel_project_search',start_task:'cancel_task'};
  return methods[method]?{method:methods[method]}:null;
}
