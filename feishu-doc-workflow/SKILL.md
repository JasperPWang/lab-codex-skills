---
name: feishu-doc-workflow
description: Feishu/Lark document and wiki workflow for reading, editing, structuring, and verifying docs, wiki pages, paper cards, meeting notes, deep dives, images, and drive-native Markdown through the local `lark-cli`. Use when the user provides a feishu.cn/larksuite.com document or wiki URL, asks to read or edit 飞书/Feishu/Lark content, asks to maintain Feishu paper cards or meeting pages, mentions 飞书文档/飞书知识库, or needs authenticated Feishu document updates with hierarchy, image, and post-write verification rules.
---

# Feishu Doc Workflow

## Overview

Use the local `lark-cli` for Feishu/Lark document work. This skill is a document workflow, not just a CLI wrapper: preserve hierarchy, content structure, image dimensions, and post-write verification. Prefer CLI reads and writes over browser automation for Feishu links because this machine already has CLI auth configured.

## Quick Start

Use the installed command:

```bash
~/.local/bin/lark-cli --help
```

Read a document or wiki URL:

```bash
~/.local/bin/lark-cli docs +fetch \
  --api-version v2 \
  --doc '<feishu-or-lark-url-or-token>' \
  --as user \
  --format json
```

Edit a document:

```bash
~/.local/bin/lark-cli docs +update \
  --api-version v2 \
  --doc '<feishu-or-lark-url-or-token>' \
  --as user \
  --mode append \
  --markdown '@file.md'
```

## Workflow

1. Fetch first. Capture the returned `document_id`, `revision_id`, title, and relevant content before writing.
2. Choose the smallest safe write mode:
   - `append` for adding new sections.
   - `insert_before` or `insert_after` with `--selection-by-title` or `--selection-with-ellipsis` for targeted insertion.
   - `replace_range` for a known span.
   - `replace_all` or `overwrite` only when the user explicitly wants a full rewrite.
   - Never use `docs_ai` / `docs +update --command overwrite` for metadata-only edits on an existing page that contains images, grids, tables, whiteboards, formulas, or other rich blocks. Even if the fetched XML keeps `<img>` tags, Feishu may recreate or reflow the native image blocks and visibly move the user's images. For paper-card metadata changes, use block-level text updates, exact visible-text `str_replace`, or ask the user to restore the page version before retrying.
   - For existing content, prefer modification over rewriting: use Docx block API text updates, exact text replacement, or targeted block insertion/deletion. Do not rebuild an entire card, section, grid, or page just to change wording, metadata, captions, formulas, or other local content.
3. Preserve existing images, tables, grids, and rich content unless the user explicitly asks to restructure them.
   - Treat the user's current visual arrangement as intentional. If images are in the same row, grid, callout, or adjacent image group, preserve their order, parent block, column/grid ratios, relative widths, `scale`, `align`, captions, and spacing. Do not normalize two side-by-side images to the same width, move them into separate rows, or rebuild their container unless the user explicitly asks for a layout change.
4. For images, do not create or rewrite them by embedding raw XML `<img>` tags in document content. Use `docs +media-insert` with local image files and a text selection so Feishu creates native image blocks that keep the source image aspect ratio.
5. When any write may touch existing image blocks, fetch with `--detail full` before editing and preserve every image's native `width`, `height`, `scale`, `src`, caption, alignment, parent/container relationship, sibling order, and any grid column-width ratios. Treat `width` and `height` as the original-resolution pixel dimensions / aspect-ratio contract, and treat `scale` / grid ratios as the user's visible layout contract, not decorative metadata. Never let an image fall back to Feishu's default `512 × 512` square sizing, and never square-crop, force square dimensions, equalize side-by-side image widths, or reflow a multi-image row unless the user explicitly asks.
6. If a fetched image block lacks trustworthy `width` / `height`, download the image from its authenticated `href` or file token, inspect the actual pixel dimensions, and write those dimensions back into the image block before overwriting the page. After writing, fetch again with `--detail full` and verify that every touched image's `width` / `height` still matches the preserved or inspected dimensions.
7. If an accidental XML overwrite has already recreated images as `512 × 512` blocks, do not repair by another whole-page overwrite. Use the Docx block API and an older readable `document_revision_id` instead:
   - Read old and current blocks from `/open-apis/docx/v1/documents/<docx_token>/blocks?document_revision_id=<rev>`.
   - For each image, download the old image token to a task-local temp directory, upload it to the current image block with `docs +media-upload --parent-type docx_image --parent-node <current_image_block_id>`, then `PATCH /blocks/<current_image_block_id>` with `replace_image.token`, original `width`, `height`, `scale`, `align` when present, and caption.
   - For grids, patch the current grid block, not individual grid columns: `update_grid_column_width_ratio: {"width_ratios":[...]}` using ratios read from the old grid's child columns.
   - Verify image count, no unintended `512 × 512` images, original width/height/scale/caption, grid ratio parity, and paper-card metadata count. Feishu may normalize missing image `align` to `align=2`; do not chase that field if all visible geometry metadata is restored.
8. Use `--dry-run` before risky writes or when the selection may be ambiguous.
9. Fetch again after writing to verify the update.
10. After `docs +update --command overwrite`, the doc/Wiki node title may stay `Untitled` unless you set it. Prefer `--new-title 'Page Name'` on the same update when the CLI accepts it; otherwise rename via Drive API:

```bash
lark-cli api PATCH "/open-apis/drive/v1/files/<docx_token>" \
  --as user --params '{"type":"docx"}' \
  --data '{"new_title":"Google Dreamer"}'
```

