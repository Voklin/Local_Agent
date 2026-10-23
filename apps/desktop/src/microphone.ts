// Explicit push-to-record; PCM never goes to disk and tracks stop on every path.
export class MicrophoneRecorder {
  private stream: MediaStream | null = null;
  private context: AudioContext | null = null;
  private processor: ScriptProcessorNode | null = null;
  private samples: Float32Array[] = [];
  private frames = 0;
  private stopped = false;
  async start(onLimit:()=>void) {
    this.stream = await navigator.mediaDevices.getUserMedia({audio:true, video:false});
    if(this.stopped) {this.dispose();return;}
    try {
      this.context=new AudioContext({sampleRate:16000});
      await this.context.resume();
      const source=this.context.createMediaStreamSource(this.stream);
      this.processor=this.context.createScriptProcessor(4096,1,1);
      const silent=this.context.createGain();silent.gain.value=0;
      this.processor.onaudioprocess=event=>{
        const available=960000-this.frames;
        if(available<=0)return;
        const block=event.inputBuffer.getChannelData(0).slice(0,available);
        this.samples.push(block);this.frames+=block.length;
        if(this.frames>=960000)onLimit();
      };
      source.connect(this.processor);this.processor.connect(silent);silent.connect(this.context.destination);
    }catch(error){this.dispose();throw error;}
  }
  finish() {
    if(!this.frames){this.dispose();throw Error('Запись пуста; повторите после разрешения доступа к микрофону');}
    const buffer=new ArrayBuffer(44+this.frames*2),view=new DataView(buffer);
    const ascii=(offset:number,text:string)=>{for(let i=0;i<text.length;i++)view.setUint8(offset+i,text.charCodeAt(i));};
    ascii(0,'RIFF');view.setUint32(4,36+this.frames*2,true);ascii(8,'WAVE');ascii(12,'fmt ');
    view.setUint32(16,16,true);view.setUint16(20,1,true);view.setUint16(22,1,true);
    view.setUint32(24,16000,true);view.setUint32(28,32000,true);view.setUint16(32,2,true);view.setUint16(34,16,true);
    ascii(36,'data');view.setUint32(40,this.frames*2,true);
    let index=44;
    for(const block of this.samples)for(const value of block){const sample=Math.max(-1,Math.min(1,value));view.setInt16(index,Math.round(sample*(sample<0?32768:32767)),true);index+=2;}
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
