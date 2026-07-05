---
name: paper-card-delivery
description: Canonical paper-card delivery standard for source-grounded research paper cards in Feishu, surveys, deep dives, meeting notes, and local wiki/project notes. Use whenever the user asks to整理/补全/生成/审核 paper card, 论文卡片, Paper Cards, literature survey cards, meeting paper cards, or deep-dive paper cards; also use when another skill such as feishu-doc-workflow, paper-deep-dive, survey-builder, ai-research-workflow, or llm-wiki-skill will create or modify paper cards.
---

# Paper Card Delivery

## Core Contract

Treat paper-card work as source verification, not formatting. A finished card is allowed only after inspecting the official full-paper source end to end enough to verify the card fields: abstract, method, experiment/evaluation, conclusion/discussion, limitations when present, affiliations, datasets, code/project links, and selected figure captions.

If official full-paper verification is incomplete, do not write a polished card. Mark it `candidate / 待核验`, `待核验`, `未报告`, `Not reported`, `N/A`, or leave a verification TODO in the affected fields.

Paper card is a lightweight reader index after source verification. It is not a full deep dive, not a PDF-to-Markdown manuscript, not a complete translation, and not a substitute for `paper-deep-dive`. If the user asks to 深读 / detailed-read / dive into one paper, use `paper-deep-dive` and create the paper card as only one component of that larger package.

When the target is Feishu, also use `feishu-doc-workflow` for hierarchy, image preservation, native image insertion, and post-write verification.

For any reader-facing Chinese prose in the card, also use [`chinese-technical-writing`](../chinese-technical-writing/SKILL.md). This card skill adds paper-card-specific structure; the broader Chinese-first terminology standard lives there.

## Required Source Order

Use primary sources first:

1. Official paper HTML, preferably arXiv HTML for arXiv papers.
2. Official PDF from arXiv, CVF, OpenReview, publisher, conference, or author page.
3. Official project page, official code repository, author/lab page, and conference metadata.
4. Secondary sources only for discovery/context, not for finished claims.

Do not finalize method, implementation, conclusion, limitation, compute, dataset, or figure claims from abstracts, snippets, project pages, README files, slides, screenshots, search results, or secondary summaries alone.

## Fixed Card Format

Use this exact compact format by default:

```markdown
#### Paper English Title
短译名｜核心创新点 / takeaway 短语  
Venue｜Institution  
[PDF](...)｜[Project](...) or w/o. project page｜[Code](...) or w/o. verified code  
Dataset: ...

![method-flow](relative-or-native-image)
图 N｜完整中文图注：...

- 定义：
- 问题：
- 方法：一句话概括整体技术路线。
  - 核心创新 1：
  - 核心创新 2：
- 实现：
- 结论：
- 边界 / 启发：
```

Format-only example. This is synthetic and not a real paper; do not copy its facts into a real card:

```markdown
#### Example Paper Title for Format Only
示例论文短译名｜把稀疏输入约束转化为可验证的重建流程  
Venue 待核验｜Institution 待核验  
[PDF](https://example.com/paper.pdf)｜w/o. project page｜w/o. verified code  
Dataset: 待核验

配图待补：需要从官方论文 HTML/PDF 或项目页补充可信方法流程图；导览图（teaser）、概览图（overview）或结果展示图不能单独作为主图。

- 定义：待核验。正式卡片中这里写任务契约：输入、输出、监督/数据类型、训练和推理流程，以及必要的评价基准和指标。
- 问题：待核验。正式卡片中这里写论文声称要解决的核心问题，而不是用户自己的研究动机。
- 方法：待核验。正式卡片中这里先用一句话概括整体技术路线。
  - 核心创新 1：待核验。
  - 核心创新 2：待核验。
- 实现：待核验。正式卡片中这里写数据、基线、消融实验、指标/结果和计算资源；缺失时写 `计算资源：未报告`。
- 结论：待核验。正式卡片中这里只写作者在摘要、结论、讨论或实验总结中声称的结论。
- 边界 / 启发：待核验。正式卡片中这里放作者局限和用户研究方向启发，不放独立评分。
```

