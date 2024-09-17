import requests
import pandas as pd

# Ambee API Key
API_KEY = 'your_actual_api_key'

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
    print(f"Fetching latest pollen data from: {url}")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        if 'data' in data:
            print(f"Latest pollen data: {data['data']}")
            return data['data']
        else:
            print(f"No 'data' field in response: {data}")
            return None
    else:
        print(f"Error: Received status code {response.status_code} from API")
        return None


# Get 1 day forecast pollen data for a place
def get_forecast_pollen_data():
    url = f"https://api.ambeedata.com/forecast/pollen/by-place?place={place}"
    response = requests.get(url, headers=headers)
    print(f"Fetching forecast pollen data from: {url}")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        if 'data' in data:
            print(f"Forecast pollen data: {data['data']}")
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

    # Initialize list for DataFrames
    similar_columns_dfs = []

    if latest_pollen:
        latest_df = pd.DataFrame(latest_pollen)
        print("Latest DataFrame (Before Flattening):")
        print(latest_df.head())

        # Flatten the latest_df
        latest_df_flat = pd.json_normalize(latest_pollen)
        print("Latest DataFrame (Flattened):")
        print(latest_df_flat.head())

        similar_columns_dfs.append(latest_df_flat)
    else:
        print("No latest pollen data available.")

    if forecast_pollen:
        forecast_df = pd.DataFrame(forecast_pollen)
        print("Forecast DataFrame (Before Flattening):")
        print(forecast_df.head())

        # Flatten the forecast_df
        forecast_df_flat = pd.json_normalize(forecast_pollen)
        print("Forecast DataFrame (Flattened):")
        print(forecast_df_flat.head())

        similar_columns_dfs.append(forecast_df_flat)
    else:
        print("No forecast pollen data available.")

    # Combine all DataFrames with similar columns
    if similar_columns_dfs:
        combined_similar_df = pd.concat(similar_columns_dfs, ignore_index=True)
        print("Combined Similar Columns DataFrame (Flattened):")
        print(combined_similar_df.head())
    else:
        combined_similar_df = pd.DataFrame()  # Empty DataFrame if no data
        print("No data to combine.")

    # Optionally, save DataFrames as CSV files
    combined_similar_df.to_csv('combined_similar_flattened.csv', index=False)


if __name__ == "__main__":
    display_pollen_data()
