import type {RpcResult} from './protocol';
export type OptionalSettings={
  research:{enabled:boolean;seconds:number;max_tokens:number};
  lsp:{enabled:boolean;program:string;arguments:string[];language:string;seconds:number};
  worktrees:{enabled:boolean};container:{enabled:boolean;image:string;memory_mb:number};
};
export type OptionalRequest={action:'research';query:string}|{action:'diagnostics';path:string}|{action:'container_status'|'worktree_list'}|{action:'worktree_create';name:string;confirmed:true}|{action:'worktree_diff'|'worktree_open';id:string}|{action:'worktree_remove';id:string;confirmed:true};
export type ManagedWorktree={id:string;name:string;path:string;root:string;commit:string;status:string;exists?:boolean;registered?:boolean};
export type LanguageDiagnostic={line:number;column:number;severity:number;message:string;source:string};
export type OptionalResult=RpcResult<{
  root:string;text?:string;complete?:boolean;requests?:number;source_chars?:number;elapsed_ms?:number;
  sources?:{path:string;start_line:number;end_line:number;sha256:string}[];usage?:Record<string,number>;
  diagnostics?:LanguageDiagnostic[];path?:string;stale?:boolean;truncated?:boolean;
  worktrees?:ManagedWorktree[];worktree?:ManagedWorktree;status?:string;diff?:string;
  available?:boolean;docker?:boolean;wsl?:boolean;notice?:string;
}>;
export type OptionalCatalog=RpcResult<{settings:OptionalSettings;running:boolean;warning?:string;inference:{busy:boolean;kind?:string;limit:number}}>;
