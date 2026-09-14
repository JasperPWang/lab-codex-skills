---
name: intern-interview-intake
description: Use when collecting, OCRing, summarizing, routing, and cleaning up internship interview screenshots or research-intake screenshots from Photos albums such as Intern, Research Intake, or research intern related albums in WorldModelVault.
---

# Internship And Research Screenshot Intake

Use this workflow when the user adds interview-experience, internship, recruiting, research-intern, or research-intake screenshots to Photos albums and asks to summarize them into notes.

## Destination Routing

- `Intern` album, 面经, JD, offer, recruiting, company interview question, and internship/research-intern application screenshots go to: `$WORLD_MODEL_VAULT/3-Projects/Intern/世界模型实习招聘与面试资料.md`
- `Research Intake` album screenshots that are paper leads, project links, research methods, workshop notes, study/research screenshots, or general research intake go under: `$WORLD_MODEL_VAULT/0-Daily/Screenshots/`
- The default rolling summary for Research Intake is: `$WORLD_MODEL_VAULT/0-Daily/Screenshots/Research Intake 截图整理.md`
- If a screenshot clearly belongs to another existing note, update that note instead and mention the path.
- If a screenshot contains both interview/recruiting content and research intake, split the summary into the appropriate destinations.

## Photo Albums

Check these Photos albums by default:

- `Intern`
- `Research Intake`
- Any album or screenshot group the user names, including "research intern" related screenshots.

## Required Workflow

1. Count and inspect candidate screenshots before editing or deleting anything.
2. Export only the relevant album media to a temporary folder under `/tmp`.
3. OCR the images. Use `tesseract` with `chi_sim+eng` when available; use Photos text recognition or visual inspection to correct important OCR errors.
4. Classify each screenshot before writing: interview/recruiting vs research intake vs mixed.
5. Compare extracted content against the routed destination note.
6. If content is already summarized, do not duplicate it.
7. If content is new, summarize it into the routed note with source context. For interview content, include role/company, question groups, and concrete interview questions. For Research Intake content, include title, links, core idea, why it matters, and follow-up routing suggestions when useful.
8. After the summary has been written and verified, delete the processed screenshots from the Photos library. This cleanup rule applies to `Intern`, `Research Intake`, and research-intern screenshots unless the user explicitly asks to keep them.
9. Verify the album count after deletion.
10. Remove temporary exported images and OCR text from `/tmp`.

## Deletion Safety

- Delete only screenshots that were processed in this workflow.
- Prefer deleting from the single-photo or selected-photo view in Photos so the image goes to Recently Deleted.
- Do not enter locked `Recently Deleted` unless the user unlocks it and explicitly asks for permanent deletion.
- If unsure whether an image was processed, keep it and ask.
