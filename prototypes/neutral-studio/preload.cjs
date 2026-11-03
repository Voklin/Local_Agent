const {contextBridge,ipcRenderer}=require('electron');
contextBridge.exposeInMainWorld('neutralPrototype',{openLola:()=>ipcRenderer.invoke('prototype:open-lola')});
