import { useMemo, useState } from 'react';

export type TextPart={code:boolean;text:string;language:string};
export function splitCodeBlocks(text:string):TextPart[] {
  const parts:TextPart[]=[];
  let lines:string[]=[],code=false,language='';
  function flush(){if(lines.length)parts.push({code,text:lines.join('\n'),language});lines=[];}
  for(const line of text.split('\n')) {
    const fence=/^\s*```([^`]*)$/.exec(line);
    if(fence&&(!code||!fence[1].trim())) {flush();code=!code;language=code?fence[1].trim().slice(0,40):'';}
    else lines.push(line);
  }
  flush();return parts;
}
export function ChatText({text}:{text:string}) {
  const parts=useMemo(()=>splitCodeBlocks(text),[text]);
  const [copied,setCopied]=useState(-1);
  const [error,setError]=useState('');
  async function copy(value:string,index:number) {
    try{await navigator.clipboard.writeText(value);setCopied(index);setError('');}
    catch{setError('Не удалось скопировать. Выделите текст вручную.');}
  }
  return <>{parts.map((part,index)=>part.code?<div className="chat-code" key={index}><div className="chat-code-heading"><span>{part.language||'Код'}</span><button type="button" onClick={()=>void copy(part.text,index)}>{copied===index?'Скопировано':'Копировать код'}</button></div><pre><code>{part.text}</code></pre></div>:<span className="chat-plain" key={index}>{part.text}</span>)}{error&&<small role="status">{error}</small>}</>;
}
