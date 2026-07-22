# Weather ADK Agent with A2UI & A2A Support

An enterprise-ready **Google Agent Development Kit (ADK)** weather agent supporting **A2UI** (Agent-to-User Interface) declarative UI generation and **A2A** (Agent-to-Agent) protocol interoperability, configured for deployment to **Vertex AI Agent Engine**.

---

## 🌟 Architecture & Features

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                             Client Application                              │
│         (Gemini Enterprise / Custom Web / Mobile / A2UI Renderer)           │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       │ A2A Message Exchange (JSON-RPC)
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          Vertex AI Agent Engine                             │
│       ┌─────────────────────────────────────────────────────────────┐       │
│       │                 Weather ADK Agent (ADK Core)                │       │
│       │  - Gemini 2.5 Flash Model                                   │       │
│       │  - Weather Tools (get_current_weather, get_forecast)       │       │
│       │  - A2UI Component Payload Generator                         │       │
│       └──────────────────────────────┬──────────────────────────────┘       │
│                                      │                                      │
│         ┌────────────────────────────┴────────────────────────────┐         │
│         ▼                                                         ▼         │
│  A2A Protocol Endpoint                               A2UI Payload Generator │
│  (/.well-known/agent.json, /a2a/v1/message)          (Card, MetricGrid, etc.)│
└─────────────────────────────────────────────────────────────────────────────┘
```

- **Google ADK Foundation**: Built using standard `google-adk` abstractions (`Agent`, `Runner`, `SessionService`).
- **A2UI Protocol**: Generates structured, declarative UI JSON payloads (`a2ui_version: "1.0"`) allowing host applications to natively render interactive weather cards, metric grids, and forecast lists.
- **A2A Protocol**: Features standard Agent Card discovery at `/.well-known/agent.json` and A2A messaging via `/a2a/v1/message`.
- **Agent Engine Ready**: Configured with `agent_engine_app.py` and automated CLI deployment via `adk deploy agent_engine`.

---

## 📁 Repository Structure

```
weather_adk_agent/
├── weather_agent/              # Core Agent Module
│   ├── __init__.py             # Exposes root_agent
│   ├── agent.py                # ADK Agent definition with instructions & tools
│   ├── tools.py                # Weather data tools (current weather & forecast)
│   ├── a2ui.py                 # A2UI protocol component builders
│   └── a2a.py                  # A2A protocol JSON-RPC router & handlers
├── agent.json                  # A2A Agent Card metadata (spec 1.0)
├── agent_engine_app.py         # Entrypoint for Vertex AI Agent Engine deployment
├── server.py                   # Local FastAPI server hosting A2A & A2UI endpoints
├── deploy.py                   # Python deployment script for Agent Engine
├── deploy.sh                   # Shell script wrapper for deployment
├── test_agent.py               # Comprehensive unit test suite
├── requirements.txt            # Dependencies (google-adk, fastapi, uvicorn, etc.)
└── .env.example                # Sample environment configuration
```

---

## 🚀 Quick Start & Local Testing

### 1. Installation

```bash
cd /Users/vineetagarwal/projects/weather_adk_agent
pip install -r requirements.txt
```

### 2. Environment Setup

Copy `.env.example` to `.env` and set your credentials:

```bash
cp .env.example .env
```

Edit `.env`:
```env
GEMINI_API_KEY=your_gemini_api_key_here
GOOGLE_CLOUD_PROJECT=your_gcp_project_id
GOOGLE_CLOUD_LOCATION=us-central1
```

### 3. Run Unit Tests

```bash
python3 -m unittest test_agent.py
```

### 4. Run Interactive Local Web UI (ADK Web)

```bash
adk web weather_agent
```

### 5. Run FastAPI A2A & A2UI Server

```bash
python3 server.py
```

Access endpoints:
- **Agent Card (A2A Discovery)**: [http://localhost:8080/.well-known/agent.json](http://localhost:8080/.well-known/agent.json)
- **A2A Messaging**: `POST http://localhost:8080/a2a/v1/message`
- **Swagger Documentation**: [http://localhost:8080/docs](http://localhost:8080/docs)

---

## 🎨 A2UI Protocol Output Example

When asked for weather, the agent generates an embedded ```a2ui JSON block:

```json
{
  "a2ui_version": "1.0",
  "protocol": "a2ui",
  "ui": {
    "components": [
      {
        "component": "Card",
        "id": "weather_main_card",
        "props": { "variant": "gradient", "theme": "weather_blue" },
        "children": [
          {
            "component": "Header",
            "props": { "title": "San Francisco, CA", "subtitle": "Current Conditions • Sunny", "icon": "sun.max.fill" }
          },
          {
            "component": "DisplayTemp",
            "props": { "temperature": "18°C", "feels_like": "Feels like 18°C", "condition": "Sunny" }
          }
        ]
      },
      {
        "component": "MetricGrid",
        "id": "weather_metrics_grid",
        "props": { "columns": 2 },
        "children": [
          { "component": "MetricBadge", "props": { "label": "Humidity", "value": "65%", "icon": "drop.fill" } },
          { "component": "MetricBadge", "props": { "label": "Wind Speed", "value": "15 km/h", "icon": "wind" } }
        ]
      }
    ],
    "actions": [
      { "id": "action_toggle_unit", "type": "button", "label": "Toggle °C / °F", "action": "WEATHER_TOGGLE_UNIT" },
      { "id": "action_get_forecast", "type": "button", "label": "Get 5-Day Forecast", "action": "WEATHER_GET_FORECAST" }
    ]
  }
}
```

---

## ☁️ Deploying to Vertex AI Agent Engine

### Option A: Using the `adk` CLI

```bash
adk deploy agent_engine \
  --project=your-gcp-project-id \
  --region=us-central1 \
  --display_name="Weather A2UI A2A Agent" \
  --adk_app=agent_engine_app.py \
  --adk_app_object=root_agent \
  weather_agent
```

### Option B: Using the Python Deployer

```bash
python3 deploy.py --project your-gcp-project-id --region us-central1
```

### Option C: Deployment with Express Mode (API Key)

```bash
python3 deploy.py --api_key YOUR_GEMINI_API_KEY
```

---

## 🔗 A2A JSON-RPC Example Request

```json
POST /a2a/v1/message
Content-Type: application/json

{
  "jsonrpc": "2.0",
  "id": "req_001",
  "method": "tasks/send",
  "params": {
    "session_id": "session_123",
    "message": {
      "role": "user",
      "content": {
        "text": "What is the weather in Tokyo?"
      }
    }
  }
}
```
