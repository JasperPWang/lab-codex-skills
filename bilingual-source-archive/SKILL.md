---
name: bilingual-source-archive
description: Canonical platform-neutral source archive workflow for web articles, essays, research-method posts, pasted source text, browser/Obsidian web-clipper captures, and similar non-paper sources delivered to Feishu/Lark, Notion, or Obsidian/Markdown when the user asks for 原文, 提取原文, 英文原文和中文译文, English original plus Chinese translation, bilingual source archive, or says not to summarize. Use especially when another workflow would otherwise summarize or distill the source.
---

# Bilingual Source Archive

## Core Contract

This skill preserves source text. It is not a summary, AI note, interpretation, or clipping digest.

Default output is a durable page or Markdown note on the user-selected platform containing the actual source text in original order plus a faithful Chinese translation. If the source is English, write each meaningful English block followed by its Chinese translation. If the source is already Chinese or mixed-language, preserve the original and translate only the non-Chinese portions that need translation.

Use [`research-doc-workflow`](../research-doc-workflow/SKILL.md) and the matching platform adapter (`feishu-doc-workflow`, `notion-doc-workflow`, or `obsidian-doc-workflow`) to choose and verify Feishu, Notion, or Obsidian delivery. Resolve the destination from the user's URL or explicit instruction; do not silently default to Feishu.

For Chinese translation blocks and any Chinese metadata/provenance notes, also use [`chinese-technical-writing`](../chinese-technical-writing/SKILL.md). Preserve English source blocks exactly; apply the Chinese-first terminology rule only to the Chinese translation or Chinese notes.

## Trigger Rules

Use this skill when the user says any of the following or equivalent:

- `提取原文`, `原文`, `原文的英文和中文译文`, `英文原文与中文译文`.
- `不要总结`, `不要乱总结`, `不是二次解读`, `我要原文`.
- The user provides a research-method article, Substack, X/Twitter long post/thread, pasted web-clipper text, Atlas capture, or Obsidian Web Clipper note and asks to preserve it in a research knowledge system.

Do not use an AI-summary skill for these requests unless the user explicitly asks for a separate summary.

## Source Acquisition

Prefer source text in this order:

1. User-provided attachment or pasted text.
2. Existing Feishu, Notion, or Obsidian page/note when the user supplies a durable target to normalize.
3. Atlas / Obsidian Web Clipper capture when the user says the browser capture exists.
4. Public source URL or official archive page.

If only a short excerpt is available, do not pretend it is the full article. Label the page or working note as `原文不完整 / 待补全文` and preserve the available source exactly.

Respect access boundaries. Do not bypass paywalls or private access. If the source text is not accessible and not supplied by the user, explain what is missing and create only a partial page if the user wants.

## Destination Placement

Preserve the platform of an existing target. For a new archive, follow `research-doc-workflow`: resolve Feishu / Notion / Obsidian from the user's URL or explicit instruction; if none is given, ask one concise destination question instead of silently choosing a platform.

If the user supplies an existing page/note, update that target. Otherwise create the archive under the most relevant existing hub, database, folder, or MOC for the chosen platform. For research-method articles used in the operating-review workflow, use that platform's review hub when appropriate:

- `科研经营复盘｜Daily Research Operating Review`

Use this title pattern unless the user gives a title:

```text
<Source Title>｜英文原文与中文译文
```

After writing, re-fetch or re-read the durable artifact and verify title, parent/hierarchy, properties/frontmatter, and visible content.

## Formatting Contract

Do:

- Preserve source order.
- Keep headings, lists, block quotes, and paragraph breaks when possible.
- Translate faithfully into Chinese, with technical terms handled as `中文（English term）` when useful.
- Keep URLs, author/date/source metadata only when they help provenance.
- Use concise Chinese punctuation and readable paragraphs.

Do not:

- Add `Original`, `译文`, `原文`, `Translation`, or similar repeated labels/headings before every block.
- Put an AI summary before the source text.
- Replace the source with thematic notes, takeaways, or a method explanation.
- Redirect the content to another platform when the user supplied a target.
- Leave syntax from a different platform, absolute local paths, iframe embeds, raw web-clipper boilerplate, or `图像： EW_IMG...` labels in reader-facing content. Obsidian frontmatter and `![[...]]` are allowed only in an Obsidian target.

Accepted default layout:

```markdown
# <Source Title>｜英文原文与中文译文

Source metadata line if useful.

English heading or paragraph.

对应中文译文。

Next English paragraph.

对应中文译文。
```

This layout intentionally has no `Original` / `译文` field labels.

## Verification Checklist

Before finishing:

- The durable artifact is on the selected platform; new documents did not silently default to Feishu.
- The page contains actual source text, not only a summary.
- English source blocks and Chinese translation blocks appear in source order.
- No repeated `Original` / `译文` labels remain.
- No cross-platform or web-clipper residue remains in reader-facing text.
- If the source is partial, the limitation is explicit.
- Re-fetch or re-read the destination and verify title, parent/hierarchy, and content presence.

## Validation Script

For Markdown drafts, run:

```bash
python .tools/skills/bilingual-source-archive/scripts/validate_bilingual_source.py path/to/draft.md --target obsidian
```

Set `--target` to `feishu`, `notion`, `obsidian`, or `markdown`. The script checks forbidden labels, summary-first headings, cross-platform residue, and a rough English/Chinese presence balance. It cannot prove source completeness; the agent must still state what source text was available.
