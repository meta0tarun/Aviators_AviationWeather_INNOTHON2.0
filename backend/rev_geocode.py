import requests

OPENCAGE_API_KEY = "e904125c22864bf6a82e097d7c186d74"

def reverse_geocode(lat: float, lon: float) -> str:
    """Convert coordinates to human-readable location"""
    try:
        url = f"https://api.opencagedata.com/geocode/v1/json?q={lat}+{lon}&key={OPENCAGE_API_KEY}"
        response = requests.get(url, timeout=10)
        results = response.json().get("results", [])
        if results:
            return results[0]["formatted"]
    except Exception as e:
        print(f"[WARN] Reverse geocoding failed for {lat},{lon}: {e}")
    return f"Location at {lat:.4f},{lon:.4f}"
