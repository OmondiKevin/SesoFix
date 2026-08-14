# SesoFix research protocol

**Status:** design freeze candidate; no confirmatory results exist

**Last revised:** 2026-08-14
**Training environment:** Google Colab only

## 1. Scientific claim

The paper will not claim that Lesotho Sesotho is the “correct” form of South
African Sesotho. It will study a deployment problem: a generic Sesotho language
code can conceal different written standards, so internationalization systems
may produce text that is linguistically valid but mismatched to the target
community.

Provisional title:

> **When One Language Code Hides Two Standards: Data-Efficient Cross-Standard
> Sesotho Post-Editing for Low-Resource Semantic Parsing**

The strongest contribution is not “we fine-tuned ByT5.” It is a controlled
answer to three questions:

1. Can general-purpose translation and language models perform South African to
   Lesotho Sesotho adaptation without task-specific training?
2. How does performance change with 0, a few, 50, 100, 250, 500, 1,000, and all
   available human examples?
3. Does better surface adaptation preserve meaning and improve a downstream
   intent/slot parser trained on internationalized synthetic data?

## 2. Evidence already available

The legacy Common Voice workbook contains 2,337 source sentences and 74 targets
created by one bidialectal collaborator. The 74 targets are human references,
not independently verified gold labels. They were used while the candidate rule
inventory was being developed, so all 74 are permanently tagged
`exposed_to_rule_development=true` and excluded from confirmatory test sets.

The present rule implementation has 30 executable candidates. Its unit tests
show that code produces the specified examples; they do not show that every rule
is linguistically sound or contextually safe.

## 3. Study A: intrinsic cross-standard adaptation

### 3.1 Data roles

| Partition | Source | Purpose | Permitted use |
|---|---|---|---|
| Legacy seed (74) | Existing workbook | Taxonomy, debugging, prompt/rule development | Development only |
| Training pool | Fresh Common Voice, newly annotated | Supervision curve and retrieval demonstrations | Training/demonstrations only |
| Development | Fresh Common Voice, newly annotated | One-time method and prompt selection | Development only |
| Natural test | Random fresh Common Voice sample | Prevalence-faithful primary evaluation | Final evaluation only |
| Challenge test | Fresh sentences enriched for candidate differences | Phenomenon coverage and failure analysis | Final evaluation only; reported separately |

No test sentence may be used to create a rule, select a prompt, choose examples,
set decoding parameters, or decide a preprocessing exception. Exact and
normalized duplicates must remain in one partition. The split manifest is
frozen before any new system output is generated.

### 3.2 Provisional annotation target

Final counts will be fixed only after the refreshed release is profiled. The
planning target is:

- 1,000 training pairs;
- 250 development pairs;
- 500 randomly sampled natural-test pairs; and
- 250 challenge-test pairs.

All development and test items receive independent second review and
adjudication. At least 25% of training items receive second review. These numbers
are workload targets, not facts about the current dataset. Before freezing them,
we will estimate the observed changed-sentence prevalence and calculate the
confidence interval/power of the primary paired comparison.

The natural and challenge tests answer different questions and must never be
pooled into one headline score. If challenge items are deliberately oversampled,
their scores do not estimate natural prevalence.

### 3.3 Systems

All systems receive exactly the same source strings and frozen normalization.

1. Identity copy.
2. Frozen rule engine versioned before test annotation is opened.
3. Generic machine-translation pivot: Sesotho → English → Sesotho, with provider,
   API model/version, date, parameters, and costs recorded.
4. Closed general-purpose model, zero-shot.
5. The same model with fixed few-shot demonstrations chosen only on development
   data.
6. At least one reproducible open model under the same zero/few-shot protocol.
7. Character-aware retrieval or edit-template baseline.
8. ByT5 and mT5 supervised baselines at each feasible point on the supervision
   curve.

Provider and checkpoint choices are frozen near execution because model
availability changes. We will not silently substitute model aliases during the
study. Training systems run only in Colab; local inference is limited to cheap
deterministic diagnostics unless the protocol explicitly records otherwise.

### 3.4 Metrics

Primary intrinsic metrics:

- exact match (EM);
- corpus chrF++ with word-order 2;
- corpus character error rate (CER);
- changed-sentence EM;
- no-change preservation accuracy;
- unnecessary-change rate on human no-change references; and
- missed-change rate on human changed references.

