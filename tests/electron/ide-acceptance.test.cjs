const assert=require('node:assert/strict');
const {test}=require('node:test');
const {emptyAcceptanceOptions,prepareAcceptanceOptions,removeAcceptanceCheck,acceptanceDraftForChat,canResumeInMode}=require('../../apps/desktop/src/idePanel/acceptanceChecks.ts');
const check={id:'check_a',purpose:'Imports',program:'node',arguments:['--test','path with spaces.mjs',''],cwd:'.',timeout:30,evidence_scope:{kind:'files',files:[' invoice.js ','totals.js'],dependencies:['verify.mjs']}};
test('criteria blanks are filtered and links reindexed without changing stable IDs or argv',()=>{
 const options={...emptyAcceptanceOptions(),auto_checks:true,criteria:[' ',' Imports work '],criteria_links:{'1':['check_a']},checks:[check]};
 const before=JSON.stringify(options),result=prepareAcceptanceOptions(options,'agent');
 assert.deepEqual(result.criteria,['Imports work']);assert.deepEqual(result.criteria_links,{'0':['check_a']});
 assert.equal(result.checks[0].id,'check_a');assert.deepEqual(result.checks[0].arguments,check.arguments);
 assert.deepEqual(result.checks[0].evidence_scope.files,['invoice.js','totals.js']);assert.deepEqual(result.checks[0].evidence_scope.dependencies,['verify.mjs']);assert.equal(JSON.stringify(options),before);
});
test('Ask and Plan cannot execute configured commands and retain the original draft',()=>{
 const value={...emptyAcceptanceOptions(),auto_checks:true,criteria:['x'],checks:[check]};
 for(const mode of ['ask','plan']){const result=prepareAcceptanceOptions(value,mode);assert.equal(result.read_only,true);assert.equal(result.auto_checks,false);assert.deepEqual(result.checks,[]);assert.deepEqual(result.criteria,[]);assert.throws(()=>prepareAcceptanceOptions(value,mode,true));}
 assert.equal(value.checks.length,1);
});
test('checks-only runs without a prompt but requires checks; invalid definitions are rejected',()=>{
 assert.throws(()=>prepareAcceptanceOptions(emptyAcceptanceOptions(),'agent',true));
 assert.equal(prepareAcceptanceOptions({...emptyAcceptanceOptions(),checks:[check]},'agent',true).checks_only,true);
 for(const broken of [{...check,purpose:''},{...check,timeout:121},{...check,evidence_scope:{kind:'files',files:[],dependencies:[]}}])assert.throws(()=>prepareAcceptanceOptions({...emptyAcceptanceOptions(),checks:[broken]},'agent'));
 assert.throws(()=>prepareAcceptanceOptions({...emptyAcceptanceOptions(),checks:[check,check]},'agent'));
});
test('removing a check removes its criterion links and never mutates the original',()=>{
 const value={...emptyAcceptanceOptions(),checks:[check],criteria:['x'],criteria_links:{'0':['check_a']}};
 const result=removeAcceptanceCheck(value,'check_a');assert.equal(result.checks.length,0);assert.deepEqual(result.criteria_links,{'0':[]});assert.equal(value.checks.length,1);
});
test('draft belongs only to its exact chat; checkpoint is otherwise restored by value',()=>{
 const saved={chatId:'one',options:{...emptyAcceptanceOptions(),checks:[check]}};
 assert.equal(acceptanceDraftForChat('one',undefined,saved).checks.length,1);
 assert.equal(acceptanceDraftForChat('two',undefined,saved).checks.length,0);
 const checkpoint={...emptyAcceptanceOptions(),checks:[check]};const restored=acceptanceDraftForChat('two',checkpoint,saved);restored.checks[0].purpose='changed';assert.equal(checkpoint.checks[0].purpose,'Imports');
});
test('corrupted view state is ignored and blank criterion rows do not consume the limit',()=>{
 assert.doesNotThrow(()=>acceptanceDraftForChat('x',undefined,{chatId:'x',options:{...emptyAcceptanceOptions(),checks:[{...check,evidence_scope:null}]}}));
 const value={...emptyAcceptanceOptions(),criteria:[...Array(20).fill(''),'Keep behavior']};assert.deepEqual(prepareAcceptanceOptions(value,'agent').criteria,['Keep behavior']);
});
test('switching to Ask or Plan cannot resume a saved Agent task with command rights',()=>{
 for(const mode of ['ask','plan']){assert.equal(canResumeInMode({read_only:false},mode),false);assert.equal(canResumeInMode(undefined,mode),false);assert.equal(canResumeInMode({read_only:true},mode),true);}
 assert.equal(canResumeInMode({read_only:false},'agent'),true);
});
test('LSP paths are normalized consistently with the Core Windows contract',()=>{
 const lsp={...check,kind:'diagnostics',program:'lsp',arguments:[' src\\main.py '],evidence_scope:{kind:'files',files:['src\\main.py'],dependencies:[]}};
 const result=prepareAcceptanceOptions({...emptyAcceptanceOptions(),checks:[lsp]},'agent');assert.deepEqual(result.checks[0].arguments,['src/main.py']);assert.deepEqual(result.checks[0].evidence_scope.files,['src/main.py']);
});
test('a legitimate leading space in cwd is not silently changed',()=>{
 const value={...emptyAcceptanceOptions(),checks:[{...check,cwd:' leading folder'}]};assert.equal(prepareAcceptanceOptions(value,'agent').checks[0].cwd,' leading folder');
});