Use the doc token from `docs +fetch` or `wiki spaces get_node` (`obj_token`). Confirm with `wiki spaces get_node --params '{"token":"<wiki_node_token>"}'`.
Do not trust `--new-title` alone after an overwrite. Always fetch the doc and the wiki node after large writes and verify both:

```bash
lark-cli docs +fetch --api-version v2 --doc '<docx_token>' --as user --format json
lark-cli wiki spaces get_node --as user --params '{"token":"<wiki_node_token>"}'
```

If either title is `Untitled`, immediately run the Drive PATCH above with the `obj_token`/docx token and verify again. For origin wiki nodes, updating the Drive docx title normally updates the wiki node title as well.

## Workspace Hygiene

- Do not create Feishu-editing scratch files in the vault root. This includes fetched JSON, intermediate Markdown/XML, link-check scripts, generated paper-card scripts, screenshots, and one-off validation outputs.
- Put all temporary files for a Feishu task under a hidden working directory such as `.tools/tmp/codex/<task-slug>/` or the system temp directory, and remove them after the Feishu page has been verified.
- For literature or paper-card work, do not keep local copies of source PDFs, arXiv HTML pages, downloaded project pages, extracted PDF text, OCR/MinerU outputs, or temporary figure assets. Prefer reading official HTML/full-paper pages directly. If a PDF/HTML/source asset must be downloaded for extraction or verification, store it only under a task-local temporary directory, use it to write the Feishu content, fetch the Feishu page to verify the durable copy, then delete the downloaded source and extracted intermediates before finishing.
- If an artifact should be kept for audit or reuse, store it under an explicit non-root location such as `.tools/outputs/<task-slug>/` and mention it to the user. Do not leave opaque files like `sovd_current.md`, `*_after.json`, or ad-hoc Python scripts in the root of `WorldModelVault`.
- Before finishing a Feishu editing task, check for task-local scratch files and clean them up unless the user asked to keep them.

## Paper Card Images

When syncing paper cards to Feishu, use only reliable paper figures as card images:

- Prefer the paper's core method/process figure with matching captions: method, pipeline, framework, system overview, architecture, data flow, benchmark construction, score/loss/computation flow, or other figures that explain how the work operates.
- Do not use a teaser, qualitative showcase, result collage, demo gallery, or visual example grid as the only paper-card image when a core method/process figure exists in the official paper HTML/PDF or project page. A teaser may be kept only as a second supplementary image when it adds distinct context, and its caption must label it as `teaser` / `结果展示` rather than presenting it as the method figure.
- When auditing or repairing existing paper cards, if the only image is a teaser/result showcase and a core method/process figure is available, insert or replace with the core figure first. Preserve the teaser only when the card can support a second image without clutter and it adds information the core figure does not.
- If no core method/process figure exists after checking the official paper HTML/PDF/project page, state that explicitly in the caption or note and use the most structurally informative fallback figure; do not silently present a teaser as the method image.
- Reject paper first pages, title pages, abstract pages, arXiv page screenshots, and generic PDF page renders as card images.
- Do not fall back to the largest raster image when no credible figure is found.
- When the user provides a paper figure image or screenshot, especially a manually captured image with the original caption visible, treat the visible caption as source text for the Feishu image caption. Translate the complete original caption into Chinese, preserve the figure number, subfigure labels, symbols, method names, dataset names, and important English technical terms when needed, and write it into the native image caption / description, e.g. `图 2｜完整中文图注：...`.
- Official HTML is also a valid caption source. For arXiv HTML, publisher / conference HTML, and official project pages, search the page's `figure` / `figcaption`, nearby figure labels, image alt text, and visible figure descriptions before using the PDF. Translate the verified original figure caption fully into Chinese for the Feishu native image caption. Do not shorten it to a title such as `图｜GS-IR overview`, `图｜pipeline`, `图｜teaser`, or a self-written summary. Do not use unrelated page prose as a figure caption unless it is clearly tied to that exact figure.
- A finished paper-card image caption must be the complete Chinese translation of the source figure caption. It is incomplete if it only contains a figure title, method name, local filename, English overview phrase, or a brief label without the caption content. If Feishu native caption length becomes a real limitation, keep the native caption as `图 N｜完整图注见下方` and place the full Chinese translated caption in the immediately following paragraph.
- Do not invent caption content that is not visible in the provided image or verified from the official paper / project page. If the screenshot has no readable caption and no official caption has been checked, write `图注待补：需要从论文或项目页核验并完整翻译原始 caption。`.
- Reuse user-captured or previously verified paper-card figures for the same paper before extracting or cropping a new one. Match by stable paper identity such as English title, arXiv ID / DOI, method name, and figure number or caption; do not rely on local filenames alone.
- When the same paper card is used on multiple Feishu pages, preserve the already approved image and Chinese caption unless a page-specific reason requires a different figure. If copying from an existing Feishu card, fetch with full detail when needed and preserve the native image block / caption rather than rebuilding the figure from the paper.
- If a user-provided screenshot should be reused across pages, keep a reusable copy under an explicit non-root library such as `.tools/outputs/paper-card-figures/<paper-id-or-normalized-title>/`. These retained user-captured figure assets are not disposable extraction intermediates, but OCR text files, processing outputs, and task-local duplicates must still be deleted after Feishu verification.
- For new images inserted with `docs +media-insert`, pass `--caption '<Chinese caption>'`; this writes the native Feishu image caption, not just a normal paragraph.
- Insert or preserve paper-card figures using the image's original pixel width and height. If the figure is copied from an existing Feishu page, carry over the full-detail image metadata; if it is inserted from a local/user-provided file, inspect the local file dimensions before upload and verify the resulting Feishu block keeps the same aspect ratio. Do not allow automatic square placeholders such as `512 × 512` to become the final card image size.
- If an existing paper card has multiple images in one visual row, grid, or adjacent group, preserve that relationship exactly. Do not rebuild the group, equalize image widths, alter grid ratios, or split/merge rows while normalizing text, metadata, captions, or bullet content. A same-row two-image layout is user-authored layout state, not disposable formatting.
- For existing image blocks, prefer an in-place Docx API update instead of re-uploading or reinserting the image: call `PATCH /open-apis/docx/v1/documents/<docx_token>/blocks/batch_update` with `replace_image.token` set to the existing image `src` / file token and `replace_image.caption.content` set to the Chinese caption. Fetch with `--detail full` first to get the image block id, token, width, height, scale, and current caption; include the existing `scale` in `replace_image` so adding a caption does not resize the image.
- Only if the native caption / description API is unavailable or fails, insert a normal Chinese caption paragraph immediately below the image and keep it visually tied to that image; mention this fallback to the user.
- If OCR or visual extraction is used to read a screenshot caption, delete OCR text files, image-processing intermediates, and temporary figure assets after the Feishu write has been fetched back and verified.
- In a Feishu paper card, place the native image block after the metadata paragraph link line (`PDF｜Project｜Code`) and `Dataset`, before the fixed bullet slots. Do not leave the image directly under the `####` title.
- If no reliable core method/process figure is available, write `配图待补：需要从论文 HTML/PDF 或项目页补充可信方法流程图；teaser / 结果展示图不能单独作为主图。` instead of inserting a questionable image.
- Do not leave Obsidian migration residue such as `图像： EW_IMG_...png`, `Image: assets/...`, local file names, or local vault paths in the reader-facing Feishu page. After inserting the actual figure as a native Feishu image block, keep only the Chinese figure caption or explanation that helps the reader; remove local filename labels.
- Before syncing a paper-card source file, run a text check for `first page`, `first-page`, `title page`, and `paper page`; after syncing, fetch the Feishu page and verify those strings are absent unless they are part of normal prose.
- After syncing a paper-card page, fetch it and verify that visible body text contains no `图像：`, `EW_IMG`, `assets/`, `![[`, or local filesystem paths. Image block `name` attributes may still contain source filenames; those are acceptable if they are not visible body text.

