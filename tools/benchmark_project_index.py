"""Measure stage 13a on the baseline's owned synthetic corpus, without an LLM."""
import argparse
import ctypes
import hashlib
import json
import os
from pathlib import Path
import statistics
import sys
import time
import zipfile

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from benchmark_agent import build_project,SIZES,save_report,snapshot_sources


def process_memory():
    """Read Windows process working set and lifetime peak; these are not isolated index metrics."""
    if os.name!='nt':return None
    from ctypes import wintypes
    class Counters(ctypes.Structure):
        """PROCESS_MEMORY_COUNTERS with pointer-width SIZE_T fields."""
        _fields_=[('cb',wintypes.DWORD),('PageFaultCount',wintypes.DWORD),*[(n,ctypes.c_size_t) for n in ('PeakWorkingSetSize','WorkingSetSize','QuotaPeakPagedPoolUsage','QuotaPagedPoolUsage','QuotaPeakNonPagedPoolUsage','QuotaNonPagedPoolUsage','PagefileUsage','PeakPagefileUsage')]]
    values=Counters();values.cb=ctypes.sizeof(values)
    kernel=ctypes.windll.kernel32;kernel.GetCurrentProcess.restype=wintypes.HANDLE
    measure=ctypes.windll.psapi.GetProcessMemoryInfo
    measure.argtypes=[wintypes.HANDLE,ctypes.POINTER(Counters),wintypes.DWORD];measure.restype=wintypes.BOOL
    if not measure(kernel.GetCurrentProcess(),ctypes.byref(values),values.cb):return None
    return {'working_set_bytes':values.WorkingSetSize,'process_lifetime_peak_bytes':values.PeakWorkingSetSize}


def wait_ready(index,seconds=60):
    """Wait while the scan makes progress; failed/partial/stalled states never pass."""
    deadline=time.monotonic()+seconds;observed=(index.revision,index.file_count)
    while time.monotonic()<deadline:
        if index.state=='ready':return
        if index.state in ('needs_rebuild','degraded'):raise RuntimeError(str(index.status()))
        progress=(index.revision,index.file_count)
        if progress!=observed:observed=progress;deadline=time.monotonic()+seconds
        time.sleep(.02)
    raise TimeoutError('Index benchmark did not finish')


def benchmark(output):
    """Create new fixtures, measure warm retrieval, then observe one external edit per size."""
    output=output.resolve();output.mkdir(parents=True,exist_ok=False);os.environ['LOCALAPPDATA']=str(output/'profile')
    from agent.project_index import ProjectIndex
    source=snapshot_sources(output);source['index_benchmark_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    with zipfile.ZipFile(output/'baseline-sources.zip','a') as archive:archive.write(__file__,'tools/benchmark_project_index.py')
    report={'version':1,'source':source,'projects':[],'status':'running',
        'targets_before_measurement':{'warm_query_p95_ms':500,'recall_at_10':1,'external_update_ms':2000,'no_rescan_on_edit':True},
        'limitations':['Synthetic repositories; one cold build per size.','21 warm query trials; not a quality claim for arbitrary repositories.','CPU/RAM refer to the complete Python process, including lifetime peak.','No LLM generation; stage 10 agent reliability is not re-evaluated.']}
    save_report(output/'report.json',report)
    for size in SIZES:
        root=output/'projects'/size;build_project(root,size);memory_before=process_memory();cpu=time.process_time();started=time.perf_counter();index=ProjectIndex(root)
        try:
            wait_ready(index);build_seconds=time.perf_counter()-started;build_cpu=time.process_time()-cpu;trials=[];last=None
            for _ in range(21):
                started=time.perf_counter();last=index.query({'query':'tax_total','mode':'text','limit':10});trials.append((time.perf_counter()-started)*1000)
            symbols=index.query({'query':'tax_total','mode':'symbols','limit':10})
            scans=index.scan_count;started=time.perf_counter();path=root/'app/totals.py'
            path.write_text(path.read_text(encoding='utf-8').replace('tax_total','renamed_total'),encoding='utf-8');result=None
            while time.perf_counter()-started<10:
                result=index.query({'query':'renamed_total','mode':'symbols','limit':10})
                if result and any(h['path']=='app/totals.py' for h in result['matches']):break
                time.sleep(.01)
            item={'size':size,'filler_files':SIZES[size],'build_wall_seconds':round(build_seconds,3),'build_process_cpu_seconds':round(build_cpu,3),
                'p50_ms':round(statistics.median(trials),3),'p95_ms':round(sorted(trials)[19],3),'samples':len(trials),
                'recall_at_10':len({'app/totals.py','app/invoice.py'}&{h['path'] for h in last['matches']})/2,
                'definition_exact':any(h['path']=='app/totals.py' and h['start_line']==1 for h in symbols['matches']),
                'query_truncated':last['truncated'],'external_update_ms':round((time.perf_counter()-started)*1000,3),
                'update_observed':bool(result and any(h['path']=='app/totals.py' for h in result['matches'])),
                'incremental_without_rescan':index.scan_count==scans,'memory_before':memory_before,'memory_after':process_memory(),'index':index.status()}
            report['projects'].append(item);save_report(output/'report.json',report);print(json.dumps(item,ensure_ascii=False),flush=True)
        finally:index.close()
    report['status']='completed';save_report(output/'report.json',report)
    rows=['# Project Intelligence 13a: synthetic benchmark','','| Размер | Filler | Build, с | Search p50 / p95, мс | Recall@10 | Внешнее изменение, мс | Без rescan |','| --- | ---: | ---: | ---: | ---: | ---: | --- |']
    rows += [f"| {p['size']} | {p['filler_files']} | {p['build_wall_seconds']} | {p['p50_ms']} / {p['p95_ms']} | {p['recall_at_10']} | {p['external_update_ms']} | {p['incremental_without_rescan']} |" for p in report['projects']]
    rows += ['','Буквальный поиск и синтаксическое определение; не семантические references и не качество LLM.','',*[f'- {value}' for value in report['limitations']]]
    (output/'report.md').write_text('\n'.join(rows)+'\n',encoding='utf-8')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--out',type=Path,required=True);options=parser.parse_args()
    try:benchmark(options.out)
    except Exception as exc:
        report_path=options.out/'report.json'
        if report_path.exists():
            report=json.loads(report_path.read_text(encoding='utf-8'));report.update(status='failed',error=type(exc).__name__+': '+str(exc)[:300]);save_report(report_path,report)
        raise
