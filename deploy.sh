#!/usr/bin/env bash
set -e

# Weather ADK Agent Deployment Script for Agent Engine
echo "============================================================"
echo "Deploying Weather ADK Agent with A2UI & A2A to Agent Engine"
echo "============================================================"

PROJECT_ID=${GOOGLE_CLOUD_PROJECT:-""}
REGION=${GOOGLE_CLOUD_LOCATION:-"us-central1"}

if [ -z "$PROJECT_ID" ] && [ -z "$GEMINI_API_KEY" ]; then
    echo "Usage: GOOGLE_CLOUD_PROJECT=your-project-id ./deploy.sh"
    echo "  or:  GEMINI_API_KEY=your-api-key ./deploy.sh"
    exit 1
fi

python3 deploy.py "$@"
