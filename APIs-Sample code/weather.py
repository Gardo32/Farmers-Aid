from weatherFunctions import *

location = 'Manama'
real_time_weather_data = get_real_time_data(location)
historical_weather_data = fetch_historical_data(location)
forecast_weather_data = fetch_forecast_data(location, days=3)

# Create DataFrames
if real_time_weather_data:
    current = real_time_weather_data['current']
    real_time_df = pd.DataFrame([{
        'Date': datetime.now().strftime('%Y-%m-%d'),
        'Location': real_time_weather_data['location']['name'],
        'Country': real_time_weather_data['location']['country'],
        'Local Time': real_time_weather_data['location']['localtime'],
        'Temperature (°C)': current['temp_c'],
        'Humidity (%)': current['humidity'],
        'Precipitation (mm)': current['precip_mm'],
        'Wind Speed (kph)': current['wind_kph'],
        'Wind Direction': current['wind_dir'],
        'Condition': current['condition']['text'],
        'UV Index': current['uv']
    }])

historical_df = pd.DataFrame(historical_weather_data)
forecast_df = pd.DataFrame(forecast_weather_data)

"""
real_time_df.to_csv("real_time_df.csv")
forecast_df.to_csv("forecast_df.csv")
historical_df.to_csv("historical_df.csv")
"""

# Print DataFrames
print("Real-Time Weather Data:")
print(real_time_df)
print("\nHistorical Weather Data (Past 7 Days):")
print(historical_df)
print("\n3-Day Weather Forecast:")
print(forecast_df)
