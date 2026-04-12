from __future__ import annotations

import json
from pathlib import Path

from local_coding_agent.quality_gates import (
    load_quality_gate_config,
    run_quality_gates,
    select_quality_gate_commands,
)


def write_config(tmp_path: Path, command: str) -> None:
    payload = {
        "version": 1,
        "default": [command],
        "groups": [
            {
                "name": "python",
                "patterns": ["src/**/*.py"],
                "commands": [command],
            }
        ],
    }
    (tmp_path / "quality-gates.json").write_text(json.dumps(payload), encoding="utf-8")


def test_select_quality_gate_commands_matches_changed_paths(tmp_path: Path) -> None:
    write_config(tmp_path, "python -c \"print('ok')\"")
    config = load_quality_gate_config(tmp_path)

    result = select_quality_gate_commands(config, changed_paths=["src/example.py"])

    assert result["commands"] == ["python -c \"print('ok')\""]
    assert result["matched_groups"][0]["name"] == "python"


def test_run_quality_gates_reports_failure(tmp_path: Path) -> None:
    write_config(tmp_path, "python -c \"import sys; sys.exit(3)\"")
    config = load_quality_gate_config(tmp_path)

    result = run_quality_gates(config, changed_paths=["src/example.py"], timeout_seconds=30)

    assert result["passed"] is False
    assert result["results"][0]["exit_code"] == 3
