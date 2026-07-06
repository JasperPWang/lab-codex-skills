---
name: chinese-technical-writing
description: Chinese-first technical/research writing standard for Feishu pages, Obsidian/LLM Wiki notes, paper cards, daily reviews, meeting notes, paper deep dives, source translations, and AI-generated Chinese documents. Use whenever Codex writes, revises, audits, or translates Chinese reader-facing research/technical prose and should avoid unnecessary English phrase mixing while preserving method names, acronyms, code names, formulas, datasets, and original source text.
---

# Chinese Technical Writing

## Core Contract

Reader-facing Chinese research documents must use Chinese as the default technical language. English is a precision tool for names, acronyms, symbols, searchability, and source fidelity; it is not a substitute for writing clear Chinese prose.

Use this skill for Chinese Feishu pages, Obsidian/LLM Wiki notes, paper cards, daily reviews, meeting notes, paper deep dives, source translations, summaries, figure captions, tables, and TODO/review documents.

## Allowed English

Keep English when it is genuinely a name, identifier, or source-fidelity object:

- paper titles, method/model/system names, dataset/benchmark names, code/repo names, organization names, and product names;
- standard acronyms and symbols such as SMPL-X, 3DGS, CLIP, PSNR, LPIPS, FID, FPS, GPU, API, $L_2$, and $\mathcal{L}$;
- code identifiers, file paths, commands, config keys, CLI flags, class/function names, and quoted error messages;
- exact original English text in `英文原文稿`, bilingual source archives, citations, block quotes, paper abstracts copied as source text, and other source-preserving sections;
- References / bibliography entries in paper translations and deep dives: keep the original English authors, titles, venues, publisher names, page ranges, DOI/arXiv strings, and other reference fields instead of translating them into Chinese;
- required bilingual mind-map nodes or headings when another workflow explicitly requires English plus Chinese.

## Chinese-First Rule

For ordinary Chinese prose, translate technical concepts into Chinese. If the English term helps search or disambiguation, write it only on first use as:

```text
中文术语（English term）
```

After the first occurrence, use the Chinese term or a stable acronym. Do not leave raw English noun phrases inside Chinese sentences when they have clear Chinese equivalents.

Good:

- `参数化人体估计（parametric human estimation）需要同时约束人体形状、姿态和相机位姿。`
- `透视畸变会让近处身体部位被放大，从而影响人体姿态估计。`
- `场景几何决定了可行接触、遮挡关系和运动边界。`

Avoid:

- `parametric human estimation 需要处理 pose 和 camera。`
- `这个方法主要解决 perspective distortion。`
- `模型没有显式利用 scene geometry。`

## Preferred Translations

Use Chinese for common translatable terms unless they are part of an official name:

| English | Preferred Chinese |
|---|---|
| parametric human estimation | 参数化人体估计 |
| perspective distortion | 透视畸变 / 透视失真 |
| scene geometry | 场景几何 |
| camera pose | 相机位姿 |
| body pose / human pose | 人体姿态 |
| mesh reconstruction | 网格重建 |
| 3D human reconstruction | 三维人体重建 |
| 3D human pose estimation | 三维人体姿态估计 |
| motion-dependent cloth dynamics | 运动相关布料动力学 |
| physically plausible deformation | 物理合理形变 |
| simulation-ready asset | 仿真就绪资产 |
| baseline | 基线 |
| ablation / ablation study | 消融实验 |
| metric | 指标 |
| benchmark | 基准 / 评测基准 |
| inference | 推理 |
| training | 训练 |
| evaluation | 评估 |
| supervision | 监督 / 监督信号 |
| representation | 表征 |
| pipeline | 流水线 / 流程 |
| framework | 框架 |
| feature | 特征 |
| optimization | 优化 |

If a term has no stable Chinese translation or the English form is the community standard, keep English but add a short Chinese explanation when first introduced.

## Document-Specific Handling

- Paper cards: also use `paper-card-delivery`; the card's metadata takeaway, caption, and six bullets must be Chinese-first.
- Paper deep dives: preserve official source text in `英文原文稿`; enforce Chinese-first wording in the body of `原文中译稿` and parent-page `精读稿`; keep References / bibliography entries in the original English rather than translating them.
- Bilingual source archives: do not modify the English original blocks; enforce this rule only on Chinese translation blocks or Chinese notes.
- Feishu rich pages: normalize wording with narrow text edits; do not rewrite or damage images, grids, tables, formulas, or whiteboards just to fix language.
- LLM Wiki / Obsidian notes: use Chinese body text, `中文（English term）` on first use, LaTeX for formulas, and English only for names/identifiers.
- Diagrams and tables: Chinese labels by default; keep method names, dataset names, symbols, and required bilingual node formats unchanged.

## Audit Checklist

Before delivering a Chinese document, check:

- Chinese prose does not contain avoidable English phrase islands.
- First-use English parentheses are used only when useful, not after every term.
- Method/model/dataset/code names, acronyms, formulas, and source quotes are preserved.
- Repeated generic English words such as `baseline`, `ablation`, `metric`, `benchmark`, `pipeline`, and `framework` have been replaced with clear Chinese unless they are official names.
- Captions, bullets, summaries, TODOs, and interpretation sections read naturally in Chinese.

## Validation Script

For local Markdown or text drafts, run:

```bash
python .tools/skills/chinese-technical-writing/scripts/validate_chinese_terms.py path/to/draft.md
```

The script checks Chinese-containing lines for known translatable English phrases. It is a lint helper, not a complete language judge. If no local draft exists, do the audit manually before writing to Feishu or answering the user.
