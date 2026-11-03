const assert=require('node:assert/strict');

async function runAcceptance({desktop,panel,until,screenshot,fs,path,project,requests}){
 const input=async(label,value)=>{
  await panel(`{const n=document.querySelector('[aria-label="${label}"]');if(!n)throw Error('Missing ${label}');Object.getOwnPropertyDescriptor(n.tagName==='TEXTAREA'?HTMLTextAreaElement.prototype:n.tagName==='SELECT'?HTMLSelectElement.prototype:HTMLInputElement.prototype,'value').set.call(n,${JSON.stringify(value)});n.dispatchEvent(new Event(n.tagName==='SELECT'?'change':'input',{bubbles:true}));}`);
  await new Promise(resolve=>setTimeout(resolve,60));
 };
 const textButton=text=>panel(`[...document.querySelectorAll('button')].find(n=>n.textContent.trim()===${JSON.stringify(text)}).click()`);
 const nav=label=>panel(`[...document.querySelectorAll('.nw-nav button')].find(n=>n.textContent===${JSON.stringify(label)}).click()`);
 const loadCurrent=async()=>{const chats=await panel("window.lca.listChats('ide')");return panel(`window.lca.loadChat(${JSON.stringify(chats.chats[0].id)},'ide')`);};
 const approve=async decision=>{await until(()=>panel("!!document.querySelector('.nw-approval')"),'check approval');assert(await panel("document.querySelector('.nw-approval').innerText.includes('verify.mjs')"));await textButton(decision);await until(()=>panel("!document.querySelector('.nw-approval') && !document.querySelector('.nw-footer').textContent.includes('Работаю')"),'check completed');};
 fs.writeFileSync(path.join(project,'package.json'),JSON.stringify({type:'module'}));
 fs.writeFileSync(path.join(project,'totals.js'),'export function tax_total(n){return n * 1.1;}\n');
 fs.writeFileSync(path.join(project,'invoice.js'),"import {tax_total} from './totals.js';\nexport function invoice(n){return tax_total(n);}\n");
 fs.writeFileSync(path.join(project,'verify.mjs'),"import assert from 'node:assert/strict';\nimport {invoice} from './invoice.js';\nassert.equal(Math.round(invoice(100)),110);\nconsole.log('Imports and behavior passed');\n");
 assert.equal((await desktop("window.lca.configureExtensions({kind:'groups',id:'commands',enabled:true})")).ok,true);
 assert.equal((await panel('window.lca.getModelSettings()')).model,'','checks_only fixture begins without a model');
 await input('Задача агенту','Этот несохранённый запрос нужно оставить');
 await panel("document.querySelector('.nw-checks-trigger').click()");await textButton('Добавить проверку');
 await input('Назначение проверки 1','Imports');await input('Аргументы проверки 1','verify.mjs');await input('Критерии готовности','Imports work');
 const checkId=await panel("document.querySelector('[aria-label=\"Проверки критерия 1\"] option').value");
 await panel("{const n=document.querySelector('[aria-label=\"Проверки критерия 1\"]');n.options[0].selected=true;n.dispatchEvent(new Event('change',{bubbles:true}));}");
 await panel("[...document.querySelectorAll('summary')].find(n=>n.textContent==='Область и дополнительные параметры').click()");
 await input('Область проверки 1','files');await input('Файлы проверки 1','invoice.js\ntotals.js');await input('Зависимости проверки 1','verify.mjs\npackage.json');
 await input('Назначение проверки 1','');await textButton('Запустить проверки без модели');await until(()=>panel("document.querySelector('.nw-error')?.textContent.includes('Укажите назначение')"),'invalid configuration');assert.equal(requests.length,0);
 await input('Назначение проверки 1','Imports');await screenshot('acceptance-settings');
 await textButton('Запустить проверки без модели');await approve('Отклонить');
 let result=await loadCurrent();assert.equal(result.task.test_results.length,1);assert.equal(result.task.test_results[0].code,'USER_DENIED');assert.equal(requests.length,0,'Denial/checks_only must not invoke the model');
 await nav('Диалог');assert.equal(await panel("document.querySelector('.nw-compose textarea').value"),'Этот несохранённый запрос нужно оставить');
 await panel("document.querySelector('.nw-checks-trigger').click()");await textButton('Запустить проверки без модели');await approve('Применить');
 result=await loadCurrent();assert.equal(result.task.verification.status,'scoped_passed');assert.equal(result.task.test_results[0].check_id,checkId);assert.equal(result.task.acceptance_evidence[0].status,'scoped_checks_passed');assert.equal(requests.length,0);
 await nav('Диалог');await panel("document.querySelector('[aria-label=\"Настройки подключения\"]').click()");
 await panel("{const n=document.querySelector('input[list=\"nw-models\"]');Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(n,'neutral-integration');n.dispatchEvent(new Event('input',{bubbles:true}));}");
 await new Promise(resolve=>setTimeout(resolve,80));await panel("document.querySelector('.nw-page form').requestSubmit()");await until(()=>panel("!!document.querySelector('.nw-compose')"),'configured model');
 await input('Задача агенту','acceptance-missing-import');await panel("document.querySelector('.nw-send').click()");
 let approvals=0;
 await until(async()=>{
  const pending=await panel("document.querySelector('.nw-approval')?.innerText||''");
  if(pending){approvals++;await textButton('Применить');await until(()=>panel("!document.querySelector('.nw-approval')"),'approval applied');return false;}
  return panel("!!document.querySelector('.nw-send') && !document.querySelector('.nw-send[aria-label=\"Остановить\"]') && document.body.innerText.includes('Import исправлен')");
 },'model repairs configured failing check',90000);
 assert.equal(approvals,5,'Two writes, failed check, repair and passing check require approvals');
 result=await loadCurrent();const targetChat=result.chat.id;
 const commandReceipts=result.chat.messages.filter(m=>m.role==='tool').map(m=>{try{return JSON.parse(m.content);}catch{return {};}}).filter(r=>Number.isInteger(r.exit_code));
 assert.deepEqual(commandReceipts.slice(-2).map(r=>r.exit_code),[1,0]);assert.equal(result.task.test_results[0].exit_code,0);assert(result.task.test_results.every(r=>r.check_id===checkId));assert.equal(result.task.acceptance_evidence[0].status,'scoped_checks_passed');
 assert.equal(result.task.options.criteria_links['0'][0],checkId);assert(fs.readFileSync(path.join(project,'invoice.js'),'utf8').includes('import {grand_total}'));
 assert(requests.some(body=>JSON.stringify(body.messages).includes('does not provide an export named')),'Actual failing receipt must reach the model');
 await nav('Работа');assert(await panel("document.body.innerText.includes('Подтверждены только выбранные файлы')"));await screenshot('acceptance-passed');
 fs.appendFileSync(path.join(project,'invoice.js'),'// external edit\n');
 const httpBefore=requests.length;const stale=await panel(`window.lca.loadChat(${JSON.stringify(targetChat)},'ide')`);assert.equal(stale.task.verification.status,'stale');assert.equal(requests.length,httpBefore);
 await nav('История');await panel("document.querySelector('.nw-history-item').click()");await until(()=>panel("!!document.querySelector('.nw-compose')"),'stale task reloaded');await nav('Работа');assert(await panel("document.body.innerText.includes('устарел') || document.body.innerText.includes('изменил')"));await screenshot('acceptance-stale');
 await nav('Диалог');await panel("document.querySelector('.nw-checks-trigger').click()");await input('Критерии готовности','Imports work\nНужна ручная оценка');
 await panel("{const n=document.querySelector('[aria-label=\"Проверки критерия 1\"]');n.options[0].selected=true;n.dispatchEvent(new Event('change',{bubbles:true}));}");
 await textButton('Запустить проверки без модели');await approve('Применить');result=await loadCurrent();assert.equal(result.task.verification.status,'incomplete');assert.equal(result.task.acceptance_evidence[1].status,'unverified');assert.equal(requests.length,httpBefore);
 await screenshot('acceptance-manual-criterion');
 await nav('Диалог');await input('Режим агента','ask');await nav('Работа');await textButton('Продолжить задачу');
 await until(()=>panel("document.querySelector('.nw-error')?.textContent.includes('переключитесь в Agent')"),'read-only resume blocked');assert.equal(requests.length,httpBefore);
 await nav('Диалог');await panel("document.querySelector('.nw-checks-trigger').click()");assert(await panel("[...document.querySelectorAll('button')].find(n=>n.textContent==='Запустить проверки без модели').disabled"),'Ask cannot run commands');
 await textButton('← К диалогу');await input('Режим агента','agent');
 await nav('Диалог');await panel("document.querySelector('.nw-checks-trigger').click()");await input('Назначение проверки 1','Unsaved next-run check');
 assert.equal((await loadCurrent()).task.options.checks[0].purpose,'Imports','UI draft must not rewrite canonical options');
 await panel("document.querySelector('[aria-label=\"Новая задача\"]').click()");await until(()=>panel("!!document.querySelector('.nw-compose')"),'new chat');await panel("document.querySelector('.nw-checks-trigger').click()");assert.equal(await panel("document.querySelectorAll('.nw-check-definition').length"),0,'New chat cannot inherit a different chat draft');
 await nav('История');await panel("[...document.querySelectorAll('.nw-history-item')].find(b=>!b.textContent.includes('Текущий')).click()");await until(()=>panel("!!document.querySelector('.nw-compose')"),'old chat returned');await panel("document.querySelector('.nw-checks-trigger').click()");assert.equal(await panel("document.querySelector('[aria-label=\"Назначение проверки 1\"]').value"),'Unsaved next-run check');
 assert.equal(await panel('window.neutralIdeCheckDraft.options.checks[0].id'),checkId,'Current draft is persisted to webview state');
 await nav('История');await panel("[...document.querySelectorAll('.nw-history-row')].find(row=>row.textContent.includes('Текущий')).querySelector('.nw-row-actions button:last-child').click()");await textButton('Подтвердить удаление');
 await until(()=>panel("!document.querySelector('.nw-confirm')"),'chat deleted');await nav('Диалог');await panel("document.querySelector('.nw-checks-trigger').click()");assert.equal(await panel("document.querySelectorAll('.nw-check-definition').length"),0,'Deleting the selected chat clears its draft');
 return {check_id:checkId,approvals,requests:requests.length,protocol:process.env.LESHY_ACCEPTANCE_JSON?'json':'native'};
}
module.exports={runAcceptance};
