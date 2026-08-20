---
name: survey-builder
description: "Build literature surveys from paper collections: taxonomy, literature tree, challenge-insight tree, novelty tree, method comparison tables, benchmark/dataset map, reading order, and Feishu/Lark, Notion, or Obsidian survey organization. Use when the user asks for Survey Builder, literature tree, challenge-insight tree, novelty tree, survey outline, or 文献综述整理."
---

# Survey Builder

Use this to turn a paper set into a structured survey.

## Canonical Paper Card Gate

When a survey includes paper cards, also use [`paper-card-delivery`](../paper-card-delivery/SKILL.md). That skill is the canonical standard for official-source verification, fixed card format, figure/caption selection, sorting, and validation. Survey Builder must not finalize cards from its local summary rules alone.

## Canonical Chinese Technical Writing Gate

For Chinese survey prose, taxonomy descriptions, challenge-insight explanations, paper matrices, reading routes, figure captions, and non-bilingual mind-map/table labels, also use [`chinese-technical-writing`](../chinese-technical-writing/SKILL.md). Keep required bilingual mind-map nodes as English newline Chinese when specified, but write ordinary Chinese explanation in Chinese-first terminology.

## Canonical Platform Delivery Gate

Use [`research-doc-workflow`](../research-doc-workflow/SKILL.md) and the matching platform adapter (`feishu-doc-workflow`, `notion-doc-workflow`, or `obsidian-doc-workflow`) to deliver the same Markdown-first survey structure to Feishu/Lark, Notion, or Obsidian. Keep headings, tables, lists, links, and prose identical; adapt only tree widgets, page/database hierarchy, captions, properties/frontmatter, and verification. Do not require a Feishu page when the user supplied a Notion or Obsidian target.

## Borrowed Research Method Layer

This is the user's canonical literature-tree workflow. It may borrow useful research methods from downloaded skills, but those skills do not own the final survey semantics or target-platform structure.

- From `deep-research`, borrow research-question clarification, scope
  boundaries, search strategy design, source verification, contradiction
  disclosure, synthesis / gap analysis, and devil's-advocate checks.
- Do not publish the external `deep-research` APA report, PRISMA report, or
  agent transcript as the final survey unless the user explicitly asks
  for that report as a separate `Full Survey Report` source page.
- Translate the borrowed method output into the user's survey artifacts:
  literature tree, challenge-insight tree, novelty tree, paper matrix, reading
  route, research gaps, and one collection-style `Paper Cards` page.
- Keep paper-card creation under `paper-card-delivery`, platform hierarchy and native blocks under `research-doc-workflow` plus the matching `*-doc-workflow`, and Chinese prose under `chinese-technical-writing`.

Canonical method reference:
- Before building or revising a literature survey, literature tree, novelty tree, or challenge-insight tree for the user's research wiki, use the user's Feishu method page as the canonical example unless a more specific template is provided: `如何构建literature tree（如何进行literature review，构建novelty tree和challenge-insight tree）`, <FEISHU_OR_LARK_URL> doc token `<DOC_TOKEN>`.
- Follow its four novelty levels when classifying papers: Type 1 = seminal work for a milestone task; Type 2 = seminal work for a novel pipeline or representation; Type 3 = seminal work for a novel module; Type 4 = module-level improvement to an existing pipeline.
- Build the literature tree by collecting papers in the same direction, identifying milestone tasks and first/seminal papers, grouping by milestone task, identifying representative pipelines/representations and their first/seminal papers, subdividing by module-level novelty, then revising milestone tasks as field understanding improves.
- Build the challenge-insight tree by collecting field challenges, grouping solution insights under each challenge, then attaching representative papers and remaining gaps. Anchor every challenge and insight in actual papers and the user's research goal; do not create a generic taxonomy detached from the literature.

## Mechanism Synthesis Gate

Build the survey around competing explanations, not only task names, years, representations, or module inventories. For each important method family, identify the concrete bottleneck, key assumption, proposed mechanism, decisive evidence, unresolved alternative explanation, and boundary condition. When papers disagree, explain whether the disagreement comes from different assumptions, data regimes, supervision, metrics, or evaluation protocols instead of averaging their conclusions.

Use the tree and matrix artifacts as complementary reasoning tools:

- Keep the literature tree readable, but attach a method family's key assumption or causal mechanism when it explains why that branch exists.
- Build the challenge-insight tree as `challenge/failure mode -> competing explanation -> proposed insight/mechanism -> representative papers -> decisive evidence -> unresolved alternative -> remaining gap` where the literature supports that depth. Do not repeat every node merely to satisfy this schema.
- Use the paper matrix to compare task/input/output plus bottleneck, key assumption, mechanism, decisive evidence or ablation, whether a relevant alternative was controlled, and failure boundary. Omit unsupported cells rather than inventing certainty or creating an unreadable table.
- Derive research opportunities from an unresolved mechanism or evidence gap. A bare combination claim such as `no one has combined A + B` is not a sufficient opportunity without a causal hypothesis and a discriminating experiment.

Before delivery, verify that the survey can explain why representative papers differ, which mechanisms are actually supported, what evidence remains ambiguous, and which next experiment would separate competing explanations. This is a semantic review; do not add keyword-based validators or empty `机制` headings to make the artifact appear compliant.

