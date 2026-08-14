@echo off
REM Run the example script for Sesotho orthography conversion
REM This script sets up the environment and runs the example.py script

REM Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements if needed
if not exist venv\.requirements_installed (
    echo Installing requirements...
    pip install -r requirements.txt
    type nul > venv\.requirements_installed
)

REM Run the example script
echo Running example script...
python example.py

REM Deactivate virtual environment
echo Deactivating virtual environment...
call deactivate

echo Example completed!