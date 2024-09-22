from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential



def get_agricultural_response(auth_token, df1, df2, temperature=0.3, max_tokens=4096, top_p=0.9):
    # Convert DataFrames to a string format that can be included in the message
    df1_str = df1.to_string(index=False)
    df2_str = df2.to_string(index=False)

    user_msg = f"Current and historical data:\n{df1_str}\n\nForecasted data:\n{df2_str}"

    # Create the client
    client = ChatCompletionsClient(
        endpoint="https://models.inference.ai.azure.com/",
        credential=AzureKeyCredential(auth_token),
    )

    # Prepare messages
    system_msg = "You will be provided with two tables containing weather and agriculture data: one with current and historical data, and another with forecasted data. Your task is to analyze this data by comparing current conditions with historical trends and forecasts. Identify patterns, anomalies, and key agricultural impacts such as optimal farming periods, weather-related risks, and crop suitability based on soil and temperature conditions. Generate a concise and insightful report tailored to farmers, offering actionable advice on irrigation, planting, harvesting, and resource management to help improve farm productivity. Add --- between each 2 chapters make chapters ## and title #"

    # Create messages to be sent to the model
    messages = [
        SystemMessage(content=system_msg),
        UserMessage(content=user_msg),
    ]

    # Get the response
    response = client.complete(
        messages=messages,
        model="Cohere-command-r",
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p
    )

    # Return the content of the response
    return response.choices[0].message.content

def get_agricultural_chat(auth_token, user_input, location,df1,df2, temperature=0.3, max_tokens=4096, top_p=0.9):
    # Create the client
    client = ChatCompletionsClient(
        endpoint="https://models.inference.ai.azure.com/",
        credential=AzureKeyCredential(auth_token),
    )

    # Prepare messages
    system_msg = f"""You will be provided with a prompt requesting a custom statistic about agriculture, along with the user's location data {location}, and current data collected from this same location {df1} and {df2}
    Output the following in Markdown format:
    1. Title
    2. **Statistics Paragraph**: Write a concise paragraph summarizing the statistics provided.
    ---
    3. Statistics paragraph from {df1}
    ---
    4. Statistics paragraph from {df2}
    """

    # Create messages to be sent to the model
    messages = [
        SystemMessage(content=system_msg),
        UserMessage(content=user_input),
    ]

    # Get the response
    response = client.complete(
        messages=messages,
        model="gpt-4o-mini",
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p
    )

    # Return the content of the response
    return response.choices[0].message.content