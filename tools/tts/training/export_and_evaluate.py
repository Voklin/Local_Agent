"""Export a trained checkpoint and exercise the CPU model on held-out Russian text."""
import argparse
from difflib import SequenceMatcher
from functools import partial
import io
import json
import os
from pathlib import Path
import shutil
import sys
import time
from unittest.mock import patch
import wave

EVALUATION_TEXTS=[
    'Привет! Я Мия. Рада тебя видеть. Чем я могу помочь?',
    'На столе лежат семь карандашей и три тетради.',
    'Открыть браузер сейчас или сначала сохранить документ?',
    'Дождь закончился, и над лесом появилась яркая радуга.',
]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--checkpoint',type=Path,required=True)
    parser.add_argument('--dataset',type=Path,required=True)
    args=parser.parse_args()
    import httpx
    import onnx
    import torch
    from piper import PiperVoice
    from piper.train import export_onnx
    root=Path(__file__).resolve().parents[3]
    sys.path.insert(0,str(Path(__file__).parent))
    from generate_serena import normalize
    output=args.dataset.resolve()/'export';output.mkdir(exist_ok=True)
    model_path=output/'ru_RU-miya-serena-medium.onnx'
    torch.set_num_threads(4)
    sys.argv=['export_onnx','--checkpoint',str(args.checkpoint.resolve()),'--output-file',str(model_path)]
    # The Piper 1.8 exporter targets the established ONNX tracer; PyTorch 2.11
    # defaults to Dynamo, which is not compatible with this VITS export script.
    original_export=torch.onnx.export
    with patch('torch.onnx.export',partial(original_export,dynamo=False)):
        export_onnx.main()
    shutil.copyfile(args.dataset/'voice-config.json',Path(str(model_path)+'.json'))
    onnx.checker.check_model(str(model_path))
    espeak_data=Path(os.environ['LOCALAPPDATA'])/'LocalCodingAgent/piper-runtime/Lib/site-packages/piper/espeak-ng-data'
    voice=PiperVoice.load(str(model_path),use_cuda=False,espeak_data_dir=espeak_data)
    results=[]
    with httpx.Client(timeout=60,trust_env=False) as client:
        for index,text in enumerate(EVALUATION_TEXTS):
            began=time.monotonic();buffer=io.BytesIO()
            with wave.open(buffer,'wb') as audio:voice.synthesize_wav(text,audio)
            elapsed=time.monotonic()-began
            destination=output/f'evaluation-{index+1}.wav';destination.write_bytes(buffer.getvalue())
            response=client.post('http://127.0.0.1:8080/inference',
                files={'file':('audio.wav',buffer.getvalue(),'audio/wav')},
                data={'response_format':'json','language':'ru'})
            response.raise_for_status();transcript=response.json()['text'].strip()
            similarity=SequenceMatcher(None,normalize(text),normalize(transcript),autojunk=False).ratio()
            with wave.open(io.BytesIO(buffer.getvalue()),'rb') as audio:
                duration=audio.getnframes()/audio.getframerate()
                if audio.getnchannels()!=1 or audio.getsampwidth()!=2 or not .5<=duration<=30:
                    raise RuntimeError('Invalid exported audio')
            results.append({'text':text,'transcript':transcript,'similarity':round(similarity,3),
                            'seconds':round(elapsed,3),'audio_seconds':round(duration,3),'file':str(destination)})
            print(json.dumps(results[-1],ensure_ascii=False),flush=True)
    mean=sum(result['similarity'] for result in results)/len(results)
    report={'checkpoint':str(args.checkpoint.resolve()),'onnx':str(model_path),'onnx_bytes':model_path.stat().st_size,
            'mean_similarity':round(mean,3),'asr_passed':mean>=.85 and min(r['similarity'] for r in results)>=.7,
            'subjective_voice_quality':'Requires user listening; ASR does not measure timbre similarity.',
            'examples':results}
    (output/'evaluation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    print('Evaluation:',json.dumps({k:v for k,v in report.items() if k!='examples'}),flush=True)
    if not report['asr_passed']:raise RuntimeError('Exported model needs further training or data review')


if __name__=='__main__':main()
