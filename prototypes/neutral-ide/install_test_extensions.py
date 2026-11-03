"""Install pinned, MIT test extensions through Code-OSS CLI in an isolated test profile."""
import hashlib,json,os,subprocess,zipfile
from pathlib import Path
import httpx
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'.test-data/neutral-ide'


def main():
    BASE.mkdir(parents=True,exist_ok=True)
    registry=json.loads((ROOT/'prototypes/neutral-ide/extensions.lock.json').read_text())
    cache=ROOT/'build/neutral-ide/extensions';cache.mkdir(parents=True,exist_ok=True)
    runtime=ROOT/'artifacts/neutral-ide/runtime';exe=runtime/'NeutralIDE.exe'
    env={**os.environ,'ELECTRON_RUN_AS_NODE':'1'}
    command=[str(exe),str(runtime/'resources/app/out/cli.js'),'--user-data-dir',str(BASE/'user-data'),'--shared-data-dir',str(BASE/'shared-data'),'--extensions-dir',str(BASE/'extensions')]
    report=[]
    for item in registry:
        package=cache/(item['namespace']+'.'+item['name']+'-'+item['version']+'.vsix')
        if not package.exists():
            response=httpx.get(item['download'],follow_redirects=True,timeout=120);response.raise_for_status()
            if hashlib.sha256(response.content).hexdigest()!=item['sha256']:raise ValueError('Extension SHA mismatch')
            package.write_bytes(response.content)
        if hashlib.sha256(package.read_bytes()).hexdigest()!=item['sha256']:raise ValueError('Cached extension SHA mismatch')
        completed=subprocess.run([*command,'--install-extension',str(package)],env=env,capture_output=True,text=True,encoding='utf8',timeout=180)
        report.append({'id':item['namespace']+'.'+item['name'],'version':item['version'],'exit':completed.returncode,'stdout':completed.stdout,'stderr':completed.stderr})
        print(report[-1]['id'],completed.returncode,flush=True)
        if completed.returncode:raise RuntimeError(completed.stdout+completed.stderr)
    local=cache/'neutral-probe-0.1.0.vsix'
    manifest={'name':'probe','publisher':'neutral','version':'0.1.0','engines':{'vscode':'^1.100.0'},'main':'./extension.cjs','activationEvents':['onCommand:neutral.probe'],'contributes':{'commands':[{'command':'neutral.probe','title':'Neutral: Extension Host probe'}]}}
    with zipfile.ZipFile(local,'w') as z:
        z.writestr('extension/package.json',json.dumps(manifest))
        z.writestr('extension/extension.cjs',"const v=require('vscode');exports.activate=c=>{c.subscriptions.push(v.commands.registerCommand('neutral.probe',()=>({host:true,version:v.version})));};")
        z.writestr('[Content_Types].xml','<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="json" ContentType="application/json"/><Default Extension="cjs" ContentType="application/javascript"/><Default Extension="vsixmanifest" ContentType="text/xml"/></Types>')
        z.writestr('extension.vsixmanifest','<?xml version="1.0"?><PackageManifest Version="2.0.0" xmlns="http://schemas.microsoft.com/developer/vsx-schema/2011"><Metadata><Identity Language="en-US" Id="probe" Version="0.1.0" Publisher="neutral"/><DisplayName>Neutral Probe</DisplayName><Description xml:space="preserve">Isolated runtime probe</Description></Metadata><Installation><InstallationTarget Id="Microsoft.VisualStudio.Code"/></Installation><Dependencies/><Assets><Asset Type="Microsoft.VisualStudio.Code.Manifest" Path="extension/package.json" Addressable="true"/></Assets></PackageManifest>')
    completed=subprocess.run([*command,'--install-extension',str(local)],env=env,capture_output=True,text=True,encoding='utf8',timeout=120)
    report.append({'id':'neutral.probe','exit':completed.returncode,'stdout':completed.stdout,'stderr':completed.stderr})
    (BASE/'installation.json').write_text(json.dumps(report,indent=2),encoding='utf8')
    if completed.returncode:raise RuntimeError(completed.stdout+completed.stderr)
    print('Local VSIX installed')


if __name__=='__main__':main()
