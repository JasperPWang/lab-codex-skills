---
name: paper-card-delivery
description: Canonical platform-neutral delivery standard for source-grounded research paper cards in Feishu/Lark, Notion, Obsidian/Markdown, surveys, deep dives, meeting notes, and project notes. Use whenever the user asks to整理/补全/生成/审核 paper card, 论文卡片, Paper Cards, literature survey cards, meeting paper cards, or deep-dive paper cards; also use when another research workflow will create or modify paper cards.
---

# Paper Card Delivery

## Core Contract

Treat paper-card work as source verification, not formatting. A finished card is allowed only after inspecting the official full-paper source end to end enough to verify the card fields: abstract, method, experiment/evaluation, conclusion/discussion, limitations when present, affiliations, datasets, code/project links, and selected figure captions.

Two failures disqualify a paper card from delivery. First, do not write plausible-sounding claims by inference when the official original paper has not been read; that is fabrication, even if the claim sounds likely from the title, abstract, project page, or method family. Second, if the official original paper is accessible by PDF, HTML, publisher/conference page, arXiv/OpenReview/CVF page, project page, official code, local rendering, MinerU extraction, or OCR, do not leave `待核验`; continue source extraction and resolve the field.

If a field is `待核验`, the required next action is to inspect the official full-paper source or other official source until the field is resolved. Do not leave `待核验` in reader-facing paper cards. A finished paper-card delivery must contain no `待核验`, `candidate`, TODO/TBD/pending verification text, or other unresolved verification markers. For missing information, use `未报告`, `Not reported`, `N/A`, or `不适用` only after checking the official paper/project/code sources and confirming the item is not reported or not applicable. `无法获取原文` is allowed only after every reasonable official acquisition route has failed, including official HTML, official PDF, arXiv/OpenReview/CVF/publisher/conference pages, DOI landing page, project page, author/lab page, official repository, local PDF download/rendering, and available extraction/OCR routes such as MinerU. When that happens, report a blocker with the attempted routes instead of shipping a finished card.

For formal delivery, every paper card must include a verified method/process figure or a user-approved figure, with a complete Chinese caption. Do not deliver cards with `配图待补`, `图注待补`, `图片待补`, `图像待补`, `待补配图`, `待补图注`, empty image slots, or text-only figure/caption TODO/TBD/pending notes. Any reader-facing sentence like `配图待补：优先从官方论文 HTML / PDF 中提取...` is a hard delivery failure, not an acceptable caveat. If the figure cannot be obtained within the current turn, continue extraction, explicitly downgrade the page to a draft, reduce scope with the user's approval, or report that the deliverable is blocked. Never mark a paper-card page complete while any card is missing its figure or figure caption.

Paper card is a lightweight reader index after source verification. It is not a full deep dive, not a PDF-to-Markdown manuscript, not a complete translation, and not a substitute for `paper-deep-dive`. If the user asks to 深读 / detailed-read / dive into one paper, use `paper-deep-dive` and create the paper card as only one component of that larger package.

Use [`research-doc-workflow`](../research-doc-workflow/SKILL.md) for platform selection, hierarchy, image/caption representation, and post-write verification. After the platform is resolved, also use the matching adapter: [`feishu-doc-workflow`](../feishu-doc-workflow/SKILL.md) for Feishu/Lark, [`notion-doc-workflow`](../notion-doc-workflow/SKILL.md) for Notion, or [`obsidian-doc-workflow`](../obsidian-doc-workflow/SKILL.md) for Obsidian/vault Markdown.

For any reader-facing Chinese prose in the card, also use [`chinese-technical-writing`](../chinese-technical-writing/SKILL.md). This card skill adds paper-card-specific structure; the broader Chinese-first terminology standard lives there.

## Mechanism Reasoning Gate

