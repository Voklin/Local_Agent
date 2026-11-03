import {BrowserWindow,Tray,Menu,ipcMain,screen} from 'electron';
import fs from 'node:fs';
import path from 'node:path';
import {fitLolaBounds,lolaDesktopDefaults,lolaInitialFrame,validateLolaSettings,validateLolaFrame,type LolaDesktopSettings,type LolaDesktopFrame,type LolaDesktopAction} from '../shared/lolaDesktop';

export class DesktopLola {
  private window:BrowserWindow|null=null;
  private tray:Tray|null=null;
  private settings:LolaDesktopSettings={...lolaDesktopDefaults};
  private frame:LolaDesktopFrame={...lolaInitialFrame};
  private disposing=false;
  private rendererReady=false;
  private pendingEvents:unknown[]=[];
  private saveTimer:ReturnType<typeof setTimeout>|null=null;
  private readonly file:string;
  private readonly displayChanged=()=>this.applyBounds();
  constructor(private options:{directory:string;preload:string;html:string;devUrl?:string;icon:string;showMain:()=>void;dispatch:(action:LolaDesktopAction)=>void;notify:(settings:LolaDesktopSettings)=>void;quit:()=>void}) {
    this.file=path.join(options.directory,'lola-desktop.json');
    try{this.settings=validateLolaSettings(JSON.parse(fs.readFileSync(this.file,'utf8')));}catch{/* Invalid preferences leave the companion disabled. */}
    for(const [name,handler] of Object.entries({
      status:()=>this.status(),
      ready:()=>{this.rendererReady=true;for(const value of this.pendingEvents)this.window?.webContents.send('core:event',value);this.pendingEvents=[];return {ok:true};},
      action:(value:unknown)=>this.action(value),
      main:()=>{this.options.showMain();return {ok:true};},
      menu:()=>{this.menu().popup({window:this.window||undefined});return {ok:true};},
      hover:(value:unknown)=>{this.window?.setIgnoreMouseEvents(this.settings.clickThrough||value!==true,{forward:true});return {ok:true};},
      move:(value:unknown)=>this.move(value),
    }))ipcMain.handle('lola-widget:'+name,(event,value)=>{
      if(!this.window||this.window.isDestroyed()||event.sender!==this.window.webContents||event.senderFrame!==this.window.webContents.mainFrame)return {ok:false,error:'Forbidden sender'};
      try{return handler(value);}catch{return {ok:false,error:'Не удалось выполнить действие Лолы'};}
    });
    screen.on('display-removed',this.displayChanged);screen.on('display-metrics-changed',this.displayChanged);
    this.apply();
  }
  get enabled(){return this.settings.enabled;}
  owns(contents:Electron.WebContents,frame:Electron.WebFrameMain|null){return !!this.window&&!this.window.isDestroyed()&&contents===this.window.webContents&&frame===this.window.webContents.mainFrame;}
  sendEvent(value:any){if(this.rendererReady&&this.window&&!this.window.isDestroyed())this.window.webContents.send('core:event',value);else if(['lola_action','lola_open_chat'].includes(value.event))this.pendingEvents=[...this.pendingEvents.slice(-7),value];}
  open(chatId?:string,action?:LolaDesktopAction){this.configure({...this.settings,enabled:true,mode:'top',clickThrough:false});if(chatId)this.sendEvent({event:'lola_open_chat',chat_id:chatId});if(action)this.action(action);return this.status();}
  status(){return {ok:true,settings:{...this.settings},frame:{...this.frame},visible:!!this.window?.isVisible()};}
  configure(value:unknown){
    const previous=this.settings;this.settings=validateLolaSettings(value);
    if(this.window&&this.settings.position&&previous.size!==this.settings.size){
      const bounds=this.window.getBounds(),delta=this.settings.size-previous.size;
      this.settings={...this.settings,position:{x:bounds.x-Math.round(delta/2),y:bounds.y-delta}};
    }
    try{this.persist();this.apply();}catch(error){this.settings=previous;try{this.persist();this.apply();}catch{}throw error;}
    this.options.notify(this.settings);return this.status();
  }
  private menuConfigure(value:unknown){try{this.configure(value);}catch{this.present({...this.frame,state:'error',caption:'Не удалось сохранить настройки. Откройте Лешего.'});}}
  present(value:unknown){this.frame=validateLolaFrame(value);this.push();}
  private persist(){
    fs.mkdirSync(path.dirname(this.file),{recursive:true});const temp=this.file+'.pending';
    const fd=fs.openSync(temp,'w');try{fs.writeFileSync(fd,JSON.stringify(this.settings));fs.fsyncSync(fd);}finally{fs.closeSync(fd);}fs.renameSync(temp,this.file);
  }
  private push(){if(this.window&&!this.window.isDestroyed())this.window.webContents.send('lola-widget:state',{settings:this.settings,frame:this.frame});}
  private menu(){return Menu.buildFromTemplate([
    {label:'Открыть Лешего',click:()=>this.options.showMain()},
    {label:'Показать Лолу',click:()=>this.menuConfigure({...this.settings,mode:'top',clickThrough:false})},
    {label:'Вернуть Лолу в угол экрана',click:()=>this.menuConfigure({...this.settings,position:null,mode:'top',clickThrough:false})},
    {label:'Слушать / завершить запись',click:()=>this.options.dispatch({action:'record'})},
    {label:'Остановить задачу и голос',click:()=>this.options.dispatch({action:'stop'})},
    {type:'separator'},
    {label:'Поверх окон',type:'checkbox',checked:this.settings.mode==='top',click:()=>this.menuConfigure({...this.settings,mode:this.settings.mode==='top'?'desktop':'top'})},
    {label:'Пропускать клики',type:'checkbox',checked:this.settings.clickThrough,click:()=>this.menuConfigure({...this.settings,clickThrough:!this.settings.clickThrough})},
    {label:'Спрятать в трэй',click:()=>this.menuConfigure({...this.settings,mode:'tray'})},
    {label:'Настройки Лолы',click:()=>{this.options.showMain();this.options.dispatch({action:'settings'});}},
    {type:'separator'},
    {label:'Выключить спутника',click:()=>{this.menuConfigure({...this.settings,enabled:false});this.options.showMain();}},
    {label:'Выйти из Лешего',click:()=>this.options.quit()},
  ]);}
  private apply(){
    if(!this.settings.enabled){this.window?.destroy();this.window=null;this.tray?.destroy();this.tray=null;return;}
    if(!this.tray){this.tray=new Tray(this.options.icon);this.tray.setToolTip('Леший · Лола');this.tray.on('double-click',()=>this.options.showMain());}
    this.tray.setContextMenu(this.menu());
    if(this.settings.mode==='tray'){this.window?.hide();this.push();return;}
    if(!this.window){
      const window=new BrowserWindow({show:false,transparent:true,frame:false,resizable:false,skipTaskbar:true,hasShadow:false,backgroundColor:'#00000000',title:'Лола · Леший',
        webPreferences:{preload:this.options.preload,contextIsolation:true,nodeIntegration:false,sandbox:true,webgl:false}});
      this.window=window;
      window.webContents.setWindowOpenHandler(()=>({action:'deny'}));window.webContents.on('will-navigate',event=>event.preventDefault());
      window.webContents.on('did-finish-load',()=>{this.push();if(this.settings.enabled&&this.settings.mode!=='tray'){window.showInactive();window.setAlwaysOnTop(this.settings.mode==='top','pop-up-menu');}});
      window.on('close',event=>{if(!this.disposing){event.preventDefault();this.menuConfigure({...this.settings,mode:'tray'});}});
      window.on('move',()=>{const [x,y]=window.getPosition();this.settings={...this.settings,position:{x,y}};if(this.saveTimer)clearTimeout(this.saveTimer);this.saveTimer=setTimeout(()=>{try{this.persist();}catch{}},350);});
      window.webContents.on('did-start-loading',()=>{this.rendererReady=false;});
      if(this.options.devUrl)void window.loadURL(this.options.devUrl);else void window.loadFile(this.options.html);
    }
    this.applyBounds();this.window.setAlwaysOnTop(this.settings.mode==='top','pop-up-menu');this.window.setIgnoreMouseEvents(true,{forward:true});this.push();
    if(!this.window.webContents.isLoading()){this.window.showInactive();this.window.setAlwaysOnTop(this.settings.mode==='top','pop-up-menu');}
  }
  private applyBounds(){
    if(!this.window||this.window.isDestroyed())return;
    const point=this.settings.position||screen.getCursorScreenPoint();const display=screen.getDisplayNearestPoint(point);
    this.window.setBounds(fitLolaBounds(this.settings,display.workArea));
  }
  private move(value:unknown){
    if(!value||typeof value!=='object')throw Error('Invalid delta');const v=value as Record<string,unknown>;
    if(typeof v.x!=='number'||typeof v.y!=='number'||!Number.isFinite(v.x)||!Number.isFinite(v.y)||Math.abs(v.x)>200||Math.abs(v.y)>200)throw Error('Invalid delta');
    const pos=this.window?.getPosition();if(!pos)return {ok:false};
    this.settings={...this.settings,position:{x:pos[0]+Math.round(v.x),y:pos[1]+Math.round(v.y)}};this.applyBounds();return {ok:true};
  }
  private action(value:unknown){
    if(!value||typeof value!=='object')throw Error('Invalid action');const v=value as Record<string,unknown>;
    if(!['ask','record','stop','settings','speak'].includes(String(v.action)))throw Error('Invalid action');
    if(v.action==='ask'&&(typeof v.text!=='string'||!v.text.trim()||v.text.length>2000))throw Error('Invalid text');
    if(v.action==='settings')this.options.showMain();
    this.options.dispatch({action:v.action as LolaDesktopAction['action'],...(typeof v.text==='string'?{text:v.text.trim()}:{})});return {ok:true};
  }
  dispose(){
    this.disposing=true;if(this.saveTimer){clearTimeout(this.saveTimer);try{this.persist();}catch{}}
    this.window?.destroy();this.window=null;this.tray?.destroy();this.tray=null;
    screen.removeListener('display-removed',this.displayChanged);screen.removeListener('display-metrics-changed',this.displayChanged);
    for(const name of ['status','ready','action','main','menu','hover','move'])ipcMain.removeHandler('lola-widget:'+name);
  }
}
