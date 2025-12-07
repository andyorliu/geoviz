# LA Crime Data Visualization Dashboard - 2022

An interactive spatial visualization dashboard for exploring Los Angeles crime data from 2022. The dashboard provides linked visualizations with cross-filtering capabilities to support multiple analytical tasks focused on seasonal, temporal, and spatial patterns within a single year.

## Features

- **Interactive Map**: Heatmap, clustered markers, and point visualizations with zoom and pan
- **Temporal Analysis**: Time series charts and hourly heatmaps showing crime patterns over time
- **Crime Type Distribution**: Bar charts, pie charts, and distribution visualizations
- **Area Comparison**: Side-by-side comparisons and correlation analysis between areas
- **Advanced Analysis**: Multi-dimensional hotspot analysis and crime displacement pattern detection

## Analytical Tasks Supported

### Task 1: Identify High-Crime Areas for Vehicle-Related Crimes in 2022
Use the filters to select vehicle-related crimes, then view the map to identify hotspots throughout 2022.

### Task 2: Compare Crime Trends by Time of Day in Wilshire vs. Central Areas (2022)
Select Wilshire and Central areas, and compare trends in the temporal analysis panel throughout 2022.

### Task 3: Seasonal Crime Pattern Analysis (2022)
Explore how crime patterns change across seasons (Spring, Summer, Fall, Winter) in 2022 using the multi-dimensional filters.

### Task 4: Multi-Dimensional Hotspot Analysis
Identify areas with high crime rates across multiple dimensions simultaneously:
- Select crime types, time of day range, days of week, and seasons
- View hotspots that match all selected criteria
- Analyze correlations between different dimensions

### Task 5: Day-of-Week and Time-of-Day Pattern Exploration
Analyze if crime hotspots shift over time:
- View animated time-lapse maps showing hotspot evolution
- Compare crime patterns between different time periods
- Identify displacement patterns where crime decreases in one area while increasing in adjacent areas

## Installation

1. Clone this repository or navigate to the project directory

2. Create a virtual environment (if not already created):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the data preprocessing script:
```bash
python src/preprocess_data.py
```

This will create processed data files in `data/processed/` directory.

## Running the Dashboard

Start the Dash application:

```bash
python src/app.py
```

The dashboard will be available at `http://localhost:8050`

## Project Structure

```
crime-data-vis-project/
├── data/
│   ├── Crime_Data_from_2020_to_Present.csv
│   └── processed/          # Preprocessed data files
├── src/
│   ├── app.py              # Main Dash application
│   ├── preprocess_data.py  # Data preprocessing script
│   ├── components/         # Visualization components
│   │   ├── map_view.py
│   │   ├── temporal_panel.py
│   │   ├── crime_type_panel.py
│   │   ├── area_comparison.py
│   │   └── stats_panel.py
│   └── utils/              # Utility modules
│       ├── data_loader.py
│       ├── filters.py
│       └── calculations.py
├── requirements.txt
└── README.md
```

## Usage

1. **Apply Filters**: Use the filter panel on the left to select:
   - Date range
   - Crime types (multi-select)
   - Areas (multi-select)

2. **Click "Apply Filters"** to update all visualizations

3. **Interact with Visualizations**:
   - **Map**: Toggle between Heatmap, Clusters, and Points views
   - **Time Series**: Hover to see values, brush to select time ranges
   - **Hourly Heatmap**: Click on cells to see details
   - **Crime Types**: Click on bars to filter

4. **Advanced Tasks**:
   - **Task 4**: Use the multi-dimensional filters in the "Advanced Analysis Tasks" section
   - **Task 5**: Select time period type and use the displacement analysis tools

## Data

The dashboard uses LA crime data from 2022. The dataset includes:
- Temporal information (date, time, day of week, season)
- Spatial information (latitude, longitude, area)
- Crime details (type, Part 1/2 classification)
- Victim and premises information

## Technologies

- **Dash**: Web framework for building interactive dashboards
- **Plotly**: Interactive visualization library
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations
- **Scikit-learn**: Machine learning utilities (for clustering)
- **Dash Bootstrap Components**: UI components

## Map Configuration

The dashboard uses OpenStreetMap by default for map tiles. For better performance and additional map styles, you can optionally configure a Mapbox token:

1. Get a free token from [Mapbox](https://www.mapbox.com/)
2. Set environment variable: `export MAPBOX_TOKEN=your_token_here`
3. Update map style in `src/components/map_view.py` to use `mapbox` style instead of `open-street-map`

## Performance Notes

- The dashboard uses pre-aggregated data for better performance
- Large datasets are sampled for visualization (10,000 points max for maps)
- All aggregations are pre-computed during data preprocessing

## Deployment

For GitHub Pages deployment:

1. Export the dashboard as static HTML (requires Dash Enterprise or custom export)
2. Or deploy to Streamlit Cloud if using Streamlit version
3. Or use Heroku/Railway for live Dash deployment

## License

This project is for educational and analytical purposes.

## Contact

For questions or issues, please refer to the project repository.

