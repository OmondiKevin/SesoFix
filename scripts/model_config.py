"""
Model configuration for Sesotho orthography conversion.
This script handles loading and configuring the ByT5 model for fine-tuning
on the task of converting South African Sesotho orthography to Lesotho Sesotho.
"""

from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    T5Config,
    Seq2SeqTrainingArguments
)
import torch

def load_byt5_model(model_name="google/byt5-small", cache_dir=None):
    """
    Load a pre-trained ByT5 model and tokenizer.
    
    Args:
        model_name: Name or path of the pre-trained model
        cache_dir: Directory to store downloaded models
        
    Returns:
        tuple: (model, tokenizer)
    """
    print(f"Loading model: {model_name}")
    
    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir)
    
    # Load model
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name, cache_dir=cache_dir)
    
    return model, tokenizer

def get_training_args(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=100,
    eval_strategy="epoch",
    save_strategy="epoch",
    save_total_limit=2,
    load_best_model_at_end=True,
    metric_for_best_model="eval_loss",
    greater_is_better=False,
    fp16=torch.cuda.is_available(),
    gradient_accumulation_steps=1,
    label_smoothing_factor=0.0,
    lr_scheduler_type="linear",
):
    """
    Get training arguments for the Seq2Seq model.
    
    Args:
        Various training parameters
        
    Returns:
        Seq2SeqTrainingArguments object
    """
    return Seq2SeqTrainingArguments(
        output_dir=output_dir,
        num_train_epochs=num_train_epochs,
        per_device_train_batch_size=per_device_train_batch_size,
        per_device_eval_batch_size=per_device_eval_batch_size,
        warmup_steps=warmup_steps,
        weight_decay=weight_decay,
        logging_dir=logging_dir,
        logging_steps=logging_steps,
        eval_strategy=eval_strategy,
        save_strategy=save_strategy,
        save_total_limit=save_total_limit,
        load_best_model_at_end=load_best_model_at_end,
        metric_for_best_model=metric_for_best_model,
        greater_is_better=greater_is_better,
        fp16=fp16,
        gradient_accumulation_steps=gradient_accumulation_steps,
        label_smoothing_factor=label_smoothing_factor,
        lr_scheduler_type=lr_scheduler_type,
        predict_with_generate=True,
    )

def get_model_size_info(model):
    """
    Get information about model size and parameters.
    
    Args:
        model: The model to analyze
        
    Returns:
        dict: Information about model size
    """
    # Count parameters
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    
    # Get model size in MB
    param_size = 0
    for param in model.parameters():
        param_size += param.nelement() * param.element_size()
    buffer_size = 0
    for buffer in model.buffers():
        buffer_size += buffer.nelement() * buffer.element_size()
    
    size_mb = (param_size + buffer_size) / 1024**2
    
    return {
        "total_parameters": total_params,
        "trainable_parameters": trainable_params,
        "model_size_mb": size_mb
    }

if __name__ == "__main__":
    # Example usage
    model, tokenizer = load_byt5_model()
    model_info = get_model_size_info(model)
    print(f"Model loaded: {model.__class__.__name__}")
    print(f"Total parameters: {model_info['total_parameters']:,}")
    print(f"Trainable parameters: {model_info['trainable_parameters']:,}")
    print(f"Model size: {model_info['model_size_mb']:.2f} MB")