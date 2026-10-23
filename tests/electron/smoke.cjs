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
let discardChoice = 1;
dialog.showMessageBox = async () => ({response:discardChoice});
fs.writeFileSync(path.join(project,'editor-a.txt'),'first\nsecond\n');
fs.writeFileSync(path.join(project,'editor-b.py'),'print(1)\n');
dialog.showOpenDialog = async (_win,options) => ({ canceled:false,filePaths:[options?.title==='Выберите GGUF'?process.env.LCA_TEST_GGUF:options?.title==='Выберите установленный llama-server'?process.env.LCA_TEST_RUNTIME:project] });

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
    if (!input.tools) {
      assert.equal(input.tool_choice, undefined);
      if(modelMode==='scroll') {
        res.write(encode({content:Array.from({length:120},(_,i)=>'Scroll line '+i).join('\n')}));
        releaseModelText=()=>res.end(encode({content:'\n'+Array.from({length:120},(_,i)=>'More line '+i).join('\n')})+'data: [DONE]\n\n');
      } else res.end(encode({content:'Standalone Chat reply\n```python\nprint("<script>safe</script>")\n```'}) + 'data: [DONE]\n\n');
    } else if (modelMode === 'stall') {
      res.write(encode({content:'Pending '}));
      res.on('close', () => { streamDisconnected = true; });
    } else if (input.messages.some(m => m.role === 'tool')) {
      if (modelMode === 'conflict') {
        res.end(encode({content:'Conflict handled'}) + 'data: [DONE]\n\n'); return;
      }
      res.write(encode({content:'Smoke '}));
      releaseModelText = () => res.end(encode({content:'completed'}) + 'data: [DONE]\n\n');
    } else {
      res.end(encode({tool_calls:[{index:0,id:'smoke-call',type:'function',function:{name:'write_file',arguments:JSON.stringify({path:modelMode === 'conflict' ? 'conflict.txt' : 'smoke.txt',content:'verified',overwrite:false})}}]}) + 'data: [DONE]\n\n');
    }
  });
});

