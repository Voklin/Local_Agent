// Test the actual Windows package using temporary data and loopback CDP.
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import http from 'node:http';
import { spawn } from 'node:child_process';
import { setTimeout as delay } from 'node:timers/promises';

async function freePort() {
  const server = http.createServer();
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  const port = server.address().port;
  await new Promise(resolve => server.close(resolve));
  return port;
}

async function connectPage(port, child) {
  const deadline = Date.now() + 30_000;
  while (Date.now() < deadline && child.exitCode === null) {
    try {
      const pages = await (await fetch(`http://127.0.0.1:${port}/json/list`, { signal: AbortSignal.timeout(1000) })).json();
      const page = pages.find(item => item.type === 'page' && item.url.startsWith('file:'));
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
    const timer = setTimeout(() => reject(new Error('CDP evaluation timed out')), 15_000);
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
    LCA_PYTHON: 'Z:\\missing-python.exe', PYTHONHOME: 'Z:\\missing-home', PYTHONPATH: 'Z:\\missing-modules' };
  delete env.ELECTRON_RUN_AS_NODE;
  const child = spawn(executable, [`--user-data-dir=${path.join(directory, 'profile')}`, '--remote-debugging-address=127.0.0.1', `--remote-debugging-port=${port}`],
    { cwd: directory, env, windowsHide: true, stdio: ['ignore', 'ignore', 'pipe'] });
  let stderr = '';
  child.stderr.on('data', chunk => { stderr = (stderr + chunk).slice(-8000); });
  const exited = new Promise(resolve => child.once('exit', resolve));
  let socket;
  try {
    socket = await connectPage(port, child);
    let health;
    for (let attempt = 0; attempt < 50; attempt++) {
      health = await evaluate(socket, 'window.lca ? window.lca.health() : null');
      if (health?.ok) break;
      await delay(100);
    }
    assert.equal(health?.service, 'python-core-bridge', stderr);
    assert.equal(await evaluate(socket, 'typeof require'), 'undefined');
    if (first) {
      const config = { base_url: modelUrl, model: 'packaged-smoke', api_key: 'packaging-test-secret' };
      assert.equal((await evaluate(socket, `window.lca.configureModel(${JSON.stringify(config)})`)).ok, true);
    }
    assert.equal((await evaluate(socket, 'window.lca.getModelSettings()')).model, 'packaged-smoke');
    assert.deepEqual((await evaluate(socket, 'window.lca.listModels()')).models, ['packaged-smoke']);
    await evaluate(socket, 'setTimeout(() => window.close(), 50); true');
    const code = await Promise.race([exited, delay(10_000).then(() => 'timeout')]);
    assert.equal(code, 0, stderr);
  } finally {
    socket?.close();
    if (child.exitCode === null) child.kill();
    await exited;
  }
}

async function main() {
  const executable = path.resolve(process.argv[2] || 'artifacts/windows/win-unpacked/LocalAgent.exe');
  await fs.access(executable);
  const directory = await fs.mkdtemp(path.join(os.tmpdir(), 'localagent-package-'));
  const model = http.createServer((_request, response) => {
    response.writeHead(200, { 'Content-Type': 'application/json' });
    response.end(JSON.stringify({ data: [{ id: 'packaged-smoke' }] }));
  });
  await new Promise(resolve => model.listen(0, '127.0.0.1', resolve));
  const modelUrl = `http://127.0.0.1:${model.address().port}/v1`;
  try {
    await run(executable, directory, true, modelUrl);
    await run(executable, directory, false, modelUrl);
    const preferences = await fs.readFile(path.join(directory, 'LocalCodingAgent/model-preferences.json'), 'utf8');
    assert.ok(!preferences.includes('packaging-test-secret'));
    const log = await fs.readFile(path.join(directory, 'profile/logs/main.log'), 'utf8');
    assert.ok(log.includes('packaged=true') && log.includes('app:quit'));
    assert.ok(!log.includes('packaging-test-secret'));
    console.log(JSON.stringify({ status: 'passed', executable, directory, checks: ['bundled-core', 'stripped-PATH', 'file-renderer', 'discovery', 'restart-preferences', 'clean-exit', 'no-secret-in-preferences-or-log'] }));
  } finally {
    await new Promise(resolve => model.close(resolve));
  }
}

main().catch(error => { console.error(error); process.exitCode = 1; });
