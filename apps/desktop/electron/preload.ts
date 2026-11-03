import {contextBridge,ipcRenderer} from 'electron';
import {createApi} from '../shared/createApi';
contextBridge.exposeInMainWorld('lca',createApi(ipcRenderer));
