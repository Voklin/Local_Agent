# Справочник архивного эталона дизайна

Этот файл создаётся `python tools/generate_code_reference.py`. Сигнатуры и номера строк извлечены из исходников; назначения — из ручных аннотаций. Изменяйте объяснения в `tools/doc_notes.py`, затем пересоздайте справочник.

Блоки сигнатур приводятся без тела; это справочные объявления, а не самостоятельные программы.

[К руководству](../README.md)

## Оглавление модулей

- [design_reference/agent_studio_reference.py](#module-design-reference-agent-studio-reference-py)

<a id="module-design-reference-agent-studio-reference-py"></a>

## `design_reference/agent_studio_reference.py`

Архивный визуальный прототип с собственными механизмами; не импортируется рабочим main.py.

### `qss`

[Исходник](../../design_reference/agent_studio_reference.py#L21)

```python
def qss(d)
```

Строит строку Qt stylesheet для параметров темы эталона. Только архивный эталон.

### `btn`

[Исходник](../../design_reference/agent_studio_reference.py#L39)

```python
def btn(t, fn=None, tip='', primary=False)
```

Создаёт кнопку с текстом, callback и визуальными флагами. Только архивный эталон.

### `mono`

[Исходник](../../design_reference/agent_studio_reference.py#L46)

```python
def mono(size=11)
```

Создаёт моноширинный шрифт заданного размера. Только архивный эталон.

### `stream_chat`

[Исходник](../../design_reference/agent_studio_reference.py#L50)

```python
def stream_chat(cfg, msgs, on_chunk=lambda c: None, stop=lambda: False)
```

Сетевой потоковый helper модели прототипа; отдельная реализация от ModelClient. Только архивный эталон.

### `Job`

[Исходник](../../design_reference/agent_studio_reference.py#L67)

```python
class Job(QThread)
```

Фоновое Qt-задание произвольного callable в визуальном прототипе.

### `Job.__init__`

[Исходник](../../design_reference/agent_studio_reference.py#L69)

```python
def __init__(s, fn)
```

Инициализирует состояние экземпляра Job; параметры показаны в сигнатуре, назначение описано у класса.

### `Job.run`

[Исходник](../../design_reference/agent_studio_reference.py#L70)

```python
def run(s)
```

Выполняет задание/чат/цикл соответствующего класса прототипа; см. тело конкретного класса. Только архивный эталон.

### `ChatWorker`

[Исходник](../../design_reference/agent_studio_reference.py#L75)

```python
class ChatWorker(QThread)
```

Поток генерации чата в прототипе, отдельный от рабочего AgentEngine.

### `ChatWorker.__init__`

[Исходник](../../design_reference/agent_studio_reference.py#L77)

```python
def __init__(s, cfg, msgs)
```

Инициализирует состояние экземпляра ChatWorker; параметры показаны в сигнатуре, назначение описано у класса.

### `ChatWorker.run`

[Исходник](../../design_reference/agent_studio_reference.py#L78)

```python
def run(s)
```

Выполняет задание/чат/цикл соответствующего класса прототипа; см. тело конкретного класса. Только архивный эталон.

### `Runner`

[Исходник](../../design_reference/agent_studio_reference.py#L83)

```python
class Runner(QThread)
```

Собственный экспериментальный исполнитель задач эталона; его tools не являются разрешёнными tools LocalAgent.

### `Runner.__init__`

[Исходник](../../design_reference/agent_studio_reference.py#L86)

```python
def __init__(s, t, cfg, root, ctx)
```

Инициализирует состояние экземпляра Runner; параметры показаны в сигнатуре, назначение описано у класса.

### `Runner.step`

[Исходник](../../design_reference/agent_studio_reference.py#L89)

```python
def step(s)
```

Обновляет шаг экспериментальной задачи Runner. Только архивный эталон.

### `Runner.ask`

[Исходник](../../design_reference/agent_studio_reference.py#L94)

```python
def ask(s, sysm, user)
```

Обращается к модели из экспериментального Runner. Только архивный эталон.

### `Runner.tool`

[Исходник](../../design_reference/agent_studio_reference.py#L97)

```python
def tool(s, name, args, fn)
```

Диспетчер инструментов экспериментального Runner; не переносится в рабочую систему автоматически. Только архивный эталон.

### `Runner.run`

[Исходник](../../design_reference/agent_studio_reference.py#L103)

```python
def run(s)
```

Выполняет задание/чат/цикл соответствующего класса прототипа; см. тело конкретного класса. Только архивный эталон.

### `Hl`

[Исходник](../../design_reference/agent_studio_reference.py#L142)

```python
class Hl(QSyntaxHighlighter)
```

Подсветка синтаксиса редактора эталона.

### `Hl.__init__`

[Исходник](../../design_reference/agent_studio_reference.py#L143)

```python
def __init__(s, doc)
```

Инициализирует состояние экземпляра Hl; параметры показаны в сигнатуре, назначение описано у класса.

### `Hl.__init__.f`

[Исходник](../../design_reference/agent_studio_reference.py#L145)

```python
def f(c, b=False, i=False)
```

Создаёт QTextCharFormat для цвета/жирности/курсива подсветки прототипа.

### `Hl.highlightBlock`

[Исходник](../../design_reference/agent_studio_reference.py#L150)

```python
def highlightBlock(s, t)
```

Подсвечивает один текстовый блок редактора. Только архивный эталон.

### `LineNums`

[Исходник](../../design_reference/agent_studio_reference.py#L155)

```python
class LineNums(QWidget)
```

Виджет поля номеров строк редактора эталона.

### `LineNums.__init__`

[Исходник](../../design_reference/agent_studio_reference.py#L156)

```python
def __init__(s, e)
```

Инициализирует состояние экземпляра LineNums; параметры показаны в сигнатуре, назначение описано у класса.

### `LineNums.sizeHint`

[Исходник](../../design_reference/agent_studio_reference.py#L157)

```python
def sizeHint(s)
```

Возвращает рекомендуемый размер виджета номеров строк. Только архивный эталон.

### `LineNums.paintEvent`

[Исходник](../../design_reference/agent_studio_reference.py#L158)

```python
def paintEvent(s, ev)
```

Рисует виджет по событию Qt. Только архивный эталон.

### `CodeEdit`

[Исходник](../../design_reference/agent_studio_reference.py#L161)

```python
class CodeEdit(QPlainTextEdit)
```

Редактор эталона с номерами строк, подсветкой и действиями ввода.

### `CodeEdit.__init__`

[Исходник](../../design_reference/agent_studio_reference.py#L162)

```python
def __init__(s)
```

Инициализирует состояние экземпляра CodeEdit; параметры показаны в сигнатуре, назначение описано у класса.

### `CodeEdit.lnw`

[Исходник](../../design_reference/agent_studio_reference.py#L167)

```python
def lnw(s)
```

Вычисляет ширину поля номеров строк. Только архивный эталон.

### `CodeEdit.upd_w`

[Исходник](../../design_reference/agent_studio_reference.py#L168)

```python
def upd_w(s, *_)
```

Обновляет отступ редактора под номера строк. Только архивный эталон.

### `CodeEdit.upd_ln`

[Исходник](../../design_reference/agent_studio_reference.py#L169)

```python
def upd_ln(s, r, dy)
```

Обновляет область номеров строк при прокрутке/изменении. Только архивный эталон.

### `CodeEdit.resizeEvent`

[Исходник](../../design_reference/agent_studio_reference.py#L173)

```python
def resizeEvent(s, e)
```

Переразмещает поле номеров строк при изменении размера. Только архивный эталон.

### `CodeEdit.paint_ln`

[Исходник](../../design_reference/agent_studio_reference.py#L175)

```python
def paint_ln(s, ev)
```

Рисует видимые номера строк. Только архивный эталон.

### `CodeEdit.hl_line`

[Исходник](../../design_reference/agent_studio_reference.py#L181)

```python
def hl_line(s)
```

Подсвечивает текущую строку редактора. Только архивный эталон.

### `CodeEdit.keyPressEvent`

[Исходник](../../design_reference/agent_studio_reference.py#L188)

```python
def keyPressEvent(s, e)
```

Обрабатывает ввод клавиатуры виджета эталона. Только архивный эталон.

### `CodeEdit.ins_comp`

[Исходник](../../design_reference/agent_studio_reference.py#L196)

```python
def ins_comp(s, t)
```

Вставляет выбранное дополнение текста. Только архивный эталон.

### `ClickText`

[Исходник](../../design_reference/agent_studio_reference.py#L200)

```python
class ClickText(QTextEdit)
```

Текстовый виджет с обработкой двойного щелчка.

### `ClickText.mouseDoubleClickEvent`

[Исходник](../../design_reference/agent_studio_reference.py#L202)

```python
def mouseDoubleClickEvent(s, e)
```

Обрабатывает двойной щелчок по тексту. Только архивный эталон.

### `Inp`

[Исходник](../../design_reference/agent_studio_reference.py#L208)

```python
class Inp(QPlainTextEdit)
```

Поле ввода с собственной обработкой клавиш.

### `Inp.keyPressEvent`

[Исходник](../../design_reference/agent_studio_reference.py#L210)

```python
def keyPressEvent(s, e)
```

Обрабатывает ввод клавиатуры виджета эталона. Только архивный эталон.

### `DiffDlg`

[Исходник](../../design_reference/agent_studio_reference.py#L215)

```python
class DiffDlg(QDialog)
```

Диалог сравнения изменений в эталоне.

### `DiffDlg.__init__`

[Исходник](../../design_reference/agent_studio_reference.py#L216)

```python
def __init__(s, path, old, new, warn='', pending=True)
```

Инициализирует состояние экземпляра DiffDlg; параметры показаны в сигнатуре, назначение описано у класса.

### `DiffDlg.go`

[Исходник](../../design_reference/agent_studio_reference.py#L247)

```python
def go(s, d)
```

Переходит к выбранному фрагменту diff. Только архивный эталон.

### `Palette`

[Исходник](../../design_reference/agent_studio_reference.py#L253)

```python
class Palette(QDialog)
```

Палитра команд эталонного интерфейса.

### `Palette.__init__`

[Исходник](../../design_reference/agent_studio_reference.py#L254)

```python
def __init__(s, cmds, parent)
```

Инициализирует состояние экземпляра Palette; параметры показаны в сигнатуре, назначение описано у класса.

### `Palette.fill`

[Исходник](../../design_reference/agent_studio_reference.py#L258)

```python
def fill(s, t)
```

Заполняет список палитры команд. Только архивный эталон.

### `Palette.run`

[Исходник](../../design_reference/agent_studio_reference.py#L261)

```python
def run(s)
```

Выполняет задание/чат/цикл соответствующего класса прототипа; см. тело конкретного класса. Только архивный эталон.

### `Main`

[Исходник](../../design_reference/agent_studio_reference.py#L266)

```python
class Main(QMainWindow)
```

Главное окно большого архивного прототипа; не импортируется production-путём проекта.

### `Main.__init__`

[Исходник](../../design_reference/agent_studio_reference.py#L267)

```python
def __init__(s)
```

Инициализирует состояние экземпляра Main; параметры показаны в сигнатуре, назначение описано у класса.

### `Main.data`

[Исходник](../../design_reference/agent_studio_reference.py#L280)

```python
def data(s)
```

Формирует путь служебных данных прототипа. Только архивный эталон.

### `Main.jload`

[Исходник](../../design_reference/agent_studio_reference.py#L282)

```python
def jload(s, n, dflt)
```

Загружает JSON прототипа с fallback. Только архивный эталон.

### `Main.jsave`

[Исходник](../../design_reference/agent_studio_reference.py#L285)

```python
def jsave(s, n, o)
```

Сохраняет JSON прототипа. Только архивный эталон.

### `Main.save_cfg`

[Исходник](../../design_reference/agent_studio_reference.py#L288)

```python
def save_cfg(s)
```

Сохраняет конфигурацию прототипа. Только архивный эталон.

### `Main.log`

[Исходник](../../design_reference/agent_studio_reference.py#L291)

```python
def log(s, lvl, msg)
```

Добавляет сообщение в диагностический вывод. Только архивный эталон.

### `Main.show_logs`

[Исходник](../../design_reference/agent_studio_reference.py#L293)

```python
def show_logs(s)
```

Показывает сохранённые диагностические сообщения. Только архивный эталон.

### `Main.toast`

[Исходник](../../design_reference/agent_studio_reference.py#L295)

```python
def toast(s, msg, err=False)
```

Показывает краткое уведомление. Только архивный эталон.

### `Main.job`

[Исходник](../../design_reference/agent_studio_reference.py#L299)

```python
def job(s, fn, ok, err=None)
```

Запускает действие через фоновый Job. Только архивный эталон.

### `Main.busy`

[Исходник](../../design_reference/agent_studio_reference.py#L302)

```python
def busy(s, on)
```

Меняет состояние занятости UI. Только архивный эталон.

### `Main.build`

[Исходник](../../design_reference/agent_studio_reference.py#L305)

```python
def build(s)
```

Собирает виджеты и панели главного окна эталона. Только архивный эталон.

### `Main.bind_keys`

[Исходник](../../design_reference/agent_studio_reference.py#L338)

```python
def bind_keys(s)
```

Подключает клавиатурные действия прототипа. Только архивный эталон.

### `Main.show_side`

[Исходник](../../design_reference/agent_studio_reference.py#L345)

```python
def show_side(s, i)
```

Переключает боковую страницу. Только архивный эталон.

### `Main.side_box`

[Исходник](../../design_reference/agent_studio_reference.py#L351)

```python
def side_box(s, title)
```

Создаёт контейнер боковой страницы. Только архивный эталон.

### `Main.pg_files`

[Исходник](../../design_reference/agent_studio_reference.py#L355)

```python
def pg_files(s)
```

Создаёт страницу проводника. Только архивный эталон.

### `Main.filter_files`

[Исходник](../../design_reference/agent_studio_reference.py#L364)

```python
def filter_files(s)
```

Фильтрует видимые файлы. Только архивный эталон.

### `Main.tree_menu`

[Исходник](../../design_reference/agent_studio_reference.py#L366)

```python
def tree_menu(s, pos)
```

Показывает контекстное меню дерева. Только архивный эталон.

### `Main.fs_new`

[Исходник](../../design_reference/agent_studio_reference.py#L375)

```python
def fs_new(s, base, folder)
```

Создаёт файловый объект средствами эталона; не доступно текущему Electron tool API. Только архивный эталон.

### `Main.fs_rename`

[Исходник](../../design_reference/agent_studio_reference.py#L380)

```python
def fs_rename(s, p)
```

Переименовывает файловый объект средствами эталона. Только архивный эталон.

### `Main.fs_delete`

[Исходник](../../design_reference/agent_studio_reference.py#L385)

```python
def fs_delete(s, p)
```

Удаляет файловый объект средствами эталона; не часть рабочих tools LocalAgent. Только архивный эталон.

### `Main.pg_search`

[Исходник](../../design_reference/agent_studio_reference.py#L395)

```python
def pg_search(s)
```

Создаёт страницу поиска. Только архивный эталон.

### `Main.do_search`

[Исходник](../../design_reference/agent_studio_reference.py#L399)

```python
def do_search(s)
```

Выполняет поиск в прототипе. Только архивный эталон.

### `Main.do_search.f`

[Исходник](../../design_reference/agent_studio_reference.py#L403)

```python
def f()
```

Фоновый обход и поиск текстовых совпадений в файлах эталона.

### `Main.do_search.ok`

[Исходник](../../design_reference/agent_studio_reference.py#L416)

```python
def ok(res)
```

Отображает найденные пути/строки и снимает busy-состояние эталона.

### `Main.pg_agents`

[Исходник](../../design_reference/agent_studio_reference.py#L424)

```python
def pg_agents(s)
```

Создаёт страницу задач/агентов прототипа. Только архивный эталон.

### `Main.refresh_tasks`

[Исходник](../../design_reference/agent_studio_reference.py#L427)

```python
def refresh_tasks(s)
```

Обновляет список экспериментальных задач. Только архивный эталон.

### `Main.pick_task`

[Исходник](../../design_reference/agent_studio_reference.py#L434)

```python
def pick_task(s)
```

Выбирает задачу из списка. Только архивный эталон.

### `Main.new_task`

[Исходник](../../design_reference/agent_studio_reference.py#L438)

```python
def new_task(s)
```

Создаёт экспериментальную задачу. Только архивный эталон.

### `Main.pg_chats`

[Исходник](../../design_reference/agent_studio_reference.py#L447)

```python
def pg_chats(s)
```

Создаёт страницу чатов. Только архивный эталон.

### `Main.chat_menu`

[Исходник](../../design_reference/agent_studio_reference.py#L450)

```python
def chat_menu(s, pos)
```

Показывает меню действий над чатом. Только архивный эталон.

### `Main.refresh_chats`

[Исходник](../../design_reference/agent_studio_reference.py#L453)

```python
def refresh_chats(s)
```

Обновляет список чатов прототипа. Только архивный эталон.

### `Main.new_chat`

[Исходник](../../design_reference/agent_studio_reference.py#L457)

```python
def new_chat(s)
```

Создаёт новый чат прототипа. Только архивный эталон.

### `Main.pick_chat`

[Исходник](../../design_reference/agent_studio_reference.py#L459)

```python
def pick_chat(s, i)
```

Открывает выбранный чат. Только архивный эталон.

### `Main.rename_chat`

[Исходник](../../design_reference/agent_studio_reference.py#L461)

```python
def rename_chat(s)
```

Переименовывает чат прототипа. Только архивный эталон.

### `Main.delete_chat`

[Исходник](../../design_reference/agent_studio_reference.py#L464)

```python
def delete_chat(s)
```

Удаляет чат прототипа. Только архивный эталон.

### `Main.pg_models`

[Исходник](../../design_reference/agent_studio_reference.py#L469)

```python
def pg_models(s)
```

Создаёт страницу модели и локального runtime. Только архивный эталон.

### `Main.set_cfg`

[Исходник](../../design_reference/agent_studio_reference.py#L485)

```python
def set_cfg(s, k, v)
```

Меняет поле конфигурации прототипа. Только архивный эталон.

### `Main.prov_changed`

[Исходник](../../design_reference/agent_studio_reference.py#L486)

```python
def prov_changed(s, p)
```

Обновляет настройки при смене провайдера. Только архивный эталон.

### `Main.set_model`

[Исходник](../../design_reference/agent_studio_reference.py#L487)

```python
def set_model(s, m)
```

Выбирает ID модели. Только архивный эталон.

### `Main.fetch_models`

[Исходник](../../design_reference/agent_studio_reference.py#L488)

```python
def fetch_models(s)
```

Запрашивает список моделей для прототипа. Только архивный эталон.

### `Main.fetch_models.f`

[Исходник](../../design_reference/agent_studio_reference.py#L490)

```python
def f()
```

HTTP GET /models в отдельной фоновой задаче прототипа.

### `Main.fetch_models.ok`

[Исходник](../../design_reference/agent_studio_reference.py#L493)

```python
def ok(ms)
```

Обновляет список ID, статус соединения и начальный выбор модели эталона.

### `Main.import_gguf`

[Исходник](../../design_reference/agent_studio_reference.py#L497)

```python
def import_gguf(s)
```

Импортирует GGUF через UI эталона. Только архивный эталон.

### `Main.refresh_gguf`

[Исходник](../../design_reference/agent_studio_reference.py#L502)

```python
def refresh_gguf(s)
```

Обновляет отображаемый список GGUF. Только архивный эталон.

### `Main.start_gguf`

[Исходник](../../design_reference/agent_studio_reference.py#L507)

```python
def start_gguf(s)
```

Запускает локальный runtime прототипа. Только архивный эталон.

### `Main.stop_gguf`

[Исходник](../../design_reference/agent_studio_reference.py#L517)

```python
def stop_gguf(s)
```

Останавливает локальный runtime прототипа. Только архивный эталон.

### `Main.resources`

[Исходник](../../design_reference/agent_studio_reference.py#L519)

```python
def resources(s)
```

Обновляет сведения о ресурсах. Только архивный эталон.

### `Main.resources.f`

[Исходник](../../design_reference/agent_studio_reference.py#L520)

```python
def f()
```

Получает RAM через необязательный psutil и VRAM через nvidia-smi в прототипе.

### `Main.pg_skills`

[Исходник](../../design_reference/agent_studio_reference.py#L531)

```python
def pg_skills(s)
```

Создаёт страницу навыков. Только архивный эталон.

### `Main.refresh_skills`

[Исходник](../../design_reference/agent_studio_reference.py#L537)

```python
def refresh_skills(s)
```

Обновляет список навыков прототипа. Только архивный эталон.

### `Main.skill_toggle`

[Исходник](../../design_reference/agent_studio_reference.py#L545)

```python
def skill_toggle(s, it, _)
```

Переключает состояние навыка в прототипе. Только архивный эталон.

### `Main.skill_desc`

[Исходник](../../design_reference/agent_studio_reference.py#L547)

```python
def skill_desc(s, it, _)
```

Показывает описание выбранного навыка. Только архивный эталон.

### `Main.skills_text`

[Исходник](../../design_reference/agent_studio_reference.py#L550)

```python
def skills_text(s)
```

Собирает текст включённых навыков прототипа. Только архивный эталон.

### `Main.refresh_mcp`

[Исходник](../../design_reference/agent_studio_reference.py#L556)

```python
def refresh_mcp(s)
```

Обновляет список MCP-конфигураций эталона. Только архивный эталон.

### `Main.mcp_toggle`

[Исходник](../../design_reference/agent_studio_reference.py#L564)

```python
def mcp_toggle(s, it, _)
```

Переключает флаг MCP-конфигурации. Только архивный эталон.

### `Main.mcp_add`

[Исходник](../../design_reference/agent_studio_reference.py#L569)

```python
def mcp_add(s)
```

Добавляет MCP-конфигурацию в UI прототипа. Только архивный эталон.

### `Main.mcp_del`

[Исходник](../../design_reference/agent_studio_reference.py#L574)

```python
def mcp_del(s)
```

Удаляет MCP-конфигурацию прототипа. Только архивный эталон.

### `Main.mcp_connect`

[Исходник](../../design_reference/agent_studio_reference.py#L577)

```python
def mcp_connect(s)
```

Обрабатывает действие подключения MCP в эталоне; не доказывает наличие транспорта в рабочем MCPRegistry. Только архивный эталон.

### `Main.mcp_connect.f`

[Исходник](../../design_reference/agent_studio_reference.py#L581)

```python
def f()
```

Экспериментально запускает subprocess и MCP initialize/tools/list в эталоне; не подключено к рабочему MCPRegistry.

### `Main.mcp_connect.f.rpc`

[Исходник](../../design_reference/agent_studio_reference.py#L583)

```python
def rpc(o)
```

Пишет JSON-RPC объект одной строкой в stdin экспериментального MCP-процесса эталона.

### `Main.mcp_connect.ok`

[Исходник](../../design_reference/agent_studio_reference.py#L591)

```python
def ok(tools)
```

Сохраняет список tools и состояние MCP-подключения прототипа.

### `Main.mcp_connect.bad`

[Исходник](../../design_reference/agent_studio_reference.py#L593)

```python
def bad(e)
```

Показывает ошибку экспериментального MCP-подключения эталона.

### `Main.pg_memory`

[Исходник](../../design_reference/agent_studio_reference.py#L597)

```python
def pg_memory(s)
```

Создаёт страницу памяти проекта прототипа. Только архивный эталон.

### `Main.mem_path`

[Исходник](../../design_reference/agent_studio_reference.py#L600)

```python
def mem_path(s)
```

Определяет путь памяти прототипа. Только архивный эталон.

### `Main.mem_load`

[Исходник](../../design_reference/agent_studio_reference.py#L601)

```python
def mem_load(s)
```

Загружает память прототипа. Только архивный эталон.

### `Main.mem_save`

[Исходник](../../design_reference/agent_studio_reference.py#L604)

```python
def mem_save(s)
```

Сохраняет память из UI прототипа. Только архивный эталон.

### `Main.mem_clear`

[Исходник](../../design_reference/agent_studio_reference.py#L605)

```python
def mem_clear(s)
```

Очищает память прототипа. Только архивный эталон.

### `Main.pg_settings`

[Исходник](../../design_reference/agent_studio_reference.py#L609)

```python
def pg_settings(s)
```

Создаёт страницу настроек. Только архивный эталон.

### `Main.apply_theme`

[Исходник](../../design_reference/agent_studio_reference.py#L622)

```python
def apply_theme(s)
```

Применяет stylesheet выбранной темы. Только архивный эталон.

### `Main.toggle_theme`

[Исходник](../../design_reference/agent_studio_reference.py#L623)

```python
def toggle_theme(s)
```

Переключает тему. Только архивный эталон.

### `Main.apply_editor_prefs`

[Исходник](../../design_reference/agent_studio_reference.py#L624)

```python
def apply_editor_prefs(s)
```

Применяет настройки редактора. Только архивный эталон.

### `Main.bottom`

[Исходник](../../design_reference/agent_studio_reference.py#L629)

```python
def bottom(s)
```

Переключает нижнюю панель прототипа. Только архивный эталон.

### `Main.run_cmd`

[Исходник](../../design_reference/agent_studio_reference.py#L640)

```python
def run_cmd(s, c)
```

Запускает команду средствами эталона; рабочий агент такого tool не имеет. Только архивный эталон.

### `Main.cmd_done`

[Исходник](../../design_reference/agent_studio_reference.py#L650)

```python
def cmd_done(s, code, *_)
```

Обрабатывает завершение команды прототипа. Только архивный эталон.

### `Main.stop_cmd`

[Исходник](../../design_reference/agent_studio_reference.py#L653)

```python
def stop_cmd(s)
```

Останавливает команду прототипа. Только архивный эталон.

### `Main.findbar`

[Исходник](../../design_reference/agent_studio_reference.py#L657)

```python
def findbar(s)
```

Создаёт панель поиска в редакторе. Только архивный эталон.

### `Main.ed`

[Исходник](../../design_reference/agent_studio_reference.py#L663)

```python
def ed(s)
```

Получает текущий редактор. Только архивный эталон.

### `Main.toggle_find`

[Исходник](../../design_reference/agent_studio_reference.py#L664)

```python
def toggle_find(s)
```

Переключает панель поиска/замены. Только архивный эталон.

### `Main.find`

[Исходник](../../design_reference/agent_studio_reference.py#L665)

```python
def find(s, back)
```

Ищет текст в редакторе. Только архивный эталон.

### `Main.replace1`

[Исходник](../../design_reference/agent_studio_reference.py#L672)

```python
def replace1(s)
```

Заменяет одно совпадение в редакторе. Только архивный эталон.

### `Main.replace_all`

[Исходник](../../design_reference/agent_studio_reference.py#L676)

```python
def replace_all(s)
```

Заменяет все совпадения в редакторе. Только архивный эталон.

### `Main.goto_line`

[Исходник](../../design_reference/agent_studio_reference.py#L682)

```python
def goto_line(s, n=None)
```

Переходит к заданной строке. Только архивный эталон.

### `Main.open_file`

[Исходник](../../design_reference/agent_studio_reference.py#L688)

```python
def open_file(s, path, line=None)
```

Открывает файл во вкладке редактора эталона. Только архивный эталон.

### `Main.sync_stack`

[Исходник](../../design_reference/agent_studio_reference.py#L698)

```python
def sync_stack(s)
```

Согласует стек редакторов и вкладки. Только архивный эталон.

### `Main.tab_mod`

[Исходник](../../design_reference/agent_studio_reference.py#L699)

```python
def tab_mod(s, e)
```

Обновляет индикатор изменения вкладки. Только архивный эталон.

### `Main.pos_status`

[Исходник](../../design_reference/agent_studio_reference.py#L701)

```python
def pos_status(s, *_)
```

Обновляет строку состояния позиции курсора. Только архивный эталон.

### `Main.save`

[Исходник](../../design_reference/agent_studio_reference.py#L703)

```python
def save(s, e=None)
```

Сохраняет открытый документ эталона. Только архивный эталон.

### `Main.close_tab`

[Исходник](../../design_reference/agent_studio_reference.py#L708)

```python
def close_tab(s, i)
```

Закрывает вкладку редактора. Только архивный эталон.

### `Main.diagnose`

[Исходник](../../design_reference/agent_studio_reference.py#L714)

```python
def diagnose(s)
```

Выполняет диагностическое действие прототипа. Только архивный эталон.

### `Main.chat_panel`

[Исходник](../../design_reference/agent_studio_reference.py#L725)

```python
def chat_panel(s)
```

Собирает чат-панель эталона. Только архивный эталон.

### `Main.render_chat`

[Исходник](../../design_reference/agent_studio_reference.py#L731)

```python
def render_chat(s)
```

Отображает сообщения прототипа. Только архивный эталон.

### `Main.sys_prompt`

[Исходник](../../design_reference/agent_studio_reference.py#L736)

```python
def sys_prompt(s)
```

Формирует system prompt прототипа. Только архивный эталон.

### `Main.send`

[Исходник](../../design_reference/agent_studio_reference.py#L739)

```python
def send(s, text=None)
```

Отправляет пользовательский запрос прототипа. Только архивный эталон.

### `Main.on_chunk`

[Исходник](../../design_reference/agent_studio_reference.py#L749)

```python
def on_chunk(s, ch)
```

Отображает полученный текстовый фрагмент. Только архивный эталон.

### `Main.gen_end`

[Исходник](../../design_reference/agent_studio_reference.py#L750)

```python
def gen_end(s)
```

Завершает состояние генерации в UI. Только архивный эталон.

### `Main.on_done`

[Исходник](../../design_reference/agent_studio_reference.py#L751)

```python
def on_done(s, _)
```

Обрабатывает успешное завершение фоновой генерации. Только архивный эталон.

### `Main.on_fail`

[Исходник](../../design_reference/agent_studio_reference.py#L752)

```python
def on_fail(s, e)
```

Обрабатывает ошибку фоновой генерации. Только архивный эталон.

### `Main.stop_gen`

[Исходник](../../design_reference/agent_studio_reference.py#L754)

```python
def stop_gen(s)
```

Запрашивает остановку генерации прототипа. Только архивный эталон.

### `Main.copy_last`

[Исходник](../../design_reference/agent_studio_reference.py#L756)

```python
def copy_last(s)
```

Копирует последний ответ. Только архивный эталон.

### `Main.resend`

[Исходник](../../design_reference/agent_studio_reference.py#L759)

```python
def resend(s)
```

Повторяет запрос/генерацию прототипа. Только архивный эталон.

### `Main.task_panel`

[Исходник](../../design_reference/agent_studio_reference.py#L766)

```python
def task_panel(s)
```

Создаёт подробную панель экспериментальной задачи. Только архивный эталон.

### `Main.show_task`

[Исходник](../../design_reference/agent_studio_reference.py#L778)

```python
def show_task(s)
```

Отображает выбранную задачу. Только архивный эталон.

### `Main.start_task`

[Исходник](../../design_reference/agent_studio_reference.py#L793)

```python
def start_task(s)
```

Запускает экспериментальный Runner. Только архивный эталон.

### `Main.on_task_changed`

[Исходник](../../design_reference/agent_studio_reference.py#L799)

```python
def on_task_changed(s)
```

Обновляет UI после изменения задачи. Только архивный эталон.

### `Main.pause_resume`

[Исходник](../../design_reference/agent_studio_reference.py#L802)

```python
def pause_resume(s)
```

Переключает паузу/продолжение экспериментальной задачи. Только архивный эталон.

### `Main.cancel_task`

[Исходник](../../design_reference/agent_studio_reference.py#L812)

```python
def cancel_task(s)
```

Запрашивает отмену экспериментальной задачи. Только архивный эталон.

### `Main.rerun_task`

[Исходник](../../design_reference/agent_studio_reference.py#L817)

```python
def rerun_task(s)
```

Повторно запускает задачу прототипа. Только архивный эталон.

### `Main.restore_cp`

[Исходник](../../design_reference/agent_studio_reference.py#L821)

```python
def restore_cp(s)
```

Восстанавливает экспериментальный checkpoint. Только архивный эталон.

### `Main.review`

[Исходник](../../design_reference/agent_studio_reference.py#L827)

```python
def review(s, i)
```

Показывает просмотр предлагаемых изменений эталона. Только архивный эталон.

### `Main.final_diff`

[Исходник](../../design_reference/agent_studio_reference.py#L846)

```python
def final_diff(s)
```

Собирает итоговый diff прототипа. Только архивный эталон.

### `Main.tick`

[Исходник](../../design_reference/agent_studio_reference.py#L853)

```python
def tick(s)
```

Периодически обновляет состояние UI. Только архивный эталон.

### `Main.open_project`

[Исходник](../../design_reference/agent_studio_reference.py#L857)

```python
def open_project(s)
```

Выбирает каталог проекта прототипа. Только архивный эталон.

### `Main.new_project`

[Исходник](../../design_reference/agent_studio_reference.py#L860)

```python
def new_project(s)
```

Создаёт учебный проект средствами эталона. Только архивный эталон.

### `Main.load_project`

[Исходник](../../design_reference/agent_studio_reference.py#L866)

```python
def load_project(s)
```

Переключает загруженный проект прототипа. Только архивный эталон.

### `Main.restore`

[Исходник](../../design_reference/agent_studio_reference.py#L879)

```python
def restore(s)
```

Восстанавливает сохранённое состояние окна прототипа. Только архивный эталон.

### `Main.closeEvent`

[Исходник](../../design_reference/agent_studio_reference.py#L887)

```python
def closeEvent(s, ev)
```

Сохраняет состояние и закрывает ресурсы эталона. Только архивный эталон.