Before drafting the visible card, reconstruct the strongest version of the paper's argument and answer five internal questions from the full paper: what concrete failure mechanism blocks prior methods; what key assumption makes the proposed route plausible; how each design changes the information, constraint, optimization, or supervision available to that bottleneck; which experiment, control, or ablation actually supports that mechanism; and under which changed data, scene, or assumption the route should fail. This is a pre-writing reasoning gate, not an extra reader-facing section. Do not add a `五问`, `机制审问`, or similar questionnaire to every card.

Compress that reasoning into the existing seven fields:

- `问题` identifies the causal bottleneck or failure mode, not a generic complaint such as low accuracy, high cost, or poor generalization.
- `方法` states the key working assumption. Each `核心创新` should explain `设计 -> 改变了什么信息/约束 -> 为什么预期有效`, rather than list module names.
- `实现` prioritizes the decisive control, ablation, or result for the claimed mechanism. State when the evidence is only correlational or does not rule out a simpler alternative explanation.
- `结论` remains the authors' conclusion and must not be upgraded beyond their evidence.
- `局限` names the assumption or condition that breaks and the resulting failure; distinguish author-reported limitations from source-grounded analysis.
- `启发` starts from a paper-specific counterfactual, minimal necessary design, simpler alternative, diagnostic, or testable next question. Connect to the user's broader research vision only when the paper itself supports that bridge.

Keep evidence status mentally and, when ambiguity matters, textually distinct as `作者声称`, `实验支持`, `我们的推断`, or `尚未验证`. A card is not semantically complete unless the writer can draw its causal chain without the source, predict what removing a claimed key module should change, point to the decisive evidence, and name the boundary where the explanation stops applying. Structural validators check delivery shape and wording duplication; they cannot prove understanding and must never be replaced with keyword checks for these concepts.

## Platform Delivery Contract

Use the same Markdown card skeleton on every platform. The fixed fields, source-verification standard, bullet-length budget, figure-selection priority, wording, and sorting rules are identical; adapt only the few unsupported representation details:

- Feishu/Lark: one compact four-line native metadata block, native image block and native caption, followed by the seven bullet slots; verify with the Docx block validator.
- Notion: one compact metadata paragraph with four logical rows separated by native hard line breaks, native image block and image caption, followed by the seven bullet slots. In the Markdown adapter, encode the four rows as one physical line with exactly three `<br>` tags so the importer creates one paragraph block; never use four physical Markdown lines or trailing-space line breaks, which create four paragraphs. Re-fetch native blocks and verify that the metadata region contains exactly one paragraph whose rich text includes three newline characters.
- Obsidian/Markdown: preserve the four physical metadata lines, use a relative image path with the complete Chinese caption in meaningful alt text or the established vault caption convention, and keep assets under a stable local asset directory; run the Markdown validator with `--target obsidian`.

Do not paste Feishu block tokens into Notion or Obsidian, and do not strip valid Obsidian frontmatter, wikilinks, or relative asset paths merely because the Feishu adapter would reject them.

## Required Source Order

Use primary sources first:

1. Official paper HTML, preferably arXiv HTML for arXiv papers.
2. Official PDF, preferring the arXiv PDF when an arXiv version exists and is usable; otherwise use CVF, OpenReview, publisher, conference, or author/lab PDF.
3. Official project page, official code repository, author/lab page, and conference metadata.
4. Secondary sources only for discovery/context, not for finished claims.

Do not finalize method, implementation, conclusion, limitation, compute, dataset, or figure claims from abstracts, snippets, project pages, README files, slides, screenshots, search results, or secondary summaries alone.

## Fixed Card Format

Use this exact compact format by default:

