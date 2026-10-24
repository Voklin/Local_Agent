// Exercise the host authorization boundary without opening user applications.
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const ts=require('typescript');
const root=path.resolve(__dirname,'../..');
const parent=path.join(root,'.test-tmp');fs.mkdirSync(parent,{recursive:true});
const directory=fs.mkdtempSync(path.join(parent,'desktop-apps-'));
const compiled=path.join(directory,'desktopApps.cjs');
fs.writeFileSync(compiled,ts.transpileModule(fs.readFileSync(path.join(root,'apps/desktop/electron/desktopApps.ts'),'utf8'),
  {compilerOptions:{module:ts.ModuleKind.CommonJS,target:ts.ScriptTarget.ES2022,esModuleInterop:true}}).outputText);
const {DesktopApplications}=require(compiled);

(async()=>{
  const opened=[];let browsers=0;
  const apps=new DesktopApplications(directory,async file=>{opened.push(file);},async()=>{browsers++;});
  const executable=path.join(directory,'Editor.exe');fs.writeFileSync(executable,'fixture');
  const selected=apps.add(executable).find(item=>item.custom);
  assert(selected);assert(!('file' in selected));
  assert.equal(apps.add(executable).filter(item=>item.custom).length,1);
  await apps.open(selected.id);assert.deepEqual(opened,[executable]);
  for(const id of [executable,'cmd /c echo test','browser --flag','unknown'])await assert.rejects(()=>apps.open(id));
  assert.equal(opened.length,1);
  const script=path.join(directory,'script.cmd');fs.writeFileSync(script,'fixture');
  assert.throws(()=>apps.add(script));
  apps.remove(selected.id);await assert.rejects(()=>apps.open(selected.id));
  assert.equal(opened.length,1);
  await apps.open('browser');assert.equal(browsers,1);
  console.log('PASS: application IDs, no paths/arguments, EXE picker, duplicate/removal, fixed browser URL');
})().catch(error=>{console.error(error);process.exitCode=1;});
