import fs from 'node:fs';
import path from 'node:path';
import { randomUUID } from 'node:crypto';

type Application = { id:string; name:string; file:string };

export class DesktopApplications {
  constructor(private directory:string, private launch:(file:string)=>Promise<void>, private browse:()=>Promise<void>) {}

  private custom():Application[] {
    try {
      const data=JSON.parse(fs.readFileSync(path.join(this.directory,'desktop-apps.json'),'utf8'));
      if(!Array.isArray(data))return [];
      return data.slice(0,30).filter(item=>item&&typeof item.id==='string'&&/^app-[a-f0-9-]{36}$/.test(item.id)&&
        typeof item.name==='string'&&item.name.length<=80&&typeof item.file==='string'&&
        path.isAbsolute(item.file)&&!item.file.startsWith('\\\\')&&path.extname(item.file).toLowerCase()==='.exe');
    }catch{return [];}
  }

  private catalog():Application[] {
    const windows=process.env.WINDIR||'C:\\Windows';
    return [
      {id:'notepad',name:'Блокнот',file:path.join(windows,'System32/notepad.exe')},
      {id:'calculator',name:'Калькулятор',file:path.join(windows,'System32/calc.exe')},
      {id:'paint',name:'Paint',file:path.join(windows,'System32/mspaint.exe')},
      {id:'explorer',name:'Проводник',file:path.join(windows,'explorer.exe')},
      ...this.custom(),
    ].filter(item=>fs.existsSync(item.file));
  }

  list() {
    return [{id:'browser',name:'Браузер',custom:false},...this.catalog().map(item=>({id:item.id,name:item.name,custom:item.id.startsWith('app-')}))];
  }

  private save(items:Application[]) {
    fs.mkdirSync(this.directory,{recursive:true});
    const destination=path.join(this.directory,'desktop-apps.json');
    const temporary=destination+'.'+randomUUID()+'.tmp';
    fs.writeFileSync(temporary,JSON.stringify(items),'utf8');fs.renameSync(temporary,destination);
  }

  add(file:string) {
    const resolved=fs.realpathSync(file);
    if(!path.isAbsolute(resolved)||resolved.startsWith('\\\\')||path.extname(resolved).toLowerCase()!=='.exe'||!fs.statSync(resolved).isFile())throw Error('Выберите локальный EXE-файл приложения');
    const items=this.custom();
    if(items.some(item=>item.file.toLowerCase()===resolved.toLowerCase()))return this.list();
    if(items.length>=30)throw Error('Можно добавить не более 30 приложений');
    items.push({id:'app-'+randomUUID(),name:path.basename(resolved,'.exe').slice(0,80),file:resolved});
    this.save(items);return this.list();
  }

  remove(id:string) {
    this.save(this.custom().filter(item=>item.id!==id));return this.list();
  }

  async open(id:string) {
    if(id==='browser'){await this.browse();return {ok:true,name:'Браузер'};}
    const selected=this.catalog().find(item=>item.id===id);
    if(!selected)throw Error('Приложение не разрешено или удалено. Используйте list_applications.');
    await this.launch(selected.file);
    return {ok:true,name:selected.name,note:'Приложение запущено. Управление его окнами не выполнялось.'};
  }
}
