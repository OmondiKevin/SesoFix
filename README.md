# SesoFix: Orthographic Harmonization in Sesotho

SesoFix is an orthographic harmonization framework designed to convert South African Sesotho text into the standardized Lesotho Sesotho variant. By resolving regional spelling and morphological discrepancies, SesoFix bridges the orthographic split that fragments low-resource Sesotho corpora, improving downstream natural language processing (NLP) performance.

SesoFix fine-tunes a byte-level pre-trained transformer (**ByT5**) in a sequence-to-sequence framework, outperforming traditional rule-based converters and subword-level multilingual models (**mT5**).

---

## Key Features

* **Byte-Level Sequence-to-Sequence Modeling**: Utilizes Google's ByT5 model, which operates directly on UTF-8 bytes to prevent subword tokenization fragmentation on regional spelling variations.
* **Leakage-Prevention Splitting**: Automatically isolates rule-based synthetic data strictly to the training set, keeping validation and test splits 100% clean and composed of real-world text.
* **Baselines Included**: Contains implementations for Identity Copy, regular expression Rule-Based systems, character-level LSTMs with attention, and Edit-Distance retrieval.
* **Downstream Integration**: Verified to improve downstream Sesotho-to-English translation quality.

---

## Project Structure

```
SesoFix/
├── data/
│   ├── processed/     # Processed data splits (sample_data.csv)
│   ├── input/         # Raw source/target files
│   └── output/        # Generated model predictions
├── models/            # Saved model weights
├── logs/              # Tensorboard training logs
├── checkpoints/       # Training checkpoint saves
├── scripts/
│   ├── __init__.py
│   ├── data_preprocessing.py  # Data loading, tokenization, and leakage-prevention splitting
│   ├── model_config.py        # ByT5/mT5 configurations and parameter counters
│   ├── train_model.py         # Seq2Seq fine-tuning script
│   └── evaluate.py            # Automatic metrics evaluation (BLEU, chrF++, CED, WER)
├── __init__.py
├── example.py         # Demonstration script (runs end-to-end on sample data)
├── requirements.txt   # Core project dependencies
├── run_example.sh     # Shell runner script for Unix/Mac
└── run_example.bat    # Batch runner script for Windows
```

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/OmondiKevin/SesoFix.git
   cd SesoFix
   ```

2. **Set up environment**:
   Using the Makefile:
   ```bash
   make setup  # Creates virtual environment and installs dependencies
   ```
   Or manually:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

---

## Usage

### 1. Fine-Tuning
To fine-tune a model, use `scripts/train_model.py`. The model size, epochs, and data splits are configurable via CLI arguments.

**Important (Leakage Prevention)**: If your CSV contains synthetic training data, pass the `--synthetic_col` argument to ensure synthetic data is strictly isolated to the training set:
```bash
# Using a CSV with a column 'is_synthetic' to prevent test set contamination
python3 scripts/train_model.py \
  --data_format csv \
  --sa_file data/processed/data.csv \
  --sa_col south_african \
  --ls_col lesotho \
  --synthetic_col is_synthetic \
  --model_name "google/byt5-small" \
  --num_train_epochs 5 \
  --output_dir ./models/byt5_harmonizer
```

Additional parameters:
* `--model_name`: Pre-trained Hugging Face model checkpoint (e.g., `google/byt5-small`, `google/mt5-small`).
* `--learning_rate`: Training learning rate (default: `5e-4`).
* `--synthetic_col`: Column indicating if a row is synthetic (default: `"is_synthetic"`). Set to `None` or omit if no synthetic data exists.

### 2. Evaluation
To run evaluation and save predictions, use `scripts/evaluate.py`:
```bash
python3 scripts/evaluate.py \
  --data_format csv \
  --sa_file data/processed/test_data.csv \
  --sa_col south_african \
  --ls_col lesotho \
  --model_dir ./models/byt5_harmonizer \
  --output_file data/output/predictions.csv
```
This script computes:
* **BLEU score** (via SacreBLEU)
* **chrF++** (character n-grams)
* **Mean Character Edit Distance (CED)**
* **Word Error Rate (WER)**
* **Exact Match** rate

---

## Main Evaluation Results (Clean Test Set)

Models evaluated on the clean validation/test splits (composed strictly of manual and web-crawled text, with 0% synthetic data):

| System | BLEU ↑ | chrF++ ↑ | CED ↓ | Norm. CED (%) | WER ↓ |
|---|---|---|---|---|---|
| Identity Copy | 76.2 | 88.4 | 4.71 | 5.3% | 12.8% |
| Edit-Distance Retrieval | 79.8 | 89.7 | 3.52 | 4.0% | 9.1% |
| Rule-Based Baseline | 84.3 | 92.1 | 2.89 | 3.2% | 7.4% |
| LSTM Seq2Seq (scratch) | 86.7 | 93.2 | 2.34 | 2.6% | 5.9% |
| **mT5-Small** (subword) | 85.8 | 91.9 | 2.67 | 3.0% | 6.8% |
| **ByT5-Small** (ours) | **89.2** | **94.1** | **1.78** | **2.0%** | **4.2%** |
| **ByT5-Base** (ours) | **89.9** | **94.5** | **1.62** | **1.8%** | **3.8%** |

---

## Verification and Example Run

Run the end-to-end sample pipeline to verify that your environment is configured correctly:
```bash
make example  # On Linux/Mac
./run_example.sh  # Or run shell script
```
The script will generate a sample CSV, split the dataset using leakage-prevention (isolating synthetic rows to the training split), fine-tune a small model, and run inference examples showing output mappings.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
 SesoCorp dataset and rules are released under the Creative Commons BY-SA 4.0 license.
