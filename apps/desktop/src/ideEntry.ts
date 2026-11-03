import {startAppearanceSync} from './AppearanceSettings';
import {createApi} from '../shared/createApi';
// Webview has no Node/IPC access; the extension validates every forwarded channel.
declare function acquireVsCodeApi():{postMessage:(message:unknown)=>void;getState:()=>unknown;setState:(state:unknown)=>void};
const host=acquireVsCodeApi(),pending=new Map<string,{resolve:(value:any)=>void;timer:ReturnType<typeof setTimeout>}>(),listeners=new Set<(event:unknown,data:any)=>void>();
window.neutralIdeHost=true;document.documentElement.classList.add('neutral-ide-document');
const saved=host.getState() as {draft?:string;checkDraft?:import('./idePanel/acceptanceChecks').AcceptanceDraft}|undefined;window.neutralIdeDraft=typeof saved?.draft==='string'?saved.draft:'';window.neutralIdeCheckDraft=saved?.checkDraft;
window.addEventListener('neutral-draft',event=>host.setState({...host.getState() as object,draft:(event as CustomEvent<string>).detail}));
window.addEventListener('neutral-check-draft',event=>{window.neutralIdeCheckDraft=(event as CustomEvent<import('./idePanel/acceptanceChecks').AcceptanceDraft>).detail;host.setState({...host.getState() as object,checkDraft:window.neutralIdeCheckDraft});});
window.lca=createApi({
 invoke:(channel,...args)=>new Promise(resolve=>{const id=crypto.randomUUID();const timer=setTimeout(()=>{pending.delete(id);resolve({ok:false,error:'IDE: время ожидания истекло. Проверьте подключение к Neutral.'});},180000);pending.set(id,{resolve,timer});host.postMessage({id,channel,args});}),
 on:(_channel,listener)=>listeners.add(listener),removeListener:(_channel,listener)=>listeners.delete(listener)
});
window.addEventListener('message',event=>{const message=event.data;if(message?.event){for(const listener of listeners)listener(null,message.event);return;}const entry=pending.get(message?.id);if(entry){clearTimeout(entry.timer);pending.delete(message.id);entry.resolve(message.result);}});
startAppearanceSync();
void import('./idePanel/entry');
