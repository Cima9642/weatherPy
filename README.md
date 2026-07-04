# 🌤️ Weather Notifier

A Python app that checks the weather daily and sends a push notification with the summary. Runs unattended on a Raspberry Pi via cron.

## Features

- Fetches live weather data from the OpenWeatherMap API
- Sends a daily summary via push notification ([ntfy.sh](https://ntfy.sh))
- Sends a failure alert if the check fails — no silent failures
- Weekly log rotation
- Fully portable via environment-based config (tested on x86 and ARM/Raspberry Pi)

## Tech Stack

Python 3 · `requests` · `python-dotenv` · built-in `logging` · [OpenWeatherMap API](https://openweathermap.org/api) · [ntfy.sh](https://ntfy.sh) · `cron`

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
```

Get an API key from [OpenWeatherMap](https://openweathermap.org/api), then install the [ntfy app](https://ntfy.sh/) and subscribe to your chosen topic.

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

## License

MIT
