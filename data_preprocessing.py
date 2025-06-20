"""
Data preprocessing for Sesotho orthography conversion.
This script handles loading and preprocessing data for fine-tuning a ByT5 model
to convert South African Sesotho orthography to Lesotho Sesotho orthography.
"""

import os
from datasets import Dataset, DatasetDict
import pandas as pd
import random

def load_data_from_txt(sa_file_path, ls_file_path):
    """
    Load parallel data from text files.
    
    Args:
        sa_file_path: Path to South African Sesotho text file
        ls_file_path: Path to Lesotho Sesotho text file
        
    Returns:
        Dataset with 'source' and 'target' columns
    """
    sa_texts = []
    ls_texts = []
    
    with open(sa_file_path, 'r', encoding='utf-8') as sa_file:
        sa_texts = [line.strip() for line in sa_file]
        
    with open(ls_file_path, 'r', encoding='utf-8') as ls_file:
        ls_texts = [line.strip() for line in ls_file]
    
    if len(sa_texts) != len(ls_texts):
        raise ValueError("Source and target files have different number of lines")
    
    data = {
        'source': sa_texts,
        'target': ls_texts
    }
    
    return Dataset.from_dict(data)

def load_data_from_csv(file_path, source_col='south_african', target_col='lesotho'):
    """
    Load parallel data from a CSV file.
    
    Args:
        file_path: Path to CSV file
        source_col: Column name for South African Sesotho text
        target_col: Column name for Lesotho Sesotho text
        
    Returns:
        Dataset with 'source' and 'target' columns
    """
    df = pd.read_csv(file_path)
    
    data = {
        'source': df[source_col].tolist(),
        'target': df[target_col].tolist()
    }
    
    return Dataset.from_dict(data)

def split_dataset(dataset, train_ratio=0.8, val_ratio=0.1, test_ratio=0.1, seed=42):
    """
    Split dataset into train, validation, and test sets.
    
    Args:
        dataset: Dataset to split
        train_ratio: Proportion for training set
        val_ratio: Proportion for validation set
        test_ratio: Proportion for test set
        seed: Random seed for reproducibility
        
    Returns:
        DatasetDict with 'train', 'validation', and 'test' splits
    """
    assert abs(train_ratio + val_ratio + test_ratio - 1.0) < 1e-6, "Ratios must sum to 1"
    
    dataset_size = len(dataset)
    indices = list(range(dataset_size))
    random.seed(seed)
    random.shuffle(indices)
    
    train_end = int(train_ratio * dataset_size)
    val_end = train_end + int(val_ratio * dataset_size)
    
    train_indices = indices[:train_end]
    val_indices = indices[train_end:val_end]
    test_indices = indices[val_end:]
    
    train_dataset = dataset.select(train_indices)
    val_dataset = dataset.select(val_indices)
    test_dataset = dataset.select(test_indices)
    
    return DatasetDict({
        'train': train_dataset,
        'validation': val_dataset,
        'test': test_dataset
    })

def preprocess_function(examples, tokenizer, max_input_length=128, max_target_length=128):
    """
    Tokenize and prepare inputs and targets for the model.
    
    Args:
        examples: Batch of examples
        tokenizer: Tokenizer to use
        max_input_length: Maximum input sequence length
        max_target_length: Maximum target sequence length
        
    Returns:
        Processed examples
    """
    inputs = examples['source']
    targets = examples['target']
    
    model_inputs = tokenizer(
        inputs, 
        max_length=max_input_length, 
        padding="max_length", 
        truncation=True
    )
    
    # Setup the tokenizer for targets
    with tokenizer.as_target_tokenizer():
        labels = tokenizer(
            targets, 
            max_length=max_target_length, 
            padding="max_length", 
            truncation=True
        )
    
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

def prepare_dataset(dataset_dict, tokenizer, batch_size=16, max_input_length=128, max_target_length=128):
    """
    Prepare dataset for training by tokenizing and batching.
    
    Args:
        dataset_dict: DatasetDict with splits
        tokenizer: Tokenizer to use
        batch_size: Batch size for training
        max_input_length: Maximum input sequence length
        max_target_length: Maximum target sequence length
        
    Returns:
        Processed DatasetDict
    """
    # Apply preprocessing function to all splits
    tokenized_datasets = dataset_dict.map(
        lambda examples: preprocess_function(
            examples, 
            tokenizer, 
            max_input_length=max_input_length, 
            max_target_length=max_target_length
        ),
        batched=True,
        remove_columns=dataset_dict["train"].column_names
    )
    
    return tokenized_datasets

if __name__ == "__main__":
    # Example usage
    print("Data preprocessing module for Sesotho orthography conversion")
    print("This module provides functions to load and preprocess data for fine-tuning a ByT5 model")