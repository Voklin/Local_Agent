import {AsyncLocalStorage} from 'node:async_hooks';
import {DesktopLola} from './desktopLola';
import {NeutralIde} from './neutralIde';
import {PROTOCOL_VERSION,rpcTimeout,rpcCancellation} from '../shared/protocol';
import type {AgentMode,StartTaskOptions,ApprovalDecision} from '../shared/protocol';
import { app, BrowserWindow, dialog, ipcMain, session, desktopCapturer, shell, screen, safeStorage, clipboard, Notification as NativeNotification } from 'electron';
import { spawn, ChildProcessWithoutNullStreams } from 'node:child_process';
import { createInterface } from 'node:readline';
import path from 'node:path';
import os from 'node:os';
import fs from 'node:fs';
import { DesktopApplications } from './desktopApps';
import { SpeechRuntime } from './speechRuntime';
import { validateMusicURL, validateAudioPath } from './assistantMedia';

// Keep the existing Chromium profile and encrypted Telegram credentials after rebranding.
if(app.isPackaged&&!app.commandLine.hasSwitch('user-data-dir'))app.setPath('userData',path.join(app.getPath('appData'),'localagent'));
let managedSpeech:SpeechRuntime|null=null;
let desktopLola:DesktopLola|null=null;
let neutralIde:NeutralIde|null=null;
const ideScope=new AsyncLocalStorage<string>();
const localHandlers=new Map<string,(...args:any[])=>any>();
let wakeListening=false;
const lolaChats=new Set<string>(),lolaRuns=new Set<string>();
const ownsInstance=app.requestSingleInstanceLock();
if(!ownsInstance)app.quit();
app.on('second-instance',()=>{if(win?.isMinimized())win.restore();win?.show();win?.focus();});
function speechRuntime() {
  if(!managedSpeech)managedSpeech=new SpeechRuntime(
    path.join(process.env.LOCALAPPDATA||app.getPath('userData'),'LocalCodingAgent'),
    app.isPackaged?path.join(process.resourcesPath,'tts'):path.resolve(__dirname,'../../../tools/tts'),
    path.resolve(__dirname,'../../../artifacts/voice/serena-piper/ru_RU-miya-serena-medium.onnx'));
  return managedSpeech;
}

function desktopApplications() {
  return new DesktopApplications(app.getPath('userData'),file=>new Promise<void>((resolve,reject)=>{
    const child=spawn(file,[],{shell:false,detached:true,stdio:'ignore',cwd:path.dirname(file)});
    child.once('error',reject);child.once('spawn',()=>{child.unref();resolve();});
  }),()=>shell.openExternal('https://www.bing.com/'));
}

