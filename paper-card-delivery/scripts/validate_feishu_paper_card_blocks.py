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
import difflib
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote


REQUIRED_BULLETS = ["定义", "问题", "方法", "实现", "结论", "局限", "启发"]
FOUNDATION_MODEL_NAMES_RE = re.compile(
    r"\b("
    r"flux(?:\.[12])?|stable\s+diffusion|sdxl|sd3|sd\s*1\.5|controlnet|"
    r"zero123|wonder3d|tripo(?:sr)?|mvdream|syncdreamer|dreamfusion|magic3d|"
    r"hunyuan3d|hunyuanimage|qwen[-\s]?image|longcat[-\s]?image|z[-\s]?image|"
    r"kolors|cogview|bagel|step1x|instantmesh|openlrm|dust3r|vggt|streamvggt|"
    r"trellis|pi3|π³|moge|metric3d|noposplat|cogvideox|sam2|t5|"
    r"shapellm|dinov2|alpha[-\s]?clip|roberta|qwen(?:[-\s]?(?:2|3)(?:[-\s]?\d+(?:\.\d+)?b)?)?"
    r")\b",
    re.I,
)
BACKBONE_HINTS_RE = re.compile(
    r"\b("
    r"backbone|base\s+model|foundation\s+model|pre[-\s]?trained\s+model|"
    r"pre[-\s]?trained\s+backbone|encoder\s+backbone|decoder\s+backbone|"
    r"diffusion\s+backbone|initialized\s+from|initialised\s+from|powered\s+by"
    r")\b|"
    r"(骨干|基座|基础模型|预训练模型|预训练骨干|初始化)",
    re.I,
)
TRAINING_MODE_HINTS_RE = re.compile(
    r"\b("
    r"training[-\s]?free|train[-\s]?free|zero[-\s]?training|without\s+training|"
    r"no\s+training|inference[-\s]?only|lora|low[-\s]?rank\s+adaptation|"
    r"adapter|fine[-\s]?tune|finetune|fine[-\s]?tuning|full[-\s]?fine[-\s]?tune|"
    r"full[-\s]?fine[-\s]?tuning|full[-\s]?training|end[-\s]?to[-\s]?end|"
    r"from[-\s]?scratch|frozen|freeze|test[-\s]?time\s+optimization|"
    r"distillation"
    r")\b|"
    r"(免训练|无需训练|零训练|仅推理|推理时优化|测试时优化|LoRA|适配器|微调|"
    r"全量微调|全量训练|端到端|从头训练|冻结|蒸馏)",
    re.I,
)
STATUS_VALUES = {"未报告", "不适用", "not reported", "n/a", "na", "none"}
BULLET_MIN_WIDTH = 75.0
BULLET_MAX_WIDTH = 100.0
INSPIRATION_TAIL_LENGTH = 16
INSPIRATION_TAIL_REPEAT_LIMIT = 3
INSPIRATION_NEAR_DUPLICATE_RATIO = 0.78
ARXIV_PDF_RE = re.compile(r"arxiv\.org/pdf/", re.I)
PDF_URL_RE = re.compile(r"\.pdf(?:$|[?#])|/pdf(?:/|$|\?)", re.I)
VENUE_OR_PUBLISHER_PDF_RE = re.compile(
    r"("
    r"openaccess\.thecvf\.com|thecvf\.com|cv-foundation\.org|ecva\.net|"
    r"openreview\.net/(?:pdf|attachment)|proceedings\.neurips\.cc|papers\.nips\.cc|"
    r"proceedings\.mlr\.press|dl\.acm\.org/(?:doi/)?pdf|ieeexplore\.ieee\.org|"
    r"computer\.org/csdl|link\.springer\.com|springer\.com|aaai\.org|ijcai\.org|"
    r"aclanthology\.org|bmvc\d*\.org|bmva-archive\.org"
    r")",
    re.I,
)
SUPPLEMENT_STATUS_RE = re.compile(
    r"(\b(?:Supplement|Supplementary|Appendix|Suppl\.?|Supp\.?)\b|w/o\. supplement)",
    re.I,
)
STATUS_MARKER_RE = re.compile(r"(未报告|不适用|not reported|n/a|na|none)", re.I)
UNRESOLVED_MARKERS_RE = re.compile(
    r"(待核验|\bcandidate\b|\bTODO\b|\bTBD\b|pending\s+(?:verification|source|check)|to\s+verify)",
    re.I,
)
VERBOSE_MODEL_METADATA_RE = re.compile(
    r"\|\s*(?:Open[-\s]?source\s+backbone|Backbone|Training|Open[-\s]?source\s+baselines?)\s*[:：]",
    re.I,
)
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


