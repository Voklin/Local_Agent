// Visual fixtures only; this never imports the application backend.
const assert=require('node:assert/strict');
module.exports=async function({win,js,click,input,capture,delay}){
 const sizes=[[1280,720],[1440,900],[1920,1080]],screens=[];
 const form=async(key,value)=>{await js(`{const n=document.querySelector('[data-form="${key}"]');n.value=${JSON.stringify(value)};n.dispatchEvent(new Event('change',{bubbles:true}));}`);};
 const snap=async(name)=>{assert.equal(await js('document.documentElement.scrollWidth>innerWidth'),false,name+': document overflow');await capture(name);screens.push(name);};
 const key=code=>js(`document.activeElement.dispatchEvent(new KeyboardEvent('keydown',${JSON.stringify({...code,bubbles:true,cancelable:true})}))`);
 await js('window.prototype.reset();window.prototype.resetLayout()');
 assert.equal(await js("document.querySelectorAll('.sidebar .conversation-row').length"),0);
 await click('[data-action=toggle-history]');
 assert.equal(await js('document.activeElement.id'),'conversation-search');
 await input('#conversation-search','разобраться');assert.equal(await js("document.querySelectorAll('.history-drawer .conversation-row').length"),1);
 await input('#conversation-search','');await click('[data-chat-menu=demo-0]');await click('[data-review=rename-chat]');await input('#review-dialog-value','Проверить новый интерфейс');await click('[data-review=dialog-confirm]');
 assert.ok(await js("document.querySelector('.history-drawer').textContent.includes('Проверить новый интерфейс')"));
 for(const [w,h] of sizes){win.setContentSize(w,h);await delay(100);await snap('review-ide-history-'+w+'x'+h);}
 await click('[data-chat-menu=demo-0]');await click('[data-review=pin-chat]');
 await click('[data-chat-menu=demo-0]');await click('[data-review=fork-chat]');assert.equal(await js("document.querySelectorAll('.history-drawer .conversation-row').length"),4);
 await click('[data-chat-menu=demo-0]');await click('[data-review=export-chat]');assert.ok(await js("document.querySelector('.review-dialog').textContent.includes('JSON:')"));await key({key:'Escape'});
 await click('[data-chat-menu=demo-0]');await click('[data-review=archive-chat]');await click('[data-review=archive]');assert.equal(await js("document.querySelectorAll('.history-drawer .conversation-row').length"),1);
 await click('[data-chat-menu=demo-0]');await click('[data-review=delete-chat]');await click('[data-review=dialog-close]');assert.equal(await js("document.querySelectorAll('.history-drawer .conversation-row').length"),1,'Cancel must preserve the demo chat');
 await click('[data-chat-menu=demo-0]');await click('[data-review=delete-chat]');await click('[data-review=dialog-confirm]');assert.equal(await js("document.querySelectorAll('.history-drawer .conversation-row').length"),0);await snap('review-history-empty');
 await key({key:'Escape'});assert.equal(await js("document.activeElement.dataset.action"),'toggle-history');
 await key({key:'k',ctrlKey:true});assert.equal(await js('document.activeElement.id'),'conversation-search');await key({key:'Escape'});
 await click('[data-review=project-menu]');await click('[data-review=new-project]');await input('#review-dialog-value','UI Review');await click('[data-review=dialog-confirm]');assert.ok(await js("document.querySelector('.review-project').textContent.includes('UI Review')"));
 await js('window.prototype.reset()');await click('[data-file="styles.css"]');assert.equal(await js("document.querySelectorAll('[data-tab-file]').length"),2);await click('[data-tab-file="TaskPanel.tsx"]');
 await key({key:'f',ctrlKey:true});await input('#review-find','status');assert.ok(await js("Number(document.querySelector('#find-count').textContent.split(' ')[0])>0"));await click('[data-review=find-next]');assert.ok(await js("document.querySelector('#code-input').selectionEnd>document.querySelector('#code-input').selectionStart"));
 await click('[data-review=goto]');await input('#review-dialog-value','8');await click('[data-review=dialog-confirm]');assert.ok(await js("document.querySelector('.editor-foot').textContent.includes('Строка 8')"));await click('[data-review=wrap]');await click('[data-review=output]');await click('[data-review=output-problems]');await snap('review-editor-tools');
 await input('#code-input','const changed = true;');await click('[data-action=save-file]');assert.ok(await js("!!document.querySelector('.review-save-diff')"));await click('[data-review=dialog-confirm]');assert.equal(await js("document.querySelector('[data-action=save-file]').disabled"),true);
 await click('[data-side-view=memory]');await input('#memory-note','Сохранённая демо-заметка');await click('[data-review=memory-rules]');assert.ok(await js("!!document.querySelector('.review-dialog')"));await click('[data-review=dialog-close]');await click('[data-review=save-memory]');await click('[data-review=memory-rules]');await click('[data-review=memory-notes]');assert.equal(await js("document.querySelector('#memory-note').value"),'Сохранённая демо-заметка');
 for(const scenario of ['approval','recovery','queue','rich']){
  for(const [w,h] of sizes){await js(`window.prototype.setScenario('${scenario}')`);win.setContentSize(w,h);await delay(80);await snap('review-ide-'+scenario+'-'+w+'x'+h);}
 }
 await js("window.prototype.setScenario('approval')");
 for(const type of ['command','mcp','delete','rename','source']){await click('[data-review=approval-'+type+']');assert.ok(await js("document.querySelector('.review-approval pre').textContent.length>10"));await snap('review-approval-'+type);}
 await click('[data-review=approval-later]');assert.ok(await js("document.querySelector('.review-approval [role=status]').textContent.includes('отложено')"));await key({key:'Escape'});
 await js("window.prototype.setScenario('recovery')");assert.equal(await js("document.querySelector('[data-review=resume]').disabled"),true);await click('[data-review=recovery-done]');await click('[data-review=dialog-confirm]');assert.equal(await js("document.querySelector('[data-review=resume]').disabled"),false);await click('[data-review=resume]');
 await click('[data-inspect=checks]');await click('[data-review=evidence-stale]');assert.ok(await js("document.querySelector('.task-drawer').textContent.includes('нельзя считать')"));await click('[data-review=rollback]');await snap('review-rollback-preview');await click('[data-review=dialog-confirm]');assert.ok(await js("document.querySelector('.task-drawer').textContent.includes('Демо-откат подтверждён')"));
 await js("window.prototype.setScenario('settings')");
 for(const page of ['model','tools','access','voice','storage','runtime','connections','ide']){await click('[data-settings-tab='+page+']');assert.ok(await js("document.querySelector('.settings-content input,.settings-content select,.settings-content button')!==null"));await snap('review-settings-'+page);}
 await click('[data-settings-tab=model]');await form('url','http://demo.invalid/v1');await click('[data-review=save-form]');await click('[data-settings-tab=tools]');await click('[data-settings-tab=model]');assert.equal(await js("document.querySelector('[data-form=url]').value"),'http://demo.invalid/v1');
 await click('[data-settings-tab=tools]');for(const sub of ['skills','mcp','agents']){await click('[data-review=settings-sub-'+sub+']');await snap('review-settings-'+sub);}
 await click('[data-settings-tab=layout]');await form('layout','Мой рабочий стол');await click('[data-review=save-layout]');await js("document.querySelector('.settings-nav [data-resize]').dispatchEvent(new KeyboardEvent('keydown',{key:'ArrowRight',bubbles:true}))");await click('[data-review=restore-layout]');assert.ok(await js("document.querySelector('.review-form-status').textContent.includes('восстановлена')"));
 await form('theme','Светлая');await click('[data-action=close-settings]');await snap('review-light');await js("window.prototype.reset()");
 await js("window.prototype.setScenario('settings')");await click('[data-settings-tab=voice]');assert.equal(await js("!!document.querySelector('[data-review=lola-window]')&&!document.querySelector('[data-review=lola-main]')"),true);await click('[data-action=close-settings]');
 await js("window.prototype.reset();window.prototype.setMode('chat')");assert.equal(await js("document.querySelectorAll('.sidebar .conversation-row').length"),3);
 for(const [w,h] of sizes){win.setContentSize(w,h);await js("window.prototype.setScenario('rich')");await delay(80);await snap('review-chat-rich-'+w+'x'+h);}
 return {ok:true,screens,scope:'Visual fixtures only; no Python, model, real project or service connection'};
};
