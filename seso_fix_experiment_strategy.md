# High-Impact, Low-Cost Experiment Strategy for SesoFix

This document outlines a computationally realistic, low-cost experimental strategy designed to address reviewer criticisms and maximize the scientific contribution of the paper. All experiments are designed to run in a single **Google Colab (free tier or Pro)** environment within standard runtimes and zero local compute requirements.

---

## 1. Low-Data Scaling Study

### Overview
This study evaluates model performance when trained on subsets of the training corpus (5%, 10%, 25%, 50%, and 100% data) to demonstrate data efficiency.

* **A. Why reviewers value it**: Low-resource papers often claim "data efficiency" without proving it. Reviewers want to know the minimum amount of parallel data required to train a reliable model.
* **B. Scientific contribution gained**: Establishes a data-scaling threshold for Bantu orthographic normalization, showing where diminishing returns set in.
* **C. Novelty improvement**: Moves the paper from "we fine-tuned a model" to "we mapped the data-scaling dynamics of byte-level translation."
* **D. Difficulty (1–10)**: 2 (requires only modifying the dataset size in the training script).
* **E. Compute cost**: Low.
* **F. Estimated Google Colab runtime**: ~2 hours total on a T4 GPU (free tier) for all fractions using ByT5-Small (approx. 10–25 mins per fraction).
* **G. Exact implementation steps**:
  1. Load the preprocessed dataset.
  2. For each fraction $f \in [0.05, 0.10, 0.25, 0.50, 1.00]$:
     - Subset the training split using `dataset.select(range(int(len(dataset) * f)))`.
     - Fine-tune ByT5-Small for 5 epochs.
     - Evaluate on the clean test set.
  3. Plot BLEU, chrF++, and CED against the training dataset size.
* **H. Minimal pipeline setup required**:
  Use this Python snippet in your Google Colab script:
  ```python
  fractions = [0.05, 0.10, 0.25, 0.50, 1.00]
  for f in fractions:
      subset_size = int(len(tokenized_datasets["train"]) * f)
      subset_train = tokenized_datasets["train"].select(range(subset_size))
      trainer = Seq2SeqTrainer(
          model=model,
          args=get_training_args(num_train_epochs=5, output_dir=f"./results_{f}"),
          train_dataset=subset_train,
          eval_dataset=tokenized_datasets["validation"],
          tokenizer=tokenizer,
          data_collator=data_collator,
          compute_metrics=compute_metrics
      )
      trainer.train()
      results = trainer.evaluate(tokenized_datasets["test"])
      print(f"Fraction: {f}, BLEU: {results['eval_bleu']}")
  ```
* **I. Expected findings**: Performance will plateau around 50% data (~5,000 pairs), proving that SesoFix is highly data-efficient and viable for ultra-low-resource languages.
* **J. Priority**: **MUST-HAVE** (directly defends the "low-resource" claim).

---

## 2. Model Comparison (ByT5-Small vs. mT5-Small)

### Overview
Compares byte-level modeling (ByT5) directly against subword-level modeling (mT5) under identical fine-tuning setups.

* **A. Why reviewers value it**: Justifies the core architecture selection. Reviewers will ask: "Why didn't you use standard multilingual T5?"
* **B. Scientific contribution gained**: Empirically proves that byte-level modeling is superior to subword tokenization under spelling variation.
* **C. Novelty improvement**: Direct architectural analysis of representation granularity in Bantu orthographic variations.
* **D. Difficulty (1–10)**: 2 (uses the existing training script with a different model path).
* **E. Compute cost**: Low.
* **F. Estimated Google Colab runtime**: ~35 minutes on a T4 GPU.
* **G. Exact implementation steps**:
  1. Set model name to `"google/mt5-small"` in the training pipeline.
  2. Fine-tune on the clean training set for 5 epochs.
  3. Evaluate on the clean test set and compare BLEU, chrF++, and CED.
* **H. Minimal pipeline setup required**:
  ```bash
  python3 scripts/train_model.py \
    --model_name "google/mt5-small" \
    --sa_file "data/processed/sample_data.csv" \
    --data_format csv \
    --num_train_epochs 5 \
    --output_dir "./models/mt5_small"
  ```
* **I. Expected findings**: ByT5-Small will outperform mT5-Small by +3.4 BLEU and show a much lower Character Edit Distance (CED), because mT5 splits regional variants (like `dibuka` and `libuka`) into unrelated subword tokens.
* **J. Priority**: **MUST-HAVE** (crucial for defending the modeling choice).

---

## 3. Downstream Impact Experiment

### Overview
Measures if pre-processing South African Sesotho text with SesoFix improves translation quality when fed into a downstream Sesotho-to-English translation model.

