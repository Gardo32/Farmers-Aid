import streamlit as st
import pandas as pd
import requests
import pycountry
import plotly.express as px
import plotly.graph_objects as go
from pollen import get_combined_pollen_data
from weather import get_combined_weather_data
from AI import get_agricultural_response, get_agricultural_chat
import datetime as dt

# Load the IP API key from the .env file
IPkey = st.secrets["ip"]
Ai_key = st.secrets["github"]

# Function to convert country code to full country name
def get_country_name(country_code):
    try:
        country = pycountry.countries.get(alpha_2=country_code)
        return country.name if country else 'Unknown'
    except Exception:
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
city = "Manama"
country = "Bahrain"
latitude = 26.169422
longitude = 50.552246

# Create a variable with the format City,Country
place = f"Isatown,Bahrain"

# Fetch data
pollen_df = get_combined_pollen_data(place)
real_df, weather_df = get_combined_weather_data(city, latitude, longitude)

# App start from here
dashb, about, faq = st.tabs(["Dashboard 📊", "About Us ℹ️", "FAQ 🔍"])

# Dashboard tab
with dashb:
    At = st.expander("Advance Tweaks", expanded=False)
    chrt, rprt, dyrt, cstm = st.tabs(["📈 Charts", "🗒️ Report", "📊 Dynamic Report", "Custom Statistics 🤖"])

    with At:
        st.write("Use the options below to tweak chart settings:")
        chart_color = st.color_picker("Select Chart Line Color", "#dad6c9")  # Changed default to #1f77b4 for better visibility
        line_style = st.selectbox("Select Line Style", ['solid', 'dot', 'dash'])
        y_axis_range_temp = st.slider("Select Y-axis range for Temperature (°C)", 0, 50, (10, 40))
        y_axis_range_humidity = st.slider("Select Y-axis range for Humidity (%)", 0, 100, (20, 80))
        show_grid = st.checkbox("Show Grid", value=True)

    with chrt:
        col1, col2 = st.columns([4, 6])

        # First chart: Line plot for weed pollen count
        with col1:
            pollen_df['time'] = pd.to_datetime(pollen_df['time'], unit='s')
            fig1 = px.line(pollen_df, x='time', y='Count.weed_pollen',
                           labels={'Count.weed_pollen': 'Weed Pollen Count', 'time': 'Time'},
                           title="Weed Pollen Counts Over Time",
                           line_shape="linear")
            fig1.update_traces(line=dict(color=chart_color))
            st.plotly_chart(fig1)

        # Second chart: Temperature and humidity trends with customization
        # Second chart: Temperature and humidity trends with customization
        with col2:
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(
                x=weather_df['Date'], y=weather_df['Avg Temperature (°C)'],
                mode='lines',
                line=dict(dash=line_style, color='#A3AB30'),
                hovertemplate='Temperature: %{y:.2f} °C<br>Date: %{x}<extra></extra>',  # Custom hover info for temperature
                yaxis='y1'
            ))
            fig2.add_trace(go.Scatter(
                x=weather_df['Date'], y=weather_df['Avg Humidity (%)'],
                mode='lines',
                line=dict(dash=line_style, color=chart_color),
                hovertemplate='Humidity: %{y:.2f} %<br>Date: %{x}<extra></extra>',  # Custom hover info for humidity
                yaxis='y2'
            ))

            fig2.update_layout(
                title="Temperature and Humidity Trends Over Time",  # Remove the title
                xaxis_title="",  # Remove x-axis title
                yaxis=dict(title="", range=y_axis_range_temp,
                           titlefont=dict(color=chart_color), tickfont=dict(color=chart_color)),
                yaxis2=dict(title="", range=y_axis_range_humidity,
                            titlefont=dict(color=chart_color), tickfont=dict(color=chart_color),
                            overlaying='y', side='right'),
                showlegend=False,  # Hide the legend
                xaxis_showgrid=show_grid,
                yaxis_showgrid=show_grid
            )
            st.plotly_chart(fig2)


        # Display metrics for Avg Temperature, Avg Humidity, and Total Precipitation
        col3, col4 = st.columns([4, 2])

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
                yaxis_title='',
                yaxis=dict(showticklabels=False)  # This removes the vertical axis labels
            )
            st.plotly_chart(fig4)

    with rprt:
        full_report = get_agricultural_response(Ai_key, weather_df, pollen_df, temperature=0.3, max_tokens=4096, top_p=0.9)
        report_sections = full_report.split('---')
        date = dt.date.today().strftime("%d %m, %Y")
        st.title(f"Comprehensive Agriculture Report: {place} ({date})")
        for chapter in report_sections:
            st.markdown(chapter)

    with dyrt:
        st.title(f"Dynamic Agriculture Report: {place} ({date})")
        for i, chapter in enumerate(report_sections):
            st.markdown(chapter)

            # Insert charts between chapters at specific points
            if i == 0:
                st.plotly_chart(fig2)
            elif i == 1:
                st.plotly_chart(fig1)

            # Insert horizontally stacked current data metrics in a box
            if i == 2:
                with st.container():
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric(label="Current Temperature (°C)", value=f"{avg_temp:.2f} °C")
                    with col2:
                        st.metric(label="Current Humidity (%)", value=f"{avg_humidity:.2f} %")
                    with col3:
                        st.metric(label="Current Precipitation (mm)", value=f"{total_precipitation:.2f} mm")

    with cstm:
        st.header("Custom Statistics")

        user_input = st.chat_input(f"Ask about agriculture in {place}:")  # Updated prompt

        if user_input:
            # Call the AI function with user input and location
            ai_response = get_agricultural_chat(Ai_key, user_input, place, weather_df, pollen_df, temperature=0.3, max_tokens=4096, top_p=0.9)
            custom_report = ai_response.split('---')
            for chapter in custom_report:
                st.markdown(chapter)
                # Display the first chart (fig1) after the first chapter
                if chapter == custom_report[0]:
                    st.plotly_chart(fig1)
                # Display the second chart (fig2) after the second chapter
                elif chapter == custom_report[1]:
                    st.plotly_chart(fig2)

