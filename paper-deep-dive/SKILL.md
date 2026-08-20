---
name: paper-deep-dive
description: Canonical single-paper deep-dive delivery standard, with Notion as the durable target. Use whenever the user mentions deep dive, 深读, 详细解析, detailed-read, dive into a paper, full paper reading, English original manuscript, 原文中译稿, or asks to audit/repair a deep-dive package. Produces one Notion main entry containing the complete 原文中译稿, with two linked child artifacts for 英文原文稿 and source-order 精读稿; no other skill may relax or replace this delivery contract.
---

# Paper Deep Dive

Short description: PDF to deep paper notes workflow. Historical source: Feishu wiki AI Research Skills; current durable delivery is Notion-first.

Use this skill when the user wants a complete paper reading workflow from PDF to stable notes, paper card, assets, and shareable summaries.

## Single Source of Truth

This skill is the only canonical delivery standard for single-paper deep dives. Other skills may trigger, route, write to Feishu/Notion/Obsidian, preserve Chinese wording, or distill the finished deep dive into a wiki, but they must not define a second deep-dive structure or mark a package complete under weaker rules.

When any user request says `deep dive`, `深读`, `详细解析`, `detailed-read`, `dive into`, `精读这篇论文`, `英文原文稿`, or `原文中译稿`, treat it as this full workflow unless the user explicitly asks for a lighter artifact such as quick summary, paper card only, or partial translation. A lighter artifact must be labeled as such and must not be called a compliant deep dive.

The completion standard is product-level, not effort-level. A good summary or a partial translation is still incomplete. A package is compliant only when the main entry contains the complete Chinese manuscript, both linked child artifacts are complete, figures/captions, formulas, references, hierarchy, and target-platform read-back verification all pass the delivery gate below.

## Canonical Platform Delivery Gate

Also use [`research-doc-workflow`](../research-doc-workflow/SKILL.md) and [`notion-doc-workflow`](../notion-doc-workflow/SKILL.md) for new deep dives. Notion is the canonical durable target because Feishu storage is limited. Keep one Markdown-first manuscript and close-reading structure; only Notion hierarchy, native equations/captions, uploads, editable trees, citation chrome, and write verification need platform adaptation. Do not create or maintain a parallel Feishu deep-dive copy unless the user explicitly requests a legacy repair or migration.

## Canonical Paper Card Gate

When this workflow creates or modifies a paper card, also use [`paper-card-delivery`](../paper-card-delivery/SKILL.md). That skill is the canonical standard for official-source verification, fixed card format, figure/caption selection, and structural validation. Do not finalize the card from this deep-dive skill alone.

## Canonical Chinese Technical Writing Gate

For `原文中译稿`, `完整中文译稿`, `精读稿`, Chinese figure captions, Chinese table captions/notes, main-entry summaries, and Chinese paper-card prose, also use [`chinese-technical-writing`](../chinese-technical-writing/SKILL.md). Preserve official English source text in `英文原文稿`, formulas, named architectures/models/methods such as `Transformer` and `DINO`, dataset names, symbols, and table cell content. Translate generic technical concepts into Chinese, but do not translate official names or force them into awkward Chinese names.

## Borrowed Method Layer

This is the user's canonical deep-dive workflow. It may borrow useful reading methods from downloaded skills, but those skills do not own the final package semantics or target-platform representation.

- From `nature-reader`, borrow the source-map-first method: build stable source
  block IDs such as `S001`, `F001`, `T001`, preserve original / Chinese
  correspondence, keep figure/table captions attached to the relevant text, and
  record uncertainty instead of guessing.
- Do not publish the external `nature-reader` artifact contract as-is. A lone `paper.md`, `source_map.json`, `translation_notes.md`, or bilingual reader does not replace the required main entry plus two complete manuscript artifacts. These files may be intermediate material or part of an explicitly requested Obsidian package.
- Use the source map as an internal scaffold for `英文原文稿`, `原文中译稿`, and source-grounded `精读稿`. The final deliverable must still follow the main-translation-plus-two-child-artifact structure and use the selected platform's native images/captions, formulas, hierarchy, and read-back verification through `research-doc-workflow`.
- In the child-page `精读稿`, short bilingual source snippets or block IDs may
  be included when they clarify a key claim, equation, or figure, but the page
  remains an analytical Chinese close-reading guide rather than a second full
  translation.

## Mechanism Interrogation Gate

Treat deep reading as reconstruction followed by audit. First recover the strongest version of the authors' logic; only then test whether the problem is important, the assumptions are defensible, the design addresses the stated bottleneck, the evidence excludes relevant alternatives, and the conclusion stays within the evidence boundary. Do not confuse skepticism with automatic rejection.

Before calling the analytical close reading complete, establish all of the following from the source package:

- the concrete prior-method bottleneck and its proposed causal explanation;
- the key assumptions and the falsifiable predictions they imply;
- a design-to-mechanism chain: `design -> changed information/constraint/optimization -> predicted effect`;
- the decisive experiment, control, or ablation for each central mechanism claim;
- plausible alternative explanations that the experiments do or do not rule out;
- counterfactual predictions for removing, replacing, or simplifying a module;
- the data, scene, supervision, or optimization conditions under which the method should fail;
- the smallest credible alternative design and the next question that would discriminate between explanations.

Keep `作者声称`, `实验支持`, `我们的推断`, and `尚未验证` distinguishable in analytical notes. These are evidence statuses, not mandatory repeated headings. Do not inject this analysis into the source-faithful `英文原文稿` or `原文中译稿`; it belongs in the editable tree and analytical `精读稿`.

## When To Use

- Reading a new paper deeply rather than only summarizing it.
- Converting PDF extraction into a complete English original manuscript artifact, a complete faithful Chinese translation artifact in the main entry, a child-page close reading, an editable paper-analysis tree, and a paper card.
- Preparing Notion paper pages/notes, or repairing an existing legacy page in another platform when explicitly requested.
- Auditing whether figures, claims, assets, and citations are complete.

If the user says `deep dive`, `深读`, `详细解析`, `dive into`, or asks to deeply read a single paper, use this full workflow by default. Do not downgrade it to a quick summary, paper card only, or close-reading note only unless the user explicitly asks for a lighter output.

## Non-Negotiable Manuscript Deliverables

For papers with an accessible official PDF or full-paper HTML, the two linked manuscript artifacts are mandatory deliverables, not optional aids:

- `<paper short name>｜英文原文稿`: complete original English manuscript in source order.
- `<paper short name>｜原文中译稿`: complete faithful Chinese manuscript in the same source order.

If the PDF can be downloaded or viewed, assume the manuscripts can be produced by MinerU extraction plus official HTML / LaTeX / PDF verification. Do not use context length, page length, one-turn time, target-page size, translation workload, or "current tool path" as reasons to downgrade the deliverable into a section summary, structured outline, selected excerpts, or partial translation. Chunk the paper by sections, append incrementally, and continue until both manuscript artifacts are complete.

Only three conditions justify not producing the complete manuscript artifacts: the full paper source is inaccessible, reproduction is blocked by a clear licensing/copyright constraint, or the user explicitly asks for a lighter / partial artifact. In all other cases, an incomplete `英文原文稿` or `原文中译稿` is work in progress, not a compliant deep-dive deliverable.

## Source Acquisition Priority

Before running MinerU or writing any target page/note, build the complete source package, including every official or source-derived HTML version that can be found. Search for arXiv HTML (`https://arxiv.org/html/<id>` and versioned variants), publisher/proceedings HTML, OpenReview/forum HTML, CVF/open-access HTML, and project-page paper HTML when present. HTML is not optional source decoration: it is often the best source for section hierarchy, MathML / TeX annotations, figure/table nodes, captions, references, and supplementary links.

For papers that have an arXiv version, search and inspect the arXiv landing page, arXiv PDF, arXiv HTML, and LaTeX source before using a conference or publisher PDF as the main extraction source. Prefer arXiv HTML / LaTeX for structure, formulas, captions, references, and appendix discovery; prefer arXiv PDF for page layout, figure placement, and visual cross-checking. The reason is practical: many official conference PDFs omit appendices or supplementary sections, while arXiv often preserves the fuller manuscript.

Use venue/publisher pages and their official article/proceedings HTML for official metadata, acceptance venue, project/code links, supplement links, and cross-checking, but do not assume the venue PDF is the complete manuscript. If the only PDF initially found is from CVF, ACM, IEEE, Springer, PMLR, OpenReview, NeurIPS, a conference proceedings site, or a publisher landing page, explicitly search for separate `supplementary`, `appendix`, `supp`, `supplemental material`, `additional material`, `SM`, or `PDF supplementary` files on the same page, the official HTML page, the proceedings page, OpenReview, the project page, author/lab page, and arXiv.

When HTML and PDF disagree, treat official HTML / LaTeX as the first authority for source text, section order, formulas, captions, and references when it clearly preserves the paper source; cross-check figure placement, page layout, missing appendices, and visual assets against the PDF and supplement. Record meaningful discrepancies instead of silently choosing one source.

If a separate appendix/supplementary PDF exists, it is part of the deep-dive source package unless the user explicitly excludes it. Download it alongside the main PDF, include its sections, figures, tables, formulas, captions, algorithms, and references in the source map, and reflect it in both `<paper short name>｜英文原文稿` and `<paper short name>｜原文中译稿`. A deep dive based only on a conference main PDF is incomplete when a separate supplement exists and has not been inspected.

**Supplementary / appendix PDF extraction priority (mandatory):** when a separate supplementary or appendix PDF has no usable official HTML (typical for project-page or ACM/IEEE “Supplementary Material” PDFs), the required first conversion path is MinerU via `.tools/mineru-md.sh` (same Local MinerU Extraction rules as the main PDF). Do not use PyMuPDF / pdfplumber / raw `get_text` / page screenshots as the primary manuscript scaffold for that supplement. After MinerU, repair formulas/captions/tables against the PDF (and against HTML/LaTeX only if a supplement HTML/LaTeX source actually exists). PyMuPDF and similar tools are allowed only as a fallback after MinerU fails, or for narrow visual checks (page count, figure crop verification), not as the default text path for supplements.

Record the source package in task notes and compact source metadata: arXiv ID/version when available, arXiv PDF status, arXiv HTML URL/status, LaTeX source status, publisher/proceedings/OpenReview/CVF HTML URL/status, venue/publisher PDF status, supplementary/appendix PDF status, project/code links, and extraction date. If no HTML version is found, state the searched routes briefly; do not write `HTML not checked`. If no supplement is found, state the searched routes briefly; do not write `supplement not checked`.

## Workflow

### Imported PDF Translation Repair Path

When the user provides an arXiv PDF or paper title and asks to download, run
`pdf2zh`, and import the Chinese PDF into Notion, also use
[`paper-pdf2zh-notion-import`](../paper-pdf2zh-notion-import/SKILL.md). That
skill owns the direct Notion desktop import, title-based PDF renaming, local
artifact cleanup, and the mandatory two-round
repair/read-back cycle. The imported PDF is always draft material; a successful
Notion upload is not a completed `原文中译稿`.

When the user has already translated a paper PDF with `pdf2zh-next` and manually imported the resulting PDF into Notion or Feishu, treat the imported page as a **draft translation**, not as a completed `原文中译稿`. This path is an accepted entry point and does not require re-running PDF translation, but it must pass the same source-fidelity and platform verification gates before delivery.

**One-line workflow trigger:** `帮我 pdf2zh 并导入 Notion` is sufficient to invoke the full import workflow. Do not ask the user to restate the repair rules. Resolve the latest arXiv PDF, run the local conversion, import the Chinese PDF directly into the supplied Notion parent, then perform the two-round repair/read-back cycle below.

**Imported-page delivery exception:** For this `pdf2zh-next` repair path, the existing imported Chinese page is the primary deliverable. Do **not** require creation of the `英文原文稿` and `精读稿` child pages unless the user explicitly asks for them. The repair gate remains mandatory for the Chinese manuscript itself: verify it against the latest official PDF and available HTML/LaTeX, repair source-order structure, formulas, figures and native captions, tables, appendices, references, and body citations, then perform target-platform read-back verification. This exception applies only to repairing an already imported translation; a new paper deep dive created from source materials still follows the complete main-entry-plus-two-child-artifact contract.

