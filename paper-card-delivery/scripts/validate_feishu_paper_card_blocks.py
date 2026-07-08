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


REQUIRED_BULLETS = ["定义", "问题", "方法", "实现", "结论", "局限", "启发"]
SIMULATION_HINTS_RE = re.compile(
    r"\b("
    r"mujoco|isaac(?:\s+gym|\s+sim)?|pybullet|bullet|gazebo|habitat|ai2-thor|"
    r"carla|sapien|airsim|unity|unreal|blender|omniverse|"
    r"clo3d|marvelous\s+designer"
    r")\b",
    re.I,
)
BASE_MODEL_HINTS_RE = re.compile(
    r"\b("
    r"flux(?:\.1)?(?:-[a-z0-9.]+)?|hunyuan(?:video)?|stable\s+diffusion|stable\s+video\s+diffusion|"
    r"sdxl|sd3|wan\d(?:\.\d)?|cogvideo(?:x)?|pixart(?:-[a-z0-9.]+)?|kandinsky|kolors|"
    r"animatediff|modelscope\s+t2v|zeroscope|open-?sora|videocrafter|qwen(?:-image|-vl)?"
    r")\b",
    re.I,
)
STATUS_VALUES = {"未报告", "不适用", "not reported", "n/a", "na", "none"}
FORBIDDEN_PLACEHOLDERS = (
    "配图待补",
    "图注待补",
    "图片待补",
    "图像待补",
    "待补配图",
    "待补图片",
    "待补图像",
    "待补图注",
    "figure todo",
    "image todo",
    "caption todo",
    "figure tbd",
    "image tbd",
    "caption tbd",
    "figure pending",
    "image pending",
    "caption pending",
)
DRAFT_STATUS_PATTERNS = (
    (re.compile(r"待核验"), "Formal paper-card delivery must not contain `待核验`; verify against the official source and resolve it. If the original source cannot be obtained after all official acquisition/extraction routes fail, report a blocker instead of shipping a card."),
    (re.compile(r"\bcandidate\s*/", re.I), "Formal paper-card delivery must not contain candidate-status markers."),
    (re.compile(r"\b(?:todo|tbd|pending)\b", re.I), "Formal paper-card delivery must not contain TODO/TBD/pending verification markers."),
    (re.compile(r"(?:核验|验证)\s*(?:TODO|TBD|pending|待办)", re.I), "Formal paper-card delivery must not contain unresolved verification TODOs."),
)


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


def dataset_entries(dataset_line: str) -> list[str]:
    value = re.sub(r"^Dataset:\s*", "", dataset_line, flags=re.I)
    dataset_part = re.split(r"\s*\|\s*(?:Base|Simulation)\s*[:：]", value, maxsplit=1, flags=re.I)[0]
    dataset_part = dataset_part.strip()
    if not dataset_part or dataset_part.lower() in STATUS_VALUES:
        return []
    parts = re.split(r"\s*(?:,|，|、|;|；|\s/\s)\s*", dataset_part)
    return [part.strip() for part in parts if part.strip()]


def metadata_component(dataset_line: str, name: str) -> str | None:
    match = re.search(rf"\|\s*{re.escape(name)}\s*[:：]\s*([^|]+)", dataset_line, flags=re.I)
    return match.group(1).strip() if match else None


def comma_entries(value: str) -> list[str]:
    if not value or value.lower() in STATUS_VALUES:
        return []
    return [part.strip() for part in re.split(r"\s*,\s*", value) if part.strip()]


