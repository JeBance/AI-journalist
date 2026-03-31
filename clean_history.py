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

# Используем HistoryManager для работы с месячными архивами
from ai_journalist.history_manager import HistoryManager

HISTORY_DIR = Path("/root/git/AI-journalist/06_history")
history_manager = HistoryManager(str(HISTORY_DIR))
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


def get_all_posts_from_monthly() -> list:
    """Получить все посты из месячных файлов."""
    all_posts = []
    posts_by_file = {}
    
    for post in history_manager.get_all_posts():
        all_posts.append({
            "date": post['date'],
            "title": post['title'],
            "body": post['body'],
            "raw": f"### [{post['date']}] {post['title']}\n\n{post['body']}",
            "file": post['file']
        })
        if post['file'] not in posts_by_file:
            posts_by_file[post['file']] = []
        posts_by_file[post['file']].append(all_posts[-1])
    
    return all_posts, posts_by_file


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


def clean_monthly_file(file_path: Path, posts_to_remove: list) -> str:
    """Удалить дубликаты из месячного файла."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Удаляем дубликаты
    for post in posts_to_remove:
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

    # Чтение истории из месячных файлов
    print(f"\n📄 Чтение истории из месячных архивов...")
    all_posts, posts_by_file = get_all_posts_from_monthly()
    total_posts = len(all_posts)
    print(f"✅ Найдено {total_posts} публикаций в {len(posts_by_file)} файлах")
    
    # Поиск дубликатов
    print("\n🔍 Поиск дубликатов...")
    duplicates = find_duplicates(all_posts)

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

        # Группируем дубликаты по файлам
        duplicates_by_file = {}
        for pattern, posts_list in duplicates.items():
            for i, post in enumerate(posts_list):
                # Оставляем одну запись (самую раннюю)
                if len(posts_list) > 1 and i > 0:
                    file_name = post.get('file', 'published_posts_2026-03.md')
                    if file_name not in duplicates_by_file:
                        duplicates_by_file[file_name] = []
                    duplicates_by_file[file_name].append(post)

        # Обрабатываем каждый файл
        for file_name, posts_to_remove in duplicates_by_file.items():
            file_path = HISTORY_DIR / file_name
            
            # Backup
            backup_file = file_path.with_suffix(".md.backup")
            with open(file_path, "r", encoding="utf-8") as f:
                original_content = f.read()
            with open(backup_file, "w", encoding="utf-8") as f:
                f.write(original_content)
            
            # Очищаем файл
            new_content = clean_monthly_file(file_path, posts_to_remove)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            
            print(f"  📁 {file_name}: удалено {len(posts_to_remove)} дубликатов")
        
        # Обновляем индекс
        history_manager._update_main_index()
        
        print(f"\n✅ Удалено {total_duplicates} дубликатов!")

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
