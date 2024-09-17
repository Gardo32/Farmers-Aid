"""
# Get Pollination Data

from pollen import get_combined_pollen_data

# Input the place
place = "Manama,Bahrain"

# Call the function to get the combined pollen data
combined_df = get_combined_pollen_data(place)

# Display the DataFrame
print(combined_df)
"""

"""
# Get Weather Data

from weather import get_combined_weather_data

# Input your location, latitude, and longitude
location = 'Manama'
latitude = 26.223
longitude = 50.586

# Get the combined weather data
combined_df = get_combined_weather_data(location, latitude, longitude)

# Display the combined DataFrame
print(combined_df)
"""