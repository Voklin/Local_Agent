# Объявленные и зафиксированные зависимости

Этот файл создаётся `python tools/generate_code_reference.py`. Сигнатуры и номера строк извлечены из исходников; назначения — из ручных аннотаций. Изменяйте объяснения в `tools/doc_notes.py`, затем пересоздайте справочник.

Блоки сигнатур приводятся без тела; это справочные объявления, а не самостоятельные программы.

[К руководству](../README.md)

## npm workspace `apps/desktop`

Диапазон берётся из package.json, конкретная версия — из package-lock.json. Это версия снимка проекта, а не рекомендация установить последнюю библиотеку.

| Пакет | Секция | Диапазон | Lock-версия | Назначение |
| --- | --- | --- | --- | --- |
| `lucide-react` | `dependencies` | `^0.468.0` | `0.468.0` | Иконки React-компонентов интерфейса. |
| `react` | `dependencies` | `^19.0.0` | `19.3.1` | Компоненты и hooks состояния UI. |
| `react-dom` | `dependencies` | `^19.0.0` | `19.3.1` | Создание React root и отрисовка в DOM. |
| `@types/react` | `devDependencies` | `^19.0.0` | `19.3.0` | Статические описания API React для TypeScript. |
| `@types/react-dom` | `devDependencies` | `^19.0.0` | `19.3.0` | Статические описания React DOM для TypeScript. |
| `electron-builder` | `devDependencies` | `26.15.3` | `26.15.3` | Упаковка Electron, включение frozen Core и создание локального NSIS installer. |
| `typescript` | `devDependencies` | `~5.7.2` | `5.7.3` | Компилятор проверки типов и AST API генератора документации. |
| `@vitejs/plugin-react` | `devDependencies` | `^4.3.4` | `4.7.0` | Преобразование React/JSX и интеграция с dev-server Vite. |
| `concurrently` | `devDependencies` | `^9.1.2` | `9.2.5` | Параллельный запуск dev-сервера и Electron-команды. |
| `electron` | `devDependencies` | `45.0.0` | `45.0.0` | Настольный runtime Chromium/Node и его TypeScript API. |
| `vite` | `devDependencies` | `^6.1.0` | `6.4.5` | Dev-server и сборка renderer/main/preload. |
| `wait-on` | `devDependencies` | `^8.0.2` | `8.0.5` | Ожидание TCP-порта Vite перед запуском Electron. |

## Python requirements

requirements-core.txt и requirements.txt задают диапазоны установки; requirements-build.txt фиксирует точные версии сборочного окружения. Qt требуется только для сохранённого GUI и соответствующих проверок. python-dotenv сохранён в полном наборе, но текущий main.py не загружает .env.

### `requirements-core.txt`

```text
# The Electron Python Core does not require Qt.
openai>=1.68.0,<4
httpx>=0.27,<1
jsonschema>=4.26.0,<5
mcp==2.3.0
lmstudio==1.5.0
watchfiles==1.1.1
pathspec==0.12.1
tree-sitter==0.25.2
tree-sitter-javascript==0.25.0
tree-sitter-typescript==0.23.2
```

### `requirements.txt`

```text
-r requirements-core.txt
PySide6>=6.8.0
python-dotenv>=1.0.1
```

### `requirements-build.txt`

```text
# Pinned Windows x64 / Python 3.12 Core build environment. No Qt.
altgraph==0.17.5
annotated-types==0.8.0
anyio==4.15.1
certifi==2026.10.19
h11==0.16.0
httpcore==1.0.9
httpcore2==2.16.0
httpx==0.28.1
httpx2==2.16.0
idna==3.20
jiter==0.17.0
openai==3.36.1
packaging==26.3
pefile==2024.8.26
pydantic==2.14.1
pydantic_core==2.50.1
pyinstaller==6.22.3
pyinstaller-hooks-contrib==2026.9
pywin32-ctypes==0.2.3
setuptools==84.2.1
sniffio==1.3.1
truststore==0.10.5
typing-inspection==0.4.4
typing_extensions==4.16.0

# MCP SDK and its pinned Windows client dependencies.
attrs==26.1.0
cffi==2.1.1
click==8.5.0
cryptography==50.0.2
jsonschema==4.26.0
jsonschema-specifications==2025.9.1
mcp==2.3.0
mcp-types==2.3.0
opentelemetry-api==1.45.1
pycparser==3.12
pyjwt==2.15.1
python-multipart==0.0.32
pywin32==312
referencing==0.37.0
rpds-py==2026.9.1
sse-starlette==3.5.1
starlette==1.10.0
uvicorn==0.54.0

# Project intelligence and managed LM Studio connection (same pins as core).
lmstudio==1.5.0
httpx-ws==0.9.0
msgspec==0.22.0
wsproto==1.3.2
watchfiles==1.1.1
pathspec==0.12.1
tree-sitter==0.25.2
tree-sitter-javascript==0.25.0
tree-sitter-typescript==0.23.2
```
