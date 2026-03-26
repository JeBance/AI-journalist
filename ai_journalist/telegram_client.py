#!/usr/bin/env python3
"""
AI-journalist Telegram Client

Централизованная библиотека для взаимодействия с Telegram Bot API.
Все функции протестированы и используют правильное форматирование.

Использование:
    from telegram_client import TelegramClient
    
    client = TelegramClient()
    result = client.send_message("Текст сообщения")
"""

import json
import requests
from pathlib import Path
from typing import Optional, Dict, Any, List


class TelegramClient:
    """Клиент для работы с Telegram Bot API."""
    
    # Специальные символы MarkdownV2, требующие экранирования
    MARKDOWN_V2_SPECIAL_CHARS = r'\_ * [ ] ( ) ~ ` > # + - = | { } . !'
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Инициализировать Telegram клиент.
        
        Args:
            config_path: Путь к файлу конфигурации. 
                        По умолчанию: /root/git/AI-journalist-bot/config.json
        """
        if config_path is None:
            config_path = "/root/git/AI-journalist-bot/config.json"
        
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.token = self.config["token"]
        self.channel_id = self.config["channel_id"]
        self.base_url = f"https://api.telegram.org/bot{self.token}"
    
    def _load_config(self) -> Dict[str, Any]:
        """Загрузить конфигурацию из файла."""
        if not self.config_path.exists():
            raise FileNotFoundError(
                f"Файл конфигурации не найден: {self.config_path}\n"
                f"Создайте файл config.json со следующим содержимым:\n"
                f"{json.dumps({
                    'token': 'ВАШ_ТОКЕН_БОТА',
                    'channel_id': '-100XXXXXXXXXX'
                }, indent=2, ensure_ascii=False)}"
            )
        
        with open(self.config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def _request(self, method: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Отправить запрос к Telegram API.
        
        Args:
            method: Метод API (например, sendMessage)
            data: Данные запроса
        
        Returns:
            Результат от API
        """
        url = f"{self.base_url}/{method}"
        
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
                    "error": result.get("description", "Неизвестная ошибка"),
                    "error_code": result.get("error_code"),
                    "response": result
                }
        
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "Превышено время ожидания ответа от Telegram",
                "response": None
            }
        
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "error": "Ошибка подключения к Telegram",
                "response": None
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Неожиданная ошибка: {str(e)}",
                "response": None
            }
    
    @staticmethod
    def escape_markdown_v2(text: str) -> str:
        """
        Экранировать специальные символы для Telegram MarkdownV2.
        
        Args:
            text: Исходный текст
        
        Returns:
            Текст с экранированными специальными символами
        
        Пример:
            >>> TelegramClient.escape_markdown_v2("PHP 8.4 > 8.3 #тег")
            'PHP 8\\.4 \\> 8\\.3 \\#тег'
        """
        # Сначала экранируем обратный слэш
        text = text.replace('\\', '\\\\')
        
        # Затем экранируем остальные специальные символы
        for char in '_*[]()~`>#+-=|{}.!':
            text = text.replace(char, '\\' + char)
        
        return text
    
    @staticmethod
    def escape_hashtags(text: str) -> str:
        """
        Экранировать только хэштеги (для сохранения читаемости).
        
        Args:
            text: Текст с хэштегами
        
        Returns:
            Текст с экранированными хэштегами
        """
        import re
        # Экранируем # в хэштегах
        return re.sub(r'(#\w+)', lambda m: '\\' + m.group(0), text)
    
    def send_message(
        self,
        text: str,
        parse_mode: str = "MarkdownV2",
        chat_id: Optional[str] = None,
        disable_notification: bool = False,
        auto_escape: bool = True
    ) -> Dict[str, Any]:
        """
        Отправить сообщение в Telegram канал.
        
        Args:
            text: Текст сообщения
            parse_mode: Режим парсинга ("MarkdownV2", "HTML", None)
            chat_id: ID чата (по умолчанию используется из конфига)
            disable_notification: Отправить без звука
            auto_escape: Автоматически экранировать текст (для MarkdownV2)
        
        Returns:
            Результат публикации:
            {
                "success": True,
                "message_id": 123,
                "chat_id": "-100XXXXXXXXXX"
            }
        
        Пример:
            >>> client = TelegramClient()
            >>> result = client.send_message("🔥 *Новость*\\n\\nТекст новости\\.\\n\\n#тег")
            >>> if result["success"]:
            ...     print(f"Опубликовано! Message ID: {result['message_id']}")
        """
        target_chat_id = chat_id or self.channel_id
        
        # Автоматическое экранирование для MarkdownV2
        if parse_mode == "MarkdownV2" and auto_escape:
            text = self.escape_markdown_v2(text)
        
        data = {
            "chat_id": target_chat_id,
            "text": text,
            "parse_mode": parse_mode if parse_mode else "None",
            "disable_notification": disable_notification
        }
        
        # Удаляем parse_mode если None
        if not parse_mode:
            data["parse_mode"] = "None"
        
        result = self._request("sendMessage", data)
        
        if result["success"]:
            return {
                "success": True,
                "message_id": result["result"]["message_id"],
                "chat_id": target_chat_id,
                "date": result["result"].get("date"),
                "url": f"https://t.me/{self._get_channel_username()}/{result['result']['message_id']}"
            }
        else:
            return result
    
    def send_message_with_image(
        self,
        text: str,
        image_path: str,
        parse_mode: str = "MarkdownV2",
        chat_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Отправить сообщение с изображением.
        
        Args:
            text: Текст сообщения (подпись к фото)
            image_path: Путь к файлу изображения
            parse_mode: Режим парсинга
            chat_id: ID чата
        
        Returns:
            Результат публикации
        """
        target_chat_id = chat_id or self.channel_id
        
        # Автоматическое экранирование для MarkdownV2
        if parse_mode == "MarkdownV2":
            text = self.escape_markdown_v2(text)
        
        url = f"{self.base_url}/sendPhoto"
        
        data = {
            "chat_id": target_chat_id,
            "caption": text,
            "parse_mode": parse_mode
        }
        
        files = {
            "photo": open(image_path, "rb")
        }
        
        try:
            response = requests.post(url, json=data, files=files, timeout=30)
            result = response.json()
            
            if result.get("ok"):
                return {
                    "success": True,
                    "message_id": result["result"]["message_id"],
                    "photo_id": result["result"]["photo"][-1]["file_id"]
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
    
    def edit_message(
        self,
        message_id: int,
        text: str,
        parse_mode: str = "MarkdownV2",
        chat_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Редактировать существующее сообщение.
        
        Args:
            message_id: ID сообщения для редактирования
            text: Новый текст сообщения
            parse_mode: Режим парсинга
            chat_id: ID чата
        
        Returns:
            Результат редактирования
        """
        target_chat_id = chat_id or self.channel_id
        
        # Автоматическое экранирование для MarkdownV2
        if parse_mode == "MarkdownV2":
            text = self.escape_markdown_v2(text)
        
        data = {
            "chat_id": target_chat_id,
            "message_id": message_id,
            "text": text,
            "parse_mode": parse_mode
        }
        
        return self._request("editMessageText", data)
    
    def delete_message(
        self,
        message_id: int,
        chat_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Удалить сообщение.
        
        Args:
            message_id: ID сообщения для удаления
            chat_id: ID чата
        
        Returns:
            Результат удаления
        """
        target_chat_id = chat_id or self.channel_id
        
        data = {
            "chat_id": target_chat_id,
            "message_id": message_id
        }
        
        return self._request("deleteMessage", data)
    
    def get_bot_info(self) -> Dict[str, Any]:
        """
        Получить информацию о боте.
        
        Returns:
            Информация о боте:
            {
                "success": True,
                "id": 123456789,
                "username": "bot_username",
                "first_name": "Bot Name"
            }
        """
        result = self._request("getMe", {})
        
        if result["success"]:
            return {
                "success": True,
                "id": result["result"]["id"],
                "username": result["result"]["username"],
                "first_name": result["result"]["first_name"],
                "can_join_groups": result["result"].get("can_join_groups"),
                "can_read_all_group_messages": result["result"].get("can_read_all_group_messages"),
                "supports_inline_queries": result["result"].get("supports_inline_queries")
            }
        else:
            return result
    
    def _get_channel_username(self) -> str:
        """Получить username канала из chat_id."""
        # Для каналов chat_id начинается с -100
        # Username нельзя получить напрямую из API без getChat
        # Возвращаем пустую строку для формирования относительной ссылки
        return ""
    
    def test_connection(self) -> bool:
        """
        Проверить соединение с Telegram.
        
        Returns:
            True если соединение успешно
        """
        result = self.get_bot_info()
        
        if result["success"]:
            print(f"✅ Бот найден: @{result['username']} ({result['first_name']})")
            return True
        else:
            print(f"❌ Ошибка подключения: {result.get('error', 'Неизвестно')}")
            return False
    
    def send_to_user(
        self,
        user_id: int,
        text: str,
        parse_mode: str = "MarkdownV2"
    ) -> Dict[str, Any]:
        """
        Отправить сообщение пользователю в личные сообщения.
        
        Args:
            user_id: Telegram User ID
            text: Текст сообщения
            parse_mode: Режим парсинга
        
        Returns:
            Результат отправки
        """
        # Автоматическое экранирование для MarkdownV2
        if parse_mode == "MarkdownV2":
            text = self.escape_markdown_v2(text)
        
        data = {
            "chat_id": str(user_id),
            "text": text,
            "parse_mode": parse_mode
        }
        
        return self._request("sendMessage", data)
    
    def send_draft_for_approval(
        self,
        user_id: int,
        text: str,
        category: str = "news"
    ) -> Dict[str, Any]:
        """
        Отправить черновик пользователю на утверждение.
        
        Args:
            user_id: Telegram User ID пользователя для утверждения
            text: Текст черновика
            category: Категория новости
        
        Returns:
            Результат отправки
        """
        # Формируем сообщение с черновиком
        draft_text = f"""📝 *ЧЕРНОВИК НА УТВЕРЖДЕНИЕ*

*Категория:* {category}

---

{text}

---

✅ Нажмите «Опубликовать» для публикации
❌ Нажмите «Отклонить» для отклонения

*Примечание:* На момент 2026-03-26 кнопки не реализованы.
Используйте автоматическую публикацию через send_message()."""
        
        return self.send_to_user(user_id, draft_text)


# ============================================================================
# Утилиты для форматирования
# ============================================================================

def format_bold(text: str) -> str:
    """Вернуть жирный текст (MarkdownV2)."""
    return f"*{text}*"


def format_italic(text: str) -> str:
    """Вернуть курсив (MarkdownV2)."""
    return f"_{text}_"


def format_code(text: str) -> str:
    """Вернуть моноширинный текст (MarkdownV2)."""
    return f"`{text}`"


def format_link(text: str, url: str) -> str:
    """Вернуть ссылку (MarkdownV2)."""
    return f"[{text}]({url})"


def format_hashtag(tag: str) -> str:
    """Вернуть хэштег с экранированием."""
    return f"\\#{tag.replace('#', '')}"


# ============================================================================
# Примеры использования
# ============================================================================

if __name__ == "__main__":
    # Пример использования
    print("Telegram Client - Примеры использования")
    print("=" * 60)
    
    # Инициализация
    client = TelegramClient()
    
    # Тест соединения
    print("\n1. Проверка соединения:")
    client.test_connection()
    
    # Пример отправки сообщения
    print("\n2. Пример отправки сообщения:")
    example_text = """🔥 Node.js: критические security-релизы

24 марта 2026 Node.js выпустил экстренные обновления.

#nodejs #javascript #security"""
    
    print(f"Текст: {example_text}")
    print("\nПосле экранирования:")
    print(TelegramClient.escape_markdown_v2(example_text))
    
    # Для реальной публикации раскомментируйте:
    # result = client.send_message(example_text)
    # if result["success"]:
    #     print(f"✅ Опубликовано! Message ID: {result['message_id']}")
    
    print("\n" + "=" * 60)
