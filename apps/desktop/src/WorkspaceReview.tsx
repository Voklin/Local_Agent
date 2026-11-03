import { useEffect, useState } from 'react';
import type { TaskSnapshot } from './TaskProgress';

type WorkspaceSnapshot={git_checkpoint?:{commit:string;repository:string;ref:string}|null;id:string;status:string;paths:string[];operations:string[]};
type RollbackPreview={id:string;group_id:string;paths:string[];diff:string;truncated:boolean};
const labels:Record<string,string>={applied:'Можно сравнить',rolled_back:'Отменено',prepared:'Снимок не завершён',unknown:'Автооткат недоступен',rolling_back:'Откат прерван',rollback_unknown:'Нужна проверка файлов',abandoned:'Проверено вручную',failed:'Без изменений'};

export function WorkspaceReview({chatId,root,busy,dirty,revision,onTask,onRestored,onWorking}:{chatId:string;root:string;busy:boolean;dirty:boolean;revision:number;onTask:(task:TaskSnapshot)=>void;onRestored:()=>void;onWorking:(working:boolean)=>void}) {
  const [items,setItems]=useState<WorkspaceSnapshot[]>([]),[notice,setNotice]=useState(''),[working,setWorking]=useState(false);
  const [checkpointing,setCheckpointing]=useState(false);
  const [preview,setPreview]=useState<RollbackPreview|null>(null),[reviewing,setReviewing]=useState('');
  useEffect(()=>{let current=true;if(!chatId||busy){setPreview(null);return;}void window.lca.listSnapshots({chat_id:chatId}).then(result=>{if(!current)return;if(result.ok)setItems(result.snapshots);else setNotice(result.error);});return()=>{current=false;};},[chatId,root,busy,revision]);
  async function compareSnapshot(group_id:string){
    if(dirty||busy||working)return;setWorking(true);onWorking(true);setNotice('');
    try{const result=await window.lca.previewRollback({chat_id:chatId,group_id});if(!result.ok)throw Error(result.error);setPreview(result.proposal);}
    catch(error){setNotice(error instanceof Error?error.message:String(error));}
    finally{setWorking(false);onWorking(false);}
  }
  async function saveCheckpoint(group_id:string){
    if(busy||dirty||working)return;setWorking(true);onWorking(true);setCheckpointing(true);setNotice('Сохраняем подтверждённые версии в отдельный Git Лешего…');
    try{const result=await window.lca.createGitCheckpoint({chat_id:chatId,group_id});if(!result.ok)throw Error(result.error);setItems(items.map(item=>item.id===group_id?{...item,git_checkpoint:result.checkpoint}:item));setNotice('Git-снимок сохранён: '+result.checkpoint.commit.slice(0,12)+'. Ветка и индекс проекта не менялись.');}
    catch(error){setNotice(error instanceof Error?error.message:String(error));}finally{setWorking(false);setCheckpointing(false);onWorking(false);}
  }
  async function applyRollback(){
    if(!preview||dirty||busy||working)return;setWorking(true);onWorking(true);setNotice('');
    try{const result=await window.lca.applyRollback({chat_id:chatId,proposal_id:preview.id,confirmed:true});setPreview(null);if(result.snapshots)setItems(result.snapshots);if(result.task)onTask(result.task);if(!result.ok)throw Error(result.error);setNotice('Файлы восстановлены. Прежние результаты проверок устарели.');onRestored();}
    catch(error){setNotice(error instanceof Error?error.message:String(error));}
    finally{setWorking(false);onWorking(false);}
  }
  async function confirmManualReview(group_id:string){
    setWorking(true);onWorking(true);setNotice('');
    try{const result=await window.lca.reviewRollback({chat_id:chatId,group_id,confirmed:true});if(!result.ok)throw Error(result.error);setItems(result.snapshots);if(result.task)onTask(result.task);setReviewing('');setNotice('Ручная проверка сохранена. Файлы не изменялись.');}
    catch(error){setNotice(error instanceof Error?error.message:String(error));}
    finally{setWorking(false);onWorking(false);}
  }
  if(!chatId)return null;
  return <section className="workspace-review" aria-label="Изменения и откат"><h4>Изменения и откат</h4><p className="task-check-note">Снимки охватывают файловые инструменты агента. Команды и внешние действия требуют отдельной проверки.</p>
    {dirty&&<p role="status">Сначала сохраните или отмените несохранённые правки редактора.</p>}
    {items.map((item,index)=><div className="snapshot-card" key={item.id} data-snapshot-status={item.status}><b>Набор правок {items.length-index}</b><span>{labels[item.status]||item.status}</span><ul>{item.paths.map(path=><li key={path}><code>{path}</code></li>)}</ul>
      {item.git_checkpoint&&<details className="git-checkpoint-info"><summary>Git-снимок · {item.git_checkpoint.commit.slice(0,12)}</summary><p>Архив подтверждённых версий в профиле Лешего. Для обычного отката используйте «Сравнить и отменить».</p><p>Хранилище: <code>{item.git_checkpoint.repository}</code></p><p>Коммит: <code>{item.git_checkpoint.commit}</code></p><p>Ссылка: <code>{item.git_checkpoint.ref}</code></p></details>}
      {item.status==='applied'&&<button type="button" className="secondary-button" disabled={busy||working||dirty} onClick={()=>void saveCheckpoint(item.id)}>Сохранить Git-снимок</button>}
      {item.status==='applied'&&<button type="button" className="secondary-button" disabled={busy||working||dirty} onClick={()=>void compareSnapshot(item.id)}>Сравнить и отменить</button>}
      {['rolling_back','rollback_unknown'].includes(item.status)&&(reviewing===item.id?<div><p>Вы вручную проверили все затронутые файлы? Подтверждение снимет блокировку и не будет повторять откат.</p><button type="button" disabled={busy||working} onClick={()=>void confirmManualReview(item.id)}>Подтвердить ручную проверку</button><button type="button" onClick={()=>setReviewing('')}>Назад</button></div>:<button type="button" disabled={busy||working} onClick={()=>setReviewing(item.id)}>Я проверил файлы вручную</button>)}
    </div>)}
    {checkpointing&&<button type="button" onClick={()=>void window.lca.cancelGitCheckpoint()}>Отменить сохранение Git</button>}
    {!items.length&&<p className="task-check-note">Подтверждённых файловых правок пока нет.</p>}{notice&&<p role="status" className="task-stop-reason">{notice}</p>}
    {preview&&<section className="rollback-preview" aria-label="Предпросмотр отката"><h4>Вернуть исходное состояние</h4><p>Будут восстановлены только перечисленные файлы. Если ревизии изменились, откат отменится.</p><pre>{preview.diff}</pre>{preview.truncated&&<p>Большой diff сокращён для просмотра.</p>}<button type="button" className="secondary-button" onClick={()=>setPreview(null)} disabled={working}>Назад</button><button type="button" className="primary-button" disabled={busy||dirty||working} onClick={()=>void applyRollback()}>Подтвердить откат файлов</button></section>}
  </section>;
}
