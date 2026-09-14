# Notion Page Icon System

Use this system for research repositories, paper libraries, meeting archives, and related Notion pages. The goal is stable visual semantics: the same page role gets the same icon wherever practical.

## Decision Order

Choose exactly one emoji icon using this precedence:

1. Preserve an existing icon unless the user explicitly requests normalization.
2. Match an explicit artifact type from the page title, such as `精读稿`, `英文原文稿`, `.pdf`, `Dataset`, or `Meeting`.
3. Match the page's structural role, such as roadmap, paper collection, experiment, or category hub.
4. For a topic hub, use the domain icon. Do not propagate a hub icon to every paper beneath it.
5. If no stronger rule applies, use `📄` for a content page and `📚` for a collection/index page.

Parent context may resolve ambiguity, but a clear title suffix has priority. For example, `SAM 3D｜精读稿` is `🔎`, not `🧊`.

## Canonical Artifact Icons

| Page role or title signal | Icon |
|---|---|
| Single paper, article, ordinary research note, unspecified content page | 📄 |
| Paper collection, `Papers`, `Baseline Papers`, `Mentioned Papers` | 📚 |
| Paper cards / `Paper Cards` | 🗂️ |
| Survey or literature review | 🔭 |
| Deep dive or `精读稿` / `中文精读稿` | 🔎 |
| English source / `英文原文稿` / `完整英文稿` | 🌐 |
| PDF, DOCX, or attachment-only page | 📎 |
| Dataset or benchmark collection | 🗃️ |
| Experiment, probe, scratch validation | 🧪 |
| Meeting archive or dated meeting page | 🗓️ |
| Roadmap | 🚩 |
| Idea | 💡 |
| Seed Papers | 🌱 |
| Evaluation metrics | 📏 |
| Image collection or `Image` | 🖼️ |
| Video collection or `Video` / `Streaming Video` | 🎬 |
| Simulator | 🎮 |

Use `🔭` for a survey/review page and `📚` for a plain list of papers. Use `🗃️` for dataset pages even when the dataset is associated with a paper.

## Canonical Research Topic Hub Icons

These icons apply to category or hub pages, not ordinary leaf papers:

| Topic hub | Icon |
|---|---|
| Human-object interaction / HOI | 🤝 |
| Human-scene interaction or human mesh recovery / HSI / HMR | 🧍 |
| Human-scene reconstruction / HS | 🏙️ |
| Contact modeling | 🫱 |
| 3D reconstruction | 🧊 |
| Depth, geometry, or 3DGS reconstruction | 📐 |
| 3D generation | 🪄 |
| Object and pose | 🎯 |
| Video generation or camera control | 🎥 |
| Editable 3D reconstruction | ✏️ |
| World model | 🌍 |
| Diffusion model | 🌫️ |
| Robotics learning | 🤖 |
| Physical AI | ⚙️ |
| Spatial intelligence | 🧭 |
| Affordance | 🖐️ |
| SDF | 🧮 |
| Agent | 🕹️ |
| LLM | 💬 |
| MLLM or multimodal agent integration | 🧠 |
| Vision-language model / VLM | 👁️ |
| Parameter-efficient finetuning | 🔧 |
| Music AI | 🎵 |
| Best-paper collection | 🏆 |
| Applications / demos | ✨ |

When a hub spans multiple topics, choose the icon for its primary organizing purpose rather than combining multiple emoji.

## Operational Rules

- Prefer native emoji icons. Do not introduce external icon URLs unless the user requests custom artwork.
- Set the icon as part of new-page creation rather than leaving a cleanup task for later.
- Keep sibling pages with the same role visually consistent.
- Do not infer a special icon from a paper's method name alone; leaf paper pages normally remain `📄` unless they are a deep dive, source manuscript, dataset, attachment, or another explicit artifact type.
- For ambiguous short titles, inspect the parent and immediate page content before choosing.
- For recursive icon cleanup, inventory the subtree first, save recovery snapshots, skip archived/in-trash pages, and never overwrite existing icons by default.
- After writing, re-fetch each changed page and verify the icon, title, parent, and untouched block structure.
