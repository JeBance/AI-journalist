#!/usr/bin/env python3
"""
Backfill article content from Telegra.ph API.
Fixed pre/code block conversion to Markdown.
"""

import re
import json
import time
import subprocess
from pathlib import Path

HISTORY_DIR = Path("/root/git/AI-journalist/06_history")
ARTICLES_FILE = Path("/root/git/AI-journalist/articles.json")
DELAY = 1.0


def fetch_content(telegraph_url):
    """Fetch article content from Telegra.ph API using curl."""
    try:
        path = telegraph_url.replace("https://telegra.ph/", "")
        url = f"https://api.telegra.ph/getPage/{path}?return_content=true"
        result = subprocess.run(
            ["curl", "-s", "--connect-timeout", "10", "--max-time", "15", url],
            capture_output=True, text=True, timeout=20
        )
        if not result.stdout.strip():
            return None
        data = json.loads(result.stdout)
        if data.get("ok") and data.get("result", {}).get("content"):
            return telegraph_nodes_to_markdown(data["result"]["content"])
    except Exception as e:
        print(f"    Error: {e}")
    return None


def telegraph_nodes_to_markdown(nodes):
    """Convert Telegraph nodes array to Markdown text. Fixed pre/code handling."""
    if not isinstance(nodes, list):
        return ""

    md = []
    for node in nodes:
        tag = node.get("tag", "")
        children = node.get("children", [])

        if tag == "p":
            text = _nodes_to_text(children)
            if text.strip():
                md.append(text)
        elif tag in ("h3", "h4"):
            text = _nodes_to_text(children)
            if text.strip():
                md.append(f"## {text}")
        elif tag == "h1":
            text = _nodes_to_text(children)
            if text.strip():
                md.append(f"# {text}")
        elif tag == "ul":
            items = []
            for child in children:
                if child.get("tag") == "li":
                    text = _nodes_to_text(child.get("children", []))
                    if text.strip():
                        items.append(f"- {text}")
            if items:
                md.append("\n".join(items))
        elif tag == "ol":
            items = []
            for i, child in enumerate(children, 1):
                if child.get("tag") == "li":
                    text = _nodes_to_text(child.get("children", []))
                    if text.strip():
                        items.append(f"{i}. {text}")
            if items:
                md.append("\n".join(items))
        elif tag == "pre":
            # Telegraph pre blocks: usually pre > code > text nodes
            # Or pre with direct children that are text nodes
            code_text = _extract_code_from_pre(node)
            if code_text.strip():
                md.append(f"```\n{code_text}\n```")
        elif tag == "blockquote":
            text = _nodes_to_text(children)
            if text.strip():
                md.append(f"> {text}")
        elif tag == "figure":
            src = node.get("attrs", {}).get("src", "")
            if src:
                caption = _nodes_to_text(children)
                md.append(f"![{caption}]({src})")
        elif tag == "hr":
            md.append("---")
        elif tag == "a":
            # Standalone link (rare)
            href = node.get("attrs", {}).get("href", "")
            text = _nodes_to_text(children)
            if text and href:
                md.append(f"[{text}]({href})")

    return "\n\n".join(md)


def _extract_code_from_pre(pre_node):
    """Extract code text from a Telegraph <pre> node.
    
    Telegraph can structure pre blocks as:
    - pre > code > [text nodes]
    - pre > [text nodes]
    - pre > code > [code, text, etc.]
    """
    children = pre_node.get("children", [])
    
    # Case 1: pre > code > content
    if len(children) == 1 and children[0].get("tag") == "code":
        return _extract_plain_text(children[0])
    
    # Case 2: pre > multiple children (mixed)
    # Join all text content
    parts = []
    for child in children:
        if isinstance(child, str):
            parts.append(child)
        elif isinstance(child, dict):
            text = _extract_plain_text(child)
            if text:
                parts.append(text)
    
    result = "".join(parts)
    # Clean up: remove leading/trailing newlines but keep internal formatting
    return result


def _extract_plain_text(node):
    """Extract plain text from any Telegraph node, preserving newlines."""
    if isinstance(node, str):
        return node
    if isinstance(node, dict):
        tag = node.get("tag", "")
        children = node.get("children", [])
        
        if tag == "br":
            return "\n"
        elif tag == "code":
            # Inside pre/code, just get raw text
            return _extract_plain_text_from_children(children)
        elif tag == "a":
            href = node.get("attrs", {}).get("href", "")
            text = _extract_plain_text_from_children(children)
            return f"{text} ({href})" if href else text
        elif tag == "strong" or tag == "b":
            return _extract_plain_text_from_children(children)
        elif tag == "em" or tag == "i":
            return _extract_plain_text_from_children(children)
        else:
            return _extract_plain_text_from_children(children)
    return ""


def _extract_plain_text_from_children(children):
    """Extract plain text from children array."""
    if not children:
        return ""
    if isinstance(children, str):
        return children
    
    parts = []
    for child in children:
        parts.append(_extract_plain_text(child))
    return "".join(parts)


