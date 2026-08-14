# SesoFix workplan

**Last updated:** 2026-08-14
**Policy:** no local model training

This is the authoritative project task list. A task is marked complete only when
its evidence artifact exists.

## Phase 0 — research recovery and evidence correction

| ID | Task | Status | Evidence |
|---|---|---|---|
| P0.1 | Audit legacy manuscript, notebook, data, rules, and reported results | Complete | `docs/REPRODUCIBILITY_STATUS.md` |
| P0.2 | Correct source provenance to South African Common Voice Sesotho | Complete | `docs/DATA_PROVENANCE.md` |
| P0.3 | Reframe task as South African → Lesotho cross-standard adaptation | Complete | `docs/RESEARCH_PROTOCOL.md` |
| P0.4 | Mark 74 legacy targets as single-annotator, rule-exposed development data | Complete | Protocol and loader metadata |
| P0.5 | Correct metric definitions and add SacreBLEU signatures | Complete | `src/sesofix/metrics.py` |
| P0.6 | Disable local model training | Complete | `Makefile`, CI, documentation |

## Phase 1 — Common Voice refresh and pilot preparation

| ID | Task | Status | Evidence |
|---|---|---|---|
| P1.1 | Preserve Common Voice 26.0 source archive and checksum | Complete | Release profile and local immutable archive |
| P1.2 | Profile 2,339 validated and 14,837 pending sentences | Complete | `docs/COMMON_VOICE_RELEASE_26_PROFILE.md` |
| P1.3 | Reconcile all 2,337 legacy rows against release 26.0 | Complete | 100% exact ID/text coverage |
| P1.4 | Generate immutable lossless merge package | Complete | `data/manifests/common_voice_refresh_v1.json` and private merge directory |
| P1.5 | Freeze deterministic 200-item pilot manifest | Complete | `data/manifests/pilot_v1_manifest.csv` |
| P1.6 | Produce separate primary/reviewer annotation workbooks | Complete | `outputs/sesofix_pilot_v1/` |
| P1.7 | Validate workbook formulas, controls, row counts, and visual layout | Complete | `docs/PILOT_PACKAGE.md` |
| P1.8 | Create stable Drive structure and verified native Google Sheets copies | Complete | `docs/GOOGLE_DRIVE_WORKFLOW.md` |

## Phase 2 — pilot annotation

**Current phase.** The next human action is P2.1. P2.2 can run in parallel once
an independent Lesotho Sesotho reviewer is confirmed.

| ID | Task | Status | Dependency |
|---|---|---|---|
| P2.0 | Restrict root Drive access or record procedural-only blinding | Pending | Project owner decision |
| P2.1 | Primary collaborator annotates all 200 pilot items | Pending | P1 complete |
| P2.2 | Independent Lesotho reviewer annotates all 200 blind | Pending | P2.0 and reviewer recruited |
| P2.3 | Adjudicate disagreements while retaining both original annotations | Pending | P2.1–P2.2 |
| P2.4 | Measure source acceptance, change prevalence, agreement, and time/item | Pending | P2.3 |
| P2.5 | Freeze revised instructions and phenomenon taxonomy | Pending | Pilot analysis |

## Phase 3 — final benchmark construction

| ID | Task | Status | Dependency |
|---|---|---|---|
| P3.1 | Calculate final sample size from pilot prevalence and paired discordance | Pending | P2 complete |
| P3.2 | Freeze training, development, natural-test, and challenge-test IDs | Pending | P3.1 |
| P3.3 | Complete primary annotation | Pending | Frozen manifests |
| P3.4 | Double-review all dev/test and at least 25% of training | Pending | Reviewer capacity |
| P3.5 | Adjudicate, run QA, and freeze human references | Pending | P3.3–P3.4 |

Provisional—not final—targets are 1,000 training, 250 development, 500 natural
test, and 250 challenge test items.

## Phase 4 — intrinsic systems

| ID | Task | Status |
|---|---|---|
| P4.1 | Freeze identity and rule baselines | Pending |
| P4.2 | Freeze Google translation-pivot version and outputs | Pending |
| P4.3 | Freeze closed-model zero-shot/few-shot prompts and outputs | Pending |
| P4.4 | Run reproducible open-model zero/few-shot baseline | Pending |
| P4.5 | Run retrieval/edit-template baseline | Pending |
| P4.6 | Prepare ByT5/mT5 supervision-curve notebooks | Pending |
| P4.7 | Execute supervised runs in Google Colab across fixed seeds | Pending |
| P4.8 | Compute paired uncertainty, significance, and phenomenon analysis | Pending |

No final-test target is opened until P4.1–P4.6 configurations are frozen.

## Phase 5 — downstream MASSIVE study

| ID | Task | Status |
|---|---|---|
| P5.1 | Select balanced MASSIVE intent/slot subset | Pending |
| P5.2 | Produce and review human South African/Lesotho Sesotho test utterances | Pending |
| P5.3 | Build synthetic training conditions with protected slot values | Pending |
| P5.4 | Train identical parsers in Colab | Pending |
| P5.5 | Evaluate intent accuracy, slot F1, frame EM, and semantic preservation | Pending |

## Phase 6 — paper and release

| ID | Task | Status |
|---|---|---|
| P6.1 | Freeze paper structure and planned tables/figures | Complete | `paper/PAPER_OUTLINE.md` |
| P6.2 | Write introduction, related work, task, and protocol sections | Pending | Literature refresh |
| P6.3 | Generate methods/results tables directly from immutable artifacts | Pending | P4/P5 results |
| P6.4 | Complete error analysis, ethics, limitations, and data statement | Pending | Final annotations/results |
| P6.5 | Internal native-speaker and reproducibility review | Pending | Full draft |
| P6.6 | Choose venue and format submission | Pending | Contribution strength known |

The old manuscript is not edited into a submission. The new paper is written
from this protocol and only from generated evidence.
