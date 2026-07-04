#!/usr/bin/env python3
"""Small deterministic helpers for a Codex-native LLM Wiki Skill."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path
from typing import Any


WIKI_DIRS = [
    "wiki/entities",
    "wiki/concepts",
    "wiki/sources",
    "wiki/claims",
    "wiki/questions",
    "wiki/queries",
    "wiki/synthesis",
    "wiki/comparisons",
    "raw/sources",
    "raw/assets",
    ".llm-wiki",
]

TEXT_EXTS = {
    ".md",
    ".txt",
    ".csv",
    ".tsv",
    ".json",
    ".yaml",
    ".yml",
    ".html",
    ".xml",
    ".rst",
    ".tex",
}

STOPWORDS = {
    "the",
    "and",
    "for",
    "with",
    "that",
    "this",
    "from",
    "are",
    "was",
    "were",
    "have",
    "has",
    "what",
    "why",
    "how",
    "一个",
    "这个",
    "我们",
    "它们",
    "以及",
    "但是",
    "因为",
}


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def today() -> str:
    return date.today().isoformat()


def ensure_file(path: Path, text: str) -> None:
    if not path.exists():
        path.write_text(text, encoding="utf-8")


def init_project(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    for d in WIKI_DIRS:
        (root / d).mkdir(parents=True, exist_ok=True)

    ensure_file(
        root / "purpose.md",
        "# Purpose\n\nDefine the goal, scope, key questions, and evolving thesis of this wiki.\n",
    )
    ensure_file(
        root / "schema.md",
        "# Schema\n\nThis is a custom LLM Wiki maintained by Codex.\n\n"
        "## Rules\n\n"
        "- Raw sources in `raw/sources/` are immutable.\n"
        "- Generated pages live under `wiki/` and use YAML frontmatter.\n"
        "- Use Obsidian `[[wikilinks]]` for cross-references.\n"
        "- Update `wiki/index.md`, `wiki/overview.md`, and `wiki/log.md` after each ingest.\n",
    )
    ensure_file(
        root / "wiki/index.md",
        f"---\ntitle: \"Index\"\ntype: \"index\"\nstatus: \"stable\"\ncreated: \"{today()}\"\nupdated: \"{today()}\"\nsources: []\ntags: []\n---\n\n# Index\n\n",
    )
    ensure_file(
        root / "wiki/overview.md",
        f"---\ntitle: \"Overview\"\ntype: \"overview\"\nstatus: \"draft\"\ncreated: \"{today()}\"\nupdated: \"{today()}\"\nsources: []\ntags: []\n---\n\n# Overview\n\n",
    )
    ensure_file(root / "wiki/log.md", "# Log\n\n")
    ensure_file(root / "wiki/reviews.md", "# Review Queue\n\n")
    ensure_file(root / "wiki/research.md", "# Research Queue\n\n")
    ensure_file(root / ".llm-wiki/queue.json", "[]\n")
    manifest(root)
    print(f"Initialized LLM Wiki at {root}")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def source_files(root: Path) -> list[Path]:
    base = root / "raw/sources"
    if not base.exists():
        return []
    return sorted(p for p in base.rglob("*") if p.is_file() and not p.name.startswith("."))


def manifest(root: Path) -> None:
    path = root / ".llm-wiki/manifest.json"
    old = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    old_sources = old.get("sources", {})
    new_sources: dict[str, Any] = {}
    added: list[str] = []
    modified: list[str] = []

    for p in source_files(root):
        rp = rel(p, root)
        digest = sha256(p)
        stat = p.stat()
        item = {
            "sha256": digest,
            "size": stat.st_size,
            "mtime": int(stat.st_mtime),
            "status": old_sources.get(rp, {}).get("status", "new"),
            "last_ingested": old_sources.get(rp, {}).get("last_ingested"),
        }
        if rp not in old_sources:
            added.append(rp)
        elif old_sources[rp].get("sha256") != digest:
            modified.append(rp)
            item["status"] = "modified"
        new_sources[rp] = item

    deleted = sorted(set(old_sources) - set(new_sources))
    data = {
        "updated": datetime.now().isoformat(timespec="seconds"),
        "sources": new_sources,
        "changes": {"added": added, "modified": modified, "deleted": deleted},
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(data["changes"], ensure_ascii=False, indent=2))


FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")


def wiki_pages(root: Path) -> list[Path]:
    base = root / "wiki"
    if not base.exists():
        return []
    return sorted(p for p in base.rglob("*.md") if p.is_file())


def slug_to_stems(root: Path) -> dict[str, list[str]]:
    out: dict[str, list[str]] = defaultdict(list)
    for p in wiki_pages(root):
        stem = p.stem
        out[stem].append(rel(p, root))
        out[stem.lower()].append(rel(p, root))
    return out


def parse_frontmatter(text: str) -> dict[str, Any]:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    fm: dict[str, Any] = {}
    current: str | None = None
    for raw in m.group(1).splitlines():
        line = raw.rstrip()
        if not line.strip():
            continue
        if line.startswith("  - ") and current:
            fm.setdefault(current, []).append(line[4:].strip().strip('"'))
            continue
        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip()
            if val == "[]":
                fm[key] = []
            elif val == "":
                fm[key] = []
                current = key
            else:
                fm[key] = val.strip('"')
                current = key
    return fm


def page_record(root: Path, p: Path) -> dict[str, Any]:
    text = p.read_text(encoding="utf-8", errors="replace")
    fm = parse_frontmatter(text)
    return {
        "path": rel(p, root),
        "stem": p.stem,
        "title": fm.get("title", p.stem),
        "type": fm.get("type", "unknown"),
        "sources": fm.get("sources", []),
        "links": sorted(set(WIKILINK_RE.findall(text))),
        "text": text,
        "has_frontmatter": bool(fm),
    }


def tokenize(text: str) -> list[str]:
    lower = text.lower()
    latin = re.findall(r"[a-z0-9][a-z0-9_\-]{1,}", lower)
    cjk_chars = re.findall(r"[\u4e00-\u9fff]", text)
    cjk = ["".join(cjk_chars[i : i + 2]) for i in range(max(0, len(cjk_chars) - 1))]
    return [t for t in latin + cjk if t not in STOPWORDS]


def read_searchable(path: Path) -> str:
    if path.suffix.lower() not in TEXT_EXTS:
        return ""
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def search(root: Path, query: str, limit: int) -> None:
    qterms = tokenize(query)
    if not qterms:
        qterms = [query.lower()]
    results = []
    files = wiki_pages(root) + [p for p in source_files(root) if p.suffix.lower() in TEXT_EXTS]
    for p in files:
        text = read_searchable(p)
        if not text:
            continue
        hay = text.lower()
        counts = Counter(tokenize(text))
        score = 0.0
        for term in qterms:
            score += counts.get(term, 0)
            if term in p.stem.lower():
                score += 10
            if term in hay:
                score += 1
        if score:
            snippet = re.sub(r"\s+", " ", text[:500]).strip()
            results.append({"score": score, "path": rel(p, root), "snippet": snippet})
    results.sort(key=lambda x: (-x["score"], x["path"]))
    print(json.dumps(results[:limit], ensure_ascii=False, indent=2))


def build_graph(root: Path) -> dict[str, Any]:
    records = [page_record(root, p) for p in wiki_pages(root)]
    by_stem = slug_to_stems(root)
    nodes = {r["path"]: {k: r[k] for k in ("title", "type", "sources")} for r in records}
    path_by_stem = {r["stem"]: r["path"] for r in records}
    path_by_stem.update({r["stem"].lower(): r["path"] for r in records})

    neighbors: dict[str, set[str]] = defaultdict(set)
    edge_weights: dict[tuple[str, str], dict[str, float]] = defaultdict(lambda: defaultdict(float))

    def add_edge(a: str, b: str, signal: str, weight: float) -> None:
        if a == b:
            return
        x, y = sorted((a, b))
        neighbors[x].add(y)
        neighbors[y].add(x)
        edge_weights[(x, y)][signal] += weight

    for r in records:
        for link in r["links"]:
            targets = by_stem.get(link) or by_stem.get(link.lower()) or []
            if targets:
                add_edge(r["path"], targets[0], "direct", 3.0)

    for i, a in enumerate(records):
        for b in records[i + 1 :]:
            shared = set(a["sources"]) & set(b["sources"])
            if shared:
                add_edge(a["path"], b["path"], "source_overlap", 4.0 * len(shared))
            if a["type"] != "unknown" and a["type"] == b["type"]:
                add_edge(a["path"], b["path"], "type_affinity", 1.0)

    for i, a in enumerate(records):
        for b in records[i + 1 :]:
            common = neighbors[a["path"]] & neighbors[b["path"]]
            if common:
                score = sum(1.0 / max(1, len(neighbors[c])) for c in common)
                add_edge(a["path"], b["path"], "adamic_adar", round(1.5 * score, 4))

    seen: set[str] = set()
    communities = []
    for node in nodes:
        if node in seen:
            continue
        stack = [node]
        comp = []
        seen.add(node)
        while stack:
            cur = stack.pop()
            comp.append(cur)
            for nb in neighbors[cur]:
                if nb not in seen:
                    seen.add(nb)
                    stack.append(nb)
        possible = len(comp) * (len(comp) - 1) / 2
        actual = sum(1 for e in edge_weights if e[0] in comp and e[1] in comp)
        cohesion = actual / possible if possible else 0
        communities.append({"id": len(communities) + 1, "size": len(comp), "cohesion": round(cohesion, 3), "pages": sorted(comp)})

    edges = []
    for (a, b), signals in edge_weights.items():
        edges.append({"source": a, "target": b, "weight": round(sum(signals.values()), 4), "signals": dict(signals)})
    edges.sort(key=lambda e: (-e["weight"], e["source"], e["target"]))

    orphans = sorted([n for n in nodes if not neighbors[n]])
    bridges = sorted(
        [{"path": n, "degree": len(neighbors[n])} for n in nodes if len(neighbors[n]) >= 3],
        key=lambda x: (-x["degree"], x["path"]),
    )
    surprising = [
        e
        for e in edges
        if nodes[e["source"]]["type"] != nodes[e["target"]]["type"] and e["weight"] >= 3
    ][:20]

    return {
        "updated": datetime.now().isoformat(timespec="seconds"),
        "nodes": nodes,
        "edges": edges,
        "communities": communities,
        "insights": {"orphans": orphans, "bridges": bridges[:20], "surprising_links": surprising},
    }


def graph(root: Path) -> None:
    data = build_graph(root)
    out = root / ".llm-wiki/graph.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary = {
        "nodes": len(data["nodes"]),
        "edges": len(data["edges"]),
        "communities": len(data["communities"]),
        "orphans": len(data["insights"]["orphans"]),
        "bridges": len(data["insights"]["bridges"]),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


def lint(root: Path) -> None:
    records = [page_record(root, p) for p in wiki_pages(root)]
    stems = slug_to_stems(root)
    source_set = {rel(p, root) for p in source_files(root)}
    inbound: Counter[str] = Counter()
    issues = []

    for r in records:
        if not r["has_frontmatter"] and Path(r["path"]).name not in {"log.md", "reviews.md", "research.md"}:
            issues.append({"severity": "warn", "type": "missing_frontmatter", "path": r["path"]})
        for s in r["sources"]:
            if s and s not in source_set:
                issues.append({"severity": "warn", "type": "missing_source", "path": r["path"], "source": s})
        for link in r["links"]:
            targets = stems.get(link) or stems.get(link.lower())
            if not targets:
                issues.append({"severity": "error", "type": "broken_wikilink", "path": r["path"], "link": link})
            else:
                inbound[targets[0]] += 1

    for r in records:
        if r["type"] not in {"index", "overview"} and inbound[r["path"]] == 0 and not r["path"].endswith(("log.md", "reviews.md", "research.md")):
            issues.append({"severity": "info", "type": "no_inbound_links", "path": r["path"]})

    title_counts = Counter((r["title"] or "").lower() for r in records)
    for r in records:
        if r["title"] and title_counts[r["title"].lower()] > 1:
            issues.append({"severity": "info", "type": "duplicate_title", "path": r["path"], "title": r["title"]})

    data = {"updated": datetime.now().isoformat(timespec="seconds"), "issues": issues}
    out = root / ".llm-wiki/lint.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"issues": len(issues), "by_type": Counter(i["type"] for i in issues)}, ensure_ascii=False, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init", help="create a new LLM Wiki project")
    p_init.add_argument("project")

    p_manifest = sub.add_parser("manifest", help="hash raw/sources and report changes")
    p_manifest.add_argument("project")

    p_search = sub.add_parser("search", help="lexical search wiki and text sources")
    p_search.add_argument("project")
    p_search.add_argument("query")
    p_search.add_argument("--limit", type=int, default=10)

    p_graph = sub.add_parser("graph", help="build graph report")
    p_graph.add_argument("project")

    p_lint = sub.add_parser("lint", help="lint wiki structure and links")
    p_lint.add_argument("project")

    args = parser.parse_args()
    root = Path(args.project).expanduser().resolve()
    if args.cmd == "init":
        init_project(root)
    elif args.cmd == "manifest":
        manifest(root)
    elif args.cmd == "search":
        search(root, args.query, args.limit)
    elif args.cmd == "graph":
        graph(root)
    elif args.cmd == "lint":
        lint(root)


if __name__ == "__main__":
    main()