```markdown
#### Paper English Title
短译名｜核心创新点 / takeaway 短语
Venue｜Institution
[PDF](...)｜[Supplement](...) or w/o. supplement if venue/publisher PDF is used｜[Project](...) or w/o. project page｜[Code](...) or w/o. verified code
Dataset: ... | <Simulation: simulator only if actually used> | <open-source backbone>，<training/adaptation mode>

![图 N｜完整中文图注：...](relative-image-path)

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
[PDF](https://example.com/arxiv-paper.pdf)｜w/o. project page｜w/o. verified code
Dataset: ExampleSet | ExampleBackbone，LoRA 微调

![图 1｜完整中文图注：这里应放原始 caption 的完整中文翻译，包括图号、子图说明和关键术语。来源：HTML](relative-or-native-image)

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

- Start every card with `#### Paper English Title`.
- The heading must be the exact official English paper title from the official paper page, arXiv/OpenReview/CVF/publisher metadata, or the first page of the official PDF. Do not shorten it to a method name, acronym, section/topic label, or locally convenient title when the official title is longer. Conversely, do not invent an explanatory subtitle when the official paper title itself is short, for example `Mapping Networks`.
- The second line must be `短译名｜核心创新点 / takeaway 短语`; do not use a plain translation-only line.
- Keep the title and the four metadata lines as a compact paragraph. In Markdown drafts, use hard line breaks after the short-takeaway, venue/institution, and link lines, and do not insert blank lines inside the metadata block.
- `Venue｜Institution` is the accepted / published journal, conference, workshop, or arXiv status plus publishing institutions/affiliations, not a long author list and not determined by which PDF URL is used. If a paper has an arXiv PDF but was accepted to CVPR / SIGGRAPH / NeurIPS / ACM TOG / IEEE TPAMI / etc., keep that venue on this line and use the arXiv PDF in the link line when preferred. Verify affiliations from official HTML/PDF/proceedings/project metadata when available. Use 1-3 primary official institutions/labs and keep visible entities <= 5. Use authors only when affiliations cannot be verified.
- Use compact link labels: `[PDF](...)｜[Project](...)｜[Code](...)`; when an official venue/publisher/conference PDF is used instead of an available arXiv PDF, add `[Supplement](...)`, `[Appendix](...)`, or `[Suppl.](...)` on the same link line before `Project` when a supplementary/appendix PDF exists. If no supplementary/appendix PDF exists after search, write `w/o. supplement` on that same link line; do not omit the supplement status silently. For missing links use exactly `w/o. PDF`, `w/o. supplement`, `w/o. project page`, or `w/o. verified code` / `w/o. code`.
- `PDF` must point directly to a PDF when one exists, not an abstract/search/project page. Prefer the arXiv PDF link (`https://arxiv.org/pdf/<id>`) when arXiv is available, because it is usually stable and often includes appendices omitted from proceedings PDFs. Do not let the PDF link choice overwrite the venue metadata: the venue line still records the accepted / published venue.
- Use an official venue/publisher/conference PDF as the `PDF` link only when no usable arXiv PDF exists, the arXiv version is incomplete/wrong for the target card, or the user explicitly asks for the official proceedings version. In that case, search for supplementary / appendix / additional-material PDFs on the proceedings page, official HTML, OpenReview, project page, author/lab page, and arXiv. If a supplement exists, include it on the same metadata link line as `[Supplement](...)` or `[Appendix](...)`; if no supplement is found after search, write `w/o. supplement` on the same link line and record the searched routes in task notes rather than inventing a link.
- Always search for code before finalizing a card: paper text, official project page, author/lab page, official organization, and GitHub by paper title / method name / lead author. Mark code as verified only when it is official or clearly author-maintained.
- `Dataset:` is mandatory. Keep it terse: dataset names only. Do not infer datasets from method family. If the official source does not report a dataset after checking the paper/project/code sources, write `Dataset: 未报告`; use `Dataset: 待核验` only in an explicitly marked draft, never in a completed card.
- Append `| Simulation: ...` only when the paper actually uses a simulator, simulation environment, physics engine, synthetic simulation tool, or physics-based data-generation environment in the method, dataset construction, training, evaluation, or ablation. Examples: `Dataset: ... | Simulation: CLO3D / Marvelous Designer`, `Dataset: ... | Simulation: MuJoCo / Isaac Gym`, or `Dataset: ... | Simulation: Blender / SAPIEN`. Use official paper/project/HTML evidence; do not infer a simulator from the task family, from the word `simulation-ready`, or from the user's research context.
- If the paper does not use a simulator or simulation environment, omit the `Simulation:` field entirely. Do not write `Simulation: 未报告`, `Simulation: Not reported`, or `Simulation: 不适用` merely because the paper is about simulation-ready assets, physics plausibility, robot/control, clothing, embodied AI, or synthetic-looking data. If the paper clearly uses simulation but does not name the simulator/environment, write `Simulation: 未报告具体仿真器` and explain the evidence in `实现`.
- For learned-model papers where the author's own method depends on a recognizable open-source backbone, pretrained open-source base model, foundation model, detector, encoder, diffusion/video generator, LLM/VLM, body model, or reconstruction module, append one unlabeled compact suffix on the same metadata line after `Dataset:` / `Simulation:`. Format it as `| <open-source backbone>，<training/adaptation mode>`, for example `| FLUX.1-dev，LoRA 微调`, `| SDXL + ControlNet，冻结基座 + 训练头部`, `| HunyuanVideo，免训练`, `| ViT-B/16，全量训练`, or `| SMPL-X + DINOv2，优化式拟合`. The first part is the paper's own open-source backbone/base, and the second part is the training or adaptation mode.
- Do not write verbose labels such as `Open-source backbone:`, `Backbone:`, `Training:`, or `Open-source baselines:` in metadata. If the paper has no open-source backbone concept, omit the compact suffix or write `| 开源基座不适用，训练方式不适用` when clarity is useful. If the paper clearly uses an open-source backbone but the official source does not report enough detail after checking method / appendix / project / code evidence, write `| 开源基座未报告，训练方式未报告`; use `待核验` only in an explicitly marked draft, never in a completed card.
- Use official method / implementation / appendix / project page / code-config evidence for the compact suffix. Do not infer training mode from model family. Allowed concise training/adaptation labels include `免训练`, `LoRA 微调`, `Adapter 微调`, `冻结基座 + 训练头部`, `全量微调`, `全量训练`, `推理时优化`, `优化式拟合`, `蒸馏`, `prompt-only 推理`, `未报告`, or `不适用`; `待核验` is a draft-only state.
- If a model/method appears only as an experiment comparison baseline, teacher, auxiliary tool, or ablation target, describe it in `实现`, not in metadata. The compact suffix is reserved for the paper's own method open-source backbone/base and its training/adaptation mode. If the same open-source model is both the author's initialization backbone and a comparison baseline in its original form, put it in the compact suffix and explain the baseline role in `实现`.
- End with exactly seven Chinese bullet slots: `定义`, `问题`, `方法`, `实现`, `结论`, `局限`, `启发`.
- Treat every fixed bullet and both nested `核心创新` items as a compact two-line reader note. Measure the body after the label with Chinese-character-equivalent visual width: non-ASCII characters count as `1`, ASCII characters count as `0.5`, and whitespace is ignored. The hard accepted range is `75–100`; write toward `75–95` so small rendering differences do not overflow. Do not pad short bullets with generic prose: return to the official full paper and add source-grounded task, method, experiment, conclusion, or limitation detail. `启发` may use user-specific analysis and ambitious brainstorming, but it must remain concrete enough to suggest a representation, system connection, experiment, or research question.
- The metadata takeaway, figure captions, and seven bullet slots are Chinese-first reader notes. For English terms, write Chinese first and use the English term only as a parenthetical gloss unless it is a method/model/dataset/code name or mathematical symbol.
- `定义` states the task contract: task, input, output, supervision/data type, training/inference flow, and evaluation benchmark/metric names when relevant. Use `未报告` / `不适用` instead of guessing after source verification; use `待核验` only in an explicitly marked draft, never in a completed card.
- `方法` must include one summary sentence and exactly two nested bullets: `核心创新 1` and `核心创新 2`.
- `实现` states how the paper realizes and validates the method: datasets, open-source backbone/base model when used, training/adaptation mode, comparison baselines, key ablations, metrics/results, data source type, and reported compute. Prioritize the experiment or ablation that most directly tests the claimed mechanism instead of dumping every metric. If the result also admits a simpler explanation, say that the alternative is not ruled out. If open-source backbone or training mode is important to the paper, summarize how it is used here after listing the compact suffix in metadata. If open-source methods/models appear only as baselines, teachers, auxiliary tools, or ablation targets, put those details here rather than in metadata. If GPU, memory, time, FPS, latency, or runtime are not reported, write `计算资源：未报告`.
- `结论` must summarize the authors' own conclusion, not the agent's route-level judgment.
- `局限` must prioritize limitations explicitly reported by the authors in limitations, discussion, conclusion, experiment analysis, appendix, or failure-case text. If the paper does not explicitly report limitations, write `作者未明确报告局限` and then add the agent's own source-grounded limitation analysis based on experimental setup, datasets, metrics, baselines, failure cases, assumptions, or deployment conditions. Clearly distinguish author-reported limitations from agent analysis; do not disguise speculation as an author claim.
- Derive `启发` from the paper itself before considering the user's broader vision. Start from a paper-specific representation, mechanism, assumption, failure mode, experimental result, or unresolved question, then propose a concrete extension, comparison, diagnostic, or experiment. Connect it to the user's project only when that bridge follows naturally from the paper and adds specificity; never force every card into the same project narrative.
- Draft every `启发` independently on multi-card pages, then compare them across the page. Reusing a generic sentence template, a shared grand-vision tail, or a lightly paraphrased conclusion is not accepted, even when every bullet passes the width budget. If an idea is short, deepen it with a testable hypothesis, an identifiable variable, an evaluation protocol, or a concrete failure case instead of padding it with broad applications.
- Treat repeated inspiration bodies, near-duplicate wording, or the same normalized ending of 16 or more characters appearing in three or more cards as a delivery failure. Run the destination validator after drafting; its cross-card checks are a guardrail, not a substitute for paper-specific reasoning.
- Do not append ranking tails such as `相关性：10/10` or `优先级：A` inside the card unless the user explicitly asks for a separate triage/ranking table.
- Keep verified missingness inside the affected metadata field or bullet, for example `w/o. verified code`, `Not reported`, `不适用`, or `计算资源：未报告`. Use `待核验` only in an explicitly marked draft/incomplete card; do not add a separate broad `核验说明` / verification disclaimer section unless the user explicitly asks for an audit note.
- Treat the Markdown image alt text in the template as the semantic figure caption. Convert it to the native image-caption field in Feishu or Notion; do not leave a duplicate ordinary caption paragraph after conversion.

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

