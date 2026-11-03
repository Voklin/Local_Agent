// Test the actual Windows package using temporary data and loopback CDP.
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import http from 'node:http';
import { spawn } from 'node:child_process';
import { setTimeout as delay } from 'node:timers/promises';
import { fileURLToPath } from 'node:url';
import { resolvePackagedExecutable } from './packaged-path.mjs';
import { verifyPackagedIde } from './packaged-ide.mjs';

async function freePort() {
  const server = http.createServer();
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  const port = server.address().port;
  await new Promise(resolve => server.close(resolve));
  return port;
}

async function connectPage(port, child, companion = false) {
  const deadline = Date.now() + 30_000;
  while (Date.now() < deadline && child.exitCode === null) {
    try {
      const pages = await (await fetch(`http://127.0.0.1:${port}/json/list`, { signal: AbortSignal.timeout(1000) })).json();
      const page = pages.find(item => item.type === 'page' && item.url.startsWith('file:') && (companion ? item.url.endsWith('/lola.html') : !item.url.endsWith('/lola.html')));
      if (page) {
        const socket = new WebSocket(page.webSocketDebuggerUrl);
        await new Promise((resolve, reject) => { socket.addEventListener('open', resolve, { once: true }); socket.addEventListener('error', reject, { once: true }); });
        return socket;
      }
    } catch { /* Chromium may still be starting. */ }
    await delay(100);
  }
  throw new Error(`Packaged page did not start; exit=${child.exitCode}`);
}

function evaluate(socket, expression) {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error('CDP evaluation timed out: ' + expression.slice(0, 80))), 45_000);
    const receive = event => {
      const message = JSON.parse(event.data);
      if (message.id !== 1) return;
      clearTimeout(timer); socket.removeEventListener('message', receive);
      if (message.error || message.result.exceptionDetails) reject(new Error(JSON.stringify(message)));
      else resolve(message.result.result.value);
    };
    socket.addEventListener('message', receive);
    socket.send(JSON.stringify({ id: 1, method: 'Runtime.evaluate', params: { expression, awaitPromise: true, returnByValue: true } }));
  });
}

