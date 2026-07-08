---
name: paper-card-delivery
description: Canonical paper-card delivery standard for source-grounded research paper cards in Feishu, surveys, deep dives, meeting notes, and local wiki/project notes. Use whenever the user asks to整理/补全/生成/审核 paper card, 论文卡片, Paper Cards, literature survey cards, meeting paper cards, or deep-dive paper cards; also use when another skill such as feishu-doc-workflow, paper-deep-dive, survey-builder, ai-research-workflow, or llm-wiki-skill will create or modify paper cards.
---

# Paper Card Delivery

## Core Contract

Treat paper-card work as source verification, not formatting. A finished card is allowed only after inspecting the official full-paper source end to end enough to verify the card fields: abstract, method, experiment/evaluation, conclusion/discussion, limitations when present, affiliations, datasets, code/project links, selected figure, and selected figure caption.

Two failures disqualify a paper card from delivery. First, do not write plausible-sounding claims by inference when the official original paper has not been read; that is fabrication, even if the claim sounds likely from the title, abstract, project page, or method family. Second, if the official original paper is accessible by PDF, HTML, publisher/conference page, arXiv/OpenReview/CVF page, project page, official code, local rendering, MinerU extraction, or OCR, do not leave `待核验`; continue source extraction and resolve the field.

If a field is `待核验`, the required next action is to inspect the official full-paper source or other official source until the field is resolved. Do not leave `待核验` in reader-facing paper cards. A finished paper-card delivery must contain no `待核验`, `candidate`, TODO/TBD/pending verification text, or other unresolved verification markers. For missing information, use `未报告`, `Not reported`, `N/A`, or `不适用` only after checking the official paper/project/code sources and confirming the item is not reported or not applicable. `无法获取原文` is allowed only after every reasonable official acquisition route has failed, including official HTML, official PDF, arXiv/OpenReview/CVF/publisher/conference pages, DOI landing page, project page, author/lab page, official repository, local PDF download/rendering, and available extraction/OCR routes such as MinerU. When that happens, report a blocker with the attempted routes instead of shipping a finished card.

For formal delivery, every paper card must include a verified method/process figure or a user-approved figure, with a complete Chinese caption. Do not deliver cards with `配图待补`, `图注待补`, `图片待补`, `图像待补`, `待补配图`, `待补图注`, empty image slots, or text-only figure/caption TODO/TBD/pending notes. Any reader-facing sentence like `配图待补：优先从官方论文 HTML / PDF 中提取...` is a hard delivery failure, not an acceptable caveat. If the figure cannot be obtained within the current turn, the correct outcome is to continue extraction, explicitly downgrade the page to a draft, reduce scope with the user's approval, or report that the deliverable is blocked. Never mark a paper-card page complete while any card is missing its figure or figure caption.

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

When the paper source cannot be opened at first, do not convert unknown fields to `待核验`. Keep trying official acquisition routes: alternate official HTML/PDF mirrors, DOI/publisher/conference pages, arXiv versioned pages, OpenReview/CVF pages, project and author pages, official code, local PDF download, local rendering, MinerU extraction, and OCR when available. Only after those routes fail may you write `无法获取原文`, and only as a blocker/source-verification TODO with attempted routes, not as a completed card field.

## Fixed Card Format

Use this exact compact format by default:

```markdown
#### Paper English Title
短译名｜核心创新点 / takeaway 短语  
Venue｜Institution  
[PDF](...)｜[Project](...) or w/o. project page｜[Code](...) or w/o. verified code  
Dataset: ...

![method-flow](relative-or-native-image)
图 N｜完整中文图注：<完整翻译原始 caption>（来源：HTML）

- 定义：
- 问题：
- 方法：一句话概括整体技术路线。
  - 核心创新 1：
  - 核心创新 2：
- 实现：
- 结论：
- 局限：
- 启发：
```

Format-only example. This is synthetic and not a real paper; do not copy its facts into a real card:

