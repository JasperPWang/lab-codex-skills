#!/usr/bin/env python3
"""Standard-library skill validator for shared bundles.

This intentionally checks only the portable invariants needed before publishing:
frontmatter exists, `name` and `description` are present, and the name is valid.
It avoids requiring PyYAML on lab machines.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


NAME_RE = re.compile(r"^[a-z0-9-]{1,64}$")


def extract_frontmatter(text: str) -> str:
    if not text.startswith("---\n"):
        raise ValueError("missing YAML frontmatter")
    end = text.find("\n---", 4)
    if end < 0:
        raise ValueError("unterminated YAML frontmatter")
    return text[4:end]


def scalar_key_exists(frontmatter: str, key: str) -> bool:
    return re.search(rf"(?m)^{re.escape(key)}\s*:\s*(.+)?$", frontmatter) is not None


def parse_name(frontmatter: str) -> str:
    match = re.search(r"(?m)^name\s*:\s*(.+)$", frontmatter)
    if not match:
        raise ValueError("missing name")
    value = match.group(1).strip().strip('"').strip("'")
    if not NAME_RE.match(value) or value.startswith("-") or value.endswith("-") or "--" in value:
        raise ValueError(f"invalid skill name: {value!r}")
    return value


def validate_skill(skill_dir: Path) -> None:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        raise ValueError("SKILL.md not found")
    frontmatter = extract_frontmatter(skill_md.read_text(encoding="utf-8"))
    parse_name(frontmatter)
    if not scalar_key_exists(frontmatter, "description"):
        raise ValueError("missing description")


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: simple-validate-skills.py <skill-root>", file=sys.stderr)
        return 2

    root = Path(argv[1])
    count = 0
    failures: list[str] = []
    for skill_md in sorted(root.glob("*/SKILL.md")):
        skill_dir = skill_md.parent
        try:
            validate_skill(skill_dir)
            count += 1
        except Exception as exc:  # noqa: BLE001 - report every validation issue.
            failures.append(f"{skill_dir.name}: {exc}")

    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1

    print(f"validated skills: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

