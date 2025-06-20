# Technical Documentation for SesoFix

This document provides technical details about the SesoFix project, including the model architecture, training process, and implementation details.

## Model Architecture

### ByT5 Model

SesoFix uses the ByT5 model, a byte-level variant of the T5 (Text-to-Text Transfer Transformer) model. Key features of ByT5:

- **Byte-level tokenization**: Unlike most transformer models that use subword tokenization, ByT5 operates directly on UTF-8 bytes. This makes it particularly suitable for languages like Sesotho, as it doesn't require a specialized tokenizer.
- **Encoder-Decoder architecture**: ByT5 follows the encoder-decoder architecture of T5, making it well-suited for sequence-to-sequence tasks like orthography conversion.
- **Pre-trained on multilingual data**: The model has been pre-trained on a large corpus of multilingual text, providing a good starting point for fine-tuning on Sesotho.

### Model Sizes

The project supports various sizes of the ByT5 model:

| Model | Parameters | Size (MB) | Recommended Use Case |
|-------|------------|-----------|----------------------|
| byt5-small | 300M | ~1,200 | Development, small datasets |
| byt5-base | 580M | ~2,300 | Medium-sized datasets |
| byt5-large | 1.2B | ~4,800 | Large datasets, production |
| byt5-xl | 3.7B | ~14,800 | Very large datasets |
| byt5-xxl | 11B | ~44,000 | Extremely large datasets |

The default model used in SesoFix is `google/byt5-small`, which provides a good balance between performance and resource requirements.

## Data Processing Pipeline

### Data Loading

The data preprocessing module supports two data formats:

1. **Text files**: Two separate files containing parallel South African Sesotho and Lesotho Sesotho texts, with one sentence per line.
2. **CSV file**: A single CSV file with columns for South African Sesotho and Lesotho Sesotho texts.

### Data Preprocessing

The preprocessing pipeline includes:

1. **Loading data**: Reading from text files or CSV files
2. **Dataset splitting**: Dividing the data into training, validation, and test sets
3. **Tokenization**: Converting text to token IDs using the ByT5 tokenizer
4. **Batching and padding**: Preparing batches of data with appropriate padding

## Training Process

### Training Configuration

The training process is configured using the `Seq2SeqTrainingArguments` class from the Hugging Face Transformers library. Key parameters include:

- **Number of epochs**: Default is 3
- **Batch size**: Default is 8 per device
- **Learning rate**: Default is 5e-5
- **Weight decay**: Default is 0.01
- **Warmup steps**: Default is 500
- **Evaluation strategy**: Evaluate after each epoch
- **Save strategy**: Save model after each epoch
- **Early stopping**: Stop training if validation loss doesn't improve for 3 consecutive evaluations

### Training Loop

The training loop is handled by the `Seq2SeqTrainer` class, which:

1. Iterates through the training data in batches
2. Computes forward and backward passes
3. Updates model parameters
4. Evaluates on validation data
5. Saves checkpoints
6. Applies early stopping if necessary

## Evaluation Metrics

The model is evaluated using the following metrics:

1. **BLEU score**: Measures the similarity between the predicted and reference texts
2. **Character Error Rate (CER)**: Measures the character-level edit distance
3. **Exact Match**: Percentage of predictions that exactly match the reference

## Inference

During inference, the model:

1. Tokenizes the input South African Sesotho text
2. Passes the tokenized input through the model
3. Generates the output sequence using beam search (default beam size: 4)
4. Decodes the output tokens to produce the Lesotho Sesotho text

## Implementation Details

### Dependencies

The project relies on the following main libraries:

- **transformers**: For the ByT5 model and training utilities
- **datasets**: For data handling and preprocessing
- **torch**: For tensor operations and model training
- **evaluate**: For computing evaluation metrics

### Memory and Compute Requirements

Memory and compute requirements vary based on the model size:

| Model | GPU Memory (Training) | GPU Memory (Inference) | Training Time (per epoch) |
|-------|----------------------|-------------------------|---------------------------|
| byt5-small | ~4GB | ~2GB | ~X minutes per 10k examples |
| byt5-base | ~8GB | ~3GB | ~2X minutes per 10k examples |
| byt5-large | ~16GB | ~5GB | ~4X minutes per 10k examples |
| byt5-xl | ~32GB+ | ~10GB | ~10X minutes per 10k examples |
| byt5-xxl | ~64GB+ | ~20GB | ~30X minutes per 10k examples |

*Note: Actual requirements may vary based on batch size, sequence length, and hardware.*

### Code Structure

The codebase is organized into the following main components:

1. **data_preprocessing.py**: Functions for loading and preprocessing data
2. **model_config.py**: Functions for loading and configuring the ByT5 model
3. **train.py**: Script for fine-tuning the model
4. **evaluate.py**: Script for evaluating the model and generating predictions
5. **example.py**: Example script demonstrating the complete pipeline

## Advanced Usage

### Custom Tokenization

While ByT5 uses byte-level tokenization by default, you can customize the tokenization process by modifying the `preprocess_function` in `data_preprocessing.py`.

### Model Customization

To customize the model architecture or training process:

1. Modify the `load_byt5_model` function in `model_config.py` to use a different pre-trained model or configuration
2. Adjust the training arguments in `get_training_args` to change the training behavior
3. Implement custom callbacks for the trainer to add functionality during training

### Distributed Training

For large datasets or models, you can enable distributed training:

```python
training_args = get_training_args(
    # ... other args
    fp16=True,  # Mixed precision training
    gradient_accumulation_steps=4,  # Accumulate gradients over multiple steps
    sharded_ddp="zero_dp_2",  # Sharded data parallel training
)
```

## Troubleshooting

See the [Troubleshooting Guide](troubleshooting.md) for solutions to common issues.