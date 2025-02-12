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

def ask_chatgpt(weather_data: dict) -> str:
    """
    Send the weather data and a prompt to ChatGPT API and return the answer.
    """
    prompt = (
        "According to above details is it rainy day or not, "
        "give me details in percentage format like 10%, 23% or any. "
        "Make sure no give any other response, since your response now use by API. "
        "just value and the percentage mark only.\n\n"
        f"Weather data: {weather_data}"
    )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or any available model you prefer
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
def weather_check(lat: float = 44.34, lon: float = 10.99):
    """
    API endpoint to check weather. It fetches the current weather data for the
    given latitude and longitude, sends it to ChatGPT, and returns a percentage value.
    """
    # Fetch weather data from OpenWeather API
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

    # Ask ChatGPT for the percentage response, retrying up to 3 times if needed
    result = None
    for _ in range(3):
        result = ask_chatgpt(weather_data)
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
