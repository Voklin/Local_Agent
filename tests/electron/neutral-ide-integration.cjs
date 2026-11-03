// Actual Desktop -> Code-OSS webview -> shared Core -> editor-owned model tool.
const {app,BrowserWindow,dialog,ipcMain}=require('electron');
const fs=require('node:fs'),path=require('node:path'),http=require('node:http'),assert=require('node:assert/strict'),{spawnSync}=require('node:child_process');
app.disableHardwareAcceleration();
const root=path.resolve(__dirname,'../..'),output=path.join(root,process.env.LESHY_ACCEPTANCE_TEST?(process.env.LESHY_ACCEPTANCE_JSON?'.test-data/ide-acceptance-json':'.test-data/ide-acceptance'):process.env.LESHY_PANEL_AUDIT?'.test-data/leshy-panel-audit':process.env.NEUTRAL_TEST_EMPTY_IDE?'.test-data/ide-empty':'.test-data/stage19');fs.mkdirSync(output,{recursive:true});
const data=fs.mkdtempSync(path.join(output,'profile-')),project=fs.mkdtempSync(path.join(output,'project-'));
process.env.LOCALAPPDATA=data;process.env.LCA_PYTHON=process.env.LCA_TEST_PYTHON||process.env.LCA_PYTHON||(fs.existsSync(path.join(root,'.venv-test/Scripts/python.exe'))?path.join(root,'.venv-test/Scripts/python.exe'):'python');process.env.NEUTRAL_IDE_TEST_CDP='1';app.setPath('userData',path.join(data,'electron'));
BrowserWindow.prototype.show=function(){};dialog.showOpenDialog=async()=>({canceled:false,filePaths:[project]});
fs.mkdirSync(path.join(project,'.vscode'));fs.writeFileSync(path.join(project,'.vscode/settings.json'),JSON.stringify({'git.openRepositoryInParentFolders':'never','git.autoRepositoryDetection':false}));
fs.writeFileSync(path.join(project,'main.ts'),'export const value = 1;\n');
let win,launch,done=false,requests=[],cdp,sessionContexts=[],mainPage,webview,acceptanceStep=0;
const handle=ipcMain.handle.bind(ipcMain);ipcMain.handle=(channel,handler)=>handle(channel,async(...args)=>{const result=await handler(...args);if(channel==='ide:open')launch=result;return result;});
const server=http.createServer((req,res)=>{let raw='';req.on('data',x=>raw+=x);req.on('end',()=>{
 if(req.method==='GET'){res.setHeader('content-type','application/json');res.end(JSON.stringify({data:[{id:'neutral-integration',context_length:8192}]}));return;}
 const body=JSON.parse(raw);requests.push(body);if(body.stream!==true){res.setHeader('content-type','application/json');res.end(JSON.stringify({id:'completion',object:'chat.completion',choices:[{index:0,message:{role:'assistant',content:' // inline suggestion'},finish_reason:'stop'}]}));return;}const tools=body.messages.filter(m=>m.role==='tool');let delta;
 if(process.env.LESHY_ACCEPTANCE_TEST){
  let action;
  const step=acceptanceStep++;
  if(step===0)action={id:'accept-definition',name:'write_file',arguments:{path:'totals.js',content:'export function grand_total(n){return n * 1.1;}\n',overwrite:true}};
  else if(step===1)action={id:'accept-caller',name:'write_file',arguments:{path:'invoice.js',content:"import {tax_total} from './totals.js';\nexport function invoice(n){return grand_total(n);}\n",overwrite:true}};
  else if(step===3)action={id:'accept-repair',name:'patch_file',arguments:{path:'invoice.js',old_text:'import {tax_total}',new_text:'import {grand_total}'}};
  const text=step>=4?'Import исправлен.':'Переименование готово.';
  delta=process.env.LESHY_ACCEPTANCE_JSON?{content:JSON.stringify(action?{protocol:'neutral.action.v1',kind:'tool',name:action.name,arguments:action.arguments}:{protocol:'neutral.action.v1',kind:'final',text})}:action?{tool_calls:[{index:0,id:action.id,type:'function',function:{name:action.name,arguments:JSON.stringify(action.arguments)}}]}:{content:text};
 }
 else if(!tools.some(m=>m.tool_call_id?.startsWith('read-')))delta={tool_calls:[{index:0,id:'read-'+requests.length,type:'function',function:{name:'read_file',arguments:'{"path":"main.ts"}'}}]};
 else if(!tools.some(m=>m.tool_call_id?.startsWith('write-')))delta={tool_calls:[{index:0,id:'write-'+requests.length,type:'function',function:{name:'write_file',arguments:JSON.stringify({path:'main.ts',content:'export const value = 2;\n',overwrite:true})}}]};
 else delta={content:'Изменение завершено. Значение равно двум.'};
 res.writeHead(200,{'Content-Type':'text/event-stream'});res.end('data: '+JSON.stringify({choices:[{delta,finish_reason:delta.tool_calls?'tool_calls':'stop'}]})+'\n\ndata: [DONE]\n\n');
 });});