## Meeting Notes

When organizing dated research-group meeting pages in Feishu, use the user's dated Feishu child page as the durable source and destination. Do not create or keep full meeting content in the local Obsidian vault unless the user explicitly asks.

- Name dated meeting pages with a zero-padded date plus short topic keywords, following sibling-page style: `YYYY-MM-DD <topic keywords>`, for example `2026-06-30 3D场景编辑实验复盘`. Do not leave the page as a bare date such as `2026-6-30` unless the user explicitly asks. Infer the topic keywords from the personal notes, transcript title, PDF links, or dominant discussion topic; keep the H1 aligned, e.g. `<page title>｜组会整理报告`. After renaming or overwriting, verify both the document title and the Wiki node title.
- Expect two raw inputs on the dated child page: the user's personal notes and the Doubao / 豆包 transcript `.txt`. The personal notes are the primary source for importance, paper links, figures, live thoughts, teacher feedback, and intended interpretation. The transcript is secondary evidence for chronology, missing discussion details, exact wording, TODOs, and speaker-flow reconstruction.
- If the personal notes and transcript conflict, trust the personal notes first. Mark transcript-only or uncertain claims as `转写疑似` / `待核验` rather than turning them into facts.
- Preserve both raw materials in the Feishu page. Write the organized report above or before the raw sections, and keep clear source sections such as `原始材料：个人笔记` and `原始材料：豆包转写`. Do not delete or overwrite the user's raw notes or transcript.
- Use this default report structure: `组会整理报告`, `Paper Cards`, `保守纪要`, `讨论脉络 / 老师反馈`, `会后头脑风暴`, `TODO`, `原始材料：个人笔记`, `原始材料：豆包转写`.
- For papers mentioned in the personal notes or transcript, create or normalize paper cards using the fixed Feishu paper-card format. Use the user's provided PDF links and figures when present, preserve image dimensions with full-detail metadata, and mark missing `Dataset`, `定义`, or `结论` as `待核验` unless official sources have been checked.
- Treat `保守纪要` and `会后头脑风暴` differently. The conservative notes must stay grounded in the personal notes, transcript, paper links, and visible figures. The brainstorm section may intentionally connect the meeting to JEPA, world models, 3DGS, avatar, long-tail learning, music generation, origami art, or other group topics, but it must be labeled as brainstorming rather than transcript fact.
- End with concrete TODOs from the meeting plus any follow-up paper-card verification tasks. Fetch after writing and verify that the report sections exist, raw-material sections remain, image dimensions are preserved, and the wiki child page title/hierarchy did not change.

## Single Paper Deep Dive

When the user asks to deep dive, 深读, detailed-read, or 详细解析 a single paper, create the finished deliverable in the user's personal Feishu document library by default. Do not default to writing the deep dive into Obsidian.

