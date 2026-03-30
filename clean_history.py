#!/usr/bin/env python3
"""
AI-journalist History Cleaner

Очищает историю от AI-generated дубликатов.
Находит похожие заголовки и предлагает удалить их.

Использование:
    python3 /root/git/AI-journalist/clean_history.py --dry-run  # превью
    python3 /root/git/AI-journalist/clean_history.py --clean    # очистка
"""

import re
import sys
import argparse
from pathlib import Path
from datetime import datetime

HISTORY_FILE = Path("/root/git/AI-journalist/06_history/01_published_posts.md")
TOPICS_FILE = Path("/root/git/AI-journalist/06_history/02_topics_covered.md")

# Ключевые слова AI-generated дубликатов
AI_GENERATED_PATTERNS = [
    r"2026: Год, когда ИИ стал",
    r"2026: Год, когда ИИ перестал",
    r"Революция в разработке: \d+ технологий",
    r"Топ-\d+ AI-инструментов",
    r"ИИ пишет код лучше.*",
    r"Будущее разработки с ИИ",
]


def parse_history(content: str) -> list:
    """Распарсить историю публикаций."""
    pattern = r'### \[(\d{4}-\d{2}-\d{2})\] (.+?)\n(.*?)(?=### \[|$)'
    matches = re.findall(pattern, content, re.DOTALL)
    
    posts = []
    for date, title, body in matches:
        posts.append({
            "date": date,
            "title": title.strip(),
            "body": body.strip(),
            "raw": f"### [{date}] {title}\n{body}"
        })
    
    return posts


def find_duplicates(posts: list) -> dict:
    """Найти дубликаты по ключевым словам."""
    duplicates = {}
    
    for pattern in AI_GENERATED_PATTERNS:
        for post in posts:
            if re.search(pattern, post["title"], re.IGNORECASE):
                if pattern not in duplicates:
                    duplicates[pattern] = []
                duplicates[pattern].append(post)
    
    return duplicates


def clean_history(posts: list, duplicates: dict) -> str:
    """Удалить дубликаты из истории."""
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Удаляем дубликаты
    for pattern, posts_list in duplicates.items():
        for post in posts_list:
            # Оставляем одну запись (самую раннюю)
            if len(posts_list) > 1 and post != posts_list[0]:
                content = content.replace(post["raw"], "")
    
    # Удаляем двойные пустые строки
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    return content


def main():
    """Главная функция."""
    parser = argparse.ArgumentParser(description="Очистка истории от AI-generated дубликатов")
    parser.add_argument("--dry-run", action="store_true", help="Только показать дубликаты")
    parser.add_argument("--clean", action="store_true", help="Удалить дубликаты")
    parser.add_argument("--force", action="store_true", help="Удалить без подтверждения")
    args = parser.parse_args()
    
    print("=" * 70)
    print("🧹 AI-JOURNALIST HISTORY CLEANER")
    print("=" * 70)
    
    if not HISTORY_FILE.exists():
        print(f"❌ Файл не найден: {HISTORY_FILE}")
        return False
    
    # Чтение истории
    print(f"\n📄 Чтение истории...")
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    
    posts = parse_history(content)
    print(f"✅ Найдено {len(posts)} публикаций")
    
    # Поиск дубликатов
    print("\n🔍 Поиск дубликатов...")
    duplicates = find_duplicates(posts)
    
    if not duplicates:
        print("✅ Дубликаты не найдены!")
        return True
    
    total_duplicates = sum(len(v) for v in duplicates.values())
    print(f"⚠️  Найдено {total_duplicates} дубликатов в {len(duplicates)} категориях\n")
    
    # Вывод дубликатов
    for pattern, posts_list in duplicates.items():
        print(f"\n📌 Паттерн: {pattern}")
        print(f"   Найдено: {len(posts_list)} записей")
        for post in posts_list:
            print(f"   • {post['date']}: {post['title'][:60]}...")
    
    # Очистка
    if args.clean:
        print("\n" + "=" * 70)
        print("🗑️  УДАЛЕНИЕ ДУБЛИКАТОВ")
        print("=" * 70)
        
        if not args.force:
            confirm = input(f"\nУдалить {total_duplicates} дубликатов? (yes/no): ")
            if confirm.lower() != "yes":
                print("❌ Отменено")
                return False
        else:
            print(f"\n🗑️  Удаление {total_duplicates} дубликатов (режим --force)...")
        
        new_content = clean_history(posts, duplicates)
        
        # Backup
        backup_file = HISTORY_FILE.with_suffix(".md.backup")
        with open(backup_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"\n💾 Backup: {backup_file}")
        
        # Запись
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            f.write(new_content)
        
        print(f"✅ Удалено {total_duplicates} дубликатов!")
        
    elif args.dry_run:
        print("\n" + "=" * 70)
        print("📋 DRY RUN - изменения не вносятся")
        print("=" * 70)
        print(f"\nПри запуске с --clean --force будет удалено {total_duplicates} дубликатов")
    
    else:
        print("\n" + "=" * 70)
        print("ℹ️  Используйте --dry-run для превью или --clean --force для очистки")
        print("=" * 70)
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
