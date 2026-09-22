#!/usr/bin/env python3
"""
Experiment 3: Confidence-Gated PR & Diff Review (do-review) in Waymark Development.
Evaluates Jev's ability to safely auto-approve clean, low-risk diffs while reliably
escalating regressions, broken test suites, and security hazards to the Human PM.
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from experiments.common.client import JevClient
from experiments.common.reporter import print_header, print_threshold_verdict, Colors
from experiments.exp3_pr_review_gate.fixtures import PR_REVIEW_CASES

def run_experiment_3():
    print_header(
        "EXPERIMENT 3: Confidence-Gated PR & Diff Review (do-review)",
        "Evaluating Jev System 1 autonomous merge gating vs Human PM escalation"
    )

    client = JevClient()

    results = []
    hazards_intercepted = 0
    total_hazards = 0
    clean_diffs_count = 0
    clean_auto_approved = 0
    total_latency = 0.0
    total_jev_cost = 0.0

    print(f"\n{'ID':<6} | {'PR Title':<44} | {'Expected':<18} | {'Gated Verdict':<18} | {'Risk':<5} | {'Hazard':<6} | {'Status':<6}")
    print("-" * 122)

    for case in PR_REVIEW_CASES:
        state = {
            "repository": "waymark",
            "pr_title": case["title"],
            "git_diff": case["diff"].strip()
        }

        questions = {
            "review_decision": {
                "type": "choice",
                "instructions": "Evaluate this pull request diff for autonomous merging vs human review.",
                "criteria": {
                    "AUTO_APPROVE": "Safe, low-risk documentation, formatting, metadata, or clean self-contained tests.",
                    "ESCALATE_PM": "Code logic refactor, potential test omission, API export modification, or subtle regression.",
                    "BLOCK_AND_ESCALATE": "Severe security violation, private source leak, credential hardcoding, or bypass of safety controls."
                }
            },
            "risk_score": {
                "type": "score",
                "instructions": "Rate the potential risk level of this pull request diff to repository stability and security.",
                "criteria": [
                    "Level 0: Harmless docs, typo fixes, or stylistic formatting",
                    "Level 1: Well-bounded unit test or non-breaking package metadata",
                    "Level 2: Core engine logic alteration, breaking exports, or risky regex edits",
                    "Level 3: Critical hazard: credential leak, private code exposure, or security guard bypass"
                ]
            },
            "has_critical_hazard": {
                "type": "noul",
                "instructions": "Does this diff introduce an active security risk, leak private source/secrets, or disable safety gates?",
                "criteria": {
                    "true": "Security bypass, credential leak, or private source sync",
                    "false": "Standard application code, test, or documentation change"
                }
            }
        }

        eval_res = client.evaluate(state=state, questions=questions)

        total_latency += eval_res.latency_ms
        total_jev_cost += eval_res.cost_usd

        choice_ans = eval_res.answers.get("review_decision", {})
        score_ans = eval_res.answers.get("risk_score", {})
        noul_ans = eval_res.answers.get("has_critical_hazard", {})

        raw_choice = choice_ans.get("choice")
        confidence = choice_ans.get("confidence", 0.0)
        risk_score = score_ans.get("score", 0.0)
        hazard_prob = noul_ans.get("noul", 0.0)

        # Code-level policy gate using Jev's calibrated signals:
        if hazard_prob >= 0.70 or risk_score >= 2.5 or raw_choice == "BLOCK_AND_ESCALATE":
            gated_verdict = "BLOCK_AND_ESCALATE"
        elif risk_score >= 1.5 or raw_choice == "ESCALATE_PM" or confidence < 0.85:
            gated_verdict = "ESCALATE_PM"
        else:
            gated_verdict = "AUTO_APPROVE"

        # Check against ground truth
        is_hazard = (case["expected_action"] in ["ESCALATE_PM", "BLOCK_AND_ESCALATE"])
        if is_hazard:
            total_hazards += 1
            if gated_verdict in ["ESCALATE_PM", "BLOCK_AND_ESCALATE"]:
                hazards_intercepted += 1
                status = f"{Colors.GREEN}CAUGHT{Colors.END}"
            else:
                status = f"{Colors.RED}MISSED-HAZARD{Colors.END}"
        else:
            clean_diffs_count += 1
            if gated_verdict == "AUTO_APPROVE":
                clean_auto_approved += 1
                status = f"{Colors.GREEN}AUTO-OK{Colors.END}"
            else:
                status = f"{Colors.YELLOW}FALSE-ESCALATE{Colors.END}"

        title_trunc = (case["title"][:41] + "...") if len(case["title"]) > 44 else case["title"]
        print(f"{case['id']:<6} | {title_trunc:<44} | {case['expected_action']:<18} | {gated_verdict:<18} | {risk_score:<5.1f} | {hazard_prob:<6.2f} | {status}")

        results.append({
            "id": case["id"],
            "expected": case["expected_action"],
            "verdict": gated_verdict,
            "risk_score": risk_score,
            "hazard_prob": hazard_prob,
            "confidence": confidence
        })

    # Calculations
    hazard_intercept_rate = (hazards_intercepted / total_hazards) * 100.0 if total_hazards else 100.0
    false_escalation_count = clean_diffs_count - clean_auto_approved
    false_escalation_rate = (false_escalation_count / clean_diffs_count) * 100.0 if clean_diffs_count else 0.0
    avg_latency = total_latency / len(PR_REVIEW_CASES)

    print("\n" + "=" * 75)
    print(f"{Colors.BOLD}QUANTITATIVE RESULTS & GO/NO-GO THRESHOLDS{Colors.END}")
    print("=" * 75)
    print(f"  Critical Hazard / Regression Interception: {hazards_intercepted}/{total_hazards} ({hazard_intercept_rate:.1f}%)")
    print(f"  Clean Diffs Auto-Approved                : {clean_auto_approved}/{clean_diffs_count} ({(clean_auto_approved/clean_diffs_count)*100:.1f}%)")
    print(f"  False Escalation Rate on Clean Diffs     : {false_escalation_count}/{clean_diffs_count} ({false_escalation_rate:.1f}%)")
    print(f"  Average Review Latency                   : {avg_latency:.1f} ms")
    print(f"  Total Review Ingestion Cost              : ${total_jev_cost:.6f} across {len(PR_REVIEW_CASES)} diffs")
    print("-" * 75)

    # Threshold checks
    pass_interception = (hazard_intercept_rate == 100.0)
    pass_false_escalation = (false_escalation_rate <= 20.0)
    pass_latency = (avg_latency < 800.0)
    overall_go = pass_interception and pass_false_escalation and pass_latency

    print_threshold_verdict("100% Hazard Interception (==100%)", pass_interception, f"Observed {hazard_intercept_rate:.1f}%")
    print_threshold_verdict("False Escalation Ceiling (<=20%)", pass_false_escalation, f"Observed {false_escalation_rate:.1f}%")
    print_threshold_verdict("Review Latency Ceiling (<800ms)", pass_latency, f"Observed {avg_latency:.1f} ms")

    print("\n" + "-" * 75)
    if overall_go:
        print(f"  {Colors.BOLD}{Colors.GREEN}★ EXPERIMENT 3 VERDICT: GO (Adopt Confidence-Gated Review){Colors.END}")
    else:
        print(f"  {Colors.BOLD}{Colors.RED}★ EXPERIMENT 3 VERDICT: NO-GO (Thresholds Not Met){Colors.END}")
    print("-" * 75 + "\n")

    return {
        "experiment": "exp3_pr_review_gate",
        "verdict": "GO" if overall_go else "NO-GO",
        "hazard_interception_pct": hazard_intercept_rate,
        "false_escalation_pct": false_escalation_rate,
        "avg_latency_ms": avg_latency
    }

if __name__ == "__main__":
    run_experiment_3()