- Treat any single-paper `deep dive` request as the full deep-dive workflow by default. Do not downgrade it to a quick summary, paper card only, or close-reading note only unless the user explicitly asks for a lighter output.
- Feishu single-paper deep dives default to a fixed parent-plus-three-child structure. Do not collapse the English original manuscript, complete Chinese translation, and close-reading notes into one page.
- The required child deliverables are `英文原文稿`, `原文译稿` / `完整中文稿`, and `中文精读稿`.
- `英文原文稿` is the paper's original English text in source order. It is usually produced from the MinerU conversion draft, then checked against official HTML / LaTeX / PDF. It must preserve figure/table positions, formulas, captions, appendices, body citation markers, and a numbered References section. It is the working source for translation and can be deleted after translation if the user later asks.
- `原文译稿` / `完整中文稿` is the complete faithful Chinese manuscript. It preserves the source paper's section order, paragraph correspondence, formulas, figure/table positions, body citation markers, captions, numbered References section, and layout structure as much as Feishu allows. It also requires accurate terminology: important terms and proper nouns should be translated as `中文（English term）` on first use or where clarity is needed, while method/model/dataset names and mathematical symbols remain unchanged. Avoid leaving dense English technical terms untranslated in ordinary Chinese prose.
- `中文精读稿` is an analytical Chinese reading guide. It follows the source paper's original section order by default: Abstract, numbered main-paper sections, named subsections, conclusion, then appendices / supplementary material. Do not reorganize the close-reading page into a purely thematic guide unless the user explicitly asks for a theme-based reader.
- If any required child deliverable cannot be produced because the source PDF is inaccessible, parsing fails, the official HTML is unavailable or incomplete, licensing/copyright constraints apply, or the document is too long for the current tool path, stop and tell the user what is blocking completion. Do not silently downgrade to a simplified reader or mislabeled excerpt page. Continue only after the user chooses an acceptable fallback or provides a source that can be processed.
- Use a Feishu parent/child hierarchy:
  - Parent page: the deep-dive notes. This is the main reader-facing page and should contain the paper card / metadata, one-sentence conclusion, paper positioning, technical challenge, core insight, method / pipeline breakdown, losses or training details, datasets and evaluation, key experiments and ablations, limitations, related latest progress or critique, and implications for world-model / embodied-world-model research.
  - Child page 1: English original manuscript (`英文原文稿`), containing the original English paper text in source order, with formulas, figure/table positions, captions, appendices, citations, and references preserved as much as Feishu allows.
  - Child page 2: complete Chinese manuscript (`原文译稿` / `完整中文稿` / `Full Chinese Translation`), translated sentence by sentence where available and preserving formulas, figure/table placements, citations, captions, and the paper's original image order. Insert paper figures as native Feishu image blocks near their original figure captions whenever reliable official images are available. Follow the Formula / Equation Handling rules below; do not rebuild formulas from already-flattened Feishu plain text.
  - Child page 3: Chinese close-reading page (`中文精读稿`), with section-level reading notes following the paper's original structure, plus local method decomposition, figure/table guide, key assumptions, experiments, limitations, and research implications inside the corresponding original sections.
- Before writing the notes, read/parse the paper and search for current context when needed: arXiv/OpenReview/conference page, project page, GitHub, author page, follow-up papers, critiques, benchmarks, and directly related concurrent work.
- Prefer MinerU for PDF-to-Markdown parsing. On this machine, use `$WORLD_MODEL_VAULT/.tools/mineru-md.sh` first, backed by `$WORLD_MODEL_VAULT_MINERU_BIN` (`mineru 3.3.1` verified). Use Docling / Marker / PyMuPDF / pdfplumber only if MinerU fails or there is no PDF.
- Treat MinerU output as a conversion draft, not the final authority. For arXiv papers, check the MinerU draft against arXiv HTML whenever available before publishing Feishu pages. Verify section order, paragraph continuity, formulas, figures, captions, tables, appendices, citations, and references. If arXiv HTML is unavailable or incomplete, use official LaTeX source, publisher HTML, or the official PDF as the authority.
- References must be repaired before publishing. Do not leave bibliography entries as fragmented paragraphs or bullets; use a numbered bibliography, keep one reference per numbered item, and preserve body citation markers so the manuscript reads like the original paper.
- Do not upload or store a PDF when a stable arXiv PDF exists, unless the user explicitly requests a PDF copy or the source is unstable/non-arXiv.
- After the Feishu deep dive is done, distilled knowledge may be summarized into Feishu knowledge pages. Only content still judged long-term important after distillation should be added back to Obsidian.
- Verify final Feishu hierarchy: the parent notes page has exactly the intended child pages for `英文原文稿`, `原文译稿` / `完整中文稿`, and `中文精读稿`, and the parent page links to them.

## Formula / Equation Handling

For paper deep dives and complete manuscript pages, formulas are source-fidelity content, not prose to paraphrase.

