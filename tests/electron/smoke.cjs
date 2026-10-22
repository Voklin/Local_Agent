// Run with Electron after building and starting Vite on 127.0.0.1:5173.
// Uses the real main process, preload, renderer, bridge and engine.
const { app, BrowserWindow, dialog } = require('electron');
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const assert = require('node:assert/strict');

const testRoot = path.resolve(__dirname, '../../.test-data/electron-smoke');
fs.mkdirSync(testRoot, { recursive: true });
const resultPath = path.join(testRoot, 'result.json');
fs.writeFileSync(resultPath, JSON.stringify({status:'running'}));
function fail(error) {
  fs.writeFileSync(resultPath, JSON.stringify({status:'failed',error:String(error.stack || error)}, null, 2));
  app.exit(1);
}
process.on('uncaughtException', fail);
process.on('unhandledRejection', fail);
const project = fs.mkdtempSync(path.join(testRoot, 'project-'));
process.env.LOCALAPPDATA = testRoot;
app.setPath('userData', path.join(testRoot, 'electron-profile'));
BrowserWindow.prototype.show = function () {}; // Keep the test window hidden.
dialog.showOpenDialog = async () => ({ canceled: false, filePaths: [project] });

let modelMode = 'write';
let releaseModelText = null;
let streamDisconnected = false;
const model = http.createServer((req, res) => {
  let raw = '';
  req.on('data', chunk => { raw += chunk; });
  req.on('end', () => {
    if (req.method === 'GET') {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ data: [{ id: 'smoke-model' }] })); return;
    }
    const input = JSON.parse(raw);
    if (!input.stream) {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ id:'test',object:'chat.completion',created:0,model:'smoke-model',choices:[{index:0,message:{role:'assistant',content:'{}'},finish_reason:'stop'}] })); return;
    }
    const encode = delta => 'data: ' + JSON.stringify({id:'test',object:'chat.completion.chunk',created:0,model:'smoke-model',choices:[{index:0,delta,finish_reason:null}]}) + '\n\n';
    res.writeHead(200, { 'Content-Type':'text/event-stream' });
    if (modelMode === 'stall') {
      res.write(encode({content:'Pending '}));
      res.on('close', () => { streamDisconnected = true; });
    } else if (input.messages.some(m => m.role === 'tool')) {
      res.write(encode({content:'Smoke '}));
      releaseModelText = () => res.end(encode({content:'completed'}) + 'data: [DONE]\n\n');
    } else {
      res.end(encode({tool_calls:[{index:0,id:'smoke-call',type:'function',function:{name:'write_file',arguments:JSON.stringify({path:'smoke.txt',content:'verified',overwrite:false})}}]}) + 'data: [DONE]\n\n');
    }
  });
});

