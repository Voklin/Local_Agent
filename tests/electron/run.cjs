const {spawn}=require('node:child_process'),path=require('node:path');
const env={...process.env};delete env.ELECTRON_RUN_AS_NODE;
const child=spawn(require('electron'),[path.resolve(__dirname,process.argv[2]||'studio-smoke.cjs'),...(String(process.argv[2]).includes('neutral-ide')?[]:['--legacy-ide'])],{cwd:path.resolve(__dirname,'../..'),env,stdio:'inherit',windowsHide:true});
child.on('exit',(code,signal)=>{process.exitCode=signal||!Number.isInteger(code)?1:code;});child.on('error',error=>{console.error(error);process.exitCode=1;});
