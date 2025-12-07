"""
Main Dash application for LA Crime Data Visualization Dashboard
"""

import dash
from dash import dcc, html, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, date

# Import utilities
import sys
import os
sys.path.append(os.path.dirname(__file__))

from utils.data_loader import get_data_loader
from utils.filters import apply_all_filters, get_spatial_bounds
from utils.calculations import calculate_trend, detect_hotspots, calculate_top_n

# Import components
from components.map_view import create_map_heatmap, create_map_clusters, create_map_points, create_temporal_map
from components.temporal_panel import create_time_series, create_hourly_heatmap
from components.crime_type_panel import create_crime_type_bar, create_part1_part2_pie
from components.area_comparison import create_area_comparison_bar, create_area_correlation_heatmap
from components.stats_panel import create_stats_cards
from utils.filters import filter_by_time_of_day, filter_by_day_of_week, filter_by_season

# Initialize data loader
print("="*50)
print("Initializing data loader...")
data_loader = get_data_loader()

# Test data loading
print("\nTesting data loading...")
test_data = data_loader.load_cleaned_data(sample=True)
if test_data is not None:
    print(f"✓ Successfully loaded {len(test_data)} rows of data")
    print(f"  Columns: {list(test_data.columns)[:5]}...")
else:
    print("✗ Failed to load data - check file paths")
print("="*50)

# Initialize Dash app with Bootstrap theme
# CSS files in assets/ folder are automatically loaded by Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "LA Crime Data Visualization Dashboard - 2022"

# Get available options
try:
    available_areas = data_loader.get_available_areas()
    available_crime_types = data_loader.get_available_crime_types()[:50]  # Top 50 for performance
    date_range = data_loader.get_date_range()
    print(f"Loaded options: {len(available_areas)} areas, {len(available_crime_types)} crime types")
except Exception as e:
    print(f"Warning: Could not load data options: {e}")
    import traceback
    traceback.print_exc()
    available_areas = []
    available_crime_types = []
    date_range = {'start': '2022-01-01', 'end': '2022-12-31'}