For PDF-only papers, or papers whose user-approved / official HTML / project sources do not expose a usable method/process figure, use MinerU before any agent manual PDF crop. On this machine, the preferred path is `$WORLD_MODEL_VAULT/.tools/mineru-md.sh` backed by the local MinerU environment. Use the MinerU output to locate extracted figure files and figure captions, then insert those native figure assets. Treat MinerU output as a conversion draft: verify figure number, caption, and visual content against the official PDF before writing. If MinerU fails or produces mismatched/low-quality figures, keep the card draft/incomplete unless a manually cropped PDF figure can be visually verified against the original caption and the failure of user-approved / HTML / project / MinerU sources is recorded in the working notes.

Agent manual PDF crop quality standard, for last-resort crops only:

- Render from the source PDF at high resolution instead of taking a screen capture from Preview, Chrome, or a PDF viewer. Use structured extraction first; if rendering is needed, render the relevant page at >= 300 DPI, preferably 450-600 DPI for dense pipeline diagrams or small labels, then crop from that render.
- Crop the actual figure area, not the whole page. Keep method-stage arrows, legends, axis labels, subfigure labels, and in-figure text that are part of the figure; exclude unrelated body text, headers/footers, neighboring figures, and page margins. Keep the printed caption out of the image unless the caption is visually inseparable from the figure; the translated caption belongs in the native caption field.
- Preserve aspect ratio and use a lossless format such as PNG for diagrams. Do not square-crop, stretch, JPEG-recompress, blur, or use AI upscaling/retouching that can alter text or diagram content.
- If the cropped figure is visually soft, too small, or hard to read at the target platform's normal card width, rerender at higher DPI and recrop. If it remains unreadable or ambiguous, keep the card incomplete rather than shipping a blurry crop.
- Before insertion, visually inspect the crop locally or in a contact sheet and verify figure number, panel labels, and caption match the official paper. After writing, re-fetch or re-read the target and verify dimensions/aspect ratio, caption association, and readability.

