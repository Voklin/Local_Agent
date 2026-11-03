// Only loaded by the isolated UI test, never included in the Neutral runtime.
const vscode=require('vscode'),fs=require('node:fs/promises'),path=require('node:path'),assert=require('node:assert/strict');
exports.activate=async()=>{
 const report=process.env.NEUTRAL_IDE_TEST_REPORT;if(!report)return;
 try{
  await vscode.extensions.getExtension('neutral.neutral-agent').activate();
  const uri=vscode.Uri.joinPath(vscode.workspace.workspaceFolders[0].uri,'safe.txt'),doc=await vscode.workspace.openTextDocument(uri);await vscode.window.showTextDocument(doc,vscode.ViewColumn.One);
  const result=await vscode.commands.executeCommand('neutral.previewEdit');assert.equal(result?.ok,true,JSON.stringify(result));assert.equal(doc.getText(),'UI approved replacement');assert(doc.isDirty);assert.equal((await fs.readFile(uri.fsPath,'utf8')).replaceAll('\r\n','\n'),'original\n');
  await vscode.window.showTextDocument(doc,vscode.ViewColumn.One);await vscode.commands.executeCommand('undo');assert.equal(doc.getText().replaceAll('\r\n','\n'),'original\n');assert(!doc.isDirty);
  await vscode.commands.executeCommand('neutral.openPanel');
  await fs.writeFile(report,JSON.stringify({status:'passed',checks:['visible-diff','explicit-confirmation','editor-buffer-only','editor-undo','activity-view']},null,2));
 }catch(error){await fs.writeFile(report,JSON.stringify({status:'failed',error:error.stack},null,2));}
 await new Promise(resolve=>setTimeout(resolve,2500));
 await vscode.commands.executeCommand('workbench.action.quit');
};
