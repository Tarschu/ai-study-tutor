#!/usr/bin/env python3
"""Generate a Markdown review card for a solved problem."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a study review card markdown file.")
    parser.add_argument("--title", required=True, help="Review card title")
    parser.add_argument("--course", default="", help="Course name")
    parser.add_argument("--topic", default="", help="Knowledge point or chapter")
    parser.add_argument("--source", default="", help="Problem source")
    parser.add_argument("--question", default="", help="Short problem restatement")
    parser.add_argument("--method", action="append", default=[], help="Correct method step")
    parser.add_argument("--formula", action="append", default=[], help="Key formula")
    parser.add_argument("--mistake", action="append", default=[], help="Common or personal mistake")
    parser.add_argument("--memory", default="", help="One-sentence memory hook")
    parser.add_argument("--practice", default="", help="Variant exercise")
    parser.add_argument("--hint", default="", help="Variant exercise hint")
    parser.add_argument("--answer", default="", help="Variant exercise answer")
    parser.add_argument(
        "--output",
        default=None,
        help="Output markdown path. Defaults to ./review-cards/<date>-<title>.md",
    )
    parser.add_argument(
        "--register",
        action="store_true",
        help="Register the generated card in the study progress queue.",
    )
    parser.add_argument(
        "--store",
        default=None,
        help="Progress JSON path used with --register.",
    )
    return parser.parse_args()


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^\w\u4e00-\u9fff]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "review-card"


def bullet_list(items: list[str], fallback: str = "待补充") -> str:
    clean = [item.strip() for item in items if item.strip()]
    if not clean:
        return f"- {fallback}"
    return "\n".join(f"- {item}" for item in clean)


def numbered_list(items: list[str], fallback: str = "待补充") -> str:
    clean = [item.strip() for item in items if item.strip()]
    if not clean:
        return f"1. {fallback}"
    return "\n".join(f"{index}. {item}" for index, item in enumerate(clean, start=1))


def register_progress(args: argparse.Namespace, card_path: Path) -> None:
    script = Path(__file__).resolve().parent / "study_progress.py"
    cmd = [sys.executable, str(script)]
    if args.store:
        cmd.extend(["--store", str(Path(args.store).expanduser())])
    cmd.extend(
        [
            "add",
            "--title",
            args.title,
            "--course",
            args.course or "未指定",
            "--topic",
            args.topic,
            "--card",
            str(card_path),
        ]
    )
    if args.memory:
        cmd.extend(["--note", args.memory])
    subprocess.run(cmd, check=True)


def main() -> None:
    args = parse_args()
    today = datetime.now().strftime("%Y-%m-%d")
    if args.output:
        output = Path(args.output).expanduser().resolve()
    else:
        output = Path.cwd() / "review-cards" / f"{today}-{slugify(args.title)}.md"
    output.parent.mkdir(parents=True, exist_ok=True)

    content = f"""# 复习卡片：{args.title}

## 来源

- 课程：{args.course or "待补充"}
- 章节/知识点：{args.topic or "待补充"}
- 题目来源：{args.source or "待补充"}
- 创建日期：{today}

## 题目简述

{args.question or "待补充"}

## 正确思路

{numbered_list(args.method)}

## 关键公式

{bullet_list(args.formula)}

## 易错点/我的错因

{bullet_list(args.mistake)}

## 一句话记忆

{args.memory or "待补充"}

## 变式练习

题目：{args.practice or "待补充"}

提示：{args.hint or "待补充"}

答案：{args.answer or "待补充"}
"""
    output.write_text(content, encoding="utf-8")
    print(output)
    if args.register:
        register_progress(args, output)


if __name__ == "__main__":
    main()