# Define app layout
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.H1("LA Crime Data Visualization Dashboard", className="text-center mb-4"),
            html.P("Interactive exploration of crime data from 2022", 
                   className="text-center text-muted mb-4")
        ])
    ]),
    
    # Global Filters
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Filters", className="card-title"),
                    html.Label("Date Range:", className="mt-2"),
                    dcc.DatePickerRange(
                        id='date-range-picker',
                        start_date=date_range.get('start', '2022-01-01') if date_range else '2022-01-01',
                        end_date=date_range.get('end', '2022-12-31') if date_range else '2022-12-31',
                        display_format='YYYY-MM-DD'
                    ),
                    html.Label("Crime Types:", className="mt-3"),
                    dcc.Dropdown(
                        id='crime-type-filter',
                        options=[{'label': ct, 'value': ct} for ct in available_crime_types],
                        multi=True,
                        placeholder="Select crime types (or leave empty for all)"
                    ),
                    html.Label("Areas:", className="mt-3"),
                    dcc.Dropdown(
                        id='area-filter',
                        options=[{'label': area, 'value': area} for area in available_areas],
                        multi=True,
                        placeholder="Select areas (or leave empty for all)"
                    ),
                    dbc.Button("Apply Filters", id="apply-filters-btn", color="primary", className="mt-3")
                ])
            ])
        ], width=3),
        
        # Main Map View
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        dbc.ButtonGroup([
                            dbc.Button("Heatmap", id="map-type-heatmap", outline=True, color="primary", n_clicks=0, active=True),
                            dbc.Button("Clusters", id="map-type-clusters", outline=True, color="primary", n_clicks=0, active=False),
                            dbc.Button("Points", id="map-type-points", outline=True, color="primary", n_clicks=0, active=False)
                        ], className="mb-2", id="map-type-button-group")
                    ]),
                    dcc.Graph(id='main-map', style={'height': '600px'})
                ])
            ])
        ], width=9)
    ], className="mb-4"),
    
    # Temporal and Crime Type Panels
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Temporal Analysis", className="card-title"),
                    dcc.Graph(id='time-series-chart', style={'height': '300px'}),
                    dcc.Graph(id='hourly-heatmap', style={'height': '300px'})
                ])
            ])
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Crime Type Distribution", className="card-title"),
                    dcc.Graph(id='crime-type-bar', style={'height': '300px'}),
                    dcc.Graph(id='part1-part2-pie', style={'height': '300px'})
                ])
            ])
        ], width=6)
    ], className="mb-4"),
    
    # Area Comparison and Stats
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Area Comparison", className="card-title"),
                    dcc.Graph(id='area-comparison-chart', style={'height': '400px'})
                ])
            ])
        ], width=8),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Statistics", className="card-title"),
                    html.Div(id='stats-cards')
                ])
            ])
        ], width=4)
    ], className="mb-4"),
    
    # Advanced Tasks Section
    dbc.Row([
        dbc.Col([
            html.H2("Advanced Analysis Tasks", className="mt-4 mb-3")
        ])
    ]),
    
    # Task 4: Multi-Dimensional Hotspot Analysis
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Task 4: Multi-Dimensional Hotspot Analysis", className="card-title"),
                    html.P("Identify areas with high crime rates across multiple dimensions (crime type, time, day, season)"),
                    dbc.Row([
                        dbc.Col([
                            html.Label("Time of Day Range:"),
                            dcc.RangeSlider(
                                id='hour-range-slider',
                                min=0, max=23, step=1,
                                marks={i: f"{i}:00" for i in range(0, 24, 4)},
                                value=[0, 23]
                            ),
                            html.Label("Day of Week:", className="mt-3"),
                            dcc.Checklist(
                                id='day-of-week-checklist',
                                options=[
                                    {'label': 'Mon', 'value': 0},
                                    {'label': 'Tue', 'value': 1},
                                    {'label': 'Wed', 'value': 2},
                                    {'label': 'Thu', 'value': 3},
                                    {'label': 'Fri', 'value': 4},
                                    {'label': 'Sat', 'value': 5},
                                    {'label': 'Sun', 'value': 6}
                                ],
                                value=[0, 1, 2, 3, 4, 5, 6],
                                inline=True
                            ),
                            html.Label("Season:", className="mt-3"),
                            dcc.Checklist(
                                id='season-checklist',
                                options=[
                                    {'label': 'Spring', 'value': 'Spring'},
                                    {'label': 'Summer', 'value': 'Summer'},
                                    {'label': 'Fall', 'value': 'Fall'},
                                    {'label': 'Winter', 'value': 'Winter'}
                                ],
                                value=['Spring', 'Summer', 'Fall', 'Winter'],
                                inline=True
                            )
                        ], width=4),
                        dbc.Col([
                            dcc.Graph(id='multi-dim-map', style={'height': '500px'})
                        ], width=8)
                    ])
                ])
            ])
        ])
    ], className="mb-4"),
    
    # Task 5: Crime Displacement Analysis
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Task 5: Seasonal Crime Pattern Analysis", className="card-title"),
                    html.P("Explore how crime patterns change across seasons (Spring, Summer, Fall, Winter) in 2022"),
                    dbc.Row([
                        dbc.Col([
                            html.Label("Select Season(s):", className="mb-2"),
                            dcc.Checklist(
                                id='season-selector-task5',
                                options=[
                                    {'label': 'Spring (Mar-May)', 'value': 'Spring'},
                                    {'label': 'Summer (Jun-Aug)', 'value': 'Summer'},
                                    {'label': 'Fall (Sep-Nov)', 'value': 'Fall'},
                                    {'label': 'Winter (Dec-Feb)', 'value': 'Winter'}
                                ],
                                value=['Spring', 'Summer', 'Fall', 'Winter'],
                                inline=False
                            ),
                            html.Hr(className="my-3"),
                            html.P("Select one or more seasons to compare crime patterns across 2022.", 
                                   className="text-muted small")
                        ], width=3),
                        dbc.Col([
                            dcc.Graph(id='seasonal-map', style={'height': '500px'})
                        ], width=9)
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(id='area-correlation-heatmap', style={'height': '400px'})
                        ])
                    ], className="mt-3")
                ])
            ])
        ])
    ], className="mb-4"),
    
    # Store for filtered data
    dcc.Store(id='filtered-data-store'),
    # Store for current map type
    dcc.Store(id='map-type-store', data='heatmap'),
    
    # Debug info (hidden by default, can be shown in browser console)
    html.Div(id='debug-info', style={'display': 'none'})
    
], fluid=True)

