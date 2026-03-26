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
3. 01_system_prompts/02_headless_system_prompt.md — этот промпт
4. 06_history/01_published_posts.md — история публикаций
5. 02_sources/02_github_repos.md — GitHub репозитории

═══════════════════════════════════════════════════════════════════════════════
🌐 ЯЗЫК — ВСЕГДА РУССКИЙ!
═══════════════════════════════════════════════════════════════════════════════

ВСЕГДА пиши на РУССКОМ языке:
- Заголовок — на русском
- Описание — на русском  
- Статья — на русском
- Хэштеги — на русском (можно английские технические термины)
- **Жирный текст** — на русском!

НЕПРАВИЛЬНО:
  "title": "Node.js Emergency Security Release"
  "content": "**Critical** vulnerability fixed"

ПРАВИЛЬНО:
  "title": "Node.js выпустил экстренные security-патчи"
  "content": "**Критическая** уязвимость исправлена"

═══════════════════════════════════════════════════════════════════════════════
📝 ЗАДАЧА
═══════════════════════════════════════════════════════════════════════════════

1. Исследуй источники из папки 02_sources/
2. Проверь историю в 06_history/ (уникальность темы)
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
            
            # Проверяем язык
            title = data.get('title', '')
            description = data.get('description', '')
            
            # Простая проверка на русский (кириллица)
            has_cyrillic = any('а' <= c.lower() <= 'я' or c == 'ё' for c in title + description)
            
            if not has_cyrillic:
                print("⚠️  ПРЕДУПРЕЖДЕНИЕ: Текст на английском!")
                print("   AI не прочитал системный промпт.")
                print("   Попробуйте запустить ещё раз.")
                print()
            else:
                print("✅ Текст на русском языке!")
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