Every selected figure needs the complete Chinese translation of the official original caption, including figure number, subfigure labels, symbols, method names, dataset names, and important technical terms. If no verified caption exists, keep the card draft/incomplete; do not ship a reader-facing `图注待补` paragraph as if the card were complete.

Place the image after metadata and `Dataset`, before the seven bullet slots. In Feishu and Notion, use the native image-caption field and do not leave a duplicate ordinary caption paragraph. In Obsidian, use the vault's established caption convention or meaningful Markdown alt text. Preserve existing image blocks/embeds, layouts, dimensions, captions, and order. Never rewrite a rich page or note just to normalize text.

If a card is copied or reused across platforms/pages, preserve already approved paper-card figures and captions unless there is a destination-specific reason to change them. If no reliable method/process figure exists after checking official sources, keep the card draft/incomplete rather than filling the slot with a weak visual.

Before batch-inserting figures into any destination, create and visually inspect a contact sheet or equivalent preview of all selected images. Reject and replace any selected image that is an HTML banner, logo, author/avatar photo, OJS/publisher UI artifact, title-page render, mostly text-only PDF crop, result-only qualitative collage when a method figure exists, or a crop whose caption belongs to another figure.

## Context-Specific Rules

Survey / research-map cards:

- A `Paper Cards` page is a collection page containing many cards in sequence. Do not create one child page per paper unless the user explicitly asks.
- Group cards by the survey's actual theme, method family, narrative arc, or reading priority when that improves scanning.
- Use report/source context to decide which papers deserve cards, but do not fill card facts from plausibility. If a paper is important but not fully verified yet, keep it as an explicitly marked draft/incomplete item rather than presenting it as a finished card.
- Avoid placeholder cards except for genuinely blocked source access after a best-effort check; state the missing item specifically and do not call the page complete.

