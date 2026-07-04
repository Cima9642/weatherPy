# 🌤️ Weather Notifier

A lightweight Python application that fetches real-time weather data for a fixed location and delivers a daily summary via push notification. Built to run unattended on a Raspberry Pi using cron for scheduling.

## Features

- Fetches live weather data (temperature, conditions, humidity, wind) from the OpenWeatherMap API
- Sends a formatted daily summary as a push notification via [ntfy.sh](https://ntfy.sh)
- Sends a failure alert if the check fails (bad API response, no internet, timeout) — no silent failures
- Rotating log files (weekly rotation, one week of backup retained)
- Runs automatically on a schedule via cron
- Fully portable: environment-based configuration means no code changes are needed between machines (tested across x86 dev machine and ARM-based Raspberry Pi)

## How it works

1. A cron job triggers the script once daily
2. The script requests current weather data for a fixed latitude/longitude from OpenWeatherMap
3. The response is parsed and formatted into a human-readable summary
4. The summary is logged locally and pushed as a notification to a subscribed device
5. If any step fails, an error is logged and a failure notification is sent instead

## Tech Stack

- **Python 3**
- [`requests`](https://pypi.org/project/requests/) — HTTP requests to the weather API and notification service
- [`python-dotenv`](https://pypi.org/project/python-dotenv/) — environment variable management
- Python's built-in `logging` module with `TimedRotatingFileHandler`
- [OpenWeatherMap API](https://openweathermap.org/api) — weather data source
- [ntfy.sh](https://ntfy.sh) — free, open-source push notification service
- `cron` — task scheduling

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/your-username/weather-py.git
cd weather-py
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate   # or .venv/bin/activate.fish for fish shell
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:
