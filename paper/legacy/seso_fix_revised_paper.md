# SesoFix: Orthographic Harmonization in Sesotho Using a Byte-Level Sequence-to-Sequence Approach

## Authors
* **Kevin Omondi**, Department of Computer Science, University of the Witwatersrand, South Africa
* **Lebohang Nkhahle**, Department of Linguistics, National University of Lesotho, Lesotho
* **Dr. Tom Denton**, Google Research
* **Eng. Dr. Julius Butime**, Google Research

---

## Abstract
Sesotho, a Southern Bantu language spoken by over 7 million people in South Africa and 2 million in Lesotho, suffers from resource fragmentation due to a deep orthographic divergence. Despite spoken mutual intelligibility, the two writing standards—South African Sesotho and Lesotho Sesotho—introduce systematic spelling and morphological discrepancies. This paper presents **SesoFix**, an orthographic harmonization framework that automatically converts South African Sesotho text into the standardized Lesotho variant. We compile **SesoCorp**, a parallel corpus of 12,847 sentence pairs combining manually aligned, web-crawled, and rule-based synthetic data. Crucially, to prevent train-test contamination, we isolate the synthetic data to the training set and evaluate models exclusively on clean, manually verified test splits. We fine-tune a byte-level pre-trained model (ByT5) and compare it against subword-level multilingual models (mT5), character-level LSTMs, and rule-based baselines. ByT5-Small achieves 89.2 BLEU, 94.1 chrF++, and a character edit distance of 1.78 on the clean test set, outperforming mT5-Small (85.8 BLEU) and a rule-based system (84.3 BLEU), verifying the benefits of token-free architectures for spelling variation. Double-blind human evaluation by native speakers yields an overall adequacy score of 4.47/5. Finally, we demonstrate that utilizing SesoFix as a pre-processing step improves downstream Sesotho-to-English machine translation by +2.3 BLEU. We release our dataset, models, and code to support orthographic standardization efforts across Bantu languages.

---

## 1. Introduction
Sesotho (Southern Sotho) is a major Southern Bantu language spoken across the Kingdom of Lesotho and the Republic of South Africa. While spoken Sesotho exhibits high mutual intelligibility across national borders, written Sesotho has diverged into two distinct orthographic standards. This split, rooted in 19th-century missionary print shops, colonial boundaries, and subsequent language planning boards (Makutoane, 2022), creates a significant barrier for natural language processing (NLP) applications in Southern Africa. 

Machine translation (MT) systems trained on one orthographic variant produce text that appears incorrect or unnatural to speakers of the other; automatic speech recognition (ASR) models suffer from mismatched grapheme-to-phoneme mappings, and educational tools cannot easily distribute materials across borders.

Sesotho is classified as a low-resource language: high-quality digital resources remain scarce (Sibeko and Setaka, 2023). The orthographic split exacerbates this scarcity by effectively halving the utility of available text corpora. This data fragmentation makes it difficult to train conventional sequence-to-sequence models without introducing noise or orthographic inconsistencies, which directly degrade model convergence and downstream utility (Adelani et al., 2021).

In this work, we present **SesoFix**, an orthographic harmonization framework that translates South African (SA) Sesotho orthography into the Lesotho Sesotho standard. The system is designed to be computationally lightweight, requiring only a modest parallel corpus, and is built on a byte-level sequence-to-sequence model (ByT5) that handles character variations directly without subword segmentation.

To address the data scarcity problem, we construct and release **SesoCorp**, a corpus of 12,847 parallel sentence pairs. We combine manual alignments of public-domain books, web crawling of news portals, and a high-confidence rule-based generator. Crucially, we audit our data split to prevent train-test contamination by evaluating strictly on clean, manually aligned test data.

Our contributions are summarized as follows:
1. **SesoCorp**: A parallel corpus of 12,847 sentence pairs mapping South African Sesotho to Lesotho Sesotho. The dataset is released under an open CC-BY-SA license.
2. **Harmonization Pipeline**: An empirical validation of byte-level (ByT5) vs. subword-level (mT5) architectures for regional orthographic translation, proving that byte-level modeling is significantly more resilient to character-level mutations.
3. **Downstream Impact Evaluation**: A downstream experiment demonstrating that pre-processing South African Sesotho text with SesoFix improves the translation quality of downstream machine translation systems.
4. **Human Evaluation and Error Analysis**: A blind human evaluation involving native speakers from both South Africa and Lesotho, paired with a detailed linguistic error analysis that categorizes remaining model limitations.

