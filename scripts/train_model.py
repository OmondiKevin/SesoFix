#!/usr/bin/env python
"""
Training script for Sesotho orthography conversion.
This script serves as an entry point for training a ByT5 model to convert
South African Sesotho orthography to Lesotho Sesotho orthography.
"""

import os
import sys
import argparse
import logging
import torch
from transformers import Seq2SeqTrainer, DataCollatorForSeq2Seq, EarlyStoppingCallback

# Import from local modules
from scripts.data_preprocessing import load_data_from_txt, load_data_from_csv, split_dataset, prepare_dataset
from scripts.model_config import load_byt5_model, get_training_args, get_model_size_info

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Train a ByT5 model for Sesotho orthography conversion")

    # Data arguments
    parser.add_argument("--data_format", type=str, choices=["txt", "csv"], default="txt",
                        help="Format of the input data (txt or csv)")
    parser.add_argument("--sa_file", type=str, required=True,
                        help="Path to South African Sesotho text file or CSV file")
    parser.add_argument("--ls_file", type=str, default=None,
                        help="Path to Lesotho Sesotho text file (only for txt format)")
    parser.add_argument("--sa_col", type=str, default="south_african",
                        help="Column name for South African Sesotho text (only for csv format)")
    parser.add_argument("--ls_col", type=str, default="lesotho",
                        help="Column name for Lesotho Sesotho text (only for csv format)")

    # Model arguments
    parser.add_argument("--model_name", type=str, default="google/byt5-small",
                        help="Pre-trained model name")
    parser.add_argument("--output_dir", type=str, default="./models",
                        help="Directory to save the model")

    # Training arguments
    parser.add_argument("--num_train_epochs", type=int, default=3,
                        help="Number of training epochs")
    parser.add_argument("--train_batch_size", type=int, default=8,
                        help="Training batch size")
    parser.add_argument("--eval_batch_size", type=int, default=8,
                        help="Evaluation batch size")
    parser.add_argument("--max_input_length", type=int, default=128,
                        help="Maximum input sequence length")
    parser.add_argument("--max_target_length", type=int, default=128,
                        help="Maximum target sequence length")
    parser.add_argument("--learning_rate", type=float, default=5e-5,
                        help="Learning rate")
    parser.add_argument("--early_stopping_patience", type=int, default=3,
                        help="Early stopping patience")
    parser.add_argument("--dry-run", action="store_true",
                        help="Run script in dry-run mode (for CI/CD test)")

    return parser.parse_args()

def main():
    """Main training function."""
    args = parse_args()

    if args.dry_run:
        logger.info("[DRY RUN] Skipping training. Arguments parsed and script structure valid.")
        sys.exit(0)

    # Load data
    logger.info("Loading data...")
    if args.data_format == "txt":
        if args.ls_file is None:
            raise ValueError("ls_file must be provided for txt format")
        dataset = load_data_from_txt(args.sa_file, args.ls_file)
    else:  # csv
        dataset = load_data_from_csv(args.sa_file, args.sa_col, args.ls_col)

    # Split dataset
    logger.info("Splitting dataset...")
    dataset_dict = split_dataset(dataset, train_ratio=0.8, val_ratio=0.1, test_ratio=0.1)

    # Print dataset statistics
    logger.info(f"Dataset sizes:")
    logger.info(f"  Train: {len(dataset_dict['train'])}")
    logger.info(f"  Validation: {len(dataset_dict['validation'])}")
    logger.info(f"  Test: {len(dataset_dict['test'])}")

    # Load model and tokenizer
    logger.info(f"Loading model: {args.model_name}")
    model, tokenizer = load_byt5_model(args.model_name)

    # Print model information
    model_info = get_model_size_info(model)
    logger.info(f"Model loaded: {model.__class__.__name__}")
    logger.info(f"Total parameters: {model_info['total_parameters']:,}")
    logger.info(f"Trainable parameters: {model_info['trainable_parameters']:,}")
    logger.info(f"Model size: {model_info['model_size_mb']:.2f} MB")

    # Prepare dataset
    logger.info("Preparing dataset...")
    tokenized_datasets = prepare_dataset(
        dataset_dict, 
        tokenizer, 
        batch_size=args.train_batch_size,
        max_input_length=args.max_input_length,
        max_target_length=args.max_target_length
    )

    # Set up training arguments
    training_args = get_training_args(
        output_dir=args.output_dir,
        num_train_epochs=args.num_train_epochs,
        per_device_train_batch_size=args.train_batch_size,
        per_device_eval_batch_size=args.eval_batch_size,
        warmup_steps=0,
        weight_decay=0.01,
        logging_dir="./logs",
        logging_steps=100,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        save_total_limit=2,
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        greater_is_better=False,
        fp16=torch.cuda.is_available(),
    )

    # Data collator
    data_collator = DataCollatorForSeq2Seq(
        tokenizer=tokenizer,
        model=model,
        padding="max_length",
        max_length=args.max_input_length
    )

    # Initialize trainer
    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets["train"],
        eval_dataset=tokenized_datasets["validation"],
        tokenizer=tokenizer,
        data_collator=data_collator,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=args.early_stopping_patience)]
    )

    # Train model
    logger.info("Starting training...")
    trainer.train()

    # Evaluate model
    logger.info("Evaluating model...")
    eval_results = trainer.evaluate(tokenized_datasets["test"])
    logger.info(f"Evaluation results: {eval_results}")

    # Save model
    logger.info(f"Saving model to {args.output_dir}")
    trainer.save_model(args.output_dir)
    tokenizer.save_pretrained(args.output_dir)

    # Save checkpoints to separate directory
    os.makedirs("./checkpoints", exist_ok=True)
    logger.info(f"Saving checkpoints to ./checkpoints")

    logger.info("Training completed!")

if __name__ == "__main__":
    logger.info("Starting Sesotho orthography conversion training...")
    main()
    logger.info("Training process completed!")
