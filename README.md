# Jev & TypeSafe System One: Engineering Evaluation & Research Repository

This repository contains documentation, empirical benchmarks, production integration patterns, and the comprehensive engineering thesis evaluating **Jev (TypeSafe AI)** as a **System One Semantic Coprocessor** within an autonomous multi-agent engineering organization.

---

## 📚 Core Publications & Deliverables

1. 📖 **[The Definitive Engineering Thesis: Dual-Process Cognitive Architecture for Autonomous Agentic Organizations](THESIS_DUAL_PROCESS_AGENTIC_ORGANIZATION.md)**  
   *Comprehensive academic & engineering paper covering the theoretical foundation, 4 interception layers, mathematical calibration, empirical findings on Waymark v6.0.1, failure modes, and a community implementation blueprint.*

2. 📊 **[Executive Decision Scorecard (Pre-Flight Experiments)](DECISION_SCORECARD.md)**  
   *Results of 5 empirical benchmarks across 55 real-world development scenarios: Tool Selection, Tiered Model Dispatch, PR Review Gating, Pre-Execution Command Guardrails, and Issue Triage.*

3. 🔬 **[Waymark Real-Task Comparative Report: Lane A vs. Lane B](WAYMARK_LANES_COMPARISON.md)**  
   *Head-to-head evaluation across 4 progressive development cycles on parallel Git branches in [Waymark](https://github.com/waymarks/waymark) (`eval/lane-a-current-org` vs `eval/lane-b-org-plus-jev`). Detailed token telemetry breaking down Frontier LLM subscription tokens vs. Jev auxiliary tokens.*

---

## 1. Executive Summary: What is Jev?

**Jev** is TypeSafe AI's flagship **System One model**.

Drawing inspiration from Daniel Kahneman’s *Thinking, Fast and Slow*, System 1 represents fast, intuitive, and calibrated judgment, while System 2 represents slow, deliberative reasoning.

* **What Jev is:** A high-speed, cost-effective semantic decision engine designed for software. It evaluates a given `state` (code, diff, bash command, or prompt) against a set of typed `questions` in parallel, returning typed values, calibrated probabilities, and confidence scores directly usable in application logic.
* **What Jev is not:** Jev is not a conversational chatbot, prose generator, or code synthesizer (like Claude, GPT, or Gemini). It does not stream tokens, explain reasoning, or execute autonomous loops.
* **The Division of Labor:**
  * **Code / Workflow (The Hard Shell):** Controls state, executes tools, enforces hard business logic, and manages deterministic operations.
  * **System One (Jev):** Supplies fast, calibrated semantic judgments (routing, classification, scoring, guardrails).
  * **System Two (Frontier LLMs):** Engaged selectively for deep synthesis, complex coding, and strategic planning.

---

## 2. Key Empirical Findings (At a Glance)

Evaluated against [Waymark](https://github.com/waymarks/waymark) (`v6.0.1`, 38 test suites, 696 tests):

| Metric | Lane A: Current Org Baseline | Lane B: Org + Jev System One | Net Improvement |
| :--- | :--- | :--- | :--- |
| **Frontier Subscription Tokens** | 88,700 tokens | **16,462 tokens** | **81.4% quota preserved** |
| **Prompt Ingestion Bloat** | 80,850 tokens | **8,550 tokens** | **89.4% context reduction** |
| **Destructive Command Containment**| 0 pre-flight checks | **100% intercepted (7/7)** | Zero uncontained side-effects |
| **Passing Test Suite** | 696 / 696 passed | **696 / 696 passed** | 100% green integrity |
| **Evaluation Latency** | 14.2s / turn (Frontier) | **511ms** (Jev) | Sub-second decision speed |

---

## 3. The Three Typed Primitives

All evaluations accept an input `state` (plain text string or structured JSON object/array) and evaluate typed questions in parallel:

### A. `noul` (Boolean Hypothesis Testing)
Evaluates whether a condition or statement is true.
* **Returns:** `noul` (float between `0.0` and `1.0`), representing the calibrated probability of "yes".
* **Use Cases:** Safety checks, guardrails, presence detection, truth verification.
```json
{
  "is_destructive": {
    "type": "noul",
    "instructions": "Does this shell command permanently delete uncommitted code or drop database tables?",
    "criteria": {
      "true": "Command removes files without trash/recovery or destroys data",
      "false": "Read-only or safe reversible action"
    }
  }
}
```

### B. `choice` (Categorical Selection)
Selects the best-fitting option from a defined set (up to 255 options).
* **Returns:** `choice` (selected option key), `probabilities` (dictionary of option floats summing to 1.0), and `confidence` (float $0.0 \dots 1.0$).
* **Use Cases:** Intent routing, skill selection, repo/team triage, classification.
```json
{
  "target_worker": {
    "type": "choice",
    "instructions": "Which specialized worker should execute this task?",
    "criteria": {
      "frontend": "UI components, CSS/HTML, client-side React/Vue",
      "backend": "Database queries, API routes, migrations, backend services",
      "devops": "CI/CD pipelines, Docker, shell scripts, environment config"
    }
  }
}
```

### C. `score` (Graded Rubric Rating)
Rates the input along an ordered rubric of 2 to 10 descriptive levels.
* **Returns:** `score` (probability-weighted continuous value across the levels), `legend`, `probabilities`, and `confidence`.
* **Use Cases:** Priority scoring, urgency, risk assessment, content quality grading.
```json
{
  "risk_score": {
    "type": "score",
    "instructions": "Rate the operational risk of running this script in production.",
    "criteria": [
      "Zero risk: read-only status command",
      "Low risk: creates new scratch files without touching existing code",
      "Moderate risk: edits source code or modifies local package installations",
      "High risk: modifies production infrastructure, credentials, or remote databases"
    ]
  }
}
```

---

## 4. Repository Structure & Test Scripts

```
jev-test/
├── THESIS_DUAL_PROCESS_AGENTIC_ORGANIZATION.md   # The complete engineering thesis
├── DECISION_SCORECARD.md                         # Phase 1: 5 empirical micro-benchmarks
├── WAYMARK_LANES_COMPARISON.md                   # Phase 2: Full Waymark dual-lane report
├── README.md                                     # Repository index & guide (this file)
├── test_jev.py                                   # Basic connection & primitive verification
├── run_lane_b_dev_task.py                        # Task 2: RBAC execution & review runner
├── run_lane_b_infra_task.py                      # Task 3: CLI approvals execution runner
├── run_lane_b_resilience_task.py                 # Task 4: Daemon health & init execution runner
├── run_lane_b_pipeline.py                        # Complete 4-phase end-to-end pipeline runner
└── experiments/                                  # Pre-flight test suites (55 test cases)
    ├── exp1_skill_selection/
    ├── exp2_model_routing/
    ├── exp3_pr_review_gate/
    ├── exp4_dev_guardrails/
    └── exp5_issue_triage/
```

---

## 5. Verification & Running the Harness

To verify your Jev connection and execute the tests:

```bash
# Verify API connection and the 3 primitives
python3 test_jev.py

# Run the 5 pre-flight micro-benchmarks
python3 experiments/exp1_skill_selection/run.py
python3 experiments/exp2_model_routing/run.py
python3 experiments/exp3_pr_review_gate/run.py
python3 experiments/exp4_dev_guardrails/run.py
python3 experiments/exp5_issue_triage/run.py

# Run the Waymark Phase 4 resilience task telemetry runner
python3 run_lane_b_resilience_task.py
```

---

## 6. How the Community Can Adopt This

See **Chapter 7 of the [Thesis](THESIS_DUAL_PROCESS_AGENTIC_ORGANIZATION.md#7-implementation-blueprint-for-the-ai-developer-community)** for complete drop-in TypeScript and Python SDK reference implementations, the `.waymark/jev_policies.json` configuration schema, and the phased 4-week rollout guide.
