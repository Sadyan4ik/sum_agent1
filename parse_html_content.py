from bs4 import BeautifulSoup
from typing import List, Dict, Union


def parse_html_content(html_content: str):
    soup = BeautifulSoup(html_content, 'html.parser')
    result = []
    current_header = None
    current_content = []

    def process_element(element):
        nonlocal current_content

        if element.name in ['h1', 'h2', 'h3']:
            return element.get_text(strip=True)
        elif element.name == 'blockquote':
            parts = []
            current_part = []

            for child in element.children:
                if child.name == 'br':
                    if current_part:
                        parts.append(' '.join(current_part))
                        current_part = []
                else:
                    text = child.get_text(strip=True)
                    if text:
                        current_part.append(text)

            if current_part:
                parts.append(' '.join(current_part))

            if parts:
                current_content.append(parts)
        elif element.name == 'ul':
            list_items = [li.get_text(strip=True) for li in element.find_all('li', recursive=False)]
            if list_items:
                current_content.append(list_items)
        elif element.name is None or element.name not in ['br', 'b']:
            text = element.get_text(strip=True)
            if text:
                current_content.append(text)

    for element in soup.children:
        if element.name in ['h1', 'h2', 'h3']:
            if current_content:
                result.append({
                    'header': current_header,
                    'content': current_content.copy()
                })
                current_content = []

            current_header = element.get_text(strip=True)
        else:
            process_element(element)

    if current_content:
        result.append({
            'header': current_header,
            'content': current_content.copy()
        })

    return result