// Isolated renderer/main/stdio/agent/MCP integration; never touches the user profile.
const {app,BrowserWindow,dialog,ipcMain}=require('electron');
const fs=require('node:fs'),path=require('node:path'),http=require('node:http'),assert=require('node:assert/strict');
app.disableHardwareAcceleration();
const root=path.resolve(__dirname,'../..'),output=path.join(root,process.env.LESHY_POPOVER_REVIEW?'.test-data/leshy-popovers':'.test-data/leshy-themes');fs.mkdirSync(output,{recursive:true});
const data=fs.mkdtempSync(path.join(output,'profile-')),project=fs.mkdtempSync(path.join(output,'project-'));
process.env.LOCALAPPDATA=data;process.env.LCA_PYTHON=process.env.LCA_TEST_PYTHON||process.env.LCA_PYTHON||(fs.existsSync(path.join(root,'.venv-test/Scripts/python.exe'))?path.join(root,'.venv-test/Scripts/python.exe'):'python');app.setPath('userData',path.join(data,'electron'));BrowserWindow.prototype.show=function(){};
BrowserWindow.prototype.loadURL=function(){return this.loadFile(path.join(root,'apps/desktop/dist/index.html'));};
dialog.showOpenDialog=async()=>({canceled:false,filePaths:[project]});dialog.showSaveDialog=async(_win,options)=>({canceled:false,filePath:path.join(output,options?.defaultPath?.endsWith('.zip')?'history.zip':'conversation.md')});dialog.showMessageBox=async()=>({response:1});
fs.writeFileSync(path.join(project,'hello.txt'),'Neutral fixture');
let currentWindow,stopping=false,requests=[],releaseStage4=null,releaseVisual=null,releaseInitialTheme=null;
// Renderer recovery fixture only: real backend calls still validate the selected
// chat and reject the deliberately nonexistent journal. No persistence schema is mocked.
let recoveryTaskFixture=null,recoveryAttempts=[],sourceApprovalFixture=null,sourceApprovalDecisions=[],lastApprovalEvent=null;
const registerHandle=ipcMain.handle.bind(ipcMain);
ipcMain.handle=(channel,handler)=>registerHandle(channel,async(...args)=>{
  if(channel==='task:approve'&&sourceApprovalFixture){sourceApprovalDecisions.push(args.slice(1));sourceApprovalFixture=null;return {ok:true};}
  const result=await handler(...args);
  if(channel==='appearance:get'&&!releaseInitialTheme){await new Promise(resolve=>{releaseInitialTheme=resolve;});}
  if(channel==='task:resolve-recovery')recoveryAttempts.push({params:args[1],result});
  return channel==='chat:load'&&result.ok&&recoveryTaskFixture?{...result,task:recoveryTaskFixture}:result;
});
const fixture=http.createServer((req,res)=>{let raw='';req.on('data',part=>raw+=part);req.on('end',()=>{
  if(req.method==='GET'){res.writeHead(200,{'Content-Type':'application/json'});res.end('{"data":[{"id":"neutral-fixture"},{"id":"neutral-fixture-2"}]}');return;}
  const p=JSON.parse(raw);requests.push(p);
  if(!p.stream){res.writeHead(200,{'Content-Type':'application/json'});res.end(JSON.stringify({id:'fixture',object:'chat.completion',model:'neutral-fixture',choices:[{index:0,message:{role:'assistant',content:'{}'},finish_reason:'stop'}]}));return;}
  const last=p.messages.map(m=>m.role).lastIndexOf('user');const after=p.messages.slice(last+1).some(m=>m.role==='tool');const command=p.messages[last]?.content.toLowerCase().includes('проверь node');const mcp=p.tools?.find(t=>t.function.name.startsWith('mcp_'));const discover=p.tools?.some(t=>t.function.name==='discover_mcp_tools');const calledMcp=p.messages.some(m=>m.role==='tool'&&m.tool_call_id==='mcp-add');
  if(p.messages[last]?.content.includes('studio-visual-error')){res.writeHead(401,{'Content-Type':'application/json'});res.end('{"error":{"message":"Тестовая ошибка доступа к модели"}}');return;}
  if(p.messages[last]?.content.includes('studio-visual-read')){const done=p.messages.slice(last+1).some(m=>m.role==='tool');const delta=done?{content:'Файл прочитан. Структура панели готова к проверке.'}:{content:'Изучу файл проекта и проверю структуру панели.',tool_calls:[{index:0,id:'studio-read',type:'function',function:{name:'read_file',arguments:'{"path":"hello.txt"}'}}]};res.writeHead(200,{'Content-Type':'text/event-stream'});res.write('data: '+JSON.stringify({id:'studio',choices:[{index:0,delta,finish_reason:done?'stop':'tool_calls'}]})+'\n\n');if(done)releaseVisual=()=>res.end('data: [DONE]\n\n');else res.end('data: [DONE]\n\n');return;}
  if(p.messages[last]?.content.toLowerCase().includes('stage6')){
    const results=p.messages.slice(last+1).filter(m=>m.role==='tool');
    const readOnly=p.messages[last].content.includes('readonly');
    const action=results.some(m=>m.tool_call_id==='stage6-write')?null:{name:'write_file',arguments:JSON.stringify({path:'hello.txt',content:'stage6 verified',overwrite:true})};
    const delta=action?{tool_calls:[{index:0,id:'stage6-write',type:'function',function:action}]}:{content:readOnly?'Только чтение: изменение не выполнено.':'Правка stage6 подготовлена.'};
    res.writeHead(200,{'Content-Type':'text/event-stream'});res.end('data: '+JSON.stringify({id:'stage6',choices:[{index:0,delta,finish_reason:delta.tool_calls?'tool_calls':'stop'}]})+'\n\ndata: [DONE]\n\n');return;
  }
  if(p.messages[last]?.content.includes('stage11-parent')||p.messages[last]?.content.includes('stage11-child')){
    const child=p.messages[last].content.includes('stage11-child'),called=p.messages.slice(last+1).some(m=>m.role==='tool');
    const delta=called?{content:child?'Дочернее исследование прочитало hello.txt.':'Результат ребёнка получен.'}:{tool_calls:[{index:0,id:child?'stage11-read':'stage11-delegate',type:'function',function:{name:child?'read_range':'delegate_readonly',arguments:child?'{"path":"hello.txt","start_line":1,"end_line":1}':'{"task":"stage11-child"}'}}]};
    res.writeHead(200,{'Content-Type':'text/event-stream'});res.end('data: '+JSON.stringify({id:'fixture',choices:[{index:0,delta,finish_reason:called?'stop':'tool_calls'}]})+'\n\ndata: [DONE]\n\n');return;
  }
  if(p.messages[last]?.content.toLowerCase().includes('stage4')){
    const results=p.messages.slice(last+1).filter(m=>m.role==='tool');
    const archived=p.messages.flatMap(m=>{
      if(m.role!=='assistant'||typeof m.content!=='string'||!/^\[(Архив контекста|Сохранённый обмен инструментами)/.test(m.content))return [];
      try{const data=JSON.parse(m.content.slice(m.content.indexOf('\n')+1));return [...(data.tool_evidence||[]),...(data.calls||[]).map(c=>({...JSON.parse(c.result),source_tool_call_id:c.source_tool_call_id}))];}catch{return [];}
    });
    const evidence=[...results.map(m=>({...JSON.parse(m.content),source_tool_call_id:m.tool_call_id})),...archived];
    // A confirmed patch implies the file and its parent exist even when older
    // creation receipts have moved out of the compact working context.
    const done=id=>evidence.some(e=>e.ok&&(e.source_tool_call_id===id||
      (id==='stage4-dir'&&['stage4-write','stage4-patch'].includes(e.source_tool_call_id))||
      (id==='stage4-write'&&e.source_tool_call_id==='stage4-patch')));
    let action;
    if(!done('stage4-dir'))action={name:'create_directory',arguments:JSON.stringify({path:'stage4/src'})};
    else if(!done('stage4-write'))action={name:'write_file',arguments:JSON.stringify({path:'stage4/src/demo.txt',content:'const value = 1;\n',overwrite:false})};
    else if(!done('stage4-patch'))action={name:'patch_file',arguments:JSON.stringify({path:'stage4/src/demo.txt',old_text:'value = 1',new_text:'value = 2'})};
    const id=action?.name==='create_directory'?'stage4-dir':action?.name==='write_file'?'stage4-write':'stage4-patch';
    const delta=action?{tool_calls:[{index:0,id,type:'function',function:action}]}:{content:'Вложенный файл готов.'};
    res.writeHead(200,{'Content-Type':'text/event-stream'});res.write('data: '+JSON.stringify({id:'stage4',object:'chat.completion.chunk',model:'neutral-fixture',choices:[{index:0,delta,finish_reason:delta.tool_calls?'tool_calls':'stop'}]})+'\n\n');
    if(action)res.end('data: [DONE]\n\n');else releaseStage4=()=>res.end('data: [DONE]\n\n');
    return;
  }
  const delta=command?(!after?{tool_calls:[{index:0,id:'command-node',type:'function',function:{name:'run_project_command',arguments:JSON.stringify({program:'node',arguments:['-e',"console.log('Neutral node OK')"]})}}]}:{content:'Проверка Node прошла.'}):mcp&&!calledMcp?{tool_calls:[{index:0,id:'mcp-add',type:'function',function:{name:mcp.function.name,arguments:'{"a":3,"b":4}'}}]}:discover&&!mcp?{tool_calls:[{index:0,id:'discover-mcp',type:'function',function:{name:'discover_mcp_tools',arguments:'{"query":"add","limit":1}'}}]}:{content:calledMcp?'MCP вернул 7. Готово.':'**Neutral** готов к работе.'};
  res.writeHead(200,{'Content-Type':'text/event-stream'});res.end('data: '+JSON.stringify({id:'fixture',object:'chat.completion.chunk',model:'neutral-fixture',choices:[{index:0,delta,finish_reason:delta.tool_calls?'tool_calls':'stop'}]})+'\n\ndata: '+JSON.stringify({id:'usage',object:'chat.completion.chunk',model:'neutral-fixture',choices:[],usage:{prompt_tokens:111,completion_tokens:7,total_tokens:118}})+'\n\ndata: [DONE]\n\n');
});});
async function js(code){try{const result=await currentWindow.webContents.executeJavaScript(code,true);await new Promise(r=>setTimeout(r,25));return result;}catch(error){throw new Error(String(error)+'\nScript: '+code.slice(0,500));}}
async function poll(expression,timeout=15000){const start=Date.now();while(Date.now()-start<timeout){if(await js(expression))return;await new Promise(r=>setTimeout(r,80));}throw Error('Timeout: '+expression);}
async function click(selector){await js(`document.querySelector(${JSON.stringify(selector)}).click()`);}
async function textButton(selector,text){await js(`Array.from(document.querySelectorAll(${JSON.stringify(selector)})).find(b=>b.textContent.trim()===${JSON.stringify(text)}).click()`);}
async function input(selector,value){await js(`{const node=document.querySelector(${JSON.stringify(selector)});Object.getOwnPropertyDescriptor(node.tagName==='TEXTAREA'?HTMLTextAreaElement.prototype:HTMLInputElement.prototype,'value').set.call(node,${JSON.stringify(value)});node.dispatchEvent(new Event('input',{bubbles:true}));}`);}
async function capture(name){fs.writeFileSync(path.join(output,name+'-layout.json'),JSON.stringify(await js(`({height:innerHeight,mode:document.querySelector('.app-shell')?.className,selected:document.querySelector('[aria-selected=true]')?.textContent,rects:Object.fromEntries(['.agent-panel','.chat-messages','.composer','.neutral-welcome','.activity-bar'].map(s=>[s,document.querySelector(s)?.getBoundingClientRect().toJSON()]))})`),null,2));await js('new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))');await currentWindow.webContents.capturePage(undefined,{stayHidden:true});await new Promise(r=>setTimeout(r,150));fs.writeFileSync(path.join(output,name+'.png'),(await currentWindow.webContents.capturePage(undefined,{stayHidden:true})).toPNG());}
async function finish(error){if(stopping)return;stopping=true;if(error){try{await capture('failure');fs.writeFileSync(path.join(output,'failure-dom.txt'),await js('document.body.innerText'));}catch{}}
  fs.writeFileSync(path.join(output,'result.json'),JSON.stringify({ok:!error,error:error?.stack||null,requests:requests.length,data,project},null,2));console.log(error?error.stack:'Neutral GUI integration passed');fixture.close();try{await js('window.lca.setEditorDirty(false)');}catch{}app.exit(error?1:0);
}
process.on('uncaughtException',finish);process.on('unhandledRejection',finish);
app.on('browser-window-created',(_,win)=>{currentWindow=win;win.webContents.setBackgroundThrottling(false);win.webContents.once('did-finish-load',async()=>{try{
 await poll("!!window.lca&&document.querySelector('.status')?.textContent.includes('Готов')");
 win.setContentSize(1440,900);
 await click('.mode-tabs [role=tab]:last-child');
 await poll("!!document.querySelector('.leshy-theme-picker')");
 // A delayed startup reply must not overwrite a more recent user selection.
 assert.ok(releaseInitialTheme);
 await click('.leshy-theme-picker button:nth-child(3)');
 await poll("document.documentElement.dataset.leshyTheme==='twilight'");
 releaseInitialTheme();
 await new Promise(r=>setTimeout(r,250));
 assert.equal(await js("document.documentElement.dataset.leshyTheme"),'twilight');
 if(process.env.LESHY_POPOVER_REVIEW){
  for(const [i,theme] of ['forest','parchment','twilight'].entries()){
   await click('.leshy-theme-picker button:nth-child('+(i+1)+')');await poll(`document.documentElement.dataset.leshyTheme==='${theme}'`);
   await click('[aria-label="Голосовая активация Лолы"]');await poll("document.querySelector('.studio-lola-controls>details')?.open");
   const menu=await js("(()=>{const n=document.querySelector('.studio-lola-controls>details>div'),r=n.getBoundingClientRect();return {inside:r.left>=0&&r.right<=innerWidth&&r.top>=0&&r.bottom<=innerHeight,image:getComputedStyle(n).backgroundImage}})()");assert(menu.inside,JSON.stringify(menu));assert.notEqual(menu.image,'none');await capture('wake-popover-'+theme);await click('[aria-label="Голосовая активация Лолы"]');
  }
  await finish();return;
 }
 // Selected main mode tab must meet the workspace edge without the inherited padding gap.
 const modeJoin=await js(`(()=>{const bar=document.querySelector('.topbar').getBoundingClientRect(),tab=document.querySelector('.mode-tabs [aria-selected=true]').getBoundingClientRect(),footer=document.querySelector('.statusbar').getBoundingClientRect(),button=document.querySelector('.statusbar button').getBoundingClientRect();return {bar:bar.toJSON(),tab:tab.toJSON(),gap:bar.bottom-tab.bottom,footer:footer.toJSON(),footerButton:button.toJSON(),scroll:[document.documentElement,document.body,document.querySelector('.studio-shell')].map(n=>({node:n.className||n.tagName,scrollTop:n.scrollTop,scrollHeight:n.scrollHeight,clientHeight:n.clientHeight}))}})()`);
 fs.writeFileSync(path.join(output,'mode-tab-join.json'),JSON.stringify(modeJoin,null,2));await capture('mode-tab-join');assert(Math.abs(modeJoin.gap)<1,JSON.stringify(modeJoin));
 assert(modeJoin.footerButton.top>=modeJoin.footer.top&&modeJoin.footerButton.bottom<=modeJoin.footer.bottom,'Footer control stays inside compact status bar: '+JSON.stringify(modeJoin));
 assert(modeJoin.bar.top>=0,'Top bar remains inside viewport: '+JSON.stringify(modeJoin));
 await click('.mode-tabs [role=tab]:first-child');await poll("document.querySelector('.mode-tabs [aria-selected=true]')?.textContent.includes('Код')");
 assert(await js("Math.abs(document.querySelector('.topbar').getBoundingClientRect().bottom-document.querySelector('.mode-tabs [aria-selected=true]').getBoundingClientRect().bottom)<1"),'Code tab joins the workspace');await capture('mode-code-join');
 await click('.mode-tabs [role=tab]:last-child');await poll("!!document.querySelector('.leshy-theme-picker')");

 // A widened settings rail must not push text underneath the decorative ink.
 await click('[title="Настройки Лешего"]');await textButton('.settings-tabs button','Расширения');win.setContentSize(1102,800);
 await js("document.querySelector('.settings-dialog').style.setProperty('--studio-settings','340px')");await poll('innerWidth>=1100&&innerWidth<=1110');await js('document.fonts.ready');await js('new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))');
 const introJoin=await js(`(()=>{const n=[...document.querySelectorAll('.section-intro')].find(n=>n.checkVisibility()),r=n.getBoundingClientRect(),s=getComputedStyle(n,'::after'),art={left:r.right-parseFloat(s.right)-parseFloat(s.width),right:r.right-parseFloat(s.right),top:r.top+parseFloat(s.top),bottom:r.top+parseFloat(s.top)+parseFloat(s.height)};const text=[...n.querySelectorAll('h3,p')].flatMap(n=>{const range=document.createRange();range.selectNodeContents(n);return [...range.getClientRects()].map(r=>r.toJSON())});return {art,text,overlap:text.some(t=>t.left<art.right&&t.right>art.left&&t.top<art.bottom&&t.bottom>art.top)}})()`);
 fs.writeFileSync(path.join(output,'settings-illustration-join.json'),JSON.stringify(introJoin,null,2));await capture('settings-illustration-join');assert.equal(introJoin.overlap,false,JSON.stringify(introJoin));
 await js("document.querySelector('.settings-dialog').style.removeProperty('--studio-settings')");await click('[title="Закрыть настройки"]');win.setContentSize(1440,900);
 if(process.env.LESHY_SPOT_REVIEW){await finish();return;}
 const colors=[];
 for(const [i,theme] of ['forest','parchment','twilight'].entries()){
  await click('.leshy-theme-picker button:nth-child('+(i+1)+')');
  await poll("document.documentElement.dataset.leshyTheme==='"+theme+"'");
  assert.equal(await js("JSON.parse(localStorage.getItem('localagent.appearance.v1')).theme"),theme);
  assert.equal(await js("document.querySelectorAll('.leshy-theme-picker button[aria-pressed=true] .leshy-theme-check').length"),1);
  colors.push(await js("getComputedStyle(document.querySelector('.app-shell')).getPropertyValue('--bg-app')"));
  fs.writeFileSync(path.join(output,theme+'-style-inventory.json'),JSON.stringify(await js(`(()=>{const props=['fontSize','fontWeight','color','borderRadius','boxShadow'];const nodes=[...document.querySelectorAll('.app-shell *')].filter(el=>el.checkVisibility());return Object.fromEntries(props.map(prop=>{const counts={};for(const el of nodes){const value=getComputedStyle(el)[prop];counts[value]=(counts[value]||0)+1}return [prop,counts]}))})()`),null,2));
  await capture(theme+'-welcome');
  await click('[title="Настройки Лешего"]');await textButton('.settings-tabs button','Оформление');await capture(theme+'-settings');
  if(process.env.LESHY_WINDOWS_MATRIX){
   for(const label of ['Модели','Голос и Лола','Расширения','Компьютер и Telegram','Оформление','Контекст и лимиты','Локальный запуск','История и копии']){
    await textButton('.settings-tabs button',label);await new Promise(r=>setTimeout(r,150));assert(await js("(()=>{const n=[...document.querySelectorAll('.section-intro')].find(n=>n.checkVisibility());if(!n)return false;const s=getComputedStyle(n,'::after');return s.maskImage==='none'&&s.backgroundImage.includes('painted')})()"),'Every settings section has painted art: '+label);await capture(theme+'-window-'+['Модели','Голос и Лола','Расширения','Компьютер и Telegram','Оформление','Контекст и лимиты','Локальный запуск','История и копии'].indexOf(label));
   }
  }
  await click('[title="Закрыть настройки"]');
  if(process.env.LESHY_WINDOWS_MATRIX){
   await click('[title="Создать проект"]');assert(await js("(()=>{const s=getComputedStyle(document.querySelector('.workspace-dialog .forest-spot'));return s.maskImage==='none'&&s.backgroundImage.includes('spot-birch-painted')})()"),'Project uses painted raster, not silhouette');await capture(theme+'-project-dialog');await textButton('.workspace-dialog button','Отмена');
   await textButton('.leshy-tool-grid button','Инструменты');await poll("!!document.querySelector('.optional-ide-dialog[open]')");
   for(const [i,label] of ['Исследователь','Диагностика','Рабочие копии','Изоляция'].entries()){await textButton('.optional-ide-dialog .extension-tabs button',label);await capture(theme+'-optional-'+i);}
   await click('[aria-label="Закрыть возможности IDE"]');
  }
 }
 assert.equal(new Set(colors).size,3);
 await input('.composer textarea','Сохранённый черновик задачи');
 await click('.studio-welcome-actions button:last-child');
 assert.equal(await js("document.activeElement===document.querySelector('.composer textarea')"),true);
 assert.equal(await js("document.querySelector('.composer textarea').value"),'Сохранённый черновик задачи');
 await click('[aria-label="Настроить модель агента"]');
 await poll("!!document.querySelector('.settings-dialog')");
 await click('[title="Закрыть настройки"]');
 await js("localStorage.setItem('localagent.appearance.v1',JSON.stringify({...JSON.parse(localStorage.getItem('localagent.appearance.v1')),theme:'light',sidebar:false}));window.dispatchEvent(new Event('appearance-changed'))");
 await poll("document.documentElement.dataset.leshyTheme==='parchment'");assert.equal(await js("document.querySelector('.app-shell').classList.contains('sidebar-hidden')"),true);
 await js("localStorage.setItem('localagent.appearance.v1',JSON.stringify({...JSON.parse(localStorage.getItem('localagent.appearance.v1')),theme:'invalid',sidebar:true}));window.dispatchEvent(new Event('appearance-changed'))");await poll("document.documentElement.dataset.leshyTheme==='forest'");
 await click('.leshy-theme-picker button:nth-child(3)');
 await currentWindow.webContents.reload();await poll("!!document.querySelector('.leshy-theme-picker')");assert.equal(await js("document.documentElement.dataset.leshyTheme"),'twilight');
 for(const zoom of [1.25,2]){win.webContents.setZoomFactor(zoom);await new Promise(r=>setTimeout(r,250));assert.equal(await js('document.documentElement.scrollWidth>innerWidth'),false);await capture('zoom-'+zoom);}
 win.webContents.setZoomFactor(1);win.setContentSize(1050,680);
 await js("document.querySelector('.chat-messages').scrollTop=0");
 assert.equal(await js("(()=>{const box=document.querySelector('.chat-messages').getBoundingClientRect(),logo=document.querySelector('.leshy-welcome>.leshy-mark').getBoundingClientRect();return logo.top>=box.top-1})()"),true,'welcome logo must be reachable at the top');
 await capture('small');
 await js("{const box=document.querySelector('.chat-messages');box.scrollTop=box.scrollHeight}");
 assert.equal(await js("(()=>{const box=document.querySelector('.chat-messages').getBoundingClientRect(),picker=document.querySelector('.leshy-theme-picker').getBoundingClientRect();return picker.bottom<=box.bottom+1})()"),true,'theme picker must be reachable above the composer');
 await js("document.querySelector('.leshy-theme-picker button').focus()");
 assert.equal(await js("document.activeElement===document.querySelector('.leshy-theme-picker button')"),true);
 win.setContentSize(1440,900);
 await poll("getComputedStyle(document.querySelector('.leshy-edge')).display!=='none'");
 await click('[title="Настройки Лешего"]');await textButton('.settings-tabs button','Оформление');await click('[aria-label="Иллюстрации на приветственном экране"]');await click('[title="Закрыть настройки"]');
 assert.equal(await js("getComputedStyle(document.querySelector('.leshy-edge')).display"),'none');
 assert.equal(await js("getComputedStyle(document.querySelector('.woodland-accent')).display"),'none');
 await click('[title="Создать проект"]');assert.equal(await js("getComputedStyle(document.querySelector('.workspace-dialog .forest-spot')).display"),'none','New project illustration follows the art preference');await textButton('.workspace-dialog button','Отмена');
 await click('[title="Настройки Лешего"]');await textButton('.settings-tabs button','Модели');assert.equal(await js("getComputedStyle(document.querySelector('.settings-section .section-intro'),'::after').display"),'none','Settings spot follows the art preference');await click('[title="Закрыть настройки"]');

 await finish();
 }catch(error){await finish(error);}})});
fixture.listen(0,'127.0.0.1',()=>require('../../apps/desktop/dist-electron/main.cjs'));