async function run(executable, directory, first, modelUrl) {
  const port = await freePort();
  const env = { ...process.env, LOCALAPPDATA: directory, PATH: path.join(process.env.SystemRoot, 'System32'),
    LCA_PYTHON: 'Z:\\missing-python.exe', PYTHONHOME: 'Z:\\missing-home', PYTHONPATH: 'Z:\\missing-modules', NEUTRAL_IDE_TEST_CDP: '1' };
  delete env.ELECTRON_RUN_AS_NODE;
  const child = spawn(executable, [`--user-data-dir=${path.join(directory, 'profile')}`, '--remote-debugging-address=127.0.0.1', `--remote-debugging-port=${port}`, '--disable-renderer-backgrounding', '--disable-background-timer-throttling', '--disable-backgrounding-occluded-windows'],
    { cwd: directory, env, windowsHide: true, stdio: ['ignore', 'ignore', 'pipe'] });
  let stderr = '';
  console.log(JSON.stringify({event:'package-start',pid:child.pid,first,directory}));
  child.stderr.on('data', chunk => { stderr = (stderr + chunk).slice(-8000); });
  const exited = new Promise(resolve => child.once('exit', (code,signal)=>{console.log(JSON.stringify({event:'package-exit',pid:child.pid,code,signal}));resolve(code);}));
  let socket, companionSocket;
  try {
    socket = await connectPage(port, child);
    let health;
    for (let attempt = 0; attempt < 50; attempt++) {
      health = await evaluate(socket, 'window.lca ? window.lca.health() : null');
      if (health?.ok) break;
      await delay(100);
    }
    assert.equal(health?.service, 'python-core-bridge', stderr);
    const optional=await evaluate(socket,'window.lca.optionalSettings()');
    assert.equal(optional.ok,true);assert.equal(optional.inference.busy,false);
    const lola=await evaluate(socket,'window.lca.getDesktopLola()');
    assert.equal(lola.ok,true);assert.equal(lola.settings.enabled,false,'Desktop Lola must stay opt-in');
    if(first){
      assert.ok(Object.values(optional.settings).every(item=>!item.enabled),'Optional IDE must default off');
      optional.settings.worktrees.enabled=true;
      assert.equal((await evaluate(socket,`window.lca.configureOptionalIde(${JSON.stringify(optional.settings)})`)).ok,true);
      lola.settings.size=280;lola.settings.animate=false;
      assert.equal((await evaluate(socket,`window.lca.configureDesktopLola(${JSON.stringify(lola.settings)})`)).ok,true);
      assert.equal((await evaluate(socket,`window.lca.configureDesktopLola(${JSON.stringify({...lola.settings,enabled:true,mode:'desktop'})})`)).ok,true);
      companionSocket=await connectPage(port,child,true);
      for(let attempt=0;attempt<50;attempt++){
        if(await evaluate(companionSocket,"!!window.lola&&!!document.querySelector('.lola-sprite')"))break;
        await delay(100);
      }
      assert.equal((await evaluate(companionSocket,'window.lola.status()')).settings.enabled,true);
      assert.equal(await evaluate(companionSocket,'typeof window.lca.startTask'),'function');
      assert.equal((await evaluate(companionSocket,"window.lca.configureModel({base_url:'http://example.invalid',model:'forbidden'})")).ok,false,'Popup cannot configure the main model');
      assert.ok(await evaluate(companionSocket,"document.querySelector('.lola-sprite image')?.getAttribute('href').includes('lola-chibi-atlas-v2')"));
      companionSocket.close();companionSocket=undefined;
      assert.equal((await evaluate(socket,`window.lca.configureDesktopLola(${JSON.stringify(lola.settings)})`)).ok,true);
    }else {
      assert.equal(optional.settings.worktrees.enabled,true,'Optional settings must survive restart');
      assert.equal(lola.settings.enabled,false,'Desktop Lola must remain disabled after restart');
      assert.equal(lola.settings.size,280,'Desktop Lola size must survive restart');
      assert.equal(lola.settings.animate,false,'Desktop Lola animation preference must survive restart');
    }
    assert.equal(await evaluate(socket,"typeof window.lca.getIDEWorkflow"),'undefined');
    assert.equal(await evaluate(socket,'typeof window.lca.previewRollback'),'function');
    assert.equal(await evaluate(socket,'typeof window.lca.listSnapshots'),'function');
    const storage=await evaluate(socket,'window.lca.storageStatus()');
    assert.equal(storage.ok,true);assert.equal(storage.report.version,3);assert.equal(storage.report.integrity,'ok');
    assert.equal(storage.report.migration.chats,2);assert.equal(storage.report.migration.messages,4);
    const chatScope=await evaluate(socket,"window.lca.listChats('chat')");const voiceScope=await evaluate(socket,"window.lca.listChats('voice')");
    assert.ok(chatScope.chats.some(chat=>chat.id==='11111111111111111111111111111111'));
    assert.ok(!chatScope.chats.some(chat=>chat.id==='22222222222222222222222222222222'));
    assert.ok(voiceScope.chats.some(chat=>chat.id==='22222222222222222222222222222222'));
    const connections=await evaluate(socket,'window.lca.listConnections()');
    assert.equal(connections.ok,true);
    if(first){const saved=await evaluate(socket,`window.lca.saveConnection({name:'Packaged API',base_url:'https://api.openai.com/v1',model:'packaged-api',api_protocol:'responses',api_key:'packaged-role-secret'})`);assert.equal(saved.ok,true);assert.ok(!JSON.stringify(saved).includes('packaged-role-secret'));}
    else{assert.ok(connections.profiles.some(p=>p.model==='packaged-api'&&p.api_protocol==='responses'));}
    const applications=await evaluate(socket,'window.lca.desktopApplications()');
    assert.equal(applications.ok,true);assert.ok(applications.applications.some(item=>item.id==='browser'));
    assert.ok(applications.applications.every(item=>typeof item.name==='string'&&!('file' in item)));
    assert.equal(await evaluate(socket, 'typeof require'), 'undefined');
    const runtime = await evaluate(socket, 'window.lca.runtimeStatus()');
    assert.equal(runtime.ok, true);
    assert.equal(path.basename(runtime.bundled_runtime), 'llama-server.exe');
    await fs.access(runtime.bundled_runtime);
    await fs.access(path.join(path.dirname(runtime.bundled_runtime), 'llama-server-impl.dll'));
    if (first) {
      const config = { base_url: modelUrl, model: 'packaged-smoke', api_key: 'packaging-test-secret', settings:{temperature:0.45,max_tokens:1536} };
      assert.equal((await evaluate(socket, `window.lca.configureModel(${JSON.stringify(config)})`)).ok, true);
    }
    assert.equal((await evaluate(socket, 'window.lca.getModelSettings()')).model, 'packaged-smoke');
    assert.equal((await evaluate(socket, 'window.lca.getModelSettings()')).settings.temperature, 0.45);
    assert.equal((await evaluate(socket, 'window.lca.getModelSettings()')).settings.max_tokens, 1536);
    assert.deepEqual((await evaluate(socket, 'window.lca.listModels()')).models, ['packaged-smoke']);
    assert.equal((await evaluate(socket, `window.lca.testModel({base_url:${JSON.stringify(modelUrl)},model:'packaged-smoke'})`)).ok, true);
    const companion=await evaluate(socket,'window.lca.getCompanionSettings()');
    if(first)assert.equal(companion.tts_provider,'piper','New installations recommend Serena');
    const voiceRuntime=await evaluate(socket,`window.lca.speechRuntime('status')`);
    assert.equal(voiceRuntime.ok,true);assert.equal(voiceRuntime.runtimeAvailable,false,'Isolated profile has no optional Python voice runtime');
    assert.equal((await evaluate(socket,`window.lca.configureCompanion({...${JSON.stringify(companion)},tts_provider:'windows'})`)).ok,true);
    assert.equal(await evaluate(socket,"document.querySelectorAll('.mode-tabs button').length"),2,'Studio keeps IDE/Chat in the main window');
    assert.equal((await evaluate(socket,`window.lca.configureDesktopLola(${JSON.stringify({...lola.settings,enabled:true,mode:'desktop'})})`)).ok,true);
    companionSocket=await connectPage(port,child,true);
    let speech;
    for(let attempt=0;attempt<100;attempt++) {
      speech=await evaluate(socket,'window.lca.voiceStatus()');
      if(speech.sequence>0&&['idle','error'].includes(speech.state))break;
      await delay(100);
    }
    assert.ok(speech.sequence>0,'Companion must request the real system voice catalog');
    assert.ok(['idle','error'].includes(speech.state),'Voice catalog must not remain busy');
    if(process.env.LCA_EXPECT_SYSTEM_VOICE==='1') {
      assert.equal(speech.state,'idle',speech.error);
      assert.ok(speech.voices.length>0,'Expected an installed system voice');
    }
    assert.equal(await evaluate(companionSocket,`!!document.querySelector('[aria-label="Говорить с Лолой"]')`),true);
    companionSocket.close();companionSocket=undefined;
    assert.equal((await evaluate(socket,`window.lca.configureDesktopLola(${JSON.stringify(lola.settings)})`)).ok,true);
    if (first) await verifyPackagedIde({ desktop: expression => evaluate(socket, expression), directory, modelUrl });
    await evaluate(socket, 'setTimeout(() => window.close(), 50); true');
    socket.close();
    socket = undefined;
    const code = await Promise.race([exited, delay(25_000).then(() => 'timeout')]);
    assert.equal(code, 0, stderr);
  } finally {
    companionSocket?.close();
    socket?.close();
    if (child.exitCode === null) child.kill();
    await exited;
  }
}