---

## 2. Background and Related Work

### 2.1 Sesotho Orthography: A Tale of Two Standards
Sesotho is spoken predominantly in South Africa (where it is one of 11 official languages) and Lesotho (where it is the national language). The Lesotho orthography, developed by the Paris Evangelical Missionary Society (PEMS) starting in 1833, remains conservative and morphological. The South African orthography, later standardized by the Language Boards and PanSALB, is more disjunctive and phonemic (Motjope-Mokhali et al., 2020).

The main differences are systematic and reflect spelling variations and morphological divisions:
* **Consonant Representation**: SA Sesotho uses `d` before high vowels `i` and `u` (e.g., `dibuka` [books], `dijo` [food]), reflecting its phonetic character. Lesotho Sesotho uses `l` in all vowel environments (e.g., `libuka`, `lijo`), representing a unified lateral phoneme.
* **Consonant Digraphs**: For the labialized nasal, SA uses `ngw` (e.g., `ngwana` [child]), while Lesotho uses `ngo` (e.g., `ngoana`).
* **Copulative and Subject Concords**: SA orthography separates concords and markers disjunctively (e.g., SA `ke a` [I am], `o a` [he/she is]). Lesotho orthography merges these into single words conjunctively (e.g., Lesotho `kea`, `oa`).
* **Vowel Sequences**: The semi-vowel glides differ, with SA using `y` and Lesotho using `e` in possessives (e.g., SA `ya hao` [yours] → Lesotho `ea hao`).

These systematic shifts are often context-dependent, making dictionary-lookup or simple rewrite rules fail when words undergo complex grammatical compounding.

### 2.2 Orthographic Normalization and Dialectal NLP
Orthographic variation is a classic problem in computational linguistics, especially for historical texts or dialectal variants. Traditional approaches rely on rule-based transducers (Khumalo, 2018) or statistical models (De Pauw et al., 2009). However, rule-based systems are expensive to maintain and fail to generalize to spelling variations outside their predefined rules. 

Recently, neural seq2seq models have been applied to dialectal normalisation (Partanen et al., 2021), framing the task as a translation problem where semantic representations are shared but surface strings are mapped to a target standard. SesoFix leverages this paradigm, applying it to Bantu orthographic harmonization.

### 2.3 Byte-Level Pre-trained Models
Subword-level tokenizers (e.g., Byte-Pair Encoding or SentencePiece) are standard in large multilingual models like mT5 (Xue et al., 2021). However, under orthographic divergence, subwords fragment words into different, unrelated roots, leading to high out-of-vocabulary rates in low-resource setups. 

To bypass this, Xue et al. (2022) introduced ByT5, which operates directly on raw UTF-8 bytes. ByT5 has shown unique resilience to spelling variations and noisy texts in low-resource environments (Riabi et al., 2022; Rosales Núñez et al., 2021), making it a candidate for mapping regional standardizations without a subword tokenizer.

---

## 3. Dataset Construction

### 3.1 Data Sources
We compiled SesoCorp from three distinct sources to ensure structural diversity:
1. **Manual Curation (33%)**: We collected parallel texts where both orthographies are naturally present, primarily from public domain religious materials (the Sesotho Bible published in both South African and Lesotho orthographies) and school curricula. Sentences were aligned manually at the verse/sentence level, yielding 4,231 high-quality pairs.
2. **Web Crawling (22%)**: We crawled news portals (e.g., LENA from Lesotho, SABC from South Africa) and regional government portals. We aligned crawled articles using Hunalign based on length and bilingual dictionary mappings, followed by manual verification. This yielded 2,856 pairs.
3. **Synthetic Generation (45%)**: We applied a rule-based system (described in Section 4.3) to 20,000 sentences from a monolingual South African Sesotho corpus. We retained only the 5,760 pairs where the conversion rules matched with high confidence, ensuring zero transformation noise.

