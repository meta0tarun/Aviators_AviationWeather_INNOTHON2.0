import requests
import datetime

OPENWEATHER_API_KEY = "d532b7350a922854f5f8a44e8c13cd73"

def get_forecast_weather(lat: float, lon: float, forecast_offset_hours: int = 0) -> str:
    """Get weather forecast for specific coordinates and time offset"""
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if "list" in data:
            target_time = datetime.datetime.utcnow() + datetime.timedelta(hours=forecast_offset_hours)
            closest = min(
                data["list"],
                key=lambda entry: abs(datetime.datetime.strptime(entry["dt_txt"], "%Y-%m-%d %H:%M:%S") - target_time)
            )
            desc = closest["weather"][0]["description"]
            wind = closest["wind"]["speed"]
            temp = closest["main"]["temp"]
            time_str = closest["dt_txt"]
            return f"{desc.capitalize()}, {temp}°C, wind {wind} m/s (forecast for {time_str} UTC)"
    except Exception as e:
        print(f"[WARN] Weather fetch failed at ({lat}, {lon}): {e}")
    return "Weather data unavailable"