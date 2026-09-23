---
name: sivia
description: Design source-grounded computer-vision paper overviews and method illustrations using Sivia's paired visual case library; reconstruct approved designs as editable PPTX or draw.io and make scoped revisions. Use for paper-to-figure, visual reference selection, and editable figure reconstruction.
---

# Sivia Integration

This entrypoint packages Sivia with its original relative directory structure.
Read [the upstream workflow](upstream/docs/workflow.md), then load only the
relevant module below. Relative paths inside upstream files resolve against
those files. References to `$design-scientific-figure` and other Sivia skills
mean the corresponding bundled module, not a separately installed skill.

## Routing

- New paper overview or method illustration: [design](upstream/skills/design-scientific-figure/SKILL.md).
- Existing figure reconstruction: [recreate](upstream/skills/recreate-scientific-figure/SKILL.md).
- Editable PPTX: [PowerPoint](upstream/skills/edit-powerpoint-live/SKILL.md).
- Editable draw.io: [draw.io](upstream/skills/recreate-scientific-figure-in-drawio/SKILL.md).
- Visual review: [audit](upstream/skills/audit-scientific-figure/SKILL.md).
- Scoped corrections: [correct](upstream/skills/correct-scientific-figure/SKILL.md).
- Reference selection: [case library](upstream/knowledge-base/README.md).

Select references by scientific relationships and communication purpose.
For visual geometry or dynamic scenes, inspect relevant VGGT, Neuralangelo,
or MegaSaM cases and their paired prompts. Reference diagrams supply style,
not evidence or the current method's topology.

## Local Runtime Adaptation

For teaser and pipeline-overview styling, consult the user-approved
[Any4D visual reference](references/any4d/style-reference.md) and inspect its
two local original figures. Use it when its result-led teaser or layered,
pastel architecture matches the communication task. This is a preferred
visual example, not a universal topology or palette requirement. The case
is maintained outside the upstream snapshot.

This is a vendored skill installation, not activation of Sivia's plugin MCP
servers. Discover available tools before choosing a construction route.
Never assume `powerpoint_*` or `drawio_live_*` tools are registered.
Use the available image-generation tool for raster design; for standalone
PPTX use the installed presentations skill and its actual-file renderer;
for draw.io use the installed drawio-diagram-builder. Load the upstream
module for design and review requirements, adapting unavailable tool names
to those real backends. Live PowerPoint editing is a separate capability;
do not represent standalone file construction as live editing.

Follow the user's requested deliverable and existing authorization. Image-only
requests end with the image; an explicit editable-delivery request already
authorizes reconstruction. Do not insert repeated approval gates solely
because an upstream default expects separate turns.

Keep empirical images and values from real outputs. Generated illustrations
must not replace measured depth, segmentation, video predictions, attention,
or reconstruction results. For those panels load
[CV qualitative guidance](../nature-figure/references/cv-qualitative.md).
Use nature-figure for numerical plots and CV result plates rather than
the image-generation route.

During revisions, preserve approved regions and stable object IDs. Change
only requested objects and dependent connectors, then render the saved file
and check both modified and preserved regions. Keep labels/arrows editable;
declare which complex assets remain raster.

## Provenance

Upstream: https://github.com/exsinger-hub/Sivia

Pinned commit: `5406fe151fa3052e9fe9856ea923a66f56fdb593` (version 1.1.3).
The original MIT license is in [upstream/LICENSE](upstream/LICENSE).
The upstream snapshot is unmodified. Update it separately from this adapter,
and verify references and runtime compatibility before publishing updates.