const delay=ms=>new Promise(resolve=>setTimeout(resolve,ms));
async function until(action,label,timeout=30000){const start=Date.now();let last;while(Date.now()-start<timeout){try{const result=await action();if(result)return result;}catch(error){last=error;}await delay(100);}throw Error('Timeout '+label+(last?' · '+last.message:''));}
async function desktop(code){return win.webContents.executeJavaScript(code,true);}
async function connect(url){const socket=new WebSocket(url),pending=new Map();let id=0;await new Promise((resolve,reject)=>{socket.onopen=resolve;socket.onerror=reject;});socket.onmessage=event=>{const m=JSON.parse(event.data);if(m.method==='Runtime.executionContextCreated')sessionContexts.push({session:m.sessionId,id:m.params.context.id});const entry=pending.get(m.id);if(entry){pending.delete(m.id);m.error?entry.reject(Error(JSON.stringify(m.error))):entry.resolve(m.result);}};return {send:(method,params={},sessionId)=>new Promise((resolve,reject)=>{const key=++id;pending.set(key,{resolve,reject});socket.send(JSON.stringify({id:key,method,params,...(sessionId?{sessionId}:{})}));}),close:()=>socket.close()};}
async function evaluate(context,expression){const result=await cdp.send('Runtime.evaluate',{expression,contextId:context.id,returnByValue:true,awaitPromise:true},context.session);if(result.exceptionDetails)throw Error(result.exceptionDetails.exception?.description||result.exceptionDetails.text);return result.result.value;}
async function findWebview(){
 const targets=(await cdp.send('Target.getTargets')).targetInfos;for(const target of targets.filter(t=>['page','iframe'].includes(t.type))){if(attached.has(target.targetId))continue;attached.add(target.targetId);try{const {sessionId}=await cdp.send('Target.attachToTarget',{targetId:target.targetId,flatten:true});await cdp.send('Runtime.enable',{},sessionId);if(target.type==='page'&&target.url.includes('workbench'))mainPage={session:sessionId};}catch{}}
 for(const context of sessionContexts){try{if(await evaluate(context,"(typeof window.lca==='object' && window.neutralIdeHost===true) || !!document.querySelector('#folder')"))return context;}catch{}}
 return null;
}
const attached=new Set();
async function panel(expression){return evaluate(webview,expression);}
async function semanticBorder(selector,token){return panel(`(()=>{const n=document.querySelector('${selector}'),c=getComputedStyle(n),hex=c.getPropertyValue('${token}').trim();return c.borderLeftColor==='rgb('+[1,3,5].map(i=>parseInt(hex.slice(i,i+2),16)).join(', ')+')'})()`);}
async function screenshot(name){const shot=await cdp.send('Page.captureScreenshot',{format:'png'},mainPage.session);fs.writeFileSync(path.join(output,name+'.png'),Buffer.from(shot.data,'base64'));}
async function finish(error){if(done)return;done=true;if(error){console.error(error.stack);try{if(cdp){await screenshot('failure');if(webview)fs.writeFileSync(path.join(output,'failure-dom.txt'),await panel('document.body.innerText'));}}catch{}}
 fs.writeFileSync(path.join(output,'requests.json'),JSON.stringify(requests,null,2));fs.writeFileSync(path.join(output,'result.json'),JSON.stringify({ok:!error,error:error?.stack,requests:requests.length,data,project,launch},null,2));cdp?.close();if(launch?.pid)spawnSync('taskkill',['/PID',String(launch.pid),'/T','/F'],{windowsHide:true,stdio:'ignore'});server.close();console.log(error?'Stage19 failed':'Stage19 native IDE/Core/editor integration passed');app.exit(error?1:0);
}
app.on('browser-window-created',(_,window)=>{win=window;window.webContents.once('did-finish-load',async()=>{try{
 await until(()=>desktop('!!window.lca'),'desktop');
 await desktop(`window.lca.configureModel(${JSON.stringify({base_url:'http://127.0.0.1:'+server.address().port+'/v1',model:process.env.LESHY_ACCEPTANCE_TEST?'':'neutral-integration',api_key:'',api_protocol:'chat',tool_protocol:process.env.LESHY_ACCEPTANCE_JSON?'json':'native',...(process.env.LESHY_ACCEPTANCE_TEST?{settings:{memory_updates:'off'}}:{})})})`);
 if(!process.env.NEUTRAL_TEST_EMPTY_IDE)await desktop('window.lca.chooseProject()');
 await until(()=>desktop("!!document.querySelector('.mode-tabs button')"),'IDE button');await desktop("document.querySelector('.mode-tabs button').click()");await until(()=>launch?.ok,'native launch');
 const mainChat=await desktop("window.lca.newChat('chat')");assert(mainChat.ok);
 const profile=path.join(data,'electron/neutral-ide/user-data');const [port,endpoint]=await until(()=>{const p=path.join(profile,'DevToolsActivePort');if(fs.existsSync(p))return fs.readFileSync(p,'utf8').split('\n');},'Code-OSS CDP');cdp=await connect('ws://127.0.0.1:'+port+endpoint);
 webview=await until(findWebview,'agent webview',45000);
 const chromeJoin=(await cdp.send('Runtime.evaluate',{expression:`(()=>{const n=document.querySelector('.part.auxiliarybar>.composite.title'),t=n.getBoundingClientRect(),s=getComputedStyle(n,'::after');let anchor=n;while(anchor&&getComputedStyle(anchor).position==='static')anchor=anchor.parentElement;const r=anchor.getBoundingClientRect(),bottom=r.bottom-parseFloat(s.bottom),top=bottom-parseFloat(s.height);return {title:t.toJSON(),ornament:{top,bottom},inside:top>=t.top-1&&bottom<=t.bottom+1}})()`,returnByValue:true},mainPage.session)).result.value;
 fs.writeFileSync(path.join(output,'chrome-join.json'),JSON.stringify(chromeJoin,null,2));assert(chromeJoin.inside,'Native title ornament escaped its header: '+JSON.stringify(chromeJoin));
 if(process.env.NEUTRAL_TEST_EMPTY_IDE){assert(await panel("!!document.querySelector('#folder') && !!document.querySelector('#recent')"));assert.equal((await desktop('window.lca.health()')).project,null);assert.equal(requests.length,0);await until(()=>panel("!!document.querySelector('img.spot')?.complete && document.querySelector('img.spot').naturalWidth>0"),'painted empty illustration loaded');assert(await panel("document.querySelector('img.spot').src.includes('spot-birch-painted.webp')"),'Empty page uses the generated raster asset');assert(await panel("[...document.querySelectorAll('button,.spot')].every(n=>{const r=n.getBoundingClientRect();return r.left>=0&&r.right<=innerWidth})"),'Empty IDE controls and art stay inside viewport');await screenshot('empty');await panel("document.querySelector('#recent').click()");await delay(500);await screenshot('recent');await finish();return;}await until(()=>panel("!!document.querySelector('.nw-header') && !!document.querySelector('.nw-compose textarea:not(:disabled)')"),'connected agent');
 if(process.env.LESHY_ACCEPTANCE_TEST){const acceptance=await require('./ide-acceptance.cjs').runAcceptance({desktop,panel,until,screenshot,fs,path,project,requests});fs.writeFileSync(path.join(output,'acceptance.json'),JSON.stringify(acceptance,null,2));await finish();return;}
 if(process.env.LESHY_PANEL_AUDIT){
  const metrics=await panel(`(()=>{const nodes=['html','body','#root','.nw','.nw-header','.nw-nav','.nw-transcript','.nw-compose','.nw-footer'];return {viewport:{width:innerWidth,height:innerHeight},nodes:Object.fromEntries(nodes.map(s=>{const n=document.querySelector(s),c=getComputedStyle(n);return [s,{rect:n.getBoundingClientRect().toJSON(),padding:c.padding,boxSizing:c.boxSizing,scroll:n.scrollWidth,client:n.clientWidth}]}))}})()`);
  fs.writeFileSync(path.join(output,'panel-layout.json'),JSON.stringify(metrics,null,2));await screenshot('panel-layout');
  assert.equal(await panel("getComputedStyle(document.body).paddingLeft"),'0px','Host webview padding consumes the panel width');
  assert.equal(await panel("getComputedStyle(document.body).paddingRight"),'0px','Host webview padding consumes the panel width');
  await panel("document.querySelector('[aria-label=\"Настройки подключения\"]').click()");
  await panel(`{const n=document.querySelector('input[list="nw-models"]');Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(n,'local/very-long-model-name-for-panel-layout-'.repeat(4));n.dispatchEvent(new Event('input',{bubbles:true}));}`);await delay(80);
  await panel("document.querySelector('.nw-page form').requestSubmit()");await until(()=>panel("!!document.querySelector('.nw-model')"),'long model saved');
  const measurements=[];
  async function resizePanel(width){
   const geometry=(await cdp.send('Runtime.evaluate',{expression:`(()=>{const bar=document.querySelector('.part.auxiliarybar'),r=bar.getBoundingClientRect();const sash=[...document.querySelectorAll('.monaco-sash.vertical')].map(n=>n.getBoundingClientRect()).filter(n=>n.height>100&&n.width>0).sort((a,b)=>Math.abs(a.x+a.width/2-r.left)-Math.abs(b.x+b.width/2-r.left))[0];return {x:sash.x+sash.width/2,y:sash.y+Math.min(160,sash.height/2),to:r.left+r.width-${width}}})()`,returnByValue:true},mainPage.session)).result.value;
   for(const event of [{type:'mouseMoved',x:geometry.x},{type:'mousePressed',x:geometry.x,button:'left',clickCount:1},{type:'mouseMoved',x:geometry.to,button:'left',buttons:1},{type:'mouseReleased',x:geometry.to,button:'left',clickCount:1}])await cdp.send('Input.dispatchMouseEvent',{y:geometry.y,...event},mainPage.session);
   await until(async()=>Math.abs(await panel('innerWidth')-width)<4,'real panel width '+width);await cdp.send('Input.dispatchMouseEvent',{type:'mouseMoved',x:500,y:200},mainPage.session);await delay(120);
  }
  async function checkControls(page,width){
   const record=await panel(`(()=>{const selectors='.nw-header button,.nw-nav button,.nw-compose button,.nw-compose select,.nw-compose textarea,.nw-page input,.nw-page select,.nw-page textarea,.nw-page button,.nw-footer button,.nw-approval button';const controls=[...document.querySelectorAll(selectors)].filter(n=>n.checkVisibility()).map(n=>({text:n.getAttribute('aria-label')||n.textContent.slice(0,45),rect:n.getBoundingClientRect().toJSON()}));return {width:innerWidth,root:document.querySelector('.nw').getBoundingClientRect().toJSON(),scroll:document.documentElement.scrollWidth,controls}})()`);
   const theme=await panel('document.documentElement.dataset.leshyTheme');measurements.push({theme,page,...record});fs.writeFileSync(path.join(output,'width-matrix.json'),JSON.stringify(measurements,null,2));await screenshot('panel-'+theme+'-'+page+'-'+width);
   assert.equal(record.root.left,0,'Panel starts at the real webview edge');assert(record.root.right<=record.width+1,'Panel fits webview');
   assert(record.controls.every(c=>c.rect.left>=-1&&c.rect.right<=record.width+1),JSON.stringify(record));
   if(page==='conversation')assert(await panel("(()=>{const b=document.querySelector('.nw-model').getBoundingClientRect(),icon=document.querySelector('.nw-model svg').getBoundingClientRect();return icon.left>=b.left&&icon.right<=b.right-4})()"),'Long model name clips its disclosure control');
  }
  for(const theme of ['forest','parchment','twilight']){
   await desktop(`window.lca.setAppearanceTheme('${theme}')`);await until(()=>panel(`document.documentElement.dataset.leshyTheme==='${theme}'`),'audit theme '+theme);
   for(const width of [240,320,420]){
    await resizePanel(width);
    for(const [page,label] of [['conversation','Диалог'],['history','История'],['activity','Работа']]){await panel(`[...document.querySelectorAll('.nw-nav button')].find(n=>n.textContent==='${label}').click()`);await delay(60);await checkControls(page,width);}
    await panel("document.querySelector('[aria-label=\"Настройки подключения\"]').click()");await delay(60);await checkControls('settings',width);
    await panel("[...document.querySelectorAll('.nw-nav button')].find(n=>n.textContent==='Диалог').click()");await panel("document.querySelector('.nw-checks-trigger').click()");if(!await panel("!!document.querySelector('.nw-check-definition')"))await panel("document.querySelector('.nw-add-check').click()");await delay(60);await checkControls('checks',width);
   }
  }
  // Validate the narrow confirmation surface with a real fixture request.
  await panel("[...document.querySelectorAll('.nw-nav button')].find(n=>n.textContent==='Диалог').click()");
  await panel(`{const n=document.querySelector('.nw-compose textarea');Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype,'value').set.call(n,'Измени значение main.ts на 2');n.dispatchEvent(new Event('input',{bubbles:true}));}`);await delay(80);await panel("document.querySelector('.nw-send').click()");await until(()=>panel("!!document.querySelector('.nw-approval')"),'audit approval');
  for(const width of [240,320,420]){await resizePanel(width);await checkControls('approval',width);}
  assert.equal(fs.readFileSync(path.join(project,'main.ts'),'utf8'),'export const value = 1;\n','Layout audit must not approve writes');
  await panel("[...document.querySelectorAll('.nw-approval button')].find(n=>n.textContent==='Остановить задачу').click()");
  await until(()=>panel("!document.querySelector('.nw-approval')"),'approval cancelled');
  await resizePanel(420);await panel("document.documentElement.style.zoom='2'");await delay(200);
  await checkControls('zoom-200',420);await panel("document.documentElement.style.zoom=''");
  await finish();return;
 }
 assert.equal(await panel("!!document.querySelector('.nw')"),true);
 const nativeDom=await cdp.send('Runtime.evaluate',{expression:"JSON.stringify({html:document.documentElement.outerHTML.slice(0,2000),body:document.body.outerHTML.slice(0,1200),workbench:document.querySelector('.monaco-workbench')?.outerHTML.slice(0,1200)})",returnByValue:true},mainPage.session);fs.writeFileSync(path.join(output,'native-dom.json'),nativeDom.result.value);

 await until(()=>panel("document.querySelector('.nw-send').getBoundingClientRect().width>10"),'visible composer');await screenshot('leshy-agent-start');
 const layout=await panel("(()=>{const r=document.querySelector('.nw-send').getBoundingClientRect();return {width:innerWidth,height:innerHeight,right:r.right,bottom:r.bottom,buttonWidth:r.width,buttonHeight:r.height,scroll:document.documentElement.scrollWidth,history:!!document.querySelector('.nonexistent-history-overlay')}})()");fs.writeFileSync(path.join(output,'layout.json'),JSON.stringify(layout,null,2));assert(layout.buttonWidth>10&&layout.buttonHeight>10&&layout.right<=layout.width+1&&layout.bottom<=layout.height+1&&layout.scroll<=layout.width+1,JSON.stringify(layout));assert(!layout.history,'History obscures the agent at startup');assert(await panel("[...document.querySelectorAll('.nw-header button,.nw-nav button')].every(b=>{const r=b.getBoundingClientRect();return r.left>=0&&r.right<=innerWidth+1&&r.width>0})"),'Agent toolbar clipped');win.close();assert.equal(win.isDestroyed(),false,'Desktop closed the shared Core while IDE was connected');assert.equal(await desktop("document.querySelector('.mode-tabs [aria-selected=true]').textContent"),'Чат');
 await panel("{const field=document.querySelector('.nw-compose textarea');Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype,'value').set.call(field,'Измени значение main.ts на 2');field.dispatchEvent(new Event('input',{bubbles:true}));}");
 await delay(100);await panel("document.querySelector('.nw-send').click()");
 await until(()=>panel("!!document.querySelector('.nw-approval')"),'Core write approval',45000);assert.equal(await panel("!!document.querySelector('.nw-diff-add')&&!!document.querySelector('.nw-diff-remove')"),true);await screenshot('approval');
 assert(await panel("(()=>{const b=[...document.querySelectorAll('.nw-approval button:not(:disabled)')];b.at(-1).focus();document.dispatchEvent(new KeyboardEvent('keydown',{key:'Tab',bubbles:true,cancelable:true}));if(document.activeElement!==b[0])return false;document.dispatchEvent(new KeyboardEvent('keydown',{key:'Tab',shiftKey:true,bubbles:true,cancelable:true}));return document.activeElement===b.at(-1)})()"),'Approval retains keyboard focus');
 assert.equal(fs.readFileSync(path.join(project,'main.ts'),'utf8'),'export const value = 1;\n');
 const diff=await panel("window.lca.idePreviewDiff('main.ts')");assert.equal(diff.ok,true,JSON.stringify(diff));await screenshot('native-diff');
 await panel("Array.from(document.querySelectorAll('.nw-approval button')).find(b=>b.textContent.includes('Применить')).click()");
 await until(()=>panel("document.body.innerText.includes('Значение равно двум') && !document.querySelector('.nw-send[aria-label=\"Остановить\"]')"),'model answer');assert.equal(fs.readFileSync(path.join(project,'main.ts'),'utf8'),'export const value = 2;\n');await screenshot('completed');await panel("[...document.querySelectorAll('.nw-nav button')].find(b=>b.textContent==='Работа').click()");await screenshot('leshy-agent-activity');await panel("[...document.querySelectorAll('.nw-nav button')].find(b=>b.textContent==='Диалог').click()");
 const shared=await desktop(`window.lca.loadChat(${JSON.stringify(mainChat.chat.id)},'chat')`);assert.equal(shared.chat.messages.length,0,'IDE selection leaked into desktop Chat');
 await panel("window.lca.ideOpenFile('main.ts')");await cdp.send('Input.dispatchKeyEvent',{type:'keyDown',key:'z',code:'KeyZ',modifiers:2,windowsVirtualKeyCode:90},mainPage.session);await cdp.send('Input.dispatchKeyEvent',{type:'keyUp',key:'z',code:'KeyZ',modifiers:2,windowsVirtualKeyCode:90},mainPage.session);
 const before=requests.length;await delay(200);const dirty=await panel("window.lca.startTask('Не отправлять при черновике',false,'ide')");assert.equal(dirty.ok,false);assert.match(dirty.error,/Сохраните/);assert.equal(requests.length,before);
 await cdp.send('Input.dispatchKeyEvent',{type:'keyDown',key:'s',code:'KeyS',modifiers:2,windowsVirtualKeyCode:83},mainPage.session);await cdp.send('Input.dispatchKeyEvent',{type:'keyUp',key:'s',code:'KeyS',modifiers:2,windowsVirtualKeyCode:83},mainPage.session);
 await until(()=>fs.readFileSync(path.join(project,'main.ts'),'utf8')==='export const value = 1;\n','editor undo/save');await screenshot('undo');
 const editorContext=await panel("window.lca.ideEditorContext()");assert.equal(editorContext.ok,true);assert.equal(editorContext.path,'main.ts');
 await panel("window.__started=[];const original=window.lca.startTask;window.lca.startTask=(...args)=>{window.__started.push(args);return Promise.resolve({ok:false,error:'mode test intercepted before inference'})};");
 for(const mode of ['ask','plan']){
  await panel(`{const select=document.querySelector('[aria-label="Режим агента"]');Object.getOwnPropertyDescriptor(HTMLSelectElement.prototype,'value').set.call(select,'${mode}');select.dispatchEvent(new Event('change',{bubbles:true}));}`);await delay(100);
  await panel("{const f=document.querySelector('.nw-compose textarea');Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype,'value').set.call(f,'Объясни код');f.dispatchEvent(new Event('input',{bubbles:true}));}");await delay(100);await panel("document.querySelector('.nw-send').click()");await until(()=>panel(`window.__started.length===${mode==='ask'?1:2}`),'mode request');await delay(150);
 }
 await until(()=>panel("!!document.querySelector('.nw-error')"),'error surface');assert(await semanticBorder('.nw-error','--status-error'),'Error keeps its semantic red rail');
 const starts=await panel('window.__started');assert(starts.every(args=>args[3].read_only===true&&args[3].auto_checks===false));assert.match(starts[1][0],/составь план/i);
 await panel("window.lca.ideOpenFile('main.ts')");
 await cdp.send('Input.dispatchKeyEvent',{type:'keyDown',key:'\\',code:'Backslash',modifiers:1,windowsVirtualKeyCode:220},mainPage.session);await cdp.send('Input.dispatchKeyEvent',{type:'keyUp',key:'\\',code:'Backslash',modifiers:1,windowsVirtualKeyCode:220},mainPage.session);
 await until(()=>requests.some(body=>body.max_tokens===160),'inline completion HTTP');await delay(500);await screenshot('inline-completion');
 assert.equal(fs.readFileSync(path.join(project,'main.ts'),'utf8'),'export const value = 1;\n','Completion must not modify disk');
 await cdp.send('Input.dispatchKeyEvent',{type:'keyDown',key:'Tab',code:'Tab',windowsVirtualKeyCode:9},mainPage.session);await cdp.send('Input.dispatchKeyEvent',{type:'keyUp',key:'Tab',code:'Tab',windowsVirtualKeyCode:9},mainPage.session);
 await cdp.send('Input.dispatchKeyEvent',{type:'keyDown',key:'s',code:'KeyS',modifiers:2,windowsVirtualKeyCode:83},mainPage.session);await cdp.send('Input.dispatchKeyEvent',{type:'keyUp',key:'s',code:'KeyS',modifiers:2,windowsVirtualKeyCode:83},mainPage.session);
 await until(()=>fs.readFileSync(path.join(project,'main.ts'),'utf8').includes('inline suggestion'),'Tab accepts suggestion');
 await cdp.send('Input.dispatchKeyEvent',{type:'keyDown',key:'k',code:'KeyK',modifiers:3,windowsVirtualKeyCode:75},mainPage.session);await cdp.send('Input.dispatchKeyEvent',{type:'keyUp',key:'k',code:'KeyK',modifiers:3,windowsVirtualKeyCode:75},mainPage.session);
 await delay(400);await cdp.send('Input.insertText',{text:'Добавь пояснение к выделенному коду'},mainPage.session);await cdp.send('Input.dispatchKeyEvent',{type:'keyDown',key:'Enter',code:'Enter',windowsVirtualKeyCode:13},mainPage.session);await cdp.send('Input.dispatchKeyEvent',{type:'keyUp',key:'Enter',code:'Enter',windowsVirtualKeyCode:13},mainPage.session);
 await until(()=>panel("document.querySelector('.nw-compose textarea').value==='Добавь пояснение к выделенному коду' && document.querySelector('.nw-context').textContent.includes('main.ts')"),'selection edit draft');assert.equal(await panel("document.querySelector('[aria-label=\"Режим агента\"]').value"),'agent');await screenshot('selection-edit');
 await panel("[...document.querySelectorAll('.nw-nav button')].find(b=>b.textContent==='История').click()");await until(()=>panel("!!document.querySelector('.nw-history-item')"),'new history page');await screenshot('history');
 await panel("document.querySelector('[aria-label=\"Настройки подключения\"]').click()");await until(()=>panel("!!document.querySelector('.nw-page form')"),'new settings page');await screenshot('settings');assert(await panel("[...document.querySelectorAll('.nw-page input')].every(n=>n.getBoundingClientRect().right<=innerWidth+1)"),'Settings overflow');
 assert.equal(await panel("!!document.querySelector('.app-shell,.studio-shell,.composer,.agent-panel')"),false,'Old UI is mounted');
 for(const [theme,label] of [['forest','Лесная'],['parchment','Парчовая'],['twilight','Сумеречная']]){
  await panel(`{const select=document.querySelector('[aria-label="Тема приложения"]');Object.getOwnPropertyDescriptor(HTMLSelectElement.prototype,'value').set.call(select,'${theme}');select.dispatchEvent(new Event('change',{bubbles:true}));}`);
  await until(()=>panel(`document.documentElement.dataset.leshyTheme==='${theme}'`),'panel theme '+theme);
  await until(async()=>{const r=await cdp.send('Runtime.evaluate',{expression:"getComputedStyle(document.querySelector('.monaco-workbench')).getPropertyValue('--vscode-editor-background').trim()",returnByValue:true},mainPage.session);return r.result.value===({forest:'#171d16',parchment:'#f1e5cd',twilight:'#171d2d'})[theme];},'native editor theme '+theme);
  await until(()=>desktop(`document.documentElement.dataset.leshyTheme==='${theme}'`),'IDE to Chat theme '+theme);
  await delay(600);await screenshot('leshy-'+theme);
  // Inspect native terminal and command picker in every theme, with real keyboard navigation.
  for(const type of ['keyDown','keyUp'])await cdp.send('Input.dispatchKeyEvent',{type,key:'`',code:'Backquote',modifiers:2,windowsVirtualKeyCode:192},mainPage.session);
  await delay(700);await screenshot('leshy-terminal-'+theme);
  assert.equal((await cdp.send('Runtime.evaluate',{expression:"!!document.querySelector('.part.panel:not(.hidden) .terminal-wrapper')",returnByValue:true},mainPage.session)).result.value,true,'Native terminal rendered');
  for(const type of ['keyDown','keyUp'])await cdp.send('Input.dispatchKeyEvent',{type,key:'`',code:'Backquote',modifiers:2,windowsVirtualKeyCode:192},mainPage.session);
  for(const type of ['keyDown','keyUp'])await cdp.send('Input.dispatchKeyEvent',{type,key:'P',code:'KeyP',modifiers:10,windowsVirtualKeyCode:80},mainPage.session);
  await delay(300);await screenshot('leshy-commands-'+theme);
  for(const type of ['keyDown','keyUp'])await cdp.send('Input.dispatchKeyEvent',{type,key:'Escape',code:'Escape',windowsVirtualKeyCode:27},mainPage.session);
  const treeRow=(await cdp.send('Runtime.evaluate',{expression:"(()=>{const n=[...document.querySelectorAll('.part.sidebar .monaco-list-row')].find(n=>n.textContent.includes('main.ts'));if(!n)return null;const r=n.getBoundingClientRect();return {x:r.x+Math.min(70,r.width/2),y:r.y+r.height/2}})()",returnByValue:true},mainPage.session)).result.value;assert(treeRow,'File row available for native menu review');
  for(const type of ['mousePressed','mouseReleased'])await cdp.send('Input.dispatchMouseEvent',{type,...treeRow,button:'right',clickCount:1},mainPage.session);
  await until(async()=>(await cdp.send('Runtime.evaluate',{expression:"[...document.querySelectorAll('.monaco-menu')].some(n=>n.getBoundingClientRect().width>0)",returnByValue:true},mainPage.session)).result.value,'native file menu');
  // Let native scale/opacity entrance animations settle before the visual capture.
  await new Promise(resolve=>setTimeout(resolve,400));
  const menuStyles=(await cdp.send('Runtime.evaluate',{expression:`(()=>{const n=[...document.querySelectorAll('.monaco-menu')].find(n=>n.getBoundingClientRect().width>0);return [...n.querySelectorAll('.action-label')].slice(0,3).map(label=>{const ancestors=[];for(let p=label;p&&p!==document.body;p=p.parentElement){const s=getComputedStyle(p);ancestors.push({class:p.className,opacity:s.opacity,color:s.color,background:s.backgroundColor})}return {text:label.textContent,ancestors}})})()`,returnByValue:true},mainPage.session)).result.value;
  fs.writeFileSync(path.join(output,'leshy-menu-'+theme+'.json'),JSON.stringify(menuStyles,null,2));await screenshot('leshy-menu-'+theme);
  for(const type of ['keyDown','keyUp'])await cdp.send('Input.dispatchKeyEvent',{type,key:'Escape',code:'Escape',windowsVirtualKeyCode:27},mainPage.session);


 }

 await panel("document.querySelector('.nw').style.width='240px'");await delay(100);
 assert(await panel("[...document.querySelectorAll('.nw-header button,.nw-nav button,.nw-page input,.nw-page select')].every(n=>n.getBoundingClientRect().right<=document.querySelector('.nw').getBoundingClientRect().right+1)"),'Narrow agent controls overflow');
 await screenshot('leshy-agent-narrow');await panel("document.querySelector('.nw').style.width=''");
 await panel("{const f=document.querySelector('.nw-page input[list=\"nw-models\"]');Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(f,'unsaved-model');f.dispatchEvent(new Event('input',{bubbles:true}));}");await until(()=>panel("!!document.querySelector('.nw-unsaved')"),'unsaved settings warning');assert(await semanticBorder('.nw-unsaved','--status-warning'),'Unsaved changes keep their warning rail');
 await panel("window.__configureBeforeDelay=window.lca.configureModel;window.lca.configureModel=()=>new Promise(resolve=>{window.__releaseSave=resolve;});document.querySelector('.nw-page form').requestSubmit();");
 await until(()=>panel("!!window.__releaseSave"),'delayed connection save');
 assert(await panel("[...document.querySelectorAll('.nw-page form input,.nw-page form select')].every(n=>n.matches(':disabled'))"),'Connection inputs must lock while saving to preserve newer drafts');
 await panel("window.__releaseSave({ok:false,error:'Fixture save rejection'});window.lca.configureModel=window.__configureBeforeDelay;");
 await until(()=>panel("!!document.querySelector('.nw-error') && !document.querySelector('.nw-page form input').matches(':disabled')"),'failed save unlocked');
 assert.equal(await panel("document.querySelector('input[list=\"nw-models\"]').value"),'unsaved-model','Failed save must retain editable draft');
 await panel("[...document.querySelectorAll('.nw-nav button')].find(b=>b.textContent==='Диалог').click()");assert.match(await panel("document.querySelector('.nw-model').textContent"),/neutral-integration/);assert.doesNotMatch(await panel("document.querySelector('.nw-model').textContent"),/unsaved-model/);
 assert.equal(await panel("document.querySelector('.nw-compose textarea').value"),'Добавь пояснение к выделенному коду','Settings navigation preserves the unsent editor draft');
 // Project a damaged recovery state through loadChat, retaining the real Core's
 // rejection of the deliberately nonexistent journal. No tool effect is replayed.
 await panel("window.__loadBeforeRecovery=window.lca.loadChat;window.__copyBeforeRecovery=window.lca.copyTaskDiagnostics;window.__diagnostics=[];window.lca.copyTaskDiagnostics=async report=>{window.__diagnostics.push(report);return {ok:true};};window.lca.loadChat=async(...args)=>{const r=await window.__loadBeforeRecovery(...args);return {...r,active_run:null,task:{...r.task,chat_id:r.chat.id,status:'paused',run_state:'needs_attention',journal_id:'f'.repeat(32),recovery_error:'sensitive-fixture-marker',snapshot_attention:[{id:'e'.repeat(32),status:'unknown'}],recovery_items:[{call_id:'d'.repeat(32),message_index:1,tool:'write_file',path:'main.ts',summary:'sensitive-fixture-marker'}]}};};");
 await panel("[...document.querySelectorAll('.nw-nav button')].find(b=>b.textContent==='История').click()");await panel("document.querySelector('.nw-history-item').click()");
 await until(()=>panel("!!document.querySelector('.nw-compose')"),'recovery chat loaded');await panel("[...document.querySelectorAll('.nw-nav button')].find(b=>b.textContent==='Работа').click()");
 assert(await panel("document.body.innerText.includes('Журнал действий недоступен') && document.body.innerText.includes('Результат отката неизвестен')"));
 await panel("document.querySelector('.nw-recovery').scrollIntoView({block:'start'})");await screenshot('recovery-blockers');
 assert(await panel("[...document.querySelectorAll('button')].find(b=>b.textContent==='Продолжить задачу').disabled"),'Recovery blocks resume');
 await panel("document.querySelector('.nw-copy-diagnostics').click()");await until(()=>panel("window.__diagnostics.length===1 && document.body.innerText.includes('Диагностика скопирована')"),'diagnostic export');
 const diagnostic=JSON.parse((await panel('window.__diagnostics'))[0]);assert.equal(diagnostic.schema,'leshy.recovery.v1');assert.equal(diagnostic.recovery.journal_unreadable,true);assert.doesNotMatch(JSON.stringify(diagnostic),/sensitive-fixture-marker|main.ts/);
 await panel("[...document.querySelectorAll('button')].find(b=>b.textContent==='Не выполнялось').click()");await panel("[...document.querySelectorAll('.nw-confirm button')].find(b=>b.textContent==='Подтвердить наблюдение').click()");
 await until(()=>panel("document.body.innerText.includes('Наблюдение не сохранено')"),'recovery rejection retained');assert(await panel("!!document.querySelector('.nw-confirm')"),'Failed confirmation must stay reviewable');await panel("document.querySelector('.nw-confirm').scrollIntoView({block:'center'})");await screenshot('recovery-diagnostics');
 await panel("window.lca.loadChat=window.__loadBeforeRecovery;window.lca.copyTaskDiagnostics=window.__copyBeforeRecovery;");
 await panel("[...document.querySelectorAll('.nw-nav button')].find(b=>b.textContent==='История').click()");await panel("document.querySelector('.nw-history-item').click()");await until(()=>panel("!!document.querySelector('.nw-compose')"),'real task restored');
 await panel("[...document.querySelectorAll('.nw-nav button')].find(b=>b.textContent==='История').click()");await panel("[...document.querySelectorAll('.nw-row-actions button')].find(b=>b.textContent==='Название').click()");
 await panel("{const f=document.querySelector('[aria-label=\"Новое название\"]');Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(f,'Проверка новой истории');f.dispatchEvent(new Event('input',{bubbles:true}));}");await delay(100);await panel("document.querySelector('.nw-history-row form').requestSubmit()");await until(()=>panel("document.querySelector('.nw-history-item strong').textContent==='Проверка новой истории'"),'rename persisted');
 await panel("[...document.querySelectorAll('.nw-row-actions button')].find(b=>b.textContent==='Удалить').click()");assert.equal((await panel("window.lca.listChats('ide')")).chats.length,1,'Delete requires confirmation');assert(await semanticBorder('.nw-confirm','--status-warning'),'Deletion confirmation keeps its warning border');
 await panel("[...document.querySelectorAll('.nw-confirm button')].find(b=>b.textContent==='Подтвердить удаление').click()");await until(async()=>(await panel("window.lca.listChats('ide')")).chats.length===0,'chat deletion');assert(fs.readFileSync(path.join(project,'main.ts'),'utf8').includes('inline suggestion'),'Delete chat changed project file');



 // Close all editor tabs and verify the actual native empty-editor mark.
 await cdp.send('Input.dispatchKeyEvent',{type:'keyDown',key:'k',code:'KeyK',modifiers:2,windowsVirtualKeyCode:75},mainPage.session);
 await cdp.send('Input.dispatchKeyEvent',{type:'keyUp',key:'k',code:'KeyK',modifiers:2,windowsVirtualKeyCode:75},mainPage.session);
 await cdp.send('Input.dispatchKeyEvent',{type:'keyDown',key:'w',code:'KeyW',modifiers:2,windowsVirtualKeyCode:87},mainPage.session);
 await cdp.send('Input.dispatchKeyEvent',{type:'keyUp',key:'w',code:'KeyW',modifiers:2,windowsVirtualKeyCode:87},mainPage.session);
 for(const theme of ['forest','parchment','twilight']){
  await desktop(`window.lca.setAppearanceTheme('${theme}')`);
  await until(()=>panel(`document.documentElement.dataset.leshyTheme==='${theme}'`),'Chat to IDE theme '+theme);
  await delay(700);
  const mark=await cdp.send('Runtime.evaluate',{expression:"(()=>{const n=document.querySelector('.editor-group-container.empty .letterpress');return n&&getComputedStyle(n,'::before').maskImage.includes('leshy-mark.svg')&&n.getBoundingClientRect().width>0})()",returnByValue:true},mainPage.session);assert.equal(mark.result.value,true,'Native empty editor emblem visible');
  const clean=await cdp.send('Runtime.evaluate',{expression:"!document.body.innerText.includes('installation appears to be corrupt')",returnByValue:true},mainPage.session);assert.equal(clean.result.value,true,'Native integrity check');
  const scene=await cdp.send('Runtime.evaluate',{expression:"getComputedStyle(document.querySelector('.editor-group-watermark-wrapper'),'::before').backgroundImage",returnByValue:true},mainPage.session);assert(scene.result.value.includes('leshy-'+theme+'.webp'),'Theme-specific native scene');
  await screenshot('leshy-empty-'+theme);
 }
 await win.webContents.reload();await until(()=>desktop("document.documentElement.dataset.leshyTheme==='twilight'"),'shared theme after reload');
 await finish();
 }catch(error){await finish(error);}});});
setTimeout(()=>void finish(Error('Stage19 overall timeout')),120000).unref();
server.listen(0,'127.0.0.1',()=>require(path.join(root,'apps/desktop/dist-electron/main.cjs')));
