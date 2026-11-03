export type LolaAnimationState='idle'|'listening'|'thinking'|'working'|'speaking'|'success'|'error';
export type LolaDesktopSettings={enabled:boolean;mode:'desktop'|'top'|'tray';size:number;animate:boolean;clickThrough:boolean;position:{x:number;y:number}|null};
export type LolaDesktopFrame={state:LolaAnimationState;caption:string;reply:string;busy:boolean;recording:boolean;wake:boolean};
export type LolaDesktopAction={action:'ask'|'record'|'stop'|'settings'|'speak';text?:string};
export type LolaVoiceAction={id:number;action:'record'|'cancel'|'settings'|'speak'};
export const lolaDesktopDefaults:LolaDesktopSettings={enabled:false,mode:'top',size:260,animate:true,clickThrough:false,position:null};
export const lolaInitialFrame:LolaDesktopFrame={state:'idle',caption:'Лола рядом',reply:'',busy:false,recording:false,wake:false};
export function validateLolaSettings(value:unknown):LolaDesktopSettings {
  if(!value||typeof value!=='object')throw Error('Некорректные настройки Лолы');
  const v=value as Record<string,unknown>;
  if(typeof v.enabled!=='boolean'||typeof v.animate!=='boolean'||typeof v.clickThrough!=='boolean'||!['desktop','top','tray'].includes(String(v.mode))||!Number.isInteger(v.size)||Number(v.size)<180||Number(v.size)>360)throw Error('Выберите режим и размер Лолы от 180 до 360 пикселей');
  let position:LolaDesktopSettings['position']=null;
  if(v.position!==null&&v.position!==undefined){const p=v.position as Record<string,unknown>;if(!p||!Number.isFinite(p.x)||!Number.isFinite(p.y)||Math.abs(Number(p.x))>100000||Math.abs(Number(p.y))>100000)throw Error('Некорректная позиция Лолы');position={x:Math.round(Number(p.x)),y:Math.round(Number(p.y))};}
  return {enabled:v.enabled,mode:v.mode as LolaDesktopSettings['mode'],size:Number(v.size),animate:v.animate,clickThrough:v.clickThrough,position};
}
export function validateLolaFrame(value:unknown):LolaDesktopFrame {
  if(!value||typeof value!=='object')return {...lolaInitialFrame};
  const v=value as Record<string,unknown>;
  const state=['idle','listening','thinking','working','speaking','success','error'].includes(String(v.state))?v.state as LolaAnimationState:'idle';
  return {state,caption:typeof v.caption==='string'?v.caption.slice(0,160):'Лола рядом',reply:typeof v.reply==='string'?v.reply.slice(0,1600):'',busy:v.busy===true,recording:v.recording===true,wake:v.wake===true};
}
export function fitLolaBounds(settings:LolaDesktopSettings,area:{x:number;y:number;width:number;height:number}) {
  const width=Math.min(settings.size+64,area.width),height=Math.min(settings.size+240,area.height);
  const x=Math.max(area.x,Math.min(settings.position?.x??area.x+area.width-width-20,area.x+area.width-width));
  const y=Math.max(area.y,Math.min(settings.position?.y??area.y+area.height-height-16,area.y+area.height-height));
  return {x:Math.round(x),y:Math.round(y),width,height};
}
