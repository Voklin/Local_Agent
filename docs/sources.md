# Официальные материалы для изучения

Ссылки проверены при подготовке руководства 22 октября 2026 года. Версии на сайтах могут двигаться вперёд; устройство именно LocalAgent определяют его исходники, конфигурации и lock-файл. Внешняя инструкция для новой версии фреймворка не должна автоматически переписывать проект на эту версию.

| Тема | Источник | Как использовать вместе с проектом |
| --- | --- | --- |
| Python | [Python 3.12 Tutorial](https://docs.python.org/3.12/tutorial/) | Модули, функции, классы, исключения перед чтением `agent/` |
| Async Python | [Coroutines and Tasks](https://docs.python.org/3.12/library/asyncio-task.html) | `await`, отмена и передача корутин в loop из другого потока |
| React | [Quick Start](https://react.dev/learn) | Компоненты, state и обработчики в `App.tsx` |
| TypeScript | [Handbook](https://www.typescriptlang.org/docs/handbook/intro.html) | Союзы типов, интерфейсы, generics и ограничения `any` |
| Electron | [Process Model](https://www.electronjs.org/docs/latest/tutorial/process-model) | Разделение main, renderer и preload |
| Vite | [Guide](https://vite.dev/guide/) | Dev-server, build и конфигурация; в проекте закреплена ветка Vite 6 |
| npm | [Workspaces](https://docs.npmjs.com/cli/v11/using-npm/workspaces/) | Связь корневого package с `apps/desktop` |
| OpenAI Python SDK | [Python API library](https://developers.openai.com/api/reference/python) | Async-клиент и потоковые ответы; локальную политику tools реализует наш код |
| SSE API | [Streaming responses](https://developers.openai.com/api/docs/guides/streaming-responses) | Разница полного ответа и последовательности чанков |
| Git | [Pro Git](https://git-scm.com/book/en/v2) | Коммит, дерево, ветка и совместная разработка |
| GitHub | [Actions documentation](https://docs.github.com/en/actions) | Workflow, jobs, steps и hosted runners |
| llama.cpp | [Server documentation](https://github.com/ggml-org/llama.cpp/tree/master/tools/server) | Отдельный inference-сервер для GGUF; не считать его встроенным Electron-компонентом |

Примеры API в официальной документации могут относиться к другим моделям и ресурсам. В текущем коде используется Chat Completions с введённым пользователем ID и URL. Изучение SDK не требует менять этот выбор или подключать облачный API.

Руководство не воспроизводит большие фрагменты внешних материалов. Его разбор поведения основан на LocalAgent; внешние ссылки нужны для углубления в язык и инструменты.
