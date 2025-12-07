# Analytical Tasks Guide

This document provides detailed guidance on how to complete each analytical task using the dashboard.

## Task 1: Identify High-Crime Areas for Vehicle-Related Crimes in 2020

### Steps:
1. In the **Crime Types** filter, search for and select vehicle-related crimes:
   - "VEHICLE - STOLEN"
   - "VEHICLE - ATTEMPT STOLEN"
   - Any other vehicle-related crime types

2. In the **Date Range** picker, set:
   - Start Date: 2020-01-01
   - End Date: 2020-12-31

3. Click **Apply Filters**

4. View the **Interactive Map**:
   - Use the Heatmap view to see density patterns
   - Areas with darker red indicate higher crime concentrations
   - Click on areas to see details

5. Check the **Area Comparison** chart to see which areas have the most vehicle crimes

### Expected Insights:
- Identify top 3-5 areas with highest vehicle crime rates
- Note spatial patterns (clustered vs. dispersed)
- Compare crime density across different neighborhoods

---

## Task 2: Compare Crime Trends by Time of Day in Wilshire vs. Central Areas (2020-2023)

### Steps:
1. In the **Areas** filter, select:
   - "Wilshire"
   - "Central"

2. Set **Date Range**:
   - Start Date: 2020-01-01
   - End Date: 2023-12-31

3. Click **Apply Filters**

4. Analyze the visualizations:
   - **Time Series Chart**: Compare overall trends between areas
   - **Hourly Heatmap**: Compare peak crime hours
   - **Area Comparison Chart**: See total crime counts

5. For detailed comparison:
   - Look at the hourly patterns in the heatmap
   - Note differences in peak hours
   - Compare overall crime volumes

### Expected Insights:
- Identify which area has higher crime rates
- Compare temporal patterns (when crimes occur)
- Note any seasonal or trend differences

---

## Task 3: Explore a Pattern (Open-Ended)

### Suggested Exploration Approaches:

#### A. Seasonal Patterns
1. Filter by different date ranges (e.g., summer months vs. winter months)
2. Compare crime types across seasons
3. Look for seasonal spikes in specific crime types

#### B. Day-of-Week Patterns
1. Use the hourly heatmap to see weekday vs. weekend patterns
2. Filter by specific days and compare
3. Identify which days have highest crime rates

#### C. Crime Type Correlations
1. Select multiple related crime types
2. See if they cluster in the same areas
3. Check temporal correlations

#### D. Area-Specific Patterns
1. Select a specific area
2. Analyze crime types, times, and trends
3. Compare with other areas

### Documentation:
When you find an interesting pattern, document:
- What pattern you observed
- Which filters/visualizations revealed it
- Potential explanations or hypotheses
- Questions for further investigation

---

## Task 4: Multi-Dimensional Hotspot Analysis

### Objective:
Find areas dangerous for specific crime types during specific times/days/seasons.

### Steps:
1. Navigate to the **"Task 4: Multi-Dimensional Hotspot Analysis"** section

2. Set multi-dimensional filters:
   - **Crime Types**: Select specific types (e.g., "BURGLARY", "ASSAULT")
   - **Time of Day Range**: Use slider (e.g., 20:00-06:00 for nighttime)
   - **Day of Week**: Check specific days (e.g., Friday, Saturday for weekends)
   - **Season**: Select seasons (e.g., Summer)

3. The map will automatically update to show hotspots matching ALL criteria

4. Analyze results:
   - Identify areas that appear as hotspots
   - Note the intensity (darker = more crimes)
   - Compare with different filter combinations

### Example Queries:
- "Where are vehicle thefts most common on weekend nights?"
- "Which areas have the most burglaries during weekday afternoons in summer?"
- "Find hotspots for assault crimes on Friday/Saturday nights"

### Expected Insights:
- Areas that are dangerous under specific conditions
- Patterns that only appear when multiple dimensions are combined
- Insights for targeted interventions

---

## Task 5: Crime Displacement and Migration Patterns

### Objective:
Determine if crime decreases in one area while increasing in adjacent areas.

### Steps:
1. Navigate to the **"Task 5: Crime Displacement and Migration Patterns"** section

2. Select **Time Period**:
   - Monthly (more granular)
   - Quarterly (broader trends)

3. Use the **Animated Map**:
   - Click "Play" to see hotspot evolution over time
   - Watch for areas where crime density increases/decreases
   - Note if decreases in one area correspond to increases in nearby areas

4. **Compare Periods** (optional):
   - Set Period 1 date range (e.g., 2020 Q1-Q2)
   - Set Period 2 date range (e.g., 2021 Q1-Q2)
   - Click "Compare Periods"
   - Analyze changes between periods

5. Check the **Area Correlation Heatmap**:
   - Look for negative correlations (one area up, another down)
   - Identify areas with similar patterns (positive correlation)
   - Note areas with independent patterns (low correlation)

### Analysis Questions:
- Do crime hotspots shift geographically over time?
- When crime decreases in Area A, does it increase in adjacent Area B?
- Are there seasonal displacement patterns?
- Which areas show the most stable vs. volatile crime patterns?

### Expected Insights:
- Evidence of displacement (crime moving, not reducing)
- Areas that consistently have high crime
- Areas showing improvement or deterioration
- Spatial-temporal relationships between areas

---

## Tips for Effective Analysis

1. **Start Broad, Then Narrow**: Begin with wide filters, then narrow down based on what you see

2. **Use Multiple Views**: Don't rely on just one visualization - cross-reference findings

3. **Compare and Contrast**: Always compare your findings with other areas/time periods

4. **Document Your Process**: Note which filters you used and what you observed

5. **Look for Surprises**: Pay attention to unexpected patterns - they often lead to insights

6. **Validate Findings**: Check if patterns hold across different time periods or filter combinations

