from summarization import *

def sum_agent(text, parsed_content, model, tokenizer):
    cleaned_basic = clean_text(text, advanced=False)
    parsed_content = parse_html_content(cleaned_basic)

    summarized = summarize_structure_fully_combined(parsed_content, model, tokenizer)

    return summarized