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
DRAFT_STATUS_PATTERNS = [
    (re.compile(r"待核验"), "Formal paper-card delivery must not contain `待核验`; verify against the official source and resolve it. If the original source cannot be obtained after all official acquisition/extraction routes fail, report a blocker instead of shipping a card."),
    (re.compile(r"\bcandidate\s*/", re.I), "Formal paper-card delivery must not contain candidate-status markers."),
    (re.compile(r"\b(?:todo|tbd|pending)\b", re.I), "Formal paper-card delivery must not contain TODO/TBD/pending verification markers."),
    (re.compile(r"(?:核验|验证)\s*(?:TODO|TBD|pending|待办)", re.I), "Formal paper-card delivery must not contain unresolved verification TODOs."),
]
BAD_CAPTION_FILLER_PATTERNS = [
    (re.compile(r"方法或实验概览"), "Figure caption must translate the original caption, not say `方法或实验概览`."),
    (re.compile(r"method\s+or\s+experiment\s+overview", re.I), "Figure caption must translate the original caption, not say `method or experiment overview`."),
    (re.compile(r"用于说明(?:论文)?的?(?:核心流程|输入输出关系|关键模块|方法流程|实验概览)"), "Figure caption must not include generic `用于说明...` filler."),
    (re.compile(r"核心流程、输入输出关系和关键模块"), "Figure caption must not include generic process/module filler."),
    (re.compile(r"原始\s*caption\s*已在图中保留", re.I), "Do not use retained-original-caption prose instead of translating the caption."),
    (re.compile(r"便于回溯核验"), "Figure caption must not add empty verification prose."),
    (re.compile(r"该图来自官方论文\s*PDF\s*裁图"), "Use a short source tag such as `来源：PDF 截图`, not verbose PDF-crop prose."),
    (re.compile(r"完整翻译原始\s*caption|这里应放原始\s*caption", re.I), "Replace caption-template text with the complete Chinese translation of the official caption."),
]
ALLOWED_SOURCE_LABEL_RE = re.compile(
    r"(?:来源|源于)\s*[:：]?\s*(?:用户截图|HTML|html|MinerU\s*PDF\s*截图|mineru\s*的?\s*pdf\s*截图|PDF\s*截图|pdf\s*截图)",
    re.I,
)
SOURCE_LABEL_RE = re.compile(r"(?:来源|源于)\s*[:：]?", re.I)
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
SIMULATION_CONTEXT_RE = re.compile(
    r"\b("
    r"mujoco|isaac(?:\s+gym|\s+sim)?|pybullet|bullet|gazebo|habitat|ai2-thor|"
    r"carla|sapien|airsim|unity|unreal|blender|omniverse|"
    r"clo3d|marvelous\s+designer|"
    r"simulator|simulation\s+environment|simulated\s+environment|synthetic\s+data(?:set)?|"
    r"physics\s+engine|game\s+engine|robotics\s+environment|cloth\s+simulator"
    r")\b|仿真器|仿真环境|模拟器|合成数据|物理引擎|游戏引擎|机器人环境|布料仿真",
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


def check_dataset_line(dataset_line: str, card: str, issue) -> None:
    card_context = card.replace(dataset_line, "")
    if re.search(r"\bbase(?:\s+model)?\s*[:：]", dataset_line, flags=re.I) and not re.search(r"\|\s*Base\s*[:：]", dataset_line, flags=re.I):
        issue("base_format", "Base-model metadata must be appended on the Dataset line as `| Base:`, not as a loose `Base:` field.")
    if re.search(r"simluation\s*[:：]", dataset_line, flags=re.I):
        issue("simulation_spelling", "Use `Simulation:` in the Dataset metadata line, not `Simluation:`.")
    if re.search(r"simulation\s*[:：]", dataset_line, flags=re.I) and not re.search(r"\|\s*Simulation\s*[:：]", dataset_line):
        issue("simulation_format", "Simulation metadata must be appended as `| Simulation:` on the Dataset line.")
    entries = dataset_entries(dataset_line)
    dataset_value = re.sub(r"^Dataset:\s*", "", dataset_line, flags=re.I)
    dataset_part = re.split(r"\s*\|\s*(?:Base|Simulation)\s*[:：]", dataset_value, maxsplit=1, flags=re.I)[0].strip()
    if dataset_part.lower() not in STATUS_VALUES and re.search(r"｜|、|，|;|；|\s/\s", dataset_part):
        issue("dataset_separator", "Separate Dataset metadata names with ASCII comma plus space, e.g. `Dataset: H3.6M, 3DPW, SURREAL`; put extra datasets in `实现`.")
    if len(entries) > 3:
        issue("dataset_too_many", "Dataset metadata must list at most three visible dataset names; put additional datasets in `实现` if needed.")
    base_value = metadata_component(dataset_line, "Base")
    if base_value is not None:
        if base_value.lower() not in STATUS_VALUES and re.search(r"｜|、|，|;|；|\s/\s", base_value):
            issue("base_separator", "Separate Base metadata names with ASCII comma plus space, e.g. `| Base: FLUX.1-dev, HunyuanVideo`; put extra base-model details in `实现`.")
        if len(comma_entries(base_value)) > 3:
            issue("base_too_many", "Base metadata must list at most three visible base model names; put additional base-model chains or variants in `实现`.")
    if BASE_MODEL_HINTS_RE.search(card) and not re.search(r"\|\s*Base\s*[:：]", dataset_line):
        issue("base_model_missing", "Card mentions a known open-source/pretrained base model; Dataset metadata should include `| Base:` or explicitly mark `Base: 未报告` when the base is involved but not reported.")
    simulation_value = metadata_component(dataset_line, "Simulation")
    if simulation_value is not None and simulation_value.lower() in STATUS_VALUES and not SIMULATION_CONTEXT_RE.search(card_context):
        issue("simulation_not_relevant", "`Simulation:` is a conditional field. Do not write `Simulation: 未报告` / `N/A` / `不适用` when the paper does not clearly involve simulation; omit the field entirely.")
    if SIMULATION_CONTEXT_RE.search(card_context) and not re.search(r"\|\s*Simulation\s*[:：]", dataset_line):
        issue("simulation_missing", "Card mentions a known simulator/environment; Dataset metadata should include `| Simulation:` or explicitly mark `Simulation: 未报告`.")


def check_draft_status_markers(text: str, issue) -> None:
    for pattern, message in DRAFT_STATUS_PATTERNS:
        if pattern.search(text):
            issue("draft_status_forbidden", message)


def check_caption_quality(text: str, issue) -> None:
    if not text.strip():
        return
    for pattern, message in BAD_CAPTION_FILLER_PATTERNS:
        if pattern.search(text):
            issue("caption_filler_forbidden", message)
    if SOURCE_LABEL_RE.search(text) and not ALLOWED_SOURCE_LABEL_RE.search(text):
        issue("caption_source_label", "Caption source must use a short controlled label: `来源：用户截图`, `来源：HTML`, `来源：MinerU PDF 截图`, or `来源：PDF 截图`.")


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

    check_draft_status_markers(card, issue)

    for bullet in REQUIRED_BULLETS:
        if not re.search(rf"^\s*[-*]\s+{re.escape(bullet)}\s*[:：]", card, flags=re.M):
            issue("required_bullet", f"Missing fixed bullet slot `{bullet}`.")

    if re.search(r"^\s*[-*]\s+边界\s*/\s*启发\s*[:：]", card, flags=re.M):
        issue("legacy_bullet", "Use separate `局限` and `启发` bullet slots instead of the legacy combined `边界 / 启发` slot.")

    limitation_match = re.search(r"^\s*[-*]\s+局限\s*[:：](.*?)(?=^\s*[-*]\s+(?:定义|问题|方法|实现|结论|启发)\s*[:：]|\Z)", card, flags=re.M | re.S)
    if limitation_match:
        limitation_text = limitation_match.group(1).strip()
        if not limitation_text:
            issue("limitation_empty", "`局限` should state author-reported limitations, `作者未明确报告局限`, or verified `未报告` after checking the official source.")
        elif not re.search(r"作者|未报告|未明确报告|Not reported|N/A", limitation_text, flags=re.I):
            issue("limitation_source_marker", "`局限` should distinguish author-reported limitations from agent analysis, or explicitly state `作者未明确报告局限` / verified `未报告`.")

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

    for line in card.splitlines():
        stripped = line.strip()
        if stripped.startswith("图 ") and "图注" in stripped:
            check_caption_quality(stripped, issue)

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
