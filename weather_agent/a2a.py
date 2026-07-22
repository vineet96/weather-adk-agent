"""
A2A (Agent-to-Agent) Protocol Server Handler for Weather ADK Agent.

Implements standard A2A endpoints:
- GET /.well-known/agent.json (A2A Agent Card Discovery)
- POST /a2a/v1/message (JSON-RPC A2A Message Exchange)
"""

import json
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Request
try:
    from weather_agent.agent import root_agent
except ImportError:
    from agent import root_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

router = APIRouter()
session_service = InMemorySessionService()
runner = Runner(app_name="weather_agent", agent=root_agent, session_service=session_service)

@router.get("/.well-known/agent.json")
async def get_agent_card() -> Dict[str, Any]:
    """
    Exposes the A2A Agent Card for agent discovery.
    """
    try:
        with open("agent.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "spec_version": "1.0",
            "name": "Weather ADK Agent",
            "id": "weather_adk_agent",
            "protocols": [{"name": "A2A", "version": "1.0"}, {"name": "A2UI", "version": "1.0"}]
        }


@router.post("/a2a/v1/message")
async def handle_a2a_message(request: Request) -> Dict[str, Any]:
    """
    Handles JSON-RPC 2.0 A2A task/message execution.
    """
    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    method = payload.get("method", "")
    params = payload.get("params", {})
    msg_id = payload.get("id", "1")

    if method != "tasks/send":
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "error": {
                "code": -32601,
                "message": f"Method '{method}' not found. Supported methods: 'tasks/send'."
            }
        }

    user_query = params.get("message", {}).get("content", {}).get("text", "")
    session_id = params.get("session_id", "a2a_session_default")

    if not user_query:
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "error": {
                "code": -32602,
                "message": "Missing 'text' inside params.message.content"
            }
        }

    # Execute ADK Agent Runner
    try:
        # Create session if not exists
        session = session_service.get_session(session_id=session_id)
        if not session:
            session = session_service.create_session(session_id=session_id)

        # Run agent
        events = runner.run(user_input=user_query, session_id=session_id)
        
        # Aggregate text output
        agent_response_text = ""
        for event in events:
            if hasattr(event, "content") and event.content:
                agent_response_text += str(event.content)

        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "task_id": f"task_{session_id}",
                "status": "completed",
                "message": {
                    "role": "agent",
                    "content": {
                        "text": agent_response_text
                    }
                },
                "protocols_supported": ["a2a/1.0", "a2ui/1.0"]
            }
        }
    except Exception as e:
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "error": {
                "code": -32000,
                "message": f"Agent execution error: {str(e)}"
            }
        }