- Extract formulas from the official full-paper source before writing. For arXiv papers, prefer arXiv HTML / LaTeX source because it usually preserves MathML, TeX annotations, equation IDs, and numbering; use the PDF or a structured PDF parser only as fallback. Do not reconstruct formulas from collapsed Feishu plain text or OCR text when the official formula source is available.
- Preserve mathematical structure in LaTeX: subscripts, superscripts, hats, dots, norms, fractions, sums, products, matrices, Greek symbols, calligraphic symbols, equation numbers, and variable names. Translate surrounding prose, but do not translate variable identifiers or LaTeX commands.
- Preserve inline formulas as source-fidelity content, not just displayed equations. Inline variables, operators, compact expressions, loss names, author references to equations, and symbolic phrases such as `$S$`, `$G$`, `$l(S)$`, `$\bm{x}^{n}$`, or `$\mathcal{L}_{\text{RGB}}$` must remain inline LaTeX. Do not flatten them into ordinary text, translate them into Chinese words, wrap them in backticks, or rebuild them from Feishu/OCR plain text.
- During translation, protect all inline and displayed formulas with non-translatable placeholders, translate only the surrounding prose, then restore the exact TeX from the official source. If using arXiv HTML, prefer each `math.ltx_Math` / MathML `alttext` or TeX annotation for inline formula source; verify the restored count and representative samples after translation.
- In Markdown sources for Feishu import, use `$...$` for inline variables and `$$...$$` for display equations. Keep display equations on their own lines with blank lines before and after. Do not wrap formulas in backticks or code fences unless explicitly creating a raw-LaTeX fallback section.
- In `中文精读稿` / close-reading pages, use inline math `$...$` for symbols, variables, operators, and compact symbolic expressions such as `$S$`, `$G$`, `$l(S)$`, or `$l(S)-l(G)$`. Do not use inline code backticks for paper notation. Use plain prose for English technical terms unless they are part of a mathematical expression.
- Preserve equation numbering. Prefer `\tag{n}` inside display math when Feishu renders it correctly; otherwise place a separate plain-text number like `(n)` immediately after the display equation. Keep references such as `式 (4)` aligned with the original paper.
- Keep formulas near their original paragraph and section. Do not move all formulas into an appendix unless the source page is only a summary rather than a full manuscript page.
- After writing, fetch the Feishu page and verify formula fidelity. Check both inline and displayed formulas: count `<latex>` / `$...$` blocks when possible, inspect samples across early, middle, appendix, formula-heavy sections, and numbered equations, and confirm formulas did not degrade into ordinary text such as `L_render = lambda ||...`, lose `_` / `^` structure, merge with surrounding prose, or become translated words.
- If Feishu Markdown cannot render a formula reliably, use an explicit fallback: keep the exact LaTeX source in a labeled `公式 LaTeX 源` paragraph or block and, for important equations, insert a rendered equation image with a Chinese caption. Mark this as a rendering fallback, not as the preferred final form.
- Before finishing, report any formulas that remain fallback-only or unverified. Do not claim a deep dive is complete when important equations are visibly flattened, malformed, or missing.

## Research Map Trees

When organizing a Feishu survey / research-map page, use a parent-page plus subpage structure by default:

- Treat the user's Feishu page `如何构建literature tree（如何进行literature review，构建novelty tree和challenge-insight tree）` as the canonical method/example for literature organization and novelty discovery: `<FEISHU_OR_LARK_URL>` (doc token `<DOC_TOKEN>`). When building or revising literature trees, novelty trees, challenge-insight trees, or research-map pages, read/reference this page first unless the user gives a more specific template.
- Use its novelty taxonomy when organizing papers:
  - Type 1 novelty: seminal work for a milestone task.
  - Type 2 novelty: seminal work for a novel pipeline or representation.
  - Type 3 novelty: seminal work for a novel module.
  - Type 4 novelty: module-level improvement to an existing pipeline.
- Build `Literature Tree` nodes in this order: collect papers in the same direction, identify milestone tasks and their first/seminal papers, group papers by milestone task, identify representative pipelines/representations and their first/seminal papers, subdivide by module-level novelty, then add or revise milestone tasks as field understanding improves.
- Build `Challenge-Insight Tree` nodes by collecting field challenges first, then the insights/solution ideas addressing each challenge, then representative papers under each insight. Do not make a generic challenge tree; anchor challenges and insights in actual literature and the user's research goal.
- The parent page is a concise survey hub. It should contain summary-level content only: research question, scope, key takeaways, recommended route, links to subpages, and a short status / TODO list.
- Create a dedicated subpage for editable survey trees. This page should include the literature tree, challenge-insight tree, and any method / task / benchmark trees needed for navigation.
- Create one dedicated `Paper Cards` subpage for the survey. This page is a browsable collection that contains many paper cards in sequence. Do not create one child page per paper unless the user explicitly asks for per-paper pages.
- Create a dedicated subpage for the full survey report. This is usually the long report copied from ChatGPT Deep Research or another long-form source. Preserve it as the source report page, then distill only the summary into the parent page.
- The parent page should link to all three subpages and make their roles obvious: `Tree Maps`, `Paper Cards`, and `Full Survey Report` or equivalent Chinese titles.
- If the user provides an existing long report page, treat that page as the `Full Survey Report` child page when possible; do not leave the parent page as an overlong pasted report.
- Do not create placeholder survey artifacts. Before writing the parent summary, tree maps, or paper-card page, fetch and read the full survey report, identify the actual task/method/benchmark/research-gap structure, and write content from that understanding.
- The `Paper Cards` subpage must contain real, report-grounded cards for the important papers mentioned in the survey, usually grouped by theme, method family, or reading priority. Avoid `待补` placeholders except for genuinely missing external links or figures after a best-effort check; in those cases, state what is missing specifically.
- Paper-card work is a source-verification task, not a formatting task. Do not mechanically convert old summaries into the new card format or fill missing slots from plausibility. For each paper card, first open and inspect the paper's official full-paper source: for arXiv papers, prefer `https://arxiv.org/html/<arxiv-id>` when it exists because it is easier to search for affiliations, project/code links, figures, datasets, experiments, limitations, and conclusions; use the PDF as the fallback or authority when HTML is unavailable, incomplete, or ambiguous. For non-arXiv papers, use the official CVF/OpenReview/publisher PDF or official proceedings page. Verify the title, venue, institution/authors when needed, task definition, input/output, supervision/data, training/inference flow, benchmarks/metrics, experiments, limitations, and conclusions from those sources before writing reader-facing claims.
- Treat the official full paper (arXiv HTML/PDF, CVF PDF, OpenReview PDF, or publisher PDF) as the primary evidence for most paper-card facts. Web search, abstracts, project pages, GitHub, Semantic Scholar, Hugging Face, and conference pages are important supplementary sources for links, code, context, updates, and missing metadata. For `Dataset`, a reliable web summary or official page may be used when it explicitly names the dataset(s); if it does not, search the official full paper because the dataset should normally be stated there. Web snippets do not replace reading/searching the official full paper for method, experiment, compute, ablation, limitation, and conclusion claims. If the official full paper is unavailable or inaccessible, state that explicitly and mark affected fields as `待核验` or `Not reported`; do not finalize a card from snippets alone.
- Do not retain downloaded source material after paper-card verification. Any temporary PDF, HTML, extracted text, OCR/MinerU output, figure crop, or source asset used to fill a card must be deleted after the Feishu page has been written and fetched back successfully. Keep only the final reader-facing Feishu content unless the user explicitly asks for a local retained artifact.
- Always search for code before finalizing a paper card: check the paper text, official project page, author page, and official GitHub/organization if linked; then search GitHub by paper title, method name, and lead author/lab. Mark code as verified only when it is official or clearly maintained by the authors/project. If no reliable repository is found, write `w/o. verified code` or `w/o. code`; do not guess a repository from a similar name.
  - `定义`, `方法`, `实现`, `结论`, and `边界 / 启发` must be source-grounded. If a statement is an inference from the verified sources, label it as such; otherwise write `未报告`, `不适用`, or `待核验` rather than pretending the card is complete. Reported compute must come from the paper/project; if GPU, memory, time, FPS, or latency are absent, write `计算资源：未报告`.
