/// <reference types="vite/client" />
type CoreEvent = { event: string; chat_id?: string; run_id?: string; [key: string]: any };
interface Window { lca: {
  listWorkspaces:()=>Promise<any>;
  saveWorkspace:(params:unknown)=>Promise<any>;
  selectWorkspace:(params:unknown)=>Promise<any>;
  deleteWorkspace:(params:unknown)=>Promise<any>;
  searchChats:(params:unknown)=>Promise<any>;
  updateChat:(params:unknown)=>Promise<any>;
  deleteChat:(params:unknown)=>Promise<any>;
  forkChat:(params:unknown)=>Promise<any>;
  exportChat:(params:unknown)=>Promise<any>;
  listExtensions:()=>Promise<any>;
  configureExtensions:(params:unknown)=>Promise<any>;
  discoverMcp:(params:unknown)=>Promise<any>;
  listConnections:()=>Promise<any>;
  saveConnection:(params:unknown)=>Promise<any>;
  deleteConnection:(params:unknown)=>Promise<any>;
  importPlugin:()=>Promise<any>;
  pickWorkspaceFolder:()=>Promise<any>;

  health: () => Promise<any>; chooseProject: () => Promise<any>;
  listFiles: (path?: string) => Promise<any>; readFile: (path: string) => Promise<any>; systemInfo: () => Promise<any>;
  pickRuntimeFile: (kind:string) => Promise<any>; startRuntime: (params:unknown) => Promise<any>; runtimeStatus: () => Promise<any>; stopRuntime: () => Promise<any>;
  getProjectMemory: () => Promise<any>; saveProjectMemory: (memory:unknown,revision:string) => Promise<any>; renameChat: (id:string,title:string,mode:string) => Promise<any>;
  telegramStatus:()=>Promise<any>;connectTelegram:(params:unknown)=>Promise<any>;disconnectTelegram:()=>Promise<any>;forgetTelegram:()=>Promise<any>;
  desktopSettings:()=>Promise<any>;configureDesktop:(enabled:boolean)=>Promise<any>;
  desktopApplications:()=>Promise<any>;addDesktopApplication:()=>Promise<any>;removeDesktopApplication:(id:string)=>Promise<any>;
  moveChat:(id:string,mode:string,target:string)=>Promise<any>;
  cancelHandoff:(id:string)=>Promise<any>;
  prepareHandoff:(id:string)=>Promise<any>;
  getCompanionSettings:()=>Promise<any>;configureCompanion:(params:unknown)=>Promise<any>;
  transcribe:(audio:string)=>Promise<any>;cancelTranscription:()=>Promise<any>;
  voicePlayback:(params:unknown)=>Promise<any>;openTtsFolder:()=>Promise<any>;
  speechRuntime:(operation:'status'|'start'|'stop'|'install')=>Promise<any>;
  activateAssistant:()=>Promise<any>;wakeListening:(enabled:boolean)=>Promise<any>;
  voiceStatus: () => Promise<any>; refreshVoices: () => Promise<any>; speak: (params:unknown) => Promise<any>; stopVoice: () => Promise<any>;
  searchProject: (params: unknown) => Promise<any>; cancelProjectSearch: () => Promise<any>;
  editorRead: (path: string) => Promise<any>; editorPreview: (path: string, content: string, revision: unknown) => Promise<any>;
  editorResolve: (proposalId: string, decision: string) => Promise<any>; setEditorDirty: (dirty: boolean) => Promise<any>;
  confirmEditorDiscard: () => Promise<{discard: boolean}>;
  configureModel: (config: {base_url: string; model: string; api_key: string; api_protocol?:string; tool_protocol?: string; settings?: Record<string, number>}) => Promise<any>;
  listModels: (config?: unknown) => Promise<any>; listChats: (mode?: string) => Promise<any>; newChat: (mode?: string) => Promise<any>; loadChat: (id: string, mode?: string) => Promise<any>;
  testModel: (config: unknown) => Promise<any>; cancelModelSetup: () => Promise<any>;
  getModelSettings: () => Promise<any>;
  startTask: (prompt: string, resume?: boolean, mode?: string) => Promise<any>; cancelTask: () => Promise<any>;
  resolveApproval: (run: string, approval: string, decision: string) => Promise<any>;
  onEvent: (callback: (event: CoreEvent) => void) => () => void;
} }
