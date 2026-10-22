#!/usr/bin/env python3
"""Agent Studio — десктопный интерфейс ИИ-агента (PySide6). Запуск: pip install PySide6 && python agent_studio.py"""
import sys, os, re, json, time, shutil, threading, subprocess, urllib.request, difflib
from pathlib import Path
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

DEF = dict(theme="dark", font=11, wrap=False, provider="LM Studio", url="http://localhost:1234/v1", key="lm-studio",
           model="", temp=0.7, max_tokens=2048, ctx=4096, ngl=99, max_steps=30, max_time=600, plan_review=True,
           sandbox=True, confirm_cmd=True, skills_on=[], gguf=[],
           keys=dict(save="Ctrl+S", palette="Ctrl+Shift+P", task="Ctrl+Shift+N", find="Ctrl+F", goto="Ctrl+G"))
PROV = {"LM Studio": "http://localhost:1234/v1", "OpenAI-compatible": "https://api.openai.com/v1",
        "Ollama": "http://localhost:11434/v1", "llama.cpp server": "http://localhost:8080/v1"}
STAGES = ["Analysis", "Research", "Implementation", "Verification", "Finish"]
IGN = {".git", "node_modules", "__pycache__", ".agent", ".venv", "venv"}
KW = "and as assert async await break class continue def del elif else except finally for from global if import in is lambda nonlocal not or pass raise return try while with yield True False None self print len range".split()
DANGER = re.compile(r"rm\s+-rf|del\s+/s|format\s+[a-z]:|shutdown|mkfs|git\s+push\s+--force", re.I)


def qss(d):
    bg, pn, tx, ac, bd, hv = (("#1e1f22", "#2b2d30", "#dfe1e5", "#4f8cff", "#3c3f45", "#393b40") if d else
                              ("#f3f4f6", "#ffffff", "#1f2328", "#2f6fed", "#d5d8de", "#e6e9ef"))
    return f"""*{{font-family:'Segoe UI','Inter',sans-serif;}}
QMainWindow,QDialog,QWidget{{background:{bg};color:{tx};}}
QPlainTextEdit,QTextEdit,QTextBrowser,QListWidget,QTreeView,QTreeWidget,QLineEdit,QComboBox,QSpinBox,QDoubleSpinBox,QKeySequenceEdit{{background:{pn};border:1px solid {bd};border-radius:6px;padding:4px;selection-background-color:{ac};}}
QPushButton{{background:{pn};border:1px solid {bd};border-radius:6px;padding:5px 12px;}} QPushButton:hover{{background:{hv};}}
QPushButton:disabled{{color:#888;}} QPushButton#primary{{background:{ac};color:white;border:none;}}
QTabWidget::pane{{border:0;}} QTabBar::tab{{padding:6px 14px;background:{bg};border-bottom:2px solid transparent;}}
QTabBar::tab:selected{{border-bottom:2px solid {ac};background:{pn};}}
QToolButton#act{{border:0;border-left:3px solid transparent;border-radius:0;padding:10px;font-size:18px;}}
QToolButton#act:checked{{border-left:3px solid {ac};background:{hv};}} QToolButton#act:hover{{background:{hv};}}
QSplitter::handle{{background:{bd};}} QStatusBar{{background:{ac};}} QStatusBar QLabel{{background:transparent;color:white;padding:0 8px;}}
QProgressBar{{border:0;background:{hv};border-radius:4px;max-height:8px;text-align:center;}} QProgressBar::chunk{{background:{ac};border-radius:4px;}}
QToolTip{{background:{pn};color:{tx};border:1px solid {bd};}} QMenu{{background:{pn};border:1px solid {bd};}}
QMenu::item{{padding:5px 24px;}} QMenu::item:selected{{background:{ac};color:white;}}"""


def btn(t, fn=None, tip="", primary=False):
    b = QPushButton(t); b.setToolTip(tip or t)
    if primary: b.setObjectName("primary")
    if fn: b.clicked.connect(lambda _=False: fn())
    return b


def mono(size=11):
    f = QFontDatabase.systemFont(QFontDatabase.FixedFont); f.setPointSize(size); return f


def stream_chat(cfg, msgs, on_chunk=lambda c: None, stop=lambda: False):
    body = json.dumps(dict(model=cfg["model"], messages=msgs, stream=True, temperature=cfg["temp"], max_tokens=cfg["max_tokens"]))
    req = urllib.request.Request(cfg["url"].rstrip("/") + "/chat/completions", body.encode(),
                                 {"Content-Type": "application/json", "Authorization": "Bearer " + cfg["key"]})
    full = ""
    with urllib.request.urlopen(req, timeout=300) as r:
        for line in r:
            if stop(): break
            line = line.decode("utf-8", "ignore").strip()
            if not line.startswith("data:"): continue
            d = line[5:].strip()
            if d == "[DONE]": break
            ch = json.loads(d)["choices"][0].get("delta", {}).get("content") or ""
            full += ch; on_chunk(ch)
    return full


class Job(QThread):
    ok = Signal(object); err = Signal(str)
    def __init__(s, fn): super().__init__(); s.fn = fn
    def run(s):
        try: s.ok.emit(s.fn())
        except Exception as e: s.err.emit(str(e))


class ChatWorker(QThread):
    chunk = Signal(str); done = Signal(str); fail = Signal(str)
    def __init__(s, cfg, msgs): super().__init__(); s.cfg, s.msgs, s.halt = cfg, msgs, False
    def run(s):
        try: s.done.emit(stream_chat(s.cfg, s.msgs, s.chunk.emit, lambda: s.halt))
        except Exception as e: s.fail.emit(str(e))


class Runner(QThread):
    """Агент: Analysis → Research → Implementation → Verification → Finish, с checkpoints, паузой и лимитами."""
    changed = Signal(); warn = Signal(str); log = Signal(str, str)
    def __init__(s, t, cfg, root, ctx):
        super().__init__(); s.t, s.cfg, s.root, s.ctx = t, cfg, Path(root), ctx
        s.cancel = False; s.ev = threading.Event(); s.ev.set(); s.calls = []; s.n = 0; s.t0 = time.time()
    def step(s):
        s.ev.wait()
        if s.cancel: raise InterruptedError
        s.n += 1
        if s.n > s.cfg["max_steps"] or time.time() - s.t0 > s.cfg["max_time"]: raise RuntimeError("Достигнут лимит выполнения агента")
    def ask(s, sysm, user):
        s.step()
        return stream_chat(s.cfg, [{"role": "system", "content": sysm + "\n" + s.ctx}, {"role": "user", "content": user}], stop=lambda: s.cancel)
    def tool(s, name, args, fn):
        sig = name + str(args); s.calls.append(sig)
        if s.calls.count(sig) >= 3: s.warn.emit(f"Повторяющееся действие: {name} {args}")
        try: r = fn()
        except Exception as e: r = f"ERROR: {e}"
        s.t["tools"].append(dict(name=name, args=str(args), res=str(r)[:4000])); s.changed.emit(); return r
    def run(s):
        t = s.t; t["status"] = "выполняется"; s.changed.emit()
        try:
            for i in range(max(t["stage"], 0), 5):
                s.ev.wait(); t["stage"] = i; s.changed.emit()
                if i == 0:
                    files = s.tool("list_files", ".", lambda: "\n".join(
                        str(p.relative_to(s.root)) for p in list(s.root.rglob("*"))[:2000]
                        if p.is_file() and not set(p.relative_to(s.root).parts) & IGN)[:6000])
                    t["files"] = files
                    t["plan"] = s.ask("Ты программный агент. Составь короткий нумерованный план.", f"Задача: {t['prompt']}\nФайлы:\n{files}")
                    if s.cfg["plan_review"]: s.ev.clear(); t["status"] = "приостановлена"; s.changed.emit()
                elif i == 1:
                    ans = s.ask("Верни ТОЛЬКО JSON-массив (до 3) относительных путей файлов, нужных для задачи.", f"{t['prompt']}\n{t['files']}")
                    m = re.search(r"\[.*?\]", ans, re.S); paths = json.loads(m.group(0)) if m else []
                    t["found"] = [p for p in paths if (s.root / p).is_file()]; t["ctx"] = {}
                    for p in t["found"]: t["ctx"][p] = s.tool("read_file", p, lambda p=p: (s.root / p).read_text("utf-8")[:6000])
                elif i == 2:
                    ans = s.ask("Предложи правки. Для каждого файла формат:\n<<<FILE относительный/путь>>>\nполное новое содержимое\n<<<END>>>\nБез пояснений вне блоков.",
                                f"Задача: {t['prompt']}\nПлан:\n{t['plan']}\nФайлы:\n" + "\n".join(f"--- {k}\n{v}" for k, v in t.get("ctx", {}).items()))
                    t["changes"] = [dict(path=p.strip(), new=c, status="ожидает") for p, c in re.findall(r"<<<FILE (.+?)>>>\n(.*?)\n?<<<END>>>", ans, re.S)]
                    for c in t["changes"]: s.tool("propose_change", c["path"], lambda: "ok")
                elif i == 3:
                    out = []
                    for c in t["changes"]:
                        if c["path"].endswith(".py"):
                            r = s.tool("py_compile", c["path"], lambda c=c: (compile(c["new"], c["path"], "exec"), "OK")[1])
                            out.append(f"{c['path']}: {r}")
                    t["verify"] = "\n".join(out) or "Автопроверка не требуется"
                else:
                    t["result"] = f"Готово. Предложено изменений: {len(t['changes'])}. Подтвердите их в Diff Viewer."
                t["checkpoints"].append(dict(stage=i + 1, plan=t.get("plan", ""), ts=time.strftime("%H:%M:%S")))
                s.changed.emit(); s.ev.wait()
            t["stage"] = 5; t["status"] = "завершена"
        except InterruptedError: t["status"] = "отменена"
        except Exception as e: t["status"] = "ошибка"; t["error"] = str(e); s.log.emit("ERROR", f"Задача: {e}")
        s.changed.emit()


