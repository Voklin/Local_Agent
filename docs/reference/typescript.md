# Справочник TypeScript и JavaScript

Этот файл создаётся `python tools/generate_code_reference.py`. Сигнатуры и номера строк извлечены из исходников; назначения — из ручных аннотаций. Изменяйте объяснения в `tools/doc_notes.py`, затем пересоздайте справочник.

Блоки сигнатур приводятся без тела; это справочные объявления, а не самостоятельные программы.

[К руководству](../README.md)

## Оглавление модулей

- [apps/desktop/build-electron.mjs](#module-apps-desktop-build-electron-mjs)
- [apps/desktop/electron/assistantMedia.ts](#module-apps-desktop-electron-assistantmedia-ts)
- [apps/desktop/electron/desktopApps.ts](#module-apps-desktop-electron-desktopapps-ts)
- [apps/desktop/electron/desktopLola.ts](#module-apps-desktop-electron-desktoplola-ts)
- [apps/desktop/electron/lolaPreload.ts](#module-apps-desktop-electron-lolapreload-ts)
- [apps/desktop/electron/main.ts](#module-apps-desktop-electron-main-ts)
- [apps/desktop/electron/neutralIde.ts](#module-apps-desktop-electron-neutralide-ts)
- [apps/desktop/electron/preload.ts](#module-apps-desktop-electron-preload-ts)
- [apps/desktop/electron/speechRuntime.ts](#module-apps-desktop-electron-speechruntime-ts)
- [apps/desktop/shared/contextTypes.ts](#module-apps-desktop-shared-contexttypes-ts)
- [apps/desktop/shared/createApi.ts](#module-apps-desktop-shared-createapi-ts)
- [apps/desktop/shared/ideTypes.ts](#module-apps-desktop-shared-idetypes-ts)
- [apps/desktop/shared/lolaDesktop.ts](#module-apps-desktop-shared-loladesktop-ts)
- [apps/desktop/shared/optionalTypes.ts](#module-apps-desktop-shared-optionaltypes-ts)
- [apps/desktop/shared/protocol.ts](#module-apps-desktop-shared-protocol-ts)
- [apps/desktop/shared/taskTypes.ts](#module-apps-desktop-shared-tasktypes-ts)
- [apps/desktop/src/App.tsx](#module-apps-desktop-src-app-tsx)
- [apps/desktop/src/AppearanceSettings.tsx](#module-apps-desktop-src-appearancesettings-tsx)
- [apps/desktop/src/ApprovalDialog.tsx](#module-apps-desktop-src-approvaldialog-tsx)
- [apps/desktop/src/BrandMark.tsx](#module-apps-desktop-src-brandmark-tsx)
- [apps/desktop/src/ChatText.tsx](#module-apps-desktop-src-chattext-tsx)
- [apps/desktop/src/CompanionSettings.tsx](#module-apps-desktop-src-companionsettings-tsx)
- [apps/desktop/src/ConnectionProfiles.tsx](#module-apps-desktop-src-connectionprofiles-tsx)
- [apps/desktop/src/ConnectionsSettings.tsx](#module-apps-desktop-src-connectionssettings-tsx)
- [apps/desktop/src/ContextUsage.tsx](#module-apps-desktop-src-contextusage-tsx)
- [apps/desktop/src/ConversationSidebar.tsx](#module-apps-desktop-src-conversationsidebar-tsx)
- [apps/desktop/src/DesktopLolaSettings.tsx](#module-apps-desktop-src-desktoplolasettings-tsx)
- [apps/desktop/src/DesktopLolaView.tsx](#module-apps-desktop-src-desktoplolaview-tsx)
- [apps/desktop/src/EditorPanel.tsx](#module-apps-desktop-src-editorpanel-tsx)
- [apps/desktop/src/ExtensionsSettings.tsx](#module-apps-desktop-src-extensionssettings-tsx)
- [apps/desktop/src/GenerationFields.tsx](#module-apps-desktop-src-generationfields-tsx)
- [apps/desktop/src/IdeTaskOptions.tsx](#module-apps-desktop-src-idetaskoptions-tsx)
- [apps/desktop/src/LocalRuntimePanel.tsx](#module-apps-desktop-src-localruntimepanel-tsx)
- [apps/desktop/src/LolaAvatar.tsx](#module-apps-desktop-src-lolaavatar-tsx)
- [apps/desktop/src/MemoryPanel.tsx](#module-apps-desktop-src-memorypanel-tsx)
- [apps/desktop/src/ModelSettings.tsx](#module-apps-desktop-src-modelsettings-tsx)
- [apps/desktop/src/NeuralAudio.tsx](#module-apps-desktop-src-neuralaudio-tsx)
- [apps/desktop/src/OptionalIdePanel.tsx](#module-apps-desktop-src-optionalidepanel-tsx)
- [apps/desktop/src/ProjectKnowledgePanel.tsx](#module-apps-desktop-src-projectknowledgepanel-tsx)
- [apps/desktop/src/ProjectSearch.tsx](#module-apps-desktop-src-projectsearch-tsx)
- [apps/desktop/src/RunHistory.tsx](#module-apps-desktop-src-runhistory-tsx)
- [apps/desktop/src/SourceContextPreview.tsx](#module-apps-desktop-src-sourcecontextpreview-tsx)
- [apps/desktop/src/StorageSettings.tsx](#module-apps-desktop-src-storagesettings-tsx)
- [apps/desktop/src/StudioControls.tsx](#module-apps-desktop-src-studiocontrols-tsx)
- [apps/desktop/src/StudioFileTree.tsx](#module-apps-desktop-src-studiofiletree-tsx)
- [apps/desktop/src/SubagentSettings.tsx](#module-apps-desktop-src-subagentsettings-tsx)
- [apps/desktop/src/TaskGraphPanel.tsx](#module-apps-desktop-src-taskgraphpanel-tsx)
- [apps/desktop/src/TaskProgress.tsx](#module-apps-desktop-src-taskprogress-tsx)
- [apps/desktop/src/VoicePanel.tsx](#module-apps-desktop-src-voicepanel-tsx)
- [apps/desktop/src/VoiceSettings.tsx](#module-apps-desktop-src-voicesettings-tsx)
- [apps/desktop/src/WakeListener.tsx](#module-apps-desktop-src-wakelistener-tsx)
- [apps/desktop/src/Welcome.tsx](#module-apps-desktop-src-welcome-tsx)
- [apps/desktop/src/WorkspaceAccessSettings.tsx](#module-apps-desktop-src-workspaceaccesssettings-tsx)
- [apps/desktop/src/WorkspaceReview.tsx](#module-apps-desktop-src-workspacereview-tsx)
- [apps/desktop/src/design/ForestSpot.tsx](#module-apps-desktop-src-design-forestspot-tsx)
- [apps/desktop/src/design/Ornaments.tsx](#module-apps-desktop-src-design-ornaments-tsx)
- [apps/desktop/src/design/themes.ts](#module-apps-desktop-src-design-themes-ts)
- [apps/desktop/src/ideEntry.ts](#module-apps-desktop-src-ideentry-ts)
- [apps/desktop/src/idePanel/acceptanceChecks.ts](#module-apps-desktop-src-idepanel-acceptancechecks-ts)
- [apps/desktop/src/idePanel/acceptanceSettings.tsx](#module-apps-desktop-src-idepanel-acceptancesettings-tsx)
- [apps/desktop/src/idePanel/connectionSettings.tsx](#module-apps-desktop-src-idepanel-connectionsettings-tsx)
- [apps/desktop/src/idePanel/entry.tsx](#module-apps-desktop-src-idepanel-entry-tsx)
- [apps/desktop/src/idePanel/recoveryDiagnostics.ts](#module-apps-desktop-src-idepanel-recoverydiagnostics-ts)
- [apps/desktop/src/idePanel/runActivity.tsx](#module-apps-desktop-src-idepanel-runactivity-tsx)
- [apps/desktop/src/idePanel/sessionState.ts](#module-apps-desktop-src-idepanel-sessionstate-ts)
- [apps/desktop/src/idePanel/workspace.tsx](#module-apps-desktop-src-idepanel-workspace-tsx)
- [apps/desktop/src/lola-main.tsx](#module-apps-desktop-src-lola-main-tsx)
- [apps/desktop/src/main.tsx](#module-apps-desktop-src-main-tsx)
- [apps/desktop/src/microphone.ts](#module-apps-desktop-src-microphone-ts)
- [apps/desktop/src/useLolaSession.tsx](#module-apps-desktop-src-uselolasession-tsx)
- [apps/desktop/src/useTaskSession.ts](#module-apps-desktop-src-usetasksession-ts)
- [apps/desktop/src/vite-env.d.ts](#module-apps-desktop-src-vite-env-d-ts)
- [apps/desktop/src/voiceText.ts](#module-apps-desktop-src-voicetext-ts)
- [apps/desktop/src/wakePhrase.ts](#module-apps-desktop-src-wakephrase-ts)
- [apps/desktop/vite.config.ts](#module-apps-desktop-vite-config-ts)
- [tests/electron/assistant-media.cjs](#module-tests-electron-assistant-media-cjs)
- [tests/electron/background-runs-smoke.cjs](#module-tests-electron-background-runs-smoke-cjs)
- [tests/electron/desktop-apps.cjs](#module-tests-electron-desktop-apps-cjs)
- [tests/electron/ide-acceptance-run.cjs](#module-tests-electron-ide-acceptance-run-cjs)
- [tests/electron/ide-acceptance.cjs](#module-tests-electron-ide-acceptance-cjs)
- [tests/electron/ide-acceptance.test.cjs](#module-tests-electron-ide-acceptance-test-cjs)
- [tests/electron/ide-session.test.cjs](#module-tests-electron-ide-session-test-cjs)
- [tests/electron/leshy-themes.cjs](#module-tests-electron-leshy-themes-cjs)
- [tests/electron/lola-desktop-smoke.cjs](#module-tests-electron-lola-desktop-smoke-cjs)
- [tests/electron/lola-preferences.cjs](#module-tests-electron-lola-preferences-cjs)
- [tests/electron/microphone.cjs](#module-tests-electron-microphone-cjs)
- [tests/electron/neutral-ide-integration.cjs](#module-tests-electron-neutral-ide-integration-cjs)
- [tests/electron/neutral-ide-smoke.cjs](#module-tests-electron-neutral-ide-smoke-cjs)
- [tests/electron/neutral-smoke.cjs](#module-tests-electron-neutral-smoke-cjs)
- [tests/electron/optional-ide-smoke.cjs](#module-tests-electron-optional-ide-smoke-cjs)
- [tests/electron/packaged-ide.mjs](#module-tests-electron-packaged-ide-mjs)
- [tests/electron/packaged-path.mjs](#module-tests-electron-packaged-path-mjs)
- [tests/electron/packaged-path.test.mjs](#module-tests-electron-packaged-path-test-mjs)
- [tests/electron/packaged-smoke.mjs](#module-tests-electron-packaged-smoke-mjs)
- [tests/electron/readiness-live.cjs](#module-tests-electron-readiness-live-cjs)
- [tests/electron/run.cjs](#module-tests-electron-run-cjs)
- [tests/electron/runner-exit.test.cjs](#module-tests-electron-runner-exit-test-cjs)
- [tests/electron/smoke.cjs](#module-tests-electron-smoke-cjs)
- [tests/electron/studio-layout.cjs](#module-tests-electron-studio-layout-cjs)
- [tests/electron/studio-smoke.cjs](#module-tests-electron-studio-smoke-cjs)
- [tests/electron/studio-visual.cjs](#module-tests-electron-studio-visual-cjs)
- [tools/extract_ts_symbols.cjs](#module-tools-extract-ts-symbols-cjs)

<a id="module-apps-desktop-build-electron-mjs"></a>

## `apps/desktop/build-electron.mjs`

Vite library-сборки main.cjs, preload.cjs и изолированного lolaPreload.cjs с внешними системными импортами.

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

### `fileName`

[Исходник](../../apps/desktop/build-electron.mjs#L6)

```typescript
fileName()
```

Возвращает фиксированное имя main.cjs или preload.cjs для соответствующей сборки Vite.

<a id="module-apps-desktop-electron-assistantmedia-ts"></a>

## `apps/desktop/electron/assistantMedia.ts`

Повторная host-валидация фиксированных музыкальных HTTPS URL и реального локального аудиофайла внутри разрешённых папок.

### `validateMusicURL`

[Исходник](../../apps/desktop/electron/assistantMedia.ts#L4)

```typescript
function validateMusicURL(value:unknown)
```

Повторно проверяет HTTPS URL по точному whitelist музыкальных хостов, без credentials и нестандартных портов.

### `validateAudioPath`

[Исходник](../../apps/desktop/electron/assistantMedia.ts#L12)

```typescript
function validateAudioPath(value:unknown, roots:unknown)
```

Канонизирует файл и корни, запрещает UNC/исполняемые расширения и выход из исходных папок через junction.

<a id="module-apps-desktop-electron-desktopapps-ts"></a>

## `apps/desktop/electron/desktopApps.ts`

Каталог локально разрешённых EXE: системные приложения, выбор пользователем, ID без путей для модели и запуск без shell/аргументов.

### `Application`

[Исходник](../../apps/desktop/electron/desktopApps.ts#L5)

```typescript
type Application = { id:string; name:string; file:string };
```

Приватная запись разрешённого приложения: ID, отображаемое имя и выбранный пользователем путь EXE.

<a id="module-apps-desktop-electron-desktoplola-ts"></a>

## `apps/desktop/electron/desktopLola.ts`

Нативные прозрачное окно и Tray спутника Лолы, сохранение preferences, изоляция IPC и пересылка ограниченных пользовательских действий.

### `status`

[Исходник](../../apps/desktop/electron/desktopLola.ts#L21)

```typescript
status()
```

IPC callback возвращает bounded снимок настроек/состояния desktop companion.

### `ready`

[Исходник](../../apps/desktop/electron/desktopLola.ts#L22)

```typescript
ready()
```

После renderer acknowledgement освобождает отложенные команды открытия чата и действия Лолы.

### `action`

[Исходник](../../apps/desktop/electron/desktopLola.ts#L23)

```typescript
action(value:unknown)
```

IPC callback проверяет и передаёт только allowlist пользовательских действий; настройки сначала показывают Neutral.

### `main`

[Исходник](../../apps/desktop/electron/desktopLola.ts#L24)

```typescript
main()
```

IPC callback показывает главное окно Neutral.

### `menu`

[Исходник](../../apps/desktop/electron/desktopLola.ts#L25)

```typescript
menu()
```

IPC callback открывает нативное контекстное меню спутника.

### `hover`

[Исходник](../../apps/desktop/electron/desktopLola.ts#L26)

```typescript
hover(value:unknown)
```

IPC callback меняет передачу кликов через прозрачное окно.

### `move`

[Исходник](../../apps/desktop/electron/desktopLola.ts#L27)

```typescript
move(value:unknown)
```

IPC callback применяет ограниченную проверенную дельту перемещения.

### `click`

[Исходник](../../apps/desktop/electron/desktopLola.ts#L57)

```typescript
click()
```

Обработчик пункта native Tray выполняет только заранее заданное действие меню.

### `click`

[Исходник](../../apps/desktop/electron/desktopLola.ts#L58)

```typescript
click()
```

Обработчик пункта native Tray выполняет только заранее заданное действие меню.

### `click`

[Исходник](../../apps/desktop/electron/desktopLola.ts#L59)

```typescript
click()
```

Обработчик пункта native Tray выполняет только заранее заданное действие меню.

### `click`

[Исходник](../../apps/desktop/electron/desktopLola.ts#L60)

```typescript
click()
```

Обработчик пункта native Tray выполняет только заранее заданное действие меню.

### `click`

[Исходник](../../apps/desktop/electron/desktopLola.ts#L61)

```typescript
click()
```

Обработчик пункта native Tray выполняет только заранее заданное действие меню.

### `click`

[Исходник](../../apps/desktop/electron/desktopLola.ts#L63)

```typescript
click()
```

Обработчик пункта native Tray выполняет только заранее заданное действие меню.

### `click`

[Исходник](../../apps/desktop/electron/desktopLola.ts#L64)

```typescript
click()
```

Обработчик пункта native Tray выполняет только заранее заданное действие меню.

### `click`

[Исходник](../../apps/desktop/electron/desktopLola.ts#L65)

```typescript
click()
```

Обработчик пункта native Tray выполняет только заранее заданное действие меню.

### `click`

[Исходник](../../apps/desktop/electron/desktopLola.ts#L66)

```typescript
click()
```

Обработчик пункта native Tray выполняет только заранее заданное действие меню.

### `click`

[Исходник](../../apps/desktop/electron/desktopLola.ts#L68)

```typescript
click()
```

Обработчик пункта native Tray выполняет только заранее заданное действие меню.

### `click`

[Исходник](../../apps/desktop/electron/desktopLola.ts#L69)

```typescript
click()
```

Обработчик пункта native Tray выполняет только заранее заданное действие меню.

<a id="module-apps-desktop-electron-lolapreload-ts"></a>

## `apps/desktop/electron/lolaPreload.ts`

Изолированный preload popup с общим типизированным facade; main разрешает только голосовые операции и собственные chat/run IDs.

### `status`

[Исходник](../../apps/desktop/electron/lolaPreload.ts#L5)

```typescript
status()
```

Запрашивает bounded snapshot из main process.

### `ready`

[Исходник](../../apps/desktop/electron/lolaPreload.ts#L6)

```typescript
ready()
```

Подтверждает установку event listener popup до доставки отложенных команд.

### `action`

[Исходник](../../apps/desktop/electron/lolaPreload.ts#L7)

```typescript
action(value:LolaDesktopAction)
```

Отправляет одно типизированное действие companion allowlist.

### `showMain`

[Исходник](../../apps/desktop/electron/lolaPreload.ts#L8)

```typescript
showMain()
```

Просит main process показать Neutral без передачи произвольных аргументов.

### `menu`

[Исходник](../../apps/desktop/electron/lolaPreload.ts#L9)

```typescript
menu()
```

Показывает нативное меню Tray/спутника.

### `hover`

[Исходник](../../apps/desktop/electron/lolaPreload.ts#L10)

```typescript
hover(value:boolean)
```

Сообщает main process о попадании pointer в интерактивную зону.

### `move`

[Исходник](../../apps/desktop/electron/lolaPreload.ts#L11)

```typescript
move(x:number, y:number)
```

Передаёт ограниченную дельту pointer для нативного перемещения окна.

### `onState`

[Исходник](../../apps/desktop/electron/lolaPreload.ts#L12)

```typescript
onState(callback:(value:{settings:LolaDesktopSettings;frame:LolaDesktopFrame})=>void)
```

Подписывает React на bounded визуальные обновления и возвращает disposer.

### `onState.receive`

[Исходник](../../apps/desktop/electron/lolaPreload.ts#L13)

```typescript
receive(_event:Electron.IpcRendererEvent, value:{settings:LolaDesktopSettings;frame:LolaDesktopFrame})
```

Передаёт проверенный IPC payload callback UI.

<a id="module-apps-desktop-electron-main-ts"></a>

## `apps/desktop/electron/main.ts`

Окно, Python-процесс, single-instance lock, pending RPC, проверка sender и фиксированные IPC handlers; создаёт нативный desktop companion.

### `speechRuntime`

[Исходник](../../apps/desktop/electron/main.ts#L28)

```typescript
function speechRuntime()
```

Создаёт один сервис Piper с локальными фиксированными путями вместо команд renderer.

### `desktopApplications`

[Исходник](../../apps/desktop/electron/main.ts#L36)

```typescript
function desktopApplications()
```

Создаёт host-каталог приложений с запуском EXE без shell и аргументов и фиксированным URL браузера.

### `bundledRuntimePath`

[Исходник](../../apps/desktop/electron/main.ts#L51)

```typescript
function bundledRuntimePath()
```

Находит включённый CPU llama-server в resources packaged приложения или в build для разработки; не принимает путь от renderer.

### `diagnostic`

[Исходник](../../apps/desktop/electron/main.ts#L58)

```typescript
function diagnostic(message: string)
```

Добавляет только lifecycle-диагностику в ограниченный main.log; ошибка I/O не блокирует приложение.

### `desktopRequest`

[Исходник](../../apps/desktop/electron/main.ts#L67)

```typescript
async function desktopRequest(message:any)
```

Исполняет только screenshot или фиксированный DuckDuckGo search URL, публикует локальный preview и отвечает Core по одноразовому UUID.

### `publish`

[Исходник](../../apps/desktop/electron/main.ts#L93)

```typescript
function publish(message: any)
```

Передаёт Core-событие живому renderer через фиксированный core:event.

### `startBackend`

[Исходник](../../apps/desktop/electron/main.ts#L102)

```typescript
function startBackend()
```

Лениво запускает Python, подключает stdout/stderr и обработчики завершения.

### `startBackend.stopped`

[Исходник](../../apps/desktop/electron/main.ts#L123)

```typescript
stopped()
```

Однократно сбрасывает процесс, завершает pending RPC ошибкой и сообщает backend_stopped.

### `callBackend`

[Исходник](../../apps/desktop/electron/main.ts#L135)

```typescript
function callBackend(method: string, params: Record<string, unknown> = {})
```

Посылает JSON-lines запрос с ID/Promise, таймером и ограничением pending.

### `createWindow`

[Исходник](../../apps/desktop/electron/main.ts#L153)

```typescript
function createWindow()
```

Создаёт изолированное Electron-окно и подключает его жизненный цикл.

### `showMain`

[Исходник](../../apps/desktop/electron/main.ts#L171)

```typescript
showMain()
```

Создаёт или восстанавливает основное окно при выборе действий спутника.

### `dispatch`

[Исходник](../../apps/desktop/electron/main.ts#L171)

```typescript
dispatch(action)
```

Направляет ограниченное действие UI через уже существующий основной event bridge.

### `notify`

[Исходник](../../apps/desktop/electron/main.ts#L171)

```typescript
notify(settings)
```

Обновляет main renderer и background throttling при сохранении настройки спутника.

### `quit`

[Исходник](../../apps/desktop/electron/main.ts#L171)

```typescript
quit()
```

Tray callback завершает приложение через штатный quit lifecycle.

### `allowedLolaRequest`

[Исходник](../../apps/desktop/electron/main.ts#L193)

```typescript
function allowedLolaRequest(channel:string, args:any[])
```

Ограничивает popup голосовыми API и известными voice chat/run IDs; запрещает основной model/workspace config.

### `handle`

[Исходник](../../apps/desktop/electron/main.ts#L205)

```typescript
function handle(channel: string, handler: (...args: any[]) => any)
```

Регистрирует IPC handler с проверкой sender и mainFrame.

### `readSharedTheme`

[Исходник](../../apps/desktop/electron/main.ts#L274)

```typescript
function readSharedTheme(fallback:unknown='forest')
```

Читает общую тему LESHY из сохранённого профиля.

### `writeSharedTheme`

[Исходник](../../apps/desktop/electron/main.ts#L280)

```typescript
function writeSharedTheme(theme:string)
```

Сохраняет выбранную общую тему для desktop и IDE.

### `modelConfig`

[Исходник](../../apps/desktop/electron/main.ts#L308)

```typescript
function modelConfig(config: any)
```

Явно перечисляет поля model IPC, остальные поля renderer не передаёт в Core.

### `confirmEditorDiscard`

[Исходник](../../apps/desktop/electron/main.ts#L311)

```typescript
async function confirmEditorDiscard()
```

Показывает нативное предупреждение с безопасным default Cancel; возвращает только явный отказ от сохранения.

<a id="module-apps-desktop-electron-neutralide-ts"></a>

## `apps/desktop/electron/neutralIde.ts`

Собственный Code-OSS launcher: отдельные runtime/profile/shared storage и авторизованный named pipe только для status/focus.

### `send`

[Исходник](../../apps/desktop/electron/neutralIde.ts#L29)

```typescript
send(id:unknown, result:any)
```

Передаёт разрешённый ответ клиенту собственного IDE транспорта.

<a id="module-apps-desktop-electron-preload-ts"></a>

## `apps/desktop/electron/preload.ts`

Узкий window.lca API и отписываемый listener событий.

Нет именованных функций/типов: модуль выполняет конфигурацию, сборочный вызов или render entry. Анонимные callbacks описаны в учебных главах.

<a id="module-apps-desktop-electron-speechruntime-ts"></a>

## `apps/desktop/electron/speechRuntime.ts`

Запуск фиксированного локального Piper, установка проверенной Serena, health и остановка только своего процесса.

Нет именованных функций/типов: модуль выполняет конфигурацию, сборочный вызов или render entry. Анонимные callbacks описаны в учебных главах.

<a id="module-apps-desktop-shared-contexttypes-ts"></a>

## `apps/desktop/shared/contextTypes.ts`

Независимые от React типы budget/usage для протокола и renderer.

### `RequestBudgetSnapshot`

[Исходник](../../apps/desktop/shared/contextTypes.ts#L1)

```typescript
export type RequestBudgetSnapshot = {
  window_tokens:number;input_tokens_estimate:number;output_tokens_reserved:number;safety_tokens:number;
  remaining_tokens:number;status:'fits'|'blocked';estimated:boolean;components:{instructions:number;history:number;tools:number;protocol:number};
  compressed?:boolean;reasons?:string[];mcp_loaded?:number;mcp_available?:number;
  mode?:'auto'|'manual';context_source?:string;counter?:string;server_adjustments?:number;tools_deferred?:number;output_adjusted?:boolean;
};
```

Оценка окончательного входа, окна, ответа/запаса, breakdown и MCP-schema counts без сырых payload.

### `ModelUsageSnapshot`

[Исходник](../../apps/desktop/shared/contextTypes.ts#L7)

```typescript
export type ModelUsageSnapshot = {input_tokens?:number;output_tokens?:number;requests?:number;requests_reported?:number;reported?:boolean};
```

Сумма фактических input/output tokens и число запросов, для которых сервер прислал usage.

### `RunLedgerSnapshot`

[Исходник](../../apps/desktop/shared/contextTypes.ts#L8)

```typescript
export type RunLedgerSnapshot={http_attempts:number;requests_reported:number;input_tokens:number;output_tokens:number;reservations:number;active_reserved_tokens:number;interrupted:number;queue_ms:number;queued_requests:number;elapsed_ms?:number;approval_ms?:number};
```

Агрегаты реального HTTP, известного usage, reservations, очереди и approval time для UI без политики caps.

### `RunSnapshot`

[Исходник](../../apps/desktop/shared/contextTypes.ts#L9)

```typescript
export type RunSnapshot={id:string;parent_id:string|null;kind:string;model:string;state:string;created_at:string;elapsed_ms:number;approval_ms:number;tool_calls:number;recovered?:boolean;recovery_cause?:'owner_exited'|'owner_replaced';recovered_at?:string;spending?:{currency:string;limit:number;estimated_spent:number;reserved:number;unknown_attempts:number;remaining:number};ledger:RunLedgerSnapshot};
```

Публичные metadata одного epoch: модель, state, duration, инструменты и ledger; без prompt/ключей/исходников.

<a id="module-apps-desktop-shared-createapi-ts"></a>

## `apps/desktop/shared/createApi.ts`

Общая фабрика фиксированного API для Electron preload и Code-OSS транспорта.

### `ApiTransport`

[Исходник](../../apps/desktop/shared/createApi.ts#L5)

```typescript
export interface ApiTransport { invoke:(channel:string,...args:any[])=>Promise<any>; on:(channel:string,listener:(event:unknown,data:any)=>void)=>unknown; removeListener:(channel:string,listener:(event:unknown,data:any)=>void)=>unknown; }
```

Минимальный транспорт invoke/on/removeListener для общей API-фабрики.

### `createApi`

[Исходник](../../apps/desktop/shared/createApi.ts#L6)

```typescript
function createApi(ipcRenderer:ApiTransport)
```

Создаёт фиксированную поверхность API поверх выбранного транспорта.

### `createApi.copyTaskDiagnostics`

[Исходник](../../apps/desktop/shared/createApi.ts#L7)

```typescript
copyTaskDiagnostics(report:string)
```

По явному действию пользователя копирует минимальный диагностический JSON через фиксированный host channel.

### `createApi.getAppearanceTheme`

[Исходник](../../apps/desktop/shared/createApi.ts#L8)

```typescript
getAppearanceTheme(fallback?:string)
```

Фиксированный API: читает общую тему через выбранный транспорт.

### `createApi.setAppearanceTheme`

[Исходник](../../apps/desktop/shared/createApi.ts#L9)

```typescript
setAppearanceTheme(theme:string)
```

Фиксированный API: изменяет общую тему через выбранный транспорт.

### `createApi.ideShell`

[Исходник](../../apps/desktop/shared/createApi.ts#L10)

```typescript
ideShell()
```

Фиксированный API: открывает shell редактора через выбранный транспорт.

### `createApi.idePreviewDiff`

[Исходник](../../apps/desktop/shared/createApi.ts#L11)

```typescript
idePreviewDiff(path:string)
```

Фиксированный API: показывает diff редактора через выбранный транспорт.

### `createApi.ideOpenFile`

[Исходник](../../apps/desktop/shared/createApi.ts#L12)

```typescript
ideOpenFile(path:string, line?:number)
```

Фиксированный API: открывает файл редактора через выбранный транспорт.

### `createApi.openNeutralIde`

[Исходник](../../apps/desktop/shared/createApi.ts#L13)

```typescript
openNeutralIde()
```

Вызывает фиксированный main IPC запуска собственного Neutral IDE; renderer не передаёт executable или произвольные аргументы.

### `createApi.workspaceAccess`

[Исходник](../../apps/desktop/shared/createApi.ts#L14)

```typescript
workspaceAccess()
```

Читает правила автоматического файлового доступа для выбранного Core проекта.

### `createApi.configureWorkspaceAccess`

[Исходник](../../apps/desktop/shared/createApi.ts#L15)

```typescript
configureWorkspaceAccess(paths:string[], confirmed:boolean)
```

Передаёт точные пути и явное согласие; модель этого API не получает.

### `createApi.cancelStorageBackup`

[Исходник](../../apps/desktop/shared/createApi.ts#L16)

```typescript
cancelStorageBackup()
```

Просит Core отменить текущий maintenance job без блокировки UI.

### `createApi.getDesktopLola`

[Исходник](../../apps/desktop/shared/createApi.ts#L17)

```typescript
getDesktopLola()
```

Читает сохранённые настройки и presentation состояния спутника.

### `createApi.openLola`

[Исходник](../../apps/desktop/shared/createApi.ts#L18)

```typescript
openLola(chatId?:string, action?:unknown)
```

Фиксированный API: открывает настольную Лолу через выбранный транспорт.

### `createApi.lolaMicrophone`

[Исходник](../../apps/desktop/shared/createApi.ts#L19)

```typescript
lolaMicrophone(active:boolean)
```

Фиксированный API: передаёт действие микрофона Лоле через выбранный транспорт.

### `createApi.configureDesktopLola`

[Исходник](../../apps/desktop/shared/createApi.ts#L20)

```typescript
configureDesktopLola(settings:LolaDesktopSettings)
```

Передаёт настройки спутника main process для проверки и записи.

### `createApi.presentDesktopLola`

[Исходник](../../apps/desktop/shared/createApi.ts#L21)

```typescript
presentDesktopLola(frame:LolaDesktopFrame)
```

Передаёт main process только bounded UI presentation frame.

### `createApi.listWorkspaces`

[Исходник](../../apps/desktop/shared/createApi.ts#L22)

```typescript
listWorkspaces()
```

Получает список пространств через ограниченный preload IPC.

### `createApi.saveWorkspace`

[Исходник](../../apps/desktop/shared/createApi.ts#L23)

```typescript
saveWorkspace(params:unknown)
```

Передаёт создание/изменение имени, папки и инструкций проекта.

### `createApi.selectWorkspace`

[Исходник](../../apps/desktop/shared/createApi.ts#L24)

```typescript
selectWorkspace(params:unknown)
```

Переключает пространство и его папку после проверок текущего состояния.

### `createApi.deleteWorkspace`

[Исходник](../../apps/desktop/shared/createApi.ts#L25)

```typescript
deleteWorkspace(params:unknown)
```

Удаляет подтверждённую группу с сохранением разговоров и файлов.

### `createApi.searchChats`

[Исходник](../../apps/desktop/shared/createApi.ts#L26)

```typescript
searchChats(params:unknown)
```

Запрашивает поиск названий/сообщений внутри режима, проекта и архива.

### `createApi.updateChat`

[Исходник](../../apps/desktop/shared/createApi.ts#L27)

```typescript
updateChat(params:unknown)
```

Меняет закрепление, архив или проект выбранного разговора.

### `createApi.deleteChat`

[Исходник](../../apps/desktop/shared/createApi.ts#L28)

```typescript
deleteChat(params:unknown)
```

Передаёт подтверждённое удаление конкретного чата.

### `createApi.forkChat`

[Исходник](../../apps/desktop/shared/createApi.ts#L29)

```typescript
forkChat(params:unknown)
```

Создаёт независимую копию или подготавливает повтор в новой ветке.

### `createApi.storageStatus`

[Исходник](../../apps/desktop/shared/createApi.ts#L30)

```typescript
storageStatus()
```

Фиксированный preload IPC проверки локального хранилища, без произвольной команды.

### `createApi.backupStorage`

[Исходник](../../apps/desktop/shared/createApi.ts#L31)

```typescript
backupStorage()
```

Фиксированный IPC резервной копии; путь берётся только из системного dialog в main.

### `createApi.exportChat`

[Исходник](../../apps/desktop/shared/createApi.ts#L32)

```typescript
exportChat(params:unknown)
```

Получает Markdown/JSON и открывает системное окно сохранения в main.

### `createApi.listExtensions`

[Исходник](../../apps/desktop/shared/createApi.ts#L33)

```typescript
listExtensions()
```

Получает публичный каталог возможностей без секретов.

### `createApi.configureExtensions`

[Исходник](../../apps/desktop/shared/createApi.ts#L34)

```typescript
configureExtensions(params:unknown)
```

Передаёт конкретное действие настройки реестра в Core.

### `createApi.discoverMcp`

[Исходник](../../apps/desktop/shared/createApi.ts#L35)

```typescript
discoverMcp(params:unknown)
```

Запускает асинхронное подключение MCP и получение схем tools.

### `createApi.cancelMcpDiscovery`

[Исходник](../../apps/desktop/shared/createApi.ts#L36)

```typescript
cancelMcpDiscovery(params:unknown)
```

Явный preload API отмены проверки MCP: передаёт ID сервера в ограниченный IPC обработчик main/Core.

### `createApi.listConnections`

[Исходник](../../apps/desktop/shared/createApi.ts#L37)

```typescript
listConnections()
```

Читает именованные публичные профили модели.

### `createApi.saveConnection`

[Исходник](../../apps/desktop/shared/createApi.ts#L38)

```typescript
saveConnection(params:unknown)
```

Сохраняет профиль API без секретного ключа.

### `createApi.deleteConnection`

[Исходник](../../apps/desktop/shared/createApi.ts#L39)

```typescript
deleteConnection(params:unknown)
```

Удаляет один выбранный публичный профиль.

### `createApi.importPlugin`

[Исходник](../../apps/desktop/shared/createApi.ts#L40)

```typescript
importPlugin()
```

Открывает системный выбор ограниченного JSON манифеста.

### `createApi.pickWorkspaceFolder`

[Исходник](../../apps/desktop/shared/createApi.ts#L41)

```typescript
pickWorkspaceFolder()
```

Выбирает папку для проекта без немедленного переключения текущего корня.

### `createApi.optionalSettings`

[Исходник](../../apps/desktop/shared/createApi.ts#L42)

```typescript
optionalSettings()
```

Читает typed catalog дополнительных возможностей через preload IPC.

### `createApi.configureOptionalIde`

[Исходник](../../apps/desktop/shared/createApi.ts#L43)

```typescript
configureOptionalIde(settings:OptionalSettings)
```

Передаёт четыре группы проверяемых opt-in настроек Core без секретов.

### `createApi.runOptionalIde`

[Исходник](../../apps/desktop/shared/createApi.ts#L44)

```typescript
runOptionalIde(params:OptionalRequest)
```

Запускает typed пользовательский IDE job через отменяемый длительный IPC.

### `createApi.cancelOptionalIde`

[Исходник](../../apps/desktop/shared/createApi.ts#L45)

```typescript
cancelOptionalIde()
```

Сигнализирует отмену текущего optional job, не освобождая gate преждевременно.

### `createApi.openManagedWorktree`

[Исходник](../../apps/desktop/shared/createApi.ts#L46)

```typescript
openManagedWorktree(id:string)
```

Открывает только проверенный owned Git ID; main не принимает произвольный путь renderer.

### `createApi.ideEditDraft`

[Исходник](../../apps/desktop/shared/createApi.ts#L47)

```typescript
ideEditDraft()
```

Фиксированный API: получает editor draft через выбранный транспорт.

### `createApi.ideEditorContext`

[Исходник](../../apps/desktop/shared/createApi.ts#L48)

```typescript
ideEditorContext()
```

Фиксированный API: получает выбранный диапазон редактора через выбранный транспорт.

### `createApi.health`

[Исходник](../../apps/desktop/shared/createApi.ts#L49)

```typescript
health()
```

Фиксированный preload-вызов проверки Core.

### `createApi.chooseProject`

[Исходник](../../apps/desktop/shared/createApi.ts#L50)

```typescript
chooseProject()
```

Выбор проекта: UI → native dialog → проверяемый set_project.

### `createApi.listFiles`

[Исходник](../../apps/desktop/shared/createApi.ts#L51)

```typescript
listFiles(relativePath = '.')
```

Preload-запрос списка файлов по относительному пути.

### `createApi.readFile`

[Исходник](../../apps/desktop/shared/createApi.ts#L52)

```typescript
readFile(relativePath: string)
```

Preload-запрос readonly текста файла.

### `createApi.pickRuntimeFile`

[Исходник](../../apps/desktop/shared/createApi.ts#L53)

```typescript
pickRuntimeFile(kind:string)
```

Вызывает системный выбор GGUF или установленного llama-server.

### `createApi.startRuntime`

[Исходник](../../apps/desktop/shared/createApi.ts#L54)

```typescript
startRuntime(params:unknown)
```

Передаёт только context/GPU; пути берутся main из предыдущего file picker.

### `createApi.runtimeStatus`

[Исходник](../../apps/desktop/shared/createApi.ts#L55)

```typescript
runtimeStatus()
```

Читает lifecycle собственного сервера без управления внешним LM Studio.

### `createApi.stopRuntime`

[Исходник](../../apps/desktop/shared/createApi.ts#L56)

```typescript
stopRuntime()
```

Останавливает только собственный локальный runtime через фиксированный IPC.

### `createApi.getProjectMemory`

[Исходник](../../apps/desktop/shared/createApi.ts#L57)

```typescript
getProjectMemory()
```

Читает семь полей и byte revision памяти текущего проекта.

### `createApi.saveProjectMemory`

[Исходник](../../apps/desktop/shared/createApi.ts#L58)

```typescript
saveProjectMemory(memory:unknown, revision:string, root?:string)
```

Сохраняет семь справочных полей через fixed IPC с CAS revision и optional expected root; renderer не пишет файлы напрямую.

### `createApi.projectMemoryAction`

[Исходник](../../apps/desktop/shared/createApi.ts#L59)

```typescript
projectMemoryAction(params:unknown)
```

Фиксированный API: выполняет действие памяти проекта через выбранный транспорт.

### `createApi.renameChat`

[Исходник](../../apps/desktop/shared/createApi.ts#L60)

```typescript
renameChat(id:string, title:string, mode:string)
```

Фиксированный IPC переименования ID/title/mode без изменения сообщений.

### `createApi.telegramStatus`

[Исходник](../../apps/desktop/shared/createApi.ts#L61)

```typescript
telegramStatus()
```

Читает безопасный статус бота без token и HTTP URL.

### `createApi.connectTelegram`

[Исходник](../../apps/desktop/shared/createApi.ts#L62)

```typescript
connectTelegram(params:unknown)
```

Подключает token/owner либо явно выбранную защищённую локальную запись; секрет не возвращается renderer.

### `createApi.disconnectTelegram`

[Исходник](../../apps/desktop/shared/createApi.ts#L63)

```typescript
disconnectTelegram()
```

Отключает polling бота через Core.

### `createApi.forgetTelegram`

[Исходник](../../apps/desktop/shared/createApi.ts#L64)

```typescript
forgetTelegram()
```

Удаляет только сохранённую encrypted запись токена по явной кнопке пользователя.

### `createApi.desktopSettings`

[Исходник](../../apps/desktop/shared/createApi.ts#L65)

```typescript
desktopSettings()
```

Читает opt-in состояние PC tools без доступа к файлам.

### `createApi.desktopApplications`

[Исходник](../../apps/desktop/shared/createApi.ts#L66)

```typescript
desktopApplications()
```

Создаёт или запрашивает каталог разрешённых приложений ПК; модель получает ID и названия без путей.

### `createApi.addDesktopApplication`

[Исходник](../../apps/desktop/shared/createApi.ts#L67)

```typescript
addDesktopApplication()
```

Открывает только системный EXE-picker для добавления разрешённого приложения.

### `createApi.removeDesktopApplication`

[Исходник](../../apps/desktop/shared/createApi.ts#L68)

```typescript
removeDesktopApplication(id:string)
```

Удаляет пользовательское разрешение запуска по ID через фиксированный IPC.

### `createApi.configureDesktop`

[Исходник](../../apps/desktop/shared/createApi.ts#L69)

```typescript
configureDesktop(enabled:boolean)
```

Включает/выключает PC tools; аргументы модели не могут изменить это разрешение.

### `createApi.moveChat`

[Исходник](../../apps/desktop/shared/createApi.ts#L70)

```typescript
moveChat(chat_id:string, mode:string, target:string)
```

Переносит только Chat/voice историю в другую область по явному действию пользователя.

### `createApi.cancelHandoff`

[Исходник](../../apps/desktop/shared/createApi.ts#L71)

```typescript
cancelHandoff(id:string)
```

Отклоняет pending передачу Лолы по точному ID без запуска основной модели.

### `createApi.prepareHandoff`

[Исходник](../../apps/desktop/shared/createApi.ts#L72)

```typescript
prepareHandoff(id:string)
```

Переносит pending задание Лолы в новый чат основной модели по точному ID.

### `createApi.getCompanionSettings`

[Исходник](../../apps/desktop/shared/createApi.ts#L73)

```typescript
getCompanionSettings()
```

Читает независимый публичный профиль Лолы через allowlisted IPC.

### `createApi.configureCompanion`

[Исходник](../../apps/desktop/shared/createApi.ts#L74)

```typescript
configureCompanion(params:unknown)
```

Сохраняет настройки Лолы отдельно от основной модели и оставляет секреты только в памяти Core.

### `createApi.transcribe`

[Исходник](../../apps/desktop/shared/createApi.ts#L75)

```typescript
transcribe(audio:string)
```

Передаёт ограниченную base64 WAV-запись в отменяемый STT RPC.

### `createApi.cancelTranscription`

[Исходник](../../apps/desktop/shared/createApi.ts#L76)

```typescript
cancelTranscription()
```

Отменяет текущую транскрипцию и закрывает её сокет.

### `createApi.voiceStatus`

[Исходник](../../apps/desktop/shared/createApi.ts#L77)

```typescript
voiceStatus()
```

Читает состояние системной озвучки через фиксированный IPC.

### `createApi.refreshVoices`

[Исходник](../../apps/desktop/shared/createApi.ts#L78)

```typescript
refreshVoices()
```

Перечисляет системные голоса/распознаватели без запроса микрофона.

### `createApi.speak`

[Исходник](../../apps/desktop/shared/createApi.ts#L79)

```typescript
speak(params:unknown)
```

Передаёт только text/voice/rate/volume для plain TTS; пути/PowerShell code не принимаются.

### `createApi.stopVoice`

[Исходник](../../apps/desktop/shared/createApi.ts#L80)

```typescript
stopVoice()
```

Запрашивает отмену собственного speech worker.

### `createApi.voicePlayback`

[Исходник](../../apps/desktop/shared/createApi.ts#L81)

```typescript
voicePlayback(params:unknown)
```

Фиксированный IPC сообщает Core об окончании/ошибке текущего sequence звука.

### `createApi.openTtsFolder`

[Исходник](../../apps/desktop/shared/createApi.ts#L82)

```typescript
openTtsFolder()
```

Открывает только штатную папку sidecar TTS, без запуска команды из ответа модели.

### `createApi.speechRuntime`

[Исходник](../../apps/desktop/shared/createApi.ts#L83)

```typescript
speechRuntime(operation:string)
```

Создаёт один сервис Piper с локальными фиксированными путями вместо команд renderer.

### `createApi.activateAssistant`

[Исходник](../../apps/desktop/shared/createApi.ts#L84)

```typescript
activateAssistant()
```

Показывает и фокусирует окно после явной включённой фразы активации.

### `createApi.wakeListening`

[Исходник](../../apps/desktop/shared/createApi.ts#L85)

```typescript
wakeListening(enabled:boolean)
```

Отключает background throttling только пока пользователь включил прослушивание.

### `createApi.searchProject`

[Исходник](../../apps/desktop/shared/createApi.ts#L86)

```typescript
searchProject(params: unknown)
```

Вызывает фиксированный read-only IPC поиска с текстом/маской/регистром.

### `createApi.projectIndex`

[Исходник](../../apps/desktop/shared/createApi.ts#L87)

```typescript
projectIndex(params: unknown)
```

Узкий renderer→main→Core API управления derived индексом выбранного проекта.

### `createApi.cancelProjectSearch`

[Исходник](../../apps/desktop/shared/createApi.ts#L88)

```typescript
cancelProjectSearch()
```

Отменяет поиск независимо от остановки агента.

### `createApi.editorRead`

[Исходник](../../apps/desktop/shared/createApi.ts#L89)

```typescript
editorRead(path: string)
```

Вызывает отдельное strict editor_read через фиксированный IPC.

### `createApi.editorPreview`

[Исходник](../../apps/desktop/shared/createApi.ts#L90)

```typescript
editorPreview(path: string, content: string, revision: unknown)
```

Передаёт draft и исходную revision для preview без записи.

### `createApi.editorResolve`

[Исходник](../../apps/desktop/shared/createApi.ts#L91)

```typescript
editorResolve(proposalId: string, decision: string)
```

Передаёт только proposal ID и явное решение, не произвольную команду записи.

### `createApi.setEditorDirty`

[Исходник](../../apps/desktop/shared/createApi.ts#L92)

```typescript
setEditorDirty(dirty: boolean)
```

Сообщает main о несохранённых вкладках для защиты закрытия окна.

### `createApi.confirmEditorDiscard`

[Исходник](../../apps/desktop/shared/createApi.ts#L93)

```typescript
confirmEditorDiscard()
```

Показывает нативное предупреждение с безопасным default Cancel; возвращает только явный отказ от сохранения.

### `createApi.systemInfo`

[Исходник](../../apps/desktop/shared/createApi.ts#L94)

```typescript
systemInfo()
```

Preload-запрос home/platform у main, без tool модели.

### `createApi.configureModel`

[Исходник](../../apps/desktop/shared/createApi.ts#L95)

```typescript
configureModel(config: { base_url: string; model: string; api_key?: string; settings?: unknown })
```

Передаёт URL/модель/сеансовый ключ в фиксированный model:configure.

### `createApi.listModels`

[Исходник](../../apps/desktop/shared/createApi.ts#L96)

```typescript
listModels(config?: unknown)
```

Запрашивает ID доступных моделей.

### `createApi.testModel`

[Исходник](../../apps/desktop/shared/createApi.ts#L97)

```typescript
testModel(config: unknown)
```

Посылает фиксированный RPC диагностики без произвольного prompt и файлов.

### `createApi.cancelModelSetup`

[Исходник](../../apps/desktop/shared/createApi.ts#L98)

```typescript
cancelModelSetup()
```

Отменяет текущую диагностику модели через отдельный фиксированный канал.

### `createApi.getModelSettings`

[Исходник](../../apps/desktop/shared/createApi.ts#L99)

```typescript
getModelSettings()
```

Читает сохранённые URL/ID без ключа.

### `createApi.listChats`

[Исходник](../../apps/desktop/shared/createApi.ts#L100)

```typescript
listChats(mode = 'ide')
```

Получает чаты выбранного проекта.

### `createApi.newChat`

[Исходник](../../apps/desktop/shared/createApi.ts#L101)

```typescript
newChat(mode = 'ide')
```

Создаёт пустой чат проекта.

### `createApi.loadChat`

[Исходник](../../apps/desktop/shared/createApi.ts#L102)

```typescript
loadChat(chatId: string, mode = 'ide')
```

Загружает проверяемый ID чата.

### `createApi.startTask`

[Исходник](../../apps/desktop/shared/createApi.ts#L103)

```typescript
startTask(prompt: string, resume = false, mode:AgentMode = 'ide', options?:StartTaskOptions, runId?:string)
```

Посылает prompt и resume-флаг, получает принятие задачи.

### `createApi.createGitCheckpoint`

[Исходник](../../apps/desktop/shared/createApi.ts#L104)

```typescript
createGitCheckpoint(params:unknown)
```

Фиксированный API: создаёт private Git checkpoint через выбранный транспорт.

### `createApi.cancelGitCheckpoint`

[Исходник](../../apps/desktop/shared/createApi.ts#L105)

```typescript
cancelGitCheckpoint()
```

Фиксированный API: отменяет создание checkpoint через выбранный транспорт.

### `createApi.listSnapshots`

[Исходник](../../apps/desktop/shared/createApi.ts#L106)

```typescript
listSnapshots(params:unknown)
```

Фиксированный IPC списка снимков текущего IDE-чата.

### `createApi.previewRollback`

[Исходник](../../apps/desktop/shared/createApi.ts#L107)

```typescript
previewRollback(params:unknown)
```

Фиксированный IPC обратного diff и server-issued proposal.

### `createApi.applyRollback`

[Исходник](../../apps/desktop/shared/createApi.ts#L108)

```typescript
applyRollback(params:unknown)
```

Фиксированный IPC подтверждения rollback proposal, без произвольного файла/команды.

### `createApi.reviewRollback`

[Исходник](../../apps/desktop/shared/createApi.ts#L109)

```typescript
reviewRollback(params:unknown)
```

Фиксированный IPC явного наблюдения после partial rollback; данные файлов не изменяет.

### `createApi.cancelTask`

[Исходник](../../apps/desktop/shared/createApi.ts#L110)

```typescript
cancelTask(runId?:string)
```

Запрашивает отмену через task:cancel.

### `createApi.updateTaskPlan`

[Исходник](../../apps/desktop/shared/createApi.ts#L111)

```typescript
updateTaskPlan(params:unknown)
```

Фиксированный API: обновляет план текущей задачи через выбранный транспорт.

### `createApi.activeRuns`

[Исходник](../../apps/desktop/shared/createApi.ts#L112)

```typescript
activeRuns()
```

Фиксированный API: читает активные запуски через выбранный транспорт.

### `createApi.runHistory`

[Исходник](../../apps/desktop/shared/createApi.ts#L113)

```typescript
runHistory(chatId:string)
```

Узкий renderer→main→Core вызов истории только выбранного чата; записи из иной scope не возвращаются.

### `createApi.resolveApproval`

[Исходник](../../apps/desktop/shared/createApi.ts#L114)

```typescript
resolveApproval(runId: string, approvalId: string, decision: ApprovalDecision)
```

Передаёт run/proposal ID и явное решение.

### `createApi.resolveToolRecovery`

[Исходник](../../apps/desktop/shared/createApi.ts#L115)

```typescript
resolveToolRecovery(params: {chat_id:string; journal_id:string; message_index:number; call_id:string; resolution:'completed'|'not_executed'})
```

Ограниченный preload API проверки неизвестного действия; передаёт chat/epoch/call identity и явное наблюдение.

### `createApi.onEvent`

[Исходник](../../apps/desktop/shared/createApi.ts#L116)

```typescript
onEvent(callback: (event: any) => void)
```

Подписывает callback на core:event и возвращает отписку.

### `createApi.onEvent.listener`

[Исходник](../../apps/desktop/shared/createApi.ts#L117)

```typescript
listener(_event: unknown, data: unknown)
```

Адаптирует Electron event в пользовательские данные callback.

<a id="module-apps-desktop-shared-idetypes-ts"></a>

## `apps/desktop/shared/ideTypes.ts`

Общие validation command и IDE task options без renderer runtime.

### `EvidenceScope`

[Исходник](../../apps/desktop/shared/ideTypes.ts#L1)

```typescript
export type EvidenceScope={kind:'workspace'}|{kind:'files';files:string[];dependencies:string[]};
```

Пользовательская область доказательств: весь проект либо точные сохранённые файлы и объявленные зависимости.

### `ValidationCommand`

[Исходник](../../apps/desktop/shared/ideTypes.ts#L2)

```typescript
export type ValidationCommand={kind?:'test'|'lint'|'types'|'syntax'|'custom'|'diagnostics';applies_to?:string[];id:string;purpose:string;program:string;arguments:string[];cwd:string;timeout:number;evidence_scope?:EvidenceScope};
```

Пользовательская программа проверки: purpose, argv, cwd, timeout и ID для acceptance links.

### `IdeOptions`

[Исходник](../../apps/desktop/shared/ideTypes.ts#L3)

```typescript
export type IdeOptions={read_only:boolean;auto_checks:boolean;criteria:string[];criteria_links:Record<string,string[]>;checks:ValidationCommand[]};
```

Ограничения IDE задачи, пользовательские критерии и список явно настроенных проверок.

<a id="module-apps-desktop-shared-loladesktop-ts"></a>

## `apps/desktop/shared/lolaDesktop.ts`

Общие строгие типы, defaults и проверка состояния, команд и размещения настольной Лолы.

### `LolaAnimationState`

[Исходник](../../apps/desktop/shared/lolaDesktop.ts#L1)

```typescript
export type LolaAnimationState='idle'|'listening'|'thinking'|'working'|'speaking'|'success'|'error';
```

Семь UI-анимационных состояний без связи с модельными командами.

### `LolaDesktopSettings`

[Исходник](../../apps/desktop/shared/lolaDesktop.ts#L2)

```typescript
export type LolaDesktopSettings={enabled:boolean;mode:'desktop'|'top'|'tray';size:number;animate:boolean;clickThrough:boolean;position:{x:number;y:number}|null};
```

Persisted opt-in настройки режима, размера, анимации, click-through и положения.

### `LolaDesktopFrame`

[Исходник](../../apps/desktop/shared/lolaDesktop.ts#L3)

```typescript
export type LolaDesktopFrame={state:LolaAnimationState;caption:string;reply:string;busy:boolean;recording:boolean;wake:boolean};
```

Bounded отображаемые подпись/ответ и наблюдаемые статусы голоса/работы.

### `LolaDesktopAction`

[Исходник](../../apps/desktop/shared/lolaDesktop.ts#L4)

```typescript
export type LolaDesktopAction={action:'ask'|'record'|'stop'|'settings'|'speak';text?:string};
```

Allowlist пользовательского ask/record/stop/settings действия.

### `LolaVoiceAction`

[Исходник](../../apps/desktop/shared/lolaDesktop.ts#L5)

```typescript
export type LolaVoiceAction={id:number;action:'record'|'cancel'|'settings'|'speak'};
```

Одноразовая команда основному владельцу VoicePanel.

### `validateLolaSettings`

[Исходник](../../apps/desktop/shared/lolaDesktop.ts#L8)

```typescript
function validateLolaSettings(value:unknown): LolaDesktopSettings
```

Fail-closed проверка prefs спутника, режима, диапазона размера и координат.

### `validateLolaFrame`

[Исходник](../../apps/desktop/shared/lolaDesktop.ts#L16)

```typescript
function validateLolaFrame(value:unknown): LolaDesktopFrame
```

Ограничивает длину текста и enum состояния перед renderer-передачей.

### `fitLolaBounds`

[Исходник](../../apps/desktop/shared/lolaDesktop.ts#L22)

```typescript
function fitLolaBounds(settings:LolaDesktopSettings, area:{x:number;y:number;width:number;height:number})
```

Размещает окно в доступной области выбранного монитора.

<a id="module-apps-desktop-shared-optionaltypes-ts"></a>

## `apps/desktop/shared/optionalTypes.ts`

Типы настроек, discriminated requests и публичных результатов дополнительных IDE операций.

### `OptionalSettings`

[Исходник](../../apps/desktop/shared/optionalTypes.ts#L2)

```typescript
export type OptionalSettings={
  research:{enabled:boolean;seconds:number;max_tokens:number};
  lsp:{enabled:boolean;program:string;arguments:string[];language:string;seconds:number};
  worktrees:{enabled:boolean};container:{enabled:boolean;image:string;memory_mb:number};
};
```

Четыре opt-in группы с явными пределами и пользовательской конфигурацией сервера/образа.

### `OptionalRequest`

[Исходник](../../apps/desktop/shared/optionalTypes.ts#L7)

```typescript
export type OptionalRequest={action:'research';query:string}|{action:'diagnostics';path:string}|{action:'container_status'|'worktree_list'}|{action:'worktree_create';name:string;confirmed:true}|{action:'worktree_diff'|'worktree_open';id:string}|{action:'worktree_remove';id:string;confirmed:true};
```

Discriminated union research/diagnostics/worktrees/runtime; эффекты требуют literal true confirmation.

### `ManagedWorktree`

[Исходник](../../apps/desktop/shared/optionalTypes.ts#L8)

```typescript
export type ManagedWorktree={id:string;name:string;path:string;root:string;commit:string;status:string;exists?:boolean;registered?:boolean};
```

Публичный ownership receipt с commit/status/path и фактической регистрацией.

### `LanguageDiagnostic`

[Исходник](../../apps/desktop/shared/optionalTypes.ts#L9)

```typescript
export type LanguageDiagnostic={line:number;column:number;severity:number;message:string;source:string};
```

Нормализованная 1-based строка/колонка, severity/message/source от сервера.

### `OptionalResult`

[Исходник](../../apps/desktop/shared/optionalTypes.ts#L10)

```typescript
export type OptionalResult=RpcResult<{
  root:string;text?:string;complete?:boolean;requests?:number;source_chars?:number;elapsed_ms?:number;
  sources?:{path:string;start_line:number;end_line:number;sha256:string}[];usage?:Record<string,number>;
  diagnostics?:LanguageDiagnostic[];path?:string;stale?:boolean;truncated?:boolean;
  worktrees?:ManagedWorktree[];worktree?:ManagedWorktree;status?:string;diff?:string;
  available?:boolean;docker?:boolean;wsl?:boolean;notice?:string;
}>;
```

Ограниченный результат фонового IDE RPC с root correlation, метриками, sources/diagnostics/worktrees.

### `OptionalCatalog`

[Исходник](../../apps/desktop/shared/optionalTypes.ts#L17)

```typescript
export type OptionalCatalog=RpcResult<{settings:OptionalSettings;running:boolean;warning?:string;inference:{busy:boolean;kind?:string;limit:number}}>;
```

Типизированные settings и состояние единого inference gate без ключей.

<a id="module-apps-desktop-shared-protocol-ts"></a>

## `apps/desktop/shared/protocol.ts`

Общие типы критического IPC, версия, runtime guard событий и таблица timeout/cancel.

### `AgentMode`

[Исходник](../../apps/desktop/shared/protocol.ts#L5)

```typescript
export type AgentMode='chat'|'ide'|'voice';
```

Три допустимых wire-режима Chat/IDE/Лола.

### `RpcFailure`

[Исходник](../../apps/desktop/shared/protocol.ts#L6)

```typescript
export type RpcFailure={ok:false;error:string;code?:string};
```

Явный отказ с текстом и необязательным code, без фиктивных полей успеха.

### `RpcResult`

[Исходник](../../apps/desktop/shared/protocol.ts#L7)

```typescript
export type RpcResult<T extends object=Record<string,never>>=({ok:true}&T)|RpcFailure;
```

Discriminated union успеха и отказа для критического API.

### `StartTaskOptions`

[Исходник](../../apps/desktop/shared/protocol.ts#L8)

```typescript
export type StartTaskOptions=IdeOptions&{checks_only?:boolean};
```

Типизированные параметры IDE и режим проверки без модели.

### `StartTaskResult`

[Исходник](../../apps/desktop/shared/protocol.ts#L9)

```typescript
export type StartTaskResult=RpcResult<{run_id:string;chat_id:string}>;
```

Успешный chat/run identity либо явная ошибка старта.

### `ApprovalDecision`

[Исходник](../../apps/desktop/shared/protocol.ts#L10)

```typescript
export type ApprovalDecision='apply'|'reject'|'cancel';
```

Только apply/reject/cancel; произвольная строка не проходит компиляцию/валидацию.

### `RecoveryRequest`

[Исходник](../../apps/desktop/shared/protocol.ts#L11)

```typescript
export type RecoveryRequest={chat_id:string;journal_id:string;message_index:number;call_id:string;resolution:TaskRecoveryResolution};
```

Якорь конкретного call и явное пользовательское наблюдение.

### `SnapshotSummary`

[Исходник](../../apps/desktop/shared/protocol.ts#L12)

```typescript
export type SnapshotSummary={id:string;status:string;paths:string[];operations:string[];journal_id?:string};
```

Публичные snapshot metadata без backup bytes.

### `SnapshotScope`

[Исходник](../../apps/desktop/shared/protocol.ts#L13)

```typescript
export type SnapshotScope={chat_id:string};
```

Выбранный chat ID для операций review.

### `SnapshotPreview`

[Исходник](../../apps/desktop/shared/protocol.ts#L14)

```typescript
export type SnapshotPreview={id:string;group_id:string;paths:string[];diff:string;truncated:boolean};
```

Обратный diff, ограничение отображения и одноразовый ID proposal.

### `SnapshotListResult`

[Исходник](../../apps/desktop/shared/protocol.ts#L15)

```typescript
export type SnapshotListResult=RpcResult<{snapshots:SnapshotSummary[];task:TaskSnapshot|null}>;
```

Типизированный список снимков и восстановленный checkpoint либо отказ.

### `SnapshotApplyResult`

[Исходник](../../apps/desktop/shared/protocol.ts#L16)

```typescript
export type SnapshotApplyResult=({ok:true;snapshots:SnapshotSummary[];task:TaskSnapshot|null;changed_paths?:string[]})|(RpcFailure&{snapshots?:SnapshotSummary[];task?:TaskSnapshot|null;changed_paths?:string[]});
```

Успех либо partial failure с необязательными актуальными snapshots/task; UI обрабатывает оба исхода.

### `TaskEventBase`

[Исходник](../../apps/desktop/shared/protocol.ts#L17)

```typescript
export type TaskEventBase={protocol_version?:number;chat_id:string;run_id:string;event_seq?:number};
```

Run/chat correlation и версия критических событий.

### `TaskLifecycleEvent`

[Исходник](../../apps/desktop/shared/protocol.ts#L18)

```typescript
export type TaskLifecycleEvent=TaskEventBase&(
  {event:'task';task:TaskSnapshot}|{event:'task_end'}|{event:'text_delta';message_id:string;text:string}|
  {event:'chat';message_id?:string;role:string;text:string}|{event:'failed'|'result'|'warning'|'log';text:string}|
  {event:'progress';count:number;maximum:number}|
  {event:'approval';approval_id:string;path:string;diff:string;exists:boolean;kind?:string;title?:string}|
  {event:'change'|'file_change';change:{status:string;path:string;error?:string;[key:string]:unknown}}
);
```

Discriminated lifecycle events вместо неограниченных полей task/stream/approval.

### `isTaskEvent`

[Исходник](../../apps/desktop/shared/protocol.ts#L26)

```typescript
function isTaskEvent(value:unknown): value is TaskLifecycleEvent
```

Проверяет wire envelope критического события до изменения UI state.

### `rpcTimeout`

[Исходник](../../apps/desktop/shared/protocol.ts#L37)

```typescript
function rpcTimeout(method:string)
```

Одна таблица допустимых таймаутов main→Core, включая долгие backup/snapshot запросы.

### `rpcCancellation`

[Исходник](../../apps/desktop/shared/protocol.ts#L41)

```typescript
function rpcCancellation(method:string): {method:string;params?:Record<string,unknown>}|null
```

Связывает истечение RPC с соответствующей отменой поиска/STT/discovery/probe/задачи без повтора effects.

<a id="module-apps-desktop-shared-tasktypes-ts"></a>

## `apps/desktop/shared/taskTypes.ts`

Единые task/recovery/evidence типы без зависимости Electron main от TSX.

### `PlanNode`

[Исходник](../../apps/desktop/shared/taskTypes.ts#L1)

```typescript
export type PlanNode={id:string;title:string;kind:'analysis'|'change'|'verification';depends_on:string[];affected_files:string[];check_ids:string[];status?:string;advisory?:boolean;evidence?:unknown[];note?:string};
```

Тип canonical plan_steps schema 2: зависимости, affected files, проверочные IDs, evidence и состояние; legacy strings поддержаны явно.

### `TaskStage`

[Исходник](../../apps/desktop/shared/taskTypes.ts#L3)

```typescript
export type TaskStage = { id: string; title: string; objective?: string; status: string };
```

UI-представление этапа: идентификатор, название, цель и статус исполнения.

### `ToolActivity`

[Исходник](../../apps/desktop/shared/taskTypes.ts#L4)

```typescript
export type ToolActivity = { id: number; tool: string; path: string; status: string; summary: string; stage: string };
```

UI-проекция метаданных tool: устойчивый ID, путь, этап, статус и сводка без raw content.

### `TaskRecoveryItem`

[Исходник](../../apps/desktop/shared/taskTypes.ts#L5)

```typescript
export type TaskRecoveryItem = { call_id: string; message_index: number; tool: string; path?: string; summary?: string };
```

Публичный якорь неизвестного эффекта: call ID, индекс сообщения, tool, безопасные path/summary.

### `TaskRecoveryResolution`

[Исходник](../../apps/desktop/shared/taskTypes.ts#L6)

```typescript
export type TaskRecoveryResolution = 'completed' | 'not_executed';
```

Два явных наблюдения пользователя: выполнено либо не выполнялось; исходный payload не выдумывается.

### `TaskSnapshot`

[Исходник](../../apps/desktop/shared/taskTypes.ts#L7)

```typescript
export type TaskSnapshot = {
  status: string; last_event: string; stage: string; turn: number; tool_calls: number;
  stages: TaskStage[]; tool_activity?: ToolActivity[]; activity_omitted?: number;
  workspace_changes?:{id:string;operation:string;path:string;destination?:string}[];project_instructions?:{path:string;scope:string;sha256:string}[];
  progress_watchdog?:{recovery_attempts:number};
  children?:{id:string;state:string;event:string;turn?:number;tool_calls?:number;activity?:Partial<ToolActivity>[];profile?:{title?:string;id?:string;version?:number}}[];
  options?:any;plan_steps?:(string|PlanNode)[];workspace_generation?:number;workspace_reverted?:boolean;workspace_reviewed?:boolean;snapshot_attention?:{id:string;status:string}[];checks_notice?:string;
  acceptance_evidence?:{id:string;description:string;status:string}[];
  verification_selection?:{required:string[];not_applicable:string[]};
  test_results?:{id:string;kind?:string;diagnostics?:{line:number;column:number;severity:number;message:string}[];program:string;arguments?:string[];purpose?:string;exit_code:number|null;ok:boolean;generation?:number;evidence_status?:string;evidence_summary?:string;coverage?:{kind:string;project_complete:boolean;files?:string[];dependencies?:string[]}}[];
  modified_files?: string[]; stop_reason?: string;
  run_state?: 'running'|'waiting_approval'|'executing'|'verifying'|'completed'|'needs_attention'|'paused'|'failed';
  journal_id?: string; recovery_items?: TaskRecoveryItem[]; recovery_error?: string;
  verification?:{status:'not_run'|'failed'|'commands_passed'|'scoped_passed'|'stale'|'incomplete';summary:string;uncovered?:string[];execution_status?:string;project_complete?:boolean};
  budget?:RequestBudgetSnapshot;usage?:ModelUsageSnapshot;
  chat_id?:string;run_id?:string;run_ledger?:import('./contextTypes').RunLedgerSnapshot;
  context_pack?:{version?:number;status:string;sources:{path:string;start_line:number;end_line:number;sha256:string;reason:string;kind:string}[];omitted?:number;budget_omitted?:number};
  context?:{compressed:boolean;before_chars:number;after_chars:number;archived_units?:number};
};
```

Тип полей checkpoint, используемых панелью плана и результатов.

<a id="module-apps-desktop-src-app-tsx"></a>

## `apps/desktop/src/App.tsx`

React-состояние и представление проекта, настроек, чата, потока, checkpoint, diff и безопасного мостика действий настольной Лолы в единый голосовой контур.

### `FileItem`

[Исходник](../../apps/desktop/src/App.tsx#L29)

```typescript
type FileItem = { name: string; path: string; kind: 'file' | 'directory' };
```

Тип элемента readonly-проводника: имя, относительный путь, вид файла/каталога.

### `ChatSummary`

[Исходник](../../apps/desktop/src/App.tsx#L30)

```typescript
type ChatSummary = { id: string; title: string };
```

Тип метаданных чата для бокового списка.

### `App`

[Исходник](../../apps/desktop/src/App.tsx#L33)

```typescript
function App()
```

Корневой React-компонент приложения с состояниями, эффектами и обработчиками.

### `App.attachEditorContext`

[Исходник](../../apps/desktop/src/App.tsx#L59)

```typescript
async function attachEditorContext()
```

Добавляет контекст выбранного редактором файла к следующему запросу.

### `App.take`

[Исходник](../../apps/desktop/src/App.tsx#L61)

```typescript
take()
```

Принимает переданный редактором черновик и контекст.

### `App.dismiss`

[Исходник](../../apps/desktop/src/App.tsx#L73)

```typescript
dismiss(e:KeyboardEvent)
```

Закрывает IDE drawer и возвращает клавиатурный фокус на кнопку открытия.

### `App.restoreBackgroundRuns`

[Исходник](../../apps/desktop/src/App.tsx#L109)

```typescript
function restoreBackgroundRuns(runs:any[])
```

Объединяет snapshot с более свежими событиями, не воскрешая завершённые run IDs при позднем IPC ответе.

### `App.report`

[Исходник](../../apps/desktop/src/App.tsx#L112)

```typescript
function report(text: string)
```

Добавляет диагностическую строку, сохраняя ограниченный хвост UI-лога.

### `App.showWarning`

[Исходник](../../apps/desktop/src/App.tsx#L113)

```typescript
function showWarning(text: string)
```

Публикует диагностическое предупреждение в логе и чате, не добавляя одинаковый текст повторно.

### `App.refreshChats`

[Исходник](../../apps/desktop/src/App.tsx#L117)

```typescript
async function refreshChats(scope = modeRef.current)
```

Запрашивает и обновляет список чатов.

### `App.receiveEvent.current`

[Исходник](../../apps/desktop/src/App.tsx#L135)

```typescript
receiveEvent.current(e)
```

Принимает lifecycle события всех чатов, буферизует target во время load и применяет к выбранному view только новые cursors правильного run.

### `App.closeProgress`

[Исходник](../../apps/desktop/src/App.tsx#L180)

```typescript
function closeProgress(restoreFocus=false)
```

Скрывает подробности без отмены задачи и при X/Escape возвращает фокус переключателю.

### `App.dismissProgress`

[Исходник](../../apps/desktop/src/App.tsx#L186)

```typescript
function dismissProgress(event:KeyboardEvent|PointerEvent)
```

Обрабатывает Escape и pointerdown вне панели; уважает уже обработанные события и модальные диалоги.

### `App.shortcuts`

[Исходник](../../apps/desktop/src/App.tsx#L201)

```typescript
function shortcuts(event:KeyboardEvent)
```

Обрабатывает Ctrl+S/F/G/Shift+R только в видимом editor и вне модальных диалогов.

### `App.clearSources`

[Исходник](../../apps/desktop/src/App.tsx#L215)

```typescript
clearSources()
```

Скрывает прежние source anchors после сохранения изменённых workspace grants до нового task snapshot.

### `App.resetConversation`

[Исходник](../../apps/desktop/src/App.tsx#L216)

```typescript
function resetConversation()
```

Сбрасывает UI-ссылки на чат/запуск, сообщения, checkpoint, approval и ввод.

### `App.switchWorkspace`

[Исходник](../../apps/desktop/src/App.tsx#L217)

```typescript
async function switchWorkspace(id:string)
```

Проверяет активность/черновики, переключает группу в Core и обновляет редактор, папку и историю.

### `App.openFork`

[Исходник](../../apps/desktop/src/App.tsx#L225)

```typescript
function openFork(result:any)
```

Открывает возвращённую копию, очищает checkpoint и подставляет запрос повтора во ввод.

### `App.openSearchFile`

[Исходник](../../apps/desktop/src/App.tsx#L226)

```typescript
async function openSearchFile(path:string, line:number)
```

Переходит в IDE и открывает результат на нужной строке, сохраняя sidebar поиска.

### `App.refreshFiles`

[Исходник](../../apps/desktop/src/App.tsx#L234)

```typescript
async function refreshFiles(path = '.')
```

Обновляет элементы и текущий относительный каталог проводника.

### `App.launchNativeIde`

[Исходник](../../apps/desktop/src/App.tsx#L238)

```typescript
async function launchNativeIde()
```

Открывает собственную IDE для выбранного workspace с проверкой состояния.

### `App.chooseProject`

[Исходник](../../apps/desktop/src/App.tsx#L241)

```typescript
async function chooseProject()
```

Выбор проекта: UI → native dialog → проверяемый set_project.

### `App.openWorktree`

[Исходник](../../apps/desktop/src/App.tsx#L257)

```typescript
async function openWorktree(id:string)
```

Через проверенный owned ID открывает копию, сбрасывает editor/chat projection и загружает scoped каталог.

### `App.switchMode`

[Исходник](../../apps/desktop/src/App.tsx#L265)

```typescript
async function switchMode(next: WorkspaceMode)
```

Переключает Chat/IDE/voice только в idle, сбрасывает выбранный UI-чат и загружает историю соответствующей области.

### `App.activateMiya`

[Исходник](../../apps/desktop/src/App.tsx#L276)

```typescript
async function activateMiya(text:string, send:boolean)
```

Открывает/фокусирует окно, переключает режим и передаёт распознанный текст Лоле.

### `App.openFile`

[Исходник](../../apps/desktop/src/App.tsx#L277)

```typescript
async function openFile(item: FileItem)
```

Открывает каталог или загружает текст файла в preview.

### `App.selectChat`

[Исходник](../../apps/desktop/src/App.tsx#L283)

```typescript
async function selectChat(id?: string, scope=modeRef.current)
```

Создаёт/загружает чат, заменяет UI-историю и checkpoint при отсутствии активной задачи.

### `App.openBackgroundRun`

[Исходник](../../apps/desktop/src/App.tsx#L302)

```typescript
async function openBackgroundRun(run:any)
```

Переходит в режим выбранного фонового чата и загружает его live snapshot без остановки других задач.

### `App.resolveToolRecovery`

[Исходник](../../apps/desktop/src/App.tsx#L308)

```typescript
async function resolveToolRecovery(item: TaskRecoveryItem, resolution: TaskRecoveryResolution)
```

Сериализует ручную проверку, вызывает фиксированный IPC и применяет возвращённые task/history только к прежнему выбранному чату.

### `App.returnToMiya`

[Исходник](../../apps/desktop/src/App.tsx#L325)

```typescript
async function returnToMiya()
```

Загружает исходный voice чат с добавленным результатом основной модели.

### `App.declineHandoff`

[Исходник](../../apps/desktop/src/App.tsx#L326)

```typescript
async function declineHandoff()
```

Очищает pending передачу и в Core, и в интерфейсе; старое задание больше не блокирует следующее.

### `App.acceptHandoff`

[Исходник](../../apps/desktop/src/App.tsx#L331)

```typescript
async function acceptHandoff()
```

Создаёт основную задачу из pending передачи, синхронизирует mode/chat/run refs и запускает модель.

### `App.renameChat`

[Исходник](../../apps/desktop/src/App.tsx#L348)

```typescript
async function renameChat()
```

Отправляет переименование выбранного chat ID в текущем scope и обновляет список после успешного сохранения.

### `App.configure`

[Исходник](../../apps/desktop/src/App.tsx#L357)

```typescript
async function configure()
```

Передаёт текущие поля модели сервису и выбрасывает ошибку при отказе.

### `App.sendPrompt`

[Исходник](../../apps/desktop/src/App.tsx#L361)

```typescript
async function sendPrompt(resume = false, voiceText?:string, checksOnly=false)
```

Проверяет готовность, блокирует повторный старт, создаёт чат и отправляет задачу/продолжение.

### `App.decide`

[Исходник](../../apps/desktop/src/App.tsx#L395)

```typescript
async function decide(decision: ApprovalDecision)
```

Передаёт явное решение по текущему approval агента, защищая от повторных кликов.

### `App.cancel`

[Исходник](../../apps/desktop/src/App.tsx#L404)

```typescript
async function cancel()
```

Показывает состояние остановки и вызывает cancelTask.

### `App.onRename`

[Исходник](../../apps/desktop/src/App.tsx#L413)

```typescript
onRename(c:ChatSummary)
```

Применяет новое название выбранного разговора из рабочего sidebar.

<a id="module-apps-desktop-src-appearancesettings-tsx"></a>

## `apps/desktop/src/AppearanceSettings.tsx`

Проверенные локальные настройки темы, акцента, плотности и панелей, синхронизация React и форма оформления.

### `Appearance`

[Исходник](../../apps/desktop/src/AppearanceSettings.tsx#L5)

```typescript
export type Appearance = {theme:LeshyTheme;backgroundArt:boolean;accent:'rose'|'violet'|'blue'|'mint';density:'comfortable'|'compact';sidebar:boolean;statusbar:boolean;output:boolean};
```

Разрешённые значения темы, акцента, плотности и трёх видимых панелей.

### `readAppearance`

[Исходник](../../apps/desktop/src/AppearanceSettings.tsx#L10)

```typescript
function readAppearance(): Appearance
```

Читает localStorage с whitelist и fallback; повреждённые или неподдерживаемые поля не ломают запуск.

### `saveAppearance`

[Исходник](../../apps/desktop/src/AppearanceSettings.tsx#L19)

```typescript
function saveAppearance(value:Appearance)
```

Сохраняет внешний вид локально и сообщает компонентам об изменении.

### `startAppearanceSync`

[Исходник](../../apps/desktop/src/AppearanceSettings.tsx#L27)

```typescript
function startAppearanceSync()
```

Подключает начальную тему и события, не позволяя позднему ответу перезаписать выбор пользователя.

### `startAppearanceSync.receive`

[Исходник](../../apps/desktop/src/AppearanceSettings.tsx#L29)

```typescript
receive(theme:unknown)
```

Принимает обновление темы и инвалидирует устаревшую начальную загрузку.

### `useAppearance`

[Исходник](../../apps/desktop/src/AppearanceSettings.tsx#L35)

```typescript
function useAppearance()
```

Подписывает React на локальное событие настроек и storage, удаляет обработчики при unmount.

### `useAppearance.refresh`

[Исходник](../../apps/desktop/src/AppearanceSettings.tsx#L38)

```typescript
refresh()
```

Перечитывает и проверяет оформление после изменения в этом или другом окне.

### `AppearanceSettings`

[Исходник](../../apps/desktop/src/AppearanceSettings.tsx#L42)

```typescript
function AppearanceSettings()
```

Показывает темы, акценты, плотность и панели с немедленным применением без изменения модели.

### `AppearanceSettings.update`

[Исходник](../../apps/desktop/src/AppearanceSettings.tsx#L44)

```typescript
function update(patch:Partial<Appearance>)
```

Применяет частичное изменение оформления и показывает результат сохранения.

<a id="module-apps-desktop-src-approvaldialog-tsx"></a>

## `apps/desktop/src/ApprovalDialog.tsx`

Рабочий модальный запрос разрешения с типизированным решением и сведениями о действии.

### `ApprovalDialog`

[Исходник](../../apps/desktop/src/ApprovalDialog.tsx#L3)

```typescript
function ApprovalDialog({approval,deciding,onDecide,onLater}:{approval:CoreEvent;deciding:boolean;onDecide:(decision:ApprovalDecision)=>void;onLater:()=>void})
```

Показывает настоящее ожидающее разрешение, preview и доступные решения через callback.

<a id="module-apps-desktop-src-brandmark-tsx"></a>

## `apps/desktop/src/BrandMark.tsx`

Векторный знак Neutral: N и точка равновесия; цвет наследуется от темы.

### `BrandMark`

[Исходник](../../apps/desktop/src/BrandMark.tsx#L2)

```typescript
function BrandMark({size=28}:{size?:number})
```

Рисует прежний знак N с точкой равновесия в геометрии и цветах Studio; статические PNG/ICO используют ту же форму.

<a id="module-apps-desktop-src-chattext-tsx"></a>

## `apps/desktop/src/ChatText.tsx`

Безопасные текстовые/code блоки без HTML, memoized parser и явное копирование.

### `TextPart`

[Исходник](../../apps/desktop/src/ChatText.tsx#L2)

```typescript
export type TextPart={code:boolean;text:string;language:string};
```

Один plain/code сегмент безопасного текстового renderer с подписью языка.

### `splitCodeBlocks`

[Исходник](../../apps/desktop/src/ChatText.tsx#L3)

```typescript
function splitCodeBlocks(text:string): TextPart[]
```

Линейно разбирает отдельные тройные backtick fences, включая незакрытый streaming code block; HTML не интерпретируется.

### `splitCodeBlocks.flush`

[Исходник](../../apps/desktop/src/ChatText.tsx#L3)

```typescript
flush()
```

Добавляет накопленные строки текущего сегмента и очищает буфер.

### `inline`

[Исходник](../../apps/desktop/src/ChatText.tsx#L4)

```typescript
function inline(text:string)
```

Разбирает безопасные inline code, выделение и HTTP(S) ссылки без raw HTML.

### `Markdown`

[Исходник](../../apps/desktop/src/ChatText.tsx#L5)

```typescript
function Markdown({text}:{text:string})
```

Отображает ограниченный Markdown ответа с кодом, таблицами, списками и заголовками.

### `Markdown.cells`

[Исходник](../../apps/desktop/src/ChatText.tsx#L5)

```typescript
cells(v:string)
```

Выделяет ячейки строк Markdown-таблицы по разделителям.

### `ChatText`

[Исходник](../../apps/desktop/src/ChatText.tsx#L6)

```typescript
function ChatText({text}:{text:string})
```

Memoizes разбор текста, выводит code как React text nodes и показывает кнопку копирования.

### `ChatText.copy`

[Исходник](../../apps/desktop/src/ChatText.tsx#L6)

```typescript
async function copy(value:string, index:number)
```

Пишет только выбранный code segment через Clipboard API и показывает успех/ошибку.

<a id="module-apps-desktop-src-companionsettings-tsx"></a>

## `apps/desktop/src/CompanionSettings.tsx`

Настройка характера, независимой модели, JSON/native protocol, автоматической передачи и STT Лолы.

### `CompanionSettings`

[Исходник](../../apps/desktop/src/CompanionSettings.tsx#L4)

```typescript
function CompanionSettings({profile,busy,onSaved}:{profile:any;busy:boolean;onSaved:(profile:any)=>void})
```

Форма собственного характера, модели, tool protocol, автоматической передачи и STT профиля Лолы.

### `CompanionSettings.save`

[Исходник](../../apps/desktop/src/CompanionSettings.tsx#L10)

```typescript
async function save()
```

Валидирует профиль в Core, сохраняет публичные настройки, не сохраняет API keys.

### `CompanionSettings.discover`

[Исходник](../../apps/desktop/src/CompanionSettings.tsx#L18)

```typescript
async function discover()
```

Загружает модели именно с чернового endpoint Лолы без изменения основной конфигурации.

<a id="module-apps-desktop-src-connectionprofiles-tsx"></a>

## `apps/desktop/src/ConnectionProfiles.tsx`

Сохранение, выбор и удаление публичных профилей подключения модели.

### `ConnectionProfiles`

[Исходник](../../apps/desktop/src/ConnectionProfiles.tsx#L5)

```typescript
function ConnectionProfiles({value,locked,onSelect}:{value:ModelConfig;locked:boolean;onSelect:(config:ModelConfig)=>void})
```

Показывает сохранённые подключения, имя профиля и действия сохранения/удаления.

### `ConnectionProfiles.refresh`

[Исходник](../../apps/desktop/src/ConnectionProfiles.tsx#L7)

```typescript
async function refresh()
```

Обновляет только чистую вкладку после записи агента, dirty draft сохраняет и предупреждает о конфликте.

### `ConnectionProfiles.save`

[Исходник](../../apps/desktop/src/ConnectionProfiles.tsx#L9)

```typescript
async function save()
```

Получает preview по исходной byte revision, не пишет файл и показывает отдельный диалог.

### `ConnectionProfiles.remove`

[Исходник](../../apps/desktop/src/ConnectionProfiles.tsx#L10)

```typescript
async function remove()
```

Удаляет подтверждённый профиль и обновляет список без смены активной модели.

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

[Исходник](../../apps/desktop/src/ConnectionsSettings.tsx#L16)

```typescript
refresh()
```

Обновляет безопасный статус Telegram с cleanup при закрытии настроек.

### `ConnectionsSettings.toggle`

[Исходник](../../apps/desktop/src/ConnectionsSettings.tsx#L20)

```typescript
async function toggle()
```

Применяет переключатель PC tools через Core только вне задачи.

### `ConnectionsSettings.connect`

[Исходник](../../apps/desktop/src/ConnectionsSettings.tsx#L24)

```typescript
async function connect(saved=false)
```

Передаёт token/owner и флаг remember/use_saved; очищает поле token после подключения.

### `ConnectionsSettings.changeApplication`

[Исходник](../../apps/desktop/src/ConnectionsSettings.tsx#L29)

```typescript
async function changeApplication(id?:string)
```

Добавляет EXE через системный picker или удаляет разрешение по ID, обновляет список и ошибки в UI.

<a id="module-apps-desktop-src-contextusage-tsx"></a>

## `apps/desktop/src/ContextUsage.tsx`

Карточка оценки полного контекста, состава входа, отложенных MCP-схем и фактического usage сервера.

### `ContextUsage`

[Исходник](../../apps/desktop/src/ContextUsage.tsx#L3)

```typescript
function ContextUsage({budget,usage}:{budget?:RequestBudgetSnapshot;usage?:ModelUsageSnapshot})
```

Показывает состав контекста, резерв и причины сжатия отдельно от фактического reported usage.

### `ContextUsage.number`

[Исходник](../../apps/desktop/src/ContextUsage.tsx#L5)

```typescript
number(value:number)
```

Форматирует значения токенов в русской локали без изменения бюджета.

<a id="module-apps-desktop-src-conversationsidebar-tsx"></a>

## `apps/desktop/src/ConversationSidebar.tsx`

Проекты, поиск разговоров, закрепление, архив, копии, повтор, экспорт, перемещение и удаление.

### `Project`

[Исходник](../../apps/desktop/src/ConversationSidebar.tsx#L5)

```typescript
type Project={id:string;name:string;root:string;instructions:string};
```

Публичные поля пространства: ID, имя, папка и инструкции.

### `Conversation`

[Исходник](../../apps/desktop/src/ConversationSidebar.tsx#L6)

```typescript
type Conversation={id:string;title:string;snippet?:string;pinned?:boolean;archived?:boolean;project_root?:string};
```

Метаданные строки истории, фрагмент поиска и флаги pin/archive.

### `Props`

[Исходник](../../apps/desktop/src/ConversationSidebar.tsx#L7)

```typescript
type Props={showWorkspace?:boolean;mode:string;root:string;visible:boolean;busy:boolean;navigating?:boolean;activeId:string;refresh:unknown;workspaceId:string;onWorkspace:(id:string)=>Promise<boolean>;onOpen:(id?:string)=>void;onRename:(chat:Conversation)=>void;onReset:()=>void;onFork:(result:any)=>void;onError:(text:string)=>void};
```

Контракт sidebar с App: выбранный режим/проект, callbacks открытия, сброса, копии и ошибок.

### `ConversationSidebar`

[Исходник](../../apps/desktop/src/ConversationSidebar.tsx#L9)

```typescript
function ConversationSidebar({showWorkspace=true,mode,root,visible,busy,navigating=false,activeId,refresh,workspaceId,onWorkspace,onOpen,onRename,onReset,onFork,onError}:Props)
```

Управляет проектами и scoped-историей через конкретные preload методы.

### `ConversationSidebar.run`

[Исходник](../../apps/desktop/src/ConversationSidebar.tsx#L20)

```typescript
async function run(action:()=>Promise<any>, message='')
```

Сериализует GUI-действие, выводит ошибку и обновляет каталог после успеха.

### `ConversationSidebar.update`

[Исходник](../../apps/desktop/src/ConversationSidebar.tsx#L26)

```typescript
async function update(chat:Conversation, values:Record<string,unknown>)
```

Применяет флаги/перемещение и сбрасывает активный чат при выходе из текущего списка.

### `ConversationSidebar.saveProject`

[Исходник](../../apps/desktop/src/ConversationSidebar.tsx#L30)

```typescript
async function saveProject()
```

Сохраняет форму проекта и переключает приложение на созданное/изменённое пространство.

### `ConversationSidebar.remove`

[Исходник](../../apps/desktop/src/ConversationSidebar.tsx#L34)

```typescript
async function remove()
```

Выполняет явно подтверждённое удаление чата/группы и обновляет активный выбор.

<a id="module-apps-desktop-src-desktoplolasettings-tsx"></a>

## `apps/desktop/src/DesktopLolaSettings.tsx`

Переиспользуемая доступная форма включения спутника, режима окон, размера и анимации с применением настроек.

### `DesktopLolaSettings`

[Исходник](../../apps/desktop/src/DesktopLolaSettings.tsx#L4)

```typescript
function DesktopLolaSettings()
```

Общая пользовательская настройка opt-in спутника из главного Voice settings.

### `DesktopLolaSettings.save`

[Исходник](../../apps/desktop/src/DesktopLolaSettings.tsx#L7)

```typescript
async function save(value=draft)
```

Применяет валидацию в main process и показывает результат сохранения.

<a id="module-apps-desktop-src-desktoplolaview-tsx"></a>

## `apps/desktop/src/DesktopLolaView.tsx`

Компактная оболочка спутника: bounded chat input, управление голосом, перетаскивание, виджет состояний и вызовы узкого preload API.

### `DesktopLolaView`

[Исходник](../../apps/desktop/src/DesktopLolaView.tsx#L12)

```typescript
function DesktopLolaView()
```

Отдельный overlay UI для компактного вопроса/ответа, drag и контролов существующего voice owner.

### `DesktopLolaView.change`

[Исходник](../../apps/desktop/src/DesktopLolaView.tsx#L23)

```typescript
change()
```

Обновляет движение персонажа при смене системного reduced-motion preference.

### `DesktopLolaView.pointer`

[Исходник](../../apps/desktop/src/DesktopLolaView.tsx#L26)

```typescript
function pointer(event:MouseEvent)
```

Определяет интерактивные hit areas для click-through native окна.

### `DesktopLolaView.leave`

[Исходник](../../apps/desktop/src/DesktopLolaView.tsx#L27)

```typescript
function leave()
```

Возвращает сквозные клики, когда окно теряет pointer focus.

### `DesktopLolaView.action`

[Исходник](../../apps/desktop/src/DesktopLolaView.tsx#L31)

```typescript
async function action(kind:'record'|'stop'|'settings'|'ask'|'speak')
```

Отправляет allowlisted команду и локально показывает bounded ошибку.

<a id="module-apps-desktop-src-editorpanel-tsx"></a>

## `apps/desktop/src/EditorPanel.tsx`

Рабочие вкладки/черновики редактора, виртуальный gutter, поиск/строка, hotkeys, reload и подтверждённое сохранение.

### `EditorDocument`

[Исходник](../../apps/desktop/src/EditorPanel.tsx#L6)

```typescript
export type EditorDocument = {path:string; content:string; original:string; revision:{path:string; sha256:string}; newline:string};
```

Документ вкладки: текущий текст, исходный текст, byte revision и стиль строк.

### `EditorHandle`

[Исходник](../../apps/desktop/src/EditorPanel.tsx#L7)

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

[Исходник](../../apps/desktop/src/EditorPanel.tsx#L13)

```typescript
type EditorProps = {root:string; busy:boolean; visible:boolean; onActive:(path:string)=>void;
  onDirty:(dirty:boolean)=>void; onProject:()=>void; onModels:()=>void; onLog:(text:string)=>void};
```

Корень/видимость/busy и callbacks редактора; file access остаётся в Core.

### `EditorPanel`

[Исходник](../../apps/desktop/src/EditorPanel.tsx#L16)

```typescript
EditorPanel(props, ref)
```

Компонент редактора с сохраняемыми между режимами вкладками и snapshot-approval.

### `EditorPanel.reset`

[Исходник](../../apps/desktop/src/EditorPanel.tsx#L60)

```typescript
function reset()
```

Сбрасывает editor-вкладки, pending diff и уведомления после подтверждённой смены проекта.

### `EditorPanel.selectDocument`

[Исходник](../../apps/desktop/src/EditorPanel.tsx#L63)

```typescript
function selectDocument(document:EditorDocument)
```

Добавляет или заменяет документ вкладки и выбирает его активным.

### `EditorPanel.read`

[Исходник](../../apps/desktop/src/EditorPanel.tsx#L68)

```typescript
async function read(path:string)
```

Запрашивает strict editor_read и отбрасывает ответ, относящийся к уже сменившемуся корню.

### `EditorPanel.open`

[Исходник](../../apps/desktop/src/EditorPanel.tsx#L75)

```typescript
async function open(path:string, line?:number)
```

Открывает существующую вкладку без потери draft либо читает файл; может перейти к нужной строке.

### `EditorPanel.refresh`

[Исходник](../../apps/desktop/src/EditorPanel.tsx#L91)

```typescript
async function refresh(path:string)
```

Обновляет только чистую вкладку после записи агента, dirty draft сохраняет и предупреждает о конфликте.

### `EditorPanel.hasDirty`

[Исходник](../../apps/desktop/src/EditorPanel.tsx#L100)

```typescript
hasDirty()
```

Читает актуальные editor tabs через ref для проверки unsaved перед нативной сменой проекта.

### `EditorPanel.closeTab`

[Исходник](../../apps/desktop/src/EditorPanel.tsx#L102)

```typescript
async function closeTab(path:string)
```

Закрывает вкладку; грязный текст требует явного подтверждения отказа от сохранения.

### `EditorPanel.reload`

[Исходник](../../apps/desktop/src/EditorPanel.tsx#L110)

```typescript
async function reload()
```

Перечитывает активный файл после подтверждения потери draft; при ошибке текст остаётся.

### `EditorPanel.save`

[Исходник](../../apps/desktop/src/EditorPanel.tsx#L116)

```typescript
async function save()
```

Получает preview по исходной byte revision, не пишет файл и показывает отдельный диалог.

### `EditorPanel.decide`

[Исходник](../../apps/desktop/src/EditorPanel.tsx#L127)

```typescript
async function decide(decision:string)
```

Потребляет editor proposal через Apply/Reject/Cancel; при отказе или конфликте сохраняет draft, после успеха обновляет revision.

### `EditorPanel.updatePosition`

[Исходник](../../apps/desktop/src/EditorPanel.tsx#L141)

```typescript
function updatePosition()
```

Вычисляет line/column по положению selectionStart в UTF-16 textarea.

### `EditorPanel.moveToLine`

[Исходник](../../apps/desktop/src/EditorPanel.tsx#L147)

```typescript
function moveToLine(line:number)
```

Ограничивает номер строки, вычисляет offset и перемещает курсор/прокрутку.

### `EditorPanel.findNext`

[Исходник](../../apps/desktop/src/EditorPanel.tsx#L156)

```typescript
function findNext()
```

Ищет следующую текстовую строку без учёта регистра с циклическим возвратом в начало файла.

### `EditorPanel.shortcuts`

[Исходник](../../apps/desktop/src/EditorPanel.tsx#L167)

```typescript
function shortcuts(event:KeyboardEvent)
```

Обрабатывает Ctrl+S/F/G/Shift+R только в видимом editor и вне модальных диалогов.

<a id="module-apps-desktop-src-extensionssettings-tsx"></a>

## `apps/desktop/src/ExtensionsSettings.tsx`

Настройки наборов, отдельных tools, навыков, JSON-пакетов и MCP серверов.

### `Skill`

[Исходник](../../apps/desktop/src/ExtensionsSettings.tsx#L5)

```typescript
type Skill={id:string;title:string;summary:string;content?:string;enabled:boolean;source:string};
```

Публичная инструкция навыка, происхождение и состояние включения.

### `ExtensionsSettings`

[Исходник](../../apps/desktop/src/ExtensionsSettings.tsx#L8)

```typescript
function ExtensionsSettings({busy}:{busy:boolean})
```

Интерфейс пакетов, групп, tools, навыков, MCP подключения/проверки и подтверждения удаления.

### `ExtensionsSettings.run`

[Исходник](../../apps/desktop/src/ExtensionsSettings.tsx#L14)

```typescript
async function run(action:()=>Promise<any>, message='Настройки применены к следующим запросам.')
```

Ограничивает одновременные операции и перечитывает публичный реестр после успеха.

### `ExtensionsSettings.toggle`

[Исходник](../../apps/desktop/src/ExtensionsSettings.tsx#L20)

```typescript
toggle(kind:string, id:string, enabled:boolean)
```

Отправляет переключение конкретной возможности через валидируемый Core метод.

### `ExtensionsSettings.includes`

[Исходник](../../apps/desktop/src/ExtensionsSettings.tsx#L21)

```typescript
includes(...values:string[])
```

Локально фильтрует название/описание по строке поиска расширений.

### `ExtensionsSettings.saveSkill`

[Исходник](../../apps/desktop/src/ExtensionsSettings.tsx#L22)

```typescript
async function saveSkill()
```

Сохраняет пользовательскую инструкцию, оставляя явное включение отдельным действием.

### `ExtensionsSettings.saveServer`

[Исходник](../../apps/desktop/src/ExtensionsSettings.tsx#L27)

```typescript
async function saveServer()
```

Преобразует строки аргументов в массив и сохраняет MCP публично, токен передаётся отдельно.

### `ExtensionsSettings.discoverServer`

[Исходник](../../apps/desktop/src/ExtensionsSettings.tsx#L32)

```typescript
async function discoverServer(id:string)
```

Показывает ожидание конкретного MCP сервера, получает каталог и сбрасывает состояние после ответа исходного запроса.

### `ExtensionsSettings.cancelDiscovery`

[Исходник](../../apps/desktop/src/ExtensionsSettings.tsx#L38)

```typescript
async function cancelDiscovery()
```

Отменяет проверку MCP через отдельный IPC без создания повторной discovery.

<a id="module-apps-desktop-src-generationfields-tsx"></a>

## `apps/desktop/src/GenerationFields.tsx`

Единые типы, значения, диапазоны, подсказки и форма генерации для Chat/IDE и отдельной модели Лолы.

### `GenerationSettings`

[Исходник](../../apps/desktop/src/GenerationFields.tsx#L1)

```typescript
export type GenerationSettings = {
  temperature: number; top_p: number; max_tokens: number; max_context_chars: number;
  request_timeout: number; max_agent_turns: number; max_runtime_minutes: number;
  context_window:number; context_reserve_tokens:number; memory_updates:'off'|'on_change'|'always';
  budget_mode:'auto'|'manual';
  paid_budget?:{enabled:boolean;amount:number;input_per_million:number;output_per_million:number;currency:'USD'|'EUR'|'RUB'};
};
```

Числовой контракт семи применяемых настроек: sampling, token/context budgets, HTTP timeout и ограничения цикла.

### `GenerationFields`

[Исходник](../../apps/desktop/src/GenerationFields.tsx#L26)

```typescript
function GenerationFields({value,locked,onChange}:{value:GenerationSettings;locked:boolean;onChange:(settings:GenerationSettings)=>void})
```

Показывает числовые лимиты, окно/резерв, пресеты 4K/8K/32K и явный режим обновления памяти.

<a id="module-apps-desktop-src-idetaskoptions-tsx"></a>

## `apps/desktop/src/IdeTaskOptions.tsx`

Компактные параметры задачи IDE: только чтение, критерии, команды и post-edit проверки.

### `serializeIdeOptions`

[Исходник](../../apps/desktop/src/IdeTaskOptions.tsx#L7)

```typescript
function serializeIdeOptions(value:IdeOptions, checks_only=false)
```

Убирает пустые строки критериев с сохранением правильных связей check_ids по новым индексам.

### `IdeTaskOptions`

[Исходник](../../apps/desktop/src/IdeTaskOptions.tsx#L12)

```typescript
function IdeTaskOptions({value,onChange,busy,onRunChecks}:{value:IdeOptions;onChange:(value:IdeOptions)=>void;busy:boolean;onRunChecks:()=>void})
```

Сворачиваемая форма IDE с readonly, критериями, командами и запуском проверок без модели.

### `IdeTaskOptions.updateCheck`

[Исходник](../../apps/desktop/src/IdeTaskOptions.tsx#L13)

```typescript
function updateCheck(id:string, values:Partial<ValidationCommand>)
```

Изменяет одну проверку по ID, сохраняя остальные настройки задачи.

### `IdeTaskOptions.removeCheck`

[Исходник](../../apps/desktop/src/IdeTaskOptions.tsx#L14)

```typescript
function removeCheck(id:string)
```

Удаляет проверку вместе с её ссылками из критериев.

<a id="module-apps-desktop-src-localruntimepanel-tsx"></a>

## `apps/desktop/src/LocalRuntimePanel.tsx`

Реальный GGUF picker, context/GPU, lifecycle status и явный перенос endpoint в настройки.

### `LocalRuntimePanel`

[Исходник](../../apps/desktop/src/LocalRuntimePanel.tsx#L3)

```typescript
function LocalRuntimePanel({locked,onUse}:{locked:boolean;onUse:(url:string,model:string,context:number)=>void})
```

Управляет локальным GGUF и переносит endpoint, модель и настоящий ctx_size в черновик настроек без автоматического сохранения.

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

<a id="module-apps-desktop-src-lolaavatar-tsx"></a>

## `apps/desktop/src/LolaAvatar.tsx`

Чиби по референсу: выбор ряда атласа 4×7 по состоянию Лолы, подпись, речевая волна и уменьшение движения.

### `LolaState`

[Исходник](../../apps/desktop/src/LolaAvatar.tsx#L4)

```typescript
export type LolaState='idle'|'listening'|'thinking'|'working'|'speaking'|'success'|'error';
```

Допустимые состояния персонажа: ожидание, слушание, размышление, работа, речь, успех и ошибка.

### `LolaAvatar`

[Исходник](../../apps/desktop/src/LolaAvatar.tsx#L8)

```typescript
function LolaAvatar({state,reducedMotion=false}:{state:LolaState;reducedMotion?:boolean})
```

Выбирает четыре кадра нужного состояния из чиби-атласа, показывает подпись и поддерживает отключение анимации.

<a id="module-apps-desktop-src-memorypanel-tsx"></a>

## `apps/desktop/src/MemoryPanel.tsx`

Редактор семи полей памяти выбранного проекта с сохранением draft при конфликте.

### `MemoryPanel`

[Исходник](../../apps/desktop/src/MemoryPanel.tsx#L15)

```typescript
function MemoryPanel({root,busy,onClose}:{root:string;busy:boolean;onClose:()=>void})
```

Модальный редактор ограниченной памяти IDE; Chat не использует эти заметки.

### `MemoryPanel.show`

[Исходник](../../apps/desktop/src/MemoryPanel.tsx#L24)

```typescript
function show(result:any)
```

Проверяет ответ/корень, преобразует списки в строки и фиксирует original/revision после успешного чтения или записи.

### `MemoryPanel.save`

[Исходник](../../apps/desktop/src/MemoryPanel.tsx#L35)

```typescript
async function save()
```

Преобразует строки списков, отправляет snapshot revision, при конфликте сохраняет draft в окне.

### `MemoryPanel.close`

[Исходник](../../apps/desktop/src/MemoryPanel.tsx#L43)

```typescript
function close()
```

Закрывает чистую форму; для dirty показывает явный выбор сохранить редактирование или потерять draft.

<a id="module-apps-desktop-src-modelsettings-tsx"></a>

## `apps/desktop/src/ModelSettings.tsx`

Общее окно Neutral с боковыми разделами моделей, Лолы, расширений, ПК, оформления, контекста и runtime.

### `ModelConfig`

[Исходник](../../apps/desktop/src/ModelSettings.tsx#L15)

```typescript
export type ModelConfig = { api_protocol?:string; tool_protocol?: string; base_url: string; model: string; api_key: string; settings: GenerationSettings };
```

Конфигурация окна/IPC: URL, ID, временный API-ключ и числовые настройки.

### `ModelSettings`

[Исходник](../../apps/desktop/src/ModelSettings.tsx#L16)

```typescript
function ModelSettings({ initial, busy, onSaved, onClose, onIde, initialSection='connection' }: {
  initial: ModelConfig; busy: boolean; onSaved: (config: ModelConfig) => void; onClose: () => void;onIde?:()=>void;initialSection?:string;
})
```

Модальное окно с отдельным draft; применяет настройки только после успешного backend save.

### `ModelSettings.change`

[Исходник](../../apps/desktop/src/ModelSettings.tsx#L34)

```typescript
function change(key: K, value: ModelConfig[K])
```

Меняет поле черновика и помечает его несохранённым; новый URL сбрасывает устаревший список моделей.

### `ModelSettings.validate`

[Исходник](../../apps/desktop/src/ModelSettings.tsx#L39)

```typescript
function validate()
```

Проверяет URL и диапазоны полей до отправки, backend повторяет обязательную валидацию.

### `ModelSettings.perform`

[Исходник](../../apps/desktop/src/ModelSettings.tsx#L57)

```typescript
async function perform(action: 'discover' | 'probe' | 'save')
```

Последовательно выполняет discovery, bounded probe или save с явным статусом и обработкой ошибок в окне.

### `ModelSettings.resetGeneration`

[Исходник](../../apps/desktop/src/ModelSettings.tsx#L84)

```typescript
function resetGeneration()
```

Возвращает числовые поля к defaults только в черновике, не меняет endpoint/ID/ключ.

### `ModelSettings.handleKeys`

[Исходник](../../apps/desktop/src/ModelSettings.tsx#L87)

```typescript
function handleKeys(event: React.KeyboardEvent<HTMLElement>)
```

Закрывает окно по Escape вне операции и удерживает Tab-навигацию в доступных контролах диалога.

<a id="module-apps-desktop-src-neuralaudio-tsx"></a>

## `apps/desktop/src/NeuralAudio.tsx`

Единый плеер нейроозвучки: PCM WAV из Core, громкость/темп, Stop и подтверждение завершения.

### `NeuralAudio`

[Исходник](../../apps/desktop/src/NeuralAudio.tsx#L3)

```typescript
function NeuralAudio()
```

Проигрывает только события Core, останавливает старый Audio и подтверждает текущую озвучку.

### `NeuralAudio.player.onended`

[Исходник](../../apps/desktop/src/NeuralAudio.tsx#L14)

```typescript
player.onended()
```

Подтверждает завершение только текущего Audio по sequence.

### `NeuralAudio.player.onerror`

[Исходник](../../apps/desktop/src/NeuralAudio.tsx#L15)

```typescript
player.onerror()
```

Сообщает Core о невозможности воспроизведения текущего Audio.

<a id="module-apps-desktop-src-optionalidepanel-tsx"></a>

## `apps/desktop/src/OptionalIdePanel.tsx`

Модальная тематическая панель исследователя/LSP/worktrees/изоляции с бюджетами, подтверждением, отменой и явным добавлением отчёта в задачу.

### `OptionalIdePanel`

[Исходник](../../apps/desktop/src/OptionalIdePanel.tsx#L8)

```typescript
function OptionalIdePanel({visible,root,path,busy,dirty,onClose,onWorking,onOpen,onUse,onWorktree}:{visible:boolean;root:string;path:string;busy:boolean;dirty:boolean;onClose:()=>void;onWorking:(value:boolean)=>void;onOpen:(path:string,line:number)=>void;onUse:(text:string)=>void;onWorktree:(id:string)=>Promise<void>})
```

Нативный modal dialog с явными opt-in, сохранением settings, stop, отчётом, diagnostics и подтверждёнными Git effects.

### `OptionalIdePanel.save`

[Исходник](../../apps/desktop/src/OptionalIdePanel.tsx#L17)

```typescript
async function save()
```

Сохраняет проверенные настройки и блокирует повторный клик через ref до завершения IPC.

### `OptionalIdePanel.run`

[Исходник](../../apps/desktop/src/OptionalIdePanel.tsx#L23)

```typescript
async function run(request:OptionalRequest)
```

Один job, root correlation, ошибки и обновление списков без автоотправки отчёта модели.

### `OptionalIdePanel.confirm`

[Исходник](../../apps/desktop/src/OptionalIdePanel.tsx#L30)

```typescript
async function confirm()
```

Создаёт/удаляет копию только по отдельному явному подтверждению, затем обновляет список.

<a id="module-apps-desktop-src-projectknowledgepanel-tsx"></a>

## `apps/desktop/src/ProjectKnowledgePanel.tsx`

Редактор решений, фактов и гипотез; источники, статусы актуальности, поиск, исправление и удаление без model calls.

### `RecordNote`

[Исходник](../../apps/desktop/src/ProjectKnowledgePanel.tsx#L3)

```typescript
type RecordNote={id:string;kind:string;text:string;state:string;origin:string;created_at:string;updated_at:string;sources:{path:string;sha256:string}[];provenance:Record<string,unknown>};
```

Запись памяти с типом, источниками, временем, происхождением и вычисленным состоянием актуальности.

### `Draft`

[Исходник](../../apps/desktop/src/ProjectKnowledgePanel.tsx#L4)

```typescript
type Draft={id?:string;kind:string;text:string;paths:string};
```

Локальный черновик user-owned решения, факта или гипотезы до CAS сохранения.

### `ProjectKnowledgePanel`

[Исходник](../../apps/desktop/src/ProjectKnowledgePanel.tsx#L7)

```typescript
function ProjectKnowledgePanel({records,root,revision,busy,onResult}:{records:RecordNote[];root:string;revision:string;busy:boolean;onResult:(value:any)=>void})
```

Показывает bounded список записей и редактор источников в существующем стиле Studio.

### `ProjectKnowledgePanel.action`

[Исходник](../../apps/desktop/src/ProjectKnowledgePanel.tsx#L9)

```typescript
async function action(params:any)
```

Передаёт fixed IPC с revision/root; сохраняет черновик при конфликте и обновляет UI только при успехе.

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

[Исходник](../../apps/desktop/src/ProjectSearch.tsx#L22)

```typescript
async function search()
```

Последовательно отменяет предыдущий запрос, отправляет новый и применяет только актуальный ticket/root.

### `ProjectSearch.cancel`

[Исходник](../../apps/desktop/src/ProjectSearch.tsx#L38)

```typescript
function cancel()
```

Инвалидирует результаты и запрашивает отмену собственного поиска.

### `ProjectSearch.refresh`

[Исходник](../../apps/desktop/src/ProjectSearch.tsx#L52)

```typescript
async function refresh()
```

Периодически получает лёгкий статус индекса только для текущей видимой панели; cleanup отбрасывает поздние ответы.

### `ProjectSearch.indexAction`

[Исходник](../../apps/desktop/src/ProjectSearch.tsx#L56)

```typescript
async function indexAction(action:string)
```

Вызывает только status/rebuild/cancel индекса и показывает ошибку без запуска модели/команд.

<a id="module-apps-desktop-src-runhistory-tsx"></a>

## `apps/desktop/src/RunHistory.tsx`

История epochs выбранного чата, физические HTTP попытки, известный usage, текущие оценки и время ожиданий.

### `Ledger`

[Исходник](../../apps/desktop/src/RunHistory.tsx#L4)

```typescript
function Ledger({value}:{value:RunLedgerSnapshot})
```

Показывает физические HTTP, только сообщённые tokens, outstanding estimates и wait time; не выдаёт unknown usage за ноль.

### `RunHistory`

[Исходник](../../apps/desktop/src/RunHistory.tsx#L13)

```typescript
function RunHistory({chatId,runId,ledger}:{chatId?:string;runId?:string;ledger?:RunLedgerSnapshot})
```

Загружает bounded epochs выбранного чата при раскрытии, отбрасывает поздние ответы и позволяет обновить историю.

<a id="module-apps-desktop-src-sourcecontextpreview-tsx"></a>

## `apps/desktop/src/SourceContextPreview.tsx`

Читаемый предпросмотр получателя, модели, диапазонов и полного текста автоматически выбранных исходников перед одной отправкой.

### `SourceContextPreview`

[Исходник](../../apps/desktop/src/SourceContextPreview.tsx#L1)

```typescript
function SourceContextPreview({text}:{text:string})
```

Показывает адрес получателя, модель и неизменённые source bodies; полный JSON доступен отдельно, HTML из исходников не исполняется.

<a id="module-apps-desktop-src-storagesettings-tsx"></a>

## `apps/desktop/src/StorageSettings.tsx`

История и копии в настройках: проверка целостности, счётчики миграции, локальный ZIP export и явные ошибки.

### `StorageReport`

[Исходник](../../apps/desktop/src/StorageSettings.tsx#L4)

```typescript
type StorageReport = {version:number;integrity:string;migration:{chats:number;messages:number};counts:{chats:number;messages:number;projects:number};sources:{status:string;path:string}[]};
```

Публичные счётчики, результат integrity check и итоги копирующей миграции без содержимого чатов.

### `StorageSettings`

[Исходник](../../apps/desktop/src/StorageSettings.tsx#L6)

```typescript
function StorageSettings({busy}:{busy:boolean})
```

Раздел истории/копий в существующем дизайне настроек; запрос только при открытии раздела.

### `StorageSettings.inspectStorage`

[Исходник](../../apps/desktop/src/StorageSettings.tsx#L8)

```typescript
async function inspectStorage()
```

Показывает текущую целостность и счётчики или явную ошибку; никакие данные не изменяет.

### `StorageSettings.backupStorage`

[Исходник](../../apps/desktop/src/StorageSettings.tsx#L15)

```typescript
async function backupStorage()
```

Открывает системный выбор ZIP, отображает отмену, ошибку либо подтверждённый путь готовой копии.

<a id="module-apps-desktop-src-studiocontrols-tsx"></a>

## `apps/desktop/src/StudioControls.tsx`

Сохраняемая раскладка, доступные разделители панелей, модель под запросом, журнал инструментов и фокус модальных окон.

### `Panel`

[Исходник](../../apps/desktop/src/StudioControls.tsx#L6)

```typescript
type Panel='sidebar'|'agent'|'context'|'settings';
```

Допустимые изменяемые панели: навигация, агент, контекст и категории настроек.

### `Layout`

[Исходник](../../apps/desktop/src/StudioControls.tsx#L7)

```typescript
type Layout={sidebar:number;agent:number;context:number;settings:number;agentVisible:boolean;contextVisible:boolean;contextSide:'left'|'right'};
```

Сохраняемые ширины, видимость панелей и сторона контекста Chat.

### `validated`

[Исходник](../../apps/desktop/src/StudioControls.tsx#L11)

```typescript
function validated(raw:Partial<Layout>): Layout
```

Проверяет finite размеры, ограничивает диапазонами и подставляет defaults.

### `readLayout`

[Исходник](../../apps/desktop/src/StudioControls.tsx#L12)

```typescript
function readLayout()
```

Безопасно читает сохранённую раскладку с возвратом defaults при повреждении.

### `StudioLayoutProvider`

[Исходник](../../apps/desktop/src/StudioControls.tsx#L14)

```typescript
function StudioLayoutProvider({children}:{children:ReactNode})
```

Публикует общую раскладку и текущую ширину viewport обоим режимам.

### `StudioLayoutProvider.resize`

[Исходник](../../apps/desktop/src/StudioControls.tsx#L16)

```typescript
resize()
```

Обновляет viewport после изменения настоящего окна.

### `StudioLayoutProvider.update`

[Исходник](../../apps/desktop/src/StudioControls.tsx#L17)

```typescript
update(value:Partial<Layout>)
```

Проверяет и сохраняет частичное изменение раскладки.

### `useStudioLayout`

[Исходник](../../apps/desktop/src/StudioControls.tsx#L20)

```typescript
function useStudioLayout()
```

Получает типизированную раскладку; требует provider.

### `ResizeRail`

[Исходник](../../apps/desktop/src/StudioControls.tsx#L21)

```typescript
function ResizeRail({name,edge='right'}:{name:Panel;edge?:'left'|'right'})
```

Меняет ширину pointer capture, стрелками, Home/End и двойным щелчком.

### `ResizeRail.change`

[Исходник](../../apps/desktop/src/StudioControls.tsx#L23)

```typescript
change(width:number)
```

Меняет поле черновика и помечает его несохранённым; новый URL сбрасывает устаревший список моделей.

### `LayoutPresets`

[Исходник](../../apps/desktop/src/StudioControls.tsx#L29)

```typescript
function LayoutPresets()
```

Сохраняет и восстанавливает именованные локальные раскладки, сбрасывает панели.

### `LayoutPresets.save`

[Исходник](../../apps/desktop/src/StudioControls.tsx#L31)

```typescript
function save()
```

Получает preview по исходной byte revision, не пишет файл и показывает отдельный диалог.

### `ComposerModel`

[Исходник](../../apps/desktop/src/StudioControls.tsx#L34)

```typescript
function ComposerModel({config,busy,onSelected,onSettings}:{config:ModelConfig;busy:boolean;onSelected:(id:string)=>void;onSettings:()=>void})
```

Получает список моделей от сервера, блокирует смену во время запуска и показывает ошибки.

### `ComposerModel.refresh`

[Исходник](../../apps/desktop/src/StudioControls.tsx#L38)

```typescript
async function refresh()
```

Обновляет только чистую вкладку после записи агента, dirty draft сохраняет и предупреждает о конфликте.

### `ComposerModel.select`

[Исходник](../../apps/desktop/src/StudioControls.tsx#L39)

```typescript
async function select(value:string)
```

Применяет ID через configureModel либо открывает настройки подключения.

### `InlineTools`

[Исходник](../../apps/desktop/src/StudioControls.tsx#L44)

```typescript
function InlineTools({task}:{task:TaskSnapshot|null})
```

Отображает реальные tool_activity и статусы в раскрываемых строках переписки.

### `DialogFocus`

[Исходник](../../apps/desktop/src/StudioControls.tsx#L49)

```typescript
function DialogFocus()
```

Удерживает Tab в верхнем видимом modal и возвращает предыдущий фокус.

### `DialogFocus.top`

[Исходник](../../apps/desktop/src/StudioControls.tsx#L50)

```typescript
top()
```

Находит последнее видимое aria-modal окно или открытый dialog.

### `DialogFocus.check`

[Исходник](../../apps/desktop/src/StudioControls.tsx#L52)

```typescript
check()
```

При изменении DOM переводит фокус внутрь нового modal или возвращает при закрытии.

### `DialogFocus.keys`

[Исходник](../../apps/desktop/src/StudioControls.tsx#L54)

```typescript
keys(e:KeyboardEvent)
```

Зацикливает Tab и Shift+Tab среди доступных контролов modal.

<a id="module-apps-desktop-src-studiofiletree-tsx"></a>

## `apps/desktop/src/StudioFileTree.tsx`

Ленивое настоящее дерево проекта с защитой от устаревших ответов после смены папки.

### `Item`

[Исходник](../../apps/desktop/src/StudioFileTree.tsx#L3)

```typescript
type Item={name:string;path:string;kind:'file'|'directory'};
```

Запись каталога IPC: имя, относительный путь и file/directory kind.

### `StudioFileTree`

[Исходник](../../apps/desktop/src/StudioFileTree.tsx#L4)

```typescript
function StudioFileTree({root,selected,refresh,onFile,onProject,onError}:{root:string;selected:string;refresh:unknown;onFile:(file:Item)=>void;onProject:()=>void;onError:(text:string)=>void})
```

Показывает настоящее дерево проекта, loading, пустые каталоги и ошибки.

### `StudioFileTree.load`

[Исходник](../../apps/desktop/src/StudioFileTree.tsx#L7)

```typescript
async function load(directory:string, epoch=generation.current)
```

Читает каталог через listFiles; игнорирует устаревший epoch и сменившийся root.

### `StudioFileTree.toggle`

[Исходник](../../apps/desktop/src/StudioFileTree.tsx#L10)

```typescript
function toggle(item:Item)
```

Раскрывает каталог и запрашивает ещё не загруженное содержимое.

### `StudioFileTree.branch`

[Исходник](../../apps/desktop/src/StudioFileTree.tsx#L11)

```typescript
function branch(directory:string, depth:number): React.ReactNode
```

Рекурсивно строит раскрытые каталоги и строки открытия настоящих файлов.

<a id="module-apps-desktop-src-subagentsettings-tsx"></a>

## `apps/desktop/src/SubagentSettings.tsx`

Настройки исследователей: профиль, инструкция, инструменты чтения, включение, удаление и общий переключатель.

### `Profile`

[Исходник](../../apps/desktop/src/SubagentSettings.tsx#L3)

```typescript
type Profile={id?:string;title:string;summary:string;instructions:string;tools:string[];enabled:boolean;source?:string;version?:number};
```

Ограниченный readonly профиль с происхождением и версией, без собственного подключения модели.

### `Catalog`

[Исходник](../../apps/desktop/src/SubagentSettings.tsx#L4)

```typescript
type Catalog={enabled:boolean;profiles:Profile[]};
```

Снимок общего переключателя и списка профилей.

### `SubagentSettings`

[Исходник](../../apps/desktop/src/SubagentSettings.tsx#L8)

```typescript
function SubagentSettings({catalog,busy,save,query=''}:{catalog:Catalog;busy:boolean;query?:string;save:(params:any)=>Promise<any>})
```

Редактор инструкции и readonly tools, явное включение/удаление и общий switch в прежнем оформлении.

### `SubagentSettings.persist`

[Исходник](../../apps/desktop/src/SubagentSettings.tsx#L10)

```typescript
async function persist()
```

Сохраняет trusted user draft через существующий IPC; закрывает редактор только при успехе.

<a id="module-apps-desktop-src-taskgraphpanel-tsx"></a>

## `apps/desktop/src/TaskGraphPanel.tsx`

Current task graph and trusted user editor with dependency/check selection; no direct effect execution.

### `TaskGraphPanel`

[Исходник](../../apps/desktop/src/TaskGraphPanel.tsx#L5)

```typescript
function TaskGraphPanel({task,busy,onTask}:{task:TaskSnapshot;busy:boolean;onTask?:(task:TaskSnapshot)=>void})
```

Показывает canonical DAG и редактор user-owned плана с dependencies/checks; рабочая задача редактируется только после idle.

### `TaskGraphPanel.patch`

[Исходник](../../apps/desktop/src/TaskGraphPanel.tsx#L8)

```typescript
function patch(id:string, values:Partial<PlanNode>)
```

Обновляет только локальный черновик одного узла до явного сохранения.

### `TaskGraphPanel.save`

[Исходник](../../apps/desktop/src/TaskGraphPanel.tsx#L9)

```typescript
async function save()
```

Передаёт whitelist полей выбранного плана trusted IPC и заменяет UI checkpoint только после успешной host validation.

<a id="module-apps-desktop-src-taskprogress-tsx"></a>

## `apps/desktop/src/TaskProgress.tsx`

Типизированная панель этапов, инструментов, результатов и продолжения задачи.

### `taskStatusLabel`

[Исходник](../../apps/desktop/src/TaskProgress.tsx#L19)

```typescript
function taskStatusLabel(task: TaskSnapshot)
```

Показывает lifecycle, ошибку и неподтверждённый исход отдельно от завершения модели.

### `TaskProgress`

[Исходник](../../apps/desktop/src/TaskProgress.tsx#L34)

```typescript
function TaskProgress({ task, busy, onResume, onResolveRecovery,onTask }: { task: TaskSnapshot; busy: boolean; onTask?:(task:TaskSnapshot)=>void; onResume: () => void; onResolveRecovery?: (item: TaskRecoveryItem, resolution: TaskRecoveryResolution) => void })
```

Показывает посещённые/пропущенные этапы, последние операции, изменённые файлы, остановку и кнопку resume.

<a id="module-apps-desktop-src-voicepanel-tsx"></a>

## `apps/desktop/src/VoicePanel.tsx`

Рабочий разговор с Лолой без file tools, системная озвучка, голос/темп/громкость/Stop и честный отключённый STT.

### `WorkspaceMode`

[Исходник](../../apps/desktop/src/VoicePanel.tsx#L13)

```typescript
export type WorkspaceMode = 'chat' | 'ide' | 'voice';
```

Три пространства интерфейса: обычный разговор, работа с проектом и будущий голосовой ассистент.

### `VoiceSessionState`

[Исходник](../../apps/desktop/src/VoicePanel.tsx#L15)

```typescript
export type VoiceSessionState = 'disconnected' | 'idle' | 'listening' | 'thinking' | 'speaking' | 'error';
```

Состояния голосовой оболочки: disconnected/idle/listening/thinking/speaking/error; listening зарезервирован до подключения STT.

### `VoicePanel`

[Исходник](../../apps/desktop/src/VoicePanel.tsx#L17)

```typescript
function VoicePanel({ headless=false, onDraft, desktopAction, attention, activation, onChat, onAsk, onCancel, onResume, onResolveRecovery, recoveryBusy, busy, messages, conversationKey, completed, task }: {
  headless?:boolean;onDraft?:(text:string)=>void;desktopAction:LolaVoiceAction|null;attention:string;
  activation:{id:number;text:string;send:boolean}|null;conversationKey:string;completed:boolean;
  onChat:()=>void;onAsk:(text:string)=>void;onCancel:()=>void;busy:boolean;
  messages:{role:string;text:string;streaming?:boolean}[];
  task?:TaskSnapshot|null;
  recoveryBusy:boolean;onResume:()=>void;
  onResolveRecovery:(item:TaskRecoveryItem,resolution:TaskRecoveryResolution)=>void;
})
```

Разговор с персонажем и реальный Windows TTS: каталог, voice/rate/volume, manual/opt-in auto speech и отдельный Stop.

### `VoicePanel.listener`

[Исходник](../../apps/desktop/src/VoicePanel.tsx#L47)

```typescript
listener(event:Event)
```

Адаптирует Electron event в пользовательские данные callback.

### `VoicePanel.changed`

[Исходник](../../apps/desktop/src/VoicePanel.tsx#L57)

```typescript
changed()
```

Перечитывает настройки голоса после изменения конфигурации в другом окне.

### `VoicePanel.selectProvider`

[Исходник](../../apps/desktop/src/VoicePanel.tsx#L58)

```typescript
async function selectProvider(provider:string)
```

Останавливает текущую озвучку, сохраняет выбранный движок профиля и обновляет каталог.

### `VoicePanel.startSerena`

[Исходник](../../apps/desktop/src/VoicePanel.tsx#L66)

```typescript
async function startSerena()
```

Запрашивает запуск/проверку управляемого Piper и выводит понятное состояние или ошибку.

### `VoicePanel.record`

[Исходник](../../apps/desktop/src/VoicePanel.tsx#L86)

```typescript
async function record()
```

Запускает явную запись микрофона или завершает текущую; ошибки и unmount освобождают tracks.

### `VoicePanel.finishRecording`

[Исходник](../../apps/desktop/src/VoicePanel.tsx#L92)

```typescript
async function finishRecording()
```

Отклоняет запись без речи, формирует обрезанный WAV, распознаёт и проверяет актуальность запроса; отправляет текст только при включённой настройке.

### `VoicePanel.cancelRecording`

[Исходник](../../apps/desktop/src/VoicePanel.tsx#L99)

```typescript
async function cancelRecording()
```

Инвалидирует результат STT, освобождает микрофон и отменяет HTTP; поздний ответ не меняет текст.

### `VoicePanel.saveVoice`

[Исходник](../../apps/desktop/src/VoicePanel.tsx#L102)

```typescript
async function saveVoice()
```

Сохраняет выбранный голос, темп, громкость и auto-speak в отдельном профиле.

### `VoicePanel.refresh`

[Исходник](../../apps/desktop/src/VoicePanel.tsx#L114)

```typescript
async function refresh()
```

Читает plain status раз в 500 мс; отбрасывает ответы после unmount. Инициализация discovery учитывает StrictMode cleanup.

### `VoicePanel.speak`

[Исходник](../../apps/desktop/src/VoicePanel.tsx#L146)

```typescript
async function speak(text:string)
```

Отправляет до 6000 символов с выбранным голосом/темпом/громкостью и показывает lifecycle/ошибку.

### `VoicePanel.stop`

[Исходник](../../apps/desktop/src/VoicePanel.tsx#L151)

```typescript
async function stop()
```

Останавливает только озвучку; не отменяет модельную генерацию.

### `VoicePanel.send`

[Исходник](../../apps/desktop/src/VoicePanel.tsx#L156)

```typescript
function send()
```

Передаёт введённую фразу в общий task flow voice без файловых инструментов.

<a id="module-apps-desktop-src-voicesettings-tsx"></a>

## `apps/desktop/src/VoiceSettings.tsx`

Общая страница голоса Лолы с громкостью, скоростью, автоматической озвучкой и расширенной конфигурацией.

### `VoiceSettings`

[Исходник](../../apps/desktop/src/VoiceSettings.tsx#L5)

```typescript
function VoiceSettings({busy}:{busy:boolean})
```

Общая настройка голоса/громкости/скорости Лолы и её расширенного профиля.

### `VoiceSettings.save`

[Исходник](../../apps/desktop/src/VoiceSettings.tsx#L8)

```typescript
async function save()
```

Получает preview по исходной byte revision, не пишет файл и показывает отдельный диалог.

### `VoiceSettings.preview`

[Исходник](../../apps/desktop/src/VoiceSettings.tsx#L9)

```typescript
async function preview()
```

Запрашивает пробную озвучку выбранным голосом и показывает результат сервиса.

<a id="module-apps-desktop-src-wakelistener-tsx"></a>

## `apps/desktop/src/WakeListener.tsx`

Явно включаемый микрофон во всех режимах: speech gate, STT, wake phrase, пауза при задаче/озвучке/ручной записи.

### `WakeListener`

[Исходник](../../apps/desktop/src/WakeListener.tsx#L5)

```typescript
function WakeListener({busy,onWake}:{busy:boolean;onWake:(text:string,send:boolean)=>Promise<void>})
```

Управляет явно включённым прослушиванием и паузами без обращения к чат-модели.

### `WakeListener.stop`

[Исходник](../../apps/desktop/src/WakeListener.tsx#L11)

```typescript
stop()
```

Отключает wake listening после команды Stop, пришедшей через спутника.

### `WakeListener.refresh`

[Исходник](../../apps/desktop/src/WakeListener.tsx#L16)

```typescript
refresh()
```

Обновляет профиль при сохранении настроек и не включает микрофон автоматически.

### `WakeListener.capture`

[Исходник](../../apps/desktop/src/WakeListener.tsx#L17)

```typescript
capture(event:Event)
```

Получает состояние ручной записи для исключения конкурентного STT.

### `WakeListener.cycle`

[Исходник](../../apps/desktop/src/WakeListener.tsx#L27)

```typescript
async function cycle()
```

Записывает фрагмент до тишины/12 секунд, распознаёт речь и активирует Лолу по началу фразы.

<a id="module-apps-desktop-src-welcome-tsx"></a>

## `apps/desktop/src/Welcome.tsx`

Пустое состояние Neutral с короткими сценариями и переходом в IDE.

### `Welcome`

[Исходник](../../apps/desktop/src/Welcome.tsx#L6)

```typescript
function Welcome({mode,onPrompt,onStart}:{mode:string;onPrompt:(text:string)=>void;onStart:()=>void})
```

Пустое состояние с брендом, примерами ввода и переходом в IDE.

<a id="module-apps-desktop-src-workspaceaccesssettings-tsx"></a>

## `apps/desktop/src/WorkspaceAccessSettings.tsx`

Форма точечных разрешений файлов для модели в возможностях IDE с явным подтверждением передачи содержимого.

### `WorkspaceAccessSettings`

[Исходник](../../apps/desktop/src/WorkspaceAccessSettings.tsx#L3)

```typescript
function WorkspaceAccessSettings({root,busy}:{root:string;busy:boolean})
```

Форма точечных исключений с уведомлением о передаче содержимого серверу модели.

### `WorkspaceAccessSettings.save`

[Исходник](../../apps/desktop/src/WorkspaceAccessSettings.tsx#L12)

```typescript
async function save()
```

Проверяет согласие, отправляет grants и игнорирует поздний ответ при смене проекта.

<a id="module-apps-desktop-src-workspacereview-tsx"></a>

## `apps/desktop/src/WorkspaceReview.tsx`

Список наборов правок, обратный diff, подтверждение отката и явное предупреждение конфликтов.

### `WorkspaceSnapshot`

[Исходник](../../apps/desktop/src/WorkspaceReview.tsx#L4)

```typescript
type WorkspaceSnapshot={git_checkpoint?:{commit:string;repository:string;ref:string}|null;id:string;status:string;paths:string[];operations:string[]};
```

Публичные status/path/operation метаданные набора; оригиналы файлов остаются в локальном хранилище.

### `RollbackPreview`

[Исходник](../../apps/desktop/src/WorkspaceReview.tsx#L5)

```typescript
type RollbackPreview={id:string;group_id:string;paths:string[];diff:string;truncated:boolean};
```

Ограниченный обратный diff и одноразовый ID подтверждения, без внутренних backup references.

### `WorkspaceReview`

[Исходник](../../apps/desktop/src/WorkspaceReview.tsx#L8)

```typescript
function WorkspaceReview({chatId,root,busy,dirty,revision,onTask,onRestored,onWorking}:{chatId:string;root:string;busy:boolean;dirty:boolean;revision:number;onTask:(task:TaskSnapshot)=>void;onRestored:()=>void;onWorking:(working:boolean)=>void})
```

Пользовательский список snapshots и diff/confirm workflow; блокирует действия при несохранённом editor draft.

### `WorkspaceReview.compareSnapshot`

[Исходник](../../apps/desktop/src/WorkspaceReview.tsx#L13)

```typescript
async function compareSnapshot(group_id:string)
```

Получает новое предложение отката после серверной проверки root/chat/revisions.

### `WorkspaceReview.saveCheckpoint`

[Исходник](../../apps/desktop/src/WorkspaceReview.tsx#L19)

```typescript
async function saveCheckpoint(group_id:string)
```

Сохраняет known snapshot в private Git через fixed async IPC; показывает repository/commit/ref и сохраняет текущий проект.

### `WorkspaceReview.applyRollback`

[Исходник](../../apps/desktop/src/WorkspaceReview.tsx#L24)

```typescript
async function applyRollback()
```

Подтверждает текущий одноразовый preview, показывает conflict/partial error и обновляет stale evidence.

### `WorkspaceReview.confirmManualReview`

[Исходник](../../apps/desktop/src/WorkspaceReview.tsx#L30)

```typescript
async function confirmManualReview(group_id:string)
```

Фиксирует явную проверку после partial rollback без повторения эффекта.

<a id="module-apps-desktop-src-design-forestspot-tsx"></a>

## `apps/desktop/src/design/ForestSpot.tsx`

Иллюстративные акценты LESHY из подготовленных прозрачных WebP.

### `ForestSpotKind`

[Исходник](../../apps/desktop/src/design/ForestSpot.tsx#L1)

```typescript
export type ForestSpotKind='birch'|'fern'|'mushrooms'|'archive';
```

Допустимые виды живописной иллюстрации LESHY.

### `ForestSpot`

[Исходник](../../apps/desktop/src/design/ForestSpot.tsx#L3)

```typescript
function ForestSpot({kind='fern',className=''}:{kind?:ForestSpotKind;className?:string})
```

Выбирает подготовленный ресурс и доступное представление иллюстрации.

<a id="module-apps-desktop-src-design-ornaments-tsx"></a>

## `apps/desktop/src/design/Ornaments.tsx`

Общие SVG-мотивы рамок, углов, разделителей и лесного акцента.

### `Diamond`

[Исходник](../../apps/desktop/src/design/Ornaments.tsx#L2)

```typescript
function Diamond()
```

Декоративный ромб через общий CSS mask.

### `OrnamentDiamond`

[Исходник](../../apps/desktop/src/design/Ornaments.tsx#L3)

```typescript
function OrnamentDiamond()
```

Общий компонент орнаментального ромба.

### `OrnamentDivider`

[Исходник](../../apps/desktop/src/design/Ornaments.tsx#L4)

```typescript
function OrnamentDivider()
```

Декоративный разделитель с ромбом.

### `OrnamentCorner`

[Исходник](../../apps/desktop/src/design/Ornaments.tsx#L5)

```typescript
function OrnamentCorner()
```

Угол рамки через общий SVG mask.

### `OrnamentLeaf`

[Исходник](../../apps/desktop/src/design/Ornaments.tsx#L6)

```typescript
function OrnamentLeaf()
```

Декоративная векторная ветка, скрытая от accessibility tree.

### `OrnamentFrame`

[Исходник](../../apps/desktop/src/design/Ornaments.tsx#L7)

```typescript
function OrnamentFrame()
```

Четыре декоративных угла рамки.

### `WoodlandAccent`

[Исходник](../../apps/desktop/src/design/Ornaments.tsx#L8)

```typescript
function WoodlandAccent({className=''}:{className?:string})
```

Лесной декоративный акцент с внешним классом размещения.

<a id="module-apps-desktop-src-design-themes-ts"></a>

## `apps/desktop/src/design/themes.ts`

Типы, нормализация и применение трёх тем LESHY.

### `LeshyTheme`

[Исходник](../../apps/desktop/src/design/themes.ts#L6)

```typescript
export type LeshyTheme = typeof leshyThemes[number]['id'];
```

Идентификатор одной из трёх тем LESHY.

### `normalizeTheme`

[Исходник](../../apps/desktop/src/design/themes.ts#L7)

```typescript
function normalizeTheme(value:unknown): LeshyTheme
```

Преобразует legacy light и неизвестные значения в поддерживаемую тему.

### `applyTheme`

[Исходник](../../apps/desktop/src/design/themes.ts#L10)

```typescript
function applyTheme(theme:LeshyTheme, art=true)
```

Применяет data attributes и color-scheme темы к документу.

<a id="module-apps-desktop-src-ideentry-ts"></a>

## `apps/desktop/src/ideEntry.ts`

Адаптер API Code-OSS webview к общему window.lca.

### `acquireVsCodeApi`

[Исходник](../../apps/desktop/src/ideEntry.ts#L4)

```typescript
function acquireVsCodeApi(): {postMessage:(message:unknown)=>void;getState:()=>unknown;setState:(state:unknown)=>void}
```

Объявление предоставленного Code-OSS API webview.

### `invoke`

[Исходник](../../apps/desktop/src/ideEntry.ts#L11)

```typescript
invoke(channel, ...args)
```

Отправляет RPC webview с идентичностью запроса.

### `on`

[Исходник](../../apps/desktop/src/ideEntry.ts#L12)

```typescript
on(_channel, listener)
```

Подключает слушателя событий IDE транспорта.

### `removeListener`

[Исходник](../../apps/desktop/src/ideEntry.ts#L12)

```typescript
removeListener(_channel, listener)
```

Удаляет слушателя событий IDE транспорта.

<a id="module-apps-desktop-src-idepanel-acceptancechecks-ts"></a>

## `apps/desktop/src/idePanel/acceptanceChecks.ts`

Подготовка существующих IdeOptions, изоляция draft по chat_id и readonly/resume guard без нового executor.

### `AcceptanceDraft`

[Исходник](../../apps/desktop/src/idePanel/acceptanceChecks.ts#L4)

```typescript
export type AcceptanceDraft={chatId:string;options:IdeOptions};
```

Локальный editable draft с точным chat_id, не canonical evidence.

### `canResumeInMode`

[Исходник](../../apps/desktop/src/idePanel/acceptanceChecks.ts#L5)

```typescript
function canResumeInMode(saved:{read_only?:boolean}|undefined, mode:string): boolean
```

Не позволяет Ask/Plan возобновить сохранённую Agent-задачу с правом выполнения команд.

### `emptyAcceptanceOptions`

[Исходник](../../apps/desktop/src/idePanel/acceptanceChecks.ts#L6)

```typescript
function emptyAcceptanceOptions(): IdeOptions
```

Создаёт независимый пустой набор options без общих mutable arrays.

### `copyOptions`

[Исходник](../../apps/desktop/src/idePanel/acceptanceChecks.ts#L7)

```typescript
function copyOptions(value:IdeOptions): IdeOptions
```

Копирует массивы критериев, links, argv и scope/dependencies перед редактированием.

### `isDraft`

[Исходник](../../apps/desktop/src/idePanel/acceptanceChecks.ts#L10)

```typescript
function isDraft(value:unknown): value is IdeOptions
```

Проверяет форму восстановленного view draft, допуская незавершённый ввод и отклоняя повреждённые структуры.

### `isDraft.strings`

[Исходник](../../apps/desktop/src/idePanel/acceptanceChecks.ts#L12)

```typescript
strings(a:unknown): a is string[]
```

Проверяет массив строк локального draft.

### `acceptanceDraftForChat`

[Исходник](../../apps/desktop/src/idePanel/acceptanceChecks.ts#L15)

```typescript
function acceptanceDraftForChat(chatId:string, checkpoint:unknown, saved?:AcceptanceDraft): IdeOptions
```

Восстанавливает только draft выбранного чата либо копию его canonical checkpoint options.

### `removeAcceptanceCheck`

[Исходник](../../apps/desktop/src/idePanel/acceptanceChecks.ts#L19)

```typescript
function removeAcceptanceCheck(value:IdeOptions, id:string): IdeOptions
```

Удаляет check definition и его связи с критериями, не мутируя исходный draft.

### `paths`

[Исходник](../../apps/desktop/src/idePanel/acceptanceChecks.ts#L22)

```typescript
function paths(values:string[]): string[]
```

Нормализует явные relative file/dependency paths для существующего Core evidence scope.

### `prepareAcceptanceOptions`

[Исходник](../../apps/desktop/src/idePanel/acceptanceChecks.ts#L27)

```typescript
function prepareAcceptanceOptions(value:IdeOptions, mode:string, checksOnly=false): StartTaskOptions
```

Сохраняет argv/check_id/scope, нормализует критерии и links, исключает команды в Ask/Plan и валидирует checks_only.

<a id="module-apps-desktop-src-idepanel-acceptancesettings-tsx"></a>

## `apps/desktop/src/idePanel/acceptanceSettings.tsx`

Независимый editor критериев, команд, scopes и ручного запуска checks_only в новой IDE.

### `AcceptanceSettings`

[Исходник](../../apps/desktop/src/idePanel/acceptanceSettings.tsx#L5)

```typescript
function AcceptanceSettings({value,mode,busy,connected,onChange,onRun,onBack}:{value:IdeOptions;mode:string;busy:boolean;connected:boolean;onChange:(value:IdeOptions)=>void;onRun:()=>void;onBack:()=>void})
```

Редактор пользовательских критериев, команд, LSP/scopes и запуска проверок без модели.

### `AcceptanceSettings.updateCheck`

[Исходник](../../apps/desktop/src/idePanel/acceptanceSettings.tsx#L6)

```typescript
function updateCheck(id:string, patch:Partial<ValidationCommand>)
```

Обновляет выбранный check с сохранением его stable id.

<a id="module-apps-desktop-src-idepanel-connectionsettings-tsx"></a>

## `apps/desktop/src/idePanel/connectionSettings.tsx`

Самостоятельная форма подключения и оформления; редактируемые настройки отделены от сохранённых.

### `ConnectionSettings`

[Исходник](../../apps/desktop/src/idePanel/connectionSettings.tsx#L7)

```typescript
function ConnectionSettings({config,savedConfig,models,locked,onChange,onSave,onList}:{config:ModelConnection|null;savedConfig:ModelConnection|null;models:string[];locked:boolean;onChange:(value:ModelConnection)=>void;onSave:()=>void;onList:()=>void})
```

Отображает независимую форму подключения, preview тем и подсказку о плане, правилах и MCP.

<a id="module-apps-desktop-src-idepanel-entry-tsx"></a>

## `apps/desktop/src/idePanel/entry.tsx`

Монтирует независимый AgentWorkspace и его стили.

Нет именованных функций/типов: модуль выполняет конфигурацию, сборочный вызов или render entry. Анонимные callbacks описаны в учебных главах.

<a id="module-apps-desktop-src-idepanel-recoverydiagnostics-ts"></a>

## `apps/desktop/src/idePanel/recoveryDiagnostics.ts`

Общий recovery gate и минимальная диагностика по allowlist без текста, путей и ключей.

### `RecoveryState`

[Исходник](../../apps/desktop/src/idePanel/recoveryDiagnostics.ts#L3)

```typescript
type RecoveryState=Pick<TaskSnapshot,'recovery_error'|'recovery_items'|'snapshot_attention'>;
```

Минимальные поля задачи, влияющие на блокировку восстановления.

### `hasRecoveryBlockers`

[Исходник](../../apps/desktop/src/idePanel/recoveryDiagnostics.ts#L4)

```typescript
function hasRecoveryBlockers(task:RecoveryState|null|undefined): boolean
```

Запрещает resume при неизвестном действии, нечитаемом журнале или неподтверждённом rollback.

### `safeId`

[Исходник](../../apps/desktop/src/idePanel/recoveryDiagnostics.ts#L7)

```typescript
function safeId(value:unknown): string|undefined
```

Пропускает только ограниченный hex-идентификатор; произвольный текст в диагностику не попадает.

### `count`

[Исходник](../../apps/desktop/src/idePanel/recoveryDiagnostics.ts#L10)

```typescript
function count(value:unknown): number
```

Принимает только неотрицательный целочисленный счётчик.

### `recoveryDiagnostics`

[Исходник](../../apps/desktop/src/idePanel/recoveryDiagnostics.ts#L13)

```typescript
function recoveryDiagnostics(task:TaskSnapshot|null)
```

Строит bounded JSON с идентичностями, счётчиками и recovery flags, без error narrative и исходников.

<a id="module-apps-desktop-src-idepanel-runactivity-tsx"></a>

## `apps/desktop/src/idePanel/runActivity.tsx`

Карточки этапов, инструментов, проверок и разрешения неизвестных эффектов.

### `RunActivity`

[Исходник](../../apps/desktop/src/idePanel/runActivity.tsx#L6)

```typescript
function RunActivity({task,busy,events,onResume,onOpen,onResolve,onCopy,onConfigureChecks}:{task:TaskSnapshot|null;busy:boolean;events:string[];onResume:()=>void;onOpen:(path:string)=>void;onResolve:(item:TaskRecoveryItem,resolution:TaskRecoveryResolution)=>Promise<void>;onCopy:()=>Promise<void>;onConfigureChecks:()=>void})
```

Показывает фактические этапы, инструменты, проверки и ручное разрешение unknown effects.

### `RunActivity.copyDiagnostics`

[Исходник](../../apps/desktop/src/idePanel/runActivity.tsx#L11)

```typescript
async function copyDiagnostics()
```

Показывает pending/result копирования безопасной диагностики.

### `RunActivity.confirmObservation`

[Исходник](../../apps/desktop/src/idePanel/runActivity.tsx#L12)

```typescript
async function confirmObservation()
```

Ожидает подтверждение Core; ошибка сохраняет проверяемое решение на экране.

<a id="module-apps-desktop-src-idepanel-sessionstate-ts"></a>

## `apps/desktop/src/idePanel/sessionState.ts`

Типы состояния новой панели и чистое преобразование событий с chat/run/sequence isolation.

### `Line`

[Исходник](../../apps/desktop/src/idePanel/sessionState.ts#L5)

```typescript
export type Line={role:string;text:string;id?:string};
```

Строка локальной переписки с ролью, текстом и optional message id.

### `Reference`

[Исходник](../../apps/desktop/src/idePanel/sessionState.ts#L6)

```typescript
export type Reference={path:string;start:number;end:number};
```

Ссылка на сохранённый диапазон файла редактора.

### `SessionIdentity`

[Исходник](../../apps/desktop/src/idePanel/sessionState.ts#L7)

```typescript
export type SessionIdentity={chat:string;run:string;seq:number};
```

Точный chat/run и последняя принятая последовательность события.

### `PanelApproval`

[Исходник](../../apps/desktop/src/idePanel/sessionState.ts#L8)

```typescript
export type PanelApproval=Extract<TaskLifecycleEvent,{event:'approval'}>;
```

Существующий approval payload из общего протокола.

### `ModelConnection`

[Исходник](../../apps/desktop/src/idePanel/sessionState.ts#L9)

```typescript
export type ModelConnection={ok:boolean;base_url:string;model:string;api_key?:string;api_protocol:'chat'|'responses';tool_protocol:'native'|'json';settings:GenerationSettings};
```

Тип сохранённого или редактируемого подключения панели.

### `ChatSummary`

[Исходник](../../apps/desktop/src/idePanel/sessionState.ts#L10)

```typescript
export type ChatSummary={id:string;title:string};
```

Тип метаданных чата для бокового списка.

### `ChatSelection`

[Исходник](../../apps/desktop/src/idePanel/sessionState.ts#L11)

```typescript
export type ChatSelection={ok:boolean;error?:string;chat:ChatSummary&{messages?:{role:string;content:unknown;message_id?:string}[]};task?:TaskSnapshot;approval?:PanelApproval;active_run?:{run_id:string};event_seq?:number};
```

Результат выбора чата с checkpoint, approval и active run.

### `SessionUpdate`

[Исходник](../../apps/desktop/src/idePanel/sessionState.ts#L12)

```typescript
export type SessionUpdate={identity:SessionIdentity;messages?:Line[];task?:TaskSnapshot;approval?:PanelApproval|null;fileEvent?:string;error?:string;ended?:boolean};
```

Изменяемые проекции одного принятого события панели.

### `projectTaskEvent`

[Исходник](../../apps/desktop/src/idePanel/sessionState.ts#L14)

```typescript
function projectTaskEvent(identity:SessionIdentity, lines:Line[], event:TaskLifecycleEvent): SessionUpdate|null
```

Отклоняет чужие/старые/невалидные события, обновляет текст и lifecycle без побочных эффектов.

<a id="module-apps-desktop-src-idepanel-workspace-tsx"></a>

## `apps/desktop/src/idePanel/workspace.tsx`

Независимая панель диалога, истории, подключений и действий агента.

### `Page`

[Исходник](../../apps/desktop/src/idePanel/workspace.tsx#L17)

```typescript
type Page='conversation'|'history'|'activity'|'settings'|'checks';
```

Допустимая страница независимой IDE-панели.

### `api`

[Исходник](../../apps/desktop/src/idePanel/workspace.tsx#L18)

```typescript
api()
```

Возвращает предоставленный транспортом window.lca.

### `checked`

[Исходник](../../apps/desktop/src/idePanel/workspace.tsx#L19)

```typescript
function checked(result:T): T
```

Преобразует failed RPC result в видимую ошибку операции.

### `Content`

[Исходник](../../apps/desktop/src/idePanel/workspace.tsx#L20)

```typescript
function Content({text}:{text:string})
```

Отображает текст и блоки кода сообщения в новой панели.

### `AgentWorkspace`

[Исходник](../../apps/desktop/src/idePanel/workspace.tsx#L22)

```typescript
function AgentWorkspace()
```

Независимое состояние диалога, истории, настроек и approvals IDE.

### `AgentWorkspace.setMessages`

[Исходник](../../apps/desktop/src/idePanel/workspace.tsx#L35)

```typescript
function setMessages(next:Line[]|((current:Line[])=>Line[]))
```

Синхронно обновляет transcript ref и React state, сохраняя соседние delta до следующего render.

### `AgentWorkspace.changeChecks`

[Исходник](../../apps/desktop/src/idePanel/workspace.tsx#L36)

```typescript
function changeChecks(value:IdeOptions)
```

Сохраняет draft только для текущего чата и синхронный ref для отправки.

### `AgentWorkspace.act`

[Исходник](../../apps/desktop/src/idePanel/workspace.tsx#L37)

```typescript
async function act(work:()=>Promise<void>, propagate=false)
```

Сериализует UI-операцию и показывает её ошибку и busy state.

### `AgentWorkspace.refresh`

[Исходник](../../apps/desktop/src/idePanel/workspace.tsx#L38)

```typescript
async function refresh()
```

Обновляет только чистую вкладку после записи агента, dirty draft сохраняет и предупреждает о конфликте.

### `AgentWorkspace.select`

[Исходник](../../apps/desktop/src/idePanel/workspace.tsx#L39)

```typescript
async function select(id?:string)
```

Загружает выбранный чат либо создаёт новый с восстановлением текущего run.

### `AgentWorkspace.takeEdit`

[Исходник](../../apps/desktop/src/idePanel/workspace.tsx#L46)

```typescript
async function takeEdit()
```

Забирает editor draft, добавляет ссылку на контекст и фокусирует ввод.

### `AgentWorkspace.trap`

[Исходник](../../apps/desktop/src/idePanel/workspace.tsx#L64)

```typescript
trap(event:KeyboardEvent)
```

Удерживает Tab-фокус внутри активного approval.

### `AgentWorkspace.escape`

[Исходник](../../apps/desktop/src/idePanel/workspace.tsx#L68)

```typescript
escape(event:KeyboardEvent)
```

Возвращает к диалогу по Escape вне approval.

### `AgentWorkspace.send`

[Исходник](../../apps/desktop/src/idePanel/workspace.tsx#L69)

```typescript
async function send(resume=false, checksOnly=false)
```

Проверяет recovery/busy, назначает run id до startTask и отправляет выбранный Agent/Ask/Plan запрос.

### `AgentWorkspace.decide`

[Исходник](../../apps/desktop/src/idePanel/workspace.tsx#L83)

```typescript
async function decide(decision:'apply'|'reject'|'cancel')
```

Передаёт явное решение по текущему approval агента, защищая от повторных кликов.

### `AgentWorkspace.attach`

[Исходник](../../apps/desktop/src/idePanel/workspace.tsx#L84)

```typescript
async function attach()
```

Добавляет один диапазон редактора на путь, ограничивая список восьмью ссылками.

<a id="module-apps-desktop-src-lola-main-tsx"></a>

## `apps/desktop/src/lola-main.tsx`

Создаёт React root отдельного спутника и загружает только companion stylesheet.

Нет именованных функций/типов: модуль выполняет конфигурацию, сборочный вызов или render entry. Анонимные callbacks описаны в учебных главах.

<a id="module-apps-desktop-src-main-tsx"></a>

## `apps/desktop/src/main.tsx`

Подключает CSS, создаёт React root и отображает App в StrictMode.

Нет именованных функций/типов: модуль выполняет конфигурацию, сборочный вызов или render entry. Анонимные callbacks описаны в учебных главах.

<a id="module-apps-desktop-src-microphone-ts"></a>

## `apps/desktop/src/microphone.ts`

16 kHz mono PCM16 WAV: подавление шума, блоки 64 мс, завершение по паузе, обрезка тишины и освобождение микрофона.

### `this.processor.onaudioprocess`

[Исходник](../../apps/desktop/src/microphone.ts#L23)

```typescript
this.processor.onaudioprocess(event)
```

Копирует mono float samples до 960000 frames, затем автоматически завершает запись по лимиту 60 секунд.

### `ascii`

[Исходник](../../apps/desktop/src/microphone.ts#L41)

```typescript
ascii(offset:number, text:string)
```

Записывает фиксированные RIFF/WAVE/fmt/data метки в WAV DataView.

<a id="module-apps-desktop-src-uselolasession-tsx"></a>

## `apps/desktop/src/useLolaSession.tsx`

Независимая голосовая сессия popup Лолы: загрузка, live events, отправка, остановка, approval и recovery.

### `useLolaSession`

[Исходник](../../apps/desktop/src/useLolaSession.tsx#L9)

```typescript
function useLolaSession()
```

Владеет голосовой перепиской popup и headless контроллером записи/воспроизведения.

### `useLolaSession.select`

[Исходник](../../apps/desktop/src/useLolaSession.tsx#L15)

```typescript
async function select(id?:string)
```

Загружает voice chat, snapshot и approval с буферизацией событий во время загрузки.

### `useLolaSession.send`

[Исходник](../../apps/desktop/src/useLolaSession.tsx#L21)

```typescript
async function send(text:string, resume=false)
```

Запускает реальную voice задачу после готовности сессии и проверки recovery.

### `useLolaSession.stop`

[Исходник](../../apps/desktop/src/useLolaSession.tsx#L26)

```typescript
async function stop()
```

Останавливает запись/озвучку и только собственный текущий run.

### `useLolaSession.decide`

[Исходник](../../apps/desktop/src/useLolaSession.tsx#L27)

```typescript
async function decide(value:ApprovalDecision)
```

Передаёт явное решение по текущему approval агента, защищая от повторных кликов.

### `useLolaSession.resolve`

[Исходник](../../apps/desktop/src/useLolaSession.tsx#L28)

```typescript
async function resolve(item:TaskRecoveryItem, resolution:TaskRecoveryResolution)
```

Применяет пользовательское решение по прерванному tool journal и обновляет snapshot.

### `useLolaSession.receive.current`

[Исходник](../../apps/desktop/src/useLolaSession.tsx#L29)

```typescript
receive.current(event)
```

Маршрутизирует команды popup и scoped live events с cursor/run фильтрами.

### `useLolaSession.clearDraft`

[Исходник](../../apps/desktop/src/useLolaSession.tsx#L48)

```typescript
clearDraft()
```

Очищает переданный из STT черновик после переноса в поле popup.

### `useLolaSession.resume`

[Исходник](../../apps/desktop/src/useLolaSession.tsx#L48)

```typescript
resume()
```

Продолжает собственную голосовую задачу через тот же send с resume flag.

<a id="module-apps-desktop-src-usetasksession-ts"></a>

## `apps/desktop/src/useTaskSession.ts`

Состояние разговора и жизненного цикла UI; отбрасывание поздних/чужих событий и редукция stream/task_end.

### `SessionMessage`

[Исходник](../../apps/desktop/src/useTaskSession.ts#L5)

```typescript
export type SessionMessage={role:string;text:string;id?:string;streaming?:boolean};
```

Публичное сообщение UI с устойчивым stream ID и признаком незавершённого текста.

### `useTaskSession`

[Исходник](../../apps/desktop/src/useTaskSession.ts#L7)

```typescript
function useTaskSession()
```

Владелец сообщений/задачи/busy/run refs; run_id задаётся до стартового IPC.

### `useTaskSession.accepts`

[Исходник](../../apps/desktop/src/useTaskSession.ts#L11)

```typescript
function accepts(event:unknown): event is TaskLifecycleEvent
```

Не принимает чужую область, старый run или события после task_end; ранний start bind не зависит от порядка ответа IPC.

### `useTaskSession.reduce`

[Исходник](../../apps/desktop/src/useTaskSession.ts#L18)

```typescript
function reduce(event:TaskLifecycleEvent)
```

Применяет только проверенные lifecycle events и завершает streaming при task_end.

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
interface Window { neutralIdeHost?:boolean;neutralIdeDraft?:string;neutralIdeCheckDraft?:import('./idePanel/acceptanceChecks').AcceptanceDraft; lca: {
  copyTaskDiagnostics:(report:string)=>Promise<import('../shared/protocol').RpcResult>;
  getAppearanceTheme:(fallback?:string)=>Promise<{ok:boolean;theme?:string;error?:string}>;
  setAppearanceTheme:(theme:string)=>Promise<{ok:boolean;theme?:string;error?:string}>;
  ideEditDraft:()=>Promise<any>;
  ideEditorContext:()=>Promise<{ok:boolean;error?:string;path?:string;start?:number;end?:number}>;
  ideShell:()=>Promise<any>;
  idePreviewDiff:(path:string)=>Promise<any>;
  ideOpenFile:(path:string,line?:number)=>Promise<any>;
  openNeutralIde:()=>Promise<import('../shared/protocol').RpcResult<{pid:number;prototype:boolean}>>;
  workspaceAccess:()=>Promise<import('../shared/protocol').RpcResult<{root:string;exceptions:string[];ignore_patterns:string[]}>>;
  configureWorkspaceAccess:(paths:string[],confirmed:boolean)=>ReturnType<Window['lca']['workspaceAccess']>;
  cancelStorageBackup:()=>Promise<import('../shared/protocol').RpcResult>;
  getDesktopLola:()=>Promise<import('../shared/protocol').RpcResult<{settings:import('../shared/lolaDesktop').LolaDesktopSettings;frame:import('../shared/lolaDesktop').LolaDesktopFrame;visible:boolean}>>;
  openLola:(chatId?:string,action?:import('../shared/lolaDesktop').LolaDesktopAction)=>ReturnType<Window['lca']['getDesktopLola']>;
  lolaMicrophone:(active:boolean)=>Promise<import('../shared/protocol').RpcResult>;
  configureDesktopLola:(settings:import('../shared/lolaDesktop').LolaDesktopSettings)=>ReturnType<Window['lca']['getDesktopLola']>;
  presentDesktopLola:(frame:import('../shared/lolaDesktop').LolaDesktopFrame)=>Promise<import('../shared/protocol').RpcResult>;

  optionalSettings:()=>Promise<import('../shared/optionalTypes').OptionalCatalog>;
  configureOptionalIde:(settings:import('../shared/optionalTypes').OptionalSettings)=>Promise<import('../shared/optionalTypes').OptionalCatalog>;
  runOptionalIde:(params:import('../shared/optionalTypes').OptionalRequest)=>Promise<import('../shared/optionalTypes').OptionalResult>;
  cancelOptionalIde:()=>Promise<import('../shared/protocol').RpcResult>;
  openManagedWorktree:(id:string)=>Promise<import('../shared/protocol').RpcResult<{root:string;name:string}>>;
  listWorkspaces:()=>Promise<any>;
  saveWorkspace:(params:unknown)=>Promise<any>;
  selectWorkspace:(params:unknown)=>Promise<any>;
  deleteWorkspace:(params:unknown)=>Promise<any>;
  searchChats:(params:unknown)=>Promise<any>;
  updateChat:(params:unknown)=>Promise<any>;
  deleteChat:(params:unknown)=>Promise<any>;
  forkChat:(params:unknown)=>Promise<any>;
  storageStatus:()=>Promise<any>;
  backupStorage:()=>Promise<any>;
  exportChat:(params:unknown)=>Promise<any>;
  listExtensions:()=>Promise<any>;
  configureExtensions:(params:unknown)=>Promise<any>;
  discoverMcp:(params:unknown)=>Promise<any>;
  cancelMcpDiscovery:(params:unknown)=>Promise<any>;
  listConnections:()=>Promise<any>;
  saveConnection:(params:unknown)=>Promise<any>;
  deleteConnection:(params:unknown)=>Promise<any>;
  importPlugin:()=>Promise<any>;
  pickWorkspaceFolder:()=>Promise<any>;

  health: () => Promise<any>; chooseProject: () => Promise<any>;
  listFiles: (path?: string) => Promise<any>; readFile: (path: string) => Promise<any>; systemInfo: () => Promise<any>;
  pickRuntimeFile: (kind:string) => Promise<any>; startRuntime: (params:unknown) => Promise<any>; runtimeStatus: () => Promise<any>; stopRuntime: () => Promise<any>;
  getProjectMemory: () => Promise<any>; saveProjectMemory: (memory:unknown,revision:string,root?:string) => Promise<any>; projectMemoryAction: (params:unknown) => Promise<any>; renameChat: (id:string,title:string,mode:string) => Promise<any>;
  telegramStatus:()=>Promise<any>;connectTelegram:(params:unknown)=>Promise<any>;disconnectTelegram:()=>Promise<any>;forgetTelegram:()=>Promise<any>;
  desktopSettings:()=>Promise<any>;configureDesktop:(enabled:boolean)=>Promise<any>;
  desktopApplications:()=>Promise<any>;addDesktopApplication:()=>Promise<any>;removeDesktopApplication:(id:string)=>Promise<any>;
  moveChat:(id:string,mode:string,target:string)=>Promise<any>;
  cancelHandoff:(id:string)=>Promise<any>;
  prepareHandoff:(id:string)=>Promise<any>;
  getCompanionSettings:()=>Promise<any>;configureCompanion:(params:unknown)=>Promise<any>;
  transcribe:(audio:string)=>Promise<any>;cancelTranscription:()=>Promise<any>;
  voicePlayback:(params:unknown)=>Promise<any>;openTtsFolder:()=>Promise<any>;
  speechRuntime:(operation:'status'|'start'|'stop'|'install')=>Promise<any>;
  activateAssistant:()=>Promise<any>;wakeListening:(enabled:boolean)=>Promise<any>;
  voiceStatus: () => Promise<any>; refreshVoices: () => Promise<any>; speak: (params:unknown) => Promise<any>; stopVoice: () => Promise<any>;
  searchProject: (params: unknown) => Promise<any>; cancelProjectSearch: () => Promise<any>;
  projectIndex: (params: unknown) => Promise<any>;
  editorRead: (path: string) => Promise<any>; editorPreview: (path: string, content: string, revision: unknown) => Promise<any>;
  editorResolve: (proposalId: string, decision: string) => Promise<any>; setEditorDirty: (dirty: boolean) => Promise<any>;
  confirmEditorDiscard: () => Promise<{discard: boolean}>;
  configureModel: (config: {base_url: string; model: string; api_key?: string; api_protocol?:string; tool_protocol?: string; settings?: import('./GenerationFields').GenerationSettings}) => Promise<any>;
  listModels: (config?: unknown) => Promise<any>; listChats: (mode?: string) => Promise<any>; newChat: (mode?: string) => Promise<any>; loadChat: (id: string, mode?: string) => Promise<any>;
  testModel: (config: unknown) => Promise<any>; cancelModelSetup: () => Promise<any>;
  getModelSettings: () => Promise<any>;
  createGitCheckpoint:(params:unknown)=>Promise<any>; cancelGitCheckpoint:()=>Promise<any>;
  listSnapshots:(params:import('../shared/protocol').SnapshotScope)=>Promise<import('../shared/protocol').SnapshotListResult>;previewRollback:(params:import('../shared/protocol').SnapshotScope&{group_id:string})=>Promise<import('../shared/protocol').RpcResult<{proposal:import('../shared/protocol').SnapshotPreview}>>;applyRollback:(params:import('../shared/protocol').SnapshotScope&{proposal_id:string;confirmed:true})=>Promise<import('../shared/protocol').SnapshotApplyResult>;reviewRollback:(params:import('../shared/protocol').SnapshotScope&{group_id:string;confirmed:true})=>Promise<import('../shared/protocol').SnapshotListResult>;
  startTask: (prompt: string, resume?: boolean, mode?: import('../shared/protocol').AgentMode,options?:import('../shared/protocol').StartTaskOptions,runId?:string) => Promise<import('../shared/protocol').StartTaskResult>; cancelTask: (runId?:string) => Promise<any>;
  updateTaskPlan:(params:unknown)=>Promise<any>;
  activeRuns:()=>Promise<any>;
  resolveApproval: (run: string, approval: string, decision: import('../shared/protocol').ApprovalDecision) => Promise<import('../shared/protocol').RpcResult>;
  runHistory:(chatId:string)=>Promise<import('../shared/protocol').RpcResult<{runs:import('../shared/contextTypes').RunSnapshot[]}>>;
  resolveToolRecovery: (params: {chat_id:string; journal_id:string; message_index:number; call_id:string; resolution:'completed'|'not_executed'}) => Promise<any>;
  onEvent: (callback: (event: CoreEvent) => void) => () => void;
} }
```

Расширение глобального Window контрактом фиксированного lca API.

### `Window`

[Исходник](../../apps/desktop/src/vite-env.d.ts#L84)

```typescript
interface Window {lola:{
 status:()=>ReturnType<Window['lca']['getDesktopLola']>;
 ready:()=>Promise<import('../shared/protocol').RpcResult>;
 action:(action:import('../shared/lolaDesktop').LolaDesktopAction)=>Promise<import('../shared/protocol').RpcResult>;
 showMain:()=>Promise<import('../shared/protocol').RpcResult>;menu:()=>Promise<import('../shared/protocol').RpcResult>;hover:(value:boolean)=>Promise<import('../shared/protocol').RpcResult>;move:(x:number,y:number)=>Promise<import('../shared/protocol').RpcResult>;
 onState:(callback:(value:{settings:import('../shared/lolaDesktop').LolaDesktopSettings;frame:import('../shared/lolaDesktop').LolaDesktopFrame})=>void)=>()=>void;
}}
```

Расширение глобального Window контрактом фиксированного lca API.

<a id="module-apps-desktop-src-voicetext-ts"></a>

## `apps/desktop/src/voiceText.ts`

Очистка презентационной разметки потокового ответа Лолы перед показом и озвучкой.

### `plainVoiceText`

[Исходник](../../apps/desktop/src/voiceText.ts#L2)

```typescript
function plainVoiceText(text:string)
```

Удаляет разметку из потокового отображения и текста для TTS без исполнения HTML.

<a id="module-apps-desktop-src-wakephrase-ts"></a>

## `apps/desktop/src/wakePhrase.ts`

Нормализация русской фразы и выделение команды только после совпадающего начала без потери пунктуации команды.

### `normalizeSpeech`

[Исходник](../../apps/desktop/src/wakePhrase.ts#L1)

```typescript
function normalizeSpeech(text:string)
```

Приводит русскую фразу к нижнему регистру, ё→е и пробелам между словами.

### `wakeCommand`

[Исходник](../../apps/desktop/src/wakePhrase.ts#L5)

```typescript
function wakeCommand(text:string, phrase:string): string|null
```

Проверяет фразу только в начале; возвращает исходный хвост с пунктуацией либо null.

<a id="module-apps-desktop-vite-config-ts"></a>

## `apps/desktop/vite.config.ts`

React-плагин, относительные assets, фиксированный локальный dev-порт и outDir.

Нет именованных функций/типов: модуль выполняет конфигурацию, сборочный вызов или render entry. Анонимные callbacks описаны в учебных главах.

<a id="module-tests-electron-assistant-media-cjs"></a>

## `tests/electron/assistant-media.cjs`

Host-проверки музыкальных ссылок и путей аудио, включая junction, без воспроизведения и браузера.

Нет именованных функций/типов: модуль выполняет конфигурацию, сборочный вызов или render entry. Анонимные callbacks описаны в учебных главах.

<a id="module-tests-electron-background-runs-smoke-cjs"></a>

## `tests/electron/background-runs-smoke.cjs`

Real renderer/Core test of switching active chats, queued Stop and a delta arriving between snapshot and IPC response.

### `BrowserWindow.prototype.show`

[Исходник](../../tests/electron/background-runs-smoke.cjs#L10)

```typescript
BrowserWindow.prototype.show()
```

Скрывает только тестовое окно, сохраняя настоящий Electron renderer.

### `BrowserWindow.prototype.loadURL`

[Исходник](../../tests/electron/background-runs-smoke.cjs#L11)

```typescript
BrowserWindow.prototype.loadURL()
```

Открывает собранный renderer вместо пользовательского dev сервера.

### `ipcMain.handle`

[Исходник](../../tests/electron/background-runs-smoke.cjs#L14)

```typescript
ipcMain.handle(channel, handler)
```

Задерживает только тестовый chat load после backend snapshot и добавляет реальную SSE delta для проверки гонки IPC.

### `done`

[Исходник](../../tests/electron/background-runs-smoke.cjs#L23)

```typescript
done()
```

Завершает ровно один удерживаемый SSE response после проверки изоляции.

### `appendAlpha`

[Исходник](../../tests/electron/background-runs-smoke.cjs#L24)

```typescript
appendAlpha()
```

Добавляет новый реальный SSE фрагмент между snapshot и поздним IPC response, проверяя отсутствие потерь и дублей.

### `js`

[Исходник](../../tests/electron/background-runs-smoke.cjs#L26)

```typescript
async function js(code)
```

Выполняет проверяемый шаг в изолированном renderer.

### `poll`

[Исходник](../../tests/electron/background-runs-smoke.cjs#L27)

```typescript
async function poll(code)
```

Ждёт DOM состояние с ограниченным timeout.

### `click`

[Исходник](../../tests/electron/background-runs-smoke.cjs#L28)

```typescript
async function click(selector)
```

Нажимает известный DOM элемент и даёт React завершить обработчик.

### `input`

[Исходник](../../tests/electron/background-runs-smoke.cjs#L29)

```typescript
async function input(selector, value)
```

Меняет controlled поле через native setter и input event.

### `finish`

[Исходник](../../tests/electron/background-runs-smoke.cjs#L30)

```typescript
async function finish(error)
```

Сохраняет результат/диагностику и закрывает только тестовое приложение и HTTP fixture.

<a id="module-tests-electron-desktop-apps-cjs"></a>

## `tests/electron/desktop-apps.cjs`

Node-проверка границы каталога приложений: ID, запрет путей/команд, EXE, повторное добавление, удаление и браузер без реальных окон.

Нет именованных функций/типов: модуль выполняет конфигурацию, сборочный вызов или render entry. Анонимные callbacks описаны в учебных главах.

<a id="module-tests-electron-ide-acceptance-run-cjs"></a>

## `tests/electron/ide-acceptance-run.cjs`

Запускает native IDE fixture в отдельном acceptance режиме; --json выбирает строгий JSON fixture.

Нет именованных функций/типов: модуль выполняет конфигурацию, сборочный вызов или render entry. Анонимные callbacks описаны в учебных главах.

<a id="module-tests-electron-ide-acceptance-cjs"></a>

## `tests/electron/ide-acceptance.cjs`

Реальный UI/Core сценарий: без модели, отказ, missing import exit1→repair→exit0, stale evidence и draft isolation.

### `runAcceptance`

[Исходник](../../tests/electron/ide-acceptance.cjs#L3)

```typescript
async function runAcceptance({desktop,panel,until,screenshot,fs,path,project,requests})
```

Выполняет native/JSON вертикальный сценарий configured checks через настоящий Core и editor.

### `runAcceptance.input`

[Исходник](../../tests/electron/ide-acceptance.cjs#L4)

```typescript
input(label, value)
```

Вводит поле по доступному имени через React-совместимый DOM setter.

### `runAcceptance.textButton`

[Исходник](../../tests/electron/ide-acceptance.cjs#L8)

```typescript
textButton(text)
```

Нажимает кнопку с точной подписью в acceptance fixture.

### `runAcceptance.nav`

[Исходник](../../tests/electron/ide-acceptance.cjs#L9)

```typescript
nav(label)
```

Открывает раздел новой панели по подписи навигации.

### `runAcceptance.loadCurrent`

[Исходник](../../tests/electron/ide-acceptance.cjs#L10)

```typescript
loadCurrent()
```

Читает canonical checkpoint текущего тестового чата после завершения запуска.

### `runAcceptance.approve`

[Исходник](../../tests/electron/ide-acceptance.cjs#L11)

```typescript
approve(decision)
```

Разрешает или отклоняет точную команду и ожидает task_end, не путая его с закрытием approval.

<a id="module-tests-electron-ide-acceptance-test-cjs"></a>

## `tests/electron/ide-acceptance.test.cjs`

Node regressions сериализации, argv/scope/check_id, readonly/resume и восстановления draft.

Нет именованных функций/типов: модуль выполняет конфигурацию, сборочный вызов или render entry. Анонимные callbacks описаны в учебных главах.

<a id="module-tests-electron-ide-session-test-cjs"></a>

## `tests/electron/ide-session.test.cjs`

Node-проверки ранних и повторных событий, завершённых runs и редактирования безопасной диагностики.

Нет именованных функций/типов: модуль выполняет конфигурацию, сборочный вызов или render entry. Анонимные callbacks описаны в учебных главах.

<a id="module-tests-electron-leshy-themes-cjs"></a>

## `tests/electron/leshy-themes.cjs`

Изолированная Electron-проверка трёх тем, настроек и состояний окон.

### `BrowserWindow.prototype.show`

[Исходник](../../tests/electron/leshy-themes.cjs#L7)

```typescript
BrowserWindow.prototype.show()
```

Только в smoke-тесте подавляет показ настоящего окна пользователю.

### `BrowserWindow.prototype.loadURL`

[Исходник](../../tests/electron/leshy-themes.cjs#L8)

```typescript
BrowserWindow.prototype.loadURL()
```

Загружает production renderer вместо dev server в тестовом окне.

### `dialog.showOpenDialog`

[Исходник](../../tests/electron/leshy-themes.cjs#L9)

```typescript
dialog.showOpenDialog()
```

Только в smoke-тесте возвращает учебный каталог вместо настоящего системного диалога.

### `dialog.showSaveDialog`

[Исходник](../../tests/electron/leshy-themes.cjs#L9)

```typescript
dialog.showSaveDialog(_win, options)
```

Направляет экспорт в изолированный output теста.

### `dialog.showMessageBox`

[Исходник](../../tests/electron/leshy-themes.cjs#L9)

```typescript
dialog.showMessageBox()
```

В Electron smoke подменяет нативное подтверждение несохранённых изменений управляемым ответом Cancel/Discard.

### `ipcMain.handle`

[Исходник](../../tests/electron/leshy-themes.cjs#L16)

```typescript
ipcMain.handle(channel, handler)
```

В Electron fixture перехватывает только speech playback для проверки UI/Stop без звука; остальные IPC проходят в настоящий main.

### `releaseVisual`

[Исходник](../../tests/electron/leshy-themes.cjs#L29)

```typescript
releaseVisual()
```

Разрешает fixture после визуальной контрольной точки.

### `done`

[Исходник](../../tests/electron/leshy-themes.cjs#L51)

```typescript
done(id)
```

Завершает тестовый сценарий и освобождает его ресурсы.

### `releaseStage4`

[Исходник](../../tests/electron/leshy-themes.cjs#L61)

```typescript
releaseStage4()
```

Разрешает отложенный HTTP fixture этапа.

### `js`

[Исходник](../../tests/electron/leshy-themes.cjs#L67)

```typescript
async function js(code)
```

Вычисляет выражение в тестовом renderer.

### `poll`

[Исходник](../../tests/electron/leshy-themes.cjs#L68)

```typescript
async function poll(expression, timeout=15000)
```

В тесте ожидает DOM-условие с ограничением времени.

### `click`

[Исходник](../../tests/electron/leshy-themes.cjs#L69)

```typescript
async function click(selector)
```

Нажимает найденный renderer control.

### `textButton`

[Исходник](../../tests/electron/leshy-themes.cjs#L70)

```typescript
async function textButton(selector, text)
```

Находит кнопку по отображаемому тексту.

### `input`

[Исходник](../../tests/electron/leshy-themes.cjs#L71)

```typescript
async function input(selector, value)
```

Вводит значение с React-совместимыми событиями.

### `capture`

[Исходник](../../tests/electron/leshy-themes.cjs#L72)

```typescript
async function capture(name)
```

Сохраняет screenshot текущего состояния renderer.

### `finish`

[Исходник](../../tests/electron/leshy-themes.cjs#L73)

```typescript
async function finish(error)
```

Сохраняет отчёт и завершает Electron с кодом результата.

<a id="module-tests-electron-lola-desktop-smoke-cjs"></a>

## `tests/electron/lola-desktop-smoke.cjs`

Изолированный Electron fixture для настоящего окна/Tray Лолы, настроек, sender isolation, скрытого основного окна и единственного model/Core запроса.

### `BrowserWindow.prototype.show`

[Исходник](../../tests/electron/lola-desktop-smoke.cjs#L7)

```typescript
BrowserWindow.prototype.show()
```

Подавляет показ тестового основного окна, чтобы GUI smoke не вмешивался в desktop session.

### `BrowserWindow.prototype.showInactive`

[Исходник](../../tests/electron/lola-desktop-smoke.cjs#L7)

```typescript
BrowserWindow.prototype.showInactive()
```

Делает тестовое окно почти прозрачным при сохранении настоящего нативного lifecycle.

### `BrowserWindow.prototype.loadURL`

[Исходник](../../tests/electron/lola-desktop-smoke.cjs#L8)

```typescript
BrowserWindow.prototype.loadURL(url)
```

Направляет dev entrypoint на собранные локальные тестовые страницы.

### `dialog.showMessageBox`

[Исходник](../../tests/electron/lola-desktop-smoke.cjs#L9)

```typescript
dialog.showMessageBox()
```

Автоматизирует только тестовый discard confirmation.

### `ipcMain.handle`

[Исходник](../../tests/electron/lola-desktop-smoke.cjs#L10)

```typescript
ipcMain.handle(name, handler)
```

Перехватывает ссылки на handlers для проверки настоящей sender authorization.

### `BrowserWindow.prototype.setIgnoreMouseEvents`

[Исходник](../../tests/electron/lola-desktop-smoke.cjs#L11)

```typescript
BrowserWindow.prototype.setIgnoreMouseEvents(value, options)
```

Записывает click-through решения настоящего окна для утверждений теста.

### `childProcess.spawn`

[Исходник](../../tests/electron/lola-desktop-smoke.cjs#L13)

```typescript
childProcess.spawn(file, ...args)
```

Считает фактические старты Core, не подменяя сам процесс.

### `js`

[Исходник](../../tests/electron/lola-desktop-smoke.cjs#L15)

```typescript
async function js(win, code)
```

Выполняет UI проверку в изолированном тестовом окне.

### `poll`

[Исходник](../../tests/electron/lola-desktop-smoke.cjs#L16)

```typescript
async function poll(win, expression, timeout=15000)
```

Ожидает DOM/API условие с жёстким timeout.

### `input`

[Исходник](../../tests/electron/lola-desktop-smoke.cjs#L17)

```typescript
async function input(win, selector, text)
```

Задаёт controlled input через native DOM setter в тестовом окне.

### `capture`

[Исходник](../../tests/electron/lola-desktop-smoke.cjs#L18)

```typescript
async function capture(name)
```

Сохраняет кадр настоящего изолированного Electron окна для визуальной проверки.

### `finish`

[Исходник](../../tests/electron/lola-desktop-smoke.cjs#L19)

```typescript
async function finish(error)
```

Сохраняет machine-readable результат, закрывает fixture и завершает тестовое приложение.

<a id="module-tests-electron-lola-preferences-cjs"></a>

## `tests/electron/lola-preferences.cjs`

Pure contract проверки defaults, валидации размеров/координат и bounded frame спутника.

Нет именованных функций/типов: модуль выполняет конфигурацию, сборочный вызов или render entry. Анонимные callbacks описаны в учебных главах.

<a id="module-tests-electron-microphone-cjs"></a>

## `tests/electron/microphone.cjs`

Проверка захвата и обрезки WAV с фиктивным AudioContext без записи реального микрофона.

### `getUserMedia`

[Исходник](../../tests/electron/microphone.cjs#L8)

```typescript
getUserMedia(value)
```

Создаёт фиктивный MediaStream, сохраняя запрошенные ограничения микрофона.

### `getUserMedia.getTracks`

[Исходник](../../tests/electron/microphone.cjs#L8)

```typescript
getTracks()
```

Возвращает фиктивную дорожку для проверки освобождения устройства.

### `getUserMedia.getTracks.stop`

[Исходник](../../tests/electron/microphone.cjs#L8)

```typescript
stop()
```

Считает остановки дорожки при завершении и отмене записи.

### `btoa`

[Исходник](../../tests/electron/microphone.cjs#L15)

```typescript
btoa(value)
```

Кодирует тестовый PCM WAV в base64 через Node Buffer.

### `main`

[Исходник](../../tests/electron/microphone.cjs#L19)

```typescript
async function main()
```

Без устройства проверяет конец речи, границы PCM после обрезки, тишину, ограничения аудио и остановку tracks.

### `main.block`

[Исходник](../../tests/electron/microphone.cjs#L23)

```typescript
block(value)
```

Передаёт детерминированный блок речи либо тишины обработчику AudioContext.

### `main.block.getChannelData`

[Исходник](../../tests/electron/microphone.cjs#L23)

```typescript
getChannelData()
```

Возвращает 1024 сэмпла с заданной тестовой амплитудой.

<a id="module-tests-electron-neutral-ide-integration-cjs"></a>

## `tests/electron/neutral-ide-integration.cjs`

Сквозная проверка Desktop → Code-OSS webview → Core → editor, истории и approvals.

### `BrowserWindow.prototype.show`

[Исходник](../../tests/electron/neutral-ide-integration.cjs#L8)

```typescript
BrowserWindow.prototype.show()
```

Только в smoke-тесте подавляет показ настоящего окна пользователю.

### `dialog.showOpenDialog`

[Исходник](../../tests/electron/neutral-ide-integration.cjs#L8)

```typescript
dialog.showOpenDialog()
```

Только в smoke-тесте возвращает учебный каталог вместо настоящего системного диалога.

### `ipcMain.handle`

[Исходник](../../tests/electron/neutral-ide-integration.cjs#L12)

```typescript
ipcMain.handle(channel, handler)
```

В Electron fixture перехватывает только speech playback для проверки UI/Stop без звука; остальные IPC проходят в настоящий main.

### `delay`

[Исходник](../../tests/electron/neutral-ide-integration.cjs#L30)

```typescript
delay(ms)
```

Короткая асинхронная пауза ожидания fixture.

### `until`

[Исходник](../../tests/electron/neutral-ide-integration.cjs#L31)

```typescript
async function until(action, label, timeout=30000)
```

Ожидает проверяемое условие с конечным timeout.

### `desktop`

[Исходник](../../tests/electron/neutral-ide-integration.cjs#L32)

```typescript
async function desktop(code)
```

Выполняет выражение в desktop renderer.

### `connect`

[Исходник](../../tests/electron/neutral-ide-integration.cjs#L33)

```typescript
async function connect(url)
```

Создаёт loopback CDP-клиент собственного Code-OSS.

### `connect.socket.onmessage`

[Исходник](../../tests/electron/neutral-ide-integration.cjs#L33)

```typescript
socket.onmessage(event)
```

Разбирает CDP ответы и события сессий.

### `connect.send`

[Исходник](../../tests/electron/neutral-ide-integration.cjs#L33)

```typescript
send(method, params={}, sessionId)
```

Отправляет CDP-команду с уникальным id и optional session.

### `connect.close`

[Исходник](../../tests/electron/neutral-ide-integration.cjs#L33)

```typescript
close()
```

Закрывает тестовое CDP соединение.

### `evaluate`

[Исходник](../../tests/electron/neutral-ide-integration.cjs#L34)

```typescript
async function evaluate(context, expression)
```

Выполняет выражение в выбранном execution context.

### `findWebview`

[Исходник](../../tests/electron/neutral-ide-integration.cjs#L35)

```typescript
async function findWebview()
```

Находит execution context независимой панели агента.

### `panel`

[Исходник](../../tests/electron/neutral-ide-integration.cjs#L41)

```typescript
async function panel(expression)
```

Вычисляет выражение в webview панели.

### `semanticBorder`

[Исходник](../../tests/electron/neutral-ide-integration.cjs#L42)

```typescript
async function semanticBorder(selector, token)
```

Сравнивает цвет границы с семантическим CSS token.

### `screenshot`

[Исходник](../../tests/electron/neutral-ide-integration.cjs#L43)

```typescript
async function screenshot(name)
```

Сохраняет CDP screenshot Code-OSS.

### `finish`

[Исходник](../../tests/electron/neutral-ide-integration.cjs#L44)

```typescript
async function finish(error)
```

Сохраняет report/requests и закрывает только своё дерево IDE.

### `resizePanel`

[Исходник](../../tests/electron/neutral-ide-integration.cjs#L68)

```typescript
async function resizePanel(width)
```

Меняет ширину панели для проверки компактных состояний.

### `checkControls`

[Исходник](../../tests/electron/neutral-ide-integration.cjs#L73)

```typescript
async function checkControls(page, width)
```

Проверяет геометрию и доступность controls панели.

<a id="module-tests-electron-neutral-ide-smoke-cjs"></a>

## `tests/electron/neutral-ide-smoke.cjs`

Изолированная проверка кнопки Neutral IDE, root/dirty guards, собственного executable/profile и реального Core через auth/allowlist.

### `BrowserWindow.prototype.show`

[Исходник](../../tests/electron/neutral-ide-smoke.cjs#L8)

```typescript
BrowserWindow.prototype.show()
```

Скрывает только окно тестируемого desktop, не меняя его Core/IPC.

### `dialog.showOpenDialog`

[Исходник](../../tests/electron/neutral-ide-smoke.cjs#L8)

```typescript
dialog.showOpenDialog()
```

Выбирает одноразовый тестовый проект для настоящего project route.

### `ipcMain.handle`

[Исходник](../../tests/electron/neutral-ide-smoke.cjs#L12)

```typescript
ipcMain.handle(channel, handler)
```

Сохраняет результат настоящего ide:open для проверки собственного PID и последующего закрытия тестового дерева.

### `delay`

[Исходник](../../tests/electron/neutral-ide-smoke.cjs#L13)

```typescript
delay(ms)
```

Небольшая асинхронная пауза в polling smoke.

### `js`

[Исходник](../../tests/electron/neutral-ide-smoke.cjs#L14)

```typescript
async function js(code)
```

Выполняет действия в renderer реального тестового окна Neutral.

### `wait`

[Исходник](../../tests/electron/neutral-ide-smoke.cjs#L15)

```typescript
async function wait(check, label, timeout=15000)
```

Ожидает проверяемое условие с конечным timeout.

### `request`

[Исходник](../../tests/electron/neutral-ide-smoke.cjs#L16)

```typescript
async function request(connection, method, token=connection.token)
```

Обращается к реальному named pipe для status/focus и отрицательных auth/allowlist checks.

### `finish`

[Исходник](../../tests/electron/neutral-ide-smoke.cjs#L17)

```typescript
async function finish(error)
```

Сохраняет отчёт, закрывает собственную IDE/process tree и завершает Electron с корректным exit code после штатного quit.

<a id="module-tests-electron-neutral-smoke-cjs"></a>

## `tests/electron/neutral-smoke.cjs`

Стабильный CI entrypoint полной проверки Studio; делегирует tests/electron/studio-smoke.cjs.

Нет именованных функций/типов: модуль выполняет конфигурацию, сборочный вызов или render entry. Анонимные callbacks описаны в учебных главах.

<a id="module-tests-electron-optional-ide-smoke-cjs"></a>

## `tests/electron/optional-ide-smoke.cjs`

Реальный UI/Core workflow исследования, LSP, создания/отказа удаления/открытия worktree и панели Docker; отдельный профиль.

### `BrowserWindow.prototype.show`

[Исходник](../../tests/electron/optional-ide-smoke.cjs#L9)

```typescript
BrowserWindow.prototype.show()
```

Только в smoke-тесте подавляет показ настоящего окна пользователю.

### `BrowserWindow.prototype.loadURL`

[Исходник](../../tests/electron/optional-ide-smoke.cjs#L9)

```typescript
BrowserWindow.prototype.loadURL()
```

Открывает собранный renderer из dist только в изолированном optional IDE smoke.

### `dialog.showOpenDialog`

[Исходник](../../tests/electron/optional-ide-smoke.cjs#L10)

```typescript
dialog.showOpenDialog()
```

Только в smoke-тесте возвращает учебный каталог вместо настоящего системного диалога.

### `dialog.showMessageBox`

[Исходник](../../tests/electron/optional-ide-smoke.cjs#L10)

```typescript
dialog.showMessageBox()
```

В Electron smoke подменяет нативное подтверждение несохранённых изменений управляемым ответом Cancel/Discard.

### `js`

[Исходник](../../tests/electron/optional-ide-smoke.cjs#L21)

```typescript
async function js(code)
```

Выполняет renderer JavaScript только в тестовом Electron окне.

### `poll`

[Исходник](../../tests/electron/optional-ide-smoke.cjs#L22)

```typescript
async function poll(expression, timeout=12000)
```

Ожидает наблюдаемое DOM условие с ограниченным timeout.

### `click`

[Исходник](../../tests/electron/optional-ide-smoke.cjs#L23)

```typescript
async function click(selector)
```

Нажимает известный тестовый элемент и даёт React применить состояние.

### `button`

[Исходник](../../tests/electron/optional-ide-smoke.cjs#L24)

```typescript
async function button(text)
```

Находит точную подпись кнопки внутри optional dialog.

### `input`

[Исходник](../../tests/electron/optional-ide-smoke.cjs#L25)

```typescript
async function input(selector, value)
```

Меняет controlled input через native setter и input event.

### `save`

[Исходник](../../tests/electron/optional-ide-smoke.cjs#L26)

```typescript
async function save()
```

Сохраняет settings UI и ждёт подтверждение Core.

### `capture`

[Исходник](../../tests/electron/optional-ide-smoke.cjs#L27)

```typescript
async function capture(name)
```

Дожидается repaint и сохраняет PNG реального окна.

### `finish`

[Исходник](../../tests/electron/optional-ide-smoke.cjs#L28)

```typescript
async function finish(error)
```

Сохраняет результат и диагностический screenshot, закрывает локальный fixture и тестовое приложение.

<a id="module-tests-electron-packaged-ide-mjs"></a>

## `tests/electron/packaged-ide.mjs`

CDP-приёмка вложенной IDE свежего пакета: frozen Core, diff approval, editor-owned запись и Undo/Save.

### `until`

[Исходник](../../tests/electron/packaged-ide.mjs#L7)

```typescript
async function until(action, label)
```

Ожидает конкретное условие packaged IDE с конечным timeout и последней ошибкой.

### `verifyPackagedIde`

[Исходник](../../tests/electron/packaged-ide.mjs#L17)

```typescript
async function verifyPackagedIde({ desktop, directory, modelUrl })
```

Открывает временный workspace в упакованной IDE и проверяет approval, запись и Undo без системного Python.

### `verifyPackagedIde.socket.onmessage`

[Исходник](../../tests/electron/packaged-ide.mjs#L38)

```typescript
socket.onmessage(event)
```

Разбирает CDP contexts и коррелированные ответы собственной IDE.

### `verifyPackagedIde.send`

[Исходник](../../tests/electron/packaged-ide.mjs#L44)

```typescript
send(method, params = {}, sessionId)
```

Отправляет CDP-команду с уникальным id и ограниченным ожиданием.

### `verifyPackagedIde.evaluate`

[Исходник](../../tests/electron/packaged-ide.mjs#L50)

```typescript
evaluate(context, expression)
```

Выполняет выражение в выбранном CDP context и проверяет исключения.

### `verifyPackagedIde.panel`

[Исходник](../../tests/electron/packaged-ide.mjs#L68)

```typescript
panel(expression)
```

Выполняет выражение только в webview упакованной панели агента.

### `verifyPackagedIde.setCheckField`

[Исходник](../../tests/electron/packaged-ide.mjs#L91)

```typescript
setCheckField(label, value)
```

Настраивает packaged check по доступному имени, дожидаясь React commit.

<a id="module-tests-electron-packaged-path-mjs"></a>

## `tests/electron/packaged-path.mjs`

Выбирает точный Windows executable из конфигурации сборки либо явного пути без fallback на старый бренд.

### `resolvePackagedExecutable`

[Исходник](../../tests/electron/packaged-path.mjs#L5)

```typescript
async function resolvePackagedExecutable({ repoRoot, explicitPath })
```

Разрешает существующий файл текущего productName/executableName или точного переданного пути.

<a id="module-tests-electron-packaged-path-test-mjs"></a>

## `tests/electron/packaged-path.test.mjs`

Проверки чистого LESHY output, старого Neutral output, обоих файлов и явного пути пакета.

### `fixture`

[Исходник](../../tests/electron/packaged-path.test.mjs#L8)

```typescript
async function fixture(t, names)
```

Создаёт одноразовую конфигурацию и output с заданными именами executable.

<a id="module-tests-electron-packaged-smoke-mjs"></a>

## `tests/electron/packaged-smoke.mjs`

CDP-проверка настоящего packaged exe с урезанным PATH, discovery и повторным запуском.

### `freePort`

[Исходник](../../tests/electron/packaged-smoke.mjs#L13)

```typescript
async function freePort()
```

Резервирует свободный loopback-порт для тестового Chromium CDP.

### `connectPage`

[Исходник](../../tests/electron/packaged-smoke.mjs#L21)

```typescript
async function connectPage(port, child, companion = false)
```

Ожидает file renderer настоящего exe и открывает WebSocket CDP с ограниченным временем.

### `evaluate`

[Исходник](../../tests/electron/packaged-smoke.mjs#L38)

```typescript
function evaluate(socket, expression)
```

Последовательно исполняет одно тестовое выражение через CDP с тайм-аутом.

### `evaluate.receive`

[Исходник](../../tests/electron/packaged-smoke.mjs#L41)

```typescript
receive(event)
```

Сопоставляет CDP response с запросом и возвращает значение либо ошибку JavaScript.

### `run`

[Исходник](../../tests/electron/packaged-smoke.mjs#L53)

```typescript
async function run(executable, directory, first, modelUrl)
```

Проверяет bundled Core/schema 3 и сохранение истории в packaged Studio без Python в PATH; IDE/Chat остаются в main, микрофон проверяется в отдельной Лоле.

### `run.desktop`

[Исходник](../../tests/electron/packaged-smoke.mjs#L157)

```typescript
desktop(expression)
```

Передаёт последовательные CDP-выражения desktop в packaged IDE acceptance helper.

### `main`

[Исходник](../../tests/electron/packaged-smoke.mjs#L171)

```typescript
async function main()
```

Поднимает HTTP-фикстуру, дважды проверяет пакет и отсутствие ключа в настройках/диагностике.

<a id="module-tests-electron-readiness-live-cjs"></a>

## `tests/electron/readiness-live.cjs`

Явно запускаемая desktop приёмка с настоящей моделью LM Studio, readonly ребёнком, правкой и независимой проверкой одноразового проекта.

### `BrowserWindow.prototype.show`

[Исходник](../../tests/electron/readiness-live.cjs#L14)

```typescript
BrowserWindow.prototype.show()
```

Подавляет показ окна только в headless тесте; NEUTRAL_INSPECT_GUI оставляет окно для осмотра.

### `dialog.showOpenDialog`

[Исходник](../../tests/electron/readiness-live.cjs#L15)

```typescript
dialog.showOpenDialog()
```

Выбирает только созданную тестом disposable папку через штатный workspace UI.

### `js`

[Исходник](../../tests/electron/readiness-live.cjs#L26)

```typescript
async function js(code)
```

Выполняет сценарий внутри настоящего Electron renderer.

### `poll`

[Исходник](../../tests/electron/readiness-live.cjs#L27)

```typescript
async function poll(expression, timeout=20000)
```

Ожидает наблюдаемое состояние DOM с ограничением времени теста.

### `click`

[Исходник](../../tests/electron/readiness-live.cjs#L28)

```typescript
async function click(selector)
```

Нажимает найденный элемент интерфейса.

### `input`

[Исходник](../../tests/electron/readiness-live.cjs#L29)

```typescript
async function input(selector, value)
```

Заполняет React input/textarea штатным setter и input event.

### `button`

[Исходник](../../tests/electron/readiness-live.cjs#L30)

```typescript
async function button(selector, label)
```

Нажимает кнопку с точным текстом в указанной области.

### `capture`

[Исходник](../../tests/electron/readiness-live.cjs#L31)

```typescript
async function capture(name)
```

Сохраняет PNG настоящего renderer для проверки layout и разрешений.

### `finish`

[Исходник](../../tests/electron/readiness-live.cjs#L37)

```typescript
async function finish(error)
```

Сохраняет фактический checkpoint, события, решения и screenshot; отмечает ошибки приёмки.

### `win.webContents.send`

[Исходник](../../tests/electron/readiness-live.cjs#L54)

```typescript
win.webContents.send(channel, value)
```

Наблюдает реальные Core events и approval для отчёта, затем передаёт их штатному renderer.

<a id="module-tests-electron-run-cjs"></a>

## `tests/electron/run.cjs`

Запускает выбранную нативную Electron-проверку без ELECTRON_RUN_AS_NODE и с наследованием её exit code.

Нет именованных функций/типов: модуль выполняет конфигурацию, сборочный вызов или render entry. Анонимные callbacks описаны в учебных главах.

<a id="module-tests-electron-runner-exit-test-cjs"></a>

## `tests/electron/runner-exit.test.cjs`

Node VM-проверки кодов launcher: успех, ошибка, сигнал и spawn failure.

### `launch`

[Исходник](../../tests/electron/runner-exit.test.cjs#L7)

```typescript
function launch()
```

Выполняет реальный launcher в VM с изолированным process и spawn.

### `launch.spawn`

[Исходник](../../tests/electron/runner-exit.test.cjs#L13)

```typescript
spawn()
```

Возвращает тестовый дочерний процесс без запуска Electron.

### `launch.spawn.on`

[Исходник](../../tests/electron/runner-exit.test.cjs#L13)

```typescript
on(event, callback)
```

Запоминает callback lifecycle для моделирования exit/error.

<a id="module-tests-electron-smoke-cjs"></a>

## `tests/electron/smoke.cjs`

Скрытое настоящее Electron-окно: все слои, запись, поток, reload и Stop.

### `desktopCapturer.getSources`

[Исходник](../../tests/electron/smoke.cjs#L5)

```typescript
desktopCapturer.getSources()
```

GUI fixture возвращает синтетический 1×1 NativeImage вместо захвата настоящего экрана; проверяет host broker и preview без чтения рабочего стола пользователя.

### `handlerForVoiceStatus`

[Исходник](../../tests/electron/smoke.cjs#L26)

```typescript
handlerForVoiceStatus()
```

В Electron fixture хранит реальный status handler для симуляции speaking без воспроизведения.

### `ipcMain.handle`

[Исходник](../../tests/electron/smoke.cjs#L27)

```typescript
ipcMain.handle(channel, handler)
```

В Electron fixture перехватывает только speech playback для проверки UI/Stop без звука; остальные IPC проходят в настоящий main.

### `fail`

[Исходник](../../tests/electron/smoke.cjs#L58)

```typescript
function fail(error)
```

В smoke-тесте записывает ошибку в result.json и завершает Electron.

### `BrowserWindow.prototype.show`

[Исходник](../../tests/electron/smoke.cjs#L68)

```typescript
BrowserWindow.prototype.show()
```

Только в smoke-тесте подавляет показ настоящего окна пользователю.

### `BrowserWindow.prototype.loadURL`

[Исходник](../../tests/electron/smoke.cjs#L69)

```typescript
BrowserWindow.prototype.loadURL()
```

Открывает готовый renderer из dist, чтобы полная проверка редактора и голоса не зависела от пользовательского Vite.

### `dialog.showMessageBox`

[Исходник](../../tests/electron/smoke.cjs#L71)

```typescript
dialog.showMessageBox()
```

В Electron smoke подменяет нативное подтверждение несохранённых изменений управляемым ответом Cancel/Discard.

### `dialog.showOpenDialog`

[Исходник](../../tests/electron/smoke.cjs#L78)

```typescript
dialog.showOpenDialog(_win, options)
```

Только в smoke-тесте возвращает учебный каталог вместо настоящего системного диалога.

### `encode`

[Исходник](../../tests/electron/smoke.cjs#L104)

```typescript
encode(delta)
```

Сериализует детерминированный SSE-чанк модельной фикстуры.

### `releaseModelText`

[Исходник](../../tests/electron/smoke.cjs#L114)

```typescript
releaseModelText()
```

Завершает задержанный ответ фикстуры после проверки видимого частичного текста.

### `releaseModelText`

[Исходник](../../tests/electron/smoke.cjs#L124)

```typescript
releaseModelText()
```

Завершает задержанный ответ фикстуры после проверки видимого частичного текста.

### `poll`

[Исходник](../../tests/electron/smoke.cjs#L131)

```typescript
async function poll(win, expression, timeout=10000)
```

В тесте ожидает DOM-условие с ограничением времени.

### `win.webContents.executeJavaScript`

[Исходник](../../tests/electron/smoke.cjs#L142)

```typescript
win.webContents.executeJavaScript(...args)
```

Добавляет текст неудавшегося renderer-шага к ошибке скрытого Electron smoke для диагностики.

<a id="module-tests-electron-studio-layout-cjs"></a>

## `tests/electron/studio-layout.cjs`

Нативная проверка pointer/keyboard resize, сохранения раскладок, фокуса, модели под запросом и IME.

### `BrowserWindow.prototype.show`

[Исходник](../../tests/electron/studio-layout.cjs#L7)

```typescript
BrowserWindow.prototype.show()
```

Только в smoke-тесте подавляет показ настоящего окна пользователю.

### `BrowserWindow.prototype.loadURL`

[Исходник](../../tests/electron/studio-layout.cjs#L8)

```typescript
BrowserWindow.prototype.loadURL()
```

Открывает собранный renderer вместо пользовательского Vite, изолируя GUI-проверку.

### `dialog.showOpenDialog`

[Исходник](../../tests/electron/studio-layout.cjs#L9)

```typescript
dialog.showOpenDialog()
```

Только в smoke-тесте возвращает учебный каталог вместо настоящего системного диалога.

### `dialog.showSaveDialog`

[Исходник](../../tests/electron/studio-layout.cjs#L9)

```typescript
dialog.showSaveDialog(_win, options)
```

Выбирает только тестовый путь экспорта без системного диалога пользователю.

### `dialog.showMessageBox`

[Исходник](../../tests/electron/studio-layout.cjs#L9)

```typescript
dialog.showMessageBox()
```

В Electron smoke подменяет нативное подтверждение несохранённых изменений управляемым ответом Cancel/Discard.

### `ipcMain.handle`

[Исходник](../../tests/electron/studio-layout.cjs#L16)

```typescript
ipcMain.handle(channel, handler)
```

В Electron fixture перехватывает только speech playback для проверки UI/Stop без звука; остальные IPC проходят в настоящий main.

### `releaseVisual`

[Исходник](../../tests/electron/studio-layout.cjs#L28)

```typescript
releaseVisual()
```

Освобождает удерживаемый fixture SSE после снимка состояния выполняющейся задачи.

### `done`

[Исходник](../../tests/electron/studio-layout.cjs#L50)

```typescript
done(id)
```

В локальной HTTP-фикстуре проверяет успешную квитанцию конкретного шага создания каталога, файла и patch.

### `releaseStage4`

[Исходник](../../tests/electron/studio-layout.cjs#L60)

```typescript
releaseStage4()
```

Завершает удерживаемый SSE-поток только после проверки, что закрытие подробностей не остановило задачу.

### `js`

[Исходник](../../tests/electron/studio-layout.cjs#L66)

```typescript
async function js(code)
```

Выполняет renderer-шаг, даёт React завершить обновление и добавляет код к ошибке.

### `poll`

[Исходник](../../tests/electron/studio-layout.cjs#L67)

```typescript
async function poll(expression, timeout=15000)
```

В тесте ожидает DOM-условие с ограничением времени.

### `click`

[Исходник](../../tests/electron/studio-layout.cjs#L68)

```typescript
async function click(selector)
```

Нажимает выбранный DOM-контрол через реальный renderer.

### `textButton`

[Исходник](../../tests/electron/studio-layout.cjs#L69)

```typescript
async function textButton(selector, text)
```

Находит кнопку в заданной области по точному видимому тексту.

### `input`

[Исходник](../../tests/electron/studio-layout.cjs#L70)

```typescript
async function input(selector, value)
```

Изменяет native input/textarea и посылает React input event.

### `capture`

[Исходник](../../tests/electron/studio-layout.cjs#L71)

```typescript
async function capture(name)
```

Сохраняет screenshot и геометрию основных панелей для визуальной проверки.

### `finish`

[Исходник](../../tests/electron/studio-layout.cjs#L72)

```typescript
async function finish(error)
```

Пишет итог и диагностику ошибки, закрывает только тестовое приложение и HTTP fixture.

### `width`

[Исходник](../../tests/electron/studio-layout.cjs#L79)

```typescript
width()
```

Измеряет ширину настоящей панели после pointer/keyboard resize для проверки clamp и persistence.

<a id="module-tests-electron-studio-smoke-cjs"></a>

## `tests/electron/studio-smoke.cjs`

Изолированная полная проверка рабочего renderer/IPC/Core: история, проекты, модель, инструменты, редактор, approvals и восстановление.

### `BrowserWindow.prototype.show`

[Исходник](../../tests/electron/studio-smoke.cjs#L7)

```typescript
BrowserWindow.prototype.show()
```

Только в smoke-тесте подавляет показ настоящего окна пользователю.

### `BrowserWindow.prototype.loadURL`

[Исходник](../../tests/electron/studio-smoke.cjs#L8)

```typescript
BrowserWindow.prototype.loadURL()
```

Открывает собранный renderer вместо пользовательского Vite, изолируя GUI-проверку.

### `dialog.showOpenDialog`

[Исходник](../../tests/electron/studio-smoke.cjs#L9)

```typescript
dialog.showOpenDialog()
```

Только в smoke-тесте возвращает учебный каталог вместо настоящего системного диалога.

### `dialog.showSaveDialog`

[Исходник](../../tests/electron/studio-smoke.cjs#L9)

```typescript
dialog.showSaveDialog(_win, options)
```

Выбирает только тестовый путь экспорта без системного диалога пользователю.

### `dialog.showMessageBox`

[Исходник](../../tests/electron/studio-smoke.cjs#L9)

```typescript
dialog.showMessageBox()
```

В Electron smoke подменяет нативное подтверждение несохранённых изменений управляемым ответом Cancel/Discard.

### `ipcMain.handle`

[Исходник](../../tests/electron/studio-smoke.cjs#L16)

```typescript
ipcMain.handle(channel, handler)
```

В Electron fixture перехватывает только speech playback для проверки UI/Stop без звука; остальные IPC проходят в настоящий main.

### `done`

[Исходник](../../tests/electron/studio-smoke.cjs#L48)

```typescript
done(id)
```

В локальной HTTP-фикстуре проверяет успешную квитанцию конкретного шага создания каталога, файла и patch.

### `releaseStage4`

[Исходник](../../tests/electron/studio-smoke.cjs#L58)

```typescript
releaseStage4()
```

Завершает удерживаемый SSE-поток только после проверки, что закрытие подробностей не остановило задачу.

### `js`

[Исходник](../../tests/electron/studio-smoke.cjs#L64)

```typescript
async function js(code)
```

Выполняет renderer-шаг, даёт React завершить обновление и добавляет код к ошибке.

### `poll`

[Исходник](../../tests/electron/studio-smoke.cjs#L65)

```typescript
async function poll(expression, timeout=15000)
```

В тесте ожидает DOM-условие с ограничением времени.

### `click`

[Исходник](../../tests/electron/studio-smoke.cjs#L66)

```typescript
async function click(selector)
```

Нажимает выбранный DOM-контрол через реальный renderer.

### `selectIdeConversation`

[Исходник](../../tests/electron/studio-smoke.cjs#L67)

```typescript
async function selectIdeConversation()
```

Открывает историю у чата IDE и выбирает реальный разговор по названию.

### `textButton`

[Исходник](../../tests/electron/studio-smoke.cjs#L68)

```typescript
async function textButton(selector, text)
```

Находит кнопку в заданной области по точному видимому тексту.

### `input`

[Исходник](../../tests/electron/studio-smoke.cjs#L69)

```typescript
async function input(selector, value)
```

Изменяет native input/textarea и посылает React input event.

### `capture`

[Исходник](../../tests/electron/studio-smoke.cjs#L70)

```typescript
async function capture(name)
```

Сохраняет screenshot и геометрию основных панелей для визуальной проверки.

### `captureThemes`

[Исходник](../../tests/electron/studio-smoke.cjs#L71)

```typescript
async function captureThemes(name)
```

Сохраняет состояния desktop в трёх темах LESHY.

### `finish`

[Исходник](../../tests/electron/studio-smoke.cjs#L84)

```typescript
async function finish(error)
```

Пишет итог и диагностику ошибки, закрывает только тестовое приложение и HTTP fixture.

### `win.webContents.send`

[Исходник](../../tests/electron/studio-smoke.cjs#L88)

```typescript
win.webContents.send(channel, message)
```

Сохраняет настоящее approval событие изолированного Core, чтобы проверить UI preview fixture и затем восстановить реальное ожидающее подтверждение.

<a id="module-tests-electron-studio-visual-cjs"></a>

## `tests/electron/studio-visual.cjs`

Снимает реальный renderer на трёх размерах: Chat, работа IDE, tools, история, пустой поиск, ошибка и настройки.

### `BrowserWindow.prototype.show`

[Исходник](../../tests/electron/studio-visual.cjs#L7)

```typescript
BrowserWindow.prototype.show()
```

Только в smoke-тесте подавляет показ настоящего окна пользователю.

### `BrowserWindow.prototype.loadURL`

[Исходник](../../tests/electron/studio-visual.cjs#L8)

```typescript
BrowserWindow.prototype.loadURL()
```

Открывает собранный renderer вместо пользовательского Vite, изолируя GUI-проверку.

### `dialog.showOpenDialog`

[Исходник](../../tests/electron/studio-visual.cjs#L9)

```typescript
dialog.showOpenDialog()
```

Только в smoke-тесте возвращает учебный каталог вместо настоящего системного диалога.

### `dialog.showSaveDialog`

[Исходник](../../tests/electron/studio-visual.cjs#L9)

```typescript
dialog.showSaveDialog(_win, options)
```

Выбирает только тестовый путь экспорта без системного диалога пользователю.

### `dialog.showMessageBox`

[Исходник](../../tests/electron/studio-visual.cjs#L9)

```typescript
dialog.showMessageBox()
```

В Electron smoke подменяет нативное подтверждение несохранённых изменений управляемым ответом Cancel/Discard.

### `ipcMain.handle`

[Исходник](../../tests/electron/studio-visual.cjs#L17)

```typescript
ipcMain.handle(channel, handler)
```

В Electron fixture перехватывает только speech playback для проверки UI/Stop без звука; остальные IPC проходят в настоящий main.

### `releaseVisual`

[Исходник](../../tests/electron/studio-visual.cjs#L29)

```typescript
releaseVisual()
```

Освобождает удерживаемый fixture SSE после снимка состояния выполняющейся задачи.

### `done`

[Исходник](../../tests/electron/studio-visual.cjs#L51)

```typescript
done(id)
```

В локальной HTTP-фикстуре проверяет успешную квитанцию конкретного шага создания каталога, файла и patch.

### `releaseStage4`

[Исходник](../../tests/electron/studio-visual.cjs#L61)

```typescript
releaseStage4()
```

Завершает удерживаемый SSE-поток только после проверки, что закрытие подробностей не остановило задачу.

### `js`

[Исходник](../../tests/electron/studio-visual.cjs#L67)

```typescript
async function js(code)
```

Выполняет renderer-шаг, даёт React завершить обновление и добавляет код к ошибке.

### `poll`

[Исходник](../../tests/electron/studio-visual.cjs#L68)

```typescript
async function poll(expression, timeout=15000)
```

В тесте ожидает DOM-условие с ограничением времени.

### `click`

[Исходник](../../tests/electron/studio-visual.cjs#L69)

```typescript
async function click(selector)
```

Нажимает выбранный DOM-контрол через реальный renderer.

### `textButton`

[Исходник](../../tests/electron/studio-visual.cjs#L70)

```typescript
async function textButton(selector, text)
```

Находит кнопку в заданной области по точному видимому тексту.

### `input`

[Исходник](../../tests/electron/studio-visual.cjs#L71)

```typescript
async function input(selector, value)
```

Изменяет native input/textarea и посылает React input event.

### `capture`

[Исходник](../../tests/electron/studio-visual.cjs#L72)

```typescript
async function capture(name)
```

Сохраняет screenshot и геометрию основных панелей для визуальной проверки.

### `finish`

[Исходник](../../tests/electron/studio-visual.cjs#L73)

```typescript
async function finish(error)
```

Пишет итог и диагностику ошибки, закрывает только тестовое приложение и HTTP fixture.

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
