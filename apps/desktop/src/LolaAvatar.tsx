import atlas from './assets/miya-states.png';

export type LolaState='idle'|'listening'|'thinking'|'working'|'speaking'|'success'|'error';
const labels:Record<LolaState,string>={idle:'Рядом с вами',listening:'Внимательно слушаю',thinking:'Обдумываю ответ',working:'Выполняю задачу',speaking:'Говорю',success:'Готово!',error:'Нужна ваша помощь'};
const positions:Record<LolaState,string>={idle:'0% 0%',listening:'33.333333% 0%',thinking:'66.666667% 0%',working:'100% 0%',speaking:'0% 100%',success:'66.666667% 100%',error:'100% 100%'};

export function LolaAvatar({state,reducedMotion=false}:{state:LolaState;reducedMotion?:boolean}) {
  return <div className={`miya-scene miya-${state}${reducedMotion?' miya-still':''}`}>
    <div className="miya-halo"/>
    <div className="miya-character" role="img" aria-label={`Лола: ${labels[state]}`} style={{backgroundImage:`url(${atlas})`,backgroundPosition:positions[state]}}/>
    <span className="miya-caption">{labels[state]}</span>
    {['listening','speaking'].includes(state)&&<div className="miya-wave" aria-hidden="true">{[0,1,2,3,4].map(index=><i key={index} style={{animationDelay:`${index*.12}s`}}/>)}</div>}
  </div>;
}
