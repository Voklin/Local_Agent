export type EvidenceScope={kind:'workspace'}|{kind:'files';files:string[];dependencies:string[]};
export type ValidationCommand={kind?:'test'|'lint'|'types'|'syntax'|'custom'|'diagnostics';applies_to?:string[];id:string;purpose:string;program:string;arguments:string[];cwd:string;timeout:number;evidence_scope?:EvidenceScope};
export type IdeOptions={read_only:boolean;auto_checks:boolean;criteria:string[];criteria_links:Record<string,string[]>;checks:ValidationCommand[]};
