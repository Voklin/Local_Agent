const vscode=require('vscode'),assert=require('node:assert/strict'),fs=require('node:fs/promises'),path=require('node:path');
const lf=text=>text.replaceAll('\r\n','\n');
const delay=ms=>new Promise(resolve=>setTimeout(resolve,ms));
async function until(action,label,timeout=30000){const start=Date.now();let last;while(Date.now()-start<timeout){try{const result=await action();if(result)return result;}catch(error){last=error;}await delay(200);}throw Error('Timeout: '+label+(last?' В· '+last.message:''));}
async function run(){
 const root=vscode.workspace.workspaceFolders[0].uri.fsPath,out=process.env.NEUTRAL_IDE_TEST_REPORT,checks=[];
 async function check(name,action){const start=Date.now();await action();checks.push({name,ok:true,ms:Date.now()-start});await fs.writeFile(out,JSON.stringify({status:'running',vscode:vscode.version,checks},null,2));}
 try{
  const extension=vscode.extensions.getExtension('neutral.neutral-agent');assert(extension,'Neutral extension missing');const api=await extension.activate();
  await check('builtin-brand-theme-local-vsix',async()=>{
   assert.equal(vscode.workspace.getConfiguration('workbench').get('colorTheme'),'Neutral Studio');
   const themes=extension.packageJSON.contributes.themes;assert(themes.some(x=>x.label==='Neutral Studio'));
   assert.deepEqual(await vscode.commands.executeCommand('neutral.probe'),{host:true,version:vscode.version});
  });
  const uri=name=>vscode.Uri.file(path.join(root,name));
  await check('tabs-split-save-undo',async()=>{
   const doc=await vscode.workspace.openTextDocument(uri('safe.txt'));await vscode.window.showTextDocument(doc,vscode.ViewColumn.One);
   const other=await vscode.workspace.openTextDocument(uri('other.txt'));await vscode.window.showTextDocument(other,vscode.ViewColumn.Two);assert(vscode.window.tabGroups.all.length>=2);
   await vscode.window.showTextDocument(doc,vscode.ViewColumn.One);const snapshot=await api.capture(doc,'replacement\n');await api.apply(snapshot);assert(doc.isDirty);assert.equal(lf(doc.getText()),'replacement\n');
   await vscode.commands.executeCommand('undo');assert.equal(lf(doc.getText()),'original\n');
   const fresh=await api.capture(doc,'saved\n');await api.apply(fresh);assert(await doc.save());assert.equal(lf(await fs.readFile(doc.uri.fsPath,'utf8')),'saved\n');
  });
  await check('stale-buffer-disk-and-outside-workspace-guards',async()=>{
   const doc=await vscode.workspace.openTextDocument(uri('safe.txt'));await vscode.window.showTextDocument(doc,vscode.ViewColumn.One);
   const snapshot=await api.capture(doc,'must not apply\n');const edit=new vscode.WorkspaceEdit();edit.insert(doc.uri,new vscode.Position(0,0),'draft ');assert(await vscode.workspace.applyEdit(edit));await assert.rejects(()=>api.apply(snapshot));assert(doc.getText().startsWith('draft '));
   await vscode.commands.executeCommand('undo');assert(!doc.isDirty);const diskSnapshot=await api.capture(doc,'must not overwrite\n');await fs.writeFile(doc.uri.fsPath,'external\n');await assert.rejects(()=>api.apply(diskSnapshot));assert.equal(await fs.readFile(doc.uri.fsPath,'utf8'),'external\n');
   // A dirty buffer must survive an external writer; never call save/overwrite.
   await until(async()=>doc.getText()==='external\n','file reload');const next=new vscode.WorkspaceEdit();next.insert(doc.uri,new vscode.Position(0,0),'my draft ');await vscode.workspace.applyEdit(next);await fs.writeFile(doc.uri.fsPath,'another external\n');await assert.rejects(()=>api.capture(doc,'replacement'));assert(doc.getText().startsWith('my draft '));
   assert.equal(await fs.readFile(doc.uri.fsPath,'utf8'),'another external\n');await vscode.commands.executeCommand('workbench.action.files.revert');
   const outside=await vscode.workspace.openTextDocument(vscode.Uri.file(path.join(path.dirname(root),'outside.txt')));await assert.rejects(()=>api.capture(outside,'no'));
  });
  await check('native-core-adapter-files-and-stale-buffers',async()=>{
   const crypto=require('node:crypto'),native=api.nativeWorkspace,sha=text=>crypto.createHash('sha256').update(text).digest('hex');
   async function operation(name,args,extra={}){
    let raw=null;try{raw=await fs.readFile(path.join(root,args.path));}catch(error){if(error.code!=='ENOENT'&&error.code!=='EISDIR')throw error;}
    const content=name==='write_file'?args.content:extra.content;
    const preview={path:args.path,exists:raw!==null,...extra,snapshot:{sha256:raw?sha(raw):null,source:{sha256:raw?sha(raw):null},...(content!==undefined?{proposed_sha256:sha(content)}:{}),...(name==='create_directory'?{directories:[args.path]}:{})}};
    const message={name,args,preview};preview.editor_state=(await native.prepare(root,message)).editor_state;return message;
   }
   await fs.writeFile(path.join(root,'native.txt'),'old\r\n');const doc=await vscode.workspace.openTextDocument(uri('native.txt'));await vscode.window.showTextDocument(doc,vscode.ViewColumn.One);
   let message=await operation('write_file',{path:'native.txt',content:'new\r\n',overwrite:true});let result=await native.apply(root,message);assert(result.ok,JSON.stringify(result));assert.equal(await fs.readFile(doc.uri.fsPath,'utf8'),'new\r\n');
   await vscode.commands.executeCommand('undo');assert.equal(doc.getText(),'old\r\n');assert(doc.isDirty);assert(await doc.save());
   message=await operation('patch_file',{path:'native.txt',old_text:'old',new_text:'patched'},{content:'patched\r\n'});result=await native.apply(root,message);assert(result.ok,JSON.stringify(result));
   message=await operation('write_file',{path:'native.txt',content:'never',overwrite:true});const dirty=new vscode.WorkspaceEdit();dirty.insert(doc.uri,new vscode.Position(0,0),'draft ');await vscode.workspace.applyEdit(dirty);await assert.rejects(()=>native.apply(root,message));assert(doc.getText().startsWith('draft '));await vscode.commands.executeCommand('undo');assert(!doc.isDirty);
   message=await operation('write_file',{path:'native.txt',content:'never',overwrite:true});await fs.writeFile(doc.uri.fsPath,'external\n');await assert.rejects(()=>native.apply(root,message));await until(()=>doc.getText()==='external\n','native reload');
   message=await operation('create_directory',{path:'native-dir'});assert((await native.apply(root,message)).ok);
   message=await operation('write_file',{path:'native-dir/new.ts',content:'export const created = true;\n'});result=await native.apply(root,message);assert(result.ok,JSON.stringify(result));
   message=await operation('rename_file',{path:'native-dir/new.ts',destination:'native-dir/renamed.ts'},{destination:'native-dir/renamed.ts'});result=await native.apply(root,message);assert(result.ok,JSON.stringify(result));assert.equal(await fs.readFile(path.join(root,'native-dir/renamed.ts'),'utf8'),'export const created = true;\n');
   message=await operation('delete_file',{path:'native-dir/renamed.ts'});result=await native.apply(root,message);assert(result.ok,JSON.stringify(result));await assert.rejects(()=>fs.stat(path.join(root,'native-dir/renamed.ts')));
   await assert.rejects(()=>native.safePath(root,'../outside.txt'));
  });
  await check('typescript-completion-definition-references-rename-diagnostics',async()=>{
   const doc=await vscode.workspace.openTextDocument(uri('main.ts'));await vscode.window.showTextDocument(doc,vscode.ViewColumn.One);
   await until(async()=>{const defs=await vscode.commands.executeCommand('vscode.executeDefinitionProvider',doc.uri,new vscode.Position(1,14));return defs?.length;},'definition',45000);
   const refs=await vscode.commands.executeCommand('vscode.executeReferenceProvider',doc.uri,new vscode.Position(0,16));assert(refs.length>=2);
   const rename=await vscode.commands.executeCommand('vscode.executeDocumentRenameProvider',doc.uri,new vscode.Position(0,16),'welcome');assert(rename.size>0);
   const completions=await vscode.commands.executeCommand('vscode.executeCompletionItemProvider',doc.uri,new vscode.Position(2,3));assert(completions.items.some(x=>(typeof x.label==='string'?x.label:x.label.label)==='greet'));
   await until(()=>vscode.languages.getDiagnostics(doc.uri).some(x=>x.severity===vscode.DiagnosticSeverity.Error),'TS diagnostic');
  });
  await check('openvsx-theme-snippets-and-prettier',async()=>{
   const theme=vscode.extensions.getExtension('dracula-theme.theme-dracula');assert(theme.packageJSON.contributes.themes.length);
   await vscode.workspace.getConfiguration('workbench').update('colorTheme','Dracula Theme',vscode.ConfigurationTarget.Workspace);assert.equal(vscode.workspace.getConfiguration('workbench').get('colorTheme'),'Dracula Theme');await vscode.workspace.getConfiguration('workbench').update('colorTheme','Neutral Studio',vscode.ConfigurationTarget.Workspace);
   const snippets=vscode.extensions.getExtension('dsznajder.es7-react-js-snippets');assert(snippets.packageJSON.contributes.snippets.length);let definitions=0;for(const item of snippets.packageJSON.contributes.snippets){const parsed=JSON.parse(await fs.readFile(path.join(snippets.extensionPath,item.path),'utf8'));definitions+=Object.keys(parsed).length;}assert(definitions>50);
   const snippetEntry=snippets.packageJSON.contributes.snippets.find(x=>x.language==='javascriptreact');assert(snippetEntry);const snippetDefinitions=JSON.parse(await fs.readFile(path.join(snippets.extensionPath,snippetEntry.path),'utf8'));const snippetName=Object.keys(snippetDefinitions)[0];
   const snippetDoc=await vscode.workspace.openTextDocument(uri('snippet.jsx'));await vscode.window.showTextDocument(snippetDoc,vscode.ViewColumn.One);await vscode.commands.executeCommand('editor.action.insertSnippet',{langId:'javascriptreact',name:snippetName});assert(snippetDoc.getText().length>10);await vscode.commands.executeCommand('workbench.action.files.revert');
   const formatter=vscode.extensions.getExtension('esbenp.prettier-vscode');await formatter.activate();const doc=await vscode.workspace.openTextDocument(uri('format.js'));await vscode.window.showTextDocument(doc,vscode.ViewColumn.One);
   await vscode.workspace.getConfiguration('editor',doc.uri).update('defaultFormatter','esbenp.prettier-vscode',vscode.ConfigurationTarget.Workspace);
   const edits=await until(async()=>{const edits=await vscode.commands.executeCommand('vscode.executeFormatDocumentProvider',doc.uri,{tabSize:2,insertSpaces:true});return edits?.length?edits:null;},'prettier formatting');const edit=new vscode.WorkspaceEdit();edit.set(doc.uri,edits);await vscode.workspace.applyEdit(edit);assert(doc.getText().includes('const foo = {'));assert(await doc.save());
  });
  await check('openvsx-yaml-language-server',async()=>{
   const extension=vscode.extensions.getExtension('redhat.vscode-yaml');await extension.activate();const doc=await vscode.workspace.openTextDocument(uri('invalid.yaml'));await vscode.window.showTextDocument(doc,vscode.ViewColumn.One);
   await until(()=>vscode.languages.getDiagnostics(doc.uri).some(x=>x.severity===vscode.DiagnosticSeverity.Error),'YAML diagnostic',45000);
  });
  await check('terminal-pty-command',async()=>{
   const marker=path.join(root,'terminal-result.txt'),terminal=vscode.window.createTerminal({name:'Neutral PTY probe',shellPath:'powershell.exe',shellArgs:['-NoLogo','-NoProfile']});
   assert(await terminal.processId);terminal.sendText("[IO.File]::WriteAllText('"+marker.replaceAll("'","''")+"', 'pty-ok')");await until(async()=>{try{return await fs.readFile(marker,'utf8')==='pty-ok';}catch{return false;}},'terminal marker');terminal.dispose();
  });
  await check('openvsx-debugpy-real-breakpoint',async()=>{
   const extension=vscode.extensions.getExtension('ms-python.debugpy');assert(extension);await extension.activate();let stop=null,terminated=false;
   const tracker=vscode.debug.registerDebugAdapterTrackerFactory('debugpy',{createDebugAdapterTracker:()=>({onDidSendMessage:message=>{if(message.type==='event'&&message.event==='stopped')stop=message.body;if(message.type==='event'&&message.event==='terminated')terminated=true;}})});
   const breakpoint=new vscode.SourceBreakpoint(new vscode.Location(uri('debug.py'),new vscode.Position(2,0)));vscode.debug.addBreakpoints([breakpoint]);
   try{
    assert(await vscode.debug.startDebugging(vscode.workspace.workspaceFolders[0],{type:'debugpy',request:'launch',name:'Neutral DAP probe',program:uri('debug.py').fsPath,python:process.env.NEUTRAL_IDE_TEST_PYTHON,console:'internalConsole',justMyCode:true}));
    await until(()=>stop,'DAP stopped',45000);assert.equal(stop.reason,'breakpoint');const session=vscode.debug.activeDebugSession;assert(session);
    const stack=await session.customRequest('stackTrace',{threadId:stop.threadId});assert(stack.stackFrames.length);const scopes=await session.customRequest('scopes',{frameId:stack.stackFrames[0].id});assert(scopes.scopes.length);const variables=await session.customRequest('variables',{variablesReference:scopes.scopes[0].variablesReference});assert(variables.variables.some(x=>x.name==='value'));
    await session.customRequest('continue',{threadId:stop.threadId});await until(()=>terminated,'DAP terminated');
   }finally{vscode.debug.removeBreakpoints([breakpoint]);if(!terminated)await vscode.debug.stopDebugging();tracker.dispose();}
  });
  await fs.writeFile(out,JSON.stringify({status:'passed',vscode:vscode.version,checks},null,2));
 }catch(error){await fs.writeFile(out,JSON.stringify({status:'failed',vscode:vscode.version,checks,error:error.stack},null,2));throw error;}
}
module.exports={run};
