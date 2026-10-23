"""Manual editor proposals share the agent's snapshot-checked atomic write path."""
import hashlib
import uuid

from agent.security import canonical_root, resolve_allowed_path
from agent.tools import preview_file_change, write_file


class EditorService:
    def __init__(self):
        self.pending = None

    def clear(self):
        self.pending = None

    def read(self, root, path):
        base = canonical_root(root)
        target = resolve_allowed_path(base, path, must_exist=True)
        if not target.is_file():
            raise ValueError('Редактор открывает только обычные файлы')
        if target.stat().st_size > 1_000_000:
            raise ValueError('Файл превышает лимит редактора 1 МБ')
        raw = target.read_bytes()
        if len(raw) > 1_000_000:
            raise ValueError('Файл вырос за пределы лимита редактора')
        try:
            text = raw.decode('utf-8')
        except UnicodeDecodeError as exc:
            raise ValueError('Редактор поддерживает только UTF-8; файл не изменён') from exc
        if '\x00' in text:
            raise ValueError('Бинарный файл нельзя редактировать как текст')
        relative = target.relative_to(base).as_posix()
        newline = 'crlf' if '\r\n' in text and '\n' not in text.replace('\r\n', '') else 'lf'
        return {'ok': True, 'path': relative, 'content': text.replace('\r\n', '\n'), 'newline': newline,
                'revision': {'path': relative, 'sha256': hashlib.sha256(raw).hexdigest()}}

    def preview(self, root, params):
        self.clear()
        content = params.get('content')
        if not isinstance(content, str) or '\x00' in content:
            raise ValueError('Содержимое должно быть текстом без NUL')
        if len(content.encode('utf-8')) > 1_000_000:
            raise ValueError('Изменение превышает лимит 1 МБ')
        current = self.read(root, str(params.get('path', '')))
        if params.get('revision') != current['revision']:
            return {'ok': False, 'code': 'FILE_CHANGED',
                    'error': 'Файл изменился на диске. Черновик сохранён в редакторе; перечитайте файл перед новым изменением.'}
        normalized = content.replace('\r\n', '\n')
        proposed = normalized.replace('\n', '\r\n') if current['newline'] == 'crlf' else normalized
        preview = preview_file_change(root, current['path'], proposed)
        if not preview['ok']:
            return preview
        if preview['snapshot']['sha256'] == preview['snapshot']['proposed_sha256']:
            return {'ok': True, 'unchanged': True, 'file': current}
        proposal_id = uuid.uuid4().hex
        self.pending = {'id': proposal_id, 'root': str(canonical_root(root)), 'path': current['path'],
                        'content': proposed, 'snapshot': preview['snapshot']}
        return {'ok': True, 'proposal_id': proposal_id, 'path': current['path'], 'diff': preview['diff']}

    def resolve(self, root, params):
        pending = self.pending
        if not pending or params.get('proposal_id') != pending['id'] or str(canonical_root(root)) != pending['root']:
            raise ValueError('Предложение редактора устарело; получите новый diff')
        decision = params.get('decision')
        if decision not in ('apply', 'reject', 'cancel'):
            raise ValueError('Неизвестное решение по изменению')
        self.clear()  # One decision consumes the proposal, including an unsuccessful Apply.
        if decision != 'apply':
            return {'ok': True, 'applied': False}
        result = write_file(root, pending['path'], pending['content'], overwrite=True,
                            approved=True, expected_snapshot=pending['snapshot'])
        if not result['ok']:
            return result
        try:
            file = self.read(root, pending['path'])
        except (OSError, ValueError) as exc:
            return {**result, 'applied': True, 'file': None,
                    'warning': f'Файл записан, но не перечитан: {exc}. Черновик оставлен в редакторе.'}
        return {**result, 'applied': True, 'file': file}
