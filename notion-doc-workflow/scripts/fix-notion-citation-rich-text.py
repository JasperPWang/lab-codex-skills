#!/usr/bin/env python3
"""Fix Notion body-citation rich_text after Markdown write-back.

Notion's Markdown importer often absorbs the opening bracket into the link
text, so `[[7](url)]` becomes a link whose visible text is `[7` instead of
`7`. This script walks page blocks via `ntn api` and PATCHes linked segments
that match `^[\\d+` into plain `[` + linked digits.

Usage:
  python3 fix-notion-citation-rich-text.py <page-id-or-url>
  python3 fix-notion-citation-rich-text.py <page-id> --check-only

Requires `ntn` on PATH and an authenticated Notion CLI session.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


def normalize_page_id(raw: str) -> str:
    s = raw.strip()
    m = re.search(
        r"([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})",
        s,
        re.I,
    )
    if m:
        return m.group(1).lower()
    # Compact 32-hex Notion id
    m = re.search(r"([0-9a-f]{32})", s, re.I)
    if m:
        h = m.group(1).lower()
        return f"{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:]}"
    raise SystemExit(f"Cannot parse Notion page id from: {raw!r}")


def ntn_api(path: str, method: str | None = None, data: dict | None = None) -> dict:
    cmd = ["ntn", "api", path]
    if method:
        cmd += ["-X", method]
    if data is not None:
        tmp = Path("/tmp/ntn_cite_fix_body.json")
        tmp.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        cmd += ["-d", f"@{tmp}"]
    # Never inherit caller stdin — ntn may try to parse it as JSON.
    r = subprocess.run(cmd, capture_output=True, text=True, stdin=subprocess.DEVNULL)
    if r.returncode != 0:
        raise RuntimeError((r.stderr or r.stdout or "ntn api failed").strip())
    return json.loads(r.stdout) if r.stdout.strip() else {}


def list_blocks(page_id: str) -> list[dict[str, Any]]:
    blocks: list[dict[str, Any]] = []
    cursor: str | None = None
    while True:
        path = f"v1/blocks/{page_id}/children?page_size=100"
        if cursor:
            path += f"&start_cursor={cursor}"
        d = ntn_api(path)
        blocks.extend(d.get("results") or [])
        if not d.get("has_more"):
            break
        cursor = d.get("next_cursor")
        time.sleep(0.12)
    return blocks


def default_annotations() -> dict[str, Any]:
    return {
        "bold": False,
        "italic": False,
        "strikethrough": False,
        "underline": False,
        "code": False,
        "color": "default",
    }


def is_bad_cite_link(item: dict[str, Any]) -> re.Match[str] | None:
    """Match link text like `[7` or mangled `[[[[9` (one or more opening brackets)."""
    pt = item.get("plain_text") or ""
    link = (item.get("text") or {}).get("link")
    if not link:
        return None
    return re.fullmatch(r"\[+(\d+)", pt)


MAX_TEXT = 2000
MAX_URL = 2000


def sanitize_cite_url(url: str) -> str | None:
    """Notion rejects link.url longer than 2000 chars.

    Markdown corruption sometimes nests the same cite URL many times
    (`https://…pdf)](https://…` / percent-encoded). Prefer the first
    bare http(s) URL that fits the limit.
    """
    if not url:
        return None
    if len(url) <= MAX_URL and ")](" not in url and "%5D(" not in url.upper():
        return url
    # First absolute URL up to a nested-markdown boundary
    m = re.search(r"https?://[^\s\]\)%]+", url)
    if not m:
        m = re.search(r"https?://\S+?", url)
    if not m:
        return None
    candidate = m.group(0)
    # Trim trailing junk from nested markdown / encoding
    candidate = re.split(r"\)\]\(|%5D\(|%29%5D", candidate, maxsplit=1, flags=re.I)[0]
    candidate = candidate.rstrip(")]'\"")
    if 0 < len(candidate) <= MAX_URL:
        return candidate
    return None


def chunk_text_items(
    content: str, link: dict | None, ann: dict[str, Any]
) -> list[dict[str, Any]]:
    """Notion limits each rich_text text.content to 2000 chars."""
    safe_link = link
    if link and link.get("url") and len(link["url"]) > MAX_URL:
        cleaned = sanitize_cite_url(link["url"])
        safe_link = {"url": cleaned} if cleaned else None
    if not content:
        return [
            {
                "type": "text",
                "text": {"content": "", "link": safe_link},
                "annotations": ann,
            }
        ]
    items: list[dict[str, Any]] = []
    for i in range(0, len(content), MAX_TEXT):
        items.append(
            {
                "type": "text",
                "text": {"content": content[i : i + MAX_TEXT], "link": safe_link},
                "annotations": ann,
            }
        )
    return items


def fix_rich_text(rt: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], int]:
    out: list[dict[str, Any]] = []
    fixes = 0
    for x in rt:
        m = is_bad_cite_link(x)
        link = (x.get("text") or {}).get("link")
        ann = x.get("annotations") or default_annotations()
        if m and link:
            cleaned = sanitize_cite_url(link.get("url") or "")
            out.append(
                {
                    "type": "text",
                    "text": {"content": "[", "link": None},
                    "annotations": ann,
                }
            )
            out.append(
                {
                    "type": "text",
                    "text": {
                        "content": m.group(1),
                        "link": {"url": cleaned} if cleaned else None,
                    },
                    "annotations": ann,
                }
            )
            fixes += 1
            continue
        content = (x.get("text") or {}).get("content", x.get("plain_text") or "")
        out.extend(chunk_text_items(content, link, ann))
    return out, fixes

def count_bad(blocks: list[dict[str, Any]]) -> tuple[int, int]:
    bad = good = 0
    for b in blocks:
        t = b.get("type")
        rt = (b.get(t) or {}).get("rich_text")
        if not isinstance(rt, list):
            continue
        for x in rt:
            pt = x.get("plain_text") or ""
            link = (x.get("text") or {}).get("link")
            if link and re.fullmatch(r"\[\d+", pt):
                bad += 1
            if link and re.fullmatch(r"\d+", pt):
                good += 1
    return bad, good


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("page", help="Notion page id or URL")
    ap.add_argument(
        "--check-only",
        action="store_true",
        help="Only report bad citation link texts; do not PATCH",
    )
    args = ap.parse_args()
    page_id = normalize_page_id(args.page)

    blocks = list_blocks(page_id)
    bad0, good0 = count_bad(blocks)
    print(f"page={page_id}")
    print(f"before: bad_[n_links={bad0} digit_only_links={good0}")

    if args.check_only:
        return 1 if bad0 else 0

    if bad0 == 0:
        print("nothing to fix")
        return 0

    patched_blocks = 0
    total_fixes = 0
    failed_blocks = 0
    for b in blocks:
        t = b.get("type")
        node = b.get(t) or {}
        rt = node.get("rich_text")
        if not isinstance(rt, list):
            continue
        if not any(is_bad_cite_link(x) for x in rt):
            continue
        new_rt, fixes = fix_rich_text(rt)
        if not fixes:
            continue
        body: dict[str, Any] = {t: {"rich_text": new_rt}}
        if "color" in node:
            body[t]["color"] = node["color"]
        try:
            ntn_api(f"v1/blocks/{b['id']}", method="PATCH", data=body)
        except Exception as e:
            failed_blocks += 1
            print(f"FAIL {b['id']} fixes={fixes}: {e}", file=sys.stderr)
            time.sleep(0.2)
            continue
        patched_blocks += 1
        total_fixes += fixes
        print(f"patched {b['id']} fixes={fixes}")
        time.sleep(0.2)

    blocks2 = list_blocks(page_id)
    bad1, good1 = count_bad(blocks2)
    print(
        f"after: patched_blocks={patched_blocks} total_fixes={total_fixes} "
        f"failed_blocks={failed_blocks} bad_[n_links={bad1} digit_only_links={good1}"
    )
    if bad1:
        print("FAIL: residual bad citation link texts remain", file=sys.stderr)
        return 2
    print("PASS: all citation links are digit-only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
