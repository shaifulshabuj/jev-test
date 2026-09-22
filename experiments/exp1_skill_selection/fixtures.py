"""
Fixtures for Experiment 1: Dynamic Dev Skill & MCP Tool Selection in Waymark Dev Workflow.
"""

# The roster of 20 MCP and development tools available in the Waymark workspace
DEV_TOOL_ROSTER = {
    "docuflow_read_module": {
        "summary": "Analyse a single file: classes, functions, AST imports, config refs, and raw content.",
        "full_schema_tokens": 190
    },
    "docuflow_list_modules": {
        "summary": "Walk codebase directories, extract high-level architecture facts and file inventory.",
        "full_schema_tokens": 180
    },
    "docuflow_write_spec": {
        "summary": "Write and persist a technical design or architectural specification to specs directory.",
        "full_schema_tokens": 210
    },
    "docuflow_query_wiki": {
        "summary": "Search living wiki, synthesize answers with citations about codebase architecture.",
        "full_schema_tokens": 220
    },
    "docuflow_lint_wiki": {
        "summary": "Health check for living wiki: detects orphan pages, broken links, and stale references.",
        "full_schema_tokens": 175
    },
    "vitest_run_unit": {
        "summary": "Run Vitest unit tests for targeted test files or matching pattern.",
        "full_schema_tokens": 195
    },
    "vitest_run_coverage": {
        "summary": "Run full test suite with Istanbul/V8 code coverage report generation.",
        "full_schema_tokens": 205
    },
    "ci_matrix_runner": {
        "summary": "Simulate and trigger cross-platform testing matrix across macOS, Windows, and Ubuntu.",
        "full_schema_tokens": 230
    },
    "secret_scanner_precommit": {
        "summary": "Scan diffs and commits for exposed tokens, private keys, and fails-open conditions.",
        "full_schema_tokens": 215
    },
    "git_status_diff": {
        "summary": "Inspect working tree modifications, staged changes, and branch commit distance.",
        "full_schema_tokens": 160
    },
    "changelog_generator": {
        "summary": "Parse recent conventional commits and compile formatted CHANGELOG entries.",
        "full_schema_tokens": 200
    },
    "npm_version_bump": {
        "summary": "Synchronize and increment semver versions across monorepo package.json files.",
        "full_schema_tokens": 185
    },
    "npm_publish_dry_run": {
        "summary": "Perform dry-run tarball packaging and verify npm registry publishing constraints.",
        "full_schema_tokens": 210
    },
    "eslint_fix": {
        "summary": "Run ESLint across TypeScript source files with auto-fixing for stylistic rules.",
        "full_schema_tokens": 170
    },
    "prettier_format": {
        "summary": "Format markdown, JSON, and source code files using Prettier formatting rules.",
        "full_schema_tokens": 150
    },
    "markdownlint_check": {
        "summary": "Lint markdown documentation against GFM rules and header conventions.",
        "full_schema_tokens": 165
    },
    "esbuild_bundle": {
        "summary": "Compile and bundle TypeScript MCP server and CLI packages into dist outputs.",
        "full_schema_tokens": 190
    },
    "docker_compose_test": {
        "summary": "Spin up isolated Docker containers for integration test environments.",
        "full_schema_tokens": 220
    },
    "waymark_policy_check": {
        "summary": "Validate waymark.config.json syntax, allowedPaths, and blockedCommands rules.",
        "full_schema_tokens": 190
    },
    "ast_import_rewriter": {
        "summary": "Automated AST codemod to rewrite import paths and module dependencies.",
        "full_schema_tokens": 210
    }
}

# 10 Representative Waymark Development Prompts
DEV_PROMPT_CASES = [
    {
        "id": "case_1",
        "prompt": "Find all TypeScript modules in packages/engine that implement the truncateBashOutput helper.",
        "expected_tool": "docuflow_read_module"
    },
    {
        "id": "case_2",
        "prompt": "Run the cross-platform testing suite across Ubuntu, Windows, and macOS to verify the new build.",
        "expected_tool": "ci_matrix_runner"
    },
    {
        "id": "case_3",
        "prompt": "Verify whether the secret scanner execution order fails open when a commit hook runs.",
        "expected_tool": "secret_scanner_precommit"
    },
    {
        "id": "case_4",
        "prompt": "Run the unit tests for micromatch path escaping on Windows: vitest run packages/engine/tests/windows-path.test.ts",
        "expected_tool": "vitest_run_unit"
    },
    {
        "id": "case_5",
        "prompt": "Bump versions across all workspace packages from 5.1.0 to 6.0.0 and sync package.json.",
        "expected_tool": "npm_version_bump"
    },
    {
        "id": "case_6",
        "prompt": "Check the living wiki for broken links, missing citations, or stale pages after the v6 proprietary pivot.",
        "expected_tool": "docuflow_lint_wiki"
    },
    {
        "id": "case_7",
        "prompt": "Format all markdown files in docs/ and mkdocs-docs/ before creating the release commit.",
        "expected_tool": "prettier_format"
    },
    {
        "id": "case_8",
        "prompt": "Compile and bundle the TypeScript MCP server into dist/mcp/server.js.",
        "expected_tool": "esbuild_bundle"
    },
    {
        "id": "case_9",
        "prompt": "Ask the codebase wiki how the before-snapshots and rollback recovery mechanism is structured.",
        "expected_tool": "docuflow_query_wiki"
    },
    {
        "id": "case_10",
        "prompt": "Check the git status and diff to verify no uncommitted files remain in the working tree.",
        "expected_tool": "git_status_diff"
    }
]
