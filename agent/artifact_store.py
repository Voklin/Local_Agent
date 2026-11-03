"""Immutable, content-addressed local tool outputs; never interpreted as instructions."""
from __future__ import annotations

import hashlib
import os
from pathlib import Path
import tempfile


ARTIFACT_THRESHOLD = 16_384


class ArtifactStore:
    """Keep large UTF-8 values outside SQLite, verified on every full read."""

    def __init__(self, directory):
        self.directory = Path(directory)

    def path(self, digest):
        """Resolve only a canonical SHA-256, never a caller-supplied filesystem path."""
        if not isinstance(digest, str) or len(digest) != 64 or any(c not in '0123456789abcdef' for c in digest):
            raise ValueError('Некорректная ссылка на артефакт')
        return self.directory / digest[:2] / (digest + '.utf8')

    def put(self, text):
        """Flush a complete immutable value before any database reference may commit."""
        raw = text.encode('utf-8')
        digest = hashlib.sha256(raw).hexdigest()
        path = self.path(digest)
        if path.exists():
            if path.read_bytes() != raw:
                raise ValueError('Сохранённый артефакт повреждён; исходник сохранён')
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            descriptor, temporary = tempfile.mkstemp(prefix='artifact_', suffix='.tmp', dir=path.parent)
            try:
                with os.fdopen(descriptor, 'wb') as stream:
                    stream.write(raw)
                    stream.flush()
                    os.fsync(stream.fileno())
                os.replace(temporary, path)
            finally:
                if os.path.exists(temporary):
                    os.unlink(temporary)
        return {'sha256': digest, 'bytes': len(raw), 'encoding': 'utf-8'}

    def get(self, reference):
        """Fail explicitly for missing or changed output, without rerunning its tool."""
        if not isinstance(reference, dict) or reference.get('encoding') != 'utf-8':
            raise ValueError('Некорректные метаданные артефакта')
        path = self.path(reference.get('sha256'))
        try:
            raw = path.read_bytes()
        except FileNotFoundError as exc:
            raise ValueError('Полный результат инструмента отсутствует; восстановите каталог artifacts из резервной копии') from exc
        if len(raw) != reference.get('bytes') or hashlib.sha256(raw).hexdigest() != reference['sha256']:
            raise ValueError('Контрольная сумма результата инструмента не совпадает; артефакт сохранён для проверки')
        return raw.decode('utf-8')
