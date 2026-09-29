

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