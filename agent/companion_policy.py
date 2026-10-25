"""Coding-only delegation and plain speech for Lola; never grants file access."""
import html
import re


def is_coding_request(prompt):
    """Conservative intent gate based on the human request, not a model rewrite."""
    text = str(prompt or '').casefold()
    if re.search(r'код\s+(?:двер|домофон|подъезд|доступ|подтвержден|скидк|купона|песни|да\s+винчи)|промокод|программ[ауы]\s+(?:праздник|концерт|мероприят|путешеств|телепередач)|функци\w*\s+(?:холодильник|организм|печени|сердц|телевизор|государств)', text):
        return False
    if re.search(r'\b(?:typeerror|syntaxerror|traceback|debug|refactor|programming|coding|программирован\w*|рефактор\w*|отлад\w*|баг\w*)\b', text):
        return True
    if re.search(r'(?:напиши|создай|сделай|исправь|объясни|проверь|доработай|разработай|измени|добавь|перепиши|оптимизируй|write|create|build|fix|explain|implement).{0,90}(?:\bкод\b|\bcode\b|сайт|скрипт|функци|приложени|программ|репозитор|алгоритм|компонент|тест\w*\s+(?:для|на)\s+код)', text):
        return True
    return bool(re.search(r'(?:python|javascript|typescript|html|css|sql|c\+\+|rust|react|vue|java\b|\.py\b|\.tsx\b|\.js\b).{0,80}(?:ошиб|код|функци|класс|напиши|исправ|не\s+работ|error|fix)|(?:ошиб|код|функци|класс|напиши|исправ|не\s+работ|error|fix).{0,80}(?:python|javascript|typescript|html|css|sql|c\+\+|rust|react|vue|java\b|\.py\b|\.tsx\b|\.js\b)', text))


def clean_speech_text(text):
    """Remove presentation markup, not meaningful letters, numbers or punctuation."""
    value = html.unescape(str(text or ''))
    value = re.sub(r'<(?:think|analysis)>[\s\S]*?</(?:think|analysis)>', '', value, flags=re.I)
    value = re.sub(r'```[^\n]*\n[\s\S]*?(?:```|$)', 'Код доступен в основном чате.', value)
    value = re.sub(r'!\[([^\]]*)\]\([^\n)]*\)', r'\1', value)
    value = re.sub(r'\[([^\]]+)\]\([^\n)]*\)', r'\1', value)
    value = re.sub(r'<[^>\n]+>', '', value)
    value = re.sub(r'(?m)^\s*(?:#{1,6}\s+|>\s*|[-+*•]\s+|\d+[.)]\s+)', '', value)
    value = re.sub(r'(?m)^\s*[-=_]{3,}\s*$', '', value)
    value = re.sub(r'(\d)\s*\*\s*(\d)', r'\1 умножить на \2', value)
    value = re.sub(r'(?<=\w)_(?=\w)', ' ', value)
    value = value.replace('\\*', '').replace('*', '').replace('`', '').replace('~', '').replace('_', '')
    value = re.sub(r'[ \t]+', ' ', value)
    return re.sub(r'\n{3,}', '\n\n', value).strip()
