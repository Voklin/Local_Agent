# Объявленные и зафиксированные зависимости

Этот файл создаётся `python tools/generate_code_reference.py`. Сигнатуры и номера строк извлечены из исходников; назначения — из ручных аннотаций. Изменяйте объяснения в `tools/doc_notes.py`, затем пересоздайте справочник.

Блоки сигнатур приводятся без тела; это справочные объявления, а не самостоятельные программы.

[К руководству](../README.md)

## npm workspace `apps/desktop`

Диапазон берётся из package.json, конкретная версия — из package-lock.json. Это версия снимка проекта, а не рекомендация установить последнюю библиотеку.

| Пакет | Секция | Диапазон | Lock-версия | Назначение |
| --- | --- | --- | --- | --- |
| `@vitejs/plugin-react` | `dependencies` | `^4.3.4` | `4.7.0` | Преобразование React/JSX и интеграция с dev-server Vite. |
| `concurrently` | `dependencies` | `^9.1.2` | `9.2.5` | Параллельный запуск dev-сервера и Electron-команды. |
| `electron` | `dependencies` | `45.0.0` | `45.0.0` | Настольный runtime Chromium/Node и его TypeScript API. |
| `lucide-react` | `dependencies` | `^0.468.0` | `0.468.0` | Иконки React-компонентов интерфейса. |
| `react` | `dependencies` | `^19.0.0` | `19.3.1` | Компоненты и hooks состояния UI. |
| `react-dom` | `dependencies` | `^19.0.0` | `19.3.1` | Создание React root и отрисовка в DOM. |
| `vite` | `dependencies` | `^6.1.0` | `6.4.5` | Dev-server и сборка renderer/main/preload. |
| `wait-on` | `dependencies` | `^8.0.2` | `8.0.5` | Ожидание TCP-порта Vite перед запуском Electron. |
| `@types/react` | `devDependencies` | `^19.0.0` | `19.3.0` | Статические описания API React для TypeScript. |
| `@types/react-dom` | `devDependencies` | `^19.0.0` | `19.3.0` | Статические описания React DOM для TypeScript. |
| `typescript` | `devDependencies` | `~5.7.2` | `5.7.3` | Компилятор проверки типов и AST API генератора документации. |

## Python requirements

Это диапазоны установки, а не lock-файл Python. Qt требуется только для сохранённого GUI и соответствующих проверок. python-dotenv сохранён в полном наборе, но текущий main.py не загружает .env.

### `requirements-core.txt`

```text
# The Electron Python Core does not require Qt.
openai>=1.68.0,<4
httpx>=0.27,<1
```

### `requirements.txt`

```text
-r requirements-core.txt
PySide6>=6.8.0
python-dotenv>=1.0.1
```
