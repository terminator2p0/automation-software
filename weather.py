import requests
from datetime import datetime

def get_location():
    try:
        # Get external IP
        ip_info = requests.get('https://api64.ipify.org?format=json').json()
        ip = ip_info.get("ip", "")
    except Exception:
        ip = ""

    city = region = country = ""

    if ip:
        # Try ipapi.co for location info
        try:
            loc_resp = requests.get(f'https://ipapi.co/{ip}/json/').json()
            city = loc_resp.get("city", "")
            region = loc_resp.get("region", "")
            country = loc_resp.get("country_name", "")
        except Exception:
            pass

        # If ipapi.co fails to give city, try ipinfo.io
        if not city:
            try:
                loc_resp = requests.get(f'https://ipinfo.io/{ip}/json').json()
                city = loc_resp.get("city", "")
                region = loc_resp.get("region", "")
                country = loc_resp.get("country", "")
            except Exception:
                pass

    return {"ip": ip, "city": city, "region": region, "country": country}

def get_weather(city, api_key):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city},US&appid={api_key}&units=metric"
        weather = requests.get(url, timeout=10).json()
        if weather.get('cod') == 200:
            temp = weather['main']['temp']
            desc = weather['weather'][0]['description']
            return f"{temp}°C, {desc}"
        else:
            return "Weather info not available or city not found"
    except Exception:
        return "Failed to retrieve weather data"

def main():
    print("Detecting your location...")
    loc = get_location()

    # Override detected city with actual known city: Frankfort, KY
    actual_city = "Frankfort"
    actual_region = "Kentucky"
    actual_country = "US"

    loc['city'] = actual_city
    loc['region'] = actual_region
    loc['country'] = actual_country

    print(f"Your IP: {loc['ip']}")
    print(f"Using location: {loc['city']}, {loc['region']}, {loc['country']}")

    # Show current local date and time
    now = datetime.now()
    print("Local Date and Time:", now.strftime('%Y-%m-%d %H:%M:%S'))

    # Enter your OpenWeatherMap API key here
    api_key = "d5553e1536ff4a9f8ccbff09e104f92a"

    if loc['city'] and api_key != "d5553e1536ff4a9f8ccbff09e104f92a" and api_key.strip():
        print(f"Getting weather for {loc['city']}...")
        weather = get_weather(loc['city'], api_key)
        print(f"Current weather in {loc['city']}: {weather}")
    else:
        print("Weather not displayed (API key missing or invalid city)")

if __name__ == "__main__":
    main()
