// Run with Electron after building; the renderer uses the isolated dist files.
// Uses the real main process, preload, renderer, bridge and engine.
const { app, BrowserWindow, dialog, ipcMain, desktopCapturer, nativeImage } = require('electron');
app.disableHardwareAcceleration();
desktopCapturer.getSources=async()=>[{display_id:'fixture',thumbnail:nativeImage.createFromBitmap(Buffer.from([255,0,0,255]),{width:1,height:1})}];
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const assert = require('node:assert/strict');
app.commandLine.appendSwitch('use-fake-device-for-media-stream');
app.commandLine.appendSwitch('use-fake-ui-for-media-stream');
let transcriptionRequests=0;
let transcriptionText='Микрофон fixture';
const transcriptionFixture=http.createServer((request,response)=>{let body=[];request.on('data',chunk=>body.push(chunk));request.on('end',()=>{body=Buffer.concat(body);assert.ok(body.includes(Buffer.from('RIFF')));transcriptionRequests++;response.writeHead(200,{'Content-Type':'application/json'});response.end(JSON.stringify({text:transcriptionText}));});});

// Capture speech IPC in GUI tests: actual System.Speech is tested through WAV,
// so this suite never plays audio on the user's speakers.
let simulatedSpeech=false;
let capturedSpeech=null;
let speechCalls=0;
let companionRequest=false;
let neuralMode=false;
let neuralRequests=0;
let piperRuntimeFixture=false;
const registerIpc=ipcMain.handle.bind(ipcMain);
let handlerForVoiceStatus=async()=>({ok:true,state:'idle',voices:[],recognizers:[]});
ipcMain.handle=(channel,handler)=>{
  if(channel==='voice:status')handlerForVoiceStatus=handler;
  return registerIpc(channel,async(event,...args)=>{
    if(channel==='voice:runtime'&&piperRuntimeFixture)return {ok:true,running:true,occupied:true,modelAvailable:true,runtimeAvailable:true,managed:false};
    if(channel==='voice:speak'&&!neuralMode) {
      capturedSpeech=args[0];speechCalls++;simulatedSpeech=true;
      const result=await handlerForVoiceStatus(event);
      return {...result,state:'speaking'};
    }
    if(channel==='voice:stop')simulatedSpeech=false;
    const result=await handler(event,...args);
    if(channel==='voice:listening')event.sender.setBackgroundThrottling(false); // Hidden fixture still needs audio callbacks and animation frames.
    return channel==='voice:status'&&simulatedSpeech?{...result,state:'speaking'}:result;
  });
};

const testRoot = path.resolve(__dirname, '../../.test-data/electron-smoke');
fs.mkdirSync(testRoot, { recursive: true });
// Continuous deterministic PCM avoids silent phases of Chromium's default fake
// device. Hardware DSP is checked by the recorder unit test, not by this fixture.
const microphoneWave=Buffer.alloc(44+16000*2*3);
microphoneWave.write('RIFF',0);microphoneWave.writeUInt32LE(microphoneWave.length-8,4);microphoneWave.write('WAVEfmt ',8);
microphoneWave.writeUInt32LE(16,16);microphoneWave.writeUInt16LE(1,20);microphoneWave.writeUInt16LE(1,22);
microphoneWave.writeUInt32LE(16000,24);microphoneWave.writeUInt32LE(32000,28);microphoneWave.writeUInt16LE(2,32);microphoneWave.writeUInt16LE(16,34);
microphoneWave.write('data',36);microphoneWave.writeUInt32LE(microphoneWave.length-44,40);
for(let sample=0;sample<48000;sample++)microphoneWave.writeInt16LE(Math.round(6000*Math.sin(2*Math.PI*220*sample/16000)),44+sample*2);
const microphonePath=path.join(testRoot,'microphone-fixture.wav');fs.writeFileSync(microphonePath,microphoneWave);
app.commandLine.appendSwitch('use-file-for-fake-audio-capture',microphonePath);
fs.writeFileSync(path.join(testRoot,'fixture-requests.log'),'');
const resultPath = path.join(testRoot, 'result.json');
fs.writeFileSync(resultPath, JSON.stringify({status:'running'}));
function fail(error) {
  fs.writeFileSync(resultPath, JSON.stringify({status:'failed',error:String(error.stack || error)}, null, 2));
  app.exit(1);
}
process.on('uncaughtException', fail);
process.on('unhandledRejection', fail);
const project = fs.mkdtempSync(path.join(testRoot, 'project-'));
const appData=fs.mkdtempSync(path.join(testRoot,'userdata-'));
process.env.LOCALAPPDATA = appData;
app.setPath('userData', path.join(appData, 'electron-profile'));
BrowserWindow.prototype.show = function () {}; // Keep the test window hidden.
BrowserWindow.prototype.loadURL = function () { return this.loadFile(path.resolve(__dirname,'../../apps/desktop/dist/index.html')); };
let discardChoice = 1;
dialog.showMessageBox = async () => ({response:discardChoice});
fs.writeFileSync(path.join(project,'editor-a.txt'),'first\nsecond\n');
fs.writeFileSync(path.join(project,'editor-b.py'),'print(1)\n');
fs.mkdirSync(path.join(project,'nested'));
fs.writeFileSync(path.join(project,'nested/draft.txt'),'nested source');
fs.symlinkSync(path.join(project,'nested'),path.join(project,'alias-nested'),'junction');
const allowedAppFixture=path.join(project,'allowed-app.exe');fs.writeFileSync(allowedAppFixture,'fixture only, never launched');
dialog.showOpenDialog = async (_win,options) => ({ canceled:false,filePaths:[options?.title==='Разрешить Лоле запуск приложения'?allowedAppFixture:options?.title==='Выберите GGUF'?process.env.LCA_TEST_GGUF:options?.title==='Выберите установленный llama-server'?process.env.LCA_TEST_RUNTIME:project] });

