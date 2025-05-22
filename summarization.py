from transformers import T5ForConditionalGeneration, T5Tokenizer
from clean_text import clean_text
from text_str import text
from parse_html_content import parse_html_content

# Загрузка токенизатора и модели
model = T5ForConditionalGeneration.from_pretrained("./my_t5_summarizer_v2")
tokenizer = T5Tokenizer.from_pretrained("./my_t5_summarizer_v2")

def summarize_structure_fully_combined(structure, model, tokenizer):
    def summarize_text(text: str):
        inputs = tokenizer("summarize: " + text, return_tensors="pt",
                           max_length=512, truncation=True)
        outputs = model.generate(
            inputs["input_ids"],
            max_length=200,
            min_length=50,
            num_beams=5,
            length_penalty=2.0,
            no_repeat_ngram_size=2,
            early_stopping=True
        )
        return tokenizer.decode(outputs[0], skip_special_tokens=True)

    def process_item(item):
        """Рекурсивные списки преобразует в список строк"""
        if isinstance(item, str):
            return item
        elif isinstance(item, list):
            processed_items = []
            for subitem in item:
                processed_items.append(process_item(subitem))
            return " ".join(processed_items)
        return str(item)

    def combine_content(section):
        """Объединяет все строки в одну строку"""
        text_parts = []
        for item in section['content']:
            text_parts.append(process_item(item))
        return " ".join(text_parts) if text_parts else ""

    for section in structure:
        full_text = combine_content(section)

        if full_text:
            section['content'] = [summarize_text(full_text)]
        else:
            section['content'] = []

    return structure

cleaned_basic = clean_text(text, advanced=False)

parsed_content = parse_html_content(cleaned_basic)

summarized = summarize_structure_fully_combined(parsed_content, model, tokenizer)

print(summarized)