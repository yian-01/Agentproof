# Architecture Decision Record — ADR-001

## Decision
Build a **Python modular monolith** with a framework-neutral core and adapters. Begin with a deterministic, synchronous in-memory simulation. Introduce async execution and external adapters after the core semantics are tested.

## Core boundaries
- **Agent protocol**: invokes an injected tool interface.
- **Fault injector**: controls *when* an exception is delivered relative to side effects.
- **Sandbox**: owns isolated, inspectable business state.
- **Assertion engine**: evaluates explicit invariants independently of model text.
- **Trace**: records ordered events and outcomes for diagnostics.
- **CLI**: renders outcomes and exports machine-readable JSON.

## Critical semantics
`response_lost_after_commit` must commit state *before* raising the simulated timeout. The first call changes state; a retry may create a duplicate unless the tool is idempotent. The test checks **committed refund records**, not what the agent claims happened.

## Threat and trust model
- Agent output and tool responses are untrusted.
- Tests must never use real money or production resources.
- LLM judgments cannot override deterministic assertions.
- Future tool adapters require explicit allowlists, isolation and secret redaction.

## Known limitations
- Current sandbox is in-memory and single-process.
- No true LLM replay: a future trace replay can deterministically replay tool responses, but model outputs may vary unless recorded or stubbed.
- The initial protocol tests a small fixed agent shape, not arbitrary frameworks.
- The example demonstrates a defect class, not broad effectiveness.

## Planned evolution
Core -> async scenario DSL -> adapters -> trace persistence -> optional LLM diagnosis -> UI. Avoid microservices until deployment requirements justify them.
