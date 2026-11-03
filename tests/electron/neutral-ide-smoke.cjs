// Real Neutral launcher/Core/named-pipe boundary in a disposable desktop profile.
const {app,BrowserWindow,dialog,ipcMain}=require('electron');
const fs=require('node:fs'),path=require('node:path'),net=require('node:net'),assert=require('node:assert/strict'),{spawnSync}=require('node:child_process');
app.disableHardwareAcceleration();app.commandLine.appendSwitch('legacy-ide');
const root=path.resolve(__dirname,'../..'),output=path.join(root,'.test-data/stage18-desktop');fs.mkdirSync(output,{recursive:true});
const data=fs.mkdtempSync(path.join(output,'profile-')),project=fs.mkdtempSync(path.join(output,'project-'));
process.env.LCA_PYTHON=path.join(root,'.venv-test/Scripts/python.exe');process.env.LOCALAPPDATA=data;app.setPath('userData',path.join(data,'electron'));
BrowserWindow.prototype.show=function(){};dialog.showOpenDialog=async()=>({canceled:false,filePaths:[project]});
fs.writeFileSync(path.join(project,'hello.ts'),'export const neutral = true;\n');
const {sampleProcesses}=require('../../prototypes/neutral-ide/tests/processes.cjs');
let win,launch=null,done=false;const began=Date.now(),handle=ipcMain.handle.bind(ipcMain);
ipcMain.handle=(channel,handler)=>handle(channel,async(...args)=>{const result=await handler(...args);if(channel==='ide:open')launch=result;return result;});
const delay=ms=>new Promise(resolve=>setTimeout(resolve,ms));
async function js(code){return win.webContents.executeJavaScript(code,true);}
async function wait(check,label,timeout=15000){const start=Date.now();while(Date.now()-start<timeout){if(await check())return;await delay(100);}throw Error('Timeout '+label);}
async function request(connection,method,token=connection.token){return new Promise((resolve,reject)=>{const socket=net.createConnection(connection.pipe);let text='';socket.setTimeout(6000,()=>socket.destroy(Error('Pipe timeout')));socket.on('connect',()=>socket.write(JSON.stringify({method,token})+'\n'));socket.on('data',part=>text+=part);socket.on('error',reject);socket.on('end',()=>{try{resolve(JSON.parse(text));}catch(error){reject(error);}});});}
async function finish(error){if(done)return;done=true;try{if(launch?.ok&&launch.pid)spawnSync('taskkill',['/PID',String(launch.pid),'/T','/F'],{windowsHide:true,stdio:'ignore'});fs.writeFileSync(path.join(output,'result.json'),JSON.stringify({ok:!error,error:error?.stack||null,launch,data,project},null,2));console.log(error?error.stack:'Neutral IDE desktop launcher passed: visible own runtime/profile, UI, Core, auth/allowlist/dirty guards');}finally{app.once('will-quit',()=>app.exit(error?1:0));app.quit();}}
app.on('browser-window-created',(_,window)=>{win=window;window.webContents.once('did-finish-load',async()=>{try{
 await wait(()=>js("!!document.querySelector('.project-pill')"),'UI');const readyMs=Date.now()-began;const desktopTree=sampleProcesses(process.pid);
 const empty=await js('window.lca.openNeutralIde()');assert.equal(empty.ok,true);assert.ok(empty.pid); // Empty IDE does not require or silently select a root.
 await wait(()=>{const r=spawnSync('powershell.exe',['-NoProfile','-Command',`(Get-Process -Id ${empty.pid} -ErrorAction SilentlyContinue).MainWindowHandle.ToInt64()`],{encoding:'utf8',windowsHide:true});return Number(r.stdout.trim())>0;},'empty IDE window',20000);
 assert.equal((await js('window.lca.health()')).project,null);
 spawnSync('taskkill',['/PID',String(empty.pid),'/T','/F'],{windowsHide:true,stdio:'ignore'});launch=null;await delay(1200);
 await js("document.querySelector('.project-pill').click()");await wait(()=>js("!!document.querySelector('[aria-label=\"Открыть в Neutral IDE\"]:not(:disabled)')"),'project');
 await js('window.lca.setEditorDirty(true)');assert.equal((await js('window.lca.openNeutralIde()')).ok,false);await js('window.lca.setEditorDirty(false)');
 await js("document.querySelector('[aria-label=\"Открыть в Neutral IDE\"]').click()");await wait(()=>launch?.ok,'own IDE launch');
 const descriptor=path.join(data,'electron/neutral-ide/connection.json'),connection=JSON.parse(fs.readFileSync(descriptor,'utf8'));
 const status=await request(connection,'status');assert.equal(status.ok,true);assert.equal(status.project,project);assert.equal(status.service,'Neutral Core');assert.equal(Object.keys(status).sort().join(','),'ok,project,prototype,service');
 assert.equal((await request(connection,'set_project')).ok,false);assert.equal((await request(connection,'status','bad')).ok,false);assert.equal((await request(connection,'focus')).ok,true);
 const settings=JSON.parse(fs.readFileSync(path.join(data,'electron/neutral-ide/user-data/User/settings.json'),'utf8'));assert.equal(settings['workbench.colorTheme'],'Neutral Studio');assert.equal(settings['telemetry.telemetryLevel'],'off');
 await wait(()=>Promise.resolve(fs.existsSync(path.join(data,'electron/neutral-ide/user-data/logs'))),'Code-OSS initialized',20000);
 await wait(()=>{const result=spawnSync('powershell.exe',['-NoLogo','-NoProfile','-NonInteractive','-Command',`(Get-Process -Id ${launch.pid} -ErrorAction SilentlyContinue).MainWindowHandle.ToInt64()`],{encoding:'utf8',windowsHide:true,timeout:5000});return result.status===0&&Number(result.stdout.trim())>0;},'visible IDE window',12000);
 fs.writeFileSync(path.join(output,'launcher.png'),(await win.webContents.capturePage(undefined,{stayHidden:true})).toPNG());
 fs.writeFileSync(path.join(output,'startup.json'),JSON.stringify({desktop_renderer_ms:readyMs,desktop_process_metrics:app.getAppMetrics(),process_tree:desktopTree},null,2));
 await finish();
 }catch(error){await finish(error);}});});
setTimeout(()=>void finish(Error('Stage18 desktop timeout')),60000).unref();
require(path.join(root,'apps/desktop/dist-electron/main.cjs'));
