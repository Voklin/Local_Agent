// Opt-in live-model desktop acceptance. Only disposable fixture files may change.
const {app,BrowserWindow,dialog}=require('electron');
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {execFileSync}=require('node:child_process');
const root=path.resolve(__dirname,'../..');
const protocol=process.env.NEUTRAL_TEST_PROTOCOL||'native';assert.ok(['native','json'].includes(protocol));
const scenario=process.env.NEUTRAL_TEST_CASE||'repair';assert.ok(['repair','multifile'].includes(scenario));
const output=path.join(root,'artifacts/readiness',(protocol==='native'?'live-gui':'live-gui-json')+(scenario==='multifile'?'-multifile':''));fs.mkdirSync(output,{recursive:true});
const data=fs.mkdtempSync(path.join(output,'profile-')),project=fs.mkdtempSync(path.join(output,'project-'));
const inspect=process.env.NEUTRAL_INSPECT_GUI==='1';
process.env.LOCALAPPDATA=data;
process.env.LCA_PYTHON=process.env.LCA_TEST_PYTHON||path.join(root,'.venv-test/Scripts/python.exe');
app.setPath('userData',path.join(data,'electron'));app.disableHardwareAcceleration();
if(!inspect)BrowserWindow.prototype.show=function(){};
dialog.showOpenDialog=async()=>({canceled:false,filePaths:[project]});
const verification="const assert=require('node:assert/strict');const {invoice}=require('./invoice');assert.equal(invoice(100),120);assert.equal(invoice(0),0);"
  +(scenario==='multifile'?"const totals=require('./total');assert.equal(typeof totals.calculateTotal,'function');assert.equal(totals.calculateTotal(100),120);assert.equal(totals.total,undefined);":"")
  +"console.log('behavior assertions passed');\n";
fs.writeFileSync(path.join(project,'total.js'),"exports.total = subtotal => subtotal * 1.1;\n");
fs.writeFileSync(path.join(project,'invoice.js'),"const {total}=require('./total');\nexports.invoice = amount => total(amount);\n");
fs.writeFileSync(path.join(project,'verify.js'),verification);
const requirements='Invoice totals must include 20 percent tax. Run node verify.js.\n'
  +(scenario==='multifile'?'Rename the public helper export total to calculateTotal in total.js and update invoice.js to call calculateTotal. Remove the old export name; preserve the invoice API.\n':'');
