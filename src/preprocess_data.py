"""
Data preprocessing script for LA Crime Dashboard
Cleans data, creates aggregated datasets, and generates features for performance optimization
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os

# LA County bounds for filtering
LA_LAT_MIN, LA_LAT_MAX = 33.7, 34.8
LA_LON_MIN, LA_LON_MAX = -118.7, -117.9

def load_and_clean_data(csv_path, year_filter=2022):
    """Load and clean the raw crime data, filtered to specified year"""
    print("Loading dataset...")
    df = pd.read_csv(csv_path)
    
    print(f"Original dataset shape: {df.shape}")
    
    # Convert date columns
    df['Date Rptd'] = pd.to_datetime(df['Date Rptd'], errors='coerce')
    df['DATE OCC'] = pd.to_datetime(df['DATE OCC'], errors='coerce')
    
    # Extract temporal features
    df['Year'] = df['DATE OCC'].dt.year
    df['Month'] = df['DATE OCC'].dt.month
    df['DayOfWeek'] = df['DATE OCC'].dt.day_name()
    df['DayOfWeekNum'] = df['DATE OCC'].dt.dayofweek
    df['Hour'] = df['TIME OCC'] // 100
    df['Date'] = df['DATE OCC'].dt.date
    
    # Filter to specified year
    if year_filter:
        print(f"Filtering to year {year_filter}...")
        df = df[df['Year'] == year_filter]
        print(f"Records for year {year_filter}: {len(df):,}")
    
    # Create season feature
    df['Season'] = df['Month'].apply(lambda x: 
        'Spring' if x in [3,4,5] else 
        'Summer' if x in [6,7,8] else 
        'Fall' if x in [9,10,11] else 'Winter')
    
    # Filter to LA County bounds
    print("Filtering to LA County bounds...")
    valid_coords = df[(df['LAT'].notna()) & (df['LON'].notna())]
    la_coords = valid_coords[
        (valid_coords['LAT'] >= LA_LAT_MIN) & (valid_coords['LAT'] <= LA_LAT_MAX) &
        (valid_coords['LON'] >= LA_LON_MIN) & (valid_coords['LON'] <= LA_LON_MAX)
    ]
    
    print(f"Records within LA County bounds: {len(la_coords):,}")
    print(f"Percentage of valid coordinates: {len(la_coords)/len(df)*100:.1f}%")
    
    # Remove records with invalid dates
    la_coords = la_coords[la_coords['DATE OCC'].notna()]
    
    return la_coords

def create_spatial_aggregations(df, output_dir):
    """Create spatial aggregations by area and grid cells"""
    print("\nCreating spatial aggregations...")
    
    # Aggregation by area
    area_agg = df.groupby(['AREA', 'AREA NAME']).agg({
        'DR_NO': 'count',
        'LAT': 'mean',
        'LON': 'mean'
    }).rename(columns={'DR_NO': 'Total_Crimes'}).reset_index()
    
    area_agg.to_csv(os.path.join(output_dir, 'area_aggregations.csv'), index=False)
    print(f"Created area aggregations: {len(area_agg)} areas")
    
    # Create grid cell aggregations (0.01 degree grid ~1km)
    df['GridLat'] = (df['LAT'] * 100).round() / 100
    df['GridLon'] = (df['LON'] * 100).round() / 100
    
    grid_agg = df.groupby(['GridLat', 'GridLon']).agg({
        'DR_NO': 'count',
        'LAT': 'mean',
        'LON': 'mean'
    }).rename(columns={'DR_NO': 'Total_Crimes'}).reset_index()
    
    grid_agg.to_csv(os.path.join(output_dir, 'grid_aggregations.csv'), index=False)
    print(f"Created grid aggregations: {len(grid_agg)} grid cells")
    
    return area_agg, grid_agg

def create_temporal_aggregations(df, output_dir):
    """Create temporal aggregations for performance"""
    print("\nCreating temporal aggregations...")
    
    # Daily aggregations
    daily_agg = df.groupby(['Date', 'Year', 'Month', 'DayOfWeek', 'DayOfWeekNum']).agg({
        'DR_NO': 'count'
    }).rename(columns={'DR_NO': 'Total_Crimes'}).reset_index()
    
    daily_agg.to_csv(os.path.join(output_dir, 'daily_aggregations.csv'), index=False)
    print(f"Created daily aggregations: {len(daily_agg)} days")
    
    # Hourly aggregations
    hourly_agg = df.groupby(['Hour', 'DayOfWeekNum']).agg({
        'DR_NO': 'count'
    }).rename(columns={'DR_NO': 'Total_Crimes'}).reset_index()
    
    hourly_agg.to_csv(os.path.join(output_dir, 'hourly_aggregations.csv'), index=False)
    print(f"Created hourly aggregations: {len(hourly_agg)} hour-day combinations")
    
    # Monthly aggregations
    monthly_agg = df.groupby(['Year', 'Month', 'Season']).agg({
        'DR_NO': 'count'
    }).rename(columns={'DR_NO': 'Total_Crimes'}).reset_index()
    
    monthly_agg.to_csv(os.path.join(output_dir, 'monthly_aggregations.csv'), index=False)
    print(f"Created monthly aggregations: {len(monthly_agg)} month-year combinations")
    
    return daily_agg, hourly_agg, monthly_agg

def create_crime_type_aggregations(df, output_dir):
    """Create crime type aggregations"""
    print("\nCreating crime type aggregations...")
    
    # Crime type counts
    crime_type_counts = df['Crm Cd Desc'].value_counts().reset_index()
    crime_type_counts.columns = ['Crime_Type', 'Count']
    crime_type_counts.to_csv(os.path.join(output_dir, 'crime_type_counts.csv'), index=False)
    print(f"Created crime type counts: {len(crime_type_counts)} crime types")
    
    # Crime type by area
    crime_area = df.groupby(['AREA NAME', 'Crm Cd Desc']).agg({
        'DR_NO': 'count'
    }).rename(columns={'DR_NO': 'Count'}).reset_index()
    crime_area.to_csv(os.path.join(output_dir, 'crime_by_area.csv'), index=False)
    print(f"Created crime by area aggregations")
    
    # Part 1 vs Part 2 aggregations
    part_agg = df.groupby(['Part 1-2']).agg({
        'DR_NO': 'count'
    }).rename(columns={'DR_NO': 'Count'}).reset_index()
    part_agg.to_csv(os.path.join(output_dir, 'part1_part2_counts.csv'), index=False)
    print(f"Created Part 1/2 aggregations")
    
    return crime_type_counts, crime_area, part_agg

def create_multi_dimensional_aggregations(df, output_dir):
    """Create multi-dimensional aggregations for Task 4 (hotspot analysis)"""
    print("\nCreating multi-dimensional aggregations...")
    
    # Crime type + Time of day + Day of week + Area
    multi_dim = df.groupby([
        'AREA NAME', 'Crm Cd Desc', 'Hour', 'DayOfWeekNum', 'Season'
    ]).agg({
        'DR_NO': 'count',
        'LAT': 'mean',
        'LON': 'mean'
    }).rename(columns={'DR_NO': 'Count'}).reset_index()
    
    multi_dim.to_csv(os.path.join(output_dir, 'multi_dimensional_agg.csv'), index=False)
    print(f"Created multi-dimensional aggregations: {len(multi_dim)} combinations")
    
    return multi_dim

def create_temporal_spatial_aggregations(df, output_dir):
    """Create temporal-spatial aggregations for Task 5 (displacement analysis)"""
    print("\nCreating temporal-spatial aggregations for displacement analysis...")
    
    # Quarterly aggregations by area
    df['Quarter'] = df['DATE OCC'].dt.to_period('Q').astype(str)
    
    quarterly_area = df.groupby(['Quarter', 'AREA NAME']).agg({
        'DR_NO': 'count',
        'LAT': 'mean',
        'LON': 'mean'
    }).rename(columns={'DR_NO': 'Count'}).reset_index()
    
    quarterly_area.to_csv(os.path.join(output_dir, 'quarterly_area_agg.csv'), index=False)
    print(f"Created quarterly area aggregations: {len(quarterly_area)} combinations")
    
    # Monthly aggregations by area (for smoother animations)
    df['YearMonth'] = df['DATE OCC'].dt.to_period('M').astype(str)
    
    monthly_area = df.groupby(['YearMonth', 'AREA NAME']).agg({
        'DR_NO': 'count',
        'LAT': 'mean',
        'LON': 'mean'
    }).rename(columns={'DR_NO': 'Count'}).reset_index()
    
    monthly_area.to_csv(os.path.join(output_dir, 'monthly_area_agg.csv'), index=False)
    print(f"Created monthly area aggregations: {len(monthly_area)} combinations")
    
    return quarterly_area, monthly_area

def main():
    """Main preprocessing function"""
    # Paths
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_dir = os.path.join(base_dir, 'data')
    csv_path = os.path.join(base_dir, 'Crime_Data_from_2020_to_Present.csv')  # CSV is in root
    output_dir = os.path.join(data_dir, 'processed')
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Load and clean data - filter to 2022 only
    df = load_and_clean_data(csv_path, year_filter=2022)
    
    # Save cleaned full dataset (sample for performance)
    print("\nSaving cleaned dataset...")
    # For dashboard, we'll use a sample for initial load, but keep full data available
    sample_df = df.sample(n=min(200000, len(df)), random_state=42)
    sample_df.to_csv(os.path.join(output_dir, 'cleaned_data_sample.csv'), index=False)
    print(f"Saved sample dataset: {len(sample_df):,} records")
    
    # Create all aggregations
    create_spatial_aggregations(df, output_dir)
    create_temporal_aggregations(df, output_dir)
    create_crime_type_aggregations(df, output_dir)
    create_multi_dimensional_aggregations(df, output_dir)
    create_temporal_spatial_aggregations(df, output_dir)
    
    # Save metadata
    metadata = {
        'total_records': len(df),
        'date_range': {
            'start': str(df['DATE OCC'].min()),
            'end': str(df['DATE OCC'].max())
        },
        'areas': df['AREA NAME'].nunique(),
        'crime_types': df['Crm Cd Desc'].nunique(),
        'la_bounds': {
            'lat_min': LA_LAT_MIN,
            'lat_max': LA_LAT_MAX,
            'lon_min': LA_LON_MIN,
            'lon_max': LA_LON_MAX
        }
    }
    
    import json
    with open(os.path.join(output_dir, 'metadata.json'), 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print("\n" + "="*50)
    print("Data preprocessing complete!")
    print(f"Processed files saved to: {output_dir}")
    print("="*50)

if __name__ == '__main__':
    main()

