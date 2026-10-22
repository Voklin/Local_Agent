import { contextBridge, ipcRenderer } from 'electron';
contextBridge.exposeInMainWorld('lca', {
  health: () => ipcRenderer.invoke('core:health'),
  chooseProject: () => ipcRenderer.invoke('project:choose'),
  listFiles: (relativePath = '.') => ipcRenderer.invoke('project:list', relativePath),
  readFile: (relativePath: string) => ipcRenderer.invoke('project:read', relativePath),
  systemInfo: () => ipcRenderer.invoke('system:home'),
  configureModel: (config: { base_url: string; model: string; api_key: string }) => ipcRenderer.invoke('model:configure', config),
  listModels: () => ipcRenderer.invoke('model:list'),
  getModelSettings: () => ipcRenderer.invoke('model:settings'),
  listChats: () => ipcRenderer.invoke('chat:list'),
  newChat: () => ipcRenderer.invoke('chat:new'),
  loadChat: (chatId: string) => ipcRenderer.invoke('chat:load', chatId),
  startTask: (prompt: string, resume = false) => ipcRenderer.invoke('task:start', prompt, resume),
  cancelTask: () => ipcRenderer.invoke('task:cancel'),
  resolveApproval: (runId: string, approvalId: string, decision: string) => ipcRenderer.invoke('task:approve', runId, approvalId, decision),
  onEvent: (callback: (event: unknown) => void) => {
    const listener = (_event: Electron.IpcRendererEvent, data: unknown) => callback(data);
    ipcRenderer.on('core:event', listener);
    return () => ipcRenderer.removeListener('core:event', listener);
  }
});
