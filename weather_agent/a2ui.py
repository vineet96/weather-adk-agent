"""
A2UI (Agent-to-User Interface) Protocol Schema Builders for Weather Agent.

A2UI is a declarative protocol for sending UI component structures in JSON format.
Client applications render these components natively according to their local UI design system.
"""

from typing import Dict, Any, List, Optional

A2UI_SPEC_VERSION = "1.0"

def create_a2ui_weather_card(current_weather: Dict[str, Any]) -> Dict[str, Any]:
    """
    Constructs an A2UI Weather Card component JSON payload.
    """
    location = current_weather.get("location", "Unknown Location")
    temp = current_weather.get("temperature", "--")
    unit = current_weather.get("unit", "°C")
    condition = current_weather.get("condition", "Clear")
    feels_like = current_weather.get("feels_like", temp)
    
    # Map weather conditions to standard A2UI icon identifiers
    icon_map = {
        "Sunny": "sun.max.fill",
        "Clear": "moon.stars.fill",
        "Partly Cloudy": "cloud.sun.fill",
        "Overcast": "cloud.fill",
        "Light Rain": "cloud.drizzle.fill",
        "Rain Showers": "cloud.rain.fill",
        "Thunderstorms": "cloud.bolt.rain.fill",
        "Breezy": "wind"
    }
    icon_id = icon_map.get(condition, "cloud.sun.fill")

    return {
        "component": "Card",
        "id": "weather_main_card",
        "props": {
            "elevation": 2,
            "variant": "gradient",
            "theme": "weather_blue"
        },
        "children": [
            {
                "component": "Header",
                "props": {
                    "title": location,
                    "subtitle": f"Current Conditions • {condition}",
                    "icon": icon_id
                }
            },
            {
                "component": "DisplayTemp",
                "props": {
                    "temperature": f"{temp}{unit}",
                    "feels_like": f"Feels like {feels_like}{unit}",
                    "condition": condition,
                    "size": "large"
                }
            }
        ]
    }


def create_a2ui_metric_grid(current_weather: Dict[str, Any]) -> Dict[str, Any]:
    """
    Constructs an A2UI Grid component for secondary weather metrics.
    """
    return {
        "component": "MetricGrid",
        "id": "weather_metrics_grid",
        "props": {
            "columns": 2,
            "gap": "medium"
        },
        "children": [
            {
                "component": "MetricBadge",
                "props": {
                    "label": "Humidity",
                    "value": f"{current_weather.get('humidity_percent', 0)}%",
                    "icon": "drop.fill",
                    "color": "blue"
                }
            },
            {
                "component": "MetricBadge",
                "props": {
                    "label": "Wind Speed",
                    "value": f"{current_weather.get('wind_speed_kmh', 0)} km/h",
                    "icon": "wind",
                    "color": "teal"
                }
            },
            {
                "component": "MetricBadge",
                "props": {
                    "label": "UV Index",
                    "value": str(current_weather.get("uv_index", 0)),
                    "icon": "sun.max",
                    "color": "orange"
                }
            },
            {
                "component": "MetricBadge",
                "props": {
                    "label": "Air Quality (AQI)",
                    "value": f"{current_weather.get('air_quality_index', 0)} AQI",
                    "icon": "leaf.fill",
                    "color": "green"
                }
            }
        ]
    }


def create_a2ui_forecast_list(forecast_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Constructs an A2UI Forecast List component for multi-day weather forecasts.
    """
    days = forecast_data.get("forecast_days", [])
    unit = forecast_data.get("unit", "°C")

    items = []
    for d in days:
        items.append({
            "component": "ForecastRow",
            "props": {
                "day": d.get("day", ""),
                "date": d.get("date", ""),
                "condition": d.get("condition", "Clear"),
                "high": f"{d.get('high')}{unit}",
                "low": f"{d.get('low')}{unit}",
                "rain_probability": f"{d.get('precipitation_chance_percent')}%"
            }
        })

    return {
        "component": "ForecastList",
        "id": "weather_forecast_list",
        "props": {
            "title": f"Forecast for {forecast_data.get('location', '')}",
            "layout": "vertical"
        },
        "children": items
    }


def wrap_a2ui_payload(components: List[Dict[str, Any]], actions: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    """
    Wraps component definitions into a compliant A2UI root payload envelope.
    """
    default_actions = actions or [
        {
            "id": "action_toggle_unit",
            "type": "button",
            "label": "Toggle °C / °F",
            "action": "WEATHER_TOGGLE_UNIT"
        },
        {
            "id": "action_get_forecast",
            "type": "button",
            "label": "Get 5-Day Forecast",
            "action": "WEATHER_GET_FORECAST"
        }
    ]

    return {
        "a2ui_version": A2UI_SPEC_VERSION,
        "protocol": "a2ui",
        "ui": {
            "components": components,
            "actions": default_actions
        }
    }
