import { contextBridge, ipcRenderer } from 'electron';
contextBridge.exposeInMainWorld('lca', {
  health: () => ipcRenderer.invoke('core:health'),
  chooseProject: () => ipcRenderer.invoke('project:choose'),
  listFiles: (relativePath = '.') => ipcRenderer.invoke('project:list', relativePath),
  readFile: (relativePath: string) => ipcRenderer.invoke('project:read', relativePath),
  pickRuntimeFile: (kind:string) => ipcRenderer.invoke('runtime:pick',kind),
  startRuntime: (params:unknown) => ipcRenderer.invoke('runtime:start',params),
  runtimeStatus: () => ipcRenderer.invoke('runtime:status'),
  stopRuntime: () => ipcRenderer.invoke('runtime:stop'),
  getProjectMemory: () => ipcRenderer.invoke('memory:get'),
  saveProjectMemory: (memory:unknown,revision:string) => ipcRenderer.invoke('memory:save',memory,revision),
  renameChat: (id:string,title:string,mode:string) => ipcRenderer.invoke('chat:rename',id,title,mode),
  voiceStatus: () => ipcRenderer.invoke('voice:status'),
  refreshVoices: () => ipcRenderer.invoke('voice:refresh'),
  speak: (params:unknown) => ipcRenderer.invoke('voice:speak',params),
  stopVoice: () => ipcRenderer.invoke('voice:stop'),
  searchProject: (params: unknown) => ipcRenderer.invoke('project:search', params),
  cancelProjectSearch: () => ipcRenderer.invoke('project:cancel-search'),
  editorRead: (path: string) => ipcRenderer.invoke('editor:read', path),
  editorPreview: (path: string, content: string, revision: unknown) => ipcRenderer.invoke('editor:preview', path, content, revision),
  editorResolve: (proposalId: string, decision: string) => ipcRenderer.invoke('editor:resolve', proposalId, decision),
  setEditorDirty: (dirty: boolean) => ipcRenderer.invoke('editor:dirty', dirty),
  confirmEditorDiscard: () => ipcRenderer.invoke('editor:confirm-discard'),
  systemInfo: () => ipcRenderer.invoke('system:home'),
  configureModel: (config: { base_url: string; model: string; api_key: string; settings?: Record<string, number> }) => ipcRenderer.invoke('model:configure', config),
  listModels: (config?: unknown) => ipcRenderer.invoke('model:list', config),
  testModel: (config: unknown) => ipcRenderer.invoke('model:test', config),
  cancelModelSetup: () => ipcRenderer.invoke('model:cancel-setup'),
  getModelSettings: () => ipcRenderer.invoke('model:settings'),
  listChats: (mode = 'ide') => ipcRenderer.invoke('chat:list', mode),
  newChat: (mode = 'ide') => ipcRenderer.invoke('chat:new', mode),
  loadChat: (chatId: string, mode = 'ide') => ipcRenderer.invoke('chat:load', chatId, mode),
  startTask: (prompt: string, resume = false, mode = 'ide') => ipcRenderer.invoke('task:start', prompt, resume, mode),
  cancelTask: () => ipcRenderer.invoke('task:cancel'),
  resolveApproval: (runId: string, approvalId: string, decision: string) => ipcRenderer.invoke('task:approve', runId, approvalId, decision),
  onEvent: (callback: (event: unknown) => void) => {
    const listener = (_event: Electron.IpcRendererEvent, data: unknown) => callback(data);
    ipcRenderer.on('core:event', listener);
    return () => ipcRenderer.removeListener('core:event', listener);
  }
});
