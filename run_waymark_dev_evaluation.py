#!/usr/bin/env python3
"""
Master Evaluation Harness: Jev in the Agentic Development Organization.
Runs all 5 experiments sequentially and prints an executive summary.
"""

import os
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from experiments.common.reporter import print_header, Colors
from experiments.exp1_skill_selection.run import run_experiment_1
from experiments.exp2_model_routing.run import run_experiment_2
from experiments.exp3_pr_review_gate.run import run_experiment_3
from experiments.exp4_dev_guardrails.run import run_experiment_4
from experiments.exp5_issue_triage.run import run_experiment_5

def main():
    print(f"\n{Colors.BOLD}{Colors.HEADER}{'#' * 80}")
    print("  EXECUTIVE EVALUATION SUITE: JEV SYSTEM ONE FOR AGENTIC DEVELOPMENT ORG")
    print(f"  Benchmark Case: Waymark Development Lifecycle | Model: jev-latest")
    print(f"{'#' * 80}{Colors.END}\n")

    start_suite = time.perf_counter()

    r1 = run_experiment_1()
    r2 = run_experiment_2()
    r3 = run_experiment_3()
    r4 = run_experiment_4()
    r5 = run_experiment_5()

    elapsed = time.perf_counter() - start_suite

    print_header(
        "SUITE SUMMARY & EMPIRICAL SCORECARD",
        f"Executed 5 experiments across 55 real-world development tasks in {elapsed:.1f}s"
    )

    summary_table = [
        ("1. Dynamic Dev Tool Selection", r1["verdict"], f"Acc: {r1['accuracy']:.1f}% | Tokens Saved: {r1['token_reduction']:.1f}% | Latency: {r1['avg_latency_ms']:.1f}ms"),
        ("2. Tiered Model Dispatch", r2["verdict"], f"Agreement: {r2['accuracy']:.1f}% | Quota Saved: {r2['cost_savings_pct']:.1f}% | Catastrophic: {r2['catastrophic_misroutes']}"),
        ("3. Confidence PR Review Gate", r3["verdict"], f"Hazard Intercept: {r3['hazard_interception_pct']:.1f}% | False Esc: {r3['false_escalation_pct']:.1f}%"),
        ("4. Pre-Execution Guardrails", r4["verdict"], f"Intercept: {r4['intercept_rate']:.1f}% | False Block: {r4['false_block_rate']:.1f}% | Latency: {r4['avg_latency_ms']:.1f}ms"),
        ("5. Issue & Backlog Triage", r5["verdict"], f"Schema: {r5['schema_adherence_pct']:.1f}% | Agreement: {r5['agreement_pct']:.1f}% | Latency: {r5['avg_latency_ms']:.1f}ms")
    ]

    print(f"{'Experiment Area':<32} | {'Verdict':<12} | {'Key Empirical Findings'}")
    print("-" * 90)
    for title, verdict, findings in summary_table:
        color = Colors.GREEN if verdict == "GO" else (Colors.YELLOW if "CONDITIONAL" in verdict else Colors.RED)
        print(f"{title:<32} | {color}{verdict:<12}{Colors.END} | {findings}")
    print("-" * 90)
    print("\nDetailed analysis and integration recommendations available in: DECISION_SCORECARD.md\n")

if __name__ == "__main__":
    main()
