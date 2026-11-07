---
name: chinese-technical-writing
description: Chinese-first writing standard for academic manuscripts, research notes, paper cards, deep dives, and technical documents. Use when writing, translating, or reviewing Chinese research prose, especially first-use terminology definitions, abbreviations, and Chinese-English typography. Preserve official names, formulas, identifiers, and original source text.
---

# Chinese Technical Writing

## Core Contract

Reader-facing Chinese research documents must use Chinese as the default technical language. English is a precision tool for names, acronyms, symbols, searchability, and source fidelity; it is not a substitute for writing clear Chinese prose.

Use this skill for Chinese academic manuscripts, Feishu/Lark pages, Notion pages/databases, Obsidian/LLM Wiki notes, paper cards, daily reviews, meeting notes, paper deep dives, source translations, summaries, figure captions, tables, and TODO/review documents. Use [`research-doc-workflow`](../research-doc-workflow/SKILL.md) when the prose will be written into a durable research document.

## Allowed English

Keep English when it is genuinely a name, identifier, or source-fidelity object:

- paper titles, method/model/system names, dataset/benchmark names, code/repo names, organization names, and product names;
- named architectures, model families, pretrained models, and named components such as Transformer, DINO, CLIP, NeRF, LoRA, SAM, and Gaussian Splatting; keep the official English name even when a Chinese translation exists;
- standard abbreviations and model identifiers such as SMPL-X, 3DGS, CLIP, PSNR, LPIPS, FID, FPS, GPU, and API;
- mathematical notation such as $L_2$ and $\mathcal{L}$, governed by the manuscript's notation conventions;
- code identifiers, file paths, commands, config keys, CLI flags, class/function names, and quoted error messages;
- exact original English text in `英文原文稿`, bilingual source archives, citations, block quotes, paper abstracts copied as source text, and other source-preserving sections;
- References / bibliography entries in paper translations and deep dives: keep the original English authors, titles, venues, publisher names, page ranges, DOI/arXiv strings, and other reference fields instead of translating them into Chinese;
- required bilingual mind-map nodes or headings when another workflow explicitly requires English plus Chinese.

## Chinese-First Rule

For ordinary Chinese prose, translate generic technical concepts into Chinese. Do not translate official names of architectures, models, methods, datasets, benchmarks, systems, or components. If a retained English name needs explanation, add a short Chinese gloss on first use, for example `Transformer（基于自注意力的网络架构）`; do not mechanically turn the name into a Chinese phrase. If an English term is generic rather than a name and helps search or disambiguation, write it only on first use as:

```text
中文术语（English term）
```

After the first occurrence, use the Chinese term or a stable acronym. Do not leave raw English noun phrases inside Chinese sentences when they have clear Chinese equivalents.

Good:

- `参数化人体估计（parametric human estimation）需要同时约束人体形状、姿态和相机位姿。`
- `透视畸变会让近处身体部位被放大，从而影响人体姿态估计。`
- `场景几何决定了可行接触、遮挡关系和运动边界。`
- `采用 Transformer 架构与 DINO 预训练模型。`

Avoid:

- `parametric human estimation 需要处理 pose 和 camera。`
- `这个方法主要解决 perspective distortion。`
- `模型没有显式利用 scene geometry。`

## Chinese Academic Manuscripts

The rules below govern authoring or editing original Chinese academic prose. For source-faithful translations such as PDF2zh output, preserve the original paper's terminology definitions, abbreviation introductions, and layout; use the translation workflow for accuracy and consistency checks rather than imposing a new manuscript-writing template.

### First-use definitions

- For an important technical term with an established abbreviation, introduce it as `中文术语（英文全称，英文缩写）` before using the abbreviation by itself. After that, use the same abbreviation consistently without repeatedly expanding it. Apply the same principle separately to the abstract and main text when they are read independently, following any venue-specific exceptions.
- If a term has no established abbreviation or does not need a shorthand, use `中文术语（英文术语）` when the English term helps. If there is no reliable Chinese term, retain the English name and give a short Chinese explanation when needed. Do not invent a translation or abbreviation.
- Verify the full form and spelling against the original paper, official project, or established field usage. Preserve case, hyphens, and digits: `3DGS`, `NeRF`, `SMPL-X`, not `3dgs`, `Nerf`, or `SMPLX`. Keep model variants distinct; the expansion of `SMPL` does not identify `SMPL-X`.