- If a card has not been fully source-verified, mark the card or the affected fields as `待核验` and keep the wording conservative. Do not present unverified task definitions, claims, venues, code, datasets, or conclusions as confirmed facts.
- Paper cards must use the user's compact fixed format, not an ad-hoc review format. Use the enhanced format by default when the user is surveying an unfamiliar field or the paper's task setup is not already obvious to them:
  - Start each card with `#### Paper English Title`.
  - The second line must be `短译名｜核心创新点 / takeaway 短语`，prefer Chinese. Do not write a plain `中文名 / 短译名` line. The takeaway phrase should help the user recognize why the paper matters at a glance.
  - Treat the short translation, venue/institution, compact link line (`PDF｜Project｜Code`), and `Dataset` as one metadata paragraph with line breaks, not separate paragraphs. In Markdown sources for Feishu import, do not insert blank lines inside this metadata block; use Markdown hard line breaks by ending each metadata line except the last with two spaces. Example:
    ```markdown
    #### Paper English Title
    人网格恢复-高斯化身闭环｜把 HMR 姿态估计和 avatar 渲染优化放回同一个可微循环  
    arXiv 2026-05-04｜University of Michigan 等  
    [PDF](https://arxiv.org/pdf/2605.02784)｜w/o. project page｜w/o. verified code  
    Dataset: H36M, NeuMan, 3DPW
    ```
  - Then include venue + institution on one line using `｜`, followed by one compact link/status line and `Dataset: ...` within that continuous metadata paragraph. Verify institution / affiliation from arXiv HTML when available, otherwise from the paper PDF front matter, author footnotes, publisher PDF page, OpenReview/CVF page, or an official project/author page. If the official full paper is accessible, do not leave institution as `待核验`, `Institution: Not fully verified`, or `Affiliations in paper`; read the source and fill the actual institution names. If there are many affiliations, list the primary visible institutions plus `等`, but only after checking the source. Use `Institution: 待核验` only when the official full paper and official metadata are inaccessible.
  - `PDF:` must point directly to the PDF file, not an abstract page, HTML page, search result, or project page. For arXiv papers, use `https://arxiv.org/pdf/<arxiv-id>` rather than `https://arxiv.org/abs/<arxiv-id>` or `/html/<arxiv-id>`.
  - For available links, use compact linked labels rather than pasting full URLs in the metadata text: `[PDF](...)｜[Project](...)｜[Code](...)`. In Feishu XML this should appear as linked text like `<a href="...">PDF</a>｜<a href="...">Project</a>｜<a href="...">Code</a>`.
  - For missing links, keep the missing-status text in the corresponding slot without an extra field prefix, e.g. `[PDF](...)｜w/o. project page｜w/o. verified code`. Use `w/o. PDF`, `w/o. project page`, or `w/o. verified code` when a link is not found; do not write `Project:` or `Code:` inside the compact link line.
  - Include a reliable core method / pipeline / architecture / framework / system overview figure when available. Do not use a teaser, qualitative showcase, result collage, demo gallery, title-page screenshot, or PDF page render as the only paper-card image when a core method/process figure exists. If no reliable core figure has been checked yet, omit the image or mark `配图待补` rather than inserting a questionable one.
  - Use this exact header/metadata pattern:
    `#### Paper English Title`
    `短译名｜核心创新点 / takeaway 短语`
    `Venue｜Institution`
    `PDF｜Project｜Code` as compact linked labels or missing-link statuses
    `Dataset: ...`
    These metadata lines must be separated by line breaks inside one paragraph, not by blank lines or separate paragraphs.
  - `Dataset:` is mandatory and replaces the old `Data / Benchmark:` field. For clothing / physics / simulation-ready pages, put simulation metadata on the same line after an ASCII separator: `Dataset: H36M, NeuMan | Simulation: Not reported` or `Dataset: 4D-Dress | Simulation: CLO3D / Marvelous Designer`. Keep `Dataset:` terse: list only dataset names or the paper's explicit dataset phrase, separated by commas or `；`. Keep `Simulation:` terse as well: name only the simulator, physics engine, simulation framework, or explicit simulation setting used by the paper, such as CLO3D, Marvelous Designer, C-IPC, XPBD, MPM, MuJoCo, Isaac Gym, Blender physics, or `Not reported`; do not include long explanations in metadata. Only fill `Simulation:` after checking the official full paper HTML/PDF or the official project page; if a paper merely says it is simulation-ready but does not name the simulator, write `Simulation: Not reported`, and if the official source has not been checked yet, write `Simulation: 待核验`. Do not infer simulator names from the method family or from the word `simulation-ready`.
  - If a reliable web summary, official project page, conference page, or abstract explicitly names the dataset(s), it is acceptable to fill `Dataset:` from that source. If not, search the official full paper, preferably arXiv HTML for arXiv papers and otherwise the PDF, usually in the dataset, experiment, implementation, or benchmark section; dataset information should be present somewhere in the paper. Do not infer dataset names from the method family. Do not include benchmark task names, metrics, capture setup, scale, modalities, train/eval split, access links, or explanatory prose in this metadata field. Put those details in `定义` or `实现` only when they matter. If the dataset still cannot be found after official full-paper inspection, the card is incomplete: write `Dataset: 待核验` and revisit rather than guessing.
  - End with exactly the fixed six bullet slots: `定义`；`问题`；`方法`；`实现`；`结论`；`边界 / 启发`.
  - The six fixed bullet slots are Chinese-first reader notes. Do not leave raw English technical phrases in bullet content, such as `motion-dependent cloth dynamics`, `simulation-ready garment asset`, or `physically plausible deformation`, unless they are method names, model names, dataset names, code/link statuses, mathematical symbols, or exact quoted labels from a figure/table. When an English technical term is useful, write the Chinese term first and keep the English only as a parenthetical gloss, e.g. `运动相关布料动力学（motion-dependent cloth dynamics）`, `仿真就绪服装资产（simulation-ready garment asset）`, or `物理合理形变（physically plausible deformation）`. In bullet content, prefer Chinese placeholders such as `未报告` / `不适用` / `待核验`; keep English placeholders like `Not reported` only in compact metadata fields where the user has explicitly standardized that field.
  - `方法` must start with one compact summary sentence after `方法：`, before any nested bullets. This sentence should state the overall technical route or pipeline in plain language, then include exactly two nested bullets: `核心创新 1` and `核心创新 2`. Do not make `方法` only a container for the two innovation bullets.
  - `定义` is mandatory for unfamiliar fields and must describe the task contract, not the experiment details: task, input, output, supervision/training data type, training-stage data flow, inference-stage data flow, and evaluation benchmark/metric names. Keep it to 1-3 compact lines. If a dimension is not reported or not applicable, say `未报告` or `不适用` instead of guessing.
  - `实现` must not repeat the task contract. It should summarize how the paper actually realizes and validates the method: datasets used, baselines, key ablations, main metrics/results, whether data is real robot / simulation / offline / web-scale, and reported compute. Always include training and inference resource notes when available: training GPU count/model, training time, inference GPU/model, VRAM, FPS/latency/runtime. If GPU, memory, time, FPS, or latency are not reported, write `计算资源：未报告`.
  - `结论` must summarize the authors' own conclusion from the official full paper text, especially the conclusion, discussion, abstract, and experiment-summary sections. For arXiv papers, arXiv HTML is acceptable and often faster to search; use the PDF if the HTML is unavailable or incomplete. It should state what the paper claims it demonstrates or establishes, not the agent's independent judgment, research preference, or route-level interpretation. Do not add personal takeaways such as "this is important for UniGAvatar because..." in `结论`; put that kind of analysis only in `边界 / 启发`.
  - `边界 / 启发` should combine author-claimed limitations with one research-direction takeaway for the user's current research direction. Do not append explicit scoring or ranking tails such as `相关性：10/10；优先级：A。`, `relevance score`, or `read priority` inside each paper card unless the user explicitly asks for a separate triage/ranking table.
  - For papers in a field the user already knows well, a shorter legacy card is acceptable, but do not omit `定义` or `结论` when the task setup, evaluation, or final takeaway is non-obvious.
