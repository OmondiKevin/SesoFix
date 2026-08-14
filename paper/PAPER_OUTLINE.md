# Paper outline

## Working title

**When One Language Code Hides Two Standards: Data-Efficient Cross-Standard
Sesotho Adaptation for Low-Resource Semantic Parsing**

The title is provisional until the downstream experiment establishes whether
semantic-parsing claims belong in the headline.

## Abstract — pending results

Five-part structure:

1. Problem: a generic Sesotho locale conceals distinct South African and Lesotho
   written standards.
2. Gap: internationalization and multilingual models are rarely evaluated for
   within-language standard mismatch.
3. Contribution: human-reviewed benchmark, supervision curve, and zero/few-shot
   comparison.
4. Results: inserted only from frozen artifacts.
5. Implication: inserted only after the downstream MASSIVE study.

## 1. Introduction

- Explain the deployment failure caused by language-code collapse.
- Distinguish cross-standard adaptation from translation and spelling correction.
- Motivate Sesotho without treating either standard as deficient.
- Connect the study to the earlier internationalization/post-editing question.
- State research questions and contributions.

Planned contributions:

1. A provenance-preserving South African→Lesotho Sesotho adaptation benchmark.
2. A controlled zero/few/supervised data-scaling comparison.
3. Safety metrics for unnecessary changes and missed necessary changes.
4. A downstream test of post-edited internationalization data for semantic
   parsing, conditional on completion.

## 2. Background and related work

### 2.1 Sesotho written standards

- Historical standardization and documented differences.
- Corpus-level South African provenance and target-community framing.
- Native-speaker roles and limits of a binary standard model.

### 2.2 Lexical normalization and cross-variety adaptation

- Lexical normalization, spelling conversion, transliteration, and dialect/variety
  adaptation.
- Why identity copy is a strong baseline when many sentences require no change.

### 2.3 Multilingual internationalization and post-editing

- Machine translation and synthetic localization.
- Zero-shot/few-shot language models.
- Prior post-editing work and the failure modes of generic language codes.

### 2.4 Multilingual semantic parsing

- MASSIVE and MTOP.
- Translation-based data creation, slot preservation, and evaluation leakage.

## 3. Task definition

- Input: South African Sesotho source string.
- Output: meaning-preserving Lesotho Sesotho written adaptation.
- `CHANGE`, `NO_CHANGE`, and exclusion decisions.
- Multiple acceptable references and adjudication policy.
- Natural-prevalence versus challenge-set estimands.

Research questions:

- **RQ1:** How well do general-purpose systems adapt the standards with no
  task-specific supervision?
- **RQ2:** How does performance change across the supervision curve?
- **RQ3:** Which linguistic phenomena cause unnecessary or missed changes?
- **RQ4:** Does adaptation improve Lesotho Sesotho semantic parsing when training
  data is created through internationalization?

## 4. Data

### 4.1 Common Voice South African Sesotho source corpus

- Release 26.0 inventory and archive checksum.
- 2,337-row exact legacy reconciliation.
- 14,837-row disjoint pending candidate universe.
- Source/domain skew and absence of per-row variant labels.

### 4.2 Legacy development seed

- One bidialectal collaborator.
- 74 targets: 51 direct changes, 23 formula-copied no-change items.
- Strict EM origin of the old `SIMILARITY` field.
- Permanent development-only contamination flag.

### 4.3 Pilot, sampling, and source-quality screening

- Fixed seed and algorithm version.
- 150-item natural sample plus 50 coverage items.
- Pilot used only to stabilize instructions and calculate workload.

### 4.4 Final annotation and adjudication

- Independent reviewer and blinding.
- Natural, challenge, development, and training roles.
- Agreement, alternative-reference retention, exclusions, and licensing.

## 5. Systems

- Identity copy.
- Frozen rule engine.
- Generic translation pivot.
- Closed-model zero-shot and few-shot.
- Reproducible open-model zero/few-shot.
- Retrieval/edit-template baseline.
- ByT5 and mT5 at matched supervision levels and fixed seeds.

Exact model/provider versions are frozen near execution and recorded verbatim.
Supervised training runs only in Google Colab.

## 6. Evaluation

- Exact match and changed-sentence exact match.
- chrF++ with SacreBLEU signature.
- Corpus CER and corpus WER.
- No-change preservation and unnecessary-change rate.
- Missed-change rate.
- Human semantic adequacy audit.
- Paired bootstrap intervals, McNemar/exact paired tests, and Holm correction.

## 7. Intrinsic results — blocked on experiments

Planned tables:

1. Corpus and annotation statistics.
2. Natural-test system comparison.
3. Challenge-test and changed/no-change comparison.
4. Supervision/data-scaling curve.
5. Phenomenon-level error analysis.
6. Human adequacy and disagreement analysis.

Planned figures:

1. End-to-end data/evidence flow.
2. Performance versus number of human pairs.
3. Error distribution by adjudicated phenomenon.

No cells or prose in this section will be populated from projections.

## 8. Downstream semantic parsing — optional until completed

- MASSIVE subset construction.
- Common English frames across all training conditions.
- Baseline localization versus post-edited conditions.
- Protected slot labels and values.
- Same parser architecture, training size, search budget, and seeds.
- Intent accuracy, slot F1, frame exact match, and slot-value preservation.

If this study is incomplete or confounded, it becomes future work and is removed
from the title and main claims.

## 9. Analysis and discussion

- What zero/few-shot systems learn without local supervision.
- Whether byte-level modeling helps once data size is controlled.
- Cost/quality trade-off of human examples.
- Conservative copying versus over-editing.
- Domain transfer from government-oriented Common Voice sentences to assistant
  utterances.
- Negative or null downstream results reported without reframing.

## 10. Ethics, data statement, and community contribution

- Annotator background by self-description, consent, compensation, and
  authorship discussion.
- Both standards treated as legitimate.
- No speaker re-identification; audio is not needed for the text task.
- Public-source/pretraining exposure caveat.
- Dataset licensing and target-release decision.
- Risks of prescriptive conversion and inappropriate deployment.

## 11. Limitations

- Small language community and limited reviewer pool.
- Corpus/domain concentration.
- Binary standard abstraction and within-standard variation.
- Public source sentences and possible pretraining exposure.
- Exact-match sensitivity to valid alternatives.
- Provider/model version drift.

## 12. Reproducibility checklist

- Source archive/file hashes.
- Frozen IDs and duplicate clusters.
- Raw and normalized text views.
- Annotation/review/adjudication lineage.
- Prompts, model IDs, dates, and raw outputs.
- Colab notebook environment and every fixed seed.
- Predictions, metric signatures, confidence intervals, and generated tables.

## Appendices

- Annotation instructions and decision examples.
- Candidate rule catalog with independent review status.
- Prompt templates.
- Hyperparameters and Colab environment.
- Full phenomenon/error taxonomy.
- Additional paired comparisons and qualitative examples.
