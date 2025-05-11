from typing import Dict, List
import requests

OPENROUTER_API_KEY = "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"

def generate_summary(flight_info: Dict, weather_data: str, waypoints: List) -> str:
    """Generate weather safety briefing using AI"""
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Safely extract flight details
    flight_number = flight_info.get('callsign', 'Unknown')
    
    # Initialize with defaults
    departure = {'name': 'Unknown', 'iata': 'UNK', 'alt': 'N/A'}
    arrival = {'name': 'Unknown', 'iata': 'UNK', 'alt': 'N/A'}
    midpoint = {'name': 'Midpoint', 'distance': 'Unknown', 'alt': 'N/A'}
    
    # Update with actual data
    for wp in waypoints:
        if wp.get('type') == 'departure':
            departure = {
                'name': wp.get('name', 'Unknown'),
                'iata': wp.get('iata', 'UNK'),
                'alt': wp.get('alt', 'N/A')
            }
        elif wp.get('type') == 'arrival':
            arrival = {
                'name': wp.get('name', 'Unknown'),
                'iata': wp.get('iata', 'UNK'),
                'alt': wp.get('alt', 'N/A')
            }
        elif wp.get('type') == 'midpoint':
            midpoint = {
                'name': wp.get('name', 'Midpoint'),
                'distance': wp.get('distance', 'Unknown'),
                'alt': wp.get('alt', 'N/A')
            }

    model = "openai/gpt-3.5-turbo-0613"
    messages = [
        {"role": "system", "content": """You are an aviation weather safety assistant. Provide concise but 
        comprehensive summaries with:
        1. Flight header with route
        2. Weather observations
        3. Hazard assessment
        4. Recommendations"""},
        
        {"role": "user", "content": f"""
FLIGHT DETAILS:
- Number: {flight_number}
- Route: {departure['name']} ({departure['iata']}) → {arrival['name']} ({arrival['iata']})
- Distance: {midpoint['distance']} km
- Altitudes: Takeoff: {departure['alt']}m | Cruise: {midpoint['alt']}m | Landing: {arrival['alt']}m

WEATHER DATA:
{weather_data}

Generate a professional pilot briefing highlighting:
- Significant weather at each phase
- Potential turbulence/wind shear
- Potential warnings regarding visibility, temperature leading to less air density and humidity while mentioning each waypoint
- Use standard aviation terminology"""}
    ]
    
    try:
        response = requests.post(url, headers=headers, json={
            "model": model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 500
        }, timeout=20)
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        print(f"[ERROR] Summary generation failed: {e}")
        return "Could not generate weather summary due to technical issues"
