# AgentProof — Product Requirements (V0.1 → V1.0)

## Product statement
AgentProof is an open-source reliability testing toolkit for AI agents. It injects controlled failures at tool boundaries, verifies business invariants using isolated state, and preserves evidence for debugging and regression testing.

## Target users
- Python agent developers building tool-using applications
- Engineering teams validating side-effecting agent workflows
- QA / reliability engineers testing tool failures and recovery behavior

## Core job to be done
"Before deploying my agent, help me prove that it behaves correctly under specified failures, with reproducible evidence."

## Differentiation hypothesis (not yet validated)
State-aware faults such as **commit succeeds, response lost** and deterministic verification of side effects. Compare against DeepEval and other existing agent evaluation frameworks before making differentiation claims.

## V0.1 acceptance criteria
1. A synthetic buggy refund agent duplicates a side effect under a response-loss fault.
2. A fixed agent with an idempotency key does not duplicate it.
3. Both are tested using the same scenario.
4. Test results contain structured event traces and explicit assertions.
5. `pytest` and the CLI run without API keys, network, or real payment systems.
6. CI executes tests on every PR.

## V0.1 exclusions
LLM-based diagnosis, GUI, multi-user auth, real payment APIs, remote agent execution, arbitrary process injection, production readiness.

## V0.2 acceptance criteria (planned)
- Async runner and tool adapters
- Three fault kinds: timeout-before-commit, response-lost-after-commit, rate limit
- Schema-validated YAML scenario DSL
- External LangGraph integration test
- HTML and JSON reports

## V0.3 acceptance criteria (planned)
- Opt-in LLM scenario drafting and diagnosis with BYOK
- Grounded diagnoses referencing trace event IDs
- Explicit separation between deterministic verdict and model suggestions
- Token/cost budgets and offline mode

## V1.0 acceptance criteria (planned)
- Documented SDK and CLI with stable public interfaces
- Versioned scenario schemas, compatibility policy, CI integration
- At least 3 external agent examples and fault benchmark dataset
- Security and privacy review, isolated runners, reproducible reports

## Metrics
- True defect detection on curated benchmark cases
- False positive rate on correct agents
- Reproduction rate under fixed simulated tool responses
- Overhead relative to agent baseline
- User time-to-first-test

Do not report numerical results until measured.