Meeting / transcript cards:

- Personal notes, supplied PDF links, screenshots, and visible figures can guide importance and context, but finished claims still require official paper sources.
- If a paper title comes only from an imperfect transcript or speech clue, mark it as `口播线索 / 待核验` in working notes or an explicitly incomplete draft, and do not fabricate metadata.
- Prefer user-provided PDF links and figures when present, but still verify title, venue, dataset, conclusion, and caption against official sources before marking the card finished.

Teacher / lab profile cards:

- Put paper cards directly in the teacher/lab page unless the user explicitly asks for a nested `Paper Cards` child page.
- Keep route overview tables separate from cards. A `路线总览` table is navigation, not a second paper-card index.

Obsidian / local Markdown cards:

- If the user explicitly asks to write paper cards to the local vault, store figure assets near the target page under `assets/YYYY-MM-DD/`.
- Use semantic, stable filenames such as `YYYY-MM-DD-short-topic-figure-role.png`, not `image.png`, `image 1.png`, or `figure.png`.
- Markdown image paths should be relative to the target file, and alt text should be a short semantic phrase.
- Remove downloaded PDFs, HTML, OCR/MinerU outputs, temporary crops, and other intermediates after the durable target deliverable is verified, unless the user explicitly asks to keep them.

## Verification Checklist

Before presenting a finished card, explicitly verify:

