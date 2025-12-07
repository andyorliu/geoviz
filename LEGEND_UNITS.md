# Legend Units and Labels Guide

This document explains the units and labels used in each visualization's legend/colorbar.

## Map Visualizations

### 1. Heatmap View
- **Legend Unit**: "Crime Density (Relative Intensity)"
- **Description**: Shows relative density of crimes across the map. Darker red indicates higher crime concentration. This is a normalized density measure, not an absolute count.

### 2. Clusters View
- **Legend**: No colorbar (markers are uniform red)
- **Description**: Individual crime locations shown as red markers. Size and color are fixed.

### 3. Points View
- **Legend**: No colorbar (markers are uniform red)
- **Description**: Individual crime locations shown as red markers. Size and color are fixed.

### 4. Temporal Map (Task 5)
- **Legend Unit**: "Number of Crimes"
- **Description**: Color intensity and marker size represent the number of crimes in each area for the selected time period.

## Temporal Visualizations

### 1. Time Series Chart
- **Y-Axis Label**: "Number of Crimes"
- **Description**: Shows the count of crimes over time (daily/weekly/monthly aggregation).

### 2. Hourly Heatmap
- **Legend Unit**: "Number of Crimes"
- **Description**: Each cell shows the count of crimes for a specific hour (0-23) and day of week combination. Darker red indicates more crimes.

## Crime Type Visualizations

### 1. Crime Type Bar Chart
- **X-Axis Label**: "Number of Crimes"
- **Description**: Horizontal bar chart showing the count of each crime type.

### 2. Part 1 vs Part 2 Pie Chart
- **Values**: Number of crimes (count)
- **Description**: Shows the proportion of Part 1 vs Part 2 crimes as percentages, with actual counts in tooltips.

## Area Comparison Visualizations

### 1. Area Comparison Bar Chart
- **Y-Axis Label**: "Number of Crimes"
- **Description**: Shows the total count of crimes for each area.

### 2. Area Correlation Heatmap
- **Legend Unit**: "Correlation Coefficient"
- **Description**: Shows Pearson correlation coefficients between areas based on monthly crime patterns. Values range from -1 to +1:
  - **+1**: Perfect positive correlation (areas have similar patterns)
  - **0**: No correlation (areas are independent)
  - **-1**: Perfect negative correlation (areas have opposite patterns)

## Task-Specific Visualizations

### Task 4: Multi-Dimensional Hotspot Analysis
- **Map Legend**: Same as Heatmap View ("Crime Density (Relative Intensity)")
- **Description**: Shows hotspots matching all selected criteria (crime type, time, day, season).

### Task 5: Seasonal Crime Pattern Analysis
- **Seasonal Map Legend**: "Number of Crimes" (for marker size)
- **Color**: Represents different seasons (categorical)
- **Area Correlation Heatmap**: "Correlation Coefficient" (same as above)

## Summary of Units

| Visualization | Unit/Label | Range/Type |
|--------------|------------|------------|
| Map Heatmap | Crime Density (Relative Intensity) | Normalized 0-1 |
| Hourly Heatmap | Number of Crimes | Integer count |
| Time Series | Number of Crimes | Integer count |
| Bar Charts | Number of Crimes | Integer count |
| Correlation Heatmap | Correlation Coefficient | -1 to +1 (unitless) |
| Temporal Map | Number of Crimes | Integer count |
| Pie Charts | Number of Crimes | Integer count (shown as %) |

## Notes

- **Counts**: All "Number of Crimes" values represent the actual count of crime incidents in the dataset.
- **Density**: The heatmap density is a relative measure, not an absolute count. It shows where crimes are concentrated.
- **Correlation**: Correlation coefficients are unitless and range from -1 to +1, indicating the strength and direction of the relationship between areas' crime patterns.
- **Sampling**: Some visualizations may sample data for performance (e.g., maps sample to 10,000 points), but the counts shown are from the sampled data.

