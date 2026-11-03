const vscode=require('vscode'),fs=require('node:fs/promises'),path=require('node:path'),crypto=require('node:crypto');
const {AgentClient}=require('./client.cjs'),workspace=require('./workspace.cjs');
function registerAgentView(context){
 const themeLabels={forest:'LESHY Лесная',parchment:'LESHY Парчовая',twilight:'LESHY Сумеречная'};
 let applyingTheme=false;
 async function applyWorkbenchTheme(theme){const label=themeLabels[theme];if(!label||vscode.workspace.getConfiguration('workbench').get('colorTheme')===label)return;applyingTheme=true;try{await vscode.workspace.getConfiguration('workbench').update('colorTheme',label,vscode.ConfigurationTarget.Global);}finally{applyingTheme=false;}}
 context.subscriptions.push(vscode.window.onDidChangeActiveColorTheme(()=>{if(applyingTheme||!client)return;const name=vscode.workspace.getConfiguration('workbench').get('colorTheme');const theme=Object.keys(themeLabels).find(id=>themeLabels[id]===name);if(theme)void client.invoke('appearance:set',[theme]);}));
 let webview=null,client=null,disposed=false,pendingEdit=null,completionBusy=false;const prepared=new Map(),virtual=new Map();let root=vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
 context.subscriptions.push(vscode.workspace.onDidChangeWorkspaceFolders(()=>{const folders=vscode.workspace.workspaceFolders||[];if(!folders.some(folder=>folder.uri.fsPath===root)){client?.dispose();client=null;root=folders[0]?.uri.fsPath;pendingEdit=null;prepared.clear();void vscode.commands.executeCommand('workbench.action.webview.reloadWebviewAction');}}));
 context.subscriptions.push(vscode.workspace.registerTextDocumentContentProvider('neutral-agent-diff',{provideTextDocumentContent:uri=>virtual.get(uri.toString())||''}));
 function errorResult(error){return {ok:false,error:error.message||String(error)};}
 const ensure=()=>{if(!root)throw Error('Откройте папку проекта');if(!client)client=new AgentClient(root,async event=>{
  if(event.event==='appearance_theme')await applyWorkbenchTheme(event.theme);
  if(event.event==='ide_editor'){
   let result;try{if(event.phase==='guard'){const files=workspace.dirty(root);result=files.length?{ok:false,code:'DIRTY_BUFFER',error:'Сохраните черновики перед командой'}:{ok:true};}else result=await (event.phase==='prepare'?workspace.prepare:workspace.apply)(root,event);}catch(error){result=errorResult(error);}
   if(result.ok&&event.phase==='prepare'){prepared.set(event.preview.path,event);if(prepared.size>10)prepared.delete(prepared.keys().next().value);}if(event.phase==='apply')prepared.delete(event.preview.path);
   await client.result(event.operation_id,result);return;
  }
  if(event.event==='backend_stopped')client?.dispose();
  await webview?.postMessage({event});
 });return client;};
 context.subscriptions.push(vscode.window.registerWebviewViewProvider('neutral.agentView',{resolveWebviewView:async view=>{
  disposed=false;webview=view.webview;webview.options={enableScripts:true,localResourceRoots:[vscode.Uri.joinPath(context.extensionUri,'ui')]};
  if(!root){
   const nonce=crypto.randomBytes(16).toString('hex'),mark=(await fs.readFile(path.join(context.extensionPath,'icon.svg'),'utf8')).replace('<svg ','<svg aria-hidden="true" ');
   const art=webview.asWebviewUri(vscode.Uri.joinPath(context.extensionUri,'ui/spot-birch-painted.webp'));
   const band=webview.asWebviewUri(vscode.Uri.joinPath(context.extensionUri,'ui/motif-border.svg'));
   const corner=webview.asWebviewUri(vscode.Uri.joinPath(context.extensionUri,'ui/motif-corner.svg'));
   const botanical=`<img class="spot" alt="" aria-hidden="true" src="${art}">`;

   webview.html=`<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src ${webview.cspSource}; style-src 'nonce-${nonce}'; script-src 'nonce-${nonce}'"><style nonce="${nonce}">*{box-sizing:border-box}html,body{margin:0;min-width:0}body{font-family:var(--vscode-font-family);color:var(--vscode-foreground);padding:16px;line-height:1.6}.spot{object-fit:contain;display:block;width:100%;max-width:220px;height:150px;margin:24px auto;opacity:1}.brand{position:relative;padding-bottom:18px;border-bottom:1px solid var(--vscode-panel-border);display:flex;align-items:center;gap:12px;margin:8px 0 28px;color:var(--vscode-button-background)}.brand svg{width:36px;height:36px;flex:none}.brand span{font:16px Georgia,serif;letter-spacing:1px}.brand::after{content:'';position:absolute;bottom:-4px;left:calc(50% - 32px);width:64px;height:8px;background:var(--vscode-button-background);mask:url('${band}') center/32px 8px repeat-x}button{position:relative}button::after{content:'';position:absolute;right:2px;bottom:2px;width:10px;height:10px;background:currentColor;mask:url('${corner}') center/contain no-repeat;opacity:.5;pointer-events:none}h1{font-size:22px;line-height:1.3}p{font-size:13px;color:var(--vscode-descriptionForeground)}button{display:block;width:100%;margin:12px 0;padding:10px;border:0;border-radius:5px;background:var(--vscode-button-background);color:var(--vscode-button-foreground);cursor:pointer}button:focus-visible{outline:2px solid var(--vscode-focusBorder)}small{display:block;font-size:12px;margin-top:20px;color:var(--vscode-descriptionForeground)}#recent{background:var(--vscode-button-secondaryBackground);color:var(--vscode-button-secondaryForeground);border:1px solid var(--vscode-input-border)}</style></head><body><div class="brand">${mark}<span>ЛЕШИЙ / LESHY</span></div><h1>Ваш редактор готов</h1><p>Открывайте файлы, терминал и расширения. Чтобы агент мог работать с кодом, откройте папку здесь, в IDE.</p><button id="folder">Открыть папку</button><button id="recent">Недавние проекты</button>${botanical}<small>Папка определяет доступ агента к файлам. Пока она не открыта, агент не получает доступ к диску.</small><script nonce="${nonce}">const api=acquireVsCodeApi();document.getElementById('folder').onclick=()=>api.postMessage({action:'folder'});document.getElementById('recent').onclick=()=>api.postMessage({action:'recent'});</script></body></html>`;
   const listener=webview.onDidReceiveMessage(async message=>{if(message?.action==='folder')await vscode.commands.executeCommand('workbench.action.files.openFolder');else if(message?.action==='recent')await vscode.commands.executeCommand('workbench.action.openRecent');});
   view.onDidDispose(()=>{disposed=true;webview=null;listener.dispose();});return;
  }
  try{
   const nonce=crypto.randomBytes(16).toString('hex'),base=vscode.Uri.joinPath(context.extensionUri,'ui');let html=await fs.readFile(path.join(context.extensionPath,'ui/ide.html'),'utf8');
   html=html.replace(/(?:src|href)="\.\/([^"#]+)"/g,(match,file)=>match.slice(0,match.indexOf('=')+1)+'"'+webview.asWebviewUri(vscode.Uri.joinPath(base,file))+'"');
   html=html.replace('<head>','<head><meta http-equiv="Content-Security-Policy" content="default-src \'none\'; script-src '+webview.cspSource+' \'nonce-'+nonce+'\'; style-src '+webview.cspSource+' \'unsafe-inline\'; img-src '+webview.cspSource+' data:; media-src data: blob:; connect-src \'none\';">');webview.html=html;
  }catch{webview.html='<h2>Леший</h2><p>Панель не собрана. Обновите ресурсы Neutral IDE после npm run build.</p>';return;}
  const subscription=webview.onDidReceiveMessage(async message=>{
   if(disposed||typeof message?.id!=='string'||typeof message.channel!=='string'||!Array.isArray(message.args))return;
   let result;try{
    const bridge=ensure();
    if(message.channel==='ide:edit-draft'){result={ok:true,draft:pendingEdit};pendingEdit=null;}
    else if(message.channel==='ide:editor-context'){
     const editor=vscode.window.activeTextEditor;if(!editor||editor.document.uri.scheme!=='file')throw Error('Откройте файл в редакторе');
     const relative=path.relative(root,editor.document.uri.fsPath);await workspace.safePath(root,relative);
     if(editor.document.isDirty)throw Error('Сохраните файл перед добавлением контекста');
     result={ok:true,path:relative.split(path.sep).join('/'),start:editor.selection.start.line+1,end:editor.selection.end.line+1};
    }
    else if(message.channel==='ide:copy-diagnostics'){
     const report=message.args[0];if(typeof report!=='string'||report.length>10000||JSON.parse(report).schema!=='leshy.recovery.v1')throw Error('Некорректная диагностика');
     await vscode.env.clipboard.writeText(report);result={ok:true};
    }
    else if(message.channel==='ide:shell')result={ok:true,native_default:false};
    else if(message.channel==='workspace:list'){const scope=await bridge.connect();result={ok:true,projects:[],selected:scope.project_id};}
    else if(message.channel==='editor:dirty')result={ok:true};
    else if(message.channel==='editor:confirm-discard')result={ok:true,discard:!workspace.dirty(root).length};
    else if(message.channel==='optional:open-worktree'){
     result=await bridge.invoke('optional:run',[{action:'worktree_open',id:message.args[0]}]);if(result.ok){await vscode.commands.executeCommand('vscode.openFolder',vscode.Uri.file(result.path),{forceNewWindow:true});result={ok:true,root:result.path,name:path.basename(result.path)};}
    }
    else if(message.channel==='project:choose'){
     const selected=await vscode.window.showOpenDialog({canSelectFiles:false,canSelectFolders:true,canSelectMany:false,openLabel:'Открыть проект'});if(selected?.[0]){await vscode.commands.executeCommand('vscode.openFolder',selected[0],{forceNewWindow:true});result={ok:true,root:selected[0].fsPath,name:path.basename(selected[0].fsPath)};}else result={ok:true,canceled:true};
    }
    else if(message.channel==='ide:preview-diff'){
     const proposal=prepared.get(message.args[0]);if(!proposal)throw Error('Предложение устарело');
     const file=await workspace.safePath(root,proposal.preview.path),proposed=vscode.Uri.parse('neutral-agent-diff:/'+crypto.randomUUID()+'/'+path.basename(file));virtual.set(proposed.toString(),proposal.name==='write_file'?proposal.args.content:proposal.preview.content||'');
     let original=vscode.Uri.file(file);if(!proposal.preview.exists){original=vscode.Uri.parse('neutral-agent-diff:/'+crypto.randomUUID()+'/empty');virtual.set(original.toString(),'');}
     if(virtual.size>20)virtual.delete(virtual.keys().next().value);await vscode.commands.executeCommand('vscode.diff',original,proposed,'Леший · '+proposal.preview.path);result={ok:true};
    }
    else if(message.channel==='ide:open-file'){
     const file=await workspace.safePath(root,message.args[0]),line=Math.max(0,Number(message.args[1]||1)-1);const doc=await vscode.workspace.openTextDocument(vscode.Uri.file(file));await vscode.window.showTextDocument(doc,{viewColumn:vscode.ViewColumn.One,selection:new vscode.Range(line,0,line,0)});result={ok:true};
    }else if(message.channel==='chat:export'){
     result=await bridge.invoke('ide:export-chat',message.args);if(result.ok){const uri=await vscode.window.showSaveDialog({saveLabel:'Сохранить разговор',defaultUri:vscode.Uri.file(path.join(root,'LESHY-chat.'+result.extension))});if(uri){await vscode.workspace.fs.writeFile(uri,Buffer.from(result.content,'utf8'));result={ok:true};}else result={ok:true,canceled:true};}
    }else{
     if(['task:start','snapshot:apply'].includes(message.channel)&&workspace.dirty(root).length)throw Error('Сохраните несохранённые файлы проекта перед запуском или откатом.');
     result=await bridge.invoke(message.channel,message.args);
    }
   }catch(error){result=errorResult(error);}
   if(result?.ok&&['appearance:get','appearance:set'].includes(message.channel))await applyWorkbenchTheme(result.theme);
   if(!disposed)await webview.postMessage({id:message.id,result});
  });
  view.onDidDispose(()=>{disposed=true;webview=null;subscription.dispose();});
 }},{webviewOptions:{retainContextWhenHidden:true}}));
 context.subscriptions.push(vscode.commands.registerCommand('neutral.editSelection',async()=>{
  const editor=vscode.window.activeTextEditor;
  if(!root||!editor||editor.document.uri.scheme!=='file')return vscode.window.showInformationMessage('Откройте файл рабочей папки');
  const document=editor.document,version=document.version,relative=path.relative(root,document.uri.fsPath),selection=editor.selection;
  try{await workspace.safePath(root,relative);if(document.isDirty)throw Error('Сохраните файл перед правкой агентом');
   const instruction=await vscode.window.showInputBox({title:'Neutral · Правка кода',prompt:'Что изменить в выделенном коде? Правка будет показана для подтверждения.'});if(!instruction?.trim())return;
   if(document.version!==version||document.isDirty)throw Error('Файл изменился: выделите код повторно');
   pendingEdit={prompt:instruction,context:{path:relative.split(path.sep).join('/'),start:selection.start.line+1,end:selection.end.line+1}};
   await vscode.commands.executeCommand('workbench.view.extension.neutral');await webview?.postMessage({event:{event:'ide_edit_ready'}});
  }catch(error){vscode.window.showWarningMessage(error.message);}
 }));
 context.subscriptions.push(vscode.languages.registerInlineCompletionItemProvider({scheme:'file'},{provideInlineCompletionItems:async(document,position,trigger,token)=>{
  if(!root||!vscode.workspace.isTrusted||completionBusy||token.isCancellationRequested)return [];
  if(trigger.triggerKind!==vscode.InlineCompletionTriggerKind.Invoke&&!vscode.workspace.getConfiguration('neutral').get('completion.automatic',false))return [];
  const version=document.version,relative=path.relative(root,document.uri.fsPath);
  try{completionBusy=true;await workspace.safePath(root,relative);await new Promise(resolve=>setTimeout(resolve,350));if(token.isCancellationRequested||document.version!==version)return [];
   completionBusy=true;const text=document.getText(),offset=document.offsetAt(position);
   const result=await ensure().invoke('ide:complete',[{path:relative,prefix:text.slice(Math.max(0,offset-6000),offset),suffix:text.slice(offset,offset+2000)}]);
   if(token.isCancellationRequested||document.version!==version)return [];
   if(!result.ok){if(trigger.triggerKind===vscode.InlineCompletionTriggerKind.Invoke)vscode.window.showInformationMessage(result.error);return [];}
   return result.text?[new vscode.InlineCompletionItem(result.text,new vscode.Range(position,position))]:[];
  }catch{return [];}finally{completionBusy=false;}
 }}));
 context.subscriptions.push(vscode.commands.registerCommand('neutral.openMain',()=>ensure().focus()));
 context.subscriptions.push(vscode.commands.registerCommand('neutral.reconnect',async()=>{client?.dispose();client=null;await vscode.commands.executeCommand('workbench.action.webview.reloadWebviewAction');}));
 let changedTimer;
 function notifyChanges(){if(!client||disposed)return;clearTimeout(changedTimer);changedTimer=setTimeout(()=>void client.invoke('ide:workspace-changed').catch(()=>{}),350);}
 context.subscriptions.push(vscode.workspace.onDidSaveTextDocument(doc=>{if(root&&vscode.workspace.getWorkspaceFolder(doc.uri)?.uri.fsPath===root)notifyChanges();}));
 for(const event of [vscode.workspace.onDidCreateFiles,vscode.workspace.onDidRenameFiles,vscode.workspace.onDidDeleteFiles])context.subscriptions.push(event(()=>notifyChanges()));
 context.subscriptions.push({dispose:()=>clearTimeout(changedTimer)});
 context.subscriptions.push({dispose:()=>client?.dispose()});
 return {get client(){return client;}};
}
module.exports={registerAgentView};
