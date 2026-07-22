"""
Weather ADK Agent Definition.

This module defines the primary Google Agent Development Kit (ADK) agent for weather
querying, supporting A2UI (Agent-to-User Interface) and A2A (Agent-to-Agent) protocol.
"""

import json
import sys
import os

# Ensure current directory is in sys.path
_current_dir = os.path.dirname(os.path.abspath(__file__))
if _current_dir not in sys.path:
    sys.path.insert(0, _current_dir)

from google.adk.agents.llm_agent import Agent

try:
    from weather_agent.tools import get_current_weather, get_weather_forecast
    from weather_agent.a2ui import (
        create_a2ui_weather_card,
        create_a2ui_metric_grid,
        create_a2ui_forecast_list,
        wrap_a2ui_payload
    )
except ImportError:
    from tools import get_current_weather, get_weather_forecast
    from a2ui import (
        create_a2ui_weather_card,
        create_a2ui_metric_grid,
        create_a2ui_forecast_list,
        wrap_a2ui_payload
    )

WEATHER_AGENT_INSTRUCTION = """
You are a Weather AI Assistant built on Google Agent Development Kit (ADK) with A2UI (Agent-to-User Interface) and A2A (Agent-to-Agent) support.
Your goal is to provide accurate weather information and format structured UI representations using A2UI payloads when requested or appropriate.

When answering weather queries:
1. Use `get_current_weather` for real-time conditions.
2. Use `get_weather_forecast` for multi-day weather outlooks.
3. Provide a clear, natural language summary of the weather.
"""

root_agent = Agent(
    model='gemini-1.5-flash',
    name='weather_adk_agent',
    description='A Weather Agent with A2UI protocol support and A2A interoperability.',
    instruction=WEATHER_AGENT_INSTRUCTION,
    tools=[get_current_weather, get_weather_forecast],
)
