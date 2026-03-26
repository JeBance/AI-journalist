#!/usr/bin/env python3
"""
AI-journalist Headless Generator

Генерирует новость в headless режиме с полным системным промптом.
AI изучает все файлы проекта и генерирует данные на русском языке.

Использование:
    python3 /root/git/AI-journalist/headless_generator.py
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime


# ============================================================================
# СИСТЕМНЫЙ ПРОМПТ
# ============================================================================

SYSTEM_PROMPT = """
Ты — главный редактор и технический журналист Telegram-канала @JeBanceOnline.

═════════════════════════════════════════════════════════════════════════════
📁 ИНФРАСТРУКТУРА ДЛЯ ИЗУЧЕНИЯ
═══════════════════════════════════════════════════════════════════════════════

Вся инфраструктура находится в /root/git/AI-journalist/

ОБЯЗАТЕЛЬНО изучи эти файлы перед генерацией:

1. 01_system_prompts/00_main_prompt.md — базовые инструкции
2. 01_system_prompts/00_learned_prompts.md — накопленные знания
3. 01_system_prompts/02_headless_system_prompt.md — детальный промпт
4. 06_history/01_published_posts.md — история публикаций (ПРОВЕРЬ УНИКАЛЬНОСТЬ!)
5. 02_sources/02_github_repos.md — GitHub репозитории
6. 03_templates/01_single_post.md — шаблон поста

═══════════════════════════════════════════════════════════════════════════════
🌐 ЯЗЫК — ВСЕГДА РУССКИЙ!
═══════════════════════════════════════════════════════════════════════════════

⚠️ КРИТИЧЕСКИ ВАЖНО: ВЕСЬ ТЕКСТ ДОЛЖЕН БЫТЬ НА РУССКОМ ЯЗЫКЕ!

- Заголовок — на русском
- Описание — на русском
- Статья — на русском
- Жирный текст — на русском!
- Хэштеги — на русском (можно английские технические термины)

НЕПРАВИЛЬНО (АНГЛИЙСКИЙ — БЛОКИРУЕТСЯ!):
  "title": "Node.js Emergency Security Release"
  "content": "**Critical** vulnerability fixed"

ПРАВИЛЬНО (РУССКИЙ — РАЗРЕШЕНО):
  "title": "Node.js выпустил экстренные security-патчи"
  "content": "**Критическая** уязвимость исправлена"

═══════════════════════════════════════════════════════════════════════════════
📝 ЗАДАЧА
═══════════════════════════════════════════════════════════════════════════════

1. Исследуй источники из папки 02_sources/
2. Проверь историю в 06_history/ (уникальность темы — не публиковалось ли за 30 дней!)
3. Найди свежую IT-новость за последние 48 часов
4. Сгенерируй JSON файл /tmp/ai_news.json

═══════════════════════════════════════════════════════════════════════════════
📋 ФОРМАТ JSON
═══════════════════════════════════════════════════════════════════════════════

Создай файл /tmp/ai_news.json со следующей структурой:

{
  "title": "Заголовок на русском (макс 80 символов, БЕЗ эмодзи)",
  "description": "Краткое описание на русском (2-3 предложения)",
  "content": "Текст статьи на русском в Markdown (БЕЗ заголовка в начале!)",
  "hashtags": ["тег1", "тег2", "тег3"],
  "sources": ["Источник 1", "Источник 2"],
  "author_name": "AI Journalist",
  "author_url": "https://t.me/JeBanceOnline"
}

═══════════════════════════════════════════════════════════════════════════════
📝 ПРАВИЛА ФОРМАТИРОВАНИЯ
═══════════════════════════════════════════════════════════════════════════════

1. Заголовок:
   - Без эмодзи (добавится автоматически)
   - Без специальных символов Markdown
   - На русском языке
   - Максимум 80 символов

2. Описание:
   - 2-3 предложения на русском
   - Без ссылок и хэштегов

