#!/usr/bin/env python3
"""
Experiment 1: Dynamic Dev Skill & MCP Tool Selection in Waymark Development Workflow.
Evaluates Jev's ability to select the exact required tool from a 20-tool roster,
comparing accuracy, latency, and context token reduction against full prompt injection.
"""

import os
import sys
import time

# Ensure imports work from project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from experiments.common.client import JevClient
from experiments.common.reporter import print_header, print_threshold_verdict, print_meter, Colors
from experiments.exp1_skill_selection.fixtures import DEV_TOOL_ROSTER, DEV_PROMPT_CASES

def run_experiment_1():
    print_header(
        "EXPERIMENT 1: Dynamic Dev Skill & MCP Tool Selection",
        "Evaluating Jev System 1 tool routing on Waymark development tasks"
    )

    client = JevClient()
    
    # Calculate baseline token overhead if all 20 tools are statically injected
    baseline_tokens_per_turn = sum(tool["full_schema_tokens"] for tool in DEV_TOOL_ROSTER.values())
    print(f"[*] Baseline Static Injection: {len(DEV_TOOL_ROSTER)} tools = {baseline_tokens_per_turn:,} tokens/turn injected into Frontier LLM")

    # Build the Choice criteria map from our roster
    choice_criteria = {name: data["summary"] for name, data in DEV_TOOL_ROSTER.items()}

    results = []
    correct_count = 0
    total_latency = 0.0
    total_jev_tokens = 0
    total_jev_cost = 0.0

    print(f"\n{'ID':<8} | {'Prompt':<42} | {'Expected':<22} | {'Jev Choice':<22} | {'Conf':<6} | {'Result':<6}")
    print("-" * 115)

    for case in DEV_PROMPT_CASES:
        state = {
            "workspace": "waymark",
            "developer_request": case["prompt"]
        }
        
        questions = {
            "selected_tool": {
                "type": "choice",
                "instructions": "Select the single most relevant tool or skill to handle the developer_request.",
                "criteria": choice_criteria
            },
            "requires_tool": {
                "type": "noul",
                "instructions": "Does this developer request require executing a technical development tool?",
                "criteria": {
                    "true": "Requires code analysis, test execution, git operations, or builds",
                    "false": "Pure conversational greeting or non-technical discussion"
                }
            }
        }

        eval_res = client.evaluate(state=state, questions=questions)
        
        total_latency += eval_res.latency_ms
        total_jev_tokens += eval_res.input_tokens
        total_jev_cost += eval_res.cost_usd
        
        choice_ans = eval_res.answers.get("selected_tool", {})
        chosen_tool = choice_ans.get("choice")
        confidence = choice_ans.get("confidence", 0.0)
        
        is_correct = (chosen_tool == case["expected_tool"])
        if is_correct:
            correct_count += 1
            status = f"{Colors.GREEN}MATCH{Colors.END}"
        else:
            status = f"{Colors.RED}DIFF{Colors.END}"

        truncated_prompt = (case["prompt"][:39] + "...") if len(case["prompt"]) > 42 else case["prompt"]
        print(f"{case['id']:<8} | {truncated_prompt:<42} | {case['expected_tool']:<22} | {chosen_tool:<22} | {confidence:<6.2f} | {status}")
        
        results.append({
            "id": case["id"],
            "expected": case["expected_tool"],
            "chosen": chosen_tool,
            "confidence": confidence,
            "is_correct": is_correct,
            "latency_ms": eval_res.latency_ms
        })

    # Metrics computation
    total_cases = len(DEV_PROMPT_CASES)
    accuracy_pct = (correct_count / total_cases) * 100.0
    avg_latency = total_latency / total_cases
    
    # Selected tool injected into Frontier LLM: only ~190 tokens avg instead of 3,860 tokens
    avg_selected_tool_tokens = sum(DEV_TOOL_ROSTER[c["expected_tool"]]["full_schema_tokens"] for c in DEV_PROMPT_CASES) / total_cases
    token_reduction_pct = ((baseline_tokens_per_turn - avg_selected_tool_tokens) / baseline_tokens_per_turn) * 100.0

    print("\n" + "=" * 75)
    print(f"{Colors.BOLD}QUANTITATIVE RESULTS & GO/NO-GO THRESHOLDS{Colors.END}")
    print("=" * 75)
    
    print(f"  Accuracy                : {correct_count}/{total_cases} ({accuracy_pct:.1f}%)")
    print(f"  Average Latency         : {avg_latency:.1f} ms")
    print(f"  Prompt Token Reduction  : {token_reduction_pct:.1f}% ({baseline_tokens_per_turn:,} -> {int(avg_selected_tool_tokens)} tokens)")
    print(f"  Total Jev Ingestion Cost: ${total_jev_cost:.6f} across {total_cases} turns")
    print("-" * 75)

    # Threshold checks
    pass_accuracy = accuracy_pct >= 90.0
    pass_reduction = token_reduction_pct >= 60.0
    pass_latency = avg_latency < 800.0
    overall_go = pass_accuracy and pass_reduction and pass_latency

    print_threshold_verdict("Accuracy Threshold (>=90%)", pass_accuracy, f"Observed {accuracy_pct:.1f}%")
    print_threshold_verdict("Token Reduction (>=60%)", pass_reduction, f"Observed {token_reduction_pct:.1f}%")
    print_threshold_verdict("Latency Ceiling (<800ms)", pass_latency, f"Observed {avg_latency:.1f} ms")

    print("\n" + "-" * 75)
    if overall_go:
        print(f"  {Colors.BOLD}{Colors.GREEN}★ EXPERIMENT 1 VERDICT: GO (Adopt Dynamic Skill Selection){Colors.END}")
    else:
        print(f"  {Colors.BOLD}{Colors.RED}★ EXPERIMENT 1 VERDICT: NO-GO (Thresholds Not Met){Colors.END}")
    print("-" * 75 + "\n")

    return {
        "experiment": "exp1_skill_selection",
        "verdict": "GO" if overall_go else "NO-GO",
        "accuracy": accuracy_pct,
        "token_reduction": token_reduction_pct,
        "avg_latency_ms": avg_latency,
        "total_cost_usd": total_jev_cost
    }

if __name__ == "__main__":
    run_experiment_1()
