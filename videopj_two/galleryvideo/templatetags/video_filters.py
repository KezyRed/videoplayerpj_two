from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.filter
def format_description(value):
    """
    Фильтр для форматирования описания видео с поддержкой:
    - Списков (*, -, •)
    - Нумерованных списков (1., 2., etc.)
    - Отступов (пробелы в начале строки)
    - Жирного текста (**текст**)
    - Курсива (*текст*)
    """
    if not value:
        return ""
    
    # Разбиваем текст на строки
    lines = value.split('\n')
    formatted_lines = []
    in_list = False
    in_ordered_list = False
    
    for line in lines:
        original_line = line
        line = line.rstrip()
        
        # Подсчитываем отступы
        indent_count = len(original_line) - len(original_line.lstrip())
        
        # Обработка списков
        if re.match(r'^\s*[\*\-•]\s+', line):
            if not in_list:
                formatted_lines.append('<ul>')
                in_list = True
            if in_ordered_list:
                formatted_lines.append('</ol>')
                in_ordered_list = False
            
            # Извлекаем текст элемента списка
            list_text = re.sub(r'^\s*[\*\-•]\s+', '', line)
            list_text = format_inline_text(list_text)
            formatted_lines.append(f'<li>{list_text}</li>')
            
        elif re.match(r'^\s*\d+\.\s+', line):
            if not in_ordered_list:
                if in_list:
                    formatted_lines.append('</ul>')
                    in_list = False
                formatted_lines.append('<ol>')
                in_ordered_list = True
            
            # Извлекаем текст элемента списка
            list_text = re.sub(r'^\s*\d+\.\s+', '', line)
            list_text = format_inline_text(list_text)
            formatted_lines.append(f'<li>{list_text}</li>')
            
        else:
            # Закрываем списки если они были открыты
            if in_list:
                formatted_lines.append('</ul>')
                in_list = False
            if in_ordered_list:
                formatted_lines.append('</ol>')
                in_ordered_list = False
            
            if line.strip():
                # Обычная строка с возможными отступами
                formatted_text = format_inline_text(line.strip())
                if indent_count > 0:
                    indent_class = f"indent-{min(indent_count // 4, 3)}"
                    formatted_lines.append(f'<p class="{indent_class}">{formatted_text}</p>')
                else:
                    formatted_lines.append(f'<p>{formatted_text}</p>')
            else:
                # Пустая строка
                if formatted_lines and not formatted_lines[-1].endswith(('</ul>', '</ol>')):
                    formatted_lines.append('<br>')
    
    # Закрываем списки в конце если нужно
    if in_list:
        formatted_lines.append('</ul>')
    if in_ordered_list:
        formatted_lines.append('</ol>')
    
    return mark_safe('\n'.join(formatted_lines))

def format_inline_text(text):
    """Форматирование инлайн элементов: жирный текст, курсив"""
    # Жирный текст **текст**
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    
    # Курсив *текст* (но не затрагиваем ** которые уже обработаны)
    text = re.sub(r'(?<!\*)\*([^*]+?)\*(?!\*)', r'<em>\1</em>', text)
    
    return text

@register.filter
def simple_format(value):
    """Простое форматирование только с переносами строк"""
    if not value:
        return ""
    
    # Заменяем двойные переносы на параграфы
    paragraphs = value.split('\n\n')
    formatted_paragraphs = []
    
    for paragraph in paragraphs:
        if paragraph.strip():
            # Заменяем одинарные переносы на <br>
            formatted_paragraph = paragraph.replace('\n', '<br>')
            formatted_paragraphs.append(f'<p>{formatted_paragraph}</p>')
    
    return mark_safe('\n'.join(formatted_paragraphs))