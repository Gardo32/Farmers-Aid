import requests
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv('weather')
# Your WeatherAPI key (replace with your actual key)

# Base URLs for the API
REALTIME_URL = 'http://api.weatherapi.com/v1/current.json'
HISTORY_URL = 'http://api.weatherapi.com/v1/history.json'
FORECAST_URL = 'http://api.weatherapi.com/v1/forecast.json'

def get_real_time_data(location):
    """Fetch real-time weather data."""
    params = {
        'key': API_KEY,
        'q': location,
        'aqi': 'no'
    }
    response = requests.get(REALTIME_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_weather_data(location, date):
    """Fetch weather data for a specific date."""
    params = {
        'key': API_KEY,
        'q': location,
        'dt': date
    }
    response = requests.get(HISTORY_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_forecast_data(location, days):
    """Fetch weather forecast data."""
    params = {
        'key': API_KEY,
        'q': location,
        'days': days,
        'aqi': 'no'
    }
    response = requests.get(FORECAST_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def fetch_historical_data(location):
    """Fetch historical weather data for the past 7 days."""
    historical_data = []
    today = datetime.now()
    for i in range(7):
        date = (today - timedelta(days=i)).strftime('%Y-%m-%d')
        data = get_weather_data(location, date)
        if data:
            day_data = data['forecast']['forecastday'][0]['day']
            historical_data.append({
                'Date': date,
                'Location': data['location']['name'],
                'Country': data['location']['country'],
                'Local Time': data['location']['localtime'],
                'Avg Temperature (°C)': day_data['avgtemp_c'],
                'Avg Humidity (%)': day_data['avghumidity'],
                'Total Precipitation (mm)': day_data['totalprecip_mm'],
                'Condition': day_data['condition']['text']
            })
        else:
            historical_data.append({'Date': date, 'Error': 'Error fetching data'})
    return historical_data

def fetch_forecast_data(location, days=3):
    """Fetch weather forecast data for the next 3 days."""
    data = get_forecast_data(location, days)
    if data:
        forecast_data = []
        for day in data['forecast']['forecastday']:
            forecast_data.append({
                'Date': day['date'],
                'Location': data['location']['name'],
                'Country': data['location']['country'],
                'Local Time': data['location']['localtime'],
                'Avg Temperature (°C)': day['day']['avgtemp_c'],
                'Avg Humidity (%)': day['day']['avghumidity'],
                'Total Precipitation (mm)': day['day']['totalprecip_mm'],
                'Condition': day['day']['condition']['text']
            })
        return forecast_data
    else:
        return [{'Date': '', 'Error': 'Error fetching forecast data'}]