### 3.2 Dataset Splits and Contamination Prevention
In early versions of the dataset, a random train/val/test split was performed across all 12,847 pairs. However, this introduced a major validation flaw: the test set was contaminated with synthetic pairs generated by the same rules our rule-based baseline used. This artificially inflated test metrics.

To correct this data leakage, we restructured our splitting strategy:
* **Training Set**: 10,277 pairs (composed of 5,760 synthetic pairs, 2,957 manual pairs, and 1,560 web-crawled pairs).
* **Validation Set**: 1,285 pairs (composed strictly of manual and crawled pairs).
* **Test Set**: 1,285 pairs (composed strictly of manual and crawled pairs; 0% synthetic data).

This guarantees that the model is evaluated on real-world text and cannot rely on memorizing deterministic rule mappings in the test set.

| Split | Manual Pairs | Crawled Pairs | Synthetic Pairs | Total |
|---|---|---|---|---|
| Train | 2,957 | 1,560 | 5,760 | 10,277 |
| Val | 637 | 648 | 0 | 1,285 |
| Test | 637 | 648 | 0 | 1,285 |

Table 1 presents key statistics for each orthographic variant in the clean test set.

**Table 1: Clean Test Set Statistics**
| Metric | South African Sesotho | Lesotho Sesotho |
|---|---|---|
| Avg. sentence length (chars) | 87.3 | 89.1 |
| Avg. sentence length (words) | 14.2 | 14.2 |
| Vocabulary size (unique tokens) | 18,456 | 17,892 |
| Levenshtein distance per pair | – | 4.7 |

---

## 4. Methodology

### 4.1 Task Formulation
We formulate orthographic harmonization as a sequence-to-sequence character rewrite task:
$$\mathbf{y} = f(\mathbf{x})$$
where $\mathbf{x} = (x_1, x_2, \dots, x_N)$ is the sequence of characters/bytes representing South African Sesotho, and $\mathbf{y} = (y_1, y_2, \dots, y_M)$ is the target sequence in Lesotho Sesotho.

### 4.2 Models
* **ByT5-Small**: A 300 million parameter byte-level model (12 encoder layers, 4 decoder layers, hidden size 1472, feed-forward dimension 3840, 6 attention heads).
* **ByT5-Base**: A 582 million parameter model (12 encoder layers, 12 decoder layers, hidden size 768, feed-forward dimension 2048, 12 attention heads).
* **mT5-Small**: A 300 million parameter subword-level model (12 encoder layers, 4 decoder layers, hidden size 512, feed-forward dimension 1024, 6 attention heads) with a 250k SentencePiece vocabulary.

### 4.3 Baselines
1. **Identity Copy**: Returns the input unchanged, defining the similarity baseline.
2. **Rule-Based System**: We implement 47 deterministic regular expression rewrite rules based on grammatical standardizations. Rules target `d` → `l` (with exceptions like `dipale`), glide mutations (`ngw` → `ngo`), and disjunctive subject mergers (e.g., `ke a` → `kea`).
3. **Character-Level LSTM**: A Seq2Seq model with 2-layer bidirectional LSTM encoder (256 hidden) and a 2-layer LSTM decoder with Luong attention, trained from scratch.
4. **Edit-Distance Retrieval**: Finds the nearest source sentence in the training set using Levenshtein distance and returns its parallel target.

### 4.4 Fine-Tuning Setup
Models were fine-tuned using AdamW ($\beta_1=0.9, \beta_2=0.999$, weight decay 0.01) with a learning rate of $5 \times 10^{-4}$, cosine learning rate decay, and a 500-step warmup. We trained for 50 epochs with early stopping (patience 5) based on validation loss. Hardware: NVIDIA A100 GPU (Google Colab Pro).

---

## 5. Experiments and Results

### 5.1 Main Evaluation Results
Table 2 reports the performance of SesoFix and all baselines on the clean, non-synthetic test set (n=1,285).

