"""
Agent Engine App Entrypoint for Weather ADK Agent.

This file is loaded by the `adk deploy agent_engine` command when deploying to
Vertex AI Agent Engine.
"""

import sys
import os

# Ensure the app directory and parent directory are in sys.path for Cloud Reasoning Engine
app_dir = os.path.dirname(os.path.abspath(__file__))
if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

from weather_agent.agent import root_agent

# Expose root_agent for ADK Agent Engine deployer
app = root_agent
