# Справочник TypeScript и JavaScript

Этот файл создаётся `python tools/generate_code_reference.py`. Сигнатуры и номера строк извлечены из исходников; назначения — из ручных аннотаций. Изменяйте объяснения в `tools/doc_notes.py`, затем пересоздайте справочник.

Блоки сигнатур приводятся без тела; это справочные объявления, а не самостоятельные программы.

[К руководству](../README.md)

## Оглавление модулей

- [apps/desktop/build-electron.mjs](#module-apps-desktop-build-electron-mjs)
- [apps/desktop/electron/main.ts](#module-apps-desktop-electron-main-ts)
- [apps/desktop/electron/preload.ts](#module-apps-desktop-electron-preload-ts)
- [apps/desktop/src/App.tsx](#module-apps-desktop-src-app-tsx)
- [apps/desktop/src/main.tsx](#module-apps-desktop-src-main-tsx)
- [apps/desktop/src/vite-env.d.ts](#module-apps-desktop-src-vite-env-d-ts)
- [apps/desktop/vite.config.ts](#module-apps-desktop-vite-config-ts)
- [tests/electron/smoke.cjs](#module-tests-electron-smoke-cjs)
- [tools/extract_ts_symbols.cjs](#module-tools-extract-ts-symbols-cjs)

<a id="module-apps-desktop-build-electron-mjs"></a>

## `apps/desktop/build-electron.mjs`

Две Vite library-сборки в main.cjs и preload.cjs с внешними системными импортами.

### `fileName`

[Исходник](../../apps/desktop/build-electron.mjs#L3)

```typescript
fileName()
```

Возвращает фиксированное имя main.cjs или preload.cjs для соответствующей сборки Vite.

### `fileName`

[Исходник](../../apps/desktop/build-electron.mjs#L4)

```typescript
fileName()
```

Возвращает фиксированное имя main.cjs или preload.cjs для соответствующей сборки Vite.

<a id="module-apps-desktop-electron-main-ts"></a>

## `apps/desktop/electron/main.ts`

Окно, Python-процесс, pending RPC, проверка sender и фиксированные IPC handlers.

### `publish`

[Исходник](../../apps/desktop/electron/main.ts#L11)

```typescript
function publish(message: any)
```

Передаёт Core-событие живому renderer через фиксированный core:event.

### `startBackend`

[Исходник](../../apps/desktop/electron/main.ts#L14)

```typescript
function startBackend()
```

Лениво запускает Python, подключает stdout/stderr и обработчики завершения.

### `startBackend.stopped`

[Исходник](../../apps/desktop/electron/main.ts#L30)

```typescript
stopped()
```

Однократно сбрасывает процесс, завершает pending RPC ошибкой и сообщает backend_stopped.

### `callBackend`

[Исходник](../../apps/desktop/electron/main.ts#L42)

```typescript
function callBackend(method: string, params: Record<string, unknown> = {})
```

Посылает JSON-lines запрос с ID/Promise, таймером и ограничением pending.

### `createWindow`

[Исходник](../../apps/desktop/electron/main.ts#L53)

```typescript
function createWindow()
```

Создаёт изолированное Electron-окно и подключает его жизненный цикл.

### `handle`

[Исходник](../../apps/desktop/electron/main.ts#L65)

```typescript
function handle(channel: string, handler: (...args: any[]) => any)
```

Регистрирует IPC handler с проверкой sender и mainFrame.

<a id="module-apps-desktop-electron-preload-ts"></a>

## `apps/desktop/electron/preload.ts`

Узкий window.lca API и отписываемый listener событий.

### `health`

[Исходник](../../apps/desktop/electron/preload.ts#L3)

```typescript
health()
```

Фиксированный preload-вызов проверки Core.

### `chooseProject`

[Исходник](../../apps/desktop/electron/preload.ts#L4)

```typescript
chooseProject()
```

Выбор проекта: UI → native dialog → проверяемый set_project.

### `listFiles`

[Исходник](../../apps/desktop/electron/preload.ts#L5)

```typescript
listFiles(relativePath = '.')
```

Preload-запрос списка файлов по относительному пути.

### `readFile`

[Исходник](../../apps/desktop/electron/preload.ts#L6)

```typescript
readFile(relativePath: string)
```

Preload-запрос readonly текста файла.

### `systemInfo`

[Исходник](../../apps/desktop/electron/preload.ts#L7)

```typescript
systemInfo()
```

Preload-запрос home/platform у main, без tool модели.

### `configureModel`

[Исходник](../../apps/desktop/electron/preload.ts#L8)

```typescript
configureModel(config: { base_url: string; model: string; api_key: string })
```

Передаёт URL/модель/сеансовый ключ в фиксированный model:configure.

### `listModels`

[Исходник](../../apps/desktop/electron/preload.ts#L9)

```typescript
listModels()
```

Запрашивает ID доступных моделей.

### `getModelSettings`

[Исходник](../../apps/desktop/electron/preload.ts#L10)

```typescript
getModelSettings()
```

Читает сохранённые URL/ID без ключа.

### `listChats`

[Исходник](../../apps/desktop/electron/preload.ts#L11)

```typescript
listChats()
```

Получает чаты выбранного проекта.

### `newChat`

[Исходник](../../apps/desktop/electron/preload.ts#L12)

```typescript
newChat()
```

Создаёт пустой чат проекта.

### `loadChat`

[Исходник](../../apps/desktop/electron/preload.ts#L13)

```typescript
loadChat(chatId: string)
```

Загружает проверяемый ID чата.

### `startTask`

[Исходник](../../apps/desktop/electron/preload.ts#L14)

```typescript
startTask(prompt: string, resume = false)
```

Посылает prompt и resume-флаг, получает принятие задачи.

### `cancelTask`

[Исходник](../../apps/desktop/electron/preload.ts#L15)

```typescript
cancelTask()
```

Запрашивает отмену через task:cancel.

### `resolveApproval`

[Исходник](../../apps/desktop/electron/preload.ts#L16)

```typescript
resolveApproval(runId: string, approvalId: string, decision: string)
```

Передаёт run/proposal ID и явное решение.

### `onEvent`

[Исходник](../../apps/desktop/electron/preload.ts#L17)

```typescript
onEvent(callback: (event: unknown) => void)
```

Подписывает callback на core:event и возвращает отписку.

### `onEvent.listener`

[Исходник](../../apps/desktop/electron/preload.ts#L18)

```typescript
listener(_event: Electron.IpcRendererEvent, data: unknown)
```

Адаптирует Electron event в пользовательские данные callback.

<a id="module-apps-desktop-src-app-tsx"></a>

## `apps/desktop/src/App.tsx`

React-состояние и представление проекта, настроек, чата, потока, checkpoint и diff.

### `FileItem`

[Исходник](../../apps/desktop/src/App.tsx#L4)

```typescript
type FileItem = { name: string; path: string; kind: 'file' | 'directory' };
```

Тип элемента readonly-проводника: имя, относительный путь, вид файла/каталога.

### `Message`

[Исходник](../../apps/desktop/src/App.tsx#L5)

```typescript
type Message = { role: string; text: string; id?: string; streaming?: boolean };
```

Тип UI-сообщения, включая ID и признак streaming; не полный Chat Completions transcript.

### `ChatSummary`

[Исходник](../../apps/desktop/src/App.tsx#L6)

```typescript
type ChatSummary = { id: string; title: string };
```

Тип метаданных чата для бокового списка.

### `App`

[Исходник](../../apps/desktop/src/App.tsx#L9)

```typescript
function App()
```

Корневой React-компонент приложения с состояниями, эффектами и обработчиками.

### `App.report`

[Исходник](../../apps/desktop/src/App.tsx#L39)

```typescript
function report(text: string)
```

Добавляет диагностическую строку, сохраняя ограниченный хвост UI-лога.

### `App.refreshChats`

[Исходник](../../apps/desktop/src/App.tsx#L40)

```typescript
async function refreshChats()
```

Запрашивает и обновляет список чатов.

### `App.refreshFiles`

[Исходник](../../apps/desktop/src/App.tsx#L89)

```typescript
async function refreshFiles(path = '.')
```

Обновляет элементы и текущий относительный каталог проводника.

### `App.chooseProject`

[Исходник](../../apps/desktop/src/App.tsx#L93)

```typescript
async function chooseProject()
```

Выбор проекта: UI → native dialog → проверяемый set_project.

### `App.openFile`

[Исходник](../../apps/desktop/src/App.tsx#L102)

```typescript
async function openFile(item: FileItem)
```

Открывает каталог или загружает текст файла в preview.

### `App.selectChat`

[Исходник](../../apps/desktop/src/App.tsx#L108)

```typescript
async function selectChat(id?: string)
```

Создаёт/загружает чат, заменяет UI-историю и checkpoint при отсутствии активной задачи.

### `App.configure`

[Исходник](../../apps/desktop/src/App.tsx#L117)

```typescript
async function configure()
```

Передаёт текущие поля модели сервису и выбрасывает ошибку при отказе.

### `App.saveSettings`

[Исходник](../../apps/desktop/src/App.tsx#L121)

```typescript
async function saveSettings()
```

Сохраняет настройки и отображает результат в output.

### `App.discoverModels`

[Исходник](../../apps/desktop/src/App.tsx#L127)

```typescript
async function discoverModels()
```

Настраивает сервер, загружает модели, выбирает ID и сохраняет выбор.

### `App.sendPrompt`

[Исходник](../../apps/desktop/src/App.tsx#L142)

```typescript
async function sendPrompt(resume = false)
```

Проверяет готовность, блокирует повторный старт, создаёт чат и отправляет задачу/продолжение.

### `App.decide`

[Исходник](../../apps/desktop/src/App.tsx#L166)

```typescript
async function decide(decision: string)
```

Защищает от повторного нажатия и отправляет решение по текущему approval.

### `App.cancel`

[Исходник](../../apps/desktop/src/App.tsx#L175)

```typescript
async function cancel()
```

Показывает состояние остановки и вызывает cancelTask.

<a id="module-apps-desktop-src-main-tsx"></a>

## `apps/desktop/src/main.tsx`

Подключает CSS, создаёт React root и отображает App в StrictMode.

Нет именованных функций/типов: модуль выполняет конфигурацию, сборочный вызов или render entry. Анонимные callbacks описаны в учебных главах.

<a id="module-apps-desktop-src-vite-env-d-ts"></a>

## `apps/desktop/src/vite-env.d.ts`

Vite reference, CoreEvent и TypeScript-контракт Window.lca.

### `CoreEvent`

[Исходник](../../apps/desktop/src/vite-env.d.ts#L2)

```typescript
type CoreEvent = { event: string; chat_id?: string; run_id?: string; [key: string]: any };
```

Общее событие Core; дополнительные поля пока описаны через any.

### `Window`

[Исходник](../../apps/desktop/src/vite-env.d.ts#L3)

```typescript
interface Window { lca: {
  health: () => Promise<any>; chooseProject: () => Promise<any>;
  listFiles: (path?: string) => Promise<any>; readFile: (path: string) => Promise<any>; systemInfo: () => Promise<any>;
  configureModel: (config: {base_url: string; model: string; api_key: string}) => Promise<any>;
  listModels: () => Promise<any>; listChats: () => Promise<any>; newChat: () => Promise<any>; loadChat: (id: string) => Promise<any>;
  getModelSettings: () => Promise<any>;
  startTask: (prompt: string, resume?: boolean) => Promise<any>; cancelTask: () => Promise<any>;
  resolveApproval: (run: string, approval: string, decision: string) => Promise<any>;
  onEvent: (callback: (event: CoreEvent) => void) => () => void;
} }
```

Расширение глобального Window контрактом фиксированного lca API.

<a id="module-apps-desktop-vite-config-ts"></a>

## `apps/desktop/vite.config.ts`

React-плагин, относительные assets, фиксированный локальный dev-порт и outDir.

Нет именованных функций/типов: модуль выполняет конфигурацию, сборочный вызов или render entry. Анонимные callbacks описаны в учебных главах.

<a id="module-tests-electron-smoke-cjs"></a>

## `tests/electron/smoke.cjs`

Скрытое настоящее Electron-окно: все слои, запись, поток, reload и Stop.

### `fail`

[Исходник](../../tests/electron/smoke.cjs#L13)

```typescript
function fail(error)
```

В smoke-тесте записывает ошибку в result.json и завершает Electron.

### `BrowserWindow.prototype.show`

[Исходник](../../tests/electron/smoke.cjs#L22)

```typescript
BrowserWindow.prototype.show()
```

Только в smoke-тесте подавляет показ настоящего окна пользователю.

### `dialog.showOpenDialog`

[Исходник](../../tests/electron/smoke.cjs#L23)

```typescript
dialog.showOpenDialog()
```

Только в smoke-тесте возвращает учебный каталог вместо настоящего системного диалога.

### `encode`

[Исходник](../../tests/electron/smoke.cjs#L41)

```typescript
encode(delta)
```

Сериализует детерминированный SSE-чанк модельной фикстуры.

### `releaseModelText`

[Исходник](../../tests/electron/smoke.cjs#L51)

```typescript
releaseModelText()
```

Завершает задержанный ответ фикстуры после проверки видимого частичного текста.

### `poll`

[Исходник](../../tests/electron/smoke.cjs#L58)

```typescript
async function poll(win, expression)
```

В тесте ожидает DOM-условие с ограничением времени.

<a id="module-tools-extract-ts-symbols-cjs"></a>

## `tools/extract_ts_symbols.cjs`

TypeScript Compiler API: структурные объявления TS/JS без исполнения приложения.

### `extract`

[Исходник](../../tools/extract_ts_symbols.cjs#L5)

```typescript
function extract(file)
```

Читает один TS/JS-файл, создаёт AST и возвращает его именованные объявления без исполнения кода.

### `extract.add`

[Исходник](../../tools/extract_ts_symbols.cjs#L8)

```typescript
function add(node, name, scope, kind, signature)
```

Добавляет структурную запись символа с квалифицированным именем, сигнатурой и строкой.

### `extract.visit`

[Исходник](../../tools/extract_ts_symbols.cjs#L12)

```typescript
function visit(node, scope = [])
```

Обходит TypeScript AST, распознавая типы, функции и именованные callbacks.