def visual_width(text: str) -> float:
    """Approximate Feishu visual width in Chinese-character-equivalent units."""
    width = 0.0
    for char in text.strip():
        if char.isspace():
            continue
        width += 0.5 if ord(char) < 128 else 1.0
    return width


def bullet_body_text(text: str, label: str) -> str | None:
    match = re.match(rf"^{re.escape(label)}\s*[:：]\s*(.*)$", text.strip())
    return match.group(1).strip() if match else None


def normalize_inspiration(text: str) -> str:
    return re.sub(r"[^0-9a-z\u3400-\u9fff]+", "", text.casefold())


def inspiration_reuse_issues(entries: list[tuple[str, str]]) -> list[dict[str, object]]:
    normalized = [(title, normalize_inspiration(body)) for title, body in entries]
    issues: list[dict[str, object]] = []

    exact_groups: dict[str, list[str]] = defaultdict(list)
    tail_groups: dict[str, list[str]] = defaultdict(list)
    for title, body in normalized:
        if not body:
            continue
        exact_groups[body].append(title)
        if len(body) >= INSPIRATION_TAIL_LENGTH:
            tail_groups[body[-INSPIRATION_TAIL_LENGTH:]].append(title)

    exact_titles: set[str] = set()
    for titles in exact_groups.values():
        if len(titles) < 2:
            continue
        exact_titles.update(titles)
        for title in titles:
            issues.append({
                "title": title,
                "code": "inspiration_duplicate",
                "message": f"`启发` duplicates another card verbatim across {len(titles)} cards; derive it independently from this paper.",
            })

    repeated_tail_titles: set[str] = set()
    for titles in tail_groups.values():
        if len(titles) < INSPIRATION_TAIL_REPEAT_LIMIT:
            continue
        repeated_tail_titles.update(titles)
        for title in titles:
            issues.append({
                "title": title,
                "code": "inspiration_repeated_tail",
                "message": f"`启发` reuses the same {INSPIRATION_TAIL_LENGTH}-character ending across {len(titles)} cards; replace the shared template with paper-specific reasoning.",
            })

    near_duplicate_titles: set[str] = set()
    for index, (title_a, body_a) in enumerate(normalized):
        if title_a in exact_titles or title_a in repeated_tail_titles or not body_a:
            continue
        for title_b, body_b in normalized[index + 1 :]:
            if title_b in exact_titles or title_b in repeated_tail_titles or not body_b:
                continue
            ratio = difflib.SequenceMatcher(None, body_a, body_b).ratio()
            if ratio < INSPIRATION_NEAR_DUPLICATE_RATIO:
                continue
            for title, other in ((title_a, title_b), (title_b, title_a)):
                if title in near_duplicate_titles:
                    continue
                near_duplicate_titles.add(title)
                issues.append({
                    "title": title,
                    "code": "inspiration_near_duplicate",
                    "message": f"`启发` is {ratio:.0%} similar to `{other}`; rewrite it from this paper's own mechanism, limitation, or open question.",
                })

    return issues


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


def linked_urls(block: dict) -> list[str]:
    urls: list[str] = []
    for element in text_elements(block):
        text_run = element.get("text_run") or {}
        style = text_run.get("text_element_style") or {}
        link = style.get("link") or {}
        url = link.get("url") or ""
        if url:
            urls.append(url)
    return urls


