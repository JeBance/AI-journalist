#!/usr/bin/env python3
"""
AI-journalist History Manager

Manages published posts archive with monthly file support.
Automatically creates files by month:
- 06_history/published_posts_2026-03.md
- 06_history/published_posts_2026-04.md
- ...

Each post entry includes full article content for offline use.

Usage:
    from history_manager import HistoryManager
    manager = HistoryManager("/root/git/AI-journalist/06_history")
    manager.add_post(title, category, hashtags, sources, content,
                     telegraph_url, telegram_id)
"""

import re
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Any


class HistoryManager:
    """History manager with monthly archive support."""

    def __init__(self, history_dir: str):
        self.history_dir = Path(history_dir)
        self.main_index_file = self.history_dir / "01_published_posts.md"
        self.topics_file = self.history_dir / "02_topics_covered.md"

    def _get_monthly_file(self, date: datetime) -> Path:
        month_str = date.strftime("%Y-%m")
        return self.history_dir / f"published_posts_{month_str}.md"

    def _get_monthly_file_pattern(self) -> str:
        return r"published_posts_(\d{4}-\d{2})\.md"

    def _create_monthly_file_header(self, month: str) -> str:
        month_name = {
            '01': 'January', '02': 'February', '03': 'March',
            '04': 'April', '05': 'May', '06': 'June',
            '07': 'July', '08': 'August', '09': 'September',
            '10': 'October', '11': 'November', '12': 'December'
        }
        year, month_num = month.split('-')
        name = month_name.get(month_num, month_num)
        return f"# Archive: {name} {year}\n\nAuto-generated file for {month}.\n\n---\n\n"

    def _create_main_index_header(self) -> str:
        return """# Published Posts Archive

## Structure

Archive split into monthly files:
- `published_posts_YYYY-MM.md` -- publications for a specific month
- This file (01_published_posts.md) -- index with links to archives

## Monthly Archives

"""

    def get_all_posts(self) -> List[Dict[str, Any]]:
        """Get all posts from all monthly files."""
        posts = []
        pattern = re.compile(self._get_monthly_file_pattern())
        for file in self.history_dir.iterdir():
            if pattern.match(file.name):
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
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
                 sources: List[str], content: str,
                 telegraph_url: str, telegram_message_id: str,
                 template: str = "telegra.ph article") -> str:
        """
        Add a new post to the corresponding monthly file.

        Args:
            title: Post title
            category: Category
            hashtags: List of hashtags
            sources: List of sources
            content: Full article content (markdown)
            telegraph_url: Telegra.ph article URL
            telegram_message_id: Telegram message ID
            template: Template name

        Returns:
            Path to the file where the post was added
        """
        today = datetime.now()
        today_str = today.strftime("%Y-%m-%d")
        month_str = today.strftime("%Y-%m")

        monthly_file = self._get_monthly_file(today)

        # Build the entry
        entry = f"### [{today_str}] {title}\n\n"
        entry += f"- **Category:** {category}\n"
        entry += f"- **Template:** {template}\n"
        entry += f"- **Key topics:** {', '.join(hashtags)}\n"
        entry += "- **Sources:**\n"
        for source in sources:
            entry += f"  - {source}\n"
        entry += f"- **Telegra.ph URL:** {telegraph_url}\n"
        entry += f"- **Telegram ID:** {telegram_message_id}\n"
        entry += "- **Status:** published\n\n"

        # Add full content as a hidden block for the website
        entry += "<!-- CONTENT_START -->\n"
        entry += content + "\n"
        entry += "<!-- CONTENT_END -->\n\n"
        entry += "---\n\n"

        # Create or append to file
        if monthly_file.exists():
            with open(monthly_file, 'r', encoding='utf-8') as f:
                file_content = f.read()

            if "## Statistics" in file_content:
                file_content = file_content.replace("## Statistics", entry + "## Statistics")
            else:
                file_content += entry
        else:
            file_content = self._create_monthly_file_header(month_str) + entry

        with open(monthly_file, 'w', encoding='utf-8') as f:
            f.write(file_content)

        self._update_main_index()
        return str(monthly_file)

    def _update_main_index(self):
        """Update main index file with links to archives."""
        pattern = re.compile(self._get_monthly_file_pattern())
        monthly_files = []

        for file in self.history_dir.iterdir():
            match = pattern.match(file.name)
            if match:
                monthly_files.append((match.group(1), file))

        monthly_files.sort(reverse=True)

        index_content = self._create_main_index_header()

        month_name = {
            '01': 'January', '02': 'February', '03': 'March',
            '04': 'April', '05': 'May', '06': 'June',
            '07': 'July', '08': 'August', '09': 'September',
            '10': 'October', '11': 'November', '12': 'December'
        }

        for month, file in monthly_files:
            with open(file, 'r', encoding='utf-8') as f:
                fc = f.read()
            post_count = fc.count("### [")
            year, month_num = month.split('-')
            name = month_name.get(month_num, month_num)
            index_content += f"### {name} {year}\n\n"
            index_content += f"- **File:** `{file.name}`\n"
            index_content += f"- **Posts:** {post_count}\n\n"

        index_content += "## Statistics\n\n"
        index_content += "| Month | File | Posts |\n"
        index_content += "|-------|------|-------|\n"
        for month, file in monthly_files:
            with open(file, 'r', encoding='utf-8') as f:
                pc = f.read().count("### [")
            year, month_num = month.split('-')
            name = month_name.get(month_num, month_num)
            index_content += f"| {name} {year} | `{file.name}` | {pc} |\n"

        index_content += "\n---\n\n"
        index_content += "## Rules\n\n"
        index_content += "1. **Posts added automatically** via `publisher_final.py`\n"
        index_content += "2. **Do not edit monthly files manually** -- use HistoryManager\n"
        index_content += "3. **Check duplicates** via `check_duplicates.py` before publishing\n"

        with open(self.main_index_file, 'w', encoding='utf-8') as f:
            f.write(index_content)

    def add_topic(self, title: str, category: str):
        """Add a topic to topics_covered.md."""
        repeat_date = datetime.now().strftime("%Y-%m-%d")
        topic_entry = f"- **Topic:** {title} | **Published:** {repeat_date} | **Repeat after:** {repeat_date}\n\n"

        if self.topics_file.exists():
            with open(self.topics_file, 'r', encoding='utf-8') as f:
                topics = f.read()
        else:
            topics = "# Unique topics\n\n"

        category_section = f"## {category}"
        if category_section in topics:
            topics = topics.replace(category_section, f"{category_section}\n{topic_entry}")
        else:
            topics += f"\n{category_section}\n{topic_entry}"

        with open(self.topics_file, 'w', encoding='utf-8') as f:
            f.write(topics)