def check_dataset_line(dataset_line: str, card_text: str, details: list[dict[str, object]], title: str) -> None:
    def add(code: str, message: str) -> None:
        details.append({"title": title, "code": code, "message": message})

    if re.search(r"\bbase(?:\s+model)?\s*[:：]", dataset_line, flags=re.I) and not re.search(r"\|\s*Base\s*[:：]", dataset_line, flags=re.I):
        add("base_format", "Base-model metadata must be appended on the Dataset line as `| Base:`, not as a loose `Base:` field.")
    if re.search(r"simluation\s*[:：]", dataset_line, flags=re.I):
        add("simulation_spelling", "Use `Simulation:` in the Dataset metadata line, not `Simluation:`.")
    if re.search(r"simulation\s*[:：]", dataset_line, flags=re.I) and not re.search(r"\|\s*Simulation\s*[:：]", dataset_line):
        add("simulation_format", "Simulation metadata must be appended as `| Simulation:` on the Dataset line.")
    entries = dataset_entries(dataset_line)
    dataset_value = re.sub(r"^Dataset:\s*", "", dataset_line, flags=re.I)
    dataset_part = re.split(r"\s*\|\s*(?:Base|Simulation)\s*[:：]", dataset_value, maxsplit=1, flags=re.I)[0].strip()
    if dataset_part.lower() not in STATUS_VALUES and re.search(r"｜|、|，|;|；|\s/\s", dataset_part):
        add("dataset_separator", "Separate Dataset metadata names with ASCII comma plus space, e.g. `Dataset: H3.6M, 3DPW, SURREAL`; put extra datasets in `实现`.")
    if len(entries) > 3:
        add("dataset_too_many", "Dataset metadata must list at most three visible dataset names; put additional datasets in `实现` if needed.")
    base_value = metadata_component(dataset_line, "Base")
    if base_value is not None:
        if base_value.lower() not in STATUS_VALUES and re.search(r"｜|、|，|;|；|\s/\s", base_value):
            add("base_separator", "Separate Base metadata names with ASCII comma plus space, e.g. `| Base: FLUX.1-dev, HunyuanVideo`; put extra base-model details in `实现`.")
        if len(comma_entries(base_value)) > 3:
            add("base_too_many", "Base metadata must list at most three visible base model names; put additional base-model chains or variants in `实现`.")
    if BASE_MODEL_HINTS_RE.search(card_text) and not re.search(r"\|\s*Base\s*[:：]", dataset_line):
        add("base_model_missing", "Card mentions a known open-source/pretrained base model; Dataset metadata should include `| Base:` or explicitly mark `Base: 未报告` when the base is involved but not reported.")
    if SIMULATION_HINTS_RE.search(card_text) and not re.search(r"\|\s*Simulation\s*[:：]", dataset_line):
        add("simulation_missing", "Card mentions a known simulator/environment; Dataset metadata should include `| Simulation:` or explicitly mark `Simulation: 未报告`.")


def check_draft_status_markers(text: str, details: list[dict[str, object]], title: str) -> None:
    for pattern, message in DRAFT_STATUS_PATTERNS:
        if pattern.search(text):
            details.append({"title": title, "code": "draft_status_forbidden", "message": message})


def iter_descendants(block: dict, by_id: dict[str, dict]):
    for child_id in block.get("children") or []:
        child = by_id.get(child_id, {})
        if not child:
            continue
        yield child
        yield from iter_descendants(child, by_id)


def captioned_images_in(block: dict, by_id: dict[str, dict]) -> list[dict]:
    candidates = [block]
    candidates.extend(iter_descendants(block, by_id))
    return [
        candidate
        for candidate in candidates
        if candidate.get("block_type") == 27
        and ((candidate.get("image") or {}).get("caption") or {}).get("content", "").strip()
    ]


def contains_formula_marker(text: str) -> bool:
    return bool(
        re.search(r"\$[^$\n]+\$", text)
        or re.search(r"\\\(|\\\[|\\[A-Za-z]+", text)
        or re.search(r"\b(?:LaTeX|TeX|公式)\b", text, flags=re.I)
    )


def formula_caption_fallback(block: dict) -> bool:
    text = elements_text(block).strip()
    return (
        block.get("block_type") == 2
        and text.startswith("图 ")
        and "图注" in text
        and contains_formula_marker(text)
    )


def images_in(block: dict, by_id: dict[str, dict]) -> list[dict]:
    candidates = [block]
    candidates.extend(iter_descendants(block, by_id))
    return [candidate for candidate in candidates if candidate.get("block_type") == 27]


