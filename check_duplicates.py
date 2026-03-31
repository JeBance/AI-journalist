#!/usr/bin/env python3
"""
AI-journalist Duplicate Checker

Проверяет темы на дублирование в истории публикаций.
Используется в headless_generator.py и publisher_final.py.

Использование:
    python3 /root/git/AI-journalist/check_duplicates.py "Тема статьи"
    
Или через Python API:
    from check_duplicates import check_topic_duplicate
    is_duplicate, reason = check_topic_duplicate("Тема статьи", "category")
"""

import re
from pathlib import Path
from datetime import datetime, timedelta
from typing import Tuple, Optional, List, Dict

# Используем HistoryManager для работы с месячными архивами
from ai_journalist.history_manager import HistoryManager

HISTORY_DIR = Path("/root/git/AI-journalist/06_history")
history_manager = HistoryManager(str(HISTORY_DIR))
TOPICS_FILE = Path("/root/git/AI-journalist/06_history/02_topics_covered.md")


def parse_topics_file() -> Dict[str, List[Dict]]:
    """
    Парсит файл 02_topics_covered.md и возвращает словарь:
    {
        "category": [
            {
                "topic": "Тема",
                "pub_date": datetime,
                "repeat_date": datetime
            },
            ...
        ],
        ...
    }
    """
    if not TOPICS_FILE.exists():
        return {}
    
    with open(TOPICS_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    
    categories = {}
    current_category = None
    
    # Парсим строки вида:
    # - **Тема:** ... | **Дата публикации:** YYYY-MM-DD | **Повторять можно не ранее:** YYYY-MM-DD
    topic_pattern = re.compile(
        r'-\s+\*\*Тема:\*\*\s+(.+?)\s+\|\s+\*\*Дата публикации:\*\*\s+(\d{4}-\d{2}-\d{2})\s+\|\s+\*\*Повторять можно не ранее:\*\*\s+(\d{4}-\d{2}-\d{2})'
    )
    
    # Парсим заголовки категорий ## category
    category_pattern = re.compile(r'^##\s+(\w+)', re.MULTILINE)
    
    lines = content.split('\n')
    current_category = None
    
    for line in lines:
        # Проверяем заголовок категории
        cat_match = category_pattern.match(line.strip())
        if cat_match:
            cat_name = cat_match.group(1).lower()
            # Пропускаем служебные секции
            if cat_name not in ['цель', 'формат', 'правила', 'исключения', 'обновление', 'проверка']:
                current_category = cat_name
                if current_category not in categories:
                    categories[current_category] = []
            continue
        
        # Проверяем тему
        if current_category:
            topic_match = topic_pattern.search(line)
            if topic_match:
                topic = topic_match.group(1).strip()
                pub_date_str = topic_match.group(2)
                repeat_date_str = topic_match.group(3)
                
                try:
                    pub_date = datetime.strptime(pub_date_str, "%Y-%m-%d")
                    repeat_date = datetime.strptime(repeat_date_str, "%Y-%m-%d")
                    
                    categories[current_category].append({
                        "topic": topic,
                        "pub_date": pub_date,
                        "repeat_date": repeat_date
                    })
                except ValueError:
                    pass
    
    return categories


def normalize_topic(topic: str) -> str:
    """Нормализует тему для сравнения (убирает лишние пробелы, приводит к нижнему регистру)."""
    # Удаляем лишние пробелы
    normalized = ' '.join(topic.split())
    # Приводим к нижнему регистру
    normalized = normalized.lower()
    # Удаляем знаки препинания
    normalized = re.sub(r'[^\w\sа-яё0-9]', '', normalized)
    return normalized


def topics_are_similar(topic1: str, topic2: str, threshold: float = 0.8) -> bool:
    """
    Проверяет схожесть двух тем.
    Использует сравнение по ключевым словам с порогом 0.8 (улучшено).
    
    Изменения в v2.1:
    - Увеличен threshold с 0.7 до 0.8 для уменьшения ложных срабатываний
    - Добавлена проверка на AI-generated дубликаты
    """
    norm1 = normalize_topic(topic1)
    norm2 = normalize_topic(topic2)

    # Полное совпадение
    if norm1 == norm2:
        return True

    # Проверка на AI-generated паттерны (критические дубликаты)
    ai_patterns = [
        r"2026.*год.*когда.*ии",
        r"революция.*разработке.*технологий",
        r"топ.*\d+.*ai.*инструмент",
        r"ии.*пишет.*код.*лучше",
        r"будущее.*разработки.*ии",
    ]
    
    for pattern in ai_patterns:
        if re.search(pattern, norm1, re.IGNORECASE) and re.search(pattern, norm2, re.IGNORECASE):
            return True  # AI-generated дубликаты всегда блокируем

    # Разбиваем на слова
    words1 = set(norm1.split())
    words2 = set(norm2.split())

    # Удаляем стоп-слова
    stop_words = {'и', 'в', 'на', 'с', 'для', 'из', 'о', 'об', 'по', 'при', 'под', 'над', 'через', 'а', 'но', 'или', 'что', 'это', 'как', 'the', 'a', 'an', 'and', 'or', 'это', 'такой', 'такая', 'такое'}
    words1 = words1 - stop_words
    words2 = words2 - stop_words

    if not words1 or not words2:
        return False

    # Считаем пересечение
    intersection = words1 & words2
    union = words1 | words2

    if not union:
        return False

    similarity = len(intersection) / len(union)

    return similarity >= threshold


def check_topic_duplicate(topic: str, category: str = None) -> Tuple[bool, Optional[str]]:
    """
    Проверяет, является ли тема дубликатом.
    
    Args:
        topic: Тема для проверки
        category: Категория (первый хэштег)
    
    Returns:
        (is_duplicate, reason):
        - is_duplicate: True если дубликат
        - reason: Описание причины или None
    """
    categories_data = parse_topics_file()
    normalized_topic = normalize_topic(topic)
    
    # Проверяем по всем категориям если категория не указана
    categories_to_check = [category] if category else list(categories_data.keys())
    
    for cat in categories_to_check:
        if cat not in categories_data:
            continue
            
        for entry in categories_data[cat]:
            existing_topic = entry["topic"]
            pub_date = entry["pub_date"]
            repeat_date = entry["repeat_date"]
            
            # Проверяем схожесть тем
            if topics_are_similar(topic, existing_topic):
                today = datetime.now()
                
                # Если дата повтора ещё не наступила — это дубликат
                if today < repeat_date:
                    days_left = (repeat_date - today).days
                    return True, f"Тема '{existing_topic}' опубликована {pub_date.strftime('%Y-%m-%d')}. Повтор возможен через {days_left} дн. ({repeat_date.strftime('%Y-%m-%d')})"
    
    return False, None


def check_title_in_history(title: str, days: int = 30) -> Tuple[bool, Optional[str]]:
    """
    Проверяет, публиковался ли заголовок в истории за последние N дней.

    Args:
        title: Заголовок для проверки
        days: Количество дней для проверки

    Returns:
        (is_duplicate, reason)
    """
    # Получаем все посты из месячных файлов
    all_posts = history_manager.get_all_posts()

    today = datetime.now()
    cutoff_date = today - timedelta(days=days)

    for post in all_posts:
        pub_date_str = post['date']
        pub_title = post['title'].strip()

        try:
            pub_date = datetime.strptime(pub_date_str, "%Y-%m-%d")

            # Проверяем дату
            if pub_date < cutoff_date:
                continue

            # Проверяем схожесть заголовков
            if topics_are_similar(title, pub_title, threshold=0.6):
                return True, f"Заголовок '{pub_title}' опубликован {pub_date.strftime('%Y-%m-%d')} (менее {days} дней назад)"
        except ValueError:
            pass

    return False, None


def get_category_suggestions() -> List[str]:
    """Возвращает список доступных категорий."""
    categories_data = parse_topics_file()
    return list(categories_data.keys())


def main():
    """Тестовый запуск проверки."""
    import sys
    
    if len(sys.argv) < 2:
        print("Использование: python3 check_duplicates.py \"Тема статьи\" [категория]")
        print()
        print("Доступные категории:", ", ".join(get_category_suggestions()))
        sys.exit(1)
    
    topic = sys.argv[1]
    category = sys.argv[2] if len(sys.argv) > 2 else None
    
    print(f"🔍 Проверка темы: {topic}")
    if category:
        print(f"📁 Категория: {category}")
    print()
    
    # Проверка по темам
    is_dup, reason = check_topic_duplicate(topic, category)
    if is_dup:
        print(f"🚫 ДУБЛИКАТ НАЙДЕН!")
        print(f"   Причина: {reason}")
    else:
        print(f"✅ Тема уникальна (по файлу topics_covered.md)")
    
    # Проверка по истории заголовков
    is_dup_hist, reason_hist = check_title_in_history(topic)
    if is_dup_hist:
        print(f"🚫 ДУБЛИКАТ В ИСТОРИИ!")
        print(f"   Причина: {reason_hist}")
    else:
        print(f"✅ Заголовок не найден в истории (за 30 дней)")
    
    if is_dup or is_dup_hist:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
