export type RequestBudgetSnapshot = {
  window_tokens:number;input_tokens_estimate:number;output_tokens_reserved:number;safety_tokens:number;
  remaining_tokens:number;status:'fits'|'blocked';estimated:boolean;components:{instructions:number;history:number;tools:number;protocol:number};
  compressed?:boolean;reasons?:string[];mcp_loaded?:number;mcp_available?:number;
  mode?:'auto'|'manual';context_source?:string;counter?:string;server_adjustments?:number;tools_deferred?:number;output_adjusted?:boolean;
};
export type ModelUsageSnapshot = {input_tokens?:number;output_tokens?:number;requests?:number;requests_reported?:number;reported?:boolean};
export type RunLedgerSnapshot={http_attempts:number;requests_reported:number;input_tokens:number;output_tokens:number;reservations:number;active_reserved_tokens:number;interrupted:number;queue_ms:number;queued_requests:number;elapsed_ms?:number;approval_ms?:number};
export type RunSnapshot={id:string;parent_id:string|null;kind:string;model:string;state:string;created_at:string;elapsed_ms:number;approval_ms:number;tool_calls:number;recovered?:boolean;recovery_cause?:'owner_exited'|'owner_replaced';recovered_at?:string;spending?:{currency:string;limit:number;estimated_spent:number;reserved:number;unknown_attempts:number;remaining:number};ledger:RunLedgerSnapshot};

