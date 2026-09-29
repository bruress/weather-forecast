import requests
from datetime import date, timedelta, datetime, timezone

def define_weather (api_key, weather_url, loc_latitude, loc_longitude): 

    try: 
        url_weather = (f'{weather_url}/data/2.5/forecast?lat={loc_latitude}&lon={loc_longitude}&appid={api_key}&units=metric&lang=ru')
        res = requests.get(url_weather)
        code = res.status_code

        # errors
        if code == 401:
            raise ValueError("Incorrect API key")
        elif code == 404:
            raise ValueError("Incorrect city")
        elif code == 429:
            raise ValueError("Request limit exceeded")
        elif code >= 500:
            raise ValueError("Server error")
        elif code != 200:
            raise ValueError("HTTP error")

        data = res.json()
        city = data["city"]["name"]

        # current day, because first day now always has 8 points
        today = datetime.now(timezone.utc).date()

        # arg data
        dates = []
        min_temps = []
        max_temps = []
        hums = []
        winds = []
        descrs= []


        for item in data["list"]:
            dates.append(date.fromisoformat(item["dt_txt"][:10]))
            min_temps.append(item["main"]["temp_min"])
            max_temps.append(item["main"]["temp_max"])
            hums.append(item["main"]["humidity"])
            winds.append(item["wind"]["speed"])
            descrs.append(item["weather"][0]["description"])

        # data by date
        forecast_dates = []
        mins_temps = []
        maxs_temps = []
        avrs_hums = []
        maxs_winds = []
        weaher_descrs= []


        for i in range (0, 4):

            day = today + timedelta(days=i)

            start = dates.index(day)
            count = dates.count(day)
            end = start + count


            forecast_dates.append(day)
            mins_temps.append(min(min_temps[start:end]))
            maxs_temps.append(max(max_temps[start:end]))
            avrs_hums.append(round(sum(hums[start:end])/count))
            maxs_winds.append(max(winds[start:end]))

            day_descr = descrs[start:end]
            weaher_descrs.append(max(day_descr, key=day_descr.count))
    
        return (city, forecast_dates, mins_temps, maxs_temps, avrs_hums, maxs_winds, weaher_descrs)

    except Exception as error:
        print(f"Weather error: {error}")
        return None
