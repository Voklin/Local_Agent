import {Check,Code2,Pencil,Play} from 'lucide-react';
import {BrandMark} from './BrandMark';
import {saveAppearance,useAppearance} from './AppearanceSettings';
import {leshyThemes} from './design/themes';
import {OrnamentDivider} from './design/Ornaments';
export function Welcome({mode,onPrompt,onStart}:{mode:string;onPrompt:(text:string)=>void;onStart:()=>void}){
 const appearance=useAppearance();
 return <div className="neutral-welcome leshy-welcome"><div className="leshy-edge left" aria-hidden="true"/><div className="leshy-edge right" aria-hidden="true"/><BrandMark size={76}/><h1>ЛЕШИЙ</h1><div className="leshy-wordmark">LESHY</div><p>{mode==='ide'?'Хранитель вашего проекта. Начнём с его изучения.':'AI-агент для разработки, исследования и автоматизации.'}<br/>Опишите задачу — и Леший возьмёт её в работу.</p><div className="studio-welcome-actions"><button onClick={()=>onPrompt('Помоги составить план: ')}><Pencil size={16}/>Составить план</button><button onClick={()=>onPrompt(mode==='ide'?'Изучи структуру проекта и объясни, как он устроен.':'Помоги разобраться: ')}><Code2 size={16}/>Разобраться в коде</button>{mode!=='ide'&&<button onClick={onStart}><Play size={16}/>Запустить агент</button>}</div><OrnamentDivider/><div className="leshy-theme-caption">ВЫБРАТЬ ТЕМУ</div><div className="leshy-theme-picker" role="group" aria-label="Оформление">{leshyThemes.map(theme=><button key={theme.id} aria-pressed={appearance.theme===theme.id} onClick={()=>saveAppearance({...appearance,theme:theme.id})}><span className={'leshy-preview '+theme.id}>{appearance.theme===theme.id&&<span className="leshy-theme-check" aria-hidden="true"><Check size={13}/></span>}</span><span>{theme.label}</span></button>)}</div></div>;
}
