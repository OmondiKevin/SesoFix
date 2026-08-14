# SesoFix takeover decision log

**Date:** 2026-08-14
**Scope:** repository, legacy manuscript/notebook, local data inventory, workbook,
rules, metrics, tests, and claimed results

## Confirmed facts

- The old manuscript's 12,847-pair SesoCorp artifact is absent.
- No trained checkpoint or complete run log supports the old ByT5, mT5, LSTM,
  human-evaluation, significance, OOD, or downstream numbers.
- The Common Voice workbook has 2,337 South African Sesotho sources and 74
  single-annotator Lesotho Sesotho targets; 2,263 target cells are blank.
- Of the 74, 51 differ and 23 are exact copies under the current comparison.
  All 23 exact-copy targets are formula results; the 51 changed targets are
  direct cells. The template formulas remain present on most blank target rows.
- The workbook's `SIMILARITY` field was derived using strict exact match after the
  collaborator produced targets. It is not a human similarity score.
- The current rule engine contains 30 candidate rules created during exploratory
  cleanup. No legacy implementation of the claimed 47 rules was found.
- All 74 targets were available during rule development, so the stored baseline
  comparison is development-only.
- Existing engineering tests passed in the takeover audit. This verifies
  deterministic code paths, not linguistic correctness.
- The prior metrics code used Hugging Face BLEU, default chrF rather than chrF++,
  and macro sentence WER rather than corpus WER.
- The proposed `opus-mt-nso-en` downstream model targets Northern Sotho/Sepedi,
  not Southern Sotho, so the old downstream design is invalid.

## Decisions

1. Preserve all legacy manuscript/notebook material under `paper/legacy/` and
   `notebooks/legacy/`; do not repair its numbers into a submission.
2. Frame the task as cross-standard adaptation, not correction of an inferior
   variety.
3. Refresh Common Voice using an untouched current Sesotho (`st`) Scripted Speech
   archive and perform a hash-based, lossless merge.
4. Preserve the 74 targets as immutable development evidence and add independent
   review; never promote them to the final test.
5. Create new natural and challenge test sets, freeze their IDs/hashes before
   system development, and double-review/adjudicate them.
6. Compare zero-shot, few-shot, translation-pivot, rules, retrieval, ByT5, and
   mT5 across a supervision curve.
7. Use Amazon MASSIVE for the optional stronger downstream semantic-parsing
   study, with human Sesotho test utterances and slot/frame preservation.
8. Never train locally. Prepare data and notebooks locally; execute training only
   in Google Colab.

## Current state

The untouched Common Voice 26.0 archive has been received, hashed, profiled, and
merged losslessly. All 2,337 legacy source rows matched by exact sentence ID and
text; all 74 existing human targets were preserved. A deterministic 200-sentence
development pilot and separate blinded primary/reviewer workbooks are ready.

The project is not blocked by code or data preparation. The next dependency is
human annotation: the primary collaborator completes the primary workbook, and
an independent Lesotho Sesotho reviewer completes the reviewer workbook without
seeing the primary annotations.

## Authoritative documents

- `docs/RESEARCH_PROTOCOL.md`
- `docs/COMMON_VOICE_REFRESH.md`
- `docs/ANNOTATION_PROTOCOL.md`
- `docs/DATA_PROVENANCE.md`
- `docs/REPRODUCIBILITY_STATUS.md`

`docs/REPRODUCIBILITY_STATUS.md` is the retained forensic summary. Where an early
legacy claim conflicts with the takeover corrections above, this decision log
and the active research protocol take precedence.
