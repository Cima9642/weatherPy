# 🌤️ Weather Notifier

A Python app that checks the weather daily, sends a push notification with the summary, and updates a Govee smart light to visually reflect current conditions. Runs unattended on a Raspberry Pi via cron.

## Features

- Fetches live weather data from the OpenWeatherMap API
- Sends a daily summary via push notification ([ntfy.sh](https://ntfy.sh))
- Sends a failure alert if the check fails — no silent failures
- Changes a Govee smart light's color based on current weather condition (clear, cloudy, rain, snow, thunderstorm, fog)
- Scales the light's brightness based on temperature
- Weekly log rotation
- Fully portable via environment-based config (tested on x86 and ARM/Raspberry Pi)

## Tech Stack

Python 3 · `requests` · `python-dotenv` · built-in `logging` · [OpenWeatherMap API](https://openweathermap.org/api) · [ntfy.sh](https://ntfy.sh) · [Govee API](https://developer.govee.com) · `cron`

## Setup

```bash
git clone https://github.com/your-username/weather-py.git
cd weather-py
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file:

```
API_KEY=your_openweathermap_api_key
LAT=your_latitude
LON=your_longitude
NTFY_TOPIC=your_unique_ntfy_topic
GOVEE_API_KEY=your_govee_api_key
GOVEE_DEVICE=your_govee_device_mac_id
GOVEE_SKU=your_govee_device_model
```

- Get an API key from [OpenWeatherMap](https://openweathermap.org/api)
- Install the [ntfy app](https://ntfy.sh/) and subscribe to your chosen topic
- Get a Govee API key via the Govee Home app (Settings → Apply for API Key), then find your device's `device` (MAC ID) and `sku` (model) by calling the [Govee device list endpoint](https://developer.govee.com/reference/get-you-devices)

Run it:

```bash
python weather.py
```

## Scheduling

```bash
crontab -e
```

```
0 7 * * * /path/to/weather-py/.venv/bin/python /path/to/weather-py/weather.py
```

Runs daily at 7:00 AM. File paths in the script are resolved relative to the script's location, so it works correctly regardless of cron's working directory.

## Future Improvements

- Multi-day forecast
- Severe weather alerts
- Configurable notification schedule
- Support for multiple Govee lights simultaneously

## License

MIT
