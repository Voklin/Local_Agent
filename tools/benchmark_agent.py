"""Reproducible Agent baseline in owned synthetic projects; never edit user projects."""
import argparse
import ast
from copy import deepcopy
import hashlib
import json
import os
import re
from pathlib import Path
import statistics
import subprocess
import sys
import time
import uuid
import zipfile
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
SIZES={'small':40,'medium':1200,'large':12000}
FILES={
 'app/__init__.py':'',
 'app/totals.py':'def tax_total(subtotal):\n    """Return the total with tax."""\n    return subtotal * 1.1\n',
 'app/invoice.py':'from .totals import tax_total\n\ndef invoice_total(subtotal):\n    return tax_total(subtotal)\n',
 'README.md':'Synthetic Neutral benchmark. Edit app/ only. Filler modules are unrelated.\n',
 '.gitignore':'generated_ignored/\n',
 '.neutralignore':'private/\n',
 'private/.env':'SYNTHETIC_SECRET=fixture-only-not-a-real-key\n',
}
CASES={
 'definition':('Найди определение tax_total инструментами. Ответь в формате путь:строка. Не изменяй файлы.',['app/totals.py']),
 'references':('Найди вызов tax_total вне определения инструментами. Ответь в формате путь:строка. Не изменяй файлы.',['app/invoice.py']),
 'bugfix':('Исправь расчёт tax_total: налог должен составлять 20%, сейчас используется 10%. Измени только множитель в return, сохрани имя и структуру функции. Используй инструменты.',['app/totals.py']),
 'multifile':('Переименуй tax_total в grand_total в определении и во всех местах использования. Поведение и коэффициент не меняй. Используй инструменты.',['app/totals.py','app/invoice.py']),
 'recovery':('Исправь расчёт tax_total: налог должен составлять 20%, сейчас используется 10%. Измени только множитель в return, сохрани имя и структуру функции. Используй инструменты.',['app/totals.py']),
}


def encode(value):
    """Stable UTF-8 report representation without non-finite numbers."""
    return json.dumps(value,ensure_ascii=False,allow_nan=False,indent=2)+'\n'


def save_report(path,value):
    """Replace one owned report atomically, retaining progress between cases."""
    temporary=path.with_suffix('.pending');temporary.write_text(encode(value),encoding='utf-8');temporary.replace(path)


def case_outcome(case):
    """Keep task correctness separate from agent closure and a censored controlled experiment."""
    reason=str(case.get('stop_reason') or '').casefold()
    return {'task_correct':bool(case.get('validation',{}).get('passed') and case.get('diff_correct') and not case.get('failures')),
        'end_to_end_passed':case.get('passed') is True,'completion_observed':case.get('status')=='completed',
        'experiment_limit_reached':'лимит циклов' in reason or 'лимит времени' in reason}


def source_location_matches(answer,location):
    """Match an actual relative path and whole line number, not :1 inside :10 or a different path."""
    return bool(re.search(r'(?<![\w/\\.\-])'+re.escape(location)+r'(?!\d)',answer))


