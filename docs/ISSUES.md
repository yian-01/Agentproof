# GitHub Issue Backlog

Use each heading as a separate GitHub Issue. Assign exactly one owner per issue; use PRs and review comments for acceptance evidence.

## AP-001 — Bootstrap Python package and CI [P0]
**Scope:** pyproject, src layout, README, unit tests, GitHub Actions.
**Acceptance:** clean Python 3.11+ environment installs editable package; `pytest -q` and `ruff check src tests` pass; CI runs on PR.
**Evidence:** CI run URL and terminal output.

## AP-002 — Define framework-neutral execution contracts [P0]
**Scope:** typed Agent, Scenario, Fault, TestResult and trace event schema.
**Acceptance:** document inputs/outputs, exception semantics, protocol compatibility; tests cover invalid scenarios.
**Evidence:** API documentation and tests.

## AP-003 — Implement state-aware fault injector [P0]
**Scope:** response-lost-after-commit, timeout-before-commit, HTTP 429; occurrence targeting.
**Acceptance:** prove side-effect ordering with deterministic tests; reject unsupported fault kinds; preserve event IDs.
**Evidence:** 3 positive and 3 negative tests.

## AP-004 — Build assertion engine [P0]
**Scope:** explicit state invariants, failure reasons, separate error vs failed assertion.
**Acceptance:** detect duplicate refund, pass idempotent refund, correctly classify agent crashes.
**Evidence:** buggy/fixed comparison and machine-readable output.

## AP-005 — Implement async test runner [P1]
**Scope:** async tool execution, per-test isolation, cancellation, timeout budgets.
**Acceptance:** no state leaks across concurrent tests; cancellation cleans up; timeout cases covered.
**Evidence:** integration tests.

## AP-006 — LangGraph adapter [P1]
**Scope:** minimal real LangGraph agent with injected tool boundary.
**Acceptance:** external agent passes same scenario contract without changing core engine; setup documented.
**Evidence:** runnable example and integration test.

## AP-007 — CLI and report schema [P1]
**Scope:** `agentproof test`, JSON report, human-readable summary and exit codes.
**Acceptance:** valid command help; CI-friendly exit semantics; report schema versioned.
**Evidence:** snapshot tests and CLI demo.

## AP-008 — AI-assisted scenario design (BYOK) [P2]
**Scope:** optional model adapter, structured scenario proposal, human review.
**Acceptance:** works without model key when disabled; no secret logging; invalid model output rejected.
**Evidence:** mocked model tests and documented sample.

## AP-009 — Trace-grounded failure diagnosis [P2]
**Scope:** diagnosis that cites trace events and separates hypothesis from verified cause.
**Acceptance:** no unsupported PASS/FAIL changes; trace evidence links; token budget.
**Evidence:** labeled failure cases and review.

## AP-010 — Benchmark and competitor evaluation [P1]
**Scope:** curated buggy/correct agent pairs, compare available existing testing tools.
**Acceptance:** reproducible scripts, documented test conditions, measured detection and false positive rates.
**Evidence:** benchmark artifacts, not invented metrics.
