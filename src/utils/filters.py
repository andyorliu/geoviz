"""
Filter utilities for the dashboard
Handles data filtering based on user selections
"""

import pandas as pd
import numpy as np
from datetime import datetime

def filter_by_date_range(df, start_date, end_date, date_col='DATE OCC'):
    """Filter dataframe by date range"""
    if df is None or df.empty:
        return df
    
    if date_col not in df.columns:
        return df
    
    # Convert to datetime if needed
    if not pd.api.types.is_datetime64_any_dtype(df[date_col]):
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    
    if start_date:
        if isinstance(start_date, str):
            start_date = pd.to_datetime(start_date)
        df = df[df[date_col] >= start_date]
    
    if end_date:
        if isinstance(end_date, str):
            end_date = pd.to_datetime(end_date)
        df = df[df[date_col] <= end_date]
    
    return df

def filter_by_crime_types(df, crime_types, crime_col='Crm Cd Desc'):
    """Filter dataframe by crime types"""
    if df is None or df.empty:
        return df
    
    if not crime_types or len(crime_types) == 0:
        return df
    
    if crime_col not in df.columns:
        return df
    
    return df[df[crime_col].isin(crime_types)]

def filter_by_areas(df, areas, area_col='AREA NAME'):
    """Filter dataframe by areas"""
    if df is None or df.empty:
        return df
    
    if not areas or len(areas) == 0:
        return df
    
    if area_col not in df.columns:
        return df
    
    return df[df[area_col].isin(areas)]

def filter_by_time_of_day(df, hour_range, hour_col='Hour'):
    """Filter dataframe by hour range"""
    if df is None or df.empty:
        return df
    
    if hour_range is None or len(hour_range) != 2:
        return df
    
    if hour_col not in df.columns:
        return df
    
    start_hour, end_hour = hour_range
    return df[(df[hour_col] >= start_hour) & (df[hour_col] <= end_hour)]

def filter_by_day_of_week(df, days, day_col='DayOfWeekNum'):
    """Filter dataframe by days of week (0=Monday, 6=Sunday)"""
    if df is None or df.empty:
        return df
    
    if not days or len(days) == 0:
        return df
    
    if day_col not in df.columns:
        return df
    
    return df[df[day_col].isin(days)]

def filter_by_season(df, seasons, season_col='Season'):
    """Filter dataframe by seasons"""
    if df is None or df.empty:
        return df
    
    if not seasons or len(seasons) == 0:
        return df
    
    if season_col not in df.columns:
        return df
    
    return df[df[season_col].isin(seasons)]

def apply_all_filters(df, filters):
    """
    Apply all filters to dataframe
    
    filters dict should contain:
    - date_range: (start_date, end_date)
    - crime_types: list of crime type strings
    - areas: list of area names
    - hour_range: (start_hour, end_hour)
    - days_of_week: list of day numbers (0-6)
    - seasons: list of season strings
    """
    if df is None or df.empty:
        return df
    
    filtered_df = df.copy()
    
    # Date range filter
    if 'date_range' in filters and filters['date_range']:
        start_date, end_date = filters['date_range']
        filtered_df = filter_by_date_range(filtered_df, start_date, end_date)
    
    # Crime types filter
    if 'crime_types' in filters and filters['crime_types']:
        filtered_df = filter_by_crime_types(filtered_df, filters['crime_types'])
    
    # Areas filter
    if 'areas' in filters and filters['areas']:
        filtered_df = filter_by_areas(filtered_df, filters['areas'])
    
    # Time of day filter
    if 'hour_range' in filters and filters['hour_range']:
        filtered_df = filter_by_time_of_day(filtered_df, filters['hour_range'])
    
    # Day of week filter
    if 'days_of_week' in filters and filters['days_of_week']:
        filtered_df = filter_by_day_of_week(filtered_df, filters['days_of_week'])
    
    # Season filter
    if 'seasons' in filters and filters['seasons']:
        filtered_df = filter_by_season(filtered_df, filters['seasons'])
    
    return filtered_df

def get_spatial_bounds(df):
    """Get spatial bounds of filtered data"""
    if df is None or df.empty:
        return None
    
    if 'LAT' not in df.columns or 'LON' not in df.columns:
        return None
    
    valid_coords = df[(df['LAT'].notna()) & (df['LON'].notna())]
    
    if valid_coords.empty:
        return None
    
    return {
        'lat_min': valid_coords['LAT'].min(),
        'lat_max': valid_coords['LAT'].max(),
        'lon_min': valid_coords['LON'].min(),
        'lon_max': valid_coords['LON'].max(),
        'center_lat': valid_coords['LAT'].mean(),
        'center_lon': valid_coords['LON'].mean()
    }

