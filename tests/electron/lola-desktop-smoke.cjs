// Native tray/transparent-window test with one Core and one synthetic voice session.
const {app,BrowserWindow,dialog,ipcMain}=require('electron');
const fs=require('node:fs'),path=require('node:path'),http=require('node:http'),assert=require('node:assert/strict');
app.disableHardwareAcceleration();
const root=path.resolve(__dirname,'../..'),output=path.join(root,'.test-data/lola-gui');fs.mkdirSync(output,{recursive:true});
const data=fs.mkdtempSync(path.join(output,'profile-'));process.env.LOCALAPPDATA=data;process.env.LCA_PYTHON=process.env.LCA_TEST_PYTHON||path.join(root,'.venv-test/Scripts/python.exe');app.setPath('userData',path.join(data,'electron'));
let mainShowCalls=0;BrowserWindow.prototype.show=function(){mainShowCalls++;};const nativeShowInactive=BrowserWindow.prototype.showInactive;BrowserWindow.prototype.showInactive=function(){this.setOpacity(.01);return nativeShowInactive.call(this);};
BrowserWindow.prototype.loadURL=function(url){return this.loadFile(path.join(root,'apps/desktop/dist',url.includes('/lola.html')?'lola.html':'index.html'));};
dialog.showMessageBox=async()=>({response:1});
const handlers=new Map(),register=ipcMain.handle.bind(ipcMain);ipcMain.handle=(name,handler)=>{handlers.set(name,handler);register(name,handler);};
const ignoreMouse=new Map(),setIgnore=BrowserWindow.prototype.setIgnoreMouseEvents;BrowserWindow.prototype.setIgnoreMouseEvents=function(value,options){ignoreMouse.set(this.id,value);return setIgnore.call(this,value,options);};
let mainWindow,widget,finished=false,requests=[],coreStarts=0;
const childProcess=require('node:child_process'),originalSpawn=childProcess.spawn;childProcess.spawn=(file,...args)=>{if(String(file).toLowerCase().includes('python'))coreStarts++;return originalSpawn(file,...args);};
const fixture=http.createServer((req,res)=>{let raw='';req.on('data',v=>raw+=v);req.on('end',()=>{if(req.method==='GET'){res.writeHead(404);res.end();return;}const body=JSON.parse(raw);requests.push(body);if(body.stream){res.writeHead(200,{'Content-Type':'text/event-stream'});res.end('data: '+JSON.stringify({choices:[{index:0,delta:{content:'Привет! Я Лола, я рядом.'},finish_reason:'stop'}]})+'\n\ndata: [DONE]\n\n');}else{res.writeHead(200,{'Content-Type':'application/json'});res.end(JSON.stringify({choices:[{message:{content:'{}'},finish_reason:'stop'}]}));}});});
async function js(win,code){return win.webContents.executeJavaScript(code,true);}
async function poll(win,expression,timeout=15000){const end=Date.now()+timeout;while(Date.now()<end){if(await js(win,expression))return;await new Promise(r=>setTimeout(r,70));}throw Error('Timeout: '+expression);}
async function input(win,selector,text){await js(win,`{const n=document.querySelector(${JSON.stringify(selector)});Object.getOwnPropertyDescriptor(n.tagName==='TEXTAREA'?HTMLTextAreaElement.prototype:HTMLInputElement.prototype,'value').set.call(n,${JSON.stringify(text)});n.dispatchEvent(new Event('input',{bubbles:true}));}`);await new Promise(r=>setTimeout(r,60));}
async function capture(name){await js(widget,'new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))');fs.writeFileSync(path.join(output,name+'.png'),(await widget.webContents.capturePage(undefined,{stayHidden:true})).toPNG());}
async function finish(error){if(finished)return;finished=true;if(error){try{if(widget){await capture('failure');fs.writeFileSync(path.join(output,'failure-layout.json'),JSON.stringify({bounds:widget.getBounds(),zoom:widget.webContents.getZoomFactor(),layout:await js(widget,"({width:innerWidth,height:innerHeight,rects:Object.fromEntries(['.desktop-lola','.lola-bubble','.lola-drag-character','.miya-scene','.miya-character','.lola-sprite'].map(s=>[s,document.querySelector(s).getBoundingClientRect().toJSON()]))})")},null,2));}fs.writeFileSync(path.join(output,'failure.txt'),await js(mainWindow,'document.body.innerText'));}catch{}}
  fs.writeFileSync(path.join(output,'result.json'),JSON.stringify({ok:!error,error:error?.stack||null,requests:requests.length,coreStarts,data},null,2));console.log(error?error.stack:'Lola desktop passed: native overlay, tray hide, scoped IPC, drag, animation, click-through, hidden-window request, one Core');fixture.close();app.once('will-quit',()=>{if(error)app.exit(1);});app.quit();setTimeout(()=>app.exit(error?1:0),18000).unref();
}
process.on('uncaughtException',finish);process.on('unhandledRejection',finish);
app.on('browser-window-created',(_,window)=>{if(mainWindow){widget=window;return;}mainWindow=window;window.webContents.setBackgroundThrottling(false);window.webContents.once('did-finish-load',async()=>{try{
  await poll(mainWindow,"!!window.lca&&document.querySelector('.status')?.textContent.includes('Готов')");
  const initial=await js(mainWindow,'window.lca.getDesktopLola()');assert.equal(initial.settings.enabled,false);assert.equal(BrowserWindow.getAllWindows().length,1);
  const profile=await js(mainWindow,`window.lca.configureCompanion({base_url:'http://127.0.0.1:${fixture.address().port}/v1',model:'lola-fixture',tts_provider:'windows',auto_speak:false})`);assert.ok(profile.ok);
  const originalMain=await js(mainWindow,"document.querySelector('.chat-messages').textContent");
  await js(mainWindow,"document.querySelector('.lola-open').click()");
  const deadline=Date.now()+10000;while(!widget&&Date.now()<deadline)await new Promise(r=>setTimeout(r,50));assert.ok(widget);await poll(widget,"!!window.lola&&!!document.querySelector('.lola-sprite')");
  assert.equal(await js(widget,'typeof window.lca.startTask'),'function');await new Promise(r=>setTimeout(r,250));widget.setOpacity(.01);assert.equal(widget.isAlwaysOnTop(),true);assert.equal(await js(widget,"getComputedStyle(document.body).backgroundColor"),'rgba(0, 0, 0, 0)');
  for(const theme of ['forest','parchment','twilight']){await js(mainWindow,`window.lca.setAppearanceTheme('${theme}')`);await poll(widget,`document.documentElement.dataset.leshyTheme==='${theme}'`);assert.equal(await js(widget,"getComputedStyle(document.body).backgroundColor"),'rgba(0, 0, 0, 0)');assert.equal(await js(widget,"getComputedStyle(document.documentElement).backgroundColor"),'rgba(0, 0, 0, 0)');assert.notEqual(await js(widget,"getComputedStyle(document.querySelector('.lola-bubble')).backgroundImage"),'none','Lola receives the shared woven frame');await capture('theme-'+theme);}

  const denied=await handlers.get('task:start')({sender:widget.webContents,senderFrame:widget.webContents.mainFrame},'bad');assert.equal(denied.ok,false);
  const invalid=await handlers.get('lola-widget:action')({sender:widget.webContents,senderFrame:widget.webContents.mainFrame},{action:'execute_shell',text:'bad'});assert.equal(invalid.ok,false);
  mainWindow.close();await new Promise(r=>setTimeout(r,100));assert.equal(mainWindow.isDestroyed(),false);assert.equal(mainWindow.isVisible(),false);
  await js(widget,"document.querySelector('[aria-label=\"Вопрос и ответ Лолы\"]').click()");await input(widget,'[aria-label="Вопрос настольной Лоле"]','Привет');await js(widget,"document.querySelector('form').dispatchEvent(new Event('submit',{bubbles:true,cancelable:true}))");
  await poll(widget,"document.querySelector('.lola-conversation')?.textContent.includes('Привет! Я Лола')&&!document.querySelector('.desktop-lola').querySelector('form input').disabled");assert.equal(mainWindow.isVisible(),false);assert.equal(coreStarts,1);assert.equal(requests.filter(r=>r.stream).length,1);
  await js(mainWindow,"window.__mic=false;window.addEventListener('manual-microphone',e=>window.__mic=e.detail)");await js(widget,'window.lca.lolaMicrophone(true)');await poll(mainWindow,'window.__mic===true');await js(widget,'window.lca.lolaMicrophone(false)');await poll(mainWindow,'window.__mic===false');
  await js(widget,"document.querySelector('[aria-label=\"Сразу отправлять распознанный запрос\"]').click()");assert.equal(await js(widget,"localStorage.getItem('miya-auto-send')"),'on');
  const voiceChat=(await js(mainWindow,"window.lca.listChats('voice')")).chats[0].id;
  const seed=[
    'import sys,json',
    'from agent.chat_store import load_chat,save_chat',
    'from agent.task_store import new_task',
    'from agent.tool_recovery import task_journal',
    'chat=load_chat(sys.argv[1]); task=new_task(chat["id"],chat["project_root"],"Проверь прерванное действие")',
    'tool={"id":"popup-recovery","type":"function","function":{"name":"open_application","arguments":json.dumps({"app_id":"fixture"})}}',
    'anchor=len(chat["messages"]); journal=task_journal(task); journal.prepare_batch([tool],anchor); journal.set_phase(anchor,"popup-recovery","started")',
    'chat["messages"].append({"role":"assistant","content":None,"tool_calls":[tool]});chat["task_checkpoint"]=task;save_chat(chat)',
  ].join('\n');
  const seeded=originalSpawn(process.env.LCA_PYTHON,['-c',seed,voiceChat],{cwd:root,env:process.env,stdio:['ignore','pipe','pipe'],windowsHide:true});await new Promise((resolve,reject)=>{let error='';seeded.stderr.on('data',part=>error+=part);seeded.on('exit',code=>code===0?resolve():reject(Error(error)));seeded.on('error',reject)});
  await js(mainWindow,'window.lca.openLola('+JSON.stringify(voiceChat)+')');await poll(widget,"!!document.querySelector('.task-recovery')");assert.equal(await js(widget,"document.querySelector('.task-progress>button.task-resume').disabled"),true);
  await js(widget,"Array.from(document.querySelectorAll('.task-recovery button')).find(b=>b.textContent==='Действие не выполнялось').click()");await js(widget,"Array.from(document.querySelectorAll('.task-recovery button')).find(b=>b.textContent==='Подтвердить результат').click()");await poll(widget,"!document.querySelector('.task-recovery')");assert.equal(requests.filter(r=>r.stream).length,1,'Recovery review must not replay the action');
  const avatarBounds=await js(widget,"(()=>{const r=document.querySelector('.lola-drag-character').getBoundingClientRect();return {bottom:r.bottom,height:innerHeight}})()");assert.ok(avatarBounds.bottom<=avatarBounds.height,'Full-body avatar must stay inside companion window');await capture('answer');
  assert.equal(await js(mainWindow,"document.querySelector('.chat-messages').textContent"),originalMain,'Popup conversation must not replace the main session');
  assert.equal(await js(mainWindow,"document.querySelectorAll('.mode-tabs [role=tab]').length"),2);
  assert.equal(await js(mainWindow,"!!document.querySelector('.voice-panel')"),false);
  const forbiddenModel=await handlers.get('model:configure')({sender:widget.webContents,senderFrame:widget.webContents.mainFrame},{base_url:'http://example.invalid',model:'bad'});assert.equal(forbiddenModel.ok,false);
  const forbiddenApproval=await handlers.get('task:approve')({sender:widget.webContents,senderFrame:widget.webContents.mainFrame},'unrelated-run','approval','apply');assert.equal(forbiddenApproval.ok,false);
  const forbiddenProject=await handlers.get('workspace:select')({sender:widget.webContents,senderFrame:widget.webContents.mainFrame},{id:''});assert.equal(forbiddenProject.ok,false);
  await new Promise(r=>setTimeout(r,150));
  await js(mainWindow,"window.lca.presentDesktopLola({state:'speaking',caption:'Говорю',reply:'Готова помочь',busy:false,recording:false,wake:false})");await poll(widget,"document.querySelector('.desktop-lola').dataset.state==='speaking'");
  const position=await js(widget,"Array.from(document.querySelectorAll('.lola-frame')).map(n=>getComputedStyle(n).opacity).join(',')");await new Promise(r=>setTimeout(r,200));assert.notEqual(await js(widget,"Array.from(document.querySelectorAll('.lola-frame')).map(n=>getComputedStyle(n).opacity).join(',')"),position);await capture('speaking');
  for(const state of ['idle','listening','thinking','working','speaking','success','error']){
    await js(mainWindow,`window.lca.presentDesktopLola({state:${JSON.stringify(state)},caption:'Проверка',reply:'Ответ '.repeat(200),busy:false,recording:false,wake:false})`);await poll(widget,`document.querySelector('.desktop-lola').dataset.state===${JSON.stringify(state)}`);
    for(const [width,height,zoom] of [[324,500,1],[300,300,1],[300,300,1.5]]){
      widget.setBounds({width,height});widget.webContents.setZoomFactor(zoom);await new Promise(r=>setTimeout(r,100));
      const nativeBounds=widget.getBounds();assert.equal(nativeBounds.width,width);assert.equal(nativeBounds.height,height);
      assert.ok(await js(widget,"(()=>{const svg=document.querySelector('.lola-sprite'),r=svg.getBoundingClientRect(),m=svg.getScreenCTM();return r.top>=0&&r.bottom<=innerHeight+.1&&r.left>=0&&r.right<=innerWidth+.1&&Array.from(svg.children).every(n=>{const a=new DOMPoint(n.x.baseVal.value,n.y.baseVal.value).matrixTransform(m),b=new DOMPoint(n.x.baseVal.value+n.width.baseVal.value,n.y.baseVal.value+n.height.baseVal.value).matrixTransform(m);return a.x>=0&&a.y>=0&&b.x<=innerWidth+.1&&b.y<=innerHeight+.1})&&getComputedStyle(document.querySelector('.lola-drag-character')).clipPath==='none'&&getComputedStyle(svg).clipPath==='none'})()"),`Complete ${state} character must fit ${width}x${height} at zoom ${zoom}`);
    }
  }
  await capture('small-window-150-percent');widget.webContents.setZoomFactor(1);
  const start=widget.getPosition();await js(widget,'window.lola.move(-40,-30)');assert.notDeepEqual(widget.getPosition(),start);
  let settings=(await js(mainWindow,'window.lca.getDesktopLola()')).settings;
  await js(mainWindow,`window.lca.configureDesktopLola(${JSON.stringify({...settings,clickThrough:true})})`);assert.equal(ignoreMouse.get(widget.id),true);
  await js(mainWindow,`window.lca.configureDesktopLola(${JSON.stringify({...settings,clickThrough:false,animate:false,mode:'desktop'})})`);assert.equal(widget.isAlwaysOnTop(),false);await poll(widget,"getComputedStyle(document.querySelector('.lola-frame')).animationName==='none'");
  await js(mainWindow,`window.lca.configureDesktopLola(${JSON.stringify({...settings,mode:'tray'})})`);assert.equal(widget.isVisible(),false);assert.equal((await js(mainWindow,'window.lca.getDesktopLola()')).settings.mode,'tray');
  settings=(await js(mainWindow,'window.lca.getDesktopLola()')).settings;
  await js(mainWindow,`window.lca.configureDesktopLola(${JSON.stringify({...settings,mode:'desktop'})})`);
  const showsBeforeSettings=mainShowCalls;
  const opened=await handlers.get('lola-widget:action')({sender:widget.webContents,senderFrame:widget.webContents.mainFrame},{action:'settings'});
  assert.equal(opened.ok,true);assert.ok(mainShowCalls>showsBeforeSettings,'Settings action must request the main window to show');await poll(mainWindow,"!!document.querySelector('.settings-dialog')");
  assert.equal(await js(mainWindow,"document.querySelector('.settings-tabs button[aria-pressed=true]')?.textContent"),'Голос и Лола');
  await js(mainWindow,"document.querySelector('.settings-dialog [title=\"Закрыть настройки\"]').click()");await poll(mainWindow,"!document.querySelector('.settings-dialog')");
  settings=(await js(mainWindow,'window.lca.getDesktopLola()')).settings;
  await js(mainWindow,`window.lca.configureDesktopLola(${JSON.stringify({...settings,enabled:false})})`);assert.equal(widget.isDestroyed(),true);assert.equal(BrowserWindow.getAllWindows().length,1);assert.equal(JSON.parse(fs.readFileSync(path.join(data,'electron/lola-desktop.json'),'utf8')).enabled,false);
  await finish();
}catch(error){await finish(error);}});});
fixture.listen(0,'127.0.0.1',()=>require('../../apps/desktop/dist-electron/main.cjs'));
