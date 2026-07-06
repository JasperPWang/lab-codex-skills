---
name: survey-builder
description: "Build literature surveys from paper collections: taxonomy, literature tree, challenge-insight tree, novelty tree, method comparison tables, benchmark/dataset map, reading order, and Feishu/Obsidian survey organization. Use when the user asks for Survey Builder, literature tree, challenge-insight tree, novelty tree, survey outline, or 文献综述整理."
---

# Survey Builder

Use this to turn a paper set into a structured survey.

## Canonical Paper Card Gate

When a survey includes paper cards, also use [`paper-card-delivery`](../paper-card-delivery/SKILL.md). That skill is the canonical standard for official-source verification, fixed card format, figure/caption selection, sorting, and validation. Survey Builder must not finalize cards from its local summary rules alone.

## Canonical Chinese Technical Writing Gate

For Chinese survey prose, taxonomy descriptions, challenge-insight explanations, paper matrices, reading routes, Feishu captions, and non-bilingual mind-map/table labels, also use [`chinese-technical-writing`](../chinese-technical-writing/SKILL.md). Keep required bilingual mind-map nodes as English newline Chinese when specified, but write ordinary Chinese explanation in Chinese-first terminology.

## Borrowed Research Method Layer

This is the user's Feishu-native literature-tree workflow. It may borrow useful
research methods from downloaded skills, but those skills do not own the final
survey format.

- From `deep-research`, borrow research-question clarification, scope
  boundaries, search strategy design, source verification, contradiction
  disclosure, synthesis / gap analysis, and devil's-advocate checks.
- Do not publish the external `deep-research` APA report, PRISMA report, or
  agent transcript as the final Feishu survey unless the user explicitly asks
  for that report as a separate `Full Survey Report` source page.
- Translate the borrowed method output into the user's survey artifacts:
  literature tree, challenge-insight tree, novelty tree, paper matrix, reading
  route, research gaps, and one collection-style `Paper Cards` page.
- Keep paper-card creation under `paper-card-delivery`, Feishu hierarchy and
  native blocks under `feishu-doc-workflow`, and Chinese prose under
  `chinese-technical-writing`.

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
5. Research entry-points tree: opportunity -> problem framing -> literature gap -> core hypothesis -> technical route -> data / benchmark -> evaluation signal -> risk / boundary -> next experiment.
6. Recommended reading path and research opportunity.

For Feishu research-map pages, follow the user's current convention: the parent page must be the main literature-review entry and include the editable tree maps directly, then link only to one collection-style `Paper Cards` page and one `Full Survey Report` page when those artifacts are needed. Do not make the parent page a thin hub that only links to a separate `Tree Maps` child page. By default the parent page should contain three native, editable Feishu mind maps: `General Goal Literature Tree`, `Challenge-Insight Tree`, and `Research Entry Points Tree`. Create a dedicated `Tree Maps` child page only when the user explicitly asks for it or the tree content is too large for the parent; in that exception, the parent must still contain a compact tree-map summary and direct links to the maps. Paper Cards are a page containing many cards, not one page per paper.

When repairing an older Feishu survey that already has a separate `Tree Maps` child page, merge the Tree Maps content back into the parent page first: copy or recreate the native Feishu mind maps in the parent page, remove the Tree Maps link from the parent `子页面` list, and keep the old child page only as a non-primary legacy copy unless the user explicitly asks to delete it. Do not add a duplicate bilingual editable outline / table below a native Feishu mind map by default; the mind map itself is the editable artifact. Add a compact textual outline only when the mind map cannot be edited reliably, the user explicitly asks for a fallback, or the tree is too large to navigate in the board alone.

For Feishu literature-review pages that require native mind maps, each mind-map node must be bilingual in the exact visual form `English` newline `Chinese`. Do not deliver all-English mind maps or one-line `English / 中文` substitutes. If Feishu imports PlantUML `\n` as literal text, repair the native whiteboard raw JSON so each `mind_map` node's `text.text` uses an actual newline, then verify with a preview image before delivery.

The `Research Entry Points Tree` is mandatory for Feishu literature-review / research-map pages unless the user explicitly excludes it. It should be comprehensive and decision-useful, not a shallow list of topic names. For each major direction, include bilingual nodes for problem framing, why-now / literature gap, core hypothesis, candidate route or pipeline, required data / benchmark, evaluation signal, compute / cost when relevant, expected contribution / novelty type, risks / boundaries, and the next concrete experiment. Do not duplicate this tree as a textual editable outline by default; the native mind map is the editable artifact.

For any formal paper card in a Feishu research-map or survey deliverable, use [`paper-card-delivery`](../paper-card-delivery/SKILL.md) as the only content standard. This skill may decide grouping, taxonomy, reading order, and survey page structure, but it must not redefine paper-card source verification, metadata, figure/caption choice, fixed bullet slots, sorting, or validation.
