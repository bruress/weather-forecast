import requests
from sqlalchemy import create_engine, func, Integer, String, Date, DateTime, Float, UniqueConstraint, select
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, sessionmaker
from datetime import date, timedelta, datetime


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

with open("output_path", "w", encoding="utf-8") as file:
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