# User Guide for SesoFix

This guide provides step-by-step instructions for using the SesoFix pipeline to convert South African Sesotho orthography to Lesotho Sesotho orthography.

## Table of Contents

- [Installation](#installation)
- [Preparing Your Data](#preparing-your-data)
- [Fine-tuning the Model](#fine-tuning-the-model)
- [Evaluating the Model](#evaluating-the-model)
- [Using the Model for Inference](#using-the-model-for-inference)
- [Example Workflows](#example-workflows)
- [Tips and Best Practices](#tips-and-best-practices)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/SesoFix.git
cd SesoFix
```

2. Create a virtual environment and install the requirements:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Preparing Your Data

SesoFix supports two data formats:

### Text Files Format

Create two text files with parallel sentences, one sentence per line:

1. `south_african.txt`: Contains South African Sesotho text
2. `lesotho.txt`: Contains the corresponding Lesotho Sesotho text

Example:
```
# south_african.txt
Ke rata ho bala dibuka.
O ya kae?
Ke nako ya ho ja.

# lesotho.txt
Ke rata ho bala libuka.
U ea kae?
Ke nako ea ho ja.
```

### CSV Format

Create a CSV file with two columns:

1. Column for South African Sesotho text (e.g., "south_african")
2. Column for Lesotho Sesotho text (e.g., "lesotho")

Example:
```csv
south_african,lesotho
"Ke rata ho bala dibuka.","Ke rata ho bala libuka."
"O ya kae?","U ea kae?"
"Ke nako ya ho ja.","Ke nako ea ho ja."
```

## Fine-tuning the Model

### Basic Fine-tuning

To fine-tune the model with default parameters:

```bash
# Using text files
python train.py --data_format txt --sa_file path/to/south_african.txt --ls_file path/to/lesotho.txt --output_dir ./model

# Using CSV file
python train.py --data_format csv --sa_file path/to/data.csv --output_dir ./model
```

### Advanced Fine-tuning Options

For more control over the fine-tuning process:

```bash
python train.py \
  --data_format csv \
  --sa_file path/to/data.csv \
  --sa_col south_african \
  --ls_col lesotho \
  --model_name google/byt5-base \
  --output_dir ./model \
  --num_train_epochs 5 \
  --train_batch_size 16 \
  --eval_batch_size 16 \
  --max_input_length 256 \
  --max_target_length 256 \
  --learning_rate 3e-5 \
  --warmup_steps 1000 \
  --weight_decay 0.01 \
  --early_stopping_patience 5
```

### Training on GPU

If you have a GPU available, the training will automatically use it. You can verify GPU usage by checking the training logs.

### Monitoring Training Progress

The training progress is logged to the console and to TensorBoard. To view the TensorBoard logs:

```bash
tensorboard --logdir ./model/logs
```

## Evaluating the Model

To evaluate the model on a test dataset:

```bash
# Using text files
python evaluate.py --data_format txt --sa_file path/to/test_sa.txt --ls_file path/to/test_ls.txt --model_dir ./model --output_file predictions.csv

# Using CSV file
python evaluate.py --data_format csv --sa_file path/to/test.csv --model_dir ./model --output_file predictions.csv
```

The evaluation script will output:
- BLEU score
- Character Error Rate (CER)
- Exact match percentage
- A CSV file with source texts, predictions, and references (if available)

## Using the Model for Inference

### Python API

You can use the fine-tuned model in your Python code:

```python
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load model and tokenizer
model_dir = "./model"
tokenizer = AutoTokenizer.from_pretrained(model_dir)
model = AutoModelForSeq2SeqLM.from_pretrained(model_dir)

# Function for inference
def convert_orthography(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    outputs = model.generate(**inputs, max_length=128)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Example usage
sa_text = "Ke rata ho bala dibuka."
ls_text = convert_orthography(sa_text)
print(f"South African: {sa_text}")
print(f"Lesotho: {ls_text}")
```

### Batch Processing

For processing multiple texts:

```python
def batch_convert(texts, batch_size=8):
    results = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        inputs = tokenizer(batch, return_tensors="pt", padding=True, truncation=True)
        outputs = model.generate(**inputs, max_length=128)
        decoded = tokenizer.batch_decode(outputs, skip_special_tokens=True)
        results.extend(decoded)
    return results

# Example usage
sa_texts = [
    "Ke rata ho bala dibuka.",
    "O ya kae?",
    "Ke nako ya ho ja."
]
ls_texts = batch_convert(sa_texts)
for sa, ls in zip(sa_texts, ls_texts):
    print(f"South African: {sa}")
    print(f"Lesotho: {ls}")
    print()
```

## Example Workflows

### Quick Start with Sample Data

The repository includes an example script that demonstrates the complete pipeline with a small sample dataset:

```bash
# On Linux/Mac
./run_example.sh

# On Windows
run_example.bat
```

### Custom Workflow for Large Datasets

For larger datasets, you might want to:

1. Split your data into training, validation, and test sets:
```python
import pandas as pd
from sklearn.model_selection import train_test_split

# Load data
df = pd.read_csv("your_data.csv")

# Split into train, validation, and test
train_df, temp_df = train_test_split(df, test_size=0.2, random_state=42)
val_df, test_df = train_test_split(temp_df, test_size=0.5, random_state=42)

# Save to separate files
train_df.to_csv("train.csv", index=False)
val_df.to_csv("val.csv", index=False)
test_df.to_csv("test.csv", index=False)
```

2. Fine-tune on the training set:
```bash
python train.py --data_format csv --sa_file train.csv --output_dir ./model
```

3. Evaluate on the test set:
```bash
python evaluate.py --data_format csv --sa_file test.csv --model_dir ./model --output_file predictions.csv
```

## Tips and Best Practices

### Data Quality

- Ensure your parallel data is well-aligned
- Clean your data to remove any inconsistencies
- Include a diverse range of examples covering different orthographic patterns

### Model Selection

- Start with `byt5-small` for development and testing
- For production or larger datasets, consider using `byt5-base` or larger
- Balance model size with your available compute resources

### Training

- Use early stopping to prevent overfitting
- Monitor the validation loss during training
- Experiment with different learning rates and batch sizes
- For very small datasets, consider data augmentation techniques

### Inference

- Use batch processing for efficiency when converting multiple texts
- Set an appropriate max_length based on your expected output length
- Consider using beam search for better quality (increase num_beams parameter)

### Evaluation

- Use multiple metrics to evaluate your model
- Compare against a baseline (e.g., rule-based conversion)
- Manually inspect a sample of predictions to identify patterns in errors

## Troubleshooting

For common issues and their solutions, see the [Troubleshooting Guide](troubleshooting.md).