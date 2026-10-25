/** Presentation-only cleanup also keeps streamed Lola fragments readable. */
export function plainVoiceText(text:string) {
  return text.replace(/<(think|analysis)>[\s\S]*?<\/\1>/gi,'')
    .replace(/```[^\n]*\n[\s\S]*?(?:```|$)/g,'Код доступен в основном чате.')
    .replace(/!?\[([^\]]+)\]\([^\n)]*\)/g,'$1').replace(/<[^>\n]+>/g,'')
    .replace(/^\s*(?:#{1,6}\s+|>\s*|[-+*•]\s+|\d+[.)]\s+)/gm,'')
    .replace(/(\d)\s*\*\s*(\d)/g,'$1 умножить на $2').replace(/\\?[*`~_]/g,'')
    .replace(/\n{3,}/g,'\n\n').trim();
}
