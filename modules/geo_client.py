import requests

def define_geolocation(geo_url, fallback_city, fallback_loc_longitude, fallback_loc_latitude):

    try:
        url_geolocation = (f'{geo_url}/json/')
        res = requests.get(url_geolocation)
        code = res.status_code

        # errors
        if code == 429:
            raise ValueError("Request limit exceeded")
        
        data = res.json()

        if data["status"] != "success":
            raise ValueError("Geolocation error")

        city, loc_latitude, loc_longitude = data["city"], data["lat"], data["lon"]        

        if not city or loc_longitude == None or loc_latitude == None:
            raise ValueError("API format error")

        return city, loc_longitude, loc_latitude

    except Exception as error:
        print(f"Geolocation error: {error}")
        return fallback_city, fallback_loc_longitude, fallback_loc_latitude
