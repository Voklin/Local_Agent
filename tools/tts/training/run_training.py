"""Bounded Windows Piper fine-tuning from the publisher's Linux checkpoint."""
import argparse
import json
import os
from pathlib import Path
import sys
from unittest.mock import patch
from lightning.pytorch.callbacks import Callback


class SaveFinalCheckpoint(Callback):
    """Preserve the true final step even when stopping in a partial epoch."""
    def on_train_end(self, trainer, pl_module):
        trainer.save_checkpoint(Path(trainer.default_root_dir)/'final.ckpt')


def prepare_checkpoint(source, target):
    """Convert trusted Linux Path metadata and discard old optimizer state."""
    import pathlib
    import torch
    if target.exists():return
    with patch('pathlib.PosixPath',pathlib.WindowsPath):
        original=torch.load(source,map_location='cpu',weights_only=False)
    target.parent.mkdir(parents=True,exist_ok=True)
    torch.save({'state_dict':original['state_dict']},target)
    details={key:str(value) for key,value in original.get('hyper_parameters',{}).items()}
    target.with_suffix('.hyperparameters.json').write_text(json.dumps(details,indent=2),encoding='utf8')
    print('Base checkpoint converted:',target,flush=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dataset',type=Path,required=True)
    parser.add_argument('--smoke',action='store_true')
    parser.add_argument('--steps',type=int,default=6000)
    parser.add_argument('--resume',type=Path)
    args=parser.parse_args()
    root=Path(__file__).resolve().parents[3]
    dataset=args.dataset.resolve()
    base=root/'build/voice-training/base'
    source=base/'ru/ru_RU/irina/medium/epoch=4139-step=929464.ckpt'
    converted=base/'irina-weights-windows.ckpt'
    prepare_checkpoint(source,converted)
    import torch
    torch.set_num_threads(4)
    os.environ['OMP_NUM_THREADS']='4'
    status=json.loads((dataset/'status.json').read_text(encoding='utf8'))
    if status['accepted']<(8 if args.smoke else 200):raise RuntimeError('Not enough accepted recordings')
    output=(root/'build/voice-training/smoke') if args.smoke else dataset/'training'
    arguments=['piper.train','fit','--data.voice_name','miya-serena',
        '--data.csv_path',str(dataset/'metadata.csv'),'--data.audio_dir',str(dataset/'wav'),
        '--data.cache_dir',str(dataset/'cache'),'--data.config_path',str(dataset/'voice-config.json'),
        '--data.espeak_voice','ru','--data.batch_size','4','--data.num_workers','0',
        '--data.num_test_examples','1','--model.sample_rate','22050',
        '--model.mos_metric','none','--model.learning_rate','0.0001',
        '--model.learning_rate_d','0.00005','--model.lr_decay','0.999875',
        '--trainer.accelerator','gpu','--trainer.devices','1','--trainer.precision','bf16-mixed',
        '--trainer.default_root_dir',str(output),'--trainer.enable_progress_bar','false',
        '--trainer.log_every_n_steps','10','--trainer.max_steps',str(args.steps),
        '--trainer.max_epochs','100','--trainer.num_sanity_val_steps','1','--seed_everything','42']
    if args.resume:arguments+=['--ckpt_path',str(args.resume.resolve())]
    else:arguments+=['--model.warmstart_ckpt',str(converted)]
    if args.smoke:arguments+=['--trainer.fast_dev_run','true']
    sys.argv=arguments
    # The wheel's eSpeak C runtime cannot open the Cyrillic workspace path.
    # Reuse its identical data files from the existing ASCII installation.
    from functools import partial
    from piper.phonemize_espeak import EspeakPhonemizer
    from piper.train.vits import dataset as dataset_module
    espeak_data=Path(os.environ['LOCALAPPDATA'])/'LocalCodingAgent/piper-runtime/Lib/site-packages/piper/espeak-ng-data'
    if not (espeak_data/'phontab').exists():raise RuntimeError('ASCII eSpeak data directory missing')
    dataset_module.EspeakPhonemizer=partial(EspeakPhonemizer,espeak_data_dir=espeak_data)
    from lightning.pytorch.callbacks import ModelCheckpoint
    import piper.train.__main__ as training_cli
    # MOS is disabled to avoid downloading another model. Its default callback
    # must also be removed; Lightning requires every monitored metric to exist.
    training_cli._DEFAULT_CALLBACKS=[ModelCheckpoint(monitor='val_mel',mode='min',
        save_top_k=2,save_last=True,filename='epoch={epoch}-val_mel={val_mel:.4f}',auto_insert_metric_name=False),
        SaveFinalCheckpoint()]
    if args.resume:
        # LightningCLI reloads model hyperparameters from the checkpoint after
        # parsing CLI options, including the original one-time warmstart path.
        # Prevent on_fit_start from resetting resumed weights to the base voice.
        original_fit_start=training_cli.VitsModel.on_fit_start
        def resume_fit_start(model):
            model._warmstart_ckpt=None;model._vocoder_warmstart_ckpt=None
            model.hparams.warmstart_ckpt=None;model.hparams.vocoder_warmstart_ckpt=None
            return original_fit_start(model)
        with patch.object(training_cli.VitsModel,'on_fit_start',resume_fit_start):
            training_cli.main()
    else:training_cli.main()


if __name__=='__main__':main()
