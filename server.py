"""
FastAPI Server for Weather ADK Agent with A2UI & A2A Support.
Run with: python server.py or uvicorn server:app --reload
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from weather_agent.a2a import router as a2a_router
from weather_agent.agent import root_agent

app = FastAPI(
    title="Weather ADK Agent with A2UI & A2A Support",
    description="Google Agent Development Kit Weather Agent with A2UI component rendering and A2A interoperability.",
    version="1.0.0"
)

# Enable CORS for web UI clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include A2A Router (includes GET /.well-known/agent.json and POST /a2a/v1/message)
app.include_router(a2a_router)

@app.get("/")
async def root():
    return {
        "status": "online",
        "agent": "Weather ADK Agent",
        "adk_version": "0.1.0+",
        "protocols": ["A2A/1.0", "A2UI/1.0"],
        "endpoints": {
            "agent_card": "/.well-known/agent.json",
            "a2a_message": "/a2a/v1/message",
            "docs": "/docs"
        }
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    print(f"Starting Weather ADK Agent Server on port {port}...")
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=True)
