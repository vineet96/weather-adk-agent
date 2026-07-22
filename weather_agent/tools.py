"""
Weather Tools for the Google ADK Weather Agent.
Provides current weather conditions, multi-day forecasts, and climate metrics.
"""

from typing import Dict, Any, List
import random
import datetime

def get_current_weather(location: str, unit: str = "celsius") -> Dict[str, Any]:
    """
    Fetches the current weather conditions for a given location.

    Args:
        location: City name or location string (e.g. 'San Francisco, CA', 'Tokyo', 'London').
        unit: Temperature unit ('celsius' or 'fahrenheit'). Defaults to 'celsius'.

    Returns:
        Dict containing current temperature, condition, humidity, wind speed, UV index, and AQI.
    """
    loc_clean = location.strip().title()
    
    # Deterministic mock data generation based on location hash
    seed = sum(ord(c) for c in loc_clean)
    random.seed(seed)

    base_temp_c = random.randint(12, 28)
    if "san francisco" in loc_clean.lower():
        base_temp_c = 18
        condition = "Partly Cloudy"
    elif "tokyo" in loc_clean.lower():
        base_temp_c = 22
        condition = "Sunny"
    elif "london" in loc_clean.lower():
        base_temp_c = 15
        condition = "Light Rain"
    elif "new york" in loc_clean.lower():
        base_temp_c = 24
        condition = "Clear"
    else:
        conditions = ["Sunny", "Partly Cloudy", "Clear", "Overcast", "Breezy"]
        condition = conditions[seed % len(conditions)]

    temp = base_temp_c if unit.lower() == "celsius" else int(base_temp_c * 9/5 + 32)
    feels_like = temp + random.randint(-2, 2)
    humidity = random.randint(40, 85)
    wind_speed = random.randint(5, 25)
    uv_index = random.randint(1, 9)
    aqi = random.randint(20, 65)

    return {
        "status": "success",
        "location": loc_clean,
        "temperature": temp,
        "unit": "°C" if unit.lower() == "celsius" else "°F",
        "feels_like": feels_like,
        "condition": condition,
        "humidity_percent": humidity,
        "wind_speed_kmh": wind_speed,
        "uv_index": uv_index,
        "air_quality_index": aqi,
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }


def get_weather_forecast(location: str, days: int = 5, unit: str = "celsius") -> Dict[str, Any]:
    """
    Retrieves a multi-day weather forecast for a specified location.

    Args:
        location: City name or location string.
        days: Number of forecast days (1 to 7). Defaults to 5.
        unit: Temperature unit ('celsius' or 'fahrenheit'). Defaults to 'celsius'.

    Returns:
        Dict containing daily forecast records with highs, lows, conditions, and rain probability.
    """
    days = max(1, min(7, days))
    current_data = get_current_weather(location, unit)
    base_temp = current_data["temperature"]
    temp_unit = current_data["unit"]

    conditions_pool = ["Sunny", "Partly Cloudy", "Rain Showers", "Clear", "Thunderstorms", "Overcast"]
    
    forecast_days: List[Dict[str, Any]] = []
    today = datetime.date.today()

    for i in range(days):
        day_date = today + datetime.timedelta(days=i)
        day_name = "Today" if i == 0 else day_date.strftime("%A")
        
        high_temp = base_temp + random.randint(1, 5) - i % 2
        low_temp = base_temp - random.randint(3, 8) + i % 2
        rain_prob = random.choice([10, 20, 40, 70, 85])
        cond = current_data["condition"] if i == 0 else conditions_pool[(hash(location) + i) % len(conditions_pool)]

        forecast_days.append({
            "day": day_name,
            "date": day_date.isoformat(),
            "high": high_temp,
            "low": low_temp,
            "condition": cond,
            "precipitation_chance_percent": rain_prob
        })

    return {
        "status": "success",
        "location": current_data["location"],
        "unit": temp_unit,
        "forecast_days": forecast_days,
        "summary": f"{days}-day forecast for {current_data['location']}: temperatures ranging from {min(d['low'] for d in forecast_days)}{temp_unit} to {max(d['high'] for d in forecast_days)}{temp_unit}."
    }
