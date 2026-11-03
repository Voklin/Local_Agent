const { app, BrowserWindow, session, ipcMain } = require('electron');
const path = require('node:path');
const fs = require('node:fs');
const assert = require('node:assert/strict');
const automated = process.argv.includes('--capture') || process.argv.includes('--verify');
const local = path.join(__dirname, '.local', automated ? 'verification-profile' : 'profile');
fs.mkdirSync(local, { recursive: true });
app.setPath('userData', local);
app.setPath('sessionData', path.join(local, 'session'));
app.disableHardwareAcceleration();
let win, lolaWindow;
function openLola(){
 if(lolaWindow&&!lolaWindow.isDestroyed()){lolaWindow.show();lolaWindow.focus();return lolaWindow;}
 lolaWindow=new BrowserWindow({width:360,height:560,minWidth:320,minHeight:460,title:'Лола · прототип',show:!automated,backgroundColor:'#171c26',webPreferences:{contextIsolation:true,sandbox:true,nodeIntegration:false}});
 lolaWindow.setMenuBarVisibility(false);
 lolaWindow.loadFile(path.join(__dirname,'lola.html'));
 lolaWindow.webContents.setWindowOpenHandler(()=>({action:'deny'}));
 lolaWindow.on('closed',()=>{lolaWindow=null;});
 return lolaWindow;
}
ipcMain.handle('prototype:open-lola',event=>{if(event.sender!==win?.webContents)return false;openLola();return true;});
const delay = ms => new Promise(resolve => setTimeout(resolve, ms));
app.whenReady().then(async () => {
  session.defaultSession.webRequest.onBeforeRequest((details, done) => {
    done({ cancel: !details.url.startsWith('file:') && !details.url.startsWith('devtools:') && !details.url.startsWith('data:') });
  });
  win = new BrowserWindow({ width: 1440, height: 940, minWidth: 960, minHeight: 640,
    title: 'Neutral · Interface prototype', backgroundColor: '#111115', show: !automated,
    webPreferences: { preload:path.join(__dirname,'preload.cjs'),nodeIntegration: false, contextIsolation: true, sandbox: true, spellcheck: false },
  });
  win.setMenuBarVisibility(false);
  win.webContents.setWindowOpenHandler(() => ({ action: 'deny' }));
  win.webContents.on('will-navigate', event => event.preventDefault());
  await win.loadFile(path.join(__dirname, 'index.html'));
  if (automated) {
    const out = path.join(__dirname, 'artifacts'); fs.mkdirSync(out, { recursive: true });
    const js = async code => {try{return await win.webContents.executeJavaScript(code, true);}catch(error){throw Error(String(error)+'\nScript: '+code);}};
    const click = selector => js(`document.querySelector(${JSON.stringify(selector)}).click()`);
    const input = (selector, value) => js(`{ const n=document.querySelector(${JSON.stringify(selector)}); n.value=${JSON.stringify(value)}; n.dispatchEvent(new Event('input',{bubbles:true})); }`);
    const frames = () => js('new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))');
    const capture = async name => {
      await frames(); await delay(100);
      fs.writeFileSync(path.join(out, name + '.png'), (await win.webContents.capturePage(undefined, { stayHidden: true })).toPNG());
    };
    const verifyLayout = async label => {
      const layout = await js(`(() => {
        const selectors=['.topbar','.sidebar','.workspace','.composer','.statusbar'];
        const rects=Object.fromEntries(selectors.map(s=>[s,document.querySelector(s)?.getBoundingClientRect().toJSON()]));
        const problems=[];
        for(const [s,r] of Object.entries(rects)) if(!r||r.left<-.5||r.top<-.5||r.right>innerWidth+.5||r.bottom>innerHeight+.5) problems.push(s);
        return {width:innerWidth,height:innerHeight,overflow:document.documentElement.scrollWidth>innerWidth,rects,problems};
      })()`);
      assert.equal(layout.overflow, false, label + ': horizontal document overflow');
      assert.deepEqual(layout.problems, [], label + ': critical controls outside viewport');
      return { label, ...layout };
    };
    const layouts=[];
    try {
      if(process.argv.includes('--review-only')){
        const result=await require('./verify-review.cjs')({win,js,click,input,capture,delay});
        fs.writeFileSync(path.join(out,'review-verification.json'),JSON.stringify(result,null,2));
        console.log('Prototype review scenarios passed');app.exit(0);return;
      }
      await js('localStorage.clear(); window.prototype.reset();window.prototype.resetLayout()');
      for (const [width,height] of [[1280,720],[1440,900],[1920,1080]]) {
        win.setContentSize(width,height); await delay(120);
        for (const mode of ['ide','chat']) {
          for (const scenario of ['ready','working','tools','changes','error','empty','settings']) {
            await js(`window.prototype.setMode(${JSON.stringify(mode)}); window.prototype.setScenario(${JSON.stringify(scenario)})`);
            if (scenario === 'tools') await click('[data-tool="read"]');
            if (scenario === 'changes') await js("document.querySelector('.review-card').scrollIntoView({block:'nearest'})");
            if (scenario === 'error') await js("document.querySelector('[role=alert]').scrollIntoView({block:'nearest'})");
            layouts.push(await verifyLayout(`${mode}-${scenario}-${width}x${height}`));
            await capture(`${mode}-${scenario}-${width}x${height}`);
          }
          await js(`window.prototype.setMode(${JSON.stringify(mode)}); window.prototype.setScenario('ready')`);
          await capture(`${mode}-${width}x${height}`);
          await js("document.querySelector('[data-resize=sidebar]').dispatchEvent(new KeyboardEvent('keydown',{key:'ArrowRight',bubbles:true}))");
          await js(`document.querySelector('[data-resize=${mode==='ide'?'agent':'context'}]').dispatchEvent(new KeyboardEvent('keydown',{key:'ArrowLeft',bubbles:true}))`);
          layouts.push(await verifyLayout(`${mode}-resized-${width}x${height}`));
          await capture(`${mode}-resized-${width}x${height}`);
          await js('window.prototype.resetLayout()');
        }
      }
      win.setContentSize(1440,900); await delay(100);
      await js("window.prototype.setMode('ide');window.prototype.setScenario('working')");
      await capture('ide-working');
      await js("window.prototype.setScenario('tools')");
      await click('[data-tool="read"]');
      assert.equal(await js("document.querySelector('[data-tool-detail=read]').hidden"), false);
      await capture('ide-tools');
      await js("window.prototype.setScenario('file')");
      const original = await js("document.querySelector('#code-input').value");
      await input('#code-input', original + '\n// local prototype draft');
      assert.equal(await js("document.querySelector('[data-action=save-file]').disabled"), false);
      await click('[data-action=save-file]');
      await click('[data-review=dialog-confirm]');
      assert.equal(await js("document.querySelector('[data-action=save-file]').disabled"), true);
      await capture('ide-file');
      await js("window.prototype.setScenario('error')");
      assert.equal(await js("document.querySelector('[role=alert]').textContent.includes('Демонстрационная ошибка')"), true);
      await capture('ide-error');
      await js("window.prototype.setScenario('settings')");
      assert.equal(await js("document.activeElement.id"), 'settings-title');
      await capture('settings');
      await click('[data-action=close-settings]');
      await js("window.prototype.setMode('chat');window.prototype.setScenario('empty')");
      await capture('chat-empty');
      await input('#prompt','Проверка локального сценария');
      await click('[data-action=send]');
      assert.equal(await js("document.querySelector('[data-action=stop]')!==null"), true);
      await click('[data-action=stop]');
      assert.equal(await js("document.querySelector('[data-action=send]')!==null"), true);
      assert.equal(await js("document.body.innerText.includes('Сценарий остановлен')"), true);
      await js("window.prototype.setScenario('ready')");
      await input('#conversation-search','ничего-не-найдено');
      assert.equal(await js("document.querySelectorAll('.conversation-row').length"), 0);
      await input('#conversation-search','');
      await click('[data-action=toggle-context]');
      assert.equal(await js("document.querySelector('.context-inspector')===null"),true);
      await click('[data-action=toggle-context]');
      assert.equal(await js("document.querySelector('.context-inspector')!==null"),true);
      await capture('chat-context');
      await click('[data-action=toggle-details]');
      await click('[data-inspect=plan]');
      assert.equal(await js("document.body.innerText.includes('План задачи')"),true);
      await click('[data-inspect=changes]');
      assert.equal(await js("document.querySelector('[data-decision=apply]')!==null"),true);
      await click('[data-decision=apply]');
      assert.equal(await js("document.body.innerText.includes('Демо принято')"),true);
      await capture('chat-review');
      await click('.task-drawer [data-action=toggle-details]');
      await input('#prompt','Сохранить черновик');
      await click('[data-tool=read]');
      assert.equal(await js("document.querySelector('#prompt').value"),'Сохранить черновик');
      await js("window.prototype.setMode('ide')");
      await click('[data-side-view=project-search]');
      await input('#project-query','styles');
      assert.equal(await js("document.querySelectorAll('.project-search [data-file]').length"),1);
      await capture('ide-project-search');
      await click('[data-side-view=memory]');
      await input('#memory-note','Память прототипа');
      await click('[data-side-view=files]');
      await click('[data-side-view=memory]');
      assert.equal(await js("document.querySelector('#memory-note').value"),'Память прототипа');
      await capture('ide-memory');
      await click('[data-side-view=files]');
      await click('[data-action=toggle-context]');
      assert.equal(await js("document.querySelector('.agent-panel')===null"),true);
      await click('[data-action=toggle-context]');
      assert.equal(await js("document.querySelector('.agent-panel')!==null"),true);
      await js("window.prototype.setScenario('settings')");
      await js("document.dispatchEvent(new KeyboardEvent('keydown',{key:'b',ctrlKey:true,bubbles:true}))");
      assert.equal(await js("document.querySelector('.sidebar')!==null"),true);
      await click('[data-settings-tab=tools]');
      assert.equal(await js("!!document.querySelector('[data-review=settings-sub-mcp]')&&!!document.querySelector('[data-review=settings-sub-agents]')"),true);
      await capture('settings-tools');
      await click('[data-action=close-settings]');
      assert.equal(await js("document.activeElement.getAttribute('data-action')"),'settings');
      await js("window.prototype.reset();window.prototype.resetLayout()");
      const leftWidth=await js("document.querySelector('.sidebar').getBoundingClientRect().width");
      const handle=await js("document.querySelector('[data-resize=sidebar]').getBoundingClientRect().toJSON()");
      win.webContents.sendInputEvent({type:'mouseMove',x:Math.round(handle.x+3),y:180});
      win.webContents.sendInputEvent({type:'mouseDown',x:Math.round(handle.x+3),y:180,button:'left',clickCount:1});
      win.webContents.sendInputEvent({type:'mouseMove',x:Math.round(handle.x+63),y:180});
      win.webContents.sendInputEvent({type:'mouseUp',x:Math.round(handle.x+63),y:180,button:'left',clickCount:1});
      await delay(120);
      assert.ok((await js("document.querySelector('.sidebar').getBoundingClientRect().width"))>leftWidth+40,'pointer resize expands sidebar');
      await js("document.querySelector('[data-resize=agent]').dispatchEvent(new KeyboardEvent('keydown',{key:'ArrowLeft',bubbles:true}))");
      const savedWidth=await js("document.querySelector('.agent-panel').getBoundingClientRect().width");
      await win.webContents.reload();await delay(450);
      assert.equal(await js("document.querySelector('.agent-panel').getBoundingClientRect().width"),savedWidth);
      await js("window.prototype.setScenario('changes')");
      await js("document.querySelector('.task-drawer [data-resize]').dispatchEvent(new KeyboardEvent('keydown',{key:'ArrowLeft',bubbles:true}))");
      await capture('ide-resized-details');
      await js("window.prototype.setScenario('error')");
      await click('[data-action=retry-demo]');
      assert.equal(await js("document.querySelector('[role=alert]')===null && document.querySelector('[data-action=stop]')!==null"),true);
      await js("window.prototype.setScenario('settings')");
      await input('#settings-query','нет-такого-раздела');
      assert.equal(await js("document.querySelector('.settings-no-results')!==null"),true);
      await input('#settings-query','');
      await js("document.querySelector('[data-resize=settings]').dispatchEvent(new KeyboardEvent('keydown',{key:'ArrowRight',bubbles:true}))");
      await capture('settings-resized');
      await js("window.prototype.reset();window.prototype.resetLayout()");
      assert.equal(await js("document.querySelector('[class*=ascii]')===null"),true);
      await js("{const n=document.querySelector('#model-select');n.value='API Demo';n.dispatchEvent(new Event('change',{bubbles:true}));}");
      await js("window.prototype.setMode('chat')");
      assert.equal(await js("document.querySelector('#model-select').value"),'API Demo');
      await click('[data-action=open-lola]');
      for(let i=0;i<50&&(!lolaWindow||lolaWindow.webContents.isLoading());i++)await delay(100);
      assert.ok(lolaWindow&&!lolaWindow.isDestroyed(),'Lola window opens');
      await delay(250);
      fs.writeFileSync(path.join(out,'lola-window.png'),(await lolaWindow.webContents.capturePage(undefined,{stayHidden:true})).toPNG());
      await lolaWindow.webContents.executeJavaScript("document.querySelector('#lola-prompt').value='Привет';document.querySelector('#lola-form').requestSubmit()");
      assert.ok((await lolaWindow.webContents.executeJavaScript("document.querySelector('#reply').textContent")).includes('Привет'));
      lolaWindow.close();
      const reviewResult=await require('./verify-review.cjs')({win,js,click,input,capture,delay});
      fs.writeFileSync(path.join(out,'review-verification.json'),JSON.stringify(reviewResult,null,2));
      await js("window.prototype.reset()");
      fs.writeFileSync(path.join(out,'verification.json'),JSON.stringify({ok:true,layouts,checks:['isolated Electron profile','no network access','42 viewport/mode/state layouts plus 6 resized layouts','tool expansion','editable local file','save draft','demo error','settings focus','empty state','send and stop','history filter','context inspector','prompt retained across tool expansion','IDE panel toggle','modal shortcut guard and focus return','plan and demonstration review decisions','project search and memory draft','settings categories','ASCII removed','model picker persists between modes','separate Lola window and local form','pointer and keyboard resizing','width persistence after reload','error retry and empty settings search']},null,2));
      console.log('Neutral prototype verified. Screenshots: ' + out);
      app.exit(0);
    } catch (error) {
      console.error(error.stack);
      try { await capture('failure'); fs.writeFileSync(path.join(out,'failure-dom.txt'),await js('document.body.innerText')); } catch {}
      fs.writeFileSync(path.join(out,'verification.json'),JSON.stringify({ok:false,error:error.stack,layouts},null,2));
      app.exit(1);
    }
  }
});
app.on('window-all-closed', () => app.quit());