- Official full paper inspected end to end enough for all reader-facing claims.
- Title, venue/date, institution/affiliation verified. The title check must compare the card heading with official metadata/PDF first-page title; for CVF pages, also compare against the PDF filename slug to catch acronym-only headings.
- PDF, project page, and official/verified code searched. The card uses the arXiv PDF when available and suitable; if it uses an official venue/publisher/conference PDF instead, supplementary/appendix PDFs were searched and any existing supplement link is present on the metadata link line.
- `Dataset:` filled from source or explicitly marked `未报告` / `不适用` after source verification; `Simulation:` is appended only when the paper actually uses a simulator/simulation environment; the open-source backbone and training/adaptation mode are appended as one compact unlabeled suffix such as `| FLUX.1-dev，LoRA 微调` when applicable, or explicitly marked `未报告` / `不适用` inside that suffix. Comparison baselines are checked and written in `实现`, not as metadata.
- Method/process figure selected from official source or user-approved source; if not obtainable, the card remains draft/incomplete rather than shipped with `配图待补`.
- User-provided or user-approved screenshots/crops were checked first; HTML / project-page figure search was completed before any agent PDF fallback, and no agent PDF screenshot/crop was used when a usable user-approved or HTML/project figure with matching caption exists.
- If PDF fallback was needed, MinerU extraction was attempted before agent manual screenshot/crop unless MinerU is unavailable; any remaining agent manual crop was visually QA'd against the official PDF, and the reason user-approved / HTML / project / MinerU sources could not be used is recorded in task notes.
- Any last-resort agent manual PDF crop was rendered from the PDF at high DPI, tightly cropped, saved losslessly, visually inspected before insertion, and verified in the target platform for dimensions/aspect ratio and readability.
- Figure caption is complete Chinese translation of the original caption.
- Seven fixed bullet slots present and source-grounded.
- Reader-facing Chinese prose uses Chinese-first terms; no raw translatable English phrase islands such as `parametric human estimation`, `perspective distortion`, or `scene geometry`.
- `结论` reflects authors' claims; `局限` distinguishes author-reported limitations from agent analysis; user takeaways are only in `启发`.
- For Feishu/Notion writes, no local-path/Obsidian residue remains. For Obsidian writes, relative `assets/` paths and valid wikilinks are allowed, but absolute machine paths, temporary filenames, `EW_IMG`, and web-clipper residue are forbidden.
- The destination was re-fetched or re-read after writing; hierarchy, title, image count/layout, captions, and card count were verified.

## Validation Script

Run the bundled structural validator on local Markdown drafts before syncing:

```bash
python .tools/skills/paper-card-delivery/scripts/validate_paper_card.py path/to/cards.md --target obsidian
```

Set `--target` to `feishu`, `notion`, `obsidian`, or `markdown`. The script catches missing headings, missing or non-compact metadata lines, `Dataset:`, missing compact open-source-backbone/training suffixes when applicable, verbose legacy metadata labels, fixed bullet slots, legacy slots, missing `核心创新` bullets, target-specific residue, common forbidden images, known raw English phrases that should be Chinese-first, and obvious non-arXiv proceedings/publisher PDF link lines that omit a visible supplement status. It cannot prove official-source verification, whether a limitation was truly author-reported, or whether a supplement exists; the agent must still state the source evidence it inspected.

For Feishu pages specifically, do not rely on fetched Markdown alone to verify compact metadata. Feishu's Markdown export can render hard line breaks inside one native text block as blank-separated lines, which is indistinguishable from four loose paragraphs in plain Markdown. After writing to Feishu, fetch the Docx blocks and run the block-level validator:

```bash
lark-cli api GET /open-apis/docx/v1/documents/<docx_token>/blocks \
  --as user --params '{"page_size":500}' > blocks.json
python .tools/skills/paper-card-delivery/scripts/validate_feishu_paper_card_blocks.py blocks.json
```

The block-level validator is authoritative only for Feishu compact metadata and image caption placement. Notion must be verified by re-fetching native page blocks/properties; Obsidian must be verified from the Markdown file and referenced assets.

## Sorting

Within the same page or section, sort normal paper cards newest to oldest. Prefer formal venue year/date; otherwise use arXiv first/latest version date. Survey, overview, or roadmap cards may appear at the top only when the section is explicitly named `Survey`, `Overview`, or `Roadmap`.
