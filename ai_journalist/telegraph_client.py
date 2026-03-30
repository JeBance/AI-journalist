#!/usr/bin/env python3
"""
AI-journalist Telegra.ph Client

Централизованная библиотека для взаимодействия с Telegra.ph API.
Все функции протестированы и используют правильное форматирование.

Использование:
    from telegraph_client import TelegraphClient
    
    client = TelegraphClient()
    result = client.create_page(
        title="Заголовок статьи",
        content="Содержимое в Markdown"
    )
"""

import json
import re
import requests
from pathlib import Path
from typing import Optional, Dict, Any, List, Union
from datetime import datetime


class TelegraphClient:
    """Клиент для работы с Telegra.ph API."""
    
    # Поддерживаемые теги Telegra.ph
    SUPPORTED_TAGS = {
        'p', 'h3', 'h4', 'b', 'strong', 'i', 'em', 'u', 's', 'strike',
        'a', 'code', 'pre', 'blockquote', 'aside', 'br', 'hr',
        'ul', 'ol', 'li', 'figure', 'figcaption', 'iframe', 'img', 'video'
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Инициализировать Telegra.ph клиент.

        Args:
            config_path: Путь к файлу конфигурации.
                        По умолчанию: telegraph_config.json в текущей директории
        """
        if config_path is None:
            config_path = Path(__file__).parent.parent / "telegraph_config.json"
        
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.access_token = self.config.get("access_token")
        self.short_name = self.config.get("short_name", "AI Journalist")
        self.author_name = self.config.get("author_name", "AI Journalist")
        self.author_url = self.config.get("author_url", "https://t.me/JeBanceOnline")
        
        if not self.access_token:
            raise ValueError(
                "Access Token не найден в конфигурации!\n"
                "Запустите: python3 get_telegraph_token.py"
            )
    
    def _load_config(self) -> Dict[str, Any]:
        """Загрузить конфигурацию из файла."""
        if not self.config_path.exists():
            # Создаём конфиг по умолчанию
            default_config = {
                "short_name": "AI Journalist",
                "author_name": "AI Journalist",
                "author_url": "https://t.me/JeBanceOnline"
            }
            
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)
            
            return default_config
        
        with open(self.config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def _request(self, method: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Отправить запрос к Telegra.ph API.
        
        Args:
            method: Метод API (createPage, editPage, и т.д.)
            data: Данные запроса
        
        Returns:
            Результат от API
        """
        url = f"https://api.telegra.ph/{method}"
        
        try:
            response = requests.post(url, json=data, timeout=30)
            result = response.json()
            
            if result.get("ok"):
                return {
                    "success": True,
                    "result": result.get("result", {}),
                    "response": result
                }
            else:
                return {
                    "success": False,
                    "error": result.get("error", "Неизвестная ошибка"),
                    "response": result
                }
        
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "Превышено время ожидания ответа от Telegra.ph",
                "response": None
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Ошибка: {str(e)}",
                "response": None
            }
    
    @staticmethod
    def markdown_to_nodes(markdown_text: str, include_title: bool = False) -> List[Dict[str, Any]]:
        """
        Конвертировать Markdown в формат Telegra.ph (Array of Node).
        
        Args:
            markdown_text: Текст в формате Markdown
            include_title: Если False — пропускаем первый заголовок и параграф
        
        Returns:
            Список узлов в формате Telegra.ph
        
        Пример:
            >>> content = "# Заголовок\\n\\nТекст статьи."
            >>> nodes = TelegraphClient.markdown_to_nodes(content)
        """
        content = []
        lines = markdown_text.split('\n')
        
        current_paragraph = []
        current_list = []
        in_list = False
        skip_first_h3 = not include_title
        skip_first_paragraph = not include_title
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Пропускаем пустые строки в начале
            if not line and not current_paragraph and not current_list:
                i += 1
                continue
            
            if not line:
                # Пустая строка - закрываем параграф и список
                if current_paragraph:
                    if not skip_first_paragraph:
                        content.append({
                            "tag": "p",
                            "children": [" ".join(current_paragraph)]
                        })
                    else:
                        skip_first_paragraph = False
                    current_paragraph = []
                
                if in_list and current_list:
                    content.append({
                        "tag": "ul",
                        "children": current_list
                    })
                    current_list = []
                    in_list = False
                i += 1
                continue
            
            # Таблицы Markdown (| col | col |)
            if line.startswith('|') and '|' in line[1:]:
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
                
                # Собираем все строки таблицы
                table_rows = []
                header_row = None
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
                
                # Конвертируем таблицу в форматированный текст
                if header_row or table_rows:
                    if header_row:
                        header_text = " | ".join(header_row)
                        content.append({
                            "tag": "p",
                            "children": [{"tag": "b", "children": [header_text]}]
                        })
                    
                    for row in table_rows:
                        row_text = " | ".join(row)
                        content.append({
                            "tag": "p",
                            "children": [row_text]
                        })
                continue
            
            # Заголовки
            if line.startswith('### '):
                if skip_first_h3:
                    skip_first_h3 = False
                    i += 1
                    continue
                
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
                
                content.append({
                    "tag": "h3",
                    "children": [line[4:]]
                })
            
            elif line.startswith('## '):
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
                
                content.append({
                    "tag": "h3",
                    "children": [line[3:]]
                })
            
            elif line.startswith('# '):
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
                
                content.append({
                    "tag": "h3",
                    "children": [line[2:]]
                })
            
            # Списки (· или -)
            elif line.startswith('· ') or line.startswith('- '):
                in_list = True
                current_list.append({
                    "tag": "li",
                    "children": [line[2:]]
                })
            
            # Код (блоки)
            elif line.startswith('```'):
                i += 1
                # Пропускаем всё до закрывающего ```
                while i < len(lines) and not lines[i].strip().startswith('```'):
                    code_line = lines[i]
                    content.append({
                        "tag": "pre",
                        "children": [code_line]
                    })
                    i += 1
            
            # Цитаты
            elif line.startswith('> '):
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
                
                content.append({
                    "tag": "blockquote",
                    "children": [line[2:]]
                })
            
            # Обычный текст
            else:
                parts = TelegraphClient._process_inline_formatting(line)
                has_nodes = any(isinstance(p, dict) for p in parts)
                
                if has_nodes:
                    content.append({
                        "tag": "p",
                        "children": parts
                    })
                else:
                    current_paragraph.append("".join(parts))
            
            i += 1
        
        # Добавляем оставшиеся элементы
        if current_paragraph and not skip_first_paragraph:
            content.append({
                "tag": "p",
                "children": [" ".join(current_paragraph)]
            })
        
        if in_list and current_list:
            content.append({
                "tag": "ul",
                "children": current_list
            })
        
        return content
    
    @staticmethod
    def _process_inline_formatting(text: str) -> List[Union[str, Dict[str, Any]]]:
        """
        Обработать inline-форматирование (жирный, курсив, код, ссылки).
        
        Args:
            text: Текст для обработки
        
        Returns:
            Список текстовых строк и узлов форматирования
        """
        parts = [text]
        
        # Жирный **текст**
        new_parts = []
        for part in parts:
            if isinstance(part, dict):
                new_parts.append(part)
            else:
                if '**' in part:
                    last_end = 0
                    for match in re.finditer(r'\*\*(.+?)\*\*', part):
                        if match.start() > last_end:
                            new_parts.append(part[last_end:match.start()])
                        new_parts.append({"tag": "b", "children": [match.group(1)]})
                        last_end = match.end()
                    if last_end < len(part):
                        new_parts.append(part[last_end:])
                else:
                    new_parts.append(part)
        parts = new_parts if new_parts else parts
        
        # Курсив _текст_
        new_parts = []
        for part in parts:
            if isinstance(part, dict):
                new_parts.append(part)
            else:
                if '_' in part:
                    last_end = 0
                    for match in re.finditer(r'_(.+?)_', part):
                        if match.start() > last_end:
                            new_parts.append(part[last_end:match.start()])
                        new_parts.append({"tag": "i", "children": [match.group(1)]})
                        last_end = match.end()
                    if last_end < len(part):
                        new_parts.append(part[last_end:])
                else:
                    new_parts.append(part)
        parts = new_parts if new_parts else parts
        
        # Код `текст`
        new_parts = []
        for part in parts:
            if isinstance(part, dict):
                new_parts.append(part)
            else:
                if '`' in part:
                    last_end = 0
                    for match in re.finditer(r'`(.+?)`', part):
                        if match.start() > last_end:
                            new_parts.append(part[last_end:match.start()])
                        new_parts.append({"tag": "code", "children": [match.group(1)]})
                        last_end = match.end()
                    if last_end < len(part):
                        new_parts.append(part[last_end:])
                else:
                    new_parts.append(part)
        parts = new_parts if new_parts else parts
        
        # Ссылки [текст](url)
        new_parts = []
        for part in parts:
            if isinstance(part, dict):
                new_parts.append(part)
            else:
                if '[' in part and '](' in part:
                    last_end = 0
                    for match in re.finditer(r'\[(.+?)\]\((.+?)\)', part):
                        if match.start() > last_end:
                            new_parts.append(part[last_end:match.start()])
                        new_parts.append({
                            "tag": "a",
                            "attrs": {"href": match.group(2)},
                            "children": [match.group(1)]
                        })
                        last_end = match.end()
                    if last_end < len(part):
                        new_parts.append(part[last_end:])
                else:
                    new_parts.append(part)
        parts = new_parts if new_parts else parts
        
        return parts
    
    def create_page(
        self,
        title: str,
        content: Union[str, List[Dict[str, Any]]],
        author_name: Optional[str] = None,
        author_url: Optional[str] = None,
        return_content: bool = False
    ) -> Dict[str, Any]:
        """
        Создать новую страницу на Telegra.ph.
        
        Args:
            title: Заголовок статьи (1-256 символов)
            content: Содержимое (Markdown строка или список узлов)
            author_name: Имя автора (0-128 символов)
            author_url: URL профиля автора (0-512 символов)
            return_content: Вернуть ли контент в ответе
        
        Returns:
            Результат создания:
            {
                "success": True,
                "url": "https://telegra.ph/Title-03-26",
                "path": "Title-03-26",
                "views": 0
            }
        
        Пример:
            >>> client = TelegraphClient()
            >>> result = client.create_page(
            ...     title="Моя статья",
            ...     content="Текст статьи в Markdown"
            ... )
            >>> print(result["url"])
        """
        # Конвертируем Markdown в узлы если нужно
        if isinstance(content, str):
            content_nodes = self.markdown_to_nodes(content, include_title=False)
        else:
            content_nodes = content
        
        data = {
            "access_token": self.access_token,
            "title": title,
            "content": json.dumps(content_nodes),
            "return_content": return_content
        }
        
        # Опциональные параметры
        if author_name:
            data["author_name"] = author_name
        else:
            data["author_name"] = self.author_name
        
        if author_url:
            data["author_url"] = author_url
        else:
            data["author_url"] = self.author_url
        
        result = self._request("createPage", data)
        
        if result["success"]:
            return {
                "success": True,
                "url": result["result"]["url"],
                "path": result["result"]["path"],
                "views": result["result"].get("views", 0),
                "can_edit": result["result"].get("can_edit", False),
                "response": result
            }
        else:
            return result
    
    def edit_page(
        self,
        path: str,
        title: str,
        content: Union[str, List[Dict[str, Any]]],
        author_name: Optional[str] = None,
        author_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Редактировать существующую страницу.
        
        Args:
            path: Путь к странице (например, "Title-03-26")
            title: Новый заголовок
            content: Новое содержимое
            author_name: Имя автора
            author_url: URL профиля
        
        Returns:
            Результат редактирования
        """
        # Конвертируем Markdown в узлы если нужно
        if isinstance(content, str):
            content_nodes = self.markdown_to_nodes(content, include_title=False)
        else:
            content_nodes = content
        
        data = {
            "access_token": self.access_token,
            "path": path,
            "title": title,
            "content": json.dumps(content_nodes),
            "return_content": False
        }
        
        if author_name:
            data["author_name"] = author_name
        else:
            data["author_name"] = self.author_name
        
        if author_url:
            data["author_url"] = author_url
        else:
            data["author_url"] = self.author_url
        
        result = self._request("editPage", data)
        
        if result["success"]:
            return {
                "success": True,
                "url": result["result"]["url"],
                "path": path,
                "views": result["result"].get("views", 0),
                "response": result
            }
        else:
            return result
    
    def get_page(
        self,
        path: str,
        return_content: bool = False
    ) -> Dict[str, Any]:
        """
        Получить страницу.
        
        Args:
            path: Путь к странице
            return_content: Вернуть ли контент
        
        Returns:
            Информация о странице
        """
        data = {
            "path": path,
            "return_content": return_content
        }
        
        result = self._request("getPage", data)
        
        if result["success"]:
            return {
                "success": True,
                "path": result["result"]["path"],
                "url": result["result"]["url"],
                "title": result["result"]["title"],
                "description": result["result"].get("description", ""),
                "author_name": result["result"].get("author_name", ""),
                "views": result["result"].get("views", 0),
                "content": result["result"].get("content", []),
                "response": result
            }
        else:
            return result
    
    def get_account_info(self) -> Dict[str, Any]:
        """
        Получить информацию об аккаунте.
        
        Returns:
            Информация об аккаунте
        """
        data = {
            "access_token": self.access_token,
            "fields": ["short_name", "author_name", "author_url", "page_count"]
        }
        
        result = self._request("getAccountInfo", data)
        
        if result["success"]:
            return {
                "success": True,
                "short_name": result["result"]["short_name"],
                "author_name": result["result"]["author_name"],
                "author_url": result["result"]["author_url"],
                "page_count": result["result"]["page_count"],
                "response": result
            }
        else:
            return result
    
    def create_announcement_post(
        self,
        article_url: str,
        title: str,
        description: str = "",
        emoji: str = "📖"
    ) -> str:
        """
        Создать пост-анонс для Telegram канала.
        
        Args:
            article_url: URL статьи на Telegra.ph
            title: Заголовок статьи
            description: Краткое описание
            emoji: Эмодзи для анонса
        
        Returns:
            Текст поста для Telegram (MarkdownV2, с экранированием)
        """
        # Экранируем URL для MarkdownV2
        escaped_url = article_url.replace('_', '\\_').replace('-', '\\-').replace('.', '\\.')
        
        post = f"""{emoji} [{title}]({escaped_url})

{description}

\\#статья \\#telegraph"""
        
        return post
    
    def publish_with_announcement(
        self,
        title: str,
        content: str,
        description: str = "",
        telegram_publish: bool = False,
        emoji: str = "📖"
    ) -> Dict[str, Any]:
        """
        Опубликовать статью на Telegra.ph и создать анонс.
        
        Args:
            title: Заголовок статьи
            content: Содержимое статьи (Markdown)
            description: Краткое описание для анонса
            telegram_publish: Опубликовать ли анонс в Telegram
            emoji: Эмодзи для анонса
        
        Returns:
            Результат публикации со ссылкой на анонс
        """
        from telegram_client import TelegramClient
        
        # Публикуем на Telegra.ph
        article_result = self.create_page(title, content)
        
        if not article_result["success"]:
            return article_result
        
        # Создаём анонс
        announcement = self.create_announcement_post(
            article_result["url"],
            title,
            description,
            emoji
        )
        
        result = {
            **article_result,
            "announcement": announcement
        }
        
        # Публикуем анонс в Telegram если нужно
        if telegram_publish:
            tg_client = TelegramClient()
            tg_result = tg_client.send_message(announcement, auto_escape=False)
            result["telegram"] = tg_result
        
        return result


# ============================================================================
# Примеры использования
# ============================================================================

if __name__ == "__main__":
    print("Telegra.ph Client - Примеры использования")
    print("=" * 60)
    
    # Пример конвертации Markdown
    example_markdown = """
## Введение

Это **жирный текст** и _курсив_, а также `код`.

## Список

· Пункт 1
· Пункт 2
· Пункт 3

[Ссылка](https://example.com)
"""
    
    print("\nПример Markdown:")
    print(example_markdown)
    
    print("\nКонвертация в узлы Telegra.ph:")
    nodes = TelegraphClient.markdown_to_nodes(example_markdown)
    print(json.dumps(nodes, indent=2, ensure_ascii=False))
    
    print("\n" + "=" * 60)
    print("\nДля реальной публикации:")
    print("client = TelegraphClient()")
    print("result = client.create_page(title='Заголовок', content='Содержимое')")
    print("print(result['url'])")
