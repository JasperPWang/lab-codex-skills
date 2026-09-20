# Computer Vision Qualitative Results

Use for baseline comparisons, video/world-model rollouts, depth, segmentation,
attention, reconstruction and point-cloud panels. These rules extend the
figure contract and apply regardless of plotting backend. Source outputs may
come from model-specific renderers; never regenerate experimental evidence
with an image-generation model.

## Comparison Contract

- Record the task, datasets/splits, method names, checkpoints, and sampling
  protocol before selecting examples. Distinguish illustrative examples from
  representative evaluation; include failure cases when making robustness claims.
- Match methods by stable sample ID, view, timestamp, conditioning and output
  resolution. Do not pair files solely by directory order. Show missing output
  explicitly rather than substituting another sample or silently dropping it.
- Record random seeds for stochastic outputs. A best-of-N illustration must
  disclose N and the selection metric; apply the same selection budget to all
  methods when claiming a fair comparison.
- Freeze panel order, method colors, sample selection and rendering parameters
  so later checkpoint updates regenerate comparable figures.

## Images and Crops

Use identical source-coordinate crop rectangles across aligned methods and GT.
Mark zoom regions on the full image and record transforms between resolutions.
Do not stretch images to fill cells. Use nearest-neighbor interpolation for
categorical masks; record interpolation for continuous images and maps.
Avoid per-method contrast or sharpening that changes apparent quality.
Separate GT, input, prediction, missing data and overlays in the labels.

## Depth, Errors, Masks and Attention

- Use a shared color map and physical range for directly compared depth/error
  panels, with units and a colorbar. Record clipping and invalid-pixel policy.
  If scale/shift alignment is part of the evaluation, name and record it.
- If per-image normalization is necessary, label it explicitly and avoid
  interpreting color differences across panels as absolute differences.
- Fix semantic-class colors across samples and methods; identify ignore labels.
  Apply the same overlay opacity. Compute error maps from aligned arrays, not
  screenshots. State the error definition and evaluation mask.
- For attention/saliency, record layer, head aggregation, query/token, spatial
  mapping and normalization. Do not label attention as causal evidence by itself.

## Video and World Models

Align by timestamps or documented frame indices, not merely panel positions.
Mark the conditioning/observation boundary and prediction horizon. Specify
frame stride, FPS and playback speed; distinguish open-loop rollout from
teacher forcing and show shared actions/conditioning when applicable.
Keep sequences from the same run together. Do not splice best frames from
different seeds into a purported single rollout. Use consistent temporal
sampling across methods and disclose dropped or unavailable frames.

## 3D Reconstruction and Point Clouds

Share camera intrinsics/extrinsics, world coordinate convention, scene scale,
viewport, projection, lighting and geometry display settings where comparable.
Persist the camera/render configuration, including point size and thresholds.
Disclose evaluation alignment (for example rigid or similarity alignment),
cropping, filtering and downsampling. Do not optimize the viewpoint separately
for each method to conceal errors. Use additional views when occlusion matters.

## Per-Panel Provenance

Write a machine-readable JSON/CSV manifest alongside the plotting script.
Each panel needs: panel ID, method, checkpoint/revision, dataset/split, sample
ID, source path and SHA256, frame/timestamp where applicable, crop/resize,
normalization/color range, and renderer/config. Record seeds and camera data
when relevant. Use project-relative paths in shareable packages; never include
credentials or private server connection details.

Store actual source outputs or documented retrieval instructions separately
from derived figures. Keep missing provenance explicit; do not invent hashes,
checkpoints or settings. A script and fixed manifest should recreate the panel
selection and transformations without an agent choosing new examples.

## Delivery Checks

Verify sample/frame alignment and shared scales against source arrays. Inspect
the full figure at target column width plus zoomed crops, checking labels,
missing panels, interpolation and colorbars. Validate that quantitative labels
come from the same evaluation protocol and samples they claim to summarize.
Deliver editable plotting code, manifest, requested PDF/PNG and concise notes
on selection, transforms and any remaining limitations. Exact reproducibility
claims require a rerun with recorded dependencies and deterministic settings.
