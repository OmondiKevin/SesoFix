# SesoFix: Claim-Versus-Evidence Reproducibility Audit

**Audit Date:** 2026-08-14
**Audit Purpose:** Comprehensive scientific and empirical validation of all quantitative, dataset, model, and experimental claims across the SesoFix project documents (`SesoFix_...docx`, `seso_fix_revised_paper.md`, `seso_fix_experiment_strategy.md`, `seso_fix_publication_review.txt`, `seso_fix_reviewer_defense.txt`, and `SesoFix_Colab_Experiments_legacy.ipynb`).

> **Takeover correction:** the 74 Common Voice targets are single-annotator human
> references, not an untouched verified test set. They were exposed during rule
> development. The active metric implementation also mislabeled default chrF as
> chrF++ and macro sentence WER as corpus WER. See `docs/RESEARCH_PROTOCOL.md` for
> the replacement study design.

---

## 1. Status Definitions

* **`VERIFIED`**: Supported by raw, inspectable data artifacts, executable logs, or stored model outputs in the repository.
* **`REPRODUCIBLE`**: The raw data and code exist locally to deterministically regenerate the output, but the manuscript number was an unverified placeholder or estimate.
* **`UNVERIFIED`**: No raw data, code implementation, checkpoint, or execution log exists in repository history to back the claim.
* **`CONTRADICTED`**: The repository code or data directly contradicts the stated claim.
* **`PLANNED`**: Future experimental milestone requiring new execution.

---

## 2. Master Claim-Versus-Evidence Matrix

| # | Claim | Source Document | Required Evidence | Evidence Found in Repository | Status |
|---|---|---|---|---|---|
| **1** | Total Parallel Corpus (**12,847 pairs** in "SesoCorp") | Paper §3.1, Revised Paper §3.1 | Serialized dataset file (CSV/JSONL/TSV) containing 12,847 verified pairs. | **None.** No 12,847-row file exists in Git or local folders. `data/` only contained a 10-line mock file. | `UNVERIFIED` |
| **2** | Manually Curated Parallel Pairs (**4,231 pairs**) | Paper §3.1, Revised Paper §3.1 | Aligned Sesotho Bible / educational parallel text files. | **None.** No aligned Bible or educational text was committed or provided in datasets. | `UNVERIFIED` |
| **3** | Web-Crawled Parallel Pairs (**2,856 pairs**) | Paper §3.1, Revised Paper §3.1 | Scraped and aligned news articles from LENA / SABC. | **None.** No raw HTML, scraped texts, or alignment manifests exist. | `UNVERIFIED` |
| **4** | Synthetic Parallel Pairs (**5,760 pairs** from 20k SA sentences) | Paper §3.1, Revised Paper §3.1 | Script generating synthetic pairs from monolingual corpus + output file. | **None.** No generator script or synthetic dataset file was present. Raw SA text exists in `st.zip` (148k lines) and `Autshumato` (171k lines). | `UNVERIFIED` |
| **5** | Existence of **47 Deterministic Transformation Rules** | Paper §4.3, Revised Paper §4.3, Review Docs | Complete implementation and independent linguistic validation of 47 rules. | No legacy 47-rule implementation exists. The current cleanup contains 30 candidate rules created during exploratory work; tests verify behavior, not linguistic validity. | `CONTRADICTED` |
| **6** | Human-Verified Test Sentences in Verification Sheet (**74 pairs**) | `Southern Sesotho Sentence Verification.xlsx` | Independently reviewed, adjudicated, untouched test references. | **Found:** 74 single-annotator human targets (51 changed, 23 exact copies); independent review is absent and all were exposed during rule development. | `PARTIALLY VERIFIED DATA` / `NOT A TEST SET` |
| **7** | Dataset Splits (10,277 Train / 1,285 Val / 1,285 Test) | Paper §3.4, Revised Paper §3.4 | Manifests or files for `train.csv`, `val.csv`, `test.csv`. | **None.** No split files exist. | `UNVERIFIED` |
| **8** | Identity Copy Baseline (76.2 BLEU, 88.4 chrF++, 4.71 CED, 12.8% WER) | Paper Table 2 | Evaluation script output or predictions log. | **None.** Script `scripts/evaluate.py` existed but was never run on a real test split. | `UNVERIFIED` |
| **9** | Rule-Based Baseline (84.3 BLEU, 92.1 chrF++, 2.89 CED, 7.4% WER) | Paper Table 2, Revised Paper Table 2 | Execution log / predictions from a 47-rule baseline. | **None.** No baseline rule script or predictions file exists. | `UNVERIFIED` |
| **10** | Retrieval Baseline (79.8 BLEU, 89.7 chrF++, 3.52 CED, 9.1% WER) | Paper Table 2 | K-NN / Levenshtein retrieval code and evaluation output. | **None.** No retrieval baseline code was ever written in `scripts/`. | `UNVERIFIED` |
| **11** | Character LSTM Seq2Seq (86.7 BLEU, 93.2 chrF++, 2.34 CED, 5.9% WER) | Paper Table 2 | PyTorch/TensorFlow LSTM model script, weights, or log. | **None.** No LSTM model code exists in the repository. | `UNVERIFIED` |
| **12** | ByT5-Small Original Score (**91.4 BLEU**, 95.8 chrF++, 1.47 CED) | Paper Table 2 | Checkpoints in `checkpoints/`, predictions in `data/output/`. | **None.** Checkpoints folder is empty. `results.csv` only contained 37 toy lines from `example.py`. | `UNVERIFIED` |
| **13** | ByT5-Small Revised Clean Split (**89.2 BLEU**, 94.1 chrF++, 1.78 CED) | Revised Paper Table 2, Review Defense | Training run logs or evaluation output on clean split. | **None.** Revised manuscript numbers were theoretical projections during rebuttal drafting. | `UNVERIFIED` |
| **14** | ByT5-Base Score (**92.1 BLEU**, 96.2 chrF++, 1.32 CED, 3.4% WER) | Paper Table 2 | ByT5-Base training log or checkpoint. | **None.** No training runs or checkpoints exist. | `UNVERIFIED` |
| **15** | mT5-Small Baseline (**85.8 BLEU**, 91.9 chrF++, 2.67 CED, 6.8% WER) | Revised Paper Table 2, Review Defense | mT5-Small training run log or checkpoint. | **None.** Added to revised text as conceptual comparison; never trained. | `UNVERIFIED` |
| **16** | ByT5-Small Ablations (No synthetic: 88.2; Synthetic only: 82.6; Enc only: 85.9; Low LR: 89.7) | Paper Table 3 | 5 separate ablation training runs and metrics logs. | **None.** No ablation checkpoints or run artifacts exist. | `UNVERIFIED` |
| **17** | Human Evaluation (6 annotators, 200 sentences, α=0.71, 4.49 overall) | Paper Table 4, Revised Paper Table 4 | Raw rating spreadsheets, annotator IDs, Likert forms, agreement calculations. | **None.** No human evaluation forms or score sheets exist in repository. | `UNVERIFIED` |
| **18** | Statistical Significance Tests (Friedman test χ²=187.3, p<0.001) | Paper §5.3 | Statistical test scripts or R/Python notebooks calculating p-values. | **None.** No statistical test scripts exist. | `UNVERIFIED` |
| **19** | Out-of-Domain Generalization (OOD: 87.2; LONG: 89.7; CS: 85.3 BLEU) | Paper Table 5 | OOD, Long, and Code-Switched test set files. | **None.** No domain test splits exist in repository. | `UNVERIFIED` |
| **20** | Downstream Machine Translation Impact (**+2.3 BLEU** via SesoFix) | Revised Paper §6, Strategy doc, Notebook Cell 11 | Execution of downstream translation using `Helsinki-NLP/opus-mt-nso-en`. | **CONTRADICTED / INVALID MODEL:** `opus-mt-nso-en` is trained on `nso` (Sepedi / Northern Sotho), **not** `sot` (Southern Sesotho). Cell in notebook was unexecuted. | `CONTRADICTED` / `PLANNED` |
| **21** | Cross-Language Transfer to Setswana / Sepedi | Revised Paper §6, Notebook Cell 13 | Cross-lingual evaluation data and test results. | **None.** Cell 13 in notebook only contained a 5-sentence hardcoded list; unexecuted. | `UNVERIFIED` / `PLANNED` |