class Hl(QSyntaxHighlighter):
    def __init__(s, doc):
        super().__init__(doc)
        def f(c, b=False, i=False):
            x = QTextCharFormat(); x.setForeground(QColor(c)); x.setFontWeight(700 if b else 400); x.setFontItalic(i); return x
        s.r = [(re.compile(r"\b(%s)\b" % "|".join(KW)), f("#cc7832", True)), (re.compile(r"\b\d+(\.\d+)?\b"), f("#6897bb")),
               (re.compile(r"\b(?:def|class)\s+(\w+)"), f("#d9a441", True)), (re.compile(r"\"[^\"\n]*\"|'[^'\n]*'"), f("#6a9955")),
               (re.compile(r"#[^\n]*"), f("#808080", i=True))]
    def highlightBlock(s, t):
        for rx, fm in s.r:
            for m in rx.finditer(t): s.setFormat(m.start(), m.end() - m.start(), fm)


class LineNums(QWidget):
    def __init__(s, e): super().__init__(e); s.e = e
    def sizeHint(s): return QSize(s.e.lnw(), 0)
    def paintEvent(s, ev): s.e.paint_ln(ev)


class CodeEdit(QPlainTextEdit):
    def __init__(s):
        super().__init__(); s.path = ""; s.diag = []; s.setFont(mono()); s.ln = LineNums(s)
        s.blockCountChanged.connect(s.upd_w); s.updateRequest.connect(s.upd_ln); s.cursorPositionChanged.connect(s.hl_line)
        s.upd_w(); s.hl_line(); s.hl = Hl(s.document())
        s.comp = QCompleter(s); s.comp.setWidget(s); s.comp.setCaseSensitivity(Qt.CaseInsensitive); s.comp.activated.connect(s.ins_comp)
    def lnw(s): return 14 + s.fontMetrics().horizontalAdvance("9") * len(str(max(1, s.blockCount())))
    def upd_w(s, *_): s.setViewportMargins(s.lnw(), 0, 0, 0)
    def upd_ln(s, r, dy):
        if dy: s.ln.scroll(0, dy)
        else: s.ln.update(0, r.y(), s.ln.width(), r.height())
        if r.contains(s.viewport().rect()): s.upd_w()
    def resizeEvent(s, e):
        super().resizeEvent(e); c = s.contentsRect(); s.ln.setGeometry(QRect(c.left(), c.top(), s.lnw(), c.height()))
    def paint_ln(s, ev):
        p = QPainter(s.ln); p.setPen(QColor("#888")); b = s.firstVisibleBlock(); n = b.blockNumber()
        top = round(s.blockBoundingGeometry(b).translated(s.contentOffset()).top()); bot = top + round(s.blockBoundingRect(b).height())
        while b.isValid() and top <= ev.rect().bottom():
            if b.isVisible() and bot >= ev.rect().top(): p.drawText(0, top, s.ln.width() - 6, s.fontMetrics().height(), Qt.AlignRight, str(n + 1))
            b = b.next(); top = bot; bot = top + round(s.blockBoundingRect(b).height()); n += 1
    def hl_line(s):
        x = QTextEdit.ExtraSelection(); x.format.setBackground(QColor(128, 128, 128, 40))
        x.format.setProperty(QTextFormat.FullWidthSelection, True); x.cursor = s.textCursor(); x.cursor.clearSelection(); sel = [x]
        for ln in s.diag:
            y = QTextEdit.ExtraSelection(); y.format.setUnderlineStyle(QTextCharFormat.WaveUnderline); y.format.setUnderlineColor(QColor("red"))
            y.cursor = QTextCursor(s.document().findBlockByNumber(max(ln - 1, 0))); y.cursor.select(QTextCursor.LineUnderCursor); sel.append(y)
        s.setExtraSelections(sel)
    def keyPressEvent(s, e):
        p = s.comp.popup()
        if p.isVisible() and e.key() in (Qt.Key_Enter, Qt.Key_Return, Qt.Key_Tab, Qt.Key_Escape, Qt.Key_Backtab): e.ignore(); return
        super().keyPressEvent(e)
        c = s.textCursor(); c.select(QTextCursor.WordUnderCursor); w = c.selectedText()
        if len(w) < 2 or not e.text() or not (e.text().isalnum() or e.text() == "_"): p.hide(); return
        s.comp.setModel(QStringListModel(sorted(set(re.findall(r"\w{3,}", s.toPlainText())) | set(KW)), s.comp)); s.comp.setCompletionPrefix(w)
        r = s.cursorRect(); r.setWidth(p.sizeHintForColumn(0) + 24); s.comp.complete(r)
    def ins_comp(s, t):
        c = s.textCursor(); c.select(QTextCursor.WordUnderCursor); c.insertText(t); s.setTextCursor(c)


class ClickText(QTextEdit):
    link = Signal(str, int)
    def mouseDoubleClickEvent(s, e):
        t = s.cursorForPosition(e.pos()).block().text(); m = re.search(r'File "(.+?)", line (\d+)|([\w./\\-]+\.\w+):(\d+)', t)
        if m: s.link.emit(m.group(1) or m.group(3), int(m.group(2) or m.group(4)))
        else: super().mouseDoubleClickEvent(e)


class Inp(QPlainTextEdit):
    submit = Signal()
    def keyPressEvent(s, e):
        if e.key() in (Qt.Key_Return, Qt.Key_Enter) and not e.modifiers() & Qt.ShiftModifier: s.submit.emit()
        else: super().keyPressEvent(e)


class DiffDlg(QDialog):
    def __init__(s, path, old, new, warn="", pending=True):
        super().__init__(); s.setWindowTitle(f"Diff — {path}"); s.resize(1150, 680); lay = QVBoxLayout(s)
        if warn:
            w = QLabel("⚠ " + warn); w.setStyleSheet("background:#b26a00;color:white;padding:8px;border-radius:6px"); lay.addWidget(w)
        A, B = old.splitlines(), new.splitlines(); L, R, lm, rm = [], [], [], []; s.starts = []
        for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, A, B).get_opcodes():
            a, b = A[i1:i2], B[j1:j2]
            if tag != "equal": s.starts.append(len(L))
            for k in range(max(len(a), len(b))):
                if tag != "equal":
                    if k < len(a): lm.append(len(L))
                    if k < len(b): rm.append(len(R))
                L.append(a[k] if k < len(a) else ""); R.append(b[k] if k < len(b) else "")
        h = QHBoxLayout(); s.a, s.b = QPlainTextEdit("\n".join(L)), QPlainTextEdit("\n".join(R))
        for e, mk, col in ((s.a, lm, QColor(200, 60, 60, 90)), (s.b, rm, QColor(60, 170, 80, 90))):
            e.setReadOnly(True); e.setLineWrapMode(QPlainTextEdit.NoWrap); e.setFont(mono()); h.addWidget(e); sel = []
            for i in mk:
                x = QTextEdit.ExtraSelection(); x.format.setBackground(col); x.format.setProperty(QTextFormat.FullWidthSelection, True)
                x.cursor = QTextCursor(e.document().findBlockByNumber(i)); sel.append(x)
            e.setExtraSelections(sel)
        s.a.verticalScrollBar().valueChanged.connect(s.b.verticalScrollBar().setValue)
        s.b.verticalScrollBar().valueChanged.connect(s.a.verticalScrollBar().setValue)
        s.a.horizontalScrollBar().valueChanged.connect(s.b.horizontalScrollBar().setValue)
        lay.addLayout(h); row = QHBoxLayout(); s.k = -1; s.info = QLabel(f"Изменений: {len(s.starts)}")
        row.addWidget(btn("◀", lambda: s.go(-1), "Предыдущее изменение")); row.addWidget(btn("▶", lambda: s.go(1), "Следующее изменение"))
        row.addWidget(s.info); row.addStretch()
        if pending:
            row.addWidget(btn("Отклонить", lambda: s.done(2), "Отклонить изменение"))
            row.addWidget(btn("Применить", s.accept, "Применить изменение", True))
        else: row.addWidget(btn("Закрыть", s.reject))
        lay.addLayout(row)
    def go(s, d):
        if not s.starts: return
        s.k = (s.k + d) % len(s.starts); c = QTextCursor(s.b.document().findBlockByNumber(s.starts[s.k])); s.b.setTextCursor(c); s.b.centerCursor()
        s.info.setText(f"Изменение {s.k + 1} из {len(s.starts)}")


class Palette(QDialog):
    def __init__(s, cmds, parent):
        super().__init__(parent, Qt.Popup); s.cmds = cmds; s.resize(520, 360); l = QVBoxLayout(s)
        s.e = QLineEdit(); s.e.setPlaceholderText("Введите команду…"); s.l = QListWidget(); l.addWidget(s.e); l.addWidget(s.l)
        s.e.textChanged.connect(s.fill); s.e.returnPressed.connect(s.run); s.l.itemActivated.connect(lambda _: s.run()); s.fill("")
    def fill(s, t):
        s.l.clear(); [s.l.addItem(n) for n in s.cmds if t.lower() in n.lower()]
        if s.l.count(): s.l.setCurrentRow(0)
    def run(s):
        it = s.l.currentItem()
        if it: s.close(); QTimer.singleShot(0, s.cmds[it.text()])


