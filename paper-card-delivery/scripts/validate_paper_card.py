#!/usr/bin/env python3
"""Validate the user's compact paper-card Markdown structure.

This is a structural lint only. It cannot verify whether the official paper was
actually read; agents must still report source-verification evidence.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote


REQUIRED_BULLETS = ["定义", "问题", "方法", "实现", "结论", "局限", "启发"]
CJK_RE = re.compile(r"[\u3400-\u9fff]")
RESIDUE_PATTERNS = [
    r"!\[\[",
    r"\bassets/",
    r"\bEW_IMG",
    r"图像：",
    r"Image:\s",
    r"/Users/",
    r"WorldModelVault",
]
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
SIMULATION_HINTS_RE = re.compile(
    r"\b("
    r"mujoco|isaac(?:\s+gym|\s+sim)?|pybullet|bullet|gazebo|habitat|ai2-thor|"
    r"carla|sapien|airsim|unity|unreal|blender|omniverse|"
    r"clo3d|marvelous\s+designer"
    r")\b",
    re.I,
)
STATUS_VALUES = {"未报告", "待核验", "不适用", "not reported", "n/a", "na", "none"}


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
    match = re.search(r"\[PDF\]\((https?://[^)]+\.pdf)\)", text)
    return match.group(1) if match else None


def dataset_entries(dataset_line: str) -> list[str]:
    value = re.sub(r"^Dataset:\s*", "", dataset_line, flags=re.I)
    dataset_part = re.split(r"\s*\|\s*Simulation\s*[:：]", value, maxsplit=1, flags=re.I)[0]
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
    entries = dataset_entries(dataset_line)
    if len(entries) > 3:
        issue("dataset_too_many", "Dataset metadata must list at most three visible dataset names; put additional datasets in `实现` if needed.")
    if SIMULATION_HINTS_RE.search(card) and not re.search(r"\|\s*Simulation\s*[:：]", dataset_line):
        issue("simulation_missing", "Card mentions a known simulator/environment; Dataset metadata should include `| Simulation:` or explicitly mark `Simulation: 未报告`.")


def split_cards(text: str) -> list[tuple[int, str, str]]:
    matches = list(re.finditer(r"^####\s+(.+?)\s*$", text, flags=re.M))
    cards: list[tuple[int, str, str]] = []
    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        line_no = text[: start].count("\n") + 1
        cards.append((line_no, m.group(1).strip(), text[start:end].strip()))
    return cards


def metadata_lines_after_heading(card: str) -> tuple[list[str], bool]:
    """Return the physical four-line metadata block after a card heading.

    Feishu paper-card metadata is intentionally compact: four consecutive
    non-empty physical lines immediately after the heading. Do not skip a
    blank line after the title; that would make the metadata visually loose.
    """

    lines = [ln.rstrip() for ln in card.splitlines()]
    metadata = lines[1:5]
    compact = len(metadata) == 4 and all(ln.strip() for ln in metadata)
    return metadata, compact


def check_card(line_no: int, title: str, card: str) -> list[dict[str, object]]:
    issues: list[dict[str, object]] = []
    metadata_lines, compact_metadata = metadata_lines_after_heading(card)

    def issue(code: str, msg: str) -> None:
        issues.append({"line": line_no, "title": title, "code": code, "message": msg})

    if len(metadata_lines) < 4:
        issue("metadata_missing", "Expected short-title, Venue｜Institution, PDF｜Project｜Code, and Dataset metadata lines.")
    else:
        if not compact_metadata:
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
            issue("limitation_empty", "`局限` should state author-reported limitations, `作者未明确报告局限`, or `待核验`.")
        elif not re.search(r"作者|未报告|未明确报告|待核验|Not reported|N/A", limitation_text, flags=re.I):
            issue("limitation_source_marker", "`局限` should distinguish author-reported limitations from agent analysis, or explicitly state `作者未明确报告局限` / `待核验`.")

    if not re.search(r"^\s*[-*]\s+核心创新\s*1\s*[:：]", card, flags=re.M):
        issue("method_innovation", "Missing nested `核心创新 1` bullet under 方法.")
    if not re.search(r"^\s*[-*]\s+核心创新\s*2\s*[:：]", card, flags=re.M):
        issue("method_innovation", "Missing nested `核心创新 2` bullet under 方法.")

    for pattern in RESIDUE_PATTERNS:
        if re.search(pattern, card):
            issue("local_residue", f"Reader-facing text contains local/Obsidian residue matching `{pattern}`.")

    lowered = card.lower()
    for hint in BAD_IMAGE_HINTS:
        if hint in lowered:
            issue("bad_image_hint", f"Possible forbidden paper-card image/source hint: `{hint}`.")

    card_casefolded = card.casefold()
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
    args = parser.parse_args()

    if not args.path or args.path == "-":
        text = sys.stdin.read()
    else:
        text = Path(args.path).read_text(encoding="utf-8")

    cards = split_cards(text)
    issues: list[dict[str, object]] = []
    if not cards:
        issues.append({"line": 1, "title": None, "code": "no_cards", "message": "No `#### Paper English Title` card headings found."})
    for card in cards:
        issues.extend(check_card(*card))

    result = {"cards": len(cards), "issues": len(issues), "details": issues}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