def write_summary(output,report):
    """Render a human-readable result without implying failed tasks passed or benchmarks are universal."""
    rows=['# Neutral: Agent baseline','',f"Модель: `{report['model']}` · протокол: `{report['protocol']}`",
        '',f"Состояние прогона: **{report['live_status']}**. Исходники: `{report['source']['source_digest']}`.",
        '', '| Проект | Сценарий | Задача / diff | E2E | Статус агента | POST | Вход / выход | Секунды |',
        '| --- | --- | --- | --- | --- | ---: | ---: | ---: |']
    for project in report['projects']:
        for case in project['cases']:
            usage=case['usage'];outcome=case_outcome(case);status=case['status']+(' · лимит эксперимента' if outcome['experiment_limit_reached'] else '')
            rows.append(f"| {project['size']} | {case['case']} | {'PASS' if outcome['task_correct'] else 'FAIL'} | {'PASS' if case['passed'] else 'FAIL'} | {status} | {case['http_attempts']} | {usage['input_tokens']} / {usage['output_tokens']} | {case['wall_seconds']} |")
    rows+=['','`completed` означает завершение агентского цикла, а не успешную независимую проверку задачи.',
        '', '| Проект | Filler-файлы | Recall@10 | Поиск p50 / p95, мс | Покрытие |',
        '| --- | ---: | ---: | ---: | --- |']
    for project in report['projects']:
        search=project['search'];coverage='частичное: '+search['reason'] if search['truncated'] else 'полный текущий обход'
        rows.append(f"| {project['size']} | {project['filler_files']} | {search['recall_at_10']} | {search['p50_ms']} / {search['p95_ms']} | {coverage} |")
    rows+=['','Ограничения:','',*[f'- {value}' for value in report['limitations']],
        '', 'Recovery здесь — Stop до approval и повторный запуск Engine с checkpoint. Это не проверка kill процесса или восстановления неизвестного эффекта.',
        '', 'Полные ответы, квитанции, загруженный профиль и параметры — в `report.json`. Снимок исходников — `baseline-sources.zip`.']
    (output/'report.md').write_text('\n'.join(rows)+'\n',encoding='utf-8')


def snapshot_sources(output):
    """Freeze existing Agent/Core sources and exact hashes before application changes."""
    names=sorted([p.relative_to(ROOT).as_posix() for group in ('agent','core/python') for p in (ROOT/group).rglob('*.py')])
    names+=['requirements-core.txt','requirements-build.txt','tools/benchmark_agent.py']
    hashes={}
    with zipfile.ZipFile(output/'baseline-sources.zip','x',zipfile.ZIP_DEFLATED) as archive:
        for name in names:
            raw=(ROOT/name).read_bytes();hashes[name]=hashlib.sha256(raw).hexdigest();archive.writestr(name,raw)
    revision=subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,capture_output=True,text=True,check=True).stdout.strip()
    return {'git_head':revision,'dirty_worktree':True,'files':hashes,'source_digest':hashlib.sha256(encode(hashes).encode()).hexdigest()}


def build_project(root,size):
    """Create deterministic owned fixture files with no dependency installation."""
    root.mkdir(parents=True,exist_ok=False)
    (root/'.neutral-benchmark.json').write_text(encode({'version':1,'size':size,'owned_files':list(FILES)}),encoding='utf-8')
    for name,text in FILES.items():
        path=root/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text,encoding='utf-8')
    for index in range(SIZES[size]):
        extension=('py','js','ts')[index%3];path=root/'modules'/f'bucket_{index//200:03d}'/f'module_{index:05d}.{extension}'
        path.parent.mkdir(parents=True,exist_ok=True)
        text=(f'def unrelated_{index}(value):\n    return value + {index}\n' if extension=='py' else
              f'export function unrelated_{index}(value{": number" if extension=="ts" else ""}) {{ return value + {index}; }}\n')
        path.write_text(text,encoding='utf-8')


def reset_project(root):
    """Restore only known files in a benchmark-owned root, never recursively delete paths."""
    marker=json.loads((root/'.neutral-benchmark.json').read_text(encoding='utf-8'))
    if marker.get('version')!=1 or marker.get('owned_files')!=list(FILES):raise ValueError('Not an owned benchmark fixture')
    for name,text in FILES.items():
        path=root/name
        if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):raise ValueError('Fixture path changed')
        path.write_text(text,encoding='utf-8')


