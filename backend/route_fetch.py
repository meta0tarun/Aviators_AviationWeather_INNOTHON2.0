import requests
from typing import Dict, List, Union
from airport_coords import get_airport_coords
from great_circle import calculate_great_circle_distance
from rev_geocode import reverse_geocode

AVSTACK_API_KEY = "d00fce0a370910f6dd4cb4c1bce2dc26"

def get_route_from_aviationstack(flight_number: str) -> List[Dict[str, Union[float, str]]]:
    """Get flight route waypoints from Aviationstack API"""
    url = f"http://api.aviationstack.com/v1/flights?access_key={AVSTACK_API_KEY}&flight_iata={flight_number}"
    try:
        response = requests.get(url, timeout=15)
        data = response.json()
        if data.get("data"):
            flight = data["data"][0]
            dep = flight.get("departure", {}).get("iata", "UNK")
            arr = flight.get("arrival", {}).get("iata", "UNK")
            dep_coords = get_airport_coords(dep)
            arr_coords = get_airport_coords(arr)

            if dep_coords is not None and arr_coords is not None:

                lat1, lon1 = dep_coords
                lat2, lon2 = arr_coords
                mid_lat = (lat1 + lat2) / 2
                mid_lon = (lon1 + lon2) / 2
                distance = calculate_great_circle_distance(lat1, lon1, lat2, lon2)
                
                return [
                    {"lat": lat1, "lon": lon1, "alt": 10000, "name": reverse_geocode(lat1, lon1),
                     "type": "departure", "iata": dep},
                    {"lat": mid_lat, "lon": mid_lon, "alt": 11000, "name": reverse_geocode(mid_lat, mid_lon),
                     "type": "midpoint", "distance": distance},
                    {"lat": lat2, "lon": lon2, "alt": 9000, "name": reverse_geocode(lat2, lon2),
                     "type": "arrival", "iata": arr},
                ]
    except Exception as e:
        print(f"[ERROR] Flight route lookup failed: {e}")
    
    # Fallback with minimal data structure
    return [
        {"lat": 0, "lon": 0, "alt": 0, "name": "Unknown", "type": "departure", "iata": "UNK"},
        {"lat": 0, "lon": 0, "alt": 0, "name": "Midpoint", "type": "midpoint", "distance": "Unknown"},
        {"lat": 0, "lon": 0, "alt": 0, "name": "Unknown", "type": "arrival", "iata": "UNK"}
    ]
