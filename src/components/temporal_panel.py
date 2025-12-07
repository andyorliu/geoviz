"""
Temporal analysis panel component
Handles time series and temporal pattern visualizations
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

def create_time_series(df, date_col='DATE OCC', aggregation='daily'):
    """Create time series chart"""
    if df is None or df.empty or date_col not in df.columns:
        return go.Figure()
    
    df_copy = df.copy()
    df_copy[date_col] = pd.to_datetime(df_copy[date_col], errors='coerce')
    df_copy = df_copy[df_copy[date_col].notna()]
    
    if df_copy.empty:
        return go.Figure()
    
    if aggregation == 'daily':
        df_copy['Date'] = df_copy[date_col].dt.date
        time_series = df_copy.groupby('Date').size().reset_index(name='Count')
        time_series.columns = ['Date', 'Count']
        time_series['Date'] = pd.to_datetime(time_series['Date'])
    elif aggregation == 'weekly':
        df_copy['YearWeek'] = df_copy[date_col].dt.to_period('W').astype(str)
        time_series = df_copy.groupby('YearWeek').size().reset_index(name='Count')
        time_series.columns = ['Period', 'Count']
    elif aggregation == 'monthly':
        df_copy['YearMonth'] = df_copy[date_col].dt.to_period('M').astype(str)
        time_series = df_copy.groupby('YearMonth').size().reset_index(name='Count')
        time_series.columns = ['Period', 'Count']
    else:
        return go.Figure()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=time_series.iloc[:, 0],
        y=time_series['Count'],
        mode='lines+markers',
        name='Crime Count',
        line=dict(color='#1f77b4', width=2),
        marker=dict(size=4)
    ))
    
    fig.update_layout(
        title=f'Crime Trends Over Time ({aggregation.title()})',
        xaxis_title='Date' if aggregation == 'daily' else 'Period',
        yaxis_title='Number of Crimes',
        hovermode='x unified',
        height=300,
        showlegend=False
    )
    
    return fig

def create_hourly_heatmap(df, hour_col='Hour', day_col='DayOfWeekNum'):
    """Create hourly heatmap (24 hours x 7 days)"""
    if df is None or df.empty:
        return go.Figure()
    
    if hour_col not in df.columns or day_col not in df.columns:
        return go.Figure()
    
    # Create heatmap data
    heatmap_data = df.groupby([day_col, hour_col]).size().reset_index(name='Count')
    
    # Pivot for heatmap
    pivot_data = heatmap_data.pivot(index=day_col, columns=hour_col, values='Count').fillna(0)
    
    # Ensure all hours (0-23) and days (0-6) are present
    for day in range(7):
        if day not in pivot_data.index:
            pivot_data.loc[day] = 0
    for hour in range(24):
        if hour not in pivot_data.columns:
            pivot_data[hour] = 0
    
    pivot_data = pivot_data.sort_index()
    pivot_data = pivot_data.reindex(columns=sorted(pivot_data.columns))
    
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_labels = [days[i] for i in pivot_data.index]
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot_data.values,
        x=[f"{h:02d}:00" for h in pivot_data.columns],
        y=day_labels,
        colorscale='Reds',
        showscale=True,
        colorbar=dict(title="Number of<br>Crimes", titleside="right"),
        hovertemplate='Day: %{y}<br>Hour: %{x}<br>Count: %{z}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Crime by Hour and Day of Week',
        xaxis_title='Hour of Day',
        yaxis_title='Day of Week',
        height=300
    )
    
    return fig

def create_calendar_heatmap(df, date_col='DATE OCC'):
    """Create calendar heatmap (day of year)"""
    if df is None or df.empty or date_col not in df.columns:
        return go.Figure()
    
    df_copy = df.copy()
    df_copy[date_col] = pd.to_datetime(df_copy[date_col], errors='coerce')
    df_copy = df_copy[df_copy[date_col].notna()]
    
    if df_copy.empty:
        return go.Figure()
    
    # Extract year, month, day
    df_copy['Year'] = df_copy[date_col].dt.year
    df_copy['Month'] = df_copy[date_col].dt.month
    df_copy['Day'] = df_copy[date_col].dt.day
    
    # Group by year, month, day
    daily_counts = df_copy.groupby(['Year', 'Month', 'Day']).size().reset_index(name='Count')
    
    # Create a more detailed visualization would require more complex logic
    # For now, create a monthly aggregation
    monthly_counts = df_copy.groupby(['Year', 'Month']).size().reset_index(name='Count')
    monthly_counts['YearMonth'] = monthly_counts['Year'].astype(str) + '-' + monthly_counts['Month'].astype(str).str.zfill(2)
    
    fig = go.Figure(data=go.Bar(
        x=monthly_counts['YearMonth'],
        y=monthly_counts['Count'],
        marker=dict(color='#2ca02c')
    ))
    
    fig.update_layout(
        title='Crime Count by Month',
        xaxis_title='Month',
        yaxis_title='Number of Crimes',
        xaxis_tickangle=-45,
        height=300
    )
    
    return fig

def create_trend_comparison(df, area_col='AREA NAME', date_col='DATE OCC', areas=None):
    """Create trend comparison across multiple areas"""
    if df is None or df.empty:
        return go.Figure()
    
    if area_col not in df.columns or date_col not in df.columns:
        return go.Figure()
    
    df_copy = df.copy()
    df_copy[date_col] = pd.to_datetime(df_copy[date_col], errors='coerce')
    
    if areas:
        df_copy = df_copy[df_copy[area_col].isin(areas)]
    
    if df_copy.empty:
        return go.Figure()
    
    # Monthly aggregation by area
    df_copy['YearMonth'] = df_copy[date_col].dt.to_period('M').astype(str)
    monthly_area = df_copy.groupby(['YearMonth', area_col]).size().reset_index(name='Count')
    
    fig = go.Figure()
    
    for area in monthly_area[area_col].unique()[:10]:  # Limit to top 10 areas
        area_data = monthly_area[monthly_area[area_col] == area]
        fig.add_trace(go.Scatter(
            x=area_data['YearMonth'],
            y=area_data['Count'],
            mode='lines+markers',
            name=area
        ))
    
    fig.update_layout(
        title='Crime Trends by Area',
        xaxis_title='Month',
        yaxis_title='Number of Crimes',
        xaxis_tickangle=-45,
        height=400,
        hovermode='x unified'
    )
    
    return fig

