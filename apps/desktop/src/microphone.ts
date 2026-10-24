// Explicit push-to-record; PCM never goes to disk and tracks stop on every path.
export class MicrophoneRecorder {
  private stream: MediaStream | null = null;
  private context: AudioContext | null = null;
  private processor: ScriptProcessorNode | null = null;
  private samples: Float32Array[] = [];
  private frames = 0;
  private stopped = false;
  private voicedBlocks = 0;
  private firstSpeech = -1;
  private lastSpeech = 0;
  async start(onLimit:()=>void, seconds=60, silenceSeconds=0) {
    const maximum=Math.max(1,Math.min(60,seconds))*16000;
    this.stream = await navigator.mediaDevices.getUserMedia({audio:{channelCount:1,echoCancellation:true,noiseSuppression:true,autoGainControl:true}, video:false});
    if(this.stopped) {this.dispose();return;}
    try {
      this.context=new AudioContext({sampleRate:16000});
      if(this.context.sampleRate!==16000)throw Error('Микрофон не поддерживает запись 16 кГц. Выберите другое устройство.');
      await this.context.resume();
      const source=this.context.createMediaStreamSource(this.stream);
      this.processor=this.context.createScriptProcessor(1024,1,1);
      const silent=this.context.createGain();silent.gain.value=0;
      this.processor.onaudioprocess=event=>{
        const available=maximum-this.frames;
        if(available<=0)return;
        const block=event.inputBuffer.getChannelData(0).slice(0,available);
        if(Math.sqrt(block.reduce((sum,value)=>sum+value*value,0)/block.length)>.01){this.voicedBlocks++;if(this.firstSpeech<0)this.firstSpeech=this.frames;this.lastSpeech=this.frames+block.length;}
        this.samples.push(block);this.frames+=block.length;
        if(this.frames>=maximum||(silenceSeconds>0&&((this.hasSpeech()&&this.frames-this.lastSpeech>=silenceSeconds*16000)||(!this.hasSpeech()&&this.frames>=8*16000))))onLimit();
      };
      source.connect(this.processor);this.processor.connect(silent);silent.connect(this.context.destination);
    }catch(error){this.dispose();throw error;}
  }
  hasSpeech() {return this.voicedBlocks>=2;}
  finish() {
    if(!this.frames){this.dispose();throw Error('Запись пуста; повторите после разрешения доступа к микрофону');}
    const begin=this.firstSpeech<0?0:Math.max(0,this.firstSpeech-3200);
    const end=this.lastSpeech?Math.min(this.frames,this.lastSpeech+4000):this.frames;
    const frames=end-begin;
    const buffer=new ArrayBuffer(44+frames*2),view=new DataView(buffer);
    const ascii=(offset:number,text:string)=>{for(let i=0;i<text.length;i++)view.setUint8(offset+i,text.charCodeAt(i));};
    ascii(0,'RIFF');view.setUint32(4,36+frames*2,true);ascii(8,'WAVE');ascii(12,'fmt ');
    view.setUint32(16,16,true);view.setUint16(20,1,true);view.setUint16(22,1,true);
    view.setUint32(24,16000,true);view.setUint32(28,32000,true);view.setUint16(32,2,true);view.setUint16(34,16,true);
    ascii(36,'data');view.setUint32(40,frames*2,true);
    let index=44,position=0;
    for(const block of this.samples){const from=Math.max(0,begin-position),to=Math.min(block.length,end-position);for(let offset=from;offset<to;offset++){const sample=Math.max(-1,Math.min(1,block[offset]));view.setInt16(index,Math.round(sample*(sample<0?32768:32767)),true);index+=2;}position+=block.length;if(position>=end)break;}
    this.dispose();
    const bytes=new Uint8Array(buffer);let binary='';
    for(let offset=0;offset<bytes.length;offset+=8192)binary+=String.fromCharCode(...bytes.subarray(offset,offset+8192));
    return btoa(binary);
  }
  dispose() {
    this.stopped=true;
    if(this.processor){this.processor.onaudioprocess=null;this.processor.disconnect();}
    this.stream?.getTracks().forEach(track=>track.stop());
    void this.context?.close();this.samples=[];this.stream=null;this.context=null;this.processor=null;
  }
}
