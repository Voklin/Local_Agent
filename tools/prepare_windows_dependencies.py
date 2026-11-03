"""Fetch pinned official Windows runtime dependencies; never execute installers."""
import hashlib
import json
from pathlib import Path
import shutil
import urllib.request
import zipfile


def verified_download(spec, destination):
    """Reuse a verified cache or download atomically, rejecting any hash mismatch."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.is_file():
        with destination.open('rb') as source:
            if hashlib.file_digest(source, 'sha256').hexdigest() == spec['sha256']:
                return destination
    temporary = destination.with_suffix(destination.suffix + '.download')
    try:
        with urllib.request.urlopen(spec['url'], timeout=120) as response, temporary.open('wb') as output:
            shutil.copyfileobj(response, output)
        with temporary.open('rb') as source:
            actual = hashlib.file_digest(source, 'sha256').hexdigest()
        if actual != spec['sha256']:
            raise ValueError(f'Untrusted dependency: SHA256 mismatch for {destination.name}: {actual}')
        temporary.replace(destination)
    finally:
        temporary.unlink(missing_ok=True)
    return destination


def prepare(root):
    """Stage server/DLLs/licenses and offline VC++ bootstrap under ignored build/."""
    manifest = json.loads((root / 'packaging/windows-dependencies.json').read_text('utf-8'))
    output = root / 'build/windows-deps'
    archive = verified_download(manifest['llama'], output / 'cache/llama.zip')
    verified_download(manifest['vcredist'], output / 'prerequisites/vc_redist.x64.exe')
    runtime = output / 'llama'
    runtime.mkdir(parents=True, exist_ok=True)
    # Copy only flat official server payload. No archive-controlled extraction paths.
    with zipfile.ZipFile(archive) as bundle:
        for item in bundle.infolist():
            if '/' in item.filename or '\\' in item.filename:
                raise ValueError('Expected flat official llama.cpp archive')
            if item.filename == 'llama-server.exe' or item.filename.endswith('.dll') or item.filename.startswith('LICENSE'):
                (runtime / item.filename).write_bytes(bundle.read(item))
    for name in ('llama-server.exe', 'llama-server-impl.dll', 'llama.dll', 'ggml.dll', 'ggml-base.dll', 'ggml-cpu-x64.dll', 'libomp.dll'):
        if not (runtime / name).is_file():
            raise ValueError(f'Incomplete runtime: {name}')
    shutil.copyfile(root / 'packaging/llama-LICENSE.txt', runtime / 'LICENSE-llama.cpp.txt')
    shutil.copyfile(root / 'packaging/windows-dependencies.json', runtime / 'dependencies.json')
    print(f'Prepared llama.cpp {manifest["llama"]["version"]} and VC++ {manifest["vcredist"]["version"]}')


if __name__ == '__main__':
    prepare(Path(__file__).resolve().parents[1])