- **A. Identify the source.** Locate the imported page and source PDF. Preserve imported figures, tables, and page order as draft material, then compare them against the source PDF and, when available, official HTML / LaTeX.
- **B. Fix identity and navigation.** Rename the page to the verified Chinese paper title only. Keep the official English title in the opening block. Add the latest arXiv PDF, Project Page, and Code links above the abstract when available. Do not add `英文原文稿` or `精读稿` links for this imported-page repair path unless explicitly requested; never infer URLs from a filename.
- **C. Repair structure.** Restore heading levels from the paper's numbered hierarchy, reconnect PDF-split paragraphs, remove duplicate headers/footers and conversion artifacts, and keep figures/tables near their source positions.
- **C1. Normalize numbered headings at every depth.** Use the numeric prefix to determine hierarchy, not the importer’s visual level: a one-part prefix such as `N.` (`3.`, `4.`) is a top-level section; a two-part prefix such as `N.M.` (`3.1.`, `4.2.`) is its subsection; a three-part prefix such as `N.M.K.` (`3.1.1.`, `4.2.1.`) is its sub-subsection; continue the same rule for deeper prefixes. Normalize full-width heading punctuation `．` (U+FF0E) to the ASCII period `.` before parsing, so `4．2．方法` becomes `4.2. 方法`. In ordinary structural text, normalize full-width slash `／` (U+FF0F) to `/`, full-width hyphen-minus `－` (U+FF0D) to `-`, and full-width brackets `［］` (U+FF3B/U+FF3D) to `[]` when they are citation, list, or link delimiters. Protect LaTeX, code, URLs, file paths, and existing backslash-escaped sequences before this cleanup, then restore them exactly; never perform a blind global replacement. Do not replace unrelated Chinese punctuation in ordinary prose. Default to `## 3. Section title`, `### 3.1. Subsection title`, and `#### 3.1.1. Sub-subsection title`. If the source consistently omits punctuation (`3 Title`, `3.1 Subtitle`), preserve that style for the whole manuscript; never mix punctuated and unpunctuated forms or place a deeper numeric prefix above its parent.
- **D. Repair formulas.** Restore inline formulas as native inline equations or exact `$...$` LaTeX, restore display equations and numbering, and sample early, middle, formula-heavy, and appendix sections.
- **E. Repair figures and tables.** Convert figure captions to native caption fields and keep the complete translated source caption without a duplicate paragraph or agent-written summary. Preserve English table cells, translate only table titles/notes, and use an original PDF/HTML screenshot when table layout is unreliable.
- **E0. Caption parser check.** Before writing a native Notion/Feishu image caption, verify that escaped citation delimiters such as `\[33\]` will not be parsed as block syntax. If the caption parser cannot preserve them, convert only those citation markers inside the caption to ordinary visible parentheses while keeping body citations and reference numbering unchanged; then verify that the caption is stored on the image block and no duplicate caption paragraph remains.
- **E1. Repair imported table corruption.** Inspect every imported table block and its surrounding text for OCR/PDF conversion residue: duplicated Markdown pipe tables after a native table, broken rows or columns, repeated cell fragments, garbled characters, malformed separators, and captions fused to table data. Keep one authoritative editable table, reconstruct rows/cells from the official PDF/HTML when the extracted structure is reliable, and otherwise add an official PDF/HTML table screenshot as the visual authority. Remove duplicate pseudo-tables and keep exactly one translated table title/note attached to the table.
- **E2. Author contacts and resource links.** Author email addresses must be written as ordinary visible text, not intentionally wrapped in Markdown links, `mailto:` links, or code formatting. Notion may auto-link a bare email during rendering; do not add an explicit link or change its visible text to code merely to fight that platform behavior. **Only in the opening resource block of a deep-dive Chinese manuscript**, omit the heading `来源` and display each link's URL as its link text, for example `[https://arxiv.org/pdf/<id>](https://arxiv.org/pdf/<id>)`. This URL-as-label rule does not apply to English manuscripts, paper cards, or general research documents.
- **F. Repair citations.** A Chinese-manuscript reference **title may be translated**, but authors, venue, publisher, year, volume/issue, pages, DOI/arXiv identifiers, URLs, and other bibliographic metadata remain in the source language. Keep `[n]` labels, one reference per paragraph, and restore verified PDF URLs. Body citation links must use the same URL map.
- **G. Verify completion.** Run the full Chinese-manuscript completion gate and record unresolved figure, table, formula, reference, URL, or hierarchy issues. A manually imported page is complete only after repair and fetch/read-back verification; the absence of the two child artifacts is not a failure for this exception path.

**Two-round repair is mandatory for imported pages.** Round 1 fixes structure and source fidelity against HTML/LaTeX/PDF. Round 2 starts from a fresh Notion read-back and independently audits formulas, inline math, figure/caption placement, table integrity, references, body citation links, appendices, and conversion residue. A first-pass upload or a single visual scan is never a completed delivery.

