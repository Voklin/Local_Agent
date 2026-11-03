import type {IdeOptions,ValidationCommand,EvidenceScope} from '../../shared/ideTypes';
import type {StartTaskOptions} from '../../shared/protocol';

export type AcceptanceDraft={chatId:string;options:IdeOptions};
export function canResumeInMode(saved:{read_only?:boolean}|undefined,mode:string):boolean{return mode==='agent'||saved?.read_only===true;}
export function emptyAcceptanceOptions():IdeOptions{return {read_only:false,auto_checks:false,criteria:[],criteria_links:{},checks:[]};}
function copyOptions(value:IdeOptions):IdeOptions{
 return {...value,criteria:[...value.criteria],criteria_links:Object.fromEntries(Object.entries(value.criteria_links).map(([key,ids])=>[key,[...ids]])),checks:value.checks.map(check=>({...check,arguments:[...check.arguments],applies_to:check.applies_to?[...check.applies_to]:undefined,evidence_scope:check.evidence_scope?.kind==='files'?{kind:'files',files:[...check.evidence_scope.files],dependencies:[...check.evidence_scope.dependencies]}:{kind:'workspace'}}))};
}
function isDraft(value:unknown):value is IdeOptions{
 if(!value||typeof value!=='object')return false;const v=value as IdeOptions;
 const strings=(a:unknown):a is string[]=>Array.isArray(a)&&a.every(s=>typeof s==='string');
 return typeof v.read_only==='boolean'&&typeof v.auto_checks==='boolean'&&strings(v.criteria)&&v.criteria.length<=64&&v.criteria.filter(s=>s.trim()).length<=12&&!!v.criteria_links&&typeof v.criteria_links==='object'&&Object.values(v.criteria_links).every(strings)&&Array.isArray(v.checks)&&v.checks.length<=8&&v.checks.every(c=>c&&typeof c.id==='string'&&typeof c.purpose==='string'&&typeof c.program==='string'&&typeof c.cwd==='string'&&typeof c.timeout==='number'&&strings(c.arguments)&&(c.applies_to===undefined||strings(c.applies_to))&&(c.evidence_scope===undefined||!!c.evidence_scope&&c.evidence_scope.kind==='workspace'||(!!c.evidence_scope&&c.evidence_scope.kind==='files'&&strings(c.evidence_scope.files)&&strings(c.evidence_scope.dependencies))));
}
export function acceptanceDraftForChat(chatId:string,checkpoint:unknown,saved?:AcceptanceDraft):IdeOptions{
 const candidate=saved?.chatId===chatId?saved.options:checkpoint;
 return isDraft(candidate)?copyOptions(candidate):emptyAcceptanceOptions();
}
export function removeAcceptanceCheck(value:IdeOptions,id:string):IdeOptions{
 return {...value,checks:value.checks.filter(check=>check.id!==id),criteria_links:Object.fromEntries(Object.entries(value.criteria_links).map(([key,ids])=>[key,ids.filter(link=>link!==id)]))};
}
function paths(values:string[]):string[]{
 const result=values.map(p=>p.trim().replaceAll('\\','/')).filter(Boolean);
 if(result.length>128||result.some(p=>p.length>1000||/[\x00\r\n:*?<>|"]/.test(p)||p.startsWith('/')||p.split('/').some(part=>!part||part==='.'||part==='..')))throw Error('Область проверки: нужны относительные пути файлов без масок и переходов ..');
 return result;
}
export function prepareAcceptanceOptions(value:IdeOptions,mode:string,checksOnly=false):StartTaskOptions{
 if(mode!=='agent'){if(checksOnly)throw Error('Для запуска проверок переключитесь в Agent');return {...emptyAcceptanceOptions(),read_only:true,checks_only:false};}
 if(value.checks.length>8)throw Error('Допускается до 8 проверок и 12 критериев');
 const selected=value.criteria.map((text,index)=>({text:text.trim(),index})).filter(row=>row.text);
 if(selected.length>12)throw Error('Допускается до 12 критериев');
 if(selected.some(row=>row.text.length>500||row.text.includes('\0')))throw Error('Критерий: до 500 символов');
 const ids=new Set<string>();
 const checks:ValidationCommand[]=value.checks.map(check=>{
  if(!/^[\p{L}\p{N}_-]{1,80}$/u.test(check.id)||ids.has(check.id))throw Error('Проверки должны иметь уникальные ID');ids.add(check.id);
  const purpose=check.purpose.trim(),program=check.program.trim(),cwd=check.cwd;
  if(!purpose||purpose.length>300||purpose.includes('\0')||!program||program.length>2000||program.includes('\0'))throw Error('Укажите назначение и программу каждой проверки');
  if(!cwd||cwd.length>1000||cwd.includes('\0')||cwd.replaceAll('\\','/').startsWith('/')||cwd.includes(':')||cwd.replaceAll('\\','/').split('/').includes('..'))throw Error('Папка проверки должна находиться внутри проекта');
  if(!Number.isInteger(check.timeout)||check.timeout<1||check.timeout>120)throw Error('Время проверки: 1–120 секунд');
  if(check.arguments.length>100||check.arguments.some(arg=>arg.length>8000||arg.includes('\0')))throw Error('Аргументы проверки: до 100 строк, по 8000 символов');
  const kind=check.kind||'custom';if(!['test','lint','types','syntax','custom','diagnostics'].includes(kind))throw Error('Неизвестный тип проверки');
  const args=kind==='diagnostics'&&check.arguments.length===1?[check.arguments[0].trim().replaceAll('\\','/')]:[...check.arguments];
  const applies_to=(check.applies_to||[]).map(p=>p.trim().replaceAll('\\','/')).filter(Boolean);
  if(applies_to.length>12||applies_to.some(p=>p.length>240||p.includes('\0')||p.startsWith('/')||p.includes(':')||p.split('/').includes('..')))throw Error('Шаблоны проверки должны быть относительными путями');
  const evidence_scope:EvidenceScope=check.evidence_scope?.kind==='files'?{kind:'files',files:paths(check.evidence_scope.files),dependencies:paths(check.evidence_scope.dependencies)}:{kind:'workspace'};
  if(evidence_scope.kind==='files'&&!evidence_scope.files.length)throw Error('Укажите хотя бы один файл области проверки');
  if(kind==='diagnostics'&&(program!=='lsp'||args.length!==1||evidence_scope.kind!=='files'||!evidence_scope.files.includes(args[0])))throw Error('LSP проверяет один сохранённый файл из указанной области');
  return {...check,purpose,program,cwd,kind,arguments:args,applies_to,evidence_scope};
 });
 const criteria_links=Object.fromEntries(selected.map((row,index)=>{const links=value.criteria_links[String(row.index)]||[];if(links.some(id=>!ids.has(id)))throw Error('Критерий ссылается на удалённую проверку');return [String(index),[...links]];}));
 if(checksOnly&&!checks.length)throw Error('Сначала добавьте хотя бы одну проверку');
 return {read_only:false,auto_checks:value.auto_checks,checks_only:checksOnly,criteria:selected.map(row=>row.text),criteria_links,checks};
}