---

## 3. Forensic Summary & Key Findings

1. **Paper Numbers Were Untracked Placeholders / Theoretical Targets**:
   Every numerical metric in both the original `.docx` paper (91.4 BLEU) and the revised paper (89.2 BLEU, 85.8 BLEU for mT5) was an estimated target drafted in the manuscript without backing model runs or saved evaluation output logs.
2. **Missing Parallel Data**:
   The 12,847-pair "SesoCorp" does not exist as a finished artifact. What actually exists are raw corpora:
   - **Autshumato**: 171,292 parallel English ↔ SA Sesotho sentences.
   - **NCHLT `st.zip`**: 148,390 raw SA Sesotho sentences.
   - **Common Voice workbook**: 2,337 SA Sesotho sentences, of which 74 have single-annotator Lesotho Sesotho targets and are development-only.
3. **The Current Rules Are Hypotheses**:
   No legacy 47-rule implementation exists. The active 30-rule development engine must be independently reviewed, frozen before test access, and evaluated on newly annotated data.
4. **Downstream MT Model Flaw**:
   The downstream MT experiment in `seso_fix_experiment_strategy.md` and the legacy notebook proposed using `Helsinki-NLP/opus-mt-nso-en`. `nso` is Northern Sotho (Sepedi), whereas Sesotho is Southern Sotho (`sot` / `st`). Using `opus-mt-nso-en` for Southern Sotho downstream validation is linguistically invalid. Downstream MT must be rebuilt using authentic Southern Sotho resources (such as Autshumato English–Sesotho).