Rules:

- Start every card with `#### Paper English Title`.
- The heading must be the exact official English paper title from the official paper page, arXiv/OpenReview/CVF/publisher metadata, or the first page of the official PDF. Do not shorten it to a method name, acronym, section/topic label, or locally convenient title when the official title is longer. Conversely, do not invent an explanatory subtitle when the official paper title itself is short, for example `Mapping Networks`.
- The second line must be `短译名｜核心创新点 / takeaway 短语`; do not use a plain translation-only line.
- Keep the title and the four metadata lines as a compact paragraph. In Markdown drafts, use hard line breaks after the short-takeaway, venue/institution, and link lines, and do not insert blank lines inside the metadata block.
- `Venue｜Institution` is venue/date plus publishing institutions/affiliations, not a long author list. Verify affiliations from official HTML/PDF/proceedings/project metadata when available. Use 1-3 primary official institutions/labs and keep visible entities <= 5. Use authors only when affiliations cannot be verified.
- Use compact link labels: `[PDF](...)｜[Project](...)｜[Code](...)`. For missing links use exactly `w/o. PDF`, `w/o. project page`, or `w/o. verified code` / `w/o. code`.
- `PDF` must point directly to a PDF when one exists, not an abstract/search/project page.
- Always search for code before finalizing a card: paper text, official project page, author/lab page, official organization, and GitHub by paper title / method name / lead author. Mark code as verified only when it is official or clearly author-maintained.
- `Dataset:` is mandatory. Keep it terse: dataset names only. Do not infer datasets from method family. If the official source does not report a dataset, write `Dataset: 未报告` or `Dataset: 待核验`.
- For clothing/physics/simulation-ready contexts, append terse simulation metadata on the same line: `Dataset: ... | Simulation: CLO3D / Marvelous Designer` or `Simulation: Not reported`.
- End with exactly six Chinese bullet slots: `定义`, `问题`, `方法`, `实现`, `结论`, `边界 / 启发`.
- The metadata takeaway, figure captions, and six bullet slots are Chinese-first reader notes. For English terms, write Chinese first and use the English term only as a parenthetical gloss unless it is a method/model/dataset/code name or mathematical symbol.
- `定义` states the task contract: task, input, output, supervision/data type, training/inference flow, and evaluation benchmark/metric names when relevant. Use `未报告` / `不适用` / `待核验` instead of guessing.
- `方法` must include one summary sentence and exactly two nested bullets: `核心创新 1` and `核心创新 2`.
- `实现` states how the paper realizes and validates the method: datasets, baselines, key ablations, metrics/results, data source type, and reported compute. If GPU, memory, time, FPS, latency, or runtime are not reported, write `计算资源：未报告`.
- `结论` must summarize the authors' own conclusion, not the agent's route-level judgment.
- Put user-specific interpretation only in `边界 / 启发`. Do not append ranking tails such as `相关性：10/10` or `优先级：A` inside the card unless the user explicitly asks for a separate triage/ranking table.
- Keep verification status inside the affected metadata field or bullet, for example `w/o. verified code`, `Not reported`, `待核验`, or `计算资源：未报告`. Do not add a separate broad `核验说明` / verification disclaimer section unless the user explicitly asks for an audit note.

## Chinese Technical Language

Default to Chinese prose for reader-facing paper-card text. English is allowed for:

- official paper titles, method/model/system names, dataset/benchmark names, code/repo names, and organization names;
- standard acronyms and symbols such as SMPL-X, 3DGS, CLIP, PSNR, LPIPS, FID, FPS, $L_2$, and $\mathcal{L}$;
- exact figure/table labels or official quoted phrases when they are needed for source alignment.

For translatable technical concepts, write Chinese first. If the English term is useful for search or disambiguation, use first occurrence only as `中文（English term）`, then use Chinese afterward. Do not leave raw English noun-phrase islands inside Chinese sentences.

Translate common concepts instead of leaving them English:

