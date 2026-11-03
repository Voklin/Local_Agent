import fs from 'node:fs';
import path from 'node:path';
import net from 'node:net';
import {randomBytes,timingSafeEqual} from 'node:crypto';
import {spawn} from 'node:child_process';

/** Isolated Code-OSS launcher. The prototype bridge cannot execute agent actions. */
export class NeutralIde {
  private server:net.Server|null=null;
  private starting:Promise<void>|null=null;
  private token=randomBytes(32).toString('hex');
  private pipe=process.platform==='win32'?`\\\\.\\pipe\\neutral-ide-${randomBytes(16).toString('hex')}`:'';
  private sockets=new Set<net.Socket>();
  private coreAlive=true;
  private launches=new Set<ReturnType<typeof spawn>>();
  private clients=new Map<net.Socket,{scope:string;root:string}>();
  private scopes=new Map<string,{session_id:string;root:string;project_id:string}>();
  get connected(){return this.clients.size>0||this.launches.size>0;}
  constructor(private runtime:string,private profile:string,private health:()=>Promise<any>,private focus:()=>void,private backend:(method:string,params:any)=>Promise<any>,private invoke:(scope:string,channel:string,args:any[])=>Promise<any>|any,private extraArgs:string[]=[]){}

  private async connect() {
    if(this.starting)return this.starting;
    this.starting=new Promise<void>((resolve,reject)=>{
      if(!this.pipe){reject(Error('Прототип Neutral IDE пока доступен для Windows x64'));return;}
      this.server=net.createServer(socket=>{
        this.sockets.add(socket);socket.setEncoding('utf8');socket.setTimeout(5000,()=>socket.destroy());
        socket.once('close',()=>{this.sockets.delete(socket);const client=this.clients.get(socket);this.clients.delete(socket);if(client&&this.coreAlive&&![...this.clients.values()].some(other=>other.scope===client.scope))void this.backend('ide_detach',{session_id:client.scope});});socket.on('error',()=>{});
        let buffer='';let inflight=0;
        const send=(id:unknown,result:any)=>{if(!socket.destroyed)socket.write(JSON.stringify({id,result})+'\n');};
        socket.on('data',chunk=>{
          buffer+=chunk.toString('utf8');if(Buffer.byteLength(buffer)>32_000_000){socket.destroy();return;}
          for(let end=buffer.indexOf('\n');end>=0;end=buffer.indexOf('\n')){
            const line=buffer.slice(0,end);buffer=buffer.slice(end+1);
            if(++inflight>100){socket.destroy();return;}
            void (async()=>{let request:any;
              try{
                request=JSON.parse(line);const client=this.clients.get(socket);
                if(!client){
                  const provided=Buffer.from(typeof request.token==='string'?request.token:'');
                  if(provided.length!==this.token.length||!timingSafeEqual(provided,Buffer.from(this.token)))throw Error('Forbidden');
                  if(request.method==='status'){const state=await this.health();socket.end(JSON.stringify({ok:state.ok===true,service:'Neutral Core',project:state.project||null,prototype:false})+'\n');return;}
                  if(request.method==='focus'){this.focus();socket.end(JSON.stringify({ok:true})+'\n');return;}
                  if(request.method!=='connect')throw Error('Forbidden');if(request.version!==2)throw Error('Версии панели и Neutral различаются. Перезапустите оба приложения.');
                  const root=fs.realpathSync(String(request.root));let scope=this.scopes.get(root.toLowerCase());if(!scope){const attached=await this.backend('ide_attach',{root});if(!attached.ok)throw Error(attached.error);scope=attached;this.scopes.set(root.toLowerCase(),attached);}if(!scope)throw Error('Нет сессии IDE');
                  this.coreAlive=true;this.clients.set(socket,{scope:scope.session_id,root:scope.root});socket.setTimeout(0);send(request.id,{ok:true,version:2,...scope});return;
                }
                if(request.method==='ping'){send(request.id,{ok:true});return;}
                if(request.method==='editor_result'){
                  send(request.id,await this.backend('ide_editor_result',{session_id:client.scope,operation_id:request.operation_id,result:request.result}));return;
                }
                if(request.method==='focus'){this.focus();send(request.id,{ok:true});return;}
                if(request.method!=='invoke'||!IDE_CHANNELS.has(request.channel)||!Array.isArray(request.args))throw Error('Операция недоступна из IDE');
                send(request.id,await this.invoke(client.scope,request.channel,request.args));
              }catch(error){const result={ok:false,error:error instanceof Error?error.message:'IDE request failed'};if(!this.clients.has(socket))socket.end(JSON.stringify(result)+'\n');else send(request?.id,result);}
              finally{inflight--;}
            })();
          }
        });
      });
      this.server.once('error',reject);
      this.server.listen(this.pipe,()=>{
        try{
          fs.mkdirSync(this.profile,{recursive:true});
          fs.writeFileSync(path.join(this.profile,'connection.json'),JSON.stringify({pipe:this.pipe,token:this.token}),{mode:0o600});
          resolve();
        }catch(error){reject(error);}
      });
    }).catch(error=>{this.starting=null;this.server?.close();this.server=null;throw error;});
    return this.starting;
  }

