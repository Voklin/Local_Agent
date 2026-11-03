import atlas from './assets/lola-chibi-atlas-v2.png';
import geometry from './assets/lola-chibi-atlas-v2.json';

export type LolaState='idle'|'listening'|'thinking'|'working'|'speaking'|'success'|'error';
const labels:Record<LolaState,string>={idle:'Рядом с вами',listening:'Внимательно слушаю',thinking:'Обдумываю ответ',working:'Выполняю задачу',speaking:'Говорю',success:'Готово!',error:'Нужна ваша помощь'};
const rows:Record<LolaState,number>={idle:0,listening:1,thinking:2,working:3,speaking:4,success:5,error:6};

export function LolaAvatar({state,reducedMotion=false}:{state:LolaState;reducedMotion?:boolean}) {
  return <div className={`miya-scene miya-${state}${reducedMotion?' miya-still':''}`}>
    <div className="miya-halo"/>
    <div className="miya-character" role="img" aria-label={`Лола: ${labels[state]}`}>
      <svg className="lola-sprite" viewBox="0 0 260 260" preserveAspectRatio="xMidYMid meet" aria-hidden="true">
        {geometry.frames.filter(frame=>frame.row===rows[state]).map((frame,index)=><svg key={index} className={`lola-frame lola-frame-${index}`} data-frame={index}
          x={(260-frame.width)/2} y={247-frame.height} width={frame.width} height={frame.height}
          viewBox={`${frame.x} ${frame.y} ${frame.width} ${frame.height}`} overflow="hidden"
          style={{animationDelay:`calc(var(--lola-cycle) * ${-((4-index)%4)/4})`}}>
          <image href={atlas} width={geometry.width} height={geometry.height}/>
        </svg>)}
      </svg>
    </div>
    <span className="miya-caption">{labels[state]}</span>
    {['listening','speaking'].includes(state)&&<div className="miya-wave" aria-hidden="true">{[0,1,2,3,4].map(index=><i key={index} style={{animationDelay:`${index*.12}s`}}/>)}</div>}
  </div>;
}
