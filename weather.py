import os
import logging
from logging.handlers import TimedRotatingFileHandler
import requests
from dotenv import load_dotenv

load_dotenv()

# Rotate log weekly on Monday, keep 1 previous week as backup
handler = TimedRotatingFileHandler(
    'weather.log',
    when='W0',
    interval=1,
    backupCount=1
)
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)

API_KEY = os.getenv("API_KEY")
LAT = os.getenv("LAT")
LON = os.getenv("LON")

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather():
    params = {
        "lat": LAT,
        "lon": LON,
        "appid": API_KEY,
        "units": "imperial"
    }
    response = requests.get(BASE_URL, params=params, timeout=10)
    response.raise_for_status()
    return response.json()

def format_weather(data):
    description = data["weather"][0]["description"].title()
    temp = round(data["main"]["temp"])
    feels_like = round(data["main"]["feels_like"])
    humidity = data["main"]["humidity"]
    wind = data["wind"]["speed"]
    city_name = data["name"]

    return (
        f"Weather update:\n"
        f"Weather in {city_name}:\n"
        f"Description: {description}\n"
        f"Temperature: {temp}°F\n"
        f"Feels Like: {feels_like}°F\n"
        f"Humidity: {humidity}%\n"
        f"Wind Speed: {wind} mph"
    )

if __name__ == "__main__":
    try:
        data = get_weather()
        summary = format_weather(data)
        logging.info("Weather data retrieved successfully.\n%s", summary)
        print(summary)
    except requests.exceptions.HTTPError as e:
        logging.error("API error: %s", e.response.status_code)
    except requests.exceptions.ConnectionError:
        logging.error("No internet connection.")
    except requests.exceptions.Timeout:
        logging.error("Request timed out.")
    except KeyError as e:
        logging.error("Unexpected response format - missing key: %s", e)