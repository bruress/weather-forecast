import requests
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, Date, DateTime

# load .env
load_dotenv() 
api_key = os.getenv("API_KEY")
geo_url = os.getenv("GEO_URL")+"/json/"
weather_url = os.getenv("WEATHER_URL")
geo_city = os.getenv("")
db_url = os.getenv("")
db_user = os.getenv("")
db_password = os.getenv("")


# agr data
min_temps = []
max_temps = []
hums = []
winds = []
descrs= []

mins_temps = []
maxs_temps = []
avrs_hums = []
maxs_winds = []
weaher_descrs= []

# create db
engine = create_engine("sqlite:///db/database.db") 
metadata = MetaData() # to store table definitions

# create table
table = Table (
    "weather_forecast", metadata,
    Column ("id", Integer, primary_key=True),
    Column ("city", String, nullable=False),
    Column ("forecast_date", Date, nullable=False),
    Column ("temp_min", Float, nullable=False),
    Column ("temp_max", Integer, nullable=False),
    Column ("humidity", Integer, nullable=False),
    Column ("wind_speed", Float, nullable=False),
    Column ("description", String, nullable=False),
    Column ("created_at", DateTime, nullable=False)
)

metadata.create_all(engine)
print("Database and table are created!")

# getting geolocation
data_local = requests.get(geo_url)
json_local = data_local.json()

status_local = json_local["status"]
Xrl_local = data_local.headers["X-Rl"]

# errors
if status_local == "fail":
    print("Error getting geolocation")
elif Xrl_local == 0:
    print("Request limit exceeded")
else:
    city, loc_latitude, loc_longitude = json_local["city"], json_local["lat"], json_local["lon"] 
    if city == "" or loc_longitude == 0.0 or loc_latitude == 0.0:
        print("Incorrect data")
        exit

# weather
url_weather = (f'{weather_url}/data/2.5/forecast?lat={loc_latitude}&lon={loc_longitude}&appid={api_key}&units=metric&lang=ru')
weather = requests.get(url_weather)
data_weather = weather.json()

status_weather = data_weather["cod"]
code_weather = weather.status_code

# errors
if status_weather == 401 or code_weather == 401:
    print("Incorrect API key")
elif status_weather == 404 or code_weather == 404:
    print("Incorrect city")
elif code_weather == 429:
    print("Request limit exceeded")
elif code_weather >= 500:
    print("Network error")
else: 
    # save
    for item in data_weather["list"]:
        min_temps.append(item["main"]["temp_min"])
        max_temps.append(item["main"]["temp_max"])
        hums.append(item["main"]["humidity"])
        winds.append(item["wind"]["speed"])
        descrs.append(item["weather"][0]["description"])

    for i in range (0, 40, 8):
        mins_temps.append(min(min_temps[i:i+8]))
        maxs_temps.append(max(max_temps[i:i+8]))
        avrs_hums.append(sum(hums[i:i+8])/8)
        maxs_winds.append(min(winds[i:i+8]))
        weaher_descrs.append(descrs[i+4])

# pi.openweathermap.org - для местоположения
# http://ip-api.com/json/" - для прогноза погоды
# SQLite через SQLAlchemy (ORM‑подход)
# python-dotenv
# markdown
# github