```markdown
#### Example Paper Title for Format Only
示例论文短译名｜把稀疏输入约束转化为可验证的重建流程  
Venue 2026｜Example University
[PDF](https://example.com/paper.pdf)｜w/o. project page｜w/o. verified code  
Dataset: 未报告

![method-flow](relative-or-native-image)
图 1｜完整中文图注：这里应放原始 caption 的完整中文翻译，包括图号、子图说明和关键术语。（来源：HTML）

- 定义：示例占位。正式卡片中这里写任务契约：输入、输出、监督/数据类型、训练和推理流程，以及必要的评价基准和指标。
- 问题：示例占位。正式卡片中这里写论文声称要解决的核心问题，而不是用户自己的研究动机。
- 方法：示例占位。正式卡片中这里先用一句话概括整体技术路线。
  - 核心创新 1：示例占位。
  - 核心创新 2：示例占位。
- 实现：示例占位。正式卡片中这里写数据、基线、消融实验、指标/结果和计算资源；缺失时写 `计算资源：未报告`。
- 结论：示例占位。正式卡片中这里只写作者在摘要、结论、讨论或实验总结中声称的结论。
- 局限：作者未明确报告局限。正式卡片中这里优先写作者明确报告的局限；若作者未明确报告，写 `作者未明确报告局限`，再补充基于实验设置、数据、指标、失败案例或适用条件分析出的论文局限。
- 启发：示例占位。正式卡片中这里写对用户研究方向的启发、可迁移想法、可试实验或头脑风暴，不放独立评分。
```

Rules:

