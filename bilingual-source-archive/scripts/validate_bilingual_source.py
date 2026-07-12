#!/usr/bin/env python3
"""Validate bilingual source-archive Markdown drafts.

This is a structural lint only. It cannot prove that the extracted source text
is complete or that the translation is faithful.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


FORBIDDEN_LABELS = [
    r"^\s*#{1,6}\s*(Original|Translation|译文|原文)\s*$",
    r"^\s*(Original|Translation|译文|原文)\s*[:：]\s*$",
]
SUMMARY_FIRST = [
    r"^\s*#{1,6}\s*(AI总结|摘要|总结|Summary|Key Takeaways|Takeaways)\s*$",
    r"^\s*(AI总结|摘要|总结|Summary|Key Takeaways|Takeaways)\s*[:：]\s*",
]
COMMON_RESIDUE_PATTERNS = [
    r"<iframe\b",
    r"\bEW_IMG",
    r"图像：",
    r"/Users/",
    r"WorldModelVault",
]
NON_OBSIDIAN_RESIDUE_PATTERNS = [r"!\[\["]


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate bilingual source archive Markdown.")
    parser.add_argument("path", nargs="?", help="Markdown file. Reads stdin if omitted or `-`.")
    parser.add_argument(
        "--target",
        choices=("feishu", "notion", "obsidian", "markdown"),
        default="markdown",
        help="Destination platform; controls platform-specific residue checks.",
    )
    args = parser.parse_args()

    if not args.path or args.path == "-":
        text = sys.stdin.read()
        source = "<stdin>"
    else:
        source = args.path
        text = Path(args.path).read_text(encoding="utf-8")

    issues: list[dict[str, object]] = []

    def issue(code: str, message: str, line: int | None = None) -> None:
        payload: dict[str, object] = {"source": source, "code": code, "message": message}
        if line is not None:
            payload["line"] = line
        issues.append(payload)

    lines = text.splitlines()
    for idx, line in enumerate(lines, start=1):
        for pattern in FORBIDDEN_LABELS:
            if re.search(pattern, line, flags=re.I):
                issue("forbidden_label", "Do not use repeated `Original` / `译文` field labels.", idx)
        residue_patterns = list(COMMON_RESIDUE_PATTERNS)
        if args.target in {"feishu", "notion"}:
            residue_patterns.extend(NON_OBSIDIAN_RESIDUE_PATTERNS)
        for pattern in residue_patterns:
            if re.search(pattern, line, flags=re.I):
                issue("source_residue", f"Reader-facing text contains residue matching `{pattern}`.", idx)
        if idx <= 25:
            for pattern in SUMMARY_FIRST:
                if re.search(pattern, line, flags=re.I):
                    issue("summary_first", "Source archive should not start with an AI summary/takeaway section.", idx)

    has_frontmatter = lines[:1] == ["---"] or (
        len(lines) > 2 and lines[0] == "---" and "---" in lines[1:10]
    )
    if has_frontmatter and args.target in {"feishu", "notion"}:
        issue(
            "frontmatter_residue",
            f"Remove Obsidian/YAML frontmatter from the {args.target}-facing draft.",
            1,
        )

    cjk_chars = len(re.findall(r"[\u4e00-\u9fff]", text))
    english_words = len(re.findall(r"\b[A-Za-z][A-Za-z'-]{2,}\b", text))
    if cjk_chars < 30:
        issue("missing_chinese", "Draft appears to lack a substantial Chinese translation.")
    if english_words < 30:
        issue("missing_original", "Draft appears to lack substantial English/source text; verify this is not summary-only.")

    result = {"issues": len(issues), "details": issues}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