  async open() {
    try{
      const exe=path.join(this.runtime,'NeutralIDE.exe');
      const product=JSON.parse(await fs.promises.readFile(path.join(this.runtime,'resources/app/product.json'),'utf8'));
      if(!fs.existsSync(exe)||product.applicationName!=='neutral-ide'||!['Neutral IDE','LESHY IDE'].includes(product.nameShort))throw Error('Runtime missing');
      const state=await this.health();
      if(!state.ok)return {ok:false,error:'Ядро Neutral недоступно'};
      const project=typeof state.project==='string'&&fs.existsSync(state.project)&&fs.statSync(state.project).isDirectory()?state.project:null;
      if(project){const scope=await this.backend('ide_attach',{root:project});if(!scope.ok)return scope;this.scopes.set(fs.realpathSync(project).toLowerCase(),scope);}
      await this.connect();
      const userData=path.join(this.profile,'user-data'),extensions=path.join(this.profile,'extensions');
      const settings=path.join(userData,'User/settings.json');fs.mkdirSync(path.dirname(settings),{recursive:true});fs.mkdirSync(extensions,{recursive:true});
      if(!fs.existsSync(settings))fs.writeFileSync(settings,JSON.stringify({'workbench.colorTheme':'LESHY Лесная','telemetry.telemetryLevel':'off','update.mode':'none','extensions.autoUpdate':'off','extensions.autoCheckUpdates':false,'workbench.startupEditor':'none'},null,2));
      try{const appearance=await this.invoke('','appearance:get',[]);const preferences=JSON.parse(fs.readFileSync(settings,'utf8'));const label=({forest:'LESHY Лесная',parchment:'LESHY Парчовая',twilight:'LESHY Сумеречная'} as Record<string,string>)[appearance.theme];if(label){preferences['workbench.colorTheme']=label;fs.writeFileSync(settings,JSON.stringify(preferences,null,2));}}catch{/* Keep custom JSONC; connected view synchronizes through configuration API. */}
      // This is an interactive GUI, not a background helper: SW_HIDE hides its window.
      const child=spawn(exe,['--new-window','--user-data-dir',userData,'--shared-data-dir',path.join(this.profile,'shared-data'),'--extensions-dir',extensions,...this.extraArgs,...(project?[project]:[])],{cwd:this.runtime,windowsHide:false,detached:true,stdio:'ignore',env:{...process.env,ELECTRON_RUN_AS_NODE:undefined,NEUTRAL_IDE_CONNECTION:path.join(this.profile,'connection.json')}});
      await new Promise<void>((resolve,reject)=>{child.once('spawn',resolve);child.once('error',reject);});this.launches.add(child);child.once('exit',()=>this.launches.delete(child));child.unref();
      return {ok:true,pid:child.pid,prototype:false};
    }catch{return {ok:false,error:'Neutral IDE не подготовлена. Выполните prototypes/neutral-ide/prepare.py; установленный VS Code не используется.'};}
  }

  publish(message:any){
    if(message.event==='backend_stopped'){this.coreAlive=false;this.scopes.clear();}
    if(message.event==='ide_editor'){
      const targets=[...this.clients].filter(([,client])=>client.scope===message.session_id);
      if(targets.length){targets[0][0].write(JSON.stringify({event:message})+'\n');}
      else void this.backend('ide_editor_result',{session_id:message.session_id,operation_id:message.operation_id,result:{ok:false,code:message.phase==='apply'?'OUTCOME_UNKNOWN':'IDE_DISCONNECTED',error:'Панель редактора отключена'}});
      return;
    }
    for(const [socket,client] of this.clients){
      if(message.event==='appearance_theme'||message.event==='backend_stopped'||(message.project_root&&path.resolve(message.project_root).toLowerCase()===path.resolve(client.root).toLowerCase()))socket.write(JSON.stringify({event:message})+'\n');
    }
  }

  dispose() {
    for(const socket of this.sockets)socket.destroy();this.server?.close();this.server=null;
    const file=path.join(this.profile,'connection.json');
    try{if(JSON.parse(fs.readFileSync(file,'utf8')).token===this.token)fs.unlinkSync(file);}catch{/* An old session cannot remove a new descriptor. */}
  }
}

// Only existing product UI channels; no arbitrary RPC, shell, desktop or voice route.
const IDE_CHANNELS=new Set([
 'appearance:get','appearance:set',
 'ide:complete','core:health','model:settings','model:configure','model:list','model:test','model:cancel-setup',
 'connections:list','connections:save','connections:delete',
 'chat:list','chat:new','chat:load','chat:rename','chat:search','chat:update','chat:delete','chat:fork',
 'task:start','task:cancel','task:approve','task:plan','task:resolve-recovery','run:active','run:history',
 'project:list','project:read','project:search','project:index','project:cancel-search',
 'memory:get','memory:save','memory:action','workspace:access','workspace:access-configure',
 'optional:settings','optional:configure','optional:run','optional:cancel',
 'storage:status','storage:backup','storage:cancel','extensions:import','extensions:list','extensions:configure','extensions:discover','extensions:cancel-discovery',
 'snapshot:list','snapshot:preview','snapshot:apply','snapshot:review','snapshot:checkpoint','snapshot:checkpoint-cancel',
 'ide:workspace-changed','ide:export-chat','runtime:pick','runtime:start','runtime:status','runtime:stop'
]);
