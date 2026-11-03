const assert=require('node:assert/strict');
const {test}=require('node:test');
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),ts=require('typescript');
const {projectTaskEvent}=require('../../apps/desktop/src/idePanel/sessionState.ts');
const {recoveryDiagnostics,hasRecoveryBlockers}=require('../../apps/desktop/src/idePanel/recoveryDiagnostics.ts');
const identity={chat:'chat',run:'run',seq:0};
test('early event for the assigned run arrives before startTask resolves',()=>{
 const update=projectTaskEvent(identity,[],{event:'text_delta',chat_id:'chat',run_id:'run',event_seq:1,message_id:'answer',text:'Hello'});
 assert.equal(update.messages[0].text,'Hello');assert.equal(update.identity.seq,1);
});
test('duplicate or out of order sequence cannot append text twice',()=>{
 for(const event_seq of [1,2])assert.equal(projectTaskEvent({...identity,seq:2},[],{event:'text_delta',chat_id:'chat',run_id:'run',event_seq,message_id:'m',text:'x'}),null);
});
test('invalid sequence values cannot poison subsequent events',()=>{
 for(const event_seq of [NaN,Infinity,-1,0.5])assert.equal(projectTaskEvent(identity,[],{event:'task_end',chat_id:'chat',run_id:'run',event_seq}),null);
});
test('foreign chat, foreign run and a finished run are ignored',()=>{
 for(const scope of [{chat_id:'other',run_id:'run'},{chat_id:'chat',run_id:'old'}])assert.equal(projectTaskEvent(identity,[],{event:'task_end',...scope}),null);
 assert.equal(projectTaskEvent({...identity,run:''},[],{event:'task_end',chat_id:'chat',run_id:'run'}),null);
});
test('task end clears identity and approval without clearing the transcript',()=>{
 const lines=[{role:'assistant',text:'Done'}];
 const update=projectTaskEvent(identity,lines,{event:'task_end',chat_id:'chat',run_id:'run',event_seq:4});
 assert.equal(update.identity.run,'');assert.equal(update.approval,null);assert.equal(update.ended,true);assert.equal(update.messages,undefined);
});
test('canonical final chat replaces a streamed message with the same identity',()=>{
 const update=projectTaskEvent(identity,[{role:'assistant',id:'m',text:'partial'}],{event:'chat',chat_id:'chat',run_id:'run',message_id:'m',role:'assistant',text:'complete'});
 assert.deepEqual(update.messages,[{role:'assistant',id:'m',text:'complete'}]);
});
test('recovery diagnostics omit credentials, source, paths and narrative',()=>{
 const task={status:'paused',turn:3,tool_calls:4,chat_id:'a'.repeat(32),journal_id:'b'.repeat(32),recovery_error:'api_key=secret source code /private/path',prompt:'secret',options:{api_key:'secret'},recovery_items:[{call_id:'c'.repeat(32),message_index:1,path:'/private/path',tool:'secret',summary:'secret'}],snapshot_attention:[{id:'d'.repeat(32),status:'secret'}]};
 const report=recoveryDiagnostics(task);
 assert.equal(report.schema,'leshy.recovery.v1');assert.equal(report.recovery.journal_unreadable,true);assert.equal(report.recovery.unknown_actions.length,1);
 assert.doesNotMatch(JSON.stringify(report),/secret|private|api_key|source code/);assert.equal(hasRecoveryBlockers(task),true);
});
test('all three recovery blockers independently prevent resume',()=>{
 for(const blocker of [{recovery_error:'bad journal'},{recovery_items:[{}]},{snapshot_attention:[{}]}])assert.equal(hasRecoveryBlockers(blocker),true);
 assert.equal(hasRecoveryBlockers(null),false);assert.equal(hasRecoveryBlockers({recovery_items:[],snapshot_attention:[]}),false);
});
test('main IPC preserves an omitted API key while allowing explicit clearing',()=>{
 const source=fs.readFileSync(path.join(__dirname,'../../apps/desktop/electron/main.ts'),'utf8');
 const ast=ts.createSourceFile('main.ts',source,ts.ScriptTarget.Latest,true);
 const declaration=ast.statements.find(node=>ts.isFunctionDeclaration(node)&&node.name?.text==='modelConfig');
 assert.ok(declaration);
 const code=ts.transpileModule(declaration.getText(ast),{compilerOptions:{target:ts.ScriptTarget.ES2022}}).outputText;
 const context={};vm.runInNewContext(code,context);
 const base={base_url:'https://fixture.invalid/v1',model:'fixture'};
 assert.equal(Object.hasOwn(context.modelConfig(base),'api_key'),false,'Omitted key must reach Core as omitted');
 assert.equal(context.modelConfig({...base,api_key:''}).api_key,'','Explicit empty key remains an explicit clear');
 assert.equal(context.modelConfig({...base,api_key:'new-key'}).api_key,'new-key');
});