Required outputs by default:
1. Scope and research question.
2. Literature tree: general goal -> milestone tasks -> method families / representations -> seminal papers.
3. Challenge-insight tree: challenge / failure mode -> competing explanation -> insight / mechanism -> representative papers -> decisive evidence -> unresolved alternative -> remaining gap.
4. Paper matrix: task, input/output, supervision, bottleneck, key assumption, mechanism, decisive evidence / ablation, alternative explanation status, benchmark, compute, and failure boundary.
5. GitHub resource map: high-signal Awesome / survey / benchmark / code-list repositories, with star count, last meaningful update, maintainer/source credibility, what they cover, and what they add to the survey.
6. Research entry-points tree: opportunity -> problem framing -> literature gap -> core hypothesis -> technical route -> data / benchmark -> evaluation signal -> risk / boundary -> next experiment.
7. Recommended reading path and research opportunity grounded in an unresolved mechanism or evidence gap.

## GitHub Awesome / Resource Repository Search

For literature surveys and research-map work, always consider whether the field has useful curated GitHub repositories such as `awesome-<topic>`, `awesome <topic>`, survey/code-list repositories, benchmark leaderboards, dataset lists, or lab-maintained resource pages. These repositories are discovery and organization sources, not replacements for official papers.

Search and screen repositories actively:

- Search GitHub and the web with queries such as `awesome <topic>`, `awesome <method family>`, `<topic> papers github`, `<topic> benchmark github`, `<topic> survey github`, and method-specific variants. Prefer repositories with high stars for the niche, recent meaningful commits or README updates, visible issue/PR activity, and maintainers who are labs, authors, benchmark organizers, or credible community curators.
- Do not only list a repository from search results. Open the repository and inspect the README, paper list, dataset/benchmark sections, code links, update history, and linked project pages. If GitHub search results are noisy, use the repository's own README and commit/release/activity pages as the source for what it actually covers.
- Treat star count as a triage signal, not proof of correctness. A lower-star repository may still be important if it is maintained by the dataset/benchmark authors or a core lab. Conversely, a high-star repository that has not been meaningfully updated for years should be labeled stale and should not dominate the survey.
- Extract concrete additions from the repository: missing papers, benchmark names, datasets, official code/project links, canonical method groupings, field terminology, and reading order clues. For any paper card or technical claim, follow up with the official paper/PDF/project/code source before writing reader-facing claims.
- In survey pages, include a compact `GitHub / Awesome 资源` section, table, or database view when relevant. Suggested fields: `Repository`, `Stars`, `Last meaningful update`, `Maintainer / credibility`, `Coverage`, `Useful additions`, and `Caveat`. Keep it separate from paper cards so readers can distinguish curated navigation sources from verified paper evidence.
- If no strong Awesome/resource repository exists after searching, say so briefly in the survey notes and continue with primary literature search. Do not fabricate an Awesome repository or pad the page with weak, stale, or unrelated lists.

On every platform, the parent/MOC page must be the main literature-review entry and expose the three tree artifacts directly: `General Goal Literature Tree`, `Challenge-Insight Tree`, and `Research Entry Points Tree`. Link to one collection-style `Paper Cards` artifact and one `Full Survey Report` only when needed. Do not make the main entry a thin hub that only links to a separate `Tree Maps` page. Paper Cards remain one collection containing many cards, not one page per paper.

Platform mapping:

- Feishu/Lark: use three native editable mind maps on the parent page through `feishu-doc-workflow` and `lark-whiteboard`.
- Notion: use a structured parent page with toggle/heading trees, linked database views, relations, or an embedded editable artifact supported by the workspace, via `notion-doc-workflow`. Keep the three tree semantics visible on the parent page.
- Obsidian: use Mermaid or Canvas when editable and supported, plus a linked Markdown outline/MOC so the tree remains searchable and diffable, via `obsidian-doc-workflow`. Store paper cards as a collection note unless the user explicitly requests atomic per-paper notes.

When repairing an older survey that already has a separate `Tree Maps` child artifact, expose the Tree Maps content from the main entry first and keep the old child only as a non-primary legacy copy unless the user explicitly asks to delete it. Do not duplicate a native editable tree with an equivalent outline by default; add a compact textual fallback only when the native representation is not searchable/editable enough or the user requests it.

When bilingual mind maps are required, each node must use the visual form `English` newline `Chinese`; do not deliver all-English maps or one-line `English / 中文` substitutes. On Feishu, repair literal `\n` imports in native whiteboard JSON and verify a preview. On Notion or Obsidian, use the platform's supported multiline label or a paired bilingual outline when multiline nodes are unavailable.

The `Research Entry Points Tree` is mandatory for literature-review / research-map deliverables unless the user explicitly excludes it. It should be comprehensive and decision-useful, not a shallow list of topic names. For each major direction, include bilingual nodes for problem framing, why-now / literature gap, core hypothesis, candidate route or pipeline, required data / benchmark, evaluation signal, compute / cost when relevant, expected contribution / novelty type, risks / boundaries, and the next concrete experiment. Do not duplicate it in equivalent forms unless the target platform needs a searchable fallback.

For any formal paper card in a research-map or survey deliverable, use [`paper-card-delivery`](../paper-card-delivery/SKILL.md) as the only content standard. This skill may decide grouping, taxonomy, reading order, and survey structure, but it must not redefine paper-card source verification, metadata, figure/caption choice, fixed bullet slots, sorting, or validation.
