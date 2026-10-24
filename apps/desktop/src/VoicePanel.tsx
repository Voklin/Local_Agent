import { useEffect, useRef, useState } from 'react';
import { MicrophoneRecorder } from './microphone';
import { CompanionSettings } from './CompanionSettings';
import { ChatText } from './ChatText';
import { Mic, Volume2, Sparkles, Settings, X } from 'lucide-react';
import { LolaAvatar, type LolaState } from './LolaAvatar';
import type { TaskSnapshot } from './TaskProgress';

export type WorkspaceMode = 'chat' | 'ide' | 'voice';
// Provider contracts keep audio processing separate from the model and renderer.
export type VoiceSessionState = 'disconnected' | 'idle' | 'listening' | 'thinking' | 'speaking' | 'error';

export function VoicePanel({ activation, onChat, onAsk, onCancel, busy, messages, conversationKey, completed, task }: {
  activation:{id:number;text:string;send:boolean}|null;conversationKey:string;completed:boolean;
  onChat:()=>void;onAsk:(text:string)=>void;onCancel:()=>void;busy:boolean;
  messages:{role:string;text:string;streaming?:boolean}[];
  task?:TaskSnapshot|null;
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
  const [runtime,setRuntime]=useState<any>({running:false});
  const [runtimeBusy,setRuntimeBusy]=useState(false);
  const [celebrating,setCelebrating]=useState(false);
  const [animate,setAnimate]=useState(()=>localStorage.getItem('miya-animation')!=='off');
  const [wakeListening,setWakeListening]=useState(false);
  const settingsDialog=useRef<HTMLDialogElement>(null);
  const settingsButton=useRef<HTMLButtonElement>(null);
  const [autoEnd,setAutoEnd]=useState(()=>localStorage.getItem('miya-auto-end')!=='off');
  const [autoSend,setAutoSend]=useState(()=>localStorage.getItem('miya-auto-send')==='on');
  const requestGeneration=useRef(0);
  useEffect(()=>{const listener=(event:Event)=>setWakeListening((event as CustomEvent).detail===true);window.addEventListener('miya-listening',listener);return()=>window.removeEventListener('miya-listening',listener);},[]);
  useEffect(()=>{setCelebrating(completed);if(!completed)return;const timer=setTimeout(()=>setCelebrating(false),4000);return()=>clearTimeout(timer);},[completed]);
  useEffect(()=>{
    let active=true;
    if(profile?.tts_provider==='piper')void window.lca.speechRuntime('start').then(result=>{if(active){setRuntime(result);if(!result.ok)setNotice(result.error);}});
    else if(profile)void window.lca.speechRuntime('stop');
    const timer=setInterval(()=>{if(profile?.tts_provider==='piper')void window.lca.speechRuntime('status').then(result=>{if(active)setRuntime(result);});},3000);
    return()=>{active=false;clearInterval(timer);};
  },[profile?.tts_provider]);
  async function selectProvider(provider:string) {
    if(!profile)return;setNotice('');
    try {
      await window.lca.stopVoice();
      const result=await window.lca.configureCompanion({...profile,voice,rate,volume,auto_speak:autoSpeak,tts_provider:provider});
      if(!result.ok)throw Error(result.error);setProfile(result);window.dispatchEvent(new Event('companion-profile'));
    }catch(error){setNotice(String(error));}
  }
  async function startSerena() {
    setRuntimeBusy(true);setNotice('');
    try{const result=await window.lca.speechRuntime('start');setRuntime(result);if(!result.ok)throw Error(result.error);}
    catch(error){setNotice(String(error));}finally{setRuntimeBusy(false);}
  }
  const recorder=useRef<MicrophoneRecorder|null>(null);
  const conversation=useRef(conversationKey);
  useEffect(()=>{conversation.current=conversationKey;requestGeneration.current++;recorder.current?.dispose();recorder.current=null;setRecording(false);setTranscribing(false);setInput('');void window.lca.cancelTranscription();},[conversationKey]);
  const model=profile?.model||'';
  const handledActivation=useRef(0);
  useEffect(()=>{
    if(!activation||!profile||busy||handledActivation.current===activation.id)return;
    handledActivation.current=activation.id;setInput(activation.text);
    setNotice(activation.text?'Команда распознана':'Лола активирована — говорите команду');
    if(activation.send&&activation.text&&profile.model){onAsk(activation.text);setInput('');}
  },[activation,profile,busy]);
  useEffect(()=>{window.dispatchEvent(new CustomEvent('manual-microphone',{detail:recording||transcribing}));return()=>{window.dispatchEvent(new CustomEvent('manual-microphone',{detail:false}));};},[recording,transcribing]);
  useEffect(()=>{if(profile)void window.lca.refreshVoices().then(result=>{if(result.ok)setStatus(result);});},[profile?.tts_provider]);

  useEffect(()=>{void window.lca.getCompanionSettings().then(result=>{if(result.ok){setProfile(result);setVoice(result.voice);setRate(result.rate);setVolume(result.volume);setAutoSpeak(result.auto_speak);}});return()=>{recorder.current?.dispose();recorder.current=null;void window.lca.cancelTranscription();};},[]);
  async function record() {
    if(recording){await finishRecording();return;}
    const capture=new MicrophoneRecorder();recorder.current=capture;setNotice('');setRecording(true);
    try{await capture.start(()=>void finishRecording(),60,autoEnd ? 0.8 : 0);if(recorder.current===capture)setRecording(true);}
    catch(error){capture.dispose();if(recorder.current===capture){recorder.current=null;setRecording(false);setNotice(String(error));}}
  }
  async function finishRecording() {
    const capture=recorder.current;if(!capture)return;const origin=conversation.current;const generation=++requestGeneration.current;recorder.current=null;setRecording(false);
    if(!capture.hasSpeech()){capture.dispose();setNotice('Не услышала речь. Поднесите микрофон ближе и повторите.');return;}
    setTranscribing(true);const started=performance.now();
    try{const result=await window.lca.transcribe(capture.finish());if(!result.ok)throw Error(result.error);if(alive.current&&conversation.current===origin&&generation===requestGeneration.current){const text=String(result.text||'').trim();if(!text)throw Error('Речь не распознана. Попробуйте ещё раз.');setInput(text);setNotice(`Распознано за ${((performance.now()-started)/1000).toFixed(1)} с`);if(autoSend&&model&&!busy){onAsk(text);setInput('');}}}
    catch(error){if(alive.current&&conversation.current===origin&&generation===requestGeneration.current)setNotice(String(error));}finally{if(alive.current&&conversation.current===origin&&generation===requestGeneration.current)setTranscribing(false);}
  }
  async function cancelRecording() {
    requestGeneration.current++;recorder.current?.dispose();recorder.current=null;setRecording(false);setTranscribing(false);setNotice('Голосовой ввод отменён');await window.lca.cancelTranscription();
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
    try{if(profile?.tts_provider==='piper'){const started=await window.lca.speechRuntime('start');if(!started.ok)throw Error(started.error);setRuntime(started);}const limit=profile?.tts_provider==='windows'?6000:1200;const result=await window.lca.speak({text:text.slice(0,limit),voice,rate,volume});if(!result.ok)throw new Error(result.error);setStatus(result);if(text.length>limit)setNotice('Озвучивается начало длинного ответа.');}
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
  const executing=task?.tool_activity?.some(item=>['running','applying','awaiting_approval'].includes(item.status));
  const avatarState:LolaState=recording||wakeListening?'listening':transcribing?'thinking':busy?(executing?'working':'thinking'):status.state==='speaking'?'speaking':status.state==='error'||task?.status==='failed'?'error':status.state==='synthesizing'?'thinking':celebrating?'success':'idle';
  return <main className={`voice-panel voice-${state}`}>

    <div className="voice-intro"><span className="eyebrow">ЛОЛА / ВСЕГДА РЯДОМ</span><div className="miya-heading"><h1>Лола · ваш ассистент</h1><button ref={settingsButton} type="button" className="secondary-button miya-settings-open" onClick={()=>settingsDialog.current?.showModal()}><Settings size={16}/>Настройки Лолы</button></div><p>Привет! Устраивайся поудобнее. Поболтаем или сделаем что-нибудь вместе?</p><span className="context-chip">Модель Лолы: {model||'не выбрана'}</span></div>
    <div className="companion-stage"><LolaAvatar state={avatarState} reducedMotion={!animate}/></div>
    <div className="voice-state" role="status"><span/>{recording?'Слушаю…':transcribing?'Распознаю речь…':busy?'Лола думает…':status.state==='speaking'?'Озвучка…':status.state==='synthesizing'?'Создаю голос Лолы…':status.state==='loading'?'Загрузка голосов…':status.state==='stopping'?'Остановка озвучки…':voice?'Готова к разговору':'Голос не подключён'}</div>
    <div className="voice-controls voice-actions">
      <div className="voice-buttons"><button className="primary-button microphone-record" disabled={!recording&&(busy||transcribing||!profile||voiceActive)} onClick={()=>void record()}><Mic size={16}/>{recording?'Завершить запись':'Микрофон · запись'}</button>
      {(recording||transcribing)&&<button className="secondary-button cancel-transcription" onClick={()=>void cancelRecording()}>Отменить голосовой ввод</button>}
      <button className="secondary-button speak-reply" disabled={!voice||voiceActive||busy||!(reply||input.trim())} onClick={()=>void speak(reply||input.trim())}><Volume2 size={15}/>Озвучить {reply?'ответ':'текст'}</button><button className="secondary-button stop-speech" disabled={!voiceActive} onClick={()=>void stop()}>Stop · голос</button></div>
      <p className="voice-stt-note">{recording?'Идёт запись · говорите, затем сделайте паузу или нажмите завершить':transcribing?'Распознаю речь… можно отменить':'Микрофон включается по нажатию. '+(autoSend?'Распознанный запрос отправится сразу.':'Распознанный текст можно проверить перед отправкой.')}</p>
      <button className="secondary-button" disabled={busy} onClick={onChat}><Sparkles size={14}/>Открыть Chat</button>
      {(notice||status.error)&&<p className="voice-error" role="status">{notice||status.error}</p>}
    </div>
    <dialog ref={settingsDialog} className="miya-settings-dialog" aria-labelledby="miya-settings-title" onClose={()=>{if(!settingsDialog.current?.open)settingsButton.current?.focus();}}>
      <header><h2 id="miya-settings-title">Настройки Лолы</h2><button type="button" aria-label="Закрыть настройки Лолы" onClick={()=>settingsDialog.current?.close()}><X size={20}/></button></header>
      <div className="miya-settings-body voice-controls">
      <div className="voice-preset-heading"><div><span className="eyebrow">ГОЛОС ЛОЛЫ</span><h2>Как я буду звучать</h2></div><span className={`voice-connection ${runtime.running?'connected':''}`}>{profile?.tts_provider==='piper'?(runtime.running?'Подключена':'Не запущена'):profile?.tts_provider==='windows'?'Голоса системы':'Внешний сервер'}</span></div>
      <label>Озвучка<select aria-label="Движок озвучки" value={profile?.tts_provider||'piper'} disabled={busy||voiceActive||!profile} onChange={event=>void selectProvider(event.target.value)}><option value="piper">Лола · Serena — рекомендуется</option><option value="windows">Голоса Windows</option><option value="qwen3">Внешний сервер / Qwen</option></select></label>
      {profile?.tts_provider==='piper'&&<div className="serena-preset"><p>Мягкий голос Лолы · работает без видеокарты</p><div className="voice-buttons"><button className="secondary-button" disabled={runtimeBusy||voiceActive} onClick={()=>void startSerena()}>{runtimeBusy?'Запускаю…':runtime.running?'Проверить подключение':'Запустить Serena'}</button><button className="secondary-button" disabled={busy||voiceActive||!voice||runtimeBusy} onClick={()=>void speak('Привет! Я Лола. Рада тебя видеть. Чем я могу помочь?')}>Послушать голос</button></div></div>}
      {profile?.tts_provider==='windows'&&<label>Голос<select aria-label="Голос ассистента" value={voice} disabled={voiceActive} onChange={event=>setVoice(event.target.value)}>{status.voices.map((item:any)=><option key={item.id} value={item.id}>{item.name||item.id} · {item.culture}</option>)}</select></label>}
      <label>Скорость · {Math.round(100*2**(rate/10))}%<input aria-label="Темп речи" type="range" min={-5} max={5} value={rate} onChange={event=>setRate(Number(event.target.value))}/></label>
      <label>Громкость · {volume}%<input aria-label="Громкость речи" type="range" min={0} max={100} value={volume} onChange={event=>setVolume(Number(event.target.value))}/></label>
      <label className="auto-speak"><input type="checkbox" checked={autoSpeak} onChange={event=>{lastRead.current=replyKey;setAutoSpeak(event.target.checked);}}/>Озвучивать новые ответы автоматически</label>
      <fieldset className="voice-input-settings"><legend>Голосовой ввод</legend>
      <label className="auto-speak"><input aria-label="Завершать запись после паузы" type="checkbox" checked={autoEnd} onChange={event=>{setAutoEnd(event.target.checked);localStorage.setItem('miya-auto-end',event.target.checked?'on':'off');}}/>Завершать запись после паузы</label>
      <label className="auto-speak"><input aria-label="Сразу отправлять распознанный запрос" type="checkbox" checked={autoSend} onChange={event=>{setAutoSend(event.target.checked);localStorage.setItem('miya-auto-send',event.target.checked?'on':'off');}}/>Сразу отправлять распознанный запрос</label>
      <p className="voice-stt-note">По умолчанию текст можно проверить перед отправкой. Автозавершение ждёт паузу около 0,8 секунды; запись всегда можно закончить кнопкой.</p>
      </fieldset>
      <button type="button" className="secondary-button miya-motion-toggle" aria-pressed={animate} onClick={()=>{setAnimate(!animate);localStorage.setItem('miya-animation',animate?'off':'on');}}>{animate?'Анимация включена':'Анимация выключена'}</button>
      <div className="voice-buttons"><button className="secondary-button" disabled={voiceActive} onClick={()=>void window.lca.refreshVoices()}>Обновить голоса</button><button className="primary-button" disabled={busy||!profile} onClick={()=>void saveVoice()}>Сохранить голос</button></div>
      {profile&&<CompanionSettings profile={{...profile,voice,rate,volume,auto_speak:autoSpeak}} busy={busy||recording||transcribing||voiceActive} onSaved={setProfile}/>}
      {(notice||status.error)&&<p className="voice-error" role="status">{notice||status.error}</p>}
      </div>
    </dialog>
    <section className="voice-conversation" aria-label="Разговор с ассистентом">{messages.slice(-8).map((message,index)=><div className={`voice-message ${message.role}`} key={index}><b>{message.role==='user'?'Вы':message.role==='assistant'?'Лола':'Состояние'}</b><ChatText text={message.text}/>{message.streaming&&<span>▍</span>}</div>)}</section>
    <form className="voice-composer" onSubmit={event=>{event.preventDefault();send();}}><textarea aria-label="Сообщение ассистенту" maxLength={50000} disabled={busy||recording||transcribing} value={input} onChange={event=>setInput(event.target.value)} placeholder={model?'Напишите Лолы…':'Выберите модель в настройках'}/>{busy?<button type="button" className="primary-button" onClick={onCancel}>Остановить ответ</button>:<button className="primary-button" disabled={!model||!input.trim()||recording||transcribing} type="submit">Отправить ассистенту</button>}</form>
  </main>;
}
