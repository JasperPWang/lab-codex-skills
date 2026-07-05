---
name: bilingual-source-archive
description: Canonical Feishu-first source archive workflow for web articles, essays, research-method posts, pasted source text, Atlas/Obsidian web-clipper captures, and similar non-paper sources when the user asks for 原文, 提取原文, 英文原文和中文译文, English original plus Chinese translation, bilingual source archive, or says not to summarize. Use especially when another skill such as feishu-doc-workflow, obsidian-clipping-ai-summary, daily-research-review, or llm-wiki would otherwise summarize or distill the source.
---

# Bilingual Source Archive

## Core Contract

This skill preserves source text. It is not a summary, AI note, interpretation, or clipping digest.

Default output is a Feishu page containing the actual source text in original order plus a faithful Chinese translation. If the source is English, write each meaningful English block followed by its Chinese translation. If the source is already Chinese or mixed-language, preserve the original and translate only the non-Chinese portions that need translation.

When the target is Feishu, also use `feishu-doc-workflow` for hierarchy, `lark-cli` writes, native document safety, and fetch-back verification.

For Chinese translation blocks and any Chinese metadata/provenance notes, also use [`chinese-technical-writing`](../chinese-technical-writing/SKILL.md). Preserve English source blocks exactly; apply the Chinese-first terminology rule only to the Chinese translation or Chinese notes.

## Trigger Rules

Use this skill when the user says any of the following or equivalent:

- `提取原文`, `原文`, `原文的英文和中文译文`, `英文原文与中文译文`.
- `不要总结`, `不要乱总结`, `不是二次解读`, `我要原文`.
- The user provides a research-method article, Substack, X/Twitter long post/thread, pasted web-clipper text, Atlas capture, or Obsidian Web Clipper note and asks to put it into Feishu.

Do not use an AI-summary skill for these requests unless the user explicitly asks for a separate summary.

## Source Acquisition

Prefer source text in this order:

1. User-provided attachment or pasted text.
2. Existing Feishu page if the user gives a Feishu URL to normalize.
3. Atlas / Obsidian Web Clipper capture when the user says the browser capture exists.
4. Public source URL or official archive page.

If only a short excerpt is available, do not pretend it is the full article. Label the page or working note as `原文不完整 / 待补全文` and preserve the available source exactly.

Respect access boundaries. Do not bypass paywalls or private access. If the source text is not accessible and not supplied by the user, explain what is missing and create only a partial page if the user wants.

## Feishu Placement

Default to Feishu first for research-method source materials unless the user explicitly asks for Obsidian/local vault first.

If the user supplies an existing Feishu page, update that page. Otherwise create a new Feishu page under the most relevant existing hub. For research-method articles used in the user's operating-review workflow, use the review hub when appropriate:

- `科研经营复盘｜Daily Research Operating Review`

Use this title pattern unless the user gives a title:

```text
<Source Title>｜英文原文与中文译文
```

After writing, fetch the page back and verify title, parent/hierarchy, and visible content.

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
- Move the content into Obsidian first when the user asked for Feishu first.
- Leave Obsidian residue such as frontmatter fences, `![[...]]`, local paths, iframe embeds, raw web-clipper boilerplate, or `图像： EW_IMG...` labels.

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

- The page is Feishu-first unless the user requested another destination.
- The page contains actual source text, not only a summary.
- English source blocks and Chinese translation blocks appear in source order.
- No repeated `Original` / `译文` labels remain.
- No Obsidian/web-clipper residue remains in reader-facing text.
- If the source is partial, the limitation is explicit.
- For Feishu writes, fetch back and verify title, parent, and content presence.

## Validation Script

For Markdown drafts, run:

```bash
python .tools/skills/bilingual-source-archive/scripts/validate_bilingual_source.py path/to/draft.md
```

The script checks for forbidden labels, summary-first headings, Obsidian residue, and a rough English/Chinese presence balance. It cannot prove source completeness; the agent must still state what source text was available.
