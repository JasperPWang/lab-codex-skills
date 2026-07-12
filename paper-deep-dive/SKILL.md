---
name: paper-deep-dive
description: Canonical platform-neutral single-paper deep-dive delivery standard for Feishu/Lark, Notion, and Obsidian/Markdown. Use whenever the user mentions deep dive, 深读, 详细解析, detailed-read, dive into a paper, full paper reading, English original manuscript, 原文中译稿, or asks to audit/repair a deep-dive package. Produces one main entry with Paper Card, 论文解析树, and source-order 精读稿, plus complete linked artifacts for 英文原文稿 and 原文中译稿; no other skill may relax or replace this delivery contract.
---

# Paper Deep Dive

Short description: PDF to deep paper notes workflow. Historical source: Feishu wiki AI Research Skills; current delivery is platform-neutral.

Use this skill when the user wants a complete paper reading workflow from PDF to stable notes, paper card, assets, and shareable summaries.

## Single Source of Truth

This skill is the only canonical delivery standard for single-paper deep dives. Other skills may trigger, route, write to Feishu/Notion/Obsidian, preserve Chinese wording, or distill the finished deep dive into a wiki, but they must not define a second deep-dive structure or mark a package complete under weaker rules.

When any user request says `deep dive`, `深读`, `详细解析`, `detailed-read`, `dive into`, `精读这篇论文`, `英文原文稿`, or `原文中译稿`, treat it as this full workflow unless the user explicitly asks for a lighter artifact such as quick summary, paper card only, or partial translation. A lighter artifact must be labeled as such and must not be called a compliant deep dive.

The completion standard is product-level, not effort-level. A main entry that has a good summary but incomplete manuscript artifacts is still incomplete. A package is compliant only when the main entry, both linked manuscript artifacts, figures/captions, formulas, references, hierarchy, and target-platform read-back verification all pass the delivery gate below.

## Canonical Platform Delivery Gate

Also use [`research-doc-workflow`](../research-doc-workflow/SKILL.md). Keep one Markdown-first manuscript and close-reading structure across platforms; only hierarchy, callouts, captions, properties/frontmatter, uploads, editable trees, and write verification need small adapters. Do not silently redirect a Notion or Obsidian request to Feishu.

## Canonical Paper Card Gate

When this workflow creates or modifies a paper card, also use [`paper-card-delivery`](../paper-card-delivery/SKILL.md). That skill is the canonical standard for official-source verification, fixed card format, figure/caption selection, and structural validation. Do not finalize the card from this deep-dive skill alone.

## Canonical Chinese Technical Writing Gate

For `原文中译稿`, `完整中文译稿`, `精读稿`, Chinese figure captions, main-entry summaries, and Chinese paper-card prose, also use [`chinese-technical-writing`](../chinese-technical-writing/SKILL.md). Preserve official English source text in `英文原文稿`, formulas, method/model/dataset names, and symbols, but do not leave ordinary technical concepts as raw English phrase islands in Chinese prose.

## Borrowed Method Layer

This is the user's canonical deep-dive workflow. It may borrow useful reading methods from downloaded skills, but those skills do not own the final package semantics or target-platform representation.

- From `nature-reader`, borrow the source-map-first method: build stable source
  block IDs such as `S001`, `F001`, `T001`, preserve original / Chinese
  correspondence, keep figure/table captions attached to the relevant text, and
  record uncertainty instead of guessing.
- Do not publish the external `nature-reader` artifact contract as-is. A lone `paper.md`, `source_map.json`, `translation_notes.md`, or bilingual reader does not replace the required main entry plus two complete manuscript artifacts. These files may be intermediate material or part of an explicitly requested Obsidian package.
- Use the source map as an internal scaffold for `英文原文稿`, `原文中译稿`, and source-grounded main-entry `精读稿`. The final deliverable must still follow the main-plus-two-linked-artifact structure and use the selected platform's native images/captions, formulas, hierarchy, and read-back verification through `research-doc-workflow`.
- In the main-entry `精读稿`, short bilingual source snippets or block IDs may
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
- Converting PDF extraction into a complete English original manuscript artifact, a complete faithful Chinese translation artifact, main-entry Chinese close-reading notes, an editable paper-analysis tree, and a paper card.
- Preparing Obsidian, Notion, or Feishu paper pages/notes.
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