3. Статья (content):
   - НЕ включай заголовок (#) в начале
   - Используй ## для разделов
   - Используй **жирный на русском** для выделения
   - Используй · для списков
   - Используй [ссылка](url) для ссылок
   - ВСЕГДА на русском языке

   НЕПРАВИЛЬНО: "**Critical** vulnerability"
   ПРАВИЛЬНО: "**Критическая** уязвимость"

4. Хэштеги:
   - Без символа # (добавится автоматически)
   - 3-5 штук
   - Можно смешивать русский и английский

═══════════════════════════════════════════════════════════════════════════════
✅ ПРИМЕР ПРАВИЛЬНОГО JSON
═══════════════════════════════════════════════════════════════════════════════

{
  "title": "Node.js выпустил экстренные security-патчи",
  "description": "Node.js выпустил экстренные обновления для всех активных версий. Исправлены 9 уязвимостей, включая 2 критические.",
  "content": "Node.js выпустил экстренные security-релизы для всех активных версий.\\n\\n## Какие уязвимости исправлены\\n\\n· **Критическая** (CVE-2026-21637) — DoS через TLS SNI\\n· **Высокий уровень** (CVE-2026-21710) — DoS через __proto__\\n\\n## Что делать\\n\\nОбновитесь до последней версии.\\n\\n---\\n\\nИсточники:\\n· Node.js Security Announcement",
  "hashtags": ["javascript", "security", "nodejs"],
  "sources": ["Node.js Security Announcement", "GitHub"],
  "author_name": "AI Journalist",
  "author_url": "https://t.me/JeBanceOnline"
}

═══════════════════════════════════════════════════════════════════════════════
🚫 ЗАПРЕЩЕНО (БУДЕТ ЗАБЛОКИРОВАНО)
═══════════════════════════════════════════════════════════════════════════════

❌ Текст на английском языке
❌ Заголовок с эмодзи
❌ Дублирование заголовка в content
❌ Непарные **жирные** теги
❌ Хэштеги с символом #
❌ Тема, опубликованная за последние 30 дней

═══════════════════════════════════════════════════════════════════════════════
✅ ПРОВЕРКА ПЕРЕД ГЕНЕРАЦИЕЙ
═══════════════════════════════════════════════════════════════════════════════

Перед созданием JSON проверь:

1. ✅ Тема уникальна (проверь 06_history/02_topics_covered.md)
2. ✅ Весь текст на русском языке
3. ✅ Заголовок без эмодзи и Markdown
4. ✅ Content без заголовка в начале
5. ✅ Все **жирные** теги парные
6. ✅ Хэштеги без #
7. ✅ Источники указаны (1-3)

═══════════════════════════════════════════════════════════════════════════════
🚀 ГЕНЕРИРУЙ JSON ПРЯМО СЕЙЧАС!
═══════════════════════════════════════════════════════════════════════════════

Создай файл /tmp/ai_news.json с правильными данными на русском языке.
"""


# ============================================================================
# ГЛАВНАЯ ФУНКЦИЯ
# ============================================================================

def main():
    """Запустить headless генерацию с системным промптом."""
    print("=" * 70)
    print("🤖 AI-JOURNALIST HEADLESS ГЕНЕРАЦИЯ")
    print("=" * 70)
    print(f"📅 Дата: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print()
    
    # Шаг 1: Проверка инфраструктуры
    print("📁 Проверка инфраструктуры...")
    infrastructure_files = [
        "/root/git/AI-journalist/01_system_prompts/00_main_prompt.md",
        "/root/git/AI-journalist/01_system_prompts/00_learned_prompts.md",
        "/root/git/AI-journalist/01_system_prompts/02_headless_system_prompt.md",
        "/root/git/AI-journalist/06_history/01_published_posts.md",
        "/root/git/AI-journalist/02_sources/02_github_repos.md",
    ]
    
    for file_path in infrastructure_files:
        if Path(file_path).exists():
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} — НЕ НАЙДЕН!")
    
    print()
    
    # Шаг 2: Запуск qwen с системным промптом
    print("🤖 Генерация новости через qwen...")
    print("(AI изучает файлы проекта и генерирует данные на русском)")
    print()
    
    try:
        # Запускаем qwen с системным промптом
        result = subprocess.run(
            ["qwen", "-o", "text"],
            input=SYSTEM_PROMPT,
            capture_output=True,
            text=True,
            timeout=600,  # 10 минут на генерацию
            env={**dict(os.environ), "HOME": "/root"}
        )
        
        print(f"qwen завершён (код: {result.returncode})")
        print()
        
        # Шаг 3: Проверка результата
        json_file = Path("/tmp/ai_news.json")
        
        if json_file.exists():
            print("✅ JSON сгенерирован!")
            print()
            
            # Читаем и показываем превью
            import json
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            print("=" * 70)
            print("📝 ПРЕВЬЮ СГЕНЕРИРОВАННЫХ ДАННЫХ")
            print("=" * 70)
            print(f"📌 Заголовок: {data.get('title', 'НЕТ')}")
            print(f"📄 Описание: {data.get('description', 'НЕТ')[:100]}...")
            print(f"🏷️ Хэштеги: {', '.join(data.get('hashtags', []))}")
            print(f"📊 Категория: {data.get('hashtags', ['НЕТ'])[0]}")
            print("=" * 70)
            print()

            # ============================================
            # ВАЛИДАЦИЯ КОНТЕНТА (КРИТИЧЕСКИ ВАЖНО!)
            # ============================================
            print("🔍 ВАЛИДАЦИЯ КОНТЕНТА...")
            validation_errors = []

            title = data.get('title', '')
            description = data.get('description', '')
            content = data.get('content', '')
            hashtags = data.get('hashtags', [])

            # 1. Проверка на русский язык (кириллица)
            has_cyrillic_title = any('а' <= c.lower() <= 'я' or c == 'ё' for c in title)
            has_cyrillic_desc = any('а' <= c.lower() <= 'я' or c == 'ё' for c in description)

            if not has_cyrillic_title:
                validation_errors.append("❌ Заголовок на английском (должен быть на русском)")

            if not has_cyrillic_desc:
                validation_errors.append("❌ Описание на английском (должно быть на русском)")

            # 2. Проверка заголовка на эмодзи
            import re
            emoji_pattern = re.compile("["
                u"\U0001F600-\U0001F64F"  # emoticons
                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                u"\U0001F1E0-\U0001F1FF"  # flags
                "]+", flags=re.UNICODE)

            if emoji_pattern.search(title):
                validation_errors.append("❌ Заголовок содержит эмодзи (запрещено)")

            # 3. Проверка заголовка на Markdown символы
            if title.startswith('#') or '**' in title or '_' in title:
                validation_errors.append("❌ Заголовок содержит Markdown символы")

            # 4. Проверка длины заголовка
            if len(title) > 80:
                validation_errors.append(f"❌ Заголовок слишком длинный ({len(title)} > 80 символов)")

            # 5. Проверка content на дублирование заголовка в начале
            if content.startswith(title[:50]):
                validation_errors.append("❌ Content дублирует заголовок в начале")

            # 6. Проверка content на наличие заголовка #
            if content.strip().startswith('#'):
                validation_errors.append("❌ Content начинается с # (запрещено)")

            # 7. Проверка парности ** жирных тегов
            bold_count = content.count('**')
            if bold_count % 2 != 0:
                validation_errors.append(f"❌ Непарные ** теги ({bold_count} штук)")

            # 8. Проверка хэштегов на #
            for tag in hashtags:
                if tag.startswith('#'):
                    validation_errors.append(f"❌ Хэштег начинается с #: {tag}")

            # 9. Проверка количества хэштегов
            if len(hashtags) < 3:
                validation_errors.append(f"❌ Мало хэштегов ({len(hashtags)} < 3)")

            if len(hashtags) > 5:
                validation_errors.append(f"❌ Много хэштегов ({len(hashtags)} > 5)")

            # 10. Проверка источников
            sources = data.get('sources', [])
            if len(sources) < 1:
                validation_errors.append("❌ Нет источников (минимум 1)")

            # ============================================
            # РЕЗУЛЬТАТ ВАЛИДАЦИИ
            # ============================================

            if validation_errors:
                print()
                print("🚫 ВАЛИДАЦИЯ НЕ ПРОЙДЕНА!")
                print()
                for error in validation_errors:
                    print(error)
                print()
                print("Публикация ЗАБЛОКИРОВАНА!")
                print("Исправьте ошибки и запустите генерацию заново.")
                return False
            else:
                print("✅ Все проверки пройдены!")
                print()

            # Проверяем язык (для совместимости)
            if not has_cyrillic_title or not has_cyrillic_desc:
                print("⚠️  ПРЕДУПРЕЖДЕНИЕ: Текст на английском!")
                print("   AI не прочитал системный промпт.")
                print("   Попробуйте запустить ещё раз.")
                print()
            else:
                print("✅ Текст на русском языке!")
                print()

            # ============================================
            # ПРОВЕРКА НА ДУБЛИКАТЫ (КРИТИЧЕСКИ ВАЖНО!)
            # ============================================
            print("🔍 ПРОВЕРКА НА ДУБЛИКАТЫ...")
            print()

            # Добавляем путь к модулю
            sys.path.insert(0, "/root/git/AI-journalist")
            from check_duplicates import check_topic_duplicate, check_title_in_history

            # Определяем категорию по первому хэштегу
            news_category = hashtags[0] if hashtags else None

            # Проверка 1: Дубликат темы
            is_topic_dup, topic_reason = check_topic_duplicate(title, news_category)
            if is_topic_dup:
                print("🚫 ДУБЛИКАТ ТЕМЫ НАЙДЕН!")
                print(f"   Причина: {topic_reason}")
                print()
                print("Публикация ЗАБЛОКИРОВАНА!")
                print("Выберите другую тему или укажите 'обновление' в заголовке.")
                return False
            else:
                print(f"✅ Тема уникальна (категория: {news_category or 'не указана'})")

            # Проверка 2: Дубликат заголовка в истории
            is_title_dup, title_reason = check_title_in_history(title, days=30)
            if is_title_dup:
                print("🚫 ДУБЛИКАТ ЗАГОЛОВКА В ИСТОРИИ!")
                print(f"   Причина: {title_reason}")
                print()
                print("Публикация ЗАБЛОКИРОВАНА!")
                print("Выберите другую тему.")
                return False
            else:
                print("✅ Заголовок не найден в истории (за 30 дней)")

            print()
            print("✅ Все проверки на дубликаты пройдены!")
            print()

            # Шаг 4: Публикация
            print("📢 Запуск публикации...")
            print()
            
            pub_result = subprocess.run(
                ["python3", "/root/git/AI-journalist/publisher_final.py", "--input", str(json_file)],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            print(pub_result.stdout)
            
            if pub_result.returncode != 0:
                print(f"❌ Ошибка публикации: {pub_result.stderr}")
                return False
            
            return True
            
        else:
            print("❌ JSON файл не создан!")
            print()
            print("Вывод qwen:")
            print(result.stdout[:500] if result.stdout else "Пусто")
            return False
        
    except subprocess.TimeoutExpired:
        print("❌ Превышено время ожидания (5 мин)")
        return False
    
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False


if __name__ == "__main__":
    import os
    success = main()
    sys.exit(0 if success else 1)
