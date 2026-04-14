#!/usr/bin/env python3
"""
AI-journalist Publisher

Скрипт для публикации статей на Telegra.ph с анонсом в Telegram.
Принимает данные от AI-агента и публикует в идеальном формате.

Использование:
    python3 publisher_final.py \
        --title "Заголовок статьи" \
        --description "Краткое описание (1-2 предложения)" \
        --content "Полный текст статьи в Markdown" \
        --hashtags "ai,технологии,практика" \
        --sources "Источник 1,Источник 2"

Или через JSON:
    python3 publisher_final.py --input article_data.json
"""

import sys
import json
import argparse
import re
import requests
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any

# Импортируем HistoryManager для работы с месячными архивами
from ai_journalist.history_manager import HistoryManager


# ============================================================================
# КОНФИГУРАЦИЯ
# ============================================================================

TELEGRAM_CONFIG = Path(__file__).parent / "config.json"
TELEGRAPH_CONFIG = Path(__file__).parent / "telegraph_config.json"
HISTORY_DIR = Path(__file__).parent / "06_history"

# HistoryManager для работы с месячными архивами
history_manager = HistoryManager(str(HISTORY_DIR))

# Эмодзи по категориям
EMOJI_MAP = {
    "ai": "🤖",
    "ai_tools": "🤖",
    "javascript": "🟨",
    "php": "🐘",
    "css": "🎨",
    "vpn": "🔒",
    "vpn_security": "🔒",
    "security": "🔒",
    "hardware": "💻",
    "devops": "🐳",
    "databases": "🗄️",
    "patterns": "📐",
    "tutorial": "📚",
    "news": "📰",
    "default": "📖"
}


# ============================================================================
# ЗАГРУЗКА КОНФИГУРАЦИИ
# ============================================================================

def load_telegram_config() -> Dict[str, str]:
    """Загрузить конфигурацию Telegram."""
    if not TELEGRAM_CONFIG.exists():
        raise FileNotFoundError(f"Файл не найден: {TELEGRAM_CONFIG}")
    
    with open(TELEGRAM_CONFIG, "r", encoding="utf-8") as f:
        return json.load(f)


def load_telegraph_config() -> Dict[str, str]:
    """Загрузить конфигурацию Telegra.ph."""
    if not TELEGRAPH_CONFIG.exists():
        # Создаём конфиг по умолчанию
        default_config = {
            "short_name": "AI Journalist",
            "author_name": "AI Journalist",
            "author_url": "https://t.me/JeBanceOnline"
        }
        TELEGRAPH_CONFIG.parent.mkdir(parents=True, exist_ok=True)
        with open(TELEGRAPH_CONFIG, "w", encoding="utf-8") as f:
            json.dump(default_config, f, indent=2, ensure_ascii=False)
        return default_config
    
    with open(TELEGRAPH_CONFIG, "r", encoding="utf-8") as f:
        config = json.load(f)
        if "access_token" not in config:
                raise ValueError(
                "Access Token не найден!\n"
                "Запустите: python3 get_telegraph_token.py"
            )
        return config


# ============================================================================
# КОНВЕРТАЦИЯ MARKDOWN → TELEGRAPH
# ============================================================================

