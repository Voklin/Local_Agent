# 8. API и протоколы

## Три границы

1. `window.lca` — типизированная поверхность renderer.
2. Electron IPC — строковые каналы между preload и main.
3. JSON-lines — запросы/ответы и события между main и Python.

HTTP модели — четвёртый, независимый канал. Не смешивайте SSE модели с `core:event` или строками stdout.

## Полная таблица операций

| `window.lca` | IPC | Python method | Данные и результат |
| --- | --- | --- | --- |
| `health()` | `core:health` | `health` | `ok`, `service`, `protocol: 1`, `project` |
| `chooseProject()` | `project:choose` | `set_project` | Main сам выбирает `root`; ответ `root`, `name`; отмена диалога даёт `canceled: true` |
| `listFiles(path='.')` | `project:list` | `list_files` | Относительный `path`; ответ `items`, `truncated` |
| `readFile(path)` | `project:read` | `read_file` | Ответ `content`, `path` |
| `systemInfo()` | `system:home` | Нет | Main возвращает `home`, `platform`; это не файловый инструмент модели |
| `configureModel(config)` | `model:configure` | `configure_model` | `base_url`, `model`, `api_key`; ответ только не-секретные поля |
| `listModels()` | `model:list` | `list_models` | `models: string[]` |
| `getModelSettings()` | `model:settings` | `get_model_settings` | `base_url`, `model`, без ключа |
| `listChats()` | `chat:list` | `list_chats` | Метаданные чатов выбранного проекта |
| `newChat()` | `chat:new` | `new_chat` | `chat`, `task` |
| `loadChat(id)` | `chat:load` | `load_chat` | `chat_id`; ответ `chat`, `task` |
| `startTask(prompt,resume=false)` | `task:start` | `start_task` | Принятие: `run_id`, `chat_id`; результат приходит отдельно |
| `cancelTask()` | `task:cancel` | `cancel_task` | Запрашивает остановку; `ok: true` не заменяет `task_end` |
| `resolveApproval(run,id,decision)` | `task:approve` | `resolve_approval` | `run_id`, `approval_id`, `apply/reject/cancel` |
| `onEvent(callback)` | Подписка `core:event` | Нет отдельного request | Возвращает функцию отписки |

Переключение проекта/чата, настройка и новый запуск отклоняются во время активной задачи. Сам просмотр файлов может выполняться, пока задача работает. `list_models` использует синхронный `urllib` timeout 5 секунд и на это короткое время занимает основной обработчик моста; отменяемый модельный transport относится к задачам генерации.

## Формат JSON-lines

Одна строка UTF-8, один объект, завершение `\n`:

```json
{"id": 12, "method": "read_file", "params": {"path": "src/main.py"}}
```

```json
{"id": 12, "ok": true, "content": "print('hello')\n", "path": "src/main.py"}
```

При ошибке ответ содержит `id`, `ok: false`, `error`. Неизвестные методы не исполняются. Вход должен быть объектом, `params` — объектом. После некорректного JSON следующий корректный запрос остаётся обрабатываемым; `req_id` сбрасывается на каждой строке, чтобы ошибка не получила ID предыдущей команды.

Stdout зарезервирован под протокол. Обычный `print` из рабочего кода способен испортить обмен; диагностический текст следует передавать событием `log` или писать в stderr. Main игнорирует неразбираемые строки, но это не делает повреждение протокола правильным поведением.

## Общие поля событий

Задачные события имеют `event`, `run_id` и `chat_id`. Дополнительные поля зависят от типа. У `backend_stopped`, создаваемого main, нет обязательных ID задачи.

| `event` | Поля | Значение |
| --- | --- | --- |
| `text_delta` | `message_id`, `text` | Дописать фрагмент assistant-текста |
| `chat` | `role`, `text`, `message_id` либо `null` | Полное сообщение; финал заменяет соответствующий поток |
| `log` | `text` | Диагностика, обрезается сервисом до 12000 символов на событие |
| `progress` | `count`, `maximum` | Число вызовов инструментов и лимит, не процент готовности задачи |
| `task` | `task` | Снимок контрольной точки |
| `change` | `change` | `path`, `diff`, `exists`, `status`, `error` |
| `approval` | `approval_id`, `path`, `diff`, `exists` | Предложение, которое ждёт решения |
| `result` | `text` | Итоговый текст движка; UI использует как fallback, если assistant не появился |
| `failed` | `text` | Ошибка выполнения |
| `task_end` | Общие ID | Поток завершён; можно снова отправлять запрос |
| `backend_stopped` | `event` | Процесс недоступен; переподключение требует выбора проекта |

Пример:

```json
{"event":"text_delta","run_id":"run-example","chat_id":"chat-example","message_id":"run-example:0","text":"Начало ответа"}
```

Эти учебные ID не являются настоящими UUID. В реальном коде `run_id` и `approval_id` создаются через `uuid4().hex`.

## Корреляция approval

Для решения нужны одновременно текущие `run_id` и `approval_id`. Сервис проверяет наличие активного движка и предложения. Старый ID, неверный запуск, повторное применение и произвольная строка решения возвращают ошибку. Входящий запрос не содержит само содержимое файла повторно: движок ждёт решение по уже предложенным аргументам.

## Файловое API моста и инструменты модели

У этих интерфейсов разные структуры:

| Свойство | UI bridge | Tool API модели |
| --- | --- | --- |
| Список файлов | `items: [{name,path,kind}]` | `entries: [{path,type}]` |
| Чтение | До 1 000 000 байт; замена некорректных UTF-8 символов | До 120 000 байт; не-UTF-8 отклоняется |
| Запись | Прямого метода нет | `write_file` через engine approval |
| Поиск | Отдельный метод UI не опубликован | `search_text` |

Поэтому ответ `listFiles` нельзя без преобразования подставить как результат модельного `list_files`.

## HTTP Chat Completions

Клиент получает `base_url`, а SDK формирует запрос `/chat/completions`. В `messages` используются роли `system`, `user`, `assistant`, `tool`. Поле `tool_calls` находится у assistant-сообщения; результат инструмента содержит соответствующий `tool_call_id`.

При streaming движок собирает `delta.content` и `delta.tool_calls`; имя и JSON-аргументы могут быть разрезаны между чанками. Обязательная проверка `json.loads` выполняется после сборки. При отсутствии tools и наличии полноценного ответа модельный ход может завершить задачу.

Модель не обязана возвращать одинаковые ответы на одинаковый prompt. Автотесты используют детерминированные HTTP-фикстуры, чтобы проверить наш протокол независимо от качества генерации.

## Внутренний контракт approval snapshot

Это Python-контракт между engine и tools, не новая RPC-команда. `preview_file_change` возвращает `snapshot` с полями `path`, `exists`, `sha256` (null для отсутствующего файла), `proposed_sha256`. Движок удерживает его во время ожидания решения. После совпадающих run/proposal ID решение Apply передаёт `approved=True, expected_snapshot=...` в `execute_tool`. Модель не может установить эти keyword-only параметры внутри своего JSON.

`APPROVAL_REQUIRED` означает отсутствие согласия; `APPROVAL_SNAPSHOT_REQUIRED` — отсутствие внутреннего снимка; `FILE_CHANGED` — несовпадение снимка/появление target. Последний исход показывается в change.error; он не должен восприниматься UI или моделью как успешная запись.