| First use | Later use |
|---|---|
| 三维高斯泼溅（3D Gaussian Splatting，3DGS） | 3DGS |
| 神经辐射场（Neural Radiance Fields，NeRF） | NeRF |
| 参数化人体模型（Skinned Multi-Person Linear Model，SMPL） | SMPL |
| 物理基础渲染（Physically Based Rendering，PBR） | PBR |
| 双向反射分布函数（Bidirectional Reflectance Distribution Function，BRDF） | BRDF |
| 卷积神经网络（Convolutional Neural Network，CNN） | CNN |

### Names, notation, and mixed typography

- Use text type for abbreviations such as `CNN`, `PBR`, and `BRDF`, and retain official names such as `Transformer` and `SMPL-X`. Explain a name in Chinese when needed, e.g. `SMPL-X（涵盖人体、手部和面部的参数化人体模型）`. Do not force a three-part expansion onto a name such as `Transformer`.
- Use math mode and the manuscript's notation conventions for variables and symbols, e.g. $x$, $\theta$, and $\mathcal{L}$. Define each symbol's meaning where introduced. An abbreviation in prose is not a mathematical variable; do not put `3DGS` or `CNN` in math mode to style it.
- Follow the target journal, conference, or thesis template for typography. As the house default when it is silent, use one half-width space between adjacent Chinese prose and a Latin word or abbreviation, e.g. `采用 CNN 提取特征` and `基于 SMPL-X 的人体建模`. Use Chinese full-width punctuation in Chinese sentences and in the first-use form above, without adding spaces next to that punctuation. Preserve internal English word spaces, official spellings, and punctuation in equations, identifiers, quotations, and source material.

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

- Paper cards: also use `paper-card-delivery`; the card's metadata takeaway, caption, and seven fixed bullets must be Chinese-first.
- Paper deep dives: enforce Chinese-first wording in the body of `原文中译稿`. A `精读稿` or `英文原文稿` is written only when the user explicitly requests it; apply the same Chinese-first rule to a requested `精读稿`, and preserve official English source text in a requested `英文原文稿`. Keep References / bibliography entries in the original English rather than translating them, except that a cited paper title in a Chinese manuscript may be translated when `paper-deep-dive` allows it.
- Bilingual source archives: do not modify the English original blocks; enforce this rule only on Chinese translation blocks or Chinese notes.
- Feishu rich pages: normalize wording with narrow text edits; do not rewrite or damage images, grids, tables, formulas, or whiteboards just to fix language.
- Notion pages/databases: preserve native blocks, properties, relations, equations, captions, and page links while editing prose.
- LLM Wiki / Obsidian notes: use Chinese body text, `中文（English term）` on first use, LaTeX for formulas, and English only for names/identifiers.
- Diagrams and tables: Chinese labels by default; keep method names, dataset names, symbols, and required bilingual node formats unchanged.

## Audit Checklist

Before delivering a Chinese document, check:

- Chinese prose does not contain avoidable English phrase islands.
- First-use English parentheses are used only when useful, not after every term.
- In academic manuscripts, important abbreviations are defined at first use; later spelling is consistent, and names, abbreviations, and mathematical notation follow their respective typography.
- Method/model/dataset/code names, acronyms, formulas, and source quotes are preserved.
- Repeated generic English words such as `baseline`, `ablation`, `metric`, `benchmark`, `pipeline`, and `framework` have been replaced with clear Chinese unless they are official names. Named architectures and models such as `Transformer` and `DINO` remain in English.
- Captions, bullets, summaries, TODOs, and interpretation sections read naturally in Chinese.

## Validation Script

For local Markdown or text drafts, run:

```bash
python .tools/skills/chinese-technical-writing/scripts/validate_chinese_terms.py path/to/draft.md
```

The script checks Chinese-containing lines for known translatable English phrases. It is a lint helper, not a complete language judge. If no local draft exists, do the audit manually before writing to Feishu or answering the user.
