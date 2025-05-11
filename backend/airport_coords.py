import requests
from typing import Optional

OPENCAGE_API_KEY = "e904125c22864bf6a82e097d7c186d74"

AIRPORT_CACHE = {}

def get_airport_coords(iata: str) -> Optional[tuple]:
    """Get airport coordinates from cache or API"""
    if iata in AIRPORT_CACHE:
        return AIRPORT_CACHE[iata]
    try:
        url = f"https://api.opencagedata.com/geocode/v1/json?q={iata}+airport&key={OPENCAGE_API_KEY}"
        response = requests.get(url, timeout=10)
        results = response.json().get("results", [])
        if results:
            lat = float(results[0]["geometry"]["lat"])
            lon = float(results[0]["geometry"]["lng"])
            AIRPORT_CACHE[iata] = (lat, lon)
            return lat, lon
    except Exception as e:
        print(f"[WARN] Airport coordinate lookup failed for {iata}: {e}")
    return None, None