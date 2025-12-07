"""
Check if processed data exists, if not, generate it
This can be run as part of the deployment process
"""
import os
import sys

def check_and_generate_data():
    """Check if processed data exists, generate if missing"""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    processed_dir = os.path.join(base_dir, 'data', 'processed')
    csv_path = os.path.join(base_dir, 'Crime_Data_from_2020_to_Present.csv')
    
    # Check if processed data exists
    sample_file = os.path.join(processed_dir, 'cleaned_data_sample.csv')
    
    if os.path.exists(sample_file):
        print("✓ Processed data files found")
        return True
    
    # Check if raw CSV exists
    if not os.path.exists(csv_path):
        print("✗ Raw CSV file not found. Cannot generate processed data.")
        print(f"  Expected at: {csv_path}")
        return False
    
    # Generate processed data
    print("Processed data not found. Generating...")
    try:
        from preprocess_data import main
        main()
        print("✓ Processed data generated successfully")
        return True
    except Exception as e:
        print(f"✗ Error generating processed data: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = check_and_generate_data()
    sys.exit(0 if success else 1)