1. Capture source metadata and source package inventory: title, authors, year, venue, DOI/arXiv, arXiv PDF URL/status, arXiv HTML URL/status, LaTeX source status, publisher/proceedings/OpenReview/CVF HTML URL/status, venue/publisher PDF URL, supplementary/appendix PDF URL(s), project/code links, local source paths, and extraction date.
2. Extract or parse the complete source package to inspectable Markdown when tooling is available; preserve figure references and equation context. On this machine, use MinerU as the default PDF-to-Markdown path before building deep-dive artifacts, but parse official HTML / LaTeX first when available for source structure, formulas, captions, references, and appendix coverage. Parse the arXiv/full manuscript first when available, then parse any separate supplement/appendix PDF with the same priority: official supplement HTML/LaTeX if present, otherwise MinerU on the supplement PDF before any other PDF text extractor.
3. Check the MinerU conversion draft against official HTML whenever HTML exists, especially arXiv HTML for arXiv papers and publisher/proceedings HTML for non-arXiv papers. This check is mandatory, not optional. Repair section order, paragraph continuity, formulas, figures, tables, captions, appendices, body citations, and references before publishing.
4. Build a source map inspired by `nature-reader`: stable block IDs for body text, figures, tables, captions, equations, appendices, and references; page / section location; extraction confidence; and links between first figure/table mention and the visual asset.
5. Create the complete English original manuscript artifact (`<paper short name>｜英文原文稿`) from the verified official paper source. This means the paper's original English text in source order, not a structural outline, not selected excerpts, and not an English summary. If an official PDF or full-paper HTML is accessible, this artifact must be completed by section-level chunking and source verification before the deep dive is marked complete. The English manuscript is the translation/alignment base and remains a mandatory deliverable even though the user usually reads the main entry and Chinese manuscript more often.
6. **English HTML correction gate (mandatory after the English manuscript draft exists):** for arXiv papers, re-open arXiv HTML and correct the English manuscript against it before starting Chinese translation. Check section order, paragraph continuity, formulas (inline and display), figure/table captions, appendix/supplement coverage, body citations such as `[[n](pdf-url)]`, and the References block under the Reference and Citation Link Contract. Prefer arXiv HTML as the correction authority for text/structure/formulas; use PDF only for layout/visual cross-check. For non-arXiv papers, run the same gate against the best available official HTML (publisher/proceedings/OpenReview/CVF); if no HTML exists, correct against LaTeX/PDF and record that HTML correction was impossible. Do not begin `原文中译稿` until this gate passes or is explicitly blocked/recorded.
7. Create the complete faithful Chinese manuscript artifact (`<paper short name>｜原文中译稿`) from the HTML-corrected English manuscript in source order. It must preserve section hierarchy, paragraph correspondence, formulas, figure/table positions, citations, captions, references, appendices/supplements, and layout structure as much as the target editor allows. Translate the paper body, figure captions, table captions/notes (表注), appendix/supplement prose, and explanatory text into Chinese, but keep table cell content (headers and body cells) in the original English, and keep the References / bibliography entries in their original English form with the same `[n] … . URL [url](url)` PDF-link contract and the same body `[[n](url)]` links as the English manuscript. A partial translation is allowed only as a clearly marked WIP state; it is not a final deep-dive deliverable.
8. **Chinese terminology correction gate (mandatory after the Chinese manuscript draft exists):** do a dedicated second pass over `原文中译稿` for terminology only. Verify key method/model/dataset/loss/module terms are consistent; keep named architectures, models, methods, datasets, and official components such as `Transformer` and `DINO` in their official English form; add a Chinese gloss only when it improves comprehension; and translate generic technical concepts instead of leaving avoidable English phrase islands. Fix inconsistent renderings of the same term across sections. Do not mark the Chinese manuscript complete until this terminology pass is done.
8b. **Reference / citation verification gate (mandatory for both manuscripts):** build a single `[n] → PDF URL` map (prefer arXiv PDF), apply it to References (`. URL [url](url)`) and body (`[[n](url)]`), then verify URL correctness and cross-consistency as specified in Reference and Citation Link Contract. For an imported PDF2ZH Chinese manuscript, the cited paper title may be translated, but all other bibliographic fields must remain source-faithful. Do not mark either manuscript complete until this gate passes.
9. Create or update the main reader-facing deep-dive entry. The main entry is the complete `原文中译稿` and should be the default reading surface. Its opening must follow a paper-like title block before the abstract: the official English title, the Chinese title directly below it, the original English author list and affiliations, then three verified resource links on separate lines: the latest arXiv PDF, the Project Page, and the Code repository. Use `未找到` / `Not found` only when a resource was searched and genuinely unavailable; never invent a link. After this opening block, continue with the source-faithful abstract and manuscript in normal paper order. Add clear links to exactly two child pages: `英文原文稿` and `精读稿`. A compact paper card and editable `论文解析树` may be placed before the translation when useful, but they must not replace, truncate, or interleave with the source-order Chinese manuscript.
10. Create an editable `论文解析树` that follows the paper's actual reasoning: problem -> concrete bottleneck -> key assumption -> design/mechanism -> changed information or constraint -> predicted effect -> decisive evidence -> boundary. Make the information-flow view (what passes between modules) and the causal-chain view (why the design should change the result) distinguishable. Add losses/training, datasets/evaluation, limitations, and user research implications where they clarify this logic rather than as disconnected inventory branches. Use a native Feishu mind map for Feishu, a structured page/database or supported embedded artifact for Notion, and Mermaid/Canvas plus a searchable linked outline for Obsidian. Do not substitute a static screenshot when an editable representation is available.
11. Create the child-page `精读稿` as a source-order analytical close reading, not a thematic essay. Follow the paper's own section order and local context: Abstract / Introduction, numbered sections, named subsections, conclusion, then appendices or supplementary material. For each part, explain which claim it advances, why that step is needed, what mechanism or evidence is introduced, and what remains unresolved. Preserve local source context instead of forcing the same audit questions into every subsection. Do not insert a repeated per-section heading or paragraph such as "what this means for my world-model research" / "对你的 world model 研究意味着什么"; that lens distorts the source-order reading. Put user-specific research implications, world-model / embodied-world-model takeaways, and future project ideas only in a final synthesis section after the source-order close reading. This is interpretation and learning material; do not present it as the complete translation. Ground important analysis in source-map block IDs or short bilingual snippets when useful.
    - Inside `精读稿`, use `###` or lower-impact paragraph/list structure for source-order close-reading subsections. Do not use `####` headings for close-reading subsections on a page that also contains paper cards, because `####` is reserved for paper-card titles and is checked by `paper-card-delivery` validators.
12. After the source-order close reading, write one integrated mechanism synthesis. Its headings may vary with the paper, but it must cover the strongest author argument, assumptions and falsifiable predictions, claim-evidence-alternative-explanation alignment, counterfactual ablation predictions, minimal necessary design, failure boundaries, and a discriminating next research question. Add user-specific transfer only at the end and only when it follows naturally from the paper.
13. Create a paper card using [`paper-card-delivery`](../paper-card-delivery/SKILL.md), then run its validator on the Markdown draft when a local draft exists.
14. Store figures and assets in a stable assets folder.
15. Mark author claim, experimental support, inference, citation needed, and unresolved questions separately.

Paper-card content standards live in [`paper-card-delivery`](../paper-card-delivery/SKILL.md). This deep-dive skill must not duplicate or override paper-card source verification, metadata, image/caption selection, fixed bullet slots, sorting, or structural validation.

## Local MinerU Extraction

For future deep dives, first create a MinerU conversion draft when a PDF is available. Use it as the source-order manuscript scaffold for `<paper short name>｜英文原文稿`, `<paper short name>｜原文中译稿`, and the child-page `精读稿`.

