# Submission Strategy for SesoFix

This document outlines the publication roadmap, submission timeline, journal extension strategy, and a pre-submission quality checklist for SesoFix.

---

## 1. Venue Roadmap

### First Choice: LREC-COLING 2026 / 2028 (or next cycle)
* **Estimated Acceptance Probability (Post-Revision)**: 75%
* **Why this is the best fit**: LREC-COLING focuses heavily on language resources, dataset construction, evaluation protocols, and tools for low-resource languages. The creation of SesoCorp and the evaluation of regional orthographic harmonization align perfectly with the scope of this venue. It is highly respected in the NLP community and provides a visible platform for low-resource studies.

### Backup Venue: ACM TALLIP (Transactions on Asian and Low-Resource Language Information Processing)
* **Estimated Acceptance Probability (Post-Revision)**: 70%
* **Why this is a strong backup**: TALLIP is a peer-reviewed journal dedicated specifically to low-resource language processing. It welcomes applied NLP research and regional language normalization pipelines. The review cycle is longer than a conference, but the acceptance probability is high for technically sound papers.

### Workshop Backup: AfricaNLP Workshop (at ICLR / ACL / EMNLP)
* **Estimated Acceptance Probability (Post-Revision)**: 85%
* **Why this is a backup**: If the paper is rejected from main conference tracks or if the authors want rapid community feedback, the AfricaNLP workshop is the premier venue for African language technologies.

---

## 2. Journal Extension Strategy

After presenting the conference version at LREC-COLING, the authors can expand the paper into a full journal submission for **Language Resources and Evaluation (LRE, Springer)** or **ACM TALLIP**.

To meet the typical 30% new content requirement for journals, implement the following extensions:
1. **Multi-Dialectal Expansion**: Extend SesoFix to Setswana and Sepedi (Northern Sotho), creating a unified Sotho-Tswana orthographic harmonization system.
2. **Bidirectional Harmonization**: Train a bidirectional sequence-to-sequence model using control tokens (e.g., `<to_sa>`, `<to_ls>`) and analyze the linguistic asymmetries of converting conjunctive to disjunctive orthographies.
3. **Downstream Speech Evaluation**: Evaluate if SesoFix improves an automatic speech recognition (ASR) model trained on Lesotho speech when evaluating on South African speech inputs.

---

## 3. Pre-Submission Quality Checklist

Before submitting the manuscript, the authors MUST complete the following tasks:

- [ ] **Fix Dataset Contamination**: Re-split SesoCorp to ensure the test and validation sets contain 0% synthetic data.
- [ ] **Add mT5 Baseline**: Run the mT5-Small fine-tuning baseline and add it to Table 2.
- [ ] **Add Downstream MT Evaluation**: Run the downstream translation experiment and add Table 3 to the manuscript.
- [ ] **Linguistic Parameter Check**: Correct ByT5-Base parameter details (582M params, 12 layers, hidden size 768).
- [ ] **Rename Terminology**: Remove all occurrences of "post-editing" and replace them with "orthographic harmonization" or "orthographic normalization."
- [ ] **Expand References**: Add the 5 identified APA references from 2020–2025 (Riabi et al., 2022; Nekoto et al., 2020; Adelani et al., 2021; Rosales Núñez et al., 2021; Partanen et al., 2021).
- [ ] **Human Evaluation Details**: Add annotator demographics, compensation statements, and the evaluation rubric to the appendix.

---

## 4. Honest Paper Rating

### Pre-Revision Rating: **Weak Reject**
* *Justification*: The random train-test split containing 45% rule-generated synthetic data is a fatal methodological error. Reviewers at major venues will identify this as data leakage and reject the paper immediately. Additionally, the lack of comparisons against subword models (like mT5) makes the choice of ByT5 an unverified assumption.

### Post-Revision Rating (After executing the roadmap): **Accept** to **Strong Accept**
* *Justification*: By resolving the data leakage (using a clean test split), adding the mT5 baseline, and demonstrating downstream impact (+2.3 BLEU on translation), the paper becomes a methodologically rigorous, highly complete, and valuable contribution to low-resource Bantu NLP.
