import {useEffect,useRef,useState} from 'react';

export function WorkspaceAccessSettings({root,busy}:{root:string;busy:boolean}) {
  const [paths,setPaths]=useState(''),[patterns,setPatterns]=useState<string[]>([]),[notice,setNotice]=useState('');
  const [confirmed,setConfirmed]=useState(false),[working,setWorking]=useState(false);
  const locked=useRef(false),scope=useRef(root);scope.current=root;
  useEffect(()=>{
    let disposed=false;setConfirmed(false);setNotice('');setPaths('');setPatterns([]);
    if(root)void window.lca.workspaceAccess().then(r=>{if(disposed)return;if(r.ok&&r.root===root){setPaths(r.exceptions.join('\n'));setPatterns(r.ignore_patterns);}else if(!r.ok)setNotice(r.error);}).catch(e=>{if(!disposed)setNotice(String(e));});
    return()=>{disposed=true;};
  },[root]);
  async function save() {
    if(locked.current||busy||!root)return;
    const savedRoot=root,entries=paths.split('\n').map(p=>p.trim()).filter(Boolean);
    if(entries.length&&!confirmed){setNotice('Подтвердите доступ к указанным файлам.');return;}
    locked.current=true;setWorking(true);setNotice('');
    try{const r=await window.lca.configureWorkspaceAccess(entries,confirmed||!entries.length);if(scope.current!==savedRoot)return;if(!r.ok)throw Error(r.error);window.dispatchEvent(new Event('workspace-access-changed'));setPaths(r.exceptions.join('\n'));setConfirmed(false);setNotice('Разрешения проекта сохранены.');}
    catch(e){if(scope.current===savedRoot)setNotice(e instanceof Error?e.message:String(e));}
    finally{locked.current=false;setWorking(false);}
  }
  return <details className="settings-section workspace-access-settings"><summary>Доступ модели к файлам проекта</summary>
    <p>Секреты, приватные ключи и пути из .neutralignore скрыты от автоматического чтения. В редакторе вы можете открывать их самостоятельно.</p>
    <label>Разрешить конкретные файлы — по одному пути относительно проекта<textarea aria-label="Разрешённые защищённые файлы" rows={3} value={paths} disabled={busy||working||!root} onChange={e=>{setPaths(e.target.value);setConfirmed(false);}} placeholder="Например: .env"/></label>
    <label className="auto-speak"><input aria-label="Подтвердить доступ модели к защищённым файлам" type="checkbox" checked={confirmed} disabled={busy||working||!root} onChange={e=>setConfirmed(e.target.checked)}/>Разрешаю модели читать и предлагать изменения этих файлов. Их содержимое может быть отправлено подключённому серверу модели.</label>
    {!!patterns.length&&<p>Исключения .neutralignore: {patterns.join(', ')}</p>}
    <button type="button" className="secondary-button" disabled={busy||working||!root} onClick={()=>void save()}>{working?'Сохраняю…':'Сохранить доступ модели'}</button>
    {notice&&<p role="status">{notice}</p>}
  </details>;
}
