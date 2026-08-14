"""
Evaluation script for Sesotho orthography conversion.
This script evaluates a fine-tuned ByT5 model on the task of converting
South African Sesotho orthography to Lesotho Sesotho orthography.
"""

import argparse
import logging
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# Prevent local scripts directory from shadowing the third-party 'evaluate' package
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
original_sys_path = list(sys.path)
sys.path = [p for p in sys.path if os.path.abspath(p) != current_dir]
import evaluate
# Restore sys.path
sys.path = original_sys_path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Evaluate a ByT5 model for Sesotho orthography conversion")
    
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
    parser.add_argument("--model_dir", type=str, required=True,
                        help="Directory containing the fine-tuned model")
    
    # Output arguments
    parser.add_argument("--output_file", type=str, default="predictions.csv",
                        help="Path to save predictions")
    parser.add_argument("--batch_size", type=int, default=8,
                        help="Batch size for inference")
    parser.add_argument("--max_length", type=int, default=128,
                        help="Maximum sequence length")
    parser.add_argument("--device", type=str, default="cuda" if torch.cuda.is_available() else "cpu",
                        help="Device to use for inference (cuda or cpu)")
    
    return parser.parse_args()

def batch_tokenize(texts, tokenizer, max_length):
    """
    Tokenize a batch of texts.
    
    Args:
        texts: List of texts to tokenize
        tokenizer: Tokenizer to use
        max_length: Maximum sequence length
        
    Returns:
        Tokenized texts
    """
    return tokenizer(
        texts,
        padding="max_length",
        max_length=max_length,
        truncation=True,
        return_tensors="pt"
    )

def batch_generate(model, tokenized_inputs, max_length, device):
    """
    Generate predictions for a batch of inputs.
    
    Args:
        model: Model to use for generation
        tokenized_inputs: Tokenized inputs
        max_length: Maximum sequence length
        device: Device to use for inference
        
    Returns:
        Generated token IDs
    """
    # Move inputs to device
    input_ids = tokenized_inputs["input_ids"].to(device)
    attention_mask = tokenized_inputs["attention_mask"].to(device)
    
    # Generate predictions
    outputs = model.generate(
        input_ids=input_ids,
        attention_mask=attention_mask,
        max_length=max_length,
        num_beams=4,
        early_stopping=True
    )
    
    return outputs

def compute_metrics(predictions, references):
    """
    Compute evaluation metrics including BLEU, SacreBLEU, chrF++, and Character Edit Distance (CED).
    
    Args:
        predictions: List of predicted texts
        references: List of reference texts
        
    Returns:
        dict: Metrics dictionary
    """
    import evaluate
    import numpy as np

    results = {}

    # 1. Exact Match
    exact_match = sum(1 for p, r in zip(predictions, references) if p == r) / max(len(predictions), 1)
    results["exact_match"] = exact_match

    # 2. Mean Character Edit Distance (CED)
    def levenshtein_distance(s1, s2):
        if len(s1) < len(s2):
            return levenshtein_distance(s2, s1)
        if len(s2) == 0:
            return len(s1)
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        return previous_row[-1]

    edit_distances = [levenshtein_distance(p, r) for p, r in zip(predictions, references)]
    results["mean_char_edit_distance"] = sum(edit_distances) / max(len(predictions), 1)

    # 3. BLEU score
    try:
        # Standard BLEU expects a list of references for each prediction
        bleu_references = [[r] for r in references]
        bleu = evaluate.load("bleu")
        bleu_results = bleu.compute(predictions=predictions, references=bleu_references)
        results["bleu"] = bleu_results["bleu"]
    except Exception as e:
        logger.warning(f"Could not compute standard BLEU: {e}")
        results["bleu"] = None

    # 4. SacreBLEU score (if available)
    try:
        sacrebleu = evaluate.load("sacrebleu")
        sacrebleu_results = sacrebleu.compute(predictions=predictions, references=[[r] for r in references])
        results["sacrebleu"] = sacrebleu_results["score"] / 100.0  # normalize to 0-1 range to match bleu
    except Exception as e:
        logger.warning(f"Could not compute SacreBLEU (sacrebleu package might not be installed): {e}")
        results["sacrebleu"] = None

    # 5. chrF++ score (if available)
    try:
        chrf = evaluate.load("chrf")
        # In evaluate, the chrf metric supports word_order parameter for chrF++ (word_order=2)
        chrf_results = chrf.compute(predictions=predictions, references=[[r] for r in references], word_order=2)
        results["chrf_plus_plus"] = chrf_results["score"] / 100.0
    except Exception as e:
        logger.warning(f"Could not compute chrF++: {e}")
        results["chrf_plus_plus"] = None

    # 6. Character Error Rate (CER)
    try:
        cer = evaluate.load("cer")
        cer_results = cer.compute(predictions=predictions, references=references)
        results["cer"] = cer_results
    except Exception as e:
        logger.warning(f"Could not compute CER: {e}")
        results["cer"] = None

    return results

def main():
    """Main evaluation function."""
    args = parse_args()
    
    # Load data
    logger.info("Loading data...")
    if args.data_format == "txt":
        if args.ls_file is None:
            raise ValueError("ls_file must be provided for txt format")
        sa_texts = []
        ls_texts = []
        
        with open(args.sa_file, 'r', encoding='utf-8') as sa_file:
            sa_texts = [line.strip() for line in sa_file]
            
        with open(args.ls_file, 'r', encoding='utf-8') as ls_file:
            ls_texts = [line.strip() for line in ls_file]
    else:  # csv
        df = pd.read_csv(args.sa_file)
        sa_texts = df[args.sa_col].tolist()
        ls_texts = df[args.ls_col].tolist() if args.ls_col in df.columns else None
    
    # Load model and tokenizer
    logger.info(f"Loading model from {args.model_dir}")
    tokenizer = AutoTokenizer.from_pretrained(args.model_dir)
    model = AutoModelForSeq2SeqLM.from_pretrained(args.model_dir)
    model.to(args.device)
    model.eval()
    
    # Generate predictions
    logger.info("Generating predictions...")
    predictions = []
    
    # Process in batches
    for i in range(0, len(sa_texts), args.batch_size):
        # Prepend task prefix to inputs for the ByT5 model
        batch_texts = [f"normalise: {text}" for text in sa_texts[i:i+args.batch_size]]
        
        # Tokenize inputs
        tokenized_inputs = batch_tokenize(batch_texts, tokenizer, args.max_length)
        
        # Generate outputs
        with torch.no_grad():
            outputs = batch_generate(model, tokenized_inputs, args.max_length, args.device)
        
        # Decode outputs
        decoded_outputs = tokenizer.batch_decode(outputs, skip_special_tokens=True)
        predictions.extend(decoded_outputs)
        
        if (i + args.batch_size) % 100 == 0 or (i + args.batch_size) >= len(sa_texts):
            logger.info(f"Processed {min(i + args.batch_size, len(sa_texts))}/{len(sa_texts)} examples")
    
    # Compute metrics if reference texts are available
    if ls_texts is not None:
        logger.info("Computing metrics...")
        metrics = compute_metrics(predictions, ls_texts)
        for metric_name, metric_value in metrics.items():
            logger.info(f"{metric_name}: {metric_value}")
    
    # Save predictions
    logger.info(f"Saving predictions to {args.output_file}")
    output_df = pd.DataFrame({
        "source": sa_texts,
        "prediction": predictions
    })
    
    if ls_texts is not None:
        output_df["reference"] = ls_texts
    
    output_df.to_csv(args.output_file, index=False)
    
    logger.info("Evaluation completed!")

if __name__ == "__main__":
    main()