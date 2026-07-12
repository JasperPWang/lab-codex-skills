#!/usr/bin/env python3
"""Validate the user's compact paper-card Markdown structure.

This is a structural lint only. It cannot verify whether the official paper was
actually read; agents must still report source-verification evidence.
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
BULLET_MIN_WIDTH = 75.0
BULLET_MAX_WIDTH = 100.0
INSPIRATION_TAIL_LENGTH = 16
INSPIRATION_TAIL_REPEAT_LIMIT = 3
INSPIRATION_NEAR_DUPLICATE_RATIO = 0.78
CJK_RE = re.compile(r"[\u3400-\u9fff]")
COMMON_RESIDUE_PATTERNS = [
    r"\bEW_IMG",
    r"图像：",
    r"Image:\s",
    r"/Users/",
    r"WorldModelVault",
]
TARGET_RESIDUE_PATTERNS = {
    "feishu": [r"!\[\[", r"\bassets/"],
    "notion": [r"!\[\[", r"\bassets/"],
    "markdown": [r"!\[\["],
    "obsidian": [],
}


def visual_width(text: str) -> float:
    """Approximate Feishu visual width in Chinese-character-equivalent units."""
    width = 0.0
    for char in text.strip():
        if char.isspace():
            continue
        width += 0.5 if ord(char) < 128 else 1.0
    return width


def normalize_inspiration(text: str) -> str:
    return re.sub(r"[^0-9a-z\u3400-\u9fff]+", "", text.casefold())


def inspiration_reuse_issues(entries: list[tuple[int, str, str]]) -> list[dict[str, object]]:
    normalized = [(line_no, title, normalize_inspiration(body)) for line_no, title, body in entries]
    issues: list[dict[str, object]] = []

    exact_groups: dict[str, list[tuple[int, str]]] = defaultdict(list)
    tail_groups: dict[str, list[tuple[int, str]]] = defaultdict(list)
    for line_no, title, body in normalized:
        if not body:
            continue
        exact_groups[body].append((line_no, title))
        if len(body) >= INSPIRATION_TAIL_LENGTH:
            tail_groups[body[-INSPIRATION_TAIL_LENGTH:]].append((line_no, title))

    exact_titles: set[str] = set()
    for cards in exact_groups.values():
        if len(cards) < 2:
            continue
        exact_titles.update(title for _, title in cards)
        for line_no, title in cards:
            issues.append({
                "line": line_no,
                "title": title,
                "code": "inspiration_duplicate",
                "message": f"`启发` duplicates another card verbatim across {len(cards)} cards; derive it independently from this paper.",
            })

    repeated_tail_titles: set[str] = set()
    for cards in tail_groups.values():
        if len(cards) < INSPIRATION_TAIL_REPEAT_LIMIT:
            continue
        repeated_tail_titles.update(title for _, title in cards)
        for line_no, title in cards:
            issues.append({
                "line": line_no,
                "title": title,
                "code": "inspiration_repeated_tail",
                "message": f"`启发` reuses the same {INSPIRATION_TAIL_LENGTH}-character ending across {len(cards)} cards; replace the shared template with paper-specific reasoning.",
            })

    near_duplicate_titles: set[str] = set()
    for index, (line_a, title_a, body_a) in enumerate(normalized):
        if title_a in exact_titles or title_a in repeated_tail_titles or not body_a:
            continue
        for line_b, title_b, body_b in normalized[index + 1 :]:
            if title_b in exact_titles or title_b in repeated_tail_titles or not body_b:
                continue
            ratio = difflib.SequenceMatcher(None, body_a, body_b).ratio()
            if ratio < INSPIRATION_NEAR_DUPLICATE_RATIO:
                continue
            for line_no, title, other in ((line_a, title_a, title_b), (line_b, title_b, title_a)):
                if title in near_duplicate_titles:
                    continue
                near_duplicate_titles.add(title)
                issues.append({
                    "line": line_no,
                    "title": title,
                    "code": "inspiration_near_duplicate",
                    "message": f"`启发` is {ratio:.0%} similar to `{other}`; rewrite it from this paper's own mechanism, limitation, or open question.",
                })

    return issues
BAD_IMAGE_HINTS = [
    "first page",
    "first-page",
    "title page",
    "paper page",
    "abstract page",
]
FORBIDDEN_PLACEHOLDERS = [
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
]
TRANSLATABLE_ENGLISH_TERMS = {
    "parametric human estimation": "参数化人体估计",
    "perspective distortion": "透视畸变/透视失真",
    "scene geometry": "场景几何",
    "camera pose": "相机位姿",
    "body pose": "人体姿态",
    "mesh reconstruction": "网格重建",
    "3d human reconstruction": "三维人体重建",
    "motion-dependent cloth dynamics": "运动相关布料动力学",
    "physically plausible deformation": "物理合理形变",
    "simulation-ready asset": "仿真就绪资产",
}
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
ARXIV_PDF_RE = re.compile(r"arxiv\.org/pdf/", re.I)
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
    r"(\[(?:Supplement|Supplementary|Appendix|Suppl\.?|Supp\.?)\]\(https?://[^)]+\)|w/o\. supplement)",
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


def find_pdf_url(text: str) -> str | None:
    match = re.search(r"\[PDF\]\((https?://[^)]+)\)", text, flags=re.I)
    return match.group(1) if match else None


def check_pdf_link_line(link_line: str, issue) -> None:
    pdf_url = find_pdf_url(link_line)
    if not pdf_url or ARXIV_PDF_RE.search(pdf_url):
        return
    if VENUE_OR_PUBLISHER_PDF_RE.search(pdf_url) and not SUPPLEMENT_STATUS_RE.search(link_line):
        issue(
            "supplement_link_missing",
            "When using an official venue/publisher/conference PDF instead of an arXiv PDF, add `[Supplement](...)`, `[Appendix](...)`, or `w/o. supplement` on the metadata link line.",
        )


def check_compact_link_labels(link_line: str, issue) -> None:
    allowed = {"PDF", "Supplement", "Suppl.", "Appendix", "Project", "Code"}
    labels = re.findall(r"\[([^\]]+)\]\(https?://[^)]+\)", link_line)
    invalid = [label for label in labels if label not in allowed]
    if invalid:
        issue(
            "noncompact_link_label",
            "Use only compact metadata link labels "
            "`PDF`, `Supplement`/`Suppl.`/`Appendix`, `Project`, and `Code`; "
            f"move extra source links out of the card metadata line: {', '.join(invalid)}.",
        )


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


def check_dataset_line(dataset_line: str, card: str, issue) -> None:
    if re.search(r"simluation\s*[:：]", dataset_line, flags=re.I):
        issue("simulation_spelling", "Use `Simulation:` in the Dataset metadata line, not `Simluation:`.")
    if re.search(r"simulation\s*[:：]", dataset_line, flags=re.I) and not re.search(r"\|\s*Simulation\s*[:：]", dataset_line):
        issue("simulation_format", "Simulation metadata must be appended as `| Simulation:` on the Dataset line.")
    if VERBOSE_MODEL_METADATA_RE.search(dataset_line):
        issue("verbose_model_metadata", "Do not use verbose model metadata labels such as `Open-source backbone:`, `Backbone:`, `Training:`, or `Open-source baselines:`; use a compact suffix like `| FLUX.1-dev，LoRA 微调`.")
    entries = dataset_entries(dataset_line)
    if len(entries) > 3:
        issue("dataset_too_many", "Dataset metadata must list at most three visible dataset names; put additional datasets in `实现` if needed.")
    backbone_needed = BACKBONE_HINTS_RE.search(card) or (
        FOUNDATION_MODEL_NAMES_RE.search(card) and TRAINING_MODE_HINTS_RE.search(card)
    )
    suffix = compact_model_suffix(dataset_line)
    if backbone_needed and not (suffix and (FOUNDATION_MODEL_NAMES_RE.search(suffix) or STATUS_MARKER_RE.search(suffix))):
        issue("compact_open_source_backbone_missing", "Card mentions a backbone/base/foundation model; Dataset metadata should append a compact suffix such as `| FLUX.1-dev，LoRA 微调`, or mark `开源基座未报告/不适用` in that suffix.")
    if TRAINING_MODE_HINTS_RE.search(card) and not (suffix and (TRAINING_MODE_HINTS_RE.search(suffix) or STATUS_MARKER_RE.search(suffix))):
        issue("compact_training_missing", "Card mentions training-free/fine-tuning/adapter/LoRA/frozen-backbone mode; Dataset metadata should append it compactly, e.g. `| FLUX.1-dev，LoRA 微调`.")


def split_cards(text: str) -> list[tuple[int, str, str]]:
    matches = list(re.finditer(r"^####\s+(.+?)\s*$", text, flags=re.M))
    cards: list[tuple[int, str, str]] = []
    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        line_no = text[: start].count("\n") + 1
        cards.append((line_no, m.group(1).strip(), text[start:end].strip()))
    return cards


def metadata_lines_after_heading(card: str, target: str) -> tuple[list[str], bool]:
    """Return the four logical metadata rows after a card heading.

    Feishu paper-card metadata is intentionally compact: four consecutive
    non-empty physical lines immediately after the heading. Do not skip a
    blank line after the title; that would make the metadata visually loose.

    Notion's Markdown importer creates a paragraph for every physical line,
    including trailing-space Markdown hard breaks. The Notion adapter must
    therefore emit one physical line containing exactly three `<br>` tags.
    """

    lines = [ln.rstrip() for ln in card.splitlines()]
    if target == "notion":
        if len(lines) < 2:
            return [], False
        parts = re.split(r"<br\s*/?>", lines[1], flags=re.I)
        metadata = [part.strip() for part in parts]
        compact = len(metadata) == 4 and all(metadata) and lines[1].lower().count("<br>") == 3
        return metadata, compact
    metadata = lines[1:5]
    compact = len(metadata) == 4 and all(ln.strip() for ln in metadata)
    return metadata, compact


def check_card(line_no: int, title: str, card: str, target: str) -> list[dict[str, object]]:
    issues: list[dict[str, object]] = []
    metadata_lines, compact_metadata = metadata_lines_after_heading(card, target)

    def issue(code: str, msg: str) -> None:
        issues.append({"line": line_no, "title": title, "code": code, "message": msg})

    if len(metadata_lines) < 4:
        issue("metadata_missing", "Expected short-title, Venue｜Institution, PDF｜Project｜Code, and Dataset metadata lines.")
    else:
        if not compact_metadata:
            if target == "notion":
                issue("metadata_spacing", "Notion metadata must be one physical Markdown line with exactly three `<br>` tags, yielding one native paragraph with four hard-break rows.")
            else:
                issue("metadata_spacing", "Metadata must be four consecutive non-empty lines with no blank lines inside the metadata block.")
        if "｜" not in metadata_lines[0]:
            issue("takeaway_line", "Second line should be `短译名｜核心创新点 / takeaway 短语`.")
        if "｜" not in metadata_lines[1]:
            issue("venue_institution", "Venue｜Institution metadata line is missing `｜`.")
        link_line = metadata_lines[2]
        if not any(token in link_line for token in ["PDF", "w/o. PDF"]):
            issue("pdf_slot", "PDF slot missing or not using compact PDF/w/o. PDF status.")
        if not any(token in link_line for token in ["Project", "w/o. project page"]):
            issue("project_slot", "Project slot missing or not using compact Project/w/o. project page status.")
        if not any(token in link_line for token in ["Code", "w/o. verified code", "w/o. code"]):
            issue("code_slot", "Code slot missing or not using compact Code/w/o. code status.")
        check_compact_link_labels(link_line, issue)
        check_pdf_link_line(link_line, issue)
        if not metadata_lines[3].startswith("Dataset:"):
            issue("dataset", "Fourth metadata line must start with `Dataset:`.")
        else:
            check_dataset_line(metadata_lines[3], card, issue)
        pdf_url = find_pdf_url(card)
        slug_title = cvf_slug_title(pdf_url or "")
        if slug_title and token_count(slug_title) > token_count(title) + 2:
            issue("title_incomplete", "Card heading appears shorter than the official CVF PDF title slug; use the complete official paper title, not only the method acronym.")

    for bullet in REQUIRED_BULLETS:
        if not re.search(rf"^\s*[-*]\s+{re.escape(bullet)}\s*[:：]", card, flags=re.M):
            issue("required_bullet", f"Missing fixed bullet slot `{bullet}`.")

    if re.search(r"^\s*[-*]\s+边界\s*/\s*启发\s*[:：]", card, flags=re.M):
        issue("legacy_bullet", "Use separate `局限` and `启发` bullet slots instead of the legacy combined `边界 / 启发` slot.")

    limitation_match = re.search(r"^\s*[-*]\s+局限\s*[:：](.*?)(?=^\s*[-*]\s+(?:定义|问题|方法|实现|结论|启发)\s*[:：]|\Z)", card, flags=re.M | re.S)
    if limitation_match:
        limitation_text = limitation_match.group(1).strip()
        if not limitation_text:
            issue("limitation_empty", "`局限` should state author-reported limitations or `作者未明确报告局限`.")
        elif not re.search(r"作者|未报告|未明确报告|Not reported|N/A", limitation_text, flags=re.I):
            issue("limitation_source_marker", "`局限` should distinguish author-reported limitations from agent analysis, or explicitly state `作者未明确报告局限`.")

    if not re.search(r"^\s*[-*]\s+核心创新\s*1\s*[:：]", card, flags=re.M):
        issue("method_innovation", "Missing nested `核心创新 1` bullet under 方法.")
    if not re.search(r"^\s*[-*]\s+核心创新\s*2\s*[:：]", card, flags=re.M):
        issue("method_innovation", "Missing nested `核心创新 2` bullet under 方法.")

    for label in [*REQUIRED_BULLETS, "核心创新 1", "核心创新 2"]:
        match = re.search(rf"^\s*[-*]\s+{re.escape(label)}\s*[:：]\s*(.+)$", card, flags=re.M)
        if not match:
            continue
        width = visual_width(match.group(1))
        if width < BULLET_MIN_WIDTH:
            issue("bullet_too_short", f"`{label}` body width is {width:.1f}; rewrite from the official paper to reach the 75–100 two-line budget.")
        elif width > BULLET_MAX_WIDTH:
            issue("bullet_too_long", f"`{label}` body width is {width:.1f}; condense it to the 75–100 two-line budget.")

    residue_patterns = [*COMMON_RESIDUE_PATTERNS, *TARGET_RESIDUE_PATTERNS[target]]
    for pattern in residue_patterns:
        if re.search(pattern, card):
            issue("platform_residue", f"Reader-facing text contains residue invalid for target `{target}` matching `{pattern}`.")

    lowered = card.lower()
    for hint in BAD_IMAGE_HINTS:
        if hint in lowered:
            issue("bad_image_hint", f"Possible forbidden paper-card image/source hint: `{hint}`.")

    card_casefolded = card.casefold()
    if UNRESOLVED_MARKERS_RE.search(card):
        issue("unresolved_verification_marker", "Formal paper-card delivery must not contain `待核验`, `candidate`, TODO/TBD, or pending-verification markers; verify the source or keep the whole item as an explicit draft/blocker outside final delivery.")
    for placeholder in FORBIDDEN_PLACEHOLDERS:
        if placeholder.casefold() in card_casefolded:
            issue(
                "figure_placeholder_forbidden",
                f"Formal paper-card delivery must not contain `{placeholder}`; add a verified figure/caption or mark the whole page as draft/blocker.",
            )

    for line in card.splitlines():
        if not CJK_RE.search(line):
            continue
        line_lowered = line.lower()
        for term, chinese in TRANSLATABLE_ENGLISH_TERMS.items():
            if term in line_lowered:
                gloss_pattern = rf"[（(]\s*{re.escape(term)}\s*[）)]"
                if re.search(gloss_pattern, line_lowered):
                    continue
                issue("language_mixing", f"Use Chinese-first wording for `{term}` -> `{chinese}`.")

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate compact paper-card Markdown structure.")
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
    else:
        text = Path(args.path).read_text(encoding="utf-8")

    cards = split_cards(text)
    issues: list[dict[str, object]] = []
    inspirations: list[tuple[int, str, str]] = []
    if not cards:
        issues.append({"line": 1, "title": None, "code": "no_cards", "message": "No `#### Paper English Title` card headings found."})
    for card in cards:
        issues.extend(check_card(*card, args.target))
        match = re.search(r"^\s*[-*]\s+启发\s*[:：]\s*(.+)$", card[2], flags=re.M)
        if match:
            inspirations.append((card[0], card[1], match.group(1).strip()))

    issues.extend(inspiration_reuse_issues(inspirations))

    result = {"cards": len(cards), "issues": len(issues), "details": issues}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
