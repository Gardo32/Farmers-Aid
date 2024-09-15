import requests
import pandas as pd
from datetime import datetime, timedelta

# Ambee API Key (replace with your actual API key)
API_KEY = 'DEMO_key'

# Place for Manama, Bahrain
place = "Manama,Bahrain"

# Headers including the API key
headers = {
    'x-api-key': API_KEY,
    'Content-type': 'application/json',
    'Accept-Language': 'en'
}


# Get current pollen data for a place
def get_latest_pollen_data():
    url = f"https://api.ambeedata.com/latest/pollen/by-place?place={place}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if 'data' in data:
            return data['data']
        else:
            print(f"No 'data' field in response: {data}")
            return None
    else:
        print(f"Error: Received status code {response.status_code} from API")
        return None


# Get 7 days historical pollen data for a place

# Get 1 day forecast pollen data for a place
def get_forecast_pollen_data():
    url = f"https://api.ambeedata.com/forecast/pollen/by-place?place={place}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if 'data' in data:
            return data['data']
        else:
            print(f"No 'data' field in response: {data}")
            return None
    else:
        print(f"Error: Received status code {response.status_code} from API")
        return None


# Display all pollen data
def display_pollen_data():
    # Fetch latest pollen data
    latest_pollen = get_latest_pollen_data()


    # Fetch forecast pollen data (1 day)
    forecast_pollen = get_forecast_pollen_data()

    if latest_pollen:
        latest_df = pd.DataFrame(latest_pollen)
        print("Latest Pollen Data:")
        print(latest_df)

    if forecast_pollen:
        forecast_df = pd.DataFrame(forecast_pollen)
        print("\n1 Day Forecast Pollen Data:")
        print(forecast_df)


if __name__ == "__main__":
    display_pollen_data()
