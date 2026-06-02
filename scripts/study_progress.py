#!/usr/bin/env python3
"""Track review cards, mastery, and due dates for study sessions."""

from __future__ import annotations

import argparse
import json
import re
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any


DEFAULT_STORE = Path.home() / ".ai-study-tutor" / "progress.json"
INTERVALS = {
    "new": 1,
    "hard": 1,
    "again": 1,
    "good": 3,
    "easy": 7,
    "mastered": 21,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Manage AI Study Tutor review progress.")
    parser.add_argument("--store", default=str(DEFAULT_STORE), help="Progress JSON path")
    sub = parser.add_subparsers(dest="cmd", required=True)

    add = sub.add_parser("add", help="Add or update a review item")
    add.add_argument("--title", required=True)
    add.add_argument("--course", required=True)
    add.add_argument("--topic", default="")
    add.add_argument("--card", default="", help="Review card Markdown path")
    add.add_argument("--note", default="")
    add.add_argument("--due-in", type=int, default=1, help="Days until next review")

    review = sub.add_parser("review", help="Record a review result")
    review.add_argument("--id", required=True)
    review.add_argument(
        "--result",
        choices=["again", "hard", "good", "easy", "mastered"],
        required=True,
    )
    review.add_argument("--note", default="")

    sub.add_parser("due", help="List due items")
    sub.add_parser("list", help="List all items")
    return parser.parse_args()


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^\w\u4e00-\u9fff]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "item"


def today() -> date:
    return date.today()


def load_store(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"version": 1, "items": []}
    return json.loads(path.read_text(encoding="utf-8"))


def save_store(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def item_id(course: str, title: str) -> str:
    return f"{slugify(course)}--{slugify(title)}"


def add_item(args: argparse.Namespace, data: dict[str, Any]) -> None:
    now = datetime.now().isoformat(timespec="seconds")
    ident = item_id(args.course, args.title)
    due = today() + timedelta(days=max(args.due_in, 0))
    items = data.setdefault("items", [])
    existing = next((item for item in items if item["id"] == ident), None)
    payload = {
        "id": ident,
        "title": args.title,
        "course": args.course,
        "topic": args.topic,
        "card": str(Path(args.card).expanduser().resolve()) if args.card else "",
        "note": args.note,
        "created_at": now,
        "updated_at": now,
        "review_count": 0,
        "mastery": "new",
        "due": due.isoformat(),
        "history": [],
    }
    if existing is None:
        items.append(payload)
    else:
        existing.update({key: value for key, value in payload.items() if key != "created_at"})
    print(ident)


def review_item(args: argparse.Namespace, data: dict[str, Any]) -> None:
    items = data.setdefault("items", [])
    item = next((entry for entry in items if entry["id"] == args.id), None)
    if item is None:
        raise SystemExit(f"Unknown review item id: {args.id}")
    now = datetime.now().isoformat(timespec="seconds")
    interval = INTERVALS[args.result]
    item["review_count"] = int(item.get("review_count", 0)) + 1
    item["mastery"] = args.result
    item["updated_at"] = now
    item["due"] = (today() + timedelta(days=interval)).isoformat()
    item.setdefault("history", []).append(
        {"at": now, "result": args.result, "note": args.note, "next_due": item["due"]}
    )
    print(f"{args.id} -> due {item['due']}")


def due_items(data: dict[str, Any]) -> list[dict[str, Any]]:
    today_s = today().isoformat()
    return sorted(
        [item for item in data.get("items", []) if item.get("due", "") <= today_s],
        key=lambda item: (item.get("due", ""), item.get("course", ""), item.get("title", "")),
    )


def print_items(items: list[dict[str, Any]]) -> None:
    if not items:
        print("No items.")
        return
    for item in items:
        print(
            f"{item['id']} | {item.get('course','')} | {item.get('topic','')} | "
            f"due {item.get('due','')} | mastery {item.get('mastery','new')} | {item.get('title','')}"
        )


def main() -> None:
    args = parse_args()
    store = Path(args.store).expanduser().resolve()
    data = load_store(store)
    if args.cmd == "add":
        add_item(args, data)
        save_store(store, data)
    elif args.cmd == "review":
        review_item(args, data)
        save_store(store, data)
    elif args.cmd == "due":
        print_items(due_items(data))
    elif args.cmd == "list":
        print_items(data.get("items", []))


if __name__ == "__main__":
    main()
