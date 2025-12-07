#!/bin/bash
# Script to set up data files for deployment
# This can be run as part of the deployment process

echo "Checking for processed data files..."

if [ ! -d "data/processed" ]; then
    echo "Creating data/processed directory..."
    mkdir -p data/processed
fi

# Check if processed files exist
if [ ! -f "data/processed/cleaned_data_sample.csv" ]; then
    echo "Processed data files not found. Generating..."
    python src/preprocess_data.py
else
    echo "Processed data files already exist. Skipping generation."
fi

echo "Data setup complete!"

