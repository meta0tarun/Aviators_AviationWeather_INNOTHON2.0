from typing import Optional, Dict
from forecast import get_forecast_weather
from route_fetch import get_route_from_aviationstack
from openai import generate_summary


def run_pipeline(flight_number: str, forecast_offset: int = 0, return_data: bool = False) -> Optional[Dict]:
    """Main pipeline to analyze flight weather"""
    print(f"\n🔍 Analyzing flight: {flight_number} (Offset: {forecast_offset}h)")
    flight_info = {"callsign": flight_number}
    
    print("🛫 Fetching route data...")
    waypoints = get_route_from_aviationstack(flight_number)
    
    if not waypoints:
        print("⚠️ Failed to retrieve flight path")
        return None if not return_data else {"error": "Failed to retrieve flight path"}

    print(f"🌤️ Collecting weather forecasts (offset: {forecast_offset}h)...")
    weather_report = []
    for wp in waypoints:
        forecast = get_forecast_weather(float(wp["lat"]), float(wp["lon"]), forecast_offset)
        weather_report.append(
            f"{str(wp['type']).upper()} - {wp['name']}\n"
            f"• Coordinates: {wp['lat']:.4f}, {wp['lon']:.4f}\n"
            f"• Altitude: {wp['alt']}m\n"
            f"• Weather: {forecast}\n"
        )
    
    print("\n🔍 Generating safety summary...")
    summary = generate_summary(flight_info, "\n".join(weather_report), waypoints)
    
    if return_data:
        return {
            "flight_number": flight_number,
            "forecast_offset": forecast_offset,
            "waypoints": [wp['name'] for wp in waypoints],
            "weather_data": weather_report,
            "summary": summary
        }
    else:
        print("\n✈️ FLIGHT ANALYSIS REPORT")
        print("="*40)
        print(f"Flight: {flight_number}")
        print(f"Route: {waypoints[0]['name']} → {waypoints[-1]['name']}")
        if waypoints[1]['distance'] != "Unknown":
            print(f"Distance: {waypoints[1]['distance']} km")
        print("\n" + "\n".join(weather_report))
        print("\n🚨 WEATHER SAFETY BRIEFING:")
        print("="*40)
        print(summary)
        print("="*40)
        return None

if __name__ == "__main__":
    # Example direct usage
    run_pipeline("BA112", forecast_offset=3)