import { app, BrowserWindow, dialog, ipcMain } from 'electron';
import { spawn, ChildProcessWithoutNullStreams } from 'node:child_process';
import { createInterface } from 'node:readline';
import path from 'node:path';
import os from 'node:os';

let win: BrowserWindow | null = null;
let backend: ChildProcessWithoutNullStreams | null = null;
let requestId = 0;
const pending = new Map<number, { resolve: (value: any) => void; timer: ReturnType<typeof setTimeout> }>();
function publish(message: any) {
  if (win && !win.isDestroyed()) win.webContents.send('core:event', message);
}
function startBackend() {
  if (backend) return;
  const root = app.isPackaged ? path.join(process.resourcesPath, 'core', 'python') : path.resolve(__dirname, '../../../core/python');
  const python = process.env.LCA_PYTHON || (process.platform === 'win32' ? 'python' : 'python3');
  const child = spawn(python, ['-u', path.join(root, 'bridge.py')], { cwd: root, stdio: ['pipe', 'pipe', 'pipe'], windowsHide: true, env: { ...process.env, PYTHONIOENCODING: 'utf-8' } });
  backend = child;
  createInterface({ input: child.stdout }).on('line', (line) => {
    try {
      const msg = JSON.parse(line);
      if (typeof msg.event === 'string') { publish(msg); return; }
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
  child.on('error', stopped);
  child.on('exit', stopped);
  child.stdin.on('error', stopped);
}
function callBackend(method: string, params: Record<string, unknown> = {}) {
  if (pending.size >= 100) return Promise.resolve({ ok: false, error: 'Слишком много запросов' });
  startBackend();
  const id = ++requestId;
  return new Promise<any>((resolve) => {
    const timer = setTimeout(() => { pending.delete(id); resolve({ ok: false, error: 'Python Core: время ожидания истекло' }); }, 10000);
    timer.unref();
    pending.set(id, { resolve, timer });
    backend!.stdin.write(JSON.stringify({ id, method, params }) + '\n');
  });
}
function createWindow() {
  win = new BrowserWindow({ show: false, width: 1500, height: 940, minWidth: 1050, minHeight: 680, backgroundColor: '#15171c', title: 'Local Coding Agent', webPreferences: { preload: path.join(__dirname, 'preload.cjs'), contextIsolation: true, nodeIntegration: false, sandbox: true } });
  win.once('ready-to-show', () => win?.show());
  win.webContents.setWindowOpenHandler(() => ({ action: 'deny' }));
  win.webContents.on('will-navigate', (event) => event.preventDefault());
  win.webContents.on('render-process-gone', () => { void callBackend('cancel_task'); });
  win.webContents.on('did-start-loading', () => { if (backend) void callBackend('cancel_task'); });
  if (app.isPackaged) win.loadFile(path.join(__dirname, '../dist/index.html')); else win.loadURL('http://127.0.0.1:5173');
}
app.whenReady().then(() => { createWindow(); app.on('activate', () => { if (BrowserWindow.getAllWindows().length === 0) createWindow(); }); });
app.on('before-quit', () => { if (backend) { backend.stdin.end(); backend.kill(); } });
app.on('window-all-closed', () => { if (process.platform !== 'darwin') app.quit(); });
function handle(channel: string, handler: (...args: any[]) => any) {
  ipcMain.handle(channel, (event, ...args) => {
    if (!win || event.sender !== win.webContents || event.senderFrame !== win.webContents.mainFrame) return { ok: false, error: 'Forbidden sender' };
    return handler(...args);
  });
}
handle('core:health', () => callBackend('health'));
handle('project:choose', async () => {
  const result = await dialog.showOpenDialog(win!, { title: 'Выбрать папку проекта', properties: ['openDirectory'] });
  if (result.canceled || !result.filePaths[0]) return { canceled: true };
  return callBackend('set_project', { root: result.filePaths[0] });
});
handle('project:list', (rel = '.') => callBackend('list_files', { path: String(rel).slice(0, 1000) }));
handle('project:read', (rel) => callBackend('read_file', { path: String(rel).slice(0, 1000) }));
handle('model:configure', (config) => callBackend('configure_model', { base_url: String(config?.base_url || '').slice(0, 2000), model: String(config?.model || '').slice(0, 300), api_key: String(config?.api_key || '').slice(0, 4000) }));
handle('model:list', () => callBackend('list_models'));
handle('chat:list', () => callBackend('list_chats'));
handle('chat:new', () => callBackend('new_chat'));
handle('chat:load', (chatId) => callBackend('load_chat', { chat_id: chatId }));
handle('task:start', (prompt, resume = false) => callBackend('start_task', { prompt: String(prompt).slice(0, 50001), resume: resume === true }));
handle('task:cancel', () => callBackend('cancel_task'));
handle('task:approve', (runId, approvalId, decision) => callBackend('resolve_approval', { run_id: runId, approval_id: approvalId, decision }));
handle('system:home', () => ({ home: os.homedir(), platform: process.platform }));