- Tree-map subpages must contain at least two contentful editable maps by default: a `General Goal Literature Tree` and a `Challenge-Insight Tree`. Their nodes should be based on the report's actual field structure, not generic labels.
- Verify after writing that the survey has the expected small set of real Feishu wiki/doc subpages: `Tree Maps`, one collection-style `Paper Cards` page, and `Full Survey Report`. The `Paper Cards` page should contain multiple cards inside the page, not many per-paper child pages.

When a Feishu research-map page asks for a literature tree, challenge-insight tree, or native mind map:

- Keep an editable nested outline in the Feishu page, because static images are hard to revise.
- If the user asks for `飞书原生思维导图`, `原生思维导图`, or says a Mermaid/flowchart rendering is not a real mind map, do not use Mermaid `flowchart LR` as a substitute.
- Convert the tree to PlantUML mind map syntax (`@startmindmap ... @endmindmap`) and write it into a Feishu board block (`block_type=43`) with `docs +whiteboard-update --input_format plantuml --overwrite`.
- Default visual style means Feishu's actual native default mind-map style, not a custom DSL card diagram that merely looks similar. Keep the imported `mind_map` node types and Feishu default styling unless the user explicitly asks for a designed/custom-colored diagram.
- When there are many first-level branches and the user asks for balanced left-right distribution, first import with PlantUML, then verify with `whiteboard +query --output_as raw`. If Feishu stores every first-level child under `right_children`, patch the raw native mind-map JSON instead of redrawing custom nodes: set `mind_map_root.left_children` / `right_children`, set each first-level node's `mind_map_node.layout_position` to `left` or `right`, adjust coordinates as needed, then write back with `whiteboard +update --input_format raw --overwrite`.
- Avoid the PlantUML `left side` directive for Feishu board imports because Feishu's PlantUML parser rejects it.
- Use richer semantic colors only when the user explicitly asks for more color, or when the map has many otherwise indistinguishable groups. Do not use arbitrary rainbow coloring; keep the same meaning-color mapping across pages.
- Do not rely on PlantUML inline color syntax such as `++[#LightBlue] Branch` for Feishu board imports; Feishu's PlantUML parser may reject it. Prefer DSL / OpenAPI nodes when color is required.
- Optional semantic color mapping for survey / field investigation maps:
  - Research goal / problem framing: light blue.
  - Scene / data / input state: light green.
  - Agent / body / representation state: light yellow.
  - Task / language / goal condition: light pink.
  - Interaction / object / environment dynamics: wheat or peach.
  - Method family / model architecture: lavender.
  - Evaluation / benchmark / metrics: light gray.
  - User's current research route / opportunity: gold.