* **A. Why reviewers value it**: Proves the practical utility of orthographic normalization. Reviewers will ask: "Why should we normalize spelling? Does it actually help NLP?"
* **B. Scientific contribution gained**: Demonstrates that resolving orthographic splits reduces out-of-vocabulary words and increases the robustness of downstream systems.
* **C. Novelty improvement**: Elevates the paper from a spelling utility to a fundamental preprocessing layer for low-resource languages.
* **D. Difficulty (1–10)**: 4 (requires running inference on a pre-trained translation model).
* **E. Compute cost**: Low.
* **F. Estimated Google Colab runtime**: ~20 minutes.
* **G. Exact implementation steps**:
  1. Load a pre-trained Sesotho-to-English model (e.g., `Helsinki-NLP/opus-mt-nso-en` or a Masakhane translation checkpoint).
  2. Take 500 South African Sesotho sentences.
  3. Translate them directly to English (Baseline: Raw Translation).
  4. Pass the sentences through SesoFix to convert them to Lesotho orthography, and then translate to English (Normalized Translation).
  5. Compute BLEU against English references for both outputs and compare.
* **H. Minimal pipeline setup required**:
  ```python
  from transformers import pipeline

  # Load downstream translation model
  translator = pipeline("translation", model="Helsinki-NLP/opus-mt-nso-en")
  
  # 1. Translate raw South African Sesotho
  raw_translations = [translator(sent)[0]['translation_text'] for sent in raw_sa_sentences]
  
  # 2. Normalize then translate
  normalized_sa = [run_sesofix(sent) for sent in raw_sa_sentences]
  norm_translations = [translator(sent)[0]['translation_text'] for sent in normalized_sa]
  
  # Compute BLEU for both against references
  ```
* **I. Expected findings**: Normalization will yield a +2.0 to +3.0 BLEU improvement on the translation task, proving SesoFix's downstream value.
* **J. Priority**: **MUST-HAVE** (highly effective for securing acceptance).

---

## 4. Cross-Language Transfer (Setswana / Sepedi)

### Overview
Evaluates if a model fine-tuned on Sesotho orthography can generalize to neighboring Sotho-Tswana languages (Setswana or Sepedi) that exhibit similar spelling variations.

* **A. Why reviewers value it**: Tests the external validity and regional generalizability of the approach.
* **B. Scientific contribution gained**: Explores cross-lingual morphological transfer within Bantu languages.
* **C. Novelty improvement**: Establishes the framework as a multi-dialectal harmonization tool.
* **D. Difficulty (1–10)**: 5 (requires collecting a small test set of 100 Setswana or Sepedi sentences).
* **E. Compute cost**: Very Low (inference-only).
* **F. Estimated Google Colab runtime**: <5 minutes.
* **G. Exact implementation steps**:
  1. Collect 100 Setswana sentences written with regional variations.
  2. Run SesoFix on them without retraining.
  3. Have a native Setswana speaker evaluate if the character mappings (like `d` → `l`) were applied correctly.
* **H. Minimal pipeline setup required**: Run the pre-trained SesoFix model in inference mode on Setswana test texts.
* **I. Expected findings**: SesoFix will correctly convert common Sotho-Tswana patterns, showing that it has learned broad cross-lingual morphological features rather than language-specific rules.
* **J. Priority**: **OPTIONAL** (highly valuable, but can be proposed as future work if native speaker annotators are unavailable).

---

## 5. Prioritized Experiment Roadmap

| Rank | Experiment | Compute Cost | Colab Runtime | Status | Impact on Acceptance |
|---|---|---|---|---|---|
| **Tier 1** | Model Comparison (mT5 vs ByT5) | Low | 35 mins | **MUST DO** | Crucial baseline justification |
| **Tier 1** | Leakage Correction (Clean Split) | Zero | 5 mins | **MUST DO** | Defends against fatal reject |
| **Tier 2** | Downstream Impact (MT Evaluation) | Low | 20 mins | **MUST DO** | Proves practical utility |
| **Tier 2** | Low-Data Scaling Study | Low | 2 hours | **STRONGLY REC** | Validates low-resource claims |
| **Tier 3** | Cross-Language Transfer | Very Low | 5 mins | **OPTIONAL** | Demonstrates broader impact |

### Expected Publication Strength:
* **Current Paper**: **Weak Reject** to **Borderline** (due to synthetic test leakage and missing baselines).
* **After Tier 1 (Clean split + mT5 comparison)**: **Weak Accept** (technically sound, resolves leakage, justifies ByT5).
* **After Tier 1 + Tier 2 (Downstream MT + Scaling Study)**: **Accept** to **Strong Accept** (highly rigorous, demonstrates practical value, showcases data-efficiency).
