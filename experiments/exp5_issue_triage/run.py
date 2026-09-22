#!/usr/bin/env python3
"""
Experiment 5: Waymark Issue & Backlog Triage (do-issue / do-triage).
Evaluates Jev's ability to extract multi-dimensional portfolio metadata
(component, category, complexity, ADR necessity) in a single parallel call.
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from experiments.common.client import JevClient
from experiments.common.reporter import print_header, print_threshold_verdict, Colors
from experiments.exp5_issue_triage.fixtures import RAW_ISSUE_REPORTS

def run_experiment_5():
    print_header(
        "EXPERIMENT 5: Multi-Question Issue & Backlog Triage (do-triage)",
        "Evaluating single-shot parallel extraction of portfolio metadata"
    )

    client = JevClient()

    results = []
    schema_valid_count = 0
    matches_count = 0
    total_fields = 0
    total_latency = 0.0
    total_cost = 0.0

    print(f"\n{'ID':<8} | {'Raw Report Snippet':<36} | {'Component':<12} | {'Category':<10} | {'ADR':<5} | {'Complx':<6} | {'Status':<6}")
    print("-" * 105)

    for case in RAW_ISSUE_REPORTS:
        state = {
            "repository": "waymark",
            "raw_developer_report": case["raw_text"]
        }

        questions = {
            "component": {
                "type": "choice",
                "instructions": "Which component of Waymark is affected by this report?",
                "criteria": {
                    "engine": "Core policy evaluation engine, path matching, bash truncation, snapshots, rollback",
                    "mcp_server": "Model Context Protocol JSON-RPC server and protocol transport",
                    "cli": "Command-line interface commands, terminal flags, stdout formatting",
                    "ci_cd": "GitHub Actions workflows, release pipelines, testing matrices, git hooks",
                    "docs": "Documentation, mkdocs, guides, licensing text, markdown files"
                }
            },
            "category": {
                "type": "choice",
                "instructions": "Classify the type of development task this report represents.",
                "criteria": {
                    "feat": "New user-facing functionality or CLI capability",
                    "fix": "Bug fix, regression repair, or error correction",
                    "chore": "Maintenance, dependency bump, documentation update, or workflow polish",
                    "security": "Vulnerability fix, secret scanner repair, or security boundary hardening"
                }
            },
            "complexity_score": {
                "type": "score",
                "instructions": "Estimate the development complexity and effort required for this task.",
                "criteria": [
                    "Level 1: Trivial text change or docs edit",
                    "Level 2: Minor CLI flag or simple error handler",
                    "Level 3: Standard feature implementation or isolated module edit",
                    "Level 4: Complex cross-platform bug or architectural refactor",
                    "Level 5: High-stakes security boundary or core protocol redesign"
                ]
            },
            "needs_adr": {
                "type": "noul",
                "instructions": "Does this proposed change alter architectural design, cross-platform behavior, or security boundaries requiring an Architectural Decision Record (ADR)?",
                "criteria": {
                    "true": "Architectural change, security boundary modification, or cross-platform redesign",
                    "false": "Standard bug fix, documentation addition, or routine chore"
                }
            }
        }

        eval_res = client.evaluate(state=state, questions=questions)

        total_latency += eval_res.latency_ms
        total_cost += eval_res.cost_usd

        answers = eval_res.answers
        
        # Schema validity check
        has_all_keys = all(k in answers for k in ["component", "category", "complexity_score", "needs_adr"])
        has_valid_types = (
            isinstance(answers.get("component", {}).get("choice"), str) and
            isinstance(answers.get("category", {}).get("choice"), str) and
            isinstance(answers.get("complexity_score", {}).get("score"), (int, float)) and
            isinstance(answers.get("needs_adr", {}).get("noul"), (int, float))
        )
        is_schema_valid = has_all_keys and has_valid_types
        if is_schema_valid:
            schema_valid_count += 1

        chosen_comp = answers.get("component", {}).get("choice")
        chosen_cat = answers.get("category", {}).get("choice")
        complx = answers.get("complexity_score", {}).get("score", 0.0)
        adr_prob = answers.get("needs_adr", {}).get("noul", 0.0)
        adr_bool = (adr_prob >= 0.50)

        # Field comparisons
        exp = case["expected"]
        comp_match = (chosen_comp == exp["component"])
        cat_match = (chosen_cat == exp["category"])
        adr_match = (adr_bool == exp["needs_adr"])

        case_matches = sum([comp_match, cat_match, adr_match])
        total_fields += 3
        matches_count += case_matches

        all_matched = (case_matches == 3)
        status = f"{Colors.GREEN}EXACT{Colors.END}" if all_matched else f"{Colors.YELLOW}{case_matches}/3{Colors.END}"

        snippet = (case["raw_text"][:33] + "...") if len(case["raw_text"]) > 36 else case["raw_text"]
        print(f"{case['id']:<8} | {snippet:<36} | {chosen_comp:<12} | {chosen_cat:<10} | {str(adr_bool):<5} | {complx:<6.1f} | {status}")

        results.append({
            "id": case["id"],
            "component": chosen_comp,
            "category": chosen_cat,
            "complexity": complx,
            "needs_adr": adr_bool,
            "all_matched": all_matched
        })

    # Calculations
    total_cases = len(RAW_ISSUE_REPORTS)
    schema_valid_pct = (schema_valid_count / total_cases) * 100.0
    field_accuracy_pct = (matches_count / total_fields) * 100.0
    avg_latency = total_latency / total_cases

    print("\n" + "=" * 75)
    print(f"{Colors.BOLD}QUANTITATIVE RESULTS & GO/NO-GO THRESHOLDS{Colors.END}")
    print("=" * 75)
    print(f"  Schema Adherence (Typed Output)   : {schema_valid_count}/{total_cases} ({schema_valid_pct:.1f}%)")
    print(f"  Field Agreement with Human Triage : {matches_count}/{total_fields} ({field_accuracy_pct:.1f}%)")
    print(f"  Average Single-Shot Latency       : {avg_latency:.1f} ms")
    print(f"  Total Ingestion Cost (8 Issues)   : ${total_cost:.6f}")
    print("-" * 75)

    # Threshold checks
    pass_schema = (schema_valid_pct == 100.0)
    pass_agreement = (field_accuracy_pct >= 90.0)
    pass_latency = (avg_latency < 700.0)
    overall_go = pass_schema and pass_agreement and pass_latency

    print_threshold_verdict("100% Schema Adherence (==100%)", pass_schema, f"Observed {schema_valid_pct:.1f}%")
    print_threshold_verdict("Field Agreement (>=90%)", pass_agreement, f"Observed {field_accuracy_pct:.1f}%")
    print_threshold_verdict("Latency Ceiling (<700ms)", pass_latency, f"Observed {avg_latency:.1f} ms")

    print("\n" + "-" * 75)
    if overall_go:
        print(f"  {Colors.BOLD}{Colors.GREEN}★ EXPERIMENT 5 VERDICT: GO (Adopt Issue & Backlog Triage){Colors.END}")
    else:
        print(f"  {Colors.BOLD}{Colors.RED}★ EXPERIMENT 5 VERDICT: NO-GO (Thresholds Not Met){Colors.END}")
    print("-" * 75 + "\n")

    return {
        "experiment": "exp5_issue_triage",
        "verdict": "GO" if overall_go else "NO-GO",
        "schema_adherence_pct": schema_valid_pct,
        "agreement_pct": field_accuracy_pct,
        "avg_latency_ms": avg_latency
    }

if __name__ == "__main__":
    run_experiment_5()
