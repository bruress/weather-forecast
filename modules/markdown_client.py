import os

def write_md(output_path, rows):
    if not rows: 
        raise ValueError("No data")
    
    root = os.path.join(os.path.dirname(__file__), "..")
    file_path = os.path.join(root, output_path)

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as file:
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