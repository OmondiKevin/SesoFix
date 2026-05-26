# Makefile for SesoFix: Sesotho Orthography Conversion

# Python interpreter
PYTHON = python
VENV = venv
PIP = $(VENV)/bin/pip
PYTHON_VENV = $(VENV)/bin/python

# Directories
DATA_DIR = data
MODELS_DIR = models
LOGS_DIR = logs
DOCS_DIR = docs
CHECKPOINTS_DIR = checkpoints

# Default target
.PHONY: all
all: setup example

# Setup virtual environment and install dependencies
.PHONY: setup
setup: $(VENV)/.requirements_installed

$(VENV):
	@echo "Creating virtual environment..."
	$(PYTHON) -m venv $(VENV)

$(VENV)/.requirements_installed: $(VENV) requirements.txt
	@echo "Installing requirements..."
	$(PIP) install -r requirements.txt
	@touch $(VENV)/.requirements_installed

# Clean generated files and directories
.PHONY: clean
clean:
	@echo "Cleaning generated files..."
	rm -rf $(MODELS_DIR)/* $(LOGS_DIR)/* $(CHECKPOINTS_DIR)/* $(DATA_DIR)/processed/* $(DATA_DIR)/output/*
	@echo "Cleaning build artifacts..."
	rm -rf __pycache__ scripts/__pycache__ .pytest_cache

# Deep clean (includes virtual environment)
.PHONY: clean-all
clean-all: clean
	@echo "Removing virtual environment..."
	rm -rf $(VENV)

# Run the example script
.PHONY: example
example: setup
	@echo "Running example script..."
	$(PYTHON_VENV) example.py

# Train the model
.PHONY: train
train: setup
	@echo "Training model..."
	$(PYTHON_VENV) scripts/train_model.py --data_format csv --sa_file data/processed/sample_data.csv --output_dir $(MODELS_DIR)/sesotho_model

# Train with custom parameters (use with make train-custom SA_FILE=path/to/file LS_FILE=path/to/file)
.PHONY: train-custom
train-custom: setup
	@echo "Training model with custom parameters..."
	$(PYTHON_VENV) scripts/train_model.py --data_format $(DATA_FORMAT) --sa_file $(SA_FILE) $(if $(LS_FILE),--ls_file $(LS_FILE)) --output_dir $(MODELS_DIR)/$(MODEL_NAME)

# Evaluate the model
.PHONY: evaluate
evaluate: setup
	@echo "Evaluating model..."
	$(PYTHON_VENV) scripts/evaluate.py --data_format csv --sa_file data/processed/sample_data.csv --model_dir $(MODELS_DIR)/sesotho_model --output_file data/output/results.csv

# Generate documentation
.PHONY: docs
docs: setup
	@echo "Generating documentation..."
	cd $(DOCS_DIR) && $(PYTHON_VENV) -m sphinx.cmd.build -b html source html

# Run tests if available
.PHONY: test
test: setup
	@echo "Running tests..."
	$(PYTHON_VENV) -m pytest -xvs

# Help target
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  all          : Setup environment and run example (default)"
	@echo "  setup        : Create virtual environment and install dependencies"
	@echo "  clean        : Remove generated files and directories"
	@echo "  clean-all    : Remove all generated files including virtual environment"
	@echo "  example      : Run the example script"
	@echo "  train        : Train the model with default parameters"
	@echo "  train-custom : Train with custom parameters (requires additional arguments)"
	@echo "  evaluate     : Evaluate the model"
	@echo "  docs         : Generate documentation"
	@echo "  test         : Run tests"
	@echo "  help         : Show this help message"
	@echo ""
	@echo "Example usage:"
	@echo "  make train-custom DATA_FORMAT=txt SA_FILE=data/input/sa.txt LS_FILE=data/input/ls.txt MODEL_NAME=custom_model"