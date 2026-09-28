import requests
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, func, Integer, String, Date, DateTime, Float, UniqueConstraint, select
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, sessionmaker
from datetime import date, timedelta, datetime

# load .env
load_dotenv() 
api_key = os.getenv("API_KEY")
geo_url = os.getenv("GEO_URL")+"/json/"
weather_url = os.getenv("WEATHER_URL")
geo_city = os.getenv("GEO_FALLBACK_CITY")
db_url = os.getenv("DB_URL")

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

# create sqlite
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
session = Session()

# create db
Base = declarative_base()

class WeatherForecast (Base):
    __tablename__ = "weather_forecast"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    city: Mapped[str] = mapped_column(String, nullable=False)
    forecast_date: Mapped[date] = mapped_column(Date, nullable=False)
    temp_min: Mapped[float] = mapped_column(Float, nullable=False)
    temp_max: Mapped[float] = mapped_column(Float, nullable=False)
    humidity: Mapped[int] = mapped_column(Integer, nullable=False)
    wind_speed: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    __table_args__ = (
        UniqueConstraint(
            "city",
            "forecast_date"
        ),
    )

# create table and database
Base.metadata.create_all(engine)
print("Database and table are created!")

# getting geolocation
data_local = requests.get(geo_url)
json_local = data_local.json()

status_local = json_local["status"]
Xrl_local = int(data_local.headers["X-Rl"])

# errors
if status_local == "fail":
    print("Error getting geolocation")
    city=geo_city
    loc_longitude=49.688891
    loc_latitude=58.573577
elif Xrl_local == 0:
    print("Request limit exceeded")
    city=geo_city
    loc_longitude=49.688891
    loc_latitude=58.573577
else:
    city, loc_latitude, loc_longitude = json_local["city"], json_local["lat"], json_local["lon"] 
    if city == "" or loc_longitude == 0.0 or loc_latitude == 0.0:
        print("Incorrect data")
        city=geo_city
        loc_longitude=49.688891
        loc_latitude=58.573577
        
# weather
url_weather = (f'{weather_url}/data/2.5/forecast?lat={loc_latitude}&lon={loc_longitude}&appid={api_key}&units=metric&lang=ru')
weather = requests.get(url_weather)
data_weather = weather.json()

status_weather = data_weather["cod"]
code_weather = int(weather.status_code)
city = data_weather["city"]["name"]

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
        maxs_winds.append(max(winds[i:i+8]))
        weaher_descrs.append(descrs[i+4])

# current day
curr_date = date.today()

# insert
for i in range (0, 4):
    exist = session.scalars(
        select(WeatherForecast).where(
            WeatherForecast.city == city,
            WeatherForecast.forecast_date == curr_date
        )
    )

    if exist is None:
        insert_stmt = WeatherForecast(
            city=city,
            forecast_date = curr_date,
            temp_min = mins_temps[i],
            temp_max = max_temps[i],
            humidity = avrs_hums[i],
            wind_speed = maxs_winds[i],
            description = weaher_descrs[i],
            created_at = func.now()
        )
        session.add(insert_stmt)
    curr_date += timedelta(days=1)

session.commit()

rows = session.scalars(
    select(WeatherForecast).order_by(WeatherForecast.forecast_date)).all()

with open("weather.md", "w", encoding="utf-8") as file:
    file.write(f"# Прогноз погоды в городе на 4 дня: {rows[0].city}\n\n")
    file.write(f"**Период:** {rows[0].forecast_date} - {rows[-1].forecast_date}\n\n")
    file.write("| Дата | Мин. °C | Макс. °C | Описание | Влажность % | Ветер м/с |\n")
    file.write("|---|---:|---:|---|---:|---:|\n")
    for row in rows:
        file.write(
            f"| {row.forecast_date}"
            f"| {row.temp_min}"
            f"| {row.temp_max}"
            f"| {row.description}"
            f"| {row.humidity}"
            f"| {row.wind_speed} |\n"
        )


# if __name__ == "__main__":
#     main()


# pi.openweathermap.org - для местоположения
# http://ip-api.com/json/" - для прогноза погоды
# SQLite через SQLAlchemy (ORM‑подход)
# python-dotenv
# markdown
# github