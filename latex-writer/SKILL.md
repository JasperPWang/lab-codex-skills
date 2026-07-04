---
name: latex-writer
description: "Handle academic LaTeX writing and template engineering: conference/journal templates, BibTeX/BibLaTeX, figures/tables, cross-references, latexmk compilation, overfull boxes, page limits, anonymous submission, Markdown/Word-to-LaTeX conversion, and compile-safe cleanup. Use when the user asks for LaTeX Writer or academic LaTeX help."
---

# LaTeX Writer

Use this for manuscript engineering, not for deciding the scientific contribution.

Workflow:
1. Inspect the project tree, template, build command, bibliography, figures, and current compile log.
2. Make small compile-safe edits. Preserve labels, citations, macros, and package conventions.
3. Run `latexmk` or the repo's documented build command when available.
4. Fix errors before warnings; then handle overfull boxes, float placement, references, page limits, and anonymization.
5. For PaperSpine manuscripts, coordinate with `paper-spine-latex`.

Do not rewrite large LaTeX files without checking diffs and compiling.
