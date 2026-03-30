#!/usr/bin/env python3
"""
AI-journalist Formatting Utilities

Утилиты для правильного форматирования текста для Telegram и Telegra.ph.

Использование:
    from formatting import escape_markdown_v2, format_post
    
    text = escape_markdown_v2("PHP 8.4 > 8.3 #тег")
    post = format_post("Заголовок", "Текст", ["теги"])
"""

import re
from typing import List, Optional, Dict, Any
from datetime import datetime


# ============================================================================
# Telegram MarkdownV2 экранирование
# ============================================================================

def escape_markdown_v2(text: str) -> str:
    """
    Экранировать специальные символы для Telegram MarkdownV2.
    
    Специальные символы: _ * [ ] ( ) ~ ` > # + - = | { } . !
    
    Args:
        text: Исходный текст
    
    Returns:
        Текст с экранированными специальными символами
    
    Пример:
        >>> escape_markdown_v2("PHP 8.4 > 8.3 #тег")
        'PHP 8\\.4 \\> 8\\.3 \\#тег'
    """
    # Сначала экранируем обратный слэш
    text = text.replace('\\', '\\\\')
    
    # Затем экранируем остальные специальные символы
    for char in '_*[]()~`>#+-=|{}.!':
        text = text.replace(char, '\\' + char)
    
    return text


def escape_hashtags_only(text: str) -> str:
    """
    Экранировать только хэштеги (сохраняет читаемость остального текста).
    
    Args:
        text: Текст с хэштегами
    
    Returns:
        Текст с экранированными хэштегами
    """
    def escape_match(match):
        return '\\' + match.group(0)
    
    return re.sub(r'(#\w+)', escape_match, text)


def escape_for_telegram(text: str, mode: str = "markdown_v2") -> str:
    """
    Экранировать текст для Telegram.
    
    Args:
        text: Исходный текст
        mode: Режим экранирования ("markdown_v2", "html", "hashtags_only")
    
    Returns:
        Экранированный текст
    """
    if mode == "markdown_v2":
        return escape_markdown_v2(text)
    elif mode == "hashtags_only":
        return escape_hashtags_only(text)
    elif mode == "html":
        # HTML не требует экранирования, но конвертируем Markdown
        return markdown_to_html(text)
    else:
        return text


# ============================================================================
# Конвертация Markdown → HTML
# ============================================================================

def markdown_to_html(text: str) -> str:
    """
    Конвертировать Markdown в HTML для Telegram.
    
    Поддерживает:
    - **жирный** → <b>жирный</b>
    - _курсив_ → <i>курсив</i>
    - `код` → <code>код</code>
    - [ссылка](url) → <a href="url">ссылка</a>
    
    Args:
        text: Текст в Markdown
    
    Returns:
        Текст в HTML
    """
    # Жирный **текст**
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    
    # Курсив _текст_
    text = re.sub(r'_(.+?)_', r'<i>\1</i>', text)
    
    # Код `текст`
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    
    # Ссылки [текст](url)
    text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', text)
    
    return text


# ============================================================================
# Форматирование постов
# ============================================================================

def format_post(
    title: str,
    content: str,
    hashtags: Optional[List[str]] = None,
    emoji: str = "🔥",
    sources: Optional[List[str]] = None,
    auto_escape: bool = True
) -> str:
    """
    Сформатировать пост для Telegram.
    
    Args:
        title: Заголовок поста
        content: Основной текст
        hashtags: Список хэштегов (без #)
        emoji: Эмодзи для заголовка
        sources: Список источников
        auto_escape: Автоматически экранировать текст
    
    Returns:
        Готовый пост для Telegram (MarkdownV2)
    
    Пример:
        >>> post = format_post(
        ...     title="Node.js security релиз",
        ...     content="Исправлены уязвимости...",
        ...     hashtags=["nodejs", "security"],
        ...     emoji="🔒"
        ... )
    """
    # Формируем текст
    lines = [
        f"{emoji} *{title}*",
        "",
        content
    ]
    
    # Добавляем источники если есть
    if sources:
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("🔗 Источники")
        lines.append("")
        for source in sources:
            lines.append(f"· {source}")
    
    # Добавляем хэштеги
    if hashtags:
        lines.append("")
        hashtag_line = " ".join([f"#{tag}" for tag in hashtags])
        lines.append(hashtag_line)
    
    post = "\n".join(lines)
    
    # Экранируем если нужно
    if auto_escape:
        post = escape_markdown_v2(post)
    
    return post


