import requests
import pandas as pd

# API URL for NASA POWER API (example: daily data for a specific location)
url = 'https://power.larc.nasa.gov/api/temporal/daily/point'

# Parameters for the request (corrected for single parameter test)
params = {
    'start': '20240901',  # Start date (YYYYMMDD format)
    'end': '20240907',  # End date (YYYYMMDD format)
    'latitude': 26.223,  # Latitude for Manama, Bahrain
    'longitude': 50.586,  # Longitude for Manama, Bahrain
    'community': 'AG',  # Data community (AG for agriculture)
    'parameters': 'PRECTOTCORR',  # Parameter: Corrected Total Precipitation
    'format': 'JSON',  # Data format: JSON
    'header': 'true',  # Include metadata header
    'api_key': 'DEMO_key'  # Use DEMO key for access
}

# Make the API request
response = requests.get(url, params=params)

# Check response status and process data
if response.status_code == 200:
    raw_data = response.json()

    # Extract the dates and precipitation values from the raw data
    data = raw_data['properties']['parameter']['PRECTOTCORR']

    # Convert the data into a DataFrame
    df = pd.DataFrame(list(data.items()), columns=['Date', 'Precipitation (mm)'])

    # Display the DataFrame
    print(df)
else:
    print(f"Error: {response.status_code}")
    print(response.json())  # Print the response content for further debugging
