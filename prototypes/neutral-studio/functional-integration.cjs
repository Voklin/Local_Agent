// Isolated renderer/main/stdio/agent/MCP integration; never touches the user profile.
const {app,BrowserWindow,dialog,ipcMain}=require('electron');
const fs=require('node:fs'),path=require('node:path'),http=require('node:http'),assert=require('node:assert/strict');
app.disableHardwareAcceleration();
const root=path.resolve(__dirname,'../..'),output=path.join(__dirname,'artifacts/functional-integration');fs.mkdirSync(output,{recursive:true});
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
async function selectIdeConversation(){await click(".functional-history-toggle");await poll("!!document.querySelector('.conversation-open')");await click(".conversation-open");await poll("!document.querySelector('#ide-agent-conversations')&&!document.querySelector('[title=\"Новый чат\"]').disabled");if(!(await js("!!document.querySelector('.progress-drawer')")))await click(".progress-toggle");}
async function textButton(selector,text){await js(`Array.from(document.querySelectorAll(${JSON.stringify(selector)})).find(b=>b.textContent.trim()===${JSON.stringify(text)}).click()`);}
async function input(selector,value){await js(`{const node=document.querySelector(${JSON.stringify(selector)});Object.getOwnPropertyDescriptor(node.tagName==='TEXTAREA'?HTMLTextAreaElement.prototype:HTMLInputElement.prototype,'value').set.call(node,${JSON.stringify(value)});node.dispatchEvent(new Event('input',{bubbles:true}));}`);}
async function capture(name){fs.writeFileSync(path.join(output,name+'-layout.json'),JSON.stringify(await js(`({height:innerHeight,mode:document.querySelector('.app-shell')?.className,selected:document.querySelector('[aria-selected=true]')?.textContent,rects:Object.fromEntries(['.agent-panel','.chat-messages','.composer','.neutral-welcome','.activity-bar'].map(s=>[s,document.querySelector(s)?.getBoundingClientRect().toJSON()]))})`),null,2));await js('new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))');await currentWindow.webContents.capturePage(undefined,{stayHidden:true});await new Promise(r=>setTimeout(r,150));fs.writeFileSync(path.join(output,name+'.png'),(await currentWindow.webContents.capturePage(undefined,{stayHidden:true})).toPNG());}
async function finish(error){if(stopping)return;stopping=true;if(error){try{await capture('failure');fs.writeFileSync(path.join(output,'failure-dom.txt'),await js('document.body.innerText'));}catch{}}
  fs.writeFileSync(path.join(output,'result.json'),JSON.stringify({ok:!error,error:error?.stack||null,requests:requests.length,data,project},null,2));console.log(error?error.stack:'Neutral GUI integration passed');fixture.close();try{await js('window.lca.setEditorDirty(false)');}catch{}app.exit(error?1:0);
}
process.on('uncaughtException',finish);process.on('unhandledRejection',finish);
app.on('browser-window-created',(_,win)=>{currentWindow=win;win.webContents.on('console-message',(_event,_level,message)=>{if(/error|undefined|defined/i.test(message))console.log('Renderer:',message);});const originalSend=win.webContents.send.bind(win.webContents);win.webContents.send=(channel,message)=>{if(channel==='core:event'&&message.event==='approval')lastApprovalEvent=message;return originalSend(channel,message);};win.webContents.setBackgroundThrottling(false);win.webContents.once('did-finish-load',async()=>{try{
  await poll("!!window.lca&&document.querySelector('.neutral-welcome')&&document.querySelector('.status')?.textContent.includes('Готов')");
  assert.equal(await js('document.title'),'Neutral · функциональный прототип');assert.equal(await js('typeof window.lca.getIDEWorkflow'),'undefined');
  assert.equal(await js('typeof window.lca.resolveToolRecovery'),'function');
  await capture('welcome');
  assert.ok(await js("document.querySelector('.composer').getBoundingClientRect().bottom<=innerHeight"),'Composer must remain inside the visible window');
  await click('[title="Создать проект"]');await input('[aria-label="Название проекта"]','Нейтральный проект');await input('[aria-label="Инструкции проекта"]','В этом проекте отвечай кратко и по-русски.');
  await textButton('.workspace-dialog button','Выбрать');await poll("document.querySelector('.folder-picker input').value.length>0");await click('.save-workspace');
  await poll("!document.querySelector('.workspace-dialog')&&document.querySelector('#workspace-select').selectedOptions[0].text==='Нейтральный проект'");
  await click('[title="Настройки модели"]');await poll("!!document.querySelector('.settings-dialog')");
  await textButton('.endpoint-presets button','OpenAI API');assert.equal(await js("document.querySelector('[aria-label=\"Тип API\"]').value"),'responses');
  await input('input[name="model"]','fixture-openai');await input('[aria-label="Название подключения"]','Облако');await click('[title="Сохранить профиль"]');await poll("document.querySelector('[aria-label=\"Сохранённые подключения\"]').options.length===2");
  await textButton('.endpoint-presets button','LM Studio');await input('input[name="base_url"]',`http://127.0.0.1:${fixture.address().port}/v1`);await input('input[name="model"]','neutral-fixture');await click('.save-model-settings');await poll("document.querySelector('.settings-feedback').textContent.includes('сохранены')");await capture('settings');
  await textButton('.settings-tabs button','Расширения');await poll("!!document.querySelector('.extension-tabs')");await textButton('.extension-tabs button','Навыки');await textButton('.extension-settings button','Создать навык');
  await input('.skill-editor label:nth-of-type(1) input','Проверка Neutral');await input('.skill-editor label:nth-of-type(2) input','Повторяемая проверка интерфейса');await input('.skill-editor textarea','Сначала откройте нужный режим, затем проверьте доступность основных действий.');await textButton('.skill-editor button','Сохранить навык');await poll("!document.querySelector('.skill-editor')");await click('[aria-label="Навык Проверка Neutral"]');
  await textButton('.extension-tabs button','Субагенты');await textButton('.subagent-settings button','Создать субагента');
  await input('.subagent-editor>label:nth-of-type(1) input','Аудитор UI');await input('.subagent-editor>label:nth-of-type(2) input','Проверка профиля');await input('.subagent-editor textarea','Читай только исходники по теме задачи и указывай источники.');
  await textButton('.subagent-editor button','Сохранить профиль');await poll("!document.querySelector('.subagent-editor')");await click('[aria-label="Субагент Аудитор UI"]');await js("document.querySelector('[aria-label=\"Субагент Аудитор UI\"]').closest('.capability-card').scrollIntoView({block:'center'})");await capture('stage12-subagent-profiles');
  assert.equal(await js("document.querySelector('[aria-label=\"Субагент Аудитор UI\"]').checked"),true);
  await click('[aria-label="Использовать субагентов"]');assert.equal(await js("document.querySelector('[aria-label=\"Субагент Аудитор UI\"]').disabled"),true);await click('[aria-label="Использовать субагентов"]');
  await textButton('.extension-tabs button','MCP');await textButton('.extension-settings button','Подключить MCP сервер');
  await input('.mcp-editor .field-grid label:nth-child(1) input','Сложение');await input('.mcp-editor .field-grid label:nth-child(2) input','echo');await input('.mcp-editor>label:nth-of-type(2) input',process.env.LCA_PYTHON);await input('.mcp-editor textarea',path.join(root,'tests/fixtures/mcp_echo.py'));await textButton('.mcp-editor button','Сохранить сервер');await poll("!document.querySelector('.mcp-editor')");await textButton('.mcp-server-card button','Проверить');await poll("document.querySelector('.mcp-server-card').textContent.includes('3 инструментов')",25000);await click('[aria-label="MCP Сложение"]');await capture('mcp');
  await textButton('.settings-tabs button','Контекст и лимиты');assert.equal(await js("document.querySelector('.reset-generation').closest('.settings-section').querySelector('[aria-label=\"Управление лимитами\"]').value"),'auto');assert.equal(await js("document.querySelector('[name=context_window]')===null"),true);
  await js("{const n=document.querySelector('.reset-generation').closest('.settings-section').querySelector('[aria-label=\"Управление лимитами\"]');n.value='manual';n.dispatchEvent(new Event('change',{bubbles:true}));}");
  await textButton('[aria-label="Размер окна модели"] button','4K');assert.equal(await js("document.querySelector('[name=context_window]').value"),'4096');assert.equal(await js("document.querySelector('[name=max_tokens]').value"),'1024');
  await js("{const n=document.querySelector('.reset-generation').closest('.settings-section').querySelector('[aria-label=\"Управление лимитами\"]');n.value='auto';n.dispatchEvent(new Event('change',{bubbles:true}));}");await click('.save-model-settings');await poll("document.querySelector('.settings-feedback').textContent.includes('сохранены')");await capture('automatic-limits');
  await js("document.querySelector('.paid-budget').open=true");assert.ok(await js("document.querySelector('.paid-budget').textContent.includes('фактический счёт')"));await js("document.querySelector('.paid-budget').open=false");
  await click('[title="Закрыть настройки"]');await input('.composer textarea','Сложи 3 и 4 через MCP');await click('.send-button');await poll("document.querySelector('#approval-title')?.textContent.includes('MCP')",20000);assert.equal(await js("document.querySelector('.approval-dialog').textContent.includes('Разрешить действие')"),true);await textButton('.approval-dialog button','Разрешить действие');await poll("!document.querySelector('[title=\"Остановить\"]')&&document.querySelector('.chat-messages').textContent.includes('MCP вернул 7')",20000);
  assert.ok(requests.some(r=>r.messages[0].content.includes('В этом проекте отвечай кратко')));
  assert.ok(requests[0].tools.some(t=>t.function.name==='discover_mcp_tools'));assert.ok(!requests[0].tools.some(t=>t.function.name.startsWith('mcp_')),'Full MCP schemas must not be sent before discovery');assert.ok(requests.some(r=>r.tools?.some(t=>t.function.name.startsWith('mcp_'))));
  await poll("document.querySelectorAll('.conversation-row').length===1");await capture('chat');
  await click('.conversation-menu summary');await textButton('.conversation-actions button','Закрепить');await poll("!!document.querySelector('.conversation-open svg.lucide-pin')");
  await textButton('.conversation-actions button','Экспорт Markdown');await poll("document.querySelector('.sidebar-notice')?.textContent.includes('экспортирован')");assert.ok(fs.readFileSync(path.join(output,'conversation.md'),'utf8').includes('MCP вернул 7'));
  await textButton('.conversation-actions button','В архив');await poll("document.querySelectorAll('.conversation-row').length===0");await click('[title="Архив чатов"]');await poll("document.querySelectorAll('.conversation-row').length===1");await click('.conversation-menu summary');await textButton('.conversation-actions button','Вернуть из архива');await poll("document.querySelectorAll('.conversation-row').length===0");await click('[title="Вернуться к чатам"]');await poll("document.querySelectorAll('.conversation-row').length===1");
  await click('.conversation-menu summary');await textButton('.conversation-actions button','Создать копию');await poll("document.querySelectorAll('.conversation-row').length===2");await capture('projects');
  await click('[role="tab"]:nth-child(2)');await poll("!!document.querySelector('.main-panel .welcome')");
  const indexRequests=requests.length;fs.writeFileSync(path.join(project,'index_fixture.py'),'def indexed_greeting():\n    return 7\n');
  await click('[title="Поиск по проекту"]');await poll("document.querySelector('.index-status')?.dataset.indexState==='ready'");
  await js(`{const s=document.querySelector('[aria-label="Тип поиска по проекту"]');s.value='symbols';s.dispatchEvent(new Event('change',{bubbles:true}));}`);
  await input('[aria-label="Текст поиска по проекту"]','indexed_greeting');await js("document.querySelector('.project-search form').requestSubmit()");
  await poll("document.querySelector('.search-results')?.textContent.includes('index_fixture.py:1')");
  assert.ok(await js("document.querySelector('.search-notice').textContent.includes('по индексу')"));await capture('project-index-symbols');
  fs.writeFileSync(path.join(project,'index_fixture.py'),'def updated_greeting():\n    return 8\n');
  await poll("(async()=>{const r=await window.lca.searchProject({mode:'symbols',query:'updated_greeting'});return r.ok&&r.matches.some(m=>m.path==='index_fixture.py');})()");
  await input('[aria-label="Текст поиска по проекту"]','updated_greeting');await js("document.querySelector('.project-search form').requestSubmit()");
  await poll("document.querySelector('.search-results')?.textContent.includes('updated_greeting')");
  assert.equal(requests.length,indexRequests,'Index search/updates must not call a model');await capture('project-index-updated');
  await click('[title="Файлы проекта"]');
  await click('[title="Настройки модели"]');await textButton('.settings-tabs button','Расширения');await textButton('.extension-tabs button','Плагины');await click('[aria-label="Проверки и команды проекта"]');await click('[title="Закрыть настройки"]');
  await click('.sidebar .file-row');await poll("document.querySelector('.editor-input')?.value==='Neutral fixture'");const nodeRequests=requests.length;await input('.composer textarea','Проверь node встроенный hello.txt');await click('.send-button');await poll("document.querySelector('#approval-title')?.textContent.includes('Команда проекта')");await textButton('.approval-dialog button','Разрешить действие');await poll("!document.querySelector('[title=\"Остановить\"]')&&document.querySelector('.chat-messages').textContent.includes('Проверка Node прошла')",20000);assert.ok(requests.some(r=>r.messages.some(m=>m.role==='tool'&&m.tool_call_id==='command-node'&&JSON.parse(m.content).exit_code===0&&JSON.parse(m.content).output.includes('Neutral node OK'))));await capture('ide');
  if(!await js("!!document.querySelector('.task-progress')"))await click('.progress-toggle');
  await poll("document.querySelector('[data-verification=commands_passed]')?.textContent.includes('Команды завершились успешно')");
  assert.ok(await js("document.querySelector('.task-progress')?.textContent.includes('не подтверждает все требования')"));
  assert.ok(await js("(()=>{const note=document.querySelector('[data-verification=commands_passed]');const r=note.getBoundingClientRect();return r.width>0&&r.height>0&&r.top>=0&&r.bottom<innerHeight&&document.elementsFromPoint(r.x+r.width/2,r.y+r.height/2).some(n=>n.closest('.task-progress'));})()"),'Verification result must be visible inside the task card');
  await capture('verification');
  await click('.run-history summary');await poll("document.querySelectorAll('.run-records li').length>0");const history=await js("(async()=>{const list=await window.lca.listChats('ide');return window.lca.runHistory(list.chats[0].id);})()");assert.equal(history.runs[0].ledger.http_attempts,requests.length-nodeRequests);assert.equal(history.runs[0].tool_calls,1);assert.ok(await js("document.querySelector('.run-history').textContent.includes('Попытки HTTP: 3')"));assert.equal((await js("window.lca.runHistory('not-selected')")).ok,false);await capture('run-ledger');await click('.run-history summary');
  assert.ok(requests.some(r=>r.messages.some(m=>m.role==='user'&&m.content.includes('neutral_context_pack'))));await poll("!!document.querySelector('.context-sources')");await click('.context-sources summary');await capture('context-sources');
  await click('[aria-label="Закрыть подробности работы модели"]');await poll("!document.querySelector('.progress-drawer')");
  assert.ok(await js("document.activeElement===document.querySelector('.progress-toggle')"));
  await click('.progress-toggle');await js("document.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',bubbles:true,cancelable:true}))");await poll("!document.querySelector('.progress-drawer')");
  await click('.progress-toggle');await js("document.querySelector('.task-progress-heading').dispatchEvent(new PointerEvent('pointerdown',{bubbles:true}))");assert.ok(await js("!!document.querySelector('.progress-drawer')"));
  await js("document.querySelector('.composer textarea').dispatchEvent(new PointerEvent('pointerdown',{bubbles:true}))");await poll("!document.querySelector('.progress-drawer')");
  await click('.progress-toggle');await click('.progress-toggle');await poll("!document.querySelector('.progress-drawer')");await click('.progress-toggle');
  await click('[title="Настройки модели"]');await poll("!!document.querySelector('.settings-dialog')");await js("document.querySelector('.settings-dialog').dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',bubbles:true,cancelable:true}))");await poll("!document.querySelector('.settings-dialog')");assert.ok(await js("!!document.querySelector('.progress-drawer')"),'Escape handled by a dialog must not also close the details panel');

  await click('.context-usage summary');assert.ok(await js("document.querySelector('.context-usage').textContent.includes('Схемы инструментов')&&document.querySelector('.context-usage').textContent.includes('Сервер сообщил')"));await capture('context-usage');await click('.context-usage summary');
  let recoveryRequestCount=requests.length;
  recoveryTaskFixture={status:'paused',run_state:'needs_attention',journal_id:'neutral-ui-missing-journal',last_event:'Проверьте прерванное действие',stage:'execution',turn:1,tool_calls:2,stages:[],recovery_items:[{call_id:'ui-effect',message_index:1,tool:'write_file',path:'hello.txt',summary:'Результат записи неизвестен'}],tool_activity:[{id:1,tool:'write_file',path:'hello.txt',status:'unknown',summary:'Итог не подтверждён'},{id:2,tool:'read_file',path:'hello.txt',status:'unknown',summary:'Чтение прервано'}]};
  await selectIdeConversation();await poll("!!document.querySelector('.task-recovery')");
  assert.equal(await js("document.querySelector('.task-progress-heading>b').textContent"),'Требует проверки');
  assert.equal(await js("document.querySelector('.task-progress>button.task-resume').disabled"),true);
  assert.equal(await js("document.querySelectorAll('.task-recovery-items>li').length"),1,'Read-only unknown calls have no resolution controls');
  assert.ok(await js("document.querySelector('.task-recovery').textContent.includes('проверьте фактический файл или внешний сервис')"));
  await textButton('.task-recovery button','Действие уже выполнено');assert.equal(recoveryAttempts.length,0,'Selecting a review result must not send an RPC');
  await poll("!!document.querySelector('[aria-label=\"Подтвердите результат проверки\"]')");await textButton('.task-recovery button','Назад');
  await textButton('.task-recovery button','Действие не выполнялось');assert.equal(recoveryAttempts.length,0);await textButton('.task-recovery button','Подтвердить результат');
  await poll("document.querySelectorAll('.message.system').length>0&&document.querySelectorAll('.task-recovery button:disabled').length===0");
  assert.equal(recoveryAttempts.length,1);assert.equal(recoveryAttempts[0].params.resolution,'not_executed');assert.equal(recoveryAttempts[0].params.call_id,'ui-effect');assert.equal(recoveryAttempts[0].result.ok,false);
  assert.ok(await js(`document.querySelector('.chat-messages').textContent.includes(${JSON.stringify(recoveryAttempts[0].result.error)})`),'Recovery rejection must be visible');
  assert.equal(requests.length,recoveryRequestCount,'Review controls must not start model or tool execution');await capture('recovery-review');
  recoveryTaskFixture={...recoveryTaskFixture,run_state:'failed',recovery_items:[]};await selectIdeConversation();await poll("document.querySelector('.task-progress-heading>b')?.textContent==='Ошибка выполнения'");
  recoveryTaskFixture={...recoveryTaskFixture,run_state:'paused'};await selectIdeConversation();await poll("document.querySelector('.task-progress-heading>b')?.textContent==='Приостановлена'");assert.equal(await js("document.querySelector('.task-progress>button.task-resume').disabled"),false);
  recoveryTaskFixture=null;await selectIdeConversation();await poll("!!document.querySelector('[data-verification=commands_passed]')");
  await click('[title="Настройки модели"]');await textButton('.settings-tabs button','История и копии');
  await poll("document.querySelector('.storage-settings')?.textContent.includes('Хранилище проверено.')");
  await textButton('.storage-settings button','Сохранить резервную копию');
  await poll("document.querySelector('.storage-settings [role=status]')?.textContent.includes('Резервная копия сохранена:')");
  assert.equal(await js("document.querySelector('.settings-tabs button[aria-pressed=true]')?.textContent"),'История и копии');
  assert.ok(fs.statSync(path.join(output,'history.zip')).size>1000);await capture('storage-backup');
  await click('[title="Закрыть настройки"]');
  // Write a real interrupted journal into this smoke test's isolated profile,
  // then resolve it through renderer -> preload -> main -> Python, without a model call.
  const backendChat=await js("window.lca.listChats('ide')");
  const recoveryChat=backendChat.chats[0].id;
  const recoverySeed=[
    'import sys,json',
    'from agent.chat_store import load_chat,save_chat',
    'from agent.task_store import new_task',
    'from agent.tool_recovery import task_journal',
    'chat=load_chat(sys.argv[1]); task=new_task(chat["id"],chat["project_root"],"Проверь уже выполненную запись")',
    'tool={"id":"real-recovery","type":"function","function":{"name":"write_file","arguments":json.dumps({"path":"hello.txt","content":"Neutral fixture","overwrite":True})}}',
    'tool["function"]["name"]=sys.argv[2] if len(sys.argv)>2 else "write_file"',
    'anchor=len(chat["messages"]); journal=task_journal(task); journal.prepare_batch([tool],anchor); journal.set_phase(anchor,"real-recovery","started")',
    'chat["messages"].append({"role":"assistant","content":None,"tool_calls":[tool]});chat["task_checkpoint"]=task;save_chat(chat)',
  ].join('\n');
  const seed=require('node:child_process').spawnSync(process.env.LCA_PYTHON,['-c',recoverySeed,recoveryChat],{cwd:root,env:process.env,encoding:'utf8',windowsHide:true});
  assert.equal(seed.status,0,seed.stderr);await selectIdeConversation();await poll("!!document.querySelector('.task-recovery')");
  await textButton('.task-recovery button','Действие уже выполнено');await textButton('.task-recovery button','Подтвердить результат');
  await poll("!document.querySelector('.task-recovery')&&document.querySelector('.task-progress-heading>b')?.textContent==='Приостановлена'");
  assert.equal(recoveryAttempts.at(-1).result.ok,true);assert.equal(await js("document.querySelector('.task-progress>button.task-resume').disabled"),false);
  assert.equal(fs.readFileSync(path.join(project,'hello.txt'),'utf8'),'Neutral fixture');assert.equal(requests.length,recoveryRequestCount);
  await selectIdeConversation();await poll("!document.querySelector('.task-recovery')&&document.querySelector('.task-tools').textContent.includes('Подтверждено вами')");await capture('recovery-resolved');
  await input('.composer textarea','stage11-parent');await click('.send-button');await poll("!!document.querySelector('[title=Отправить]')&&document.querySelector('.chat-messages')?.textContent.includes('Результат ребёнка получен.')");
  if(!(await js("!!document.querySelector('.progress-drawer')")))await click('.progress-toggle');
  assert.ok(await js("document.querySelector('.child-runs')?.textContent.includes('Завершён')"));
  await js("document.querySelector('.run-history').open=true");await poll("document.querySelectorAll('.run-records>li[data-parent]').length===1");await capture('stage11-child-tree');
  await input('.composer textarea','Создай stage4 вложенный файл');await click('.send-button');
  await poll("document.querySelector('#approval-title')?.textContent.includes('Создание каталогов')");
  const beforeLater=requests.length;await textButton('.approval-dialog button','Решить позже');await poll("!document.querySelector('.approval-dialog')");
  assert.ok(await js("document.querySelector('.background-runs')?.textContent.includes('Нужно решение')"));await click('.background-runs button.selected');
  await poll("document.querySelector('#approval-title')?.textContent.includes('Создание каталогов')");assert.equal(requests.length,beforeLater);
  // Renderer fixture only; real transport consent is covered by test_task_service.
  const directoryApproval=lastApprovalEvent,previewRequests=requests.length;sourceApprovalFixture={recipient:'https://example.invalid/v1/chat/completions',model:'fixture',sources:[{path:'hello.txt',start_line:1,end_line:1,content:'Neutral fixture'}]};
  currentWindow.webContents.send('core:event',{...directoryApproval,event_seq:undefined,kind:'context',path:'Выбранные исходники',diff:JSON.stringify(sourceApprovalFixture,null,2)});
  await poll("document.querySelector('#approval-title')?.textContent.includes('Передача исходников')");assert.ok(await js("document.querySelector('.source-context-recipient').textContent.includes('example.invalid')"));await capture('context-approval');await textButton('.approval-dialog button','Не отправлять');
  await poll("!document.querySelector('.approval-dialog')");assert.equal(sourceApprovalDecisions.length,1);assert.equal(sourceApprovalDecisions[0][2],'reject');assert.equal(requests.length,previewRequests);currentWindow.webContents.send('core:event',{...directoryApproval,event_seq:undefined});
  await poll("document.querySelector('#approval-title')?.textContent.includes('Создание каталогов')");assert.ok(!fs.existsSync(path.join(project,'stage4/src')));await textButton('.approval-dialog button','Создать каталоги');
  await poll("document.querySelector('#approval-title')?.textContent.includes('Новый файл')");await textButton('.approval-dialog button','Применить изменение');
  await poll("document.querySelector('#approval-title')?.textContent.includes('Точечная правка')");assert.ok(await js("document.querySelector('.approval-dialog pre').textContent.includes('+const value = 2')"));await textButton('.approval-dialog button','Применить правку');
  await poll("!!document.querySelector('[title=\"Остановить\"]')");for(let tries=0;!releaseStage4&&tries<200;tries++)await new Promise(r=>setTimeout(r,30));assert.equal(typeof releaseStage4,'function');
  if(!await js("!!document.querySelector('.progress-drawer')"))await click('.progress-toggle');await click('[aria-label="Закрыть подробности работы модели"]');
  currentWindow.webContents.send('core:event',{event:'task_end',chat_id:recoveryChat,run_id:'stale-run-stage7'});
  currentWindow.webContents.send('core:event',{event:'remote_error',run_id:'stale-run-stage7',text:'Old remote error'});
  assert.ok(await js("!!document.querySelector('[title=\"Остановить\"]')"),'Hiding model details must not stop the active run');releaseStage4();
  await poll("!document.querySelector('[title=\"Остановить\"]')&&document.querySelector('.chat-messages').textContent.includes('Вложенный файл готов.')",20000);
  currentWindow.webContents.send('core:event',{event:'text_delta',chat_id:recoveryChat,run_id:'stale-run-stage7',message_id:'stale',text:'LATE STAGE7 TEXT'});
  await js('new Promise(r=>setTimeout(r,50))');assert.equal(await js("document.querySelector('.chat-messages').textContent.includes('LATE STAGE7 TEXT')"),false);
  assert.equal(fs.readFileSync(path.join(project,'stage4/src/demo.txt'),'utf8'),'const value = 2;\n');recoveryRequestCount=requests.length;await capture('stage4-workspace');

  if(await js("!!document.querySelector('.progress-drawer')"))await click('[aria-label="Закрыть подробности работы модели"]');
  await click('.ide-task-options>summary');await input('[aria-label="Критерии готовности"]','Содержимое файла проверено');
  await textButton('.ide-options-body button','Добавить проверку');await input('[aria-label="Назначение проверки"]','Проверить сохранённый файл');
  await input('[aria-label="Аргументы проверки"]','-e\nif(!require("node:fs").readFileSync("hello.txt","utf8").includes("stage6"))process.exit(2)');
  await js(`{const select=document.querySelector('[aria-label="Проверка критерия 1"]');select.value=select.options[1].value;select.dispatchEvent(new Event('change',{bubbles:true}));}`);
  await click('[aria-label="Проверки после правок"]');await click('.ide-task-options>summary');
  await input('.composer textarea','Сделай stage6 правку');await click('.send-button');await poll("!!document.querySelector('.approval-dialog')");await click('.approval-dialog .primary-button');
  await poll("document.querySelector('#approval-title')?.textContent.includes('Команда проекта')");assert.ok(await js("document.querySelector('.approval-dialog pre').textContent.includes('Проверить сохранённый файл')"));await textButton('.approval-dialog button','Разрешить действие');
  await poll("!document.querySelector('[title=\"Остановить\"]')&&document.querySelector('.chat-messages').textContent.includes('Правка stage6 подготовлена')",20000);
  if(!await js("!!document.querySelector('.progress-drawer')"))await click('.progress-toggle');
  await poll("!!document.querySelector('[data-criterion-status=checks_passed]')&&!!document.querySelector('.workspace-review .snapshot-card')");await capture('stage6-checks');
  await js("document.querySelector('.workspace-review .snapshot-card[data-snapshot-status=applied] button').scrollIntoView({block:'center'})");
  assert.ok(await js("(()=>{const b=document.querySelector('.workspace-review .snapshot-card[data-snapshot-status=applied] button'),r=b.getBoundingClientRect();return document.elementFromPoint(r.x+r.width/2,r.y+r.height/2)?.closest('button')===b;})()"),'Rollback controls must be reachable by a real pointer');
  await textButton('.workspace-review .snapshot-card button','Сравнить и отменить');await poll("!!document.querySelector('.rollback-preview')");
  assert.equal(fs.readFileSync(path.join(project,'hello.txt'),'utf8'),'stage6 verified');await textButton('.rollback-preview button','Подтвердить откат файлов');
  await poll("document.querySelector('.workspace-review [role=status]')?.textContent.includes('Файлы восстановлены')");
  assert.equal(fs.readFileSync(path.join(project,'hello.txt'),'utf8'),'Neutral fixture');assert.ok(await js("!!document.querySelector('[data-criterion-status=stale]')"));await capture('stage6-rollback');
  await js("document.querySelector('.workspace-review .snapshot-card[data-snapshot-status=applied] button').scrollIntoView({block:'center'})");
  assert.ok(await js("(()=>{const b=document.querySelector('.workspace-review .snapshot-card[data-snapshot-status=applied] button'),r=b.getBoundingClientRect();return document.elementFromPoint(r.x+r.width/2,r.y+r.height/2)?.closest('button')===b;})()"),'Rollback controls must be reachable by a real pointer');
  await textButton('.workspace-review .snapshot-card button','Сравнить и отменить');await poll("!!document.querySelector('.rollback-preview')");
  fs.writeFileSync(path.join(project,'stage4/src/demo.txt'),'manual change after preview');await textButton('.rollback-preview button','Подтвердить откат файлов');
  await poll("document.querySelector('.workspace-review [role=status]')?.textContent.includes('ручные изменения')");
  assert.equal(fs.readFileSync(path.join(project,'stage4/src/demo.txt'),'utf8'),'manual change after preview');await capture('stage6-conflict');
  await click('[aria-label="Закрыть подробности работы модели"]');
  await click('.ide-task-options>summary');await click('[aria-label="Агент только читает"]');await click('.ide-task-options>summary');
  await input('.composer textarea','Изучи stage6 readonly');await click('.send-button');await poll("!document.querySelector('[title=\"Остановить\"]')&&document.querySelector('.chat-messages').textContent.includes('Только чтение: изменение не выполнено')");
  assert.equal(fs.readFileSync(path.join(project,'hello.txt'),'utf8'),'Neutral fixture');assert.ok(requests.some(request=>request.messages.some(message=>message.role==='tool'&&message.tool_call_id==='stage6-write'&&JSON.parse(message.content).code==='READ_ONLY')));
  // Explicit selected-file evidence must remain usable with a tree too large for the old fingerprint.
  const scopedRequests=requests.length;
  fs.writeFileSync(path.join(project,'large.bin'),Buffer.alloc(8_000_001));fs.writeFileSync(path.join(project,'scope-config.json'),'{}');
  await click('.ide-task-options>summary');await click('[aria-label="Агент только читает"]');
  await input('[aria-label="Аргументы проверки"]','-e\nif(!require("node:fs").readFileSync("hello.txt","utf8"))process.exit(2)');
  await js(`{const s=document.querySelector('[aria-label="Область подтверждения проверки"]');s.value='files';s.dispatchEvent(new Event('change',{bubbles:true}));}`);
  await input('[aria-label="Файлы области проверки"]','hello.txt\n');await input('[aria-label="Зависимости области проверки"]','scope-config.json\n');
  await js(`document.querySelector('[aria-label="Файлы области проверки"]').scrollIntoView({block:'center'})`);await capture('scoped-options');
  await textButton('.ide-options-body button','Запустить проверки без модели');
  await poll("!!document.querySelector('.approval-dialog')");
  assert.ok(await js("document.querySelector('.approval-dialog pre').textContent.includes('только выбранные файлы')"));
  assert.ok(await js("document.querySelector('.approval-dialog pre').textContent.includes('scope-config.json')"));
  await textButton('.approval-dialog button','Разрешить действие');
  await poll("!document.querySelector('[title=\"Остановить\"]')");
  await click('.ide-task-options>summary');
  if(!await js("!!document.querySelector('.progress-drawer')"))await click('.progress-toggle');
  await poll("!!document.querySelector('[data-verification=scoped_passed]')&&!!document.querySelector('[data-check-status=scoped]')");
  assert.equal(await js("document.querySelector('.task-progress-heading>b').textContent"),'Проверены выбранные файлы');
  assert.equal(await js("document.querySelectorAll('.task-stages li[data-status=active]').length"),0,'Completed checks have no running model stages');
  assert.ok(await js("document.querySelector('.task-checks').textContent.includes('Остальной проект не сверялся')"));
  assert.equal(requests.length,scopedRequests,'Checks-only with a selected scope must not call the model');await capture('scoped-verification');
  await click('[aria-label="Закрыть подробности работы модели"]');
  const beforePlanEdit=requests.length;
  if(!(await js("!!document.querySelector('.progress-drawer')")))await click('.progress-toggle');
  await textButton('.task-graph button','Добавить план');await textButton('.graph-editor button','Добавить шаг');await input('.graph-editor fieldset input','Проверить результат вручную');await capture('stage15-plan-editor');await textButton('.graph-editor button','Сохранить план');
  await poll("!document.querySelector('.graph-editor')&&document.querySelector('.task-graph')?.textContent.includes('Проверить результат вручную')");
  assert.equal(requests.length,beforePlanEdit);assert.ok(await js("document.querySelector('.task-progress-heading')?.textContent.includes('Приостановлена')"));await capture('stage15-user-plan');
  await click('[aria-label="Закрыть подробности работы модели"]');
  recoveryRequestCount=requests.length;
  await click('[role="tab"]:nth-child(3)');await poll("!!document.querySelector('.voice-panel')");await capture('lola');
  assert.equal(await js("document.querySelector('[aria-selected=true]').textContent"),'Лола');
  await click('.new-conversation');await poll("document.querySelectorAll('.conversation-row').length===1");
  const voiceChat=(await js("window.lca.listChats('voice')")).chats[0].id;
  const voiceSeed=require('node:child_process').spawnSync(process.env.LCA_PYTHON,['-c',recoverySeed,voiceChat,'open_application'],{cwd:root,env:process.env,encoding:'utf8',windowsHide:true});
  assert.equal(voiceSeed.status,0,voiceSeed.stderr);await click('.conversation-open');await poll("!!document.querySelector('.voice-panel .task-recovery')");
  assert.equal(await js("document.querySelector('.voice-panel .task-progress>button.task-resume').disabled"),true);
  await textButton('.voice-panel .task-recovery button','Действие не выполнялось');await textButton('.voice-panel .task-recovery button','Подтвердить результат');
  await poll("!document.querySelector('.voice-panel .task-recovery')&&document.querySelector('.voice-panel .task-progress-heading>b')?.textContent==='Приостановлена'");
  assert.equal(await js("document.querySelector('.voice-panel .task-progress>button.task-resume').disabled"),false);
  assert.equal(requests.length,recoveryRequestCount);await capture('lola-recovery');

  currentWindow.setSize(1050,680);await js('new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))');assert.equal(await js('document.documentElement.scrollWidth>window.innerWidth'),false);await capture('compact');
  await click('[role="tab"]:first-child');await poll("!!document.querySelector('.neutral-welcome')");await js("localStorage.setItem('localagent.appearance.v1',JSON.stringify({theme:'light',accent:'rose'}));window.dispatchEvent(new Event('appearance-changed'))");await capture('light');
  await poll("document.querySelectorAll('.conversation-row').length===2");await click('.conversation-menu summary');await textButton('.conversation-actions button','Удалить разговор');await click('.confirm-delete');await poll("document.querySelectorAll('.conversation-row').length===1");
  await click('.workspace-edit');await textButton('.workspace-dialog button','Удалить проект');await click('.confirm-delete');await poll("document.querySelector('#workspace-select').value===''&&document.querySelectorAll('.conversation-row').length===1");assert.ok(fs.existsSync(path.join(project,'hello.txt')));
  await finish();
}catch(error){await finish(error);}});});
fixture.listen(0,'127.0.0.1',()=>require(path.join(root,'apps/desktop/dist-electron/main.cjs')));
