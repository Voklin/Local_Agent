/// <reference types="vite/client" />
type CoreEvent = { event: string; chat_id?: string; run_id?: string; [key: string]: any };
interface Window { lca: {
  health: () => Promise<any>; chooseProject: () => Promise<any>;
  listFiles: (path?: string) => Promise<any>; readFile: (path: string) => Promise<any>; systemInfo: () => Promise<any>;
  configureModel: (config: {base_url: string; model: string; api_key: string}) => Promise<any>;
  listModels: () => Promise<any>; listChats: () => Promise<any>; newChat: () => Promise<any>; loadChat: (id: string) => Promise<any>;
  getModelSettings: () => Promise<any>;
  startTask: (prompt: string, resume?: boolean) => Promise<any>; cancelTask: () => Promise<any>;
  resolveApproval: (run: string, approval: string, decision: string) => Promise<any>;
  onEvent: (callback: (event: CoreEvent) => void) => () => void;
} }
