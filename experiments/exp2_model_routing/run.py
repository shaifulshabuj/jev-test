#!/usr/bin/env python3
"""
Experiment 2: Intelligent Tiered Model Routing in Waymark Development Workflow.
Evaluates Jev's ability to classify development tasks into Tier 0 (Script),
Tier 1 (Fast Model), or Tier 2 (Frontier LLM), preventing rate limit exhaustion.
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from experiments.common.client import JevClient
from experiments.common.reporter import print_header, print_threshold_verdict, Colors
from experiments.exp2_model_routing.fixtures import ROUTING_TIERS, WAYMARK_DEV_TASKS

# Estimated cost per development task in each tier
COST_PER_TASK_BASELINE_FRONTIER = 0.0150   # 100% routed to Frontier Model (Sonnet/Opus)
COST_PER_TASK_TIER_0 = 0.0000              # Local shell script / deterministic
COST_PER_TASK_TIER_1 = 0.0005              # Fast model (Gemini Flash / Claude Haiku)
COST_PER_TASK_TIER_2 = 0.0150              # Frontier Reasoning Model

def run_experiment_2():
    print_header(
        "EXPERIMENT 2: Intelligent Tiered Model Routing (do-gate)",
        "Evaluating Jev System 1 task classification across execution tiers"
    )

    client = JevClient()

    results = []
    correct_count = 0
    catastrophic_misroutes = 0
    total_latency = 0.0
    total_jev_cost = 0.0

    print(f"\n{'ID':<8} | {'Task Description':<48} | {'Expected':<22} | {'Jev Route':<22} | {'Risk':<5} | {'Status':<6}")
    print("-" * 122)

    for task in WAYMARK_DEV_TASKS:
        state = {
            "project": "waymark",
            "task_description": task["description"],
            "category": task["category"]
        }

        questions = {
            "assigned_tier": {
                "type": "choice",
                "instructions": "Determine the optimal execution tier for this development task.",
                "criteria": ROUTING_TIERS
            },
            "complexity_score": {
                "type": "score",
                "instructions": "Rate the technical complexity and failure risk of this development task.",
                "criteria": [
                    "Level 0: Purely mechanical formatting, status check, or version bump",
                    "Level 1: Routine documentation, translation, or text formatting",
                    "Level 2: Standard application logic, helper function, or unit test",
                    "Level 3: Security-critical fix, cross-platform OS bug, or architectural refactor"
                ]
            },
            "is_critical": {
                "type": "noul",
                "instructions": "Is this task security-sensitive or high-risk for system integrity?"
            }
        }

        eval_res = client.evaluate(state=state, questions=questions)
        
        total_latency += eval_res.latency_ms
        total_jev_cost += eval_res.cost_usd

        choice_ans = eval_res.answers.get("assigned_tier", {})
        score_ans = eval_res.answers.get("complexity_score", {})
        
        chosen_tier = choice_ans.get("choice")
        confidence = choice_ans.get("confidence", 0.0)
        risk_score = score_ans.get("score", 0.0)

        is_correct = (chosen_tier == task["expected_tier"])
        if is_correct:
            correct_count += 1
            status = f"{Colors.GREEN}MATCH{Colors.END}"
        else:
            status = f"{Colors.YELLOW}DIFF{Colors.END}"

        # Catastrophic failure: A Tier 2 task routed to Tier 0 or Tier 1
        is_catastrophic = (task["expected_tier"] == "tier_2_frontier_model" and chosen_tier != "tier_2_frontier_model")
        if is_catastrophic:
            catastrophic_misroutes += 1
            status = f"{Colors.RED}CRIT-MISROUTE{Colors.END}"

        desc_trunc = (task["description"][:45] + "...") if len(task["description"]) > 48 else task["description"]
        print(f"{task['id']:<8} | {desc_trunc:<48} | {task['expected_tier']:<22} | {chosen_tier:<22} | {risk_score:<5.1f} | {status}")

        results.append({
            "id": task["id"],
            "expected": task["expected_tier"],
            "chosen": chosen_tier,
            "confidence": confidence,
            "risk_score": risk_score,
            "is_correct": is_correct,
            "is_catastrophic": is_catastrophic
        })

    # Calculations
    total_tasks = len(WAYMARK_DEV_TASKS)
    accuracy_pct = (correct_count / total_tasks) * 100.0
    avg_latency = total_latency / total_tasks

    # Cost Analysis: Baseline (all Frontier) vs Tiered System
    baseline_total_cost = total_tasks * COST_PER_TASK_BASELINE_FRONTIER
    
    tiered_execution_cost = 0.0
    for r in results:
        tier = r["chosen"]
        if tier == "tier_0_local_script":
            tiered_execution_cost += COST_PER_TASK_TIER_0
        elif tier == "tier_1_fast_model":
            tiered_execution_cost += COST_PER_TASK_TIER_1
        else:
            tiered_execution_cost += COST_PER_TASK_TIER_2

    actual_tiered_total_cost = tiered_execution_cost + total_jev_cost
    cost_savings_pct = ((baseline_total_cost - actual_tiered_total_cost) / baseline_total_cost) * 100.0

    print("\n" + "=" * 75)
    print(f"{Colors.BOLD}QUANTITATIVE RESULTS & GO/NO-GO THRESHOLDS{Colors.END}")
    print("=" * 75)
    print(f"  Agreement with Human Triage : {correct_count}/{total_tasks} ({accuracy_pct:.1f}%)")
    print(f"  Catastrophic Misroutes      : {catastrophic_misroutes} (Critical tasks downgraded)")
    print(f"  Average Triage Latency      : {avg_latency:.1f} ms")
    print(f"  Baseline Cost (All Frontier): ${baseline_total_cost:.4f}")
    print(f"  Tiered System Cost (w/ Jev) : ${actual_tiered_total_cost:.4f} (Inference: ${tiered_execution_cost:.4f} + Jev: ${total_jev_cost:.6f})")
    print(f"  Net Cost & Quota Savings    : {cost_savings_pct:.1f}%")
    print("-" * 75)

    # Threshold checks
    pass_no_catastrophic = (catastrophic_misroutes == 0)
    pass_accuracy = accuracy_pct >= 85.0
    pass_cost = cost_savings_pct >= 40.0
    overall_go = pass_no_catastrophic and pass_accuracy and pass_cost

    print_threshold_verdict("Zero Catastrophic Misroutes (==0)", pass_no_catastrophic, f"Observed {catastrophic_misroutes}")
    print_threshold_verdict("Triage Agreement Threshold (>=85%)", pass_accuracy, f"Observed {accuracy_pct:.1f}%")
    print_threshold_verdict("Frontier Quota Savings (>=40%)", pass_cost, f"Observed {cost_savings_pct:.1f}% savings")

    print("\n" + "-" * 75)
    if overall_go:
        print(f"  {Colors.BOLD}{Colors.GREEN}★ EXPERIMENT 2 VERDICT: GO (Adopt Tiered Model Routing){Colors.END}")
    else:
        print(f"  {Colors.BOLD}{Colors.RED}★ EXPERIMENT 2 VERDICT: NO-GO (Thresholds Not Met){Colors.END}")
    print("-" * 75 + "\n")

    return {
        "experiment": "exp2_model_routing",
        "verdict": "GO" if overall_go else "NO-GO",
        "accuracy": accuracy_pct,
        "catastrophic_misroutes": catastrophic_misroutes,
        "cost_savings_pct": cost_savings_pct,
        "avg_latency_ms": avg_latency
    }

if __name__ == "__main__":
    run_experiment_2()