- `parametric human estimation` -> `参数化人体估计`
- `perspective distortion` -> `透视畸变` or `透视失真`
- `scene geometry` -> `场景几何`
- `camera pose` -> `相机位姿`
- `body pose` -> `人体姿态`
- `mesh reconstruction` -> `网格重建`
- `3D human reconstruction` -> `三维人体重建`
- `motion-dependent cloth dynamics` -> `运动相关布料动力学`
- `physically plausible deformation` -> `物理合理形变`
- `simulation-ready asset` -> `仿真就绪资产`

## Figure Contract

The main figure should be a reliable method/process figure when available: pipeline, workflow, architecture with stages/arrows, method/training/inference/data flow, benchmark construction flow, or computation/loss flow.

Do not use as the only main card image when a process figure exists:

- title page, first page, abstract page, PDF page render;
- teaser, result showcase, qualitative collage, demo gallery;
- generic overview without clear stages/modules/data/control flow.

Extraction priority is mandatory, not a loose preference. User-provided or user-approved manual screenshots are the highest-priority source when they clearly show the intended paper figure and include or are accompanied by the original paper caption. Agent-generated PDF crops/screenshots are different: do not crop or screenshot from PDF when a user-approved figure or official HTML/project figure asset with a matching caption is available. A PDF-derived figure made by the agent can only be used after the earlier source classes below have been checked and found unavailable, unusable, or not a method/process figure.

1. User-provided or user-approved manual screenshot/crop of the paper figure, especially when it includes the full original caption. Preserve it unless it is visibly wrong, too blurry, or the user asks to replace it.
2. Official HTML / arXiv HTML / publisher HTML figure assets plus exact `figcaption`.
3. Official project-page method figure only when it clearly matches the paper.
4. Structured PDF extraction with MinerU when no usable user-approved / HTML / project figure is available.
5. Agent manual PDF crop only when user-approved, HTML/project, and MinerU sources are unavailable or unusable, and only after visual QA confirms the crop is a method/process figure rather than a text column, result gallery, banner, title page, or unrelated page artifact.

HTML search is mandatory before any PDF fallback. Do not assume a paper has no HTML figure assets just because the card only links a PDF. For arXiv/CVF/OpenReview/publisher pages, the HTML image asset and its `figcaption` are the default source of truth for figure selection and caption matching. Check, in order:

- arXiv abstract and HTML variants: `https://arxiv.org/abs/<id>`, `https://arxiv.org/html/<id>`, versioned HTML such as `https://arxiv.org/html/<id>v1`, and ar5iv only as a secondary discovery fallback;
- conference / publisher HTML and open-access pages: CVF / ICCV / ECCV / NeurIPS / OpenReview / ACM / IEEE / Springer / project-proceedings pages when available;
- official project pages, author pages, lab pages, and official GitHub README assets;
- figure URLs referenced by those HTML pages, including relative `img/`, `assets/`, `static/`, `_images/`, `figures/`, and extracted arXiv asset paths.

Do not use ad hoc PDF screenshots, PyMuPDF page crops, browser screenshots, or search-result thumbnails as the normal image extraction path. Hand-written PDF screenshot/crop logic is not an acceptable substitute for HTML assets or MinerU. PDF screenshot/crop is a last resort and must be clearly sourced from the official PDF. If it is used, keep the crop tight around the selected figure and its original caption, verify that the caption belongs to the figure, and reject crops that are mostly surrounding body text.

For PDF-only papers, or papers whose user-approved / official HTML / project sources do not expose a usable method/process figure, use MinerU before any agent manual PDF crop. On this machine, the preferred path is `$WORLD_MODEL_VAULT/.tools/mineru-md.sh` backed by the local MinerU environment. Use the MinerU output to locate extracted figure files and figure captions, then insert those native figure assets. Treat MinerU output as a conversion draft: verify figure number, caption, and visual content against the official PDF before writing. If MinerU fails or produces mismatched/low-quality figures, mark the figure `配图待补` unless a manually cropped PDF figure can be visually verified against the original caption and the failure of user-approved / HTML / project / MinerU sources is recorded in the working notes.