def _nodes_to_text(children):
    """Convert children array to formatted text (for non-pre contexts)."""
    if not children:
        return ""
    if isinstance(children, str):
        return children
    
    parts = []
    for child in children:
        if isinstance(child, str):
            parts.append(child)
        elif isinstance(child, dict):
            sub = _inline_format(child)
            if sub:
                parts.append(sub)
    return "".join(parts)


def _inline_format(child):
    """Format inline Telegraph node to Markdown."""
    tag = child.get("tag", "")
    children = child.get("children", [])
    text = _nodes_to_text(children)
    
    if tag == "strong" or tag == "b":
        return f"**{text}**"
    elif tag == "em" or tag == "i":
        return f"_{text}_"
    elif tag == "code":
        return f"`{text}`"
    elif tag == "a":
        href = child.get("attrs", {}).get("href", "")
        return f"[{text}]({href})" if text else ""
    else:
        return text


def load_monthly_files():
    """Load all monthly files into a dict: filepath -> content."""
    files = {}
    pattern = re.compile(r"published_posts_(\d{4}-\d{2})\.md")
    for f in HISTORY_DIR.iterdir():
        if pattern.match(f.name):
            with open(f, "r", encoding="utf-8") as fh:
                files[f] = fh.read()
    return files


def find_article_in_content(file_content, date_str, title):
    """Find article position in file content using fuzzy matching."""
    patterns = [
        rf"### \[{re.escape(date_str)}\] {re.escape(title)}",
        rf"### \[{re.escape(date_str)}\] .{{0,5}}{re.escape(title[15:])}",
        rf"### \[{re.escape(date_str)}\] .*{re.escape(title[-40:])}" if len(title) > 40 else None,
    ]
    patterns = [p for p in patterns if p]

    for pattern in patterns:
        match = re.search(pattern, file_content)
        if match:
            return match
    return None


def inject_content(file_content, match_pos, title, content):
    """Inject content into file content at the position after title."""
    after_title = file_content[match_pos.end():]
    sep_match = re.search(r"\n---\n", after_title)

    if sep_match:
        insert_pos = match_pos.end() + sep_match.start()
        existing = re.search(r"<!-- CONTENT_START -->.*?<!-- CONTENT_END -->",
                           file_content[match_pos.end():insert_pos], re.DOTALL)
        if existing:
            # Replace existing content
            existing_end = match_pos.end() + existing.end()
            new_content = (file_content[:match_pos.end() + existing.start()] +
                          "\n<!-- CONTENT_START -->\n" + content + "\n<!-- CONTENT_END -->" +
                          file_content[existing_end:])
            return new_content
        else:
            new_content = (file_content[:insert_pos] +
                          "\n<!-- CONTENT_START -->\n" + content + "\n<!-- CONTENT_END -->" +
                          file_content[insert_pos:])
    else:
        new_content = file_content + "\n<!-- CONTENT_START -->\n" + content + "\n<!-- CONTENT_END -->\n\n---\n"

    return new_content


def main():
    print("=" * 60)
    print("Backfilling content from Telegra.ph (v4 - fixed pre/code)")
    print("=" * 60)

    with open(ARTICLES_FILE, "r", encoding="utf-8") as f:
        articles = json.load(f)

    to_fetch = [a for a in articles if not a.get("content") and a.get("telegraph_url")]
    print(f"Articles to fetch: {len(to_fetch)}")
    print()

    monthly_files = load_monthly_files()
    print(f"Loaded {len(monthly_files)} monthly files")

    success = 0
    failed = 0

    for i, article in enumerate(to_fetch):
        title = article["title"]
        url = article["telegraph_url"]
        date = article["date"]

        print(f"[{i+1}/{len(to_fetch)}] {title[:55]}...", end=" ", flush=True)

        content = fetch_content(url)
        if content and len(content) > 20:
            article["content"] = content

            month = date[:7]
            target_file = None
            for fp in monthly_files:
                if month in fp.name:
                    target_file = fp
                    break

            if target_file and target_file in monthly_files:
                match = find_article_in_content(monthly_files[target_file], date, title)
                if match:
                    monthly_files[target_file] = inject_content(
                        monthly_files[target_file], match, title, content)
                    print(f"OK ({len(content)} chars)")
                    success += 1
                else:
                    print(f"NOT_FOUND_IN_FILE")
                    failed += 1
            else:
                print(f"NO_MONTHLY_FILE")
                failed += 1
        else:
            failed += 1
            print("FETCH_FAILED")

        if i < len(to_fetch) - 1:
            time.sleep(DELAY)

        if (i + 1) % 10 == 0:
            with open(ARTICLES_FILE, "w", encoding="utf-8") as f:
                json.dump(articles, f, indent=2, ensure_ascii=False)
            print(f"  [Saved progress: {success + failed}/{len(to_fetch)}]")

    with open(ARTICLES_FILE, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)

    for fp, content in monthly_files.items():
        with open(fp, "w", encoding="utf-8") as f:
            f.write(content)

    print(f"\n{'=' * 60}")
    print(f"Done! Success: {success}, Failed: {failed}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