def markdown_to_telegraph_nodes(markdown_text: str) -> List[Dict[str, Any]]:
    """
    Конвертировать Markdown в формат Telegra.ph (Array of Node).
    
    Поддерживает:
    - Заголовки ##, ###
    - Жирный **текст**
    - Курсив _текст_
    - Код `текст` и блоки ```
    - Списки ·, -
    - Ссылки [текст](url)
    - Таблицы |col|col|
    - Цитаты >
    """
    import re
    
    content = []
    lines = markdown_text.split('\n')
    
    current_paragraph = []
    current_list = []
    in_list = False
    in_code_block = False
    code_block_content = []
    
    for line in lines:
        # Пропускаем пустые строки в начале
        if not line.strip() and not current_paragraph and not current_list:
            continue
        
        # Блоки кода
        if line.strip().startswith('```'):
            if in_code_block:
                # Заканчиваем блок кода
                for code_line in code_block_content:
                    content.append({
                        "tag": "pre",
                        "children": [code_line]
                    })
                code_block_content = []
                in_code_block = False
            else:
                # Начинаем блок кода
                in_code_block = True
            continue
        
        if in_code_block:
            code_block_content.append(line)
            continue
        
        # Пустая строка - закрываем параграф и список
        if not line.strip():
            if current_paragraph:
                content.append({
                    "tag": "p",
                    "children": [" ".join(current_paragraph)]
                })
                current_paragraph = []
            
            if in_list and current_list:
                content.append({
                    "tag": "ul",
                    "children": current_list
                })
                current_list = []
                in_list = False
            continue
        
        # Таблицы
        if line.strip().startswith('|') and '|' in line.strip()[1:]:
            if current_paragraph:
                content.append({"tag": "p", "children": [" ".join(current_paragraph)]})
                current_paragraph = []
            
            table_rows = []
            header_row = None
            i = lines.index(line)
            while i < len(lines) and lines[i].strip().startswith('|'):
                row_line = lines[i].strip()
                if re.match(r'\|[\s\-:|]+\|', row_line):
                    i += 1
                    continue
                cells = [cell.strip() for cell in row_line.split('|')[1:-1]]
                if cells:
                    if header_row is None:
                        header_row = cells
                    else:
                        table_rows.append(cells)
                i += 1
            
            if header_row:
                content.append({
                    "tag": "p",
                    "children": [{"tag": "b", "children": [" | ".join(header_row)]}]
                })
            for row in table_rows:
                content.append({"tag": "p", "children": [" | ".join(row)]})
            continue
        
        # Заголовки
        if line.strip().startswith('### ') or line.strip().startswith('## '):
            if current_paragraph:
                content.append({"tag": "p", "children": [" ".join(current_paragraph)]})
                current_paragraph = []
            if in_list and current_list:
                content.append({"tag": "ul", "children": current_list})
                current_list = []
                in_list = False
            
            content.append({
                "tag": "h3",
                "children": [line.strip()[4:] if line.strip().startswith('### ') else line.strip()[3:]]
            })
            continue
        
        # Списки
        if line.strip().startswith('· ') or line.strip().startswith('- '):
            in_list = True
            # Обрабатываем inline-форматирование внутри элемента списка!
            list_text = line.strip()[2:]
            list_parts = process_inline_formatting(list_text)
            current_list.append({
                "tag": "li",
                "children": list_parts
            })
            continue
        
        # Цитаты
        if line.strip().startswith('> '):
            if current_paragraph:
                content.append({"tag": "p", "children": [" ".join(current_paragraph)]})
                current_paragraph = []
            content.append({
                "tag": "blockquote",
                "children": [line.strip()[2:]]
            })
            continue
        
        # Обычный текст с inline-форматированием
        parts = process_inline_formatting(line.strip())
        has_nodes = any(isinstance(p, dict) for p in parts)
        
        if has_nodes:
            content.append({"tag": "p", "children": parts})
        else:
            current_paragraph.append("".join(parts))
    
    # Добавляем оставшиеся элементы
    if current_paragraph:
        content.append({"tag": "p", "children": [" ".join(current_paragraph)]})
    
    if in_list and current_list:
        content.append({"tag": "ul", "children": current_list})
    
    return content


