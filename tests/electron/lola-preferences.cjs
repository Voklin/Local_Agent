// Pure input and multi-display bounds contracts; no app, microphone or user profile.
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),ts=require('typescript');
const root=path.resolve(__dirname,'../..'),directory=path.join(root,'.test-data/lola-unit');fs.mkdirSync(directory,{recursive:true});
const compiled=path.join(directory,'lolaDesktop.cjs');fs.writeFileSync(compiled,ts.transpileModule(fs.readFileSync(path.join(root,'apps/desktop/shared/lolaDesktop.ts'),'utf8'),{compilerOptions:{module:ts.ModuleKind.CommonJS,target:ts.ScriptTarget.ES2022}}).outputText);
const {lolaDesktopDefaults,validateLolaSettings,validateLolaFrame,fitLolaBounds}=require(compiled);
assert.equal(lolaDesktopDefaults.enabled,false);
for(const patch of [{enabled:'true'},{mode:'fullscreen'},{size:0},{size:NaN},{size:1000},{clickThrough:'no'},{position:{x:Infinity,y:1}}])assert.throws(()=>validateLolaSettings({...lolaDesktopDefaults,...patch}));
const negative=fitLolaBounds({...lolaDesktopDefaults,position:{x:-5000,y:5000}},{x:-1920,y:0,width:1920,height:1040});assert.equal(negative.x,-1920);assert.ok(negative.y+negative.height<=1040);
const desktop=fitLolaBounds(lolaDesktopDefaults,{x:0,y:0,width:1920,height:1080});assert.ok(desktop.height>=lolaDesktopDefaults.size+226,'Window must fit the character, bounded bubble, and outer padding');
const tiny=fitLolaBounds({...lolaDesktopDefaults,size:360},{x:0,y:0,width:300,height:300});assert.ok(tiny.width<=300&&tiny.height<=300&&tiny.x>=0&&tiny.y>=0);
const frame=validateLolaFrame({state:'execute_shell',caption:'x'.repeat(10000),reply:'x'.repeat(10000),busy:'true',recording:false,wake:true});assert.equal(frame.state,'idle');assert.equal(frame.busy,false);assert.equal(frame.caption.length,160);assert.equal(frame.reply.length,1600);
assert.equal(validateLolaSettings({...lolaDesktopDefaults,position:{x:12.6,y:-200.4}}).position.x,13);
console.log('PASS: Lola opt-in, strict settings, size bounds, negative display, small display and bounded presentation data');