def search_measurement(root,repetitions=9):
    """Measure existing lexical search; distinguish top-k recall from full corpus coverage."""
    from agent.workspace_search import search_project
    samples=[];last=None
    for _ in range(repetitions):
        started=time.perf_counter();last=search_project(root,{'query':'tax_total','limit':50})
        samples.append((time.perf_counter()-started)*1000)
    paths=list(dict.fromkeys(item['path'] for item in last['matches']))
    expected=['app/totals.py','app/invoice.py']
    return {'query':'tax_total','top_k':10,'expected_paths':expected,'returned_paths':paths,
        'recall_at_10':sum(path in paths[:10] for path in expected)/len(expected),
        'p50_ms':round(statistics.median(samples),3),'p95_ms':round(sorted(samples)[-1],3),
        'samples':len(samples),'cache':'warm filesystem cache','truncated':last['truncated'],
        'reason':last['reason'],'scanned_files':last['scanned_files']}


def fixture_validation(root,case):
    """Validate a held-out pure-arithmetic contract without executing arbitrary model code."""
    totals=(root/'app/totals.py').read_text(encoding='utf-8');invoice=(root/'app/invoice.py').read_text(encoding='utf-8')
    name='grand_total' if case=='multifile' else 'tax_total';coefficient=1.2 if case in ('bugfix','recovery') else 1.1
    try:
        tree=ast.parse(totals);caller=ast.parse(invoice)
        if len(tree.body)!=1 or not isinstance(tree.body[0],ast.FunctionDef):raise ValueError('Expected one pure function')
        function=tree.body[0]
        args=function.args
        if function.name!=name or function.decorator_list or [a.arg for a in args.args]!=['subtotal'] or args.posonlyargs or args.kwonlyargs or args.defaults or args.vararg or args.kwarg or function.returns or any(a.annotation for a in args.args):raise ValueError('Function contract changed')
        expressions=[n for n in function.body if not isinstance(n,ast.Expr) or not isinstance(n.value,ast.Constant) or not isinstance(n.value.value,str)]
        if len(expressions)!=1 or not isinstance(expressions[0],ast.Return):raise ValueError('Expected one arithmetic return')
        value=expressions[0].value
        if not isinstance(value,ast.BinOp) or not isinstance(value.op,ast.Mult) or not isinstance(value.left,ast.Name) or value.left.id!='subtotal' or not isinstance(value.right,ast.Constant) or type(value.right.value) not in (int,float):raise ValueError('Only subtotal * coefficient is supported')
        if abs(value.right.value-coefficient)>1e-9:raise ValueError('Wrong coefficient')
        if case=='multifile':
            if len(caller.body)!=2 or not isinstance(caller.body[0],ast.ImportFrom) or not isinstance(caller.body[1],ast.FunctionDef):raise ValueError('Unexpected caller module statements')
            imported=next((n for n in caller.body if isinstance(n,ast.ImportFrom)),None)
            if not imported or imported.module!='totals' or imported.level!=1 or [(a.name,a.asname) for a in imported.names]!=[(name,None)]:raise ValueError('Caller import not renamed')
            method=next((n for n in caller.body if isinstance(n,ast.FunctionDef)),None)
            if method.name!='invoice_total' or method.decorator_list or [a.arg for a in method.args.args]!=['subtotal'] or method.args.defaults or method.args.kwonlyargs or method.args.posonlyargs or method.args.vararg or method.args.kwarg:raise ValueError('Caller signature changed')
            returned=method.body[0].value if method and len(method.body)==1 and isinstance(method.body[0],ast.Return) else None
            if not isinstance(returned,ast.Call) or not isinstance(returned.func,ast.Name) or returned.func.id!=name or len(returned.args)!=1 or returned.keywords or not isinstance(returned.args[0],ast.Name) or returned.args[0].id!='subtotal':raise ValueError('Caller not renamed')
        # Execute only the constructed, validated arithmetic AST, never an import from the fixture.
        expression=ast.Expression(value);program=compile(ast.fix_missing_locations(expression),'<validated-fixture>','eval')
        for subtotal in (0,100,-10):
            actual=eval(program,{'__builtins__':{}},{'subtotal':subtotal})
            if abs(actual-subtotal*coefficient)>1e-8:raise ValueError('Arithmetic check failed')
        return {'passed':True,'checks':3,'method':'held-out AST contract + restricted arithmetic evaluation'}
    except (ValueError,SyntaxError,TypeError,AttributeError) as error:return {'passed':False,'error':str(error),'checks':0}