- Preferred wrapper in this vault: `$WORLD_MODEL_VAULT/.tools/mineru-md.sh`
- MinerU binary on this machine: `$WORLD_MODEL_VAULT_MINERU_BIN`
- Verified local version: `mineru 3.3.1`
- Store MinerU outputs, downloaded PDFs, supplementary/appendix PDFs, official HTML snapshots/pages, arXiv HTML, LaTeX source, and temporary figure assets under `.tools/tmp/codex/<task-slug>/`; delete them after the target artifacts are written and verified successfully.
- MinerU is a conversion draft, not the authoritative final text. When an official HTML version exists, always check the MinerU draft against it before publishing target artifacts. For arXiv papers, arXiv HTML is the preferred HTML check; for non-arXiv papers, use publisher/proceedings/OpenReview/CVF HTML when available. Verify section order, paragraph continuity, equations, figures, captions, tables, appendices, citations, and references. If HTML is unavailable or incomplete, use official LaTeX source or the official PDF as the authority and record that HTML could not be used.
- If MinerU misses or corrupts formulas, figures, captions, appendices, or references, repair from official HTML/LaTeX/PDF or the official publisher source before marking the deep dive complete.
- If MinerU itself fails but the PDF is accessible, try the local wrapper again with a clean output directory, inspect the error, and then use a structured fallback such as official HTML/LaTeX, publisher HTML, Docling, Marker, PyMuPDF, or pdfplumber. MinerU failure is a workflow problem to resolve or work around, not permission to ship manuscript summaries.

## Manuscript Fidelity Requirements

- `<paper short name>｜英文原文稿` and `<paper short name>｜原文中译稿` must preserve paper-like citation flow. Preserve the source paper's citation style in the body: author-year forms such as `（Hassan 等人，2019a）` / `(Hassan et al., 2019a)` are valid and should not be forcibly converted to numeric citations. When a verified PDF URL exists, the author-year citation itself should carry the link, for example `（[Hassan 等人，2019a](pdf-url)）` or `([Hassan et al., 2019a](pdf-url))`. Numeric citations must remain bracketed (`[n]`, or clusters such as `[1, 3, 5]` / `[1–3]`) when the source uses them, with the numeric PDF-link contract below applied to those numeric citations.
- Both manuscript artifacts must cover the full paper source package that the user is trying to deep dive: Abstract, Introduction, all numbered / named main sections, Conclusion / Discussion, **appendices and/or supplementary materials (mandatory when they exist in any official source)**, figure and table captions, algorithms when present, and References. If the conference/publisher PDF omits appendices but arXiv or a separate supplement contains them, include those materials unless the user explicitly excludes them. If the user explicitly excludes appendices or supplementary material, record that exclusion in the affected artifact and final report.
- **Supplementary / appendix is a first-class deep-dive deliverable**, not an optional add-on. Reproduction details, hyper-parameters, extra ablations, proofs, and implementation notes often live only there. Both `英文原文稿` and `原文中译稿` must include the same appendix/supplementary coverage (English keeps original text; Chinese translates body/captions/notes of the supplement with the same fidelity rules as the main text). A package that stops at the main conference PDF while a usable supplement/appendix exists is incomplete.
- Before marking complete, compare both manuscript artifacts against the official source section list **including appendix/supplement headings**. Missing sections, reordered sections, dropped captions, collapsed tables, omitted algorithms, omitted appendices/supplements, or absent References make the artifacts incomplete.
- Figures and tables must be placed near their original reference/caption positions. Use native Feishu/Notion image blocks or stable relative Obsidian assets when reliable official image assets are available.
- For tables, verify both semantic extraction and visual fidelity. Compare complex or formula-heavy tables against an official PDF/HTML screenshot, and include that screenshot in `原文中译稿` when extraction cannot guarantee merged cells, multi-level headers, footnotes, symbols, colors, borders, or layout. MinerU is a manuscript scaffold and locator, not the sole authority for table screenshots.
- Attach captions using the selected platform's native or established representation: native image captions in Feishu/Notion, and the vault convention or meaningful alt text in Obsidian. Captions with formulas may use an immediately adjacent formula-capable block when the native caption cannot preserve TeX; preserve the exact TeX source and do not duplicate the caption.
- Figure captions are source-fidelity content. English original pages must preserve the official original caption, and Chinese manuscript pages must use a complete Chinese translation of that caption. Do not replace captions with agent-written summaries such as `方法或实验概览` / `method or experiment overview`, source-process notes, or generic explanations such as `用于说明论文的核心流程、输入输出关系和关键模块`, `原始 caption 已在图中保留`, or `便于回溯核验`. If a source tag is useful, keep only a short controlled label from `paper-card-delivery`, such as `来源：用户截图`, `来源：HTML`, `来源：MinerU PDF 截图`, or `来源：PDF 截图`.
- Table translation rule for `原文中译稿`: translate table captions and table notes (表注 / footnotes under the table) into Chinese; do **not** translate table cell content, including column/row headers and body cells. Keep the table body in the original English so numeric comparisons and method/dataset labels stay aligned with the source. English original manuscript pages keep both table captions and table cells in the original English.
- Table screenshot support: `原文中译稿` may and should include an original table screenshot when the table's visual structure cannot be trusted after extraction. Use a crop from the official PDF or a verified official HTML rendering as the visual authority; do not treat a MinerU-generated table image or reconstructed screenshot as authoritative. Place the screenshot near the corresponding table position, preserve the official English cell content in the screenshot, and put the translated Chinese table title and table notes into the platform's native image caption. Do not duplicate the same caption or notes as adjacent body prose. If the target platform supports an editable table, retain the editable English-cell table as well; the screenshot is the visual-fidelity reference, not an excuse to drop the table entirely. If only a screenshot can preserve the table reliably, label it as an original table screenshot and record the rendering fallback in the verification notes.
- Formulas must be checked against official HTML/LaTeX/PDF and preserved in LaTeX where possible. This includes inline formulas, not only displayed equations. Do not publish pages where important equations, inline variables, losses, or symbolic expressions have collapsed into prose or lost subscripts/superscripts.
- The complete Chinese manuscript follows the same fidelity requirements as the English original manuscript: original section order, paragraph correspondence, figure/table positions, formula placement, body citations, References, captions, appendices/supplements, and table structure. The Chinese manuscript's References section remains the original English bibliography (never translated) with the same `[n]` labels and PDF-link contract as the English manuscript.
- Chinese terminology must be deliberate. Translate generic technical concepts into accurate Chinese, but keep named architectures, models, methods, datasets, and official components unchanged in their source form, including names such as `Transformer` and `DINO`. Add a short Chinese gloss on first use only when it helps comprehension; do not invent translations for official names. Do not leave dense generic English terminology untranslated in ordinary Chinese explanatory prose. After drafting the Chinese manuscript, run the dedicated terminology correction gate before marking it complete.

