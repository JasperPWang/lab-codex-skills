#!/usr/bin/env python3
"""Lint Chinese technical prose for avoidable English phrase islands."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


CJK_RE = re.compile(r"[\u3400-\u9fff]")
FENCE_RE = re.compile(r"```.*?```", flags=re.S)

TRANSLATABLE_TERMS = {
    "parametric human estimation": "参数化人体估计",
    "perspective distortion": "透视畸变/透视失真",
    "scene geometry": "场景几何",
    "camera pose": "相机位姿",
    "body pose": "人体姿态",
    "human pose": "人体姿态",
    "mesh reconstruction": "网格重建",
    "3d human reconstruction": "三维人体重建",
    "3d human pose estimation": "三维人体姿态估计",
    "motion-dependent cloth dynamics": "运动相关布料动力学",
    "physically plausible deformation": "物理合理形变",
    "simulation-ready asset": "仿真就绪资产",
    "ablation study": "消融实验",
}


def strip_fenced_code(text: str) -> str:
    return FENCE_RE.sub("", text)


def check_text(text: str) -> list[dict[str, object]]:
    issues: list[dict[str, object]] = []
    text = strip_fenced_code(text)
    for line_no, line in enumerate(text.splitlines(), 1):
        if not CJK_RE.search(line):
            continue
        lowered = line.lower()
        for term, chinese in TRANSLATABLE_TERMS.items():
            if term in lowered:
                gloss_pattern = rf"[（(]\s*{re.escape(term)}\s*[）)]"
                if re.search(gloss_pattern, lowered):
                    continue
                issues.append(
                    {
                        "line": line_no,
                        "code": "language_mixing",
                        "term": term,
                        "suggested": chinese,
                        "message": f"Use Chinese-first wording for `{term}` -> `{chinese}`.",
                    }
                )
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Chinese-first technical prose.")
    parser.add_argument("path", nargs="?", help="Text/Markdown file. Reads stdin if omitted or `-`.")
    args = parser.parse_args()

    if not args.path or args.path == "-":
        text = sys.stdin.read()
    else:
        text = Path(args.path).read_text(encoding="utf-8")

    issues = check_text(text)
    result = {"issues": len(issues), "details": issues}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
