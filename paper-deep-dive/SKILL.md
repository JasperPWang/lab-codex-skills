---
name: paper-deep-dive
description: Use to turn a research paper PDF or extracted Markdown into a Feishu-first deep reading packet with source extraction, English original manuscript, complete faithful Chinese translation, Chinese close-reading notes, paper card, figures/assets, and sync-ready outputs.
---

# Paper Deep Dive

Short description: PDF to deep paper notes workflow. Source: Feishu wiki AI Research Skills.

Use this skill when the user wants a complete paper reading workflow from PDF to stable notes, paper card, assets, and shareable summaries.

## Canonical Paper Card Gate

When this workflow creates or modifies a paper card, also use [`paper-card-delivery`](../paper-card-delivery/SKILL.md). That skill is the canonical standard for official-source verification, fixed card format, figure/caption selection, and structural validation. Do not finalize the card from this deep-dive skill alone.

## Canonical Chinese Technical Writing Gate

For `原文译稿`, `完整中文译稿`, `中文精读稿`, Chinese figure captions, parent-page summaries, and Chinese paper-card prose, also use [`chinese-technical-writing`](../chinese-technical-writing/SKILL.md). Preserve official English source text in `英文原文稿`, formulas, method/model/dataset names, and symbols, but do not leave ordinary technical concepts as raw English phrase islands in Chinese prose.

## Borrowed Method Layer

This is the user's Feishu-native deep-dive workflow. It may borrow useful reading
methods from downloaded skills, but those skills do not own the final output
format.

- From `nature-reader`, borrow the source-map-first method: build stable source
  block IDs such as `S001`, `F001`, `T001`, preserve original / Chinese
  correspondence, keep figure/table captions attached to the relevant text, and
  record uncertainty instead of guessing.
- Do not publish the external `nature-reader` artifact contract as-is. Do not
  replace the required Feishu hierarchy with `paper.md`, `source_map.json`,
  `translation_notes.md`, or an English/Chinese Markdown reader unless the user
  explicitly asks for a local Markdown artifact.
- Use the source map as an internal scaffold for `英文原文稿`, `原文译稿`, and
  source-grounded `中文精读稿`. The final Feishu deliverable must still follow the
  parent-plus-three-child structure below and must use native Feishu images,
  captions, formulas, and fetch-back verification through `feishu-doc-workflow`.
- In `中文精读稿`, short bilingual source snippets or block IDs may be included
  when they clarify a key claim, equation, or figure, but the page remains an
  analytical Chinese close-reading guide rather than a second full translation.

## When To Use

- Reading a new paper deeply rather than only summarizing it.
- Converting PDF extraction into English original manuscript, complete Chinese translation, Chinese close-reading notes, and a paper card.
- Preparing Obsidian or Feishu paper pages.
- Auditing whether figures, claims, assets, and citations are complete.

If the user says `deep dive`, `深读`, `详细解析`, `dive into`, or asks to deeply read a single paper, use this full workflow by default. Do not downgrade it to a quick summary, paper card only, or close-reading note only unless the user explicitly asks for a lighter output.

## Workflow

