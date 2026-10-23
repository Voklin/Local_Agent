import { useEffect, useRef, useState } from 'react';
import { MicrophoneRecorder } from './microphone';
import { CompanionSettings } from './CompanionSettings';
import { ChatText } from './ChatText';
import { Mic, Volume2, Sparkles } from 'lucide-react';

export type WorkspaceMode = 'chat' | 'ide' | 'voice';
// Provider contracts keep audio processing separate from the model and renderer.
export type VoiceSessionState = 'disconnected' | 'idle' | 'listening' | 'thinking' | 'speaking' | 'error';
export interface VoiceProfile {
  persona: string;
  transcriptionProvider: string | null;
  speechProvider: string | null;
  pushToTalk: boolean;
}

export function VoicePanel({ activation, onChat, onAsk, onCancel, busy, messages, conversationKey, completed }: {
  activation:{id:number;text:string;send:boolean}|null;conversationKey:string;completed:boolean;
  onChat:()=>void;onAsk:(text:string)=>void;onCancel:()=>void;busy:boolean;
  messages:{role:string;text:string;streaming?:boolean}[];
}) {
  const [status,setStatus]=useState<any>({state:'idle',voices:[],recognizers:[]});
  const [voice,setVoice]=useState('');
  const [rate,setRate]=useState(0);
  const [volume,setVolume]=useState(70);
  const [input,setInput]=useState('');
  const [autoSpeak,setAutoSpeak]=useState(false);
  const [notice,setNotice]=useState('');
  const [profile,setProfile]=useState<any>(null);
  const [recording,setRecording]=useState(false);
  const [transcribing,setTranscribing]=useState(false);
  const recorder=useRef<MicrophoneRecorder|null>(null);
  const conversation=useRef(conversationKey);
  useEffect(()=>{conversation.current=conversationKey;recorder.current?.dispose();recorder.current=null;setRecording(false);setTranscribing(false);setInput('');void window.lca.cancelTranscription();},[conversationKey]);
  const model=profile?.model||'';
  const handledActivation=useRef(0);
  useEffect(()=>{
    if(!activation||!profile||busy||handledActivation.current===activation.id)return;
    handledActivation.current=activation.id;setInput(activation.text);
    setNotice(activation.text?'Команда распознана':'Мия активирована — говорите команду');
    if(activation.send&&activation.text&&profile.model){onAsk(activation.text);setInput('');}
  },[activation,profile,busy]);
  useEffect(()=>{window.dispatchEvent(new CustomEvent('manual-microphone',{detail:recording||transcribing}));return()=>{window.dispatchEvent(new CustomEvent('manual-microphone',{detail:false}));};},[recording,transcribing]);
  useEffect(()=>{if(profile)void window.lca.refreshVoices().then(result=>{if(result.ok)setStatus(result);});},[profile?.tts_provider]);

  useEffect(()=>{void window.lca.getCompanionSettings().then(result=>{if(result.ok){setProfile(result);setVoice(result.voice);setRate(result.rate);setVolume(result.volume);setAutoSpeak(result.auto_speak);}});return()=>{recorder.current?.dispose();recorder.current=null;void window.lca.cancelTranscription();};},[]);
  async function record() {
    if(recording){await finishRecording();return;}
    const capture=new MicrophoneRecorder();recorder.current=capture;setNotice('');setRecording(true);
    try{await capture.start(()=>void finishRecording());if(recorder.current===capture)setRecording(true);}
    catch(error){capture.dispose();if(recorder.current===capture){recorder.current=null;setRecording(false);setNotice(String(error));}}
  }
  async function finishRecording() {
    const capture=recorder.current;if(!capture)return;const origin=conversation.current;recorder.current=null;setRecording(false);setTranscribing(true);
    try{const result=await window.lca.transcribe(capture.finish());if(!result.ok)throw Error(result.error);if(alive.current&&conversation.current===origin)setInput(result.text);}
    catch(error){if(alive.current&&conversation.current===origin)setNotice(String(error));}finally{if(alive.current&&conversation.current===origin)setTranscribing(false);}
  }
  async function saveVoice() {
    try{const result=await window.lca.configureCompanion({...profile,voice,rate,volume,auto_speak:autoSpeak});if(!result.ok)throw Error(result.error);setProfile(result);window.dispatchEvent(new Event('companion-profile'));setNotice('Голос сохранён');}
    catch(error){setNotice(String(error));}
  }
  const alive=useRef(true);
  const lastRead=useRef('');
  const replyEntry=messages.map((message,index)=>({message,index})).reverse().find(entry=>entry.message.role==='assistant'&&!entry.message.streaming);
  const reply=replyEntry?.message.text||'';
  const replyKey=conversationKey+':'+replyEntry?.index+':'+reply;
  const voiceActive=['loading','synthesizing','speaking','stopping'].includes(status.state);
  useEffect(()=>{
    alive.current=true;
    async function refresh() {
      try{const result=await window.lca.voiceStatus();if(alive.current&&result.ok)setStatus(result);}
      catch(error){if(alive.current)setNotice(String(error));}
    }
    let initializing=true;
    const initialTimer=setTimeout(async()=>{
      try {
        let current=await window.lca.voiceStatus();
        for(let attempt=0;initializing&&['stopping','loading'].includes(current.state)&&attempt<30;attempt++) {
          await new Promise(resolve=>setTimeout(resolve,100));current=await window.lca.voiceStatus();
        }
        if(!initializing)return;
        if(!current.voices?.length) {
          const result=await window.lca.refreshVoices();if(!result.ok)throw new Error(result.error);
        }
        await refresh();
      }catch(error){if(initializing)setNotice(String(error));}
    },150);
    const timer=setInterval(()=>void refresh(),500);
    return ()=>{initializing=false;alive.current=false;clearTimeout(initialTimer);clearInterval(timer);void window.lca.stopVoice().catch(()=>{});};
  },[]);
  useEffect(()=>{
    if(!status.voices.some((item:any)=>item.id===voice))setVoice(status.voices.find((item:any)=>item.culture==='ru-RU')?.id||status.voices[0]?.id||'');
  },[status.voices,voice]);
  useEffect(()=>{lastRead.current=replyKey;},[conversationKey]);
  useEffect(()=>{
    if(busy||!reply||lastRead.current===replyKey)return;
    if(autoSpeak&&!completed)return;
    if(autoSpeak&&(!voice||voiceActive))return;
    lastRead.current=replyKey;
    if(autoSpeak)void speak(reply);
  },[replyKey,busy,autoSpeak,voice,voiceActive,completed]);
  async function speak(text:string) {
    setNotice('');
    try{const result=await window.lca.speak({text:text.slice(0,profile?.tts_provider==='qwen3'?1200:6000),voice,rate,volume});if(!result.ok)throw new Error(result.error);setStatus(result);if(text.length>(profile?.tts_provider==='qwen3'?1200:6000))setNotice('Озвучивается начало длинного ответа.');}
    catch(error){setNotice(String(error));}
  }
  async function stop() {
    lastRead.current=replyKey;
    try{const result=await window.lca.stopVoice();if(result.ok)setStatus(result);else setNotice(result.error);}
    catch(error){setNotice(String(error));}
  }
  function send() {
    if(!input.trim()||busy||recording||transcribing||!model)return;
    onAsk(input.trim());setInput('');
  }
  const state:VoiceSessionState=recording?'listening':(busy||transcribing)?'thinking':status.state==='speaking'?'speaking':status.state==='error'?'error':voice?'idle':'disconnected';
  return <main className={`voice-panel voice-${state}`}>

    <div className="voice-intro"><span className="eyebrow">LOCALAGENT / COMPANION</span><h1>Мия · ваш ассистент</h1><p>Локальная модель, нейроозвучка и активация голосом. Собственная история, отдельная модель и настраиваемый характер. Сложные задачи можно передать основной модели.</p><span className="context-chip">Модель Мии: {model||'не выбрана'}</span></div>
    <div className="companion-stage">
      <div className="companion-orbit"/>
      <svg className="maid-concept" viewBox="0 0 240 290" role="img" aria-label="Эскиз аниме-горничной для будущего ассистента">
        <path fill="#555875" d="M63 120Q33 28 120 24q87 4 57 96l18 107H45z"/>
        <path fill="#eedbe1" d="M72 83q0-45 48-45t48 45v26q-3 51-48 53-45-2-48-53z"/>
        <path fill="#656583" d="M62 88q-2-65 59-61 64 0 57 72l-32-39-11 33-22-35-18 39-9-23z"/>
        <path fill="#ece6ef" d="m67 45 9-18 18 1 13-15 14 8 17-8 13 15 17 1 8 18-18-1-17-10-21 2-24-1-16 10z"/>
        <ellipse cx="99" cy="108" rx="7" ry="10" fill="#79659a"/><ellipse cx="144" cy="108" rx="7" ry="10" fill="#79659a"/>
        <circle cx="101" cy="104" r="2.5" fill="white"/><circle cx="146" cy="104" r="2.5" fill="white"/>
        <path className="maid-mouth" d="M113 133q8 6 16 0" fill="none" stroke="#b38697" strokeWidth="3" strokeLinecap="round"/>
        <path fill="#34384e" d="m91 155-35 22-24 88h176l-24-88-35-22-29 18z"/>
        <path fill="#f0eaf0" d="m88 161 32 17 31-17 14 32-13 72H88l-13-72z"/>
        <path fill="#b99ab9" d="m120 180-20-9v21l20-7 20 7v-21z"/>
        <path d="M85 235h70M96 204v47m48-47v47" stroke="#d2c6d6" fill="none" strokeWidth="2"/>
      </svg>
      <span className="concept-caption">Образ персонажа · анимация состояния</span>
    </div>
    <div className="voice-state" role="status"><span/>{recording?'Слушаю…':transcribing?'Распознаю речь…':busy?'Мия думает…':status.state==='speaking'?'Озвучка…':status.state==='synthesizing'?'Создаю голос Мии…':status.state==='loading'?'Загрузка голосов…':status.state==='stopping'?'Остановка озвучки…':voice?'Готова к разговору':'Голос не подключён'}</div>
    <div className="voice-controls">
      <label>Голос<select aria-label="Голос ассистента" value={voice} disabled={voiceActive} onChange={event=>setVoice(event.target.value)}>{status.voices.map((item:any)=><option key={item.id} value={item.id}>{item.id} · {item.culture}</option>)}</select></label>
      <label>Темп<input aria-label="Темп речи" type="range" min={-5} max={5} value={rate} onChange={event=>setRate(Number(event.target.value))}/></label>
      <label>Громкость<input aria-label="Громкость речи" type="range" min={0} max={100} value={volume} onChange={event=>setVolume(Number(event.target.value))}/></label>
      <label className="auto-speak"><input type="checkbox" checked={autoSpeak} onChange={event=>{lastRead.current=replyKey;setAutoSpeak(event.target.checked);}}/>Озвучивать новые ответы автоматически</label>
      <div className="voice-buttons"><button className="secondary-button speak-reply" disabled={!voice||voiceActive||busy||!(reply||input.trim())} onClick={()=>void speak(reply||input.trim())}><Volume2 size={15}/>Озвучить {reply?'ответ':'текст'}</button><button className="secondary-button stop-speech" disabled={!voiceActive} onClick={()=>void stop()}>Stop · голос</button><button className="secondary-button" disabled={voiceActive} onClick={()=>void window.lca.refreshVoices()}>Обновить голоса</button><button className="secondary-button microphone-record" disabled={!recording&&(busy||transcribing||!profile||voiceActive)} onClick={()=>void record()}><Mic size={15}/>{recording?'Завершить запись':'Микрофон · запись'}</button>{transcribing&&<button className="secondary-button" onClick={()=>void window.lca.cancelTranscription()}>Отменить распознавание</button>}<button className="secondary-button" disabled={busy||!profile} onClick={()=>void saveVoice()}>Сохранить голос</button></div>
      <p className="voice-stt-note">{recording?'Идёт запись · до 60 секунд':transcribing?'Распознавание…':'Микрофон включается по нажатию. Распознанный текст появится в поле: проверьте его перед отправкой.'}</p>
      {profile&&<CompanionSettings profile={{...profile,voice,rate,volume,auto_speak:autoSpeak}} busy={busy||recording||transcribing||voiceActive} onSaved={setProfile}/>}
      <button className="secondary-button" disabled={busy} onClick={onChat}><Sparkles size={14}/>Открыть Chat</button>
      {(notice||status.error)&&<p className="voice-error" role="alert">{notice||status.error}</p>}
    </div>
    <section className="voice-conversation" aria-label="Разговор с ассистентом">{messages.slice(-8).map((message,index)=><div className={`voice-message ${message.role}`} key={index}><b>{message.role==='user'?'Вы':message.role==='assistant'?'Мия':'Состояние'}</b><ChatText text={message.text}/>{message.streaming&&<span>▍</span>}</div>)}</section>
    <form className="voice-composer" onSubmit={event=>{event.preventDefault();send();}}><textarea aria-label="Сообщение ассистенту" maxLength={50000} disabled={busy||recording||transcribing} value={input} onChange={event=>setInput(event.target.value)} placeholder={model?'Напишите Мии…':'Выберите модель в настройках'}/>{busy?<button type="button" className="primary-button" onClick={onCancel}>Остановить ответ</button>:<button className="primary-button" disabled={!model||!input.trim()||recording||transcribing} type="submit">Отправить ассистенту</button>}</form>
  </main>;
}
