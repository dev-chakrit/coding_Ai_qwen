from __future__ import annotations

import json
from pathlib import Path

from local_coding_agent.vscode_hooks import process_hook_event


def test_readonly_guard_denies_mutation(tmp_path: Path) -> None:
    payload = {
        "hookEventName": "PreToolUse",
        "tool_name": "write_text_file",
        "tool_input": {"path": "src/example.py"},
    }

    result = process_hook_event(payload, workspace_root=tmp_path, profile="readonly-guard")

    assert result["hookSpecificOutput"]["permissionDecision"] == "deny"


def test_quality_gate_blocks_when_configured_command_fails(tmp_path: Path) -> None:
    (tmp_path / "quality-gates.json").write_text(
        json.dumps(
            {
                "version": 1,
                "default": ["python -c \"import sys; sys.exit(1)\""],
                "groups": [],
            }
        ),
        encoding="utf-8",
    )

    post_tool_payload = {
        "sessionId": "session-1",
        "tool_name": "write_text_file",
        "tool_input": {"path": "src/example.py"},
    }
    process_hook_event(post_tool_payload, workspace_root=tmp_path, profile="track-edits")

    stop_payload = {
        "sessionId": "session-1",
        "stop_hook_active": False,
    }
    result = process_hook_event(stop_payload, workspace_root=tmp_path, profile="quality-gate")

    assert result["hookSpecificOutput"]["decision"] == "block"
    assert "Quality gate failed" in result["hookSpecificOutput"]["reason"]