def model_metadata(base_url,model):
    """Read loaded model metadata only; refuse a baseline that would silently trigger a JIT load."""
    import urllib.request
    base=base_url.rstrip('/').removesuffix('/v1')
    with urllib.request.urlopen(base+'/api/v1/models',timeout=3) as response:data=json.load(response)
    for entry in data.get('models',[]):
        for instance in entry.get('loaded_instances',[]):
            if instance.get('id')==model:return {'key':entry.get('key'),'quantization':entry.get('quantization'),
                'size_bytes':entry.get('size_bytes'),'instance':instance}
    raise ValueError('Load the selected model first; this benchmark never loads a model')


def resource_sample():
    """Read whole-device VRAM; unavailable telemetry remains null rather than invented."""
    try:
        process=subprocess.run(['nvidia-smi','--query-gpu=name,memory.total,memory.used','--format=csv,noheader,nounits'],capture_output=True,text=True,timeout=3)
        if process.returncode:return None
        name,total,used=process.stdout.strip().splitlines()[0].split(',')
        return {'gpu':name.strip(),'total_mib':int(total),'used_mib':int(used),'scope':'whole device, not isolated model peak'}
    except (OSError,ValueError,subprocess.TimeoutExpired):return None


def run_case(root,case,connection,profile):
    """Exercise the existing Engine/JSON/approval/journal pipeline, serially and within fixtures."""
    from agent import engine as module
    from agent.model_client import ModelClient
    from agent.tools import TOOL_DEFINITIONS
    reset_project(root);prompt,expected=CASES[case];initial={name:(root/name).read_bytes() for name in FILES}
    transcript=[];failures=[];http_attempts=[];clients=[];approvals=[];did_interrupt=False;context_evidence=[]
    class MeasuredClient(ModelClient):
        """Count physical inference POST attempts, including retries and auxiliary generations."""
        def __init__(self,*args,**kwargs):
            super().__init__(*args,**kwargs);clients.append(self)
            async def request_hook(request):
                """Count inference attempts without recording headers or secrets."""
                if request.method=='POST' and request.url.path.endswith(('/chat/completions','/responses')):
                    http_attempts.append({'path':request.url.path})
                    # Physical HTTP projection, never merely a builder preview.
                    context_evidence.extend(deepcopy(getattr(self,'context_pack_summary',{}).get('sources',[])))
            self.client._client.event_hooks.setdefault('request',[]).append(request_hook)
        def create(self,**params):
            """Fix generation seed for a reproducible controlled baseline."""
            return super().create(**{**params,'seed':0})
    definitions=[deepcopy(d) for d in TOOL_DEFINITIONS if d['function']['name'] in ('list_files','read_file','read_range','search_text','write_file','patch_file')]
    settings={'budget_mode':connection.get('budget_mode','manual'),'context_window':8192,'context_reserve_tokens':256,'max_tokens':1536,
        'temperature':0,'top_p':1,'max_agent_turns':10,'max_runtime_minutes':3,'request_timeout':90,'memory_updates':'off'}
    identity=uuid.uuid4().hex;history=[];first=None
    def execute(interrupt=False):
        """Run one isolated generation sequence; approvals are limited to the known fixture sources."""
        nonlocal did_interrupt,history
        from agent.context_builder import ContextBuilder
        agent=module.AgentEngine(connection['base_url'],'',connection['model'],str(root),prompt,
            settings=settings,task_id=identity,history=history,auto_memory=False,managed_extensions=True,
            context_builder=ContextBuilder(root) if connection.get('context_pack',False) else False,
            tool_protocol=connection['tool_protocol'],tool_definitions=definitions,
            task_options={'read_only':case in ('definition','references')})
        agent.failed.connect(failures.append)
        agent.conversation_updated.connect(lambda messages:transcript.append(deepcopy(messages)))
        def approve(path,diff,exists):
            """Consent only to edits of this fixture's two arithmetic source files."""
            nonlocal did_interrupt
            candidate=Path(path);candidate=candidate if candidate.is_absolute() else root/candidate
            relative=candidate.resolve().relative_to(root.resolve()).as_posix()
            approvals.append({'path':relative,'interrupted':interrupt})
            if interrupt:
                did_interrupt=True;agent.requestInterruption();return
            allowed=relative in {'app/totals.py','app/invoice.py'}
            agent.resolve_write_approval('apply' if allowed else 'reject')
        agent.write_approval_requested.connect(approve)
        agent.run();history=deepcopy(agent._messages[1:]);return agent
    started=time.perf_counter();before_resource=resource_sample()
    with patch.object(module,'ModelClient',MeasuredClient):
        if case=='recovery':
            first=execute(True)
            interrupted_unchanged=all((root/name).read_bytes()==value for name,value in initial.items())
            agent=execute() if did_interrupt and interrupted_unchanged else first
        else:agent=execute();interrupted_unchanged=None
    elapsed=time.perf_counter()-started
    changed=[name for name in FILES if (root/name).read_bytes()!=initial[name]]
    messages=transcript[-1] if transcript else []
    answer=next((str(m.get('content','')) for m in reversed(messages) if m.get('role')=='assistant' and not m.get('tool_calls')),'')
    inspected={source['path'] for source in context_evidence}
    for message in messages:
        if message.get('role')!='tool':continue
        try:receipt=json.loads(message.get('content',''))
        except (ValueError,TypeError):continue
        if not isinstance(receipt,dict) or receipt.get('ok') is not True:continue
        if isinstance(receipt.get('path'),str):inspected.add(receipt['path'])
        inspected.update(item['path'] for item in receipt.get('matches',[]) if isinstance(item,dict) and isinstance(item.get('path'),str))
    location='app/totals.py:1' if case=='definition' else 'app/invoice.py:4'
    check=({'passed':source_location_matches(answer,location) and set(expected)<=inspected and not changed,'method':'exact source location, successful tool provenance, no writes'}
        if case in ('definition','references') else fixture_validation(root,case))
    diff_correct=set(changed)==set(expected) if case not in ('definition','references') else not changed
    if case=='recovery':diff_correct=diff_correct and did_interrupt and interrupted_unchanged and first.task_snapshot()['status']=='paused'
    usage={'input_tokens':0,'output_tokens':0,'requests_reported':0}
    for client in clients:
        for key in usage:usage[key]+=client.usage_totals[key]
    snapshot=agent.task_snapshot()
    return {'case':case,'passed':bool(check['passed'] and diff_correct and not failures and snapshot['status']=='completed'),
        'validation':check,'diff_correct':diff_correct,'changed_files':changed,'expected_paths':expected,
        'status':snapshot['status'],'stop_reason':snapshot.get('stop_reason'),'failures':failures,
        'wall_seconds':round(elapsed,3),'http_attempts':len(http_attempts),'usage':usage,
        'json_repairs':sum(getattr(client,'json_repair_count',0) for client in clients),
        'tool_calls':snapshot.get('tool_calls'),'verification':snapshot.get('verification'),'inspected_paths':sorted(inspected),'approvals':approvals,'interruption_exercised':did_interrupt,
        'interrupted_files_unchanged':interrupted_unchanged,'generation_settings':settings,'seed':0,
        'resource_before':before_resource,'resource_after':resource_sample(),'answer':answer[-8000:],
        'transcript':messages,'profile':str(profile),'context_evidence':context_evidence,'context_pack':connection.get('context_pack',False)}


