"""Генерирует справочники из AST; объяснения берёт из ручных аннотаций."""
from __future__ import annotations
import argparse
import ast
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from doc_notes import FILE_NOTES, SYMBOL_NOTES, TEST_PURPOSES, TEST_HELPERS, DESIGN_CLASSES, DESIGN_METHODS, TS_NOTES, DEPENDENCY_NOTES

ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = {
    'docs/reference/file-map.md': 'Карта файлов',
    'docs/reference/python.md': 'Справочник Python',
    'docs/reference/typescript.md': 'Справочник TypeScript и JavaScript',
    'docs/reference/tests.md': 'Справочник Python-тестов',
    'docs/reference/design-reference.md': 'Справочник архивного эталона дизайна',
    'docs/reference/dependencies.md': 'Объявленные и зафиксированные зависимости',
}


def configure_console():
    """Включает UTF-8 для диагностического вывода CLI, включая Windows с исходной кодировкой CP1252."""
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, 'reconfigure'):
            stream.reconfigure(encoding='utf-8')


def git_executable():
    """Находит Git в PATH, LCA_GIT или штатной поставке GitHub Desktop на Windows."""
    if os.environ.get('LCA_GIT'):
        return os.environ['LCA_GIT']
    if executable := shutil.which('git'):
        return executable
    candidates = sorted((Path.home() / 'AppData/Local/GitHubDesktop').glob('app-*/resources/app/git/cmd/git.exe'))
    if candidates:
        return str(candidates[-1])
    raise RuntimeError('Нужен Git в PATH или полный путь в LCA_GIT')


def repository_files():
    """Возвращает существующие tracked/untracked файлы Git без ignored-окружений и сборок."""
    result = subprocess.run([git_executable(), 'ls-files', '--cached', '--others', '--exclude-standard', '-z'],
                            cwd=ROOT, check=True, capture_output=True)
    files = {name for name in result.stdout.decode('utf-8').split('\0') if name and (ROOT / name).is_file()}
    return sorted(files | OUTPUTS.keys())


def file_description(name):
    """Находит ручное назначение файла или заголовок главы; неизвестный исходник требует аннотации."""
    if name in FILE_NOTES:
        return FILE_NOTES[name]
    if name in OUTPUTS:
        return 'Генерируемый документ: ' + OUTPUTS[name] + '.'
    if name.startswith('docs/') and name.endswith('.md'):
        text = (ROOT / name).read_text(encoding='utf-8-sig')
        heading = next((line.lstrip('# ').strip() for line in text.splitlines() if line.startswith('# ')), name)
        return 'Ручная учебная глава или исторический материал: ' + heading + '.'
    if name.startswith('skills/') and name.endswith('/SKILL.md'):
        return 'Краткий навык ' + name.split('/')[1] + '; SkillManager использует метаданные для выбора по prompt.'
    raise ValueError('Нет назначения файла: ' + name)


def python_symbols(path):
    """Извлекает классы, функции, методы и вложенные объявления Python с реальными строками."""
    tree = ast.parse(path.read_text(encoding='utf-8-sig'))
    result = []

    def visit(node, scope=()):
        """Рекурсивно обходит объявления, сохраняя квалифицированное имя родителя."""
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                qualified = '.'.join((*scope, child.name))
                if isinstance(child, ast.ClassDef):
                    signature = 'class ' + child.name + ('(' + ', '.join(ast.unparse(b) for b in child.bases) + ')' if child.bases else '')
                    fields = [ast.unparse(item) for item in child.body if isinstance(item, ast.AnnAssign)]
                    kind = 'class'
                else:
                    signature = ('async ' if isinstance(child, ast.AsyncFunctionDef) else '') + 'def ' + child.name + '(' + ast.unparse(child.args) + ')'
                    if child.returns:
                        signature += ' -> ' + ast.unparse(child.returns)
                    fields, kind = [], 'function'
                decorators = ['@' + ast.unparse(d) for d in child.decorator_list]
                result.append({'name':qualified,'leaf':child.name,'line':child.lineno,'kind':kind,
                    'signature':'\n'.join([*decorators, signature]),'fields':fields,'docstring':ast.get_docstring(child)})
                visit(child, (*scope, child.name))
            else:
                visit(child, scope)
    visit(tree)
    return result


