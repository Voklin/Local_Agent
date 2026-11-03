// Two visible chats through the real renderer/main/Core, one held HTTP stream.
const {app,BrowserWindow,ipcMain}=require('electron');
const fs=require('node:fs'),path=require('node:path'),http=require('node:http'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..'),output=path.join(__dirname,'artifacts/functional-background');
fs.mkdirSync(output,{recursive:true});
const data=fs.mkdtempSync(path.join(output,'profile-'));
process.env.LOCALAPPDATA=data;
process.env.LCA_PYTHON=path.join(root,'.venv-test/Scripts/python.exe');
app.setPath('userData',path.join(data,'electron'));app.disableHardwareAcceleration();
BrowserWindow.prototype.show=function(){};
BrowserWindow.prototype.loadURL=function(){return this.loadFile(path.join(__dirname,'.local/functional-dist/index.html'));};
let win,release,appendAlpha,deferLoad=false,stopping=false,requests=[];
const register=ipcMain.handle.bind(ipcMain);
ipcMain.handle=(channel,handler)=>register(channel,async(...args)=>{const result=await handler(...args);if(channel==='chat:load'&&deferLoad){deferLoad=false;appendAlpha();await new Promise(r=>setTimeout(r,200));}return result;});
const fixture=http.createServer(async(req,res)=>{
  if(req.method==='GET'){res.setHeader('Content-Type','application/json');res.end('{"data":[{"id":"fixture"}]}');return;}
  let body='';for await(const chunk of req)body+=chunk;
  const payload=JSON.parse(body);requests.push(payload);
  const user=payload.messages.filter(m=>m.role==='user').at(-1).content;
  if(!payload.stream){res.setHeader('Content-Type','application/json');res.end(JSON.stringify({id:'fixture',choices:[{index:0,message:{role:'assistant',content:'{}'},finish_reason:'stop'}]}));return;}
  res.writeHead(200,{'Content-Type':'text/event-stream'});
  res.write('data: '+JSON.stringify({id:'fixture',choices:[{index:0,delta:{content:user==='hold-alpha'?'alpha-part':'beta done'},finish_reason:null}]})+'\n\n');
  const done=()=>res.end('data: '+JSON.stringify({id:'fixture',choices:[{index:0,delta:{},finish_reason:'stop'}]})+'\n\ndata: [DONE]\n\n');
  if(user==='hold-alpha'){release=done;appendAlpha=()=>res.write('data: '+JSON.stringify({id:'fixture',choices:[{index:0,delta:{content:'-after-snapshot'},finish_reason:null}]})+'\n\n');}else done();
});
async function js(code){return win.webContents.executeJavaScript(code,true);}
async function poll(code){const end=Date.now()+15000;while(Date.now()<end){if(await js(code))return;await new Promise(r=>setTimeout(r,40));}throw Error('Timeout: '+code);}
async function click(selector){await js(`document.querySelector(${JSON.stringify(selector)}).click()`);await new Promise(r=>setTimeout(r,60));}
async function input(selector,value){await js(`{const n=document.querySelector(${JSON.stringify(selector)});Object.getOwnPropertyDescriptor(n.tagName==='TEXTAREA'?HTMLTextAreaElement.prototype:HTMLInputElement.prototype,'value').set.call(n,${JSON.stringify(value)});n.dispatchEvent(new Event('input',{bubbles:true}));}`);await new Promise(r=>setTimeout(r,40));}
async function finish(error){
  if(stopping)return;stopping=true;
  if(error&&win)fs.writeFileSync(path.join(output,'failure-dom.txt'),await js('document.body.innerText').catch(()=>''));
  fs.writeFileSync(path.join(output,'result.json'),JSON.stringify({ok:!error,error:error?.stack||null,requests:requests.length,data},null,2));
  console.log(error?error.stack:'Background chat GUI passed');if(release)release();fixture.close();app.exit(error?1:0);
}
process.on('uncaughtException',finish);process.on('unhandledRejection',finish);
app.on('browser-window-created',(_,window)=>{
  win=window;win.webContents.setBackgroundThrottling(false);
  win.webContents.once('did-finish-load',async()=>{try{
    await poll("!!window.lca&&document.querySelector('.status')?.textContent.includes('Готов')");
    await click('[title="Настройки модели"]');await poll("!!document.querySelector('[name=model]')");
    await input('[name=base_url]',`http://127.0.0.1:${fixture.address().port}/v1`);await input('[name=model]','fixture');
    await click('.save-model-settings');await poll("document.querySelector('.settings-feedback')?.textContent.includes('сохранены')");await click('[title="Закрыть настройки"]');
    await input('.composer textarea','hold-alpha');await js("document.querySelector('[title=Отправить]').click();document.querySelector('.new-conversation').click()");
    await poll("document.querySelector('.chat-messages')?.textContent.includes('alpha-part')&&document.querySelectorAll('.background-runs button').length===1&&!document.querySelector('.new-conversation').disabled");
    await click('.new-conversation');await poll("!!document.querySelector('[title=Отправить]')");
    await input('.composer textarea','beta');await click('[title="Отправить"]');
    await poll("document.querySelectorAll('.background-runs button').length===2&&!!document.querySelector('[title=Остановить]')");
    assert.equal(requests.length,1,'Second chat must wait without a second HTTP call');
    deferLoad=true;
    await js("{const buttons=Array.from(document.querySelectorAll('.background-runs button'));buttons.find(b=>b.textContent.includes('hold-alpha')).click();buttons.find(b=>b.textContent.includes('beta')).click();}");
    await poll("document.querySelector('.chat-messages')?.textContent.includes('alpha-part-after-snapshot')&&!!document.querySelector('.streaming-caret')");
    assert.equal(await js("document.querySelector('.chat-messages').textContent.includes('beta')"),false);
    await js('new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))');
    await win.webContents.capturePage(undefined,{stayHidden:true});await new Promise(r=>setTimeout(r,150));
    fs.writeFileSync(path.join(output,'two-chats.png'),(await win.webContents.capturePage(undefined,{stayHidden:true})).toPNG());
    await js("Array.from(document.querySelectorAll('.background-runs button')).find(b=>b.textContent.includes('beta')).click()");
    await poll("document.querySelector('.message.user .functional-markdown')?.textContent==='beta'&&!!document.querySelector('[title=Остановить]')");
    await click('[title="Остановить"]');await poll("document.querySelectorAll('.background-runs button').length===1&&!!document.querySelector('[title=Отправить]')");
    assert.equal(requests.length,1);
    await click('.background-runs button');await poll("!!document.querySelector('.streaming-caret')");
    release();release=null;
    await poll("document.querySelectorAll('.background-runs button').length===0&&!!document.querySelector('[title=Отправить]')");
    assert.equal(await js("document.querySelectorAll('.message.assistant').length"),1);
    assert.equal(await js("document.querySelector('.message.assistant .functional-markdown').textContent"),'alpha-part-after-snapshot');
    assert.equal(await js("document.documentElement.scrollWidth>innerWidth"),false);
    await finish();
  }catch(error){await finish(error);}});
});
fixture.listen(0,'127.0.0.1',()=>require('../../apps/desktop/dist-electron/main.cjs'));
