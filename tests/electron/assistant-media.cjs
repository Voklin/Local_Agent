// Validate host inputs without opening a browser or playing audio.
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const ts=require('typescript');
const root=path.resolve(__dirname,'../..');
const parent=path.join(root,'.test-tmp');fs.mkdirSync(parent,{recursive:true});
const directory=fs.mkdtempSync(path.join(parent,'assistant-media-'));
const compiled=path.join(directory,'assistantMedia.cjs');
fs.writeFileSync(compiled,ts.transpileModule(fs.readFileSync(path.join(root,'apps/desktop/electron/assistantMedia.ts'),'utf8'),
  {compilerOptions:{module:ts.ModuleKind.CommonJS,target:ts.ScriptTarget.ES2022,esModuleInterop:true}}).outputText);
const {validateMusicURL,validateAudioPath}=require(compiled);
for(const url of ['https://music.yandex.ru/album/123','https://youtu.be/abc','https://open.spotify.com/track/xyz'])assert.equal(validateMusicURL(url),url);
for(const url of ['http://youtube.com/','https://youtube.com.evil.test/','https://youtube.com@evil.test/','https://user:password@youtube.com/','https://youtube.com:8888/','file:///C:/Windows/cmd.exe','https://127.0.0.1/','javascript:alert(1)'])assert.throws(()=>validateMusicURL(url));
const allowed=path.join(directory,'music');fs.mkdirSync(allowed);
const track=path.join(allowed,'track.MP3');fs.writeFileSync(track,'fixture');
assert.equal(validateAudioPath(track,[allowed]),fs.realpathSync(track));
const outside=path.join(directory,'outside.mp3');fs.writeFileSync(outside,'fixture');
const script=path.join(allowed,'script.cmd');fs.writeFileSync(script,'fixture');
for(const [file,roots] of [[outside,[allowed]],[script,[allowed]],[track,[]],['relative.mp3',[allowed]],[track,'not-an-array']])assert.throws(()=>validateAudioPath(file,roots));
const link=path.join(allowed,'outside');fs.symlinkSync(directory,link,'junction');
assert.throws(()=>validateAudioPath(path.join(link,'outside.mp3'),[allowed]));
console.log('PASS: music URL host/protocol/auth/port boundaries; audio extension, realpath and prompt-root containment');