async function main() {
  const executable = await resolvePackagedExecutable({ repoRoot: path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..'), explicitPath: process.argv[2] });
  const directory = await fs.mkdtemp(path.join(os.tmpdir(), 'localagent-package-'));
  const legacyFolder=path.join(directory,'LocalCodingAgent','chats');await fs.mkdir(legacyFolder,{recursive:true});
  const originalChats=[];
  for(const [id,mode] of [['1'.repeat(32),'chat'],['2'.repeat(32),'voice']]){
    const content=JSON.stringify({id,title:'Packaged legacy '+mode,mode,project_id:'',project_root:'',model:'fixture',created_at:'2026',updated_at:'2026',messages:[{role:'user',content:'Сохранить разговор'},{role:'assistant',content:'История сохранена.'}]});
    await fs.writeFile(path.join(legacyFolder,id+'.json'),content);originalChats.push([id,content]);
  }
  const model = http.createServer((request, response) => {
    let raw = '';
    request.on('data', chunk => { raw += chunk; });
    request.on('end', () => {
      const body = raw ? JSON.parse(raw) : {};
      if (body.stream) {
        const written = (body.messages || []).some(m => m.role === 'tool' && m.tool_call_id === 'packaged-write');
        const delta = written ? { content: 'Значение равно двум.' } : { tool_calls: [{ index: 0, id: 'packaged-write', type: 'function', function: { name: 'write_file', arguments: JSON.stringify({ path: 'main.ts', content: 'export const value = 2;\n', overwrite: true }) } }] };
        response.writeHead(200, { 'Content-Type': 'text/event-stream' });
        response.end('data: ' + JSON.stringify({ choices: [{ delta, finish_reason: written ? 'stop' : 'tool_calls' }] }) + '\n\ndata: [DONE]\n\n');
      } else {
        response.writeHead(200, { 'Content-Type': 'application/json' });
        response.end(JSON.stringify(request.method === 'POST' ? { choices: [{ message: { content: 'Probe OK' } }] } : { data: [{ id: 'packaged-smoke' }] }));
      }
    });
  });
  await new Promise(resolve => model.listen(0, '127.0.0.1', resolve));
  const modelUrl = `http://127.0.0.1:${model.address().port}/v1`;
  try {
    await run(executable, directory, true, modelUrl);
    await run(executable, directory, false, modelUrl);
    for(const [id,content] of originalChats)assert.equal(await fs.readFile(path.join(legacyFolder,id+'.json'),'utf8'),content);
    const preferences = await fs.readFile(path.join(directory, 'LocalCodingAgent/model-preferences.json'), 'utf8');
    assert.ok(!preferences.includes('packaging-test-secret'));
    assert.ok(!(await fs.readFile(path.join(directory,'LocalCodingAgent/connections.json'),'utf8')).includes('packaged-role-secret'));
    const log = await fs.readFile(path.join(directory, 'profile/logs/main.log'), 'utf8');
    assert.ok(log.includes('packaged=true') && log.includes('app:quit'));
    assert.ok(!log.includes('packaging-test-secret'));
    console.log(JSON.stringify({ status: 'passed', executable, directory, checks: ['sqlite-bundled-core','legacy-chat-voice-migration','original-json-preserved','storage-integrity','optional-ide-defaults-and-restart','desktop-lola-opt-in-and-restart', 'stripped-PATH', 'file-renderer', 'discovery', 'restart-preferences', 'clean-exit', 'no-secret-in-preferences-or-log','system-voice-catalog-no-audio','explicit-microphone-control'] }));
  } finally {
    await new Promise(resolve => model.close(resolve));
  }
}

main().catch(error => { console.error(error); process.exitCode = 1; });
