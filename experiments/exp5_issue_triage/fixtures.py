"""
Fixtures for Experiment 5: Waymark Issue & Backlog Triage.
"""

RAW_ISSUE_REPORTS = [
    {
        "id": "issue_1",
        "raw_text": "On Windows 11, running commands with backslashes in paths gets immediately denied by policy engine because micromatch treats backslash as an escape character rather than a directory separator.",
        "expected": {
            "component": "engine",
            "category": "fix",
            "needs_adr": True
        }
    },
    {
        "id": "issue_2",
        "raw_text": "The release workflow in .github/workflows/release.yml needs to sync docs with GitHub Pages and trigger npm publish with 2FA tokens.",
        "expected": {
            "component": "ci_cd",
            "category": "chore",
            "needs_adr": False
        }
    },
    {
        "id": "issue_3",
        "raw_text": "Users are requesting a --json output flag for waymark status command so terminal scripts can parse active policies programmatically.",
        "expected": {
            "component": "cli",
            "category": "feat",
            "needs_adr": False
        }
    },
    {
        "id": "issue_4",
        "raw_text": "We need to document the proprietary freeware license change in docs/license.md and add warning banners to public GitHub repo READMEs.",
        "expected": {
            "component": "docs",
            "category": "chore",
            "needs_adr": False
        }
    },
    {
        "id": "issue_5",
        "raw_text": "Critical security bug: secret scanner runs after git commit hook has already staged and created commit object, resulting in leaked keys if pre-commit aborts late.",
        "expected": {
            "component": "ci_cd",
            "category": "security",
            "needs_adr": True
        }
    },
    {
        "id": "issue_6",
        "raw_text": "The MCP server crashes with unhandled rejection when an agent sends a tool request with malformed JSON arguments in process stdin.",
        "expected": {
            "component": "mcp_server",
            "category": "fix",
            "needs_adr": False
        }
    },
    {
        "id": "issue_7",
        "raw_text": "Implement streaming bash output truncation in engine so large logs over 50KB don't exhaust Node.js memory buffers before policy evaluation.",
        "expected": {
            "component": "engine",
            "category": "feat",
            "needs_adr": True
        }
    },
    {
        "id": "issue_8",
        "raw_text": "Update contributing guidelines in CONTRIBUTING.md explaining the new 3-OS matrix test requirements before opening a PR.",
        "expected": {
            "component": "docs",
            "category": "chore",
            "needs_adr": False
        }
    }
]
