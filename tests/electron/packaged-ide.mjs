import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { setTimeout as delay } from 'node:timers/promises';

async function until(action, label) {
  const deadline = Date.now() + 45_000;
  let last;
  while (Date.now() < deadline) {
    try { const value = await action(); if (value) return value; } catch (error) { last = error; }
    await delay(100);
  }
  throw new Error(`Packaged IDE timeout: ${label}; ${last?.message || ''}`);
}

export async function verifyPackagedIde({ desktop, directory, modelUrl }) {
  const project = path.join(directory, 'ide-project');
  await fs.mkdir(project, { recursive: true });
  const original = 'export const value = 1;\n';
  await fs.writeFile(path.join(project, 'main.ts'), original);
  const saved = await desktop(`window.lca.saveWorkspace(${JSON.stringify({ name: 'Packaged IDE', root: project })})`);
  assert.equal(saved.ok, true, JSON.stringify(saved));
  assert.equal((await desktop(`window.lca.selectWorkspace({id:${JSON.stringify(saved.project.id)}})`)).ok, true);
  const current = await desktop('window.lca.getModelSettings()');
  assert.equal((await desktop(`window.lca.configureModel(${JSON.stringify({ base_url: modelUrl, model: 'packaged-smoke', api_key: '', api_protocol: 'chat', tool_protocol: 'native', settings: { ...current.settings, memory_updates: 'off' } })})`)).ok, true);
  const launch = await desktop('window.lca.openNeutralIde()');
  assert.equal(launch.ok, true, JSON.stringify(launch));
  assert.ok(Number.isInteger(launch.pid) && launch.pid > 0);
  let socket;
  const pending = new Map(), contexts = [], attached = new Set();
  let serial = 0;
  try {
    const activePort = path.join(directory, 'profile/neutral-ide/user-data/DevToolsActivePort');
    const [port, endpoint] = await until(async () => (await fs.readFile(activePort, 'utf8')).split('\n'), 'CDP port');
    socket = new WebSocket(`ws://127.0.0.1:${port}${endpoint}`);
    await new Promise((resolve, reject) => { socket.onopen = resolve; socket.onerror = reject; });
    socket.onmessage = event => {
      const message = JSON.parse(event.data);
      if (message.method === 'Runtime.executionContextCreated') contexts.push({ session: message.sessionId, id: message.params.context.id });
      const entry = pending.get(message.id);
      if (entry) { pending.delete(message.id); clearTimeout(entry.timer); message.error ? entry.reject(new Error(JSON.stringify(message.error))) : entry.resolve(message.result); }
    };
    const send = (method, params = {}, sessionId) => new Promise((resolve, reject) => {
      const id = ++serial;
      const timer = setTimeout(() => { pending.delete(id); reject(new Error(`CDP timeout: ${method}`)); }, 10_000);
      pending.set(id, { resolve, reject, timer });
      socket.send(JSON.stringify({ id, method, params, ...(sessionId ? { sessionId } : {}) }));
    });
    const evaluate = async (context, expression) => {
      const result = await send('Runtime.evaluate', { expression, contextId: context.id, awaitPromise: true, returnByValue: true }, context.session);
      if (result.exceptionDetails) throw new Error(JSON.stringify(result.exceptionDetails));
      return result.result.value;
    };
    let mainPage;
    const view = await until(async () => {
      for (const target of (await send('Target.getTargets')).targetInfos.filter(t => ['page', 'iframe'].includes(t.type))) {
        if (attached.has(target.targetId)) continue;
        attached.add(target.targetId);
        const { sessionId } = await send('Target.attachToTarget', { targetId: target.targetId, flatten: true });
        await send('Runtime.enable', {}, sessionId);
        if (target.type === 'page' && target.url.includes('workbench')) mainPage = sessionId;
      }
      for (const context of contexts) {
        try { if (await evaluate(context, "window.neutralIdeHost===true && !!document.querySelector('.nw-compose textarea:not(:disabled)')")) return context; } catch { /* Context may belong to native chrome. */ }
      }
    }, 'connected webview');
    const panel = expression => evaluate(view, expression);
    await panel("{const n=document.querySelector('.nw-compose textarea');Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype,'value').set.call(n,'Измени значение main.ts на 2');n.dispatchEvent(new Event('input',{bubbles:true}));}");
    await delay(100);
    await panel("document.querySelector('.nw-send').click()");
    await until(() => panel("!!document.querySelector('.nw-approval')"), 'diff approval');
    assert.equal(await fs.readFile(path.join(project, 'main.ts'), 'utf8'), original, 'No disk write before approval');
    assert.equal(await panel("!!document.querySelector('.nw-diff-add') && !!document.querySelector('.nw-diff-remove')"), true);
    await panel("[...document.querySelectorAll('.nw-approval button')].find(b=>b.textContent.includes('Применить')).click()");
    await until(async () => (await fs.readFile(path.join(project, 'main.ts'), 'utf8')) === 'export const value = 2;\n', 'editor write');
    await until(() => panel("!document.querySelector('.nw-send[aria-label=\"Остановить\"]')"), 'completed run');
    assert.equal((await panel("window.lca.ideOpenFile('main.ts')")).ok, true);
    await delay(500);
    assert.ok(mainPage, 'Native workbench attached');
    for (const [key, code, vk] of [['z', 'KeyZ', 90], ['s', 'KeyS', 83]]) {
      await send('Input.dispatchKeyEvent', { type: 'keyDown', key, code, modifiers: 2, windowsVirtualKeyCode: vk }, mainPage);
      await send('Input.dispatchKeyEvent', { type: 'keyUp', key, code, modifiers: 2, windowsVirtualKeyCode: vk }, mainPage);
      await delay(250);
    }
    await until(async () => (await fs.readFile(path.join(project, 'main.ts'), 'utf8')) === original, 'undo and save');
    assert.equal((await desktop("window.lca.configureExtensions({kind:'groups',id:'commands',enabled:true})")).ok,true);
    await panel("document.querySelector('.nw-checks-trigger').click();document.querySelector('.nw-add-check')?.click()");
    await until(()=>panel("!!document.querySelector('.nw-add-check')"),'packaged checks editor');
    if(!await panel("!!document.querySelector('.nw-check-definition')"))await panel("document.querySelector('.nw-add-check').click()");
    const setCheckField=async(label,value)=>{
      await panel(`{const n=document.querySelector('[aria-label="${label}"]');Object.getOwnPropertyDescriptor(n.tagName==='TEXTAREA'?HTMLTextAreaElement.prototype:HTMLInputElement.prototype,'value').set.call(n,${JSON.stringify(value)});n.dispatchEvent(new Event('input',{bubbles:true}));}`);
      await delay(80);
    };
    await setCheckField('Назначение проверки 1','Bundled Node');await setCheckField('Программа проверки 1','node');
    await setCheckField('Аргументы проверки 1','-e\nif(!process.versions.electron)process.exit(2); console.log("bundled node acceptance OK")');
    await setCheckField('Критерии готовности','Bundled Node is available');
    await panel("{const n=document.querySelector('[aria-label=\"Проверки критерия 1\"]');n.options[0].selected=true;n.dispatchEvent(new Event('change',{bubbles:true}));}");
    await delay(80);await panel("[...document.querySelectorAll('button')].find(n=>n.textContent==='Запустить проверки без модели').click()");
    await until(()=>panel("!!document.querySelector('.nw-approval')"),'bundled Node command approval');
    assert(await panel("document.querySelector('.nw-approval').innerText.includes('bundled node acceptance OK')"));
    await panel("[...document.querySelectorAll('.nw-approval button')].find(n=>n.textContent==='Применить').click()");
    await until(()=>panel("!document.querySelector('.nw-approval') && !document.querySelector('.nw-footer').textContent.includes('Работаю')"),'bundled Node check finished');
    const checkTask=await panel("(async()=>{const chats=await window.lca.listChats('ide');return window.lca.loadChat(chats.chats[0].id,'ide');})()");
    assert.equal(checkTask.task.test_results[0].exit_code,0);assert.equal(checkTask.task.acceptance_evidence[0].status,'checks_passed');assert.equal(checkTask.task.options.checks_only,true);
    const result = { ok: true, project, pid: launch.pid, checks: ['packaged-ide-launch', 'frozen-core-to-webview', 'diff-approval', 'editor-write', 'undo-save','configured-acceptance','bundled-node-stripped-PATH'] };
    await fs.writeFile(path.join(directory, 'packaged-ide-result.json'), JSON.stringify(result, null, 2));
    return result;
  } finally {
    for (const entry of pending.values()) { clearTimeout(entry.timer); entry.reject(new Error('Packaged IDE closed')); }
    socket?.close();
    spawnSync(path.join(process.env.SystemRoot, 'System32/taskkill.exe'), ['/PID', String(launch.pid), '/T', '/F'], { windowsHide: true, stdio: 'ignore' });
  }
}
