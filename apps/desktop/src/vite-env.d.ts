/// <reference types="vite/client" />
type CoreEvent = { event: string; chat_id?: string; run_id?: string; [key: string]: any };
interface Window { lca: {
  health: () => Promise<any>; chooseProject: () => Promise<any>;
  listFiles: (path?: string) => Promise<any>; readFile: (path: string) => Promise<any>; systemInfo: () => Promise<any>;
  searchProject: (params: unknown) => Promise<any>; cancelProjectSearch: () => Promise<any>;
  editorRead: (path: string) => Promise<any>; editorPreview: (path: string, content: string, revision: unknown) => Promise<any>;
  editorResolve: (proposalId: string, decision: string) => Promise<any>; setEditorDirty: (dirty: boolean) => Promise<any>;
  confirmEditorDiscard: () => Promise<{discard: boolean}>;
  configureModel: (config: {base_url: string; model: string; api_key: string; settings?: Record<string, number>}) => Promise<any>;
  listModels: (config?: unknown) => Promise<any>; listChats: (mode?: string) => Promise<any>; newChat: (mode?: string) => Promise<any>; loadChat: (id: string, mode?: string) => Promise<any>;
  testModel: (config: unknown) => Promise<any>; cancelModelSetup: () => Promise<any>;
  getModelSettings: () => Promise<any>;
  startTask: (prompt: string, resume?: boolean, mode?: string) => Promise<any>; cancelTask: () => Promise<any>;
  resolveApproval: (run: string, approval: string, decision: string) => Promise<any>;
  onEvent: (callback: (event: CoreEvent) => void) => () => void;
} }
