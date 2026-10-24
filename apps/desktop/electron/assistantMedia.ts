import fs from 'node:fs';
import path from 'node:path';

export function validateMusicURL(value:unknown) {
  if(typeof value!=='string'||value.length>2000)throw Error('Некорректная ссылка');
  const url=new URL(value);
  const hosts=['www.youtube.com','youtube.com','youtu.be','music.youtube.com','music.yandex.ru','music.vk.com','open.spotify.com','soundcloud.com','www.soundcloud.com'];
  if(url.protocol!=='https:'||!hosts.includes(url.hostname)||url.username||url.password||(url.port&&url.port!=='443'))throw Error('Разрешена только HTTPS ссылка музыкального сервиса');
  return url.toString();
}

export function validateAudioPath(value:unknown,roots:unknown) {
  if(typeof value!=='string'||!path.isAbsolute(value)||!Array.isArray(roots))throw Error('Нужен локальный аудиофайл');
  const file=fs.realpathSync(value);
  if(file.startsWith('\\\\')||!['.mp3','.wav','.flac','.ogg','.m4a','.aac','.wma','.opus'].includes(path.extname(file).toLowerCase())||!fs.statSync(file).isFile())throw Error('Формат аудио не разрешён');
  const allowed=roots.some(root=>{if(typeof root!=='string'||!path.isAbsolute(root))return false;const relative=path.relative(fs.realpathSync(root),file);return !!relative&&relative!=='..'&&!relative.startsWith('..'+path.sep)&&!path.isAbsolute(relative);});
  if(!allowed)throw Error('Аудиофайл вне разрешённых папок');
  return file;
}
