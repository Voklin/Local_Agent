import { Mic, Volume2, Sparkles } from 'lucide-react';

export type WorkspaceMode = 'chat' | 'ide' | 'voice';
// Provider contracts keep audio processing separate from the model and renderer.
export type VoiceSessionState = 'disconnected' | 'listening' | 'thinking' | 'speaking' | 'error';
export interface VoiceProfile {
  persona: string;
  transcriptionProvider: string | null;
  speechProvider: string | null;
  pushToTalk: boolean;
}

export function VoicePanel({ onChat }: { onChat: () => void }) {
  return <main className="voice-panel">
    <div className="voice-intro"><span className="eyebrow">LOCALAGENT / COMPANION</span><h1>Ваш голосовой ассистент</h1><p>Отдельное пространство для общения голосом с аниме-персонажем.</p></div>
    <div className="companion-stage">
      <div className="companion-orbit"/>
      <svg className="maid-concept" viewBox="0 0 240 290" role="img" aria-label="Эскиз аниме-горничной для будущего ассистента">
        <path fill="#555875" d="M63 120Q33 28 120 24q87 4 57 96l18 107H45z"/>
        <path fill="#eedbe1" d="M72 83q0-45 48-45t48 45v26q-3 51-48 53-45-2-48-53z"/>
        <path fill="#656583" d="M62 88q-2-65 59-61 64 0 57 72l-32-39-11 33-22-35-18 39-9-23z"/>
        <path fill="#ece6ef" d="m67 45 9-18 18 1 13-15 14 8 17-8 13 15 17 1 8 18-18-1-17-10-21 2-24-1-16 10z"/>
        <ellipse cx="99" cy="108" rx="7" ry="10" fill="#79659a"/><ellipse cx="144" cy="108" rx="7" ry="10" fill="#79659a"/>
        <circle cx="101" cy="104" r="2.5" fill="white"/><circle cx="146" cy="104" r="2.5" fill="white"/>
        <path d="M113 133q8 6 16 0" fill="none" stroke="#b38697" strokeWidth="3" strokeLinecap="round"/>
        <path fill="#34384e" d="m91 155-35 22-24 88h176l-24-88-35-22-29 18z"/>
        <path fill="#f0eaf0" d="m88 161 32 17 31-17 14 32-13 72H88l-13-72z"/>
        <path fill="#b99ab9" d="m120 180-20-9v21l20-7 20 7v-21z"/>
        <path d="M85 235h70M96 204v47m48-47v47" stroke="#d2c6d6" fill="none" strokeWidth="2"/>
      </svg>
      <span className="concept-caption">Эскиз персонажа · анимация появится позже</span>
    </div>
    <div className="voice-state"><span/>Подготовка · голос ещё не подключён</div>
    <div className="voice-capabilities">
      <article><Mic size={20}/><h3>Распознавание речи</h3><p>Провайдер STT не выбран. Доступ к микрофону пока не запрашивается.</p></article>
      <article><Volume2 size={20}/><h3>Синтез голоса</h3><p>Провайдер TTS не выбран. Будут добавлены выбор голоса и остановка озвучки.</p></article>
      <article><Sparkles size={20}/><h3>Персонаж</h3><p>Аниме-горничная: будущие настройки имени, манеры общения и анимации.</p></article>
    </div>
    <button className="primary-button" onClick={onChat}>Пока общаться в Chat</button>
  </main>;
}