def run_benchmark(output,base_url,model,protocol,sizes,cases,live,context_pack=False,indexed=False,budget_mode='manual'):
    """Persist a baseline incrementally, with explicit live-model versus deterministic coverage."""
    if budget_mode not in ('manual','auto'):raise ValueError('Invalid benchmark budget mode')
    output=output.resolve();output.mkdir(parents=True,exist_ok=False)
    os.environ['LOCALAPPDATA']=str(output/'profile')
    report={'version':1,'kind':'ContextPack comparison' if context_pack else 'Agent control baseline','context_pack':context_pack,'indexed':indexed,'protocol':protocol,'model':model,'base_url':base_url,'budget_mode':budget_mode,
        'created_utc':__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),
        'source':snapshot_sources(output),'projects':[],'live_requested':live,'live_status':'running' if live else 'pending',
        'limitations':['Synthetic repositories; not a quality claim for arbitrary real projects.',
            'One trial per case; wall-time percentiles require repeated runs.',
            'Recovery: cancellation before approval and Engine recreation; process-kill/unknown-effect LLM scenarios are not covered.',
            'VRAM samples describe the whole device, not an isolated peak; CPU/RAM profiling is pending.']}
    save_report(output/'report.json',report)
    if live:report['loaded_model']=model_metadata(base_url,model)
    for size in sizes:
        root=output/'projects'/size;build_project(root,size)
        project={'size':size,'filler_files':SIZES[size],'fixture_files':len(FILES)+1,'search':search_measurement(root),'cases':[]}
        report['projects'].append(project);save_report(output/'report.json',report)
        if indexed:
            from agent.project_index import get_index
            index=get_index(root,create=True);deadline=time.monotonic()+600
            while index.state!='ready' and time.monotonic()<deadline:time.sleep(.05)
            if index.state!='ready':raise RuntimeError('Benchmark index unavailable: '+str(index.status()))
        print(encode({'phase':'search_baseline','size':size,**project['search']}),flush=True)
        if live:
            for case in cases:
                model_metadata(base_url,model)
                print(encode({'phase':'model_case_started','size':size,'case':case}),flush=True)
                result=run_case(root,case,{'base_url':base_url,'model':model,'tool_protocol':protocol,'context_pack':context_pack,'budget_mode':budget_mode},output/'profile')
                project['cases'].append(result);save_report(output/'report.json',report)
                print(encode({'phase':'model_case_finished','size':size,**{k:v for k,v in result.items() if k not in ('transcript','answer','profile','generation_settings')}}),flush=True)
        if indexed:
            from agent.project_index import close_indexes
            close_indexes()
    report['live_status']='completed' if live else 'pending'
    completed=[case for project in report['projects'] for case in project['cases']]
    report['summary']={'passed':sum(case['passed'] for case in completed),'total':len(completed),
        'task_correct':sum(case_outcome(case)['task_correct'] for case in completed),
        'experiment_limits_reached':sum(case_outcome(case)['experiment_limit_reached'] for case in completed),
        'http_attempts':sum(case['http_attempts'] for case in completed),'wall_seconds':round(sum(case['wall_seconds'] for case in completed),3)}
    save_report(output/'report.json',report);write_summary(output,report);return report


def main():
    """Create a fresh report directory; model execution is explicitly opt-in."""
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--base-url',default='http://127.0.0.1:1234/v1')
    parser.add_argument('--model',default='neutral-baseline-ornith-9b')
    parser.add_argument('--protocol',choices=['native','json'],default='json')
    parser.add_argument('--sizes',nargs='+',choices=list(SIZES),default=list(SIZES))
    parser.add_argument('--cases',nargs='+',choices=list(CASES),default=list(CASES))
    parser.add_argument('--live',action='store_true')
    parser.add_argument('--context-pack',action='store_true')
    parser.add_argument('--indexed',action='store_true')
    parser.add_argument('--budget-mode',choices=['manual','auto'],default='manual')
    options=parser.parse_args()
    report=run_benchmark(options.out,options.base_url,options.model,options.protocol,options.sizes,options.cases,options.live,options.context_pack,options.indexed,options.budget_mode)
    print(encode(report['summary']))


if __name__=='__main__':main()
