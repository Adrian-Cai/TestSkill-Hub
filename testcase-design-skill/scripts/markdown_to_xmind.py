#!/usr/bin/env python3
"""Convert markdown test case docs to .xmind (Zen JSON format)."""

from __future__ import annotations

import argparse
import json
import re
import uuid
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Tuple


HEADING_RE = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")
BULLET_RE = re.compile(r"^(\s*)[-*+]\s+(.*\S)\s*$")
NUMBER_RE = re.compile(r"^(\s*)\d+[.)]\s+(.*\S)\s*$")
TABLE_ROW_RE = re.compile(r"^\s*\|(.+)\|\s*$")


@dataclass
class Topic:
    title: str
    id: str = field(default_factory=lambda: uuid.uuid4().hex)
    children: List["Topic"] = field(default_factory=list)

    def to_dict(self) -> dict:
        data = {"id": self.id, "title": self.title}
        if self.children:
            data["children"] = {"attached": [child.to_dict() for child in self.children]}
        return data


def clean_markdown_text(value: str) -> str:
    text = value.strip()
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\[(.*?)\]\((.*?)\)", r"\1", text)
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    return text.strip()


def infer_title(lines: List[str], default_title: str) -> str:
    for line in lines:
        match = HEADING_RE.match(line)
        if match:
            title = clean_markdown_text(match.group(2))
            if title:
                return title
    return default_title


def append_topic(parent: Topic, title: str) -> Topic:
    topic = Topic(title=title)
    parent.children.append(topic)
    return topic


def parse_table_cells(row_text: str) -> List[str]:
    return [clean_markdown_text(cell) for cell in row_text.split("|")]


def is_separator_row(cells: List[str]) -> bool:
    if not cells:
        return True
    for cell in cells:
        stripped = cell.replace(":", "").replace("-", "").replace(" ", "")
        if stripped:
            return False
    return True


def build_topic_tree(lines: List[str], root_title: str) -> Topic:
    root = Topic(title=root_title)

    heading_stack: List[Tuple[int, Topic]] = [(0, root)]
    list_stack: List[Tuple[int, Topic]] = [(-1, root)]
    current_section = root

    table_header_seen = False
    in_table = False

    for raw_line in lines:
        line = raw_line.rstrip("\n")

        heading_match = HEADING_RE.match(line)
        if heading_match:
            in_table = False
            table_header_seen = False

            heading_level = len(heading_match.group(1))
            heading_text = clean_markdown_text(heading_match.group(2))
            if not heading_text:
                continue

            while heading_stack and heading_stack[-1][0] >= heading_level:
                heading_stack.pop()
            parent = heading_stack[-1][1] if heading_stack else root
            node = append_topic(parent, heading_text)
            heading_stack.append((heading_level, node))

            current_section = node
            list_stack = [(-1, node)]
            continue

        bullet_match = BULLET_RE.match(line) or NUMBER_RE.match(line)
        if bullet_match:
            in_table = False
            table_header_seen = False

            indent = len(bullet_match.group(1))
            bullet_text = clean_markdown_text(bullet_match.group(2))
            if not bullet_text:
                continue

            while list_stack and indent <= list_stack[-1][0]:
                list_stack.pop()
            parent = list_stack[-1][1] if list_stack else current_section
            node = append_topic(parent, bullet_text)
            list_stack.append((indent, node))
            continue

        table_match = TABLE_ROW_RE.match(line)
        if table_match:
            in_table = True
            cells = parse_table_cells(table_match.group(1))
            if is_separator_row(cells):
                continue

            if not table_header_seen:
                table_header_seen = True
                continue

            display_cells = [cell for cell in cells if cell]
            if not display_cells:
                continue
            title = " | ".join(display_cells[:3])
            append_topic(current_section, title)
            continue

        if in_table and not line.strip():
            in_table = False
            table_header_seen = False

    return root


def write_xmind(output_path: Path, title: str, root_topic: Topic) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    sheet_id = uuid.uuid4().hex
    content = [
        {
            "id": sheet_id,
            "class": "sheet",
            "title": title,
            "rootTopic": root_topic.to_dict(),
        }
    ]
    metadata = {
        "creator": {"name": "CatPaw"},
        "activeSheetId": sheet_id,
    }
    manifest = {
        "file-entries": {
            "content.json": {},
            "metadata.json": {},
        }
    }

    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as xmind_zip:
        xmind_zip.writestr("content.json", json.dumps(content, ensure_ascii=False, indent=2))
        xmind_zip.writestr("metadata.json", json.dumps(metadata, ensure_ascii=False, indent=2))
        xmind_zip.writestr("manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert markdown test case files to XMind format"
    )
    parser.add_argument("--input", required=True, help="Input markdown file path")
    parser.add_argument("--output", required=True, help="Output .xmind file path")
    parser.add_argument(
        "--title",
        default="",
        help="Root topic title. Defaults to first markdown heading or file name.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        raise FileNotFoundError(f"Input markdown not found: {input_path}")

    lines = input_path.read_text(encoding="utf-8").splitlines()
    title = args.title.strip() or infer_title(lines, input_path.stem)

    root_topic = build_topic_tree(lines, title)
    if not root_topic.children:
        append_topic(root_topic, "No structured content parsed from markdown")

    write_xmind(output_path, title, root_topic)
    print(f"Generated XMind file: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