def process_inline_formatting(text: str) -> List:
    """Обработать inline-форматирование (жирный, курсив, код, ссылки)."""
    import re
    
    def process_bold(txt: str) -> List:
        """Обработать жирный **текст**."""
        parts = []
        last_end = 0
        for match in re.finditer(r'\*\*(.+?)\*\*', txt):
            if match.start() > last_end:
                parts.append(txt[last_end:match.start()])
            parts.append({"tag": "b", "children": [match.group(1)]})
            last_end = match.end()
        if last_end < len(txt):
            parts.append(txt[last_end:])
        return parts if parts else [txt]
    
    def process_italic(txt: str) -> List:
        """Обработать курсив _текст_."""
        parts = []
        last_end = 0
        for match in re.finditer(r'_(.+?)_', txt):
            if match.start() > last_end:
                parts.append(txt[last_end:match.start()])
            parts.append({"tag": "i", "children": [match.group(1)]})
            last_end = match.end()
        if last_end < len(txt):
            parts.append(txt[last_end:])
        return parts if parts else [txt]
    
    def process_code(txt: str) -> List:
        """Обработать код `текст`."""
        parts = []
        last_end = 0
        for match in re.finditer(r'`(.+?)`', txt):
            if match.start() > last_end:
                parts.append(txt[last_end:match.start()])
            parts.append({"tag": "code", "children": [match.group(1)]})
            last_end = match.end()
        if last_end < len(txt):
            parts.append(txt[last_end:])
        return parts if parts else [txt]
    
    def process_links(txt: str) -> List:
        """Обработать ссылки [текст](url)."""
        parts = []
        last_end = 0
        for match in re.finditer(r'\[(.+?)\]\((.+?)\)', txt):
            if match.start() > last_end:
                parts.append(txt[last_end:match.start()])
            parts.append({
                "tag": "a",
                "attrs": {"href": match.group(2)},
                "children": [match.group(1)]
            })
            last_end = match.end()
        if last_end < len(txt):
            parts.append(txt[last_end:])
        return parts if parts else [txt]
    
    # Начинаем с текста
    parts = [text]

    # Обрабатываем жирный (может быть несколько раз)
    new_parts = []
    for part in parts:
        if isinstance(part, dict):
            new_parts.append(part)
        else:
            if '**' in part:
                new_parts.extend(process_bold(part))
            else:
                new_parts.append(part)
    parts = new_parts

    # Обрабатываем ссылки — ОБРАБАТЫВАЕМ ДО КУРСИВА!
    # Это критично: если обрабатывать курсив до ссылок, то символы '_'
    # внутри URL (напр., the_end_of_kubernetes) будут приняты за курсив,
    # что сломает структуру ссылки.
    new_parts = []
    for part in parts:
        if isinstance(part, dict):
            if 'children' in part:
                new_children = []
                for child in part['children']:
                    if isinstance(child, str) and '[' in child and '](' in child:
                        new_children.extend(process_links(child))
                    else:
                        new_children.append(child)
                part['children'] = new_children
            new_parts.append(part)
        else:
            if '[' in part and '](' in part:
                new_parts.extend(process_links(part))
            else:
                new_parts.append(part)
    parts = new_parts

    # Обрабатываем курсив — после ссылок, чтобы '_' внутри URL не триггерили курсив
    new_parts = []
    for part in parts:
        if isinstance(part, dict):
            # Рекурсивно обрабатываем children
            if 'children' in part:
                new_children = []
                for child in part['children']:
                    if isinstance(child, str) and '_' in child:
                        new_children.extend(process_italic(child))
                    else:
                        new_children.append(child)
                part['children'] = new_children
            new_parts.append(part)
        else:
            if '_' in part:
                new_parts.extend(process_italic(part))
            else:
                new_parts.append(part)
    parts = new_parts

    # Обрабатываем код
    new_parts = []
    for part in parts:
        if isinstance(part, dict):
            if 'children' in part:
                new_children = []
                for child in part['children']:
                    if isinstance(child, str) and '`' in child:
                        new_children.extend(process_code(child))
                    else:
                        new_children.append(child)
                part['children'] = new_children
            new_parts.append(part)
        else:
            if '`' in part:
                new_parts.extend(process_code(part))
            else:
                new_parts.append(part)
    parts = new_parts

    return parts


# ============================================================================
# ПУБЛИКАЦИЯ НА TELEGRAPH.PH
# ============================================================================

