import { useEffect, useState } from 'react';
import { Archive, CheckCircle2, RefreshCw } from 'lucide-react';

type StorageReport = {version:number;integrity:string;migration:{chats:number;messages:number};counts:{chats:number;messages:number;projects:number};sources:{status:string;path:string}[]};

export function StorageSettings({busy}:{busy:boolean}) {
  const [report,setReport]=useState<StorageReport|null>(null),[working,setWorking]=useState(false),[notice,setNotice]=useState('');
  async function inspectStorage() {
    setWorking(true);setNotice('');
    try {const result=await window.lca.storageStatus();if(!result.ok)throw Error(result.error);setReport(result.report);}
    catch(error){setNotice(error instanceof Error?error.message:String(error));}
    finally{setWorking(false);}
  }
  useEffect(()=>{void inspectStorage();},[]);
  async function backupStorage() {
    if(busy||working)return;
    setWorking(true);setNotice('Создаём резервную копию…');
    try {const result=await window.lca.backupStorage();if(result.canceled){setNotice('Сохранение отменено.');return;}if(!result.ok)throw Error(result.error);setNotice('Резервная копия сохранена: '+result.path);}
    catch(error){setNotice(error instanceof Error?error.message:String(error));}
    finally{setWorking(false);}
  }
  const skipped=report?.sources.filter(source=>source.status==='skipped')||[];
  return <section className="settings-section storage-settings" aria-label="История и резервные копии">
    <div className="section-intro"><span className="eyebrow">ВАШЕ ПРОСТРАНСТВО</span><h3>История под рукой.</h3><p>Разговоры, проекты и состояние задач сохраняются на этом компьютере.</p></div>
    {report&&<div className="settings-notice"><p><CheckCircle2 size={16}/> {report.integrity==='ok'?'Хранилище проверено.':'Нужна проверка хранилища: '+report.integrity}</p><p>Чатов: {report.counts.chats} · сообщений: {report.counts.messages} · проектов: {report.counts.projects}</p><p>При переходе перенесено чатов: {report.migration.chats}, сообщений: {report.migration.messages}. Исходные файлы сохранены.</p></div>}
    {skipped.length>0&&<p role="alert">Не удалось перенести файлов: {skipped.length}. Их исходники сохранены; подробности показаны в предупреждениях истории.</p>}
    <div className="generation-presets"><button type="button" className="secondary-button" disabled={busy||working} onClick={()=>void inspectStorage()}><RefreshCw size={14}/>Проверить хранилище</button><button type="button" className="secondary-button" disabled={busy||working} onClick={()=>void backupStorage()}><Archive size={14}/>Сохранить резервную копию</button></div>
    <p className="settings-help">В ZIP входят чаты, проекты, результаты инструментов и сохранённые исходники истории. Выберите личную папку вне каталога данных приложения. Для переноса закройте Лешего и восстановите копию в пустой каталог данных. Голосовые модели и настройки подключения сохраняются отдельно.</p>
    {working&&<button type="button" className="secondary-button" onClick={()=>void window.lca.cancelStorageBackup()}>Отменить фоновую операцию</button>}
    {notice&&<p role="status" aria-live="polite" className="settings-notice">{notice}</p>}
  </section>;
}
