# SesoFix: Sesotho Orthography Conversion

This project fine-tunes a ByT5 model to convert South African Sesotho orthography to Lesotho Sesotho orthography. The model is trained to take South African Sesotho text as input and produce the corrected Lesotho Sesotho equivalent as output.

## Project Structure

- `data_preprocessing.py`: Functions for loading and preprocessing data
- `model_config.py`: Functions for loading and configuring the ByT5 model
- `train.py`: Script for fine-tuning the model
- `evaluate.py`: Script for evaluating the model and generating predictions
- `requirements.txt`: List of required packages

## Installation

1. Clone the repository:
```bash
git clone https://github.com/OmondiKevin/SesoFix.git
cd SesoFix
```

2. Create a virtual environment and install the requirements:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Data Format

The pipeline supports two data formats:

1. **Text files**: Two separate files containing parallel South African Sesotho and Lesotho Sesotho texts, with one sentence per line.
2. **CSV file**: A single CSV file with columns for South African Sesotho and Lesotho Sesotho texts.

## Usage

### Fine-tuning

To fine-tune the model, use the `train.py` script:

```bash
# Using text files
python train.py --data_format txt --sa_file path/to/south_african.txt --ls_file path/to/lesotho.txt --output_dir ./model

# Using CSV file
python train.py --data_format csv --sa_file path/to/data.csv --sa_col south_african --ls_col lesotho --output_dir ./model
```

Additional training parameters:
- `--model_name`: Pre-trained model name (default: "google/byt5-small")
- `--num_train_epochs`: Number of training epochs (default: 3)
- `--train_batch_size`: Training batch size (default: 8)
- `--eval_batch_size`: Evaluation batch size (default: 8)
- `--max_input_length`: Maximum input sequence length (default: 128)
- `--max_target_length`: Maximum target sequence length (default: 128)
- `--learning_rate`: Learning rate (default: 5e-5)
- `--early_stopping_patience`: Early stopping patience (default: 3)

### Evaluation

To evaluate the model and generate predictions, use the `evaluate.py` script:

```bash
# Using text files
python evaluate.py --data_format txt --sa_file path/to/south_african.txt --ls_file path/to/lesotho.txt --model_dir ./model --output_file predictions.csv

# Using CSV file
python evaluate.py --data_format csv --sa_file path/to/data.csv --sa_col south_african --ls_col lesotho --model_dir ./model --output_file predictions.csv
```

Additional evaluation parameters:
- `--batch_size`: Batch size for inference (default: 8)
- `--max_length`: Maximum sequence length (default: 128)
- `--device`: Device to use for inference (default: "cuda" if available, else "cpu")

## Model Selection

The default model used is `google/byt5-small`, which is a byte-level T5 model that can handle any Unicode text. This makes it suitable for processing Sesotho text without the need for a specialized tokenizer.

Other ByT5 model sizes available:
- `google/byt5-small`: 300M parameters
- `google/byt5-base`: 580M parameters
- `google/byt5-large`: 1.2B parameters
- `google/byt5-xl`: 3.7B parameters
- `google/byt5-xxl`: 11B parameters

## Metrics

The evaluation script computes the following metrics:
- **BLEU score**: Measures the similarity between the predicted and reference texts
- **Character Error Rate (CER)**: Measures the character-level edit distance
- **Exact Match**: Percentage of predictions that exactly match the reference

## Example

The repository includes an example script that demonstrates the complete pipeline with a small sample dataset:

```bash
# On Linux/Mac
./run_example.sh

# On Windows
run_example.bat
```

This will:
1. Create a virtual environment and install dependencies
2. Generate a small sample dataset of South African Sesotho to Lesotho Sesotho pairs
3. Fine-tune a ByT5-small model on this dataset
4. Evaluate the model and test inference on a few examples

You can also run the example script directly:

```bash
python example.py
```

For a more customized approach, here's how to use the pipeline with your own data:

1. Prepare your data in either text files or a CSV file.
2. Fine-tune the model:
```bash
python train.py --data_format txt --sa_file data/sa_train.txt --ls_file data/ls_train.txt --output_dir ./sesotho_model --num_train_epochs 5
```
3. Evaluate the model:
```bash
python evaluate.py --data_format txt --sa_file data/sa_test.txt --ls_file data/ls_test.txt --model_dir ./sesotho_model --output_file results.csv
```
4. Check the results in the output file.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
