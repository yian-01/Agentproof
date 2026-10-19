from agentproof.core import RefundSandbox, Scenario, run_scenario
from agentproof.demo import FixedRefundAgent, demo_results


def test_buggy_agent_is_detected():
    result = demo_results()["buggy"]
    assert not result.passed
    assert result.actual_refund_count == 2
    assert any(event["event"] == "response_lost" for event in result.trace)


def test_fixed_agent_passes():
    result = demo_results()["fixed"]
    assert result.passed
    assert result.actual_refund_count == 1
    assert any(event["event"] == "deduplicated" for event in result.trace)


def test_normal_execution_passes():
    assert run_scenario(FixedRefundAgent(), Scenario("normal")).passed


def test_sandbox_never_reuses_state():
    assert demo_results()["buggy"].actual_refund_count == 2
    assert demo_results()["buggy"].actual_refund_count == 2


def test_invalid_amount_is_rejected():
    sandbox = RefundSandbox()
    try:
        sandbox.refund("order", -1)
        assert False, "expected ValueError"
    except ValueError:
        assert sandbox.refunds == []
