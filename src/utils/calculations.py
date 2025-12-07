"""
Calculation utilities for the dashboard
Provides statistical and analytical functions
"""

import pandas as pd
import numpy as np
from scipy import stats
from sklearn.cluster import DBSCAN

def calculate_crime_rate(df, population=None):
    """Calculate crime rate per capita if population data available"""
    if df is None or df.empty:
        return 0
    
    total_crimes = len(df)
    
    if population:
        return (total_crimes / population) * 100000  # Per 100k
    return total_crimes

def calculate_trend(df, date_col='DATE OCC', value_col='DR_NO'):
    """Calculate trend (increasing/decreasing) over time"""
    if df is None or df.empty or date_col not in df.columns:
        return None
    
    # Group by date and count
    if value_col in df.columns:
        daily_counts = df.groupby(date_col)[value_col].count()
    else:
        daily_counts = df.groupby(date_col).size()
    
    if len(daily_counts) < 2:
        return None
    
    # Calculate linear trend
    x = np.arange(len(daily_counts))
    y = daily_counts.values
    
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    
    return {
        'slope': slope,
        'r_squared': r_value ** 2,
        'p_value': p_value,
        'trend': 'increasing' if slope > 0 else 'decreasing',
        'strength': 'strong' if abs(r_value) > 0.7 else 'moderate' if abs(r_value) > 0.4 else 'weak'
    }

def detect_hotspots(df, lat_col='LAT', lon_col='LON', min_samples=10, eps=0.01):
    """Detect crime hotspots using DBSCAN clustering"""
    if df is None or df.empty:
        return None
    
    if lat_col not in df.columns or lon_col not in df.columns:
        return None
    
    # Get valid coordinates
    valid_coords = df[[lat_col, lon_col]].dropna()
    
    if len(valid_coords) < min_samples:
        return None
    
    # Apply DBSCAN clustering
    coords = valid_coords.values
    clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(coords)
    
    # Get cluster labels
    valid_coords = valid_coords.copy()
    valid_coords['cluster'] = clustering.labels_
    
    # Calculate hotspot centers and counts
    hotspots = []
    for cluster_id in range(valid_coords['cluster'].max() + 1):
        cluster_points = valid_coords[valid_coords['cluster'] == cluster_id]
        hotspots.append({
            'lat': cluster_points[lat_col].mean(),
            'lon': cluster_points[lon_col].mean(),
            'count': len(cluster_points),
            'cluster_id': cluster_id
        })
    
    # Sort by count (descending)
    hotspots.sort(key=lambda x: x['count'], reverse=True)
    
    return hotspots

def calculate_correlation_between_areas(df, area_col='AREA NAME', date_col='DATE OCC'):
    """Calculate correlation matrix between areas over time"""
    if df is None or df.empty:
        return None
    
    if area_col not in df.columns or date_col not in df.columns:
        return None
    
    # Create time series for each area
    df_copy = df.copy()
    if not pd.api.types.is_datetime64_any_dtype(df_copy[date_col]):
        df_copy[date_col] = pd.to_datetime(df_copy[date_col], errors='coerce')
    
    df_copy['YearMonth'] = df_copy[date_col].dt.to_period('M').astype(str)
    
    # Count crimes by area and month
    area_monthly = df_copy.groupby([area_col, 'YearMonth']).size().reset_index(name='Count')
    
    # Pivot to create time series matrix
    area_matrix = area_monthly.pivot(index='YearMonth', columns=area_col, values='Count').fillna(0)
    
    # Calculate correlation
    correlation_matrix = area_matrix.corr()
    
    return correlation_matrix

def calculate_displacement_metrics(df, area_col='AREA NAME', date_col='DATE OCC', 
                                   period1_start=None, period1_end=None,
                                   period2_start=None, period2_end=None):
    """Calculate crime displacement between two time periods"""
    if df is None or df.empty:
        return None
    
    if not all([period1_start, period1_end, period2_start, period2_end]):
        return None
    
    # Convert dates
    period1_start = pd.to_datetime(period1_start)
    period1_end = pd.to_datetime(period1_end)
    period2_start = pd.to_datetime(period2_start)
    period2_end = pd.to_datetime(period2_end)
    
    # Filter by periods
    period1 = df[(df[date_col] >= period1_start) & (df[date_col] <= period1_end)]
    period2 = df[(df[date_col] >= period2_start) & (df[date_col] <= period2_end)]
    
    # Count by area
    period1_counts = period1.groupby(area_col).size()
    period2_counts = period2.groupby(area_col).size()
    
    # Calculate change
    all_areas = set(period1_counts.index) | set(period2_counts.index)
    displacement = []
    
    for area in all_areas:
        count1 = period1_counts.get(area, 0)
        count2 = period2_counts.get(area, 0)
        change = count2 - count1
        change_pct = (change / count1 * 100) if count1 > 0 else 0
        
        displacement.append({
            'area': area,
            'period1_count': count1,
            'period2_count': count2,
            'change': change,
            'change_pct': change_pct
        })
    
    return pd.DataFrame(displacement)

def aggregate_by_dimensions(df, dimensions, agg_func='count'):
    """
    Aggregate data by multiple dimensions
    
    dimensions: list of column names to group by
    agg_func: aggregation function ('count', 'sum', 'mean', etc.)
    """
    if df is None or df.empty:
        return None
    
    # Check all dimensions exist
    missing_dims = [d for d in dimensions if d not in df.columns]
    if missing_dims:
        return None
    
    # Group by dimensions
    grouped = df.groupby(dimensions)
    
    # Apply aggregation
    if agg_func == 'count':
        result = grouped.size().reset_index(name='Count')
    elif agg_func == 'sum':
        # Need a numeric column to sum
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            result = grouped[numeric_cols[0]].sum().reset_index(name='Sum')
        else:
            result = grouped.size().reset_index(name='Count')
    elif agg_func == 'mean':
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            result = grouped[numeric_cols[0]].mean().reset_index(name='Mean')
        else:
            result = grouped.size().reset_index(name='Count')
    else:
        result = grouped.size().reset_index(name='Count')
    
    return result

def calculate_top_n(df, group_col, n=10, value_col=None):
    """Calculate top N items by count or value"""
    if df is None or df.empty:
        return None
    
    if group_col not in df.columns:
        return None
    
    if value_col and value_col in df.columns:
        # Group and sum
        grouped = df.groupby(group_col)[value_col].sum().sort_values(ascending=False)
    else:
        # Group and count
        grouped = df.groupby(group_col).size().sort_values(ascending=False)
    
    return grouped.head(n).reset_index()

