import {Check} from 'lucide-react';
import {ForestSpot} from '../design/ForestSpot';
import {useAppearance,saveAppearance} from '../AppearanceSettings';
import {leshyThemes} from '../design/themes';
import type {ModelConnection} from './sessionState';

export function ConnectionSettings({config,savedConfig,models,locked,onChange,onSave,onList}:{config:ModelConnection|null;savedConfig:ModelConnection|null;models:string[];locked:boolean;onChange:(value:ModelConnection)=>void;onSave:()=>void;onList:()=>void}){
 const appearance=useAppearance();
 return <section className="nw-page"><header className="nw-page-heading"><h1>Оформление и подключение</h1><ForestSpot kind="birch"/></header>
 <label>Тема приложения<select aria-label="Тема приложения" value={appearance.theme} onChange={e=>saveAppearance({...appearance,theme:e.target.value as typeof appearance.theme})}>{leshyThemes.map(t=><option key={t.id} value={t.id}>{t.label}</option>)}</select></label>
 <div className="nw-theme-options" role="group" aria-label="Образцы тем">{leshyThemes.map(t=><button key={t.id} aria-label={t.label} aria-pressed={appearance.theme===t.id} onClick={()=>saveAppearance({...appearance,theme:t.id})}><span className={'leshy-preview '+t.id}>{appearance.theme===t.id&&<Check size={14}/>}</span>{t.label}</button>)}</div>
 {JSON.stringify(config)!==JSON.stringify(savedConfig)&&<p className="nw-unsaved">Есть несохранённые изменения. Запросы используют сохранённое подключение.</p>}
 <p>Общие настройки ядра Лешего. Ключ не отображается и не сохраняется в панели.</p>
 {config&&<form onSubmit={e=>{e.preventDefault();onSave();}}><fieldset disabled={locked}>
 <label>Адрес API<input required value={config.base_url||''} onChange={e=>onChange({...config,base_url:e.target.value})}/></label>
 <label>Модель<input required list="nw-models" value={config.model||''} onChange={e=>onChange({...config,model:e.target.value})}/><datalist id="nw-models">{models.map(model=><option key={model} value={model}/>)}</datalist></label>
 <label>Ключ API<input type="password" autoComplete="off" placeholder="Оставьте пустым, чтобы сохранить текущий" value={config.api_key||''} onChange={e=>onChange({...config,api_key:e.target.value})}/></label>
 <label>Протокол<select value={config.api_protocol||'chat'} onChange={e=>onChange({...config,api_protocol:e.target.value as ModelConnection['api_protocol']})}><option value="chat">Chat Completions</option><option value="responses">Responses</option></select></label>
 <label>Вызовы инструментов<select value={config.tool_protocol||'native'} onChange={e=>onChange({...config,tool_protocol:e.target.value as ModelConnection['tool_protocol']})}><option value="native">Native</option><option value="json">JSON</option></select></label>
 <button type="button" disabled={locked} onClick={onList}>Получить список моделей</button><button type="button" disabled={locked||!savedConfig} onClick={()=>{if(savedConfig)onChange({...savedConfig});}}>Отменить изменения</button><button className="nw-primary" disabled={locked} type="submit">Сохранить подключение</button></fieldset></form>}
 <details className="nw-settings-help"><summary>План, правила и MCP</summary><p>План и результаты текущей задачи находятся в разделе «Работа». Подробный редактор плана пока недоступен в этой панели. Правила проекта хранятся в AGENTS.md. MCP, навыки и разрешённые возможности настраиваются в главном окне Лешего.</p></details>
 </section>;
}
