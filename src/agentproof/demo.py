"""Synthetic agents for a controlled, repeatable reliability benchmark."""
from __future__ import annotations

from .core import Fault, ResponseLost, Scenario, run_scenario


class BuggyRefundAgent:
    def run(self, refund):
        try:
            refund("order-001", 100, None)
        except ResponseLost:
            refund("order-001", 100, None)


class FixedRefundAgent:
    def run(self, refund):
        key = "refund:order-001"
        try:
            refund("order-001", 100, key)
        except ResponseLost:
            refund("order-001", 100, key)


def demo_results():
    scenario = Scenario("response_lost_after_commit", Fault(tool="refund_order"))
    return {
        "buggy": run_scenario(BuggyRefundAgent(), scenario),
        "fixed": run_scenario(FixedRefundAgent(), scenario),
    }
