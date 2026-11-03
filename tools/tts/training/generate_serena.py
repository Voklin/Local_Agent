"""Resumable synthetic Serena corpus with per-utterance provenance and CPU STT QA."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import random
import re
import time
import wave
from difflib import SequenceMatcher


def texts():
    """Combine curated phonetic coverage with varied everyday sentences."""
    corpus=Path(__file__).with_name('serena_texts.txt')
    if not corpus.is_file():raise ValueError('Локальный корпус не публикуется: создайте serena_texts.txt рядом со скриптом, по одной фразе на строке.')
    lines=corpus.read_text(encoding='utf8').splitlines()
    places=['в библиотеке','у большого окна','на городской площади','в тихом парке','около старого моста',
            'в маленьком кафе','на берегу озера','у входа в музей','на лесной поляне','в уютной комнате']
    events=['мы обсуждали планы на выходные','посетители рассматривали новые фотографии',
            'звучала негромкая приятная музыка','друзья делились впечатлениями о путешествии',
            'она записывала интересные мысли в блокнот','я заметила необычное сочетание цветов',
            'было особенно спокойно после долгого дня','началась наша небольшая история',
            'все внимательно слушали рассказчика','мы нашли время для приятного разговора',
            'хотелось ненадолго остановиться и отдохнуть','он задумался над неожиданным вопросом',
            'удалось закончить работу немного раньше','мы вместе выбирали следующую книгу',
            'оказалось удобнее обсуждать новый проект','я нашла нужный ответ после короткого поиска',
            'мы договорились проверить результат вечером','она улыбнулась и помахала рукой',
            'появилась идея для следующего рисунка','собрались люди с общими интересами']
    for place in places:
        for event in events:
            line=f'Сегодня {place} {event}.'
            lines.append(line)
    return list(dict.fromkeys(line.strip() for line in lines if line.strip()))


def normalize(text):
    """Ignore punctuation/case when comparing Russian teacher audio with STT."""
    return ' '.join(re.findall(r'[а-яёa-z0-9]+',text.lower().replace('ё','е')))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--limit',type=int,default=12)
    parser.add_argument('--batch-size',type=int,default=2)
    args=parser.parse_args()
    import httpx
    import numpy as np
    import soundfile as sf
    import torch
    from huggingface_hub import snapshot_download
    from qwen_tts import Qwen3TTSModel
    from scipy.signal import resample_poly
    args.output.mkdir(parents=True,exist_ok=True)
    audio_dir=args.output/'wav';audio_dir.mkdir(exist_ok=True)
    prompts=texts()
    manifest={'teacher':'Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice',
              'teacher_revision':'85e237c12c027371202489a0ec509ded67b5e4b5','speaker':'Serena','language':'Russian',
              'sample_rate':22050,'prompt_sha256':hashlib.sha256('\n'.join(prompts).encode()).hexdigest(),
              'total_prompts':len(prompts),'seed':42}
    manifest_path=args.output/'manifest.json'
    if manifest_path.exists():
        previous=json.loads(manifest_path.read_text(encoding='utf8'))
        previous.setdefault('teacher_revision',manifest['teacher_revision'])
        if previous!=manifest:raise RuntimeError('Corpus configuration changed; use a new output directory')
    manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
    records_path=args.output/'records.jsonl'
    records={}
    if records_path.exists():
        for line in records_path.read_text(encoding='utf8').splitlines():
            record=json.loads(line);records[record['id']]=record
    pending=[(f'{index:05d}',text) for index,text in enumerate(prompts[:args.limit])
             if f'{index:05d}' not in records]
    if not pending:print('Nothing to generate',flush=True);return
    if torch.cuda.mem_get_info()[0]<3*1024**3:raise RuntimeError('Need 3 GiB free VRAM')
    torch.set_num_threads(4)
    model_path=snapshot_download(manifest['teacher'],revision=manifest['teacher_revision'],local_files_only=True)
    model=Qwen3TTSModel.from_pretrained(model_path,device_map='cuda:0',dtype=torch.bfloat16,attn_implementation='sdpa')
    with httpx.Client(timeout=60,trust_env=False) as client:
        for start in range(0,len(pending),args.batch_size):
            batch=pending[start:start+args.batch_size]
            batch_seed=42+int(batch[0][0])
            began=time.monotonic();torch.manual_seed(batch_seed)
            with torch.inference_mode():
                waves,rate=model.generate_custom_voice(text=[text for _,text in batch],language='Russian',
                    speaker='Serena',max_new_tokens=768)
            for (identifier,text),audio in zip(batch,waves,strict=True):
                record={'id':identifier,'text':text,'seed_batch':batch_seed,
                        'generation_seconds_batch':round(time.monotonic()-began,2)}
                try:
                    audio=np.asarray(audio,dtype=np.float32)
                    if audio.ndim!=1 or not np.isfinite(audio).all() or not .6<=len(audio)/rate<=20:
                        raise ValueError('Invalid teacher audio')
                    converted=resample_poly(audio,147,160) if rate==24000 else resample_poly(audio,22050,rate)
                    buffer=io.BytesIO();sf.write(buffer,converted,22050,format='WAV',subtype='PCM_16')
                    response=client.post('http://127.0.0.1:8080/inference',
                        files={'file':('utterance.wav',buffer.getvalue(),'audio/wav')},
                        data={'response_format':'json','language':'ru'})
                    response.raise_for_status();transcript=response.json()['text'].strip()
                    similarity=SequenceMatcher(None,normalize(text),normalize(transcript),autojunk=False).ratio()
                    record.update(seconds=round(len(converted)/22050,3),transcript=transcript,similarity=round(similarity,3),
                                  accepted=similarity>=.78)
                    target=audio_dir/f'{identifier}.wav';target.write_bytes(buffer.getvalue())
                    record['sha256']=hashlib.sha256(buffer.getvalue()).hexdigest()
                except Exception as exc:
                    record.update(accepted=False,error=f'{type(exc).__name__}: {exc}')
                with records_path.open('a',encoding='utf8') as log:log.write(json.dumps(record,ensure_ascii=False)+'\n')
                records[identifier]=record
                print(json.dumps(record,ensure_ascii=False),flush=True)
            accepted=[r for r in records.values() if r.get('accepted')]
            (args.output/'metadata.csv').write_text(''.join(f"{r['id']}.wav|{r['text']}\n" for r in accepted),encoding='utf8')
            status={'generated':len(records),'accepted':len(accepted),'audio_seconds':round(sum(r.get('seconds',0) for r in accepted),1)}
            (args.output/'status.json').write_text(json.dumps(status),encoding='utf8')
            if len(records)>=12 and len(accepted)/len(records)<.7:raise RuntimeError('Teacher QA rejection rate too high')
    print('Dataset ready:',json.dumps(status),flush=True)


if __name__=='__main__':main()
