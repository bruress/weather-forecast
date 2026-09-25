import requests
import os
from dotenv import load_dotenv

# load .env
load_dotenv() 
api_key = os.getenv("API_KEY")

# agr data
min_temps = []
max_temps = []
hums = []
winds = []
descrs= []

# getting geolocation
url_local = "http://ip-api.com/json/"
local = requests.get(url_local)
data_local = local.json()

status_local = data_local["status"]
Xrl_local = local.headers["X-Rl"]

# errors
if status_local == "fail":
    print("Error getting geolocation")
elif Xrl_local == 0:
    print("Request limit exceeded")
else:
    city, loc_latitude, loc_longitude = data_local["city"], data_local["lat"], data_local["lon"] 
    if city == "" or loc_longitude == 0.0 or loc_latitude == 0.0:
        print("Incorrect data")
        exit

# weather
url_weather = (f'https://api.openweathermap.org/data/2.5/forecast?lat={loc_latitude}&lon={loc_longitude}&appid={api_key}&units=metric&lang=ru')
data_weather = requests.get(url_weather).json()
print(data_weather)

# сохраняем все параметры в массивы
for i in data_weather:
    min_temps[i] = data_weather.main.temp_min
    max_temps[i] = data_weather.main.temp_max
    hums[i] = data_weather.main.humidity
    winds[i] = data_weather.main.wind
    descrs[i] = data_weather.main.description

min_temp = min(min_temps)
max_te

# pi.openweathermap.org - для местоположения
# http://ip-api.com/json/" - для прогноза погоды
# SQLite через SQLAlchemy (ORM‑подход)
# python-dotenv
# markdown
# github