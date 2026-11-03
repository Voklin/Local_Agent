"""Finish dataset generation, bounded fine-tuning, ONNX export and CPU QA locally."""
import argparse
import json
import msvcrt
import os
from pathlib import Path
import subprocess
import sys
import time
import traceback


def save_state(path, **values):
    """Atomically publish stage/progress without reporting a model ready prematurely."""
    state=json.loads(path.read_text(encoding='utf8')) if path.exists() else {}
    state.update(values,worker_pid=os.getpid(),updated_unix=time.time())
    temporary=path.with_suffix('.tmp')
    temporary.write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding='utf8')
    temporary.replace(path)


def run(command, log_path):
    """Run one dependent stage, retaining its exact command and full local log."""
    print(json.dumps(command,ensure_ascii=False),flush=True)
    with log_path.open('w',encoding='utf8') as log:
        process=subprocess.Popen(command,stdout=log,stderr=subprocess.STDOUT,env={**os.environ,'PYTHONIOENCODING':'utf-8','PYTHONUTF8':'1'})
        print('Child PID:',process.pid,'Log:',log_path,flush=True)
        return process.wait()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dataset',type=Path,required=True)
    parser.add_argument('--generator-pid',type=int)
    args=parser.parse_args()
    import psutil
    root=Path(__file__).resolve().parents[3]
    dataset=args.dataset.resolve();dataset.mkdir(parents=True,exist_ok=True)
    state_path=dataset/'pipeline-state.json'
    with (dataset/'pipeline.lock').open('a+b') as lock:
        lock.seek(0);lock.write(b'0');lock.flush();lock.seek(0)
        msvcrt.locking(lock.fileno(),msvcrt.LK_NBLCK,1)
        try:
            if args.generator_pid and psutil.pid_exists(args.generator_pid):
                save_state(state_path,stage='generating',generator_pid=args.generator_pid)
                psutil.Process(args.generator_pid).wait()
            status=json.loads((dataset/'status.json').read_text(encoding='utf8'))
            if status['generated']<320 or status['accepted']<200:
                raise RuntimeError(f'Corpus incomplete or quality too low: {status}')
            resume=None
            for steps in [6000,12000]:
                save_state(state_path,stage='training',target_steps=steps,dataset_status=status)
                command=[sys.executable,str(Path(__file__).with_name('run_training.py')),
                         '--dataset',str(dataset),'--steps',str(steps)]
                if resume:command+=['--resume',str(resume)]
                if run(command,dataset/f'training-{steps}.log'):
                    raise RuntimeError(f'Training failed at target {steps}; see training log')
                checkpoints=sorted((dataset/'training').rglob('last.ckpt'),key=lambda p:p.stat().st_mtime)
                final_checkpoint=dataset/'training/final.ckpt'
                if not checkpoints and not final_checkpoint.exists():raise RuntimeError('Training produced no checkpoint')
                resume=final_checkpoint if final_checkpoint.exists() else checkpoints[-1]
                save_state(state_path,stage='exporting',checkpoint=str(resume))
                code=run([sys.executable,str(Path(__file__).with_name('export_and_evaluate.py')),
                          '--dataset',str(dataset),'--checkpoint',str(resume)],dataset/f'export-{steps}.log')
                report_path=dataset/'export/evaluation.json'
                if code==0 and report_path.exists():
                    report=json.loads(report_path.read_text(encoding='utf8'))
                    if report.get('asr_passed'):
                        save_state(state_path,stage='trial_ready',evaluation=report,
                                   note='CPU/STT checks passed; timbre requires user listening.')
                        return
                # An exporter/dependency failure requires repair, not more training.
                if not report_path.exists():raise RuntimeError('Export failed before evaluation; see export log')
            save_state(state_path,stage='needs_review',note='ASR quality did not meet thresholds after 12000 steps.')
        except Exception as exc:
            save_state(state_path,stage='failed',error=f'{type(exc).__name__}: {exc}',traceback=traceback.format_exc())
            raise


if __name__=='__main__':main()