If a separate appendix/supplementary PDF exists, it is part of the deep-dive source package unless the user explicitly excludes it. Download/parse it alongside the main PDF, include its sections, figures, tables, formulas, captions, algorithms, and references in the source map, and reflect it in both `<paper short name>｜英文原文稿` and `<paper short name>｜原文中译稿`. A deep dive based only on a conference main PDF is incomplete when a separate supplement exists and has not been inspected.

Record the source package in task notes and compact source metadata: arXiv ID/version when available, arXiv PDF status, arXiv HTML URL/status, LaTeX source status, publisher/proceedings/OpenReview/CVF HTML URL/status, venue/publisher PDF status, supplementary/appendix PDF status, project/code links, and extraction date. If no HTML version is found, state the searched routes briefly; do not write `HTML not checked`. If no supplement is found, state the searched routes briefly; do not write `supplement not checked`.

## Workflow

1. Capture source metadata and source package inventory: title, authors, year, venue, DOI/arXiv, arXiv PDF URL/status, arXiv HTML URL/status, LaTeX source status, publisher/proceedings/OpenReview/CVF HTML URL/status, venue/publisher PDF URL, supplementary/appendix PDF URL(s), project/code links, local source paths, and extraction date.
2. Extract or parse the complete source package to inspectable Markdown when tooling is available; preserve figure references and equation context. On this machine, use MinerU as the default PDF-to-Markdown path before building deep-dive artifacts, but parse official HTML / LaTeX first when available for source structure, formulas, captions, references, and appendix coverage. Parse the arXiv/full manuscript first when available, then parse any separate supplement/appendix PDF.
3. Check the MinerU conversion draft against official HTML whenever HTML exists, especially arXiv HTML for arXiv papers and publisher/proceedings HTML for non-arXiv papers. This check is mandatory, not optional. Repair section order, paragraph continuity, formulas, figures, tables, captions, appendices, body citations, and references before publishing.
4. Build a source map inspired by `nature-reader`: stable block IDs for body text, figures, tables, captions, equations, appendices, and references; page / section location; extraction confidence; and links between first figure/table mention and the visual asset.
5. Create the complete English original manuscript artifact (`<paper short name>｜英文原文稿`) from the verified official paper source. This means the paper's original English text in source order, not a structural outline, not selected excerpts, and not an English summary. If an official PDF or full-paper HTML is accessible, this artifact must be completed by section-level chunking and source verification before the deep dive is marked complete.
6. Create the complete faithful Chinese manuscript artifact (`<paper short name>｜原文中译稿`) from the verified English manuscript in source order. It must preserve section hierarchy, paragraph correspondence, formulas, figure/table positions, citations, captions, references, and layout structure as much as the target editor allows. Translate the paper body, captions, and explanatory prose into Chinese, but keep the References / bibliography entries in their original English form. A partial translation is allowed only as a clearly marked WIP state; it is not a final deep-dive deliverable.
7. Check terminology in the Chinese manuscript. Technical terms should be translated accurately; important terms and proper nouns should appear as `中文（English term）` on first use or where clarity is needed. Avoid leaving large runs of English technical terms untranslated in Chinese prose.
8. Create or update the main reader-facing deep-dive entry. It must contain, in order: paper card, `论文解析树`, and `精读稿`.
9. Create an editable `论文解析树` that follows the paper's actual reasoning: problem -> concrete bottleneck -> key assumption -> design/mechanism -> changed information or constraint -> predicted effect -> decisive evidence -> boundary. Make the information-flow view (what passes between modules) and the causal-chain view (why the design should change the result) distinguishable. Add losses/training, datasets/evaluation, limitations, and user research implications where they clarify this logic rather than as disconnected inventory branches. Use a native Feishu mind map for Feishu, a structured page/database or supported embedded artifact for Notion, and Mermaid/Canvas plus a searchable linked outline for Obsidian. Do not substitute a static screenshot when an editable representation is available.
10. Create the main-entry `精读稿` as a source-order analytical close reading, not a thematic essay. Follow the paper's own section order and local context: Abstract / Introduction, numbered sections, named subsections, conclusion, then appendices or supplementary material. For each part, explain which claim it advances, why that step is needed, what mechanism or evidence is introduced, and what remains unresolved. Preserve local source context instead of forcing the same audit questions into every subsection. Do not insert a repeated per-section heading or paragraph such as "what this means for my world-model research" / "对你的 world model 研究意味着什么"; that lens distorts the source-order reading. Put user-specific research implications, world-model / embodied-world-model takeaways, and future project ideas only in a final synthesis section after the source-order close reading. This is interpretation and learning material; do not present it as the complete translation. Ground important analysis in source-map block IDs or short bilingual snippets when useful.
    - Inside `精读稿`, use `###` or lower-impact paragraph/list structure for source-order close-reading subsections. Do not use `####` headings for close-reading subsections on a main entry that also contains paper cards, because `####` is reserved for paper-card titles and is checked by `paper-card-delivery` validators.
