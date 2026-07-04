---
name: paper-rag
description: Build or use a local paper RAG / paper knowledge base for PDF, arXiv, LaTeX source, MinerU Markdown, paper notes, and citation-grounded question answering. Use when the user asks for Paper RAG, local paper library search, paper QA, formula lookup, implementation checks against a paper, or multi-paper evidence retrieval.
---

# Paper RAG

Use this skill for retrieval-grounded paper work, not freeform literature synthesis.

Workflow:
1. Identify the source corpus: PDFs, arXiv IDs, MinerU Markdown, LaTeX source, Obsidian notes, Feishu pages, or Zotero entries.
2. Prefer structured paper artifacts already in the vault: paper cards, deep-dive notes, English manuscript, Chinese translation, and assets.
3. Extract metadata: title, authors, venue, year, PDF/arXiv, code/project links, sections, equations, figures, datasets, and metrics.
4. Answer with source-grounded citations or local file references. Separate `source says`, `inference`, and `citation needed`.
5. For implementation checks, quote or paraphrase the exact relevant method/equation/ablation first, then compare code/config.

Do not treat vector search output as a finished literature review. For survey structure, hand off to `survey-builder` or `academic-research-skills`.

