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
        url = f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no"
        weather = requests.get(url, timeout=10).json()

        if "error" in weather:
            return "Weather info not available or city not found"

        temp = weather["current"]["temp_c"]
        desc = weather["current"]["condition"]["text"]
        return f"{temp}°C, {desc}"
    except Exception as e:
        return f"Failed to retrieve weather data: {str(e)}"

def main():
    print("Detecting your location...")
    loc = get_location()

    print(f"Your IP: {loc['ip']}")
    print(f"Using location: {loc['city']}, {loc['region']}, {loc['country']}")

    # Show current local date and time
    now = datetime.now()
    print("Local Date and Time:", now.strftime('%Y-%m-%d %H:%M:%S'))

    # WeatherAPI key (replace this with your own if needed)
    api_key = "f6f75279ea3946e696f193206252707"

    if loc['city'] and api_key.strip():
        print(f"Getting weather for {loc['city']}...")
        weather = get_weather(loc['city'], api_key)
        print(f"Current weather in {loc['city']}: {weather}")
    else:
        print("Weather not displayed (API key missing or invalid city)")

if __name__ == "__main__":
    main()