from __future__ import annotations

import argparse
import json
from pathlib import Path

from local_coding_agent.quality_gates import load_quality_gate_config, run_quality_gates


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run repo quality gates.")
    parser.add_argument(
        "--files",
        nargs="*",
        default=[],
        help="Workspace-relative changed files used to select relevant commands.",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=300,
        help="Per-command timeout in seconds.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print full JSON output instead of a short text summary.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    workspace_root = Path(__file__).resolve().parent.parent
    config = load_quality_gate_config(workspace_root)
    result = run_quality_gates(
        config,
        changed_paths=args.files,
        timeout_seconds=args.timeout_seconds,
    )

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"passed: {result['passed']}")
        print(f"commands: {len(result['commands'])}")
        for item in result["results"]:
            print(f"- [{item['exit_code']}] {item['command']}")

    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
