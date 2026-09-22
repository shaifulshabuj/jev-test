#!/usr/bin/env python3
"""
Test script for TypeSafe AI / Jev System One capabilities.
Demonstrates multi-primitive evaluation (Noul, Choice, Score) in a single API call.
"""

import json
import os
import sys
import urllib.request
import urllib.error

API_KEY = os.environ.get("TYPESAFE_API_KEY")
BASE_URL = "https://api.typesafe.ai/v1"

if not API_KEY:
    print("ERROR: TYPESAFE_API_KEY environment variable is not set.", file=sys.stderr)
    sys.exit(1)

def request(endpoint: str, data: dict | None = None) -> dict:
    url = f"{BASE_URL}{endpoint}"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    
    body = json.dumps(data).encode("utf-8") if data is not None else None
    req = urllib.request.Request(url, data=body, headers=headers, method="POST" if data is not None else "GET")
    
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        print(f"HTTP Error {e.code}: {err_msg}", file=sys.stderr)
        raise

def test_models():
    print("=" * 60)
    print("1. Checking Available Models (GET /v1/models)")
    print("=" * 60)
    res = request("/models")
    for m in res.get("models", []):
        print(f" - Model: {m.get('name'):<15} | Description: {m.get('description')}")
    print()

def test_system_one_evaluation():
    print("=" * 60)
    print("2. Testing Jev Multi-Primitive Evaluation (POST /v1/systemone)")
    print("=" * 60)

    # Realistic Agentic Org scenario:
    # An incoming task request from a user arrives at the PM / Gate layer.
    state = {
        "author": "dev-lead",
        "action_requested": "rm -rf build/ dist/ && git clean -fdx && python3 deploy.py --force --target=staging",
        "context": "Clean build artifacts and deploy latest build to staging environment."
    }

    payload = {
        "model": "jev-latest",
        "state": state,
        "questions": {
            # Primitive 1: Noul (Yes/No probability)
            "is_destructive": {
                "type": "noul",
                "instructions": "Does this action command delete files or modify deployed environments?",
                "criteria": {
                    "true": "Deletes local files, directories, or initiates remote deployment",
                    "false": "Purely read-only inspection command"
                }
            },
            # Primitive 2: Choice (Categorical selection + distribution + confidence)
            "target_lane": {
                "type": "choice",
                "instructions": "Which execution lane should handle this task?",
                "criteria": {
                    "automated_ci": "Standard automated builds, testing, or cleanups",
                    "human_pm_review": "Actions requiring explicit human authorization or credentials",
                    "rejected": "Invalid, unsafe, or corrupted command requests"
                }
            },
            # Primitive 3: Score (Graded rubric rating 0..N + confidence)
            "risk_assessment": {
                "type": "score",
                "instructions": "Assess the risk level of running this command in an automated agent loop.",
                "criteria": [
                    "Level 0: Harmless read-only inspection",
                    "Level 1: Routine local file cleanup",
                    "Level 2: Deployment with force flags or environment mutations",
                    "Level 3: Critical production risk or unrecoverable deletion"
                ]
            }
        }
    }

    print(f"State being evaluated:\n{json.dumps(state, indent=2)}\n")
    print("Sending evaluation request to Jev...")
    
    response = request("/systemone", payload)
    
    model_version = response.get("model")
    answers = response.get("answers", {})
    usage = response.get("usage", {})
    
    print(f"\nResponse from model [{model_version}]:")
    print(f"Token Usage: Input = {usage.get('input_tokens')}, Output = {usage.get('output_tokens')}\n")

    # Inspect Noul
    noul_ans = answers.get("is_destructive", {})
    print(f"[Noul] is_destructive: probability = {noul_ans.get('noul'):.2f}")

    # Inspect Choice
    choice_ans = answers.get("target_lane", {})
    print(f"[Choice] target_lane: '{choice_ans.get('choice')}' (confidence: {choice_ans.get('confidence'):.2f})")
    print(f"         Probabilities: {choice_ans.get('probabilities')}")

    # Inspect Score
    score_ans = answers.get("risk_assessment", {})
    print(f"[Score] risk_assessment: {score_ans.get('score'):.2f} / 3.0 (confidence: {score_ans.get('confidence'):.2f})")
    print(f"        Level breakdown: {score_ans.get('probabilities')}")
    
    # Practical Agent Logic Demonstration
    print("\n" + "-" * 60)
    print("3. Programmatic Decision in Agent Code:")
    print("-" * 60)
    
    risk = score_ans.get("score", 0.0)
    confidence = choice_ans.get("confidence", 0.0)
    
    if risk >= 2.0 or confidence < 0.80:
        print("-> [DECISION]: Escalate to PM / User Review (Risk >= 2.0 or Low Confidence).")
    else:
        print("-> [DECISION]: Auto-execute command in automated worker lane.")

if __name__ == "__main__":
    test_models()
    test_system_one_evaluation()
