import {useState} from 'react';

type Profile={id?:string;title:string;summary:string;instructions:string;tools:string[];enabled:boolean;source?:string;version?:number};
type Catalog={enabled:boolean;profiles:Profile[]};
const reads=[['list_files','Список файлов'],['read_file','Читать файл'],['read_range','Читать диапазон строк']];
const empty:Profile={title:'',summary:'',instructions:'',tools:reads.map(([id])=>id),enabled:false};

export function SubagentSettings({catalog,busy,save,query=''}:{catalog:Catalog;busy:boolean;query?:string;save:(params:any)=>Promise<any>}) {
  const [draft,setDraft]=useState<Profile|null>(null),[removing,setRemoving]=useState<string|null>(null);
  async function persist(){if(!draft)return;const result=await save({kind:'subagent_save',...draft});if(result)setDraft(null);}
  return <div className="subagent-settings">
    <div className="capability-card"><div><b>Дочерние исследования в IDE</b><p>Исследователь работает на той же модели, читает разрешённые файлы и возвращает источники. До трёх запусков, без вложенных детей. Stop останавливает всё дерево.</p></div><label><input type="checkbox" role="switch" aria-label="Использовать субагентов" disabled={busy} checked={catalog.enabled} onChange={e=>void save({kind:'subagents_toggle',enabled:e.target.checked})}/>{catalog.enabled?'Включены':'Выключены'}</label></div>
    <p className="settings-help">Для простых задач агент работает самостоятельно. Профили модели сохраняются выключенными: прочитайте инструкцию перед включением. Профиль не получает отдельную модель, команды, MCP или право изменять файлы.</p>
    <button type="button" disabled={busy} onClick={()=>setDraft({...empty,tools:[...empty.tools]})}>Создать субагента</button>
    {catalog.profiles.filter(p=>[p.title,p.summary,p.id].join(' ').toLocaleLowerCase().includes(query.toLocaleLowerCase())).map(p=><div className="capability-card" key={p.id}><div><button type="button" className="text-button" onClick={()=>setDraft({...p,tools:[...p.tools]})}>{p.title}</button><p>{p.summary}</p><small>{p.source==='model'?'Предложен моделью':p.source==='builtin'?'Встроенный':'Ваш профиль'} · версия {p.version} · ID: {p.id}</small><p>{p.tools.map(id=>reads.find(([key])=>key===id)?.[1]).join(' · ')}</p></div><input type="checkbox" role="switch" aria-label={'Субагент '+p.title} disabled={busy||!catalog.enabled} checked={p.enabled} onChange={e=>void save({kind:'subagent_save',...p,enabled:e.target.checked})}/>{p.id!=='research'&&<button type="button" disabled={busy} onClick={()=>setRemoving(p.id!)}>Удалить</button>}</div>)}
    {draft&&<div className="inline-editor subagent-editor"><div className="settings-section-heading"><h3>Профиль исследователя</h3><button type="button" onClick={()=>setDraft(null)}>Закрыть</button></div>
      <label>Название<input maxLength={80} value={draft.title} onChange={e=>setDraft({...draft,title:e.target.value})}/></label>
      <label>Когда использовать<input maxLength={300} value={draft.summary} onChange={e=>setDraft({...draft,summary:e.target.value})}/></label>
      <label>Инструкция<textarea rows={6} maxLength={4000} value={draft.instructions} onChange={e=>setDraft({...draft,instructions:e.target.value})}/></label>
      <fieldset><legend>Доступ к файлам · в пределах прав родителя</legend>{reads.map(([id,title])=><label className="check-row" key={id}><input type="checkbox" checked={draft.tools.includes(id)} onChange={e=>setDraft({...draft,tools:e.target.checked?[...draft.tools,id]:draft.tools.filter(t=>t!==id)})}/>{title}</label>)}</fieldset>
      <label className="check-row"><input type="checkbox" checked={draft.enabled} onChange={e=>setDraft({...draft,enabled:e.target.checked})}/>Включить после сохранения</label>
      <button type="button" disabled={busy||!draft.title.trim()||!draft.summary.trim()||draft.instructions.trim().length<10||!draft.tools.length} onClick={()=>void persist()}>Сохранить профиль</button>
    </div>}
    {removing&&<div className="inline-confirm" role="alert"><p>Удалить профиль? Выполненные исследования останутся в истории.</p><button type="button" disabled={busy} onClick={()=>void save({kind:'subagent_delete',id:removing}).then(r=>{if(r){setRemoving(null);setDraft(null);}})}>Да, удалить</button><button type="button" onClick={()=>setRemoving(null)}>Отмена</button></div>}
  </div>;
}
