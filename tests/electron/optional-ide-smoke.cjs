// Real optional IDE UI/Core integration in disposable profiles and repositories.
const {app,BrowserWindow,dialog}=require('electron');
const fs=require('node:fs'),path=require('node:path'),http=require('node:http'),assert=require('node:assert/strict'),{spawnSync}=require('node:child_process');
app.disableHardwareAcceleration();
const root=path.resolve(__dirname,'../..'),output=path.join(root,'.test-data/sopt');fs.mkdirSync(output,{recursive:true});
const data=fs.mkdtempSync(path.join(output,'profile-')),project=fs.mkdtempSync(path.join(output,'project-'));
const python=process.env.LCA_TEST_PYTHON||path.join(root,'.venv-test/Scripts/python.exe');
process.env.LCA_PYTHON=python;process.env.LOCALAPPDATA=data;app.setPath('userData',path.join(data,'electron'));
BrowserWindow.prototype.show=function(){};BrowserWindow.prototype.loadURL=function(){return this.loadFile(path.join(root,'apps/desktop/dist/index.html'));};
dialog.showOpenDialog=async()=>({canceled:false,filePaths:[project]});dialog.showMessageBox=async()=>({response:1});
fs.writeFileSync(path.join(project,'main.py'),'def main():\n    print("hello")\n');
fs.writeFileSync(path.join(project,'.env'),'SYNTHETIC_FIXTURE_SECRET=not-a-real-key\n');
for(const args of [['init'],['add','.'],['-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','-m','Initial']]){
  const r=spawnSync(process.env.LCA_GIT||'git',args,{cwd:project,encoding:'utf8',windowsHide:true});assert.equal(r.status,0,r.stderr||r.error?.message);
}
let win,finished=false,requests=[];
const fixture=http.createServer((req,res)=>{let raw='';req.on('data',part=>raw+=part);req.on('end',()=>{
  if(req.method==='GET'){res.writeHead(404);res.end();return;}
  requests.push(JSON.parse(raw));res.writeHead(200,{'Content-Type':'application/json'});res.end(JSON.stringify({choices:[{message:{content:'main.py:1 — точка входа'},finish_reason:'stop'}],usage:{prompt_tokens:80,completion_tokens:12}}));
});});
async function js(code){return win.webContents.executeJavaScript(code,true);}
async function poll(expression,timeout=12000){const start=Date.now();while(Date.now()-start<timeout){if(await js(expression))return;await new Promise(r=>setTimeout(r,70));}throw Error('Timeout: '+expression);}
async function click(selector){await js(`document.querySelector(${JSON.stringify(selector)}).click()`);await new Promise(r=>setTimeout(r,50));}
async function button(text){await js(`Array.from(document.querySelectorAll('.optional-ide-dialog button')).find(b=>b.textContent.trim()===${JSON.stringify(text)}).click()`);await new Promise(r=>setTimeout(r,50));}
async function input(selector,value){await js(`{const n=document.querySelector(${JSON.stringify(selector)});Object.getOwnPropertyDescriptor(n.tagName==='TEXTAREA'?HTMLTextAreaElement.prototype:HTMLInputElement.prototype,'value').set.call(n,${JSON.stringify(value)});n.dispatchEvent(new Event('input',{bubbles:true}));}`);await new Promise(r=>setTimeout(r,60));}
async function save(){await button('Сохранить возможности');await poll("document.querySelector('.optional-ide-dialog [role=status]')?.textContent.includes('Настройки сохранены')");}
async function capture(name){await js('new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))');await new Promise(r=>setTimeout(r,150));fs.writeFileSync(path.join(output,name+'.png'),(await win.webContents.capturePage(undefined,{stayHidden:true})).toPNG());}
async function finish(error){if(finished)return;finished=true;if(error){try{await capture('failure');fs.writeFileSync(path.join(output,'failure.txt'),await js('document.body.innerText'));}catch{}}
  fs.writeFileSync(path.join(output,'result.json'),JSON.stringify({ok:!error,error:error?.stack||null,requests:requests.length,project,data},null,2));console.log(error?error.stack:'Optional IDE GUI passed: research, LSP, worktrees, Docker availability, compact/light dialog');fixture.close();app.exit(error?1:0);
}
process.on('uncaughtException',finish);process.on('unhandledRejection',finish);
app.on('browser-window-created',(_,window)=>{win=window;win.webContents.setBackgroundThrottling(false);win.webContents.once('did-finish-load',async()=>{try{
  await poll("!!window.lca&&document.querySelector('.status')?.textContent.includes('Готов')");
  const config=await js(`window.lca.configureModel({base_url:'http://127.0.0.1:${fixture.address().port}/v1',model:'fixture',api_key:''})`);assert.ok(config.ok);
  await click('.mode-tabs [role=tab]:first-child');await click('.project-pill');await poll("document.querySelector('.project-pill')?.textContent.includes('project-')");
  await js("Array.from(document.querySelectorAll('.file-row')).find(b=>b.textContent.includes('main.py')).click()");await poll("document.querySelector('.editor-tab')?.textContent.includes('main.py')||document.querySelector('.editor-tabs')?.textContent.includes('main.py')");
  await click('[title="Дополнительные возможности IDE"]');await poll("!!document.querySelector('.optional-ide-dialog[open] input')");
  assert.ok(await js("Array.from(document.querySelectorAll('.optional-ide-dialog input[type=checkbox]')).every(i=>!i.checked)"));
  await input('[aria-label="Вопрос исследователю"]','main');assert.equal(await js("Array.from(document.querySelectorAll('.optional-ide-dialog button')).find(b=>b.textContent==='Исследовать · один запрос').disabled"),true);
  await click('[aria-label="Включить research"]');await save();await button('Исследовать · один запрос');await poll("document.querySelector('.optional-result')?.textContent.includes('точка входа')");
  assert.equal(requests.length,1);assert.equal(requests[0].tools,undefined);await capture('research');
  await button('Диагностика');await input('[aria-label="Программа LSP"]',python);await input('[aria-label="Аргументы LSP"]','-u\n'+path.join(root,'tests/fixtures/lsp_diagnostics.py'));await click('[aria-label="Включить lsp"]');await save();
  await button('Проверить сохранённый файл');await poll("document.querySelector('.optional-diagnostic')?.textContent.includes('Fixture warning')");assert.equal(fs.readFileSync(path.join(project,'main.py'),'utf8'),'def main():\n    print("hello")\n');await capture('lsp');
  await button('Рабочие копии');await click('[aria-label="Включить worktrees"]');await save();await button('Создать рабочую копию');assert.equal(await js("document.querySelectorAll('.optional-result').length"),0);await button('Подтвердить создание');await poll("document.querySelector('.optional-result')?.textContent.includes('Пробная задача')");
  const catalog=await js("window.lca.runOptionalIde({action:'worktree_list'})");assert.ok(catalog.ok);assert.equal(catalog.worktrees.length,1);const tree=catalog.worktrees[0];
  fs.writeFileSync(path.join(tree.path,'manual.txt'),'keep manual');await button('Удалить чистую копию');await button('Подтвердить удаление');await poll("document.querySelector('.optional-ide-dialog [role=status]')?.textContent.includes('изменения или новые файлы')");assert.ok(fs.existsSync(path.join(tree.path,'manual.txt')));fs.unlinkSync(path.join(tree.path,'manual.txt'));
  await button('Удалить чистую копию');await button('Подтвердить удаление');await poll("document.querySelectorAll('.optional-result').length===0");assert.equal(fs.existsSync(tree.path),false);
  await button('Изоляция');await button('Проверить Docker');await poll("!!document.querySelector('.optional-ide-dialog [role=status]')");await capture('container');assert.equal(requests.length,1);
  win.setSize(1050,680);await js("localStorage.setItem('localagent.appearance.v1',JSON.stringify({theme:'light',accent:'rose'}));window.dispatchEvent(new Event('appearance-changed'))");await poll("document.querySelector('.app-shell').dataset.theme==='light'");await poll("getComputedStyle(document.querySelector('.optional-ide-dialog')).backgroundColor==='rgb(237, 242, 245)'");await capture('compact-light');
  assert.ok(await js("(()=>{const b=document.querySelector('.optional-ide-dialog>footer button:last-child'),r=b.getBoundingClientRect();return r.bottom<=innerHeight&&document.elementFromPoint(r.x+r.width/2,r.y+r.height/2)?.closest('button')===b;})()"),'Dialog footer must be reachable');
  await button('Рабочие копии');await button('Создать рабочую копию');await button('Подтвердить создание');await poll("document.querySelector('.optional-result')?.textContent.includes('Пробная задача')");
  const opened=(await js("window.lca.runOptionalIde({action:'worktree_list'})")).worktrees[0];await button('Открыть в IDE');await poll(`document.querySelector('.project-pill')?.title===${JSON.stringify(opened.path)}`);
  await poll("!document.querySelector('.optional-ide-dialog[open]')");await new Promise(r=>setTimeout(r,200));
  await click('[title="Дополнительные возможности IDE"]');await poll("!!document.querySelector('.optional-ide-dialog[open]')");await button('Рабочие копии');await button('Обновить копии');await poll("!!document.querySelector('.optional-result')");
  await js("document.querySelector('.workspace-access-settings').open=true");
  await input('[aria-label="Разрешённые защищённые файлы"]','.env');await button('Сохранить доступ модели');
  assert.deepEqual((await js('window.lca.workspaceAccess()')).exceptions,[]);
  await click('[aria-label="Подтвердить доступ модели к защищённым файлам"]');await button('Сохранить доступ модели');
  await poll("document.querySelector('.workspace-access-settings [role=status]')?.textContent.includes('сохранены')");assert.deepEqual((await js('window.lca.workspaceAccess()')).exceptions,['.env']);
  assert.equal(await js("document.querySelector('.optional-ide-dialog').matches(':modal')"),true);
  await js("document.querySelector('[aria-label=\"Разрешённые защищённые файлы\"]').scrollIntoView({block:'center'})");
  assert.ok(await js("(()=>{const n=document.querySelector('[aria-label=\"Разрешённые защищённые файлы\"]'),r=n.getBoundingClientRect();return document.elementFromPoint(r.x+r.width/2,r.y+r.height/2)===n})()"),'Access form must actually be reachable in the modal');
  await capture('access-policy');await input('[aria-label="Разрешённые защищённые файлы"]','');await button('Сохранить доступ модели');
  await poll("(async()=>{const r=await window.lca.workspaceAccess();return r.ok&&!r.exceptions.length})()");
  await click('[aria-label="Закрыть возможности IDE"]');await poll("!document.querySelector('.optional-ide-dialog[open]')");await finish();
}catch(error){await finish(error);}});});
fixture.listen(0,'127.0.0.1',()=>require('../../apps/desktop/dist-electron/main.cjs'));
