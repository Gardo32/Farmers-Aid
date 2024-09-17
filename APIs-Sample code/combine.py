import pandas as pd
from weatherFunctions import *
from datetime import datetime
from nasa import get_precipitation_data  # Import the NASA precipitation function

# Step 1: Fetch real-time, historical, and forecast weather data
location = 'Manama'
real_time_weather_data = get_real_time_data(location)
historical_weather_data = fetch_historical_data(location)
forecast_weather_data = fetch_forecast_data(location, days=3)

# Step 2: Create DataFrames

# Real-time weather data
if real_time_weather_data:
    current = real_time_weather_data['current']
    real_time_df = pd.DataFrame([{
        'Date': datetime.now().strftime('%Y-%m-%d'),  # Ensure the date is in YYYY-MM-DD format
        'Location': real_time_weather_data['location']['name'],
        'Country': real_time_weather_data['location']['country'],
        'Local Time': real_time_weather_data['location']['localtime'],
        'Avg Temperature (°C)': current['temp_c'],
        'Avg Humidity (%)': current['humidity'],
        'Total Precipitation (mm)': current['precip_mm'],
        'Condition': current['condition']['text']
    }])
else:
    real_time_df = pd.DataFrame()  # Empty DataFrame if no data is fetched

# Historical weather data
historical_df = pd.DataFrame(historical_weather_data)

# Forecast weather data
forecast_df = pd.DataFrame(forecast_weather_data)

# Step 3: Fetch the Precipitation Data from NASA API (from nasa.py)
nasa_precipitation_df = get_precipitation_data()

# Step 4: Ensure 'Date' in nasa_precipitation_df is in the same format (YYYY-MM-DD)
if nasa_precipitation_df is not None:
    nasa_precipitation_df['Date'] = pd.to_datetime(nasa_precipitation_df['Date']).dt.strftime('%Y-%m-%d')

# Step 5: Define the columns to keep
columns_to_keep = ['Date', 'Location', 'Country', 'Local Time', 'Avg Temperature (°C)',
                   'Avg Humidity (%)', 'Total Precipitation (mm)', 'Condition']

# Ensure all DataFrames have the same columns
real_time_df = real_time_df.reindex(columns=columns_to_keep)
historical_df = historical_df.reindex(columns=columns_to_keep)
forecast_df = forecast_df.reindex(columns=columns_to_keep)

# Step 6: Concatenate the filtered DataFrames
combined_df = pd.concat([real_time_df, historical_df, forecast_df], ignore_index=True)

# Step 7: Replace the "Total Precipitation (mm)" column with the NASA data
if nasa_precipitation_df is not None:
    # Merge the combined data with NASA data on the 'Date' column
    combined_df = pd.merge(combined_df, nasa_precipitation_df[['Date', 'Precipitation (mm)']],
                           on='Date', how='left')
    # Replace "Total Precipitation (mm)" with the NASA values where available
    combined_df['Total Precipitation (mm)'] = combined_df['Precipitation (mm)'].combine_first(combined_df['Total Precipitation (mm)'])
    # Drop the extra "Precipitation (mm)" column from NASA
    combined_df.drop(columns=['Precipitation (mm)'], inplace=True)

# Step 8: Cap values of "Total Precipitation (mm)"
# - Replace values below 0 with 0.01
# - Replace values above 0.99 with 0.99
combined_df['Total Precipitation (mm)'] = combined_df['Total Precipitation (mm)'].clip(lower=0.01, upper=0.99)

# Display the combined DataFrame
print(combined_df)
