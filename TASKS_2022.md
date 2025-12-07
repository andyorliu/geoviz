# Analytical Tasks Guide - 2022 Data

This document provides detailed guidance on how to complete each analytical task using the dashboard with **2022 data only**.

## Task 1: Identify High-Crime Areas for Vehicle-Related Crimes in 2022

### Objective:
Find which areas in LA had the highest concentration of vehicle-related crimes throughout 2022.

### Steps:
1. In the **Crime Types** filter, search for and select vehicle-related crimes:
   - "VEHICLE - STOLEN"
   - "VEHICLE - ATTEMPT STOLEN"
   - "VEHICLE - STOLEN (TRAILER)"
   - Any other vehicle-related crime types

2. The **Date Range** is automatically set to 2022 (2022-01-01 to 2022-12-31)

3. View the **Interactive Map**:
   - Use the Heatmap view to see density patterns
   - Areas with darker red indicate higher crime concentrations
   - Click on areas to see detailed counts

4. Check the **Area Comparison** chart to see which areas have the most vehicle crimes

5. Review the **Statistical Summary** panel for total counts and top areas

### Expected Insights:
- Identify top 3-5 areas with highest vehicle crime rates in 2022
- Note spatial patterns (clustered vs. dispersed)
- Compare crime density across different neighborhoods
- Understand which areas need targeted vehicle crime prevention

---

## Task 2: Compare Crime Patterns by Time of Day in Wilshire vs. Central Areas (2022)

### Objective:
Compare when crimes occur throughout the day in two different areas during 2022.

### Steps:
1. In the **Areas** filter, select:
   - "Wilshire"
   - "Central"

2. The date range is automatically set to 2022

3. Analyze the visualizations:
   - **Hourly Heatmap**: Compare peak crime hours between the two areas
   - **Time Series Chart**: See daily/weekly patterns throughout 2022
   - **Area Comparison Chart**: Compare total crime counts
   - **Area Correlation Heatmap**: See if patterns are similar or different

4. For detailed comparison:
   - Look at the hourly patterns in the heatmap
   - Note differences in peak hours (morning, afternoon, evening, night)
   - Compare overall crime volumes
   - Check if weekends vs. weekdays differ between areas

### Expected Insights:
- Identify which area has higher crime rates in 2022
- Compare temporal patterns (when crimes occur during the day)
- Note differences in peak crime hours between areas
- Understand if one area is safer at certain times of day

---

## Task 3: Seasonal Crime Pattern Analysis (2022)

### Objective:
Explore how crime patterns change across seasons (Spring, Summer, Fall, Winter) in 2022.

### Steps:
1. Navigate to the **"Task 4: Multi-Dimensional Hotspot Analysis"** section

2. Use the **Season** filter to explore different seasons:
   - Start with **Spring** (March-May) - select only Spring
   - Then **Summer** (June-August)
   - Then **Fall** (September-November)
   - Then **Winter** (December, January, February)

3. For each season:
   - Observe the **Interactive Map** to see spatial patterns
   - Check the **Temporal Patterns** chart for daily trends
   - Review the **Crime Type Distribution** to see which crimes are most common

4. Compare across seasons:
   - Note which seasons have higher overall crime
   - Identify if certain crime types spike in specific seasons
   - See if spatial hotspots change by season

### Analysis Questions:
- Which season had the most crimes in 2022?
- Do certain crime types peak in specific seasons?
- Do crime hotspots shift geographically by season?
- Are there seasonal patterns that could inform resource allocation?

### Expected Insights:
- Seasonal trends in crime volume
- Seasonal variations in crime types
- Geographic shifts in crime hotspots by season
- Insights for seasonal resource planning

---

## Task 4: Multi-Dimensional Hotspot Analysis (2022)

### Objective:
Find areas that are dangerous for specific crime types during specific times/days/seasons in 2022.

### Steps:
1. Navigate to the **"Task 4: Multi-Dimensional Hotspot Analysis"** section

2. Set multi-dimensional filters:
   - **Crime Types**: Select specific types (e.g., "BURGLARY", "ASSAULT", "VEHICLE - STOLEN")
   - **Time of Day Range**: Use slider (e.g., 20:00-06:00 for nighttime, 12:00-18:00 for afternoon)
   - **Day of Week**: Check specific days (e.g., Friday, Saturday for weekends; Monday-Friday for weekdays)
   - **Season**: Select seasons (e.g., Summer, Winter)