def symbol_description(file, symbol):
    """Подбирает проверяемую ручную аннотацию; отсутствие назначения рабочего символа — ошибка."""
    key = file + ':' + symbol['name']
    if key in SYMBOL_NOTES:
        return SYMBOL_NOTES[key]
    leaf = symbol['leaf']
    if leaf == '__init__':
        return 'Инициализирует состояние экземпляра ' + symbol['name'].rsplit('.',1)[0] + '; параметры показаны в сигнатуре, назначение описано у класса.'
    if file.startswith('tests/') or 'SandboxTests' in symbol['name']:
        if symbol['kind'] == 'class':
            return 'Тестовый класс/фикстура: ' + file_description(file)
        if leaf.startswith('test_') and leaf[5:] in TEST_PURPOSES:
            return 'Проверка: ' + TEST_PURPOSES[leaf[5:]]
        if leaf in TEST_HELPERS:
            return TEST_HELPERS[leaf]
    if file.startswith('design_reference/'):
        if symbol['kind'] == 'class' and leaf in DESIGN_CLASSES:
            return DESIGN_CLASSES[leaf]
        if leaf in DESIGN_METHODS:
            return DESIGN_METHODS[leaf] + ' Только архивный эталон.'
    if file.startswith('tools/') and symbol.get('docstring'):
        return symbol['docstring'].split('\n')[0]
    raise ValueError('Нет описания символа: ' + key)


def markdown_symbol(file, symbol, description, language):
    """Формирует блок объявления с сигнатурой, назначением и ссылкой на строку исходника."""
    result = ['### `' + symbol['name'] + '`', '',
        '[Исходник](../../' + file + '#L' + str(symbol['line']) + ')', '',
        '```' + language, symbol['signature'], '```', '', description, '']
    if symbol.get('fields'):
        result += ['Поля, объявленные в классе:', '', '```python', '\n'.join(symbol['fields']), '```', '']
    return '\n'.join(result)


def module_anchor(file):
    """Создаёт стабильный ASCII-якорь модуля для оглавления больших справочников."""
    return 'module-' + re.sub(r'[^a-z0-9]+', '-', file.lower()).strip('-')


