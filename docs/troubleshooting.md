# Troubleshooting Guide for SesoFix

This guide addresses common issues you might encounter when using the SesoFix pipeline and provides solutions to resolve them.

## Installation Issues

### Package Installation Failures

**Issue**: Error when installing requirements.

**Solution**:
1. Ensure you have Python 3.7 or higher installed:
   ```bash
   python --version
   ```
2. Try updating pip:
   ```bash
   pip install --upgrade pip
   ```
3. Install packages one by one to identify problematic dependencies:
   ```bash
   pip install transformers
   pip install datasets
   # etc.
   ```

### CUDA/GPU Issues

**Issue**: CUDA-related errors when trying to use GPU.

**Solution**:
1. Verify your CUDA installation:
   ```bash
   nvidia-smi
   ```
2. Ensure PyTorch is installed with CUDA support:
   ```bash
   python -c "import torch; print(torch.cuda.is_available())"
   ```
3. If CUDA is not available, reinstall PyTorch with the appropriate CUDA version from the [PyTorch website](https://pytorch.org/get-started/locally/).
4. If you continue to have issues, you can force CPU usage by setting:
   ```bash
   export CUDA_VISIBLE_DEVICES=""
   ```

## Data Loading Issues

### File Not Found

**Issue**: `FileNotFoundError` when loading data files.

**Solution**:
1. Check that the file paths are correct and the files exist.
2. Use absolute paths instead of relative paths.
3. Ensure you have read permissions for the files.

### CSV Format Issues

**Issue**: Error when loading CSV files.

**Solution**:
1. Check that your CSV file has the correct format and column names.
2. Ensure there are no encoding issues by specifying the encoding:
   ```python
   pd.read_csv("your_file.csv", encoding="utf-8")
   ```
3. If your CSV uses a different delimiter, specify it:
   ```python
   pd.read_csv("your_file.csv", sep="\t")  # For tab-separated files
   ```

### Mismatched Data

**Issue**: Error about source and target files having different numbers of lines.

**Solution**:
1. Ensure your parallel data files have the same number of lines.
2. Check for empty lines at the end of files.
3. Use a script to verify alignment:
   ```python
   with open("south_african.txt", "r", encoding="utf-8") as f1, open("lesotho.txt", "r", encoding="utf-8") as f2:
       sa_lines = f1.readlines()
       ls_lines = f2.readlines()
       print(f"SA lines: {len(sa_lines)}, LS lines: {len(ls_lines)}")
   ```

## Training Issues

### Out of Memory Errors

**Issue**: CUDA out of memory errors during training.

**Solution**:
1. Reduce batch size:
   ```bash
   python train.py --train_batch_size 4 --eval_batch_size 4
   ```
2. Reduce sequence length:
   ```bash
   python train.py --max_input_length 64 --max_target_length 64
   ```
3. Use a smaller model variant:
   ```bash
   python train.py --model_name google/byt5-small
   ```
4. Enable gradient accumulation:
   ```bash
   python train.py --gradient_accumulation_steps 4
   ```

### Slow Training

**Issue**: Training is taking too long.

**Solution**:
1. Use a smaller dataset for initial experiments.
2. Use a smaller model variant.
3. Reduce the number of training epochs.
4. Enable mixed precision training if you have a compatible GPU:
   ```bash
   python train.py --fp16 True
   ```

### Poor Training Results

**Issue**: Model is not learning effectively (high loss, poor metrics).

**Solution**:
1. Check your data quality and ensure the examples are representative.
2. Try different learning rates:
   ```bash
   python train.py --learning_rate 1e-4  # or 1e-5, 3e-5, etc.
   ```
3. Increase the number of training epochs:
   ```bash
   python train.py --num_train_epochs 10
   ```
4. Ensure your validation set is representative of the task.
5. Try a larger model if your dataset is substantial.

## Evaluation Issues

### Metric Calculation Errors

**Issue**: Errors when computing evaluation metrics.

**Solution**:
1. Ensure you have the `evaluate` library installed:
   ```bash
   pip install evaluate
   ```
2. Check that your predictions and references are properly formatted.
3. If using custom metrics, verify their implementation.

### Low BLEU Scores

**Issue**: Model achieves very low BLEU scores.

**Solution**:
1. BLEU may not be the most appropriate metric for orthography conversion. Consider using character error rate (CER) or exact match percentage instead.
2. Check if your test data is representative of the training data.
3. Ensure your model has been trained for enough epochs.
4. Manually inspect some predictions to understand the types of errors.

## Inference Issues

### Unexpected Outputs

**Issue**: Model produces unexpected or incorrect outputs.

**Solution**:
1. Verify that you're using the correct model checkpoint.
2. Check if your input text is properly preprocessed.
3. Try adjusting generation parameters:
   ```python
   outputs = model.generate(
       **inputs,
       max_length=128,
       num_beams=5,  # Increase beam size
       early_stopping=True
   )
   ```
4. Ensure your model was trained on similar examples.

### Slow Inference

**Issue**: Inference is too slow for your application.

**Solution**:
1. Use batch processing for multiple inputs.
2. Reduce the max_length parameter if your outputs are typically short.
3. Use a smaller model variant.
4. Consider model quantization for deployment:
   ```python
   from transformers import AutoModelForSeq2SeqLM
   
   # Load model
   model = AutoModelForSeq2SeqLM.from_pretrained("./model")
   
   # Quantize model
   model = model.half()  # Convert to FP16
   ```

## Common Error Messages

### "CUDA out of memory"

**Issue**: GPU memory is exhausted.

**Solution**: See "Out of Memory Errors" section above.

### "Expected input batch_size * num_beams to be less than"

**Issue**: Beam search parameters are too large for your GPU memory.

**Solution**: Reduce the number of beams or batch size during generation.

### "Token indices sequence length is longer than the specified maximum sequence length"

**Issue**: Input text is too long for the model's maximum sequence length.

**Solution**: 
1. Increase the max_length parameter:
   ```python
   tokenizer(text, max_length=256, truncation=True)
   ```
2. Split long texts into smaller chunks and process them separately.

## Getting Help

If you continue to experience issues not covered in this guide:

1. Check the [GitHub Issues](https://github.com/yourusername/SesoFix/issues) to see if others have encountered the same problem.
2. Create a new issue with:
   - A clear description of the problem
   - Steps to reproduce
   - Error messages and logs
   - Your environment details (OS, Python version, GPU, etc.)
3. For general questions about the underlying technologies:
   - [Hugging Face Forums](https://discuss.huggingface.co/)
   - [PyTorch Forums](https://discuss.pytorch.org/)