Agent manual PDF crop quality standard, for last-resort crops only:

- Render from the source PDF at high resolution instead of taking a screen capture from Preview, Chrome, or a PDF viewer. Use structured extraction first; if rendering is needed, render the relevant page at >= 300 DPI, preferably 450-600 DPI for dense pipeline diagrams or small labels, then crop from that render.
- Crop the actual figure area, not the whole page. Keep method-stage arrows, legends, axis labels, subfigure labels, and in-figure text that are part of the figure; exclude unrelated body text, headers/footers, neighboring figures, and page margins. Keep the printed caption out of the image unless the caption is visually inseparable from the figure; the translated caption belongs in the native caption field.
- Preserve aspect ratio and use a lossless format such as PNG for diagrams. Do not square-crop, stretch, JPEG-recompress, blur, or use AI upscaling/retouching that can alter text or diagram content.
- If the cropped figure is visually soft, too small, or hard to read at normal Feishu card width, rerender at higher DPI and recrop. If it remains unreadable or ambiguous, use `配图待补` rather than shipping a blurry crop.
- Before upload, visually inspect the crop locally or in a contact sheet and verify figure number, panel labels, and caption match the official paper. After Feishu upload, fetch back and verify native image dimensions/aspect ratio, no `512 x 512` fallback, and no visible blur introduced by the upload.

Every selected figure needs the complete Chinese translation of the official original caption, including figure number, subfigure labels, symbols, method names, dataset names, and important technical terms. If no verified caption exists, write `图注待补：需要从官方论文 HTML/PDF 或项目页核验并完整翻译原始 caption。` and keep the card incomplete.

For Feishu, insert images as native image blocks after the metadata and `Dataset`, before the six bullet slots, and put the complete Chinese caption into the native image caption field. Do not leave the figure caption as a separate ordinary paragraph below the image unless the native caption API is unavailable and the fallback is explicitly stated. Preserve existing image blocks, same-row layouts, grid ratios, dimensions, captions, and order. Never rewrite a rich page just to normalize text.

If a card is copied or reused across Feishu pages, preserve already approved paper-card figures and captions unless there is a page-specific reason to change them. If no reliable method/process figure exists after checking official sources, write `配图待补` instead of filling the slot with a weak visual.

Before batch-inserting figures into Feishu, create and visually inspect a contact sheet or equivalent preview of all selected images. Reject and replace any selected image that is an HTML banner, logo, author/avatar photo, OJS/publisher UI artifact, title-page render, mostly text-only PDF crop, result-only qualitative collage when a method figure exists, or a crop whose caption belongs to another figure.

## Context-Specific Rules

Survey / research-map cards:

- A `Paper Cards` page is a collection page containing many cards in sequence. Do not create one child page per paper unless the user explicitly asks.
- Group cards by the survey's actual theme, method family, narrative arc, or reading priority when that improves scanning.
- Use report/source context to decide which papers deserve cards, but do not fill card facts from plausibility. If a paper is important but not fully verified yet, keep the affected fields `待核验`.
- Avoid placeholder cards except for genuinely missing links, figures, datasets, or source access after a best-effort check; state the missing item specifically.

Meeting / transcript cards:

- Personal notes, supplied PDF links, screenshots, and visible figures can guide importance and context, but finished claims still require official paper sources.
- If a paper title comes only from an imperfect transcript or speech clue, mark it as `口播线索 / 待核验` and do not fabricate metadata.
- Prefer user-provided PDF links and figures when present, but still verify title, venue, dataset, conclusion, and caption against official sources before marking the card finished.

Teacher / lab profile cards:

- Put paper cards directly in the teacher/lab page unless the user explicitly asks for a nested `Paper Cards` child page.
- Keep route overview tables separate from cards. A `路线总览` table is navigation, not a second paper-card index.

Local Markdown / vault cards:

- If the user explicitly asks to write paper cards to the local vault, store figure assets near the target page under `assets/YYYY-MM-DD/`.
- Use semantic, stable filenames such as `YYYY-MM-DD-short-topic-figure-role.png`, not `image.png`, `image 1.png`, or `figure.png`.
- Markdown image paths should be relative to the target file, and alt text should be a short semantic phrase.
- Remove downloaded PDFs, HTML, OCR/MinerU outputs, temporary crops, and other intermediates after the durable Feishu/local deliverable is verified, unless the user explicitly asks to keep them.

## Verification Checklist

Before presenting a finished card, explicitly verify:

- Official full paper inspected end to end enough for all reader-facing claims.
- Title, venue/date, institution/affiliation verified. The title check must compare the card heading with official metadata/PDF first-page title; for CVF pages, also compare against the PDF filename slug to catch acronym-only headings.
- PDF, project page, and official/verified code searched.
- `Dataset:` filled from source or explicitly marked.
- Method/process figure selected from official source, or `配图待补` stated.
- User-provided or user-approved screenshots/crops were checked first; HTML / project-page figure search was completed before any agent PDF fallback, and no agent PDF screenshot/crop was used when a usable user-approved or HTML/project figure with matching caption exists.
- If PDF fallback was needed, MinerU extraction was attempted before agent manual screenshot/crop unless MinerU is unavailable; any remaining agent manual crop was visually QA'd against the official PDF, and the reason user-approved / HTML / project / MinerU sources could not be used is recorded in task notes.
- Any last-resort agent manual PDF crop was rendered from the PDF at high DPI, tightly cropped, saved losslessly, visually inspected before upload, and fetched back from Feishu to verify dimensions/aspect ratio and readability.
- Figure caption is complete Chinese translation of the original caption.
- Six fixed bullet slots present and source-grounded.
- Reader-facing Chinese prose uses Chinese-first terms; no raw translatable English phrase islands such as `parametric human estimation`, `perspective distortion`, or `scene geometry`.
- `结论` reflects authors' claims; user takeaways are only in `边界 / 启发`.
- No local-path/Obsidian residue in reader-facing text: `assets/`, `![[`, `EW_IMG`, `图像：`, local filenames, or vault paths.
- For Feishu writes: page fetched back after writing; hierarchy, title, image count/layout, and card count verified.

## Validation Script

Run the bundled structural validator on local Markdown drafts before syncing:

```bash
python .tools/skills/paper-card-delivery/scripts/validate_paper_card.py path/to/cards.md
```

The script catches missing headings, missing or non-compact metadata lines, `Dataset:`, fixed bullet slots, missing `核心创新` bullets, local-path residue, common forbidden images, and known raw English phrases that should be Chinese-first. It cannot prove official-source verification; the agent must still state the source evidence it inspected.

For Feishu pages, do not rely on fetched Markdown alone to verify compact metadata. Feishu's Markdown export can render hard line breaks inside one native text block as blank-separated lines, which is indistinguishable from four loose paragraphs in plain Markdown. After writing to Feishu, fetch the Docx blocks and run the block-level validator:

```bash
lark-cli api GET /open-apis/docx/v1/documents/<docx_token>/blocks \
  --as user --params '{"page_size":500}' > blocks.json
python .tools/skills/paper-card-delivery/scripts/validate_feishu_paper_card_blocks.py blocks.json
```

The block-level validator is authoritative for Feishu compact metadata and image caption placement: each card heading must be followed by exactly one normal text block whose content has four non-empty hard-break lines: takeaway, `Venue｜Institution`, `PDF｜Project｜Code`, and `Dataset:`; each image card must then use a native image block whose caption field contains the complete Chinese figure caption, with no separate `图 N｜...图注...` paragraph after the image. It also checks CVF PDF links for title-shortening errors when the PDF filename exposes a longer official title than the card heading.

## Sorting

Within the same page or section, sort normal paper cards newest to oldest. Prefer formal venue year/date; otherwise use arXiv first/latest version date. Survey, overview, or roadmap cards may appear at the top only when the section is explicitly named `Survey`, `Overview`, or `Roadmap`.
