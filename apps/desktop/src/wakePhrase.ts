export function normalizeSpeech(text:string) {
  return text.toLocaleLowerCase('ru').replace(/ё/g,'е').replace(/[^\p{L}\p{N}]+/gu,' ').trim();
}

export function wakeCommand(text:string, phrase:string):string|null {
  const words=Array.from(text.matchAll(/[\p{L}\p{N}]+/gu));
  const wanted=normalizeSpeech(phrase).split(' ');
  if(!wanted[0]||words.length<wanted.length)return null;
  if(wanted.some((word,index)=>normalizeSpeech(words[index][0])!==word))return null;
  const last=words[wanted.length-1];
  return text.slice(last.index!+last[0].length).replace(/^[\s,!.:;—-]+/,'').trim();
}
