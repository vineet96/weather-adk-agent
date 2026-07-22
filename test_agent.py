"""
Test suite for Weather ADK Agent with A2UI & A2A Support.
"""

import json
import unittest
from weather_agent.tools import get_current_weather, get_weather_forecast
from weather_agent.a2ui import (
    create_a2ui_weather_card,
    create_a2ui_metric_grid,
    create_a2ui_forecast_list,
    wrap_a2ui_payload
)
from weather_agent.agent import root_agent

class TestWeatherADKAgent(unittest.TestCase):

    def test_current_weather_tool(self):
        result = get_current_weather("San Francisco, CA", unit="celsius")
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["location"], "San Francisco, Ca")
        self.assertIn("temperature", result)
        self.assertIn("humidity_percent", result)
        self.assertIn("wind_speed_kmh", result)

    def test_forecast_weather_tool(self):
        result = get_weather_forecast("Tokyo", days=3, unit="celsius")
        self.assertEqual(result["status"], "success")
        self.assertEqual(len(result["forecast_days"]), 3)
        self.assertIn("summary", result)

    def test_a2ui_payload_generation(self):
        weather = get_current_weather("London", unit="celsius")
        card = create_a2ui_weather_card(weather)
        grid = create_a2ui_metric_grid(weather)
        
        forecast = get_weather_forecast("London", days=3)
        forecast_list = create_a2ui_forecast_list(forecast)

        a2ui_payload = wrap_a2ui_payload([card, grid, forecast_list])

        self.assertEqual(a2ui_payload["a2ui_version"], "1.0")
        self.assertEqual(a2ui_payload["protocol"], "a2ui")
        self.assertEqual(len(a2ui_payload["ui"]["components"]), 3)
        self.assertEqual(a2ui_payload["ui"]["components"][0]["component"], "Card")

    def test_agent_card_json(self):
        with open("agent.json", "r") as f:
            data = json.load(f)
        self.assertEqual(data["spec_version"], "1.0")
        self.assertIn("protocols", data)
        protocol_names = [p["name"] for p in data["protocols"]]
        self.assertIn("A2A", protocol_names)
        self.assertIn("A2UI", protocol_names)

    def test_root_agent_definition(self):
        self.assertEqual(root_agent.name, "weather_adk_agent")
        self.assertTrue(len(root_agent.tools) >= 2)

if __name__ == "__main__":
    unittest.main()
