#!/usr/bin/env python3
"""Sanitize a skill bundle copy before public GitHub publication."""

from __future__ import annotations

import re
import sys
from pathlib import Path


TEXT_SUFFIXES = {
    ".md",
    ".txt",
    ".yaml",
    ".yml",
    ".json",
    ".py",
    ".sh",
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
}

REPLACEMENTS = [
    (
        "$WORLD_MODEL_VAULT",
        "$WORLD_MODEL_VAULT",
    ),
    (
        "$WORLD_MODEL_VAULT_MINERU_BIN",
        "$WORLD_MODEL_VAULT_MINERU_BIN",
    ),
]

FEISHU_URL_RE = re.compile(
    r"https://[A-Za-z0-9-]+(?:\.feishu\.cn|\.larksuite\.com)/[^\s)`>]+"
)
DOC_TOKEN_RE = re.compile(r"(doc token\s*)`[^`]+`", re.IGNORECASE)


def is_text_file(path: Path) -> bool:
    return path.suffix in TEXT_SUFFIXES or path.name in {"README", "LICENSE", "NOTICE"}


def sanitize_text(text: str) -> str:
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    text = FEISHU_URL_RE.sub("<FEISHU_OR_LARK_URL>", text)
    text = DOC_TOKEN_RE.sub(r"\1`<DOC_TOKEN>`", text)
    return text


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: sanitize-public-export.py <bundle-root>", file=sys.stderr)
        return 2

    root = Path(argv[1])
    changed = 0
    for path in root.rglob("*"):
        if not path.is_file() or not is_text_file(path):
            continue
        try:
            old = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        new = sanitize_text(old)
        if new != old:
            path.write_text(new, encoding="utf-8")
            changed += 1

    print(f"sanitized files: {changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