def image_caption_text(block: dict) -> str:
    return (((block.get("image") or {}).get("caption") or {}).get("content") or "").strip()


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
    for card_pos, index in enumerate(card_indices):
        heading = by_id.get(children[index], {})
        title = elements_text(heading).strip()
        next_card_index = card_indices[card_pos + 1] if card_pos + 1 < len(card_indices) else len(children)
        if index + 1 >= len(children):
            details.append({"title": title, "code": "metadata_missing", "message": "No block after card heading."})
            continue
        card_text_all = "\n".join(elements_text(by_id.get(block_id, {})).strip() for block_id in children[index:next_card_index])
        check_draft_status_markers(card_text_all, details, title)
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
        else:
            check_dataset_line(lines[3], card_text_all, details, title)
        for pdf_url in pdf_links(meta_block):
            slug_title = cvf_slug_title(pdf_url)
            if slug_title and token_count(slug_title) > token_count(title) + 2:
                details.append({"title": title, "code": "title_incomplete", "message": "Card heading appears shorter than the official CVF PDF title slug; use the complete official paper title, not only the method acronym."})
        media_blocks = []
        for scan_block_id in children[index + 2 : next_card_index]:
            scan_block = by_id.get(scan_block_id, {})
            scan_text = elements_text(scan_block)
            if scan_block.get("block_type") == 12 and scan_block.get("parent_id") == root.get("block_id"):
                break
            media_blocks.append(scan_block)
            if scan_block.get("block_type") == 2 and (
                scan_text.startswith("CVPR")
                or scan_text.startswith("[PDF]")
                or scan_text.startswith("PDF")
                or scan_text.startswith("Dataset:")
            ):
                details.append({"title": title, "code": "metadata_duplicate_block", "message": "Metadata lines 2-4 must not remain as separate blocks."})
        card_images = [image for block in media_blocks for image in images_in(block, by_id)]
        captioned_images = [image for block in media_blocks for image in captioned_images_in(block, by_id)]
        formula_caption_fallbacks = [block for block in media_blocks if formula_caption_fallback(block)]
        for block in media_blocks:
            block_text = elements_text(block).strip()
            block_text_casefolded = block_text.casefold()
            for placeholder in FORBIDDEN_PLACEHOLDERS:
                if placeholder.casefold() in block_text_casefolded:
                    details.append({"title": title, "code": "figure_placeholder_forbidden", "message": f"Formal paper-card delivery must not contain `{placeholder}`; add a verified figure/caption or mark the whole page as draft/blocker."})
        for image in card_images:
            caption = image_caption_text(image)
            if caption:
                check_draft_status_markers(caption, details, title)
            caption_casefolded = caption.casefold()
            for placeholder in FORBIDDEN_PLACEHOLDERS:
                if placeholder.casefold() in caption_casefolded:
                    details.append({"title": title, "code": "figure_caption_placeholder_forbidden", "message": f"Native image caption must not contain `{placeholder}` in formal paper-card delivery."})
        if card_images and len(captioned_images) + len(formula_caption_fallbacks) < len(card_images):
            details.append({"title": title, "code": "image_caption_missing", "message": "Every native image block, including images nested in grids, must carry the no-formula figure caption as native image caption. Formula-bearing captions may remain as an adjacent paragraph only to preserve formula fidelity."})
        if not captioned_images and not formula_caption_fallbacks:
            details.append({"title": title, "code": "image_missing", "message": "Formal paper-card delivery requires a native image block with complete caption, or a formula-caption fallback. `配图待补` is not accepted."})
        for offset, block in enumerate(media_blocks):
            block_text = elements_text(block).strip()
            if block.get("block_type") == 2 and block_text.startswith("图 ") and "图注" in block_text and not contains_formula_marker(block_text):
                details.append({"title": title, "code": "separate_caption_paragraph", "message": "No-formula figure captions must be native image captions, not separate paragraphs after the image."})

        card_texts = [
            elements_text(by_id.get(block_id, {})).strip()
            for block_id in children[index + 2 : next_card_index]
        ]
        for bullet in REQUIRED_BULLETS:
            if not any(text.startswith(f"{bullet}:") or text.startswith(f"{bullet}：") for text in card_texts):
                details.append({"title": title, "code": "required_bullet", "message": f"Missing fixed bullet slot `{bullet}`."})
        if any(re.match(r"^边界\s*/\s*启发\s*[:：]", text) for text in card_texts):
            details.append({"title": title, "code": "legacy_bullet", "message": "Use separate `局限` and `启发` bullet slots instead of the legacy combined `边界 / 启发` slot."})
        limitation_text = next(
            (re.sub(r"^局限\s*[:：]\s*", "", text).strip() for text in card_texts if re.match(r"^局限\s*[:：]", text)),
            None,
        )
        if limitation_text is None:
            pass
        elif not limitation_text:
            details.append({"title": title, "code": "limitation_empty", "message": "`局限` should state author-reported limitations, `作者未明确报告局限`, or verified `未报告` after checking the official source."})
        elif not re.search(r"作者|未报告|未明确报告|Not reported|N/A", limitation_text, flags=re.I):
            details.append({"title": title, "code": "limitation_source_marker", "message": "`局限` should distinguish author-reported limitations from agent analysis, or explicitly state `作者未明确报告局限` / verified `未报告`."})

    result = {"cards": len(card_indices), "issues": len(details), "details": details}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if details else 0


if __name__ == "__main__":
    raise SystemExit(main())
