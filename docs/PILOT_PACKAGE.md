# SesoFix annotation pilot package

**Frozen:** 2026-08-14

**Role:** development-only protocol pilot

**Training performed:** no

## Purpose

This package tests whether the annotation question is well defined before the
final benchmark is sampled. It is not final test evidence and must not be used to
claim model performance.

## Frozen sample

- 200 unique Common Voice 26.0 South African Sesotho sentences;
- seed 42 and algorithm `pilot_v1_natural150_coverage50`;
- 150 natural random candidates;
- 15 short-sentence coverage candidates;
- 15 downvoted coverage candidates; and
- 20 non-government-source coverage candidates.

The four assignment strata are disjoint. Natural random sampling occurs before
coverage sampling, so the final package can contain more than the minimum number
of short, downvoted, or non-government sentences.

The public manifest at `data/manifests/pilot_v1_manifest.csv` contains stable IDs,
hashes, provenance, strata, and the two randomized row orders. It intentionally
does not contain Common Voice sentence text. The source text remains in ignored
private data and in the local workbooks. Its SHA-256 is
`52841c6976dbc2496a2fd69cebdc9de928319438c4ae9e0c4ac48651fb6efae6`;
a clean rerun from the untouched pending-sentence table produced the identical
file byte for byte.

## Local workbooks

| Role | File | SHA-256 |
|---|---|---|
| Primary collaborator | `outputs/sesofix_pilot_v1/SesoFix_Pilot_Primary.xlsx` | `4bc8bd4a45b3cd784d136546677c5559130cf260be3cec6503ef552ca3cd8ae0` |
| Independent reviewer | `outputs/sesofix_pilot_v1/SesoFix_Pilot_Reviewer.xlsx` | `b0ad5a541a76bd5e657071e3ace553eabcf136f4710cb7466034faa380271e57` |

The reviewer workbook uses a different random row order. Neither workbook
contains previous Lesotho targets, rules, model outputs, or the other person's
annotations.

## Online annotation copies

- [Primary annotation](https://docs.google.com/spreadsheets/d/1fmK-hxu5vMmd9aYb77MscDcRD1C_kWtn_Z3v1xZcFBQ/edit)
- [Independent review](https://docs.google.com/spreadsheets/d/1j-nfWo7zec04SjFR_s8616n8e3ERkrcIo14jH5vQW7I/edit)

Both files are native Google Sheets imported from the hashed local workbooks.
Their tabs, 200 rows, formulas, dropdowns, conditional formatting, role labels,
and visual layout were checked after conversion. Share only the relevant file
link with each annotator; do not share the project-root folder during the blind
pass. See `GOOGLE_DRIVE_WORKFLOW.md` for the current permission limitation.

## Workbook quality checks

Both workbooks were generated from the same frozen manifest and independently
checked for:

- exactly 200 unique pilot IDs and source sentence IDs;
- one `Instructions`, one `Annotation`, and one `Lists` sheet;
- protected-looking source columns and visually distinct editable columns;
- controlled dropdowns for categorical decisions;
- an automatic row-level QC status and live completion counts;
- no `#REF!`, `#DIV/0!`, `#VALUE!`, `#NAME?`, or `#N/A` formula errors;
- readable headers, wrapped source text, frozen identifier columns, and filters;
- separate annotator/reviewer labels and different row orders; and
- visual review of all six rendered sheets.

The `.xlsx` files are intentionally ignored by Git because they contain licensed
source text and future human annotations. Their hashes above bind the local files
to this frozen protocol state.

## Handoff and return

1. Give the primary workbook only to the original collaborator.
2. Give the reviewer workbook only to an independent Lesotho Sesotho reviewer.
3. Require independent completion; do not share either person's decisions.
4. Preserve the returned originals unchanged.
5. Import responses by `Pilot_ID`, retain both annotators, and adjudicate only
   after the blind pass is complete.

The next repository tasks are P2.1–P2.5 in `WORKPLAN.md`.