def publish_to_telegraph(title: str, content: str, author_name: str, author_url: str) -> Dict[str, Any]:
    """
    Опубликовать статью на Telegra.ph.
    
    Args:
        title: Заголовок статьи
        content: Содержимое в Markdown
        author_name: Имя автора
        author_url: URL профиля
    
    Returns:
        Результат: {"success": True, "url": "...", "path": "..."}
    """
    access_token = load_telegraph_config().get("access_token")
    
    # Конвертируем Markdown в узлы
    content_nodes = markdown_to_telegraph_nodes(content)
    
    url = "https://api.telegra.ph/createPage"
    data = {
        "access_token": access_token,
        "title": title,
        "content": json.dumps(content_nodes),
        "author_name": author_name,
        "author_url": author_url,
        "return_content": False
    }
    
    try:
        response = requests.post(url, json=data, timeout=30)
        result = response.json()
        
        if result.get("ok"):
            return {
                "success": True,
                "url": result["result"]["url"],
                "path": result["result"]["path"],
                "views": result["result"].get("views", 0)
            }
        else:
            return {
                "success": False,
                "error": result.get("error", "Неизвестная ошибка")
            }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# ============================================================================
# ПУБЛИКАЦИЯ В TELEGRAM
# ============================================================================

def escape_markdown_v2(text: str) -> str:
    """Экранировать специальные символы для Telegram MarkdownV2."""
    text = text.replace('\\', '\\\\')
    for char in '_*[]()~`>#+-=|{}.!':
        text = text.replace(char, '\\' + char)
    return text


def format_announcement(title: str, description: str, article_url: str, hashtags: List[str], emoji: str) -> str:
    """
    Сформатировать анонс для Telegram в HTML формате.

    Формат:
    - Заголовок-ссылка (жирный)
    - Краткое описание (без обрезки)
    - Хэштеги

    Telegram автоматически создаст превью статьи под сообщением.
    """
    # HTML не требует экранирования большинства символов
    # Экранируем только < и > для безопасности
    safe_title = title.replace('<', '&lt;').replace('>', '&gt;')
    safe_description = description.replace('<', '&lt;').replace('>', '&gt;')

    # Формируем пост в HTML формате
    lines = [
        f"{emoji} <b><a href=\"{article_url}\">{safe_title}</a></b>",
        "",
        safe_description,
        ""
    ]

    # Добавляем хэштеги (без экранирования)
    if hashtags:
        hashtag_line = " ".join([f"#{tag}" for tag in hashtags])
        lines.append(hashtag_line)

    return "\n".join(lines)


def publish_to_telegram(text: str) -> Dict[str, Any]:
    """
    Опубликовать сообщение в Telegram канал.

    Args:
        text: Текст сообщения (HTML)

    Returns:
        Результат: {"success": True, "message_id": 123}
    """
    config = load_telegram_config()
    token = config["token"]
    channel_id = config["channel_id"]

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        "chat_id": channel_id,
        "text": text,
        "parse_mode": "HTML",
        "link_preview_options": {
            "is_enabled": True,
            "prefer_small_media": False,
            "prefer_large_media": True
        }
    }

    try:
        response = requests.post(url, json=data, timeout=30)
        result = response.json()

        if result.get("ok"):
            return {
                "success": True,
                "message_id": result["result"]["message_id"],
                "date": result["result"].get("date")
            }
        else:
            return {
                "success": False,
                "error": result.get("description", "Неизвестная ошибка")
            }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# ============================================================================
# ЗАПИСЬ В ИСТОРИЮ
# ============================================================================

def write_to_history(title: str, telegraph_url: str, telegram_message_id: int, hashtags: List[str], sources: List[str]):
    """Записать публикацию в историю с использованием HistoryManager."""
    category = hashtags[0] if hashtags else "general"
    
    # Используем HistoryManager для добавления поста в месячный файл
    monthly_file = history_manager.add_post(
        title=title,
        category=category,
        hashtags=hashtags,
        sources=sources,
        telegraph_url=telegraph_url,
        telegram_message_id=str(telegram_message_id)
    )
    
    # Добавляем тему в topics_covered.md
    history_manager.add_topic(title, category)


