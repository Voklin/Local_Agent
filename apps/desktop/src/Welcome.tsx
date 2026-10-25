import { Code2, Compass, Globe } from 'lucide-react';
import { BrandMark } from './BrandMark';

export function Welcome({mode,onPrompt,onIde}:{mode:string;onPrompt:(text:string)=>void;onIde:()=>void}) {
  return <div className="neutral-welcome"><div className="welcome-symbol"><BrandMark size={40}/></div><span className="eyebrow">ЯСНОСТЬ В МЫСЛЯХ. СВОБОДА В ДЕЛАХ.</span><h1>{mode==='ide'?'От замысла к работающему коду.':<>Ваши идеи.<br/><em>Новые возможности.</em></>}</h1><p>{mode==='ide'?'Исследуйте проект, обсуждайте решения и просматривайте каждое изменение.':'Обсудим идею, разберёмся в сложном или создадим что-то вместе.'}</p><div className="welcome-cards"><button onClick={()=>onPrompt('Помоги составить план: ')}><Compass size={21}/><b>От идеи к плану</b><span>Разложим задачу по шагам</span></button><button onClick={()=>onPrompt('Помоги разобраться: ')}><Globe size={21}/><b>Найти и разобраться</b><span>Понятные ответы и источники</span></button><button onClick={onIde}><Code2 size={21}/><b>Создать в IDE</b><span>Код, файлы и ваш проект</span></button></div></div>;
}