# Add debug endpoint
@app.server.route('/debug')
def debug_info():
    """Debug endpoint to check data loading status"""
    import json
    debug_data = {
        'data_loader_base_dir': data_loader.base_dir,
        'data_loader_processed_dir': data_loader.processed_dir,
        'base_dir_exists': os.path.exists(data_loader.base_dir),
        'processed_dir_exists': os.path.exists(data_loader.processed_dir),
    }
    
    if os.path.exists(data_loader.processed_dir):
        files = os.listdir(data_loader.processed_dir)
        debug_data['processed_files'] = files
        debug_data['file_count'] = len(files)
        
        # Check if key files exist
        key_files = ['cleaned_data_sample.csv', 'area_aggregations.csv', 'crime_type_counts.csv', 'metadata.json']
        debug_data['key_files_exist'] = {
            f: os.path.exists(os.path.join(data_loader.processed_dir, f)) for f in key_files
        }
    
    # Test data loading
    test_data = data_loader.load_cleaned_data(sample=True)
    debug_data['test_data_loaded'] = test_data is not None
    if test_data is not None:
        debug_data['test_data_rows'] = len(test_data)
        debug_data['test_data_columns'] = list(test_data.columns)[:10]
    
    return json.dumps(debug_data, indent=2)

# Callback to apply filters and update store
@app.callback(
    Output('filtered-data-store', 'data'),
    [Input('apply-filters-btn', 'n_clicks')],
    [State('date-range-picker', 'start_date'),
     State('date-range-picker', 'end_date'),
     State('crime-type-filter', 'value'),
     State('area-filter', 'value')]
)
def update_filtered_data(n_clicks, start_date, end_date, crime_types, areas):
    """Load and filter data based on user selections"""
    try:
        df = data_loader.load_cleaned_data(sample=True)
        
        if df is None or df.empty:
            return None
        
        filters = {
            'date_range': (start_date, end_date) if start_date and end_date else None,
            'crime_types': crime_types if crime_types else None,
            'areas': areas if areas else None
        }
        
        filtered_df = apply_all_filters(df, filters)
        
        # Convert to JSON-serializable format
        if filtered_df.empty:
            return None
        
        # Convert datetime columns to strings for JSON serialization
        for col in filtered_df.columns:
            if pd.api.types.is_datetime64_any_dtype(filtered_df[col]):
                filtered_df[col] = filtered_df[col].astype(str)
        
        return filtered_df.to_dict('records')
    except Exception as e:
        print(f"Error in update_filtered_data: {e}")
        return None

# Callback to update button active states
@app.callback(
    [Output('map-type-heatmap', 'active'),
     Output('map-type-clusters', 'active'),
     Output('map-type-points', 'active'),
     Output('map-type-store', 'data')],
    [Input('map-type-heatmap', 'n_clicks'),
     Input('map-type-clusters', 'n_clicks'),
     Input('map-type-points', 'n_clicks')],
    [State('map-type-store', 'data')]
)
def update_map_type_buttons(heatmap_clicks, clusters_clicks, points_clicks, current_map_type):
    """Update button active states based on which button was clicked"""
    ctx = callback_context
    if not ctx.triggered:
        # Default to heatmap on initial load
        return True, False, False, 'heatmap'
    
    # Get the button that was clicked
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    map_type = button_id.replace('map-type-', '')
    
    # Set active state based on which button was clicked
    return (
        map_type == 'heatmap',
        map_type == 'clusters',
        map_type == 'points',
        map_type
    )

