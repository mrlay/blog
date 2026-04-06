#!/usr/bin/env python3
"""
自动生成博客索引页脚本
扫描 blog 目录下的所有 .md 文件，生成 index.md
"""

import os
from pathlib import Path

BLOG_DIR = Path(__file__).parent.parent / "docs" / "blog"
INDEX_FILE = BLOG_DIR / "index.md"


def get_article_title(file_path: Path) -> str:
    """从 markdown 文件中提取 H1 标题"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("# "):
                    return line[2:].strip()
        # 如果没有 H1 标题，使用文件名
        return file_path.stem
    except Exception:
        return file_path.stem


def generate_index():
    """生成博客索引页"""
    # 获取所有 markdown 文件（排除 index.md 自身）
    md_files = sorted(
        [f for f in BLOG_DIR.glob("*.md") if f.name != "index.md"],
        key=lambda x: x.stat().st_mtime,
        reverse=True
    )

    if not md_files:
        print("No blog posts found.")
        return

    # 生成内容
    lines = [
        "# 博客文章",
        "",
        "欢迎访问我的博客！",
        "",
        "## 最新文章",
        "",
    ]

    for md_file in md_files:
        title = get_article_title(md_file)
        link = md_file.stem + ".md"
        lines.append(f"- [{title}]({link})")

    # 写入文件
    content = "\n".join(lines) + "\n"
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Generated {INDEX_FILE} with {len(md_files)} articles")


if __name__ == "__main__":
    generate_index()
