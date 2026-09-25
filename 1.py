import requests

# getting geolocation
url_local = "http://ip-api.com/json/"
data_local = requests.get(url_local).json()

status_local = data_local["status"]
Xrl_local = data_local.headers["X-Rl"]

# errors
if status_local == "fail":
    print("Error getting geolocation")
elif Xrl_local == 0:
    print("Request limit exceeded")
else:
    city, loc_latitude, loc_longitude = data_local["city"], data_local["lat"], data_local["lon"] 
    if city == "" or loc_longitude == 0.0 or loc_latitude == 0.0:
        print("Incorrect data")

# pi.openweathermap.org - для местоположения
# http://ip-api.com/json/" - для прогноза погоды
# SQLite через SQLAlchemy (ORM‑подход)
# python-dotenv
# markdown
# github