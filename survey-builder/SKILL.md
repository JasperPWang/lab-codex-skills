---
name: survey-builder
description: "Build literature surveys from paper collections: taxonomy, literature tree, challenge-insight tree, novelty tree, method comparison tables, benchmark/dataset map, reading order, and Feishu/Obsidian survey organization. Use when the user asks for Survey Builder, literature tree, challenge-insight tree, novelty tree, survey outline, or 文献综述整理."
---

# Survey Builder

Use this to turn a paper set into a structured survey.

Canonical method reference:
- Before building or revising a literature survey, literature tree, novelty tree, or challenge-insight tree for the user's research wiki, use the user's Feishu method page as the canonical example unless a more specific template is provided: `如何构建literature tree（如何进行literature review，构建novelty tree和challenge-insight tree）`, <FEISHU_OR_LARK_URL> doc token `<DOC_TOKEN>`.
- Follow its four novelty levels when classifying papers: Type 1 = seminal work for a milestone task; Type 2 = seminal work for a novel pipeline or representation; Type 3 = seminal work for a novel module; Type 4 = module-level improvement to an existing pipeline.
- Build the literature tree by collecting papers in the same direction, identifying milestone tasks and first/seminal papers, grouping by milestone task, identifying representative pipelines/representations and their first/seminal papers, subdividing by module-level novelty, then revising milestone tasks as field understanding improves.
- Build the challenge-insight tree by collecting field challenges, grouping solution insights under each challenge, then attaching representative papers and remaining gaps. Anchor every challenge and insight in actual papers and the user's research goal; do not create a generic taxonomy detached from the literature.

Required outputs by default:
1. Scope and research question.
2. Literature tree: general goal -> milestone tasks -> method families / representations -> seminal papers.
3. Challenge-insight tree: challenge -> failure mode -> insight -> representative papers -> remaining gap.
4. Paper matrix: task, input/output, supervision, method, benchmark, metric, compute, limitation.
5. Recommended reading path and research opportunity.

For Feishu research-map pages, follow the user's convention: concise parent page, `Tree Maps` subpage, one collection-style `Paper Cards` page, and `Full Survey Report` subpage. Paper Cards are a page containing many cards, not one page per paper.

For any formal paper card in a Feishu research-map or survey deliverable, first read or search the official full-paper source end to end. Abstracts, project pages, README files, slides, screenshots, search snippets, and secondary summaries can help find metadata and links, but they do not justify a finished paper card. If official full-paper verification has not been completed, mark the card as `candidate / 待核验` or leave a verification TODO instead of presenting it as complete.

For paper-card images in surveys, the main image must be the paper's core method/process figure when available: method, pipeline, framework, system overview, architecture, data flow, benchmark construction, or score/loss/computation flow. Do not use a teaser, qualitative showcase, result collage, demo gallery, or visual example grid as the only card image when a core method/process figure exists in the official paper HTML/PDF or project page. A teaser can be a second supplementary image only when it adds distinct context and is clearly captioned as teaser / result showcase. If no core method/process figure exists after checking official sources, state that explicitly and use the most structurally informative fallback figure rather than silently presenting a teaser as the method image.

Every survey paper-card figure caption must be the complete Chinese translation of the official source figure caption, including figure number, subfigure labels, symbols, method names, dataset names, and important technical terms. Do not replace the caption with a short label such as `图｜GS-IR overview`, `图｜pipeline`, `图｜teaser`, a local filename, or a self-written summary. If the official caption has not been found and translated in full, mark `图注待补` and treat the card as incomplete.
