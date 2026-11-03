export const leshyThemes = [
 {id:'forest',label:'Лесная',scheme:'dark'},
 {id:'parchment',label:'Парчовая',scheme:'light'},
 {id:'twilight',label:'Сумеречная',scheme:'dark'},
] as const;
export type LeshyTheme = typeof leshyThemes[number]['id'];
export function normalizeTheme(value:unknown):LeshyTheme {
 return value==='light'?'parchment':leshyThemes.some(t=>t.id===value)?value as LeshyTheme:'forest';
}
export function applyTheme(theme:LeshyTheme,art=true){
 document.documentElement.dataset.leshyTheme=theme;
 document.documentElement.dataset.backgroundArt=String(art);
 document.documentElement.style.colorScheme=theme==='parchment'?'light':'dark';
}
