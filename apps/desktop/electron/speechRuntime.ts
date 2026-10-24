import { spawn, type ChildProcess } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { createHash } from 'node:crypto';

const MODEL='ru_RU-miya-serena-medium.onnx';
const SHA='4610a755335a68bb102ea0bde426aa95f75191e8d6d438d8a51d99397319913d';

export class SpeechRuntime {
  private child:ChildProcess|null=null;
  private starting:Promise<any>|null=null;
  constructor(private localDirectory:string,private scripts:string,private candidate:string) {}
  private files() {
    return {python:path.join(this.localDirectory,'piper-runtime/Scripts/python.exe'),
      model:path.join(this.localDirectory,'speech/piper/serena',MODEL),script:path.join(this.scripts,'piper_server.py')};
  }
  install(source=this.candidate) {
    if(!fs.existsSync(source)||!fs.existsSync(source+'.json'))return {ok:false,error:'Выберите ONNX и соответствующий JSON обученной Serena.'};
    if(fs.statSync(source).size!==63516051||createHash('sha256').update(fs.readFileSync(source)).digest('hex')!==SHA)
      return {ok:false,error:'Это другая модель. Нужен файл обученной Serena из папки serena-piper.'};
    const config=JSON.parse(fs.readFileSync(source+'.json','utf8'));
    if(config.audio?.sample_rate!==22050||config.espeak?.voice!=='ru')return {ok:false,error:'Неверный файл настроек голоса Serena.'};
    const {model}=this.files();fs.mkdirSync(path.dirname(model),{recursive:true});
    if(path.resolve(source)!==path.resolve(model)){fs.copyFileSync(source,model);fs.copyFileSync(source+'.json',model+'.json');}
    return {ok:true};
  }
  async status() {
    const files=this.files();let health:any=null;
    try {const response=await fetch('http://127.0.0.1:9080/health',{signal:AbortSignal.timeout(1500)});if(response.ok)health=await response.json();}catch{/* Not running. */}
    return {ok:true,running:health?.model==='Piper/'+path.basename(MODEL,'.onnx'),occupied:!!health,
      modelAvailable:fs.existsSync(files.model)&&fs.existsSync(files.model+'.json'),runtimeAvailable:fs.existsSync(files.python),
      managed:!!this.child,model:health?.model||'',device:health?.device||'',busy:health?.busy===true};
  }
  async start() {
    if(this.starting)return this.starting;
    this.starting=this.launch().finally(()=>{this.starting=null;});return this.starting;
  }
  private async launch() {
    let status=await this.status();if(status.running)return status;
    if(status.occupied)return {ok:false,error:'Порт озвучки занят другим голосом. Остановите его перед запуском Serena.'};
    if(!status.modelAvailable){const installed=this.install();if(!installed.ok)return installed;}
    const files=this.files();
    if(!fs.existsSync(files.python))return {ok:false,error:'Компоненты Piper не установлены. Откройте папку TTS и запустите start-piper.ps1.'};
    if(!fs.existsSync(files.script))return {ok:false,error:'Не найден локальный сервер Piper.'};
    const child=spawn(files.python,[files.script,'--model',files.model],{windowsHide:true,stdio:'ignore',cwd:this.scripts});
    this.child=child;let error='';
    child.once('error',()=>{error='Не удалось запустить компоненты Piper.';if(this.child===child)this.child=null;});
    child.once('exit',()=>{if(this.child===child)this.child=null;});
    for(let attempt=0;attempt<30;attempt++) {
      await new Promise(resolve=>setTimeout(resolve,300));status=await this.status();
      if(status.running)return status;if(error)return {ok:false,error};
      if(child.exitCode!==null)break;
    }
    await this.stop();return {ok:false,error:'Serena не запустилась. Проверьте установку Piper в дополнительных настройках.'};
  }
  async stop() {
    const child=this.child;if(!child?.pid)return {ok:true};this.child=null;
    if(process.platform==='win32')await new Promise<void>(resolve=>{
      const killer=spawn(path.join(process.env.WINDIR||'C:/Windows','System32/taskkill.exe'),['/PID',String(child.pid),'/T','/F'],{windowsHide:true,stdio:'ignore'});
      killer.once('error',()=>resolve());killer.once('exit',()=>resolve());
    });else child.kill();
    return {ok:true};
  }
}