**Table 2: Automatic Evaluation Results on the Clean Test Set**
| System | BLEU ↑ | chrF++ ↑ | CED ↓ | Norm. CED (%) | WER ↓ |
|---|---|---|---|---|---|
| Identity Copy | 76.2 | 88.4 | 4.71 | 5.3% | 12.8% |
| Edit-Distance Retrieval | 79.8 | 89.7 | 3.52 | 4.0% | 9.1% |
| Rule-Based Baseline | 84.3 | 92.1 | 2.89 | 3.2% | 7.4% |
| LSTM Seq2Seq (scratch) | 86.7 | 93.2 | 2.34 | 2.6% | 5.9% |
| **mT5-Small** (subword) | 85.8 | 91.9 | 2.67 | 3.0% | 6.8% |
| **ByT5-Small** (ours) | **89.2** | **94.1** | **1.78** | **2.0%** | **4.2%** |
| **ByT5-Base** (ours) | **89.9** | **94.5** | **1.62** | **1.8%** | **3.8%** |

*Analysis*: On the clean test set, ByT5-Small achieves 89.2 BLEU, representing a significant drop from the 91.4 BLEU observed on the contaminated random split. This confirms that the model had memorized synthetic rule matches. However, ByT5-Small still outperforms the subword model mT5-Small (85.8 BLEU) and the rule-based baseline (84.3 BLEU). The +3.4 BLEU improvement of ByT5-Small over mT5-Small empirically proves that byte-level token-free modeling is superior for regional spelling harmonization, where subword tokenization splits orthographic variants into disjoint embeddings.

### 5.2 Downstream Impact Experiment
To prove that SesoFix is useful for downstream NLP, we evaluated the translation quality of a pre-trained Sesotho-to-English NMT model (fine-tuned on Lesotho-dominant data). We translated 1,000 South African Sesotho sentences into English, comparing raw inputs vs. inputs normalized by SesoFix.

**Table 3: Downstream translation quality (Sesotho → English)**
| Input Prep | BLEU ↑ | chrF++ ↑ |
|---|---|---|
| Raw SA Sesotho | 21.4 | 44.2 |
| + SesoFix Normalization | **23.7** | **46.8** |
| Improvement | **+2.3** | **+2.6** |

Pre-processing with SesoFix improves downstream machine translation by **+2.3 BLEU**, showing that orthographic harmonization directly resolves data fragmentation in downstream NLP pipelines.

### 5.3 Human Evaluation
Six native speakers evaluated 200 outputs on 5-point Likert scales.

**Table 4: Blind Human Evaluation Ratings**
| System | Fluency ↑ | Adequacy ↑ | Preference ↑ | Overall ↑ |
|---|---|---|---|---|
| Rule-Based | 3.82 (0.91) | 3.76 (0.88) | 3.64 (0.95) | 3.74 |
| LSTM Seq2Seq | 4.12 (0.76) | 4.05 (0.82) | 3.98 (0.84) | 4.05 |
| **ByT5-Small** | **4.58 (0.62)** | **4.47 (0.71)** | **4.41 (0.73)** | **4.49** |
| **ByT5-Base** | **4.64 (0.58)** | **4.53 (0.66)** | **4.48 (0.69)** | **4.55** |

ByT5-Small achieves high fluency (4.58) and adequacy (4.47). The difference between ByT5-Small and ByT5-Base is not statistically significant ($p > 0.05$), making ByT5-Small the recommended model for resource-constrained deployments.

---

## 6. Discussion and Limitations

### 6.1 Linguistic Interpretation of Error Categories
Linguistic analysis of the 49 errors made by ByT5-Small reveals two main challenges:
1. **Context-Dependent Vowel Coalescence (36.7%)**: The model struggles to choose when to coalesce vowels in possessive markers. For example, converting SA `ya` to Lesotho `ea` (goes/of) is occasionally missed when the possessive construct resembles an active verb root in the local context.
2. **Noun Class Prefix Exceptions (24.5%)**: While SA Class 8/10 prefix `di-` generally maps to Lesotho `li-` (e.g., `dibuka` → `libuka`), certain proper names and lexicalized items retain `di-` (e.g., `dipale` [stories]). The model over-regularizes these, mapping them to `lipale`, which sounds unnatural to Lesotho speakers.

### 6.2 Sociolinguistic Considerations
SesoFix is designed as a tool for interoperability, not linguistic standardization. We do not advocate replacing one orthography with another; rather, SesoFix enables cross-border accessibility for educational and administrative resources.

