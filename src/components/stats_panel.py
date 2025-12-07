"""
Statistical summary panel component
Handles statistics and summary visualizations
"""

import plotly.graph_objects as go
import pandas as pd
import numpy as np
from utils.calculations import calculate_trend, calculate_crime_rate

def create_stats_cards(df):
    """Create statistics cards HTML"""
    if df is None or df.empty:
        return "No data available"
    
    try:
        from dash import html
        import dash_bootstrap_components as dbc
    except ImportError:
        return "Dash components not available"
    
    total_crimes = len(df)
    
    # Calculate trend
    trend_text = "N/A"
    trend_color = "secondary"
    if 'DATE OCC' in df.columns:
        df_copy = df.copy()
        df_copy['DATE OCC'] = pd.to_datetime(df_copy['DATE OCC'], errors='coerce')
        trend = calculate_trend(df_copy)
        if trend:
            trend_text = f"{trend['trend'].title()} ({trend['strength']})"
            trend_color = "danger" if trend['trend'] == 'increasing' else "success"
    
    unique_areas = df['AREA NAME'].nunique() if 'AREA NAME' in df.columns else 0
    unique_crime_types = df['Crm Cd Desc'].nunique() if 'Crm Cd Desc' in df.columns else 0
    
    # Calculate average crimes per day
    if 'DATE OCC' in df.columns:
        df_copy = df.copy()
        df_copy['DATE OCC'] = pd.to_datetime(df_copy['DATE OCC'], errors='coerce')
        date_range = (df_copy['DATE OCC'].max() - df_copy['DATE OCC'].min()).days
        avg_per_day = total_crimes / date_range if date_range > 0 else 0
    else:
        avg_per_day = 0
    
    return html.Div([
        dbc.Card([
            dbc.CardBody([
                html.H4(f"{total_crimes:,}", className="text-primary"),
                html.P("Total Crimes", className="text-muted mb-0")
            ])
        ], className="mb-2"),
        dbc.Card([
            dbc.CardBody([
                html.H4(trend_text, className=f"text-{trend_color}"),
                html.P("Trend", className="text-muted mb-0")
            ])
        ], className="mb-2"),
        dbc.Card([
            dbc.CardBody([
                html.H4(f"{unique_areas}", className="text-success"),
                html.P("Areas", className="text-muted mb-0")
            ])
        ], className="mb-2"),
        dbc.Card([
            dbc.CardBody([
                html.H4(f"{unique_crime_types}", className="text-warning"),
                html.P("Crime Types", className="text-muted mb-0")
            ])
        ], className="mb-2"),
        dbc.Card([
            dbc.CardBody([
                html.H4(f"{avg_per_day:.1f}", className="text-info"),
                html.P("Avg Crimes/Day", className="text-muted mb-0")
            ])
        ])
    ])

def create_correlation_heatmap(df, numeric_cols=None):
    """Create correlation heatmap for numeric columns"""
    if df is None or df.empty:
        return go.Figure()
    
    if numeric_cols is None:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if not numeric_cols:
        return go.Figure()
    
    # Calculate correlation
    correlation_matrix = df[numeric_cols].corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=correlation_matrix.values,
        x=correlation_matrix.columns,
        y=correlation_matrix.index,
        colorscale='RdBu',
        zmid=0,
        zmin=-1,
        zmax=1,
        showscale=True,
        hovertemplate='%{x} vs %{y}<br>Correlation: %{z:.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Correlation Matrix',
        xaxis_title='Variable',
        yaxis_title='Variable',
        height=400
    )
    
    return fig

def create_summary_table(df, top_n=10):
    """Create summary statistics table"""
    if df is None or df.empty:
        return go.Figure()
    
    stats = []
    
    # Total crimes
    stats.append({'Metric': 'Total Crimes', 'Value': len(df)})
    
    # Unique areas
    if 'AREA NAME' in df.columns:
        stats.append({'Metric': 'Unique Areas', 'Value': df['AREA NAME'].nunique()})
    
    # Unique crime types
    if 'Crm Cd Desc' in df.columns:
        stats.append({'Metric': 'Unique Crime Types', 'Value': df['Crm Cd Desc'].nunique()})
    
    # Date range
    if 'DATE OCC' in df.columns:
        df_copy = df.copy()
        df_copy['DATE OCC'] = pd.to_datetime(df_copy['DATE OCC'], errors='coerce')
        date_range = (df_copy['DATE OCC'].max() - df_copy['DATE OCC'].min()).days
        stats.append({'Metric': 'Date Range (days)', 'Value': date_range})
    
    # Top area
    if 'AREA NAME' in df.columns:
        top_area = df['AREA NAME'].value_counts().index[0]
        top_area_count = df['AREA NAME'].value_counts().iloc[0]
        stats.append({'Metric': 'Top Area', 'Value': f"{top_area} ({top_area_count:,})"})
    
    # Top crime type
    if 'Crm Cd Desc' in df.columns:
        top_crime = df['Crm Cd Desc'].value_counts().index[0]
        top_crime_count = df['Crm Cd Desc'].value_counts().iloc[0]
        stats.append({'Metric': 'Top Crime Type', 'Value': f"{top_crime[:30]}... ({top_crime_count:,})"})
    
    stats_df = pd.DataFrame(stats)
    
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=list(stats_df.columns),
            fill_color='paleturquoise',
            align='left'
        ),
        cells=dict(
            values=[stats_df[col].tolist() for col in stats_df.columns],
            fill_color='lavender',
            align='left'
        )
    )])
    
    fig.update_layout(
        title='Summary Statistics',
        height=300
    )
    
    return fig

