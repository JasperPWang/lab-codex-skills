# PDF2ZH Terminology Workflow

Use this reference before generating a Chinese paper PDF and when checking terminology in an existing translated PDF. Four steps are required: collect candidate terms, review the glossary, translate using the selected engine's actual capabilities, then audit and correct the output PDF. Automatic extraction is optional; terminology review and output verification are not.

## Collect and review terms

1. Start from the verified English HTML/LaTeX/PDF and any existing project glossary or translation. Collect important task, representation, geometry, rendering, optimization, loss, module, and evaluation terms, along with official method/model/dataset names. Include ambiguous terms and previously observed mistranslations. Reuse available source text instead of launching another full translation merely to build a candidate list.
2. Automatic extraction is an additional candidate source when a configured LLM service is suitable. Record the resolved extraction engine and whether `no_auto_extract_glossary` is false; request `--save-auto-extracted-glossary` and verify that a nonempty CSV was actually written. The flag alone proves neither that extraction ran nor that the saved terms are correct. The ordinary PDF2zh run may also translate the paper; do not describe it as an extraction-only command or assume that it pauses for review. If no suitable extractor exists, collect candidates from the official source in the current session.
3. Review each candidate against its sentence and technical meaning in the original paper. Choose accurate, consistent translations for generic concepts and preserve official names, abbreviation spellings, and mathematical symbols. Resolve ambiguous translations with the source and established domain usage. This is a source-faithful PDF translation check, separate from conventions for authoring a new Chinese academic manuscript: do not insert new acronym definitions or change typography merely to conform to a writing template. Record unresolved choices rather than declaring them reviewed. If the review was performed by the agent, do not claim human approval; request user input only for a material unresolved preference or ambiguity, or when the user explicitly requests approval of the glossary.
4. Save `glossary.reviewed.csv` under the task's translation directory, using UTF-8 and a CSV writer. For the verified installation, headers are `source,target` with optional `tgt_lng`; when present, `tgt_lng` must match `--lang-out` (for example `zh-CN`). Keep provenance, context, review status, and decisions in the task's terminology audit. Resolve duplicate/conflicting source entries before import rather than relying on file order or silent deduplication.

Example reviewed entries; apply only where appropriate for the paper:

```csv
source,target,tgt_lng
NeRF,NeRF,zh-CN
SMPL-X,SMPL-X,zh-CN
Gaussian Splatting,高斯泼溅,zh-CN
```

Use stable term translations in the CSV. Preserve the source's definitions and abbreviation introductions where present; do not add a three-part first-use definition absent from the original or map every acronym occurrence to an expanded explanation. Do not apply terminology normalization to original English figure interiors, table cells, source quotes, formulas, or code.

## Translate with the reviewed glossary

Resolve the actual executable and service before choosing parameters. CLI acceptance, extraction, glossary consumption, and output quality are separate checks.

| Path | Required handling |
|---|---|
| Main engine supports glossary use | Load the reviewed CSV through `--glossaries`; confirm the resolved engine accepts it and the run loaded the intended entries. |
| Automatic extraction is available | Use its output as candidates, review them, then perform a final run with the reviewed CSV. Disable new automatic extraction in that final run so unchecked candidate choices do not replace the reviewed glossary. |
| Bing/non-LLM path in the verified installation | Use the reviewed glossary as an external audit checklist. Do not pass `--glossaries` to Bing. Keep the PDF classified as a draft until its actual terminology has been checked and any errors corrected. |

For a glossary-capable LLM already configured for the task, add `--glossaries "$REVIEWED_GLOSSARY" --no-auto-extract-glossary` to the established translation command, keeping its figure/table protection and output settings. The disable flag freezes automatic candidate extraction, not the supplied CSV. Do not invent credentials, change the service silently, or assume that a custom prompt provides deterministic glossary enforcement. A separate LLM extraction engine does not make a Bing main translator glossary-capable.

If a Bing draft contains incorrect terminology, regenerate with a suitable configured glossary-capable engine when within the task's scope, or use an established layout-preserving PDF repair path. If neither is available, report the PDF's unresolved issues and continue only work that does not depend on calling that PDF verified. A correction made only in Notion/Markdown does not correct the PDF.

## Audit and correct the output PDF

1. Read the actual Chinese PDF's text and compare key-term occurrences and known wrong variants across the whole document with the reviewed glossary. Check the abstract, introduction, method, losses, experiments, captions, and included appendix/supplement prose. Confirm that terms are used in the correct sense, names and abbreviations are intact, source definitions are translated faithfully, and repeated renderings agree. Extracted text can locate candidates but is not a complete visual check, particularly for scanned or outlined text.
2. Inspect representative rendered pages and every page with a terminology correction. Check text overflow, line breaks, fonts, formulas, captions, and the original English figure labels and table cells. Preserve source spelling in protected regions even if it differs from a Chinese prose entry. Follow the `pdf` skill for rendering and layout verification.
3. Correct confirmed issues by regenerating from the reviewed settings/glossary or by a verified local PDF repair. If a reviewed glossary changes, recheck the affected terms throughout the output. When a rerun may reuse earlier translations, verify glossary-sensitive cache behavior; use `--ignore-cache` when needed to prevent stale wording. Never perform blind replacement in PDF bytes or a whole-document layout rebuild to change a term.
4. Audit the corrected output again, including unchanged protected regions on affected pages. Keep a concise `terminology-audit.md` with the source identity, executable/host and versions, main/extraction engines, reviewed glossary version/hash and reviewer, final PDF filename/hash, sections/pages checked, issues and repairs, unresolved items, and completion status. Record `no issues found in the stated checks` when appropriate; do not imply an automatic guarantee of translation accuracy.

Newly generated PDFs pass this step only when the planned checks are complete and no known terminology defects remain, unless the user explicitly accepts a documented draft/exception. Reuse the same glossary for the later manuscript repair, then verify that manuscript separately. Do not rerun PDF generation merely to repair an already imported page when the task only concerns that page.

## Verified Version Boundaries

Checked on **4090-single on 2026-11-07**, with `pdf2zh-next 2.9.0` and `BabelDOC 0.6.2`:

- The parser accepts `--glossaries`, `--save-auto-extracted-glossary`, and `--no-auto-extract-glossary`. This does not prove all engines support them.
- Without a separate LLM term-extraction service, selecting Bing causes configuration validation to disable automatic extraction.
- Creating the Bing translator with `glossaries` set raises `Bing does not support glossary`. The rejection occurs before a translation request. A separate term service does not bypass that main-engine check.
- `Glossary.from_csv` accepts `source,target,tgt_lng` and filters by the selected output language. Candidate export depends on actual extracted terms and the backend export path; require the file as evidence.

These checks verified parsing/configuration and CSV loading without translating a PDF. They do not establish end-to-end glossary adherence, extraction quality, or output layout quality. Recheck the execution host after upgrades; do not describe this server installation as a verified Mac installation.

Official references: [parameter and glossary documentation](https://github.com/PDFMathTranslate/PDFMathTranslate-next/blob/main/docs/en/advanced/advanced.md), [engine/extraction configuration](https://github.com/PDFMathTranslate/PDFMathTranslate-next/blob/main/pdf2zh_next/config/model.py), and [translator glossary support checks](https://github.com/PDFMathTranslate/PDFMathTranslate-next/blob/main/pdf2zh_next/translator/utils.py). Installed source and observed behavior govern the version-specific statements above.
