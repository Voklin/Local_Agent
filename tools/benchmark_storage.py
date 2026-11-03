"""Measure migration/catalog/search against legacy corpus reads in a disposable profile."""
import argparse
import json
from pathlib import Path
import statistics
import sys
import tempfile
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from agent.storage import Storage, encode


def measure(operation, repetitions=12):
    """Return median and nearest-rank p95 in milliseconds, with warm caches explicit."""
    samples = []
    for _ in range(repetitions):
        started = time.perf_counter()
        operation()
        samples.append((time.perf_counter()-started)*1000)
    return {'p50_ms':round(statistics.median(samples),3),'p95_ms':round(sorted(samples)[int((len(samples)-1)*0.95+0.999)],3),'samples':len(samples)}


def benchmark(chats=2000, messages=25):
    """Build mixed Chat/IDE/voice JSON, copy-migrate, then compare equivalent lists."""
    with tempfile.TemporaryDirectory(prefix='neutral_storage_benchmark_') as directory:
        root = Path(directory)
        (root/'chats').mkdir()
        for index in range(chats):
            identity = f'{index:032x}'
            value = {'id':identity,'title':f'Задача {index}','mode':('chat','ide','voice')[index%3],
                'project_root':'','project_id':'','model':'benchmark','created_at':'2026','updated_at':f'{index:08d}',
                'messages':[{'role':'assistant' if i%2 else 'user','content':f'Разговор {index}, сообщение {i}. '+('Пример содержимого проекта. '*12)} for i in range(messages)]}
            value['messages'].append({'role':'tool','tool_call_id':'large','content':encode({'ok':True,'stdout':'Сохранённый вывод. '*1800})})
            (root/'chats'/(identity+'.json')).write_text(encode(value),encoding='utf-8')
        original_bytes = sum(p.stat().st_size for p in (root/'chats').glob('*.json'))
        started = time.perf_counter()
        database = Storage(root).ready()
        migration_seconds = time.perf_counter()-started
        def legacy_catalog():
            """Match the previous listing cost: decode every complete JSON transcript."""
            items = []
            for path in (root/'chats').glob('*.json'):
                value = json.loads(path.read_text(encoding='utf-8'))
                items.append({key:value.get(key) for key in ('id','title','updated_at','mode')})
            return sorted(items,key=lambda item:item['updated_at'],reverse=True)
        legacy = measure(legacy_catalog,6)
        indexed = measure(database.catalog)
        search = measure(lambda:database.search(f'Разговор {chats//2}, сообщение',root='',mode=('chat','ide','voice')[(chats//2)%3],project_id=''))
        report = database.report()
        return {'dataset':{'chats':chats,'messages':chats*(messages+1),'legacy_bytes':original_bytes},
            'migration_seconds':round(migration_seconds,3),'legacy_catalog':legacy,'indexed_catalog':indexed,
            'indexed_search':search,'search_backend':report['search_backend'],'integrity':report['integrity'],
            'database_bytes':database.path.stat().st_size,
            'artifact_bytes':sum(p.stat().st_size for p in database.artifacts.directory.glob('*/*.utf8')),
            'conditions':'Windows local temporary directory, warm filesystem cache; synthetic data, no model requests'}


def main():
    """Write reproducible machine-readable measurements without user history or secrets."""
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--chats',type=int,default=2000)
    parser.add_argument('--messages',type=int,default=25)
    parser.add_argument('--out',type=Path,default=Path('.test-data/stage5-storage-benchmark.json'))
    options=parser.parse_args()
    if not 1<=options.chats<=10000 or not 1<=options.messages<=100:
        parser.error('Use 1..10000 chats and 1..100 messages')
    result=benchmark(options.chats,options.messages)
    options.out.parent.mkdir(parents=True,exist_ok=True)
    options.out.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=True,indent=2))


if __name__=='__main__':
    main()