11. After the source-order close reading, write one integrated mechanism synthesis. Its headings may vary with the paper, but it must cover the strongest author argument, assumptions and falsifiable predictions, claim-evidence-alternative-explanation alignment, counterfactual ablation predictions, minimal necessary design, failure boundaries, and a discriminating next research question. Add user-specific transfer only at the end and only when it follows naturally from the paper.
12. Create a paper card using [`paper-card-delivery`](../paper-card-delivery/SKILL.md), then run its validator on the Markdown draft when a local draft exists.
13. Store figures and assets in a stable assets folder.
14. Mark author claim, experimental support, inference, citation needed, and unresolved questions separately.

Paper-card content standards live in [`paper-card-delivery`](../paper-card-delivery/SKILL.md). This deep-dive skill must not duplicate or override paper-card source verification, metadata, image/caption selection, fixed bullet slots, sorting, or structural validation.

## Local MinerU Extraction

For future deep dives, first create a MinerU conversion draft when a PDF is available. Use it as the source-order manuscript scaffold for `<paper short name>｜英文原文稿`, `<paper short name>｜原文中译稿`, and the main-entry `精读稿`.

- Preferred wrapper in this vault: `$WORLD_MODEL_VAULT/.tools/mineru-md.sh`
- MinerU binary on this machine: `$WORLD_MODEL_VAULT_MINERU_BIN`
- Verified local version: `mineru 3.3.1`
- Store MinerU outputs, downloaded PDFs, supplementary/appendix PDFs, official HTML snapshots/pages, arXiv HTML, LaTeX source, and temporary figure assets under `.tools/tmp/codex/<task-slug>/`; delete them after the target artifacts are written and verified successfully.
- MinerU is a conversion draft, not the authoritative final text. When an official HTML version exists, always check the MinerU draft against it before publishing target artifacts. For arXiv papers, arXiv HTML is the preferred HTML check; for non-arXiv papers, use publisher/proceedings/OpenReview/CVF HTML when available. Verify section order, paragraph continuity, equations, figures, captions, tables, appendices, citations, and references. If HTML is unavailable or incomplete, use official LaTeX source or the official PDF as the authority and record that HTML could not be used.
- If MinerU misses or corrupts formulas, figures, captions, appendices, or references, repair from official HTML/LaTeX/PDF or the official publisher source before marking the deep dive complete.
- If MinerU itself fails but the PDF is accessible, try the local wrapper again with a clean output directory, inspect the error, and then use a structured fallback such as official HTML/LaTeX, publisher HTML, Docling, Marker, PyMuPDF, or pdfplumber. MinerU failure is a workflow problem to resolve or work around, not permission to ship manuscript summaries.

## Manuscript Fidelity Requirements

