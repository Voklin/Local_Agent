import {applyTheme,normalizeTheme,leshyThemes,type LeshyTheme} from './design/themes';
import {LayoutPresets} from './StudioControls';
import { useEffect, useState } from 'react';

export type Appearance = {theme:LeshyTheme;backgroundArt:boolean;accent:'rose'|'violet'|'blue'|'mint';density:'comfortable'|'compact';sidebar:boolean;statusbar:boolean;output:boolean};
const defaults:Appearance={theme:'forest',backgroundArt:true,accent:'mint',density:'comfortable',sidebar:true,statusbar:true,output:false};
const storageKey='localagent.appearance.v1';
let themeRevision=0;

export function readAppearance():Appearance {
  try {
    const saved=JSON.parse(localStorage.getItem(storageKey)||'{}')||{};
    if(localStorage.getItem('neutral.studio.appearance.v1')!=='1'){saved.accent='mint';saved.statusbar=true;localStorage.setItem(storageKey,JSON.stringify(saved));localStorage.setItem('neutral.studio.appearance.v1','1');}
    return {theme:normalizeTheme(saved.theme),backgroundArt:saved.backgroundArt!==false,accent:['rose','violet','blue','mint'].includes(saved.accent)?saved.accent:'mint',density:saved.density==='compact'?'compact':'comfortable',
      sidebar:typeof saved.sidebar==='boolean'?saved.sidebar:defaults.sidebar,statusbar:typeof saved.statusbar==='boolean'?saved.statusbar:defaults.statusbar,output:typeof saved.output==='boolean'?saved.output:defaults.output};
  }catch{return {...defaults};}
}

export function saveAppearance(value:Appearance) {
  const previous=readAppearance().theme;
  if(previous!==value.theme)themeRevision++;
  localStorage.setItem(storageKey,JSON.stringify(value));applyTheme(value.theme,value.backgroundArt);window.dispatchEvent(new Event('appearance-changed'));
  if(previous!==value.theme)void window.lca?.setAppearanceTheme(value.theme);
}

let syncStarted=false;
export function startAppearanceSync(){
 if(syncStarted||!window.lca)return;syncStarted=true;
 const receive=(theme:unknown)=>{themeRevision++;const next={...readAppearance(),theme:normalizeTheme(theme)};localStorage.setItem(storageKey,JSON.stringify(next));applyTheme(next.theme,next.backgroundArt);window.dispatchEvent(new Event('appearance-changed'));};
 window.lca.onEvent(event=>{if(event.event==='appearance_theme')receive(event.theme);});
 const revision=themeRevision;
 void window.lca.getAppearanceTheme(readAppearance().theme).then(result=>{if(result.ok&&revision===themeRevision)receive(result.theme);}).catch(()=>{/* Keep the locally saved appearance if the host is unavailable. */});
}

export function useAppearance() {
  const [value,setValue]=useState(readAppearance);
  useEffect(()=>applyTheme(value.theme,value.backgroundArt),[value.theme,value.backgroundArt]);
  useEffect(()=>{const refresh=()=>setValue(readAppearance());window.addEventListener('appearance-changed',refresh);window.addEventListener('storage',refresh);return()=>{window.removeEventListener('appearance-changed',refresh);window.removeEventListener('storage',refresh);};},[]);
  return value;
}

export function AppearanceSettings() {
  const value=useAppearance();const [notice,setNotice]=useState('Изменения применяются сразу и сохраняются на этом ПК.');
  function update(patch:Partial<Appearance>) {try{saveAppearance({...value,...patch});setNotice('Оформление сохранено');}catch{setNotice('Не удалось сохранить оформление');}}
  return <section className="settings-section appearance-settings"><div className="section-intro"><span className="eyebrow">ОФОРМЛЕНИЕ</span><h3>Ваше рабочее пространство</h3><p className="settings-help">Три книжные темы Лешего. Оформление применяется сразу; редактор кода остаётся без фоновых иллюстраций.</p></div>
    <label>Тема<select aria-label="Тема интерфейса" value={value.theme} onChange={event=>update({theme:event.target.value as Appearance['theme']})}>{leshyThemes.map(theme=><option key={theme.id} value={theme.id}>{theme.label}</option>)}</select></label>

    <label>Плотность<select aria-label="Плотность интерфейса" value={value.density} onChange={event=>update({density:event.target.value as Appearance['density']})}><option value="comfortable">Свободная</option><option value="compact">Компактная</option></select></label>
    {([{key:'backgroundArt',label:'Иллюстрации на приветственном экране'},{key:'sidebar',label:'Боковая панель и история'},{key:'output',label:'Журнал событий в IDE'},{key:'statusbar',label:'Нижняя строка состояния'}] as const).map(item=><label className="appearance-toggle" key={item.key}><input type="checkbox" aria-label={item.label} checked={value[item.key]} onChange={event=>update({[item.key]:event.target.checked})}/>{item.label}</label>)}
    <LayoutPresets/><button type="button" className="secondary-button" onClick={()=>update(defaults)}>Вернуть стандартное оформление</button><p role="status" className="settings-help">{notice}</p>
  </section>;
}
