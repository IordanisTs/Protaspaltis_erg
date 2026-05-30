# Protaspaltis_erg
# Kozani Urban Mobility & Local Events 2025 - Visual Analytics

## Overview
This repository contains a Visual Analytics project developed for the "Special Topics and Applications of Digital Technologies" course at the University of Western Macedonia (UOWM). The project analyzes the impact of local events on urban mobility and traffic congestion in the city of Kozani for the year 2025.

## Project Structure
The analysis is broken down into three main Python scripts:
* **`pipeline.py`**: Handles data preprocessing, cleaning (handling missing values), and data fusion. It merges urban mobility data with local event schedules and calculates a custom metric (`PT_Preference_Score`).
* **`plots.py`**: Generates static visualizations using `Matplotlib` and `Seaborn` to highlight historical patterns (e.g., traffic distribution, bike trip trends, and parking occupancy by event type).
* **`app.py`**: An interactive web dashboard built with `Dash` and `Plotly`. It allows users to filter data dynamically (by day type and holidays) and explore correlations between event attendance, parking occupancy, and transport strain index.

## Datasets Used
* `urban_mobility_kozani_2025.csv`: Daily metrics on bus passengers, bike trips, parking occupancy, and overall traffic count.
* `local_events_kozani_2025.csv`: Schedule of events including type, location, and expected attendance.

## Technology Stack
* **Language:** Python
* **Data Manipulation:** Pandas, NumPy
* **Static Visualizations:** Matplotlib, Seaborn
* **Interactive Dashboard:** Dash, Plotly

## How to Run the Dashboard Locally
1. Clone the repository or download the files.
2. Ensure you have the required libraries installed:
   ```bash
   pip install pandas numpy matplotlib seaborn dash plotly
Run the dashboard application: python app.py

Open your web browser and navigate to http://127.0.0.1:8050/.
