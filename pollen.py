import requests
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta

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
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if 'data' in data:
            return data['data']
    except requests.RequestException:
        return None  # Return None if API request fails
    return None


# Get 1 day forecast pollen data for a place
def get_forecast_pollen_data(place):
    url = f"https://api.ambeedata.com/forecast/pollen/by-place?place={place}"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if 'data' in data:
            return data['data']
    except requests.RequestException:
        return None  # Return None if API request fails
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
        # If no data from the API, fall back to 'pollen-backup.csv'
        try:
            fallback_df = pd.read_csv('pollen-backup.csv')

            # Get current date
            current_date = datetime.now()

            # Calculate date range
            start_date = current_date - timedelta(days=1)
            end_date = current_date + timedelta(days=1)

            # Generate new dates
            new_dates = pd.date_range(start=start_date, end=end_date, freq='H')

            # Ensure the DataFrame has the same number of rows as new_dates
            fallback_df = fallback_df.iloc[:len(new_dates)].copy()

            # Update the 'updatedAt' column with new dates
            fallback_df['updatedAt'] = new_dates.strftime('%Y-%m-%dT%H:%M:%S.000Z')

            # Update the 'time' column (Unix timestamp)
            fallback_df['time'] = new_dates.astype('int64') // 10 ** 9

            return fallback_df
        except FileNotFoundError:
            st.error("Pollen data not available, and fallback CSV not found.")
            return pd.DataFrame()  # Return empty DataFrame if no data is available