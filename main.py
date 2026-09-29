from modules import config
from modules.db_modules import define_db, insert_table, read_table
from modules.geo_client import define_geolocation
from modules.markdown_client import write_md
from modules.weather_client import define_weather

def main():
    city, loc_longitude, loc_latitude = define_geolocation(config.geo_url, config.city, config.loc_longitude, config.loc_latitude)
    city, forecast_dates, mins_temps, maxs_temps, avrs_hums, maxs_winds, weaher_descrs = define_weather(config.api_key, config.weather_url, loc_latitude, loc_longitude)
    session = define_db(config.db_url)
    insert_table(session, city, forecast_dates, mins_temps, maxs_temps, avrs_hums, maxs_winds, weaher_descrs)
    rows = read_table(session, city, forecast_dates)
    write_md(config.output_path, rows)


if __name__ == "__main__":
    main()
