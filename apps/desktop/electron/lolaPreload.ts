import {contextBridge,ipcRenderer} from 'electron';
import type {LolaDesktopAction,LolaDesktopSettings,LolaDesktopFrame} from '../shared/lolaDesktop';
import './preload';
contextBridge.exposeInMainWorld('lola',{
  status:()=>ipcRenderer.invoke('lola-widget:status'),
  ready:()=>ipcRenderer.invoke('lola-widget:ready'),
  action:(value:LolaDesktopAction)=>ipcRenderer.invoke('lola-widget:action',value),
  showMain:()=>ipcRenderer.invoke('lola-widget:main'),
  menu:()=>ipcRenderer.invoke('lola-widget:menu'),
  hover:(value:boolean)=>ipcRenderer.invoke('lola-widget:hover',value),
  move:(x:number,y:number)=>ipcRenderer.invoke('lola-widget:move',{x,y}),
  onState:(callback:(value:{settings:LolaDesktopSettings;frame:LolaDesktopFrame})=>void)=>{
    const receive=(_event:Electron.IpcRendererEvent,value:{settings:LolaDesktopSettings;frame:LolaDesktopFrame})=>callback(value);
    ipcRenderer.on('lola-widget:state',receive);return()=>ipcRenderer.removeListener('lola-widget:state',receive);
  },
});
