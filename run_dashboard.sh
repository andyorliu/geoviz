#!/bin/bash
# Script to run the LA Crime Dashboard

# Activate virtual environment
source venv/bin/activate

# Check if processed data exists
if [ ! -d "data/processed" ] || [ -z "$(ls -A data/processed)" ]; then
    echo "Processed data not found. Running preprocessing..."
    python src/preprocess_data.py
fi

# Run the dashboard
echo "Starting dashboard..."
python src/app.py

