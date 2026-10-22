# Справочник TypeScript и JavaScript

Этот файл создаётся `python tools/generate_code_reference.py`. Сигнатуры и номера строк извлечены из исходников; назначения — из ручных аннотаций. Изменяйте объяснения в `tools/doc_notes.py`, затем пересоздайте справочник.

Блоки сигнатур приводятся без тела; это справочные объявления, а не самостоятельные программы.

[К руководству](../README.md)

## Оглавление модулей

- [apps/desktop/build-electron.mjs](#module-apps-desktop-build-electron-mjs)
- [apps/desktop/electron/main.ts](#module-apps-desktop-electron-main-ts)
- [apps/desktop/electron/preload.ts](#module-apps-desktop-electron-preload-ts)
- [apps/desktop/src/App.tsx](#module-apps-desktop-src-app-tsx)
- [apps/desktop/src/ModelSettings.tsx](#module-apps-desktop-src-modelsettings-tsx)
- [apps/desktop/src/TaskProgress.tsx](#module-apps-desktop-src-taskprogress-tsx)
- [apps/desktop/src/VoicePanel.tsx](#module-apps-desktop-src-voicepanel-tsx)
- [apps/desktop/src/main.tsx](#module-apps-desktop-src-main-tsx)
- [apps/desktop/src/vite-env.d.ts](#module-apps-desktop-src-vite-env-d-ts)
- [apps/desktop/vite.config.ts](#module-apps-desktop-vite-config-ts)
- [tests/electron/packaged-smoke.mjs](#module-tests-electron-packaged-smoke-mjs)
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

### `diagnostic`

[Исходник](../../apps/desktop/electron/main.ts#L12)

```typescript
function diagnostic(message: string)
```

Добавляет только lifecycle-диагностику в ограниченный main.log; ошибка I/O не блокирует приложение.

### `publish`

[Исходник](../../apps/desktop/electron/main.ts#L21)

```typescript
function publish(message: any)
```

Передаёт Core-событие живому renderer через фиксированный core:event.

### `startBackend`

[Исходник](../../apps/desktop/electron/main.ts#L24)

```typescript
function startBackend()
```

Лениво запускает Python, подключает stdout/stderr и обработчики завершения.

### `startBackend.stopped`

[Исходник](../../apps/desktop/electron/main.ts#L43)

```typescript
stopped()
```

Однократно сбрасывает процесс, завершает pending RPC ошибкой и сообщает backend_stopped.

### `callBackend`

[Исходник](../../apps/desktop/electron/main.ts#L55)

```typescript
function callBackend(method: string, params: Record<string, unknown> = {})
```

Посылает JSON-lines запрос с ID/Promise, таймером и ограничением pending.

### `createWindow`

[Исходник](../../apps/desktop/electron/main.ts#L66)

```typescript
function createWindow()
```

Создаёт изолированное Electron-окно и подключает его жизненный цикл.

### `handle`

[Исходник](../../apps/desktop/electron/main.ts#L78)

```typescript
function handle(channel: string, handler: (...args: any[]) => any)
```

Регистрирует IPC handler с проверкой sender и mainFrame.

### `modelConfig`

[Исходник](../../apps/desktop/electron/main.ts#L92)

```typescript
function modelConfig(config: any)
```

Явно перечисляет поля model IPC, остальные поля renderer не передаёт в Core.

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
configureModel(config: { base_url: string; model: string; api_key: string; settings?: Record<string, number> })
```

Передаёт URL/модель/сеансовый ключ в фиксированный model:configure.

### `listModels`

[Исходник](../../apps/desktop/electron/preload.ts#L9)

```typescript
listModels(config?: unknown)
```

Запрашивает ID доступных моделей.

### `testModel`

[Исходник](../../apps/desktop/electron/preload.ts#L10)

```typescript
testModel(config: unknown)
```

Посылает фиксированный RPC диагностики без произвольного prompt и файлов.

### `cancelModelSetup`

[Исходник](../../apps/desktop/electron/preload.ts#L11)

```typescript
cancelModelSetup()
```

Отменяет текущую диагностику модели через отдельный фиксированный канал.

### `getModelSettings`

[Исходник](../../apps/desktop/electron/preload.ts#L12)

```typescript
getModelSettings()
```

Читает сохранённые URL/ID без ключа.

### `listChats`

[Исходник](../../apps/desktop/electron/preload.ts#L13)

```typescript
listChats(mode = 'ide')
```

Получает чаты выбранного проекта.

### `newChat`

[Исходник](../../apps/desktop/electron/preload.ts#L14)

```typescript
newChat(mode = 'ide')
```

Создаёт пустой чат проекта.

### `loadChat`

[Исходник](../../apps/desktop/electron/preload.ts#L15)

```typescript
loadChat(chatId: string, mode = 'ide')
```

Загружает проверяемый ID чата.

### `startTask`

[Исходник](../../apps/desktop/electron/preload.ts#L16)

```typescript
startTask(prompt: string, resume = false, mode = 'ide')
```

Посылает prompt и resume-флаг, получает принятие задачи.

### `cancelTask`

[Исходник](../../apps/desktop/electron/preload.ts#L17)

```typescript
cancelTask()
```

Запрашивает отмену через task:cancel.

### `resolveApproval`

[Исходник](../../apps/desktop/electron/preload.ts#L18)

```typescript
resolveApproval(runId: string, approvalId: string, decision: string)
```

Передаёт run/proposal ID и явное решение.

### `onEvent`

[Исходник](../../apps/desktop/electron/preload.ts#L19)

```typescript
onEvent(callback: (event: unknown) => void)
```

Подписывает callback на core:event и возвращает отписку.

### `onEvent.listener`

[Исходник](../../apps/desktop/electron/preload.ts#L20)

```typescript
listener(_event: Electron.IpcRendererEvent, data: unknown)
```

Адаптирует Electron event в пользовательские данные callback.

<a id="module-apps-desktop-src-app-tsx"></a>

## `apps/desktop/src/App.tsx`

React-состояние и представление проекта, настроек, чата, потока, checkpoint и diff.

### `FileItem`

[Исходник](../../apps/desktop/src/App.tsx#L7)

```typescript
type FileItem = { name: string; path: string; kind: 'file' | 'directory' };
```

Тип элемента readonly-проводника: имя, относительный путь, вид файла/каталога.

### `Message`

[Исходник](../../apps/desktop/src/App.tsx#L8)

```typescript
type Message = { role: string; text: string; id?: string; streaming?: boolean };
```

Тип UI-сообщения, включая ID и признак streaming; не полный Chat Completions transcript.

### `ChatSummary`

[Исходник](../../apps/desktop/src/App.tsx#L9)

```typescript
type ChatSummary = { id: string; title: string };
```

Тип метаданных чата для бокового списка.

### `App`

[Исходник](../../apps/desktop/src/App.tsx#L12)

```typescript
function App()
```

Корневой React-компонент приложения с состояниями, эффектами и обработчиками.

### `App.report`

[Исходник](../../apps/desktop/src/App.tsx#L45)

```typescript
function report(text: string)
```

Добавляет диагностическую строку, сохраняя ограниченный хвост UI-лога.

### `App.showWarning`

[Исходник](../../apps/desktop/src/App.tsx#L46)

```typescript
function showWarning(text: string)
```

Публикует диагностическое предупреждение в логе и чате, не добавляя одинаковый текст повторно.

### `App.refreshChats`

[Исходник](../../apps/desktop/src/App.tsx#L50)

```typescript
async function refreshChats(scope = modeRef.current)
```

Запрашивает и обновляет список чатов.

### `App.refreshFiles`

[Исходник](../../apps/desktop/src/App.tsx#L103)

```typescript
async function refreshFiles(path = '.')
```

Обновляет элементы и текущий относительный каталог проводника.

### `App.chooseProject`

[Исходник](../../apps/desktop/src/App.tsx#L107)

```typescript
async function chooseProject()
```

Выбор проекта: UI → native dialog → проверяемый set_project.

### `App.switchMode`

[Исходник](../../apps/desktop/src/App.tsx#L117)

```typescript
async function switchMode(next: WorkspaceMode)
```

Переключает Chat/IDE/voice только в idle, сбрасывает выбранный UI-чат и загружает историю соответствующей области.

### `App.openFile`

[Исходник](../../apps/desktop/src/App.tsx#L125)

```typescript
async function openFile(item: FileItem)
```

Открывает каталог или загружает текст файла в preview.

### `App.selectChat`

[Исходник](../../apps/desktop/src/App.tsx#L131)

```typescript
async function selectChat(id?: string)
```

Создаёт/загружает чат, заменяет UI-историю и checkpoint при отсутствии активной задачи.

### `App.configure`

[Исходник](../../apps/desktop/src/App.tsx#L141)

```typescript
async function configure()
```

Передаёт текущие поля модели сервису и выбрасывает ошибку при отказе.

### `App.sendPrompt`

[Исходник](../../apps/desktop/src/App.tsx#L145)

```typescript
async function sendPrompt(resume = false)
```

Проверяет готовность, блокирует повторный старт, создаёт чат и отправляет задачу/продолжение.

### `App.decide`

[Исходник](../../apps/desktop/src/App.tsx#L170)

```typescript
async function decide(decision: string)
```

Защищает от повторного нажатия и отправляет решение по текущему approval.

### `App.cancel`

[Исходник](../../apps/desktop/src/App.tsx#L179)

```typescript
async function cancel()
```

Показывает состояние остановки и вызывает cancelTask.

<a id="module-apps-desktop-src-modelsettings-tsx"></a>

## `apps/desktop/src/ModelSettings.tsx`

Модальное окно draft-настроек: endpoint, ключ, список моделей, тест ответа, генерация, лимиты, сохранение и focus trap.

### `GenerationSettings`

[Исходник](../../apps/desktop/src/ModelSettings.tsx#L4)

```typescript
export type GenerationSettings = {
  temperature: number; top_p: number; max_tokens: number; max_context_chars: number;
  request_timeout: number; max_agent_turns: number; max_runtime_minutes: number;
};
```

Числовой контракт семи применяемых настроек: sampling, token/context budgets, HTTP timeout и ограничения цикла.

### `ModelConfig`

[Исходник](../../apps/desktop/src/ModelSettings.tsx#L8)

```typescript
export type ModelConfig = { base_url: string; model: string; api_key: string; settings: GenerationSettings };
```

Конфигурация окна/IPC: URL, ID, временный API-ключ и числовые настройки.

### `ModelSettings`

[Исходник](../../apps/desktop/src/ModelSettings.tsx#L23)

```typescript
function ModelSettings({ initial, busy, onSaved, onClose }: {
  initial: ModelConfig; busy: boolean; onSaved: (config: ModelConfig) => void; onClose: () => void;
})
```

Модальное окно с отдельным draft; применяет настройки только после успешного backend save.

### `ModelSettings.change`

[Исходник](../../apps/desktop/src/ModelSettings.tsx#L39)

```typescript
function change(key: K, value: ModelConfig[K])
```

Меняет поле черновика и помечает его несохранённым; новый URL сбрасывает устаревший список моделей.

### `ModelSettings.validate`

[Исходник](../../apps/desktop/src/ModelSettings.tsx#L44)

```typescript
function validate()
```

Проверяет URL и диапазоны полей до отправки, backend повторяет обязательную валидацию.

### `ModelSettings.perform`

[Исходник](../../apps/desktop/src/ModelSettings.tsx#L56)

```typescript
async function perform(action: 'discover' | 'probe' | 'save')
```

Последовательно выполняет discovery, bounded probe или save с явным статусом и обработкой ошибок в окне.

### `ModelSettings.resetGeneration`

[Исходник](../../apps/desktop/src/ModelSettings.tsx#L83)

```typescript
function resetGeneration()
```

Возвращает числовые поля к defaults только в черновике, не меняет endpoint/ID/ключ.

### `ModelSettings.handleKeys`

[Исходник](../../apps/desktop/src/ModelSettings.tsx#L86)

```typescript
function handleKeys(event: React.KeyboardEvent<HTMLElement>)
```

Закрывает окно по Escape вне операции и удерживает Tab-навигацию в доступных контролах диалога.

<a id="module-apps-desktop-src-taskprogress-tsx"></a>

## `apps/desktop/src/TaskProgress.tsx`

Типизированная панель этапов, инструментов, результатов и продолжения задачи.

### `TaskStage`

[Исходник](../../apps/desktop/src/TaskProgress.tsx#L3)

```typescript
export type TaskStage = { id: string; title: string; objective?: string; status: string };
```

UI-представление этапа: идентификатор, название, цель и статус исполнения.

### `ToolActivity`

[Исходник](../../apps/desktop/src/TaskProgress.tsx#L4)

```typescript
export type ToolActivity = { id: number; tool: string; path: string; status: string; summary: string; stage: string };
```

UI-проекция метаданных tool: устойчивый ID, путь, этап, статус и сводка без raw content.

### `TaskSnapshot`

[Исходник](../../apps/desktop/src/TaskProgress.tsx#L5)

```typescript
export type TaskSnapshot = {
  status: string; last_event: string; stage: string; turn: number; tool_calls: number;
  stages: TaskStage[]; tool_activity?: ToolActivity[]; activity_omitted?: number;
  modified_files?: string[]; stop_reason?: string;
};
```

Тип полей checkpoint, используемых панелью плана и результатов.

### `TaskProgress`

[Исходник](../../apps/desktop/src/TaskProgress.tsx#L18)

```typescript
function TaskProgress({ task, busy, onResume }: { task: TaskSnapshot; busy: boolean; onResume: () => void })
```

Показывает посещённые/пропущенные этапы, последние операции, изменённые файлы, остановку и кнопку resume.

<a id="module-apps-desktop-src-voicepanel-tsx"></a>

## `apps/desktop/src/VoicePanel.tsx`

Подготовительный экран голосового ассистента: SVG-эскиз горничной, честные состояния отсутствующих STT/TTS и контракты будущей сессии; аудио пока не записывает.

### `WorkspaceMode`

[Исходник](../../apps/desktop/src/VoicePanel.tsx#L3)

```typescript
export type WorkspaceMode = 'chat' | 'ide' | 'voice';
```

Три пространства интерфейса: обычный разговор, работа с проектом и будущий голосовой ассистент.

### `VoiceSessionState`

[Исходник](../../apps/desktop/src/VoicePanel.tsx#L5)

```typescript
export type VoiceSessionState = 'disconnected' | 'listening' | 'thinking' | 'speaking' | 'error';
```

Будущие состояния аудиосессии: отключена, слушает, думает, говорит, ошибка; сейчас backend не реализован.

### `VoiceProfile`

[Исходник](../../apps/desktop/src/VoicePanel.tsx#L6)

```typescript
export interface VoiceProfile {
  persona: string;
  transcriptionProvider: string | null;
  speechProvider: string | null;
  pushToTalk: boolean;
}
```

Контракт будущих настроек персоны, STT/TTS провайдеров и push-to-talk; пока не сохраняется и не используется как рабочая функция.

### `VoicePanel`

[Исходник](../../apps/desktop/src/VoicePanel.tsx#L13)

```typescript
function VoicePanel({ onChat }: { onChat: () => void })
```

Рисует эскиз горничной и карточки ещё не подключённых голосовых возможностей, предлагает перейти в Chat.

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
  configureModel: (config: {base_url: string; model: string; api_key: string; settings?: Record<string, number>}) => Promise<any>;
  listModels: (config?: unknown) => Promise<any>; listChats: (mode?: string) => Promise<any>; newChat: (mode?: string) => Promise<any>; loadChat: (id: string, mode?: string) => Promise<any>;
  testModel: (config: unknown) => Promise<any>; cancelModelSetup: () => Promise<any>;
  getModelSettings: () => Promise<any>;
  startTask: (prompt: string, resume?: boolean, mode?: string) => Promise<any>; cancelTask: () => Promise<any>;
  resolveApproval: (run: string, approval: string, decision: string) => Promise<any>;
  onEvent: (callback: (event: CoreEvent) => void) => () => void;
} }
```

Расширение глобального Window контрактом фиксированного lca API.

<a id="module-apps-desktop-vite-config-ts"></a>

## `apps/desktop/vite.config.ts`

React-плагин, относительные assets, фиксированный локальный dev-порт и outDir.

Нет именованных функций/типов: модуль выполняет конфигурацию, сборочный вызов или render entry. Анонимные callbacks описаны в учебных главах.

<a id="module-tests-electron-packaged-smoke-mjs"></a>

## `tests/electron/packaged-smoke.mjs`

CDP-проверка настоящего packaged exe с урезанным PATH, discovery и повторным запуском.

### `freePort`

[Исходник](../../tests/electron/packaged-smoke.mjs#L10)

```typescript
async function freePort()
```

Резервирует свободный loopback-порт для тестового Chromium CDP.

### `connectPage`

[Исходник](../../tests/electron/packaged-smoke.mjs#L18)

```typescript
async function connectPage(port, child)
```

Ожидает file renderer настоящего exe и открывает WebSocket CDP с ограниченным временем.

### `evaluate`

[Исходник](../../tests/electron/packaged-smoke.mjs#L35)

```typescript
function evaluate(socket, expression)
```

Последовательно исполняет одно тестовое выражение через CDP с тайм-аутом.

### `evaluate.receive`

[Исходник](../../tests/electron/packaged-smoke.mjs#L38)

```typescript
receive(event)
```

Сопоставляет CDP response с запросом и возвращает значение либо ошибку JavaScript.

### `run`

[Исходник](../../tests/electron/packaged-smoke.mjs#L50)

```typescript
async function run(executable, directory, first, modelUrl)
```

Запускает packaged exe с изолированными данными/урезанным PATH и проверяет Core, настройки и нормальное закрытие.

### `main`

[Исходник](../../tests/electron/packaged-smoke.mjs#L90)

```typescript
async function main()
```

Поднимает HTTP-фикстуру, дважды проверяет пакет и отсутствие ключа в настройках/диагностике.

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

[Исходник](../../tests/electron/smoke.cjs#L54)

```typescript
releaseModelText()
```

Завершает задержанный ответ фикстуры после проверки видимого частичного текста.

### `poll`

[Исходник](../../tests/electron/smoke.cjs#L61)

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
