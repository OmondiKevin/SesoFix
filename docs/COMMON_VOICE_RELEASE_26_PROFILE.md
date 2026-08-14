# Common Voice Sesotho release 26.0 profile

**Release:** `cv-corpus-26.0-2026-06-12`

**Corpus role:** South African Sesotho source text
**Archive SHA-256:** `4c1863e94979c75a4dec3f6b479a5f9742b9af9b4b9e063f2d86e89d1eec6436`

## Inventory

| Component | Rows/files | Interpretation |
|---|---:|---|
| Validated sentences | 2,339 | Text-corpus validation, not paired Lesotho targets |
| Pending sentences | 14,837 | Candidate pool requiring project source-quality review |
| Validated clips | 14 | ASR metadata; not the adaptation split |
| Other clips | 194 | Unresolved ASR clips |
| Invalidated clips | 1 | Failed ASR validation |
| Audio files | 209 | All reconcile with duration and clip metadata |

There are no duplicate sentence IDs, exact texts, or NFC/whitespace-normalized
texts within either the validated or pending sentence table, and no overlap
between those tables.

## Legacy reconciliation

- All 2,337 workbook rows match the current validated table by exact sentence ID.
- All 2,337 also match by exact raw text and normalized text.
- No source changed on ID match.
- All 74 collaborator targets retain exact source coverage.
- The current validated table adds only two sentences beyond the legacy set.

This makes the merge lossless and unambiguous. The 74 targets remain
development-only because their evaluation role, not their source alignment, is
contaminated by rule exposure.

## Pending-pool quality signals

| Signal | Count | Share |
|---|---:|---:|
| No community votes | 12,106 | 81.59% |
| At least one downvote | 470 | 3.17% |
| Fewer than three tokens | 180 | 1.21% |
| Non-empty variety label | 0 | 0.00% |
| Non-empty domain label | 1 | 0.01% |

Source distribution is highly concentrated: 88.66% `*.gov.za`, 6.62% Peace
Corps, 3.43% African WordNet, and 1.19% the North-West University Write It
project. Consequently, a random benchmark estimates performance on this
screened Common Voice candidate population, not on all Sesotho domains.

The empty `variant` field does not change the documented South African origin of
this corpus. It means the national standard is not encoded per row, so that
provenance must be stated at corpus level and source validity must be checked by
human annotators.

## Research decision

The 14,837 pending sentences are not called Common Voice-validated data. They are
an untouched, disjoint candidate universe. The project first runs a
development-only 200-item human pilot, then calculates the final annotation
sample and review workload from observed acceptance and disagreement.
