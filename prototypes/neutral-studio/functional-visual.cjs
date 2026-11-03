// Isolated renderer/main/stdio/agent/MCP integration; never touches the user profile.
const {app,BrowserWindow,dialog,ipcMain}=require('electron');
const fs=require('node:fs'),path=require('node:path'),http=require('node:http'),assert=require('node:assert/strict');
app.disableHardwareAcceleration();
const root=path.resolve(__dirname,'../..'),output=path.join(__dirname,'artifacts/functional-visual');fs.mkdirSync(output,{recursive:true});
const data=fs.mkdtempSync(path.join(output,'profile-')),project=fs.mkdtempSync(path.join(output,'project-'));
process.env.LOCALAPPDATA=data;process.env.LCA_PYTHON=process.env.LCA_TEST_PYTHON||process.env.LCA_PYTHON||(fs.existsSync(path.join(root,'.venv-test/Scripts/python.exe'))?path.join(root,'.venv-test/Scripts/python.exe'):'python');app.setPath('userData',path.join(data,'electron'));BrowserWindow.prototype.show=function(){};
BrowserWindow.prototype.loadURL=function(){return this.loadFile(path.join(__dirname,'.local/functional-dist/index.html'));};
dialog.showOpenDialog=async()=>({canceled:false,filePaths:[project]});dialog.showSaveDialog=async(_win,options)=>({canceled:false,filePath:path.join(output,options?.defaultPath?.endsWith('.zip')?'history.zip':'conversation.md')});dialog.showMessageBox=async()=>({response:1});
fs.writeFileSync(path.join(project,'hello.txt'),'Neutral fixture');
let currentWindow,stopping=false,requests=[],releaseStage4=null;
// Renderer recovery fixture only: real backend calls still validate the selected
// chat and reject the deliberately nonexistent journal. No persistence schema is mocked.
let recoveryTaskFixture=null,recoveryAttempts=[],sourceApprovalFixture=null,sourceApprovalDecisions=[],lastApprovalEvent=null;
const registerHandle=ipcMain.handle.bind(ipcMain);
ipcMain.handle=(channel,handler)=>registerHandle(channel,async(...args)=>{
  if(channel==='task:approve'&&sourceApprovalFixture){sourceApprovalDecisions.push(args.slice(1));sourceApprovalFixture=null;return {ok:true};}
  const result=await handler(...args);
  if(channel==='task:resolve-recovery')recoveryAttempts.push({params:args[1],result});
  return channel==='chat:load'&&result.ok&&recoveryTaskFixture?{...result,task:recoveryTaskFixture}:result;
});
const fixture=http.createServer((req,res)=>{let raw='';req.on('data',part=>raw+=part);req.on('end',()=>{
  if(req.method==='GET'){res.writeHead(200,{'Content-Type':'application/json'});res.end('{"data":[{"id":"neutral-fixture"}]}');return;}
  const p=JSON.parse(raw);requests.push(p);
  if(!p.stream){res.writeHead(200,{'Content-Type':'application/json'});res.end(JSON.stringify({id:'fixture',object:'chat.completion',model:'neutral-fixture',choices:[{index:0,message:{role:'assistant',content:'{}'},finish_reason:'stop'}]}));return;}
  const last=p.messages.map(m=>m.role).lastIndexOf('user');const after=p.messages.slice(last+1).some(m=>m.role==='tool');const command=p.messages[last]?.content.toLowerCase().includes('проверь node');const mcp=p.tools?.find(t=>t.function.name.startsWith('mcp_'));const discover=p.tools?.some(t=>t.function.name==='discover_mcp_tools');const calledMcp=p.messages.some(m=>m.role==='tool'&&m.tool_call_id==='mcp-add');
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
 await js("window.lca.configureModel("+JSON.stringify({base_url:'http://127.0.0.1:'+fixture.address().port+'/v1',model:'neutral-fixture',api_key:''})+")");
 // Reload picks up saved real model configuration from the temporary backend.
 await js("window.dispatchEvent(new Event('resize'))");
 for(const mode of ['chat','ide']){
  if(mode==='ide'){await click('[role=tab]:nth-child(2)');await click('.project-pill');await poll("document.querySelector('.composer textarea').placeholder==='Опишите задачу…'");}
  const config=await js('window.lca.getModelSettings()');
  // App reads settings on its dialog; apply through existing form so renderer and Core agree.
  await click('[title="Настройки Neutral"]');await input('input[name="base_url"]','http://127.0.0.1:'+fixture.address().port+'/v1');await input('input[name="model"]','neutral-fixture');await click('.save-model-settings');await poll("document.querySelector('.settings-feedback').textContent.includes('сохранены')");await textButton('.settings-actions button','Закрыть');
  for(const [sample,value] of [
   ['short','Проверь, пожалуйста, структуру проекта и кратко объясни результат.'],
   ['long','Пожалуйста, проверь интерфейс.\n\nТребования:\n- Сохрани существующие функции.\n- Объясни найденные ошибки.\n- Проверь поведение на узком окне.\n\nСсылка на локальное описание: https://example.invalid/'+ 'very-long-path/'.repeat(12)],
   ['code','Поясни этот код:\n\n'+String.fromCharCode(96).repeat(3)+'typescript\nconst title = "Neutral";\nconsole.log(title);\n'+String.fromCharCode(96).repeat(3)]
  ]){
   await click('[title="Новый чат"]');
   await input('.composer textarea',value);await click('.send-button');await poll("document.querySelectorAll('.message.assistant').length>0&&!document.querySelector('.streaming-caret')");
   for(const [width,height] of [[1280,720],[1440,900],[1920,1080]]){
    win.setContentSize(width,height);await new Promise(r=>setTimeout(r,100));
    await js("document.querySelector('.message.user').scrollIntoView({block:'start'})");
    assert.equal(await js("document.documentElement.scrollWidth>innerWidth"),false);
    assert.equal(await js("getComputedStyle(document.querySelector('.message.user .message-content')).backgroundColor"),'rgba(0, 0, 0, 0)');
    await capture(mode+'-user-'+sample+'-'+width+'x'+height);
   }
  }
 }
 await finish();
 }catch(e){await finish(e)}})});
fixture.listen(0,'127.0.0.1',()=>require('../../apps/desktop/dist-electron/main.cjs'));
