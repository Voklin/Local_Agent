"""Opt-in Linux container checks with readonly workspace and no implicit pulls."""
import json
import re
import shutil
import uuid
from pathlib import Path
from .operation_context import OperationContext
from .optional_process import run_bounded
from .security import canonical_root,resolve_allowed_path


def container_command(root,args,settings,name):
    base=canonical_root(root);cwd=resolve_allowed_path(base,args.get('cwd','.'),must_exist=True)
    if not cwd.is_dir() or ',' in str(base):raise ValueError('Папка должна быть внутри проекта; Docker mount не поддерживает запятую в пути')
    program=args.get('program');arguments=args.get('arguments',[])
    if not isinstance(program,str) or not re.fullmatch(r'[\w./+-]{1,200}',program) or program.startswith('-'):raise ValueError('Укажите программу внутри контейнера без shell-строки')
    if not isinstance(arguments,list) or len(arguments)>100 or any(not isinstance(a,str) or len(a)>8000 or '\x00' in a for a in arguments):raise ValueError('Нужен массив до 100 аргументов')
    image=settings['image']
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._/:@-]{0,199}',image):raise ValueError('Укажите существующий локальный Docker image')
    return ['run','--rm','--pull=never','--name',name,'--network=none','--read-only','--cap-drop=ALL',
        '--security-opt=no-new-privileges','--pids-limit=64','--memory='+str(settings['memory_mb'])+'m','--cpus=1',
        '--user=65534:65534','--tmpfs=/tmp:rw,noexec,nosuid,size=128m',
        '--mount',f'type=bind,src={base},dst=/workspace,readonly','--workdir','/workspace'+('/'+cwd.relative_to(base).as_posix() if cwd!=base else ''),
        '--entrypoint',program,image,*arguments]


def container_status(root,context):
    docker=shutil.which('docker');wsl=shutil.which('wsl')
    if not docker:return {'ok':True,'available':False,'docker':False,'wsl':bool(wsl),'notice':'Docker не найден. Нужен Docker с Linux containers (например, WSL2 backend). Ничего не устанавливается автоматически.'}
    result=run_bounded([docker,'info','--format','{{.OSType}}'],root,context,limit=4000)
    available=result['ok'] and result['output'].strip()=='linux'
    return {'ok':True,'available':available,'docker':True,'wsl':bool(wsl),'notice':'Linux containers доступны' if available else 'Docker не запущен или выбран не Linux engine'}


def run_container(root,args,settings,context,approve):
    docker=shutil.which('docker')
    if not docker:raise ValueError('Docker не найден; изолированная команда не запускалась')
    timeout=args.get('timeout',60)
    if type(timeout) is not int or not 1<=timeout<=120:raise ValueError('Предел команды: 1–120 секунд')
    purpose=args.get('purpose','Проверка в контейнере')
    if not isinstance(purpose,str) or not 1<=len(purpose.strip())<=300:raise ValueError('Укажите назначение команды')
    name='neutral-'+uuid.uuid4().hex;command=container_command(root,args,settings,name)
    proposal=json.dumps({'purpose':purpose,'runtime':'Docker Linux','image':settings['image'],'program':args['program'],
        'arguments':args.get('arguments',[]),'cwd':args.get('cwd','.'),'workspace':'только чтение','network':False,'memory_mb':settings['memory_mb'],'timeout_seconds':timeout},ensure_ascii=False,indent=2)
    if context.is_set() or not approve('Изолированная команда',proposal,'command'):return {'ok':False,'error':'Запуск отклонён пользователем'}
    operation=OperationContext(timeout,parent=context)
    try:
        status=container_status(root,operation.child(5))
        if not status['available']:raise ValueError(status['notice'])
        image=run_bounded([docker,'image','inspect','--format','{{.Id}}',settings['image']],root,operation.child(5),limit=4000)
        if not image['ok']:raise ValueError('Образ не найден локально; загрузите его самостоятельно. Автоматического pull нет.')
        result=run_bounded([docker,*command],root,operation)
        return {**result,'runtime':'container','image':settings['image'],'workspace_readonly':True}
    finally:
        # Killing docker CLI does not kill its daemon-owned container.
        cleanup=run_bounded([docker,'rm','--force',name],root,OperationContext(5),limit=2000)
        if not cleanup['ok'] and 'No such container' not in cleanup['output']:
            # Do not claim cancellation/cleanup if the daemon could not confirm it.
            raise ValueError('Не удалось подтвердить удаление контейнера '+name+'; проверьте Docker вручную')
