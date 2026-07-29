import os
import uuid
import logging
from logging.handlers import TimedRotatingFileHandler
import requests
from dotenv import load_dotenv


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

load_dotenv(os.path.join(SCRIPT_DIR, ".env"))

# Rotate log weekly on Monday, keep 1 previous week as backup
handler = TimedRotatingFileHandler(
    os.path.join(SCRIPT_DIR, "weather.log"),
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

GOVEE_API_KEY = os.getenv("GOVEE_API_KEY")
GOVEE_DEVICE = os.getenv("GOVEE_DEVICE")
GOVEE_SKU = os.getenv("GOVEE_SKU")
GOVEE_BASE_URL = "https://openapi.api.govee.com/router/api/v1/device/control"

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

NTFY_TOPIC = os.getenv("NTFY_TOPIC")


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
        
        f"Weather in {city_name}:\n"
        f"Description: {description}\n"
        f"Temperature: {temp}°F\n"
        f"Feels Like: {feels_like}°F"
        f"Humidity: {humidity}%\n"
        f"Wind Speed: {wind} mph"
    )

def send_notification(summary):
    requests.post(
        f"https://ntfy.sh/{NTFY_TOPIC}",
        data=summary.encode("utf-8"),
        headers={"Title": "Daily Weather Update"}
    )
    
def get_color_for_condition(condition_id):
    if 200 <= condition_id < 300:
        return (128,0,128) # Purple for Thunderstorm
    elif 300 <= condition_id < 400:
        return (100,149,237) # Light Blue for Drizzle
    elif 500 <= condition_id < 600:
        return (0,0,255) # Blue for Rain
    elif 600 <= condition_id < 700:
        return (255,255,255) # White for Snow
    elif 700 <= condition_id < 800:
        return (169, 169, 169) # Gray for Fog/mist/Haze
    elif condition_id == 800:
        return (255,140,0) # Orange for Clear
    elif 801 <= condition_id <= 804:
        return (128,128,128) # Teal for Clouds
    else:
        return (255, 255, 255) # Fallback to White for unknown conditions
    
def get_brightness_for_temp(temp_f):
    min_temp, max_temp = 30, 100
    min_brightness, max_brightness = 20, 100
    
    clamped_temp = max(min_temp, min(temp_f, max_temp))
    ratio = (clamped_temp - min_temp) / (max_temp - min_temp)
    brightness = min_brightness + ratio * (max_brightness - min_brightness)
    
    return round(brightness)

def set_light_color(r, g, b):
    color_int = (r << 16) | (g << 8) | b
    payload = {
        "requestId": str(uuid.uuid4()),
        "payload": {
            "sku": GOVEE_SKU,
            "device": GOVEE_DEVICE,
            "capability": {
                "type": "devices.capabilities.color_setting",
                "instance": "colorRgb",
                "value": color_int
            }
        }
    }
    headers = {
        "Content-Type": "application/json",
        "Govee-API-Key": GOVEE_API_KEY
    }
    requests.post(GOVEE_BASE_URL, json=payload, headers=headers, timeout=10)

    
def set_light_brightness(percent):
    payload = {
        "requestId": str(uuid.uuid4()),
        "payload": {
            "sku": GOVEE_SKU,
            "device": GOVEE_DEVICE,
            "capability": {
                "type": "devices.capabilities.range",
                "instance": "brightness",
                "value": percent
            }
        }
    }
    headers = {
        "Content-Type": "application/json",
        "Govee-API-Key": GOVEE_API_KEY
    }
    requests.post(GOVEE_BASE_URL, json=payload, headers=headers, timeout=10)
    
    
if __name__ == "__main__":
    try:
        data = get_weather()
        summary = format_weather(data)
        logging.info("Weather data retrieved successfully.\n%s", summary)
        print(summary)
        send_notification(summary)

        condition_id = data["weather"][0]["id"]
        temp = data["main"]["temp"]
        r, g, b = get_color_for_condition(condition_id)
        brightness = get_brightness_for_temp(temp)

        set_light_color(r, g, b)
        set_light_brightness(brightness)
        logging.info("Light updated: color=(%d,%d,%d), brightness=%d%%", r, g, b, brightness)

    except requests.exceptions.HTTPError as e:
        logging.error("API error: %s", e.response.status_code)
        send_notification(f"Weather check failed: API error {e.response.status_code}")
    except requests.exceptions.ConnectionError:
        logging.error("No internet connection.")
        send_notification("Weather check failed: no internet connection.")
    except requests.exceptions.Timeout:
        logging.error("Request timed out.")
        send_notification("Weather check failed: request timed out.")
    except KeyError as e:
        logging.error("Unexpected response format - missing key: %s", e)
        send_notification(f"Weather check failed: unexpected API response (missing {e}).")