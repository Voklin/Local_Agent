import { useEffect, useState } from 'react';

export const ideRoles=[{id:'conductor',title:'Дирижёр',hint:'План и архитектура'},{id:'coder',title:'Автор кода',hint:'Полный код для передачи'},{id:'builder',title:'Сборщик проекта',hint:'Файлы через подтверждение diff'},{id:'reviewer',title:'Проверяющий',hint:'Чтение результата и проверка'}] as const;

export function IDEWorkflowSettings({busy,primary}:{busy:boolean;primary:{base_url:string;model:string}}) {
  const [draft,setDraft]=useState<any>(null);
  const [models,setModels]=useState<Record<string,string[]>>({});
  const [operation,setOperation]=useState('');const [notice,setNotice]=useState('');
  useEffect(()=>{let alive=true;void window.lca.getIDEWorkflow().then(result=>{if(alive){if(result.ok)setDraft(result);else setNotice(result.error);}}).catch(error=>{if(alive)setNotice(String(error));});return()=>{alive=false;};},[]);
  const locked=busy||!!operation;
  function changeRole(role:string,patch:any) {setDraft((current:any)=>({...current,roles:{...current.roles,[role]:{...current.roles[role],...patch}}}));}
  async function discover(role:string) {
    setOperation(role);setNotice('');
    try{const workflow={...draft,roles:{...draft.roles,[role]:{...draft.roles[role],base_url:draft.roles[role].base_url||primary.base_url}}};const result=await window.lca.listIDEModels({role,workflow});if(!result.ok)throw Error(result.error);setModels(current=>({...current,[role]:result.models}));setNotice(`Найдено моделей: ${result.models.length}`);}
    catch(error){setNotice(String(error));}finally{setOperation('');}
  }
  async function save() {
    setOperation('save');setNotice('');
    try{const result=await window.lca.configureIDEWorkflow(draft);if(!result.ok)throw Error(result.error);setDraft(result);window.dispatchEvent(new Event('ide-workflow-changed'));setNotice('Роли IDE сохранены. Ключи остаются только в памяти.');}
    catch(error){setNotice(String(error));}finally{setOperation('');}
  }
  return <section className="settings-section ide-workflow-settings"><h3>Команда IDE</h3><p className="settings-help">Четыре последовательные роли. Только сборщик меняет файлы, каждый diff подтверждаете вы. Дизайн проекта сохраняется.</p>
    {!draft?<p role="status">{notice||'Загрузка настроек…'}</p>:<>
    <label className="appearance-toggle"><input aria-label="Включить роли IDE" type="checkbox" checked={draft.enabled} disabled={locked} onChange={event=>setDraft({...draft,enabled:event.target.checked})}/>Использовать роли в IDE</label>
    <label>Запуск<select aria-label="Режим ролей IDE" value={draft.mode} disabled={locked} onChange={event=>setDraft({...draft,mode:event.target.value})}><option value="pipeline">Полный цикл · 4 роли</option>{ideRoles.map(role=><option key={role.id} value={role.id}>{role.title}</option>)}</select></label>
    <div className="ide-workflow-options"><label>Контекст моделей<select aria-label="Контекст моделей ролей" value={draft.context_length} disabled={locked} onChange={event=>setDraft({...draft,context_length:Number(event.target.value)})}>{[2048,4096,8192,16384,32768].map(value=><option key={value} value={value}>{value.toLocaleString('ru')} токенов</option>)}</select></label><label>Циклы исправлений<select value={draft.repair_passes} disabled={locked} onChange={event=>setDraft({...draft,repair_passes:Number(event.target.value)})}>{[0,1,2].map(value=><option key={value} value={value}>{value}</option>)}</select></label></div>
    <p className="settings-help">LM Studio 0.4+ и Ollama: перед переключением выгружается предыдущая модель роли, после завершения — последняя. Модели вне назначенных ролей не выгружаются: при их наличии цикл попросит освободить память. Внешний API работает без управления загрузкой.</p>
    <button type="button" className="secondary-button" disabled={locked||!primary.model} onClick={()=>setDraft({...draft,roles:Object.fromEntries(ideRoles.map(role=>[role.id,{...draft.roles[role.id],base_url:primary.base_url,model:primary.model}]))})}>Основная модель для всех ролей</button>
    <div className="ide-role-grid">{ideRoles.map(role=><fieldset key={role.id}><legend>{role.title}</legend><p className="settings-help">{role.hint}</p>
      <label>Сервер<select aria-label={`Сервер: ${role.title}`} value={draft.roles[role.id].provider} disabled={locked} onChange={event=>changeRole(role.id,{provider:event.target.value})}><option value="lmstudio">LM Studio · автозагрузка</option><option value="ollama">Ollama · автозагрузка</option><option value="external">Внешний API · без управления памятью</option></select></label>
      <label>URL<input aria-label={`URL: ${role.title}`} maxLength={2000} value={draft.roles[role.id].base_url} placeholder={primary.base_url} disabled={locked} onChange={event=>changeRole(role.id,{base_url:event.target.value})}/></label>
      <label>Модель<input aria-label={`Модель: ${role.title}`} maxLength={300} list={`ide-models-${role.id}`} value={draft.roles[role.id].model} placeholder={primary.model||'Точный ID модели'} disabled={locked} onChange={event=>changeRole(role.id,{model:event.target.value})}/><datalist id={`ide-models-${role.id}`}>{(models[role.id]||[]).map(model=><option key={model} value={model}/>)}</datalist></label>
      <button type="button" className="secondary-button" disabled={locked} onClick={()=>void discover(role.id)}>{operation===role.id?'Получаю список…':'Список моделей'}</button>
      <label>Инструменты<select aria-label={`Протокол: ${role.title}`} value={draft.roles[role.id].tool_protocol} disabled={locked} onChange={event=>changeRole(role.id,{tool_protocol:event.target.value})}><option value="native">Native tools</option><option value="json">JSON · без native tools</option></select></label>
      <label>API-ключ роли<input aria-label={`Ключ: ${role.title}`} type="password" maxLength={4000} autoComplete="off" value={draft.roles[role.id].api_key??''} disabled={locked} placeholder="Новый ключ · только в памяти" onChange={event=>changeRole(role.id,{api_key:event.target.value})}/></label>
    </fieldset>)}</div>
    <p className="settings-help">Пустые URL/ID используют основную конфигурацию. Основной API-ключ наследуется только для того же URL. Контекст и бюджет ответа основной модели должны вмещать передаваемый код; при превышении код не обрезается — цикл останавливается с пояснением.</p>
    <button type="button" className="primary-button save-ide-workflow" disabled={locked} onClick={()=>void save()}>{operation==='save'?'Сохраняю…':'Сохранить роли IDE'}</button><p role="status">{notice}</p>
    {operation&&operation!=='save'&&<button type="button" className="secondary-button" onClick={()=>void window.lca.cancelModelSetup()}>Отменить список моделей</button>}
    </>}
  </section>;
}

export function IDEWorkflowBar({workflow,busy,onConfigure}:{workflow:any;busy:boolean;onConfigure:()=>void}) {
  const [notice,setNotice]=useState('');const [working,setWorking]=useState(false);
  async function select(mode:string) {
    setWorking(true);setNotice('');
    try{const result=await window.lca.configureIDEWorkflow({...workflow,enabled:mode!=='single',mode:mode==='single'?workflow.mode:mode});if(!result.ok)throw Error(result.error);window.dispatchEvent(new Event('ide-workflow-changed'));}
    catch(error){setNotice(String(error));}finally{setWorking(false);}
  }
  return <div className="ide-workflow-bar"><label>Режим IDE<select aria-label="Режим IDE" value={workflow.enabled?workflow.mode:'single'} disabled={busy||working} onChange={event=>void select(event.target.value)}><option value="single">Одна модель</option><option value="pipeline">Дирижёр · полный цикл</option>{ideRoles.map(role=><option key={role.id} value={role.id}>{role.title}</option>)}</select></label><button type="button" className="secondary-button" disabled={busy} onClick={onConfigure}>Роли IDE</button>{notice&&<span role="status">{notice}</span>}</div>;
}
