"""Framework-neutral deterministic test runner for tool-driven agents."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass(frozen=True)
class Fault:
    tool: str
    kind: str = "response_lost_after_commit"
    occurrence: int = 1


@dataclass(frozen=True)
class Scenario:
    name: str
    fault: Fault | None = None
    expected_refund_count: int = 1


@dataclass
class TestResult:
    name: str
    passed: bool
    actual_refund_count: int
    expected_refund_count: int
    trace: list[dict[str, Any]] = field(default_factory=list)
    error: str | None = None


class ResponseLost(TimeoutError):
    """The side effect was committed, but the tool response was lost."""


class Agent(Protocol):
    def run(self, tool: Callable[[str, int, str | None], str]) -> None: ...


class RefundSandbox:
    """Isolated in-memory fake payment service; never touches real money."""

    def __init__(self, fault: Fault | None = None) -> None:
        self.fault = fault
        self.calls = 0
        self.refunds: list[tuple[str, int]] = []
        self.idempotency_keys: dict[str, str] = {}
        self.trace: list[dict[str, Any]] = []

    def refund(self, order_id: str, amount: int, key: str | None = None) -> str:
        if amount <= 0:
            raise ValueError("amount must be positive")
        self.calls += 1
        if key and key in self.idempotency_keys:
            self.trace.append({"event": "deduplicated", "key": key, "call": self.calls})
            return self.idempotency_keys[key]
        refund_id = f"refund-{len(self.refunds) + 1}"
        self.refunds.append((order_id, amount))
        if key:
            self.idempotency_keys[key] = refund_id
        self.trace.append({"event": "refund_committed", "id": refund_id, "call": self.calls})
        if (self.fault and self.fault.tool == "refund_order"
                and self.fault.kind == "response_lost_after_commit"
                and self.calls == self.fault.occurrence):
            self.trace.append({"event": "response_lost", "call": self.calls})
            raise ResponseLost("Refund committed; response was lost")
        return refund_id


def run_scenario(agent: Agent, scenario: Scenario) -> TestResult:
    sandbox = RefundSandbox(scenario.fault)
    error = None
    try:
        agent.run(sandbox.refund)
    except Exception as exc:  # noqa: BLE001 - agent exceptions are test results
        error = f"{type(exc).__name__}: {exc}"
        sandbox.trace.append({"event": "agent_error", "message": error})
    actual = len(sandbox.refunds)
    return TestResult(
        name=scenario.name,
        passed=actual == scenario.expected_refund_count and error is None,
        actual_refund_count=actual,
        expected_refund_count=scenario.expected_refund_count,
        trace=sandbox.trace,
        error=error,
    )
