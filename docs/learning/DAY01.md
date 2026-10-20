# Day 1 — Trace the Existing Execution Flow

Date: 2026-10-20
Issue: #1 (AP-002)
Branch: `feat/ap-002-execution-contracts`

## Learning outcomes
- Explain the roles of `Scenario`, `Fault`, `Agent`, `RefundSandbox`, `TestResult`.
- Explain the difference between passing a bound method (`sandbox.refund`) and invoking it (`sandbox.refund(...)`).
- Explain Python structural subtyping via `typing.Protocol`.
- Explain why the scenario runner inspects sandbox state rather than trusting an agent's response.

## Source reading
1. `src/agentproof/demo.py:demo_results` creates a scenario and two different agent implementations.
2. `src/agentproof/core.py:run_scenario` creates a new sandbox for each run.
3. It passes the bound method `sandbox.refund` to `agent.run` as a dependency.
4. The buggy agent retries without an idempotency key.
5. The sandbox records the refund *before* raising `ResponseLost`, causing two committed refunds on retry.
6. The fixed agent retries with the same idempotency key; the sandbox returns the original refund ID.
7. `run_scenario` validates the sandbox's committed refund count and records a structured result.

## Sequence diagram (illustrative)
```text
demo_results
  -> run_scenario(BuggyRefundAgent, scenario)
       -> RefundSandbox(fault)
       -> agent.run(sandbox.refund)
           -> refund(order, 100, key=None)
               -> append refund #1
               -> raise ResponseLost
           -> retry refund(order, 100, key=None)
               -> append refund #2
       -> assert refund count == 1: FAIL

  -> run_scenario(FixedRefundAgent, scenario)
       -> fresh RefundSandbox(fault)
       -> agent.run(sandbox.refund)
           -> refund(order, 100, key="refund:order-001")
               -> append refund #1
               -> raise ResponseLost
           -> retry refund(order, 100, same key)
               -> return existing refund ID
       -> assert refund count == 1: PASS
```

## Independent exercise — do not copy the existing implementation
Create `experiments/day01_protocol.py` locally (not a production module).

1. Implement two classes: `EmailAgent` and `LogAgent`.
2. Give both a `run(send: Callable[[str], None]) -> None` method.
3. Define an `Agent` Protocol that accepts a callable with one string parameter.
4. Write a `Runner` that injects a fake `send` function, captures calls into a list, and prints the list.
5. Explain in your own words: why does this `Runner` not care which concrete Agent implementation it receives?

**Optional extension:** Add a `RuntimeError` in the injected function, capture the exception, and explain why the runner should distinguish ERROR from an assertion FAIL.

## Day 1 acceptance
- [ ] `python -m pytest -q` passes before changes.
- [ ] `python -m agentproof.cli demo` demonstrates bug detection.
- [ ] Independently explain `agent.run(sandbox.refund)` and idempotency behavior.
- [ ] Finish the local exercise and describe what the injection boundary does.
- [ ] Keep all work on `feat/ap-002-execution-contracts`; do not merge until Issue #1 acceptance criteria are met.

## Next
Day 2: dataclass frozen/mutable semantics, `Protocol` vs ABC, typed scenario validation. Expand the contract only after understanding the present code.
