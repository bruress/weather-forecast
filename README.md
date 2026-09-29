# Weather Forecast

A Python app that finds your city by IP, gets a weather forecast for today and the next 3 days, saves it to SQLite, and creates a Markdown report.

Uses OpenWeatherMap, ip-api.com, requests, SQLAlchemy, and python-dotenv.

## Install

```bash
git clone https://github.com/bruress/weather-forecast.git
cd weather-forecast
pip install sqlalchemy, python-dotenv
cp .env.example .env
```

## Settings

Get an API key at [OpenWeatherMap](https://openweathermap.org/). Add these settings to `.env`:

```dotenv
API_KEY=your_api_key
WEATHER_URL=https://api.openweathermap.org
GEO_URL=http://ip-api.com
GEO_FALLBACK_CITY=Kirov
LOC_LONG=49.6
LOC_LATI=58.6
DB_URL=sqlite:///db/weather.db
OUTPUT_FILE=output/weather.md
```

## Run

```bash
python main.py
```

## Files

- `main.py` — runs the app.
- `modules/config.py` — loads settings.
- `modules/geo_client.py` — finds the city and coordinates.
- `modules/weather_client.py` — gets weather and calculates daily values.
- `modules/db_modules.py` — saves and reads data.
- `modules/markdown_client.py` — writes the report.

## Example

Sample data for Kirov:

| Date       | Min °C | Max °C | Weather  | Humidity % | Wind m/s |
| ---------- | -----: | -----: | -------- | ---------: | -------: |
| 2026-09-29 |    9.5 |   16.9 | пасмурно |         82 |      2.1 |