# ============================================================================

# ==============================================
# GIT PUSH НА GITHUB
# ==============================================

def git_push_to_github(title="auto"):
    """Add changes to git and push to GitHub."""
    repo_dir = Path(__file__).parent
    
    try:
        # Generate articles.json before commit
        generate_script = repo_dir / "generate_json.py"
        if generate_script.exists():
            print("\n[INFO] Generating articles.json...")
            subprocess.run(
                ["python3", str(generate_script)],
                cwd=str(repo_dir),
                capture_output=True, text=True, timeout=60
            )
            print("[OK] articles.json updated")
        
        # git add
        subprocess.run(
            ["git", "add", "06_history/", "articles.json"],
            cwd=str(repo_dir),
            capture_output=True, text=True, timeout=30
        )
        
        # git commit
        result = subprocess.run(
            ["git", "commit", "-m", f"feat: new article - {title}"],
            cwd=str(repo_dir),
            capture_output=True, text=True, timeout=30
        )
        
        if "nothing to commit" in result.stdout.lower() or "nothing to commit" in result.stderr.lower():
            print("[SKIP] No changes to commit")
            return True
        
        if result.returncode != 0:
            print(f"[WARN] Commit error: {result.stderr.strip()}")
            return False
        
        print("[OK] Commit created")
        
        # git push
        print("\n[INFO] Pushing to GitHub...")
        result = subprocess.run(
            ["git", "push", "origin", "gh-pages"],
            cwd=str(repo_dir),
            capture_output=True, text=True, timeout=120
        )
        
        if result.returncode == 0:
            print("[OK] Pushed to GitHub!")
            return True
        else:
            print(f"[ERROR] Push error: {result.stderr.strip()}")
            return False
            
    except Exception as e:
        print(f"[ERROR] Git error: {e}")
        return False


# ГЛАВНАЯ ФУНКЦИЯ
# ============================================================================

