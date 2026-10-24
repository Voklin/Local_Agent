import { useEffect, useState } from 'react';

export function ConnectionsSettings({busy}:{busy:boolean}) {
  const [enabled,setEnabled]=useState(false);
  const [applications,setApplications]=useState<{id:string;name:string;custom:boolean}[]>([]);
  const [token,setToken]=useState('');
  const [owner,setOwner]=useState('');
  const [remember,setRemember]=useState(false);
  const [status,setStatus]=useState<any>({state:'disconnected'});
  const [notice,setNotice]=useState('');
  const [working,setWorking]=useState(false);
  useEffect(()=>{
    let alive=true;
    void window.lca.desktopSettings().then(result=>{if(alive&&result.ok)setEnabled(result.enabled);});
    void window.lca.desktopApplications().then(result=>{if(alive&&result.ok)setApplications(result.applications);});
    const refresh=async()=>{try{const result=await window.lca.telegramStatus();if(alive)setStatus(result);}catch(error){if(alive)setNotice(String(error));}};
    void refresh();const timer=setInterval(()=>void refresh(),1500);
    return()=>{alive=false;clearInterval(timer);};
  },[]);
  async function toggle() {
    try{const result=await window.lca.configureDesktop(!enabled);if(!result.ok)throw Error(result.error);setEnabled(result.enabled);}
    catch(error){setNotice(String(error));}
  }
  async function connect(saved=false) {
    setWorking(true);setNotice('');
    try{const result=await window.lca.connectTelegram({token,owner_id:owner,remember,use_saved:saved});if(!result.ok)throw Error(result.error);setStatus(result);setToken('');if(result.warning)setNotice(result.warning);}
    catch(error){setNotice(String(error));}finally{setWorking(false);}
  }
  async function changeApplication(id?:string) {
    setWorking(true);setNotice('');
    try{
      const result=id?await window.lca.removeDesktopApplication(id):await window.lca.addDesktopApplication();
      if(!result.ok)throw Error(result.error);setApplications(result.applications);
    }catch(error){setNotice(String(error));}finally{setWorking(false);}
  }
  return <section className="settings-section connections-settings"><h3>Инструменты ПК и Telegram</h3>
    <label className="auto-speak"><input type="checkbox" checked={enabled} disabled={busy} onChange={()=>void toggle()}/>Включить приложения, поиск, скриншоты и чтение разрешённых папок</label>
    <p className="settings-help">Скажите Лоле «Открой калькулятор», «Найди в браузере информацию о…» или «Найди музыку…». Музыка открывается в YouTube, Яндекс Музыке, VK Музыке или Spotify; аккаунт и нажатие Play могут потребоваться на сайте. Локальное аудио открывается только из папки, указанной в исходном запросе в кавычках. Приложения запускаются без командной строки.</p>
    <details><summary>Разрешённые приложения ({applications.length})</summary>
      {applications.map(item=><div className="connection-actions" key={item.id}><span>{item.name}</span>{item.custom&&<button type="button" className="secondary-button" disabled={busy||working} onClick={()=>void changeApplication(item.id)}>Убрать</button>}</div>)}
      <button type="button" className="secondary-button" disabled={busy||working} onClick={()=>void changeApplication()}>Добавить приложение…</button>
      <p className="settings-help">Выберите EXE-файл через окно Windows. Лола получает название и ID; она не может добавлять приложения или передавать аргументы запуска.</p>
    </details>
    <p className="settings-help">Скриншот требует явного запроса. Для дополнительных папок укажите полный путь в двойных кавычках в сообщении. Модель не может сама расширить доступ. Запись вне выбранного проекта не предоставляется.</p>
    <details><summary>Telegram: удалённое управление</summary>
      <p>Бот принимает команды только от вашего user ID в личном чате. Ответы агента, путь проекта и diff передаются в Telegram вашему ID для контроля и подтверждения изменений.</p>
      <label>BotFather token<input type="password" autoComplete="off" value={token} onChange={e=>setToken(e.target.value)} placeholder="123456789:…"/></label>
      <label>Ваш Telegram user ID<input inputMode="numeric" value={owner} onChange={e=>setOwner(e.target.value)} placeholder="Числовой ID пользователя"/></label>
      <label className="auto-speak"><input type="checkbox" checked={remember} onChange={e=>setRemember(e.target.checked)}/>Сохранить токен защищённо на этом ПК</label>
      <div className="connection-actions"><button type="button" className="primary-button" disabled={working||status.state!=='disconnected'||!token||!owner} onClick={()=>void connect()}>Подключить бота</button><button type="button" className="secondary-button" disabled={working||status.state!=='disconnected'} onClick={()=>void connect(true)}>Подключить сохранённого</button><button type="button" className="secondary-button" disabled={status.state==='disconnected'} onClick={()=>void window.lca.disconnectTelegram().then(setStatus)}>Отключить</button><button type="button" className="secondary-button" onClick={()=>void window.lca.forgetTelegram().then(()=>setNotice('Сохранённый токен удалён'))}>Забыть токен</button></div>
      <p role="status">Telegram: {status.state}{status.username?` · @${status.username}`:''} {status.error}</p>
      <p className="settings-help">Команды: /help, /status, /result, /resume, /stop, /chat задача, /ide задача, /miya задача, /approval, /approve ID, /reject ID. При подключении старые команды пропускаются. Приложение и ПК должны оставаться запущенными; webhook у бота должен быть отключён.</p>
    </details><p role="status">{notice}</p>
  </section>;
}
