"""Launch real Extension Host tests against a disposable trusted fixture only."""
import json,os,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'.test-data/neutral-ide'


def main():
    ui='--ui' in sys.argv
    report=BASE/('ui-report.json' if ui else 'host-report.json')
    report.unlink(missing_ok=True)
    fixture=BASE/('fixture-'+str(int(time.time())));fixture.mkdir(parents=True)
    for name,text in {'snippet.jsx':'','ui.txt':'before\n','safe.txt':'original\n','other.txt':'second\n','main.ts':'export function greet(name: string) { return "Hello " + name; }\nconst value = greet("Neutral");\ngre\nconst broken: number = "text";\n','format.js':'const foo={bar:1,baz:2}\n','invalid.yaml':'key: [unterminated\n','debug.py':'value = 7\nother = 2\nresult = value + other\nprint(result)\n'}.items():(fixture/name).write_text(text,encoding='utf8')
    (fixture.parent/'outside.txt').write_text('outside',encoding='utf8')
    (fixture/'.vscode').mkdir();(fixture/'.vscode/settings.json').write_text(json.dumps({'git.openRepositoryInParentFolders':'never','git.autoRepositoryDetection':False,'files.autoSave':'off','editor.formatOnSave':False,'yaml.schemaStore.enable':False}),encoding='utf8')
    settings=BASE/'user-data/User/settings.json';settings.parent.mkdir(parents=True,exist_ok=True)
    settings.write_text(json.dumps({'workbench.colorTheme':'Neutral Studio','telemetry.telemetryLevel':'off','update.mode':'none','extensions.autoUpdate':'off','extensions.autoCheckUpdates':False,'workbench.startupEditor':'none','window.dialogStyle':'custom','security.workspace.trust.enabled':False}),encoding='utf8')
    env={**os.environ,'NEUTRAL_IDE_TEST_REPORT':str(report),'NEUTRAL_IDE_TEST_PYTHON':str(ROOT/'.venv-test/Scripts/python.exe')};env.pop('ELECTRON_RUN_AS_NODE',None)
    command=[str(ROOT/'artifacts/neutral-ide/runtime/NeutralIDE.exe'),'--user-data-dir',str(BASE/'user-data'),'--shared-data-dir',str(BASE/'shared-data'),'--extensions-dir',str(BASE/'extensions'),'--extensionDevelopmentPath='+str(ROOT/'artifacts/neutral-ide/runtime/resources/app/extensions/neutral-agent'),'--extensionTestsPath='+str(ROOT/'prototypes/neutral-ide/tests/host.cjs'),'--remote-debugging-port=0','--disable-gpu','--skip-welcome','--skip-release-notes','--disable-workspace-trust',str(fixture)]
    if ui:
        command=[arg for arg in command if not arg.startswith('--extensionTestsPath=')]
        command.insert(-1,'--extensionDevelopmentPath='+str(ROOT/'prototypes/neutral-ide/tests/ui-probe'))
        command=['node',str(ROOT/'prototypes/neutral-ide/tests/drive.cjs'),*command]
    start=time.monotonic()
    with (BASE/('ui.log' if ui else 'host.log')).open('w',encoding='utf8') as log:result=subprocess.run(command,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=300)
    print('exit',result.returncode,'seconds',round(time.monotonic()-start,2));print(report.read_text(encoding='utf8'))
    if result.returncode or json.loads(report.read_text(encoding='utf8'))['status']!='passed':raise SystemExit(result.returncode or 1)


if __name__=='__main__':main()
