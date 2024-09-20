# pollen_data.py
import requests
import pandas as pd
import streamlit as st

API_KEY = st.secrets["AMBEE_API_KEY"]

# Headers including the API key
headers = {
    'x-api-key': API_KEY,
    'Content-type': 'application/json',
    'Accept-Language': 'en'
}


# Get current pollen data for a place
def get_latest_pollen_data(place):
    url = f"https://api.ambeedata.com/latest/pollen/by-place?place={place}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if 'data' in data:
            return data['data']
    return None


# Get 1 day forecast pollen data for a place
def get_forecast_pollen_data(place):
    url = f"https://api.ambeedata.com/forecast/pollen/by-place?place={place}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if 'data' in data:
            return data['data']
    return None


# Function to fetch pollen data and return the combined DataFrame
def get_combined_pollen_data(place):
    # Fetch latest pollen data
    latest_pollen = get_latest_pollen_data(place)

    # Fetch forecast pollen data (1 day)
    forecast_pollen = get_forecast_pollen_data(place)

    # Initialize list for DataFrames
    similar_columns_dfs = []

    if latest_pollen:
        # Flatten the latest_df
        latest_df_flat = pd.json_normalize(latest_pollen)
        similar_columns_dfs.append(latest_df_flat)

    if forecast_pollen:
        # Flatten the forecast_df
        forecast_df_flat = pd.json_normalize(forecast_pollen)
        similar_columns_dfs.append(forecast_df_flat)

    # Combine all DataFrames with similar columns
    if similar_columns_dfs:
        combined_similar_df = pd.concat(similar_columns_dfs, ignore_index=True)
        return combined_similar_df
    else:
        return pd.DataFrame()  # Return empty DataFrame if no data is available
