from pathlib import Path
from html import escape

from PySide6.QtCore import Qt, QSettings, QSize
from PySide6.QtGui import QFont, QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFileDialog, QTextBrowser, QPlainTextEdit, QMessageBox,
    QSplitter, QSpinBox, QGroupBox, QFormLayout, QDialog, QListWidget,
    QListWidgetItem, QInputDialog, QFrame, QToolButton, QComboBox,
    QSizePolicy, QApplication
)
from openai import OpenAI
from .worker import AgentWorker, DEFAULT_SETTINGS
from .tools import run_sandbox_self_test
from .chat_store import list_chats, create_chat, load_chat, save_chat, delete_chat, rename_chat, title_from_messages


APP_QSS = """
QMainWindow, QWidget { background: #111318; color: #e7e9ee; font-family: "Segoe UI"; font-size: 13px; }
QFrame#Sidebar { background: #17191f; border-right: 1px solid #292d36; }
QFrame#TopBar { background: #15171c; border-bottom: 1px solid #292d36; }
QFrame#Composer { background: #15171c; border-top: 1px solid #292d36; }
QFrame#Card { background: #181b21; border: 1px solid #292d36; border-radius: 10px; }
QFrame#InspectorCard { background: #171a20; border: 1px solid #292d36; border-radius: 10px; }
QLabel#Brand { font-size: 16px; font-weight: 700; }
QLabel#Muted { color: #8f96a3; }
QLabel#Status { color: #9aa2af; padding: 4px 8px; border-radius: 8px; background: #1c2027; }
QLabel#StatusWorking { color: #f0c36b; background: #2b2518; padding: 4px 8px; border-radius: 8px; }
QLabel#StatusReady { color: #75d49a; background: #18261f; padding: 4px 8px; border-radius: 8px; }
QLabel#StatusError { color: #ff8d8d; background: #2b1b1e; padding: 4px 8px; border-radius: 8px; }
QPushButton, QToolButton { background: #20242c; border: 1px solid #303540; border-radius: 7px; padding: 7px 11px; color: #e8eaf0; }
QPushButton:hover, QToolButton:hover { background: #292e38; }
QPushButton:pressed, QToolButton:pressed { background: #343a46; }
QPushButton#Primary { background: #3b82f6; border-color: #3b82f6; color: white; font-weight: 600; }
QPushButton#Primary:hover { background: #4b8df7; }
QPushButton#Danger { background: #342024; border-color: #5a2b32; color: #ff9b9b; }
QLineEdit, QPlainTextEdit, QTextBrowser, QComboBox { background: #0f1115; border: 1px solid #2b3039; border-radius: 8px; color: #e8eaf0; selection-background-color: #315f9f; }
QLineEdit { padding: 8px 10px; }
QPlainTextEdit { padding: 8px; }
QTextBrowser { padding: 14px; }
QComboBox { padding: 7px 9px; }
QComboBox QAbstractItemView { background: #171a20; color: #e8eaf0; selection-background-color: #2c5b95; }
QListWidget { background: transparent; border: none; outline: none; }
QListWidget::item { padding: 10px 10px; margin: 2px 4px; border-radius: 7px; color: #c8ccd5; }
QListWidget::item:hover { background: #20242c; }
QListWidget::item:selected { background: #252b35; color: white; }
QSplitter::handle { background: #252932; }
QScrollBar:vertical { background: transparent; width: 9px; margin: 2px; }
QScrollBar::handle:vertical { background: #343a46; border-radius: 4px; min-height: 30px; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QGroupBox { border: 1px solid #2a2f38; border-radius: 9px; margin-top: 10px; padding: 10px; }
QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; color: #aeb5c1; }
QSpinBox { background: #0f1115; border: 1px solid #2b3039; border-radius: 7px; padding: 5px; }
"""


