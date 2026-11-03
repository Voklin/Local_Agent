const vscode=require('vscode'),fs=require('node:fs/promises'),path=require('node:path'),net=require('node:net'),crypto=require('node:crypto');
const hash=text=>crypto.createHash('sha256').update(text).digest('hex');

// The MVP works with saved files only, and never writes through the Python writer.
async function capture(document,replacement){
  if(!vscode.workspace.isTrusted)throw Error('Сначала подтвердите доверие проекту в IDE');
  if(document.uri.scheme!=='file'||document.isDirty)throw Error('Сначала сохраните файл');
  if(typeof replacement!=='string'||Buffer.byteLength(replacement)>262144)throw Error('Правка превышает 256 КБ');
  const folder=vscode.workspace.getWorkspaceFolder(document.uri);if(!folder)throw Error('Файл вне проекта');
  const [root,file,disk]=await Promise.all([fs.realpath(folder.uri.fsPath),fs.realpath(document.uri.fsPath),fs.readFile(document.uri.fsPath)]);
  const relative=path.relative(root,file);if(relative.startsWith('..')||path.isAbsolute(relative))throw Error('Файл вне проекта');
  if(disk.length>262144||disk.includes(0))throw Error('Нужен текстовый файл до 256 КБ');
  if(document.isDirty||document.getText()!==disk.toString('utf8').replace(/^\uFEFF/,''))throw Error('Буфер и диск различаются. Сохраните или перечитайте файл');
  return {uri:document.uri.toString(),source_kind:'disk',document_version:document.version,buffer_hash:hash(document.getText()),disk_base_hash:hash(disk),replacement};
}
async function apply(snapshot){
  const document=await vscode.workspace.openTextDocument(vscode.Uri.parse(snapshot.uri));
  const disk=await fs.readFile(document.uri.fsPath);
  if(!vscode.workspace.isTrusted||document.isClosed||document.isDirty||document.version!==snapshot.document_version||hash(document.getText())!==snapshot.buffer_hash||hash(disk)!==snapshot.disk_base_hash)throw Error('Файл изменился. Подготовьте новую правку');
  // Revalidate workspace/symlink membership immediately before editor-owned mutation.
  const fresh=await capture(document,snapshot.replacement);
  if(fresh.document_version!==snapshot.document_version||fresh.buffer_hash!==snapshot.buffer_hash||fresh.disk_base_hash!==snapshot.disk_base_hash)throw Error('Снимок устарел');
  const edit=new vscode.WorkspaceEdit();edit.replace(document.uri,new vscode.Range(document.positionAt(0),document.positionAt(document.getText().length)),snapshot.replacement);
  if(!await vscode.workspace.applyEdit(edit,{isRefactoring:false}))throw Error('Редактор отклонил правку');
  return {ok:true,saved:false,document_version:document.version};
}
async function request(method){
  if(!process.env.NEUTRAL_IDE_CONNECTION)throw Error('Запустите IDE кнопкой из Neutral');
  const connection=JSON.parse(await fs.readFile(process.env.NEUTRAL_IDE_CONNECTION,'utf8'));
  if(typeof connection.pipe!=='string'||!connection.pipe.startsWith('\\\\.\\pipe\\neutral-ide-')||typeof connection.token!=='string')throw Error('Неверное подключение');
  return new Promise((resolve,reject)=>{
    const socket=net.createConnection(connection.pipe);let text='';
    socket.setTimeout(5000,()=>socket.destroy(Error('Neutral не отвечает')));
    socket.once('connect',()=>socket.write(JSON.stringify({token:connection.token,method})+'\n'));
    socket.on('data',chunk=>{text+=chunk.toString('utf8');if(text.length>8192)socket.destroy(Error('Invalid response'));});
    socket.once('error',reject);socket.once('end',()=>{try{resolve(JSON.parse(text));}catch(error){reject(error);}});
  });
}
function activate(context){
  const previews=new Map();
  context.subscriptions.push(vscode.workspace.registerTextDocumentContentProvider('neutral-preview',{provideTextDocumentContent:uri=>previews.get(uri.toString())||''}));
  context.subscriptions.push(vscode.commands.registerCommand('neutral.status',async()=>{
    try{const status=await request('status');vscode.window.showInformationMessage(status.ok?'Neutral Core подключено':'Neutral Core недоступно');return status;}catch(error){vscode.window.showWarningMessage(String(error.message));return {ok:false};}
  }));
  context.subscriptions.push(vscode.commands.registerCommand('neutral.previewEdit',async()=>{
    let previewKey;
    try{
      const document=vscode.window.activeTextEditor?.document;if(!document)throw Error('Откройте сохранённый файл');
      const replacement=await vscode.window.showInputBox({title:'Проверка правки Neutral',prompt:'Новое содержимое файла. Применение потребует отдельного подтверждения.'});if(replacement===undefined)return {ok:false,canceled:true};
      const snapshot=await capture(document,replacement),uri=vscode.Uri.parse('neutral-preview:/'+crypto.randomUUID()+'/'+path.basename(document.uri.fsPath));
      previewKey=uri.toString();previews.set(previewKey,replacement);
      await vscode.commands.executeCommand('vscode.diff',document.uri,uri,'Neutral · Предпросмотр правки');
      if(await vscode.window.showInformationMessage('Применить показанную правку к открытому буферу?',{modal:true,detail:'Файл останется несохранённым. Ctrl+Z отменяет правку.'},'Применить')==='Применить')await apply(snapshot);
      return {ok:true};
    }catch(error){vscode.window.showWarningMessage(error.message);return {ok:false,error:error.message};}finally{if(previewKey)previews.delete(previewKey);}
  }));
  const agentView=require('./agent-view.cjs').registerAgentView(context);
  context.subscriptions.push(vscode.commands.registerCommand('neutral.openPanel',()=>vscode.commands.executeCommand('workbench.view.extension.neutral')));
  if(process.env.NEUTRAL_IDE_CONNECTION)void vscode.commands.executeCommand('workbench.view.extension.neutral');
  return {capture,apply,request,agentView,nativeWorkspace:require('./workspace.cjs')};
}
module.exports={activate};