class Main(QMainWindow):
    def __init__(s):
        super().__init__(); s.q = QSettings("AgentStudio", "AgentStudio"); s.cfg = json.loads(json.dumps(DEF))
        try: s.cfg.update(json.loads(s.q.value("cfg", "{}")))
        except Exception: pass
        r = s.q.value("root", ""); s.root = Path(r) if r and Path(r).is_dir() else None
        s.logs, s.jobs, s.tasks, s.chats = [], [], [], []; s.cur_task = s.cur_chat = s.runner = s.cw = s.gproc = None
        s.mcp = {}; s.shortcuts = {}; s.setWindowTitle("Agent Studio"); s.resize(1500, 900); s.build()
        s.apply_theme(); s.load_project(); s.restore()
        s.clock = QTimer(s, interval=1000, timeout=s.tick); s.clock.start()
        s.auto = QTimer(s, interval=60000, timeout=s.fetch_models); s.auto.start()
        s.diag_t = QTimer(s, singleShot=True, interval=600, timeout=s.diagnose)

    # ---------- хранилище ----------
    def data(s):
        d = (s.root or Path.home() / ".agent_studio") / ".agent"; d.mkdir(parents=True, exist_ok=True); return d
    def jload(s, n, dflt):
        try: return json.loads((s.data() / n).read_text("utf-8"))
        except Exception: return dflt
    def jsave(s, n, o):
        try: (s.data() / n).write_text(json.dumps(o, ensure_ascii=False, indent=1), "utf-8")
        except Exception as e: s.toast(f"Не удалось сохранить {n}: {e}", True)
    def save_cfg(s): s.q.setValue("cfg", json.dumps(s.cfg))

    # ---------- уведомления / логи ----------
    def log(s, lvl, msg):
        s.logs.append((time.strftime("%H:%M:%S"), lvl, msg)); s.show_logs()
    def show_logs(s):
        f = s.lvl.currentText(); s.out.setPlainText("\n".join(f"[{t}] {l:5} {m}" for t, l, m in s.logs if f == "Все" or f == l))
    def toast(s, msg, err=False):
        s.log("ERROR" if err else "INFO", msg); l = QLabel(msg, s)
        l.setStyleSheet(f"background:{'#c0392b' if err else '#2e7d32'};color:white;padding:9px 16px;border-radius:8px;")
        l.adjustSize(); l.move(s.width() - l.width() - 24, s.height() - l.height() - 48); l.show(); QTimer.singleShot(3500, l.deleteLater)
    def job(s, fn, ok, err=None):
        j = Job(fn); j.ok.connect(ok); j.err.connect(err or (lambda e: s.toast(e, True)))
        j.finished.connect(lambda j=j: s.jobs.remove(j) if j in s.jobs else None); s.jobs.append(j); j.start()
    def busy(s, on): s.bar.setVisible(on)

    # ---------- построение UI ----------
    def build(s):
        c = QWidget(); h = QHBoxLayout(c); h.setContentsMargins(0, 0, 0, 0); h.setSpacing(0); s.setCentralWidget(c)
        ab = QFrame(); ab.setFixedWidth(54); v = QVBoxLayout(ab); v.setContentsMargins(0, 6, 0, 6); v.setSpacing(0)
        s.side = QStackedWidget(); s.acts = []
        pages = [("📁", "Проект и файлы", s.pg_files()), ("🔍", "Поиск по проекту", s.pg_search()), ("🤖", "Agent Manager", s.pg_agents()),
                 ("💬", "Чаты", s.pg_chats()), ("🧠", "Model Manager", s.pg_models()), ("🧩", "Skills и MCP", s.pg_skills()),
                 ("📝", "Память проекта", s.pg_memory()), ("⚙", "Настройки", s.pg_settings())]
        for i, (ic, tip, pg) in enumerate(pages):
            b = QToolButton(); b.setObjectName("act"); b.setText(ic); b.setToolTip(tip); b.setCheckable(True)
            b.clicked.connect(lambda _, i=i: s.show_side(i)); v.addWidget(b); s.acts.append(b); s.side.addWidget(pg)
        v.addStretch(); h.addWidget(ab)
        s.hs = QSplitter(Qt.Horizontal); s.hs.setObjectName("hs"); s.vs = QSplitter(Qt.Vertical)
        s.cstack = QStackedWidget(); wl = QLabel("Откройте файл или проект\nCtrl+Shift+P — палитра команд"); wl.setAlignment(Qt.AlignCenter)
        wl.setStyleSheet("font-size:16px;color:#888"); s.cstack.addWidget(wl)
        ew = QWidget(); el = QVBoxLayout(ew); el.setContentsMargins(0, 0, 0, 0); s.tabs = QTabWidget(); s.tabs.setTabsClosable(True); s.tabs.setMovable(True)
        s.tabs.tabCloseRequested.connect(s.close_tab); s.tabs.currentChanged.connect(s.pos_status)
        s.fb = s.findbar(); el.addWidget(s.fb); el.addWidget(s.tabs); s.cstack.addWidget(ew)
        s.vs.addWidget(s.cstack); s.vs.addWidget(s.bottom()); s.vs.setSizes([650, 220])
        s.right = QTabWidget(); s.right.addTab(s.chat_panel(), "Чат"); s.right.addTab(s.task_panel(), "Задача")
        s.hs.addWidget(s.side); s.hs.addWidget(s.vs); s.hs.addWidget(s.right); s.hs.setSizes([280, 800, 420]); s.hs.setCollapsible(1, False); h.addWidget(s.hs)
        sb = s.statusBar(); s.l_proj, s.l_pos, s.l_model, s.l_task = QLabel(), QLabel(), QLabel(), QLabel()
        s.bar = QProgressBar(); s.bar.setRange(0, 0); s.bar.setFixedWidth(100); s.bar.hide()
        for w in (s.l_proj, s.l_task, s.bar): sb.addWidget(w)
        sb.addPermanentWidget(s.l_model); sb.addPermanentWidget(s.l_pos)
        s.cmds = {"Открыть проект": s.open_project, "Новый проект": s.new_project, "Сохранить файл": s.save, "Найти/заменить": s.toggle_find,
                  "Перейти к строке": s.goto_line, "Сменить тему": s.toggle_theme, "Новый чат": s.new_chat, "Новая задача агента": s.new_task,
                  "Показать/скрыть боковую панель": lambda: s.side.setVisible(not s.side.isVisible()),
                  "Показать/скрыть нижнюю панель": lambda: s.bot.setVisible(not s.bot.isVisible()),
                  "Показать/скрыть панель агента": lambda: s.right.setVisible(not s.right.isVisible()),
                  "Проверить подключение к модели": s.fetch_models, "Запустить тесты": lambda: s.run_cmd("python -m pytest -q"),
                  "Настройки": lambda: s.show_side(7)}
        s.bind_keys(); s.show_side(0)

    def bind_keys(s):
        for sc in s.shortcuts.values(): sc.setEnabled(False); sc.deleteLater()
        k = s.cfg["keys"]; m = dict(save=s.save, palette=lambda: Palette(s.cmds, s).exec(), task=s.new_task, find=s.toggle_find, goto=s.goto_line)
        s.shortcuts = {n: QShortcut(QKeySequence(k[n]), s, activated=f) for n, f in m.items()}
        for key, f in (("Ctrl+B", s.cmds["Показать/скрыть боковую панель"]), ("Ctrl+J", s.cmds["Показать/скрыть нижнюю панель"])):
            s.shortcuts[key] = QShortcut(QKeySequence(key), s, activated=f)

    def show_side(s, i):
        if s.acts[i].isChecked() is False and s.side.currentIndex() == i and s.side.isVisible(): s.side.hide(); return
        s.side.show(); s.side.setCurrentIndex(i)
        for j, b in enumerate(s.acts): b.setChecked(j == i)
        if i == 4: s.fetch_models()

    def side_box(s, title):
        w = QWidget(); l = QVBoxLayout(w); l.setContentsMargins(8, 8, 8, 8); t = QLabel(title.upper()); t.setStyleSheet("font-weight:600;color:#888"); l.addWidget(t); return w, l

    # --- файлы ---
    def pg_files(s):
        w, l = s.side_box("Проект"); s.proj_lbl = QLabel("Проект не открыт"); s.proj_lbl.setWordWrap(True); l.addWidget(s.proj_lbl)
        r = QHBoxLayout(); r.addWidget(btn("Открыть", s.open_project, "Открыть папку проекта")); r.addWidget(btn("Новый", s.new_project, "Создать проект")); l.addLayout(r)
        s.ff = QLineEdit(); s.ff.setPlaceholderText("Поиск файлов по имени…"); s.ext = QComboBox(); s.ext.addItems(["Все файлы", ".py", ".md", ".json", ".txt", ".js", ".html"])
        s.ff.textChanged.connect(s.filter_files); s.ext.currentTextChanged.connect(s.filter_files); l.addWidget(s.ff); l.addWidget(s.ext)
        s.fm = QFileSystemModel(); s.tree = QTreeView(); s.tree.setModel(s.fm); s.tree.setHeaderHidden(True)
        for i in (1, 2, 3): s.tree.hideColumn(i)
        s.tree.doubleClicked.connect(lambda ix: s.fm.isDir(ix) or s.open_file(s.fm.filePath(ix)))
        s.tree.setContextMenuPolicy(Qt.CustomContextMenu); s.tree.customContextMenuRequested.connect(s.tree_menu); l.addWidget(s.tree); return w
    def filter_files(s):
        e = "" if s.ext.currentIndex() == 0 else s.ext.currentText(); s.fm.setNameFilters([f"*{s.ff.text()}*{e}"]); s.fm.setNameFilterDisables(False)
    def tree_menu(s, pos):
        ix = s.tree.indexAt(pos); path = Path(s.fm.filePath(ix)) if ix.isValid() else s.root
        if not path: return
        base = path if path.is_dir() else path.parent; m = QMenu(s)
        acts = {"Новый файл": lambda: s.fs_new(base, False), "Новая папка": lambda: s.fs_new(base, True),
                "Переименовать": lambda: s.fs_rename(path), "Удалить": lambda: s.fs_delete(path),
                "Копировать путь": lambda: QApplication.clipboard().setText(str(path))}
        for n, f in acts.items(): m.addAction(n, f)
        m.exec(s.tree.viewport().mapToGlobal(pos))
    def fs_new(s, base, folder):
        n, ok = QInputDialog.getText(s, "Создать", "Имя:")
        if ok and n:
            try: (base / n).mkdir(parents=True) if folder else (base / n).touch(); s.toast(f"Создано: {n}")
            except Exception as e: s.toast(f"Ошибка доступа: {e}", True)
    def fs_rename(s, p):
        n, ok = QInputDialog.getText(s, "Переименовать", "Новое имя:", text=p.name)
        if ok and n:
            try: p.rename(p.with_name(n)); s.toast("Переименовано")
            except Exception as e: s.toast(f"Ошибка доступа: {e}", True)
    def fs_delete(s, p):
        if QMessageBox.warning(s, "Удаление", f"Удалить «{p.name}» безвозвратно?", QMessageBox.Yes | QMessageBox.Cancel) != QMessageBox.Yes: return
        try:
            shutil.rmtree(p) if p.is_dir() else p.unlink(); s.toast("Удалено")
            for i in reversed(range(s.tabs.count())):
                if s.tabs.widget(i).path == str(p): s.tabs.removeTab(i)
            s.sync_stack()
        except Exception as e: s.toast(f"Ошибка доступа: {e}", True)

    # --- поиск ---
    def pg_search(s):
        w, l = s.side_box("Поиск по проекту"); s.sq = QLineEdit(); s.sq.setPlaceholderText("Текст…"); s.sq.returnPressed.connect(s.do_search)
        s.sr = QTreeWidget(); s.sr.setHeaderHidden(True); s.sr.itemDoubleClicked.connect(lambda it, _: it.data(0, Qt.UserRole) and s.open_file(*it.data(0, Qt.UserRole)))
        l.addWidget(s.sq); l.addWidget(btn("Искать", s.do_search, primary=True)); l.addWidget(s.sr); return w
    def do_search(s):
        q, root = s.sq.text(), s.root
        if not root or not q: return s.toast("Откройте проект и введите текст", True)
        s.busy(True)
        def f():
            out = []
            for dp, dn, fn in os.walk(root):
                dn[:] = [d for d in dn if d not in IGN]
                for n in fn:
                    p = os.path.join(dp, n)
                    try:
                        if os.path.getsize(p) > 1e6: continue
                        for i, ln in enumerate(open(p, encoding="utf-8"), 1):
                            if q.lower() in ln.lower(): out.append((p, i, ln.strip()[:110]))
                            if len(out) >= 500: return out
                    except Exception: pass
            return out
        def ok(res):
            s.busy(False); s.sr.clear()
            if not res: s.sr.addTopLevelItem(QTreeWidgetItem(["Ничего не найдено"]))
            for p, i, t in res:
                it = QTreeWidgetItem([f"{os.path.relpath(p, root)}:{i}  {t}"]); it.setData(0, Qt.UserRole, (p, i)); s.sr.addTopLevelItem(it)
        s.job(f, ok, lambda e: (s.busy(False), s.toast(e, True)))

    # --- Agent Manager (список) ---
    def pg_agents(s):
        w, l = s.side_box("Agent Manager"); l.addWidget(btn("＋ Новая задача", s.new_task, "Создать задачу (Ctrl+Shift+N)", True))
        s.tl = QTreeWidget(); s.tl.setHeaderLabels(["Задача", "Статус"]); s.tl.itemSelectionChanged.connect(s.pick_task); l.addWidget(s.tl); return w
    def refresh_tasks(s):
        s.tl.blockSignals(True); s.tl.clear()
        if not s.tasks: s.tl.addTopLevelItem(QTreeWidgetItem(["Задач пока нет", ""]))
        for t in reversed(s.tasks):
            it = QTreeWidgetItem([t["title"][:40], t["status"]]); it.setData(0, Qt.UserRole, t["id"]); s.tl.addTopLevelItem(it)
            if s.cur_task is t: s.tl.setCurrentItem(it)
        s.tl.blockSignals(False)
    def pick_task(s):
        it = s.tl.currentItem()
        t = next((x for x in s.tasks if it and x["id"] == it.data(0, Qt.UserRole)), None)
        if t: s.cur_task = t; s.right.setCurrentIndex(1); s.show_task()
    def new_task(s):
        if not s.root: return s.toast("Сначала откройте проект", True)
        txt, ok = QInputDialog.getMultiLineText(s, "Новая задача", "Опишите задачу для агента:")
        if ok and txt.strip():
            t = dict(id=str(int(time.time() * 1000)), title=txt.strip().splitlines()[0], prompt=txt.strip(), status="ожидает", stage=0, duration=0,
                     plan="", found=[], tools=[], changes=[], checkpoints=[], verify="", result="", files="")
            s.tasks.append(t); s.cur_task = t; s.jsave("tasks.json", s.tasks); s.refresh_tasks(); s.right.setCurrentIndex(1); s.show_task(); s.start_task()

    # --- чаты (список) ---
    def pg_chats(s):
        w, l = s.side_box("Чаты"); l.addWidget(btn("＋ Новый чат", s.new_chat, primary=True)); s.cl = QListWidget(); s.cl.currentRowChanged.connect(s.pick_chat)
        s.cl.setContextMenuPolicy(Qt.CustomContextMenu); s.cl.customContextMenuRequested.connect(s.chat_menu); l.addWidget(s.cl); return w
    def chat_menu(s, pos):
        if s.cl.currentRow() < 0: return
        m = QMenu(s); m.addAction("Переименовать", s.rename_chat); m.addAction("Удалить", s.delete_chat); m.exec(s.cl.viewport().mapToGlobal(pos))
    def refresh_chats(s):
        s.cl.blockSignals(True); s.cl.clear(); [s.cl.addItem(c["title"]) for c in s.chats]
        if s.cur_chat in s.chats: s.cl.setCurrentRow(s.chats.index(s.cur_chat))
        s.cl.blockSignals(False); s.render_chat()
    def new_chat(s):
        s.cur_chat = dict(title=f"Чат {len(s.chats) + 1}", msgs=[]); s.chats.append(s.cur_chat); s.jsave("chats.json", s.chats); s.refresh_chats(); s.right.setCurrentIndex(0)
    def pick_chat(s, i):
        if 0 <= i < len(s.chats): s.cur_chat = s.chats[i]; s.render_chat()
    def rename_chat(s):
        n, ok = QInputDialog.getText(s, "Переименовать чат", "Название:", text=s.cur_chat["title"])
        if ok and n: s.cur_chat["title"] = n; s.jsave("chats.json", s.chats); s.refresh_chats()
    def delete_chat(s):
        if s.cur_chat and QMessageBox.question(s, "Удалить чат", "Удалить выбранный чат?") == QMessageBox.Yes:
            s.chats.remove(s.cur_chat); s.cur_chat = s.chats[-1] if s.chats else None; s.jsave("chats.json", s.chats); s.refresh_chats()

    # --- Model Manager ---
    def pg_models(s):
        w, l = s.side_box("Model Manager"); s.prov = QComboBox(); s.prov.addItems(PROV); s.prov.setCurrentText(s.cfg["provider"]); s.prov.currentTextChanged.connect(s.prov_changed)
        s.url = QLineEdit(s.cfg["url"]); s.key = QLineEdit(s.cfg["key"]); s.key.setEchoMode(QLineEdit.Password)
        for ed, k in ((s.url, "url"), (s.key, "key")): ed.editingFinished.connect(lambda ed=ed, k=k: s.set_cfg(k, ed.text()))
        s.mstate = QLabel("Не проверено"); s.mlist = QListWidget(); s.mlist.itemDoubleClicked.connect(lambda it: s.set_model(it.text()))
        f = QFormLayout(); f.addRow("Провайдер", s.prov); f.addRow("URL", s.url); f.addRow("API key", s.key); l.addLayout(f)
        r = QHBoxLayout(); r.addWidget(btn("Проверить / обновить", s.fetch_models, "Проверка подключения и обновление списка моделей", True)); l.addLayout(r)
        l.addWidget(s.mstate); l.addWidget(QLabel("Модели (двойной клик — выбрать):")); l.addWidget(s.mlist)
        g = QFormLayout(); s.sp = {}
        for k, lab, cls, rng in (("temp", "Temperature", QDoubleSpinBox, (0, 2)), ("max_tokens", "Max tokens", QSpinBox, (16, 65536)),
                                 ("ctx", "Контекст", QSpinBox, (512, 1048576)), ("ngl", "GPU layers", QSpinBox, (0, 999))):
            sp = cls(); sp.setRange(*rng); sp.setValue(s.cfg[k]); sp.valueChanged.connect(lambda v, k=k: s.set_cfg(k, v)); g.addRow(lab, sp)
        l.addLayout(g); l.addWidget(QLabel("Локальные GGUF:")); s.gl = QListWidget(); l.addWidget(s.gl); s.gl.setMaximumHeight(100)
        r = QHBoxLayout(); r.addWidget(btn("Импорт GGUF", s.import_gguf)); r.addWidget(btn("▶ Запуск", s.start_gguf, "Запустить llama-server")); r.addWidget(btn("■ Стоп", s.stop_gguf)); l.addLayout(r)
        s.gstate = QLabel("Локальная модель: остановлена"); s.res = QLabel(""); l.addWidget(s.gstate); l.addWidget(s.res); s.refresh_gguf()
        QTimer(s, interval=5000, timeout=s.resources).start(); return w
    def set_cfg(s, k, v): s.cfg[k] = v; s.save_cfg()
    def prov_changed(s, p): s.cfg["provider"] = p; s.url.setText(PROV[p]); s.set_cfg("url", PROV[p])
    def set_model(s, m): s.set_cfg("model", m); s.l_model.setText("🧠 " + m); s.toast(f"Активная модель: {m}")
    def fetch_models(s):
        cfg = dict(s.cfg)
        def f():
            r = urllib.request.Request(cfg["url"].rstrip("/") + "/models", headers={"Authorization": "Bearer " + cfg["key"]})
            return [m["id"] for m in json.load(urllib.request.urlopen(r, timeout=8))["data"]]
        def ok(ms):
            s.mlist.clear(); s.mlist.addItems(ms); s.mstate.setText(f"✔ Подключено, моделей: {len(ms)}")
            if ms and cfg["model"] not in ms and not cfg["model"]: s.set_model(ms[0])
        s.job(f, ok, lambda e: (s.mstate.setText("✖ " + e), s.log("ERROR", "Модель/подключение: " + e)))
    def import_gguf(s):
        fs, _ = QFileDialog.getOpenFileNames(s, "GGUF", "", "GGUF (*.gguf)")
        for f in fs:
            if f not in s.cfg["gguf"]: s.cfg["gguf"].append(f)
        s.save_cfg(); s.refresh_gguf()
    def refresh_gguf(s):
        s.gl.clear()
        for f in s.cfg["gguf"]:
            q = re.search(r"(I?Q\d\w*|F16|BF16)", Path(f).stem, re.I); sz = os.path.getsize(f) / 2**30 if os.path.exists(f) else 0
            it = QListWidgetItem(f"{Path(f).name} — {sz:.1f} GB, {q.group(1).upper() if q else '?'}"); it.setData(Qt.UserRole, f); s.gl.addItem(it)
    def start_gguf(s):
        it = s.gl.currentItem()
        if not it: return s.toast("Выберите GGUF-файл", True)
        if s.gproc: return
        s.gproc = QProcess(s); s.gproc.setProcessChannelMode(QProcess.MergedChannels)
        s.gproc.readyRead.connect(lambda: (lambda t: (s.log("INFO", t.strip()[-200:]), "listening" in t and s.gstate.setText("Локальная модель: ✔ загружена")))(bytes(s.gproc.readAll()).decode("utf-8", "ignore")))
        s.gproc.errorOccurred.connect(lambda e: (s.gstate.setText("Ошибка загрузки модели"), s.toast("Не удалось запустить llama-server (установлен ли он в PATH?)", True), setattr(s, "gproc", None)))
        s.gproc.finished.connect(lambda *_: (s.gstate.setText("Локальная модель: остановлена"), setattr(s, "gproc", None)))
        s.gproc.start("llama-server", ["-m", it.data(Qt.UserRole), "-c", str(s.cfg["ctx"]), "-ngl", str(s.cfg["ngl"]), "--port", "8080"])
        s.gstate.setText("Локальная модель: ⏳ загрузка…"); s.prov.setCurrentText("llama.cpp server")
    def stop_gguf(s):
        if s.gproc: s.gproc.kill()
    def resources(s):
        def f():
            t = ""
            try:
                import psutil; v = psutil.virtual_memory(); t += f"RAM {v.used / 2**30:.1f}/{v.total / 2**30:.1f} GB  "
            except Exception: pass
            try: t += "VRAM " + subprocess.check_output(["nvidia-smi", "--query-gpu=memory.used,memory.total", "--format=csv,noheader"], timeout=3, text=True).strip()
            except Exception: pass
            return t
        s.job(f, lambda t: s.res.setText(t or "VRAM/RAM: недоступно"), lambda e: None)

    # --- Skills и MCP ---
    def pg_skills(s):
        w, l = s.side_box("Skills"); s.sk = QTreeWidget(); s.sk.setHeaderHidden(True); s.sk.itemChanged.connect(s.skill_toggle); s.sk.currentItemChanged.connect(s.skill_desc)
        s.sd = QPlainTextEdit(); s.sd.setReadOnly(True); s.sd.setMaximumHeight(110); l.addWidget(s.sk); l.addWidget(s.sd)
        t = QLabel("MCP-СЕРВЕРЫ"); t.setStyleSheet("font-weight:600;color:#888"); l.addWidget(t)
        s.mt = QTreeWidget(); s.mt.setHeaderLabels(["Сервер / инструмент", "Состояние"]); s.mt.itemChanged.connect(s.mcp_toggle); l.addWidget(s.mt)
        r = QHBoxLayout(); r.addWidget(btn("＋", s.mcp_add, "Добавить сервер")); r.addWidget(btn("－", s.mcp_del, "Удалить сервер")); r.addWidget(btn("Подключить", s.mcp_connect, "Получить список инструментов")); l.addLayout(r); return w
    def refresh_skills(s):
        s.sk.blockSignals(True); s.sk.clear(); dirs = [Path.home() / ".agent_studio" / "skills"] + ([s.root / ".agent" / "skills"] if s.root else [])
        found = [p for d in dirs if d.is_dir() for p in sorted(d.glob("*/SKILL.md"))]
        if not found: s.sk.addTopLevelItem(QTreeWidgetItem(["Нет Skills. Положите SKILL.md в .agent/skills/<имя>/"]))
        for p in found:
            it = QTreeWidgetItem([p.parent.name]); it.setFlags(it.flags() | Qt.ItemIsUserCheckable); it.setCheckState(0, Qt.Checked if p.parent.name in s.cfg["skills_on"] else Qt.Unchecked)
            it.setData(0, Qt.UserRole, str(p)); s.sk.addTopLevelItem(it)
        s.sk.blockSignals(False)
    def skill_toggle(s, it, _):
        on = set(s.cfg["skills_on"]); (on.add if it.checkState(0) == Qt.Checked else on.discard)(it.text(0)); s.set_cfg("skills_on", sorted(on))
    def skill_desc(s, it, _):
        p = it.data(0, Qt.UserRole) if it else None
        if p: s.sd.setPlainText(Path(p).read_text("utf-8", "ignore")[:1500])
    def skills_text(s):
        out = []
        for i in range(s.sk.topLevelItemCount()):
            it = s.sk.topLevelItem(i)
            if it.checkState(0) == Qt.Checked and it.data(0, Qt.UserRole): out.append(f"[Skill {it.text(0)}]\n" + Path(it.data(0, Qt.UserRole)).read_text("utf-8", "ignore")[:1500])
        return "\n".join(out)
    def refresh_mcp(s):
        s.mt.blockSignals(True); s.mt.clear()
        for n, m in s.mcp.items():
            it = QTreeWidgetItem([n, m.get("state", "отключён")]); it.setFlags(it.flags() | Qt.ItemIsUserCheckable); it.setCheckState(0, Qt.Checked if m.get("enabled") else Qt.Unchecked)
            for tn, allow in m.get("tools", {}).items():
                c = QTreeWidgetItem([tn, "разрешён" if allow else "запрещён"]); c.setFlags(c.flags() | Qt.ItemIsUserCheckable); c.setCheckState(0, Qt.Checked if allow else Qt.Unchecked); it.addChild(c)
            s.mt.addTopLevelItem(it); it.setExpanded(True)
        s.mt.blockSignals(False)
    def mcp_toggle(s, it, _):
        p = it.parent(); on = it.checkState(0) == Qt.Checked
        if p: s.mcp[p.text(0)]["tools"][it.text(0)] = on; it.setText(1, "разрешён" if on else "запрещён")
        else: s.mcp[it.text(0)]["enabled"] = on
        s.jsave("mcp.json", s.mcp)
    def mcp_add(s):
        n, ok = QInputDialog.getText(s, "MCP-сервер", "Имя:")
        if not (ok and n): return
        c, ok = QInputDialog.getText(s, "MCP-сервер", "Команда запуска (stdio):")
        if ok and c: s.mcp[n] = dict(cmd=c, enabled=True, tools={}, state="отключён"); s.jsave("mcp.json", s.mcp); s.refresh_mcp()
    def mcp_del(s):
        it = s.mt.currentItem()
        if it and not it.parent() and QMessageBox.question(s, "Удаление", f"Удалить сервер {it.text(0)}?") == QMessageBox.Yes: s.mcp.pop(it.text(0)); s.jsave("mcp.json", s.mcp); s.refresh_mcp()
    def mcp_connect(s):
        it = s.mt.currentItem(); it = it.parent() if it and it.parent() else it
        if not it: return
        n = it.text(0); cmd = s.mcp[n]["cmd"]; it.setText(1, "подключение…")
        def f():
            p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
            def rpc(o): p.stdin.write(json.dumps(o) + "\n"); p.stdin.flush()
            try:
                rpc(dict(jsonrpc="2.0", id=1, method="initialize", params=dict(protocolVersion="2024-11-05", capabilities={}, clientInfo=dict(name="agent-studio", version="1"))))
                p.stdout.readline(); rpc(dict(jsonrpc="2.0", method="notifications/initialized")); rpc(dict(jsonrpc="2.0", id=2, method="tools/list"))
                while True: 
                    r = json.loads(p.stdout.readline())
                    if r.get("id") == 2: return [t["name"] for t in r["result"]["tools"]]
            finally: p.kill()
        def ok(tools):
            old = s.mcp[n].get("tools", {}); s.mcp[n]["tools"] = {t: old.get(t, False) for t in tools}; s.mcp[n]["state"] = "подключён"; s.jsave("mcp.json", s.mcp); s.refresh_mcp()
        def bad(e): s.mcp[n]["state"] = "ошибка"; s.refresh_mcp(); s.toast(f"MCP {n}: {e}", True)
        s.job(f, ok, bad)

    # --- память ---
    def pg_memory(s):
        w, l = s.side_box("Память проекта"); s.mem = QPlainTextEdit(); s.mem.setPlaceholderText("Заметки о проекте: стек, соглашения, договорённости. Передаются агенту как контекст.")
        l.addWidget(s.mem); r = QHBoxLayout(); r.addWidget(btn("Сохранить", s.mem_save, primary=True)); r.addWidget(btn("Обновить", s.mem_load)); r.addWidget(btn("Очистить", s.mem_clear)); l.addLayout(r); return w
    def mem_path(s): return s.data() / "memory.md"
    def mem_load(s):
        if s.mem.document().isModified() and QMessageBox.question(s, "Обновить", "Несохранённые заметки будут потеряны. Продолжить?") != QMessageBox.Yes: return
        s.mem.setPlainText(s.mem_path().read_text("utf-8") if s.mem_path().exists() else ""); s.mem.document().setModified(False)
    def mem_save(s): s.mem_path().write_text(s.mem.toPlainText(), "utf-8"); s.mem.document().setModified(False); s.toast("Память сохранена")
    def mem_clear(s):
        if QMessageBox.warning(s, "Очистка", "Очистить память проекта?", QMessageBox.Yes | QMessageBox.Cancel) == QMessageBox.Yes: s.mem.clear(); s.mem_save()

    # --- настройки ---
    def pg_settings(s):
        w, l = s.side_box("Настройки"); f = QFormLayout(); l.addLayout(f)
        s.s_theme = QComboBox(); s.s_theme.addItems(["dark", "light"]); s.s_theme.setCurrentText(s.cfg["theme"]); s.s_theme.currentTextChanged.connect(lambda t: (s.set_cfg("theme", t), s.apply_theme()))
        s.s_font = QSpinBox(); s.s_font.setRange(7, 32); s.s_font.setValue(s.cfg["font"]); s.s_font.valueChanged.connect(lambda v: (s.set_cfg("font", v), s.apply_editor_prefs()))
        s.s_wrap = QCheckBox("Перенос длинных строк"); s.s_wrap.setChecked(s.cfg["wrap"]); s.s_wrap.toggled.connect(lambda v: (s.set_cfg("wrap", v), s.apply_editor_prefs()))
        f.addRow("Тема", s.s_theme); f.addRow("Шрифт редактора", s.s_font); f.addRow(s.s_wrap)
        for k, lab, rng in (("max_steps", "Лимит шагов агента", (1, 500)), ("max_time", "Лимит времени, сек", (10, 7200))):
            sp = QSpinBox(); sp.setRange(*rng); sp.setValue(s.cfg[k]); sp.valueChanged.connect(lambda v, k=k: s.set_cfg(k, v)); f.addRow(lab, sp)
        for k, lab in (("plan_review", "Подтверждать план до выполнения"), ("sandbox", "Sandbox: команды только в папке проекта"), ("confirm_cmd", "Подтверждать команды терминала")):
            c = QCheckBox(lab); c.setChecked(s.cfg[k]); c.toggled.connect(lambda v, k=k: s.set_cfg(k, v)); f.addRow(c)
        for k, lab in (("save", "Сохранить"), ("palette", "Палитра команд"), ("task", "Новая задача"), ("find", "Поиск/замена"), ("goto", "Перейти к строке")):
            e = QKeySequenceEdit(QKeySequence(s.cfg["keys"][k])); e.editingFinished.connect(lambda e=e, k=k: (s.cfg["keys"].__setitem__(k, e.keySequence().toString()), s.save_cfg(), s.bind_keys())); f.addRow("⌨ " + lab, e)
        l.addStretch(); return w
    def apply_theme(s): QApplication.instance().setStyleSheet(qss(s.cfg["theme"] == "dark"))
    def toggle_theme(s): s.s_theme.setCurrentText("light" if s.cfg["theme"] == "dark" else "dark")
    def apply_editor_prefs(s):
        for i in range(s.tabs.count()):
            e = s.tabs.widget(i); e.setFont(mono(s.cfg["font"])); e.setLineWrapMode(QPlainTextEdit.WidgetWidth if s.cfg["wrap"] else QPlainTextEdit.NoWrap)

    # --- нижняя панель ---
    def bottom(s):
        s.bot = QTabWidget(); w = QWidget(); l = QVBoxLayout(w); l.setContentsMargins(4, 4, 4, 4); r = QHBoxLayout()
        s.lvl = QComboBox(); s.lvl.addItems(["Все", "INFO", "WARN", "ERROR"]); s.lvl.currentTextChanged.connect(lambda _: s.show_logs())
        s.out = QPlainTextEdit(); s.out.setReadOnly(True); s.out.setFont(mono(10))
        r.addWidget(QLabel("Уровень:")); r.addWidget(s.lvl); r.addWidget(btn("Копировать", lambda: QApplication.clipboard().setText(s.out.toPlainText()))); r.addWidget(btn("Очистить", lambda: (s.logs.clear(), s.show_logs()))); r.addStretch()
        l.addLayout(r); l.addWidget(s.out); s.bot.addTab(w, "Output")
        t = QWidget(); l = QVBoxLayout(t); l.setContentsMargins(4, 4, 4, 4); s.term = ClickText(); s.term.setReadOnly(True); s.term.setFont(mono(10)); s.term.link.connect(lambda p, n: s.open_file(p if os.path.isabs(p) else str((s.root or Path()) / p), n))
        s.cmd = QLineEdit(); s.cmd.setPlaceholderText("$ команда (Enter) — выполняется в папке проекта"); s.cmd.returnPressed.connect(lambda: s.run_cmd(s.cmd.text()))
        r = QHBoxLayout(); s.running = QLabel(""); r.addWidget(s.cmd); r.addWidget(btn("▶ Тесты", lambda: s.run_cmd("python -m pytest -q"), "Запустить pytest")); r.addWidget(btn("■ Стоп", s.stop_cmd, "Остановить операцию"))
        r.addWidget(btn("Очистить", s.term.clear)); l.addWidget(s.term); l.addLayout(r); l.addWidget(s.running); s.bot.addTab(t, "Terminal"); s.proc = None
        s.prob = QListWidget(); s.prob.itemDoubleClicked.connect(lambda it: s.open_file(*it.data(Qt.UserRole))); s.bot.addTab(s.prob, "Problems"); return s.bot
    def run_cmd(s, c):
        if not c.strip() or not s.root: return s.toast("Откройте проект и введите команду", True)
        if s.proc: return s.toast("Предыдущая команда ещё выполняется", True)
        if DANGER.search(c) and QMessageBox.warning(s, "Опасная операция", f"Команда выглядит потенциально опасной:\n{c}\nВыполнить?", QMessageBox.Yes | QMessageBox.Cancel) != QMessageBox.Yes: return
        if s.cfg["confirm_cmd"] and not DANGER.search(c) and QMessageBox.question(s, "Выполнить команду", c) != QMessageBox.Yes: return
        s.bot.setCurrentIndex(1); s.bot.show(); s.term.append(f"<span style='color:#4f8cff'>$ {c}</span>"); s.proc = QProcess(s); s.proc.setWorkingDirectory(str(s.root))
        s.proc.readyReadStandardOutput.connect(lambda: s.term.append(bytes(s.proc.readAllStandardOutput()).decode("utf-8", "ignore").rstrip()))
        s.proc.readyReadStandardError.connect(lambda: s.term.append("<span style='color:#e5534b'>" + bytes(s.proc.readAllStandardError()).decode("utf-8", "ignore").rstrip().replace("<", "&lt;").replace("\n", "<br>") + "</span>"))
        s.proc.finished.connect(s.cmd_done); s.running.setText("⏳ Выполняется…"); s.busy(True)
        s.proc.start(*(("cmd", ["/c", c]) if os.name == "nt" else ("sh", ["-c", c])))
    def cmd_done(s, code, *_):
        s.running.setText(""); s.busy(False); out = s.term.toPlainText()[-600:]; m = re.search(r"(\d+) passed|(\d+) failed", out)
        s.toast(f"Команда завершена, код {code}" + (f" — {m.group(0)}" if m else ""), code != 0); s.proc = None
    def stop_cmd(s):
        if s.proc: s.proc.kill(); s.toast("Операция остановлена")

    # --- редактор ---
    def findbar(s):
        w = QWidget(); l = QHBoxLayout(w); l.setContentsMargins(6, 4, 6, 4); s.fe, s.re_ = QLineEdit(), QLineEdit(); s.fe.setPlaceholderText("Найти"); s.re_.setPlaceholderText("Заменить на")
        s.fe.returnPressed.connect(lambda: s.find(False))
        for x in (s.fe, s.re_): l.addWidget(x)
        for t, f in (("↓", lambda: s.find(False)), ("↑", lambda: s.find(True)), ("Заменить", s.replace1), ("Все", s.replace_all), ("✕", w.hide)): l.addWidget(btn(t, f))
        w.hide(); return w
    def ed(s): return s.tabs.currentWidget()
    def toggle_find(s): s.fb.setVisible(not s.fb.isVisible()); s.fb.isVisible() and s.fe.setFocus()
    def find(s, back):
        e = s.ed()
        if not e: return
        fl = QTextDocument.FindBackward if back else QTextDocument.FindFlag(0)
        if not e.find(s.fe.text(), fl):
            e.moveCursor(QTextCursor.End if back else QTextCursor.Start)
            if not e.find(s.fe.text(), fl): s.toast("Не найдено", True)
    def replace1(s):
        e = s.ed()
        if e and e.textCursor().selectedText() == s.fe.text(): e.textCursor().insertText(s.re_.text())
        s.find(False)
    def replace_all(s):
        e = s.ed()
        if not e or not s.fe.text(): return
        c = e.textCursor(); c.beginEditBlock(); c.movePosition(QTextCursor.Start); e.setTextCursor(c); n = 0
        while e.find(s.fe.text()): e.textCursor().insertText(s.re_.text()); n += 1
        c.endEditBlock(); s.toast(f"Заменено: {n}")
    def goto_line(s, n=None):
        e = s.ed()
        if not e: return
        if n is None: n, ok = QInputDialog.getInt(s, "Перейти к строке", "Строка:", 1, 1, e.blockCount())
        else: ok = True
        if ok: e.setTextCursor(QTextCursor(e.document().findBlockByNumber(n - 1))); e.centerCursor(); e.setFocus()
    def open_file(s, path, line=None):
        path = str(path)
        for i in range(s.tabs.count()):
            if s.tabs.widget(i).path == path: s.tabs.setCurrentIndex(i); line and s.goto_line(line); return
        try: text = Path(path).read_text("utf-8")
        except Exception as e: return s.toast(f"Не удалось открыть {Path(path).name}: {e}", True)
        e = CodeEdit(); e.path = path; e.setPlainText(text); e.document().setModified(False); e.setFont(mono(s.cfg["font"]))
        e.setLineWrapMode(QPlainTextEdit.WidgetWidth if s.cfg["wrap"] else QPlainTextEdit.NoWrap)
        e.document().modificationChanged.connect(lambda m, e=e: s.tab_mod(e)); e.cursorPositionChanged.connect(s.pos_status); e.textChanged.connect(lambda: s.diag_t.start())
        s.tabs.addTab(e, Path(path).name); s.tabs.setTabToolTip(s.tabs.count() - 1, path); s.tabs.setCurrentWidget(e); s.sync_stack(); s.diagnose(); line and s.goto_line(line)
    def sync_stack(s): s.cstack.setCurrentIndex(1 if s.tabs.count() else 0)
    def tab_mod(s, e):
        i = s.tabs.indexOf(e); i >= 0 and s.tabs.setTabText(i, ("● " if e.document().isModified() else "") + Path(e.path).name)
    def pos_status(s, *_):
        e = s.ed(); c = e.textCursor() if e else None; s.l_pos.setText(f"Стр {c.blockNumber() + 1}, Стлб {c.columnNumber() + 1}" if c else "")
    def save(s, e=None):
        e = e or s.ed()
        if not e: return True
        try: Path(e.path).write_text(e.toPlainText(), "utf-8"); e.document().setModified(False); s.toast(f"Сохранено: {Path(e.path).name}"); return True
        except Exception as x: s.toast(f"Не удалось сохранить: {x}", True); return False
    def close_tab(s, i):
        e = s.tabs.widget(i)
        if e.document().isModified():
            r = QMessageBox.question(s, "Несохранённые изменения", f"Сохранить {Path(e.path).name}?", QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
            if r == QMessageBox.Cancel or (r == QMessageBox.Save and not s.save(e)): return False
        s.tabs.removeTab(i); s.sync_stack(); return True
    def diagnose(s):
        e = s.ed(); s.prob.clear()
        if not e: return
        e.diag = []
        if e.path.endswith(".py"):
            try: compile(e.toPlainText(), e.path, "exec")
            except SyntaxError as x:
                e.diag = [x.lineno or 1]; it = QListWidgetItem(f"✖ {Path(e.path).name}:{x.lineno} — {x.msg}"); it.setData(Qt.UserRole, (e.path, x.lineno or 1)); s.prob.addItem(it)
        s.bot.setTabText(2, f"Problems ({s.prob.count()})"); e.hl_line()

    # --- чат ---
    def chat_panel(s):
        w = QWidget(); l = QVBoxLayout(w); l.setContentsMargins(6, 6, 6, 6); r = QHBoxLayout(); s.ct = QLabel("Чат"); s.ct.setStyleSheet("font-weight:600"); r.addWidget(s.ct); r.addStretch()
        r.addWidget(btn("＋", s.new_chat, "Новый чат")); r.addWidget(btn("⧉", s.copy_last, "Копировать последний ответ")); r.addWidget(btn("↻", s.resend, "Отправить запрос повторно")); l.addLayout(r)
        s.view = QTextBrowser(); s.view.setOpenExternalLinks(True); l.addWidget(s.view)
        s.inp = Inp(); s.inp.setPlaceholderText("Сообщение агенту… (Enter — отправить, Shift+Enter — перенос)"); s.inp.setFixedHeight(80); s.inp.submit.connect(s.send); l.addWidget(s.inp)
        r = QHBoxLayout(); s.b_send = btn("Отправить", s.send, "Enter", True); s.b_stop = btn("■ Стоп", s.stop_gen, "Остановить генерацию"); s.b_stop.setEnabled(False); r.addStretch(); r.addWidget(s.b_stop); r.addWidget(s.b_send); l.addLayout(r); return w
    def render_chat(s):
        c = s.cur_chat; s.ct.setText(c["title"] if c else "Чат")
        if not c or not c["msgs"]: return s.view.setHtml("<p style='color:#888;margin-top:40px' align='center'>Сообщений пока нет.<br>Напишите первый запрос агенту.</p>")
        s.view.setMarkdown("\n\n".join(f"**{'Вы' if m['role'] == 'user' else 'Агент'}:**\n\n{m['content']}" for m in c["msgs"]))
        s.view.verticalScrollBar().setValue(s.view.verticalScrollBar().maximum())
    def sys_prompt(s):
        mem = s.mem_path().read_text("utf-8")[:3000] if s.root and s.mem_path().exists() else ""
        return "Ты — ИИ-агент программирования в IDE. Отвечай кратко и по делу.\n" + (f"Память проекта:\n{mem}\n" if mem else "") + s.skills_text()
    def send(s, text=None):
        text = text if isinstance(text, str) else s.inp.toPlainText().strip()
        if not text or s.cw: return
        if not s.cur_chat: s.new_chat()
        if not s.cfg["model"]: return s.toast("Выберите модель в Model Manager", True)
        s.cur_chat["msgs"] += [dict(role="user", content=text), dict(role="assistant", content="")]; s.inp.clear()
        if len(s.cur_chat["msgs"]) == 2: s.cur_chat["title"] = text[:30]; s.refresh_chats()
        msgs = [{"role": "system", "content": s.sys_prompt()}] + s.cur_chat["msgs"][:-1][-20:]
        s.cw = ChatWorker(dict(s.cfg), msgs); s.cw.chunk.connect(s.on_chunk); s.cw.done.connect(s.on_done); s.cw.fail.connect(s.on_fail)
        s.b_send.setEnabled(False); s.b_stop.setEnabled(True); s.busy(True); s.l_task.setText("💬 генерация…"); s.render_chat(); s.cw.start()
    def on_chunk(s, ch): s.cur_chat["msgs"][-1]["content"] += ch; s.render_chat()
    def gen_end(s): s.cw = None; s.b_send.setEnabled(True); s.b_stop.setEnabled(False); s.busy(False); s.l_task.setText(""); s.jsave("chats.json", s.chats)
    def on_done(s, _): s.gen_end(); s.render_chat()
    def on_fail(s, e):
        s.cur_chat["msgs"][-1]["content"] = f"⚠ Ошибка модели/подключения: {e}"; s.gen_end(); s.render_chat(); s.toast("Ошибка подключения к модели: " + e, True)
    def stop_gen(s):
        if s.cw: s.cw.halt = True
    def copy_last(s):
        a = [m for m in (s.cur_chat or {}).get("msgs", []) if m["role"] == "assistant"]
        if a: QApplication.clipboard().setText(a[-1]["content"]); s.toast("Скопировано")
    def resend(s):
        m = (s.cur_chat or {}).get("msgs", [])
        if s.cw or not m: return
        while m and m[-1]["role"] == "assistant": m.pop()
        if m: t = m.pop()["content"]; s.send(t)

    # --- панель задачи ---
    def task_panel(s):
        w = QWidget(); l = QVBoxLayout(w); l.setContentsMargins(6, 6, 6, 6); s.t_title = QLabel("Нет выбранной задачи"); s.t_title.setStyleSheet("font-weight:600;font-size:14px"); s.t_title.setWordWrap(True)
        s.t_stat = QLabel(); s.t_prog = QProgressBar(); s.t_prog.setRange(0, 100); l.addWidget(s.t_title); l.addWidget(s.t_stat); l.addWidget(s.t_prog)
        s.t_stages = QListWidget(); s.t_stages.setMaximumHeight(125); l.addWidget(s.t_stages)
        r = QHBoxLayout(); s.b_pause = btn("⏸ Пауза", s.pause_resume, "Пауза / продолжить"); r.addWidget(s.b_pause); r.addWidget(btn("✕ Отмена", s.cancel_task)); r.addWidget(btn("↻ Повтор", s.rerun_task)); l.addLayout(r)
        r = QHBoxLayout(); s.cp = QComboBox(); r.addWidget(s.cp, 1); r.addWidget(btn("К checkpoint", s.restore_cp, "Восстановить задачу из checkpoint")); l.addLayout(r)
        s.t_tabs = QTabWidget(); s.t_plan = QPlainTextEdit(); s.t_plan.setReadOnly(True); s.t_found = QListWidget(); s.t_tools = QTreeWidget(); s.t_tools.setHeaderLabels(["Инструмент", "Аргументы", "Результат"])
        s.t_tools.itemDoubleClicked.connect(lambda it, _: QMessageBox.information(s, it.text(0), it.data(2, Qt.UserRole) or ""))
        s.t_chg = QListWidget(); s.t_chg.itemDoubleClicked.connect(lambda it: s.review(s.t_chg.row(it))); s.t_res = QPlainTextEdit(); s.t_res.setReadOnly(True)
        for wd, n in ((s.t_plan, "План"), (s.t_found, "Найдено"), (s.t_tools, "Инструменты"), (s.t_chg, "Изменения"), (s.t_res, "Проверка")): s.t_tabs.addTab(wd, n)
        l.addWidget(s.t_tabs, 1); r = QHBoxLayout(); r.addWidget(btn("Просмотреть diff", lambda: s.review(s.t_chg.currentRow()), "Двухпанельный Diff Viewer"))
        r.addWidget(btn("Итоговый diff…", s.final_diff)); l.addLayout(r); s.t_info = QLabel(); l.addWidget(s.t_info); return w
    def show_task(s):
        t = s.cur_task
        if not t: return
        s.t_title.setText(t["title"]); st = t["status"]; s.t_stat.setText(f"Статус: {st}  ·  Этап: {STAGES[min(t['stage'], 4)]}  ·  ⏱ {t['duration']} с")
        s.t_prog.setValue(100 if st == "завершена" else int(t["stage"] / 5 * 100)); s.t_stages.clear()
        for i, n in enumerate(STAGES):
            m = "✔" if i < t["stage"] or st == "завершена" else ("▶" if i == t["stage"] and st == "выполняется" else ("⏸" if i == t["stage"] and st == "приостановлена" else "○"))
            s.t_stages.addItem(f"{m}  {n}")
        s.b_pause.setText("▶ Продолжить" if st == "приостановлена" else "⏸ Пауза"); s.cp.clear(); [s.cp.addItem(f"{c['ts']} · после {STAGES[c['stage'] - 1]}", c) for c in t["checkpoints"]]
        s.t_plan.setPlainText(t["plan"] or "План ещё не составлен"); s.t_found.clear(); s.t_found.addItems(t["found"] or ["Файлы ещё не найдены"])
        s.t_tools.clear()
        for x in t["tools"]: it = QTreeWidgetItem([x["name"], x["args"][:40], x["res"][:60].replace("\n", " ")]); it.setData(2, Qt.UserRole, x["res"]); s.t_tools.addTopLevelItem(it)
        s.t_chg.clear(); [s.t_chg.addItem(f"{c['path']} — {c['status']}") for c in t["changes"]] or s.t_chg.addItem("Изменений нет")
        s.t_res.setPlainText((t["verify"] + "\n\n" + t["result"] + ("\n⚠ " + t["error"] if t.get("error") else "")).strip() or "Проверка ещё не выполнялась")
        s.t_info.setText(f"Лимиты: {s.cfg['max_steps']} шагов / {s.cfg['max_time']} с  ·  Навыки: {', '.join(s.cfg['skills_on']) or '—'}")
    def start_task(s):
        t = s.cur_task
        if not t or (s.runner and s.runner.isRunning()): return s.toast("Агент уже выполняет задачу" if s.runner and s.runner.isRunning() else "Нет задачи", True)
        if not s.cfg["model"]: return s.toast("Выберите модель в Model Manager", True)
        s.runner = Runner(t, dict(s.cfg), s.root, s.sys_prompt()); s.runner.changed.connect(s.on_task_changed); s.runner.warn.connect(lambda m: s.toast("⚠ " + m, True))
        s.runner.log.connect(s.log); s.runner.finished.connect(lambda: (s.busy(False), s.toast(f"Задача: {t['status']}", t["status"] == "ошибка"))); s.busy(True); s.runner.start()
    def on_task_changed(s):
        s.jsave("tasks.json", s.tasks); s.refresh_tasks(); s.show_task()
        if s.cur_task: s.l_task.setText(f"🤖 {s.cur_task['status']}")
    def pause_resume(s):
        t = s.cur_task
        if not t: return
        r = s.runner
        if t["status"] == "выполняется" and r: r.ev.clear(); t["status"] = "приостановлена"
        elif t["status"] == "приостановлена":
            t["status"] = "выполняется"
            if r and r.isRunning() and r.t is t: r.ev.set()
            else: t["status"] = "ожидает"; s.start_task()
        s.on_task_changed()
    def cancel_task(s):
        t = s.cur_task
        if not t or t["status"] not in ("выполняется", "приостановлена", "ожидает"): return
        if s.runner and s.runner.isRunning(): s.runner.cancel = True; s.runner.ev.set()
        else: t["status"] = "отменена"; s.on_task_changed()
    def rerun_task(s):
        t = s.cur_task
        if not t or (s.runner and s.runner.isRunning()): return
        t.update(stage=0, status="ожидает", duration=0, plan="", found=[], tools=[], changes=[], checkpoints=[], verify="", result="", error=""); s.start_task()
    def restore_cp(s):
        t, c = s.cur_task, s.cp.currentData()
        if not t or not c or (s.runner and s.runner.isRunning()): return
        t["stage"] = c["stage"]; t["status"] = "приостановлена"; t["plan"] = c["plan"]; t["checkpoints"] = [x for x in t["checkpoints"] if x["stage"] <= c["stage"]]
        if c["stage"] <= 2: t["changes"] = []
        s.on_task_changed(); s.toast("Задача восстановлена из checkpoint — нажмите «Продолжить»")
    def review(s, i):
        t = s.cur_task
        if not t or i < 0 or i >= len(t["changes"]): return
        c = t["changes"][i]; p = (s.root / c["path"]).resolve(); old = p.read_text("utf-8") if p.exists() else ""; warn = ""
        if s.root.resolve() not in p.parents: warn = "Файл находится ВНЕ папки проекта!"
        elif old and len(c["new"].splitlines()) < len(old.splitlines()) * 0.4: warn = "Изменение удаляет более 60% содержимого файла."
        elif not p.exists(): warn = "Будет создан новый файл."
        d = DiffDlg(c["path"], old, c["new"], warn, c["status"] == "ожидает"); r = d.exec()
        if c["status"] != "ожидает" or r == 0: return
        if r == 1:
            if warn.startswith("Файл находится ВНЕ") and s.cfg["sandbox"]: return s.toast("Sandbox запрещает запись вне проекта", True)
            try:
                p.parent.mkdir(parents=True, exist_ok=True); p.write_text(c["new"], "utf-8"); c["status"] = "применено"; s.toast(f"Применено: {c['path']}")
                for k in range(s.tabs.count()):
                    e = s.tabs.widget(k)
                    if e.path == str(p): e.setPlainText(c["new"]); e.document().setModified(False)
            except Exception as x: s.toast(f"Ошибка записи: {x}", True)
        else: c["status"] = "отклонено"
        s.on_task_changed()
    def final_diff(s):
        t = s.cur_task
        if not t or not t["changes"]: return s.toast("Нет изменений", True)
        old, new = [], []
        for c in t["changes"]:
            p = s.root / c["path"]; old.append(f"# ===== {c['path']}\n" + (p.read_text("utf-8") if p.exists() else "")); new.append(f"# ===== {c['path']}\n" + c["new"])
        DiffDlg("итог задачи", "\n".join(old), "\n".join(new), pending=False).exec()
    def tick(s):
        if s.cur_task and s.runner and s.runner.isRunning() and s.cur_task["status"] == "выполняется": s.cur_task["duration"] += 1; s.show_task()

    # ---------- проект ----------
    def open_project(s):
        d = QFileDialog.getExistingDirectory(s, "Выберите корневую папку проекта", str(s.root or Path.home()))
        if d: s.root = Path(d); s.load_project()
    def new_project(s):
        d = QFileDialog.getExistingDirectory(s, "Где создать проект?")
        n, ok = QInputDialog.getText(s, "Новый проект", "Название:") if d else ("", False)
        if ok and n:
            try: (Path(d) / n).mkdir(); s.root = Path(d) / n; s.load_project()
            except Exception as e: s.toast(f"Не удалось создать проект: {e}", True)
    def load_project(s):
        r = s.root
        if r and not os.access(r, os.R_OK): s.toast("Нет доступа к папке проекта", True); s.root = r = None
        s.q.setValue("root", str(r or "")); s.proj_lbl.setText(f"📂 {r.name}\n{r}" if r else "Проект не открыт. Нажмите «Открыть».")
        s.l_proj.setText(f"📂 {r.name}" if r else "Нет проекта"); s.l_model.setText("🧠 " + (s.cfg["model"] or "модель не выбрана")); s.setWindowTitle(f"Agent Studio — {r.name}" if r else "Agent Studio")
        if r: s.fm.setRootPath(str(r)); s.tree.setRootIndex(s.fm.index(str(r)))
        s.tasks = s.jload("tasks.json", []) if r else []; s.chats = s.jload("chats.json", []); s.mcp = s.jload("mcp.json", {}); s.cur_chat = s.chats[-1] if s.chats else None; s.cur_task = None
        for t in s.tasks:
            if t["status"] == "выполняется": t["status"] = "приостановлена"
        s.refresh_tasks(); s.refresh_chats(); s.refresh_skills(); s.refresh_mcp(); s.mem.setPlainText(s.mem_path().read_text("utf-8") if r and s.mem_path().exists() else ""); s.mem.document().setModified(False)
        s.fetch_models()

    # ---------- состояние окна ----------
    def restore(s):
        g = s.q.value("geom")
        if g: s.restoreGeometry(g)
        for n, w in (("hs", s.hs), ("vs", s.vs)):
            v = s.q.value(n)
            if v: w.restoreState(v)
        for p in json.loads(s.q.value("tabs", "[]")):
            if os.path.exists(p): s.open_file(p)
    def closeEvent(s, ev):
        paths = [s.tabs.widget(i).path for i in range(s.tabs.count())]
        for i in reversed(range(s.tabs.count())):
            if not s.close_tab(i): return ev.ignore()
        s.q.setValue("tabs", json.dumps(paths)); s.q.setValue("geom", s.saveGeometry()); s.q.setValue("hs", s.hs.saveState()); s.q.setValue("vs", s.vs.saveState()); s.save_cfg()
        if s.runner and s.runner.isRunning(): s.runner.cancel = True; s.runner.ev.set(); s.runner.wait(2000)
        if s.gproc: s.gproc.kill()
        ev.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv); app.setApplicationName("Agent Studio"); w = Main(); w.show(); sys.exit(app.exec())
