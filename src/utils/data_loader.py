"""
Data loading utilities for the dashboard
Handles loading of preprocessed data and provides efficient data access
"""

import pandas as pd
import numpy as np
import os
import json

class DataLoader:
    """Centralized data loader with caching"""
    
    def __init__(self, data_dir=None):
        if data_dir is None:
            # Default to project data directory - try multiple path strategies
            # Strategy 1: Relative to this file (src/utils/data_loader.py -> data/)
            base1 = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
            # Strategy 2: Current working directory
            base2 = os.path.join(os.getcwd(), 'data')
            # Strategy 3: Absolute path from script location
            script_dir = os.path.dirname(os.path.abspath(__file__))
            base3 = os.path.join(os.path.dirname(os.path.dirname(script_dir)), 'data')
            
            # Use first path that exists, or default to base1
            if os.path.exists(base1):
                self.base_dir = base1
            elif os.path.exists(base2):
                self.base_dir = base2
            elif os.path.exists(base3):
                self.base_dir = base3
            else:
                self.base_dir = base1  # Default fallback
            
            # Debug: print paths
            print(f"DEBUG: DataLoader initialized")
            print(f"  base_dir: {self.base_dir}")
            print(f"  base_dir exists: {os.path.exists(self.base_dir)}")
        else:
            self.base_dir = data_dir
        
        self.processed_dir = os.path.join(self.base_dir, 'processed')
        print(f"  processed_dir: {self.processed_dir}")
        print(f"  processed_dir exists: {os.path.exists(self.processed_dir)}")
        
        # List files in processed directory
        if os.path.exists(self.processed_dir):
            files = os.listdir(self.processed_dir)
            print(f"  Files in processed_dir: {len(files)} files")
            print(f"  Sample files: {files[:5]}")
        else:
            print(f"  WARNING: processed_dir does not exist!")
        
        self._cache = {}
        self._metadata = None
    
    def load_metadata(self):
        """Load dataset metadata"""
        if self._metadata is None:
            metadata_path = os.path.join(self.processed_dir, 'metadata.json')
            if os.path.exists(metadata_path):
                with open(metadata_path, 'r') as f:
                    self._metadata = json.load(f)
            else:
                self._metadata = {}
        return self._metadata
    
    def load_cleaned_data(self, sample=True):
        """Load cleaned crime data (sample or full)"""
        cache_key = 'cleaned_data_sample' if sample else 'cleaned_data_full'
        
        if cache_key not in self._cache:
            if sample:
                file_path = os.path.join(self.processed_dir, 'cleaned_data_sample.csv')
            else:
                file_path = os.path.join(self.base_dir, 'Crime_Data_from_2020_to_Present.csv')
            
            print(f"DEBUG: Loading data from: {file_path}")
            print(f"DEBUG: File exists: {os.path.exists(file_path)}")
            
            if os.path.exists(file_path):
                try:
                    df = pd.read_csv(file_path)
                    print(f"DEBUG: Loaded {len(df)} rows, {len(df.columns)} columns")
                    print(f"DEBUG: Columns: {list(df.columns)[:5]}...")
                    # Convert date columns if they exist
                    if 'DATE OCC' in df.columns:
                        df['DATE OCC'] = pd.to_datetime(df['DATE OCC'], errors='coerce')
                    if 'Date Rptd' in df.columns:
                        df['Date Rptd'] = pd.to_datetime(df['Date Rptd'], errors='coerce')
                    self._cache[cache_key] = df
                    print(f"DEBUG: Data cached successfully")
                except Exception as e:
                    print(f"DEBUG: Error loading CSV: {e}")
                    return None
            else:
                print(f"DEBUG: File not found: {file_path}")
                return None
        
        return self._cache[cache_key]
    
    def load_area_aggregations(self):
        """Load area-level aggregations"""
        if 'area_agg' not in self._cache:
            file_path = os.path.join(self.processed_dir, 'area_aggregations.csv')
            if os.path.exists(file_path):
                self._cache['area_agg'] = pd.read_csv(file_path)
            else:
                return None
        return self._cache['area_agg']
    
    def load_grid_aggregations(self):
        """Load grid cell aggregations"""
        if 'grid_agg' not in self._cache:
            file_path = os.path.join(self.processed_dir, 'grid_aggregations.csv')
            if os.path.exists(file_path):
                self._cache['grid_agg'] = pd.read_csv(file_path)
            else:
                return None
        return self._cache['grid_agg']
    
    def load_daily_aggregations(self):
        """Load daily temporal aggregations"""
        if 'daily_agg' not in self._cache:
            file_path = os.path.join(self.processed_dir, 'daily_aggregations.csv')
            if os.path.exists(file_path):
                df = pd.read_csv(file_path)
                if 'Date' in df.columns:
                    df['Date'] = pd.to_datetime(df['Date'])
                self._cache['daily_agg'] = df
            else:
                return None
        return self._cache['daily_agg']
    
    def load_hourly_aggregations(self):
        """Load hourly aggregations"""
        if 'hourly_agg' not in self._cache:
            file_path = os.path.join(self.processed_dir, 'hourly_aggregations.csv')
            if os.path.exists(file_path):
                self._cache['hourly_agg'] = pd.read_csv(file_path)
            else:
                return None
        return self._cache['hourly_agg']
    
    def load_monthly_aggregations(self):
        """Load monthly aggregations"""
        if 'monthly_agg' not in self._cache:
            file_path = os.path.join(self.processed_dir, 'monthly_aggregations.csv')
            if os.path.exists(file_path):
                self._cache['monthly_agg'] = pd.read_csv(file_path)
            else:
                return None
        return self._cache['monthly_agg']
    
    def load_crime_type_counts(self):
        """Load crime type counts"""
        if 'crime_type_counts' not in self._cache:
            file_path = os.path.join(self.processed_dir, 'crime_type_counts.csv')
            if os.path.exists(file_path):
                self._cache['crime_type_counts'] = pd.read_csv(file_path)
            else:
                return None
        return self._cache['crime_type_counts']
    
    def load_crime_by_area(self):
        """Load crime by area aggregations"""
        if 'crime_by_area' not in self._cache:
            file_path = os.path.join(self.processed_dir, 'crime_by_area.csv')
            if os.path.exists(file_path):
                self._cache['crime_by_area'] = pd.read_csv(file_path)
            else:
                return None
        return self._cache['crime_by_area']
    
    def load_multi_dimensional_agg(self):
        """Load multi-dimensional aggregations for Task 4"""
        if 'multi_dim_agg' not in self._cache:
            file_path = os.path.join(self.processed_dir, 'multi_dimensional_agg.csv')
            if os.path.exists(file_path):
                self._cache['multi_dim_agg'] = pd.read_csv(file_path)
            else:
                return None
        return self._cache['multi_dim_agg']
    
    def load_quarterly_area_agg(self):
        """Load quarterly area aggregations for Task 5"""
        if 'quarterly_area_agg' not in self._cache:
            file_path = os.path.join(self.processed_dir, 'quarterly_area_agg.csv')
            if os.path.exists(file_path):
                self._cache['quarterly_area_agg'] = pd.read_csv(file_path)
            else:
                return None
        return self._cache['quarterly_area_agg']
    
    def load_monthly_area_agg(self):
        """Load monthly area aggregations for Task 5"""
        if 'monthly_area_agg' not in self._cache:
            file_path = os.path.join(self.processed_dir, 'monthly_area_agg.csv')
            if os.path.exists(file_path):
                self._cache['monthly_area_agg'] = pd.read_csv(file_path)
            else:
                return None
        return self._cache['monthly_area_agg']
    
    def get_available_areas(self):
        """Get list of available areas"""
        area_agg = self.load_area_aggregations()
        if area_agg is not None:
            # Try different possible column names
            if 'AREA NAME' in area_agg.columns:
                return sorted(area_agg['AREA NAME'].unique().tolist())
            elif 'AREA_NAME' in area_agg.columns:
                return sorted(area_agg['AREA_NAME'].unique().tolist())
            elif 'Area Name' in area_agg.columns:
                return sorted(area_agg['Area Name'].unique().tolist())
            else:
                # Try to find a column that looks like area names
                for col in area_agg.columns:
                    if 'area' in col.lower() or 'name' in col.lower():
                        return sorted(area_agg[col].unique().tolist())
        return []
    
    def get_available_crime_types(self):
        """Get list of available crime types"""
        crime_types = self.load_crime_type_counts()
        if crime_types is not None:
            # Try different possible column names
            if 'Crm Cd Desc' in crime_types.columns:
                return crime_types['Crm Cd Desc'].tolist()
            elif 'Crime_Type' in crime_types.columns:
                return crime_types['Crime_Type'].tolist()
            elif 'Crime Type' in crime_types.columns:
                return crime_types['Crime Type'].tolist()
            else:
                # Return first column if we can't find the right one
                return crime_types.iloc[:, 0].tolist()
        return []
    
    def get_date_range(self):
        """Get available date range"""
        metadata = self.load_metadata()
        if 'date_range' in metadata:
            return metadata['date_range']
        return None
    
    def clear_cache(self):
        """Clear the data cache"""
        self._cache = {}
        self._metadata = None

# Global instance
_data_loader = None

def get_data_loader():
    """Get or create global data loader instance"""
    global _data_loader
    if _data_loader is None:
        _data_loader = DataLoader()
    return _data_loader

