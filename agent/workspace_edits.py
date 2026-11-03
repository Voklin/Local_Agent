"""Bounded workspace changes with explicit previews and revision checks."""
import difflib
import hashlib
import json
import os
from pathlib import Path

from .security import AccessDenied, canonical_root, resolve_allowed_path

MUTATION_TOOLS=frozenset({'patch_file','create_directory','rename_file','delete_file'})
MAX_EDIT_BYTES=1_000_000


def record_workspace_change(task,name,result,call_id,message_index):
    if task and result.get('ok') and isinstance(result.get('workspace_generation'),int):
        task['workspace_generation']=max(task.get('workspace_generation',0),result['workspace_generation'])
    if not task or name not in MUTATION_TOOLS|{'write_file'} or not result.get('ok') or result.get('unchanged') or result.get('result_unavailable'):return
    identity=f'{message_index}:{call_id}'
    event={'id':identity,'operation':name,'path':str(result.get('path',''))[:1000]}
    if result.get('destination'):event['destination']=result['destination']
    changes=task.setdefault('workspace_changes',[])
    if not any(item.get('id')==identity for item in changes):changes.append(event);del changes[:-100]
    if name!='create_directory':
        paths=task.setdefault('modified_files',[])
        for path in (event['path'],event.get('destination')):
            if path and path not in paths:paths.append(path)


def mutation_path(root,path):
    base=canonical_root(root)
    raw=Path(path).expanduser();raw=raw if raw.is_absolute() else base/raw
    target=resolve_allowed_path(base,raw)
    if target==base:raise AccessDenied('Корень проекта нельзя изменять этой операцией')
    if any(part.casefold()=='.git' for part in target.relative_to(base).parts):raise AccessDenied('Служебный каталог .git недоступен для файловых изменений')
    try:relative=raw.relative_to(base)
    except ValueError:raise AccessDenied('Путь вне проекта')
    current=base
    for part in relative.parts:
        current=current/part
        if current.is_symlink() or getattr(current,'is_junction',lambda:False)():
            raise AccessDenied('Для изменения используйте реальный путь, а не ссылку или junction')
    return target


def file_revision(path):
    if not path.is_file():raise ValueError('Нужен обычный файл')
    before=path.stat()
    if before.st_size>MAX_EDIT_BYTES:raise ValueError('Файл превышает лимит изменения 1 МБ')
    with path.open('rb') as stream:raw=stream.read(MAX_EDIT_BYTES+1)
    after=path.stat()
    identity=lambda stat:(stat.st_dev,stat.st_ino,stat.st_size,stat.st_mtime_ns)
    if len(raw)>MAX_EDIT_BYTES or identity(before)!=identity(after):raise ValueError('Файл изменился во время чтения; повторите preview')
    return raw,{'sha256':hashlib.sha256(raw).hexdigest(),'size':len(raw),'identity':list(identity(after))}


def parent_revision(path):
    stat=path.stat()
    return [stat.st_dev,stat.st_ino]


def preview_mutation(root,name,args):
    base=canonical_root(root);target=mutation_path(base,args['path']);relative=target.relative_to(base).as_posix()
    signature=hashlib.sha256(json.dumps(args,sort_keys=True,ensure_ascii=False).encode('utf-8')).hexdigest()
    snapshot={'operation':name,'path':relative,'arguments_sha256':signature}
    result={'ok':True,'path':relative,'exists':target.exists(),'operation':name,'snapshot':snapshot}
    if name=='create_directory':
        if target.exists():
            if not target.is_dir():raise ValueError('Путь уже занят файлом')
            return {**result,'unchanged':True,'diff':'Каталог уже существует'}
        missing=[];ancestor=target
        while not ancestor.exists():missing.append(ancestor);ancestor=ancestor.parent
        if not ancestor.is_dir() or len(missing)>30:raise ValueError('Нужен каталог-родитель; максимум 30 новых уровней')
        snapshot.update(parent=ancestor.relative_to(base).as_posix(),parent_identity=parent_revision(ancestor),
            directories=[p.relative_to(base).as_posix() for p in reversed(missing)])
        return {**result,'diff':'Создать каталоги:\n'+'\n'.join('+ '+p for p in snapshot['directories'])}
    raw,revision=file_revision(target);snapshot.update(source=revision,parent_identity=parent_revision(target.parent))
    if args.get('expected_sha256') and args['expected_sha256']!=revision['sha256']:
        return {'ok':False,'code':'FILE_CHANGED','error':'Ревизия файла изменилась; перечитайте нужный диапазон'}
    if name=='rename_file':
        destination=mutation_path(base,args['destination'])
        if destination==target or destination.exists():raise ValueError('Выберите новый, ещё не существующий путь')
        if not destination.parent.is_dir():raise ValueError('Сначала создайте каталог назначения')
        snapshot.update(destination=destination.relative_to(base).as_posix(),destination_parent=parent_revision(destination.parent))
        return {**result,'destination':snapshot['destination'],'diff':f"Переместить файл без замены:\n− {relative}\n+ {snapshot['destination']}\nРазмер: {len(raw)} байт\nSHA256: {revision['sha256']}"}
    try:text=raw.decode('utf-8')
    except UnicodeDecodeError:raise ValueError('Точечная правка и удаление поддерживают только UTF-8 текст')
    if '\x00' in text:raise ValueError('Бинарный файл нельзя изменять как текст')
    if name=='delete_file':
        proposed=''
    elif name=='patch_file':
        old=args['old_text'];new=args['new_text']
        if not old or '\x00' in old+new:raise ValueError('Нужен непустой old_text и текст без NUL')
        crlf='\r\n' in text and '\n' not in text.replace('\r\n','')
        if crlf:
            old=old.replace('\r\n','\n').replace('\n','\r\n');new=new.replace('\r\n','\n').replace('\n','\r\n')
        count=text.count(old)
        if count!=1:return {'ok':False,'code':'PATCH_NOT_UNIQUE' if count else 'PATCH_NOT_FOUND','error':f'old_text найден {count} раз. Укажите один точный фрагмент с контекстом.'}
        proposed=text.replace(old,new,1)
        if len(proposed.encode('utf-8'))>MAX_EDIT_BYTES:raise ValueError('Изменение превышает 1 МБ')
        snapshot['proposed_sha256']=hashlib.sha256(proposed.encode('utf-8')).hexdigest()
        result['content']=proposed
    else:raise ValueError('Неизвестная файловая операция')
    diff=''.join(difflib.unified_diff(text.splitlines(keepends=True),proposed.splitlines(keepends=True),fromfile='a/'+relative,tofile='/dev/null' if name=='delete_file' else 'b/'+relative))
    return {**result,'diff':diff or '(Нет текстовых изменений)','unchanged':name=='patch_file' and text==proposed}


