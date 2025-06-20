#!/bin/bash

# Run the example script for Sesotho orthography conversion
# This script sets up the environment and runs the example.py script

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements if needed
if [ ! -f "venv/.requirements_installed" ]; then
    echo "Installing requirements..."
    pip install -r requirements.txt
    touch venv/.requirements_installed
fi

# Run the example script
echo "Running example script..."
python example.py

# Deactivate virtual environment
echo "Deactivating virtual environment..."
deactivate

echo "Example completed!"