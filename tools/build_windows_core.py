"""Build the Windows x64 stdio Core from a pinned Python 3.12 environment."""
from pathlib import Path
import platform
import subprocess
import sys
import ssl


def main():
    """Freeze the bridge and its imports into an onedir bundle without Qt."""
    if sys.platform != 'win32' or sys.version_info[:2] != (3, 12) or platform.machine().lower() not in ('amd64', 'x86_64'):
        raise SystemExit('Build requires Windows x64 and Python 3.12; see docs/14-windows-packaging.md')
    root = Path(__file__).resolve().parents[1]
    runtime_data = []
    # The bundled Codex Python has an ssl.py patch requiring this adjacent PEM.
    # Standard CPython has no such file and needs no extra option.
    rejected_cas = Path(ssl.__file__).with_name('codex-rejected-cas.pem')
    if rejected_cas.is_file():
        runtime_data = ['--add-data', str(rejected_cas) + ':.']
    subprocess.run([sys.executable, '-m', 'PyInstaller', '--noconfirm', '--clean', '--onedir', '--console',
                    '--name', 'lca-core', '--paths', str(root), '--noupx',
                    '--distpath', str(root / 'build/core'), '--workpath', str(root / 'build/pyinstaller'),
                    '--specpath', str(root / 'build'), '--exclude-module', 'PySide6',
                    '--collect-submodules', 'mcp.client', '--collect-data', 'jsonschema_specifications',
                    '--collect-submodules', 'openai.resources', '--collect-submodules', 'openai.types',
                    '--add-data', str(root / 'skills') + ':skills', *runtime_data,
                    str(root / 'core/python/bridge.py')], cwd=root, check=True)
    print(root / 'build/core/lca-core/lca-core.exe')


if __name__ == '__main__':
    main()
