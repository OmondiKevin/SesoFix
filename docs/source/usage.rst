Usage
=====

Data Format
----------

The pipeline supports two data formats:

1. **Text files**: Two separate files containing parallel South African Sesotho and Lesotho Sesotho texts, with one sentence per line.
2. **CSV file**: A single CSV file with columns for South African Sesotho and Lesotho Sesotho texts.

Fine-tuning
----------

To fine-tune the model, use the ``scripts/train_model.py`` script:

.. code-block:: bash

   # Using text files
   python scripts/train_model.py --data_format txt --sa_file data/processed/south_african.txt --ls_file data/processed/lesotho.txt --output_dir ./models

   # Using CSV file
   python scripts/train_model.py --data_format csv --sa_file data/processed/data.csv --sa_col south_african --ls_col lesotho --output_dir ./models

Additional training parameters:

- ``--model_name``: Pre-trained model name (default: "google/byt5-small")
- ``--num_train_epochs``: Number of training epochs (default: 3)
- ``--train_batch_size``: Training batch size (default: 8)
- ``--eval_batch_size``: Evaluation batch size (default: 8)
- ``--max_input_length``: Maximum input sequence length (default: 128)
- ``--max_target_length``: Maximum target sequence length (default: 128)
- ``--learning_rate``: Learning rate (default: 5e-5)
- ``--early_stopping_patience``: Early stopping patience (default: 3)

Evaluation
---------

To evaluate the model and generate predictions, use the ``scripts/evaluate.py`` script:

.. code-block:: bash

   # Using text files
   python scripts/evaluate.py --data_format txt --sa_file data/processed/south_african.txt --ls_file data/processed/lesotho.txt --model_dir ./models --output_file data/output/predictions.csv

   # Using CSV file
   python scripts/evaluate.py --data_format csv --sa_file data/processed/data.csv --sa_col south_african --ls_col lesotho --model_dir ./models --output_file data/output/predictions.csv

Additional evaluation parameters:

- ``--batch_size``: Batch size for inference (default: 8)
- ``--max_length``: Maximum sequence length (default: 128)
- ``--device``: Device to use for inference (default: "cuda" if available, else "cpu")

Example
------

The repository includes an example script that demonstrates the complete pipeline with a small sample dataset:

.. code-block:: bash

   # On Linux/Mac
   ./run_example.sh

   # On Windows
   run_example.bat

This will:

1. Create a virtual environment and install dependencies
2. Generate a small sample dataset of South African Sesotho to Lesotho Sesotho pairs
3. Fine-tune a ByT5-small model on this dataset
4. Evaluate the model and test inference on a few examples

You can also run the example script directly:

.. code-block:: bash

   python example.py

For a more customized approach, here's how to use the pipeline with your own data:

1. Prepare your data in either text files or a CSV file and place them in the ``data/processed/`` directory.
2. Fine-tune the model:

   .. code-block:: bash

      python scripts/train_model.py --data_format txt --sa_file data/processed/sa_train.txt --ls_file data/processed/ls_train.txt --output_dir ./models/sesotho_model --num_train_epochs 5

3. Evaluate the model:

   .. code-block:: bash

      python scripts/evaluate.py --data_format txt --sa_file data/processed/sa_test.txt --ls_file data/processed/ls_test.txt --model_dir ./models/sesotho_model --output_file data/output/results.csv

4. Check the results in the output file.