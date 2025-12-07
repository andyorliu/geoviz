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
            # Default to project data directory
            self.base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
        else:
            self.base_dir = data_dir
        
        self.processed_dir = os.path.join(self.base_dir, 'processed')
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
            
            if os.path.exists(file_path):
                df = pd.read_csv(file_path)
                # Convert date columns if they exist
                if 'DATE OCC' in df.columns:
                    df['DATE OCC'] = pd.to_datetime(df['DATE OCC'], errors='coerce')
                if 'Date Rptd' in df.columns:
                    df['Date Rptd'] = pd.to_datetime(df['Date Rptd'], errors='coerce')
                self._cache[cache_key] = df
            else:
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
            return sorted(area_agg['AREA NAME'].unique().tolist())
        return []
    
    def get_available_crime_types(self):
        """Get list of available crime types"""
        crime_types = self.load_crime_type_counts()
        if crime_types is not None:
            return crime_types['Crime_Type'].tolist()
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