def main():
    """Основная функция."""
    parser = argparse.ArgumentParser(
        description="Публикация статей на Telegra.ph с анонсом в Telegram",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры:

  # Через аргументы:
  python3 publisher_final.py \\
    --title "10 ситуаций, где ИИ уже работает" \\
    --description "Практическое руководство по применению нейросетей" \\
    --content "@article.md" \\
    --hashtags "ai,технологии,практика,нейросети" \\
    --sources "MIT Technology Review,Stanford HAI"

  # Через JSON:
  python3 publisher_final.py --input article_data.json

Формат JSON:
{
  "title": "Заголовок",
  "description": "Краткое описание",
  "content": "Текст статьи в Markdown",
  "hashtags": ["ai", "технологии"],
  "sources": ["Источник 1", "Источник 2"],
  "author_name": "AI Journalist",
  "author_url": "https://t.me/JeBanceOnline"
}
        """
    )
    
    parser.add_argument("--title", type=str, help="Заголовок статьи")
    parser.add_argument("--description", type=str, help="Краткое описание (1-2 предложения)")
    parser.add_argument("--content", type=str, help="Содержимое статьи (Markdown) или @file.md")
    parser.add_argument("--hashtags", type=str, help="Хэштеги через запятую")
    parser.add_argument("--sources", type=str, help="Источники через запятую")
    parser.add_argument("--author-name", type=str, default="AI Journalist", help="Имя автора")
    parser.add_argument("--author-url", type=str, default="https://t.me/JeBanceOnline", help="URL автора")
    parser.add_argument("--input", type=str, help="JSON файл с данными")
    parser.add_argument("--telegram-only", action="store_true", help="Только Telegram (без Telegra.ph)")
    parser.add_argument("--telegraph-only", action="store_true", help="Только Telegra.ph (без Telegram)")
    
    args = parser.parse_args()
    
    # Загружаем данные из JSON если указано
    if args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        title = data.get("title")
        description = data.get("description", "")
        content = data.get("content", "")
        hashtags = data.get("hashtags", [])
        sources = data.get("sources", [])
        author_name = data.get("author_name", "AI Journalist")
        author_url = data.get("author_url", "https://t.me/JeBanceOnline")
    else:
        title = args.title
        description = args.description
        content = args.content
        hashtags = args.hashtags.split(",") if args.hashtags else []
        sources = args.sources.split(",") if args.sources else []
        author_name = args.author_name
        author_url = args.author_url
    
    # Проверяем обязательные параметры
    if not title:
        print("❌ Заголовок обязателен!")
        sys.exit(1)
    
    # Загружаем контент из файла если указано
    if content and content.startswith("@"):
        file_path = content[1:]
        if Path(file_path).exists():
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        else:
            print(f"❌ Файл не найден: {file_path}")
            sys.exit(1)
    
    if not content and not args.telegram_only:
        print("❌ Содержимое статьи обязательно!")
        sys.exit(1)

    # ============================================
    # УДАЛЯЕМ ХЭШТЕГИ ИЗ CONTENT (если есть)
    # ============================================
    # Хэштеги должны быть только в анонсе Telegram, не в статье Telegra.ph
    if content:
        # Паттерны для поиска хэштегов в конце статьи
        hashtag_patterns = [
            r'\n---\n\n((?:#[а-яa-z0-9_]+[\s,]*)+)$',  # "---\n\n#тег1 #тег2"
            r'\n\n((?:#[а-яa-z0-9_]+[\s,]*)+)$',       # "\n\n#тег1 #тег2" в конце
            r'\n((?:#[а-яa-z0-9_]+[\s,]*)+)$',         # "\n#тег1 #тег2" в конце
        ]
        
        original_content = content
        for pattern in hashtag_patterns:
            content = re.sub(pattern, '', content, flags=re.IGNORECASE | re.MULTILINE)
        
        # Удаляем одиночные хэштеги в конце (после всех разделов)
        content = re.sub(r'\n+#[а-яa-z0-9_]+\s*$', '', content, flags=re.IGNORECASE | re.MULTILINE)
        
        # Удаляем лишние пустые строки в конце
        content = re.sub(r'\n{3,}$', '\n', content)
        
        if content != original_content:
            print("ℹ️ Хэштеги удалены из content (остались только в JSON)")
        else:
            print("✅ Хэштегов в content нет")

    # ============================================
    # ДОБАВЛЯЕМ ИСТОЧНИКИ С ССЫЛКАМИ В CONTENT
    # ============================================
    if sources and content:
        # Проверяем, есть ли уже раздел "Источники" в content
        # Учитываем разные варианты: "Источники:", "🔗 Источники", "### Источники", и т.д.
        sources_patterns = [
            r'источники:',           # "Источники:"
            r'🔗\s*источники',       # "🔗 Источники"
            r'#{1,3}\s*источники',   # "### Источники", "## Источники", "# Источники"
            r'---\n\nисточники',     # "---\n\nИсточники"
        ]
        has_sources = any(re.search(pattern, content, re.IGNORECASE) for pattern in sources_patterns)

        if not has_sources:
            # Добавляем источники с Markdown-ссылками
            sources_section = "\n\n---\n\nИсточники:\n"
            for source in sources:
                source = source.strip()
                # Преобразуем "Название (URL)" → "[Название](URL)"
                url_match = re.search(r'\((https?://[^)]+)\)$', source)
                if url_match:
                    name = source[:url_match.start()].strip()
                    url = url_match.group(1)
                    sources_section += f"• [{name}]({url})\n"
                else:
                    sources_section += f"• {source}\n"
            content += sources_section
            print("✅ Источники с ссылками добавлены в статью")
        else:
            print("ℹ️ Раздел 'Источники' уже есть в content")

    # Определяем эмодзи
    category = hashtags[0] if hashtags else "default"
    emoji = EMOJI_MAP.get(category, EMOJI_MAP.get("default"))

    print("=" * 60)
    print("📰 ПУБЛИКАЦИЯ СТАТЬИ")
    print("=" * 60)
    print(f"📝 Заголовок: {title}")
    print(f"📄 Описание: {description}")
    print(f"🏷️ Хэштеги: {', '.join(hashtags)}")
    print(f"{'🤖' if 'ai' in category.lower() else '📌'} Категория: {category}")
    print("=" * 60)

    # ============================================
    # ПРОВЕРКА НА ДУБЛИКАТЫ (КРИТИЧЕСКИ ВАЖНО!)
    # ============================================
    print()
    print("🔍 ПРОВЕРКА НА ДУБЛИКАТЫ...")

    # Добавляем путь к модулю
    sys.path.insert(0, "/root/git/AI-journalist")
    from check_duplicates import check_topic_duplicate, check_title_in_history

    # Проверка 1: Дубликат темы
    is_topic_dup, topic_reason = check_topic_duplicate(title, category)
    if is_topic_dup:
        print("🚫 ДУБЛИКАТ ТЕМЫ НАЙДЕН!")
        print(f"   Причина: {topic_reason}")
        print()
        print("Публикация ЗАБЛОКИРОВАНА!")
        print("Выберите другую тему или укажите 'обновление' в заголовке.")
        sys.exit(1)
    else:
        print(f"✅ Тема уникальна (категория: {category})")

    # Проверка 2: Дубликат заголовка в истории
    is_title_dup, title_reason = check_title_in_history(title, days=30)
    if is_title_dup:
        print("🚫 ДУБЛИКАТ ЗАГОЛОВКА В ИСТОРИИ!")
        print(f"   Причина: {title_reason}")
        print()
        print("Публикация ЗАБЛОКИРОВАНА!")
        print("Выберите другую тему.")
        sys.exit(1)
    else:
        print("✅ Заголовок не найден в истории (за 30 дней)")

    print()
    print("✅ Все проверки на дубликаты пройдены!")
    print()

    telegraph_url = None
    telegram_message_id = None
    
    # Публикуем на Telegra.ph
    if not args.telegram_only and content:
        print("\n📝 Публикация на Telegra.ph...")
        result = publish_to_telegraph(title, content, author_name, author_url)
        
        if result["success"]:
            telegraph_url = result["url"]
            print(f"✅ Опубликовано! URL: {telegraph_url}")
        else:
            print(f"❌ Ошибка: {result['error']}")
            sys.exit(1)
    
    # Публикуем в Telegram
    if not args.telegraph_only:
        print("\n📢 Публикация анонса в Telegram...")
        
        # Формируем анонс
        if telegraph_url:
            announcement = format_announcement(title, description, telegraph_url, hashtags, emoji)
        else:
            # Только Telegram (без ссылки)
            announcement = format_announcement(title, description, "https://t.me/JeBanceOnline", hashtags, emoji)
            announcement = announcement.replace("https://t.me/JeBanceOnline", "")
            announcement = announcement.replace("[]()", "")
        
        print(f"Текст анонса:\n{announcement}")
        
        result = publish_to_telegram(announcement)
        
        if result["success"]:
            telegram_message_id = result["message_id"]
            print(f"✅ Анонс опубликован! Message ID: {telegram_message_id}")
        else:
            print(f"❌ Ошибка: {result['error']}")
            sys.exit(1)
    
    # Записываем в историю
    if telegraph_url and telegram_message_id:
        print("\n📝 Запись в историю...")
        write_to_history(title, telegraph_url, telegram_message_id, hashtags, sources)
        print("✅ История обновлена!")
        
        # Push в GitHub
        print("💾 Сохранение в GitHub...")
        git_push_to_github(title)
    
    print("\n" + "=" * 60)
    print("🎉 ПУБЛИКАЦИЯ ЗАВЕРШЕНА!")
    print("=" * 60)
    if telegraph_url:
        print(f"📰 Статья: {telegraph_url}")
    if telegram_message_id:
        print(f"📢 Telegram ID: {telegram_message_id}")
    print("=" * 60)


if __name__ == "__main__":
    main()
