from dotenv import load_dotenv
import os

# load .env
api_key = os.getenv("API_KEY")
geo_url = os.getenv("GEO_URL")
weather_url = os.getenv("WEATHER_URL")
db_url = os.getenv("DB_URL")
output_path = os.getenv("OUTPUT_FILE")
city = os.getenv("GEO_FALLBACK_CITY")
loc_longitude = os.getenv("LOC_LONG")
loc_latitude = os.getenv("LOC_LATI")
