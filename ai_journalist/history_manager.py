#!/usr/bin/env python3
"""
AI-journalist History Manager

Управление архивом опубликованных постов с поддержкой месячных файлов.

Автоматически создаёт файлы по месяцам:
- 06_history/published_posts_2026-03.md
- 06_history/published_posts_2026-04.md
- ...

Основной файл 01_published_posts.md остаётся как индекс с ссылками на архивы.

Использование:
    from history_manager import HistoryManager
    
    manager = HistoryManager("/root/git/AI-journalist/06_history")
    manager.add_post(title, category, hashtags, sources, telegraph_url, telegram_id)
"""

import re
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Any


class HistoryManager:
    """Менеджер истории публикаций с поддержкой месячных архивов."""
    
    def __init__(self, history_dir: str):
        """
        Инициализировать менеджер истории.
        
        Args:
            history_dir: Путь к директории 06_history
        """
        self.history_dir = Path(history_dir)
        self.main_index_file = self.history_dir / "01_published_posts.md"
        self.topics_file = self.history_dir / "02_topics_covered.md"
        
    def _get_monthly_file(self, date: datetime) -> Path:
        """
        Получить путь к файлу за указанный месяц.
        
        Args:
            date: Дата для определения месяца
            
        Returns:
            Путь к файлу published_posts_YYYY-MM.md
        """
        month_str = date.strftime("%Y-%m")
        return self.history_dir / f"published_posts_{month_str}.md"
    
    def _get_monthly_file_pattern(self) -> str:
        """Получить regex паттерн для поиска месячных файлов."""
        return r"published_posts_(\d{4}-\d{2})\.md"
    
    def _parse_date_from_title(self, title: str) -> Optional[datetime]:
        """
        Извлечь дату из заголовка вида [YYYY-MM-DD] Title.
        
        Args:
            title: Заголовок с датой
            
        Returns:
            datetime или None
        """
        match = re.search(r'\[(\d{4}-\d{2}-\d{2})\]', title)
        if match:
            return datetime.strptime(match.group(1), "%Y-%m-%d")
        return None
    
    def _create_monthly_file_header(self, month: str) -> str:
        """
        Создать заголовок для месячного файла.
        
        Args:
            month: Строка месяца в формате YYYY-MM
            
        Returns:
            Заголовок файла
        """
        month_name = {
            '01': 'Январь', '02': 'Февраль', '03': 'Март',
            '04': 'Апрель', '05': 'Май', '06': 'Июнь',
            '07': 'Июль', '08': 'Август', '09': 'Сентябрь',
            '10': 'Октябрь', '11': 'Ноябрь', '12': 'Декабрь'
        }
        
        year, month_num = month.split('-')
        name = month_name.get(month_num, month_num)
        
        return f"""# Архив публикаций: {name} {year}

Автоматически сгенерированный файл с публикациями за {month}.

---

"""
    
    def _create_main_index_header(self) -> str:
        """
        Создать заголовок для основного файла-индекса.
        
        Returns:
            Заголовок индексного файла
        """
        return """# Архив опубликованных постов

## 📋 О структуре

Архив разбит на месячные файлы для удобства работы:
- `published_posts_YYYY-MM.md` — публикации за конкретный месяц
- Этот файл (01_published_posts.md) — индекс с ссылками на архивы

## 📁 Месячные архивы

"""
    
    def get_all_posts(self) -> List[Dict[str, Any]]:
        """
        Получить все посты из всех месячных файлов.
        
        Returns:
            Список постов
        """
        posts = []
        
        # Ищем все месячные файлы
        pattern = re.compile(self._get_monthly_file_pattern())
        for file in self.history_dir.iterdir():
            if pattern.match(file.name):
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Парсим посты
                post_pattern = r'### \[(\d{4}-\d{2}-\d{2})\] (.+?)\n\n(.*?)(?=---\n\n### |$)'
                matches = re.findall(post_pattern, content, re.DOTALL)
                
                for date, title, body in matches:
                    posts.append({
                        'date': date,
                        'title': title,
                        'body': body.strip(),
                        'file': file.name
                    })
        
        return posts
    
    def add_post(self, title: str, category: str, hashtags: List[str],
                 sources: List[str], telegraph_url: str,
                 telegram_message_id: str, template: str = "telegra.ph article") -> str:
        """
        Добавить новый пост в соответствующий месячный файл.
        
        Args:
            title: Заголовок поста
            category: Категория
            hashtags: Список хэштегов
            sources: Список источников
            telegraph_url: URL статьи на Telegra.ph
            telegram_message_id: ID сообщения в Telegram
            template: Название шаблона
            
        Returns:
            Путь к файлу, куда добавлен пост
        """
        today = datetime.now()
        today_str = today.strftime("%Y-%m-%d")
        month_str = today.strftime("%Y-%m")
        
        # Определяем целевой файл
        monthly_file = self._get_monthly_file(today)
        
        # Формируем запись
        entry = f"""### [{today_str}] {title}

- **Категория:** {category}
- **Шаблон:** {template}
- **Ключевые темы:** {", ".join(hashtags)}
- **Источники:**
"""
        for source in sources:
            entry += f"  - {source}\n"
        
        entry += f"""- **Telegra.ph URL:** {telegraph_url}
- **Telegram ID:** {telegram_message_id}
- **Статус:** опубликован

---

"""
        
        # Создаём или дополняем файл
        if monthly_file.exists():
            with open(monthly_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Вставляем перед статистикой если есть
            if "## 📊 Статистика" in content:
                content = content.replace("## 📊 Статистика", entry + "## 📊 Статистика")
            else:
                content += entry
        else:
            # Создаём новый файл
            content = self._create_monthly_file_header(month_str) + entry
        
        with open(monthly_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Обновляем главный индекс
        self._update_main_index()
        
        return str(monthly_file)
    
    def _update_main_index(self):
        """Обновить главный индексный файл со ссылками на архивы."""
        # Находим все месячные файлы
        pattern = re.compile(self._get_monthly_file_pattern())
        monthly_files = []
        
        for file in self.history_dir.iterdir():
            match = pattern.match(file.name)
            if match:
                monthly_files.append((match.group(1), file))
        
        # Сортируем по убыванию (новые сверху)
        monthly_files.sort(reverse=True)
        
        # Формируем содержимое индекса
        index_content = self._create_main_index_header()
        
        for month, file in monthly_files:
            # Считаем количество постов
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
            post_count = content.count("### [")
            
            # Добавляем ссылку
            month_name = {
                '01': 'Январь', '02': 'Февраль', '03': 'Март',
                '04': 'Апрель', '05': 'Май', '06': 'Июнь',
                '07': 'Июль', '08': 'Август', '09': 'Сентябрь',
                '10': 'Октябрь', '11': 'Ноябрь', '12': 'Декабрь'
            }
            year, month_num = month.split('-')
            name = month_name.get(month_num, month_num)
            
            index_content += f"### {name} {year}\n\n"
            index_content += f"- **Файл:** `{file.name}`\n"
            index_content += f"- **Постов:** {post_count}\n\n"
        
        # Добавляем раздел статистики
        index_content += "## 📊 Общая статистика\n\n"
        index_content += "| Месяц | Файл | Постов |\n"
        index_content += "|-------|------|--------|\n"
        
        for month, file in monthly_files:
            with open(file, 'r', encoding='utf-8') as f:
                post_count = f.read().count("### [")
            year, month_num = month.split('-')
            name = month_name.get(month_num, month_num)
            index_content += f"| {name} {year} | `{file.name}` | {post_count} |\n"
        
        index_content += "\n---\n\n"
        index_content += "## 📝 Правила добавления\n\n"
        index_content += "1. **Посты добавляются автоматически** через `publisher_final.py`\n"
        index_content += "2. **Не редактируй месячные файлы вручную** — используйте HistoryManager\n"
        index_content += "3. **Проверяй дубликаты** через `check_duplicates.py` перед публикацией\n"
        
        with open(self.main_index_file, 'w', encoding='utf-8') as f:
            f.write(index_content)
    
    def add_topic(self, title: str, category: str):
        """
        Добавить тему в файл topics_covered.md.
        
        Args:
            title: Заголовок темы
            category: Категория
        """
        repeat_date = datetime.now().strftime("%Y-%m-%d")
        topic_entry = f"- **Тема:** {title} | **Дата публикации:** {repeat_date} | **Повторять можно не ранее:** {repeat_date}\n\n"
        
        if self.topics_file.exists():
            with open(self.topics_file, 'r', encoding='utf-8') as f:
                topics = f.read()
        else:
            topics = "# Уникальные темы\n\n"
        
        # Находим категорию
        category_section = f"## {category}"
        if category_section in topics:
            topics = topics.replace(category_section, f"{category_section}\n{topic_entry}")
        else:
            topics += f"\n{category_section}\n{topic_entry}"
        
        with open(self.topics_file, 'w', encoding='utf-8') as f:
            f.write(topics)
    
    def migrate_existing_posts(self):
        """
        Мигрировать существующие посты из основного файла в месячные архивы.
        
        Вызывается один раз при переходе на новую систему.
        """
        if not self.main_index_file.exists():
            return
        
        with open(self.main_index_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Находим все посты
        post_pattern = r'(### \[(\d{4}-\d{2}-\d{2})\] .*?)(?=---\n\n### |---\n\n## |\Z)'
        matches = re.findall(post_pattern, content, re.DOTALL)

        # Группируем по месяцам
        posts_by_month: Dict[str, List[str]] = {}

        for full_post, date in matches:
            month = date[:7]  # YYYY-MM
            if month not in posts_by_month:
                posts_by_month[month] = []
            posts_by_month[month].append(full_post)
        
        # Создаём месячные файлы
        for month, posts in sorted(posts_by_month.items()):
            monthly_file = self.history_dir / f"published_posts_{month}.md"
            
            file_content = self._create_monthly_file_header(month)
            
            for post in posts:
                file_content += post + "\n---\n\n"
            
            # Добавляем статистику
            file_content += "## 📊 Статистика месяца\n\n"
            file_content += f"| Показатель | Значение |\n"
            file_content += f"|------------|----------|\n"
            file_content += f"| Постов | {len(posts)} |\n\n"
            
            with open(monthly_file, 'w', encoding='utf-8') as f:
                f.write(file_content)
        
        # Обновляем индекс
        self._update_main_index()


# ============================================================================
# Утилиты для обратной совместимости
# ============================================================================

def get_history_manager() -> HistoryManager:
    """Получить экземпляр HistoryManager для стандартного пути."""
    return HistoryManager("/root/git/AI-journalist/06_history")


if __name__ == "__main__":
    print("History Manager — тестовый запуск")
    print("=" * 60)
    
    manager = get_history_manager()
    
    # Показываем текущие файлы
    print("\n📁 Месячные архивы:")
    pattern = re.compile(manager._get_monthly_file_pattern())
    for file in sorted(manager.history_dir.iterdir()):
        if pattern.match(file.name):
            with open(file, 'r', encoding='utf-8') as f:
                post_count = f.read().count("### [")
            print(f"   {file.name}: {post_count} постов")
    
    print("\n" + "=" * 60)