def format_news_post(
    headline: str,
    summary: str,
    details: List[str],
    category: str,
    sources: Optional[List[str]] = None,
    auto_escape: bool = True
) -> str:
    """
    Сформатировать пост с новостью по шаблону.
    
    Args:
        headline: Заголовок новости
        summary: Краткое описание (1-2 предложения)
        details: Список деталей/фактов
        category: Категория новости
        sources: Список источников
        auto_escape: Автоматически экранировать текст
    
    Returns:
        Готовый пост для Telegram
    """
    emoji_map = {
        "javascript": "🟨",
        "php": "🐘",
        "css": "🎨",
        "vpn_security": "🔒",
        "hardware": "💻",
        "devops": "🐳",
        "databases": "🗄️",
        "ai_tools": "🤖",
        "patterns": "📐"
    }
    
    emoji = emoji_map.get(category, "🔥")
    
    lines = [
        f"{emoji} *{headline}*",
        "",
        summary,
        "",
        "📌 Детали:",
        ""
    ]
    
    for detail in details:
        lines.append(f"· {detail}")
    
    if sources:
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("🔗 Источники")
        lines.append("")
        for source in sources:
            lines.append(f"· {source}")
    
    lines.append("")
    lines.append(f"\\#{category}")
    
    post = "\n".join(lines)
    
    if auto_escape:
        post = escape_markdown_v2(post)
    
    return post


def format_tutorial_post(
    title: str,
    introduction: str,
    steps: List[Dict[str, str]],
    conclusion: str,
    tags: List[str],
    auto_escape: bool = True
) -> str:
    """
    Сформатировать пост-туториал.
    
    Args:
        title: Заголовок туториала
        introduction: Введение
        steps: Список шагов [{"title": "...", "content": "..."}]
        conclusion: Заключение
        tags: Теги
        auto_escape: Автоматически экранировать
    
    Returns:
        Готовый пост для Telegram
    """
    lines = [
        f"📚 *{title}*",
        "",
        introduction,
        ""
    ]
    
    for i, step in enumerate(steps, 1):
        lines.append(f"*Шаг {i}: {step['title']}*")
        lines.append(step['content'])
        lines.append("")
    
    lines.append(conclusion)
    lines.append("")
    lines.append(" ".join([f"\\#{tag}" for tag in tags]))
    
    post = "\n".join(lines)
    
    if auto_escape:
        post = escape_markdown_v2(post)
    
    return post


# ============================================================================
# Форматирование для Telegra.ph
# ============================================================================

def format_telegraph_article(
    title: str,
    introduction: str,
    sections: List[Dict[str, Any]],
    conclusion: str = "",
    sources: Optional[List[str]] = None
) -> str:
    """
    Сформатировать статью для Telegra.ph.
    
    Args:
        title: Заголовок статьи
        introduction: Введение
        sections: Секции [{"heading": "...", "content": "...", "type": "text|code|list"}]
        conclusion: Заключение
        sources: Источники
    
    Returns:
        Статья в формате Markdown для Telegra.ph
    """
    lines = [
        introduction,
        ""
    ]
    
    for section in sections:
        lines.append(f"## {section['heading']}")
        lines.append("")
        
        if section.get('type') == 'code':
            lines.append("```")
            lines.append(section['content'])
            lines.append("```")
        elif section.get('type') == 'list':
            for item in section['content']:
                lines.append(f"· {item}")
        else:
            lines.append(section['content'])
        
        lines.append("")
    
    if conclusion:
        lines.append("## Заключение")
        lines.append("")
        lines.append(conclusion)
        lines.append("")
    
    if sources:
        lines.append("---")
        lines.append("")
        lines.append("Источники:")
        lines.append("")
        for source in sources:
            # Преобразуем "Название (URL)" → "[Название](URL)"
            source_link = source.strip()
            url_match = re.search(r'\((https?://[^)]+)\)$', source_link)
            if url_match:
                name = source_link[:url_match.start()].strip()
                url = url_match.group(1)
                source_link = f"[{name}]({url})"
            lines.append(f"· {source_link}")

    return "\n".join(lines)


# ============================================================================
# Утилиты для дат и времени
# ============================================================================

def get_current_date_russian() -> str:
    """
    Получить текущую дату на русском языке.
    
    Returns:
        Строка с датой в формате "DD месяц YYYY"
    
    Пример:
        >>> get_current_date_russian()
        '26 марта 2026'
    """
    month_names = {
        1: "января", 2: "февраля", 3: "марта", 4: "апреля",
        5: "мая", 6: "июня", 7: "июля", 8: "августа",
        9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"
    }
    
    now = datetime.now()
    day = now.day
    month = month_names[now.month]
    year = now.year
    
    return f"{day} {month} {year}"


def get_current_datetime_iso() -> str:
    """
    Получить текущую дату и время в ISO формате.
    
    Returns:
        Строка в формате "YYYY-MM-DD HH:MM"
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M")


# ============================================================================
# Примеры использования
# ============================================================================

if __name__ == "__main__":
    print("Formatting Utilities - Примеры")
    print("=" * 60)
    
    # Пример экранирования
    print("\n1. Экранирование MarkdownV2:")
    test_text = "PHP 8.4 > 8.3 #тег [ссылка](url)"
    print(f"   Исходный: {test_text}")
    print(f"   Экранированный: {escape_markdown_v2(test_text)}")
    
    # Пример форматирования поста
    print("\n2. Форматирование поста:")
    post = format_post(
        title="Node.js security релиз",
        content="Исправлены 9 уязвимостей в Node.js",
        hashtags=["nodejs", "security", "javascript"],
        emoji="🔒"
    )
    print(f"   {post[:100]}...")
    
    # Пример даты
    print("\n3. Текущая дата:")
    print(f"   {get_current_date_russian()}")
    
    print("\n" + "=" * 60)
