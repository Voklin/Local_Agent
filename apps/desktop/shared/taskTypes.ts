export type PlanNode={id:string;title:string;kind:'analysis'|'change'|'verification';depends_on:string[];affected_files:string[];check_ids:string[];status?:string;advisory?:boolean;evidence?:unknown[];note?:string};
import type {RequestBudgetSnapshot,ModelUsageSnapshot} from './contextTypes';
export type TaskStage = { id: string; title: string; objective?: string; status: string };
export type ToolActivity = { id: number; tool: string; path: string; status: string; summary: string; stage: string };
export type TaskRecoveryItem = { call_id: string; message_index: number; tool: string; path?: string; summary?: string };
export type TaskRecoveryResolution = 'completed' | 'not_executed';
export type TaskSnapshot = {
  status: string; last_event: string; stage: string; turn: number; tool_calls: number;
  stages: TaskStage[]; tool_activity?: ToolActivity[]; activity_omitted?: number;
  workspace_changes?:{id:string;operation:string;path:string;destination?:string}[];project_instructions?:{path:string;scope:string;sha256:string}[];
  progress_watchdog?:{recovery_attempts:number};
  children?:{id:string;state:string;event:string;turn?:number;tool_calls?:number;activity?:Partial<ToolActivity>[];profile?:{title?:string;id?:string;version?:number}}[];
  options?:any;plan_steps?:(string|PlanNode)[];workspace_generation?:number;workspace_reverted?:boolean;workspace_reviewed?:boolean;snapshot_attention?:{id:string;status:string}[];checks_notice?:string;
  acceptance_evidence?:{id:string;description:string;status:string}[];
  verification_selection?:{required:string[];not_applicable:string[]};
  test_results?:{id:string;kind?:string;diagnostics?:{line:number;column:number;severity:number;message:string}[];program:string;arguments?:string[];purpose?:string;exit_code:number|null;ok:boolean;generation?:number;evidence_status?:string;evidence_summary?:string;coverage?:{kind:string;project_complete:boolean;files?:string[];dependencies?:string[]}}[];
  modified_files?: string[]; stop_reason?: string;
  run_state?: 'running'|'waiting_approval'|'executing'|'verifying'|'completed'|'needs_attention'|'paused'|'failed';
  journal_id?: string; recovery_items?: TaskRecoveryItem[]; recovery_error?: string;
  verification?:{status:'not_run'|'failed'|'commands_passed'|'scoped_passed'|'stale'|'incomplete';summary:string;uncovered?:string[];execution_status?:string;project_complete?:boolean};
  budget?:RequestBudgetSnapshot;usage?:ModelUsageSnapshot;
  chat_id?:string;run_id?:string;run_ledger?:import('./contextTypes').RunLedgerSnapshot;
  context_pack?:{version?:number;status:string;sources:{path:string;start_line:number;end_line:number;sha256:string;reason:string;kind:string}[];omitted?:number;budget_omitted?:number};
  context?:{compressed:boolean;before_chars:number;after_chars:number;archived_units?:number};
};

