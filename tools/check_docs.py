"""Проверяет локальные Markdown-ссылки, source lines и актуальность справочников."""
import re
from pathlib import Path
from urllib.parse import unquote
from generate_code_reference import ROOT, render, configure_console


def check_links(files):
    """Проверяет локальные цели ссылок и существование строк #L; внешние URL не скачивает."""
    errors = []
    count = 0
    for path in files:
        text = path.read_text(encoding='utf-8-sig')
        text = re.sub(r'```[^\n]*\n.*?```', '', text, flags=re.S)
        for target in re.findall(r'\]\(([^)]+)\)', text):
            target = target.strip().strip('<>')
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',target):
                continue
            local, _, fragment = target.partition('#')
            destination = (path.parent / unquote(local)).resolve() if local else path
            count += 1
            if not destination.exists():
                errors.append(f'{path.relative_to(ROOT)}: отсутствует {target}')
            elif fragment.startswith('L') and fragment[1:].isdigit():
                if not destination.is_file() or int(fragment[1:]) < 1 or int(fragment[1:]) > len(destination.read_text(encoding='utf-8-sig').splitlines()):
                    errors.append(f'{path.relative_to(ROOT)}: неверная строка {target}')
            elif fragment:
                contents = destination.read_text(encoding='utf-8-sig')
                if f'id="{unquote(fragment)}"' not in contents:
                    errors.append(f'{path.relative_to(ROOT)}: отсутствует явный якорь {target}')
    return errors, count


def main():
    """Сопоставляет структурные справочники с AST и завершает проверку ошибкой при расхождении/битой ссылке."""
    configure_console()
    expected = render()
    errors = []
    for name, content in expected.items():
        path = ROOT / name
        if not path.exists() or path.read_text(encoding='utf-8') != content:
            errors.append('Устаревший справочник: ' + name)
    files = [ROOT / 'README.md', ROOT / 'README_V6_MIGRATION.md', ROOT / 'MIGRATION_PLAN.md', *sorted((ROOT / 'docs').rglob('*.md'))]
    link_errors, count = check_links(files)
    errors.extend(link_errors)
    if errors:
        raise SystemExit('\n'.join(errors))
    print(f'Документация: {len(files)} Markdown-файлов, {count} локальных ссылок; справочники актуальны')


if __name__ == '__main__':
    main()