- `<paper short name>｜英文原文稿` and `<paper short name>｜原文中译稿` must preserve paper-like citation flow. Body citation markers must remain where they appear in the source, using the source style when feasible, such as `[12]`, `[Author et al., 2025]`, or `(Author et al., 2025)`.
- Both manuscript artifacts must cover the full paper source package that the user is trying to deep dive: Abstract, Introduction, all numbered / named main sections, Conclusion / Discussion, appendices, supplementary sections/materials, figure and table captions, algorithms when present, and References. If the conference/publisher PDF omits appendices but arXiv or a separate supplement contains them, include those materials unless the user explicitly excludes them. If the user explicitly excludes appendices or supplementary material, record that exclusion in the affected artifact and final report.
- Before marking complete, compare both manuscript artifacts against the official source section list. Missing sections, reordered sections, dropped captions, collapsed tables, omitted algorithms, or absent References make the artifacts incomplete.
- The References section must be a numbered bibliography, not a bullet list. Use ordered lists or the target platform's numbered-list blocks, keep one reference per item, and preserve the original English bibliography text. Do not translate paper titles, venues, publisher names, author names, page ranges, DOI/arXiv strings, or other reference-entry fields into Chinese.
- Figures and tables must be placed near their original reference/caption positions. Use native Feishu/Notion image blocks or stable relative Obsidian assets when reliable official image assets are available.
- Attach captions using the selected platform's native or established representation: native image captions in Feishu/Notion, and the vault convention or meaningful alt text in Obsidian. Captions with formulas may use an immediately adjacent formula-capable block when the native caption cannot preserve TeX; preserve the exact TeX source and do not duplicate the caption.
- Figure captions are source-fidelity content. English original pages must preserve the official original caption, and Chinese manuscript pages must use a complete Chinese translation of that caption. Do not replace captions with agent-written summaries such as `方法或实验概览` / `method or experiment overview`, source-process notes, or generic explanations such as `用于说明论文的核心流程、输入输出关系和关键模块`, `原始 caption 已在图中保留`, or `便于回溯核验`. If a source tag is useful, keep only a short controlled label from `paper-card-delivery`, such as `来源：用户截图`, `来源：HTML`, `来源：MinerU PDF 截图`, or `来源：PDF 截图`.
- Formulas must be checked against official HTML/LaTeX/PDF and preserved in LaTeX where possible. This includes inline formulas, not only displayed equations. Do not publish pages where important equations, inline variables, losses, or symbolic expressions have collapsed into prose or lost subscripts/superscripts.
- The complete Chinese manuscript follows the same fidelity requirements as the English original manuscript: original section order, paragraph correspondence, figure/table positions, formula placement, body citations, numbered references, captions, appendices, and table structure. The Chinese manuscript's References section remains the original English bibliography, even though the main body is translated.
- Chinese terminology must be deliberate. Translate technical terms into accurate Chinese, keep method/model/dataset names and symbols unchanged when they are names, and write important terms as `中文（English term）` when first introduced. Do not leave dense English terminology untranslated in ordinary Chinese explanatory prose.

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

- Main entry: title must be the official paper/article title only. Do not append status suffixes such as `中文`, `深度笔记`, `学习页`, `Deep Dive`, `阅读笔记`, or `解析`. The main entry contains exactly the durable reader-facing synthesis: `Paper Card`, editable `论文解析树`, and `精读稿` on the same page/note. The paper card and tree should include metadata, source-verified pipeline/process/computation-flow figure(s), one-sentence conclusion, core problem, method/pipeline summary, experiments, limitations, and implications. The `精读稿` must first follow the paper's source order and original argumentative context; user-specific research takeaways belong in one final synthesis section.
- Linked artifact 1: `<paper short name>｜英文原文稿`, the complete original English manuscript from official PDF/HTML/LaTeX/MinerU extraction. Do not replace it with an extraction-status page when the official PDF or full-paper HTML is accessible.
- Linked artifact 2: `<paper short name>｜原文中译稿`, the complete faithful Chinese manuscript / translation. Use this name instead of `中文原文稿`, `完整中文稿`, or `原文译稿` for new artifacts.

Platform mapping:

- Feishu/Lark: one parent wiki page plus two child pages, native image captions/equations, and a native whiteboard mind map.
- Notion: one parent page plus two subpages or related database entries, native image captions/equations, and an editable structured tree or supported embed.
- Obsidian: one main note plus two linked Markdown notes in a stable folder, relative assets, LaTeX math, and Mermaid/Canvas plus a searchable outline for `论文解析树`.

Choose `<paper short name>` as the shortest unambiguous paper identifier already used by the community or the paper itself, such as method acronym, article short title, or arXiv/project name. Do not use the full official title for linked manuscript artifacts when it makes the title unwieldy.