async function poll(win, expression) {
  const deadline = Date.now() + 15000;
  while (Date.now() < deadline) {
    if (await win.webContents.executeJavaScript(expression)) return;
    await new Promise(r => setTimeout(r, 100));
  }
  throw new Error('Timed out: ' + expression);
}
const deadline = setTimeout(() => fail(new Error('Smoke timed out')), 45000);
app.on('browser-window-created', (_event, win) => {
  win.webContents.setBackgroundThrottling(false);
  win.webContents.on('preload-error', (_event, preloadPath, error) => {
    fs.writeFileSync(path.join(testRoot, 'preload-error.txt'), preloadPath + '\n' + String(error.stack || error));
  });
  win.webContents.once('did-finish-load', async () => {
    try {
      await poll(win, `document.body.textContent.includes('Python Core подключён')`);
      assert.equal(await win.webContents.executeJavaScript('typeof require'), 'undefined');
      await win.webContents.executeJavaScript(`document.querySelector('.project-pill').click()`);
      await poll(win, `document.querySelector('.project-pill').textContent.includes(${JSON.stringify(path.basename(project))})`);
      await win.webContents.executeJavaScript(`document.querySelector('[title="Настройки модели"]').click()`);
      await poll(win, `!!document.querySelector('.model-settings input')`);
      const url = `http://127.0.0.1:${model.address().port}/v1`;
      await win.webContents.executeJavaScript(`{
        const input = document.querySelector('.model-settings input');
        Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(input, ${JSON.stringify(url)});
        input.dispatchEvent(new Event('input', { bubbles:true }));
      }`);
      await win.webContents.executeJavaScript(`{
        const input = document.querySelector('input[type="password"]');
        Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(input, 'test-secret');
        input.dispatchEvent(new Event('input', { bubbles:true }));
      }`);
      await win.webContents.executeJavaScript(`document.querySelector('.model-settings button').click()`);
      await poll(win, `document.querySelector('input[list="model-names"]').value === 'smoke-model'`);
      await win.webContents.executeJavaScript(`{
        const input = document.querySelector('textarea');
        Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype,'value').set.call(input, 'hello');
        input.dispatchEvent(new Event('input', { bubbles:true }));
      }`);
      await poll(win, `!document.querySelector('[title="Отправить"]').disabled`);
      await win.webContents.executeJavaScript(`document.querySelector('[title="Отправить"]').click()`);
      await poll(win, `!!document.querySelector('[role="dialog"]')`);
      assert.equal(fs.existsSync(path.join(project, 'smoke.txt')), false);
      assert.ok(await win.webContents.executeJavaScript(`document.querySelector('[role="dialog"] pre').textContent.includes('+verified')`));
      await win.webContents.executeJavaScript('new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))');
      fs.writeFileSync(path.join(testRoot, 'approval.png'), (await win.webContents.capturePage(undefined, {stayHidden:true})).toPNG());
      await win.webContents.executeJavaScript(`document.querySelector('.approval-actions .primary-button').click()`);
      await poll(win, `!!document.querySelector('.streaming-caret') && document.querySelector('.chat-messages').textContent.includes('Smoke ')`);
      assert.equal(await win.webContents.executeJavaScript(`document.querySelector('.chat-messages').textContent.includes('Smoke completed')`), false);
      assert.equal(typeof releaseModelText, 'function');
      releaseModelText();
      await poll(win, `document.body.textContent.includes('Smoke completed') && !document.querySelector('[title="Остановить"]')`);
      assert.equal(await win.webContents.executeJavaScript(`Array.from(document.querySelectorAll('.message-content')).filter(m => m.textContent === 'Smoke completed').length`), 1);
      assert.equal(await win.webContents.executeJavaScript(`!!document.querySelector('.streaming-caret')`), false);
      assert.equal(fs.readFileSync(path.join(project, 'smoke.txt'), 'utf8'), 'verified');
      await win.webContents.executeJavaScript('new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))');
      fs.writeFileSync(path.join(testRoot, 'completed.png'), (await win.webContents.capturePage(undefined, {stayHidden:true})).toPNG());
      const saved = JSON.parse(fs.readFileSync(path.join(testRoot, 'LocalCodingAgent/model-preferences.json'), 'utf8'));
      assert.deepEqual(saved, {base_url:url, model:'smoke-model'});
      assert.equal(JSON.stringify(saved).includes('test-secret'), false);
      const reloaded = new Promise(resolve => win.webContents.once('did-finish-load', resolve));
      win.webContents.reload();
      await reloaded;
      await poll(win, `document.querySelector('.agent-context').textContent.includes('smoke-model')`);
      await win.webContents.executeJavaScript(`document.querySelector('[title="Настройки модели"]').click()`);
      await poll(win, `!!document.querySelector('.model-settings input')`);
      assert.equal(await win.webContents.executeJavaScript(`document.querySelector('.model-settings input').value`), url);
      assert.equal(await win.webContents.executeJavaScript(`document.querySelector('input[type="password"]').value`), '');
      await win.webContents.executeJavaScript(`document.querySelector('.project-pill').click()`);
      await poll(win, `document.querySelector('.project-pill').textContent.includes(${JSON.stringify(path.basename(project))})`);
      modelMode = 'stall';
      await win.webContents.executeJavaScript(`{
        const input = document.querySelector('textarea');
        Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype,'value').set.call(input, 'hello');
        input.dispatchEvent(new Event('input', { bubbles:true }));
      }`);
      await poll(win, `!document.querySelector('[title="Отправить"]').disabled`);
      await win.webContents.executeJavaScript(`document.querySelector('[title="Отправить"]').click()`);
      await poll(win, `!!document.querySelector('.streaming-caret') && document.body.textContent.includes('Pending ')`);
      const stoppedAt = Date.now();
      await win.webContents.executeJavaScript(`document.querySelector('[title="Остановить"]').click()`);
      await poll(win, `!document.querySelector('[title="Остановить"]') && document.querySelector('.task-card').textContent.includes('Приостановлена')`);
      assert.ok(Date.now() - stoppedAt < 3000, 'Stop should not wait for the model timeout');
      assert.equal(streamDisconnected, true);
      assert.equal(await win.webContents.executeJavaScript(`!!document.querySelector('.streaming-caret')`), false);
      console.log('PASS: Electron file approval, incremental text without duplicate answer, persisted preferences, fast network cancellation');
      fs.writeFileSync(resultPath, JSON.stringify({status:'passed',project}, null, 2));
      clearTimeout(deadline); model.close(); app.quit();
    } catch (error) {
      fs.writeFileSync(path.join(testRoot, 'failure.png'), (await win.webContents.capturePage()).toPNG());
      fs.writeFileSync(path.join(testRoot, 'failure-state.txt'), await win.webContents.executeJavaScript(`JSON.stringify({text:document.body.textContent,api:typeof window.lca})`));
      model.close(); fail(error);
    }
  });
});
model.listen(0, '127.0.0.1', () => require('../../apps/desktop/dist-electron/main.cjs'));
