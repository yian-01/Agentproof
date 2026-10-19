# AgentProof

**Reliability Engineering for AI Agents**

An early-stage, framework-neutral Python prototype for **state-aware fault injection**. This repository currently ships a deterministic **refund simulation** that detects a duplicate side effect after an API response is lost.

> Status: **V0.1 scaffold / proof of concept**, not a production-ready testing platform. No LLM or real payment API is required.

## Quick start (Windows PowerShell)

Prerequisites: Python 3.11+ and Git. From the repository root:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\agentproof.exe demo --json reports/demo.json
```

Expected result:

```text
buggy FAIL refunds=2 expected=1
fixed PASS refunds=1 expected=1
Report: reports/demo.json
```

The CLI exits with status 0 **only if it detects the buggy agent and the fixed agent passes**. This is intentional; the demo's `FAIL` is a successfully detected defect, not a failed CLI execution.

## What is implemented

- Framework-neutral `Agent` protocol (synchronous demo)
- Isolated in-memory refund sandbox
- Response-lost-after-commit fault injection
- Idempotency-key simulation
- Deterministic state assertion and JSON event trace
- CLI demo, unit tests, GitHub Actions CI

## Not yet implemented

- Real LangGraph / OpenAI Agents SDK adapters
- General-purpose fault DSL and async runners
- Deterministic replay of LLM decisions
- AI test generation and diagnosis
- Web dashboard / production hardening

## Architecture

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), [docs/PRD.md](docs/PRD.md), and [docs/ISSUES.md](docs/ISSUES.md).

## Safety

This demo never makes external requests or real refunds. Future tool adapters must default to isolated mocks and deny production side effects unless explicitly and safely configured.

## License

MIT. See [LICENSE](LICENSE).