- In local Markdown drafts, the `图 N｜完整中文图注：...` line is the caption source. The caption body must be a complete Chinese translation of the official original caption, not a generated description of why the figure is useful. When synced to Feishu, a no-formula caption must become the native image caption instead of remaining as a separate paragraph; captions containing inline formulas may use an adjacent paragraph only when the native caption field cannot preserve the formula.
- If a source label is useful, keep it to one short controlled tag at the end of the caption: `来源：用户截图`, `来源：HTML`, `来源：MinerU PDF 截图`, or `来源：PDF 截图`. Do not write verbose source prose such as `该图来自官方论文 PDF 裁图`, and do not add filler such as `用于说明论文的核心流程、输入输出关系和关键模块`, `原始 caption 已在图中保留`, or `便于回溯核验`.
- The visual slot may contain one or two figures. For new paper cards, prefer a two-figure group when both are available: `teaser / visual result / problem context` plus `pipeline / method overview / architecture / process figure`. In Markdown drafts, keep them consecutive in teaser-then-method order; in Feishu, place them in the same-row native image group/grid with each figure's own native caption. If no teaser is available, use the pipeline/method overview figure alone.
- When relevant, keep base-model and simulation metadata on the fourth metadata line, for example `Dataset: ... | Base: ...`, `Dataset: ... | Simulation: ...`, or `Dataset: ... | Base: ... | Simulation: ...`. Do not create a fifth metadata line for base models or simulation. `Simulation:` is a conditional field, not a default placeholder; if the paper does not involve simulation, omit it entirely.
- Start every card with `#### Paper English Title`.
- The heading must be the exact official English paper title from the official paper page, arXiv/OpenReview/CVF/publisher metadata, or the first page of the official PDF. Do not shorten it to a method name, acronym, section/topic label, or locally convenient title when the official title is longer. Conversely, do not invent an explanatory subtitle when the official paper title itself is short, for example `Mapping Networks`.
- The second line must be `短译名｜核心创新点 / takeaway 短语`; do not use a plain translation-only line.
- Keep the title and the four metadata lines as a compact paragraph. In Markdown drafts, use hard line breaks after the short-takeaway, venue/institution, and link lines, and do not insert blank lines inside the metadata block.
- `Venue｜Institution` is venue/date plus publishing institutions/affiliations, not a long author list. Verify affiliations from official HTML/PDF/proceedings/project metadata when available. Use 1-3 primary official institutions/labs and keep visible entities <= 5. Use authors only when affiliations cannot be verified.
- Use compact link labels: `[PDF](...)｜[Project](...)｜[Code](...)`. For missing links use exactly `w/o. PDF`, `w/o. project page`, or `w/o. verified code` / `w/o. code`.
- `PDF` must point directly to a PDF when one exists, not an abstract/search/project page.
- Always search for code before finalizing a card: paper text, official project page, author/lab page, official organization, and GitHub by paper title / method name / lead author. Mark code as verified only when it is official or clearly author-maintained.
- `Dataset:` is mandatory. Keep it terse: dataset names only, maximum three visible datasets. Separate multiple dataset names with ASCII comma plus space, for example `Dataset: H3.6M, 3DPW, SURREAL`; do not use `｜`, `/`, `、`, `，`, `;`, or `；` as dataset delimiters. If the paper uses more than three datasets, choose the three most important for the card metadata and put the fuller training/evaluation dataset list in `实现` when needed. Do not infer datasets from method family. If the official source does not report a dataset after checking the full paper and related official sources, write `Dataset: 未报告`. Never leave `Dataset: 待核验`; go back to the original source and resolve it.
- If the paper uses an open-source foundation model, pretrained base model, diffusion/video generation backbone, large multimodal model, or public checkpoint as a base, append terse base-model metadata on the same `Dataset:` line using exactly `| Base:`. Examples: `Dataset: LAION-Aesthetics | Base: FLUX.1-dev (LoRA fine-tuned)`, `Dataset: WebVid-10M | Base: HunyuanVideo (fine-tuned)`, `Dataset: 未报告 | Base: Stable Diffusion XL (frozen)`, or `Dataset: 未报告 | Base: 未报告`. Keep visible base models to at most three names; put adapters, LoRA rank, checkpoint variants, freezing/fine-tuning details, or longer base-model chains in `实现`. Use official paper/project/code evidence, and do not infer the base from the task family or visual style. Do not write `Base:` if the paper trains from scratch or does not involve a reported open-source/pretrained base.
- If the paper uses a simulator, synthetic-data generator, physics engine, game engine, robotics environment, cloth simulator, or other explicit simulation environment, append terse simulation metadata on the same line using exactly `| Simulation:`: `Dataset: ... | Simulation: CLO3D / Marvelous Designer`, `Dataset: ... | Simulation: MuJoCo / Isaac Gym`, or `Dataset: ... | Simulation: 未报告`. Use `Simulation: 未报告` only when the paper clearly involves simulation but does not report the specific simulator/environment after source verification. If the paper does not involve simulation, do not write any `Simulation:` field. Use official paper/project/HTML evidence for the simulator or environment; do not infer a simulator from the task family. Do not write misspellings such as `Simluation`.
- End with exactly seven Chinese bullet slots: `定义`, `问题`, `方法`, `实现`, `结论`, `局限`, `启发`.
- The metadata takeaway, figure captions, and seven bullet slots are Chinese-first reader notes. For English terms, write Chinese first and use the English term only as a parenthetical gloss unless it is a method/model/dataset/code name or mathematical symbol.
- `定义` states the task contract: task, input, output, supervision/data type, training/inference flow, and evaluation benchmark/metric names when relevant. Use `未报告` / `不适用` instead of guessing only after checking the official source. Never leave `待核验`; treat it as an instruction to verify from the original paper.
- `方法` must include one summary sentence and exactly two nested bullets: `核心创新 1` and `核心创新 2`.
- `实现` states how the paper realizes and validates the method: datasets beyond the three-name metadata limit when needed, base model usage beyond the compact `| Base:` metadata when needed, baselines, key ablations, metrics/results, data source type, simulation environment details when too long for metadata, and reported training/implementation compute. For open-source/pretrained bases, report whether the base is fine-tuned, frozen/directly used, LoRA/adapted, distilled, or used only for initialization when the official source says so. Always report GPU details when the paper, appendix, project page, or official code reports them, especially GPU count, model, and memory. If GPU, memory, time, FPS, latency, or runtime are not reported, write `计算资源：未报告`.
- `结论` must summarize the authors' own conclusion, not the agent's route-level judgment.
- `局限` must prioritize limitations explicitly reported by the authors in limitations, discussion, conclusion, experiment analysis, appendix, or failure-case text. If the paper does not explicitly report limitations, write `作者未明确报告局限` and then add the agent's own source-grounded limitation analysis based on experimental setup, datasets, metrics, baselines, failure cases, assumptions, or deployment conditions. Clearly distinguish author-reported limitations from agent analysis; do not disguise speculation as an author claim.
- Put user-specific interpretation, brainstormed research ideas, possible extensions, and project-specific transfer only in `启发`. This slot can be freer than `局限`, but should still be useful for the user's research direction.
- Do not append ranking tails such as `相关性：10/10` or `优先级：A` inside the card unless the user explicitly asks for a separate triage/ranking table.
- Keep verified absence status inside the affected metadata field or bullet, for example `w/o. verified code`, `Not reported`, `N/A`, `不适用`, or `计算资源：未报告`. `待核验`, `candidate`, TODO/TBD/pending verification text, and broad `核验说明` disclaimers must not remain in paper-card delivery. When they appear, fetch the official source and resolve them before writing back. `无法获取原文` is not a replacement for `待核验`; use it only after exhausting official acquisition/extraction routes, and record it outside the finished card as a blocker. Figure and caption fields are stricter: formal delivery must not use any `配图待补` / `图注待补` / `图片待补` / `待补图注` / figure TODO-style text as a verification status.

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

