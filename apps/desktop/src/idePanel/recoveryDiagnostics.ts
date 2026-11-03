import type {TaskSnapshot} from '../../shared/taskTypes';

type RecoveryState=Pick<TaskSnapshot,'recovery_error'|'recovery_items'|'snapshot_attention'>;
export function hasRecoveryBlockers(task:RecoveryState|null|undefined):boolean {
 return !!(task?.recovery_error||task?.recovery_items?.length||task?.snapshot_attention?.length);
}
function safeId(value:unknown):string|undefined {
 return typeof value==='string'&&/^[a-f0-9]{32,64}$/i.test(value)?value:undefined;
}
function count(value:unknown):number {
 return typeof value==='number'&&Number.isSafeInteger(value)&&value>=0?value:0;
}
export function recoveryDiagnostics(task:TaskSnapshot|null){
 // Deliberate allowlist: never export messages, paths, model settings or error narrative.
 return {schema:'leshy.recovery.v1',task:{chat_id:safeId(task?.chat_id),run_id:safeId(task?.run_id),journal_id:safeId(task?.journal_id),turn:count(task?.turn),tool_calls:count(task?.tool_calls)},
  recovery:{journal_unreadable:!!task?.recovery_error,snapshot_attention_count:task?.snapshot_attention?.length||0,
   unknown_actions:(task?.recovery_items||[]).slice(0,100).map(item=>({call_id:safeId(item.call_id),message_index:count(item.message_index)}))}};
}
