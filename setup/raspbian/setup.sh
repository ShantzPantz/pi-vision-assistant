#!/bin/bash

# Create python environment
python3 -m venv venv
source venv/bin/activate

# Install the dependencies:
pip install -r requirements.txt