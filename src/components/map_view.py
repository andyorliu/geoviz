"""
Map view component for the dashboard
Handles interactive map visualizations
"""

import plotly.graph_objects as go
import pandas as pd
import numpy as np

def create_map_heatmap(df, center_lat=None, center_lon=None):
    """Create heatmap visualization"""
    if df is None or df.empty:
        return go.Figure()
    
    valid_df = df[(df['LAT'].notna()) & (df['LON'].notna())]
    
    if valid_df.empty:
        return go.Figure()
    
    # Sample for performance
    if len(valid_df) > 10000:
        valid_df = valid_df.sample(n=10000, random_state=42)
    
    if center_lat is None:
        center_lat = valid_df['LAT'].mean()
    if center_lon is None:
        center_lon = valid_df['LON'].mean()
    
    fig = go.Figure()
    
    fig.add_trace(go.Densitymapbox(
        lat=valid_df['LAT'],
        lon=valid_df['LON'],
        z=[1] * len(valid_df),
        radius=10,
        colorscale='Reds',
        showscale=True,
        colorbar=dict(title="Crime Density<br>(Relative Intensity)", titleside="right"),
        below=''
    ))
    
    fig.update_layout(
        mapbox=dict(
            style='open-street-map',
            center=dict(lat=center_lat, lon=center_lon),
            zoom=10
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        height=600
    )
    
    return fig

def create_map_clusters(df, center_lat=None, center_lon=None):
    """Create clustered markers visualization"""
    if df is None or df.empty:
        return go.Figure()
    
    valid_df = df[(df['LAT'].notna()) & (df['LON'].notna())]
    
    if valid_df.empty:
        return go.Figure()
    
    # Sample for performance
    if len(valid_df) > 5000:
        valid_df = valid_df.sample(n=5000, random_state=42)
    
    if center_lat is None:
        center_lat = valid_df['LAT'].mean()
    if center_lon is None:
        center_lon = valid_df['LON'].mean()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scattermapbox(
        lat=valid_df['LAT'],
        lon=valid_df['LON'],
        mode='markers',
        marker=dict(size=5, color='red', opacity=0.6),
        text=valid_df.get('Crm Cd Desc', ''),
        hovertemplate='<b>%{text}</b><br>Lat: %{lat:.4f}<br>Lon: %{lon:.4f}<extra></extra>'
    ))
    
    fig.update_layout(
        mapbox=dict(
            style='open-street-map',
            center=dict(lat=center_lat, lon=center_lon),
            zoom=10
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        height=600
    )
    
    return fig

def create_map_points(df, center_lat=None, center_lon=None):
    """Create individual points visualization"""
    if df is None or df.empty:
        return go.Figure()
    
    valid_df = df[(df['LAT'].notna()) & (df['LON'].notna())]
    
    if valid_df.empty:
        return go.Figure()
    
    # Sample for performance
    if len(valid_df) > 3000:
        valid_df = valid_df.sample(n=3000, random_state=42)
    
    if center_lat is None:
        center_lat = valid_df['LAT'].mean()
    if center_lon is None:
        center_lon = valid_df['LON'].mean()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scattermapbox(
        lat=valid_df['LAT'],
        lon=valid_df['LON'],
        mode='markers',
        marker=dict(size=3, color='red', opacity=0.5),
        text=valid_df.get('Crm Cd Desc', ''),
        hovertemplate='<b>%{text}</b><br>Lat: %{lat:.4f}<br>Lon: %{lon:.4f}<extra></extra>'
    ))
    
    fig.update_layout(
        mapbox=dict(
            style='open-street-map',
            center=dict(lat=center_lat, lon=center_lon),
            zoom=10
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        height=600
    )
    
    return fig

def create_temporal_map(df, time_period_col, center_lat=None, center_lon=None):
    """Create animated temporal map for Task 5 (displacement analysis)"""
    if df is None or df.empty:
        return go.Figure()
    
    if time_period_col not in df.columns or 'AREA NAME' not in df.columns:
        return go.Figure()
    
    # Data is already aggregated, so use it directly
    period_agg = df.copy()
    
    # Ensure we have valid coordinates
    if 'LAT' not in period_agg.columns or 'LON' not in period_agg.columns:
        return go.Figure()
    
    valid_df = period_agg[(period_agg['LAT'].notna()) & (period_agg['LON'].notna())]
    
    if valid_df.empty:
        return go.Figure()
    
    if center_lat is None:
        center_lat = valid_df['LAT'].mean()
    if center_lon is None:
        center_lon = valid_df['LON'].mean()
    
    # Get count column (may be named differently)
    count_col = 'Count' if 'Count' in valid_df.columns else 'Total_Crimes' if 'Total_Crimes' in valid_df.columns else valid_df.columns[-1]
    
    # Create frames for animation
    frames = []
    time_periods = sorted(valid_df[time_period_col].unique())
    
    if len(time_periods) == 0:
        return go.Figure()
    
    max_count = valid_df[count_col].max() if valid_df[count_col].max() > 0 else 1
    
    for period in time_periods:
        period_data = valid_df[valid_df[time_period_col] == period]
        if period_data.empty:
            continue
        
        frames.append(go.Frame(
            data=[go.Scattermapbox(
                lat=period_data['LAT'],
                lon=period_data['LON'],
                mode='markers',
                marker=dict(
                    size=(period_data[count_col] / max_count * 20).clip(lower=5, upper=30),
                    color=period_data[count_col],
                    colorscale='Reds',
                    showscale=True,
                    colorbar=dict(title="Number of<br>Crimes", titleside="right"),
                    opacity=0.7,
                    cmin=0,
                    cmax=max_count
                ),
                text=period_data['AREA NAME'] + '<br>Count: ' + period_data[count_col].astype(str),
                hovertemplate='<b>%{text}</b><br>Lat: %{lat:.4f}<br>Lon: %{lon:.4f}<extra></extra>'
            )],
            name=str(period)
        ))
    
    if not frames:
        return go.Figure()
    
    # Initial data (first period)
    initial_data = valid_df[valid_df[time_period_col] == time_periods[0]]
    
    fig = go.Figure(
        data=[go.Scattermapbox(
            lat=initial_data['LAT'],
            lon=initial_data['LON'],
            mode='markers',
            marker=dict(
                size=(initial_data[count_col] / max_count * 20).clip(lower=5, upper=30),
                color=initial_data[count_col],
                colorscale='Reds',
                showscale=True,
                colorbar=dict(title="Number of<br>Crimes", titleside="right"),
                opacity=0.7,
                cmin=0,
                cmax=max_count
            ),
            text=initial_data['AREA NAME'] + '<br>Count: ' + initial_data[count_col].astype(str),
            hovertemplate='<b>%{text}</b><br>Lat: %{lat:.4f}<br>Lon: %{lon:.4f}<extra></extra>'
        )],
        frames=frames
    )
    
    # Add animation controls
    fig.update_layout(
        updatemenus=[{
            'type': 'buttons',
            'showactive': False,
            'buttons': [
                {
                    'label': 'Play',
                    'method': 'animate',
                    'args': [None, {
                        'frame': {'duration': 500, 'redraw': True},
                        'fromcurrent': True
                    }]
                },
                {
                    'label': 'Pause',
                    'method': 'animate',
                    'args': [[None], {
                        'frame': {'duration': 0, 'redraw': False},
                        'mode': 'immediate',
                        'transition': {'duration': 0}
                    }]
                }
            ]
        }],
        sliders=[{
            'active': 0,
            'steps': [{
                'args': [[str(period)],
                         {'frame': {'duration': 300, 'redraw': True},
                          'mode': 'immediate',
                          'transition': {'duration': 300}}],
                'label': str(period),
                'method': 'animate'
            } for period in time_periods]
        }],
        mapbox=dict(
            style='open-street-map',
            center=dict(lat=center_lat, lon=center_lon),
            zoom=10
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        height=600
    )
    
    return fig