1. Capture source metadata: title, authors, year, venue, DOI/arXiv, URL, local PDF path, and extraction date.
2. Extract the paper to inspectable Markdown when tooling is available; preserve figure references and equation context. On this machine, use MinerU as the default PDF-to-Markdown path before building Feishu deep-dive pages.
3. Check the MinerU conversion draft against official HTML when available, especially arXiv HTML for arXiv papers. Repair section order, paragraph continuity, formulas, figures, tables, captions, appendices, body citations, and references before publishing.
4. Build a source map inspired by `nature-reader`: stable block IDs for body text, figures, tables, captions, equations, appendices, and references; page / section location; extraction confidence; and links between first figure/table mention and the visual asset.
5. Create the English original manuscript (`英文原文稿`) from the verified official paper source. This means the paper's original English text in source order, not a structural outline, not selected excerpts, and not an English summary. It is used as the source for Chinese translation and may be deleted after the translation is complete if the user wants.
6. Create the complete faithful Chinese translation (`原文译稿` / `完整中文译稿`) from the verified English manuscript in source order. It must preserve section hierarchy, paragraph correspondence, formulas, figure/table positions, citations, captions, references, and layout structure as much as the target editor allows.
7. Check terminology in the Chinese translation. Technical terms should be translated accurately; important terms and proper nouns should appear as `中文（English term）` on first use or where clarity is needed. Avoid leaving large runs of English technical terms untranslated in Chinese prose.
8. Create the Chinese close-reading notes (`中文精读稿`) with problem, motivation, method, experiments, results, limitations, next questions, and research implications. This is interpretation and learning material; do not present it as the complete translation. Ground important analysis in source-map block IDs or short bilingual snippets when useful.
9. Create a paper card using [`paper-card-delivery`](../paper-card-delivery/SKILL.md), then run its validator on the Markdown draft when a local draft exists.
10. Store figures and assets in a stable assets folder.
11. Mark source says, inference, citation needed, and unresolved questions separately.

Paper-card content standards live in [`paper-card-delivery`](../paper-card-delivery/SKILL.md). This deep-dive skill must not duplicate or override paper-card source verification, metadata, image/caption selection, fixed bullet slots, sorting, or structural validation.

## Local MinerU Extraction

For future deep dives, first create a MinerU conversion draft when a PDF is available. Use it as the source-order manuscript scaffold for `英文原文稿`, `原文译稿`, and `中文精读稿`.

- Preferred wrapper in this vault: `$WORLD_MODEL_VAULT/.tools/mineru-md.sh`
- MinerU binary on this machine: `$WORLD_MODEL_VAULT_MINERU_BIN`
- Verified local version: `mineru 3.3.1`
- Store MinerU outputs, downloaded PDFs, arXiv HTML, and temporary figure assets under `.tools/tmp/codex/<task-slug>/`; delete them after the Feishu pages are written and fetched back successfully.
- MinerU is a conversion draft, not the authoritative final text. For arXiv papers, always check the MinerU draft against arXiv HTML when available before publishing Feishu pages. Verify section order, paragraph continuity, equations, figures, captions, tables, appendices, citations, and references. If arXiv HTML is unavailable or incomplete, use official LaTeX source, publisher HTML, or the official PDF as the authority.
- If MinerU misses or corrupts formulas, figures, captions, appendices, or references, repair from official arXiv HTML/LaTeX/PDF or the official publisher source before marking the deep dive complete.

## Manuscript Fidelity Requirements

- `英文原文稿` and `原文译稿` must preserve paper-like citation flow. Body citation markers must remain where they appear in the source, using the source style when feasible, such as `[12]`, `[Author et al., 2025]`, or `(Author et al., 2025)`.
- The References section must be a numbered bibliography, not a bullet list. Use Markdown ordered lists or Feishu numbered-list blocks, and preserve enough bibliographic detail for each item to be identifiable.
- Figures and tables must be placed near their original reference/caption positions. Use native Feishu image blocks for figures when reliable official image assets are available.
- Formulas must be checked against official HTML/LaTeX/PDF and preserved in LaTeX where possible. This includes inline formulas, not only displayed equations. Do not publish pages where important equations, inline variables, losses, or symbolic expressions have collapsed into prose or lost subscripts/superscripts.
- The complete Chinese manuscript follows the same fidelity requirements as the English original manuscript: original section order, paragraph correspondence, figure/table positions, formula placement, body citations, numbered references, captions, appendices, and table structure.
- Chinese terminology must be deliberate. Translate technical terms into accurate Chinese, keep method/model/dataset names and symbols unchanged when they are names, and write important terms as `中文（English term）` when first introduced. Do not leave dense English terminology untranslated in ordinary Chinese explanatory prose.

## Formula / Equation Handling

