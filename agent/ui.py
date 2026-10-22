from pathlib import Path
from html import escape

from PySide6.QtCore import Qt, QSettings
from PySide6.QtGui import QFont, QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QToolButton, QFrame, QSplitter, QTreeWidget, QTreeWidgetItem,
    QTextBrowser, QPlainTextEdit, QFileDialog, QLineEdit, QComboBox,
    QMessageBox, QDialog, QDialogButtonBox, QFormLayout, QSpinBox, QCheckBox,
    QListWidget, QListWidgetItem, QStackedWidget, QTabWidget
)
from openai import OpenAI

from .worker import AgentWorker, DEFAULT_SETTINGS
from .chat_store import list_chats, create_chat, load_chat, save_chat, delete_chat, rename_chat, title_from_messages
from .project_memory import load_project_memory
from .task_store import load_task
from .security import resolve_allowed_path, AccessDenied


STYLE = """
* { font-family: 'Segoe UI', 'Inter', sans-serif; font-size: 12px; }
QMainWindow, QWidget { background:#1e1f22; color:#dfe1e5; }
QFrame#Top { background:#252629; border-bottom:1px solid #3c3f45; }
QFrame#Activity { background:#252629; border-right:1px solid #3c3f45; }
QFrame#Side { background:#232427; border-right:1px solid #3c3f45; }
QFrame#Bottom { background:#252629; border-top:1px solid #3c3f45; }
QLabel#Brand { font-size:14px; font-weight:700; }
QLabel#Muted { color:#92959e; }
QLabel#Heading { font-size:18px; font-weight:650; }
QLabel#Status { color:#b9d4ff; background:#26344b; border:1px solid #354d70; border-radius:9px; padding:5px 10px; }
QPushButton, QToolButton { background:#2b2d30; border:1px solid #41434a; border-radius:6px; padding:7px 10px; }
QPushButton:hover, QToolButton:hover { background:#393b40; }
QPushButton#Primary { background:#4f8cff; color:white; border:0; font-weight:650; }
QPushButton#Primary:hover { background:#6a9dff; }
QPushButton#Primary:disabled { background:#343b48; color:#858b96; }
QToolButton#Nav { background:transparent; border:0; color:#aeb1bb; padding:10px 4px; min-height:36px; font-size:17px; }
QToolButton#Nav:checked { background:#34363d; color:#ffffff; border-left:3px solid #4f8cff; }
QLineEdit, QComboBox, QSpinBox, QPlainTextEdit { background:#1a1b1e; border:1px solid #3c3f45; border-radius:7px; padding:7px; selection-background-color:#365b95; }
QComboBox QAbstractItemView { background:#2b2d30; selection-background-color:#365b95; }
QTextBrowser { background:transparent; border:0; padding:12px; }
QTreeWidget, QListWidget { background:transparent; border:0; outline:0; }
QTreeWidget::item, QListWidget::item { padding:7px; border-radius:5px; }
QTreeWidget::item:selected, QListWidget::item:selected { background:#34363d; }
QTabWidget::pane { border:1px solid #3c3f45; border-radius:5px; }
QTabBar::tab { background:#252629; color:#aeb1bb; padding:8px 14px; border-right:1px solid #3c3f45; }
QTabBar::tab:selected { background:#1e1f22; color:#ffffff; border-bottom:2px solid #4f8cff; }
QSplitter::handle { background:#3c3f45; }
QScrollBar:vertical { background:transparent; width:8px; } QScrollBar::handle:vertical { background:#484b53; border-radius:4px; }
"""