## Reference and Citation Link Contract (mandatory)

This contract applies to **both** `<paper short name>｜英文原文稿` and `<paper short name>｜原文中译稿`. The Chinese manuscript must not invent a different citation scheme.

### References block (bibliography)

- In the English manuscript, do not translate any bibliography field. In the Chinese manuscript, the cited paper title may be translated for readability, including when the title was already translated by `pdf2zh-next`; authors, venues, publishers, page ranges, year, DOI/arXiv strings, URLs, and all other bibliographic metadata must remain in the original language and source order.
- **Format**: plain text lines / paragraphs starting with bracket labels such as `[1]`, `[2]`, `[12]`. One reference per line or paragraph.
- **Title delimiters**: enclose each cited paper title in Chinese quotation marks `“...”` so the title is visually distinct from authors, venue, year, and other bibliographic metadata. This applies whether the title is retained in English or translated in a Chinese manuscript.
- **Important references**: when a reference is central to the paper's method, baseline, theoretical foundation, or the user's research context, underline **only the paper title** using the target platform's native underline formatting. In Notion enhanced Markdown, use `<span underline="true">...</span>`; do not underline the citation number, authors, venue, year, URL, or the entire reference entry. Do not overuse this emphasis: mark only genuinely important references.
- **Forbidden formats**: Markdown/platform ordered lists (`1.` `2.` `3.`), bullet lists that replace or hide the bracket numbers, renumbered citations, or Chinese-translated bibliography entries.
- **PDF link suffix (mandatory when a usable PDF URL can be found):** after the full reference text, append `. URL ` (period, space, `URL`, space) — or just ` URL ` if the bibliography text already ends with a period, to avoid `.. URL` — and then a hyperlink whose **display text equals the URL string itself**. Prefer an **arXiv PDF** URL of the form `https://arxiv.org/pdf/<id>` (with or without version, matching the cited work). If no arXiv PDF exists, use the best open PDF (OpenReview, CVF, PMLR, publisher OA, project page) in the same `. URL [url](url)` form. If no PDF can be verified after search, keep the entry without a fake link and mark `PDF link: not found` in the verification log—do not invent URLs.
- **Canonical References line example (Markdown):**
  ```markdown
  [1] Author A, Author B. “Paper title.” Conference/Journal, year. URL [https://arxiv.org/pdf/2401.12345](https://arxiv.org/pdf/2401.12345)
  ```
- **Important-reference example (Notion):**
  ```markdown
  [12] Author A, Author B. “<span underline="true">Paper title</span>.” Conference/Journal, year. URL [https://arxiv.org/pdf/2401.12345](https://arxiv.org/pdf/2401.12345)
  ```
- On Feishu/Notion, render the same structure: `[n]` plain label + original English bibliography text + `. URL ` (or ` URL ` after an existing period) + clickable URL whose visible text is the full URL.

### Body citations

- Preserve every in-text citation that corresponds to the bibliography in the source paper's native style. Author-year citations such as `（Hassan 等人，2019a）` / `(Hassan et al., 2019a)` are allowed in both manuscripts when that is the source style; when a verified PDF URL exists, link the author-year text itself, e.g. `（[Hassan 等人，2019a](pdf-url)）`. Numeric citations must appear as bracketed numeric citation(s), preserving source positions, when the source uses numeric keys.
- **Link only the number, never the citation brackets.** The canonical body-citation form is `[[1](https://arxiv.org/pdf/2401.12345)]`: the inner `1` is the hyperlink text, while the outer `[` and `]` are ordinary plain-text citation brackets. The link range must not include either bracket. Do not use `[[1]](https://arxiv.org/pdf/2401.12345)` or any platform form that makes `[1]` the hyperlink text. Target the **same PDF URL** recorded for that `[n]` in References:
  ```markdown
  [[1](https://arxiv.org/pdf/2401.12345)]
  ```
  Multi-cite example:
  ```markdown
  [[1](https://arxiv.org/pdf/2401.12345), [3](https://arxiv.org/pdf/2305.67890)]
  ```
- **Platform read-back check:** after writing to Feishu or Notion, inspect the rendered link range. It must show a plain outer bracket before and after a linked numeral, visually `[1]`; selecting the link must select only `1`, not `[1]`. **On Notion**, Markdown write-back routinely stores the first number in a cluster as link text `[n`; after every such write, run `notion-doc-workflow/scripts/fix-notion-citation-rich-text.py <page>` and require `--check-only` to exit 0 before delivery.
- The body link target for numeric `[n]` citations must be **identical** to the URL used after `. URL ` for that same `[n]` in References (same string, not a different landing page). For author-year citations, build an equivalent author-year → PDF URL map and use the same URL in the linked citation text. Prefer arXiv PDF over abstract HTML when both exist.
- Do not leave bare `[1]` without a PDF hyperlink when References already has a verified PDF URL for `[1]`. If References has no PDF for that entry, keep plain `[n]` and record the gap in verification.
- Author-year markers in the source (e.g. `(Smith et al., 2024)` or `（Hassan 等人，2019a）`) may be retained as valid body citations. When the corresponding PDF is verified, link the author-year text itself using the same PDF URL as the matching bibliography entry. The numeric `[n]` link contract remains mandatory only where the paper uses numeric bibliography keys; do not invent numeric links for an author-year-only source.

### Reference / citation verification gate (mandatory)

Before marking either manuscript complete, run an explicit verification pass and record pass/fail in task notes:

1. **References inventory:** list every numeric `[n]` or author-year key present in the paper's References; confirm none were dropped, renumbered, or converted to `1.` lists; confirm no Chinese translation of bibliography text.
2. **PDF URL resolution:** for each numeric `[n]` or author-year key, resolve the preferred PDF URL (arXiv PDF first); spot-check that the URL opens the cited work (title/authors/year match), not a wrong paper or abstract-only page mistaken for PDF when a PDF URL is required.
3. **Suffix format:** each linked entry uses `. URL [url](url)` (or ` URL [url](url)` when the entry already ends with `.`) with display text == URL.
4. **Body coverage:** sample early / middle / late / appendix sections; every numeric citation site that should be `[n]` is present; linked numbers point to the same URL as References for that `n`.
5. **Cross-check:** no body `[n]` links to a URL that References does not use for that `n`; no References URL is assigned to the wrong number.
6. **Failure handling:** fix mismatches before delivery. Unresolvable PDFs are allowed only with an explicit `not found` note—never placeholder or guessed links.

