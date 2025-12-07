"""
Crime type distribution panel component
Handles crime type visualizations and distributions
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def create_crime_type_bar(df, crime_col='Crm Cd Desc', top_n=10):
    """Create horizontal bar chart of top crime types"""
    if df is None or df.empty or crime_col not in df.columns:
        return go.Figure()
    
    top_crimes = df[crime_col].value_counts().head(top_n)
    
    fig = go.Figure(data=go.Bar(
        x=top_crimes.values,
        y=top_crimes.index,
        orientation='h',
        marker=dict(color='#ff7f0e')
    ))
    
    fig.update_layout(
        title=f'Top {top_n} Crime Types',
        xaxis_title='Number of Crimes',
        yaxis_title='Crime Type',
        height=300,
        yaxis={'categoryorder': 'total ascending'}
    )
    
    return fig

def create_part1_part2_pie(df, part_col='Part 1-2'):
    """Create pie chart for Part 1 vs Part 2 crimes"""
    if df is None or df.empty or part_col not in df.columns:
        return go.Figure()
    
    part_counts = df[part_col].value_counts()
    
    labels = []
    values = []
    for idx in sorted(part_counts.index):
        labels.append('Part 1' if idx == 1 else 'Part 2')
        values.append(part_counts[idx])
    
    fig = go.Figure(data=go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        marker=dict(colors=['#1f77b4', '#ff7f0e'])
    ))
    
    fig.update_layout(
        title='Part 1 vs Part 2 Crimes',
        height=300,
        showlegend=True
    )
    
    return fig

def create_crime_type_sunburst(df, crime_col='Crm Cd Desc', area_col='AREA NAME', top_n=20):
    """Create sunburst chart for crime type hierarchy"""
    if df is None or df.empty:
        return go.Figure()
    
    if crime_col not in df.columns:
        return go.Figure()
    
    # Get top crime types
    top_crimes = df[crime_col].value_counts().head(top_n).index.tolist()
    df_filtered = df[df[crime_col].isin(top_crimes)]
    
    if area_col in df_filtered.columns:
        # Create hierarchy: Area -> Crime Type
        hierarchy_data = df_filtered.groupby([area_col, crime_col]).size().reset_index(name='Count')
        
        fig = go.Figure(go.Sunburst(
            labels=hierarchy_data[area_col].tolist() + hierarchy_data[crime_col].tolist(),
            parents=[''] * len(hierarchy_data) + hierarchy_data[area_col].tolist(),
            values=hierarchy_data['Count'].tolist() * 2,
            branchvalues="total"
        ))
    else:
        # Simple sunburst with just crime types
        crime_counts = df_filtered[crime_col].value_counts()
        fig = go.Figure(go.Sunburst(
            labels=crime_counts.index.tolist(),
            parents=[''] * len(crime_counts),
            values=crime_counts.values.tolist()
        ))
    
    fig.update_layout(
        title='Crime Type Distribution (Sunburst)',
        height=400
    )
    
    return fig

def create_crime_type_by_area(df, crime_col='Crm Cd Desc', area_col='AREA NAME', top_crimes=5, top_areas=10):
    """Create grouped bar chart showing crime types by area"""
    if df is None or df.empty:
        return go.Figure()
    
    if crime_col not in df.columns or area_col not in df.columns:
        return go.Figure()
    
    # Get top crimes and areas
    top_crime_list = df[crime_col].value_counts().head(top_crimes).index.tolist()
    top_area_list = df[area_col].value_counts().head(top_areas).index.tolist()
    
    df_filtered = df[
        (df[crime_col].isin(top_crime_list)) & 
        (df[area_col].isin(top_area_list))
    ]
    
    # Create grouped data
    grouped = df_filtered.groupby([area_col, crime_col]).size().reset_index(name='Count')
    
    fig = go.Figure()
    
    for crime in top_crime_list:
        crime_data = grouped[grouped[crime_col] == crime]
        fig.add_trace(go.Bar(
            name=crime[:30] + '...' if len(crime) > 30 else crime,
            x=crime_data[area_col],
            y=crime_data['Count']
        ))
    
    fig.update_layout(
        title=f'Top {top_crimes} Crime Types by Top {top_areas} Areas',
        xaxis_title='Area',
        yaxis_title='Number of Crimes',
        barmode='group',
        xaxis_tickangle=-45,
        height=400,
        legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.02)
    )
    
    return fig