The paper-card visual slot should be a reliable one- or two-figure group. For new cards, the preferred layout is a side-by-side pair when both figures exist: a teaser / visual result / problem-context figure plus a pipeline / method overview / architecture / process figure. The method/process figure remains the anchor when available: pipeline, workflow, architecture with stages/arrows, method/training/inference/data flow, benchmark construction flow, or computation/loss flow.

If no teaser figure is available, use the pipeline/method overview figure alone. Do not force a weak teaser just to make a two-image layout.

Do not use as the only card image when a process figure exists:

- title page, first page, abstract page, PDF page render;
- teaser, result showcase, qualitative collage, demo gallery;
- generic overview without clear stages/modules/data/control flow.

When using two figures, put the teaser first and the method/process figure second unless the official paper's own combined layout clearly implies another order. In Feishu, place them as a same-row native image group/grid with adaptive widths: preserve each image's original aspect ratio and readable scale, use relative column widths that fit the actual image shapes, and do not force equal-width columns if that makes a dense pipeline unreadable. On narrow viewports, allow the document to wrap/stack naturally rather than shrinking text to illegibility.

Each selected figure must pass visual QA independently. Reject all-black, near-all-black, or mostly dark low-information images when they are likely web hero backgrounds, dark-mode browser/page screenshots, transparent PNGs rendered on a black background, failed/partial loading frames, UI wrappers, or screenshots whose actual figure content is unreadable. A dark or black background is acceptable only when it is clearly the official paper figure itself and the figure content, labels, legends, and caption alignment remain readable; when possible, crop away surrounding dark page/UI/background and prefer an official HTML asset, PDF figure crop, or MinerU extraction on a normal paper background. If a teaser is black/near-black or weak, omit it rather than weakening the card; the method/process figure remains sufficient.

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

For PDF-only papers, or papers whose user-approved / official HTML / project sources do not expose a usable method/process figure, use MinerU before any agent manual PDF crop. On this machine, the preferred path is `$WORLD_MODEL_VAULT/.tools/mineru-md.sh` backed by the local MinerU environment. Use the MinerU output to locate extracted figure files and figure captions, then insert those native figure assets. Treat MinerU output as a conversion draft: verify figure number, caption, and visual content against the official PDF before writing. If MinerU fails or produces mismatched/low-quality figures, continue with a manually cropped PDF figure only when it can be visually verified against the original caption and the failure of user-approved / HTML / project / MinerU sources is recorded in the working notes. If no verified figure can be produced, do not deliver a finished card; stop, report the blocker, or explicitly label the whole page as a draft.

Agent manual PDF crop quality standard, for last-resort crops only:

- Render from the source PDF at high resolution instead of taking a screen capture from Preview, Chrome, or a PDF viewer. Use structured extraction first; if rendering is needed, render the relevant page at >= 300 DPI, preferably 450-600 DPI for dense pipeline diagrams or small labels, then crop from that render.
- Crop the actual figure area, not the whole page. Keep method-stage arrows, legends, axis labels, subfigure labels, and in-figure text that are part of the figure; exclude unrelated body text, headers/footers, neighboring figures, and page margins. Keep the printed caption out of the image unless the caption is visually inseparable from the figure; the translated caption belongs in the native caption field.
- Preserve aspect ratio and use a lossless format such as PNG for diagrams. Do not square-crop, stretch, JPEG-recompress, blur, or use AI upscaling/retouching that can alter text or diagram content.
- If the cropped figure is visually soft, too small, or hard to read at normal Feishu card width, rerender at higher DPI and recrop. If it remains unreadable or ambiguous, do not ship the card as finished; continue extraction or mark the overall deliverable as a draft/blocker.
- Before upload, visually inspect the crop locally or in a contact sheet and verify figure number, panel labels, and caption match the official paper. After Feishu upload, fetch back and verify native image dimensions/aspect ratio, no `512 x 512` fallback, and no visible blur introduced by the upload.