def render():
    """Строит содержимое всех справочников без изменения файлов рабочего приложения."""
    files = repository_files()
    documents = {path:'# ' + title + '\n\nЭтот файл создаётся `python tools/generate_code_reference.py`. '
        'Сигнатуры и номера строк извлечены из исходников; назначения — из ручных аннотаций. '
        'Изменяйте объяснения в `tools/doc_notes.py`, затем пересоздайте справочник.\n\n'
        'Блоки сигнатур приводятся без тела; это справочные объявления, а не самостоятельные программы.\n\n'
        '[К руководству](../README.md)\n\n' for path,title in OUTPUTS.items()}
    groups = {path:[] for path in OUTPUTS if path not in ('docs/reference/file-map.md', 'docs/reference/dependencies.md')}
    for file in files:
        if file.endswith('.py'):
            output = 'docs/reference/tests.md' if file.startswith('tests/') else 'docs/reference/design-reference.md' if file.startswith('design_reference/') else 'docs/reference/python.md'
            groups[output].append(file)
        elif file.endswith(('.ts','.tsx','.mjs','.cjs')):
            groups['docs/reference/typescript.md'].append(file)
    for output, modules in groups.items():
        documents[output] += '## Оглавление модулей\n\n' + '\n'.join('- [' + file + '](#' + module_anchor(file) + ')' for file in modules) + '\n\n'
    inventory = ['| Файл | Назначение |', '| --- | --- |']
    used_symbols = set()
    for file in files:
        description = file_description(file)
        inventory.append('| [' + file + '](../../' + file + ') | ' + description.replace('|','\\|') + ' |')
        if not file.endswith('.py'):
            continue
        output = 'docs/reference/tests.md' if file.startswith('tests/') else 'docs/reference/design-reference.md' if file.startswith('design_reference/') else 'docs/reference/python.md'
        documents[output] += '<a id="' + module_anchor(file) + '"></a>\n\n## `' + file + '`\n\n' + description + '\n\n'
        symbols = python_symbols(ROOT / file)
        if not symbols:
            documents[output] += 'Именованных классов/функций нет. Исполняемый entry point и константы описаны в главе о соответствующем слое.\n\n'
        for symbol in symbols:
            used_symbols.add(file + ':' + symbol['name'])
            documents[output] += markdown_symbol(file, symbol, symbol_description(file,symbol), 'python') + '\n'
    stale = sorted(set(SYMBOL_NOTES) - used_symbols)
    if stale:
        raise ValueError('Устаревшие аннотации: ' + ', '.join(stale))
    stale_files = sorted(set(FILE_NOTES) - set(files))
    if stale_files:
        raise ValueError('Устаревшие назначения файлов: ' + ', '.join(stale_files))
    ts_files = [name for name in files if name.endswith(('.ts','.tsx','.mjs','.cjs'))]
    result = subprocess.run(['node','tools/extract_ts_symbols.cjs'], cwd=ROOT,
        input=json.dumps(ts_files), text=True, encoding='utf-8', capture_output=True, check=True)
    used_ts = set()
    for module in json.loads(result.stdout):
        file = module['file']
        documents['docs/reference/typescript.md'] += '<a id="' + module_anchor(file) + '"></a>\n\n## `' + file + '`\n\n' + file_description(file) + '\n\n'
        if not module['symbols']:
            documents['docs/reference/typescript.md'] += 'Нет именованных функций/типов: модуль выполняет конфигурацию, сборочный вызов или render entry. Анонимные callbacks описаны в учебных главах.\n\n'
        for symbol in module['symbols']:
            key = file + ':' + symbol['name'] if file + ':' + symbol['name'] in TS_NOTES else symbol['leaf']
            description = TS_NOTES.get(key)
            if not description:
                raise ValueError('Нет TS/JS описания: ' + file + ':' + symbol['name'])
            used_ts.add(key)
            documents['docs/reference/typescript.md'] += markdown_symbol(file,symbol,description,'typescript') + '\n'
    if stale_ts := sorted(set(TS_NOTES) - used_ts):
        raise ValueError('Устаревшие TS/JS аннотации: ' + ', '.join(stale_ts))
    manifest = json.loads((ROOT / 'apps/desktop/package.json').read_text(encoding='utf-8-sig'))
    lock = json.loads((ROOT / 'package-lock.json').read_text(encoding='utf-8-sig'))
    dependency_rows = ['## npm workspace `apps/desktop`', '',
        'Диапазон берётся из package.json, конкретная версия — из package-lock.json. Это версия снимка проекта, а не рекомендация установить последнюю библиотеку.', '',
        '| Пакет | Секция | Диапазон | Lock-версия | Назначение |', '| --- | --- | --- | --- | --- |']
    for section in ('dependencies', 'devDependencies'):
        for name, requested in manifest.get(section, {}).items():
            installed = lock['packages'].get('node_modules/' + name) or lock['packages'].get('apps/desktop/node_modules/' + name)
            if not installed or name not in DEPENDENCY_NOTES:
                raise ValueError('Нет lock-версии или описания зависимости: ' + name)
            dependency_rows.append('| `' + name + '` | `' + section + '` | `' + requested + '` | `' + installed['version'] + '` | ' + DEPENDENCY_NOTES[name] + ' |')
    dependency_rows += ['', '## Python requirements', '',
        'Это диапазоны установки, а не lock-файл Python. Qt требуется только для сохранённого GUI и соответствующих проверок. python-dotenv сохранён в полном наборе, но текущий main.py не загружает .env.', '']
    for name in ('requirements-core.txt', 'requirements.txt'):
        dependency_rows += ['### `' + name + '`', '', '```text', (ROOT / name).read_text(encoding='utf-8').strip(), '```', '']
    documents['docs/reference/dependencies.md'] += '\n'.join(dependency_rows)
    documents['docs/reference/file-map.md'] += 'Перечислены файлы репозитория; зависимости, окружения и результаты сборки исключены правилами Git.\n\n' + '\n'.join(inventory) + '\n'
    return {name: content.rstrip() + '\n' for name, content in documents.items()}


def main():
    """Записывает справочники либо с --check проверяет, совпадают ли они с текущим AST."""
    configure_console()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Только проверить актуальность без записи')
    args = parser.parse_args()
    documents = render()
    stale = []
    for name, content in documents.items():
        path = ROOT / name
        if args.check:
            if not path.exists() or path.read_text(encoding='utf-8') != content:
                stale.append(name)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding='utf-8', newline='\n')
    if stale:
        raise SystemExit('Справочник устарел: ' + ', '.join(stale))
    print(('Проверено' if args.check else 'Создано') + f' справочников: {len(documents)}')


if __name__ == '__main__':
    main()
