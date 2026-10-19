from pathlib import Path
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFileDialog, QTextEdit, QPlainTextEdit, QMessageBox, QSplitter)
from openai import OpenAI
from .worker import AgentWorker
from .tools import run_sandbox_self_test

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__(); self.setWindowTitle("Local Coding Agent — Sandbox Edition"); self.resize(1050, 760)
        self.worker = None
        central = QWidget(); self.setCentralWidget(central); layout = QVBoxLayout(central)
        row = QHBoxLayout(); layout.addLayout(row)
        self.base_url = QLineEdit("http://127.0.0.1:8080/v1"); self.api_key = QLineEdit("no-key"); self.model = QLineEdit("local-model")
        for label, widget in [("Base URL", self.base_url), ("API key", self.api_key), ("Model ID", self.model)]:
            row.addWidget(QLabel(label)); row.addWidget(widget)
        project_row = QHBoxLayout(); layout.addLayout(project_row)
        self.project_path = QLineEdit(str(Path.home())); self.project_path.setReadOnly(True)
        project_row.addWidget(QLabel("Project directory")); project_row.addWidget(self.project_path, 1)
        self.browse_btn = QPushButton("Browse…"); self.browse_btn.clicked.connect(self.choose_project); project_row.addWidget(self.browse_btn)
        self.sandbox_status = QLabel("🔒 File tools are restricted to the selected project directory.")
        layout.addWidget(self.sandbox_status)
        buttons = QHBoxLayout(); layout.addLayout(buttons)
        self.connect_btn = QPushButton("Test connection"); self.connect_btn.clicked.connect(self.test_connection); buttons.addWidget(self.connect_btn)
        self.tool_btn = QPushButton("Test tool calling"); self.tool_btn.clicked.connect(self.test_tool_calling); buttons.addWidget(self.tool_btn)
        self.sandbox_btn = QPushButton("🔒 Test sandbox"); self.sandbox_btn.clicked.connect(self.test_sandbox); buttons.addWidget(self.sandbox_btn)
        split = QSplitter(Qt.Orientation.Vertical); layout.addWidget(split, 1)
        self.chat_view = QTextEdit(); self.chat_view.setReadOnly(True); self.chat_view.setPlaceholderText("Диалог с агентом")
        self.log_view = QPlainTextEdit(); self.log_view.setReadOnly(True); self.log_view.setPlaceholderText("Журнал вызовов инструментов и проверок безопасности")
        split.addWidget(self.chat_view); split.addWidget(self.log_view); split.setSizes([450, 250])
        input_row = QHBoxLayout(); layout.addLayout(input_row)
        self.prompt = QLineEdit(); self.prompt.setPlaceholderText("Например: изучи структуру проекта и кратко опиши его")
        self.prompt.returnPressed.connect(self.send_message); input_row.addWidget(self.prompt, 1)
        self.send_btn = QPushButton("Send"); self.send_btn.clicked.connect(self.send_message); input_row.addWidget(self.send_btn)
        self.clear_btn = QPushButton("Clear log"); self.clear_btn.clicked.connect(self.log_view.clear); input_row.addWidget(self.clear_btn)

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
        self.start_agent("Вызови list_files ровно один раз для корня проекта: path='.', recursive=false. Затем кратко опиши результат, не угадывай содержимое.", force_tool="list_files")

    def send_message(self):
        prompt = self.prompt.text().strip()
        if prompt:
            self.prompt.clear(); self.chat_view.append(f"<b>Вы:</b> {prompt}")
            self.start_agent(prompt)

    def start_agent(self, prompt, force_tool=None):
        if self.worker and self.worker.isRunning():
            QMessageBox.warning(self, "Agent busy", "Дождись завершения текущего запроса."); return
        root = Path(self.project_path.text())
        if not root.is_dir():
            QMessageBox.warning(self, "Project directory", "Выбери существующую папку проекта."); return
        self.worker = AgentWorker(self.base_url.text().strip(), self.api_key.text().strip() or "no-key", self.model.text().strip(), str(root.resolve()), prompt, force_tool)
        self.worker.chat.connect(self.on_chat); self.worker.log.connect(self.log_view.appendPlainText)
        self.worker.failed.connect(lambda err: QMessageBox.critical(self, "Agent error", err))
        self.worker.finished_text.connect(lambda _: self.log_view.appendPlainText("Agent turn finished."))
        self.worker.start()

    def on_chat(self, role, content):
        self.chat_view.append(f"<b>{role.title()}:</b> {content.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace(chr(10), '<br>')}")