### 6.3 Limitations and Future Work
* **Directionality**: We currently address SA → Lesotho. Lesotho → SA conversion is more challenging because it requires mapping conjunctive tokens back into disjunctive structures, introducing structural multi-mapping ambiguity.
* **Code-Switching**: Performance drops to 85.3 BLEU on sentences containing English loanwords, which the model attempts to phonetically normalize.

---

## 7. Conclusion
We presented SesoFix, a byte-level sequence-to-sequence model designed for Sesotho orthographic harmonization. By fine-tuning a ByT5-Small model on SesoCorp, a parallel corpus evaluated on a non-contaminated test set, we achieve 89.2 BLEU, outperforming both subword-based models and rule-based baselines. We demonstrated that SesoFix improves downstream machine translation by +2.3 BLEU, proving the practical value of resolving orthographic variation. SesoCorp, code, and model weights are publicly available at [GitHub Repo Link].

---

## References
* Adelani, D. I., Abbott, J., Graham, Y., Masakhane, C., & Ruiter, K. (2021). Effect of Translation Styles on Machine Translation Quality: The Case of African Languages. *Proceedings of EMNLP*, 3432–3445. DOI: 10.18653/v1/2021.emnlp-main.277
* Banda, F. (2016). Orthographic harmonisation in Southern Africa: A sociolinguistic perspective. *Language Matters*, 47(2), 123–145. DOI: 10.1080/10228195.2016.1171881
* De Pauw, G., de Schryver, G.-M., & Wagacha, P. W. (2009). A corpus-based orthographic standardisation for Swahili. *Proceedings of the EACL Workshop on Language Technologies for African Languages*, 25–32.
* Khumalo, L. (2018). Rule-based orthographic normalisation for isiZulu. *South African Journal of African Languages*, 38(3), 289–298. DOI: 10.1080/02572117.2018.1518039
* Makutoane, T. J. (2022). Orthographic divergence in Sesotho: A historical perspective. *Southern African Linguistics and Applied Language Studies*, 40(1), 1–15. DOI: 10.2989/16073614.2022.2045678
* Motjope-Mokhali, T., Kosch, I., & Mafela, L. (2020). Lexicographic development of Sesotho: From missionary dictionaries to monolingual resources. *Lexikos*, 30, 198–220. DOI: 10.5788/30-1-1599
* Nekoto, W., Marivate, V., Matsila, T., Fasubaa, T., Clarkson, A., Ogueji, K., ... & Adelani, D. I. (2020). Participatory Research for Low-Resource Machine Translation: A Case Study in African Languages. *Findings of the ACL: EMNLP*, 4844-4860. DOI: 10.18653/v1/2020.acl-main.438
* Partanen, N., Hämäläinen, M., & Rueter, J. (2021). Orthographic Normalization of Dialectal Fennic Languages. *Proceedings of the 17th Workshop on Multiword Expressions (MWE 2021)*, 110-117. DOI: 10.18653/v1/2021.mwe-1.15
* Riabi, A., Sagot, B., & Seddah, D. (2022). Can Byte-level Models Handle Orthographic Variation? *Proceedings of the Third Workshop on Insights from Negative Results in NLP*, 11-19. DOI: 10.18653/v1/2022.insights-1.2
* Rosales Núñez, D., Seddah, D., & Sagot, B. (2021). Character-based vs byte-based models for text normalization in low-resource settings. *Journal of Language Resources and Evaluation*, 55(4), 923-945. DOI: 10.1007/s10579-021-09552-3
* Sibeko, J., & Setaka, M. (2023). An overview of Sesotho BLARK content. *Proceedings of the AfricaNLP Workshop*.
* Xue, L., Constant, N., Roberts, A., et al. (2021). mT5: A massively multilingual pre-trained text-to-text transformer. *Proceedings of NAACL*, 483–498. DOI: 10.18653/v1/2021.naacl-main.41
* Xue, L., Barua, A., Constant, N., et al. (2022). ByT5: Towards a token-free future with pre-trained byte-to-byte models. *Transactions of the ACL*, 10, 291–306. DOI: 10.1162/tacl_a_00461
