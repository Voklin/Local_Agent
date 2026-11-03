// Drive the visible confirmation in our disposable Code-OSS test window via CDP.
const fs=require('node:fs'),path=require('node:path'),{spawn}=require('node:child_process');
const args=process.argv.slice(2),exe=args.shift(),profile=args[args.indexOf('--user-data-dir')+1],report=process.env.NEUTRAL_IDE_TEST_REPORT;
const {sampleProcesses}=require('./processes.cjs');
const began=Date.now(),child=spawn(exe,args,{env:process.env,stdio:'inherit',windowsHide:true});let exited=false,exitCode=null;
child.on('exit',code=>{exited=true;exitCode=code;});child.on('error',error=>{throw error;});
const delay=ms=>new Promise(resolve=>setTimeout(resolve,ms));
async function until(action,label,timeout=60000){const start=Date.now();while(Date.now()-start<timeout){if(exited)throw Error('IDE exited during '+label+' · '+exitCode);try{const result=await action();if(result)return result;}catch(error){if(exited)throw error;}await delay(100);}throw Error('Timeout '+label);}
async function connect(url){const socket=new WebSocket(url),pending=new Map();let id=0;await new Promise((resolve,reject)=>{socket.onopen=resolve;socket.onerror=reject;});socket.onmessage=event=>{const result=JSON.parse(event.data),entry=pending.get(result.id);if(entry){pending.delete(result.id);result.error?entry.reject(Error(JSON.stringify(result.error))):entry.resolve(result.result);}};return {send:(method,params={})=>new Promise((resolve,reject)=>{const key=++id;pending.set(key,{resolve,reject});socket.send(JSON.stringify({id:key,method,params}));}),close:()=>socket.close()};}
(async()=>{
 let cdp,browser;
 try{
  const port=await until(()=>{const file=path.join(profile,'DevToolsActivePort');if(!fs.existsSync(file)||fs.statSync(file).mtimeMs<began)return null;return fs.readFileSync(file,'utf8').split('\n');},'CDP');
  browser=await connect('ws://127.0.0.1:'+port[0]+port[1]);
  const page=await until(async()=>{const targets=await(await fetch('http://127.0.0.1:'+port[0]+'/json/list')).json();return targets.find(x=>x.type==='page'&&x.url.includes('workbench'));},'workbench');
  cdp=await connect(page.webSocketDebuggerUrl);const evaluate=async expression=>(await cdp.send('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true})).result.value;
  await until(()=>evaluate("document.body?.innerText.includes('safe.txt')"),'first rendered editor');
  const readyMs=Date.now()-began,processInfo=await browser.send('SystemInfo.getProcessInfo');
  fs.writeFileSync(path.join(path.dirname(report),'startup.json'),JSON.stringify({codeoss_first_editor_ms:readyMs,chromium_processes:processInfo.processInfo,process_tree:sampleProcesses(child.pid)},null,2));
  await until(()=>evaluate("!!document.querySelector('.quick-input-widget input:not([type=checkbox])') && document.querySelector('.quick-input-widget').getBoundingClientRect().height>0"),'preview input',120000);
  await evaluate("document.querySelector('.quick-input-widget input:not([type=checkbox])').focus()");
  await cdp.send('Input.insertText',{text:'UI approved replacement'});await cdp.send('Input.dispatchKeyEvent',{type:'keyDown',key:'Enter',code:'Enter',windowsVirtualKeyCode:13});await cdp.send('Input.dispatchKeyEvent',{type:'keyUp',key:'Enter',code:'Enter',windowsVirtualKeyCode:13});
  await until(()=>evaluate("!!Array.from(document.querySelectorAll('.monaco-dialog-box .monaco-button')).find(x=>x.textContent.includes('Применить'))"),'apply confirmation');
  const screenshot=await cdp.send('Page.captureScreenshot',{format:'png'});fs.writeFileSync(path.join(path.dirname(report),'preview-confirmation.png'),Buffer.from(screenshot.data,'base64'));
  await evaluate("Array.from(document.querySelectorAll('.monaco-dialog-box .monaco-button')).find(x=>x.textContent.includes('Применить')).click()");
  await until(()=>{if(!fs.existsSync(report))return false;const result=JSON.parse(fs.readFileSync(report,'utf8'));if(result.status==='failed')throw Error(result.error);return result.status==='passed';},'UI report');
  await delay(500);const panelScreenshot=await cdp.send('Page.captureScreenshot',{format:'png'});fs.writeFileSync(path.join(path.dirname(report),'neutral-view.png'),Buffer.from(panelScreenshot.data,'base64'));
  await new Promise((resolve,reject)=>{const timeout=setTimeout(()=>reject(Error('Extension tests did not finish')),60000);if(exited){clearTimeout(timeout);resolve();return;}child.once('exit',()=>{clearTimeout(timeout);resolve();});});
  process.exitCode=exitCode||0;if(JSON.parse(fs.readFileSync(report,'utf8')).status!=='passed')process.exitCode=1;
 }catch(error){console.error(error.stack);if(cdp){try{const shot=await cdp.send('Page.captureScreenshot',{format:'png'});fs.writeFileSync(path.join(path.dirname(report),'ui-failure.png'),Buffer.from(shot.data,'base64'));const state=await cdp.send('Runtime.evaluate',{expression:'JSON.stringify({text:document.body.innerText,active:document.activeElement?.outerHTML})',returnByValue:true});fs.writeFileSync(path.join(path.dirname(report),'ui-failure.json'),state.result.value);}catch{}}if(!exited)child.kill();process.exitCode=1;}
 finally{cdp?.close();browser?.close();}
})();
