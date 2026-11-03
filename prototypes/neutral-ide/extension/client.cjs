const vscode=require('vscode'),fs=require('node:fs/promises'),net=require('node:net');
class AgentClient{
 constructor(root,onEvent){this.root=root;this.onEvent=onEvent;this.socket=null;this.pending=new Map();this.sequence=0;this.starting=null;this.scope=null;}
 async connect(){
  if(this.socket&&!this.socket.destroyed&&this.scope)return this.scope;
  if(this.starting)return this.starting;
  this.starting=(async()=>{
   if(!process.env.NEUTRAL_IDE_CONNECTION)throw Error('Откройте проект кнопкой IDE из Neutral');
   const config=JSON.parse(await fs.readFile(process.env.NEUTRAL_IDE_CONNECTION,'utf8'));
   if(typeof config.pipe!=='string'||!config.pipe.startsWith('\\\\.\\pipe\\neutral-ide-'))throw Error('Неверный канал Neutral');
   const socket=this.socket=net.createConnection(config.pipe);socket.setEncoding('utf8');let buffer='';
   socket.on('data',chunk=>{buffer+=chunk.toString('utf8');if(Buffer.byteLength(buffer)>32_000_000){socket.destroy();return;}for(let end=buffer.indexOf('\n');end>=0;end=buffer.indexOf('\n')){const line=buffer.slice(0,end);buffer=buffer.slice(end+1);try{const message=JSON.parse(line);if(message.event){this.onEvent(message.event);continue;}const entry=this.pending.get(message.id);if(entry){clearTimeout(entry.timer);this.pending.delete(message.id);entry.resolve(message.result);}}catch{socket.destroy();}}});
   socket.on('error',()=>{});socket.on('close',()=>{this.scope=null;this.starting=null;for(const entry of this.pending.values()){clearTimeout(entry.timer);entry.resolve({ok:false,error:'Neutral отключено. Перезапустите Neutral и перезагрузите панель.'});}this.pending.clear();this.onEvent({event:'backend_stopped'});});
   await new Promise((resolve,reject)=>{socket.once('connect',resolve);socket.once('error',reject);});
   const result=await this.send({method:'connect',version:2,token:config.token,root:this.root});if(!result.ok){socket.destroy();throw Error(result.error);}this.scope=result;return result;
  })().catch(error=>{this.starting=null;throw error;});return this.starting;
 }
 send(message){return new Promise(resolve=>{const id=++this.sequence,timer=setTimeout(()=>{this.pending.delete(id);resolve({ok:false,error:'Время ожидания Neutral истекло'});},180000);this.pending.set(id,{resolve,timer});this.socket.write(JSON.stringify({id,...message})+'\n');});}
 async invoke(channel,args=[]){await this.connect();return this.send({method:'invoke',channel,args});}
 async result(operation_id,result){await this.connect();return this.send({method:'editor_result',operation_id,result});}
 async focus(){await this.connect();return this.send({method:'focus'});}
 dispose(){this.socket?.destroy();}
}
module.exports={AgentClient};
