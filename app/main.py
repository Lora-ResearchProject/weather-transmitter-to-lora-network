import re
import requests
import openai
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = FastAPI()

# Enable CORS for all origins (Allow all requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for development)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# API keys and endpoints
openweatherapi = os.getenv("OPENWEATHER_API_KEY")
openweatherurl = os.getenv("OPENWEATHER_URL")
openai.api_key = os.getenv("OPENAI_API_KEY")

def is_valid_percentage(text: str) -> bool:
    """
    Check if the given text is in the form of a percentage,
    e.g., "85%" (only digits followed by a percent sign).
    """
    pattern = r'^\d+%$'
    return re.match(pattern, text.strip()) is not None

def ask_chatgpt(filtered_data: dict) -> str:
    """
    Send the filtered weather data and a prompt to the ChatGPT API and return the answer.
    """
    prompt = (
        "According to the following weather details, is it a rainy day or not? "
        "Provide your answer in percentage format (e.g., 10%, 23%). "
        "Return only the value with a percentage sign, nothing else.\n\n"
        f"Weather details: {filtered_data}"
    )
    response = openai.ChatCompletion.create(
        model=os.getenv("OPENAI_API_MODEL"),  # or any available model you prefer
        messages=[
            {"role": "system", "content": "You are a weather data analyzer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    # Extract and return the ChatGPT answer
    answer = response.choices[0].message.content.strip()
    return answer

@app.get("/weather-check")
def weather_check(lat: float, lon: float):
    """
    API endpoint to check weather.
    The endpoint fetches the current weather data for the provided latitude and longitude,
    filters out necessary fields for determining rain likelihood,
    sends the filtered data to the ChatGPT API, and returns a percentage value.
    """
    # Fetch weather data from OpenWeather API using the provided lat and lon
    params = {
        "lat": lat,
        "lon": lon,
        "appid": openweatherapi
    }
    weather_response = requests.get(openweatherurl, params=params)
    if weather_response.status_code != 200:
        raise HTTPException(
            status_code=weather_response.status_code,
            detail="Error fetching weather data"
        )
    weather_data = weather_response.json()

    # Filter out necessary fields for rain decision
    try:
        filtered_data = {
            "weather_main": weather_data["weather"][0]["main"],
            "weather_description": weather_data["weather"][0]["description"],
            "clouds": weather_data.get("clouds", {}).get("all"),
            "humidity": weather_data.get("main", {}).get("humidity")
        }
    except (KeyError, IndexError) as e:
        raise HTTPException(status_code=500, detail="Error parsing weather data: " + str(e))

    # Ask ChatGPT for the percentage response, retrying up to 3 times if needed
    result = None
    for _ in range(3):
        result = ask_chatgpt(filtered_data)
        if is_valid_percentage(result):
            break

    if not is_valid_percentage(result):
        raise HTTPException(
            status_code=500,
            detail="Failed to get valid percentage response from ChatGPT API"
        )

    return {"rain_percentage": result}

# To run the API, use the command:
# uvicorn your_filename:app --reload