class FileChangeDialog(QDialog):
    def __init__(self, parent, path, diff, exists):
        super().__init__(parent)
        self.setWindowTitle("Подтверждение изменения файла")
        self.setModal(True)
        self.resize(950, 680)
        layout = QVBoxLayout(self)
        action = "Перезаписать существующий файл" if exists else "Создать новый файл"
        title = QLabel(f"<b>{action}</b>")
        title.setStyleSheet("font-size: 15px;")
        layout.addWidget(title)
        path_label = QLabel(f"Файл: <code>{escape(path)}</code><br><span style='color:#8f96a3'>Проверь diff перед записью.</span>")
        path_label.setWordWrap(True)
        layout.addWidget(path_label)
        diff_view = QPlainTextEdit()
        diff_view.setReadOnly(True)
        diff_view.setPlainText(diff)
        layout.addWidget(diff_view, 1)
        buttons = QHBoxLayout()
        buttons.addStretch(1)
        cancel = QPushButton("Отмена")
        reject = QPushButton("Отклонить")
        apply = QPushButton("Применить")
        apply.setObjectName("Primary")
        cancel.clicked.connect(lambda: self.done(3))
        reject.clicked.connect(lambda: self.done(2))
        apply.clicked.connect(lambda: self.done(1))
        buttons.addWidget(cancel); buttons.addWidget(reject); buttons.addWidget(apply)
        layout.addLayout(buttons)

    @staticmethod
    def ask(parent, path, diff, exists):
        result = FileChangeDialog(parent, path, diff, exists).exec()
        return {1: "apply", 2: "reject", 3: "cancel"}.get(result, "cancel")


class SettingsDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Настройки агента")
        self.resize(520, 380)
        self.parent_window = parent
        layout = QVBoxLayout(self)
        group = QGroupBox("Ограничения агента")
        form = QFormLayout(group)
        self.controls = {}
        for key, label, minimum, maximum, step in [
            ("max_tool_calls", "Вызовов инструментов за запрос", 1, 100, 1),
            ("max_consecutive_errors", "Ошибок подряд", 1, 20, 1),
            ("max_tokens", "Максимум токенов ответа", 64, 16384, 64),
            ("max_entries", "Записей в списке файлов", 10, 5000, 10),
            ("max_search_depth", "Глубина поиска", 1, 30, 1),
        ]:
            spin = QSpinBox(); spin.setRange(minimum, maximum); spin.setSingleStep(step)
            spin.setValue(parent.settings_store.value(f"limits/{key}", DEFAULT_SETTINGS[key], type=int))
            self.controls[key] = spin; form.addRow(label, spin)
        layout.addWidget(group)
        note = QLabel("Изменения сохраняются автоматически при нажатии «Сохранить». Система разрешений и sandbox остаются без изменений.")
        note.setWordWrap(True); note.setObjectName("Muted"); layout.addWidget(note)
        buttons = QHBoxLayout(); buttons.addStretch(1)
        cancel = QPushButton("Отмена"); save = QPushButton("Сохранить"); save.setObjectName("Primary")
        cancel.clicked.connect(self.reject); save.clicked.connect(self.accept)
        buttons.addWidget(cancel); buttons.addWidget(save); layout.addLayout(buttons)

    def values(self):
        return {k: v.value() for k, v in self.controls.items()}


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Local Coding Agent")
        self.resize(1450, 900)
        self.setMinimumSize(1050, 700)
        self.setStyleSheet(APP_QSS)
        self.worker = None
        self.conversation_history = []
        self.settings_store = QSettings("LocalCodingAgent", "LocalCodingAgent")
        self.current_chat_id = None
        self.current_chat_title = "Новый чат"
        self._build_ui()
        self._create_hidden_connection_fields()
        self._bind_shortcuts()
        self.refresh_chat_list()
        saved_chat_id = self.settings_store.value("chat/current_id", "")
        if saved_chat_id:
            chat = load_chat(str(saved_chat_id))
            if chat:
                self._load_chat_record(chat, announce=False)
        self._set_status("Готов", "ready")

    def _build_ui(self):
        root = QWidget(); self.setCentralWidget(root)
        outer = QVBoxLayout(root); outer.setContentsMargins(0, 0, 0, 0); outer.setSpacing(0)
        outer.addWidget(self._build_topbar())
        body = QSplitter(Qt.Horizontal); body.setChildrenCollapsible(False)
        body.addWidget(self._build_sidebar())
        body.addWidget(self._build_center())
        body.addWidget(self._build_inspector())
        body.setSizes([250, 850, 280]); outer.addWidget(body, 1)
        outer.addWidget(self._build_composer())

    def _build_topbar(self):
        bar = QFrame(); bar.setObjectName("TopBar"); layout = QHBoxLayout(bar); layout.setContentsMargins(16, 10, 16, 10)
        brand = QLabel("◈  Local Coding Agent"); brand.setObjectName("Brand"); layout.addWidget(brand)
        layout.addSpacing(18)
        self.chat_title_label = QLabel("Новый чат"); self.chat_title_label.setObjectName("Muted"); layout.addWidget(self.chat_title_label)
        layout.addStretch(1)
        self.project_label = QLabel("Проект: —"); self.project_label.setObjectName("Muted"); layout.addWidget(self.project_label)
        self.model_label = QLabel("Модель: local-model"); self.model_label.setObjectName("Muted"); layout.addWidget(self.model_label)
        self.status_label = QLabel("Готов"); self.status_label.setObjectName("StatusReady"); layout.addWidget(self.status_label)
        settings = QToolButton(); settings.setText("⚙"); settings.setToolTip("Настройки агента"); settings.clicked.connect(self.open_settings); layout.addWidget(settings)
        return bar

    def _build_sidebar(self):
        panel = QFrame(); panel.setObjectName("Sidebar"); panel.setMinimumWidth(220); panel.setMaximumWidth(340)
        layout = QVBoxLayout(panel); layout.setContentsMargins(10, 12, 10, 12)
        new_btn = QPushButton("＋  Новый чат"); new_btn.setObjectName("Primary"); new_btn.clicked.connect(self.new_chat); layout.addWidget(new_btn)
        self.chat_search = QLineEdit(); self.chat_search.setPlaceholderText("Поиск по истории…"); self.chat_search.textChanged.connect(self.filter_chats); layout.addWidget(self.chat_search)
        label = QLabel("ИСТОРИЯ"); label.setObjectName("Muted"); layout.addWidget(label)
        self.chat_list = QListWidget(); self.chat_list.itemClicked.connect(self.open_chat_item); layout.addWidget(self.chat_list, 1)
        row = QHBoxLayout()
        rename = QPushButton("Переименовать"); rename.clicked.connect(self.rename_current_chat)
        delete = QPushButton("Удалить"); delete.setObjectName("Danger"); delete.clicked.connect(self.delete_current_chat)
        row.addWidget(rename); row.addWidget(delete); layout.addLayout(row)
        project_card = QFrame(); project_card.setObjectName("Card"); p = QVBoxLayout(project_card)
        p.addWidget(QLabel("ПРОЕКТ")); self.sidebar_project = QLabel("—"); self.sidebar_project.setWordWrap(True); self.sidebar_project.setObjectName("Muted"); p.addWidget(self.sidebar_project)
        choose = QPushButton("Выбрать папку"); choose.clicked.connect(self.choose_project); p.addWidget(choose); layout.addWidget(project_card)
        return panel

    def _build_center(self):
        panel = QWidget(); layout = QVBoxLayout(panel); layout.setContentsMargins(14, 14, 14, 14)
        self.chat_view = QTextBrowser(); self.chat_view.setOpenExternalLinks(False); self.chat_view.setPlaceholderText("Начните диалог с агентом…"); layout.addWidget(self.chat_view, 1)
        self.log_toggle = QToolButton(); self.log_toggle.setText("⌄  Журнал инструментов"); self.log_toggle.setCheckable(True); self.log_toggle.setChecked(False); layout.addWidget(self.log_toggle)
        self.log_view = QPlainTextEdit(); self.log_view.setReadOnly(True); self.log_view.setMaximumHeight(220); self.log_view.hide(); layout.addWidget(self.log_view)
        self.log_toggle.toggled.connect(self.log_view.setVisible)
        return panel

    def _build_inspector(self):
        panel = QFrame(); panel.setObjectName("Sidebar"); panel.setMinimumWidth(240); panel.setMaximumWidth(360)
        layout = QVBoxLayout(panel); layout.setContentsMargins(12, 14, 12, 14)
        title = QLabel("РАБОЧАЯ ОБЛАСТЬ"); title.setObjectName("Muted"); layout.addWidget(title)
        card = QFrame(); card.setObjectName("InspectorCard"); c = QVBoxLayout(card)
        self.inspector_project = QLabel("Проект не выбран"); self.inspector_project.setWordWrap(True); c.addWidget(self.inspector_project)
        self.inspector_model = QLabel("Модель: local-model"); self.inspector_model.setObjectName("Muted"); c.addWidget(self.inspector_model)
        self.inspector_sandbox = QLabel("🔒 Sandbox включён\nФайлы доступны только внутри выбранного проекта."); self.inspector_sandbox.setWordWrap(True); c.addWidget(self.inspector_sandbox)
        layout.addWidget(card)
        changes = QFrame(); changes.setObjectName("InspectorCard"); ch = QVBoxLayout(changes)
        ch.addWidget(QLabel("ИЗМЕНЕНИЯ")); self.changes_label = QLabel("Нет ожидающих изменений"); self.changes_label.setObjectName("Muted"); self.changes_label.setWordWrap(True); ch.addWidget(self.changes_label)
        layout.addWidget(changes)
        tools = QFrame(); tools.setObjectName("InspectorCard"); t = QVBoxLayout(tools); t.addWidget(QLabel("ДИАГНОСТИКА"))
        connection = QPushButton("Проверить подключение"); connection.clicked.connect(self.test_connection); t.addWidget(connection)
        tool_test = QPushButton("Проверить tool calling"); tool_test.clicked.connect(self.test_tool_calling); t.addWidget(tool_test)
        sandbox = QPushButton("🔒 Проверить sandbox"); sandbox.clicked.connect(self.test_sandbox); t.addWidget(sandbox)
        layout.addWidget(tools); layout.addStretch(1)
        return panel

    def _build_composer(self):
        panel = QFrame(); panel.setObjectName("Composer"); layout = QHBoxLayout(panel); layout.setContentsMargins(14, 10, 14, 10)
        self.prompt = QPlainTextEdit(); self.prompt.setPlaceholderText("Опишите задачу…  Enter — отправить, Shift+Enter — новая строка"); self.prompt.setFixedHeight(72); layout.addWidget(self.prompt, 1)
        buttons = QVBoxLayout()
        self.send_btn = QPushButton("Отправить  ↵"); self.send_btn.setObjectName("Primary"); self.send_btn.clicked.connect(self.send_message); buttons.addWidget(self.send_btn)
        self.stop_btn = QPushButton("Остановить"); self.stop_btn.setObjectName("Danger"); self.stop_btn.setEnabled(False); self.stop_btn.clicked.connect(self.stop_agent); buttons.addWidget(self.stop_btn)
        layout.addLayout(buttons)
        return panel

    def _bind_shortcuts(self):
        QShortcut(QKeySequence("Ctrl+N"), self, activated=self.new_chat)
        QShortcut(QKeySequence("Ctrl+L"), self, activated=self.prompt.setFocus)
        QShortcut(QKeySequence("Escape"), self, activated=self.stop_agent)

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter) and self.prompt.hasFocus():
            if event.modifiers() & Qt.ShiftModifier:
                super().keyPressEvent(event)
            else:
                self.send_message()
                event.accept()
            return
        super().keyPressEvent(event)

    def _set_status(self, text, kind="ready"):
        self.status_label.setText(text)
        self.status_label.setObjectName({"ready": "StatusReady", "working": "StatusWorking", "error": "StatusError"}.get(kind, "Status"))
        self.status_label.style().unpolish(self.status_label); self.status_label.style().polish(self.status_label)

    def _update_context_labels(self):
        project = self.project_path.text() if hasattr(self, "project_path") else str(Path.home())
        self.project_label.setText(f"Проект: {Path(project).name or project}")
        self.sidebar_project.setText(project)
        self.inspector_project.setText(project)
        self.model_label.setText(f"Модель: {self.model.text()}")
        self.inspector_model.setText(f"Модель: {self.model.text()}")
        self.chat_title_label.setText(self.current_chat_title)

    def _create_hidden_connection_fields(self):
        self.base_url = QLineEdit(self.settings_store.value("connection/base_url", "http://127.0.0.1:8080/v1"))
        self.api_key = QLineEdit(self.settings_store.value("connection/api_key", "no-key"))
        self.model = QLineEdit(self.settings_store.value("connection/model", "local-model"))
        self.project_path = QLineEdit(self.settings_store.value("project/path", str(Path.home())))
        self.project_path.setReadOnly(True)

    # Connection fields are kept as application state; the modern UI exposes them through settings.
    def _spin(self, key, minimum, maximum, default, step=1):
        spin = QSpinBox(); spin.setRange(minimum, maximum); spin.setSingleStep(step)
        spin.setValue(self.settings_store.value(f"limits/{key}", default, type=int)); return spin

    def current_limits(self):
        return {k: self.settings_store.value(f"limits/{k}", DEFAULT_SETTINGS[k], type=int) for k in DEFAULT_SETTINGS}

    def save_limits(self):
        self.settings_store.sync()

    def open_settings(self):
        dialog = SettingsDialog(self)
        if dialog.exec():
            for key, value in dialog.values().items(): self.settings_store.setValue(f"limits/{key}", value)
            self.settings_store.sync()
            self.log_view.appendPlainText("Agent limits saved.")

    def choose_project(self):
        current = getattr(self, "project_path", QLineEdit(str(Path.home()))).text()
        selected = QFileDialog.getExistingDirectory(self, "Выберите папку проекта", current)
        if selected:
            path = str(Path(selected).resolve())
            self.project_path.setText(path); self.settings_store.setValue("project/path", path); self.settings_store.sync()
            self._update_context_labels()
            self.inspector_sandbox.setText("🔒 Sandbox включён\nФайлы доступны только внутри выбранного проекта.")

    def test_connection(self):
        try:
            client = OpenAI(base_url=self.base_url.text().strip(), api_key=self.api_key.text().strip() or "no-key", timeout=15, max_retries=0)
            models = client.models.list(); ids = [m.id for m in models.data]
            self.log_view.appendPlainText("Connection OK. Models: " + (", ".join(ids) if ids else "(none)"))
            if ids and self.model.text().strip() in ("", "local-model"):
                self.model.setText(ids[0]); self.settings_store.setValue("connection/model", ids[0]); self._update_context_labels()
            self._set_status("Подключено", "ready")
            QMessageBox.information(self, "Подключение", "Подключение успешно.")
        except Exception as exc:
            self._set_status("Ошибка подключения", "error")
            QMessageBox.critical(self, "Ошибка подключения", f"{type(exc).__name__}: {exc}")

    def test_sandbox(self):
        result = run_sandbox_self_test(); self.log_view.appendPlainText("\n=== SANDBOX SELF-TEST ===\n" + result["details"])
        summary = f"Passed: {result['passed']} | Failed: {result['failed']} | Skipped: {result['skipped']}"
        self._set_status("Sandbox OK" if result["ok"] else "Sandbox error", "ready" if result["ok"] else "error")
        (QMessageBox.information if result["ok"] else QMessageBox.warning)(self, "Sandbox test", summary)

    def test_tool_calling(self):
        self.start_agent("Вызови list_files ровно один раз для корня проекта: path='.', recursive=false. Затем кратко опиши результат, не угадывай содержимое.", force_tool="list_files", use_history=False)

    def send_message(self):
        prompt = self.prompt.toPlainText().strip()
        if not prompt or (self.worker and self.worker.isRunning()): return
        self.prompt.clear(); self._append_message("user", prompt); self.start_agent(prompt)

    def new_chat(self):
        if self.worker and self.worker.isRunning():
            QMessageBox.warning(self, "Агент занят", "Дождитесь завершения или нажмите «Остановить»."); return
        self._save_current_chat()
        chat = create_chat(self.project_path.text(), self.model.text().strip())
        self.current_chat_id = chat["id"]; self.current_chat_title = chat["title"]; self.conversation_history = []
        self.settings_store.setValue("chat/current_id", self.current_chat_id); self.settings_store.sync()
        self.render_history(); self.refresh_chat_list(select_id=self.current_chat_id); self._update_context_labels(); self._set_status("Готов", "ready")

    def start_agent(self, prompt, force_tool=None, use_history=True):
        if self.worker and self.worker.isRunning(): return
        root = Path(self.project_path.text())
        if not root.is_dir(): QMessageBox.warning(self, "Проект", "Выберите существующую папку проекта."); return
        if use_history:
            if not self.current_chat_id:
                chat = create_chat(str(root.resolve()), self.model.text().strip()); self.current_chat_id = chat["id"]
            self._save_current_chat(extra_message={"role": "user", "content": prompt})
        self.settings_store.setValue("connection/base_url", self.base_url.text()); self.settings_store.setValue("connection/api_key", self.api_key.text()); self.settings_store.setValue("connection/model", self.model.text()); self.settings_store.sync()
        self.worker = AgentWorker(self.base_url.text().strip(), self.api_key.text().strip() or "no-key", self.model.text().strip(), str(root.resolve()), prompt, force_tool, settings=self.current_limits(), history=self.conversation_history if use_history else [])
        self.worker.chat.connect(self.on_chat); self.worker.log.connect(self.log_view.appendPlainText); self.worker.failed.connect(self.on_failed); self.worker.finished_text.connect(lambda _: self.log_view.appendPlainText("Agent turn finished.")); self.worker.progress.connect(self.on_progress)
        if use_history: self.worker.conversation_updated.connect(self.update_conversation_history)
        self.worker.write_approval_requested.connect(self.confirm_file_change, Qt.ConnectionType.BlockingQueuedConnection); self.worker.finished.connect(self.on_worker_finished)
        self.send_btn.setEnabled(False); self.stop_btn.setEnabled(True); self._set_status("Работает…", "working"); self.worker.start()

    def update_conversation_history(self, messages):
        self.conversation_history = list(messages); self._save_current_chat(); self.refresh_chat_list(select_id=self.current_chat_id)

    def _save_current_chat(self, extra_message=None):
        if not self.current_chat_id: return
        chat = load_chat(self.current_chat_id)
        if not chat: chat = create_chat(self.project_path.text(), self.model.text().strip()); self.current_chat_id = chat["id"]
        messages = list(self.conversation_history)
        if extra_message is not None and (not messages or messages[-1] != extra_message): messages.append(extra_message)
        chat["messages"] = messages; chat["project_root"] = self.project_path.text(); chat["model"] = self.model.text().strip()
        if messages: chat["title"] = title_from_messages(messages); self.current_chat_title = chat["title"]
        save_chat(chat); self.settings_store.setValue("chat/current_id", self.current_chat_id); self.settings_store.sync(); self._update_context_labels()

    def refresh_chat_list(self, select_id=None):
        chats = list_chats(); query = getattr(self, "chat_search", QLineEdit()).text().strip().lower() if hasattr(self, "chat_search") else ""
        self.chat_list.blockSignals(True); self.chat_list.clear(); selected = None
        for chat in chats:
            title = chat.get("title") or "Новый чат"; project = chat.get("project_root") or "Проект не указан"
            haystack = f"{title} {project}".lower()
            if query and query not in haystack: continue
            item = QListWidgetItem(f"{title}\n{Path(project).name if project else 'Проект не указан'}")
            item.setData(Qt.ItemDataRole.UserRole, chat.get("id")); item.setToolTip(f"{title}\n{project}"); self.chat_list.addItem(item)
            if select_id and chat.get("id") == select_id: selected = item
        if selected: self.chat_list.setCurrentItem(selected)
        self.chat_list.blockSignals(False)

    def filter_chats(self, _text): self.refresh_chat_list(select_id=self.current_chat_id)

    def _load_chat_record(self, chat, announce=True):
        self._save_current_chat(); self.current_chat_id = chat["id"]; self.current_chat_title = chat.get("title", "Новый чат"); self.conversation_history = list(chat.get("messages", []))
        if chat.get("project_root") and Path(chat["project_root"]).is_dir(): self.project_path.setText(str(Path(chat["project_root"]).resolve()))
        if chat.get("model"): self.model.setText(chat["model"])
        self.settings_store.setValue("chat/current_id", self.current_chat_id); self.settings_store.sync(); self.render_history(); self.refresh_chat_list(select_id=self.current_chat_id); self._update_context_labels()
        if announce: self.log_view.appendPlainText(f"=== Открыт чат: {self.current_chat_title} ===")

    def open_chat_item(self, item):
        if self.worker and self.worker.isRunning(): QMessageBox.warning(self, "Агент занят", "Сначала завершите текущий запрос."); return
        chat = load_chat(item.data(Qt.ItemDataRole.UserRole))
        if chat: self._load_chat_record(chat)

    def render_history(self):
        self.chat_view.clear()
        for msg in self.conversation_history:
            role = msg.get("role"); content = msg.get("content")
            if role in ("user", "assistant", "system") and isinstance(content, str) and content: self._append_message(role, content, render_only=True)

    def _append_message(self, role, content, render_only=False):
        labels = {"user": "Вы", "assistant": "Ассистент", "system": "Система"}; label = labels.get(role, role.title())
        safe = escape(content).replace("\n", "<br>")
        if role == "user": html = f"<div style='margin:10px 0;padding:11px 13px;background:#20252e;border-radius:10px;'><b>{label}</b><br>{safe}</div>"
        elif role == "system": html = f"<div style='margin:10px 0;padding:10px;border-left:3px solid #8b93a1;color:#aeb5c1;'><b>{label}</b> · {safe}</div>"
        else: html = f"<div style='margin:10px 0;padding:11px 13px;background:#181b21;border:1px solid #292d36;border-radius:10px;'><b>{label}</b><br>{safe}</div>"
        self.chat_view.append(html)
        self.chat_view.verticalScrollBar().setValue(self.chat_view.verticalScrollBar().maximum())

    def rename_current_chat(self):
        if not self.current_chat_id: return
        chat = load_chat(self.current_chat_id)
        if not chat: return
        title, ok = QInputDialog.getText(self, "Переименовать чат", "Название:", text=chat.get("title", "Новый чат"))
        if ok and title.strip(): rename_chat(self.current_chat_id, title.strip()); self.current_chat_title = title.strip(); self.refresh_chat_list(select_id=self.current_chat_id); self._update_context_labels()

    def delete_current_chat(self):
        if not self.current_chat_id: return
        if QMessageBox.question(self, "Удалить чат", "Удалить выбранный чат и историю?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No) != QMessageBox.Yes: return
        delete_chat(self.current_chat_id); self.current_chat_id = None; self.conversation_history = []; self.chat_view.clear(); self.new_chat()

    def stop_agent(self):
        if self.worker and self.worker.isRunning(): self.worker.requestInterruption(); self.stop_btn.setEnabled(False); self.log_view.appendPlainText("Stop requested…")

    def confirm_file_change(self, path, diff, exists):
        decision = FileChangeDialog.ask(self, path, diff, exists)
        if self.worker: self.worker.resolve_write_approval(decision)
        self.changes_label.setText({"apply": "Изменение применено: " + path, "reject": "Изменение отклонено: " + path, "cancel": "Изменение отменено: " + path}[decision])
        self.log_view.appendPlainText(f"WRITE {decision.upper()}: {path}")

    def on_progress(self, count, maximum): self.stop_btn.setText(f"Остановить ({count}/{maximum})")

    def on_failed(self, err): self._set_status("Ошибка", "error"); QMessageBox.critical(self, "Ошибка агента", err)

    def on_worker_finished(self):
        self.send_btn.setEnabled(True); self.stop_btn.setEnabled(False); self.stop_btn.setText("Остановить"); self._set_status("Готов", "ready")

    def on_chat(self, role, content): self._append_message(role, content)


# Keep the original connection fields out of the visual layout while preserving the existing backend API.