let modelMode = 'write';
let releaseModelText = null;
let streamDisconnected = false;
const model = http.createServer((req, res) => {
  fs.appendFileSync(path.join(testRoot,'fixture-requests.log'), `${new Date().toISOString()} ${req.method} ${req.url}\n`);
  let raw = '';
  req.on('data', chunk => { raw += chunk; });
  req.on('end', () => {
    if(req.url==='/tts') {
      const input=JSON.parse(raw);assert.ok(input.instructions.includes('anime'));neuralRequests++;
      const wav=Buffer.alloc(4844);wav.write('RIFF');wav.writeUInt32LE(4836,4);wav.write('WAVEfmt ',8);
      wav.writeUInt32LE(16,16);wav.writeUInt16LE(1,20);wav.writeUInt16LE(1,22);wav.writeUInt32LE(24000,24);
      wav.writeUInt32LE(48000,28);wav.writeUInt16LE(2,32);wav.writeUInt16LE(16,34);wav.write('data',36);wav.writeUInt32LE(4800,40);
      res.writeHead(200,{'Content-Type':'audio/wav'});res.end(wav);return;
    }
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
    if(modelMode==='desktop') {
      const delta=input.messages.some(message=>message.role==='tool')?{content:'Screenshot created'}:{tool_calls:[{index:0,id:'screen-fixture',type:'function',function:{name:'desktop_screenshot',arguments:'{}'}}]};
      res.end(encode(delta)+'data: [DONE]\n\n');
    }else if (!input.tools?.some(tool=>tool.function.name==='write_file')) {
      if(!input.tools)assert.equal(input.tool_choice, undefined);
      if(input.messages[0].content.includes('Лола'))companionRequest=true;
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
const deadline = setTimeout(() => fail(new Error('Smoke timed out')), process.env.LCA_TEST_RUNTIME?180000:90000);
app.on('browser-window-created', (_event, win) => {
  const executeScript=win.webContents.executeJavaScript.bind(win.webContents);
  win.webContents.executeJavaScript=async(...args)=>{
    try{const result=await executeScript(...args);await new Promise(resolve=>setTimeout(resolve,25));return result;}
    catch(error){throw new Error(`Renderer script failed: ${args[0]}\n${error}`);}
  };
  win.webContents.setBackgroundThrottling(false);
  win.webContents.on('preload-error', (_event, preloadPath, error) => {
    fs.writeFileSync(path.join(testRoot, 'preload-error.txt'), preloadPath + '\n' + String(error.stack || error));
  });
  win.webContents.once('did-finish-load', async () => {
    try {
      await poll(win, `document.querySelector('.status')?.textContent.includes('Готов к работе')`);
      assert.equal(await win.webContents.executeJavaScript('typeof require'), 'undefined');
      await win.webContents.executeJavaScript(`document.querySelector('.activity-bar [role=tab]:nth-child(2)').click()`);
      await poll(win, `!!document.querySelector('.project-pill')`);
      await win.webContents.executeJavaScript(`document.querySelector('.activity-bar [role=tab]:nth-child(2)').click()`);
      await poll(win, `!!document.querySelector('.project-pill')`);
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
      await win.webContents.executeJavaScript(`Array.from(document.querySelectorAll('.sidebar .file-row')).find(button=>button.textContent==='nested').click()`);
      await poll(win, `Array.from(document.querySelectorAll('.sidebar .file-row')).some(button=>button.textContent==='draft.txt')`);
      await win.webContents.executeJavaScript(`Array.from(document.querySelectorAll('.sidebar .file-row')).find(button=>button.textContent==='draft.txt').click()`);
      await poll(win, `document.querySelector('.editor-input').value==='nested source'`);
      await win.webContents.executeJavaScript(`{const input=document.querySelector('.editor-input');Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype,'value').set.call(input,'unsaved nested draft');input.dispatchEvent(new Event('input',{bubbles:true}));}`);
      await poll(win, `!!document.querySelector('.editor-tabs [title="nested/draft.txt"] .editor-dirty')`);
      await win.webContents.executeJavaScript(`Array.from(document.querySelectorAll('.sidebar .file-row')).find(button=>button.textContent==='draft.txt').click()`);
      await win.webContents.executeJavaScript('window.lca.health()');
      await win.webContents.executeJavaScript('new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)))');
      assert.equal(await win.webContents.executeJavaScript(`document.querySelector('.editor-input').value`),'unsaved nested draft');
      assert.equal(fs.readFileSync(path.join(project,'nested/draft.txt'),'utf8'),'nested source');
      await win.webContents.executeJavaScript(`Array.from(document.querySelectorAll('.sidebar .file-row')).find(button=>button.textContent==='..').click()`);
      await poll(win, `Array.from(document.querySelectorAll('.sidebar .file-row')).some(button=>button.textContent==='alias-nested')`);
      await win.webContents.executeJavaScript(`Array.from(document.querySelectorAll('.sidebar .file-row')).find(button=>button.textContent==='alias-nested').click()`);
      await poll(win, `Array.from(document.querySelectorAll('.sidebar .file-row')).some(button=>button.textContent==='draft.txt')`);
      await win.webContents.executeJavaScript(`Array.from(document.querySelectorAll('.sidebar .file-row')).find(button=>button.textContent==='draft.txt').click()`);
      await win.webContents.executeJavaScript('window.lca.health()');
      await win.webContents.executeJavaScript('new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)))');
      assert.equal(await win.webContents.executeJavaScript(`document.querySelector('.editor-input').value`),'unsaved nested draft');
      assert.equal(await win.webContents.executeJavaScript(`document.querySelectorAll('.editor-tabs [title="nested/draft.txt"]').length`),1);
      await win.webContents.executeJavaScript(`document.querySelector('[title="Закрыть nested/draft.txt"]').click()`);
      await poll(win, `!document.querySelector('.editor-tabs [title="nested/draft.txt"]')`);
      await win.webContents.executeJavaScript(`document.querySelector('[title="Файлы проекта"]').click()`);
      await win.webContents.executeJavaScript(`Array.from(document.querySelectorAll('.sidebar .file-row')).find(button=>button.textContent==='..').click()`);
      await poll(win, `Array.from(document.querySelectorAll('.sidebar .file-row')).some(button=>button.textContent==='editor-a.txt')`);
      await win.webContents.executeJavaScript(`document.querySelector('.editor-tabs [title="editor-a.txt"]').click()`);
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
      app.quit();
      await new Promise(resolve=>setTimeout(resolve,100));
      assert.equal(win.isDestroyed(),false);
      assert.equal((await win.webContents.executeJavaScript('window.lca.health()')).ok,true);
      fs.writeFileSync(path.join(project,'editor-a.txt'),'external change');
      await win.webContents.executeJavaScript(`window.dispatchEvent(new KeyboardEvent('keydown',{key:'s',ctrlKey:true,bubbles:true}))`);
      await poll(win, `!!document.querySelector('.editor-notice')?.textContent.includes('изменился на диске')`);
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
      await poll(win, `!!document.querySelector('input[name="base_url"]')`);
      await win.webContents.executeJavaScript(`Array.from(document.querySelectorAll('.settings-tabs button')).find(b=>b.textContent==='Оформление').click()`);
      await poll(win, `!document.querySelector('.appearance-settings').parentElement.hidden`);
      await win.webContents.executeJavaScript(`{const input=document.querySelector('[aria-label="Тема интерфейса"]');input.value='light';input.dispatchEvent(new Event('change',{bubbles:true}));}`);
      await poll(win, `document.querySelector('.app-shell').dataset.theme==='light'`);
      await win.webContents.executeJavaScript(`{const input=document.querySelector('[aria-label="Плотность интерфейса"]');input.value='compact';input.dispatchEvent(new Event('change',{bubbles:true}));}`);
      await poll(win, `document.querySelector('.app-shell').dataset.density==='compact'`);
      await win.webContents.executeJavaScript(`document.querySelector('[aria-label="Боковая панель и история"]').click()`);
      await poll(win, `getComputedStyle(document.querySelector('.sidebar')).display==='none'`);
      await win.webContents.executeJavaScript('new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)))');
      fs.writeFileSync(path.join(testRoot,'appearance.png'),(await win.webContents.capturePage(undefined,{stayHidden:true})).toPNG());
      await win.webContents.executeJavaScript(`Array.from(document.querySelectorAll('.appearance-settings button')).find(button=>button.textContent.includes('Вернуть стандартное')).click();document.querySelector('.settings-tabs button:first-child').click()`);
      await poll(win, `document.querySelector('.app-shell').dataset.theme==='dark'&&getComputedStyle(document.querySelector('.sidebar')).display!=='none'`);
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
        const input = document.querySelector('input[name="base_url"]');
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
          const input=document.querySelector('.reset-generation').closest('.settings-section').querySelector('input[name="${name}"]');
          Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(input,${JSON.stringify(value)});
          input.dispatchEvent(new Event('input',{bubbles:true}));
        }`);
        await poll(win, `document.querySelector('.reset-generation').closest('.settings-section').querySelector('input[name="${name}"]').value === ${JSON.stringify(value)}`);
      }
      await win.webContents.executeJavaScript(`document.querySelector('.probe-model').click()`);
      await poll(win, `document.querySelector('.settings-feedback').textContent.includes('Модель ответила')`);
      const beforeInvalid = await win.webContents.executeJavaScript('window.lca.getModelSettings()');
      await win.webContents.executeJavaScript(`{ const input=document.querySelector('.reset-generation').closest('.settings-section').querySelector('input[name="temperature"]'); Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(input,'3'); input.dispatchEvent(new Event('input',{bubbles:true})); }`);
      await win.webContents.executeJavaScript(`document.querySelector('.save-model-settings').click()`);
      await poll(win, `document.querySelector('[role="alert"]')?.textContent.includes('Temperature')`);
      const afterInvalid = await win.webContents.executeJavaScript('window.lca.getModelSettings()');
      assert.equal(afterInvalid.base_url, beforeInvalid.base_url);
      assert.equal(afterInvalid.model, beforeInvalid.model);
      assert.deepEqual(afterInvalid.settings, beforeInvalid.settings);
      await win.webContents.executeJavaScript(`{ const input=document.querySelector('.reset-generation').closest('.settings-section').querySelector('input[name="temperature"]'); Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(input,'0.65'); input.dispatchEvent(new Event('input',{bubbles:true})); }`);

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
      await poll(win, `!!document.querySelector('[role="dialog"]')`, 30000);
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
      await win.webContents.executeJavaScript(`document.querySelector('[title="Разговоры"]').click()`);
      await poll(win, `Array.from(document.querySelectorAll('.sidebar .file-row')).some(b => b.textContent === 'hello')`);
      await win.webContents.executeJavaScript(`Array.from(document.querySelectorAll('.sidebar .file-row')).find(b => b.textContent === 'hello').click()`);
      await poll(win, `!!document.querySelector('.task-tools [data-status="succeeded"]') && document.querySelector('.task-files').textContent.includes('smoke.txt')`);
      await win.webContents.executeJavaScript('new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))');
      fs.writeFileSync(path.join(testRoot, 'completed.png'), (await win.webContents.capturePage(undefined, {stayHidden:true})).toPNG());
      const corruptChat = path.join(appData, 'LocalCodingAgent/chats', '0'.repeat(32) + '.json');
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
      const saved = JSON.parse(fs.readFileSync(path.join(appData, 'LocalCodingAgent/model-preferences.json'), 'utf8'));
      assert.deepEqual(saved, {api_protocol:'chat',tool_protocol:'native',base_url:url, model:'smoke-model', settings:{temperature:0.65,top_p:1,max_tokens:1024,max_context_chars:80000,request_timeout:180,max_agent_turns:200,max_runtime_minutes:180}});
      assert.equal(JSON.stringify(saved).includes('test-secret'), false);
      const reloaded = new Promise(resolve => win.webContents.once('did-finish-load', resolve));
      win.webContents.reload();
      await reloaded;
      await poll(win, `document.querySelector('.agent-context').textContent.includes('smoke-model')`);
      await win.webContents.executeJavaScript(`document.querySelector('[title="Настройки модели"]').click()`);
      await poll(win, `!!document.querySelector('input[name="base_url"]')`);
      assert.equal(await win.webContents.executeJavaScript(`document.querySelector('input[name="base_url"]').value`), url);
      assert.equal(await win.webContents.executeJavaScript(`document.querySelector('input[type="password"]').value`), '');
      assert.equal(await win.webContents.executeJavaScript(`document.querySelector('.reset-generation').closest('.settings-section').querySelector('input[name="temperature"]').value`), '0.65');
      await win.webContents.executeJavaScript(`document.querySelector('[title="Закрыть настройки"]').click()`);
      await poll(win, `!document.querySelector('.settings-dialog')`);

      await win.webContents.executeJavaScript(`document.querySelector('.activity-bar [role=tab]:nth-child(2)').click()`);
      await poll(win, `!!document.querySelector('.project-pill')`);
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
      assert.equal(await win.webContents.executeJavaScript(`getComputedStyle(document.querySelector('.main-panel')).backgroundColor`), await win.webContents.executeJavaScript(`getComputedStyle(document.querySelector('.app-shell')).backgroundColor`));
      await win.webContents.executeJavaScript(`window.lca.configureCompanion({base_url:${JSON.stringify(url)},model:'smoke-model',tts_provider:'windows',persona:'Лола — дружелюбная помощница',auto_delegate:false,stt_url:'http://127.0.0.1:${transcriptionFixture.address().port}/inference'})`);
      await win.webContents.executeJavaScript(`document.querySelector('[role=tab]:last-child').click()`);
      await poll(win, `!!document.querySelector('.voice-panel')`);
      await win.webContents.executeJavaScript(`{const media=navigator.mediaDevices;const capture=media.getUserMedia.bind(media);media.getUserMedia=()=>capture({audio:{echoCancellation:false,noiseSuppression:false,autoGainControl:false},video:false});const create=AudioContext.prototype.createScriptProcessor;AudioContext.prototype.createScriptProcessor=function(...args){window.__micBlocks=0;const processor=create.apply(this,args);processor.addEventListener('audioprocess',()=>window.__micBlocks++);return processor;};void 0;}`);
      assert.equal(await win.webContents.executeJavaScript(`!!document.querySelector('.miya-character')&&getComputedStyle(document.querySelector('.miya-character')).backgroundImage.includes('miya-states')`),true,'Reference character atlas must be displayed');
      await poll(win, `document.querySelector('.voice-panel').textContent.includes('Микрофон включается по нажатию')`);
      assert.equal(await win.webContents.executeJavaScript(`!!document.querySelector('.microphone-record')`),true);
      await poll(win, `!document.querySelector('.microphone-record').disabled`);
      await poll(win, `(()=>{const button=document.querySelector('.microphone-record');if(button.disabled)return false;window.__micBlocks=0;button.click();return true;})()`);
      await poll(win, `document.querySelector('.voice-stt-note').textContent.includes('Идёт запись')`);
      await poll(win, `window.__micBlocks>=10`,15000);
      await win.webContents.executeJavaScript(`window.__micBlocks=0;document.querySelector('.microphone-record').click()`,true);
      await poll(win, `document.querySelector('[aria-label="Сообщение ассистенту"]').value==='Микрофон fixture'`);
      assert.equal(transcriptionRequests,1,'Synthetic microphone must send one actual WAV request');
      assert.equal(await win.webContents.executeJavaScript(`!!document.querySelector('.voice-composer button[type=button]')`),false,'Recognition does not submit the task automatically');

      await win.webContents.executeJavaScript(`{const input=document.querySelector('[aria-label="Сообщение ассистенту"]');Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype,'value').set.call(input,'Привет, Лола');input.dispatchEvent(new Event('input',{bubbles:true}));}`);
      await win.webContents.executeJavaScript(`document.querySelector('.voice-composer').dispatchEvent(new Event('submit',{bubbles:true,cancelable:true}))`);
      await poll(win, `document.querySelector('.voice-conversation').textContent.includes('Standalone Chat reply')&&!document.querySelector('.voice-composer button[type=button]')`);
      assert.equal(companionRequest,true,'Companion uses a persona and no file tools');
      assert.equal(await win.webContents.executeJavaScript(`document.querySelector('.voice-conversation').getBoundingClientRect().height>200`),true);
      assert.equal(await win.webContents.executeJavaScript(`document.querySelector('.miya-settings-dialog').open`),false,'Settings must be hidden by default');
      await win.webContents.executeJavaScript(`document.querySelector('.miya-settings-open').click()`);
      await poll(win, `document.querySelector('.miya-settings-dialog').open`);
      assert.equal(await win.webContents.executeJavaScript(`document.querySelector('.miya-settings-dialog').contains(document.activeElement)`),true,'Modal must capture keyboard focus');
      await win.webContents.executeJavaScript(`document.querySelector('[aria-label="Сразу отправлять распознанный запрос"]').click();document.querySelector('[aria-label="Закрыть настройки Лолы"]').click()`);
      await win.webContents.executeJavaScript(`window.__micBlocks=0;document.querySelector('.microphone-record').click()`,true);
      await poll(win, `document.querySelector('.voice-stt-note').textContent.includes('Идёт запись')`);
      await poll(win, `window.__micBlocks>=10`,15000);
      await win.webContents.executeJavaScript(`window.__micBlocks=0;document.querySelector('.microphone-record').click()`,true);
      await poll(win, `document.querySelector('.voice-conversation').textContent.includes('Микрофон fixture')&&document.querySelector('[aria-label="Сообщение ассистенту"]').value===''&&!document.querySelector('.voice-composer button[type=button]')`);
      assert.equal(transcriptionRequests,2,'Opt-in voice command is submitted exactly once');
      await win.webContents.executeJavaScript(`document.querySelector('.miya-settings-open').click()`);
      await poll(win, `document.querySelector('.miya-settings-dialog').open`);
      await win.webContents.executeJavaScript(`document.querySelector('[aria-label="Сразу отправлять распознанный запрос"]').click()`);
      win.webContents.sendInputEvent({type:'keyDown',keyCode:'Escape'});
      win.webContents.sendInputEvent({type:'keyUp',keyCode:'Escape'});
      await poll(win, `!document.querySelector('.miya-settings-dialog').open`);
      assert.equal(await win.webContents.executeJavaScript(`document.activeElement===document.querySelector('.miya-settings-open')`),true,'Escape restores focus to Settings');
      await poll(win, `document.querySelector('.voice-state').textContent.includes('Готова')||!!document.querySelector('.voice-error')`);
      const voiceStatus=await win.webContents.executeJavaScript('window.lca.voiceStatus()');
      if(voiceStatus.voices.length) {
        await win.webContents.executeJavaScript(`document.querySelector('.speak-reply').click()`);
        await poll(win, `!!document.querySelector('.voice-speaking')`);
        assert.ok(capturedSpeech.text.includes('Standalone Chat reply'));
        assert.ok(voiceStatus.voices.some(voice=>voice.id===capturedSpeech.voice));
        await win.webContents.executeJavaScript(`document.querySelector('.stop-speech').click()`);
        await poll(win, `!document.querySelector('.voice-speaking')`);
        const callsBefore=speechCalls;
        await win.webContents.executeJavaScript(`document.querySelector('.miya-settings-open').click()`);
        await poll(win, `document.querySelector('.miya-settings-dialog').open`);
        await win.webContents.executeJavaScript(`document.querySelector('.miya-settings-dialog .auto-speak input').click();document.querySelector('[aria-label="Закрыть настройки Лолы"]').click()`);
        await win.webContents.executeJavaScript(`{const input=document.querySelector('[aria-label="Сообщение ассистенту"]');Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype,'value').set.call(input,'Повтори ответ');input.dispatchEvent(new Event('input',{bubbles:true}));}`);
        await win.webContents.executeJavaScript(`document.querySelector('.voice-composer').dispatchEvent(new Event('submit',{bubbles:true,cancelable:true}))`);
        await poll(win, `!!document.querySelector('.voice-speaking')`);
        assert.equal(speechCalls,callsBefore+1,'An identical new reply must be spoken once when opt-in is enabled');
        await win.webContents.executeJavaScript(`document.querySelector('.stop-speech').click()`);
        await poll(win, `!document.querySelector('.voice-speaking')`);
      }
      await win.webContents.executeJavaScript('new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)))');
      assert.equal(await win.webContents.executeJavaScript(`document.querySelector('.miya-settings-dialog').open`),false,'Settings close without hiding the conversation');
      fs.writeFileSync(path.join(testRoot,'voice.png'),(await win.webContents.capturePage(undefined,{stayHidden:true})).toPNG());
      await win.webContents.executeJavaScript(`document.querySelector('[role=tab]:first-child').click()`);
      await poll(win, `!!document.querySelector('.mode-chat') && !document.querySelector('.main-panel')`);
      await poll(win, `!document.querySelector('.sidebar').textContent.includes('Привет, Лола')`);
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
      await win.webContents.executeJavaScript('new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)))');
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
      modelMode='desktop';
      const allowedApps=await win.webContents.executeJavaScript('window.lca.addDesktopApplication()');
      assert.equal(allowedApps.ok,true);
      const addedApp=allowedApps.applications.find(item=>item.name==='allowed-app');
      assert.ok(addedApp?.custom);assert.equal(addedApp.file,undefined);
      const persistedApps=await win.webContents.executeJavaScript('window.lca.desktopApplications()');
      assert.ok(persistedApps.applications.some(item=>item.id===addedApp.id));
      const removedApps=await win.webContents.executeJavaScript(`window.lca.removeDesktopApplication(${JSON.stringify(addedApp.id)})`);
      assert.ok(!removedApps.applications.some(item=>item.id===addedApp.id));
      await win.webContents.executeJavaScript('window.lca.configureDesktop(true)');
      await win.webContents.executeJavaScript(`{const input=document.querySelector('.composer textarea');Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype,'value').set.call(input,'Сделай скриншот');input.dispatchEvent(new Event('input',{bubbles:true}));}`);
      await poll(win, `!document.querySelector('[title="Отправить"]').disabled`);
      await win.webContents.executeJavaScript(`document.querySelector('[title="Отправить"]').click()`);
      await poll(win, `!!document.querySelector('.desktop-artifact img')&&!document.querySelector('[title="Остановить"]')`);
      assert.ok(await win.webContents.executeJavaScript(`document.querySelector('.desktop-artifact img').src.startsWith('data:image/png;base64,')`));
      await win.webContents.executeJavaScript(`document.querySelector('.desktop-artifact button').click();window.lca.configureDesktop(false)`);
      neuralMode=true;
      await win.webContents.executeJavaScript(`window.lca.configureCompanion({base_url:${JSON.stringify(url)},model:'smoke-model',tts_provider:'qwen3',tts_url:${JSON.stringify(url.replace('/v1','/tts'))},stt_url:'http://127.0.0.1:${transcriptionFixture.address().port}/inference',wake_phrase:'Привет, Лола',wake_auto_send:false})`);
      await win.webContents.executeJavaScript(`window.dispatchEvent(new Event('companion-profile'));true`);
      const neural=await win.webContents.executeJavaScript(`window.lca.speak({text:'Привет, я Лола!',volume:0,rate:0})`);
      assert.equal(neural.ok,true);
      await poll(win, `(async()=>{const s=await window.lca.voiceStatus();return s.sequence>0&&s.state==='idle';})()`,15000);
      assert.equal(neuralRequests,1);
      transcriptionText='Привет, Лола';
      await win.webContents.executeJavaScript(`document.querySelector('.wake-control button').click()`,true);
      await poll(win, `!!document.querySelector('.voice-panel')`,20000);
      await poll(win, `document.querySelector('.wake-control').textContent.includes('Лола активирована')`,5000);
      transcriptionText='Расскажи про музыку';
      await poll(win, `document.querySelector('[aria-label="Сообщение ассистенту"]').value==='Расскажи про музыку'`,20000);
      assert.equal(await win.webContents.executeJavaScript(`!!document.querySelector('.voice-composer button[type=button]')`),false,'Wake command requires review by default');
      await win.webContents.executeJavaScript(`document.querySelector('.wake-control button').click()`,true);
      piperRuntimeFixture=true;neuralMode=false;
      await win.webContents.executeJavaScript(`(async()=>{const profile=await window.lca.getCompanionSettings();await window.lca.configureCompanion({...profile,tts_provider:'piper'});document.querySelector('[role=tab]:first-child').click();})()`);
      await poll(win, `!document.querySelector('.voice-panel')`);
      await win.webContents.executeJavaScript(`document.querySelector('[role=tab]:last-child').click()`);
      await poll(win, `document.querySelector('.voice-connection')?.textContent==='Подключена'`);
      assert.equal(await win.webContents.executeJavaScript(`document.querySelector('[aria-label="Движок озвучки"]').value`),'piper');
      assert.equal(await win.webContents.executeJavaScript(`!!document.querySelector('[aria-label="Голос ассистента"]')`),false,'Serena should not expose a technical voice ID selector');
      await win.webContents.executeJavaScript(`document.querySelector('.miya-settings-open').click()`);
      await poll(win, `document.querySelector('.miya-settings-dialog').open`);
      assert.equal(await win.webContents.executeJavaScript(`getComputedStyle(document.querySelector('.miya-settings-dialog')).display`),'flex');
      await win.webContents.executeJavaScript('new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)))');
      fs.writeFileSync(path.join(testRoot,'miya-settings.png'),(await win.webContents.capturePage(undefined,{stayHidden:true})).toPNG());
      await win.webContents.executeJavaScript(`document.querySelector('.miya-motion-toggle').click()`);
      assert.equal(await win.webContents.executeJavaScript(`!!document.querySelector('.miya-still')`),true);
      await win.webContents.executeJavaScript(`document.querySelector('.miya-motion-toggle').click();document.querySelector('[aria-label="Закрыть настройки Лолы"]').click();document.querySelector('.voice-panel').scrollTop=0;`);
      await win.webContents.executeJavaScript('new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)))');
      fs.writeFileSync(path.join(testRoot,'serena.png'),(await win.webContents.capturePage(undefined,{stayHidden:true})).toPNG());
      console.log('PASS: editor, approvals, streaming, voice profiles, silent neural WAV playback and wake phrase from Chat');
      fs.writeFileSync(resultPath, JSON.stringify({status:'passed',project}, null, 2));
      clearTimeout(deadline); model.close(); transcriptionFixture.close(); app.quit();
    } catch (error) {
      console.error(String(error.stack||error));
      try {
        fs.writeFileSync(path.join(testRoot, 'failure.png'), (await win.webContents.capturePage()).toPNG());
        fs.writeFileSync(path.join(testRoot, 'failure-state.txt'), await win.webContents.executeJavaScript(`JSON.stringify({text:document.body.textContent,api:typeof window.lca,baseUrl:document.querySelector('input[name="base_url"]')?.value})`));
      }catch(captureError){console.error('Failure snapshot unavailable: '+String(captureError));}
      model.close(); transcriptionFixture.close(); fail(error);
    }
  });
});
transcriptionFixture.listen(0,'127.0.0.1',()=>model.listen(0, '127.0.0.1', () => require('../../apps/desktop/dist-electron/main.cjs')));