For paper deep dives and complete manuscript pages, formulas are source-fidelity content, not prose to paraphrase.

- Extract formulas from the official full-paper source before writing. For arXiv papers, prefer arXiv HTML / LaTeX source because it usually preserves MathML, TeX annotations, equation IDs, and numbering; use the PDF or a structured PDF parser only as fallback. Do not reconstruct formulas from collapsed Feishu plain text or OCR text when the official formula source is available.
- Preserve inline formulas as carefully as displayed equations. Inline variables, operators, compact expressions, losses, references such as `Eq. (4)`, and symbolic phrases such as `$S$`, `$G$`, `$l(S)$`, `$\bm{x}^{n}$`, or `$\mathcal{L}_{\text{RGB}}$` must stay in inline LaTeX, not ordinary text, translated prose, or backticks.
- During translation, protect inline and displayed formulas with non-translatable placeholders, translate surrounding prose only, then restore the exact TeX from the official source. Do not let machine translation translate variable names, LaTeX commands, `\text{...}` labels, Greek letters, superscripts, subscripts, hats, dots, norms, fractions, sums, products, matrices, or equation tags.
- In Markdown sources for Feishu import, use `$...$` for inline math and `$$...$$` for displayed equations. Keep displayed equations on their own lines with blank lines before and after. Do not wrap formulas in code fences or backticks unless explicitly creating a raw-LaTeX fallback section.
- Preserve equation numbering. Prefer `\tag{n}` inside displayed equations when Feishu renders it correctly; otherwise place a separate plain-text number like `(n)` immediately after the displayed equation. Keep references such as `式 (4)` aligned with the original paper.
- After writing, fetch the Feishu page and verify formula fidelity. Check both inline and displayed formulas: count `<latex>` / `$...$` blocks when possible, inspect samples from early, middle, appendix, and formula-heavy sections, and confirm formulas did not degrade into text such as `L_render = lambda ||...`, lose `_` / `^`, merge with surrounding prose, or become translated words.
- If Feishu Markdown cannot render a formula reliably, keep the exact LaTeX source in a labeled `公式 LaTeX 源` paragraph or block and, for important equations, insert a rendered equation image with a Chinese caption. Mark this as a rendering fallback, not as the preferred final form.

## Output

For Feishu deliverables, use this fixed hierarchy by default:

- Parent page: paper card and summary only. Include metadata, source-verified pipeline / process / computation-flow figure(s), one-sentence conclusion, core problem, method/pipeline summary, experiments, limitations, and implications.
- Child page 1: `英文原文稿`, the complete original English manuscript from official PDF/HTML/LaTeX/MinerU extraction. It is a temporary translation source and can be deleted after translation if the user requests cleanup.
- Child page 2: `原文译稿`, the complete faithful Chinese translation.
- Child page 3: `中文精读稿`, the Chinese close-reading / learning notes.

Do not replace these three child pages with an `English Structured Reader`, outline, section summary, or mixed translation/interpretation page.

Use:

- `Paper Metadata`
- `Extraction Result`
- `English Original Manuscript`
- `Faithful Chinese Translation`
- `Chinese Close Reading Notes`
- `Paper Card`
- `Assets`
- `Open Questions`
- `Sync Checklist`

## Guardrails

- Do not fabricate paper content when extraction is incomplete.
- Do not merge translation, interpretation, and speculation without labels.
- Do not call a page `英文原文稿` unless it contains the original English paper text in source order.
- Do not call a page `原文译稿` or `完整中文稿` unless it is a complete, faithful translation of the source paper rather than a close-reading note.
- Do not call `中文精读稿` a complete translation; it is learning-oriented interpretation.
- Do not cite figures or equations that were not actually extracted or inspected.
- Do not present a paper card as finished unless its problem, method, implementation, conclusion, limitations, and figure claims are grounded in the official full paper; use `Not reported`, `N/A`, or `待核验` instead of guessing.
