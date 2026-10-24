import { useEffect, useState } from 'react';

export type Appearance = {theme:'dark'|'light';accent:'violet'|'blue'|'mint';density:'comfortable'|'compact';sidebar:boolean;statusbar:boolean;output:boolean};
const defaults:Appearance={theme:'dark',accent:'violet',density:'comfortable',sidebar:true,statusbar:false,output:false};
const storageKey='localagent.appearance.v1';

export function readAppearance():Appearance {
  try {
    const saved=JSON.parse(localStorage.getItem(storageKey)||'{}')||{};
    return {theme:saved.theme==='light'?'light':'dark',accent:['violet','blue','mint'].includes(saved.accent)?saved.accent:'violet',density:saved.density==='compact'?'compact':'comfortable',
      sidebar:typeof saved.sidebar==='boolean'?saved.sidebar:defaults.sidebar,statusbar:typeof saved.statusbar==='boolean'?saved.statusbar:defaults.statusbar,output:typeof saved.output==='boolean'?saved.output:defaults.output};
  }catch{return {...defaults};}
}

export function saveAppearance(value:Appearance) {
  localStorage.setItem(storageKey,JSON.stringify(value));window.dispatchEvent(new Event('appearance-changed'));
}

export function useAppearance() {
  const [value,setValue]=useState(readAppearance);
  useEffect(()=>{const refresh=()=>setValue(readAppearance());window.addEventListener('appearance-changed',refresh);window.addEventListener('storage',refresh);return()=>{window.removeEventListener('appearance-changed',refresh);window.removeEventListener('storage',refresh);};},[]);
  return value;
}

export function AppearanceSettings() {
  const value=useAppearance();const [notice,setNotice]=useState('Изменения применяются сразу и сохраняются на этом ПК.');
  function update(patch:Partial<Appearance>) {try{saveAppearance({...value,...patch});setNotice('Оформление сохранено');}catch{setNotice('Не удалось сохранить оформление');}}
  return <section className="settings-section appearance-settings"><h3>Ваше рабочее пространство</h3><p className="settings-help">Спокойный интерфейс для Chat и IDE. У Лолы — собственные мягкие акценты.</p>
    <label>Тема<select aria-label="Тема интерфейса" value={value.theme} onChange={event=>update({theme:event.target.value as Appearance['theme']})}><option value="dark">Тёмная · графит</option><option value="light">Светлая · бумага</option></select></label>
    <label>Акцент<select aria-label="Акцент интерфейса" value={value.accent} onChange={event=>update({accent:event.target.value as Appearance['accent']})}><option value="violet">Лаванда</option><option value="blue">Небесный</option><option value="mint">Мятный</option></select></label>
    <label>Плотность<select aria-label="Плотность интерфейса" value={value.density} onChange={event=>update({density:event.target.value as Appearance['density']})}><option value="comfortable">Свободная</option><option value="compact">Компактная</option></select></label>
    {([{key:'sidebar',label:'Боковая панель и история'},{key:'output',label:'Журнал событий в IDE'},{key:'statusbar',label:'Нижняя строка состояния'}] as const).map(item=><label className="appearance-toggle" key={item.key}><input type="checkbox" aria-label={item.label} checked={value[item.key]} onChange={event=>update({[item.key]:event.target.checked})}/>{item.label}</label>)}
    <button type="button" className="secondary-button" onClick={()=>update(defaults)}>Вернуть стандартное оформление</button><p role="status" className="settings-help">{notice}</p>
  </section>;
}