Do not create a separate `中文精读稿` linked artifact by default. The close-reading notes belong on the main entry as `精读稿`. Do not replace the two original-manuscript artifacts with an outline, section summary, or mixed translation/interpretation page.

Remove obsolete process/status scaffolding from reader-facing main entries. Sections such as `Source Extraction`, `Deep Dive Structure Status`, long extraction inventories, local MinerU availability notes, and self-referential statements about which linked artifact is complete are working notes, not deep-dive content. Keep durable source links in a compact `来源` section when useful.

Use:

- `Paper Metadata`
- `Extraction Result`
- `English Original Manuscript`
- `Faithful Chinese Manuscript`
- `Editable Paper Analysis Tree`
- `Chinese Close Reading Notes on Main Entry`
- `Paper Card`
- `Assets`
- `Open Questions`
- `Sync Checklist`

## Guardrails

- Do not fabricate paper content when extraction is incomplete.
- Do not merge translation, interpretation, and speculation without labels.
- Do not call a page `英文原文稿` unless it is named `<paper short name>｜英文原文稿` and contains the original English paper text in source order.
- Do not call a page `原文中译稿` unless it is a complete, faithful translation of the source paper rather than a close-reading note. For legacy pages named `中文原文稿`, rename them to `<paper short name>｜原文中译稿` when repairing the hierarchy.
- Do not mark a deep dive complete if either manuscript artifact is partial, section-summary-only, selected-excerpt-only, missing References, missing appendices included in the PDF, or missing major figures/tables/captions from the source paper.
- Do not mark a deep dive complete when HTML availability has not been searched and recorded. If official HTML exists, the MinerU/PDF draft must be checked against it; if HTML is unavailable or incomplete, record the searched routes and fallback authority.
- Do not mark a deep dive complete when the source was taken from a conference/publisher PDF and supplementary/appendix material has not been searched. If separate supplementary material exists, the deep dive is incomplete until it is parsed, incorporated, or explicitly excluded by the user.
- Do not create a source-link / extraction-status artifact as a substitute for `英文原文稿` or `原文中译稿` when the official PDF or full-paper HTML is accessible. Use that fallback only for genuine source access or licensing blockers, and label the whole deep dive as blocked / incomplete.
- Do not treat long papers as a reason to reduce scope. Split the manuscript and translation by source sections, append incrementally, and verify coverage before final delivery.
- Do not create a separate `中文精读稿` artifact unless the user explicitly asks; the default close-reading deliverable is the main-entry `精读稿`.
- Do not cite figures or equations that were not actually extracted or inspected.
- Do not present a paper card as finished unless its problem, method, implementation, conclusion, limitations, and figure claims are grounded in the official full paper; use `Not reported`, `N/A`, or `待核验` instead of guessing.

## Manuscript Completion Gate

Before declaring a deep dive compliant, re-fetch or re-read the main entry and both linked manuscript artifacts, then verify:

- The main entry links exactly the two required manuscript artifacts and contains `Paper Card`, editable `论文解析树`, and `精读稿`.
- `<paper short name>｜英文原文稿` contains the original English source text in paper order, not a summary or outline.
- `<paper short name>｜原文中译稿` mirrors the English manuscript section by section and paragraph by paragraph as closely as the editor allows.
- Official source sections, captions, tables, algorithms, appendices, body citations, and References are present or explicitly excluded by the user.
- Source package inventory records arXiv availability, HTML URL/status, venue/publisher PDF status, and supplementary/appendix search result; arXiv HTML / LaTeX / full manuscript sources were preferred when available, and any HTML fallback or absence is explicitly recorded.
- Formulas and inline symbols survive source verification against official HTML/LaTeX/PDF samples from early, middle, formula-heavy, and appendix sections.
- The editable tree and `精读稿` expose both information flow and the causal chain from bottleneck through mechanism to predicted effect and evidence.
- The synthesis identifies the decisive evidence, relevant alternative explanations, and at least one counterfactual prediction for removing or simplifying a claimed key design.
- The reader can explain where the paper's assumptions stop applying and why; a section-by-section paraphrase without this mechanism audit is incomplete.
- Any remaining missing section, figure, table, formula, or translation block is reported as an incomplete WIP item; do not call the package finished.
