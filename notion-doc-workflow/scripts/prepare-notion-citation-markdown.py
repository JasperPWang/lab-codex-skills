#!/usr/bin/env python3
"""Escape outer citation brackets for Notion Markdown writes.

Canonical body cites are `[[n](url)]` / `[[n](url), [m](url)]`. Notion's
Markdown importer always absorbs the first opening `[` into the first link
text (`[n` linked). Escaping that outer bracket — `\\[[n](url)]` — makes the
importer store plain `[` + digit-only links on first write.

Usage:
  python3 prepare-notion-citation-markdown.py < draft.md > notion-ready.md
  python3 prepare-notion-citation-markdown.py draft.md -o notion-ready.md

Idempotent: already-escaped `\\[[n](url)]` is left unchanged.
Does not change Feishu/Obsidian drafts; apply only immediately before a
Notion Markdown write (`ntn pages create|edit`, MCP markdown update, etc.).
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Match an unescaped outer [[ before a numeric cite link.
# Negative lookbehind skips already-escaped \[[n](...
_CITE_OUTER = re.compile(r"(?<!\\)\[(\[\d+\]\()")


def prepare_notion_citation_markdown(text: str) -> str:
    """Turn `[[n](url)]` clusters into Notion-safe `\\[[n](url)]`."""
    return _CITE_OUTER.sub(r"\\[\1", text)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "input",
        nargs="?",
        help="Input Markdown path (default: stdin)",
    )
    ap.add_argument(
        "-o",
        "--output",
        help="Output path (default: stdout)",
    )
    args = ap.parse_args()

    if args.input:
        src = Path(args.input).read_text(encoding="utf-8")
    else:
        src = sys.stdin.read()

    out = prepare_notion_citation_markdown(src)

    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
    else:
        sys.stdout.write(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
