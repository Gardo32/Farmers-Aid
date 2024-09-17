import requests
import pandas as pd
from datetime import datetime, timedelta

def get_precipitation_data():
    # Get the current date
    current_date = datetime.now()

    # Get the date 7 days ago and 3 days ahead
    seven_days_ago = current_date - timedelta(days=7)
    three_days_ahead = current_date + timedelta(days=3)

    # Format the dates as YYYYMMDD strings
    seven_days_ago_str = seven_days_ago.strftime('%Y%m%d')
    three_days_ahead_str = three_days_ahead.strftime('%Y%m%d')

    # API URL for NASA POWER API
    url = 'https://power.larc.nasa.gov/api/temporal/daily/point'

    # Parameters for the request (use formatted dates as strings)
    params = {
        'start': seven_days_ago_str,
        'end': three_days_ahead_str,
        'latitude': 26.223,
        'longitude': 50.586,
        'community': 'AG',
        'parameters': 'PRECTOTCORR',
        'format': 'JSON',
        'header': 'true',
        'api_key': 'DEMO_key'
    }

    # Make the API request
    response = requests.get(url, params=params)

    # Check response status and process data
    if response.status_code == 200:
        raw_data = response.json()
        data = raw_data['properties']['parameter']['PRECTOTCORR']
        df = pd.DataFrame(list(data.items()), columns=['Date', 'Precipitation (mm)'])
        return df
    else:
        print(f"Error: {response.status_code}")
        return None
