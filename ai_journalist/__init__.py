#!/usr/bin/env python3
"""
AI-journalist Library

Централизованная библиотека для взаимодействия с Telegram и Telegra.ph.
Все функции протестированы и используют правильное форматирование.

Использование:
    from ai_journalist import TelegramClient, TelegraphClient, format_post
    
    # Telegram
    tg = TelegramClient()
    result = tg.send_message("Текст сообщения")
    
    # Telegra.ph
    tph = TelegraphClient()
    article = tph.create_page("Заголовок", "Содержимое")
    
    # Форматирование
    post = format_post("Заголовок", "Текст", ["теги"])
"""

from .telegram_client import TelegramClient
from .telegraph_client import TelegraphClient
from .formatting import (
    escape_markdown_v2,
    escape_hashtags_only,
    escape_for_telegram,
    markdown_to_html,
    format_post,
    format_news_post,
    format_tutorial_post,
    format_telegraph_article,
    get_current_date_russian,
    get_current_datetime_iso
)

__version__ = "1.0.0"
__all__ = [
    # Клиенты
    "TelegramClient",
    "TelegraphClient",
    
    # Форматирование
    "escape_markdown_v2",
    "escape_hashtags_only",
    "escape_for_telegram",
    "markdown_to_html",
    "format_post",
    "format_news_post",
    "format_tutorial_post",
    "format_telegraph_article",
    "get_current_date_russian",
    "get_current_datetime_iso"
]


# ============================================================================
# Примеры использования (Quick Start)
# ============================================================================

def quick_start_example():
    """Пример быстрого старта."""
    print("=" * 60)
    print("AI-jOURNALIST LIBRARY - QUICK START")
    print("=" * 60)
    
    # Пример 1: Отправка сообщения в Telegram
    print("\n1. ОТПРАВКА СООБЩЕНИЯ В TELEGRAM:")
    print("""
    from ai_journalist import TelegramClient, format_post
    
    # Инициализация
    tg = TelegramClient()
    
    # Вариант A: Готовый пост с форматированием
    post = format_post(
        title="Node.js security релиз",
        content="Исправлены 9 уязвимостей",
        hashtags=["nodejs", "security"],
        emoji="🔒"
    )
    
    # Отправка (auto_escape=True по умолчанию)
    result = tg.send_message(post)
    print(f"Message ID: {result['message_id']}")
    """)
    
    # Пример 2: Публикация статьи на Telegra.ph
    print("\n2. ПУБЛИКАЦИЯ СТАТЬИ НА TELEGRAPH.PH:")
    print("""
    from ai_journalist import TelegraphClient
    
    tph = TelegraphClient()
    
    article_content = '''
    ## Введение
    
    Текст введения.
    
    ## Основная часть
    
    · Пункт 1
    · Пункт 2
    
    ## Заключение
    
    Выводы.
    '''
    
    result = tph.create_page(
        title="Моя статья",
        content=article_content
    )
    
    print(f"URL: {result['url']}")
    """)
    
    # Пример 3: Публикация с анонсом
    print("\n3. ПУБЛИКАЦИЯ С АНОНСОМ В TELEGRAM:")
    print("""
    from ai_journalist import TelegraphClient, TelegramClient
    
    tph = TelegraphClient()
    tg = TelegramClient()
    
    # Публикуем статью
    article = tph.create_page(
        title="PHP 8.4: полное руководство",
        content="Содержимое статьи..."
    )
    
    # Создаём анонс
    announcement = tph.create_announcement_post(
        article_url=article["url"],
        title="PHP 8.4: полное руководство",
        description="Разбираем новые фичи"
    )
    
    # Публикуем анонс
    tg.send_message(announcement, auto_escape=False)
    """)
    
    # Пример 4: Автоматическое экранирование
    print("\n4. АВТОМАТИЧЕСКОЕ ЭКРАНИРОВАНИЕ:")
    print("""
    from ai_journalist import escape_markdown_v2
    
    text = "PHP 8.4 > 8.3 #тег"
    escaped = escape_markdown_v2(text)
    # Результат: "PHP 8\\.4 \\> 8\\.3 \\#тег"
    """)
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    quick_start_example()
