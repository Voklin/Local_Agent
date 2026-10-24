import { useEffect, useRef, useState } from 'react';
import { MicrophoneRecorder } from './microphone';
import { wakeCommand } from './wakePhrase';

export function WakeListener({busy,onWake}:{busy:boolean;onWake:(text:string,send:boolean)=>Promise<void>}) {
  const [armed,setArmed]=useState(false);
  const [profile,setProfile]=useState<any>(null);
  const [notice,setNotice]=useState('');
  const [manual,setManual]=useState(false);
  const [speaking,setSpeaking]=useState(false);
  const action=useRef(onWake);action.current=onWake;
  useEffect(()=>{void window.lca.wakeListening(armed);return()=>{void window.lca.wakeListening(false);};},[armed]);
  useEffect(()=>{
    let alive=true;
    const refresh=()=>void window.lca.getCompanionSettings().then(p=>{if(alive&&p.ok)setProfile(p);});
    const capture=(event:Event)=>setManual((event as CustomEvent).detail===true);
    refresh();window.addEventListener('companion-profile',refresh);window.addEventListener('manual-microphone',capture);
    const timer=setInterval(()=>void window.lca.voiceStatus().then(s=>{if(alive)setSpeaking(['loading','synthesizing','speaking','stopping'].includes(s.state));}),500);
    return()=>{alive=false;clearInterval(timer);window.removeEventListener('companion-profile',refresh);window.removeEventListener('manual-microphone',capture);};
  },[]);
  useEffect(()=>{
    if(!armed||!profile||busy||manual||speaking)return;
    window.dispatchEvent(new CustomEvent('miya-listening',{detail:true}));
    let alive=true;let capture:MicrophoneRecorder|null=null;let inRequest=false;let pending=false;
    let previous='';let commandUntil=0;
    async function cycle() {
      if(!alive)return;
      try {
        capture=new MicrophoneRecorder();
        await new Promise<void>((resolve,reject)=>{void capture!.start(resolve,12,.8).catch(reject);});
        if(!alive)return;
        const voiced=capture.hasSpeech();const audio=capture.finish();capture=null;
        if(!voiced){previous='';return;}
        inRequest=true;setNotice('Проверяю фразу…');
        const result=await window.lca.transcribe(audio);inRequest=false;
        if(!alive)return;
        if(!result.ok)throw Error(result.error);
        const text=String(result.text||'').trim();
        if(commandUntil>Date.now()&&text){commandUntil=0;await action.current(text,profile.wake_auto_send);return;}
        const command=wakeCommand(text,profile.wake_phrase)??wakeCommand(previous+' '+text,profile.wake_phrase);
        previous=text.split(/\s+/).slice(-8).join(' ');
        if(command!==null){
          previous='';commandUntil=command?0:Date.now()+15000;
          setNotice(command?'Команда услышана':'Лола активирована — говорите команду');
          await action.current(command,profile.wake_auto_send);
        }
      }catch(error){if(alive){setNotice(String(error));setArmed(false);}}
      finally{if(alive&&!pending){pending=true;setTimeout(()=>{pending=false;void cycle();},50);}}
    }
    setNotice(`Слушаю: «${profile.wake_phrase}»`);void cycle();
    return()=>{window.dispatchEvent(new CustomEvent('miya-listening',{detail:false}));alive=false;capture?.dispose();if(inRequest)void window.lca.cancelTranscription();};
  },[armed,profile,busy,manual,speaking]);
  return <div className="wake-control"><button className={armed?'secondary-button selected':'secondary-button'} disabled={!profile} onClick={()=>{setNotice('');setArmed(!armed);}}>{armed?'Выключить прослушивание':'Активация голосом'}</button><span role="status" title={notice}>{armed?(busy||manual||speaking?'Прослушивание на паузе':notice):notice||'Микрофон выключен'}</span></div>;
}
