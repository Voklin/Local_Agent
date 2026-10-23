import { useEffect, useState } from 'react';

const memoryFields=[
  {key:'project_summary',label:'Описание проекта',limit:1200},
  {key:'current_focus',label:'Текущая задача',limit:600},
  {key:'next_steps',label:'Следующие шаги',limit:800},
  {key:'decisions',label:'Решения',limit:300,count:30},
  {key:'constraints',label:'Ограничения',limit:300,count:30},
  {key:'conventions',label:'Соглашения',limit:300,count:30},
  {key:'important_files',label:'Важные файлы',limit:240,count:40},
];

export function MemoryPanel({root,busy,onClose}:{root:string;busy:boolean;onClose:()=>void}) {
  const [draft,setDraft]=useState<Record<string,string>|null>(null);
  const [original,setOriginal]=useState('');
  const [revision,setRevision]=useState('');
  const [notice,setNotice]=useState('Загрузка…');
  const [working,setWorking]=useState(false);
  const [discard,setDiscard]=useState(false);
  const dirty=!!draft&&JSON.stringify(draft)!==original;
  function show(result:any) {
    if(!result.ok)throw new Error(result.error);
    if(result.root!==root)throw new Error('Проект изменился. Откройте память заново.');
    const fields=Object.fromEntries(memoryFields.map(field=>[field.key,field.count?result.memory[field.key].join('\n'):result.memory[field.key]]));
    setDraft(fields);setOriginal(JSON.stringify(fields));setRevision(result.revision);setDiscard(false);
  }
  useEffect(()=>{
    let active=true;
    window.lca.getProjectMemory().then(result=>{if(active){show(result);setNotice('Заметки применятся к следующей задаче агента.');}}).catch(error=>{if(active)setNotice(String(error));});
    return ()=>{active=false;};
  },[root]);
  async function save() {
    if(!draft||busy||working)return;
    setWorking(true);
    try {
      const memory=Object.fromEntries(memoryFields.map(field=>[field.key,field.count?draft[field.key].split('\n').map(s=>s.trim()).filter(Boolean):draft[field.key]]));
      const result=await window.lca.saveProjectMemory(memory,revision);show(result);setNotice('Память сохранена.');
    }catch(error){setNotice(String(error));}finally{setWorking(false);}
  }
  function close() {if(dirty)setDiscard(true);else onClose();}
  return <div className="modal-backdrop"><section className="settings-dialog memory-dialog" role="dialog" aria-modal="true" aria-labelledby="memory-title" onKeyDown={event=>{if(event.key==='Escape'&&!working){event.preventDefault();close();}}}>
    <header className="settings-header"><div><h2 id="memory-title">Память проекта</h2><p>{root}</p></div></header>
    <form className="model-settings" onSubmit={event=>{event.preventDefault();void save();}}>
      <div className="settings-scroll"><p className="settings-help">Компактные справочные заметки для IDE. Личный Chat их не использует. Модель также может обновлять память после задачи; конфликт сохранения сохраняет ваш черновик. Списки — по одному пункту на строке.</p>
        {draft&&memoryFields.map(field=><label className="memory-field" key={field.key}>{field.label}<textarea aria-label={field.label} value={draft[field.key]} maxLength={field.count?field.count*(field.limit+1):field.limit} disabled={working||busy} onChange={event=>setDraft({...draft,[field.key]:event.target.value})}/><small>{field.count?`До ${field.count} пунктов по ${field.limit} символов`:`${draft[field.key].length}/${field.limit}`}</small></label>)}
      </div>
      <footer className="settings-footer"><p className="settings-feedback" role="status">{notice}</p>{discard?<div className="settings-actions"><span>Закрыть и потерять черновик?</span><button type="button" onClick={()=>setDiscard(false)}>Продолжить редактирование</button><button type="button" onClick={onClose}>Закрыть без сохранения</button></div>:<div className="settings-actions"><button type="button" className="secondary-button" disabled={working} onClick={close}>Закрыть</button><button type="submit" className="primary-button save-memory" disabled={!draft||!dirty||busy||working}>Сохранить память</button></div>}</footer>
    </form>
  </section></div>;
}