Secondary reporting includes corpus word error rate, BLEU, edit operation counts,
length buckets, and adjudicated transformation categories. All text metrics are
computed both on raw reference-preserving text and on a documented Unicode/
whitespace normalization view. Normalization must never erase a substantive
orthographic distinction.

Identity is a serious baseline: a dataset containing many no-change pairs can
make a conservative system appear strong. Headline scores therefore always show
the changed and unchanged strata separately.

### 3.5 Statistical analysis

- Report paired bootstrap 95% confidence intervals for corpus metrics.
- Use paired exact tests or McNemar tests for EM-style outcomes.
- For trained systems, report every fixed seed and the mean with uncertainty;
  do not choose the best seed.
- Correct families of multiple pairwise tests (Holm procedure).
- Perform phenomenon analysis on adjudicated categories, not on categories
  inferred from the evaluated system's own outputs.
- Treat prompt/model/version changes after test access as a new exploratory run,
  never as the confirmatory result.

## 4. Study B: internationalization and semantic parsing

Study B tests the original post-editing idea in a cleaner causal design.

### 4.1 Data construction

Use Amazon MASSIVE because its intent and slot representation is simpler to
preserve than the nested MTOP representation for a first downstream study.
Construct a human evaluation subset in both South African and Lesotho Sesotho.
Annotators translate meaning and slot spans/values, not just surface words.

For the larger training partition:

1. Start with the same English MASSIVE utterances and frames for every condition.
2. Produce one machine-localized South African Sesotho version.
3. Create parallel training conditions by applying no post-editing, frozen rules,
   the strongest zero/few-shot method, and the strongest supervised adapter.
4. Validate that protected slot values and frame labels are unchanged.
5. Train the same parser architecture, data size, hyperparameter search budget,
   and seeds for each condition in Colab.
6. Evaluate every parser on the same human Lesotho Sesotho test set.

This isolates the value of post-editing. Comparing different translators,
training sizes, or parser configurations across conditions would confound the
claim.

### 4.2 Downstream metrics

- intent accuracy;
- slot span/value F1;
- full-frame exact match;
- slot-value preservation after localization;
- failure counts caused specifically by post-editing; and
- human semantic adequacy on a stratified audit sample.

If post-editing improves surface similarity but damages slots or fails to improve
the parser, the paper reports that result. A negative downstream result can still
be publishable if the benchmark and analysis explain why.

## 5. Validity threats and controls

| Threat | Control |
|---|---|
| One collaborator defines the target standard | Independent Lesotho reviewer plus adjudication; document annotator backgrounds |
| Public source sentences may occur in pretraining | Targets remain newly created; report public-source limitation; separate zero-shot from supervised claims |
| Rule/prompt leakage from the original 74 | Permanent development-only tag |
| Duplicate Common Voice sentences across releases/splits | Merge by stable ID, raw hash, normalized hash; manual review for fuzzy candidates |
| “Similarity” mistaken for a human label | Recompute and name it `exact_copy_derived` |
| Inflated scores from no-change sentences | Report changed/no-change strata and challenge test separately |
| Language varieties framed as errors | Use adaptation terminology and native-speaker review |
| Model/provider drift | Record immutable model IDs, dates, parameters, prompts, and raw outputs |
| Training leakage from synthetic rules | Synthetic provenance on every row; no synthetic examples in human evaluation sets |
| Local/Colab divergence | Data manifests and hashes created locally; training notebook verifies hashes before execution |

## 6. Publication gates

The project moves forward only when each gate is satisfied:

1. **Lineage gate:** fresh archive, release metadata, checksums, and lossless legacy
   merge are complete.
2. **Annotation gate:** instructions are piloted; reviewer disagreement is
   measured; test targets are adjudicated and frozen.
3. **Benchmark gate:** identity/rules/zero/few-shot outputs and exact versions are
   archived; test set remains unopened during selection.
4. **Training gate:** Colab notebooks reproduce all supervised runs from frozen
   manifests and emit predictions/logs for every seed.
5. **Downstream gate:** slot/frame preservation passes QA before parser training.
6. **Writing gate:** manuscript tables are generated from immutable result files;
   no number is typed from memory or projected.

The legacy manuscript is not revised into a submission until at least Gates 1–4
are complete. Study B is included only if Gate 5 is completed rigorously.
