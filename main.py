import os
import streamlit as st
import pandas as pd
import requests
import pycountry
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv
from pollen import get_combined_pollen_data
from weather import get_combined_weather_data
from AI import get_agricultural_response

# Load the IP API key from the .env file
load_dotenv()
IPkey = os.getenv('ip')
Ai_key = os.getenv("github")


# Function to convert country code to full country name
def get_country_name(country_code):
    try:
        country = pycountry.countries.get(alpha_2=country_code)
        return country.name if country else 'Unknown'
    except Exception as e:
        return 'Unknown'


# Function to get user's location data from ipinfo.io using the API key
def get_ip_info():
    try:
        response = requests.get(f"https://ipinfo.io?token={IPkey}")
        data = response.json()
        location = data.get('loc', '').split(',')
        city = data.get('city', 'Unknown')
        country_code = data.get('country', 'Unknown')
        country_name = get_country_name(country_code)
        return {
            "city": city,
            "country": country_name,
            "latitude": location[0] if location else 'Unknown',
            "longitude": location[1] if location else 'Unknown'
        }
    except Exception as e:
        return {"error": str(e)}


# Get and display the location data
location_data = get_ip_info()

# Variables for each location data
city = location_data.get('city', 'Unknown')
country = location_data.get('country', 'Unknown')
latitude = location_data.get('latitude', 'Unknown')
longitude = location_data.get('longitude', 'Unknown')

# Create a variable with the format City,Country
place = f"{city},{country}"

pollen_df = get_combined_pollen_data(place)
real_df, weather_df = get_combined_weather_data(city, latitude, longitude)
pollen_df.to_csv("pollen.csv")
weather_df.to_csv("weather.csv")
# App start from here

st.title('Farmers Aid')

At = st.expander("Advance Tweaks", expanded=False)
chrt, rprt, dyrt = st.tabs(["📈 Charts", "🗒️ Report", "📊 Dynamic Report"])

# Add tweak options in the expander
with At:
    st.write("Use the options below to tweak chart settings:")

    # Select chart color
    chart_color = st.color_picker("Select Chart Line Color", "#1f77b4")

    # Select line style
    line_style = st.selectbox("Select Line Style", ['solid', 'dot', 'dash'])

    # Axis scaling options
    y_axis_range_temp = st.slider("Select Y-axis range for Temperature (°C)", 0, 50, (10, 40))
    y_axis_range_humidity = st.slider("Select Y-axis range for Humidity (%)", 0, 100, (20, 80))

    # Toggle grid visibility
    show_grid = st.checkbox("Show Grid", value=True)

with chrt:
    col1, col2 = st.columns([4, 6])

    # First chart: Line plot for weed pollen count
    with col1:
        pollen_df['time'] = pd.to_datetime(pollen_df['time'], unit='s')

        # Line plot for weed pollen count
        fig1 = px.line(pollen_df, x='time', y='Count.weed_pollen',
                       labels={'Count.weed_pollen': 'Weed Pollen Count', 'time': 'Time'},
                       title="Weed Pollen Counts Over Time")
        st.plotly_chart(fig1)

    # Second chart: Temperature and humidity trends with customization
    with col2:
        # Create figure for temperature and humidity
        fig2 = go.Figure()

        # Add temperature trace with selected line style and color
        fig2.add_trace(go.Scatter(
            x=weather_df['Date'], y=weather_df['Avg Temperature (°C)'],
            mode='lines', name='Avg Temperature (°C)',
            line=dict(dash=line_style, color=chart_color),
            yaxis='y1'))

        # Add humidity trace with selected line style
        fig2.add_trace(go.Scatter(
            x=weather_df['Date'], y=weather_df['Avg Humidity (%)'],
            mode='lines', name='Avg Humidity (%)',
            line=dict(dash=line_style),
            yaxis='y2'))

        # Update layout for dual y-axes and user-selected ranges
        fig2.update_layout(
            title="Temperature and Humidity Trends Over Time",
            xaxis_title="Date",
            yaxis=dict(
                title="Avg Temperature (°C)",
                range=y_axis_range_temp,
                titlefont=dict(color="#1f77b4"),
                tickfont=dict(color="#1f77b4")
            ),
            yaxis2=dict(
                title="Avg Humidity (%)",
                range=y_axis_range_humidity,
                titlefont=dict(color="#ff7f0e"),
                tickfont=dict(color="#ff7f0e"),
                overlaying='y',
                side='right'
            ),
            showlegend=True,
            xaxis_showgrid=show_grid,
            yaxis_showgrid=show_grid
        )

        st.plotly_chart(fig2)

    with chrt:
        col3, col4 = st.columns([4, 2])

        # Display metrics for Avg Temperature, Avg Humidity, and Total Precipitation
        with col4:
            avg_temp = real_df['Avg Temperature (°C)'].mean()
            avg_humidity = real_df['Avg Humidity (%)'].mean()
            total_precipitation = real_df['Total Precipitation (mm)'].sum()

            st.metric(label="Current Temperature (°C)", value=f"{avg_temp:.2f} °C")
            st.metric(label="Current Humidity (%)", value=f"{avg_humidity:.2f} %")
            st.metric(label="Current Precipitation (mm)", value=f"{total_precipitation:.2f} mm")

        # Correlation heatmap
        with col3:
            combined_df = pollen_df[['Count.weed_pollen']].join(
                weather_df[['Avg Temperature (°C)', 'Avg Humidity (%)']]
            )
            corr_matrix = combined_df.corr()

            fig4 = go.Figure(data=go.Heatmap(
                z=corr_matrix.values,
                x=corr_matrix.columns,
                y=corr_matrix.columns,
                colorscale='Viridis'
            ))
            fig4.update_layout(
                title='Correlation Heatmap',
                xaxis_title='Variables',
                yaxis_title='Variables'
            )
            st.plotly_chart(fig4)

with rprt:
    full_report = get_agricultural_response(Ai_key, weather_df, pollen_df, temperature=0.3, max_tokens=4096, top_p=0.9)
    report_sections = full_report.split('---')
    for chapter in report_sections:
        st.markdown(chapter)

with dyrt:
    for i, chapter in enumerate(report_sections):
        # Display each chapter of the report
        st.markdown(chapter)

        # Insert charts between chapters at specific points (e.g., after the first chapter)
        if i == 0:
            # Insert temperature and humidity chart
            st.plotly_chart(fig2)
        elif i == 1:
            # Insert correlation heatmap
            st.plotly_chart(fig4)

        # Insert horizontally stacked current data metrics in a box
        if i == 2:
            avg_temp = real_df['Avg Temperature (°C)'].mean()
            avg_humidity = real_df['Avg Humidity (%)'].mean()
            total_precipitation = real_df['Total Precipitation (mm)'].sum()


            with st.container(border=True):
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(label="Current Temperature (°C)", value=f"{avg_temp:.2f} °C")
                with col2:
                    st.metric(label="Current Humidity (%)", value=f"{avg_humidity:.2f} %")
                with col3:
                    st.metric(label="Current Precipitation (mm)", value=f"{total_precipitation:.2f} mm")