Do not mark the deep dive complete if this gate has not been run on both manuscript artifacts (English and Chinese share the same URL map; verify both surfaces still render the links correctly after platform write-back).

## Formula / Equation Handling

For paper deep dives and complete manuscript pages, formulas are source-fidelity content, not prose to paraphrase.

- Extract formulas from the official full-paper source before writing. For arXiv papers, prefer arXiv HTML / LaTeX source because it usually preserves MathML, TeX annotations, equation IDs, and numbering; use the PDF or a structured PDF parser only as fallback. Do not reconstruct formulas from collapsed platform exports or OCR text when the official formula source is available.
- Preserve inline formulas as carefully as displayed equations. Inline variables, operators, compact expressions, losses, references such as `Eq. (4)`, and symbolic phrases such as `$S$`, `$G$`, `$l(S)$`, `$\bm{x}^{n}$`, or `$\mathcal{L}_{\text{RGB}}$` must stay in inline LaTeX, not ordinary text, translated prose, or backticks.
- During translation, protect inline and displayed formulas with non-translatable placeholders, translate surrounding prose only, then restore the exact TeX from the official source. Do not let machine translation translate variable names, LaTeX commands, `\text{...}` labels, Greek letters, superscripts, subscripts, hats, dots, norms, fractions, sums, products, matrices, or equation tags.
- In platform-neutral Markdown sources, use `$...$` for inline math and `$$...$$` for displayed equations. Map them to native equation blocks in Feishu or Notion and preserve them directly in Obsidian. Keep displayed equations on their own lines with blank lines before and after. Do not wrap formulas in code fences or backticks unless explicitly creating a raw-LaTeX fallback section.
- Preserve equation numbering. Prefer `\tag{n}` when the target renderer supports it; otherwise place a separate plain-text number like `(n)` immediately after the displayed equation. Keep references such as `式 (4)` aligned with the original paper.
- After writing, re-fetch or re-read the target and verify formula fidelity. Inspect samples from early, middle, appendix, and formula-heavy sections, and confirm formulas did not degrade into plain text, lose `_` / `^`, merge with surrounding prose, or become translated words.
- If the target platform cannot render a formula reliably, keep the exact LaTeX source in a labeled `公式 LaTeX 源` block and, for important equations, insert a rendered equation image with a Chinese caption. Mark this as a rendering fallback, not as the preferred final form.

## Output

Use this fixed semantic package on every platform:

- Main entry: title must be the verified Chinese paper title only, including the method name when it is part of that title. Do not append status or artifact suffixes such as `原文中译稿`, `中文`, `深度笔记`, `学习页`, `Deep Dive`, `阅读笔记`, or `解析`. The main entry's semantic role is the complete faithful `原文中译稿`; this role is expressed by the content and structure, not by a title suffix. It links exactly two child pages: `<paper short name>｜英文原文稿` and `<paper short name>｜精读稿`. A compact `Paper Card` and editable `论文解析树` may appear before the translation as navigation/context, but the Chinese manuscript remains complete, source-order, and visually distinct.
- Main-entry opening block: before `摘要`, place the official English title, the Chinese title directly below it, the original English author list and affiliations, and three separate verified links in this order: `最新 arXiv PDF`, `Project Page`, `Code`. The arXiv link must point to the latest available arXiv PDF version, not merely the abstract/landing page. Project and Code links must point to the official project or repository when available.
- Child artifact 1: `<paper short name>｜英文原文稿`, the complete original English manuscript from official PDF/HTML/LaTeX/MinerU extraction, corrected against arXiv/official HTML when available. It is the bilingual-alignment base and remains mandatory and high-fidelity. Do not replace it with an extraction-status page when the official PDF or full-paper HTML is accessible.
- Child artifact 2: `<paper short name>｜精读稿`, the source-order analytical close reading with the editable `论文解析树` and mechanism synthesis. It is interpretation and learning material, not a substitute for either manuscript. Keep user-specific research takeaways in its final synthesis section.

Platform mapping for new deep dives:

- Notion (via `notion-doc-workflow`): one parent page containing the complete Chinese manuscript plus two subpages for English manuscript and close reading, native image captions/equations, and an editable structured tree or supported embed.
- Obsidian (via `obsidian-doc-workflow`) is an optional local staging or archival surface, not the default durable deep-dive destination.

Feishu deep-dive pages are legacy compatibility targets only. Do not create new Feishu deep dives or keep a synchronized Feishu copy unless the user explicitly asks.

Choose `<paper short name>` as the shortest unambiguous paper identifier already used by the community or the paper itself, such as method acronym, article short title, or arXiv/project name. Do not use the full official title for linked manuscript artifacts when it makes the title unwieldy.

Do not create a separate `中文精读稿` linked artifact by default. The close-reading notes belong in the dedicated `精读稿` child page. Do not replace the complete Chinese manuscript, English manuscript, or close-reading child page with an outline, section summary, or mixed translation/interpretation page.

Do not omit the main-entry opening title/author/resource block. Keep the English title and author affiliations source-faithful; place the Chinese title below the English title, and keep the three resource links separate from the translated manuscript prose.

Remove obsolete process/status scaffolding from reader-facing main entries. Sections such as `Source Extraction`, `Deep Dive Structure Status`, long extraction inventories, local MinerU availability notes, and self-referential statements about which linked artifact is complete are working notes, not deep-dive content. Keep durable source links in a compact `来源` section when useful.

Use:

- `Paper Metadata`
- `Extraction Result`
- `English Original Manuscript`
- `Faithful Chinese Manuscript`
- `Editable Paper Analysis Tree`
- `Chinese Close Reading Notes`
- `Paper Card`
- `Assets`
- `Open Questions`
- `Sync Checklist`

## Guardrails

