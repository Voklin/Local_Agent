const vscode=require('vscode'),fs=require('node:fs/promises'),path=require('node:path'),crypto=require('node:crypto');
const sha=bytes=>crypto.createHash('sha256').update(bytes).digest('hex');
async function safePath(root,relative){
 if(typeof relative!=='string'||!relative||path.isAbsolute(relative)||relative.split(/[\\/]/).includes('..'))throw Error('Некорректный путь проекта');
 const base=await fs.realpath(root),file=path.resolve(base,relative),inside=path.relative(base,file);if(inside.startsWith('..')||path.isAbsolute(inside)||inside.split(path.sep).some(part=>part.toLowerCase()==='.git'))throw Error('Путь вне проекта');
 let ancestor=file;while(true){try{const real=await fs.realpath(ancestor),rel=path.relative(base,real);if(rel.startsWith('..')||path.isAbsolute(rel))throw Error('Ссылка вне проекта');break;}catch(error){if(error.code!=='ENOENT')throw error;const parent=path.dirname(ancestor);if(parent===ancestor)throw error;ancestor=parent;}}
 return file;
}
function dirty(root){return vscode.workspace.textDocuments.filter(doc=>doc.isDirty&&doc.uri.scheme==='file'&&!path.relative(root,doc.uri.fsPath).startsWith('..')&&!path.isAbsolute(path.relative(root,doc.uri.fsPath)));}
async function witness(root,relative){
 const file=await safePath(root,relative),uri=vscode.Uri.file(file);let bytes=null;let handle;try{handle=await fs.open(file,'r');const stat=await handle.stat();if(stat.isFile()){if(stat.size>1_000_000)throw Error('Файл превышает 1 МБ');const buffer=Buffer.alloc(1_000_001);const read=await handle.read(buffer,0,buffer.length,0);if(read.bytesRead>1_000_000)throw Error('Файл вырос за пределы 1 МБ');bytes=buffer.subarray(0,read.bytesRead);}}catch(error){if(error.code!=='ENOENT'&&error.code!=='EISDIR')throw error;}finally{await handle?.close();}
 const document=vscode.workspace.textDocuments.find(doc=>doc.uri.toString()===uri.toString());if(document?.isDirty)throw Error('Сначала сохраните черновик: '+relative);
 if(bytes&&document&&document.getText()!==bytes.toString('utf8').replace(/^\uFEFF/,''))throw Error('Редактор ещё не перечитал внешнее изменение: '+relative);
 return {path:relative,exists:bytes!==null,disk_hash:bytes?sha(bytes):null,bom:bytes?.subarray(0,3).equals(Buffer.from([239,187,191]))||false,version:document?.version??null,buffer_hash:document?sha(document.getText()):null};
}
async function prepare(root,message){
 if(!vscode.workspace.isTrusted)throw Error('Подтвердите доверие проекту перед запуском агента');
 const {preview,name}=message,paths=[preview.path,...(preview.destination?[preview.destination]:[])],states=[];
 for(const relative of paths)states.push(await witness(root,relative));
 const expected=preview.snapshot.sha256??preview.snapshot.source?.sha256??null;if(name!=='create_directory'&&states[0].disk_hash!==expected)throw Error('Файл изменился после подготовки diff');
 const content=name==='write_file'?message.args.content:preview.content;if(!preview.exists&&typeof content==='string'&&content.startsWith('\uFEFF'))throw Error('Новый файл должен быть UTF-8 без BOM');if(states[0].bom&&typeof content==='string'&&!content.startsWith('\uFEFF'))throw Error('Файл содержит UTF-8 BOM. Используйте patch_file или сохраните BOM в полном содержимом.');
 return {ok:true,editor_state:states};
}
async function apply(root,message){
 if(!vscode.workspace.isTrusted)throw Error('Доверие проекту отозвано');
 const {name,preview,args}=message;if(!Array.isArray(preview.editor_state))throw Error('Нет снимка редактора');
 for(const previous of preview.editor_state){const current=await witness(root,previous.path);if(current.exists!==previous.exists||current.disk_hash!==previous.disk_hash||(previous.version!==null&&(current.version!==previous.version||current.buffer_hash!==previous.buffer_hash)))throw Error('Буфер или диск изменился после preview');}
 const file=await safePath(root,preview.path),uri=vscode.Uri.file(file),edit=new vscode.WorkspaceEdit();let effected=false;
 try{
  if(name==='create_directory'){
   for(const relative of preview.snapshot.directories){const target=await safePath(root,relative);effected=true;await fs.mkdir(target);}
   return {ok:true,path:preview.path,operation:name,created_directories:preview.snapshot.directories,editor:true};
  }
  if(name==='rename_file')edit.renameFile(uri,vscode.Uri.file(await safePath(root,preview.destination)),{overwrite:false});
  else if(name==='delete_file')edit.deleteFile(uri,{recursive:false,ignoreIfNotExists:false});
  else{
   const content=name==='write_file'?args.content:preview.content;if(typeof content!=='string'||content.includes('\0'))throw Error('Нужен UTF-8 текст');
   if(content.includes('\r\n')&&content.replaceAll('\r\n','').includes('\n'))throw Error('Смешанные переводы строк: используйте единый LF или CRLF');
   if(preview.editor_state[0].bom&&!content.startsWith('\uFEFF'))throw Error('Нельзя незаметно удалить BOM');
   const text=preview.editor_state[0].bom?content.slice(1):content;
   if(!preview.exists){const creation=new vscode.WorkspaceEdit();creation.createFile(uri,{overwrite:false,ignoreIfExists:false});effected=true;if(!await vscode.workspace.applyEdit(creation))throw Error('Редактор отклонил создание файла');}
   const doc=await vscode.workspace.openTextDocument(uri),editor=await vscode.window.showTextDocument(doc,{viewColumn:vscode.ViewColumn.One,preserveFocus:true});
   if(doc.isDirty)throw Error('Сначала сохраните черновик');
   if(preview.exists){const previous=preview.editor_state[0],current=await witness(root,previous.path);if(current.disk_hash!==previous.disk_hash||(previous.version!==null&&current.version!==previous.version))throw Error('Снимок редактора устарел');}
   effected=true;const applied=await editor.edit(builder=>{builder.setEndOfLine(content.includes('\r\n')?vscode.EndOfLine.CRLF:vscode.EndOfLine.LF);builder.replace(new vscode.Range(doc.positionAt(0),doc.positionAt(doc.getText().length)),text);},{undoStopBefore:true,undoStopAfter:true});
   if(!applied)return {ok:false,code:'OUTCOME_UNKNOWN',error:'Редактор отклонил изменение. Проверьте буфер.'};
   if(!await doc.save())return {ok:false,code:'OUTCOME_UNKNOWN',error:'Правка в буфере; сохранение не подтверждено'};
   const expected=preview.snapshot.proposed_sha256,raw=await fs.readFile(file);if(sha(raw)!==expected)return {ok:false,code:'OUTCOME_UNKNOWN',error:'Содержимое после сохранения отличается от diff. Проверьте save participants и файл.'};
   return {ok:true,path:preview.path,operation:name,editor:true,bytes:raw.length,sha256:sha(raw)};
  }
  effected=true;if(!await vscode.workspace.applyEdit(edit,{isRefactoring:false}))return {ok:false,code:'OUTCOME_UNKNOWN',error:'Редактор отклонил файловую операцию'};
  return {ok:true,path:preview.path,operation:name,editor:true,...(name==='rename_file'?{destination:preview.destination,renamed_files:[{from:preview.path,to:preview.destination}]}:{deleted_files:[preview.path]})};
 }catch(error){return {ok:false,code:effected?'OUTCOME_UNKNOWN':'FILE_CHANGED',error:error.message};}
}
module.exports={safePath,dirty,prepare,apply};
