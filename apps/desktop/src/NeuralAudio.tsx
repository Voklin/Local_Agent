import { useEffect } from 'react';

export function NeuralAudio() {
  useEffect(()=>{
    let audio:HTMLAudioElement|null=null;
    let sequence=0;
    const unsubscribe=window.lca.onEvent(event=>{
      if(event.event==='voice_audio_stop') {sequence++;audio?.pause();audio=null;return;}
      if(event.event!=='voice_audio')return;
      audio?.pause();sequence=event.sequence;
      const current=sequence;
      const player=new Audio('data:audio/wav;base64,'+event.audio);audio=player;
      player.volume=event.volume;player.playbackRate=event.rate;
      player.onended=()=>{if(current===sequence)void window.lca.voicePlayback({sequence:current});};
      player.onerror=()=>{if(current===sequence)void window.lca.voicePlayback({sequence:current,error:true});};
      void player.play().catch(()=>{if(current===sequence)void window.lca.voicePlayback({sequence:current,error:true});});
    });
    return()=>{unsubscribe();sequence++;audio?.pause();void window.lca.stopVoice();};
  },[]);
  return null;
}
