# Справочник TypeScript и JavaScript

Этот файл создаётся `python tools/generate_code_reference.py`. Сигнатуры и номера строк извлечены из исходников; назначения — из ручных аннотаций. Изменяйте объяснения в `tools/doc_notes.py`, затем пересоздайте справочник.

Блоки сигнатур приводятся без тела; это справочные объявления, а не самостоятельные программы.

[К руководству](../README.md)

## Оглавление модулей

- [apps/desktop/build-electron.mjs](#module-apps-desktop-build-electron-mjs)
- [apps/desktop/electron/main.ts](#module-apps-desktop-electron-main-ts)
- [apps/desktop/electron/preload.ts](#module-apps-desktop-electron-preload-ts)
- [apps/desktop/src/App.tsx](#module-apps-desktop-src-app-tsx)
- [apps/desktop/src/ChatText.tsx](#module-apps-desktop-src-chattext-tsx)
- [apps/desktop/src/CompanionSettings.tsx](#module-apps-desktop-src-companionsettings-tsx)
- [apps/desktop/src/ConnectionsSettings.tsx](#module-apps-desktop-src-connectionssettings-tsx)
- [apps/desktop/src/EditorPanel.tsx](#module-apps-desktop-src-editorpanel-tsx)
- [apps/desktop/src/LocalRuntimePanel.tsx](#module-apps-desktop-src-localruntimepanel-tsx)
- [apps/desktop/src/MemoryPanel.tsx](#module-apps-desktop-src-memorypanel-tsx)
- [apps/desktop/src/ModelSettings.tsx](#module-apps-desktop-src-modelsettings-tsx)
- [apps/desktop/src/ProjectSearch.tsx](#module-apps-desktop-src-projectsearch-tsx)
- [apps/desktop/src/TaskProgress.tsx](#module-apps-desktop-src-taskprogress-tsx)
- [apps/desktop/src/VoicePanel.tsx](#module-apps-desktop-src-voicepanel-tsx)
- [apps/desktop/src/main.tsx](#module-apps-desktop-src-main-tsx)
- [apps/desktop/src/microphone.ts](#module-apps-desktop-src-microphone-ts)
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

### `bundledRuntimePath`

[Исходник](../../apps/desktop/electron/main.ts#L16)

```typescript
function bundledRuntimePath()
```

Находит включённый CPU llama-server в resources packaged приложения или в build для разработки; не принимает путь от renderer.

### `diagnostic`

[Исходник](../../apps/desktop/electron/main.ts#L23)

```typescript
function diagnostic(message: string)
```

Добавляет только lifecycle-диагностику в ограниченный main.log; ошибка I/O не блокирует приложение.

### `desktopRequest`

[Исходник](../../apps/desktop/electron/main.ts#L32)

```typescript
async function desktopRequest(message:any)
```

Исполняет только screenshot или фиксированный DuckDuckGo search URL, публикует локальный preview и отвечает Core по одноразовому UUID.

### `publish`

[Исходник](../../apps/desktop/electron/main.ts#L49)

```typescript
function publish(message: any)
```

Передаёт Core-событие живому renderer через фиксированный core:event.

### `startBackend`

[Исходник](../../apps/desktop/electron/main.ts#L52)

```typescript
function startBackend()
```

Лениво запускает Python, подключает stdout/stderr и обработчики завершения.

### `startBackend.stopped`

[Исходник](../../apps/desktop/electron/main.ts#L71)

```typescript
stopped()
```

Однократно сбрасывает процесс, завершает pending RPC ошибкой и сообщает backend_stopped.

### `callBackend`

[Исходник](../../apps/desktop/electron/main.ts#L83)

```typescript
function callBackend(method: string, params: Record<string, unknown> = {})
```

Посылает JSON-lines запрос с ID/Promise, таймером и ограничением pending.

### `createWindow`

[Исходник](../../apps/desktop/electron/main.ts#L95)

```typescript
function createWindow()
```

Создаёт изолированное Electron-окно и подключает его жизненный цикл.

### `handle`

[Исходник](../../apps/desktop/electron/main.ts#L132)

```typescript
function handle(channel: string, handler: (...args: any[]) => any)
```

Регистрирует IPC handler с проверкой sender и mainFrame.

### `modelConfig`

[Исходник](../../apps/desktop/electron/main.ts#L146)

```typescript
function modelConfig(config: any)
```

Явно перечисляет поля model IPC, остальные поля renderer не передаёт в Core.

### `confirmEditorDiscard`

[Исходник](../../apps/desktop/electron/main.ts#L149)

```typescript
async function confirmEditorDiscard()
```

Показывает нативное предупреждение с безопасным default Cancel; возвращает только явный отказ от сохранения.

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

### `pickRuntimeFile`

[Исходник](../../apps/desktop/electron/preload.ts#L7)

```typescript
pickRuntimeFile(kind:string)
```

Вызывает системный выбор GGUF или установленного llama-server.

### `startRuntime`

[Исходник](../../apps/desktop/electron/preload.ts#L8)

```typescript
startRuntime(params:unknown)
```

Передаёт только context/GPU; пути берутся main из предыдущего file picker.

### `runtimeStatus`

[Исходник](../../apps/desktop/electron/preload.ts#L9)

```typescript
runtimeStatus()
```

Читает lifecycle собственного сервера без управления внешним LM Studio.

### `stopRuntime`

[Исходник](../../apps/desktop/electron/preload.ts#L10)

```typescript
stopRuntime()
```

Останавливает только собственный локальный runtime через фиксированный IPC.

### `getProjectMemory`

[Исходник](../../apps/desktop/electron/preload.ts#L11)

```typescript
getProjectMemory()
```

Читает семь полей и byte revision памяти текущего проекта.

### `saveProjectMemory`

[Исходник](../../apps/desktop/electron/preload.ts#L12)

```typescript
saveProjectMemory(memory:unknown, revision:string)
```

Передаёт editable memory и исходную revision для конфликтобезопасной записи.

### `renameChat`

[Исходник](../../apps/desktop/electron/preload.ts#L13)

```typescript
renameChat(id:string, title:string, mode:string)
```

Фиксированный IPC переименования ID/title/mode без изменения сообщений.

### `telegramStatus`

[Исходник](../../apps/desktop/electron/preload.ts#L14)

```typescript
telegramStatus()
```

Читает безопасный статус бота без token и HTTP URL.

### `connectTelegram`

[Исходник](../../apps/desktop/electron/preload.ts#L15)

```typescript
connectTelegram(params:unknown)
```

Подключает token/owner либо явно выбранную защищённую локальную запись; секрет не возвращается renderer.

### `disconnectTelegram`

[Исходник](../../apps/desktop/electron/preload.ts#L16)

```typescript
disconnectTelegram()
```

Отключает polling бота через Core.

### `forgetTelegram`

[Исходник](../../apps/desktop/electron/preload.ts#L17)

```typescript
forgetTelegram()
```

Удаляет только сохранённую encrypted запись токена по явной кнопке пользователя.

### `desktopSettings`

[Исходник](../../apps/desktop/electron/preload.ts#L18)

```typescript
desktopSettings()
```

Читает opt-in состояние PC tools без доступа к файлам.

### `configureDesktop`

[Исходник](../../apps/desktop/electron/preload.ts#L19)

```typescript
configureDesktop(enabled:boolean)
```

Включает/выключает PC tools; аргументы модели не могут изменить это разрешение.

### `moveChat`

[Исходник](../../apps/desktop/electron/preload.ts#L20)

```typescript
moveChat(chat_id:string, mode:string, target:string)
```

Переносит только Chat/voice историю в другую область по явному действию пользователя.

### `cancelHandoff`

[Исходник](../../apps/desktop/electron/preload.ts#L21)

```typescript
cancelHandoff(id:string)
```

Отклоняет pending передачу Мии по точному ID без запуска основной модели.

### `prepareHandoff`

[Исходник](../../apps/desktop/electron/preload.ts#L22)

```typescript
prepareHandoff(id:string)
```

Переносит pending задание Мии в новый чат основной модели по точному ID.

### `getCompanionSettings`

[Исходник](../../apps/desktop/electron/preload.ts#L23)

```typescript
getCompanionSettings()
```

Читает независимый публичный профиль Мии через allowlisted IPC.

### `configureCompanion`

[Исходник](../../apps/desktop/electron/preload.ts#L24)

```typescript
configureCompanion(params:unknown)
```

Сохраняет настройки Мии отдельно от основной модели и оставляет секреты только в памяти Core.

### `transcribe`

[Исходник](../../apps/desktop/electron/preload.ts#L25)

```typescript
transcribe(audio:string)
```

Передаёт ограниченную base64 WAV-запись в отменяемый STT RPC.

### `cancelTranscription`

[Исходник](../../apps/desktop/electron/preload.ts#L26)

```typescript
cancelTranscription()
```

Отменяет текущую транскрипцию и закрывает её сокет.

### `voiceStatus`

[Исходник](../../apps/desktop/electron/preload.ts#L27)

```typescript
voiceStatus()
```

Читает состояние системной озвучки через фиксированный IPC.

### `refreshVoices`

[Исходник](../../apps/desktop/electron/preload.ts#L28)

```typescript
refreshVoices()
```

Перечисляет системные голоса/распознаватели без запроса микрофона.

### `speak`

[Исходник](../../apps/desktop/electron/preload.ts#L29)

```typescript
speak(params:unknown)
```

Передаёт только text/voice/rate/volume для plain TTS; пути/PowerShell code не принимаются.

### `stopVoice`

[Исходник](../../apps/desktop/electron/preload.ts#L30)

```typescript
stopVoice()
```

Запрашивает отмену собственного speech worker.

### `searchProject`

[Исходник](../../apps/desktop/electron/preload.ts#L31)

```typescript
searchProject(params: unknown)
```

Вызывает фиксированный read-only IPC поиска с текстом/маской/регистром.

### `cancelProjectSearch`

[Исходник](../../apps/desktop/electron/preload.ts#L32)

```typescript
cancelProjectSearch()
```

Отменяет поиск независимо от остановки агента.

### `editorRead`

[Исходник](../../apps/desktop/electron/preload.ts#L33)

```typescript
editorRead(path: string)
```

Вызывает отдельное strict editor_read через фиксированный IPC.

### `editorPreview`

[Исходник](../../apps/desktop/electron/preload.ts#L34)

```typescript
editorPreview(path: string, content: string, revision: unknown)
```

Передаёт draft и исходную revision для preview без записи.

### `editorResolve`

[Исходник](../../apps/desktop/electron/preload.ts#L35)

```typescript
editorResolve(proposalId: string, decision: string)
```

Передаёт только proposal ID и явное решение, не произвольную команду записи.

### `setEditorDirty`

[Исходник](../../apps/desktop/electron/preload.ts#L36)

```typescript
setEditorDirty(dirty: boolean)
```

Сообщает main о несохранённых вкладках для защиты закрытия окна.

### `confirmEditorDiscard`

[Исходник](../../apps/desktop/electron/preload.ts#L37)

```typescript
confirmEditorDiscard()
```

Показывает нативное предупреждение с безопасным default Cancel; возвращает только явный отказ от сохранения.

### `systemInfo`

[Исходник](../../apps/desktop/electron/preload.ts#L38)

```typescript
systemInfo()
```

Preload-запрос home/platform у main, без tool модели.

### `configureModel`

[Исходник](../../apps/desktop/electron/preload.ts#L39)

```typescript
configureModel(config: { base_url: string; model: string; api_key: string; settings?: Record<string, number> })
```

Передаёт URL/модель/сеансовый ключ в фиксированный model:configure.

### `listModels`

[Исходник](../../apps/desktop/electron/preload.ts#L40)

```typescript
listModels(config?: unknown)
```

Запрашивает ID доступных моделей.

### `testModel`

[Исходник](../../apps/desktop/electron/preload.ts#L41)

```typescript
testModel(config: unknown)
```

Посылает фиксированный RPC диагностики без произвольного prompt и файлов.

### `cancelModelSetup`

[Исходник](../../apps/desktop/electron/preload.ts#L42)

```typescript
cancelModelSetup()
```

Отменяет текущую диагностику модели через отдельный фиксированный канал.

### `getModelSettings`

[Исходник](../../apps/desktop/electron/preload.ts#L43)

```typescript
getModelSettings()
```

Читает сохранённые URL/ID без ключа.

### `listChats`

[Исходник](../../apps/desktop/electron/preload.ts#L44)

```typescript
listChats(mode = 'ide')
```

Получает чаты выбранного проекта.

### `newChat`

[Исходник](../../apps/desktop/electron/preload.ts#L45)

```typescript
newChat(mode = 'ide')
```

Создаёт пустой чат проекта.

### `loadChat`

[Исходник](../../apps/desktop/electron/preload.ts#L46)

```typescript
loadChat(chatId: string, mode = 'ide')
```

Загружает проверяемый ID чата.

### `startTask`

[Исходник](../../apps/desktop/electron/preload.ts#L47)

```typescript
startTask(prompt: string, resume = false, mode = 'ide')
```

Посылает prompt и resume-флаг, получает принятие задачи.

### `cancelTask`

[Исходник](../../apps/desktop/electron/preload.ts#L48)

```typescript
cancelTask()
```

Запрашивает отмену через task:cancel.

### `resolveApproval`

[Исходник](../../apps/desktop/electron/preload.ts#L49)

```typescript
resolveApproval(runId: string, approvalId: string, decision: string)
```

Передаёт run/proposal ID и явное решение.

### `onEvent`

[Исходник](../../apps/desktop/electron/preload.ts#L50)

```typescript
onEvent(callback: (event: unknown) => void)
```

Подписывает callback на core:event и возвращает отписку.

### `onEvent.listener`

[Исходник](../../apps/desktop/electron/preload.ts#L51)

```typescript
listener(_event: Electron.IpcRendererEvent, data: unknown)
```

Адаптирует Electron event в пользовательские данные callback.

<a id="module-apps-desktop-src-app-tsx"></a>

## `apps/desktop/src/App.tsx`

React-состояние и представление проекта, настроек, чата, потока, checkpoint и diff.

### `FileItem`

[Исходник](../../apps/desktop/src/App.tsx#L11)

```typescript
type FileItem = { name: string; path: string; kind: 'file' | 'directory' };
```

Тип элемента readonly-проводника: имя, относительный путь, вид файла/каталога.

### `Message`

[Исходник](../../apps/desktop/src/App.tsx#L12)

```typescript
type Message = { role: string; text: string; id?: string; streaming?: boolean };
```

Тип UI-сообщения, включая ID и признак streaming; не полный Chat Completions transcript.

### `ChatSummary`

[Исходник](../../apps/desktop/src/App.tsx#L13)

```typescript
type ChatSummary = { id: string; title: string };
```

Тип метаданных чата для бокового списка.

### `App`

[Исходник](../../apps/desktop/src/App.tsx#L16)

```typescript
function App()
```

Корневой React-компонент приложения с состояниями, эффектами и обработчиками.

### `App.report`

[Исходник](../../apps/desktop/src/App.tsx#L62)

```typescript
function report(text: string)
```

Добавляет диагностическую строку, сохраняя ограниченный хвост UI-лога.

### `App.showWarning`

[Исходник](../../apps/desktop/src/App.tsx#L63)

```typescript
function showWarning(text: string)
```

Публикует диагностическое предупреждение в логе и чате, не добавляя одинаковый текст повторно.

### `App.refreshChats`

[Исходник](../../apps/desktop/src/App.tsx#L67)

```typescript
async function refreshChats(scope = modeRef.current)
```

Запрашивает и обновляет список чатов.

### `App.shortcuts`

[Исходник](../../apps/desktop/src/App.tsx#L126)

```typescript
function shortcuts(event:KeyboardEvent)
```

Обрабатывает Ctrl+S/F/G/Shift+R только в видимом editor и вне модальных диалогов.

### `App.openSearchFile`

[Исходник](../../apps/desktop/src/App.tsx#L137)

```typescript
async function openSearchFile(path:string, line:number)
```

Переходит в IDE и открывает результат на нужной строке, сохраняя sidebar поиска.

### `App.refreshFiles`

[Исходник](../../apps/desktop/src/App.tsx#L144)

```typescript
async function refreshFiles(path = '.')
```

Обновляет элементы и текущий относительный каталог проводника.

### `App.chooseProject`

[Исходник](../../apps/desktop/src/App.tsx#L148)

```typescript
async function chooseProject()
```

Выбор проекта: UI → native dialog → проверяемый set_project.

### `App.switchMode`

[Исходник](../../apps/desktop/src/App.tsx#L161)

```typescript
async function switchMode(next: WorkspaceMode)
```

Переключает Chat/IDE/voice только в idle, сбрасывает выбранный UI-чат и загружает историю соответствующей области.

### `App.openFile`

[Исходник](../../apps/desktop/src/App.tsx#L170)

```typescript
async function openFile(item: FileItem)
```

Открывает каталог или загружает текст файла в preview.

### `App.selectChat`

[Исходник](../../apps/desktop/src/App.tsx#L175)

```typescript
async function selectChat(id?: string)
```

Создаёт/загружает чат, заменяет UI-историю и checkpoint при отсутствии активной задачи.

### `App.moveChat`

[Исходник](../../apps/desktop/src/App.tsx#L186)

```typescript
async function moveChat(id:string)
```

Переносит выбранный личный чат в область Мии или обратно и обновляет текущий список.

### `App.returnToMiya`

[Исходник](../../apps/desktop/src/App.tsx#L190)

```typescript
async function returnToMiya()
```

Загружает исходный voice чат с добавленным результатом основной модели.

### `App.declineHandoff`

[Исходник](../../apps/desktop/src/App.tsx#L195)

```typescript
async function declineHandoff()
```

Очищает pending передачу и в Core, и в интерфейсе; старое задание больше не блокирует следующее.

### `App.acceptHandoff`

[Исходник](../../apps/desktop/src/App.tsx#L200)

```typescript
async function acceptHandoff()
```

Создаёт основную задачу из pending передачи, синхронизирует mode/chat/run refs и запускает модель.

### `App.renameChat`

[Исходник](../../apps/desktop/src/App.tsx#L216)

```typescript
async function renameChat()
```

Отправляет переименование выбранного chat ID в текущем scope и обновляет список после успешного сохранения.

### `App.configure`

[Исходник](../../apps/desktop/src/App.tsx#L225)

```typescript
async function configure()
```

Передаёт текущие поля модели сервису и выбрасывает ошибку при отказе.

### `App.sendPrompt`

[Исходник](../../apps/desktop/src/App.tsx#L229)

```typescript
async function sendPrompt(resume = false, voiceText?:string)
```

Проверяет готовность, блокирует повторный старт, создаёт чат и отправляет задачу/продолжение.

### `App.decide`

[Исходник](../../apps/desktop/src/App.tsx#L255)

```typescript
async function decide(decision: string)
```

Передаёт явное решение по текущему approval агента, защищая от повторных кликов.

### `App.cancel`

[Исходник](../../apps/desktop/src/App.tsx#L264)

```typescript
async function cancel()
```

Показывает состояние остановки и вызывает cancelTask.

<a id="module-apps-desktop-src-chattext-tsx"></a>

## `apps/desktop/src/ChatText.tsx`

Безопасные текстовые/code блоки без HTML, memoized parser и явное копирование.

### `TextPart`

[Исходник](../../apps/desktop/src/ChatText.tsx#L3)

```typescript
export type TextPart={code:boolean;text:string;language:string};
```

Один plain/code сегмент безопасного текстового renderer с подписью языка.

### `splitCodeBlocks`

[Исходник](../../apps/desktop/src/ChatText.tsx#L4)

```typescript
function splitCodeBlocks(text:string): TextPart[]
```

Линейно разбирает отдельные тройные backtick fences, включая незакрытый streaming code block; HTML не интерпретируется.

### `splitCodeBlocks.flush`

[Исходник](../../apps/desktop/src/ChatText.tsx#L7)

```typescript
function flush()
```

Добавляет накопленные строки текущего сегмента и очищает буфер.

### `ChatText`

[Исходник](../../apps/desktop/src/ChatText.tsx#L15)

```typescript
function ChatText({text}:{text:string})
```

Memoizes разбор текста, выводит code как React text nodes и показывает кнопку копирования.

### `ChatText.copy`

[Исходник](../../apps/desktop/src/ChatText.tsx#L19)

```typescript
async function copy(value:string, index:number)
```

Пишет только выбранный code segment через Clipboard API и показывает успех/ошибку.

<a id="module-apps-desktop-src-companionsettings-tsx"></a>

## `apps/desktop/src/CompanionSettings.tsx`

Настройка характера, независимой модели, JSON/native protocol, автоматической передачи и STT Мии.

### `CompanionSettings`

[Исходник](../../apps/desktop/src/CompanionSettings.tsx#L3)

```typescript
function CompanionSettings({profile,busy,onSaved}:{profile:any;busy:boolean;onSaved:(profile:any)=>void})
```

Форма собственного характера, модели, tool protocol, автоматической передачи и STT профиля Мии.

### `CompanionSettings.save`

[Исходник](../../apps/desktop/src/CompanionSettings.tsx#L8)

```typescript
async function save()
```

Валидирует профиль в Core, сохраняет публичные настройки, не сохраняет API keys.

### `CompanionSettings.discover`

[Исходник](../../apps/desktop/src/CompanionSettings.tsx#L16)

```typescript
async function discover()
```

Загружает модели именно с чернового endpoint Мии без изменения основной конфигурации.

<a id="module-apps-desktop-src-connectionssettings-tsx"></a>

## `apps/desktop/src/ConnectionsSettings.tsx`

Настройка PC-инструментов и Telegram; явное подключение владельца и защищённое сохранение токена.

### `ConnectionsSettings`

[Исходник](../../apps/desktop/src/ConnectionsSettings.tsx#L3)

```typescript
function ConnectionsSettings({busy}:{busy:boolean})
```

Настройка opt-in инструментов ПК и owner-only Telegram подключения с защищённым сохранением токена.

### `ConnectionsSettings.refresh`

[Исходник](../../apps/desktop/src/ConnectionsSettings.tsx#L14)

```typescript
refresh()
```

Обновляет безопасный статус Telegram с cleanup при закрытии настроек.

### `ConnectionsSettings.toggle`

[Исходник](../../apps/desktop/src/ConnectionsSettings.tsx#L18)

```typescript
async function toggle()
```

Применяет переключатель PC tools через Core только вне задачи.

### `ConnectionsSettings.connect`

[Исходник](../../apps/desktop/src/ConnectionsSettings.tsx#L22)

```typescript
async function connect(saved=false)
```

Передаёт token/owner и флаг remember/use_saved; очищает поле token после подключения.

<a id="module-apps-desktop-src-editorpanel-tsx"></a>

## `apps/desktop/src/EditorPanel.tsx`

Рабочие вкладки/черновики редактора, виртуальный gutter, поиск/строка, hotkeys, reload и подтверждённое сохранение.

### `EditorDocument`

[Исходник](../../apps/desktop/src/EditorPanel.tsx#L4)

```typescript
export type EditorDocument = {path:string; content:string; original:string; revision:{path:string; sha256:string}; newline:string};
```

Документ вкладки: текущий текст, исходный текст, byte revision и стиль строк.

### `EditorHandle`

[Исходник](../../apps/desktop/src/EditorPanel.tsx#L5)

```typescript
export type EditorHandle = {
  open: (path:string, line?:number) => Promise<string | undefined>;
  refresh: (path:string) => Promise<void>;
  reset: () => void;
  hasDirty: () => boolean;
};
```

Узкая ref-поверхность open/refresh/reset/hasDirty, сохраняющая drafts при переключении режимов.

### `EditorProps`

[Исходник](../../apps/desktop/src/EditorPanel.tsx#L11)

```typescript
type EditorProps = {root:string; busy:boolean; visible:boolean; onActive:(path:string)=>void;
  onDirty:(dirty:boolean)=>void; onProject:()=>void; onModels:()=>void; onLog:(text:string)=>void};
```

Корень/видимость/busy и callbacks редактора; file access остаётся в Core.

### `EditorPanel`

[Исходник](../../apps/desktop/src/EditorPanel.tsx#L14)

```typescript
EditorPanel(props, ref)
```

Компонент редактора с сохраняемыми между режимами вкладками и snapshot-approval.

### `EditorPanel.reset`

[Исходник](../../apps/desktop/src/EditorPanel.tsx#L58)

```typescript
function reset()
```

Сбрасывает editor-вкладки, pending diff и уведомления после подтверждённой смены проекта.

### `EditorPanel.selectDocument`

[Исходник](../../apps/desktop/src/EditorPanel.tsx#L61)

```typescript
function selectDocument(document:EditorDocument)
```

Добавляет или заменяет документ вкладки и выбирает его активным.

### `EditorPanel.read`

[Исходник](../../apps/desktop/src/EditorPanel.tsx#L66)

```typescript
async function read(path:string)
```

Запрашивает strict editor_read и отбрасывает ответ, относящийся к уже сменившемуся корню.

### `EditorPanel.open`

[Исходник](../../apps/desktop/src/EditorPanel.tsx#L73)

```typescript
async function open(path:string, line?:number)
```

Открывает существующую вкладку без потери draft либо читает файл; может перейти к нужной строке.

### `EditorPanel.refresh`

[Исходник](../../apps/desktop/src/EditorPanel.tsx#L86)

```typescript
async function refresh(path:string)
```

Обновляет только чистую вкладку после записи агента, dirty draft сохраняет и предупреждает о конфликте.

### `EditorPanel.hasDirty`

[Исходник](../../apps/desktop/src/EditorPanel.tsx#L95)

```typescript
hasDirty()
```

Читает актуальные editor tabs через ref для проверки unsaved перед нативной сменой проекта.

### `EditorPanel.closeTab`

[Исходник](../../apps/desktop/src/EditorPanel.tsx#L97)

```typescript
async function closeTab(path:string)
```

Закрывает вкладку; грязный текст требует явного подтверждения отказа от сохранения.

### `EditorPanel.reload`

[Исходник](../../apps/desktop/src/EditorPanel.tsx#L105)

```typescript
async function reload()
```

Перечитывает активный файл после подтверждения потери draft; при ошибке текст остаётся.

### `EditorPanel.save`

[Исходник](../../apps/desktop/src/EditorPanel.tsx#L111)

```typescript
async function save()
```

Получает preview по исходной byte revision, не пишет файл и показывает отдельный диалог.

### `EditorPanel.decide`

[Исходник](../../apps/desktop/src/EditorPanel.tsx#L122)

```typescript
async function decide(decision:string)
```

Потребляет editor proposal через Apply/Reject/Cancel; при отказе или конфликте сохраняет draft, после успеха обновляет revision.

### `EditorPanel.updatePosition`

[Исходник](../../apps/desktop/src/EditorPanel.tsx#L136)

```typescript
function updatePosition()
```

Вычисляет line/column по положению selectionStart в UTF-16 textarea.

### `EditorPanel.moveToLine`

[Исходник](../../apps/desktop/src/EditorPanel.tsx#L142)

```typescript
function moveToLine(line:number)
```

Ограничивает номер строки, вычисляет offset и перемещает курсор/прокрутку.

### `EditorPanel.findNext`

[Исходник](../../apps/desktop/src/EditorPanel.tsx#L151)

```typescript
function findNext()
```

Ищет следующую текстовую строку без учёта регистра с циклическим возвратом в начало файла.

### `EditorPanel.shortcuts`

[Исходник](../../apps/desktop/src/EditorPanel.tsx#L162)

```typescript
function shortcuts(event:KeyboardEvent)
```

Обрабатывает Ctrl+S/F/G/Shift+R только в видимом editor и вне модальных диалогов.

<a id="module-apps-desktop-src-localruntimepanel-tsx"></a>

## `apps/desktop/src/LocalRuntimePanel.tsx`

Реальный GGUF picker, context/GPU, lifecycle status и явный перенос endpoint в настройки.

### `LocalRuntimePanel`

[Исходник](../../apps/desktop/src/LocalRuntimePanel.tsx#L3)

```typescript
function LocalRuntimePanel({locked,onUse}:{locked:boolean;onUse:(url:string,model:string)=>void})
```

Панель собственного GGUF с file picker, реальным lifecycle и явным переносом endpoint без сохранения.

### `LocalRuntimePanel.refresh`

[Исходник](../../apps/desktop/src/LocalRuntimePanel.tsx#L18)

```typescript
async function refresh()
```

Раз в секунду читает runtime status и игнорирует ответ после unmount.

### `LocalRuntimePanel.pick`

[Исходник](../../apps/desktop/src/LocalRuntimePanel.tsx#L25)

```typescript
async function pick(kind:'model'|'runtime')
```

Получает только выбранный системным диалогом путь GGUF/runtime; отмена не меняет выбор.

### `LocalRuntimePanel.control`

[Исходник](../../apps/desktop/src/LocalRuntimePanel.tsx#L29)

```typescript
async function control(start:boolean)
```

Отправляет start/stop собственного сервера и показывает ошибку без блокировки настроек на время загрузки.

<a id="module-apps-desktop-src-memorypanel-tsx"></a>

## `apps/desktop/src/MemoryPanel.tsx`

Редактор семи полей памяти выбранного проекта с сохранением draft при конфликте.

### `MemoryPanel`

[Исходник](../../apps/desktop/src/MemoryPanel.tsx#L13)

```typescript
function MemoryPanel({root,busy,onClose}:{root:string;busy:boolean;onClose:()=>void})
```

Модальный редактор ограниченной памяти IDE; Chat не использует эти заметки.

### `MemoryPanel.show`

[Исходник](../../apps/desktop/src/MemoryPanel.tsx#L21)

```typescript
function show(result:any)
```

Проверяет ответ/корень, преобразует списки в строки и фиксирует original/revision после успешного чтения или записи.

### `MemoryPanel.save`

[Исходник](../../apps/desktop/src/MemoryPanel.tsx#L32)

```typescript
async function save()
```

Преобразует строки списков, отправляет snapshot revision, при конфликте сохраняет draft в окне.

### `MemoryPanel.close`

[Исходник](../../apps/desktop/src/MemoryPanel.tsx#L40)

```typescript
function close()
```

Закрывает чистую форму; для dirty показывает явный выбор сохранить редактирование или потерять draft.

<a id="module-apps-desktop-src-modelsettings-tsx"></a>

## `apps/desktop/src/ModelSettings.tsx`

Модальное окно draft-настроек: endpoint, ключ, список моделей, тест ответа, генерация, лимиты, сохранение и focus trap.

### `GenerationSettings`

[Исходник](../../apps/desktop/src/ModelSettings.tsx#L6)

```typescript
export type GenerationSettings = {
  temperature: number; top_p: number; max_tokens: number; max_context_chars: number;
  request_timeout: number; max_agent_turns: number; max_runtime_minutes: number;
};
```

Числовой контракт семи применяемых настроек: sampling, token/context budgets, HTTP timeout и ограничения цикла.

### `ModelConfig`

[Исходник](../../apps/desktop/src/ModelSettings.tsx#L10)

```typescript
export type ModelConfig = { tool_protocol?: string; base_url: string; model: string; api_key: string; settings: GenerationSettings };
```

Конфигурация окна/IPC: URL, ID, временный API-ключ и числовые настройки.

### `ModelSettings`

[Исходник](../../apps/desktop/src/ModelSettings.tsx#L25)

```typescript
function ModelSettings({ initial, busy, onSaved, onClose }: {
  initial: ModelConfig; busy: boolean; onSaved: (config: ModelConfig) => void; onClose: () => void;
})
```

Модальное окно с отдельным draft; применяет настройки только после успешного backend save.

### `ModelSettings.change`

[Исходник](../../apps/desktop/src/ModelSettings.tsx#L41)

```typescript
function change(key: K, value: ModelConfig[K])
```

Меняет поле черновика и помечает его несохранённым; новый URL сбрасывает устаревший список моделей.

### `ModelSettings.validate`

[Исходник](../../apps/desktop/src/ModelSettings.tsx#L46)

```typescript
function validate()
```

Проверяет URL и диапазоны полей до отправки, backend повторяет обязательную валидацию.

### `ModelSettings.perform`

[Исходник](../../apps/desktop/src/ModelSettings.tsx#L58)

```typescript
async function perform(action: 'discover' | 'probe' | 'save')
```

Последовательно выполняет discovery, bounded probe или save с явным статусом и обработкой ошибок в окне.

### `ModelSettings.resetGeneration`

[Исходник](../../apps/desktop/src/ModelSettings.tsx#L85)

```typescript
function resetGeneration()
```

Возвращает числовые поля к defaults только в черновике, не меняет endpoint/ID/ключ.

### `ModelSettings.handleKeys`

[Исходник](../../apps/desktop/src/ModelSettings.tsx#L88)

```typescript
function handleKeys(event: React.KeyboardEvent<HTMLElement>)
```

Закрывает окно по Escape вне операции и удерживает Tab-навигацию в доступных контролах диалога.

<a id="module-apps-desktop-src-projectsearch-tsx"></a>

## `apps/desktop/src/ProjectSearch.tsx`

Боковой поиск и Ctrl+P: один IPC-запрос за раз, отмена и защита от устаревших результатов.

### `Match`

[Исходник](../../apps/desktop/src/ProjectSearch.tsx#L4)

```typescript
type Match = {path:string; line:number; text:string};
```

Найденный относительный путь, номер строки и ограниченный текстовый preview.

### `Props`

[Исходник](../../apps/desktop/src/ProjectSearch.tsx#L5)

```typescript
type Props = {root:string; visible:boolean; quick:boolean; focus:number; onClose:()=>void; onOpen:(path:string,line:number)=>void};
```

Корень, видимость, режим quick open и переход в editor.

### `ProjectSearch`

[Исходник](../../apps/desktop/src/ProjectSearch.tsx#L7)

```typescript
function ProjectSearch({root, visible, quick, focus, onClose, onOpen}:Props)
```

Единая форма text/files с bounded результатами, явной отменой и клавиатурным выбором.

### `ProjectSearch.search`

[Исходник](../../apps/desktop/src/ProjectSearch.tsx#L20)

```typescript
async function search()
```

Последовательно отменяет предыдущий запрос, отправляет новый и применяет только актуальный ticket/root.

### `ProjectSearch.cancel`

[Исходник](../../apps/desktop/src/ProjectSearch.tsx#L36)

```typescript
function cancel()
```

Инвалидирует результаты и запрашивает отмену собственного поиска.

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

Рабочий разговор с Мией без file tools, системная озвучка, голос/темп/громкость/Stop и честный отключённый STT.

### `WorkspaceMode`

[Исходник](../../apps/desktop/src/VoicePanel.tsx#L7)

```typescript
export type WorkspaceMode = 'chat' | 'ide' | 'voice';
```

Три пространства интерфейса: обычный разговор, работа с проектом и будущий голосовой ассистент.

### `VoiceSessionState`

[Исходник](../../apps/desktop/src/VoicePanel.tsx#L9)

```typescript
export type VoiceSessionState = 'disconnected' | 'idle' | 'listening' | 'thinking' | 'speaking' | 'error';
```

Состояния голосовой оболочки: disconnected/idle/listening/thinking/speaking/error; listening зарезервирован до подключения STT.

### `VoiceProfile`

[Исходник](../../apps/desktop/src/VoicePanel.tsx#L10)

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

[Исходник](../../apps/desktop/src/VoicePanel.tsx#L17)

```typescript
function VoicePanel({ onChat, onAsk, onCancel, busy, messages, conversationKey, completed }: {
  conversationKey:string;completed:boolean;
  onChat:()=>void;onAsk:(text:string)=>void;onCancel:()=>void;busy:boolean;
  messages:{role:string;text:string;streaming?:boolean}[];
})
```

Разговор с персонажем и реальный Windows TTS: каталог, voice/rate/volume, manual/opt-in auto speech и отдельный Stop.

### `VoicePanel.record`

[Исходник](../../apps/desktop/src/VoicePanel.tsx#L37)

```typescript
async function record()
```

Запускает явную запись микрофона или завершает текущую; ошибки и unmount освобождают tracks.

### `VoicePanel.finishRecording`

[Исходник](../../apps/desktop/src/VoicePanel.tsx#L43)

```typescript
async function finishRecording()
```

Формирует PCM16 WAV, отправляет STT и помещает распознанный текст в редактируемое поле без автоматической отправки.

### `VoicePanel.saveVoice`

[Исходник](../../apps/desktop/src/VoicePanel.tsx#L48)

```typescript
async function saveVoice()
```

Сохраняет выбранный голос, темп, громкость и auto-speak в отдельном профиле.

### `VoicePanel.refresh`

[Исходник](../../apps/desktop/src/VoicePanel.tsx#L60)

```typescript
async function refresh()
```

Читает plain status раз в 500 мс; отбрасывает ответы после unmount. Инициализация discovery учитывает StrictMode cleanup.

### `VoicePanel.speak`

[Исходник](../../apps/desktop/src/VoicePanel.tsx#L92)

```typescript
async function speak(text:string)
```

Отправляет до 6000 символов с выбранным голосом/темпом/громкостью и показывает lifecycle/ошибку.

### `VoicePanel.stop`

[Исходник](../../apps/desktop/src/VoicePanel.tsx#L97)

```typescript
async function stop()
```

Останавливает только озвучку; не отменяет модельную генерацию.

### `VoicePanel.send`

[Исходник](../../apps/desktop/src/VoicePanel.tsx#L102)

```typescript
function send()
```

Передаёт введённую фразу в общий task flow voice без файловых инструментов.

<a id="module-apps-desktop-src-main-tsx"></a>

## `apps/desktop/src/main.tsx`

Подключает CSS, создаёт React root и отображает App в StrictMode.

Нет именованных функций/типов: модуль выполняет конфигурацию, сборочный вызов или render entry. Анонимные callbacks описаны в учебных главах.

<a id="module-apps-desktop-src-microphone-ts"></a>

## `apps/desktop/src/microphone.ts`

Запись только по действию пользователя: 16 kHz mono PCM16 WAV, максимум 60 секунд, остановка MediaStream tracks.

### `this.processor.onaudioprocess`

[Исходник](../../apps/desktop/src/microphone.ts#L18)

```typescript
this.processor.onaudioprocess(event)
```

Копирует mono float samples до 960000 frames, затем автоматически завершает запись по лимиту 60 секунд.

### `ascii`

[Исходник](../../apps/desktop/src/microphone.ts#L31)

```typescript
ascii(offset:number, text:string)
```

Записывает фиксированные RIFF/WAVE/fmt/data метки в WAV DataView.

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
  pickRuntimeFile: (kind:string) => Promise<any>; startRuntime: (params:unknown) => Promise<any>; runtimeStatus: () => Promise<any>; stopRuntime: () => Promise<any>;
  getProjectMemory: () => Promise<any>; saveProjectMemory: (memory:unknown,revision:string) => Promise<any>; renameChat: (id:string,title:string,mode:string) => Promise<any>;
  telegramStatus:()=>Promise<any>;connectTelegram:(params:unknown)=>Promise<any>;disconnectTelegram:()=>Promise<any>;forgetTelegram:()=>Promise<any>;
  desktopSettings:()=>Promise<any>;configureDesktop:(enabled:boolean)=>Promise<any>;
  moveChat:(id:string,mode:string,target:string)=>Promise<any>;
  cancelHandoff:(id:string)=>Promise<any>;
  prepareHandoff:(id:string)=>Promise<any>;
  getCompanionSettings:()=>Promise<any>;configureCompanion:(params:unknown)=>Promise<any>;
  transcribe:(audio:string)=>Promise<any>;cancelTranscription:()=>Promise<any>;
  voiceStatus: () => Promise<any>; refreshVoices: () => Promise<any>; speak: (params:unknown) => Promise<any>; stopVoice: () => Promise<any>;
  searchProject: (params: unknown) => Promise<any>; cancelProjectSearch: () => Promise<any>;
  editorRead: (path: string) => Promise<any>; editorPreview: (path: string, content: string, revision: unknown) => Promise<any>;
  editorResolve: (proposalId: string, decision: string) => Promise<any>; setEditorDirty: (dirty: boolean) => Promise<any>;
  confirmEditorDiscard: () => Promise<{discard: boolean}>;
  configureModel: (config: {base_url: string; model: string; api_key: string; tool_protocol?: string; settings?: Record<string, number>}) => Promise<any>;
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

[Исходник](../../tests/electron/packaged-smoke.mjs#L112)

```typescript
async function main()
```

Поднимает HTTP-фикстуру, дважды проверяет пакет и отсутствие ключа в настройках/диагностике.

<a id="module-tests-electron-smoke-cjs"></a>

## `tests/electron/smoke.cjs`

Скрытое настоящее Electron-окно: все слои, запись, поток, reload и Stop.

### `desktopCapturer.getSources`

[Исходник](../../tests/electron/smoke.cjs#L4)

```typescript
desktopCapturer.getSources()
```

GUI fixture возвращает синтетический 1×1 NativeImage вместо захвата настоящего экрана; проверяет host broker и preview без чтения рабочего стола пользователя.

### `handlerForVoiceStatus`

[Исходник](../../tests/electron/smoke.cjs#L21)

```typescript
handlerForVoiceStatus()
```

В Electron fixture хранит реальный status handler для симуляции speaking без воспроизведения.

### `ipcMain.handle`

[Исходник](../../tests/electron/smoke.cjs#L22)

```typescript
ipcMain.handle(channel, handler)
```

В Electron fixture перехватывает только speech playback для проверки UI/Stop без звука; остальные IPC проходят в настоящий main.

### `fail`

[Исходник](../../tests/electron/smoke.cjs#L41)

```typescript
function fail(error)
```

В smoke-тесте записывает ошибку в result.json и завершает Electron.

### `BrowserWindow.prototype.show`

[Исходник](../../tests/electron/smoke.cjs#L51)

```typescript
BrowserWindow.prototype.show()
```

Только в smoke-тесте подавляет показ настоящего окна пользователю.

### `dialog.showMessageBox`

[Исходник](../../tests/electron/smoke.cjs#L53)

```typescript
dialog.showMessageBox()
```

В Electron smoke подменяет нативное подтверждение несохранённых изменений управляемым ответом Cancel/Discard.

### `dialog.showOpenDialog`

[Исходник](../../tests/electron/smoke.cjs#L56)

```typescript
dialog.showOpenDialog(_win, options)
```

Только в smoke-тесте возвращает учебный каталог вместо настоящего системного диалога.

### `encode`

[Исходник](../../tests/electron/smoke.cjs#L75)

```typescript
encode(delta)
```

Сериализует детерминированный SSE-чанк модельной фикстуры.

### `releaseModelText`

[Исходник](../../tests/electron/smoke.cjs#L85)

```typescript
releaseModelText()
```

Завершает задержанный ответ фикстуры после проверки видимого частичного текста.

### `releaseModelText`

[Исходник](../../tests/electron/smoke.cjs#L95)

```typescript
releaseModelText()
```

Завершает задержанный ответ фикстуры после проверки видимого частичного текста.

### `poll`

[Исходник](../../tests/electron/smoke.cjs#L102)

```typescript
async function poll(win, expression, timeout=10000)
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
