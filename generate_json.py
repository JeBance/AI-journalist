#!/usr/bin/env python3
"""
AI-journalist — Генератор articles.json

Парсит markdown-файлы из 06_history/ и создаёт единый articles.json
для сайта ai.jebance.ru

Запуск:
    python3 generate_json.py
"""

import re
import json
from pathlib import Path
from datetime import datetime

HISTORY_DIR = Path(__file__).parent / "06_history"
OUTPUT_FILE = Path(__file__).parent / "articles.json"

# Эмодзи категорий
EMOJI_MAP = {
    "ai": "\U0001f916",
    "ai_tools": "\U0001f916",
    "javascript": "\U0001f7e8",
    "typescript": "\U0001f7e8",
    "python": "\U0001f40d",
    "rust": "\U0001f980",
    "go": "\U0001f535",
    "php": "\U0001f418",
    "css": "\U0001f3a8",
    "html": "\U0001f3a8",
    "security": "\U0001f512",
    "vpn_security": "\U0001f512",
    "privacy": "\U0001f512",
    "hardware": "\U0001f4bb",
    "devops": "\U0001f433",
    "docker": "\U0001f433",
    "kubernetes": "\U0001f433",
    "databases": "\U0001f5c4\ufe0f",
    "postgresql": "\U0001f5c4\ufe0f",
    "tutorial": "\U0001f4da",
    "news": "\U0001f4f0",
    "google": "\U0001f50d",
    "apple": "\U0001f34e",
    "microsoft": "\U0001f5d3\ufe0f",
    "anthropic": "\U0001f916",
    "telegram": "\U00002708\ufe0f",
    "linux": "\U0001f427",
    "web": "\U0001f310",
    "mobile": "\U0001f4f1",
    "ai_models": "\U0001f916",
    "llm": "\U0001f916",
    "opensource": "\U0001f4e6",
    "default": "\U0001f4d6",
}


def parse_monthly_file(filepath: Path) -> list:
    """Парсить один месячный файл и вернуть список статей."""
    articles = []

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Паттерн для статьи: ### [YYYY-MM-DD] Title\n\n- **Категория:** ...\n...
    pattern = r"### \[(\d{4}-\d{2}-\d{2})\] (.+?)\n\n(.*?)(?=---\n\n### |$)"
    matches = re.findall(pattern, content, re.DOTALL)

    for date_str, title, body in matches:
        article = {
            "id": 0,  # будет назначено позже
            "date": date_str,
            "title": title.strip(),
            "category": "",
            "tags": [],
            "description": "",
            "telegraph_url": "",
            "telegram_id": 0,
            "status": "",
            "sources": [],
            "emoji": "\U0001f4d6",
        }

        # Категория
        cat_match = re.search(r"\*\*Категория:\*\* (.+)", body)
        if cat_match:
            article["category"] = cat_match.group(1).strip()

        # Теги
        tags_match = re.search(r"\*\*Ключевые темы:\*\* (.+)", body)
        if tags_match:
            article["tags"] = [
                t.strip() for t in tags_match.group(1).split(",") if t.strip()
            ]

        # Источники
        sources = re.findall(r"  - (.+?)(?:\n|$)", body)
        article["sources"] = [s.strip() for s in sources if s.strip()]

        # Telegra.ph URL
        tele_match = re.search(r"\*\*Telegra\.ph URL:\*\* (.+)", body)
        if tele_match:
            article["telegraph_url"] = tele_match.group(1).strip()

        # Telegram ID
        tg_match = re.search(r"\*\*Telegram ID:\*\* (\d+)", body)
        if tg_match:
            article["telegram_id"] = int(tg_match.group(1))

        # Статус
        status_match = re.search(r"\*\*Статус:\*\* (.+)", body)
        if status_match:
            article["status"] = status_match.group(1).strip()

        # Описание (берём из источников если нет явного)
        article["description"] = _generate_description(article)

        # Эмодзи
        article["emoji"] = EMOJI_MAP.get(
            article["category"], EMOJI_MAP.get("default")
        )

        articles.append(article)

    return articles


def _generate_description(article: dict) -> str:
    """Сгенерировать краткое описание из данных статьи."""
    tags = article["tags"][:5]  # первые 5 тегов
    category = article["category"]
    if tags:
        return f"{category}: {', '.join(tags)}"
    return category


def main():
    """Главная функция."""
    print("=" * 60)
    print("AI-journalist: Генерация articles.json")
    print("=" * 60)

    all_articles = []

    # Ищем все месячные файлы
    pattern = re.compile(r"published_posts_(\d{4}-\d{2})\.md")
    if not HISTORY_DIR.exists():
        print(f"\u274c Директория не найдена: {HISTORY_DIR}")
        return

    for filepath in sorted(HISTORY_DIR.iterdir()):
        if pattern.match(filepath.name):
            print(f"\U0001f4c2 Парсинг {filepath.name}...")
            articles = parse_monthly_file(filepath)
            all_articles.extend(articles)
            print(f"  \u2705 {len(articles)} статей")

    # Сортируем по дате (новые первыми)
    all_articles.sort(key=lambda a: a["date"], reverse=True)

    # Назначаем ID
    for i, article in enumerate(all_articles, 1):
        article["id"] = i

    # Сохраняем
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_articles, f, indent=2, ensure_ascii=False)

    file_size = OUTPUT_FILE.stat().st_size
    print(f"\n\U00002705 articles.json создан!")
    print(f"   \U0001f4d6 {len(all_articles)} статей")
    print(f"   \U0001f4be Размер: {file_size / 1024:.1f} KB")
    print("=" * 60)


if __name__ == "__main__":
    main()
