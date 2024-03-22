#!/bin/bash

# Check if the virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate the virtual environment
source venv/bin/activate
# Check if requirements are already installed
if [ ! -f "requirements_installed.txt" ]; then
    # Install requirements
    pip install -r requirements.txt
    # Create a file to mark that requirements are installed
    touch requirements_installed.txt
fi

# Run main.py
python main.py