import {createContext,useContext,useEffect,useRef,useState,type ReactNode} from 'react';
import {Check,ChevronRight,LoaderCircle,Settings2,RotateCw,SquareTerminal,XCircle} from 'lucide-react';
import type {ModelConfig} from './ModelSettings';
import type {TaskSnapshot} from '../shared/taskTypes';

type Panel='sidebar'|'agent'|'context'|'settings';
type Layout={sidebar:number;agent:number;context:number;settings:number;agentVisible:boolean;contextVisible:boolean;contextSide:'left'|'right'};
const defaults:Layout={sidebar:234,agent:400,context:258,settings:230,agentVisible:true,contextVisible:true,contextSide:'right'};
const limits:Record<Panel,[number,number]>={sidebar:[180,420],agent:[300,720],context:[200,500],settings:[180,340]};
const key='neutral.studio.layout.v1';
function validated(raw:Partial<Layout>):Layout{const result={...defaults};for(const name of Object.keys(limits) as Panel[]){const value=raw[name];if(typeof value==='number'&&Number.isFinite(value))result[name]=Math.max(limits[name][0],Math.min(limits[name][1],value));}for(const name of ['agentVisible','contextVisible'] as const)if(typeof raw[name]==='boolean')result[name]=raw[name];if(raw.contextSide==='left')result.contextSide='left';return result;}
function readLayout(){try{return validated(JSON.parse(localStorage.getItem(key)||'{}'));}catch{return {...defaults};}}
const LayoutContext=createContext<{layout:Layout;update:(value:Partial<Layout>)=>void;viewport:number}|null>(null);
export function StudioLayoutProvider({children}:{children:ReactNode}){
 const [layout,setLayout]=useState(readLayout),[viewport,setViewport]=useState(innerWidth);
 useEffect(()=>{const resize=()=>setViewport(innerWidth);window.addEventListener('resize',resize);return()=>window.removeEventListener('resize',resize);},[]);
 const update=(value:Partial<Layout>)=>setLayout(current=>{const next=validated({...current,...value});try{localStorage.setItem(key,JSON.stringify(next));}catch{/* Keep usable layout when storage is unavailable. */}return next;});
 return <LayoutContext.Provider value={{layout,update,viewport}}>{children}</LayoutContext.Provider>;
}
export function useStudioLayout(){const value=useContext(LayoutContext);if(!value)throw Error('StudioLayoutProvider is missing');return value;}
export function ResizeRail({name,edge='right'}:{name:Panel;edge?:'left'|'right'}){
 const {layout,update}=useStudioLayout(),drag=useRef<{x:number;width:number}|null>(null);
 const change=(width:number)=>update({[name]:Math.max(limits[name][0],Math.min(limits[name][1],width))});
 return <div className={'studio-resize '+edge} role="separator" aria-label={'Ширина '+({sidebar:'боковой панели',agent:'агента',context:'контекста',settings:'разделов настроек'}[name])} aria-orientation="vertical" aria-valuemin={limits[name][0]} aria-valuemax={limits[name][1]} aria-valuenow={layout[name]} tabIndex={0} title="Перетащите границу · стрелки · двойной щелчок для сброса"
  onDoubleClick={()=>change(defaults[name])} onKeyDown={e=>{if(!['ArrowLeft','ArrowRight','Home','End'].includes(e.key))return;e.preventDefault();e.stopPropagation();change(e.key==='Home'?limits[name][0]:e.key==='End'?limits[name][1]:layout[name]+(e.key==='ArrowRight'?16:-16)*(edge==='left'?-1:1));}}
  onPointerDown={e=>{if(e.button!==0)return;e.preventDefault();e.currentTarget.focus();const panel=e.currentTarget.parentElement;drag.current={x:e.clientX,width:panel?.getBoundingClientRect().width||layout[name]};e.currentTarget.setPointerCapture(e.pointerId);}}
  onPointerMove={e=>{if(drag.current)change(drag.current.width+(e.clientX-drag.current.x)*(edge==='left'?-1:1));}} onPointerUp={()=>{drag.current=null;}} onPointerCancel={()=>{drag.current=null;}} onLostPointerCapture={()=>{drag.current=null;}}/>;
}
export function LayoutPresets(){
 const {layout,update}=useStudioLayout();const [name,setName]=useState('Рабочая'),[notice,setNotice]=useState(''),[presets,setPresets]=useState<Record<string,Layout>>(()=>{try{const raw=JSON.parse(localStorage.getItem(key+'.presets')||'{}');return Object.fromEntries(Object.entries(raw).filter(([n])=>n.length<=80).map(([n,v])=>[n,validated(v as Layout)]));}catch{return {};}});
 function save(){if(!name.trim())return;const next={...presets,[name.trim()]:layout};try{localStorage.setItem(key+'.presets',JSON.stringify(next));setPresets(next);setNotice('Раскладка сохранена');}catch{setNotice('Не удалось сохранить раскладку');}}
 return <div className="studio-layout-presets"><h3>Панели и раскладки</h3><label>Название<input maxLength={80} value={name} onChange={e=>setName(e.target.value)}/></label><button type="button" className="secondary-button" onClick={save}>Сохранить раскладку</button>{Object.keys(presets).length>0&&<label>Сохранённые раскладки<select value="" onChange={e=>{if(presets[e.target.value]){update(presets[e.target.value]);setName(e.target.value);setNotice('Раскладка восстановлена');}}}><option value="" disabled>Выбрать раскладку…</option>{Object.keys(presets).map(n=><option key={n}>{n}</option>)}</select></label>}<label>Контекст Chat<select value={layout.contextSide} onChange={e=>update({contextSide:e.target.value as 'left'|'right'})}><option value="right">Справа</option><option value="left">Слева</option></select></label><button type="button" className="secondary-button" onClick={()=>update(defaults)}>Сбросить расположение панелей</button><p role="status">{notice}</p></div>;
}
export function ComposerModel({config,busy,onSelected,onSettings}:{config:ModelConfig;busy:boolean;onSelected:(id:string)=>void;onSettings:()=>void}){
 const [models,setModels]=useState<string[]>([]),[notice,setNotice]=useState(''),[loading,setLoading]=useState(false),[applying,setApplying]=useState(false);
 const generation=useRef(0),latest=useRef(config);latest.current=config;
 useEffect(()=>{generation.current++;setModels([]);setNotice('');setLoading(false);},[config.base_url,config.api_protocol,config.api_key]);
 async function refresh(){if(loading||busy||applying)return;const revision=++generation.current;setLoading(true);try{const result=await window.lca.listModels(latest.current);if(revision!==generation.current)return;if(!result.ok)throw Error(result.error);setModels(result.models||[]);setNotice(result.models?.length?'':'Список пуст. Укажите ID модели в настройках.');}catch(error){if(revision===generation.current)setNotice(String(error));}finally{if(revision===generation.current)setLoading(false);}}
 async function select(value:string){if(value==='__settings'){onSettings();return;}if(busy||applying)return;setApplying(true);try{const result=await window.lca.configureModel({...latest.current,model:value});if(!result.ok)throw Error(result.error);onSelected(value);setNotice('');}catch(error){setNotice(String(error));}finally{setApplying(false);}}
 return <div className="studio-model-picker"><span>Модель</span><select aria-label="Выбрать модель" aria-busy={loading||applying} disabled={busy||applying} value={config.model||''} onFocus={()=>void refresh()} onChange={e=>void select(e.target.value)}><option value="" disabled>{loading?'Получаю список…':'Выбрать модель'}</option>{[...new Set([config.model,...models].filter(Boolean))].map(id=><option key={id}>{id}</option>)}<option value="__settings">Настроить подключение…</option></select><button type="button" className="icon-button studio-model-refresh" title="Обновить список моделей" aria-label="Обновить список моделей" disabled={busy||loading||applying} onClick={()=>void refresh()}>{loading?<LoaderCircle size={12}/>:<RotateCw size={12}/>}</button><button type="button" className="icon-button" title="Настройки модели" aria-label="Настройки модели" onClick={onSettings}><Settings2 size={13}/></button>{notice&&<div className="studio-model-notice" role="status">{notice}<button type="button" onClick={()=>setNotice('')} aria-label="Скрыть сообщение модели">×</button></div>}</div>;
}
const toolNames:Record<string,string>={read_file:'Чтение файла',read_range:'Чтение строк',list_files:'Обзор файлов',search_text:'Поиск в проекте',glob_files:'Поиск файлов',write_file:'Запись файла',patch_file:'Точечная правка',run_project_command:'Команда проекта',create_directory:'Создание каталога',delete_file:'Удаление файла',rename_file:'Перемещение файла',delegate_readonly:'Дочернее исследование'};
const statuses:Record<string,string>={running:'Выполняется',applying:'Применяется',awaiting_approval:'Нужно решение',succeeded:'Готово',failed:'Ошибка',rejected:'Отклонено',cancelled:'Остановлено',unknown:'Итог неизвестен',confirmed:'Подтверждено вами',not_executed:'Не выполнялось',interrupted:'Прервано'};
export function InlineTools({task}:{task:TaskSnapshot|null}){
 if(!task?.tool_activity?.length)return null;
 return <section className="studio-activity" aria-label="Действия агента"><header><span>ХОД РАБОТЫ</span><span>{task.tool_activity.length} действий</span></header><div className="studio-activity-list">{task.tool_activity.map(item=><details key={item.id} data-status={item.status}><summary>{['running','applying'].includes(item.status)?<LoaderCircle className="spin" size={14}/>:item.status==='succeeded'||item.status==='confirmed'?<Check size={14}/>:item.status==='failed'?<XCircle size={14}/>:<SquareTerminal size={14}/>}<span>{toolNames[item.tool]||item.tool}<small>{item.path||statuses[item.status]||item.status}</small></span><ChevronRight size={14}/></summary><div><b>{statuses[item.status]||item.status}</b><p>{item.summary}</p>{item.path&&<code>{item.path}</code>}{item.status==='unknown'&&<p>Проверьте фактический результат в подробностях задачи перед продолжением.</p>}</div></details>)}</div>{!!task.activity_omitted&&<small>Более ранних действий: {task.activity_omitted}. Полный журнал сохранён в истории запуска.</small>}</section>;
}
/** Keep keyboard focus inside the topmost existing modal, including native dialogs. */
export function DialogFocus(){useEffect(()=>{
 const top=()=>[...document.querySelectorAll<HTMLElement>('[aria-modal="true"],dialog[open]')].filter(n=>n.getClientRects().length>0).at(-1);
 let previous:HTMLElement|null=null,last:HTMLElement|undefined;
 const check=()=>{const modal=top();if(modal===last)return;if(!modal){previous?.focus();last=undefined;return;}previous=document.activeElement as HTMLElement;last=modal;if(!modal.contains(document.activeElement))modal.querySelector<HTMLElement>('input,textarea,button,select,[tabindex="0"]')?.focus();};
 const observer=new MutationObserver(check);observer.observe(document.body,{childList:true,subtree:true});
 const keys=(e:KeyboardEvent)=>{const modal=top();if(!modal||e.key!=='Tab')return;const nodes=[...modal.querySelectorAll<HTMLElement>('button,input,textarea,select,[tabindex="0"]')].filter(n=>n.getClientRects().length&&!n.hasAttribute('disabled'));if(!nodes.length)return;const i=nodes.indexOf(document.activeElement as HTMLElement);if(e.shiftKey&&i<=0){e.preventDefault();nodes.at(-1)?.focus();}else if(!e.shiftKey&&(i<0||i===nodes.length-1)){e.preventDefault();nodes[0].focus();}};
 document.addEventListener('keydown',keys,true);return()=>{observer.disconnect();document.removeEventListener('keydown',keys,true);};
},[]);return null;}
