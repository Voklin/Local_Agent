import {useEffect,useState} from 'react';
import {lolaDesktopDefaults,type LolaDesktopSettings} from '../shared/lolaDesktop';

export function DesktopLolaSettings(){
  const [draft,setDraft]=useState<LolaDesktopSettings>(lolaDesktopDefaults),[notice,setNotice]=useState(''),[working,setWorking]=useState(false);
  useEffect(()=>{void window.lca.getDesktopLola().then(r=>{if(r.ok)setDraft(r.settings);else setNotice(r.error);});return window.lca.onEvent(event=>{if(event.event==='lola_config')setDraft(event.settings);});},[]);
  async function save(value=draft){
    setWorking(true);try{const r=await window.lca.configureDesktopLola(value);if(!r.ok)throw Error(r.error);setDraft(r.settings);setNotice(value.enabled?'Лола доступна на рабочем столе и в трее.':'Спутник выключен.');}
    catch(e){setNotice(String(e instanceof Error?e.message:e));}finally{setWorking(false);}
  }
  return <fieldset className="voice-input-settings lola-desktop-settings"><legend>Лола на рабочем столе</legend>
    <label className="auto-speak"><input type="checkbox" aria-label="Настольная Лола" checked={draft.enabled} disabled={working} onChange={e=>setDraft({...draft,enabled:e.target.checked})}/>Показывать спутника и значок в трее</label>
    <label>Расположение<select aria-label="Режим настольной Лолы" disabled={working} value={draft.mode} onChange={e=>setDraft({...draft,mode:e.target.value as LolaDesktopSettings['mode']})}><option value="top">Поверх обычных окон</option><option value="desktop">Обычное окно на рабочем столе</option><option value="tray">Только в трее</option></select></label>
    <label>Размер · {draft.size} пикселей<input aria-label="Размер настольной Лолы" type="range" min={180} max={360} step={10} value={draft.size} disabled={working} onChange={e=>setDraft({...draft,size:Number(e.target.value)})}/></label>
    <label className="auto-speak"><input type="checkbox" aria-label="Анимации настольной Лолы" disabled={working} checked={draft.animate} onChange={e=>setDraft({...draft,animate:e.target.checked})}/>Анимации персонажа</label>
    <label className="auto-speak"><input type="checkbox" aria-label="Клики сквозь Лолу" disabled={working} checked={draft.clickThrough} onChange={e=>setDraft({...draft,clickThrough:e.target.checked})}/>Пропускать все клики к окнам под Лолой</label>
    <p className="settings-help">Лолу можно перетаскивать. При пропуске кликов верните управление через меню значка Лешего в трее. Когда спутник включён, закрытие основного окна сворачивает Лешего в трей. Полный выход — через меню трея; микрофон включается только вашим действием. Обычный режим не закрепляет персонажа в обоях Windows.</p>
    <button type="button" className="secondary-button" disabled={working} onClick={()=>void save()}>Применить расположение Лолы</button>
    <button type="button" className="secondary-button" disabled={working} onClick={()=>void save({...draft,position:null,clickThrough:false})}>Вернуть в угол экрана</button><p role="status">{notice}</p>
  </fieldset>;
}