def pdf_links(block: dict) -> list[str]:
    return [
        url
        for url in linked_urls(block)
        if PDF_URL_RE.search(url) or VENUE_OR_PUBLISHER_PDF_RE.search(url)
    ]


def compact_model_suffix(dataset_line: str) -> str:
    value = re.sub(r"^Dataset:\s*", "", dataset_line, flags=re.I)
    parts = [part.strip() for part in value.split("|")]
    suffixes: list[str] = []
    for part in parts[1:]:
        if re.match(r"^Simulation\s*[:：]", part, flags=re.I):
            continue
        if re.search(r"[:：]", part):
            continue
        if part:
            suffixes.append(part)
    return " | ".join(suffixes)


def dataset_entries(dataset_line: str) -> list[str]:
    value = re.sub(r"^Dataset:\s*", "", dataset_line, flags=re.I)
    dataset_part = re.split(r"\s*\|\s*", value, maxsplit=1)[0]
    dataset_part = dataset_part.strip()
    if not dataset_part or dataset_part.lower() in STATUS_VALUES:
        return []
    parts = re.split(r"\s*(?:,|，|、|;|；|\s/\s)\s*", dataset_part)
    return [part.strip() for part in parts if part.strip()]


def check_dataset_line(dataset_line: str, card_text: str, details: list[dict[str, object]], title: str) -> None:
    def add(code: str, message: str) -> None:
        details.append({"title": title, "code": code, "message": message})

    if re.search(r"simluation\s*[:：]", dataset_line, flags=re.I):
        add("simulation_spelling", "Use `Simulation:` in the Dataset metadata line, not `Simluation:`.")
    if re.search(r"simulation\s*[:：]", dataset_line, flags=re.I) and not re.search(r"\|\s*Simulation\s*[:：]", dataset_line):
        add("simulation_format", "Simulation metadata must be appended as `| Simulation:` on the Dataset line.")
    if VERBOSE_MODEL_METADATA_RE.search(dataset_line):
        add("verbose_model_metadata", "Do not use verbose model metadata labels such as `Open-source backbone:`, `Backbone:`, `Training:`, or `Open-source baselines:`; use a compact suffix like `| FLUX.1-dev，LoRA 微调`.")
    entries = dataset_entries(dataset_line)
    if len(entries) > 3:
        add("dataset_too_many", "Dataset metadata must list at most three visible dataset names; put additional datasets in `实现` if needed.")
    backbone_needed = BACKBONE_HINTS_RE.search(card_text) or (
        FOUNDATION_MODEL_NAMES_RE.search(card_text) and TRAINING_MODE_HINTS_RE.search(card_text)
    )
    suffix = compact_model_suffix(dataset_line)
    if backbone_needed and not (suffix and (FOUNDATION_MODEL_NAMES_RE.search(suffix) or STATUS_MARKER_RE.search(suffix))):
        add("compact_open_source_backbone_missing", "Card mentions a backbone/base/foundation model; Dataset metadata should append a compact suffix such as `| FLUX.1-dev，LoRA 微调`, or mark `开源基座未报告/不适用` in that suffix.")
    if TRAINING_MODE_HINTS_RE.search(card_text) and not (suffix and (TRAINING_MODE_HINTS_RE.search(suffix) or STATUS_MARKER_RE.search(suffix))):
        add("compact_training_missing", "Card mentions training-free/fine-tuning/adapter/LoRA/frozen-backbone mode; Dataset metadata should append it compactly, e.g. `| FLUX.1-dev，LoRA 微调`.")


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
    inspirations: list[tuple[str, str]] = []
    for card_pos, index in enumerate(card_indices):
        heading = by_id.get(children[index], {})
        title = elements_text(heading).strip()
        next_card_index = card_indices[card_pos + 1] if card_pos + 1 < len(card_indices) else len(children)
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
        for pdf_url in pdf_links(meta_block):
            if ARXIV_PDF_RE.search(pdf_url):
                continue
            if VENUE_OR_PUBLISHER_PDF_RE.search(pdf_url) and not SUPPLEMENT_STATUS_RE.search(lines[2]):
                details.append({"title": title, "code": "supplement_link_missing", "message": "When using an official venue/publisher/conference PDF instead of an arXiv PDF, add `[Supplement](...)`, `[Appendix](...)`, or `w/o. supplement` on metadata line 3."})
        if not lines[3].startswith("Dataset:"):
            details.append({"title": title, "code": "dataset", "message": "Metadata line 4 must start with `Dataset:`."})
        else:
            card_text = "\n".join(elements_text(by_id.get(block_id, {})).strip() for block_id in children[index:next_card_index])
            check_dataset_line(lines[3], card_text, details, title)
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

        card_blocks: list[dict] = []
        for block_id in children[index + 2 : next_card_index]:
            block = by_id.get(block_id, {})
            card_blocks.append(block)
            card_blocks.extend(iter_descendants(block, by_id))
        card_texts = [elements_text(block).strip() for block in card_blocks]
        if any(UNRESOLVED_MARKERS_RE.search(text) for text in card_texts):
            details.append({"title": title, "code": "unresolved_verification_marker", "message": "Formal paper-card delivery must not contain `待核验`, `candidate`, TODO/TBD, or pending-verification markers; verify the source or keep the whole item as an explicit draft/blocker outside final delivery."})
        if any(UNRESOLVED_MARKERS_RE.search(image_caption_text(image)) for image in card_images):
            details.append({"title": title, "code": "unresolved_caption_marker", "message": "Native figure captions must not contain unresolved verification markers such as `待核验`, TODO/TBD, or pending-verification text."})
        for bullet in REQUIRED_BULLETS:
            if not any(text.startswith(f"{bullet}:") or text.startswith(f"{bullet}：") for text in card_texts):
                details.append({"title": title, "code": "required_bullet", "message": f"Missing fixed bullet slot `{bullet}`."})
        for label in [*REQUIRED_BULLETS, "核心创新 1", "核心创新 2"]:
            body = next((body for text in card_texts if (body := bullet_body_text(text, label)) is not None), None)
            if body is None:
                if label.startswith("核心创新"):
                    details.append({"title": title, "code": "method_innovation", "message": f"Missing nested `{label}` bullet under 方法."})
                continue
            width = visual_width(body)
            if width < BULLET_MIN_WIDTH:
                details.append({"title": title, "code": "bullet_too_short", "message": f"`{label}` body width is {width:.1f}; rewrite from the official paper to reach the 75–100 two-line budget."})
            elif width > BULLET_MAX_WIDTH:
                details.append({"title": title, "code": "bullet_too_long", "message": f"`{label}` body width is {width:.1f}; condense it to the 75–100 two-line budget."})
            if label == "启发":
                inspirations.append((title, body))
        if any(re.match(r"^边界\s*/\s*启发\s*[:：]", text) for text in card_texts):
            details.append({"title": title, "code": "legacy_bullet", "message": "Use separate `局限` and `启发` bullet slots instead of the legacy combined `边界 / 启发` slot."})
        limitation_text = next(
            (re.sub(r"^局限\s*[:：]\s*", "", text).strip() for text in card_texts if re.match(r"^局限\s*[:：]", text)),
            None,
        )
        if limitation_text is None:
            pass
        elif not limitation_text:
            details.append({"title": title, "code": "limitation_empty", "message": "`局限` should state author-reported limitations or `作者未明确报告局限`."})
        elif not re.search(r"作者|未报告|未明确报告|Not reported|N/A", limitation_text, flags=re.I):
            details.append({"title": title, "code": "limitation_source_marker", "message": "`局限` should distinguish author-reported limitations from agent analysis, or explicitly state `作者未明确报告局限`."})

    details.extend(inspiration_reuse_issues(inspirations))
    result = {"cards": len(card_indices), "issues": len(details), "details": details}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if details else 0


if __name__ == "__main__":
    raise SystemExit(main())