3. The map will automatically update to show hotspots matching ALL criteria

4. Analyze results:
   - Identify areas that appear as hotspots
   - Note the intensity (darker = more crimes)
   - Compare with different filter combinations
   - Check the statistical summary for counts

### Example Queries:
- "Where are vehicle thefts most common on weekend nights in summer 2022?"
- "Which areas have the most burglaries during weekday afternoons in fall 2022?"
- "Find hotspots for assault crimes on Friday/Saturday nights in winter 2022"
- "Where do robberies occur most during weekday mornings in spring 2022?"

### Expected Insights:
- Areas that are dangerous under specific conditions
- Patterns that only appear when multiple dimensions are combined
- Insights for targeted interventions based on time, place, and crime type
- Understanding of when and where specific crimes are most likely

---

## Task 5: Day-of-Week and Time-of-Day Pattern Exploration (2022)

### Objective:
Discover how crime patterns vary by day of week and time of day throughout 2022.

### Steps:
1. Start with a broad view:
   - Leave all filters at default (all areas, all crime types)
   - Observe the **Hourly Heatmap** (24 hours × 7 days grid)

2. Analyze day-of-week patterns:
   - Note which days have the most crimes
   - Identify if weekends differ from weekdays
   - Check if certain days have unique patterns

3. Analyze time-of-day patterns:
   - Identify peak crime hours
   - Note if there are multiple peaks (morning, afternoon, evening, night)
   - Compare weekday vs. weekend hourly patterns

4. Combine with crime type filters:
   - Select specific crime types (e.g., "ASSAULT", "BURGLARY")
   - See how their day/time patterns differ
   - Compare violent vs. property crimes

5. Combine with area filters:
   - Select specific areas
   - Compare their day/time patterns
   - Identify if certain areas have unique temporal signatures

### Analysis Questions:
- Which day of the week has the most crimes in 2022?
- What time of day is most dangerous?
- Do weekends have different patterns than weekdays?
- Do different crime types have different temporal patterns?
- Do different areas have different temporal patterns?

### Expected Insights:
- Understanding of when crimes are most likely to occur
- Differences between weekday and weekend patterns
- Peak hours for different crime types
- Area-specific temporal signatures
- Insights for resource allocation by time and day

---

## Tips for Effective Analysis with 2022 Data

1. **Focus on Patterns Within the Year**: Since we only have 2022 data, focus on:
   - Seasonal variations (Spring, Summer, Fall, Winter)
   - Day-of-week patterns
   - Time-of-day patterns
   - Spatial patterns across areas
   - Crime type distributions

2. **Use Multi-Dimensional Filters**: The power of the dashboard is combining filters:
   - Crime type + Time + Day + Season
   - Area + Crime type + Time
   - Multiple areas for comparison

3. **Compare and Contrast**: 
   - Compare different areas
   - Compare different crime types
   - Compare different times/days/seasons
   - Compare different filter combinations

4. **Look for Surprises**: 
   - Unexpected patterns (e.g., high crime on a specific day/time)
   - Areas with unique patterns
   - Crime types with unusual temporal patterns

5. **Document Your Findings**: 
   - Note which filters revealed each insight
   - Record specific numbers and patterns
   - Formulate hypotheses about why patterns exist

6. **Validate with Multiple Views**: 
   - Don't rely on just one visualization
   - Cross-reference map, temporal, and statistical views
   - Use area comparison to validate map findings

---

## Key Differences from Multi-Year Analysis

Since we're working with **2022 data only**, the focus shifts from:
- ❌ **Year-over-year trends** → ✅ **Within-year patterns**
- ❌ **Long-term displacement** → ✅ **Seasonal shifts**
- ❌ **Multi-year comparisons** → ✅ **Seasonal/day-of-week comparisons**

This allows for deeper analysis of:
- ✅ **Seasonal variations** within a single year
- ✅ **Day-of-week patterns** with full year of data
- ✅ **Time-of-day patterns** across all seasons
- ✅ **Spatial patterns** with consistent temporal context
- ✅ **Multi-dimensional combinations** (crime type + time + day + season)

