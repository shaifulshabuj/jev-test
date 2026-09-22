"""
Fixtures for Experiment 2: Intelligent Tiered Model Routing in Waymark Development.
"""

ROUTING_TIERS = {
    "tier_0_local_script": "Trivial or deterministic operation: formatting, simple git command, version bump script, dry run.",
    "tier_1_fast_model": "Routine semantic task with low complexity: changelog compilation, documentation formatting, simple comment additions.",
    "tier_2_frontier_model": "Complex, algorithmic, security-sensitive, or architectural engineering: race conditions, regex policy engine, security scanners, multi-file refactors."
}

WAYMARK_DEV_TASKS = [
    {
        "id": "task_1",
        "description": "Run prettier --check docs/ to verify code style formatting.",
        "expected_tier": "tier_0_local_script",
        "category": "formatting"
    },
    {
        "id": "task_2",
        "description": "Bump version in packages/engine/package.json to 6.0.1.",
        "expected_tier": "tier_0_local_script",
        "category": "chore"
    },
    {
        "id": "task_3",
        "description": "Clean out tmp/ before running npm pack.",
        "expected_tier": "tier_0_local_script",
        "category": "cleanup"
    },
    {
        "id": "task_4",
        "description": "Generate formatted release notes markdown from git log v5.1.0..v6.0.0.",
        "expected_tier": "tier_1_fast_model",
        "category": "documentation"
    },
    {
        "id": "task_5",
        "description": "Draft concise one-paragraph summary of the proprietary freeware license change for the README.",
        "expected_tier": "tier_1_fast_model",
        "category": "documentation"
    },
    {
        "id": "task_6",
        "description": "Translate error code E_POLICY_DENIED into friendly developer diagnostic message in CLI output.",
        "expected_tier": "tier_1_fast_model",
        "category": "ux_polish"
    },
    {
        "id": "task_7",
        "description": "Reformat CHANGELOG.md into KeepAChangelog structure with release dates.",
        "expected_tier": "tier_1_fast_model",
        "category": "documentation"
    },
    {
        "id": "task_8",
        "description": "Add TypeScript docstrings and parameter descriptions to truncateBashOutput utility.",
        "expected_tier": "tier_1_fast_model",
        "category": "docs"
    },
    {
        "id": "task_9",
        "description": "Fix Windows micromatch path escape bug where backslashes are interpreted as escapes and cause false-positive denials.",
        "expected_tier": "tier_2_frontier_model",
        "category": "bugfix_algorithmic"
    },
    {
        "id": "task_10",
        "description": "Fix secret scanner execution order where scanner ran after git commit hook and failed open on detected tokens.",
        "expected_tier": "tier_2_frontier_model",
        "category": "security_critical"
    },
    {
        "id": "task_11",
        "description": "Redesign before-snapshot capture in engine to ensure atomic rollback when write_file encounters EACCES mid-stream.",
        "expected_tier": "tier_2_frontier_model",
        "category": "architecture_resilience"
    },
    {
        "id": "task_12",
        "description": "Investigate why vitest test suite reported 0 tests executed in CI due to missing import without failing build.",
        "expected_tier": "tier_2_frontier_model",
        "category": "ci_debugging"
    },
    {
        "id": "task_13",
        "description": "Implement regex bash output truncation helper enforcing maxBashOutputBytes with multibyte UTF-8 safety.",
        "expected_tier": "tier_2_frontier_model",
        "category": "feature_core"
    },
    {
        "id": "task_14",
        "description": "Check git branch status and verify working tree is clean.",
        "expected_tier": "tier_0_local_script",
        "category": "git_status"
    },
    {
        "id": "task_15",
        "description": "Audit release.yml to ensure packages/ source sync exclusions prevent leaking private TypeScript files.",
        "expected_tier": "tier_2_frontier_model",
        "category": "security_release"
    }
]