let win: BrowserWindow | null = null;
let backend: ChildProcessWithoutNullStreams | null = null;
let requestId = 0;
let editorDirty = false;
let confirmingClose = false;
let quitting = false;
let selectedRuntime = '';
let selectedModel = '';
function bundledRuntimePath() {
  const candidate = app.isPackaged
    ? path.join(process.resourcesPath, 'runtime/llama/llama-server.exe')
    : path.resolve(__dirname, '../../../build/windows-deps/llama/llama-server.exe');
  return fs.existsSync(candidate) ? candidate : '';
}
const pending = new Map<number, { resolve: (value: any) => void; timer: ReturnType<typeof setTimeout> }>();
function diagnostic(message: string) {
  try {
    const directory = path.join(app.getPath('userData'), 'logs');
    fs.mkdirSync(directory, { recursive: true });
    const file = path.join(directory, 'main.log');
    if (fs.existsSync(file) && fs.statSync(file).size > 1_000_000) fs.writeFileSync(file, '');
    fs.appendFileSync(file, `${new Date().toISOString()} ${message}\n`, 'utf8');
  } catch { /* Diagnostics must not prevent startup or shutdown. */ }
}
async function desktopRequest(message:any) {
  let result:any={ok:false,error:'Неизвестная операция ПК'};
  try {
    if(message.operation==='screenshot') {
      const displays=await desktopCapturer.getSources({types:['screen'],thumbnailSize:{width:1280,height:720}});
      const primary=String(screen.getPrimaryDisplay().id);
      const source=displays.find(item=>item.display_id===primary)||displays[0];
      if(!source||source.thumbnail.isEmpty())throw Error('Снимок экрана недоступен');
      publish({event:'desktop_artifact',image:source.thumbnail.toDataURL(),title:'Скриншот экрана'});
      result={ok:true,capture_id:message.request_id,note:'Скриншот показан в приложении. Без VLM модель не получает изображение и не должна описывать его содержимое.'};
    }else if(message.operation==='list_applications') {
      result={ok:true,applications:desktopApplications().list()};
    }else if(message.operation==='open_application') {
      result=await desktopApplications().open(String(message.args?.app_id||''));
    }else if(message.operation==='search') {
      const query=String(message.args?.query||'');if(!query||query.length>500)throw Error('Некорректный запрос');
      await shell.openExternal('https://www.bing.com/search?q='+encodeURIComponent(query));result={ok:true};
    }else if(message.operation==='music') {
      await shell.openExternal(validateMusicURL(message.args?.url));result={ok:true,browser_opened:true,playback_confirmed:false};
    }else if(message.operation==='local_audio') {
      const error=await shell.openPath(validateAudioPath(message.args?.path,message.args?.roots));
      result=error?{ok:false,error}:{ok:true,player_opened:true,playback_confirmed:false};
    }
  }catch(error){result={ok:false,error:String(error)};}
  await callBackend('desktop_result',{request_id:message.request_id,result});
}
function publish(message: any) {
  neutralIde?.publish(message);
  if(message.event==='ide_editor')return;
  if(message.mode==='voice'&&message.chat_id)lolaChats.add(message.chat_id);
  if(message.chat_id&&lolaChats.has(message.chat_id)&&message.run_id)lolaRuns.add(message.run_id);
  if(message.event==='backend_stopped'){lolaChats.clear();lolaRuns.clear();}
  if (win && !win.isDestroyed()) win.webContents.send('core:event', message);
  desktopLola?.sendEvent(message);
}
function startBackend() {
  if (backend) return;
  const root = app.isPackaged ? path.join(process.resourcesPath, 'core') : path.resolve(__dirname, '../../../core/python');
  const python = app.isPackaged ? path.join(root, 'lca-core.exe') : process.env.LCA_PYTHON || (process.platform === 'win32' ? 'python' : 'python3');
  const env: NodeJS.ProcessEnv = { ...process.env, NEUTRAL_NODE_PATH:process.execPath, PYTHONIOENCODING: 'utf-8', NEUTRAL_NATIVE_IDE:app.commandLine.hasSwitch('legacy-ide')?'0':'1' };
  if (app.isPackaged) { delete env.PYTHONHOME; delete env.PYTHONPATH; }
  diagnostic(`core:start packaged=${app.isPackaged}`);
  const child = spawn(python, app.isPackaged ? [] : ['-u', path.join(root, 'bridge.py')], { cwd: root, stdio: ['pipe', 'pipe', 'pipe'], windowsHide: true, env });
  backend = child;
  createInterface({ input: child.stdout }).on('line', (line) => {
    try {
      const msg = JSON.parse(line);
      if(msg.protocol_version!==PROTOCOL_VERSION){const entry=pending.get(msg.id);if(entry){clearTimeout(entry.timer);pending.delete(msg.id);entry.resolve({ok:false,error:'Версии интерфейса и Core несовместимы'});}return;}
      if(msg.event==='assistant_notice'&&NativeNotification.isSupported()){try{new NativeNotification({title:String(msg.title||'Лола').slice(0,160),body:String(msg.text||'').slice(0,300)}).show();}catch{diagnostic('assistant:notification-unavailable');}}
      if (typeof msg.event === 'string') { if(msg.event==='desktop_request')void desktopRequest(msg);else publish(msg); return; }
      const entry = pending.get(msg.id);
      if (entry) { clearTimeout(entry.timer); pending.delete(msg.id); entry.resolve(msg); }
    } catch { /* Backend output is data, never commands. */ }
  });
  child.stderr.on('data', (chunk) => console.error('[Python Core]', String(chunk).slice(0, 2000)));
  let closed = false;
  const stopped = () => {
    if (closed) return;
    closed = true;
    if (backend === child) backend = null;
    for (const entry of pending.values()) { clearTimeout(entry.timer); entry.resolve({ ok: false, error: 'Python Core остановлен. Выберите проект заново.' }); }
    pending.clear();
    publish({ event: 'backend_stopped' });
  };
  child.on('error', (error: NodeJS.ErrnoException) => { diagnostic(`core:error code=${error.code || 'unknown'}`); stopped(); });
  child.on('exit', (code, signal) => { diagnostic(`core:exit code=${code} signal=${signal}`); stopped(); });
  child.stdin.on('error', stopped);
}
function callBackend(method: string, params: Record<string, unknown> = {}) {
  const scope=ideScope.getStore();
  if (quitting) return Promise.resolve({ok:false,error:'Приложение завершает работу'});
  if (pending.size >= 100) return Promise.resolve({ ok: false, error: 'Слишком много запросов' });
  startBackend();
  const id = ++requestId;
  return new Promise<any>((resolve) => {
    const timer = setTimeout(() => {
      pending.delete(id);
      if(method==='mcp_discover')void callBackend('mcp_cancel_discovery',{id:params.id});
      const cancellation=rpcCancellation(method);if(cancellation&&(method!=='start_task'||typeof params.run_id==='string'))void callBackend(cancellation.method,method==='start_task'?{run_id:params.run_id}:cancellation.params);
      resolve({ ok: false, error: 'Python Core: время ожидания истекло' });
    }, rpcTimeout(method));
    timer.unref();
    pending.set(id, { resolve, timer });
    backend!.stdin.write(JSON.stringify({ id, method:scope?'ide_call':method, params:scope?{session_id:scope,method,params}:params, protocol_version:PROTOCOL_VERSION }) + '\n');
  });
}
function createWindow() {
  win = new BrowserWindow({ show: false, width: 1500, height: 940, minWidth: 1050, minHeight: 680, backgroundColor: '#15171c', title: 'ЛЕШИЙ / LESHY', icon:app.isPackaged?path.join(process.resourcesPath,'brand/leshy.png'):path.resolve(__dirname,'../../../assets/leshy.png'), webPreferences: { preload: path.join(__dirname, 'preload.cjs'), contextIsolation: true, nodeIntegration: false, sandbox: true } });
  win.on('close', (event) => {
    if (!editorDirty) {if(!quitting&&(desktopLola?.enabled||neutralIde?.connected)){event.preventDefault();win?.hide();}return;}
    event.preventDefault();
    if (confirmingClose) return;
    confirmingClose = true;
    void confirmEditorDiscard().then(result => {
      if (result.discard) { editorDirty = false; win?.close(); }
    }).finally(() => { confirmingClose = false; });
  });
  win.once('ready-to-show', () => {win?.show();win?.webContents.setBackgroundThrottling(!desktopLola?.enabled&&!wakeListening);});
  win.webContents.setWindowOpenHandler(() => ({ action: 'deny' }));
  win.webContents.on('will-navigate', (event) => event.preventDefault());
  win.webContents.on('render-process-gone', () => { void callBackend('cancel_task'); void callBackend('voice_stop'); });
  win.webContents.on('did-start-loading', () => { if (backend) void callBackend('cancel_task'); void callBackend('voice_stop'); });
  if (app.isPackaged||!app.commandLine.hasSwitch('development')) win.loadFile(path.join(__dirname, '../dist/index.html')); else win.loadURL('http://127.0.0.1:5173');
}
app.whenReady().then(() => { if(!ownsInstance)return; session.defaultSession.setPermissionRequestHandler((contents, permission, callback, details) => { callback((contents===win?.webContents || desktopLola?.owns(contents,contents.mainFrame)===true) && (permission==='clipboard-sanitized-write' || (permission==='media' && 'mediaTypes' in details && details.mediaTypes?.includes('audio')===true && details.mediaTypes.every(type=>type==='audio')))); }); diagnostic(`app:start version=${app.getVersion()} packaged=${app.isPackaged} platform=${process.platform} arch=${process.arch}`); desktopLola=new DesktopLola({directory:app.getPath('userData'),preload:path.join(__dirname,'lolaPreload.cjs'),html:path.join(__dirname,'../dist/lola.html'),devUrl:!app.isPackaged&&app.commandLine.hasSwitch('development')?'http://127.0.0.1:5173/lola.html':undefined,icon:app.isPackaged?path.join(process.resourcesPath,'brand/leshy.png'):path.resolve(__dirname,'../../../assets/leshy.png'),showMain:()=>{if(!win||win.isDestroyed())createWindow();if(win?.isMinimized())win.restore();win?.show();win?.focus();},dispatch:action=>publish({event:'lola_action',...action}),notify:settings=>{publish({event:'lola_config',settings});win?.webContents.setBackgroundThrottling(!settings.enabled&&!wakeListening);},quit:()=>app.quit()}); createWindow(); app.on('activate', () => { if (!win||win.isDestroyed()) createWindow();else{win.show();win.focus();} }); });
app.on('before-quit', event => {
  if (editorDirty) {
    event.preventDefault();
    if (confirmingClose) return;
    confirmingClose = true;
    void confirmEditorDiscard().then(result => {
      if (result.discard) { editorDirty = false; app.quit(); }
    }).finally(() => { confirmingClose = false; });
    return;
  }
  if(!quitting){void managedSpeech?.stop();desktopLola?.dispose();neutralIde?.dispose();}
  if (quitting || !backend) return;
  event.preventDefault(); quitting = true; diagnostic('app:quit');
  const child=backend;
  const deadline=setTimeout(()=>{child.kill();app.exit(1);},15000);
  child.once('exit',()=>{clearTimeout(deadline);app.quit();});
  child.stdin.end();
});
app.on('window-all-closed', () => { if (process.platform !== 'darwin') app.quit(); });
// The popup can use its voice session and audio services, never workspace/editor/model administration.
const lolaChannels=new Set(['appearance:get','core:health','lola:settings','lola:present','lola:microphone','companion:settings','companion:configure','voice:status','voice:refresh','voice:speak','voice:stop','voice:transcribe','voice:cancel-transcription','voice:playback','voice:activate','voice:listening','voice:runtime','run:active','workspace:list']);
function allowedLolaRequest(channel:string,args:any[]){
 if(['task:cancel','task:approve'].includes(channel))return typeof args[0]==='string'&&lolaRuns.has(args[0]);
 if(channel==='task:resolve-recovery')return lolaChats.has(args[0]?.chat_id);
 if(channel==='run:history')return lolaChats.has(args[0]);
 if(lolaChannels.has(channel))return true;
 if(['chat:list','chat:new'].includes(channel))return args[0]==='voice';
 if(channel==='chat:load'||channel==='chat:rename')return args[channel==='chat:load'?1:2]==='voice';
 if(['chat:search','chat:update','chat:delete','chat:fork','chat:export'].includes(channel))return args[0]?.mode==='voice';
 if(channel==='chat:move')return args[0]?.mode==='voice'&&args[0]?.target==='chat';
 if(channel==='task:start')return args[2]==='voice';
 return false;
}
function handle(channel: string, handler: (...args: any[]) => any) {
  localHandlers.set(channel,handler);
  ipcMain.handle(channel, async (event, ...args) => {
    const main=!!win&&!win.isDestroyed()&&event.sender===win.webContents&&event.senderFrame===win.webContents.mainFrame;
    if(!main&&!(desktopLola?.owns(event.sender,event.senderFrame)&&allowedLolaRequest(channel,args)))return {ok:false,error:'Forbidden sender'};
    return handler(...args);
  });
}
handle('lola:open',(value)=>{try{if(value?.chat_id!==undefined&&(typeof value.chat_id!=='string'||value.chat_id.length>160))return {ok:false,error:'Некорректный разговор'};return desktopLola?.open(value?.chat_id,value?.action)||{ok:false,error:'Лола загружается'};}catch(error){return {ok:false,error:String(error)};}});
handle('lola:settings',()=>desktopLola?.status()||{ok:false,error:'Спутник ещё загружается'});
handle('lola:configure',settings=>{try{return desktopLola?.configure(settings)||{ok:false,error:'Спутник ещё загружается'};}catch(error){return {ok:false,error:String(error instanceof Error?error.message:error)};}});
handle('lola:microphone',active=>{publish({event:'lola_microphone',active:active===true});return {ok:true};});
handle('lola:present',frame=>{desktopLola?.present(frame);return {ok:true};});
handle('workspace:list',()=>callBackend('workspace_list'));
handle('workspace:save',(params)=>callBackend('workspace_save',params));
handle('workspace:select',(params)=>callBackend('workspace_select',params));
handle('workspace:delete',(params)=>callBackend('workspace_delete',params));
handle('chat:search',(params)=>callBackend('chat_search',params));
handle('chat:update',(params)=>callBackend('chat_update',params));
handle('chat:delete',(params)=>callBackend('chat_delete',params));
handle('chat:fork',(params)=>callBackend('chat_fork',params));
handle('extensions:list',()=>callBackend('extensions_list'));
handle('extensions:configure',(params)=>callBackend('extensions_configure',params));
handle('extensions:discover',(params)=>callBackend('mcp_discover',params));
handle('extensions:cancel-discovery',(params)=>callBackend('mcp_cancel_discovery',params));
handle('connections:list',()=>callBackend('connections_list'));
handle('connections:save',(params)=>callBackend('connections_save',params));
handle('connections:delete',(params)=>callBackend('connections_delete',params));
handle('workspace:pick-folder',async()=>{
  const result=await dialog.showOpenDialog(win!,{title:'Папка проекта · необязательно',properties:['openDirectory']});
  return result.canceled?{canceled:true}:{ok:true,path:result.filePaths[0]};
});
handle('storage:status',()=>callBackend('storage_status'));
handle('storage:cancel',()=>callBackend('storage_cancel'));
handle('workspace:access',()=>callBackend('workspace_access'));
handle('workspace:access-configure',(paths:string[],confirmed:boolean)=>callBackend('workspace_access_configure',{paths,confirmed}));
handle('storage:backup',async()=>{
  const selected=await dialog.showSaveDialog(win!,{title:'Резервная копия Neutral',defaultPath:'Neutral-history-'+new Date().toISOString().slice(0,10)+'.zip',filters:[{name:'Архив ZIP',extensions:['zip']}]});
  if(selected.canceled||!selected.filePath)return {ok:true,canceled:true};
  return callBackend('storage_backup',{path:selected.filePath});
});
handle('chat:export',async(params)=>{
  const result=await callBackend('chat_export',params);
  if(!result.ok)return result;
  const selected=await dialog.showSaveDialog(win!,{title:'Экспорт разговора',defaultPath:'Neutral-chat.'+result.extension,filters:[{name:result.extension==='json'?'JSON':'Markdown',extensions:[result.extension]}]});
  if(selected.canceled||!selected.filePath)return {ok:true,canceled:true};
  try{await fs.promises.writeFile(selected.filePath,result.content,'utf8');return {ok:true,path:selected.filePath};}
  catch{return {ok:false,error:'Не удалось сохранить файл. Проверьте доступ к выбранной папке.'};}
});
handle('extensions:import',async()=>{
  const selected=await dialog.showOpenDialog(win!,{title:'Добавить плагин Neutral',properties:['openFile'],filters:[{name:'Манифест Neutral',extensions:['json']}]});
  if(selected.canceled||!selected.filePaths[0])return {canceled:true};
  try{const file=selected.filePaths[0];if((await fs.promises.stat(file)).size>200000)return {ok:false,error:'Манифест превышает 200 КБ'};
    return await callBackend('extensions_import',{manifest:JSON.parse(await fs.promises.readFile(file,'utf8'))});
  }catch{return {ok:false,error:'Не удалось прочитать JSON манифест плагина'};}
});
handle('optional:settings',()=>callBackend('optional_settings'));
handle('optional:configure',settings=>callBackend('optional_configure',{settings}));
handle('optional:run',params=>callBackend('optional_run',params));
handle('optional:cancel',()=>callBackend('optional_cancel'));
handle('optional:open-worktree',async(id:string)=>{
  if(editorDirty)return {ok:false,error:'Сначала сохраните или отмените правки в редакторе'};
  const result=await callBackend('optional_run',{action:'worktree_open',id});
  if(!result.ok)return result;
  return callBackend('set_project',{root:result.path});
});
// Shared presentation preference; stays outside Python settings and execution protocols.
const themeIds=new Set(['forest','parchment','twilight']);
let sharedTheme:string|undefined;
function readSharedTheme(fallback:unknown='forest') {
 if(sharedTheme)return sharedTheme;
 try{const value=JSON.parse(fs.readFileSync(path.join(app.getPath('userData'),'leshy-appearance.json'),'utf8')).theme;if(themeIds.has(value))sharedTheme=value;}catch{}
 if(!sharedTheme){sharedTheme=typeof fallback==='string'&&themeIds.has(fallback)?fallback:'forest';writeSharedTheme(sharedTheme);}
 return sharedTheme;
}
function writeSharedTheme(theme:string){const file=path.join(app.getPath('userData'),'leshy-appearance.json');fs.mkdirSync(path.dirname(file),{recursive:true});fs.writeFileSync(file+'.tmp',JSON.stringify({theme}));fs.renameSync(file+'.tmp',file);sharedTheme=theme;
 // Also reaches an open Code-OSS window without an attached project/agent bridge.
 const nativeFile=path.join(app.getPath('userData'),'neutral-ide/user-data/User/settings.json');
 try{const settings=JSON.parse(fs.readFileSync(nativeFile,'utf8'));const label=({forest:'LESHY Лесная',parchment:'LESHY Парчовая',twilight:'LESHY Сумеречная'} as Record<string,string>)[theme];if(settings['workbench.colorTheme']!==label){settings['workbench.colorTheme']=label;fs.writeFileSync(nativeFile,JSON.stringify(settings,null,2));}}catch{/* Preserve manually edited JSONC settings; connected windows use the bridge. */}
}
handle('appearance:get',(fallback)=>({ok:true,theme:readSharedTheme(fallback)}));
handle('appearance:set',(theme)=>{if(typeof theme!=='string'||!themeIds.has(theme))return {ok:false,error:'Неизвестная тема'};if(readSharedTheme()!==theme){writeSharedTheme(theme);publish({event:'appearance_theme',theme});}return {ok:true,theme};});
handle('core:health', () => callBackend('health'));
handle('ide:export-chat',params=>callBackend('chat_export',params));
handle('ide:workspace-changed',()=>callBackend('ide_workspace_changed'));
handle('ide:shell',()=>({ok:true,native_default:!app.commandLine.hasSwitch('legacy-ide')}));
handle('ide:open',()=>{
  if(editorDirty)return {ok:false,error:'Сначала сохраните или отмените правки в редакторе Neutral'};
  if(!neutralIde)neutralIde=new NeutralIde(
    app.isPackaged?path.join(process.resourcesPath,'neutral-ide'):path.resolve(__dirname,'../../../artifacts/neutral-ide/runtime'),
    path.join(app.getPath('userData'),'neutral-ide'),()=>callBackend('health'),()=>{win?.show();win?.focus();},
    (method,params)=>callBackend(method,params),
    (scope,channel,args)=>ideScope.run(scope,()=>{const handler=localHandlers.get(channel);if(!handler)throw Error('Неизвестный канал IDE');return handler(...args);}),
    process.env.NEUTRAL_IDE_TEST_CDP==='1'?['--remote-debugging-port=0','--disable-gpu','--disable-workspace-trust','--skip-welcome','--skip-release-notes']:[]);
  return neutralIde.open();
});
handle('project:choose', async () => {
  const result = await dialog.showOpenDialog(win!, { title: 'Выбрать папку проекта', properties: ['openDirectory'] });
  if (result.canceled || !result.filePaths[0]) return { canceled: true };
  return callBackend('set_project', { root: result.filePaths[0] });
});
handle('project:list', (rel = '.') => callBackend('list_files', { path: String(rel).slice(0, 1000) }));
handle('project:read', (rel) => callBackend('read_file', { path: String(rel).slice(0, 1000) }));
function modelConfig(config: any) {
  return { api_protocol:config?.api_protocol||'chat', tool_protocol: config?.tool_protocol || 'native', base_url: String(config?.base_url || '').slice(0, 2000), model: String(config?.model || '').slice(0, 300), ...(config&&Object.hasOwn(config,'api_key')?{api_key:String(config.api_key||'').slice(0,4000)}:{}), settings: config?.settings ?? {} };
}
async function confirmEditorDiscard() {
  if (!win) return {discard:false};
  const result = await dialog.showMessageBox(win, {type:'warning', title:'Несохранённые изменения', message:'В редакторе есть несохранённые изменения.', detail:'Если продолжить, эти черновики будут потеряны. Сначала сохраните их через просмотр diff.', buttons:['Отмена','Не сохранять'], defaultId:0, cancelId:0, noLink:true});
  return {discard:result.response === 1};
}
handle('project:search', (params) => callBackend('search_project', {mode:params?.mode,query:params?.query,pattern:params?.pattern,case_sensitive:params?.case_sensitive,limit:params?.limit}));
handle('project:cancel-search', () => callBackend('cancel_project_search'));
handle('project:index', (params) => callBackend('project_index', {action:params?.action||'status'}));
handle('editor:read', (path) => callBackend('editor_read', {path:String(path).slice(0,1000)}));
handle('editor:preview', (path, content, revision) => callBackend('editor_preview', {path:String(path).slice(0,1000), content, revision}));
handle('editor:resolve', (proposalId, decision) => callBackend('editor_resolve', {proposal_id:proposalId, decision}));
handle('editor:dirty', (dirty) => { editorDirty = dirty === true; return {ok:true}; });
handle('editor:confirm-discard', () => confirmEditorDiscard());
handle('telegram:status',()=>callBackend('telegram_status'));
handle('telegram:connect',async(params)=>{
  const secretFile=path.join(app.getPath('userData'),'telegram-secret.bin');
  let credentials={token:String(params?.token||''),owner_id:String(params?.owner_id||'')};
  if(params?.use_saved===true){
    if(!safeStorage.isEncryptionAvailable())return {ok:false,error:'Защищённое хранилище недоступно'};
    try{credentials=JSON.parse(safeStorage.decryptString(fs.readFileSync(secretFile)));}
    catch{return {ok:false,error:'Сохранённый токен не найден или недоступен'};}
  }
  const result=await callBackend('telegram_start',credentials);
  if(result.ok&&params?.remember===true){
    if(!safeStorage.isEncryptionAvailable())return {...result,warning:'Подключено, но сохранение токена недоступно'};
    fs.mkdirSync(path.dirname(secretFile),{recursive:true});fs.writeFileSync(secretFile,safeStorage.encryptString(JSON.stringify(credentials)));
  }
  return result;
});
handle('telegram:disconnect',()=>callBackend('telegram_stop'));
handle('telegram:forget',()=>{const file=path.join(app.getPath('userData'),'telegram-secret.bin');if(fs.existsSync(file))fs.unlinkSync(file);return {ok:true};});
handle('desktop:settings',()=>callBackend('desktop_settings'));
handle('desktop:configure',params=>callBackend('configure_desktop',{enabled:params?.enabled===true}));
handle('desktop:applications',()=>({ok:true,applications:desktopApplications().list()}));
handle('desktop:add-application',async()=>{
  const selected=await dialog.showOpenDialog(win!,{title:'Разрешить Лоле запуск приложения',properties:['openFile'],filters:[{name:'Приложение Windows',extensions:['exe']}]});
  return {ok:true,applications:selected.canceled?desktopApplications().list():desktopApplications().add(selected.filePaths[0])};
});
handle('desktop:remove-application',params=>({ok:true,applications:desktopApplications().remove(String(params?.id||''))}));
handle('chat:move',params=>callBackend('move_chat_mode',{chat_id:params?.chat_id,mode:params?.mode,target:params?.target}));
handle('companion:cancel-handoff',params=>callBackend('discard_handoff',{id:params?.id}));
handle('companion:handoff',params=>callBackend('prepare_handoff',{id:params?.id}));
handle('companion:settings',()=>callBackend('get_companion_settings'));
handle('companion:configure',async params=>{const result=await callBackend('configure_companion',params);if(result.ok)publish({event:'companion_configured'});return result;});
handle('voice:runtime',async(operation:string)=>{
  try {
    if(operation==='start')return await speechRuntime().start();
    if(operation==='stop')return await speechRuntime().stop();
    if(operation==='status')return await speechRuntime().status();
    if(operation==='install') {
      const selected=await dialog.showOpenDialog(win!,{title:'Выберите обученную модель Serena',properties:['openFile'],filters:[{name:'Serena ONNX',extensions:['onnx']}]});
      if(selected.canceled)return {ok:false,error:'Выбор отменён'};
      return speechRuntime().install(selected.filePaths[0]);
    }
    return {ok:false,error:'Неизвестная операция озвучки'};
  }catch{return {ok:false,error:'Не удалось настроить локальную озвучку. Проверьте файлы голоса и компоненты Piper.'};}
});
handle('voice:transcribe',params=>callBackend('transcribe',{audio:params?.audio}));
handle('voice:cancel-transcription',()=>callBackend('cancel_transcription'));
handle('voice:status',()=>callBackend('voice_status'));
handle('voice:refresh',()=>callBackend('voice_refresh'));
handle('voice:speak',params=>callBackend('voice_speak',{text:params?.text,voice:params?.voice,rate:params?.rate,volume:params?.volume}));
handle('voice:stop',()=>callBackend('voice_stop'));
handle('voice:playback',params=>callBackend('voice_playback',{sequence:params?.sequence,error:params?.error===true}));
handle('voice:tts-folder',()=>shell.openPath(app.isPackaged?path.join(process.resourcesPath,'tts'):path.resolve(__dirname,'../../../tools/tts')));
handle('voice:activate',()=>{if(desktopLola?.enabled)return {ok:true};if(win?.isMinimized())win.restore();win?.show();win?.focus();return {ok:true};});
handle('voice:listening',(enabled)=>{wakeListening=enabled===true;publish({event:'lola_wake',enabled:wakeListening});win?.webContents.setBackgroundThrottling(!wakeListening&&!desktopLola?.enabled);return {ok:true};});
handle('runtime:pick', async (kind) => {
  if(!win || !['model','runtime'].includes(kind)) return {ok:false,error:'Некорректный выбор файла'};
  const result=await dialog.showOpenDialog(win,{properties:['openFile'],title:kind==='model'?'Выберите GGUF':'Выберите установленный llama-server',filters:kind==='model'?[{name:'GGUF',extensions:['gguf']}]:[{name:'llama-server',extensions:process.platform==='win32'?['exe']:['*']}]});
  if(result.canceled||!result.filePaths[0])return {canceled:true};
  if(kind==='model')selectedModel=result.filePaths[0];else selectedRuntime=result.filePaths[0];
  return {ok:true,path:result.filePaths[0]};
});
handle('runtime:start', params => {
  const runtime = selectedRuntime || bundledRuntimePath();
  if(!runtime||!selectedModel)return {ok:false,error:'Выберите сервер и модель через диалог файлов'};
  return callBackend('runtime_start',{runtime_path:runtime,model_path:selectedModel,ctx_size:params?.ctx_size,gpu_layers:params?.gpu_layers,threads:params?.threads,cache_type_k:params?.cache_type_k,cache_type_v:params?.cache_type_v});
});
handle('runtime:status',async()=>({...await callBackend('runtime_status'),bundled_runtime:bundledRuntimePath()}));
handle('runtime:stop',()=>callBackend('runtime_stop'));
handle('model:configure', (config) => callBackend('configure_model', modelConfig(config)));
handle('model:list', (config) => callBackend('list_models', config ? modelConfig(config) : {}));
handle('model:test', (config) => callBackend('test_model', modelConfig(config)));
handle('model:cancel-setup', () => callBackend('cancel_model_setup'));
handle('ide:complete',params=>callBackend('ide_complete',params));
handle('model:settings', () => callBackend('get_model_settings'));
handle('memory:get',()=>callBackend('get_project_memory'));
handle('memory:save',(memory,revision,root)=>callBackend('save_project_memory',{memory,revision,root}));
handle('memory:action',params=>callBackend('project_memory_action',params));
handle('chat:rename',(chatId,title,mode='ide')=>callBackend('rename_chat',{chat_id:chatId,title,mode}));
handle('chat:list', (mode = 'ide') => callBackend('list_chats', {mode}));
handle('chat:new', (mode = 'ide') => callBackend('new_chat', {mode}));
handle('chat:load', (chatId, mode = 'ide') => callBackend('load_chat', { chat_id: chatId, mode }));
handle('task:start', (prompt:string, resume = false, mode:AgentMode = 'ide', taskOptions:StartTaskOptions|undefined = undefined,runId?:string) => callBackend('start_task', { mode, prompt: String(prompt).slice(0, 50001), resume: resume === true, task_options:taskOptions,run_id:runId }));
handle('snapshot:checkpoint',params=>callBackend('snapshot_checkpoint',params));
handle('snapshot:checkpoint-cancel',()=>callBackend('snapshot_checkpoint_cancel'));
for(const action of ['list','preview','apply','review'])handle('snapshot:'+action,params=>callBackend('snapshot_'+action,params));
handle('task:cancel', (runId?:string) => callBackend('cancel_task',{run_id:runId}));
handle('task:plan',params=>callBackend('update_task_plan',params));
handle('run:active',()=>callBackend('active_runs'));
handle('run:history',(chatId:string)=>callBackend('run_history',{chat_id:chatId}));
handle('task:approve', (runId:string, approvalId:string, decision:ApprovalDecision) => callBackend('resolve_approval', { run_id: runId, approval_id: approvalId, decision }));
handle('task:resolve-recovery', params => callBackend('resolve_tool_recovery', {chat_id:params?.chat_id, journal_id:params?.journal_id, message_index:params?.message_index, call_id:params?.call_id, resolution:params?.resolution}));
handle('ide:copy-diagnostics', report => {
  if(typeof report!=='string'||report.length>10000||JSON.parse(report).schema!=='leshy.recovery.v1')return {ok:false,error:'Некорректная диагностика'};
  clipboard.writeText(report);return {ok:true};
});
handle('system:home', () => ({ home: os.homedir(), platform: process.platform }));