Every selected figure needs the complete Chinese translation of the official original caption, including figure number, subfigure labels, symbols, method names, dataset names, and important technical terms. This applies independently to teaser figures and method/process figures in a two-figure group. The caption must not be replaced by an agent-written summary such as `method or experiment overview` / `方法或实验概览` or by an explanation of what the figure is "used to show". If no verified caption exists, do not deliver the card as finished. A `图注待补` caption is allowed only in an explicitly labeled draft or work-in-progress page and must fail final validation.

For Feishu, insert images as native image blocks after the metadata and `Dataset`, before the seven bullet slots, and put the complete Chinese caption into each native image caption field. If the card has both a teaser and a method/process figure, insert them as one same-row image group/grid rather than two distant vertical figures; preserve adaptive sizing, original aspect ratios, readable dimensions, captions, and order. If the caption has no formula, native caption placement is mandatory: do not leave the figure caption as a separate ordinary paragraph below the image. If the caption contains inline formulas, displayed formulas, or a formula-rendering fallback that the native caption field cannot preserve, an immediately adjacent caption paragraph is acceptable; preserve the exact TeX source and keep it visually tied to the image. Preserve existing image blocks, same-row layouts, grid ratios, dimensions, captions, and order. Never rewrite a rich page just to normalize text.

If a card is copied or reused across Feishu pages, preserve already approved paper-card figures and captions unless there is a page-specific reason to change them. If no reliable method/process figure exists after checking official sources, do not fill the slot with a weak visual and do not write `配图待补`; report the card/page as not ready for formal delivery.

Before batch-inserting figures into Feishu, create and visually inspect a contact sheet or equivalent preview of all selected images. Reject and replace any selected image that is an HTML banner, logo, author/avatar photo, OJS/publisher UI artifact, title-page render, mostly text-only PDF crop, result-only qualitative collage when a method figure exists, all-black / near-all-black / mostly dark with unreadable content, a transparent image rendered against black, a dark-mode web screenshot, a loading/failure frame, or a crop whose caption belongs to another figure. If an image appears black after Feishu upload or fetch-back, inspect its source pixels/dimensions/thumbnail and replace it with a verified official asset, MinerU extraction, or PDF crop instead of accepting the uploaded block.

## Context-Specific Rules

Survey / research-map cards:

- A `Paper Cards` page is a collection page containing many cards in sequence. Do not create one child page per paper unless the user explicitly asks.
- Group cards by the survey's actual theme, method family, narrative arc, or reading priority when that improves scanning.
- Use report/source context to decide which papers deserve cards, but do not fill card facts from plausibility. If a paper is important but not fully verified yet, fetch the official paper source and resolve the missing fields before delivering the card; otherwise list it outside the card section as a source-verification TODO.
- Reject placeholder cards in formal delivery. A card with missing figure or missing caption is not complete, even if all text fields are filled. For survey-scale work, reduce the number of delivered cards or label the page as a draft instead of shipping `配图待补` placeholders.

Meeting / transcript cards:

- Personal notes, supplied PDF links, screenshots, and visible figures can guide importance and context, but finished claims still require official paper sources.
- If a paper title comes only from an imperfect transcript or speech clue, do not fabricate a paper card. Put it in a separate source-verification TODO such as `口播线索：需从官方论文核验 <title clue>`; finished meeting paper cards still require official paper-source verification.
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
- No `待核验`, `candidate`, TODO/TBD/pending verification markers, broad verification disclaimers, or other unresolved source-verification statuses remain in formal delivery.
- `Dataset:` filled from source or explicitly marked, with at most three visible dataset names separated by ASCII comma plus space; extra training/evaluation datasets belong in `实现`.
- Papers using open-source/pretrained base models include `| Base:` on the `Dataset:` line with at most three visible base model names, sourced from official paper/project/code evidence; fine-tuning/frozen/direct-use details belong in `实现` when too long.
- Papers using a simulator or simulation environment include `| Simulation:` on the `Dataset:` line, sourced from official paper/project evidence or marked `Simulation: 未报告` only when simulation is clearly involved but the specific environment is not reported. Papers that do not involve simulation must omit the `Simulation:` field entirely.
- Method/process figure selected from official source or user-approved source for every card when available; if a teaser is also available, the new card uses a same-row teaser + method/process figure group. No `配图待补`, `图注待补`, empty image slot, or text-only image TODO remains in a finished page.
- User-provided or user-approved screenshots/crops were checked first; HTML / project-page figure search was completed before any agent PDF fallback, and no agent PDF screenshot/crop was used when a usable user-approved or HTML/project figure with matching caption exists.
- If PDF fallback was needed, MinerU extraction was attempted before agent manual screenshot/crop unless MinerU is unavailable; any remaining agent manual crop was visually QA'd against the official PDF, and the reason user-approved / HTML / project / MinerU sources could not be used is recorded in task notes.
- Any last-resort agent manual PDF crop was rendered from the PDF at high DPI, tightly cropped, saved losslessly, visually inspected before upload, and fetched back from Feishu to verify dimensions/aspect ratio and readability.
- Selected figures are not all-black, near-all-black, failed-render frames, dark-mode web screenshots, or transparent images rendered on black unless the official paper figure itself is intentionally dark and still readable. In a two-figure group, both the teaser and method/process figure pass this check independently.
- Figure caption is complete Chinese translation of the original caption, optionally ending with only one short source tag (`来源：用户截图`, `来源：HTML`, `来源：MinerU PDF 截图`, or `来源：PDF 截图`). Captions must not contain generic filler like `用于说明...`, `核心流程、输入输出关系和关键模块`, `原始 caption 已在图中保留`, or `便于回溯核验`. In Feishu, no-formula captions are native image captions, while formula-bearing captions may use a directly adjacent paragraph only to preserve formula fidelity.
- Seven fixed bullet slots present and source-grounded.
- Reader-facing Chinese prose uses Chinese-first terms; no raw translatable English phrase islands such as `parametric human estimation`, `perspective distortion`, or `scene geometry`.
- `结论` reflects authors' claims; `局限` distinguishes author-reported limitations from agent analysis; user takeaways are only in `启发`.
- No local-path/Obsidian residue in reader-facing text: `assets/`, `![[`, `EW_IMG`, `图像：`, local filenames, or vault paths.
- For Feishu writes: page fetched back after writing; hierarchy, title, image count/layout, and card count verified.

## Validation Script

Run the bundled structural validator on local Markdown drafts before syncing:

```bash
python .tools/skills/paper-card-delivery/scripts/validate_paper_card.py path/to/cards.md
```

The script catches missing headings, missing or non-compact metadata lines, `Dataset:`, dataset lists longer than three visible names, malformed or misspelled `Base:` / `Simulation:` metadata, unnecessary default `Simulation: 未报告` placeholders, fixed bullet slots, legacy `边界 / 启发` slots, missing `核心创新` bullets, `待核验` / candidate verification markers, `配图待补` / `图注待补` placeholders, generic caption filler, verbose source-label prose, local-path residue, common forbidden images, and known raw English phrases that should be Chinese-first. It cannot prove official-source verification, caption translation completeness, or whether a limitation was truly author-reported; the agent must still state the source evidence it inspected.

For Feishu pages, do not rely on fetched Markdown alone to verify compact metadata. Feishu's Markdown export can render hard line breaks inside one native text block as blank-separated lines, which is indistinguishable from four loose paragraphs in plain Markdown. After writing to Feishu, fetch the Docx blocks and run the block-level validator:

```bash
lark-cli api GET /open-apis/docx/v1/documents/<docx_token>/blocks \
  --as user --params '{"page_size":500}' > blocks.json
python .tools/skills/paper-card-delivery/scripts/validate_feishu_paper_card_blocks.py blocks.json
```

The block-level validator is authoritative for Feishu compact metadata and image caption placement: each card heading must be followed by exactly one normal text block whose content has four non-empty hard-break lines: takeaway, `Venue｜Institution`, `PDF｜Project｜Code`, and `Dataset:`; each card must then use one native image block or a same-row native image group whose image caption fields contain complete Chinese figure captions, unless a formula-bearing caption requires an adjacent paragraph fallback. A separate `图 N｜...图注...` paragraph after the image is an error when the caption has no formula; formula-bearing captions may remain adjacent as a fidelity fallback. Cards with `待核验` / candidate verification markers, `配图待补`, `图注待补`, generic caption filler, verbose source-label prose, no image block, or image blocks without captions must fail validation. It also checks CVF PDF links for title-shortening errors when the PDF filename exposes a longer official title than the card heading.

## Sorting

Within the same page or section, sort normal paper cards newest to oldest. Prefer formal venue year/date; otherwise use arXiv first/latest version date. Survey, overview, or roadmap cards may appear at the top only when the section is explicitly named `Survey`, `Overview`, or `Roadmap`.