- Do not fabricate paper content when extraction is incomplete.
- Do not merge translation, interpretation, and speculation without labels.
- Do not call a page `英文原文稿` unless it is named `<paper short name>｜英文原文稿` and contains the original English paper text in source order.
- Do not call a page `原文中译稿` unless it is a complete, faithful translation of the source paper rather than a close-reading note. For legacy pages named `中文原文稿`, rename them to `<paper short name>｜原文中译稿` when repairing the hierarchy.
- Do not mark a deep dive complete if either manuscript artifact is partial, section-summary-only, selected-excerpt-only, missing References, missing appendices/supplements included in any official source of the package, or missing major figures/tables/captions from the source paper.
- Do not convert References into platform ordered-list numbering (`1.` `2.`). Keep original labels such as `[1]` visible in ordinary text, and append `. URL [pdf-url](pdf-url)` when a verified PDF URL exists.
- Do not translate bibliography metadata in `原文中译稿`. A cited paper title may be translated, but authors, venue, year, pages, identifiers, URLs, and other reference fields must remain source-faithful.
- Do not leave numeric body `[n]` citations without the shared PDF hyperlink when References already records a verified PDF URL for that `n`; body and References must use the same URL string. Author-year citations do not need to be rewritten as numeric links when the source uses author-year style.
- Do not invent or guess PDF / arXiv links. Unresolved links must be marked `not found` after search, not fabricated.
- Do not translate table cell content in `原文中译稿`; translate only table captions and table notes (表注).
- Do not mark a deep dive complete when HTML availability has not been searched and recorded. If official HTML exists, the MinerU/PDF draft must be checked against it; for arXiv papers, the finished English manuscript must also pass the dedicated arXiv HTML correction gate before Chinese translation starts. If HTML is unavailable or incomplete, record the searched routes and fallback authority.
- Do not mark `原文中译稿` complete until the dedicated Chinese terminology correction gate has been run.
- Do not mark either manuscript complete until the Reference / citation verification gate has been run.
- Do not mark a deep dive complete when the source was taken from a conference/publisher PDF and supplementary/appendix material has not been searched. If separate supplementary material exists, the deep dive is incomplete until it is parsed, incorporated into **both** manuscript artifacts, or explicitly excluded by the user.
- Do not create a source-link / extraction-status artifact as a substitute for `英文原文稿` or `原文中译稿` when the official PDF or full-paper HTML is accessible. Use that fallback only for genuine source access or licensing blockers, and label the whole deep dive as blocked / incomplete.
- Do not treat long papers as a reason to reduce scope. Split the manuscript and translation by source sections, append incrementally, and verify coverage before final delivery.
- Do not create a separate `中文精读稿` artifact unless the user explicitly asks; the default close-reading deliverable is the dedicated `精读稿` child page.
- Do not cite figures or equations that were not actually extracted or inspected.
- Do not present a paper card as finished unless its problem, method, implementation, conclusion, limitations, and figure claims are grounded in the official full paper; use `Not reported`, `N/A`, or `待核验` instead of guessing.

## Manuscript Completion Gate

Before declaring a deep dive compliant, re-fetch or re-read the main entry and both linked manuscript artifacts, then verify:

- The main entry contains the complete `原文中译稿`, links exactly two child pages named `英文原文稿` and `精读稿`, and keeps any paper card/tree content clearly separate from the translation.
- Before `摘要`, the main entry has the English title, Chinese title, original English authors/affiliations, and separate verified links for latest arXiv PDF, Project Page, and Code in that order.
- `<paper short name>｜英文原文稿` contains the original English source text in paper order, not a summary or outline, and has passed the arXiv/official HTML correction gate when HTML exists.
- `<paper short name>｜原文中译稿` mirrors the English manuscript section by section and paragraph by paragraph as closely as the editor allows, and has passed the dedicated terminology correction gate.
- Official source sections, captions, tables, algorithms, appendices/supplements, body citations, and References are present or explicitly excluded by the user. Both manuscripts include the same appendix/supplement coverage when those materials exist.
- References keep original `[n]` labels as plain text (not `1.` ordered lists), remain untranslated in Chinese manuscripts, and use `. URL [pdf-url](pdf-url)` with display text equal to the URL when a verified PDF (prefer arXiv) exists.
- Body citations preserve the source style: author-year citations use linked author-year text such as `（[Hassan 等人，2019a](pdf-url)）` when a verified PDF exists, while numeric citations use `[[n](pdf-url)]` (or multi-cite equivalents). For numeric citations, the outer square brackets are plain text and only `n` is the link text; each URL must match the corresponding References map entry.
- The Reference / citation verification gate has passed for both manuscript artifacts (inventory, URL correctness, body↔References consistency).
- If the Chinese manuscript came from a manually imported `pdf2zh-next` PDF, its page title is the verified Chinese paper title, the opening resource links are present, native captions/equations are restored where supported, and imported formatting defects have been repaired or recorded.
- Source package inventory records arXiv availability, HTML URL/status, venue/publisher PDF status, and supplementary/appendix search result; arXiv HTML / LaTeX / full manuscript sources were preferred when available, and any HTML fallback or absence is explicitly recorded.
- Formulas and inline symbols survive source verification against official HTML/LaTeX/PDF samples from early, middle, formula-heavy, and appendix sections.
- Numbered headings at every depth follow the source section tree: the number of numeric components determines heading depth (`N` → level 1, `N.M` → level 2, `N.M.K` → level 3, and so on), parent sections appear before children, and punctuation is consistent throughout each manuscript.
- Heading-number punctuation is normalized: full-width `．` is not left in numbered prefixes when the target uses ASCII Markdown/Notion heading text; ordinary Chinese punctuation outside heading prefixes is preserved.
- Structural full-width marks such as `／`, `－`, and `［］` are normalized to ASCII `/`, `-`, and `[]` only outside protected formulas, code, URLs, paths, and escaped sequences.
- Complex tables have passed a visual check against an official PDF/HTML screenshot; any table screenshot included in `原文中译稿` is sourced from the official rendering or is explicitly marked as a rendering fallback.
- The editable tree and `精读稿` expose both information flow and the causal chain from bottleneck through mechanism to predicted effect and evidence.
- The synthesis identifies the decisive evidence, relevant alternative explanations, and at least one counterfactual prediction for removing or simplifying a claimed key design.
- The reader can explain where the paper's assumptions stop applying and why; a section-by-section paraphrase without this mechanism audit is incomplete.
- Any remaining missing section, figure, table, formula, or translation block is reported as an incomplete WIP item; do not call the package finished.