class ApprovalDialog(QDialog):
    def __init__(self, path, diff, exists, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Подтверждение изменения")
        self.resize(760, 520)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(("Изменить файл: " if exists else "Создать файл: ") + path))
        view = QPlainTextEdit(); view.setReadOnly(True); view.setPlainText(diff or "(diff отсутствует)")
        view.setFont(QFont("Consolas", 10)); layout.addWidget(view, 1)
        buttons = QDialogButtonBox()
        apply_btn = buttons.addButton("Применить", QDialogButtonBox.ButtonRole.AcceptRole)
        reject_btn = buttons.addButton("Отклонить", QDialogButtonBox.ButtonRole.DestructiveRole)
        cancel_btn = buttons.addButton("Отмена", QDialogButtonBox.ButtonRole.RejectRole)
        apply_btn.clicked.connect(lambda: self.done(1))
        reject_btn.clicked.connect(lambda: self.done(2))
        cancel_btn.clicked.connect(lambda: self.done(0))
        layout.addWidget(buttons)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Local Coding Agent")
        self.resize(1440, 900); self.setMinimumSize(1000, 650)
        self.setStyleSheet(STYLE)
        self.settings = QSettings("LocalCodingAgent", "LocalCodingAgent")
        self.worker = None
        self.project_root = str(self.settings.value("project/root", str(Path.home())))
        self.chat_id = None
        self.chat_title = "Новый чат"
        self.history = []
        self.current_view = "Agent"
        self._build()
        self._load_connection()
        self._refresh_tree()
        self._refresh_chats()
        self._refresh_models()
        self._load_saved_chat()
        self._bind_shortcuts()
        self.status_label.setText("Готов")

    def _build(self):
        central = QWidget(); self.setCentralWidget(central)
        outer = QVBoxLayout(central); outer.setContentsMargins(0,0,0,0); outer.setSpacing(0)
        top = QFrame(); top.setObjectName("Top"); top_l = QHBoxLayout(top); top_l.setContentsMargins(14,8,14,8)
        brand = QLabel("◈  Agent Studio  /  Local Coding Agent"); brand.setObjectName("Brand"); top_l.addWidget(brand)
        self.project_btn = QPushButton("📂  " + Path(self.project_root).name); self.project_btn.clicked.connect(self._choose_project); top_l.addWidget(self.project_btn)
        top_l.addStretch(1)
        self.model_combo = QComboBox(); self.model_combo.setMinimumWidth(190); top_l.addWidget(self.model_combo)
        self.connection_btn = QPushButton("Подключение"); self.connection_btn.clicked.connect(self._connection_dialog); top_l.addWidget(self.connection_btn)
        self.status_label = QLabel("Загрузка…"); self.status_label.setObjectName("Status"); top_l.addWidget(self.status_label)
        outer.addWidget(top)

        body = QSplitter(Qt.Orientation.Horizontal); body.setChildrenCollapsible(False)
        activity = QFrame(); activity.setObjectName("Activity"); activity.setFixedWidth(62)
        av = QVBoxLayout(activity); av.setContentsMargins(5,10,5,8); av.setSpacing(5)
        self.nav_buttons = {}
        for key, glyph in [("Explorer","📁"),("Search","⌕"),("Agent","✦"),("History","◷"),("Models","⚙")]:
            b = QToolButton(); b.setObjectName("Nav"); b.setText(glyph); b.setToolTip(key); b.setCheckable(True)
            b.clicked.connect(lambda checked=False, k=key: self._switch_view(k))
            av.addWidget(b); self.nav_buttons[key] = b
        av.addStretch(1); body.addWidget(activity)

        self.sidebar = QFrame(); self.sidebar.setObjectName("Side"); self.sidebar.setMinimumWidth(190); self.sidebar.setMaximumWidth(360)
        sv = QVBoxLayout(self.sidebar); sv.setContentsMargins(12,12,12,12)
        self.side_title = QLabel("EXPLORER"); self.side_title.setObjectName("Muted"); sv.addWidget(self.side_title)
        self.side_stack = QStackedWidget()
        self.tree = QTreeWidget(); self.tree.setHeaderHidden(True); self.tree.itemDoubleClicked.connect(self._open_tree_item)
        self.side_stack.addWidget(self.tree)
        search_page = QWidget(); search_l = QVBoxLayout(search_page); self.search_input = QLineEdit(); self.search_input.setPlaceholderText("Поиск по имени файла")
        self.search_input.textChanged.connect(self._filter_tree); search_l.addWidget(self.search_input)
        self.search_results = QListWidget(); self.search_results.itemDoubleClicked.connect(self._open_search_item); search_l.addWidget(self.search_results,1)
        self.side_stack.addWidget(search_page)
        self.chat_list = QListWidget(); self.chat_list.itemDoubleClicked.connect(self._open_chat_item); self.side_stack.addWidget(self.chat_list)
        models_page = QWidget(); ml = QVBoxLayout(models_page)
        ml.addWidget(QLabel("Подключённая модель"))
        self.models_info = QLabel("Модели загружаются через OpenAI-compatible API.\nВстроенный GGUF runtime будет подключён отдельным этапом.")
        self.models_info.setWordWrap(True); self.models_info.setObjectName("Muted"); ml.addWidget(self.models_info)
        refresh = QPushButton("Обновить модели"); refresh.clicked.connect(self._refresh_models); ml.addWidget(refresh); ml.addStretch(1)
        self.side_stack.addWidget(models_page)
        sv.addWidget(self.side_stack,1); body.addWidget(self.sidebar)

        center = QWidget(); cv = QVBoxLayout(center); cv.setContentsMargins(0,0,0,0); cv.setSpacing(0)
        self.workspace_header = QFrame(); self.workspace_header.setObjectName("Top")
        wh = QHBoxLayout(self.workspace_header); wh.setContentsMargins(18,10,18,10)
        self.workspace_title = QLabel("Agent"); self.workspace_title.setObjectName("Heading"); wh.addWidget(self.workspace_title)
        wh.addStretch(1)
        self.new_chat_btn = QPushButton("+ Новый чат"); self.new_chat_btn.clicked.connect(self._new_chat); wh.addWidget(self.new_chat_btn)
        self.open_folder_btn = QPushButton("Открыть папку"); self.open_folder_btn.clicked.connect(self._choose_project); wh.addWidget(self.open_folder_btn)
        cv.addWidget(self.workspace_header)
        self.center_stack = QStackedWidget()
        agent_page = QWidget(); al = QVBoxLayout(agent_page); al.setContentsMargins(0,0,0,0)
        self.chat_view = QTextBrowser(); self.chat_view.setOpenExternalLinks(True); al.addWidget(self.chat_view,1)
        self.welcome = QLabel("Опишите задачу — агент изучит проект и предложит действия.\nИзменения файлов по-прежнему требуют подтверждения.")
        self.welcome.setAlignment(Qt.AlignmentFlag.AlignCenter); self.welcome.setObjectName("Muted"); al.addWidget(self.welcome)
        self.center_stack.addWidget(agent_page)
        self.editor_placeholder = QWidget(); ep = QVBoxLayout(self.editor_placeholder); ep.setContentsMargins(10,10,10,10); ep.setSpacing(0)
        self.editor_hint = QLabel("ПРОЕКТ  ·  ПРОСМОТР ФАЙЛОВ")
        self.editor_hint.setObjectName("Muted"); self.editor_hint.setContentsMargins(8,5,8,8); ep.addWidget(self.editor_hint)
        self.file_tabs = QTabWidget(); self.file_tabs.setTabsClosable(True); self.file_tabs.tabCloseRequested.connect(self._close_preview_tab)
        self.file_tabs.setDocumentMode(True); self.file_tabs.setMovable(True)
        ep.addWidget(self.file_tabs,1); self.center_stack.addWidget(self.editor_placeholder)
        self.center_stack.addWidget(self._make_simple_page("Поиск", "Поиск по именам файлов проекта доступен в боковой панели."))
        cv.addWidget(self.center_stack,1)

        bottom = QFrame(); bottom.setObjectName("Bottom"); bl = QVBoxLayout(bottom); bl.setContentsMargins(16,12,16,12)
        self.prompt = QPlainTextEdit(); self.prompt.setPlaceholderText("Опишите задачу для агента…  Enter — отправить · Shift+Enter — новая строка")
        self.prompt.setFixedHeight(94); self.prompt.setMaximumHeight(150); bl.addWidget(self.prompt)
        row = QHBoxLayout()
        self.log_btn = QPushButton("⌄  Вывод"); self.log_btn.clicked.connect(self._show_output); row.addWidget(self.log_btn)
        self.output = QPlainTextEdit(); self.output.setReadOnly(True); self.output.setMaximumHeight(95); self.output.hide()
        row.addStretch(1)
        self.stop_btn = QPushButton("■  Остановить"); self.stop_btn.setEnabled(False); self.stop_btn.clicked.connect(self._stop_agent); row.addWidget(self.stop_btn)
        self.send_btn = QPushButton("↑  Отправить"); self.send_btn.setObjectName("Primary"); self.send_btn.clicked.connect(self._send); row.addWidget(self.send_btn)
        bl.addLayout(row); bl.addWidget(self.output)
        cv.addWidget(bottom)
        body.addWidget(center); body.setSizes([62,250,1128]); outer.addWidget(body,1)
        self.nav_buttons["Agent"].setChecked(True)
        self._switch_view("Agent")

    def _make_simple_page(self, title, message):
        w=QWidget(); l=QVBoxLayout(w); l.addStretch(1)
        t=QLabel(title); t.setObjectName("Heading"); t.setAlignment(Qt.AlignmentFlag.AlignCenter); l.addWidget(t)
        m=QLabel(message); m.setObjectName("Muted"); m.setAlignment(Qt.AlignmentFlag.AlignCenter); l.addWidget(m); l.addStretch(1); return w

    def _load_connection(self):
        self.base_url = str(self.settings.value("connection/base_url", "http://localhost:1234/v1"))
        self.api_key = str(self.settings.value("connection/api_key", "lm-studio"))
        self.model_name = str(self.settings.value("connection/model", ""))
    def _connection_dialog(self):
        d=QDialog(self); d.setWindowTitle("Подключение модели"); d.resize(440,180)
        f=QFormLayout(d); url=QLineEdit(self.base_url); key=QLineEdit(self.api_key); model=QLineEdit(self.model_name)
        f.addRow("Base URL",url); f.addRow("API key",key); f.addRow("Model",model)
        buttons=QDialogButtonBox(QDialogButtonBox.StandardButton.Save|QDialogButtonBox.StandardButton.Cancel); f.addRow(buttons)
        buttons.accepted.connect(d.accept); buttons.rejected.connect(d.reject)
        if d.exec()!=QDialog.DialogCode.Accepted:return
        self.base_url=url.text().strip(); self.api_key=key.text().strip(); self.model_name=model.text().strip()
        self.settings.setValue("connection/base_url",self.base_url); self.settings.setValue("connection/api_key",self.api_key); self.settings.setValue("connection/model",self.model_name)
        self._refresh_models()

    def _refresh_models(self):
        self.model_combo.clear()
        try:
            client=OpenAI(base_url=self.base_url,api_key=self.api_key or "no-key",timeout=4)
            models=client.models.list().data
            names=[m.id for m in models]
            if not names: names=[self.model_name] if self.model_name else []
            self.model_combo.addItems(names)
            if self.model_name and self.model_combo.findText(self.model_name)>=0:self.model_combo.setCurrentText(self.model_name)
            elif names:self.model_name=names[0]
            self.models_info.setText("Найдено моделей: "+str(len(names))+"\nИсточник: "+self.base_url)
        except Exception as e:
            if self.model_name:self.model_combo.addItem(self.model_name)
            self.models_info.setText("Не удалось получить список моделей.\n"+str(e))
        if not self.model_combo.count(): self.model_combo.addItem("Укажите модель в подключении")
    def _choose_project(self):
        p=QFileDialog.getExistingDirectory(self,"Выберите папку проекта",self.project_root)
        if p:
            self.project_root=str(Path(p).resolve()); self.settings.setValue("project/root",self.project_root)
            self.project_btn.setText("📂  "+Path(p).name); self._refresh_tree(); self._refresh_chats()
    def _refresh_tree(self):
        self.tree.clear(); root=Path(self.project_root)
        root_item=QTreeWidgetItem([root.name or str(root)]); root_item.setData(0,Qt.ItemDataRole.UserRole,str(root)); self.tree.addTopLevelItem(root_item)
        try:
            for p in sorted(root.iterdir(),key=lambda x:(not x.is_dir(),x.name.lower())):
                if p.name in {".git","__pycache__",".venv","venv","node_modules"}: continue
                item=QTreeWidgetItem([("▸ " if p.is_dir() else "  ")+p.name]); item.setData(0,Qt.ItemDataRole.UserRole,str(p)); root_item.addChild(item)
                if p.is_dir():
                    try:
                        for child in sorted(p.iterdir(),key=lambda x:(not x.is_dir(),x.name.lower()))[:250]:
                            if child.name in {".git","__pycache__","node_modules",".venv"}:continue
                            ci=QTreeWidgetItem([("▸ " if child.is_dir() else "  ")+child.name]); ci.setData(0,Qt.ItemDataRole.UserRole,str(child)); item.addChild(ci)
                    except OSError: pass
            root_item.setExpanded(True)
        except OSError as e: self.output.appendPlainText(str(e))
    def _filter_tree(self,text):
        self.search_results.clear()
        if not text.strip():return
        try:
            for p in Path(self.project_root).rglob("*"):
                if any(x in {".git","node_modules",".venv","venv","__pycache__"} for x in p.parts):continue
                if text.lower() in p.name.lower():
                    item=QListWidgetItem(str(p.relative_to(self.project_root)));item.setData(Qt.ItemDataRole.UserRole,str(p));self.search_results.addItem(item)
                    if self.search_results.count()>=300:break
        except OSError:pass
    def _open_tree_item(self,item,column=0):
        p=Path(item.data(0,Qt.ItemDataRole.UserRole) or "")
        if p.is_dir():item.setExpanded(not item.isExpanded());return
        self._open_file(p)
    def _open_search_item(self,item):self._open_file(Path(item.data(Qt.ItemDataRole.UserRole)))
    def _open_file(self,p):
        try:
            safe=resolve_allowed_path(self.project_root,str(p))
            if not safe.is_file():return
            if safe.stat().st_size>2*1024*1024: QMessageBox.information(self,"Файл","Файл больше 2 МБ, предпросмотр отключён.");return
            safe_path = str(safe.resolve())
            existing = -1
            for i in range(self.file_tabs.count()):
                if self.file_tabs.widget(i).property("file_path") == safe_path:
                    existing = i; break
            if existing >= 0:
                self.file_tabs.setCurrentIndex(existing)
            else:
                editor = QPlainTextEdit(); editor.setReadOnly(True)
                editor.setFont(QFont("Consolas", 10)); editor.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
                editor.setPlainText(safe.read_text(encoding="utf-8",errors="replace")); editor.setProperty("file_path", safe_path)
                index = self.file_tabs.addTab(editor, safe.name); self.file_tabs.setTabToolTip(index, safe_path); self.file_tabs.setCurrentIndex(index)
            self.editor_hint.setText("ПРОСМОТР ФАЙЛА  ·  " + str(safe.relative_to(Path(self.project_root).resolve())))
            self.workspace_title.setText(safe.name); self.center_stack.setCurrentIndex(1)
        except (OSError,AccessDenied) as e:QMessageBox.warning(self,"Не удалось открыть файл",str(e))
    def _close_preview_tab(self,index):
        widget = self.file_tabs.widget(index)
        if widget is not None:
            self.file_tabs.removeTab(index)
            widget.deleteLater()
        if self.file_tabs.count() == 0:
            self.editor_hint.setText("ПРОЕКТ  ·  ПРОСМОТР ФАЙЛОВ")

    def _switch_view(self,key):
        self.current_view=key
        titles={"Explorer":"EXPLORER","Search":"SEARCH","Agent":"AGENT","History":"HISTORY","Models":"MODELS"}
        self.side_title.setText(titles.get(key,key).upper())
        idx={"Explorer":0,"Search":1,"History":2,"Agent":0,"Models":3}.get(key,0)
        self.side_stack.setCurrentIndex(idx)
        for k,b in self.nav_buttons.items():b.setChecked(k==key)
        if key=="Agent":self.center_stack.setCurrentIndex(0);self.workspace_title.setText("Agent")
        elif key=="History":self._refresh_chats();self.center_stack.setCurrentIndex(0);self.workspace_title.setText("История чатов")
        elif key=="Models":self.center_stack.setCurrentIndex(0);self.workspace_title.setText("Модели")
        elif key=="Search":self.center_stack.setCurrentIndex(2);self.workspace_title.setText("Поиск")
        else:self.center_stack.setCurrentIndex(1);self.workspace_title.setText(Path(self.project_root).name)
    def _append_message(self,role,content):
        label={"user":"Вы","assistant":"Агент","system":"Система"}.get(role,role)
        color="#c7f36b" if role=="assistant" else "#a7b0c2"
        html=f'<div style="margin:14px 0;padding:12px 15px;background:#191a20;border:1px solid #2b2d35;border-radius:10px"><b style="color:{color}">{label}</b><p style="white-space:pre-wrap;margin-bottom:2px">{escape(str(content)).replace(chr(10),"<br>")}</p></div>'
        self.chat_view.append(html)
    def _send(self):
        prompt=self.prompt.toPlainText().strip()
        if not prompt:return
        self.prompt.clear(); self._switch_view("Agent"); self._append_message("user",prompt)
        self.welcome.hide()
        self.start_agent(prompt)
    def start_agent(self,prompt):
        if self.worker and self.worker.isRunning():return
        if not Path(self.project_root).is_dir():QMessageBox.warning(self,"Проект","Выберите существующую папку проекта.");return
        if not self.chat_id:
            chat=create_chat(self.project_root,self.model_combo.currentText());self.chat_id=chat["id"]
        self.history.append({"role":"user","content":prompt})
        self._save_chat()
        self.model_name=self.model_combo.currentText()
        self.settings.setValue("connection/model",self.model_name)
        self.worker=AgentWorker(self.base_url,self.api_key or "no-key",self.model_name,self.project_root,prompt,None,
            settings=dict(DEFAULT_SETTINGS),history=self.history,memory=load_project_memory(self.project_root),
            auto_memory=True,task_id=self.chat_id)
        self.worker.chat.connect(self._on_chat)
        self.worker.log.connect(self._log)
        self.worker.failed.connect(self._failed)
        self.worker.finished_text.connect(lambda _:self._log("Задача агента завершена."))
        self.worker.progress.connect(lambda count,maximum:self.status_label.setText(f"Работает · {count}/{maximum}"))
        self.worker.conversation_updated.connect(self._conversation_updated)
        self.worker.write_approval_requested.connect(self._approve_change,Qt.ConnectionType.BlockingQueuedConnection)
        self.worker.change_event.connect(lambda event:self._log(f"Изменение: {event.get('status','')} · {event.get('path','')}"))
        self.worker.finished.connect(self._finished)
        self.send_btn.setEnabled(False);self.stop_btn.setEnabled(True);self.status_label.setText("Агент работает")
        self.worker.start()
    def _on_chat(self,role,content):
        self._append_message(role,content)
        if role=="assistant":self.history.append({"role":"assistant","content":content});self._save_chat()
    def _conversation_updated(self,messages):
        if isinstance(messages,list):self.history=messages;self._save_chat()
    def _save_chat(self):
        if not self.chat_id:return
        record=load_chat(self.chat_id) or create_chat(self.project_root,self.model_combo.currentText())
        record.update({"project_root":self.project_root,"model":self.model_combo.currentText(),"messages":self.history,"title":title_from_messages(self.history)})
        save_chat(record)
        self._refresh_chats()
    def _refresh_chats(self):
        if not hasattr(self,"chat_list"):return
        self.chat_list.clear()
        try:chats=[c for c in list_chats() if not c.get("project_root") or str(Path(c.get("project_root")).resolve()) == str(Path(self.project_root).resolve())]
        except Exception:chats=[]
        for c in chats:
            it=QListWidgetItem(c.get("title","Чат"));it.setData(Qt.ItemDataRole.UserRole,c.get("id"));self.chat_list.addItem(it)
    def _open_chat_item(self,item):
        if self.worker and self.worker.isRunning():QMessageBox.information(self,"Агент","Дождитесь завершения задачи.");return
        c=load_chat(item.data(Qt.ItemDataRole.UserRole))
        if not c:return
        self.chat_id=c.get("id");self.chat_title=c.get("title","Чат");self.history=c.get("messages",[])
        self.chat_view.clear()
        for m in self.history:
            if m.get("role") in ("user","assistant","system") and isinstance(m.get("content"),str):self._append_message(m["role"],m["content"])
        self._switch_view("Agent")
    def _new_chat(self):
        if self.worker and self.worker.isRunning():return
        self.chat_id=None;self.chat_title="Новый чат";self.history=[];self.chat_view.clear();self.welcome.show();self._switch_view("Agent")
    def _load_saved_chat(self):
        cid=str(self.settings.value("chat/current_id",""))
        if cid:
            c=load_chat(cid)
            if c:
                self.chat_id=cid;self.history=c.get("messages",[])
                for m in self.history:
                    if m.get("role") in ("user","assistant","system") and isinstance(m.get("content"),str):self._append_message(m["role"],m["content"])
    def _approve_change(self,path,diff,exists):
        d=ApprovalDialog(path,diff,exists,self);result=d.exec()
        decision={1:"apply",2:"reject"}.get(result,"cancel")
        if self.worker:self.worker.resolve_write_approval(decision)
        self._log(f"Изменение {decision}: {path}")
    def _log(self,text):self.output.appendPlainText(str(text))
    def _show_output(self):self.output.setVisible(not self.output.isVisible())
    def _stop_agent(self):
        if self.worker and self.worker.isRunning():self.worker.requestInterruption();self.stop_btn.setEnabled(False)
    def _failed(self,error):
        self._log(error);QMessageBox.critical(self,"Ошибка агента",str(error));self.status_label.setText("Ошибка")
    def _finished(self):
        self.send_btn.setEnabled(True);self.stop_btn.setEnabled(False);self.status_label.setText("Готов")
    def _bind_shortcuts(self):
        QShortcut(QKeySequence("Ctrl+L"),self,activated=lambda:self.prompt.setFocus())
        QShortcut(QKeySequence("Ctrl+Shift+N"),self,activated=self._new_chat)
        QShortcut(QKeySequence("Ctrl+O"),self,activated=self._choose_project)
        QShortcut(QKeySequence("Return"),self.prompt,activated=self._enter_send)
    def _enter_send(self):
        if QApplication.keyboardModifiers() & Qt.KeyboardModifier.ShiftModifier:
            self.prompt.insertPlainText("\n")
        else:self._send()
    def closeEvent(self,event):
        if self.worker and self.worker.isRunning():
            self.worker.requestInterruption()
        self.settings.setValue("project/root",self.project_root)
        if self.chat_id:self.settings.setValue("chat/current_id",self.chat_id)
        super().closeEvent(event)
