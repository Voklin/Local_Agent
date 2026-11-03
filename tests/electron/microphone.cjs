// Deterministic PCM tests: no real microphone or speakers.
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const ts=require('typescript');
const path=require('node:path');
let processor,stops=0,options;
const context={exports:{},navigator:{mediaDevices:{getUserMedia:async value=>{options=value;return {getTracks:()=>[{stop:()=>stops++}]};}}},
  AudioContext:class {
    sampleRate=16000;destination={};
    async resume(){} async close(){}
    createMediaStreamSource(){return {connect(){}};}
    createGain(){return {gain:{value:1},connect(){}};}
    createScriptProcessor(size){assert.equal(size,1024);processor={connect(){},disconnect(){}};return processor;}
  },btoa:value=>Buffer.from(value,'binary').toString('base64')};
const source=fs.readFileSync(path.resolve(__dirname,'../../apps/desktop/src/microphone.ts'),'utf8');
vm.runInNewContext(ts.transpileModule(source,{compilerOptions:{module:ts.ModuleKind.CommonJS,target:ts.ScriptTarget.ES2022}}).outputText,context);
const {MicrophoneRecorder}=context.exports;
async function main(){
  const capture=new MicrophoneRecorder();let ended=0;
  await capture.start(()=>ended++,60,.8);
  assert.equal(options.audio.echoCancellation,true);assert.equal(options.audio.noiseSuppression,true);
  const block=value=>processor.onaudioprocess({inputBuffer:{getChannelData:()=>new Float32Array(1024).fill(value)}});
  for(let i=0;i<32;i++)block(0);
  for(let i=0;i<5;i++)block(.1);
  for(let i=0;i<13;i++)block(0);
  assert.equal(ended,1,'End after 0.832 seconds of silence');assert.equal(capture.hasSpeech(),true);
  const wav=Buffer.from(capture.finish(),'base64');
  assert.equal(wav.readUInt32LE(24),16000);assert.equal(wav.readUInt32LE(40),wav.length-44);
  assert.equal(wav.length,44+2*(3200+5120+4000),'Trim silence but retain speech margins');assert.equal(stops,1);
  const silent=new MicrophoneRecorder();ended=0;await silent.start(()=>ended++,60,.8);
  for(let i=0;i<125;i++)block(0);
  assert.equal(ended,1);assert.equal(silent.hasSpeech(),false);silent.dispose();assert.equal(stops,2);
  const cancelled=new MicrophoneRecorder();await cancelled.start(()=>{},60,.8);cancelled.dispose();assert.equal(stops,3);
  console.log('PASS: silence endpoint, trimmed PCM, silent capture, audio constraints, track cleanup');
}
main().catch(error=>{console.error(error);process.exitCode=1;});
