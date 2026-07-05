#!/usr/bin/env python3
"""Validate Feishu Docx block structure for paper-card pages.

Use this on JSON returned by:

    lark-cli api GET /open-apis/docx/v1/documents/<docx_token>/blocks --params '{"page_size":500}'

The Markdown exporter can render hard line breaks inside one Feishu text block as
blank-separated lines, so compact metadata cannot be reliably checked from
fetched Markdown alone.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote


def elements_text(block: dict) -> str:
    for key in (
        "text",
        "heading1",
        "heading2",
        "heading3",
        "heading4",
        "heading5",
        "heading6",
        "heading7",
        "heading8",
        "heading9",
        "bullet",
        "ordered",
    ):
        if key not in block:
            continue
        elements = block[key].get("elements") or []
        return "".join((element.get("text_run") or {}).get("content", "") for element in elements)
    return ""


def text_elements(block: dict) -> list[dict]:
    for key in (
        "text",
        "heading1",
        "heading2",
        "heading3",
        "heading4",
        "heading5",
        "heading6",
        "heading7",
        "heading8",
        "heading9",
        "bullet",
        "ordered",
    ):
        if key in block:
            return block[key].get("elements") or []
    return []


def normalize_title(value: str) -> str:
    value = value.lower()
    value = value.replace("ω", "ohm").replace("Ω", "ohm").replace("Ω", "ohm")
    value = re.sub(r"\\omega|\\Omega", "ohm", value)
    return re.sub(r"[^a-z0-9]+", " ", value).strip()


def token_count(value: str) -> int:
    return len(re.findall(r"[A-Za-z0-9]+", normalize_title(value)))


def cvf_slug_title(pdf_url: str) -> str | None:
    match = re.search(r"/papers/([^/]+?)(?:_paper)?\.pdf$", pdf_url)
    if not match:
        return None
    stem = unquote(match.group(1))
    stem = re.sub(r"_CVPR_\d{4}$", "", stem)
    parts = stem.split("_")
    if len(parts) >= 2:
        parts = parts[1:]
    title = " ".join(parts).strip()
    return title or None


def pdf_links(block: dict) -> list[str]:
    urls: list[str] = []
    for element in text_elements(block):
        text_run = element.get("text_run") or {}
        style = text_run.get("text_element_style") or {}
        link = style.get("link") or {}
        url = link.get("url") or ""
        if re.search(r"\.pdf(?:$|[?#])", url):
            urls.append(url)
    return urls


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Feishu block-level paper-card metadata compactness.")
    parser.add_argument("path", nargs="?", help="Blocks JSON file. Reads stdin if omitted or `-`.")
    args = parser.parse_args()

    if not args.path or args.path == "-":
        payload = json.loads(sys.stdin.read())
    else:
        payload = json.loads(Path(args.path).read_text(encoding="utf-8"))

    items = payload.get("data", {}).get("items") or payload.get("data", {}).get("blocks") or []
    if not items:
        result = {"cards": 0, "issues": 1, "details": [{"line": 1, "title": None, "code": "no_blocks", "message": "No Docx blocks found."}]}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1

    by_id = {block["block_id"]: block for block in items if "block_id" in block}
    root = next((block for block in items if block.get("block_type") == 1 and block.get("children")), items[0])
    children = root.get("children") or []
    paper_cards_index = -1
    for index, block_id in enumerate(children):
        block = by_id.get(block_id, {})
        if elements_text(block).strip().lower() == "paper cards":
            paper_cards_index = index
            break

    card_indices = [
        index
        for index, block_id in enumerate(children)
        if index > paper_cards_index and by_id.get(block_id, {}).get("block_type") == 6
    ]

    details: list[dict[str, object]] = []
    for index in card_indices:
        heading = by_id.get(children[index], {})
        title = elements_text(heading).strip()
        if index + 1 >= len(children):
            details.append({"title": title, "code": "metadata_missing", "message": "No block after card heading."})
            continue
        meta_block = by_id.get(children[index + 1], {})
        meta_text = elements_text(meta_block)
        lines = meta_text.split("\n")
        if meta_block.get("block_type") != 2:
            details.append({"title": title, "code": "metadata_block_type", "message": "Metadata must be one normal text block after the heading."})
            continue
        if len(lines) != 4 or any(not line.strip() for line in lines):
            details.append({"title": title, "code": "metadata_compact", "message": "Metadata block must contain exactly four non-empty hard-break lines."})
            continue
        if "｜" not in lines[0]:
            details.append({"title": title, "code": "takeaway_line", "message": "Metadata line 1 must contain `｜`."})
        if "｜" not in lines[1]:
            details.append({"title": title, "code": "venue_institution", "message": "Metadata line 2 must be `Venue｜Institution`."})
        if not re.search(r"\bPDF\b|w/o\. PDF", lines[2]):
            details.append({"title": title, "code": "pdf_slot", "message": "Metadata line 3 must contain PDF status."})
        if not ("Project" in lines[2] or "w/o. project page" in lines[2]):
            details.append({"title": title, "code": "project_slot", "message": "Metadata line 3 must contain Project status."})
        if not ("Code" in lines[2] or "w/o. verified code" in lines[2] or "w/o. code" in lines[2]):
            details.append({"title": title, "code": "code_slot", "message": "Metadata line 3 must contain Code status."})
        if not lines[3].startswith("Dataset:"):
            details.append({"title": title, "code": "dataset", "message": "Metadata line 4 must start with `Dataset:`."})
        for pdf_url in pdf_links(meta_block):
            slug_title = cvf_slug_title(pdf_url)
            if slug_title and token_count(slug_title) > token_count(title) + 2:
                details.append({"title": title, "code": "title_incomplete", "message": "Card heading appears shorter than the official CVF PDF title slug; use the complete official paper title, not only the method acronym."})
        if index + 2 < len(children):
            next_block = by_id.get(children[index + 2], {})
            next_text = elements_text(next_block)
            if next_block.get("block_type") == 2 and (
                next_text.startswith("CVPR")
                or next_text.startswith("[PDF]")
                or next_text.startswith("PDF")
                or next_text.startswith("Dataset:")
            ):
                details.append({"title": title, "code": "metadata_duplicate_block", "message": "Metadata lines 2-4 must not remain as separate blocks."})
            if next_block.get("block_type") == 27:
                image = next_block.get("image") or {}
                caption = ((image.get("caption") or {}).get("content") or "").strip()
                if not caption:
                    details.append({"title": title, "code": "image_caption_missing", "message": "Image block must carry the figure caption as native image caption."})
                if index + 3 < len(children):
                    after_image = by_id.get(children[index + 3], {})
                    after_text = elements_text(after_image).strip()
                    if after_image.get("block_type") == 2 and after_text.startswith("图 ") and "图注" in after_text:
                        details.append({"title": title, "code": "separate_caption_paragraph", "message": "Figure caption must be native image caption, not a separate paragraph after the image."})
            else:
                if not next_text.startswith("配图待补"):
                    details.append({"title": title, "code": "image_or_placeholder_missing", "message": "Card must have a native image block with caption or an explicit `配图待补` paragraph after metadata."})

    result = {"cards": len(card_indices), "issues": len(details), "details": details}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if details else 0


if __name__ == "__main__":
    raise SystemExit(main())
