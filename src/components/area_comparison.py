"""
Area comparison panel component
Handles area comparison visualizations
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

def create_area_comparison_bar(df, area_col='AREA NAME', top_n=15):
    """Create bar chart comparing areas"""
    if df is None or df.empty or area_col not in df.columns:
        return go.Figure()
    
    area_counts = df[area_col].value_counts().head(top_n)
    
    fig = go.Figure(data=go.Bar(
        x=area_counts.index,
        y=area_counts.values,
        marker=dict(color='#2ca02c')
    ))
    
    fig.update_layout(
        title=f'Crime Count by Area (Top {top_n})',
        xaxis_title='Area',
        yaxis_title='Number of Crimes',
        xaxis_tickangle=-45,
        height=400
    )
    
    return fig

def create_area_radar_chart(df, area_col='AREA NAME', areas=None, metrics=None):
    """Create radar/spider chart for multi-dimensional area comparison"""
    if df is None or df.empty or area_col not in df.columns:
        return go.Figure()
    
    if areas is None:
        # Get top areas by count
        top_areas = df[area_col].value_counts().head(5).index.tolist()
    else:
        top_areas = areas[:5]  # Limit to 5 for readability
    
    if metrics is None:
        # Default metrics: total crimes, crime types, avg hour, etc.
        metrics = {}
    
    # Calculate metrics for each area
    radar_data = []
    for area in top_areas:
        area_df = df[df[area_col] == area]
        
        metrics_dict = {
            'Total Crimes': len(area_df),
            'Crime Types': area_df['Crm Cd Desc'].nunique() if 'Crm Cd Desc' in area_df.columns else 0,
            'Avg Hour': area_df['Hour'].mean() if 'Hour' in area_df.columns else 0
        }
        
        # Normalize metrics to 0-100 scale for radar chart
        max_values = {
            'Total Crimes': df[area_col].value_counts().max(),
            'Crime Types': df['Crm Cd Desc'].nunique() if 'Crm Cd Desc' in df.columns else 1,
            'Avg Hour': 23
        }
        
        normalized = {k: (v / max_values[k] * 100) if max_values[k] > 0 else 0 
                     for k, v in metrics_dict.items()}
        
        radar_data.append({
            'area': area,
            **normalized
        })
    
    if not radar_data:
        return go.Figure()
    
    fig = go.Figure()
    
    categories = list(radar_data[0].keys())
    categories.remove('area')
    
    for data in radar_data:
        values = [data[cat] for cat in categories]
        fig.add_trace(go.Scatterpolar(
            r=values + [values[0]],  # Close the loop
            theta=categories + [categories[0]],
            fill='toself',
            name=data['area']
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        title='Multi-Dimensional Area Comparison',
        height=400,
        showlegend=True
    )
    
    return fig

def create_area_small_multiples(df, area_col='AREA NAME', date_col='DATE OCC', areas=None, n_areas=6):
    """Create small multiples for area comparison"""
    if df is None or df.empty:
        return go.Figure()
    
    if area_col not in df.columns or date_col not in df.columns:
        return go.Figure()
    
    if areas is None:
        top_areas = df[area_col].value_counts().head(n_areas).index.tolist()
    else:
        top_areas = areas[:n_areas]
    
    df_copy = df.copy()
    df_copy[date_col] = pd.to_datetime(df_copy[date_col], errors='coerce')
    df_copy = df_copy[df_copy[area_col].isin(top_areas)]
    
    if df_copy.empty:
        return go.Figure()
    
    # Monthly aggregation
    df_copy['YearMonth'] = df_copy[date_col].dt.to_period('M').astype(str)
    monthly_area = df_copy.groupby(['YearMonth', area_col]).size().reset_index(name='Count')
    
    # Create subplots
    try:
        from plotly.subplots import make_subplots
    except ImportError:
        # Fallback if subplots not available
        return go.Figure()
    
    n_cols = 3
    n_rows = (len(top_areas) + n_cols - 1) // n_cols
    
    fig = make_subplots(
        rows=n_rows, cols=n_cols,
        subplot_titles=top_areas,
        vertical_spacing=0.1,
        horizontal_spacing=0.1
    )
    
    for idx, area in enumerate(top_areas):
        row = (idx // n_cols) + 1
        col = (idx % n_cols) + 1
        
        area_data = monthly_area[monthly_area[area_col] == area]
        
        fig.add_trace(
            go.Scatter(
                x=area_data['YearMonth'],
                y=area_data['Count'],
                mode='lines+markers',
                name=area,
                showlegend=False
            ),
            row=row, col=col
        )
    
    fig.update_layout(
        title_text='Crime Trends by Area (Small Multiples)',
        height=400 * n_rows,
        showlegend=False
    )
    
    fig.update_xaxes(tickangle=-45)
    
    return fig

def create_area_correlation_heatmap(df, area_col='AREA NAME', date_col='DATE OCC', top_n=15):
    """Create correlation heatmap between areas"""
    if df is None or df.empty:
        return go.Figure()
    
    if area_col not in df.columns or date_col not in df.columns:
        return go.Figure()
    
    df_copy = df.copy()
    df_copy[date_col] = pd.to_datetime(df_copy[date_col], errors='coerce')
    
    # Get top areas
    top_areas = df_copy[area_col].value_counts().head(top_n).index.tolist()
    df_filtered = df_copy[df_copy[area_col].isin(top_areas)]
    
    # Monthly aggregation
    df_filtered['YearMonth'] = df_filtered[date_col].dt.to_period('M').astype(str)
    monthly_area = df_filtered.groupby(['YearMonth', area_col]).size().reset_index(name='Count')
    
    # Pivot for correlation
    area_matrix = monthly_area.pivot(index='YearMonth', columns=area_col, values='Count').fillna(0)
    
    # Calculate correlation
    correlation_matrix = area_matrix.corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=correlation_matrix.values,
        x=correlation_matrix.columns,
        y=correlation_matrix.index,
        colorscale='RdBu',
        zmid=0,
        showscale=True,
        colorbar=dict(title="Correlation<br>Coefficient", titleside="right"),
        hovertemplate='%{x} vs %{y}<br>Correlation: %{z:.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Area Correlation Matrix',
        xaxis_title='Area',
        yaxis_title='Area',
        xaxis_tickangle=-45,
        height=500
    )
    
    return fig