def apply_mutation(root,name,args,*,approved=False,expected_snapshot=None,cancelled=None):
    if not approved:return {'ok':False,'code':'APPROVAL_REQUIRED','error':'Требуется подтверждение preview'}
    if not isinstance(expected_snapshot,dict):return {'ok':False,'code':'APPROVAL_SNAPSHOT_REQUIRED','error':'Нужен snapshot подтверждённого предложения'}
    if cancelled and cancelled.is_set():return {'ok':False,'code':'USER_CANCELLED','error':'Остановлено пользователем'}
    try:current=preview_mutation(root,name,args)
    except (OSError,ValueError,AccessDenied):current={'ok':False}
    if not current.get('ok') or current.get('snapshot')!=expected_snapshot:
        return {'ok':False,'code':'FILE_CHANGED','error':'Путь, файл или предложение изменились после preview; получите новое подтверждение'}
    base=canonical_root(root);target=mutation_path(base,args['path'])
    if name=='patch_file':
        from .tools import preview_file_change, write_file
        preview=preview_file_change(base,target,current['content'],max_existing_bytes=MAX_EDIT_BYTES)
        if not preview.get('ok') or preview['snapshot']['sha256']!=expected_snapshot['source']['sha256']:
            return {'ok':False,'code':'FILE_CHANGED','error':'Файл изменился перед записью'}
        return {**write_file(base,target,current['content'],overwrite=True,approved=True,
            expected_snapshot=preview['snapshot'],max_existing_bytes=MAX_EDIT_BYTES),'operation':name}
    changed=[]
    try:
        if name=='create_directory':
            for relative in expected_snapshot['directories']:
                if cancelled and cancelled.is_set():
                    if changed:return {'ok':False,'code':'OUTCOME_UNKNOWN','created_directories':changed,'error':'Остановлено после частичного создания каталогов; проверьте результат'}
                    return {'ok':False,'code':'USER_CANCELLED','error':'Остановлено пользователем'}
                path=mutation_path(base,relative)
                path.mkdir();changed.append(relative)
            return {'ok':True,'path':current['path'],'operation':name,'created_directories':changed}
        if name=='delete_file':
            target.unlink()
            return {'ok':True,'path':current['path'],'operation':name,'deleted_files':[current['path']]}
        if name=='rename_file':
            destination=mutation_path(base,args['destination'])
            if os.name=='nt':os.rename(target,destination)
            else:
                os.link(target,destination,follow_symlinks=False);changed.append(current['destination'])
                if file_revision(target)[1]!=expected_snapshot['source']:raise ValueError('Источник изменился перед завершением переноса')
                target.unlink()
            return {'ok':True,'path':current['path'],'destination':current['destination'],'operation':name,
                'renamed_files':[{'from':current['path'],'to':current['destination']}]}
    except Exception as exc:
        return {'ok':False,'code':'OUTCOME_UNKNOWN','error':'Операция могла выполниться частично: '+type(exc).__name__,'changed_paths':changed}
    return {'ok':False,'error':'Неизвестная файловая операция'}