# Callback to update main map
@app.callback(
    Output('main-map', 'figure'),
    [Input('filtered-data-store', 'data'),
     Input('map-type-store', 'data')]
)
def update_map(data, map_type):
    """Update the main map visualization"""
    if data is None or len(data) == 0:
        return go.Figure().add_annotation(
            text="No data available. Please apply filters.",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    try:
        df = pd.DataFrame(data)
        
        # Debug: Check for coordinate columns
        print(f"DEBUG update_map: DataFrame shape: {df.shape}")
        print(f"DEBUG update_map: Columns: {list(df.columns)[:10]}")
        if 'LAT' in df.columns and 'LON' in df.columns:
            valid_coords = df[(df['LAT'].notna()) & (df['LON'].notna())]
            print(f"DEBUG update_map: Valid coordinates: {len(valid_coords)}/{len(df)}")
        else:
            print(f"DEBUG update_map: LAT/LON columns not found!")
        
        # Use component functions based on map type
        if map_type == 'heatmap':
            return create_map_heatmap(df)
        elif map_type == 'clusters':
            return create_map_clusters(df)
        else:  # points
            return create_map_points(df)
    except Exception as e:
        print(f"Error in update_map: {e}")
        import traceback
        traceback.print_exc()
        return go.Figure().add_annotation(
            text=f"Error loading map: {str(e)}",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )

# Callback to update time series
@app.callback(
    Output('time-series-chart', 'figure'),
    [Input('filtered-data-store', 'data')]
)
def update_time_series(data):
    """Update time series chart"""
    if data is None or len(data) == 0:
        return go.Figure()
    
    df = pd.DataFrame(data)
    return create_time_series(df)

# Callback to update hourly heatmap
@app.callback(
    Output('hourly-heatmap', 'figure'),
    [Input('filtered-data-store', 'data')]
)
def update_hourly_heatmap(data):
    """Update hourly heatmap"""
    if data is None or len(data) == 0:
        return go.Figure()
    
    df = pd.DataFrame(data)
    return create_hourly_heatmap(df)

# Callback to update crime type bar chart
@app.callback(
    Output('crime-type-bar', 'figure'),
    [Input('filtered-data-store', 'data')]
)
def update_crime_type_bar(data):
    """Update crime type bar chart"""
    if data is None or len(data) == 0:
        return go.Figure()
    
    df = pd.DataFrame(data)
    return create_crime_type_bar(df)

# Callback to update Part 1/2 pie chart
@app.callback(
    Output('part1-part2-pie', 'figure'),
    [Input('filtered-data-store', 'data')]
)
def update_part1_part2_pie(data):
    """Update Part 1 vs Part 2 pie chart"""
    if data is None or len(data) == 0:
        return go.Figure()
    
    df = pd.DataFrame(data)
    return create_part1_part2_pie(df)

# Callback to update area comparison
@app.callback(
    Output('area-comparison-chart', 'figure'),
    [Input('filtered-data-store', 'data')]
)
def update_area_comparison(data):
    """Update area comparison chart"""
    if data is None or len(data) == 0:
        return go.Figure()
    
    df = pd.DataFrame(data)
    return create_area_comparison_bar(df)

# Callback to update statistics cards
@app.callback(
    Output('stats-cards', 'children'),
    [Input('filtered-data-store', 'data')]
)
def update_stats_cards(data):
    """Update statistics cards"""
    if data is None or len(data) == 0:
        return html.Div("No data available")
    
    df = pd.DataFrame(data)
    return create_stats_cards(df)

# Callback for Task 4: Multi-dimensional hotspot analysis
@app.callback(
    Output('multi-dim-map', 'figure'),
    [Input('filtered-data-store', 'data'),
     Input('hour-range-slider', 'value'),
     Input('day-of-week-checklist', 'value'),
     Input('season-checklist', 'value')]
)
def update_multi_dim_map(data, hour_range, days, seasons):
    """Update multi-dimensional hotspot map"""
    if data is None or len(data) == 0:
        return go.Figure()
    
    df = pd.DataFrame(data)
    
    # Apply multi-dimensional filters
    if hour_range:
        df = filter_by_time_of_day(df, hour_range)
    if days:
        df = filter_by_day_of_week(df, days)
    if seasons:
        df = filter_by_season(df, seasons)
    
    if df.empty:
        return go.Figure()
    
    return create_map_heatmap(df)

# Callback for Task 5: Seasonal pattern analysis
@app.callback(
    [Output('seasonal-map', 'figure'),
     Output('area-correlation-heatmap', 'figure')],
    [Input('filtered-data-store', 'data'),
     Input('season-selector-task5', 'value')]
)
def update_seasonal_analysis(data, selected_seasons):
    """Update seasonal pattern visualization and area correlation"""
    try:
        if data is None or len(data) == 0:
            return go.Figure(), go.Figure()
        
        df = pd.DataFrame(data)
        
        # Filter by selected seasons
        if selected_seasons:
            season_months = {
                'Spring': [3, 4, 5],
                'Summer': [6, 7, 8],
                'Fall': [9, 10, 11],
                'Winter': [12, 1, 2]
            }
            months_to_include = []
            for season in selected_seasons:
                months_to_include.extend(season_months.get(season, []))
            if months_to_include:
                df = df[df['Month'].isin(months_to_include)]
        
        if df.empty:
            return go.Figure(), go.Figure()
        
        # Create map colored by season
        if 'Season' in df.columns:
            # Aggregate by location and season
            agg_df = df.groupby(['LAT', 'LON', 'Season']).size().reset_index(name='Count')
            
            # Create scatter map with season colors
            fig = px.scatter_mapbox(
                agg_df,
                lat="LAT",
                lon="LON",
                size="Count",
                color="Season",
                zoom=10,
                height=500,
                title="Crime Patterns by Season (2022)",
                hover_name="Count",
                mapbox_style="open-street-map",
                labels={"Count": "Number of Crimes", "size": "Number of Crimes"}
            )
            fig.update_traces(
                hovertemplate='<b>Season: %{marker.color}</b><br>Crimes: %{marker.size}<br>Lat: %{lat:.4f}<br>Lon: %{lon:.4f}<extra></extra>'
            )
        else:
            # Fallback: create heatmap
            fig = create_map_heatmap(df, title="Seasonal Crime Patterns (2022)")
        
        fig.update_layout(margin={"r":0,"t":50,"l":0,"b":0})
        
        # Create area correlation heatmap
        # Ensure DATE OCC is datetime if it exists
        if 'DATE OCC' in df.columns:
            correlation_fig = create_area_correlation_heatmap(df, area_col='AREA NAME', date_col='DATE OCC')
        elif 'Date' in df.columns:
            # Try alternative date column
            df['DATE OCC'] = pd.to_datetime(df['Date'], errors='coerce')
            correlation_fig = create_area_correlation_heatmap(df, area_col='AREA NAME', date_col='DATE OCC')
        else:
            # If no date column, create a simple correlation based on crime counts
            correlation_fig = go.Figure()
            correlation_fig.add_annotation(
                text="Area correlation requires date information. Please ensure date filters are applied.",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
        
        return fig, correlation_fig
    except Exception as e:
        print(f"Error in update_seasonal_analysis: {e}")
        import traceback
        traceback.print_exc()
        return go.Figure(), go.Figure()

# Make app server available for gunicorn
server = app.server

if __name__ == '__main__':
    # Get port from environment variable or default to 8050
    port = int(os.environ.get('PORT', 8050))
    debug = os.environ.get('DASH_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug, host='0.0.0.0', port=port)

