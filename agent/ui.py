from pathlib import Path
from html import escape

from PySide6.QtCore import Qt, QSettings, QSize, QRect, Signal
from PySide6.QtGui import (QFont, QKeySequence, QShortcut, QSyntaxHighlighter, QTextCharFormat, QColor, QPainter, QTextFormat)
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFileDialog, QTextBrowser, QPlainTextEdit, QMessageBox,
    QSplitter, QSpinBox, QGroupBox, QFormLayout, QDialog, QListWidget,
    QListWidgetItem, QInputDialog, QFrame, QToolButton, QComboBox, QTextEdit,
    QSizePolicy, QApplication, QCheckBox, QTabWidget, QTreeWidget, QTreeWidgetItem
)
from openai import OpenAI
from .worker import AgentWorker, DEFAULT_SETTINGS
from .tools import run_sandbox_self_test
from .chat_store import list_chats, create_chat, load_chat, save_chat, delete_chat, rename_chat, title_from_messages
from .project_memory import load_project_memory, save_project_memory, clear_project_memory
from .security import resolve_allowed_path, AccessDenied
from .editor_io import read_project_text, save_project_text, MAX_EDITOR_FILE_BYTES


APP_QSS = """
QMainWindow, QWidget { background: #111318; color: #e7e9ee; font-family: "Segoe UI"; font-size: 13px; }
QFrame#Sidebar { background: #17191f; border-right: 1px solid #292d36; }
QFrame#TopBar { background: #15171c; border-bottom: 1px solid #292d36; }
QFrame#Composer { background: #15171c; border-top: 1px solid #292d36; }
QTabWidget::pane { border: 1px solid #292d36; border-radius: 9px; background: #111318; top: -1px; }
QTabBar::tab { background: #171a20; color: #9ca4b2; border: 1px solid #292d36; padding: 9px 16px; margin-right: 3px; border-top-left-radius: 7px; border-top-right-radius: 7px; }
QTabBar::tab:selected { background: #222731; color: #f2f4f8; border-bottom-color: #3b82f6; }
QTreeWidget { background: #12151a; border: 1px solid #292d36; border-radius: 8px; alternate-background-color: #171a20; }
QTreeWidget::item { padding: 4px; }
QTreeWidget::item:selected { background: #26354a; color: #ffffff; }
QLabel#SectionTitle { color: #c6cbd4; font-weight: 700; letter-spacing: 1px; }
QLabel#EditorPath { color: #8f96a3; padding: 4px 8px; }
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


class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QSize(self.editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.editor.line_number_area_paint_event(event)


class CodeHighlighter(QSyntaxHighlighter):
    """Small dependency-free syntax highlighter for common source formats."""
    def __init__(self, document, suffix):
        super().__init__(document)
        self.rules = []
        self._rule(r"\b(def|class|return|if|elif|else|for|while|try|except|finally|with|as|import|from|pass|break|continue|yield|async|await|lambda|raise|in|is|not|and|or|True|False|None|self)\b", "#c792ea")
        self._rule(r"\b(const|let|var|function|new|this|export|default|extends|public|private|static|void|int|string|bool|null|undefined|true|false)\b", "#c792ea")
        self._rule(r"\b[0-9]+(\.[0-9]+)?\b", "#f78c6c")
        self._rule(r"\"([^\"\\]|\\.)*\"|'([^'\\]|\\.)*'", "#c3e88d")
        self._rule(r"#.*$", "#697386")
        self._rule(r"//.*$", "#697386")
        self._rule(r"/\*.*\*/", "#697386")
        self._rule(r"\b(print|len|range|open|str|int|float|list|dict|set|tuple|super|enumerate|zip|map|filter)\b", "#82aaff")
        self._rule(r"[{}\[\]()]", "#89ddff")
        self._rule(r"[=+*/<>!%-]", "#89ddff")
        self.suffix = suffix.lower()

    def _rule(self, pattern, color):
        fmt = QTextCharFormat(); fmt.setForeground(QColor(color))
        self.rules.append((pattern, fmt))

    def highlightBlock(self, text):
        for pattern, fmt in self.rules:
            from PySide6.QtCore import QRegularExpression
            expression = QRegularExpression(pattern)
            iterator = expression.globalMatch(text)
            while iterator.hasNext():
                match = iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)


class CodeEditor(QPlainTextEdit):
    """Editor with line numbers and a subtle current-line highlight."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.line_number_area = LineNumberArea(self)
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)
        self.update_line_number_area_width(0)
        self.highlight_current_line()
        self.setFont(QFont("Cascadia Code", 10))
        self.setTabStopDistance(4 * self.fontMetrics().horizontalAdvance(' '))
        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.setStyleSheet("QPlainTextEdit { background:#11151b; color:#d6deeb; border:0; border-radius:0; padding:8px; selection-background-color:#294b70; }")

    def line_number_area_width(self):
        digits = max(2, len(str(max(1, self.blockCount()))))
        return 14 + self.fontMetrics().horizontalAdvance('9') * digits

    def update_line_number_area_width(self, _):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height()))

    def line_number_area_paint_event(self, event):
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QColor("#171b22"))
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                painter.setPen(QColor("#687386"))
                painter.drawText(0, top, self.line_number_area.width() - 6, self.fontMetrics().height(), Qt.AlignmentFlag.AlignRight, str(block_number + 1))
            block = block.next(); top = bottom; bottom = top + int(self.blockBoundingRect(block).height())
            block_number += 1

    def highlight_current_line(self):
        selections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            selection.format.setBackground(QColor("#1a2230"))
            selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
            selection.cursor = self.textCursor(); selection.cursor.clearSelection()
            selections.append(selection)
        self.setExtraSelections(selections)


class FileChangeDialog(QDialog):
    def __init__(self, parent, path, diff, exists):
        super().__init__(parent)
        self.setWindowTitle("Подтверждение изменения файла")
        self.setModal(True)
        self.resize(1000, 720)
        layout = QVBoxLayout(self)
        action = "Перезаписать существующий файл" if exists else "Создать новый файл"
        title = QLabel(f"<b>{action}</b>")
        title.setStyleSheet("font-size: 15px;")
        layout.addWidget(title)
        path_label = QLabel(f"Файл: <code>{escape(path)}</code><br><span style='color:#8f96a3'>Проверь diff перед записью. Batch-действия действуют только на текущий запуск агента.</span>")
        path_label.setWordWrap(True)
        layout.addWidget(path_label)
        diff_view = QTextBrowser()
        diff_view.setOpenExternalLinks(False)
        diff_view.setHtml(MainWindow.format_diff_html(diff))
        layout.addWidget(diff_view, 1)
        buttons = QHBoxLayout()
        buttons.addStretch(1)
        cancel = QPushButton("Отмена")
        reject = QPushButton("Отклонить")
        reject_all = QPushButton("Отклонить всё")
        apply_all = QPushButton("Применить всё")
        apply = QPushButton("Применить")
        apply.setObjectName("Primary")
        cancel.clicked.connect(lambda: self.done(3))
        reject.clicked.connect(lambda: self.done(2))
        reject_all.clicked.connect(lambda: self.done(5))
        apply_all.clicked.connect(lambda: self.done(4))
        apply.clicked.connect(lambda: self.done(1))
        for button in (cancel, reject, reject_all, apply_all, apply): buttons.addWidget(button)
        layout.addLayout(buttons)

    @staticmethod
    def ask(parent, path, diff, exists):
        result = FileChangeDialog(parent, path, diff, exists).exec()
        return {1: "apply", 2: "reject", 3: "cancel", 4: "apply_all", 5: "reject_all"}.get(result, "cancel")


class SettingsDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Настройки агента")
        self.resize(520, 380)
        self.parent_window = parent
        layout = QVBoxLayout(self)

        connection = QGroupBox("Локальный сервер / LM Studio")
        cf = QFormLayout(connection)
        self.base_url = QLineEdit(parent.base_url.text())
        self.api_key = QLineEdit(parent.api_key.text())
        self.api_key.setEchoMode(QLineEdit.EchoMode.Password)
        model_row = QHBoxLayout()
        self.model_combo = QComboBox()
        self.model_combo.setEditable(False)
        current_model = parent.model.currentText().strip()
        if current_model:
            self.model_combo.addItem(current_model)
        self.model_combo.setCurrentText(current_model)
        refresh = QPushButton("↻ Обновить")
        refresh.clicked.connect(self.refresh_models)
        model_row.addWidget(self.model_combo, 1); model_row.addWidget(refresh)
        cf.addRow("URL:", self.base_url)
        cf.addRow("API key:", self.api_key)
        cf.addRow("Модель:", model_row)
        hint = QLabel("Список моделей загружается через OpenAI-совместимый endpoint /models. Для LM Studio обычно используется http://127.0.0.1:1234/v1.")
        hint.setWordWrap(True); hint.setObjectName("Muted")
        cf.addRow("", hint)
        layout.addWidget(connection)

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
        self.auto_memory = QCheckBox("Автоматически обновлять память проекта после успешного ответа")
        self.auto_memory.setChecked(parent.settings_store.value("memory/auto_update", True, type=bool))
        layout.addWidget(self.auto_memory)
        note = QLabel("Память хранится отдельно для каждого проекта. Автообновление не сохраняет сырой вывод инструментов или содержимое файлов. Система разрешений и sandbox остаются без изменений.")
        note.setWordWrap(True); note.setObjectName("Muted"); layout.addWidget(note)
        buttons = QHBoxLayout(); buttons.addStretch(1)
        cancel = QPushButton("Отмена"); save = QPushButton("Сохранить"); save.setObjectName("Primary")
        cancel.clicked.connect(self.reject); save.clicked.connect(self.accept)
        buttons.addWidget(cancel); buttons.addWidget(save); layout.addLayout(buttons)

    def refresh_models(self):
        try:
            client = OpenAI(base_url=self.base_url.text().strip(), api_key=self.api_key.text().strip() or "no-key", timeout=8, max_retries=0)
            ids = sorted({str(m.id) for m in client.models.list().data if getattr(m, "id", None)})
            current = self.model_combo.currentText().strip()
            self.model_combo.blockSignals(True)
            self.model_combo.clear()
            self.model_combo.addItems(ids)
            if current and current not in ids:
                self.model_combo.addItem(current)
            if current:
                self.model_combo.setCurrentText(current)
            elif ids:
                self.model_combo.setCurrentIndex(0)
            self.model_combo.blockSignals(False)
            if ids:
                self.parent_window.log_view.appendPlainText("Модели обновлены: " + ", ".join(ids))
            else:
                QMessageBox.warning(self, "Модели", "Сервер ответил, но список моделей пуст.")
        except Exception as exc:
            QMessageBox.critical(self, "Ошибка получения моделей", f"Не удалось получить список моделей.\n\n{type(exc).__name__}: {exc}")

    def values(self):
        return {k: v.value() for k, v in self.controls.items()}

    def auto_memory_enabled(self):
        return self.auto_memory.isChecked()


class ProjectMemoryDialog(QDialog):
    """Review and edit the structured memory for the selected project."""
    def __init__(self, parent, project_root):
        super().__init__(parent)
        self.project_root = project_root
        self.setWindowTitle("Память проекта")
        self.resize(760, 680)
        layout = QVBoxLayout(self)
        info = QLabel("Память хранится отдельно от файлов проекта. Здесь можно проверить, исправить или полностью очистить её. Не добавляйте пароли и токены.")
        info.setWordWrap(True); info.setObjectName("Muted"); layout.addWidget(info)
        self.editor = QPlainTextEdit()
        self.editor.setLineWrapMode(QPlainTextEdit.LineWrapMode.WidgetWidth)
        self.editor.setPlainText(__import__("json").dumps(load_project_memory(project_root), ensure_ascii=False, indent=2))
        layout.addWidget(self.editor, 1)
        buttons = QHBoxLayout()
        clear = QPushButton("Очистить память")
        save = QPushButton("Сохранить память"); save.setObjectName("Primary")
        close = QPushButton("Закрыть")
        clear.clicked.connect(self.clear_memory); save.clicked.connect(self.save_memory); close.clicked.connect(self.reject)
        buttons.addWidget(clear); buttons.addStretch(1); buttons.addWidget(close); buttons.addWidget(save); layout.addLayout(buttons)

    def save_memory(self):
        import json
        try:
            data = json.loads(self.editor.toPlainText())
            saved = save_project_memory(self.project_root, data)
            self.editor.setPlainText(json.dumps(saved, ensure_ascii=False, indent=2))
            QMessageBox.information(self, "Память", "Память проекта сохранена.")
        except (json.JSONDecodeError, ValueError, OSError) as exc:
            QMessageBox.warning(self, "Не удалось сохранить", str(exc))

    def clear_memory(self):
        if QMessageBox.question(self, "Очистить память", "Удалить долговременную память только для этого проекта? История чатов не будет удалена.", QMessageBox.Yes | QMessageBox.No, QMessageBox.No) != QMessageBox.Yes:
            return
        clear_project_memory(self.project_root)
        from .project_memory import empty_memory
        import json
        self.editor.setPlainText(json.dumps(empty_memory(self.project_root), ensure_ascii=False, indent=2))
        QMessageBox.information(self, "Память", "Память проекта очищена. История чатов сохранена.")


