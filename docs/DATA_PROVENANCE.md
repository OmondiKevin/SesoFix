# SesoFix dataset provenance and evidence roles

**Last revised:** 2026-08-14

This document distinguishes provider facts, human annotations, and planned data
construction. A dataset being present does not make it an evaluation set, and a
human-produced target does not become independently verified without review.

## 1. Active sources

### DS01 — Autshumato English–Sesotho v2.0

- Provider: CTexT / SADiLaR.
- Content observed locally: 171,292 aligned English–South African Sesotho lines.
- License recorded with the local source: CC BY-NC-SA 4.0; re-check bundled terms
  before redistribution.
- Permitted research role: additional South African Sesotho text and possible
  translation diagnostics.
- Not evidence for: Lesotho Sesotho targets, cross-standard accuracy, or the
  previously claimed downstream improvement.

### DS02 — NCHLT Southern Sotho text corpus

- Provider: NCHLT / SADiLaR.
- Content observed locally: 148,390 non-empty lines across 2,816 text files.
- Recorded variety: South African Sesotho.
- License recorded with the local source: CC BY-NC-SA 4.0; re-check bundled terms
  before redistribution.
- Permitted research role: monolingual profiling and exploratory synthetic-data
  generation with explicit machine provenance.
- Not evidence for: human Lesotho Sesotho references.

### DS03 — legacy Common Voice verification workbook

- File: `Southern Sesotho Sentence Verification.xlsx`.
- Source sentences: an earlier Mozilla Common Voice Sesotho export, according to
  the researcher; exact release/export method is not yet recovered.
- Target creator: one collaborator who is a native/bidialectal speaker with
  experience of South African and Lesotho Sesotho.
- Sheet: `Validated CV Southern Sesotho S`.
- Observed rows: 2,337 source sentences.
- Observed targets: 74 non-empty target cells; 51 differ and 23 are exact copies
  under the current comparison view.
- Remaining source-only rows: 2,263.
- All 23 exact-copy target strings are displayed results of spreadsheet formulas;
  the 51 changed targets are direct target cells. The template also retains
  formula cells with blank cached results on most unannotated rows. The merge
  must preserve displayed target, formula presence, and shared-formula metadata.

Evidence interpretation:

- The 74 are **single-annotator human references**.
- `SIMILARITY` is a strict exact-match result derived after target creation, not
  a human similarity score.
- Independent review and adjudication have not yet occurred.
- The 74 were visible during creation/refinement of the current rules and are
  permanently development-only.
- The 2,263 blank rows are an unannotated source pool, not evaluation data.
- The Common Voice source is CC0 under the bundled release terms. The terms for
  redistributing collaborator targets must be recorded separately.

### DS17 — refreshed Common Voice Sesotho release

- Status: active local release, received untouched and hashed.
- Release: `cv-corpus-26.0-2026-06-12`, full Common Voice **Scripted Speech** for
  Sesotho locale `st`, not Northern Sotho/Sepedi `nso`.
- Archive SHA-256:
  `4c1863e94979c75a4dec3f6b479a5f9742b9af9b4b9e063f2d86e89d1eec6436`.
- Observed source inventory: 2,339 validated and 14,837 pending sentences,
  giving 17,176 canonical sentence records.
- Legacy overlap: all 2,337 rows matched by exact ID and text; 0 ambiguous and 0
  unmatched. All 74 existing human targets were preserved.
- Active role: fresh source inventory and human-annotation candidate pool.
- The archive's original ASR split names remain provenance only; SesoFix will
  freeze independent cross-standard adaptation manifests after deduplication.

See [the refresh protocol](COMMON_VOICE_REFRESH.md).

## 2. Reference-only local resources

- DS04: South African Sesotho government custom dictionary (~3,300 entries).
- DS05: Lwazi II pronunciation dictionary (~9,500 entries).
- DS06/DS07: Sesotho syllabifier and wordlist resources.

These resources may support error analysis or candidate-rule review. None is an
independent sentence-level Lesotho Sesotho gold standard.

## 3. Excluded resources

Speech/audio collections, Praat acoustic files, Android applications, wordlists
for other languages, nested duplicates, and stale repository snapshots have no
current role in the text adaptation study. Their historical inventory remains in
`data/DATA_MANIFEST.csv` for auditability.

## 4. Canonical lineage fields

Every accepted record must retain:

| Group | Required fields |
|---|---|
| Provider | dataset ID, release, locale, source TSV/split, provider sentence ID |
| Source identity | raw text, NFC view, raw SHA-256, matching SHA-256 |
| Human target | raw target, annotator code, stage, timestamp, decision, confidence |
| Review | reviewer code, independent target/decision, disagreement, adjudicated target |
| Evidence | human/machine origin, single-annotator flag, contamination flag, eligibility |
| Legacy | workbook file, sheet, row, raw similarity cell, target-formula flag, match method |
| Split | duplicate cluster, frozen partition, manifest hash |

Raw and normalized strings are both kept. Matching normalization is limited to
Unicode NFC and documented whitespace/quote handling; it must not rewrite a
linguistic difference.

## 5. Planned downstream source

Amazon MASSIVE is planned for the semantic-parsing study. It is not currently a
Sesotho gold dataset in this repository. Any South African and Lesotho Sesotho
utterances will be newly constructed, with intent/slot labels preserved and
human test translations independently reviewed. MASSIVE-derived machine
localizations are synthetic training data, never gold targets.
