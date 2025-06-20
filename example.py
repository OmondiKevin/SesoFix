"""
Example script for Sesotho orthography conversion.
This script demonstrates how to use the SesoFix pipeline with a small sample dataset.
"""

import os
import pandas as pd
from data_preprocessing import load_data_from_csv, split_dataset, prepare_dataset
from model_config import load_byt5_model, get_training_args
from transformers import Seq2SeqTrainer, DataCollatorForSeq2Seq, EarlyStoppingCallback

def create_sample_data():
    """Create a small sample dataset for demonstration."""
    # Create directories if they don't exist
    os.makedirs("data", exist_ok=True)
    
    # Sample data: South African Sesotho to Lesotho Sesotho pairs
    # These are simplified examples for demonstration purposes
    sample_data = {
        "south_african": [
            "Ke rata ho bala dibuka.",
            "O ya kae?",
            "Ke nako ya ho ja.",
            "Bana ba bapala kantle.",
            "Ke a leboga.",
            "Dumela, o phela joang?",
            "Ke batla ho ithuta Sesotho.",
            "Letsatsi le a tjhaba.",
            "Ke lapile haholo.",
            "Metsi a phodile."
        ],
        "lesotho": [
            "Ke rata ho bala libuka.",
            "U ea kae?",
            "Ke nako ea ho ja.",
            "Bana ba bapala kantle.",
            "Kea leboha.",
            "Lumela, u phela joang?",
            "Ke batla ho ithuta Sesotho.",
            "Letsatsi lea chaba.",
            "Ke lapile haholo.",
            "Metsi a pholile."
        ]
    }
    
    # Create a DataFrame and save to CSV
    df = pd.DataFrame(sample_data)
    csv_path = "data/sample_data.csv"
    df.to_csv(csv_path, index=False)
    
    print(f"Sample data created and saved to {csv_path}")
    return csv_path

def run_example():
    """Run the example pipeline."""
    # Create sample data
    csv_path = create_sample_data()
    
    # Load data
    print("Loading data...")
    dataset = load_data_from_csv(csv_path)
    
    # Split dataset
    print("Splitting dataset...")
    dataset_dict = split_dataset(dataset, train_ratio=0.6, val_ratio=0.2, test_ratio=0.2)
    
    # Print dataset statistics
    print(f"Dataset sizes:")
    print(f"  Train: {len(dataset_dict['train'])}")
    print(f"  Validation: {len(dataset_dict['validation'])}")
    print(f"  Test: {len(dataset_dict['test'])}")
    
    # Load model and tokenizer
    print("Loading model...")
    model, tokenizer = load_byt5_model("google/byt5-small")
    
    # Prepare dataset
    print("Preparing dataset...")
    tokenized_datasets = prepare_dataset(
        dataset_dict, 
        tokenizer, 
        batch_size=2,
        max_input_length=64,
        max_target_length=64
    )
    
    # Set up training arguments
    training_args = get_training_args(
        output_dir="./example_model",
        num_train_epochs=5,
        per_device_train_batch_size=2,
        per_device_eval_batch_size=2,
        warmup_steps=0,
        weight_decay=0.01,
        logging_dir="./example_logs",
        logging_steps=1,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        save_total_limit=1,
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        greater_is_better=False,
        fp16=False,  # Set to False for CPU training
    )
    
    # Data collator
    data_collator = DataCollatorForSeq2Seq(
        tokenizer=tokenizer,
        model=model,
        padding="max_length",
        max_length=64
    )
    
    # Initialize trainer
    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets["train"],
        eval_dataset=tokenized_datasets["validation"],
        tokenizer=tokenizer,
        data_collator=data_collator,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=3)]
    )
    
    # Train model
    print("Starting training...")
    trainer.train()
    
    # Evaluate model
    print("Evaluating model...")
    eval_results = trainer.evaluate(tokenized_datasets["test"])
    print(f"Evaluation results: {eval_results}")
    
    # Save model
    print("Saving model...")
    trainer.save_model("./example_model")
    tokenizer.save_pretrained("./example_model")
    
    # Test inference
    print("\nTesting inference with examples:")
    test_examples = [
        "Ke rata ho bala dibuka.",
        "O ya kae?",
        "Metsi a phodile."
    ]
    
    model.eval()
    for example in test_examples:
        inputs = tokenizer(example, return_tensors="pt", padding=True, truncation=True)
        outputs = model.generate(**inputs, max_length=64)
        prediction = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"Input: {example}")
        print(f"Prediction: {prediction}\n")
    
    print("Example completed!")

if __name__ == "__main__":
    run_example()