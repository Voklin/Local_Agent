from pathlib import Path
from PySide6.QtCore import Qt, QSettings
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFileDialog, QTextEdit, QPlainTextEdit, QMessageBox,
    QSplitter, QSpinBox, QGroupBox, QFormLayout, QDialog, QDialogButtonBox
)
from openai import OpenAI
from .worker import AgentWorker, DEFAULT_SETTINGS
from .tools import run_sandbox_self_test



class FileChangeDialog(QDialog):
    """GUI approval dialog for one proposed file change."""
    def __init__(self, parent, path, diff, exists):
        super().__init__(parent)
        self.setWindowTitle("Подтверждение изменения файла")
        self.setModal(True)
        self.resize(900, 650)

        from PySide6.QtWidgets import QLabel, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout

        layout = QVBoxLayout(self)
        action = "Перезаписать существующий файл" if exists else "Создать новый файл"
        label = QLabel(
            f"<b>{action}</b><br>"
            f"Файл: <code>{path}</code><br><br>"
            "Проверь diff перед записью."
        )
        label.setWordWrap(True)
        layout.addWidget(label)

        self.diff_view = QTextEdit()
        self.diff_view.setReadOnly(True)
        self.diff_view.setPlainText(diff)
        layout.addWidget(self.diff_view, 1)

        buttons = QHBoxLayout()
        apply_btn = QPushButton("Применить")
        reject_btn = QPushButton("Отклонить")
        cancel_btn = QPushButton("Отмена")

        apply_btn.setDefault(True)
        apply_btn.clicked.connect(lambda: self.done(1))
        reject_btn.clicked.connect(lambda: self.done(2))
        cancel_btn.clicked.connect(lambda: self.done(3))

        buttons.addStretch(1)
        buttons.addWidget(cancel_btn)
        buttons.addWidget(reject_btn)
        buttons.addWidget(apply_btn)
        layout.addLayout(buttons)

    @staticmethod
    def ask(parent, path, diff, exists):
        dialog = FileChangeDialog(parent, path, diff, exists)
        result = dialog.exec()
        return {1: "apply", 2: "reject", 3: "cancel"}.get(result, "cancel")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Local Coding Agent — File Editing Edition")
        self.resize(1100, 850)
        self.worker = None
        # In-memory chat history for this session, including tool calls/results.
        self.conversation_history = []
        self.settings_store = QSettings("LocalCodingAgent", "LocalCodingAgent")

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        row = QHBoxLayout()
        layout.addLayout(row)
        self.base_url = QLineEdit("http://127.0.0.1:8080/v1")
        self.api_key = QLineEdit("no-key")
        self.model = QLineEdit("local-model")
        for label, widget in [("Base URL", self.base_url), ("API key", self.api_key), ("Model ID", self.model)]:
            row.addWidget(QLabel(label))
            row.addWidget(widget)

        project_row = QHBoxLayout()
        layout.addLayout(project_row)
        self.project_path = QLineEdit(str(Path.home()))
        self.project_path.setReadOnly(True)
        project_row.addWidget(QLabel("Project directory"))
        project_row.addWidget(self.project_path, 1)
        self.browse_btn = QPushButton("Browse…")
        self.browse_btn.clicked.connect(self.choose_project)
        project_row.addWidget(self.browse_btn)

        self.sandbox_status = QLabel("🔒 File tools are restricted to the selected project directory.")
        layout.addWidget(self.sandbox_status)

        self.limits_group = QGroupBox("Agent limits (saved automatically)")
        limits_layout = QFormLayout(self.limits_group)
        self.max_tool_calls = self._spin("max_tool_calls", 1, 100, DEFAULT_SETTINGS["max_tool_calls"])
        self.max_consecutive_errors = self._spin("max_consecutive_errors", 1, 20, DEFAULT_SETTINGS["max_consecutive_errors"])
        self.max_tokens = self._spin("max_tokens", 64, 16384, DEFAULT_SETTINGS["max_tokens"], step=64)
        self.max_entries = self._spin("max_entries", 10, 5000, DEFAULT_SETTINGS["max_entries"], step=10)
        self.max_search_depth = self._spin("max_search_depth", 1, 30, DEFAULT_SETTINGS["max_search_depth"])
        limits_layout.addRow("Maximum tool calls per request", self.max_tool_calls)
        limits_layout.addRow("Maximum consecutive tool errors", self.max_consecutive_errors)
        limits_layout.addRow("Maximum tokens per model response", self.max_tokens)
        limits_layout.addRow("Maximum entries in a file listing", self.max_entries)
        limits_layout.addRow("Maximum recursive search depth", self.max_search_depth)
        layout.addWidget(self.limits_group)

        buttons = QHBoxLayout()
        layout.addLayout(buttons)
        self.connect_btn = QPushButton("Test connection")
        self.connect_btn.clicked.connect(self.test_connection)
        buttons.addWidget(self.connect_btn)
        self.tool_btn = QPushButton("Test tool calling")
        self.tool_btn.clicked.connect(self.test_tool_calling)
        buttons.addWidget(self.tool_btn)
        self.sandbox_btn = QPushButton("🔒 Test sandbox")
        self.sandbox_btn.clicked.connect(self.test_sandbox)
        buttons.addWidget(self.sandbox_btn)
        self.stop_btn = QPushButton("Stop")
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self.stop_agent)
        buttons.addWidget(self.stop_btn)

        split = QSplitter(Qt.Orientation.Vertical)
        layout.addWidget(split, 1)
        self.chat_view = QTextEdit()
        self.chat_view.setReadOnly(True)
        self.chat_view.setPlaceholderText("Диалог с агентом")
        self.log_view = QPlainTextEdit()
        self.log_view.setReadOnly(True)
        self.log_view.setPlaceholderText("Журнал вызовов инструментов и проверок безопасности")
        split.addWidget(self.chat_view)
        split.addWidget(self.log_view)
        split.setSizes([450, 250])

        input_row = QHBoxLayout()
        layout.addLayout(input_row)
        self.prompt = QLineEdit()
        self.prompt.setPlaceholderText("Например: изучи проект и предложи исправление; запись потребует подтверждения")
        self.prompt.returnPressed.connect(self.send_message)
        input_row.addWidget(self.prompt, 1)
        self.send_btn = QPushButton("Send")
        self.send_btn.clicked.connect(self.send_message)
        input_row.addWidget(self.send_btn)
        self.clear_btn = QPushButton("Clear log")
        self.clear_btn.clicked.connect(self.log_view.clear)
        input_row.addWidget(self.clear_btn)
        self.new_chat_btn = QPushButton("New chat")
        self.new_chat_btn.setToolTip("Очистить историю диалога и начать новый разговор")
        self.new_chat_btn.clicked.connect(self.new_chat)
        input_row.addWidget(self.new_chat_btn)

        for control in self._limit_controls():
            control.valueChanged.connect(self.save_limits)

    def _spin(self, key, minimum, maximum, default, step=1):
        spin = QSpinBox()
        spin.setRange(minimum, maximum)
        spin.setSingleStep(step)
        spin.setValue(int(self.settings_store.value(f"limits/{key}", default)))
        spin.setToolTip(f"Настройка сохраняется автоматически: {key}")
        return spin

    def _limit_controls(self):
        return [self.max_tool_calls, self.max_consecutive_errors, self.max_tokens, self.max_entries, self.max_search_depth]

    def save_limits(self, *_):
        for key, control in zip(DEFAULT_SETTINGS.keys(), self._limit_controls()):
            self.settings_store.setValue(f"limits/{key}", control.value())
        self.settings_store.sync()

    def current_limits(self):
        return {key: control.value() for key, control in zip(DEFAULT_SETTINGS.keys(), self._limit_controls())}

    def choose_project(self):
        selected = QFileDialog.getExistingDirectory(self, "Select project directory", self.project_path.text())
        if selected:
            self.project_path.setText(str(Path(selected).resolve()))
            self.sandbox_status.setText(f"🔒 Sandbox root: {self.project_path.text()}")

    def test_connection(self):
        try:
            client = OpenAI(base_url=self.base_url.text().strip(), api_key=self.api_key.text().strip() or "no-key", timeout=15, max_retries=0)
            models = client.models.list()
            ids = [m.id for m in models.data]
            self.log_view.appendPlainText("Connection OK. Models: " + (", ".join(ids) if ids else "(server returned no models)"))
            if ids and self.model.text().strip() in ("", "local-model"):
                self.model.setText(ids[0])
            QMessageBox.information(self, "Connection", "Подключение успешно. Сверь Model ID с журналом.")
        except Exception as exc:
            QMessageBox.critical(self, "Connection failed", f"{type(exc).__name__}: {exc}")

    def test_sandbox(self):
        result = run_sandbox_self_test()
        self.log_view.appendPlainText("\n=== SANDBOX SELF-TEST ===\n" + result["details"])
        summary = f"Passed: {result['passed']} | Failed: {result['failed']} | Skipped: {result['skipped']}"
        self.sandbox_status.setText(("✅ " if result["ok"] else "❌ ") + summary)
        (QMessageBox.information if result["ok"] else QMessageBox.warning)(self, "Sandbox test", summary + "\nПодробности записаны в журнал.")

    def test_tool_calling(self):
        self.start_agent("Вызови list_files ровно один раз для корня проекта: path='.', recursive=false. Затем кратко опиши результат, не угадывай содержимое.", force_tool="list_files", use_history=False)

    def send_message(self):
        prompt = self.prompt.text().strip()
        if prompt:
            self.prompt.clear()
            self.chat_view.append(f"<b>Вы:</b> {prompt}")
            self.start_agent(prompt)

    def new_chat(self):
        if self.worker and self.worker.isRunning():
            QMessageBox.warning(self, "Agent busy", "Сначала дождись завершения запроса или нажми Stop.")
            return
        self.conversation_history = []
        self.chat_view.clear()
        self.log_view.appendPlainText("=== New chat: conversation history cleared ===")

    def start_agent(self, prompt, force_tool=None, use_history=True):
        if self.worker and self.worker.isRunning():
            QMessageBox.warning(self, "Agent busy", "Дождись завершения текущего запроса или нажми Stop.")
            return
        root = Path(self.project_path.text())
        if not root.is_dir():
            QMessageBox.warning(self, "Project directory", "Выбери существующую папку проекта.")
            return
        self.save_limits()
        self.worker = AgentWorker(
            self.base_url.text().strip(), self.api_key.text().strip() or "no-key",
            self.model.text().strip(), str(root.resolve()), prompt, force_tool,
            settings=self.current_limits(),
            history=self.conversation_history if use_history else [],
        )
        self.worker.chat.connect(self.on_chat)
        self.worker.log.connect(self.log_view.appendPlainText)
        self.worker.failed.connect(lambda err: QMessageBox.critical(self, "Agent error", err))
        self.worker.finished_text.connect(lambda _: self.log_view.appendPlainText("Agent turn finished."))
        self.worker.progress.connect(self.on_progress)
        if use_history:
            self.worker.conversation_updated.connect(self.update_conversation_history)
        self.worker.write_approval_requested.connect(
            self.confirm_file_change, Qt.ConnectionType.BlockingQueuedConnection
        )
        self.worker.finished.connect(self.on_worker_finished)
        self.send_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.worker.start()

    def update_conversation_history(self, messages):
        # Copy the list so later worker-side mutations cannot alter GUI state.
        self.conversation_history = list(messages)

    def stop_agent(self):
        if self.worker and self.worker.isRunning():
            self.worker.requestInterruption()
            self.stop_btn.setEnabled(False)
            self.log_view.appendPlainText("Stop requested: waiting for the current streaming response to close…")

    def confirm_file_change(self, path, diff, exists):
        # The worker waits here for the GUI decision. No chat reply is needed.
        decision = FileChangeDialog.ask(self, path, diff, exists)
        if self.worker:
            self.worker.resolve_write_approval(decision)
        if decision == "apply":
            self.log_view.appendPlainText("WRITE APPROVED: " + path)
        elif decision == "reject":
            self.log_view.appendPlainText("WRITE DENIED: " + path)
        else:
            self.log_view.appendPlainText("WRITE CANCELLED: " + path)

    def on_progress(self, count, maximum):
        self.stop_btn.setText(f"Stop ({count}/{maximum} tool calls)")

    def on_worker_finished(self):
        self.send_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setText("Stop")

    def on_chat(self, role, content):
        safe = content.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")
        self.chat_view.append(f"<b>{role.title()}:</b> {safe}")
