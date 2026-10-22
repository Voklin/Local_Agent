import { contextBridge, ipcRenderer } from 'electron';
contextBridge.exposeInMainWorld('lca', {
  health: () => ipcRenderer.invoke('core:health'),
  chooseProject: () => ipcRenderer.invoke('project:choose'),
  listFiles: (relativePath = '.') => ipcRenderer.invoke('project:list', relativePath),
  readFile: (relativePath: string) => ipcRenderer.invoke('project:read', relativePath),
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
