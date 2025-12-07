#!/usr/bin/env python3
"""
Quick deployment check script
Run this to verify data files are accessible and paths are correct
"""

import os
import sys

print("="*60)
print("Deployment Environment Check")
print("="*60)

# Check current working directory
print(f"\n1. Current working directory: {os.getcwd()}")

# Check if data directory exists
data_paths = [
    os.path.join(os.getcwd(), 'data'),
    os.path.join(os.path.dirname(__file__), 'data'),
    '/app/data',
    './data'
]

print("\n2. Checking data directory paths:")
for path in data_paths:
    exists = os.path.exists(path)
    print(f"   {path}: {'✓ EXISTS' if exists else '✗ NOT FOUND'}")
    if exists:
        processed = os.path.join(path, 'processed')
        if os.path.exists(processed):
            files = os.listdir(processed)
            print(f"      → Found {len(files)} files in processed/")
            print(f"      → Sample: {files[:3]}")

# Check if processed data exists
print("\n3. Checking processed data files:")
processed_dir = os.path.join(os.getcwd(), 'data', 'processed')
if os.path.exists(processed_dir):
    required_files = [
        'cleaned_data_sample.csv',
        'area_aggregations.csv',
        'crime_type_counts.csv',
        'metadata.json'
    ]
    for file in required_files:
        filepath = os.path.join(processed_dir, file)
        exists = os.path.exists(filepath)
        size = os.path.getsize(filepath) if exists else 0
        print(f"   {file}: {'✓' if exists else '✗'} ({size:,} bytes)" if exists else f"   {file}: ✗")
else:
    print(f"   ✗ Processed directory not found at {processed_dir}")

# Test data loader
print("\n4. Testing data loader:")
try:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
    from utils.data_loader import get_data_loader
    
    loader = get_data_loader()
    print(f"   ✓ DataLoader initialized")
    print(f"   Base dir: {loader.base_dir}")
    
    test_data = loader.load_cleaned_data(sample=True)
    if test_data is not None:
        print(f"   ✓ Successfully loaded {len(test_data)} rows")
    else:
        print(f"   ✗ Failed to load data")
        
except Exception as e:
    print(f"   ✗ Error: {e}")
    import traceback
    traceback.print_exc()

# Check environment variables
print("\n5. Environment variables:")
env_vars = ['PORT', 'DASH_DEBUG', 'PYTHONPATH']
for var in env_vars:
    value = os.environ.get(var, 'Not set')
    print(f"   {var}: {value}")

print("\n" + "="*60)
print("Check complete!")
print("="*60)

