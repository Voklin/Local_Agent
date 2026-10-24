import { app, BrowserWindow, dialog, ipcMain, session, desktopCapturer, shell, screen, safeStorage, Notification as NativeNotification } from 'electron';
import { spawn, ChildProcessWithoutNullStreams } from 'node:child_process';
import { createInterface } from 'node:readline';
import path from 'node:path';
import os from 'node:os';
import fs from 'node:fs';
import { DesktopApplications } from './desktopApps';
import { SpeechRuntime } from './speechRuntime';
import { validateMusicURL, validateAudioPath } from './assistantMedia';

let managedSpeech:SpeechRuntime|null=null;
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
  if (win && !win.isDestroyed()) win.webContents.send('core:event', message);
}
function startBackend() {
  if (backend) return;
  const root = app.isPackaged ? path.join(process.resourcesPath, 'core') : path.resolve(__dirname, '../../../core/python');
  const python = app.isPackaged ? path.join(root, 'lca-core.exe') : process.env.LCA_PYTHON || (process.platform === 'win32' ? 'python' : 'python3');
  const env: NodeJS.ProcessEnv = { ...process.env, PYTHONIOENCODING: 'utf-8' };
  if (app.isPackaged) { delete env.PYTHONHOME; delete env.PYTHONPATH; }
  diagnostic(`core:start packaged=${app.isPackaged}`);
  const child = spawn(python, app.isPackaged ? [] : ['-u', path.join(root, 'bridge.py')], { cwd: root, stdio: ['pipe', 'pipe', 'pipe'], windowsHide: true, env });
  backend = child;
  createInterface({ input: child.stdout }).on('line', (line) => {
    try {
      const msg = JSON.parse(line);
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
  if (quitting) return Promise.resolve({ok:false,error:'Приложение завершает работу'});
  if (pending.size >= 100) return Promise.resolve({ ok: false, error: 'Слишком много запросов' });
  startBackend();
  const id = ++requestId;
  return new Promise<any>((resolve) => {
    const timer = setTimeout(() => { pending.delete(id); resolve({ ok: false, error: 'Python Core: время ожидания истекло' }); }, method === 'transcribe' ? 95000 : method === 'test_model' ? 35000 : 10000);
    timer.unref();
    pending.set(id, { resolve, timer });
    backend!.stdin.write(JSON.stringify({ id, method, params }) + '\n');
  });
}
function createWindow() {
  win = new BrowserWindow({ show: false, width: 1500, height: 940, minWidth: 1050, minHeight: 680, backgroundColor: '#15171c', title: 'Local Coding Agent', webPreferences: { preload: path.join(__dirname, 'preload.cjs'), contextIsolation: true, nodeIntegration: false, sandbox: true } });
  win.on('close', (event) => {
    if (!editorDirty) return;
    event.preventDefault();
    if (confirmingClose) return;
    confirmingClose = true;
    void confirmEditorDiscard().then(result => {
      if (result.discard) { editorDirty = false; win?.close(); }
    }).finally(() => { confirmingClose = false; });
  });
  win.once('ready-to-show', () => win?.show());
  win.webContents.setWindowOpenHandler(() => ({ action: 'deny' }));
  win.webContents.on('will-navigate', (event) => event.preventDefault());
  win.webContents.on('render-process-gone', () => { void callBackend('cancel_task'); void callBackend('voice_stop'); });
  win.webContents.on('did-start-loading', () => { if (backend) void callBackend('cancel_task'); void callBackend('voice_stop'); });
  if (app.isPackaged) win.loadFile(path.join(__dirname, '../dist/index.html')); else win.loadURL('http://127.0.0.1:5173');
}
app.whenReady().then(() => { session.defaultSession.setPermissionRequestHandler((contents, permission, callback, details) => { callback(contents===win?.webContents && (permission==='clipboard-sanitized-write' || (permission==='media' && 'mediaTypes' in details && details.mediaTypes?.includes('audio')===true && details.mediaTypes.every(type=>type==='audio')))); }); diagnostic(`app:start version=${app.getVersion()} packaged=${app.isPackaged} platform=${process.platform} arch=${process.arch}`); createWindow(); app.on('activate', () => { if (BrowserWindow.getAllWindows().length === 0) createWindow(); }); });
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
  if(!quitting)void managedSpeech?.stop();
  if (quitting || !backend) return;
  event.preventDefault(); quitting = true; diagnostic('app:quit');
  const child=backend;
  const deadline=setTimeout(()=>{child.kill();app.exit(1);},15000);
  child.once('exit',()=>{clearTimeout(deadline);app.quit();});
  child.stdin.end();
});
app.on('window-all-closed', () => { if (process.platform !== 'darwin') app.quit(); });
function handle(channel: string, handler: (...args: any[]) => any) {
  ipcMain.handle(channel, (event, ...args) => {
    if (!win || event.sender !== win.webContents || event.senderFrame !== win.webContents.mainFrame) return { ok: false, error: 'Forbidden sender' };
    return handler(...args);
  });
}
handle('core:health', () => callBackend('health'));
handle('ide:workflow',()=>callBackend('get_ide_workflow'));
handle('ide:configure-workflow',params=>callBackend('configure_ide_workflow',params));
handle('ide:models',params=>callBackend('list_ide_models',params));
handle('project:choose', async () => {
  const result = await dialog.showOpenDialog(win!, { title: 'Выбрать папку проекта', properties: ['openDirectory'] });
  if (result.canceled || !result.filePaths[0]) return { canceled: true };
  return callBackend('set_project', { root: result.filePaths[0] });
});
handle('project:list', (rel = '.') => callBackend('list_files', { path: String(rel).slice(0, 1000) }));
handle('project:read', (rel) => callBackend('read_file', { path: String(rel).slice(0, 1000) }));
function modelConfig(config: any) {
  return { tool_protocol: config?.tool_protocol || 'native', base_url: String(config?.base_url || '').slice(0, 2000), model: String(config?.model || '').slice(0, 300), api_key: String(config?.api_key || '').slice(0, 4000), settings: config?.settings ?? {} };
}
async function confirmEditorDiscard() {
  if (!win) return {discard:false};
  const result = await dialog.showMessageBox(win, {type:'warning', title:'Несохранённые изменения', message:'В редакторе есть несохранённые изменения.', detail:'Если продолжить, эти черновики будут потеряны. Сначала сохраните их через просмотр diff.', buttons:['Отмена','Не сохранять'], defaultId:0, cancelId:0, noLink:true});
  return {discard:result.response === 1};
}
handle('project:search', (params) => callBackend('search_project', {mode:params?.mode,query:params?.query,pattern:params?.pattern,case_sensitive:params?.case_sensitive,limit:params?.limit}));
handle('project:cancel-search', () => callBackend('cancel_project_search'));
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
handle('companion:configure',params=>callBackend('configure_companion',params));
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
handle('voice:activate',()=>{if(win?.isMinimized())win.restore();win?.show();win?.focus();return {ok:true};});
handle('voice:listening',(enabled)=>{win?.webContents.setBackgroundThrottling(enabled!==true);return {ok:true};});
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
handle('model:settings', () => callBackend('get_model_settings'));
handle('memory:get',()=>callBackend('get_project_memory'));
handle('memory:save',(memory,revision)=>callBackend('save_project_memory',{memory,revision}));
handle('chat:rename',(chatId,title,mode='ide')=>callBackend('rename_chat',{chat_id:chatId,title,mode}));
handle('chat:list', (mode = 'ide') => callBackend('list_chats', {mode}));
handle('chat:new', (mode = 'ide') => callBackend('new_chat', {mode}));
handle('chat:load', (chatId, mode = 'ide') => callBackend('load_chat', { chat_id: chatId, mode }));
handle('task:start', (prompt, resume = false, mode = 'ide') => callBackend('start_task', { mode, prompt: String(prompt).slice(0, 50001), resume: resume === true }));
handle('task:cancel', () => callBackend('cancel_task'));
handle('task:approve', (runId, approvalId, decision) => callBackend('resolve_approval', { run_id: runId, approval_id: approvalId, decision }));
handle('system:home', () => ({ home: os.homedir(), platform: process.platform }));
