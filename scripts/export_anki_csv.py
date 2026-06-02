#!/usr/bin/env python3
"""Export AI Study Tutor review cards to an Anki-importable CSV."""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Any


DEFAULT_STORE = Path.home() / ".ai-study-tutor" / "progress.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export review items as Anki CSV.")
    parser.add_argument("--store", default=str(DEFAULT_STORE), help="Progress JSON path")
    parser.add_argument("--output", required=True, help="Output CSV path")
    parser.add_argument("--course", default="", help="Optional course filter")
    return parser.parse_args()


def read_card(path: str) -> str:
    if not path:
        return ""
    card_path = Path(path).expanduser()
    if not card_path.is_file():
        return ""
    return card_path.read_text(encoding="utf-8", errors="replace")


def section(text: str, title: str) -> str:
    pattern = re.compile(rf"^##\s+{re.escape(title)}\s*$([\s\S]*?)(?=^##\s+|\Z)", re.M)
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def build_front_back(item: dict[str, Any]) -> tuple[str, str]:
    card_text = read_card(item.get("card", ""))
    question = section(card_text, "题目简述") or item.get("title", "")
    method = section(card_text, "正确思路")
    formulas = section(card_text, "关键公式")
    mistakes = section(card_text, "易错点/我的错因") or section(card_text, "易错点")
    memory = section(card_text, "一句话记忆")
    front = f"{item.get('course','')}｜{item.get('topic','')}\n\n{question}".strip()
    back_parts = [
        ("正确思路", method),
        ("关键公式", formulas),
        ("易错点", mistakes),
        ("一句话记忆", memory),
    ]
    back = "\n\n".join(f"【{name}】\n{value}" for name, value in back_parts if value)
    return front, back or item.get("note", "") or item.get("title", "")


def main() -> None:
    args = parse_args()
    store = Path(args.store).expanduser().resolve()
    if not store.is_file():
        raise SystemExit(f"Progress store does not exist: {store}")
    data = json.loads(store.read_text(encoding="utf-8"))
    output = Path(args.output).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for item in data.get("items", []):
        if args.course and item.get("course") != args.course:
            continue
        front, back = build_front_back(item)
        tags = " ".join(
            part for part in [item.get("course", ""), item.get("topic", ""), item.get("mastery", "")]
            if part
        ).replace(" ", "_")
        rows.append([front, back, tags])
    with output.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["Front", "Back", "Tags"])
        writer.writerows(rows)
    print(output)


if __name__ == "__main__":
    main()
