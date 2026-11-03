export function SourceContextPreview({text}:{text:string}) {
  let proposal:any;
  try{proposal=JSON.parse(text);}catch{return <pre>{text}</pre>;}
  if(proposal?.kind==='project_memory'&&typeof proposal.recipient==='string'&&Array.isArray(proposal.records))return <div className="source-context-preview"><dl><dt>Получатель</dt><dd>{proposal.recipient}</dd><dt>Модель</dt><dd>{proposal.model}</dd></dl><p>Записей памяти: {proposal.records.length}. Будут переданы только показанные данные.</p>{proposal.records.map((record:any,index:number)=><section key={index}><b>{record.kind} · {record.state}</b><p>{record.text}</p><small>{record.sources?.map((s:any)=>s.path).join(', ')}</small></section>)}<details><summary>Полный пакет памяти</summary><pre>{text}</pre></details></div>;
  if(typeof proposal?.recipient!=='string'||!Array.isArray(proposal.sources))return <pre>{text}</pre>;
  return <div className="source-context-preview">
    <dl><dt>Получатель</dt><dd className="source-context-recipient">{proposal.recipient}</dd><dt>Модель</dt><dd>{proposal.model}</dd></dl>
    <p>Файлов и фрагментов: {proposal.sources.length}. Содержимое показано полностью.</p>
    {proposal.sources.map((source:any,index:number)=><section key={index}><b>{source.path}:{source.start_line}–{source.end_line}</b><small>SHA-256: {source.sha256}</small><pre>{source.content}</pre></section>)}
    <details><summary>Полный пакет данных</summary><pre>{text}</pre></details>
  </div>;
}
