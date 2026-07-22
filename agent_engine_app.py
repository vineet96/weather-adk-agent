"""
Agent Engine App Entrypoint for Weather ADK Agent.

This file is loaded by the `adk deploy agent_engine` command when deploying to
Vertex AI Agent Engine.
"""

try:
    from weather_agent.agent import root_agent
except ImportError:
    from agent import root_agent

# Expose root_agent for ADK Agent Engine deployer
app = root_agent