class SideBySideDiffDialog(QDialog):
    """Safe read-only side-by-side view of a unified diff.

    This dialog intentionally works only with the diff already produced by the
    existing change pipeline. It never writes files and does not touch sandbox
    or approval state.
    """
    def __init__(self, parent, path, diff):
        super().__init__(parent)
        self.setWindowTitle(f"Сравнение изменений — {Path(path).name}")
        self.resize(1200, 760)
        layout = QVBoxLayout(self)

        header = QHBoxLayout()
        title = QLabel(str(path))
        title.setObjectName("EditorPath")
        header.addWidget(title, 1)
        info = QLabel("Только просмотр · файл не изменяется")
        info.setObjectName("Muted")
        header.addWidget(info)
        layout.addLayout(header)

        toolbar = QHBoxLayout()
        self.sync_scroll = QCheckBox("Синхронная прокрутка")
        self.sync_scroll.setChecked(True)
        self.sync_scroll.setToolTip("Прокручивать оригинал и новую версию одновременно")
        toolbar.addWidget(self.sync_scroll)
        self.change_position = QLabel("Изменения: 0")
        self.change_position.setObjectName("Muted")
        toolbar.addWidget(self.change_position)
        toolbar.addStretch(1)
        self.prev_change_btn = QPushButton("↑ Предыдущее")
        self.next_change_btn = QPushButton("Следующее ↓")
        self.prev_change_btn.setEnabled(False)
        self.next_change_btn.setEnabled(False)
        toolbar.addWidget(self.prev_change_btn)
        toolbar.addWidget(self.next_change_btn)
        layout.addLayout(toolbar)

        panes = QSplitter(Qt.Horizontal)
        self.left = QPlainTextEdit()
        self.right = QPlainTextEdit()
        for editor in (self.left, self.right):
            editor.setReadOnly(True)
            editor.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
            editor.setFont(QFont("Consolas", 10))
            editor.verticalScrollBar().valueChanged.connect(self._scroll_from_editor)
        self.left.setPlaceholderText("Оригинал")
        self.right.setPlaceholderText("Предложенная версия")
        panes.addWidget(self.left)
        panes.addWidget(self.right)
        panes.setSizes([1, 1])
        layout.addWidget(panes, 1)

        self._syncing_scroll = False
        self._changed_groups = []
        self._current_change = -1
        self.prev_change_btn.clicked.connect(lambda: self._go_to_change(-1))
        self.next_change_btn.clicked.connect(lambda: self._go_to_change(1))

        self._populate(diff)
        close_btn = QPushButton("Закрыть")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn, 0, Qt.AlignmentFlag.AlignRight)

    def _populate(self, diff):
        left_lines, right_lines = [], []
        for raw in (diff or "").splitlines():
            if raw.startswith("diff ") or raw.startswith("index ") or raw.startswith("--- ") or raw.startswith("+++ "):
                continue
            if raw.startswith("@@"):
                marker = raw
                left_lines.append(marker)
                right_lines.append(marker)
            elif raw.startswith("-"):
                left_lines.append(raw[1:])
                right_lines.append("")
            elif raw.startswith("+"):
                left_lines.append("")
                right_lines.append(raw[1:])
            elif raw.startswith(" "):
                value = raw[1:]
                left_lines.append(value)
                right_lines.append(value)
            elif raw.startswith("\\ No newline"):
                # Metadata line; show it on both sides without trying to patch.
                left_lines.append(raw)
                right_lines.append(raw)
            elif raw:
                left_lines.append(raw)
                right_lines.append(raw)

        self.left.setPlainText("\n".join(left_lines))
        self.right.setPlainText("\n".join(right_lines))
        self._highlight_changed_lines(left_lines, right_lines)

    @staticmethod
    def _line_selection(editor, line_number, background):
        """Create a read-only line highlight using the supported Qt API."""
        selection = QTextEdit.ExtraSelection()
        selection.format.setBackground(QColor(background))
        selection.format.setProperty(QTextFormat.FullWidthSelection, True)
        cursor = editor.textCursor()
        cursor.movePosition(cursor.MoveOperation.Start)
        cursor.movePosition(cursor.MoveOperation.Down, cursor.MoveMode.MoveAnchor, line_number)
        selection.cursor = cursor
        return selection

    def _highlight_changed_lines(self, left_lines, right_lines):
        """Highlight deleted/added lines and build navigation groups."""
        left_selections = []
        right_selections = []
        changed = []

        for index in range(max(len(left_lines), len(right_lines))):
            left_value = left_lines[index] if index < len(left_lines) else ""
            right_value = right_lines[index] if index < len(right_lines) else ""
            if left_value and not right_value:
                left_selections.append(self._line_selection(self.left, index, "#4a2529"))
                changed.append(index)
            elif right_value and not left_value:
                right_selections.append(self._line_selection(self.right, index, "#1f4030"))
                changed.append(index)

        self.left.setExtraSelections(left_selections)
        self.right.setExtraSelections(right_selections)

        # Collapse consecutive changed rows into navigation groups.
        groups = []
        for line in sorted(set(changed)):
            if not groups or line > groups[-1][-1] + 1:
                groups.append([line])
            else:
                groups[-1].append(line)
        self._changed_groups = groups
        self._current_change = -1
        count = len(groups)
        self.change_position.setText(f"Изменения: {count}")
        self.prev_change_btn.setEnabled(count > 0)
        self.next_change_btn.setEnabled(count > 0)

    def _scroll_from_editor(self, value):
        """Keep both panes vertically aligned without recursive signal loops."""
        if self._syncing_scroll or not self.sync_scroll.isChecked():
            return
        sender = self.sender()
        target = self.right if sender is self.left else self.left
        self._syncing_scroll = True
        try:
            target.verticalScrollBar().setValue(value)
        finally:
            self._syncing_scroll = False

    def _go_to_change(self, direction):
        if not self._changed_groups:
            return
        self._current_change = (self._current_change + direction) % len(self._changed_groups)
        line = self._changed_groups[self._current_change][0]
        self.left.verticalScrollBar().setValue(line)
        self.right.verticalScrollBar().setValue(line)
        self.change_position.setText(
            f"Изменение {self._current_change + 1}/{len(self._changed_groups)}"
        )


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
        self.change_records = []
        self._create_hidden_connection_fields()
        self._build_ui()
        self._bind_shortcuts()
        self.refresh_chat_list()
        saved_chat_id = self.settings_store.value("chat/current_id", "")
        if saved_chat_id:
            chat = load_chat(str(saved_chat_id))
            if chat:
                self._load_chat_record(chat, announce=False)
        self._set_status("Готов", "ready")
        # Populate the model selector automatically from the configured OpenAI-compatible server.
        self.refresh_models(show_message=False)
        self.refresh_project_tree()

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
        self.model_selector = QComboBox()
        self.model_selector.setMinimumWidth(180)
        self.model_selector.setToolTip("Модель локального сервера")
        self.model_selector.addItems([self.model.itemText(i) for i in range(self.model.count())])
        self.model_selector.setCurrentText(self.model.currentText())
        self.model_selector.currentTextChanged.connect(self._on_model_selected)
        layout.addWidget(QLabel("Модель:")); layout.addWidget(self.model_selector)
        refresh_models = QToolButton(); refresh_models.setText("↻"); refresh_models.setToolTip("Получить список моделей с локального сервера"); refresh_models.clicked.connect(lambda: self.refresh_models(show_message=True)); layout.addWidget(refresh_models)
        editor_btn = QToolButton(); editor_btn.setText("</>"); editor_btn.setToolTip("Открыть редактор кода · Ctrl+Shift+E"); editor_btn.clicked.connect(self.open_editor_tab); layout.addWidget(editor_btn)
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
        choose = QPushButton("Выбрать папку"); choose.clicked.connect(self.choose_project); p.addWidget(choose)
        memory_btn = QPushButton("Память проекта…"); memory_btn.clicked.connect(self.open_project_memory); p.addWidget(memory_btn); layout.addWidget(project_card)
        return panel

    def _build_center(self):
        self.center_tabs = QTabWidget(); self.center_tabs.setDocumentMode(True)
        self.chat_panel = self._build_chat_panel()
        self.editor_workspace = self._build_editor_workspace()
        self.center_tabs.addTab(self.chat_panel, "◉  Чат")
        self.center_tabs.addTab(self.editor_workspace, "</>  Редактор")
        return self.center_tabs

    def _build_chat_panel(self):
        panel = QWidget(); layout = QVBoxLayout(panel); layout.setContentsMargins(14, 14, 14, 14)
        self.chat_view = QTextBrowser(); self.chat_view.setOpenExternalLinks(False); self.chat_view.setPlaceholderText("Начните диалог с агентом…"); layout.addWidget(self.chat_view, 1)
        self.log_toggle = QToolButton(); self.log_toggle.setText("⌄  Журнал инструментов"); self.log_toggle.setCheckable(True); self.log_toggle.setChecked(False); layout.addWidget(self.log_toggle)
        self.log_view = QPlainTextEdit(); self.log_view.setReadOnly(True); self.log_view.setMaximumHeight(220); self.log_view.hide(); layout.addWidget(self.log_view)
        self.log_toggle.toggled.connect(self.log_view.setVisible)
        return panel

    def _build_editor_workspace(self):
        panel = QWidget(); outer = QVBoxLayout(panel); outer.setContentsMargins(10, 10, 10, 10); outer.setSpacing(8)
        toolbar = QFrame(); toolbar.setObjectName("Card"); row = QHBoxLayout(toolbar); row.setContentsMargins(10, 7, 10, 7)
        heading = QLabel("WORKSPACE / EDITOR"); heading.setObjectName("SectionTitle"); row.addWidget(heading); row.addStretch(1)
        self.editor_path_label = QLabel("Файл не открыт"); self.editor_path_label.setObjectName("EditorPath"); row.addWidget(self.editor_path_label, 1)
        self.editor_find = QLineEdit(); self.editor_find.setPlaceholderText("Найти в файле…"); self.editor_find.setMaximumWidth(190); self.editor_find.returnPressed.connect(self.find_in_editor); row.addWidget(self.editor_find)
        find_btn = QToolButton(); find_btn.setText("⌕"); find_btn.setToolTip("Найти следующий результат"); find_btn.clicked.connect(self.find_in_editor); row.addWidget(find_btn)
        save_btn = QPushButton("Сохранить  Ctrl+S"); save_btn.setObjectName("Primary"); save_btn.clicked.connect(self.save_current_editor); row.addWidget(save_btn)
        refresh_btn = QToolButton(); refresh_btn.setText("↻"); refresh_btn.setToolTip("Обновить дерево файлов"); refresh_btn.clicked.connect(self.refresh_project_tree); row.addWidget(refresh_btn)
        outer.addWidget(toolbar)
        splitter = QSplitter(Qt.Horizontal); splitter.setChildrenCollapsible(False)
        file_panel = QFrame(); file_panel.setObjectName("Card"); file_layout = QVBoxLayout(file_panel); file_layout.setContentsMargins(8, 8, 8, 8)
        file_head = QHBoxLayout(); file_head.addWidget(QLabel("ФАЙЛЫ ПРОЕКТА")); file_head.addStretch(1)
        self.file_count_label = QLabel("0"); self.file_count_label.setObjectName("Status"); file_head.addWidget(self.file_count_label); file_layout.addLayout(file_head)
        self.project_tree = QTreeWidget(); self.project_tree.setHeaderHidden(True); self.project_tree.setIndentation(15); self.project_tree.setAnimated(True); self.project_tree.setUniformRowHeights(True); self.project_tree.itemActivated.connect(self.on_project_tree_double_click); file_layout.addWidget(self.project_tree, 1)
        tree_buttons = QHBoxLayout(); open_btn = QPushButton("Открыть файл…"); open_btn.clicked.connect(self.open_file_dialog); tree_buttons.addWidget(open_btn); file_layout.addLayout(tree_buttons)
        splitter.addWidget(file_panel)
        editor_panel = QFrame(); editor_panel.setObjectName("Card"); editor_layout = QVBoxLayout(editor_panel); editor_layout.setContentsMargins(6, 6, 6, 6)
        self.editor_tabs = QTabWidget(); self.editor_tabs.setDocumentMode(True); self.editor_tabs.setTabsClosable(True); self.editor_tabs.tabCloseRequested.connect(self.close_editor_tab); self.editor_tabs.currentChanged.connect(self.on_editor_tab_changed); editor_layout.addWidget(self.editor_tabs, 1)
        self.editor_empty = QLabel("Выберите файл в дереве проекта\n\n• Подсветка синтаксиса\n• Номера строк\n• Ctrl+S — сохранить\n• Поиск по открытому файлу\n\nРедактор работает только внутри выбранной папки проекта.")
        self.editor_empty.setAlignment(Qt.AlignmentFlag.AlignCenter); self.editor_empty.setObjectName("Muted")
        self.editor_tabs.addTab(self.editor_empty, "Старт")
        splitter.addWidget(editor_panel); splitter.setSizes([250, 720]); outer.addWidget(splitter, 1)
        self.editor_status = QLabel("Готов к работе · файлы не изменены"); self.editor_status.setObjectName("Muted"); outer.addWidget(self.editor_status)
        return panel

    def _build_inspector(self):
        panel = QFrame(); panel.setObjectName("Sidebar"); panel.setMinimumWidth(300); panel.setMaximumWidth(460)
        layout = QVBoxLayout(panel); layout.setContentsMargins(12, 14, 12, 14)
        title = QLabel("РАБОЧАЯ ОБЛАСТЬ"); title.setObjectName("Muted"); layout.addWidget(title)
        card = QFrame(); card.setObjectName("InspectorCard"); c = QVBoxLayout(card)
        self.inspector_project = QLabel("Проект не выбран"); self.inspector_project.setWordWrap(True); c.addWidget(self.inspector_project)
        self.inspector_model = QLabel("Модель: local-model"); self.inspector_model.setObjectName("Muted"); c.addWidget(self.inspector_model)
        self.inspector_sandbox = QLabel("🔒 Sandbox включён\nФайлы доступны только внутри выбранного проекта."); self.inspector_sandbox.setWordWrap(True); c.addWidget(self.inspector_sandbox)
        layout.addWidget(card)

        changes = QFrame(); changes.setObjectName("InspectorCard"); ch = QVBoxLayout(changes)
        header = QHBoxLayout(); header.addWidget(QLabel("ЦЕНТР ИЗМЕНЕНИЙ")); header.addStretch(1)
        self.changes_count = QLabel("0"); self.changes_count.setObjectName("Status"); header.addWidget(self.changes_count); ch.addLayout(header)
        self.changes_list = QListWidget(); self.changes_list.setMinimumHeight(170); self.changes_list.itemClicked.connect(self.show_change_diff); ch.addWidget(self.changes_list)
        self.change_diff_view = QTextBrowser(); self.change_diff_view.setPlaceholderText("Выберите файл, чтобы посмотреть diff"); self.change_diff_view.setMinimumHeight(220); ch.addWidget(self.change_diff_view, 1)
        row = QHBoxLayout()
        open_diff_file = QPushButton("Открыть файл"); open_diff_file.clicked.connect(self.open_selected_change_in_editor)
        compare = QPushButton("Сравнить"); compare.clicked.connect(self.open_selected_diff_viewer)
        clear = QPushButton("Очистить"); clear.clicked.connect(self.clear_changes)
        copy_btn = QPushButton("Копировать diff"); copy_btn.clicked.connect(self.copy_selected_diff)
        row.addWidget(open_diff_file); row.addWidget(compare); row.addWidget(clear); row.addWidget(copy_btn); ch.addLayout(row)
        layout.addWidget(changes, 1)

        tools = QFrame(); tools.setObjectName("InspectorCard"); t = QVBoxLayout(tools); t.addWidget(QLabel("ДИАГНОСТИКА"))
        connection = QPushButton("Проверить подключение"); connection.clicked.connect(self.test_connection); t.addWidget(connection)
        tool_test = QPushButton("Проверить tool calling"); tool_test.clicked.connect(self.test_tool_calling); t.addWidget(tool_test)
        sandbox = QPushButton("🔒 Проверить sandbox"); sandbox.clicked.connect(self.test_sandbox); t.addWidget(sandbox)
        layout.addWidget(tools)
        return panel

    def _build_composer(self):
        panel = QFrame(); panel.setObjectName("Composer"); layout = QHBoxLayout(panel); layout.setContentsMargins(14, 10, 14, 10)
        self.prompt = QPlainTextEdit(); self.prompt.setPlaceholderText("Опишите задачу…  Enter — отправить, Shift+Enter — новая строка"); self.prompt.setFixedHeight(72); layout.addWidget(self.prompt, 1)
        buttons = QVBoxLayout()
        self.send_btn = QPushButton("Отправить  ↵"); self.send_btn.setObjectName("Primary"); self.send_btn.clicked.connect(self.send_message); buttons.addWidget(self.send_btn)
        self.stop_btn = QPushButton("Остановить"); self.stop_btn.setObjectName("Danger"); self.stop_btn.setEnabled(False); self.stop_btn.clicked.connect(self.stop_agent); buttons.addWidget(self.stop_btn)
        layout.addLayout(buttons)
        return panel

    def open_editor_tab(self):
        self.center_tabs.setCurrentWidget(self.editor_workspace)
        self.refresh_project_tree()
        if self.editor_tabs.currentWidget() is self.editor_empty:
            self.editor_status.setText("Выберите файл в дереве проекта или нажмите «Открыть файл…»")

    def _project_root(self):
        return Path(self.project_path.text()).expanduser().resolve(strict=True)

    def refresh_project_tree(self):
        if not hasattr(self, "project_tree"):
            return
        self.project_tree.clear(); count = 0
        try:
            root = self._project_root()
            root_item = QTreeWidgetItem([f"📁  {root.name or str(root)}"]); root_item.setData(0, Qt.ItemDataRole.UserRole, str(root)); root_item.setExpanded(True); self.project_tree.addTopLevelItem(root_item)
            ignored = {".git", ".venv", "venv", "__pycache__", "node_modules", ".pytest_cache", "dist", "build"}
            max_entries, max_depth = 2500, 5
            def populate(parent_item, directory, depth):
                nonlocal count
                if depth > max_depth or count >= max_entries: return
                try: children = sorted(directory.iterdir(), key=lambda item: (not item.is_dir(), item.name.lower()))
                except OSError: return
                for child in children:
                    if count >= max_entries: break
                    if child.name in ignored: continue
                    try:
                        safe = resolve_allowed_path(root, child, must_exist=True)
                    except (AccessDenied, OSError, RuntimeError):
                        continue
                    # Never follow a symlink to a location outside the project root.
                    if child.is_symlink() and safe == root: continue
                    is_dir = safe.is_dir()
                    node = QTreeWidgetItem([("📁  " if is_dir else "   ") + child.name])
                    node.setData(0, Qt.ItemDataRole.UserRole, str(safe)); node.setToolTip(0, str(safe)); parent_item.addChild(node); count += 1
                    if is_dir and depth < max_depth: populate(node, safe, depth + 1)
            populate(root_item, root, 1)
            self.file_count_label.setText(str(count))
            if count >= max_entries: self.editor_status.setText(f"Показаны первые {max_entries} элементов; скрытые служебные каталоги пропущены.")
            else: self.editor_status.setText(f"Проект: {root.name} · {count} элементов")
        except (OSError, RuntimeError, AccessDenied) as exc:
            self.file_count_label.setText("—"); self.editor_status.setText(f"Не удалось прочитать дерево проекта: {exc}")

    def on_project_tree_double_click(self, item, _column=0):
        raw = item.data(0, Qt.ItemDataRole.UserRole)
        if not raw: return
        try:
            root = self._project_root(); path = resolve_allowed_path(root, raw, must_exist=True)
            if path.is_dir():
                return
            self.open_project_file(path)
        except (OSError, RuntimeError, AccessDenied) as exc:
            QMessageBox.warning(self, "Доступ к файлу", str(exc))

    def open_file_dialog(self):
        try: root = self._project_root()
        except (OSError, RuntimeError, AccessDenied) as exc:
            QMessageBox.warning(self, "Проект", str(exc)); return
        selected, _ = QFileDialog.getOpenFileName(self, "Открыть файл проекта", str(root), "Все файлы (*.*)")
        if not selected: return
        try:
            path = resolve_allowed_path(root, selected, must_exist=True)
            if not path.is_file(): raise ValueError("Выбранный путь не является файлом.")
            self.open_project_file(path)
        except (OSError, RuntimeError, AccessDenied, ValueError) as exc:
            QMessageBox.warning(self, "Файл вне проекта", f"Можно открывать только файлы внутри выбранного проекта.\n\n{exc}")

    def open_project_file(self, path):
        root = self._project_root()
        path = resolve_allowed_path(root, path, must_exist=True)
        if not path.is_file(): raise ValueError("Путь не является файлом.")
        if path.stat().st_size > MAX_EDITOR_FILE_BYTES:
            QMessageBox.warning(self, "Слишком большой файл", "Редактор пока открывает текстовые файлы размером до 2 МБ."); return
        for i in range(self.editor_tabs.count()):
            widget = self.editor_tabs.widget(i)
            if getattr(widget, "file_path", None) == path:
                self.editor_tabs.setCurrentIndex(i); self.center_tabs.setCurrentWidget(self.editor_workspace); return
        try:
            path, text = read_project_text(root, path)
            if self.editor_tabs.count() == 1 and self.editor_tabs.widget(0) is self.editor_empty:
                self.editor_tabs.removeTab(0)
                self.editor_empty.setParent(None)
            editor = CodeEditor()
            editor.file_path = path
            editor.saved_text = text
            editor.setPlainText(text)
            editor.document().setModified(False)
            editor.highlighter = CodeHighlighter(editor.document(), path.suffix)
            editor.document().modificationChanged.connect(
                lambda modified, e=editor: self.update_editor_tab_title(e, modified)
            )
            index = self.editor_tabs.addTab(editor, path.name)
            self.editor_tabs.setTabToolTip(index, str(path))
            self.editor_tabs.setCurrentIndex(index)
            self.center_tabs.setCurrentWidget(self.editor_workspace)
            self.update_editor_tab_title(editor, False)
            self.on_editor_tab_changed(index)
            self.editor_status.setText(f"Открыт {path.relative_to(root)} · UTF-8")
        except UnicodeDecodeError:
            QMessageBox.warning(self, "Не текстовый файл", "Файл не удалось прочитать как UTF-8. Бинарные файлы редактор не открывает.")
            self.editor_status.setText(f"Не удалось открыть {path.name}: файл не в UTF-8")
        except (OSError, RuntimeError, AccessDenied, ValueError) as exc:
            QMessageBox.warning(self, "Ошибка открытия файла", str(exc))
            self.editor_status.setText(f"Не удалось открыть {path.name}: {exc}")
        except Exception as exc:
            # Keep editor failures visible instead of silently leaving the previous tab selected.
            QMessageBox.critical(self, "Ошибка редактора", f"Не удалось открыть файл:\n{path}\n\n{type(exc).__name__}: {exc}")
            self.editor_status.setText(f"Ошибка редактора при открытии {path.name}: {type(exc).__name__}")

    def current_code_editor(self):
        widget = self.editor_tabs.currentWidget() if hasattr(self, "editor_tabs") else None
        return widget if isinstance(widget, CodeEditor) else None

    def update_editor_tab_title(self, editor, modified=None):
        if editor not in [self.editor_tabs.widget(i) for i in range(self.editor_tabs.count())]: return
        if modified is None: modified = editor.document().isModified()
        idx = self.editor_tabs.indexOf(editor)
        if idx >= 0:
            self.editor_tabs.setTabText(idx, editor.file_path.name + (" •" if modified else ""))
            self.editor_tabs.setTabToolTip(idx, str(editor.file_path) + (" (есть несохранённые изменения)" if modified else ""))
        if self.current_code_editor() is editor:
            self.editor_path_label.setText(str(editor.file_path))
            self.editor_status.setText("Есть несохранённые изменения" if modified else f"Сохранено · {editor.file_path.name}")

    def on_editor_tab_changed(self, index):
        widget = self.editor_tabs.widget(index) if index >= 0 else None
        if isinstance(widget, CodeEditor):
            self.editor_path_label.setText(str(widget.file_path)); self.update_editor_tab_title(widget)
        else:
            self.editor_path_label.setText("Файл не открыт")

    def save_current_editor(self):
        editor = self.current_code_editor()
        if not editor: return
        try:
            root = self._project_root(); path = save_project_text(root, editor.file_path, editor.toPlainText())
            editor.saved_text = editor.toPlainText(); editor.document().setModified(False)
            self.update_editor_tab_title(editor, False); self.editor_status.setText(f"Сохранено · {path.relative_to(root)}")
            self.log_view.appendPlainText(f"EDITOR SAVE: {path}")
        except (OSError, RuntimeError, AccessDenied, ValueError) as exc:
            QMessageBox.warning(self, "Не удалось сохранить файл", str(exc))

    def close_editor_tab(self, index):
        editor = self.editor_tabs.widget(index)
        if not isinstance(editor, CodeEditor): return
        if editor.document().isModified():
            answer = QMessageBox.question(self, "Несохранённые изменения", f"Сохранить изменения в {editor.file_path.name} перед закрытием?", QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel, QMessageBox.Save)
            if answer == QMessageBox.Cancel: return
            if answer == QMessageBox.Save:
                self.editor_tabs.setCurrentIndex(index); self.save_current_editor()
                if editor.document().isModified(): return
        self.editor_tabs.removeTab(index); editor.deleteLater()
        if self.editor_tabs.count() == 0:
            self.editor_tabs.addTab(self.editor_empty, "Старт")
        self.on_editor_tab_changed(self.editor_tabs.currentIndex())

    def refresh_open_editors_from_disk(self):
        for i in range(self.editor_tabs.count()):
            editor = self.editor_tabs.widget(i)
            if not isinstance(editor, CodeEditor) or editor.document().isModified(): continue
            try:
                root = self._project_root(); path, text = read_project_text(root, editor.file_path)
                if text != editor.toPlainText():
                    cursor = editor.textCursor(); pos = cursor.position(); editor.setPlainText(text); cursor.setPosition(min(pos, len(text))); editor.setTextCursor(cursor); editor.document().setModified(False); editor.saved_text = text
            except (OSError, RuntimeError, AccessDenied, UnicodeDecodeError, ValueError):
                continue
        self.refresh_project_tree()

    def open_selected_change_in_editor(self):
        item = self.changes_list.currentItem()
        if not item: return
        record = item.data(Qt.ItemDataRole.UserRole) or {}; raw = record.get("path")
        if not raw: return
        try:
            path = resolve_allowed_path(self._project_root(), raw, must_exist=True)
            self.open_project_file(path)
        except (OSError, RuntimeError, AccessDenied, ValueError) as exc:
            QMessageBox.warning(self, "Не удалось открыть файл", str(exc))

    def focus_editor_search(self):
        self.open_editor_tab(); self.editor_find.setFocus(); self.editor_find.selectAll()

    def find_in_editor(self):
        editor = self.current_code_editor()
        if not editor: return
        term = self.editor_find.text()
        if not term: return
        if not editor.find(term):
            cursor = editor.textCursor(); cursor.movePosition(cursor.MoveOperation.Start); editor.setTextCursor(cursor)
            if not editor.find(term): self.editor_status.setText(f"Не найдено: {term}")

    def _bind_shortcuts(self):
        QShortcut(QKeySequence("Ctrl+N"), self, activated=self.new_chat)
        QShortcut(QKeySequence("Ctrl+L"), self, activated=self.prompt.setFocus)
        QShortcut(QKeySequence("Escape"), self, activated=self.stop_agent)
        QShortcut(QKeySequence("Ctrl+S"), self, activated=self.save_current_editor)
        QShortcut(QKeySequence("Ctrl+Shift+E"), self, activated=self.open_editor_tab)
        QShortcut(QKeySequence("Ctrl+F"), self, activated=self.focus_editor_search)

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
        if hasattr(self, "model_selector"):
            self.model_selector.blockSignals(True)
            self.model_selector.clear()
            self.model_selector.addItems([self.model.itemText(i) for i in range(self.model.count())])
            self.model_selector.setCurrentText(self.model.currentText())
            self.model_selector.blockSignals(False)
        self.inspector_model.setText(f"Модель: {self.model.currentText() or 'не выбрана'}")
        self.chat_title_label.setText(self.current_chat_title)

    def _create_hidden_connection_fields(self):
        self.base_url = QLineEdit(self.settings_store.value("connection/base_url", "http://127.0.0.1:8080/v1"))
        self.api_key = QLineEdit(self.settings_store.value("connection/api_key", "no-key"))
        self.model = QComboBox()
        self.model.setEditable(False)
        saved_model = str(self.settings_store.value("connection/model", ""))
        if saved_model:
            self.model.addItem(saved_model)
        self.model.setCurrentText(saved_model)
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
            self.base_url.setText(dialog.base_url.text().strip())
            self.api_key.setText(dialog.api_key.text())
            self._set_model(dialog.model_combo.currentText().strip())
            self.settings_store.setValue("connection/base_url", self.base_url.text())
            self.settings_store.setValue("connection/api_key", self.api_key.text())
            for key, value in dialog.values().items(): self.settings_store.setValue(f"limits/{key}", value)
            self.settings_store.setValue("memory/auto_update", dialog.auto_memory_enabled())
            self.settings_store.sync()
            self._update_context_labels()
            self.log_view.appendPlainText("Connection and agent settings saved.")

    def open_project_memory(self):
        root = Path(self.project_path.text())
        if not root.is_dir():
            QMessageBox.warning(self, "Память проекта", "Сначала выберите существующую папку проекта.")
            return
        dialog = ProjectMemoryDialog(self, str(root.resolve()))
        dialog.exec()

    def on_memory_updated(self, memory):
        # The worker already writes atomically; this slot updates the UI/log only.
        summary = memory.get("project_summary", "") if isinstance(memory, dict) else ""
        self.log_view.appendPlainText("Память проекта обновлена." + (f" Краткое описание: {summary[:180]}" if summary else ""))

    def _confirm_project_switch_with_dirty_editors(self):
        dirty = [self.editor_tabs.widget(i) for i in range(self.editor_tabs.count()) if isinstance(self.editor_tabs.widget(i), CodeEditor) and self.editor_tabs.widget(i).document().isModified()]
        if dirty:
            answer = QMessageBox.question(self, "Несохранённые изменения", f"В редакторе есть несохранённые изменения в {len(dirty)} файле(ах). Сохранить их перед сменой проекта?", QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel, QMessageBox.Save)
            if answer == QMessageBox.Cancel:
                return False
            if answer == QMessageBox.Save:
                for editor in dirty:
                    self.editor_tabs.setCurrentWidget(editor)
                    self.save_current_editor()
                    if editor.document().isModified():
                        return False
        for i in reversed(range(self.editor_tabs.count())):
            widget = self.editor_tabs.widget(i)
            if isinstance(widget, CodeEditor):
                self.editor_tabs.removeTab(i); widget.deleteLater()
        if self.editor_tabs.count() == 0:
            self.editor_tabs.addTab(self.editor_empty, "Старт")
        return True

    def choose_project(self):
        if not self._confirm_project_switch_with_dirty_editors():
            return
        current = getattr(self, "project_path", QLineEdit(str(Path.home()))).text()
        selected = QFileDialog.getExistingDirectory(self, "Выберите папку проекта", current)
        if selected:
            path = str(Path(selected).resolve())
            self.project_path.setText(path); self.settings_store.setValue("project/path", path); self.settings_store.sync()
            self._update_context_labels()
            self.refresh_project_tree()
            self.inspector_sandbox.setText("🔒 Sandbox включён\nФайлы доступны только внутри выбранного проекта.")

    def _on_model_selected(self, model_id):
        if model_id:
            self._set_model(model_id)

    def _set_model(self, model_id):
        model_id = str(model_id).strip()
        if not model_id:
            return
        if self.model.findText(model_id) < 0:
            self.model.addItem(model_id)
        self.model.setCurrentText(model_id)
        self.settings_store.setValue("connection/model", model_id)
        self._update_context_labels()

    def refresh_models(self, show_message=False):
        try:
            client = OpenAI(base_url=self.base_url.text().strip(), api_key=self.api_key.text().strip() or "no-key", timeout=8, max_retries=0)
            ids = sorted({str(m.id) for m in client.models.list().data if getattr(m, "id", None)})
            current = self.model.currentText().strip()
            self.model.blockSignals(True)
            self.model.clear()
            self.model.addItems(ids)
            if current and current not in ids:
                self.model.addItem(current)
            if current and current in [self.model.itemText(i) for i in range(self.model.count())]:
                self.model.setCurrentText(current)
            elif ids:
                self.model.setCurrentIndex(0)
            self.model.blockSignals(False)
            if ids:
                self._set_model(self.model.currentText())
                self.log_view.appendPlainText("Модели сервера: " + ", ".join(ids))
                if show_message:
                    QMessageBox.information(self, "Модели", f"Найдено моделей: {len(ids)}")
            elif show_message:
                QMessageBox.warning(self, "Модели", "Список моделей пуст.")
            return ids
        except Exception as exc:
            self.log_view.appendPlainText(f"Ошибка получения моделей: {type(exc).__name__}: {exc}")
            if show_message:
                QMessageBox.critical(self, "Ошибка получения моделей", f"{type(exc).__name__}: {exc}")
            return []

    def test_connection(self):
        try:
            client = OpenAI(base_url=self.base_url.text().strip(), api_key=self.api_key.text().strip() or "no-key", timeout=15, max_retries=0)
            models = client.models.list(); ids = sorted({str(m.id) for m in models.data if getattr(m, "id", None)})
            self.log_view.appendPlainText("Connection OK. Models: " + (", ".join(ids) if ids else "(none)"))
            self.refresh_models(show_message=False)
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
        chat = create_chat(self.project_path.text(), self.model.currentText().strip())
        self.current_chat_id = chat["id"]; self.current_chat_title = chat["title"]; self.conversation_history = []
        self.settings_store.setValue("chat/current_id", self.current_chat_id); self.settings_store.sync()
        self.render_history(); self.refresh_chat_list(select_id=self.current_chat_id); self._update_context_labels(); self._set_status("Готов", "ready")

    def start_agent(self, prompt, force_tool=None, use_history=True):
        if self.worker and self.worker.isRunning(): return
        root = Path(self.project_path.text())
        if not root.is_dir(): QMessageBox.warning(self, "Проект", "Выберите существующую папку проекта."); return
        if use_history:
            if not self.current_chat_id:
                chat = create_chat(str(root.resolve()), self.model.currentText().strip()); self.current_chat_id = chat["id"]
            self._save_current_chat(extra_message={"role": "user", "content": prompt})
        self.settings_store.setValue("connection/base_url", self.base_url.text()); self.settings_store.setValue("connection/api_key", self.api_key.text()); self.settings_store.setValue("connection/model", self.model.currentText()); self.settings_store.sync()
        self.worker = AgentWorker(self.base_url.text().strip(), self.api_key.text().strip() or "no-key", self.model.currentText().strip(), str(root.resolve()), prompt, force_tool, settings=self.current_limits(), history=self.conversation_history if use_history else [], memory=load_project_memory(str(root.resolve())), auto_memory=(self.settings_store.value("memory/auto_update", True, type=bool) and use_history))
        self.worker.chat.connect(self.on_chat); self.worker.log.connect(self.log_view.appendPlainText); self.worker.memory_updated.connect(self.on_memory_updated); self.worker.failed.connect(self.on_failed); self.worker.finished_text.connect(lambda _: self.log_view.appendPlainText("Agent turn finished.")); self.worker.progress.connect(self.on_progress)
        if use_history: self.worker.conversation_updated.connect(self.update_conversation_history)
        self.worker.write_approval_requested.connect(self.confirm_file_change, Qt.ConnectionType.BlockingQueuedConnection); self.worker.change_event.connect(self.add_change_event); self.worker.finished.connect(self.on_worker_finished)
        self.send_btn.setEnabled(False); self.stop_btn.setEnabled(True); self._set_status("Работает…", "working"); self.worker.start()

    def update_conversation_history(self, messages):
        self.conversation_history = list(messages); self._save_current_chat(); self.refresh_chat_list(select_id=self.current_chat_id)

    def _save_current_chat(self, extra_message=None):
        if not self.current_chat_id: return
        chat = load_chat(self.current_chat_id)
        if not chat: chat = create_chat(self.project_path.text(), self.model.currentText().strip()); self.current_chat_id = chat["id"]
        messages = list(self.conversation_history)
        if extra_message is not None and (not messages or messages[-1] != extra_message): messages.append(extra_message)
        chat["messages"] = messages; chat["project_root"] = self.project_path.text(); chat["model"] = self.model.currentText().strip()
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
        if chat.get("model"): self._set_model(chat["model"])
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

    @staticmethod
    def format_diff_html(diff):
        if not diff:
            return "<span style='color:#8f96a3'>Нет diff</span>"
        parts = []
        for line in diff.splitlines():
            safe = escape(line) or "&nbsp;"
            if line.startswith("+++") or line.startswith("---"):
                cls = "#7fb3ff"
            elif line.startswith("+"):
                cls = "#79d99a"
            elif line.startswith("-"):
                cls = "#ff8d8d"
            elif line.startswith("@@"):
                cls = "#d7a8ff"
            else:
                cls = "#c7ccd5"
            parts.append(f"<div style='color:{cls};font-family:Consolas,monospace;white-space:pre'>{safe}</div>")
        return "".join(parts)

    def add_change_event(self, event):
        record = dict(event)
        self.change_records.append(record)
        # Update an existing record for the same path when the worker moves pending -> applied/rejected.
        matches = [i for i, r in enumerate(self.change_records[:-1]) if r.get("path") == record.get("path") and r.get("status") == "pending"]
        if matches and record.get("status") != "pending":
            idx = matches[-1]
            self.change_records[idx] = record
            self.change_records.pop()
        self.refresh_change_center(select_path=record.get("path"))

    def refresh_change_center(self, select_path=None):
        self.changes_list.blockSignals(True); self.changes_list.clear()
        icons = {"pending": "●", "applied": "✓", "rejected": "✕", "cancelled": "⏹", "error": "!"}
        for record in self.change_records:
            status = record.get("status", "")
            item = QListWidgetItem(f"{icons.get(status, '•')}  {record.get('path', '')}")
            item.setData(Qt.ItemDataRole.UserRole, record)
            item.setToolTip(record.get("error", "") or status)
            self.changes_list.addItem(item)
        self.changes_count.setText(str(len(self.change_records)))
        selected = None
        for i in range(self.changes_list.count()):
            item = self.changes_list.item(i)
            if select_path and item.data(Qt.ItemDataRole.UserRole).get("path") == select_path:
                selected = item; break
        if selected:
            self.changes_list.setCurrentItem(selected); self.show_change_diff(selected)
        self.changes_list.blockSignals(False)

    def show_change_diff(self, item):
        if not item: return
        record = item.data(Qt.ItemDataRole.UserRole) or {}
        self.change_diff_view.setHtml(self.format_diff_html(record.get("diff", "")))

    def clear_changes(self):
        if self.worker and self.worker.isRunning():
            QMessageBox.information(self, "Центр изменений", "Очистка доступна после завершения текущего запроса."); return
        self.change_records.clear(); self.refresh_change_center(); self.change_diff_view.clear()

    def open_selected_diff_viewer(self):
        item = self.changes_list.currentItem()
        if not item:
            QMessageBox.information(self, "Центр изменений", "Сначала выберите изменение.")
            return
        record = item.data(Qt.ItemDataRole.UserRole) or {}
        diff = record.get("diff", "")
        if not diff:
            QMessageBox.information(self, "Центр изменений", "Для выбранного изменения нет diff.")
            return
        dialog = SideBySideDiffDialog(self, record.get("path", ""), diff)
        dialog.exec()

    def copy_selected_diff(self):
        item = self.changes_list.currentItem()
        if not item: return
        record = item.data(Qt.ItemDataRole.UserRole) or {}
        QApplication.clipboard().setText(record.get("diff", ""))
        self.log_view.appendPlainText(f"DIFF COPIED: {record.get('path', '')}")

    def confirm_file_change(self, path, diff, exists):
        decision = FileChangeDialog.ask(self, path, diff, exists)
        if self.worker: self.worker.resolve_write_approval(decision)
        self.log_view.appendPlainText(f"WRITE {decision.upper()}: {path}")

    def on_progress(self, count, maximum): self.stop_btn.setText(f"Остановить ({count}/{maximum})")

    def on_failed(self, err): self._set_status("Ошибка", "error"); QMessageBox.critical(self, "Ошибка агента", err)

    def on_worker_finished(self):
        self.send_btn.setEnabled(True); self.stop_btn.setEnabled(False); self.stop_btn.setText("Остановить"); self._set_status("Готов", "ready")
        self.refresh_open_editors_from_disk()

    def on_chat(self, role, content): self._append_message(role, content)

    def closeEvent(self, event):
        dirty = [self.editor_tabs.widget(i) for i in range(self.editor_tabs.count()) if isinstance(self.editor_tabs.widget(i), CodeEditor) and self.editor_tabs.widget(i).document().isModified()]
        if dirty:
            answer = QMessageBox.question(self, "Несохранённые файлы", f"Есть несохранённые изменения в {len(dirty)} файле(ах). Всё равно закрыть приложение?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if answer != QMessageBox.Yes:
                event.ignore(); return
        if self.worker and self.worker.isRunning():
            self.worker.requestInterruption()
        super().closeEvent(event)


# Keep the original connection fields out of the visual layout while preserving the existing backend API.
