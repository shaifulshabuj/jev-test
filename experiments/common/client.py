"""
Reusable TypeSafe AI (Jev) API Client for Agentic Org Experiments.
Tracks latency, token consumption, and cost calculations.
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error
from dataclasses import dataclass
from typing import Any, Dict, Optional

BASE_URL = "https://api.typesafe.ai/v1"
INPUT_TOKEN_PRICE_PER_MTOK = 0.042  # $0.042 per 1M input tokens
OUTPUT_TOKEN_PRICE_PER_MTOK = 0.000  # Output tokens are free

@dataclass
class EvaluationResult:
    model: str
    answers: Dict[str, Any]
    input_tokens: int
    output_tokens: int
    cost_usd: float
    latency_ms: float
    raw_response: Dict[str, Any]

class JevClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("TYPESAFE_API_KEY")
        if not self.api_key:
            raise ValueError("TYPESAFE_API_KEY environment variable is not set.")

    def evaluate(self, state: Any, questions: Dict[str, Any], model: str = "jev-latest") -> EvaluationResult:
        url = f"{BASE_URL}/systemone"
        payload = {
            "model": model,
            "state": state,
            "questions": questions
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        body = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=body, headers=headers, method="POST")
        
        start_time = time.perf_counter()
        try:
            with urllib.request.urlopen(req) as resp:
                raw_data = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            err_msg = e.read().decode("utf-8")
            print(f"[JevClient Error] HTTP {e.code}: {err_msg}", file=sys.stderr)
            raise
        except Exception as e:
            print(f"[JevClient Connection Error]: {e}", file=sys.stderr)
            raise
        
        latency_ms = (time.perf_counter() - start_time) * 1000.0
        
        usage = raw_data.get("usage", {})
        input_tokens = usage.get("input_tokens", 0)
        output_tokens = usage.get("output_tokens", 0)
        cost_usd = (input_tokens / 1_000_000.0) * INPUT_TOKEN_PRICE_PER_MTOK
        
        return EvaluationResult(
            model=raw_data.get("model", model),
            answers=raw_data.get("answers", {}),
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost_usd=cost_usd,
            latency_ms=latency_ms,
            raw_response=raw_data
        )

    def list_models(self) -> Dict[str, Any]:
        url = f"{BASE_URL}/models"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        req = urllib.request.Request(url, headers=headers, method="GET")
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