# About Us tab
with about:
    # Title of the page
    st.title("About Us")

    # Project Overview
    st.header("Project Overview")
    st.write(
        """
        Welcome to **Farmers Aid**! Our project is dedicated to helping farmers make data-driven decisions through real-time data analytics collected from NASA and public APIs. We strive to empower farmers with the insights they need to optimize their practices and improve yields.
        """
    )

    # Team Members Section
    st.header("Meet Our Team")
    team_members = {
        "Mohammed Aldaqaq": "Team Leader & Data Analyst",
        "Ali Alsheikh": "AI Engineer",
        "Mohammed Azan": "UI/UX Designer",
        "Abdulla Hilal": "Web Developer"
    }

    # Display team members in a collapsible section
    with st.expander("Click to view team members"):
        for name, role in team_members.items():
            st.write(f"**{name}**: {role}")

    # Educational Background
    st.header("Our Background")
    st.write(
        """
        We are students at the **Nasser Vocational Training Centre (NVTC)**, where we are learning and developing our skills in technology and data science.
        """
    )

    # App Features Section
    st.header("App Features")
    st.write(
        """
        Our application performs data analytics to produce visual charts and sends the collected data to a large language model (LLM) for report generation. We combine these insights to create dynamic reports tailored to user needs. Additionally, we have developed a custom statistics AI assistant that provides personalized statistics based on user prompts and the provided data.
        """
    )

    # Interactive Feature: Feedback Section
    st.header("We Value Your Feedback!")
    feedback = st.text_area("What do you think about Farmers Aid?", placeholder="Share your thoughts...")
    if st.button("Submit Feedback"):
        if feedback:
            st.success("Thank you for your feedback!")
        else:
            st.warning("Please enter your feedback before submitting.")

# FAQ tab
with faq:
    st.title("Frequently Asked Questions")
    # Define FAQs as a dictionary
    faqs = {
        "What is Farmers Aid?":
            "Farmers Aid is a project dedicated to helping farmers make data-driven decisions through real-time data analytics collected from NASA and public APIs. It aims to empower farmers with insights to optimize their practices and improve yields.",

        "Who is behind Farmers Aid?":
            "The Farmers Aid team consists of students from the Nasser Vocational Training Centre (NVTC):\n"
            "1. Mohammed Aldaqaq - Team Leader & Data Analyst\n"
            "2. Ali Alsheikh - AI Engineer\n"
            "3. Mohammed Azan - UI/UX Designer\n"
            "4. Abdulla Hilal - Web Developer",

        "What is the main goal of Farmers Aid?":
            "The main goal of Farmers Aid is to empower farmers with data-driven insights to optimize their farming practices and improve yields through real-time analytics and dynamic reports.",

        "What does the application do?":
            "The Farmers Aid application performs data analytics to create visual charts, sends the collected data to a large language model (LLM) for report generation, and produces personalized dynamic reports based on user needs. It also includes a custom AI assistant for generating personalized statistics.",

        "Where are the team members from?":
            "The team members are students from the Nasser Vocational Training Centre (NVTC), where they are developing their skills in technology and data science."
    }

    # Create an expandable section for each FAQ
    for question, answer in faqs.items():
        with st.expander(question):
            st.write(answer)
