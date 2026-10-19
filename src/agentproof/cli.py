"""Small stdlib-only CLI for the first milestone."""
import argparse
import json
from dataclasses import asdict
from pathlib import Path

from .demo import demo_results


def main() -> None:
    parser = argparse.ArgumentParser(prog="agentproof", description="Agent reliability testing")
    parser.add_argument("command", choices=["demo"], help="Run the isolated refund benchmark")
    parser.add_argument("--json", dest="json_path", help="Write machine-readable report")
    args = parser.parse_args()
    results = demo_results()
    for label, result in results.items():
        status = "PASS" if result.passed else "FAIL"
        print(f"{label:5} {status:4} refunds={result.actual_refund_count} expected={result.expected_refund_count}")
    if args.json_path:
        output = Path(args.json_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps({k: asdict(v) for k, v in results.items()}, indent=2), encoding="utf-8")
        print(f"Report: {output}")
    # Demo succeeds when it detects the buggy agent AND validates the fixed agent.
    if results["buggy"].passed or not results["fixed"].passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
