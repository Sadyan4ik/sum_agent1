import re

def basic_clean(text):
    if not isinstance(text, str):
        return text
    text = re.sub(r'\n', ' ', text)  # Замена переносов строк на пробелы
    text = re.sub(r'\s+', ' ', text)  # Удаляем лишних пробелов
    return text.strip()

def advanced_clean(text):
    if not isinstance(text, str):
        return ''

    text = basic_clean(text)
    # Удаляем url, email и теги
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\S+@\S+', '', text)
    text = re.sub(r'<.*?>', '', text)

    # Фиксируем пробелы вокруг пунктуации
    text = re.sub(r'\s+([.,!?:;])', r'\1', text)
    text = re.sub(r'([.,!?:;])\s+', r'\1 ', text)

    return re.sub(r'\s+', ' ', text).strip()

def clean_text(text, advanced=False):
    if not isinstance(text, str):
        return text

    return advanced_clean(text) if advanced else basic_clean(text)