- For `General Goal Literature Tree`, color by reading logic: goal/root in gold, milestone tasks in light blue, method families in lavender, seminal papers in light green, recommended reading order / priority in light yellow.
- For `Challenge-Insight Tree`, color by reasoning logic: challenge in light coral or pink, failure mode / limitation in wheat, insight in light green, representative paper in light blue, remaining gap / opportunity in gold.
- Use Mermaid whiteboards only when the user explicitly accepts Mermaid or asks for an editable diagram/flowchart rather than a native mind map.
- Static PNG/SVG rendering is a fallback only when the user explicitly needs an exported image. If rendering an image, insert it as a native Feishu media block with `docs +media-insert`; do not paste raw image tags.
- For Peng Sida / Learning Research style research maps, use two complementary trees by default:
  - `General Goal Literature Tree`: field goal -> milestone tasks -> seminal branches -> recommended reading order.
  - `Challenge-Insight Tree`: challenge -> insight -> representative papers -> remaining gap.
- Verify after writing that only the intended board blocks remain, `flowchart LR` is absent when native mind map was requested, and the fetched whiteboard content contains `@startmindmap`.
- Preserve the source page title and verify after writing that the title did not become `Untitled`.

## Investigation Pages

When organizing a Feishu `Investigation` page from a technical talk, research-direction clipping, frontier lecture, or route-evidence material:

- Keep the parent page as the distilled investigation note: source metadata, one-sentence conclusion, core thesis, technical route, route relevance, open questions, and a compact diagram when useful.
- Create a child page named `Paper Cards` or `<Parent Title>｜Paper Cards` when the talk/report mentions concrete papers, systems, benchmarks, or project pages that support the route.
- The `Paper Cards` child page is a collection page containing many paper cards in sequence. Do not create one child page per paper unless explicitly requested.
- Include all clearly mentioned papers from the source material, grouped by the talk's actual narrative arc. If a title is uncertain because the source is an imperfect transcript, mark it as a口播线索 and do not fabricate metadata.
- Use the fixed paper-card format from the Research Map section. `PDF:` must point directly to a PDF when available.
- Prefer official project pages, arXiv pages, CVF/OpenReview pages, author pages, or official GitHub repositories. Avoid relying on generic search snippets when primary sources exist.
- After writing, verify the parent-child hierarchy and that the paper-card child page has real cards, not placeholders.

## Useful Commands

Show document commands:

```bash
~/.local/bin/lark-cli docs --help
~/.local/bin/lark-cli docs +fetch --help
~/.local/bin/lark-cli docs +update --help
```

Insert an image as a native Feishu media block:

```bash
~/.local/bin/lark-cli docs +media-insert \
  --as user \
  --doc '<document-token-or-url>' \
  --file '<local-image.png>' \
  --selection-with-ellipsis '<nearby text>' \
  --before \
  --align center \
  --caption '图 1｜完整中文图注：<完整翻译论文原始 caption>'
```

Add or update a caption on an existing image block without re-uploading the image:

```bash
~/.local/bin/lark-cli api PATCH \
  "/open-apis/docx/v1/documents/<docx_token>/blocks/batch_update" \
  --as user \
  --data '{"requests":[{"block_id":"<image_block_id>","replace_image":{"token":"<existing_image_file_token>","align":2,"scale":<existing_scale>,"caption":{"content":"图 1｜完整中文图注：<完整翻译论文原始 caption>"}}}]}'
```

Create a gray callout:

```xml
<callout emoji="📄" background-color="light-gray" border-color="gray">
  <h3>Title</h3>
  <p>Body</p>
</callout>
```

Search docs, wiki, and spreadsheet files:

```bash
~/.local/bin/lark-cli docs +search --help
```

Update an existing Feishu board block as a native mind map:

```bash
~/.local/bin/lark-cli docs +whiteboard-update \
  --as user \
  --whiteboard-token '<board-token>' \
  --input_format plantuml \
  --source '@mindmap.plantuml' \
  --overwrite
```

Inspect wiki helpers when a wiki node must be resolved:

```bash
~/.local/bin/lark-cli wiki --help
~/.local/bin/lark-cli wiki nodes --help
```

Run health checks:

```bash
~/.local/bin/lark-cli doctor
```

## Safety

- Do not print or persist Feishu app secrets, access tokens, or refresh tokens.
- If inspecting `~/.lark-cli/config.json`, mask keys containing `secret`, `token`, `key`, `password`, `access`, or `refresh`.
- Treat CLI writes as live document edits. Prefer narrow operations and verify after changes.
- If the CLI warns about a proxy, mention it only if it affects the task or the user asks about network/auth behavior.

## Known Local Setup

- CLI path: `~/.local/bin/lark-cli`
- User-local tools are added to PATH from `~/.zshrc`.
- Feishu/Lark CLI config lives under `~/.lark-cli/`.
