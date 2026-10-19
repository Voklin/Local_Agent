from __future__ import annotations

import json
from pathlib import Path

from openai import OpenAI
from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel,
    QLineEdit, QPushButton, QTextEdit, QFileDialog, QGroupBox, QMessageBox,
    QSplitter, QPlainTextEdit
)

from .worker import AgentWorker


class ConnectionWorker(QThread):
    done = Signal(str)
    failed = Signal(str)

    def __init__(self, base_url: str, api_key: str, parent=None):
        super().__init__(parent)
        self.base_url = base_url
        self.api_key = api_key

    def run(self):
        try:
            client = OpenAI(base_url=self.base_url, api_key=self.api_key or "no-key", timeout=12.0, max_retries=0)
            models = client.models.list()
            ids = [item.id for item in models.data]
            self.done.emit("Соединение успешно. Модели API: " + (", ".join(ids[:10]) if ids else "(сервер не перечислил модели)"))
        except Exception as exc:
            self.failed.emit(f"{type(exc).__name__}: {exc}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Local Coding Agent — v1")
        self.resize(1100, 760)
        self.project_root = Path.home()
        self.worker = None
        self.connection_worker = None

        central = QWidget()
        self.setCentralWidget(central)
        root_layout = QVBoxLayout(central)

        settings = QGroupBox("Подключение к модели")
        form = QFormLayout(settings)
        self.base_url = QLineEdit("http://127.0.0.1:8080/v1")
        self.api_key = QLineEdit("no-key")
        self.api_key.setEchoMode(QLineEdit.EchoMode.Password)
        self.model = QLineEdit("local-model")
        form.addRow("Base URL:", self.base_url)
        form.addRow("API key:", self.api_key)
        form.addRow("Model ID:", self.model)

        connection_row = QHBoxLayout()
        self.test_connection_btn = QPushButton("Test connection")
        self.test_connection_btn.clicked.connect(self.test_connection)
        connection_row.addWidget(self.test_connection_btn)
        self.connection_status = QLabel("Не подключено")
        connection_row.addWidget(self.connection_status, 1)
        form.addRow(connection_row)
        root_layout.addWidget(settings)

        project_row = QHBoxLayout()
        self.project_label = QLabel(f"Рабочая папка: {self.project_root}")
        self.project_label.setTextInteractionFlags(self.project_label.textInteractionFlags())
        self.choose_project_btn = QPushButton("Выбрать папку проекта…")
        self.choose_project_btn.clicked.connect(self.choose_project)
        project_row.addWidget(self.project_label, 1)
        project_row.addWidget(self.choose_project_btn)
        root_layout.addLayout(project_row)

        splitter = QSplitter()
        self.chat = QTextEdit()
        self.chat.setReadOnly(True)
        self.chat.setPlaceholderText("Здесь появятся сообщения и ответы агента.")
        self.log = QPlainTextEdit()
        self.log.setReadOnly(True)
        self.log.setPlaceholderText("Журнал вызовов инструментов.")
        splitter.addWidget(self.chat)
        splitter.addWidget(self.log)
        splitter.setSizes([650, 450])
        root_layout.addWidget(splitter, 1)

        self.prompt = QTextEdit()
        self.prompt.setMaximumHeight(100)
        self.prompt.setPlaceholderText("Например: изучи структуру проекта и найди, где реализован инвентарь…")
        root_layout.addWidget(self.prompt)

        actions = QHBoxLayout()
        self.send_btn = QPushButton("Отправить")
        self.send_btn.clicked.connect(self.send_message)
        self.test_tools_btn = QPushButton("Test tool calling")
        self.test_tools_btn.clicked.connect(self.test_tool_calling)
        self.clear_btn = QPushButton("Очистить журнал")
        self.clear_btn.clicked.connect(self.clear_log)
        actions.addWidget(self.send_btn)
        actions.addWidget(self.test_tools_btn)
        actions.addWidget(self.clear_btn)
        root_layout.addLayout(actions)

        self.append_chat("Система", "Выбери папку проекта, проверь подключение и нажми «Test tool calling».\nВ первой версии инструменты только читают файлы; запись и запуск команд добавим позже.")
        self.statusBar().showMessage("Готово")

    def choose_project(self):
        folder = QFileDialog.getExistingDirectory(self, "Выбрать папку проекта", str(self.project_root))
        if folder:
            self.project_root = Path(folder).resolve()
            self.project_label.setText(f"Рабочая папка: {self.project_root}")
            self.append_log(f"Рабочая папка: {self.project_root}")

    def append_chat(self, who: str, text: str):
        self.chat.append(f"<b>{who}</b><br>{text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace(chr(10), '<br>')}<br>")

    def append_log(self, text: str):
        self.log.appendPlainText(text)

    def config(self):
        return self.base_url.text().strip(), self.api_key.text().strip() or "no-key", self.model.text().strip()

    def test_connection(self):
        base_url, api_key, model = self.config()
        if not base_url or not model:
            QMessageBox.warning(self, "Не хватает настроек", "Укажи Base URL и Model ID.")
            return
        self.test_connection_btn.setEnabled(False)
        self.connection_status.setText("Проверка…")
        self.connection_worker = ConnectionWorker(base_url, api_key, self)
        self.connection_worker.done.connect(self.connection_ok)
        self.connection_worker.failed.connect(self.connection_failed)
        self.connection_worker.finished.connect(lambda: self.test_connection_btn.setEnabled(True))
        self.connection_worker.start()

    def connection_ok(self, text: str):
        self.connection_status.setText("Подключено")
        self.append_log(text)
        self.statusBar().showMessage("Соединение успешно")

    def connection_failed(self, text: str):
        self.connection_status.setText("Ошибка соединения")
        self.append_log(text)
        QMessageBox.critical(self, "Не удалось подключиться", text)

    def test_tool_calling(self):
        if self.worker and self.worker.isRunning():
            return
        prompt = "Используй инструмент list_files ровно один раз для корня проекта (path='.', recursive=false). Затем кратко опиши, что найдено. Не угадывай содержимое папки."
        self.start_agent(prompt, force_tool="list_files")

    def send_message(self):
        if self.worker and self.worker.isRunning():
            return
        text = self.prompt.toPlainText().strip()
        if not text:
            return
        self.prompt.clear()
        self.append_chat("Ты", text)
        self.start_agent(text)

    def start_agent(self, text: str, force_tool: str | None = None):
        base_url, api_key, model = self.config()
        if not base_url or not model:
            QMessageBox.warning(self, "Не хватает настроек", "Укажи Base URL и Model ID.")
            return
        self.send_btn.setEnabled(False)
        self.test_tools_btn.setEnabled(False)
        self.statusBar().showMessage("Агент работает…")
        self.worker = AgentWorker(base_url, api_key, model, self.project_root, text, force_tool, self)
        self.worker.log.connect(self.append_log)
        self.worker.answer.connect(self.agent_answer)
        self.worker.error.connect(self.agent_error)
        self.worker.finished.connect(self.agent_finished)
        self.worker.start()

    def agent_answer(self, text: str):
        self.append_chat("Агент", text)
        self.statusBar().showMessage("Ответ получен")

    def agent_error(self, text: str):
        self.append_log("ERROR: " + text)
        self.append_chat("Ошибка", text)
        self.statusBar().showMessage("Ошибка")

    def agent_finished(self):
        self.send_btn.setEnabled(True)
        self.test_tools_btn.setEnabled(True)

    def clear_log(self):
        self.log.clear()