async function poll(win, expression, timeout=10000) {
  const deadline = Date.now() + timeout;
  while (Date.now() < deadline) {
    if (await win.webContents.executeJavaScript(expression)) return;
    await new Promise(r => setTimeout(r, 100));
  }
  throw new Error('Timed out: ' + expression);
}
const deadline = setTimeout(() => fail(new Error('Smoke timed out')), process.env.LCA_TEST_RUNTIME?180000:45000);
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
      await poll(win, `Array.from(document.querySelectorAll('.sidebar .file-row')).some(button=>button.textContent.includes('editor-a.txt'))`);
      await win.webContents.executeJavaScript(`Array.from(document.querySelectorAll('.sidebar .file-row')).find(button=>button.textContent.includes('editor-a.txt')).click()`);
      await poll(win, `!!document.querySelector('.editor-input')`);
      await win.webContents.executeJavaScript(`{const input=document.querySelector('.editor-input'); Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype,'value').set.call(input,'edited\\nsecond\\n'); input.dispatchEvent(new Event('input',{bubbles:true}));}`);
      await poll(win, `!!document.querySelector('.editor-dirty')`);
      await win.webContents.executeJavaScript(`document.querySelector('.mode-tabs button:first-child').click()`);
      await poll(win, `!!document.querySelector('.mode-chat')`);
      await win.webContents.executeJavaScript(`document.querySelector('.mode-tabs button:nth-child(2)').click()`);
      await poll(win, `document.querySelector('.editor-input').value.startsWith('edited')`);
      await win.webContents.executeJavaScript(`Array.from(document.querySelectorAll('.sidebar .file-row')).find(button=>button.textContent.includes('editor-b.py')).click()`);
      await poll(win, `document.querySelectorAll('.editor-tabs [role=tab]').length===2`);
      await win.webContents.executeJavaScript(`document.querySelector('.editor-tabs [title="editor-a.txt"]').click()`);
      await win.webContents.executeJavaScript(`window.dispatchEvent(new KeyboardEvent('keydown',{key:'s',ctrlKey:true,bubbles:true}))`);
      await poll(win, `!!document.querySelector('.editor-approval')`);
      assert.equal(fs.readFileSync(path.join(project,'editor-a.txt'),'utf8'),'first\nsecond\n');
      await win.webContents.executeJavaScript(`document.querySelector('.editor-approval .primary-button').click()`);
      await poll(win, `!document.querySelector('.editor-approval') && !document.querySelector('.editor-dirty')`);
      assert.equal(fs.readFileSync(path.join(project,'editor-a.txt'),'utf8'),'edited\nsecond\n');
      await win.webContents.executeJavaScript(`window.dispatchEvent(new KeyboardEvent('keydown',{key:'f',ctrlKey:true,bubbles:true}))`);
      await poll(win, `!!document.querySelector('.editor-find')`);
      await win.webContents.executeJavaScript(`{const input=document.querySelector('[aria-label="Поиск в файле"]'); Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(input,'second'); input.dispatchEvent(new Event('input',{bubbles:true}));}`);
      await win.webContents.executeJavaScript(`document.querySelector('.editor-find button').click()`);
      assert.equal(await win.webContents.executeJavaScript(`{const input=document.querySelector('.editor-input'); input.value.slice(input.selectionStart,input.selectionEnd)}`),'second');
      await win.webContents.executeJavaScript('new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))');
      await win.webContents.executeJavaScript(`window.dispatchEvent(new KeyboardEvent('keydown',{key:'f',ctrlKey:true,shiftKey:true,bubbles:true}))`);
      await poll(win, `!!document.querySelector('[aria-label="Текст поиска по проекту"]')`);
      await win.webContents.executeJavaScript(`{const input=document.querySelector('[aria-label="Текст поиска по проекту"]');Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(input,'second');input.dispatchEvent(new Event('input',{bubbles:true}));}`);
      await win.webContents.executeJavaScript(`document.querySelector('.sidebar .project-search form').dispatchEvent(new Event('submit',{bubbles:true,cancelable:true}))`);
      await poll(win, `document.querySelectorAll('.search-results button').length===1`);
      await win.webContents.executeJavaScript(`document.querySelector('.search-results button').click()`);
      await poll(win, `document.querySelector('.editor-status').textContent.includes('Ln 2, Col 1')`);
      await win.webContents.executeJavaScript(`window.dispatchEvent(new KeyboardEvent('keydown',{key:'p',ctrlKey:true,bubbles:true}))`);
      await poll(win, `!!document.querySelector('.quick-open input')`);
      await win.webContents.executeJavaScript(`{const input=document.querySelector('.quick-open input');Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(input,'editor-b');input.dispatchEvent(new Event('input',{bubbles:true}));}`);
      await poll(win, `document.querySelectorAll('.quick-open .search-results button').length===1`);
      await win.webContents.executeJavaScript(`document.querySelector('.quick-open form').dispatchEvent(new Event('submit',{bubbles:true,cancelable:true}))`);
      await poll(win, `!document.querySelector('.quick-open') && document.querySelector('.editor-input').value.includes('print(1)')`);
      await win.webContents.executeJavaScript(`document.querySelector('.editor-tabs [title="editor-a.txt"]').click()`);
      fs.writeFileSync(path.join(testRoot,'editor.png'),(await win.webContents.capturePage(undefined,{stayHidden:true})).toPNG());

      await win.webContents.executeJavaScript(`{const input=document.querySelector('.editor-input'); Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype,'value').set.call(input,'my draft'); input.dispatchEvent(new Event('input',{bubbles:true}));}`);
      discardChoice=0;
      win.close();
      assert.equal((await win.webContents.executeJavaScript('window.lca.health()')).ok,true);
      assert.equal(win.isDestroyed(),false);
      fs.writeFileSync(path.join(project,'editor-a.txt'),'external change');
      await win.webContents.executeJavaScript(`window.dispatchEvent(new KeyboardEvent('keydown',{key:'s',ctrlKey:true,bubbles:true}))`);
      await poll(win, `document.querySelector('.editor-notice').textContent.includes('изменился на диске')`);
      assert.equal(await win.webContents.executeJavaScript(`document.querySelector('.editor-input').value`),'my draft');
      discardChoice=0;
      await win.webContents.executeJavaScript(`document.querySelector('[title="Перечитать · Ctrl+Shift+R"]').click()`);
      assert.equal(await win.webContents.executeJavaScript(`document.querySelector('.editor-input').value`),'my draft');
      discardChoice=1;
      await win.webContents.executeJavaScript(`document.querySelector('[title="Перечитать · Ctrl+Shift+R"]').click()`);
      await poll(win, `document.querySelector('.editor-input').value==='external change' && !document.querySelector('.editor-dirty')`);

      await win.webContents.executeJavaScript(`document.querySelector('[title="Память проекта"]').click()`);
      await poll(win, `!!document.querySelector('[aria-label="Описание проекта"]')`);
      await win.webContents.executeJavaScript(`{const input=document.querySelector('[aria-label="Описание проекта"]');Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype,'value').set.call(input,'Тестовая память проекта');input.dispatchEvent(new Event('input',{bubbles:true}));}`);
      await poll(win, `!document.querySelector('.save-memory').disabled`);
      await win.webContents.executeJavaScript(`document.querySelector('.save-memory').click()`);
      await poll(win, `document.querySelector('.memory-dialog').textContent.includes('Память сохранена')`);
      assert.equal((await win.webContents.executeJavaScript('window.lca.getProjectMemory()')).memory.project_summary,'Тестовая память проекта');
      await win.webContents.executeJavaScript(`document.querySelector('.memory-dialog .settings-actions .secondary-button').click()`);
      await poll(win, `!document.querySelector('.memory-dialog')`);
      await win.webContents.executeJavaScript(`document.querySelector('[title="Настройки модели"]').click()`);
      await poll(win, `!!document.querySelector('.model-settings input')`);
      if(process.env.LCA_TEST_RUNTIME&&process.env.LCA_TEST_GGUF) {
        await win.webContents.executeJavaScript(`document.querySelector('.pick-runtime').click()`);
        await poll(win, `document.querySelector('.runtime-path').textContent.includes('llama-server')`);
        await win.webContents.executeJavaScript(`document.querySelector('.pick-gguf').click()`);
        await poll(win, `!document.querySelector('.start-runtime').disabled`);
        await win.webContents.executeJavaScript(`document.querySelector('.start-runtime').click()`);
        await poll(win, `!document.querySelector('.stop-runtime').disabled`);
        await win.webContents.executeJavaScript(`document.querySelector('.stop-runtime').click()`);
        await poll(win, `document.querySelector('.runtime-status').textContent==='Остановлен'`);
        await win.webContents.executeJavaScript(`document.querySelector('.start-runtime').click()`);
        await poll(win, `document.querySelector('.runtime-status').textContent.includes('Готов')`,120000);
        const runtime=await win.webContents.executeJavaScript('window.lca.runtimeStatus()');
        assert.equal(runtime.state,'running');
        assert.equal((await win.webContents.executeJavaScript('window.lca.health()')).ok,true);
        await win.webContents.executeJavaScript(`document.querySelector('.use-runtime').click()`);
        await poll(win, `document.querySelector('input[name="base_url"]').value===${JSON.stringify(runtime.base_url)}`);
        const answer=await win.webContents.executeJavaScript(`window.lca.testModel({base_url:${JSON.stringify(runtime.base_url)},model:${JSON.stringify(runtime.model.name)},api_key:'',settings:{max_tokens:128,temperature:0}})`);
        assert.equal(answer.ok,true,JSON.stringify(answer));
        fs.writeFileSync(path.join(testRoot,'runtime-result.json'),JSON.stringify({runtime,answer},null,2));
        await win.webContents.executeJavaScript(`document.querySelector('.local-runtime').scrollIntoView({block:'start'})`);
        await win.webContents.executeJavaScript('new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)))');
        fs.writeFileSync(path.join(testRoot,'runtime.png'),(await win.webContents.capturePage(undefined,{stayHidden:true})).toPNG());
        await win.webContents.executeJavaScript(`document.querySelector('.stop-runtime').click()`);
        await poll(win, `document.querySelector('.runtime-status').textContent==='Остановлен'`);
        await win.webContents.executeJavaScript(`{const input=document.querySelector('input[name="model"]');Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(input,'');input.dispatchEvent(new Event('input',{bubbles:true}));}`);
      }
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
      await win.webContents.executeJavaScript(`document.querySelector('.discover-models').click()`);
      await poll(win, `document.querySelector('input[list="model-names"]').value === 'smoke-model' && !document.querySelector('.discover-models').disabled && document.querySelector('.settings-feedback').textContent.includes('Сервер доступен')`);
      for (const [name,value] of [['temperature','0.65'],['max_tokens','1024']]) {
        await win.webContents.executeJavaScript(`{
          const input=document.querySelector('input[name="${name}"]');
          Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(input,${JSON.stringify(value)});
          input.dispatchEvent(new Event('input',{bubbles:true}));
        }`);
        await poll(win, `document.querySelector('input[name="${name}"]').value === ${JSON.stringify(value)}`);
      }
      await win.webContents.executeJavaScript(`document.querySelector('.probe-model').click()`);
      await poll(win, `document.querySelector('.settings-feedback').textContent.includes('Модель ответила')`);
      const beforeInvalid = await win.webContents.executeJavaScript('window.lca.getModelSettings()');
      await win.webContents.executeJavaScript(`{ const input=document.querySelector('input[name="temperature"]'); Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(input,'3'); input.dispatchEvent(new Event('input',{bubbles:true})); }`);
      await win.webContents.executeJavaScript(`document.querySelector('.save-model-settings').click()`);
      await poll(win, `document.querySelector('[role="alert"]').textContent.includes('Temperature')`);
      const afterInvalid = await win.webContents.executeJavaScript('window.lca.getModelSettings()');
      assert.equal(afterInvalid.base_url, beforeInvalid.base_url);
      assert.equal(afterInvalid.model, beforeInvalid.model);
      assert.deepEqual(afterInvalid.settings, beforeInvalid.settings);
      await win.webContents.executeJavaScript(`{ const input=document.querySelector('input[name="temperature"]'); Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(input,'0.65'); input.dispatchEvent(new Event('input',{bubbles:true})); }`);

      await win.webContents.executeJavaScript(`document.querySelector('.save-model-settings').click()`);
      await poll(win, `document.querySelector('.settings-feedback').textContent.includes('Настройки сохранены')`);
      assert.equal((await win.webContents.executeJavaScript('window.lca.getModelSettings()')).settings.temperature, 0.65);
      await win.webContents.executeJavaScript('new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))');
      fs.writeFileSync(path.join(testRoot, 'settings.png'), (await win.webContents.capturePage(undefined, {stayHidden:true})).toPNG());
      await win.webContents.executeJavaScript(`document.querySelector('[title="Закрыть настройки"]').click()`);
      await poll(win, `!document.querySelector('.settings-dialog')`);

      await win.webContents.executeJavaScript(`{
        const input = document.querySelector('.composer textarea');
        Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype,'value').set.call(input, 'hello');
        input.dispatchEvent(new Event('input', { bubbles:true }));
      }`);
      await poll(win, `!document.querySelector('[title="Отправить"]').disabled`);
      await win.webContents.executeJavaScript(`document.querySelector('[title="Отправить"]').click()`);
      await poll(win, `!!document.querySelector('[role="dialog"]')`);
      await win.webContents.executeJavaScript(`document.querySelector('.progress-toggle').click()`);
      assert.equal(await win.webContents.executeJavaScript(`document.querySelector('.task-tools [data-status="awaiting_approval"]').textContent.includes('smoke.txt')`), true);
      assert.equal(await win.webContents.executeJavaScript(`document.querySelector('.task-stages [aria-current="step"]').textContent.includes('Реализация')`), true);
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
      assert.equal(await win.webContents.executeJavaScript(`document.querySelector('.task-tools [data-status="succeeded"]').textContent.includes('Файл записан')`), true);
      assert.equal(await win.webContents.executeJavaScript(`document.querySelector('.task-stages [data-status="skipped"]').textContent.includes('Исследование')`), true);
      await win.webContents.executeJavaScript(`document.querySelector('[title="History"]').click()`);
      await poll(win, `Array.from(document.querySelectorAll('.sidebar .file-row')).some(b => b.textContent === 'hello')`);
      await win.webContents.executeJavaScript(`Array.from(document.querySelectorAll('.sidebar .file-row')).find(b => b.textContent === 'hello').click()`);
      await poll(win, `!!document.querySelector('.task-tools [data-status="succeeded"]') && document.querySelector('.task-files').textContent.includes('smoke.txt')`);
      await win.webContents.executeJavaScript('new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))');
      fs.writeFileSync(path.join(testRoot, 'completed.png'), (await win.webContents.capturePage(undefined, {stayHidden:true})).toPNG());
      const corruptChat = path.join(testRoot, 'LocalCodingAgent/chats', '0'.repeat(32) + '.json');
      fs.writeFileSync(corruptChat, '{broken source');
      modelMode = 'conflict';
      await win.webContents.executeJavaScript(`document.querySelector('[title="Новый чат"]').click()`);
      await poll(win, `!document.querySelector('.task-card') && !document.querySelector('.chat-messages').textContent.includes('Smoke completed')`);
      await poll(win, `document.querySelector('.chat-messages').textContent.includes('исходный файл сохранён')`);
      assert.equal(fs.readFileSync(corruptChat, 'utf8'), '{broken source');
      await win.webContents.executeJavaScript(`{
        const input = document.querySelector('.composer textarea');
        Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype,'value').set.call(input, 'hello conflict');
        input.dispatchEvent(new Event('input', { bubbles:true }));
      }`);
      await poll(win, `!document.querySelector('[title="Отправить"]').disabled`);
      await win.webContents.executeJavaScript(`document.querySelector('[title="Отправить"]').click()`);
      await poll(win, `!!document.querySelector('[role="dialog"]')`);
      fs.writeFileSync(path.join(project, 'conflict.txt'), 'external edit');
      await win.webContents.executeJavaScript(`document.querySelector('.approval-actions .primary-button').click()`);
      await poll(win, `!document.querySelector('[title="Остановить"]') && document.querySelector('.chat-messages').textContent.includes('запросите новый diff')`);
      assert.equal(fs.readFileSync(path.join(project, 'conflict.txt'), 'utf8'), 'external edit');
      assert.equal(await win.webContents.executeJavaScript(`document.querySelector('.task-tools [data-status="failed"]').textContent.includes('изменились')`), true);
      const saved = JSON.parse(fs.readFileSync(path.join(testRoot, 'LocalCodingAgent/model-preferences.json'), 'utf8'));
      assert.deepEqual(saved, {base_url:url, model:'smoke-model', settings:{temperature:0.65,top_p:1,max_tokens:1024,max_context_chars:80000,request_timeout:180,max_agent_turns:200,max_runtime_minutes:180}});
      assert.equal(JSON.stringify(saved).includes('test-secret'), false);
      const reloaded = new Promise(resolve => win.webContents.once('did-finish-load', resolve));
      win.webContents.reload();
      await reloaded;
      await poll(win, `document.querySelector('.agent-context').textContent.includes('smoke-model')`);
      await win.webContents.executeJavaScript(`document.querySelector('[title="Настройки модели"]').click()`);
      await poll(win, `!!document.querySelector('.model-settings input')`);
      assert.equal(await win.webContents.executeJavaScript(`document.querySelector('.model-settings input').value`), url);
      assert.equal(await win.webContents.executeJavaScript(`document.querySelector('input[type="password"]').value`), '');
      assert.equal(await win.webContents.executeJavaScript(`document.querySelector('input[name="temperature"]').value`), '0.65');
      await win.webContents.executeJavaScript(`document.querySelector('[title="Закрыть настройки"]').click()`);
      await poll(win, `!document.querySelector('.settings-dialog')`);

      await win.webContents.executeJavaScript(`document.querySelector('.project-pill').click()`);
      await poll(win, `document.querySelector('.project-pill').textContent.includes(${JSON.stringify(path.basename(project))})`);
      modelMode = 'stall';
      await win.webContents.executeJavaScript(`{
        const input = document.querySelector('.composer textarea');
        Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype,'value').set.call(input, 'hello');
        input.dispatchEvent(new Event('input', { bubbles:true }));
      }`);
      await poll(win, `!document.querySelector('[title="Отправить"]').disabled`);
      await win.webContents.executeJavaScript(`document.querySelector('[title="Отправить"]').click()`);
      await poll(win, `!!document.querySelector('.streaming-caret') && document.body.textContent.includes('Pending ')`);
      const stoppedAt = Date.now();
      await win.webContents.executeJavaScript(`document.querySelector('[title="Остановить"]').click()`);
      await poll(win, `!document.querySelector('[title="Остановить"]') && !!document.querySelector('.progress-toggle')`);
      await win.webContents.executeJavaScript(`document.querySelector('.progress-toggle').click()`);
      await poll(win, `document.querySelector('.task-card').textContent.includes('Приостановлена')`);
      assert.ok(Date.now() - stoppedAt < 3000, 'Stop should not wait for the model timeout');
      assert.equal(streamDisconnected, true);
      assert.equal(await win.webContents.executeJavaScript(`!!document.querySelector('.streaming-caret')`), false);
      await win.webContents.executeJavaScript(`document.querySelector('.progress-toggle').click()`);
      await win.webContents.executeJavaScript('new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))');
      fs.writeFileSync(path.join(testRoot, 'ide.png'), (await win.webContents.capturePage(undefined, {stayHidden:true})).toPNG());
      assert.equal(await win.webContents.executeJavaScript(`getComputedStyle(document.querySelector('.main-panel')).backgroundColor`), 'rgb(25, 25, 28)');
      await win.webContents.executeJavaScript(`document.querySelector('[role=tab]:last-child').click()`);
      await poll(win, `!!document.querySelector('.voice-panel')`);
      fs.writeFileSync(path.join(testRoot, 'voice.png'), (await win.webContents.capturePage(undefined, {stayHidden:true})).toPNG());
      assert.equal(await win.webContents.executeJavaScript(`document.querySelector('.voice-panel').textContent.includes('голос ещё не подключён')`), true);
      await win.webContents.executeJavaScript(`document.querySelector('[role=tab]:first-child').click()`);
      await poll(win, `!!document.querySelector('.mode-chat') && !document.querySelector('.main-panel')`);
      await win.webContents.executeJavaScript(`{ const input=document.querySelector('.composer textarea'); Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype,'value').set.call(input, 'chat without files'); input.dispatchEvent(new Event('input',{bubbles:true})); }`);
      await poll(win, `!document.querySelector('[title="Отправить"]').disabled`);
      await win.webContents.executeJavaScript(`document.querySelector('[title="Отправить"]').click()`);
      await poll(win, `document.querySelector('.chat-messages').textContent.includes('Standalone Chat reply') && !document.querySelector('[title="Остановить"]')`);
      await poll(win, `!!document.querySelector('.chat-code code')`);
      assert.equal(await win.webContents.executeJavaScript(`document.querySelector('.chat-code code').textContent`),'print("<script>safe</script>")');
      assert.equal(await win.webContents.executeJavaScript(`!!document.querySelector('.message-content script')`),false);
      await win.webContents.executeJavaScript(`navigator.clipboard.writeText=async text=>{window.__copiedCode=text;};document.querySelector('.chat-code-heading button').click()`,true);
      await poll(win, `document.querySelector('.chat-code-heading button').textContent==='Скопировано'`);
      assert.equal(await win.webContents.executeJavaScript('window.__copiedCode'),'print("<script>safe</script>")');
      await poll(win, `Array.from(document.querySelectorAll('.chat-history-row')).some(row=>row.textContent.includes('chat without files'))`);
      await win.webContents.executeJavaScript(`Array.from(document.querySelectorAll('.chat-history-row')).find(row=>row.textContent.includes('chat without files')).querySelector('.rename-chat').click()`);
      await poll(win, `!!document.querySelector('[aria-label="Название чата"]')`);
      await win.webContents.executeJavaScript(`{const input=document.querySelector('[aria-label="Название чата"]');Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(input,'Переименованный разговор');input.dispatchEvent(new Event('input',{bubbles:true}));}`);
      await win.webContents.executeJavaScript(`document.querySelector('.rename-dialog form').dispatchEvent(new Event('submit',{bubbles:true,cancelable:true}))`);
      await poll(win, `!document.querySelector('.rename-dialog') && document.querySelector('.sidebar').textContent.includes('Переименованный разговор')`);
      assert.equal(await win.webContents.executeJavaScript(`!!document.querySelector('[role="dialog"]')`), false);
      fs.writeFileSync(path.join(testRoot, 'chat.png'), (await win.webContents.capturePage(undefined, {stayHidden:true})).toPNG());
      modelMode='scroll';
      await win.webContents.executeJavaScript(`{const input=document.querySelector('.composer textarea');Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype,'value').set.call(input,'Scroll verification');input.dispatchEvent(new Event('input',{bubbles:true}));}`);
      await win.webContents.executeJavaScript(`document.querySelector('[title="Отправить"]').click()`);
      await poll(win, `document.querySelector('.chat-messages').textContent.includes('Scroll line 119')`);
      await win.webContents.executeJavaScript(`{const box=document.querySelector('.chat-messages');box.scrollTop=0;box.dispatchEvent(new Event('scroll',{bubbles:true}));}`);
      await poll(win, `!!document.querySelector('.follow-chat')`);
      releaseModelText();
      await poll(win, `document.querySelector('.chat-messages').textContent.includes('More line 119')&&!document.querySelector('[title="Остановить"]')`);
      assert.ok(await win.webContents.executeJavaScript(`document.querySelector('.chat-messages').scrollTop<5`),'Reading old messages must not jump to the streamed answer');
      await win.webContents.executeJavaScript(`document.querySelector('.follow-chat').click()`);
      await poll(win, `!document.querySelector('.follow-chat') && document.querySelector('.chat-messages').scrollTop>100`);
      console.log('PASS: Electron approval and stale-diff conflict, incremental text without duplicate answer, persisted preferences, fast network cancellation');
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
