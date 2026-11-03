"""Bounded cancellable range reads without changing file bytes or newlines."""
import hashlib
import time
from .security import canonical_root, resolve_allowed_path
from .workspace_access import WorkspaceAccessPolicy


def read_range(root,path,start_line=1,end_line=None,cancelled=None,*,max_bytes=8_000_000,max_chars=12000):
    if type(start_line) is not int or start_line<1:raise ValueError('start_line: целое число от 1')
    end_line=start_line+199 if end_line is None else end_line
    if type(end_line) is not int or end_line<start_line or end_line-start_line>=400:raise ValueError('Диапазон: от 1 до 400 строк')
    base=canonical_root(root);target=WorkspaceAccessPolicy(base).require(path)
    if not target.is_file():raise ValueError('Нужен обычный файл')
    before=target.stat();deadline=time.monotonic()+5;chunks=[];length=0;digest=hashlib.sha256()
    if before.st_size>max_bytes:return {'ok':False,'error':'Файл превышает предел range reader 8 МБ'}
    with target.open('rb') as stream:
        while True:
            if cancelled and cancelled.is_set():return {'ok':False,'code':'USER_CANCELLED','error':'Чтение остановлено'}
            if time.monotonic()>deadline:return {'ok':False,'error':'Превышено время чтения'}
            block=stream.read(65536)
            if not block:break
            length+=len(block)
            if length>max_bytes:return {'ok':False,'error':'Файл вырос за пределы чтения'}
            chunks.append(block);digest.update(block)
    after=target.stat()
    if (before.st_ino,before.st_size,before.st_mtime_ns)!=(after.st_ino,after.st_size,after.st_mtime_ns):
        return {'ok':False,'code':'FILE_CHANGED','error':'Файл изменился во время чтения'}
    text=b''.join(chunks).decode('utf-8')
    if '\x00' in text:return {'ok':False,'error':'Бинарный файл нельзя читать как исходный текст'}
    lines=text.splitlines(keepends=True)
    if start_line>max(1,len(lines)):return {'ok':False,'error':'Начальная строка за концом файла','total_lines':len(lines)}
    selected=[];used=0
    for line in lines[start_line-1:end_line]:
        if used+len(line)>max_chars:break
        selected.append(line);used+=len(line)
    if lines and not selected:return {'ok':False,'code':'LINE_TOO_LONG','error':'Одна строка превышает 12000 символов; она не обрезана'}
    last=start_line+len(selected)-1
    return {'ok':True,'path':target.relative_to(base).as_posix(),'content':''.join(selected),
        'start_line':start_line,'end_line':last,'total_lines':len(lines),'sha256':digest.hexdigest(),
        'truncated':last<len(lines),'next_line':last+1 if last<len(lines) else None}
