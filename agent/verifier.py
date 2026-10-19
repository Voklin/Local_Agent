"""Deterministic stage verification. It does not modify files or grant permissions."""
from __future__ import annotations
class StageVerifier:
    def verify(self, stage_id, *, tool_events=None, final_text="", stop_reason=""):
        events=tool_events or []
        if stop_reason: return {"ok":False,"reason":stop_reason}
        if stage_id in ("implementation", "verification"):
            if any(e.get("tool")=="write_file" and e.get("ok") for e in events):
                return {"ok":True,"reason":"Есть подтверждённый результат инструмента."}
        if final_text.strip(): return {"ok":True,"reason":"Модель сформировала итоговый ответ."}
        return {"ok":False,"reason":"Нет проверяемого результата."}