fs.writeFileSync(path.join(project,'README.md'),requirements);
let win,ended=false,approval=null;const events=[],decisions=[];const started=Date.now();
async function js(code){return win.webContents.executeJavaScript(code,true);}
async function poll(expression,timeout=20000){const until=Date.now()+timeout;while(Date.now()<until){if(await js(expression))return;await new Promise(r=>setTimeout(r,80));}throw Error('Timeout: '+expression);}
async function click(selector){await js(`document.querySelector(${JSON.stringify(selector)}).click()`);await new Promise(r=>setTimeout(r,50));}
async function input(selector,value){await js(`{const n=document.querySelector(${JSON.stringify(selector)});Object.getOwnPropertyDescriptor(n.tagName==='TEXTAREA'?HTMLTextAreaElement.prototype:HTMLInputElement.prototype,'value').set.call(n,${JSON.stringify(value)});n.dispatchEvent(new Event('input',{bubbles:true}));}`);}
async function button(selector,label){await js(`Array.from(document.querySelectorAll(${JSON.stringify(selector)})).find(n=>n.textContent.trim()===${JSON.stringify(label)}).click()`);await new Promise(r=>setTimeout(r,70));}
async function capture(name){
  await js('new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))');
  await win.webContents.capturePage(undefined,{stayHidden:true});
  await new Promise(r=>setTimeout(r,150));
  fs.writeFileSync(path.join(output,name+'.png'),(await win.webContents.capturePage(undefined,{stayHidden:true})).toPNG());
}
async function finish(error){
  if(ended)return;ended=true;
  try{await capture(error?'failed':'completed');}catch{}
  const task=events.filter(e=>e.event==='task').at(-1)?.task;
  const report=JSON.stringify({passed:!error,error:error?.stack,
    model:process.env.NEUTRAL_TEST_MODEL||'ornith-1.5-9b',base_url:process.env.NEUTRAL_TEST_URL||'http://127.0.0.1:1234/v1',
    protocol,scenario,budget_mode:'auto',seconds:(Date.now()-started)/1000,project,data,decisions,task},null,2);
  fs.writeFileSync(path.join(output,'report.json'),report);fs.writeFileSync(path.join(output,'report-'+started+'.json'),report);
  fs.writeFileSync(path.join(output,'events.json'),JSON.stringify(events,null,2));
  console.log(error?error.stack:'Live Neutral desktop coding workflow PASSED');
  if(inspect&&!error){console.log('GUI retained for native visual inspection');return;}
  app.exit(error?1:0);
}
process.on('uncaughtException',finish);process.on('unhandledRejection',finish);
app.on('browser-window-created',(_,created)=>{
  win=created;win.webContents.setBackgroundThrottling(false);
  const send=win.webContents.send.bind(win.webContents);
  win.webContents.send=(channel,value)=>{if(channel==='core:event'){events.push(value);if(value.event==='approval')approval=value;}return send(channel,value);};
  win.webContents.once('did-finish-load',async()=>{try{
    await poll("!!window.lca&&document.querySelector('.status')?.textContent.includes('Готов')");
    await click('[title="Создать проект"]');await input('[aria-label="Название проекта"]','Readiness live fixture');
    await button('.workspace-dialog button','Выбрать');await poll("document.querySelector('.folder-picker input').value.length>0");
    await click('.save-workspace');await poll("!document.querySelector('.workspace-dialog')");
    await click('[title="Настройки модели"]');await input('[name=base_url]',process.env.NEUTRAL_TEST_URL||'http://127.0.0.1:1234/v1');
    await input('[name=model]',process.env.NEUTRAL_TEST_MODEL||'ornith-1.5-9b');
    await js(`{const n=document.querySelector('[aria-label="Протокол инструментов"]');Object.getOwnPropertyDescriptor(HTMLSelectElement.prototype,'value').set.call(n,${JSON.stringify(protocol)});n.dispatchEvent(new Event('change',{bubbles:true}));}`);
    await click('.save-model-settings');
    await poll("document.querySelector('.settings-feedback')?.textContent.includes('сохранены')");
    // The fixture enables only the existing command capability; approvals stay on.
    // Use the same public UI control as a user; never bypass the executor.
    await button('.settings-tabs button','Расширения');
    await poll("!!document.querySelector('[aria-label=\"Проверки и команды проекта\"]')");
    if(!await js("document.querySelector('[aria-label=\"Проверки и команды проекта\"]').checked"))await click('[aria-label="Проверки и команды проекта"]');
    await click('[title="Закрыть настройки"]');
    await click('.mode-tabs [role=tab]:first-child');await click('.ide-task-options>summary');
    await button('.ide-options-body button','Добавить проверку');await input('[aria-label="Назначение проверки"]','Verify invoice behavior');
    await input('[aria-label="Аргументы проверки"]','verify.js');await click('[aria-label="Проверки после правок"]');
    await click('.ide-task-options>summary');
    await input('.composer textarea','Сначала поручите readonly субагенту research изучить README.md и verify.js и вернуть требования к расчёту со ссылками на строки. После получения результата самостоятельно найдите причину неверного итога счёта и исправьте реализацию. Запустите существующую проверку node verify.js и проверьте результат. verify.js и README.md не изменяйте. В конце сообщите изменённые файлы и фактический результат проверки.');
    await click('.send-button');await poll("!!document.querySelector('[title=\"Остановить\"]')");
    const deadline=Date.now()+180000;
    while(await js("!!document.querySelector('[title=\"Остановить\"]')")){
      if(Date.now()>deadline){await click('[title="Остановить"]');await poll("!document.querySelector('[title=\"Остановить\"]')");throw Error('180s experiment watchdog: run cancelled, checkpoint retained');}
      if(approval&&await js("!!document.querySelector('.approval-dialog')")){
        const current=approval;approval=null;let allowed=false;
        if(['write','patch'].includes(current.kind))allowed=['total.js','invoice.js'].includes(path.basename(current.path));
        if(current.kind==='command'){
          const proposal=JSON.parse(current.diff.slice(0,current.diff.lastIndexOf('}')+1));
          allowed=[process.execPath,path.join(path.dirname(process.execPath),'node.exe')].map(p=>p.toLowerCase()).includes(path.resolve(proposal.program).toLowerCase())&&JSON.stringify(proposal.arguments)==='["verify.js"]'&&path.resolve(proposal.cwd)===project;
        }
        decisions.push({kind:current.kind,path:current.path,allowed});await capture('approval-'+decisions.length);
        if(allowed)await click('.approval-dialog .primary-button');else await button('.approval-dialog button',current.kind==='command'?'Отклонить действие':'Отклонить изменение');
      }
      await new Promise(r=>setTimeout(r,100));
    }
    assert.equal(fs.readFileSync(path.join(project,'verify.js'),'utf8'),verification,'Agent may not rewrite the oracle');
    assert.equal(fs.readFileSync(path.join(project,'README.md'),'utf8'),requirements,'Agent may not rewrite the requirements');
    if(scenario==='multifile')assert.match(fs.readFileSync(path.join(project,'invoice.js'),'utf8'),/\bcalculateTotal\b/,'Caller must use the renamed helper');
    execFileSync(process.execPath,['verify.js'],{cwd:project,env:{...process.env,ELECTRON_RUN_AS_NODE:'1'},windowsHide:true});
    const task=events.filter(e=>e.event==='task').at(-1)?.task;
    assert.equal(task.status,'completed');assert.equal(task.verification.status,'commands_passed');
    assert.ok(task.children?.some(child=>child.state==='completed'),'A real readonly child must return before parent completion');
    assert.ok(events.some(e=>e.event==='change'&&e.change.status==='applied'));
    if(scenario==='multifile')for(const file of ['total.js','invoice.js'])assert.ok(events.some(e=>e.event==='change'&&e.change.status==='applied'&&e.change.path===file),'Both source files require applied diffs: '+file);
    if(!await js("!!document.querySelector('.progress-drawer')"))await click('.progress-toggle');
    assert.equal(await js("document.querySelectorAll('.chat-messages .studio-activity').length"),0);
    await button('[aria-label="Раздел подробностей"] button','Инструменты');
    await poll("!!document.querySelector('.progress-drawer .studio-activity')");await capture('tools-tab');
    await button('[aria-label="Раздел подробностей"] button','Обзор и субагенты');
    assert.ok(await js("document.querySelector('.child-runs')?.textContent.includes('Ход работы')"));
    await finish();
  }catch(error){await finish(error);}});
});
require('../../apps/desktop/dist-electron/main.cjs');
