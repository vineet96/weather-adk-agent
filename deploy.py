#!/usr/bin/env python3
"""
Deployment script for deploying Weather ADK Agent to Vertex AI Agent Engine.

Usage:
    python deploy.py --project YOUR_PROJECT_ID --region us-central1
    OR
    python deploy.py --api_key YOUR_GEMINI_API_KEY
"""

import sys
import os
import argparse
import subprocess

def deploy_agent_engine(
    agent_dir: str = "weather_agent",
    project: str = None,
    region: str = None,
    api_key: str = None,
    display_name: str = "Weather A2UI A2A Agent",
    description: str = "Weather ADK Agent with A2UI protocol support and A2A interoperability."
):
    print("=" * 60)
    print(" Deploying Weather ADK Agent to Vertex AI Agent Engine")
    print("=" * 60)

    adk_bin = "/Library/Frameworks/Python.framework/Versions/3.11/bin/adk"
    if not os.path.exists(adk_bin):
        adk_bin = "adk"

    cmd = [
        adk_bin, "deploy", "agent_engine",
        agent_dir,
        "--display_name", display_name,
        "--description", description,
        "--adk_app", "agent_engine_app.py",
        "--adk_app_object", "root_agent"
    ]

    if api_key:
        cmd.extend(["--api_key", api_key])
    elif project:
        cmd.extend(["--project", project])
        if region:
            cmd.extend(["--region", region])
    else:
        # Fallback to environment variables
        env_project = os.environ.get("GOOGLE_CLOUD_PROJECT")
        env_region = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
        env_key = os.environ.get("GEMINI_API_KEY")

        if env_key:
            cmd.extend(["--api_key", env_key])
        elif env_project:
            cmd.extend(["--project", env_project, "--region", env_region])
        else:
            print("[ERROR] You must provide --project or --api_key, or set GOOGLE_CLOUD_PROJECT / GEMINI_API_KEY in environment.")
            sys.exit(1)

    print(f"Running command: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print("\n[SUCCESS] Agent successfully deployed to Agent Engine!")
    else:
        print(f"\n[FAILURE] Deployment exited with code {result.returncode}")
    
    return result.returncode

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deploy Weather ADK Agent to Agent Engine")
    parser.add_argument("--project", type=str, help="Google Cloud Project ID")
    parser.add_argument("--region", type=str, default="us-central1", help="Google Cloud Region")
    parser.add_argument("--api_key", type=str, help="Gemini API Key (Express Mode)")
    parser.add_argument("--display_name", type=str, default="Weather A2UI A2A Agent", help="Display name in Agent Engine")

    args = parser.parse_args()
    deploy_agent_engine(
        project=args.project,
        region=args.region,
        api_key=args.api_key,
        display_name=args.display_name
    )
