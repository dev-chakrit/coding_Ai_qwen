from __future__ import annotations

import json
import os
import subprocess
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from local_coding_agent.quality_gates import (
    load_quality_gate_config,
    run_quality_gates,
    summarize_quality_gates,
)


RUNTIME_DIRNAME = ".local-coding-agent-runtime/hooks"
MUTATING_TOOL_HINTS = (
    "edit",
    "write",
    "replace",
    "create",
    "delete",
    "rename",
    "move",
    "scaffold",
)
PATH_KEYS = {
    "path",
    "paths",
    "file",
    "files",
    "filepath",
    "filepaths",
    "uri",
}
SAFE_READONLY_COMMANDS = (
    "git status",
    "git diff",
    "pytest",
    "python -m pytest",
    "uv --directory ./apps/agent-server run pytest",
    "ls",
    "pwd",
    "find ",
    "cat ",
    "sed ",
    "head ",
    "tail ",
    "rg ",
)
DESTRUCTIVE_COMMAND_HINTS = (
    "rm -rf",
    "git reset --hard",
    "git clean -fd",
    "drop table",
    "delete from",
    "truncate ",
    "mkfs",
)


@dataclass(slots=True)
class HookState:
    session_id: str
    edited_files: list[str] = field(default_factory=list)
    edit_generation: int = 0
    last_gate_edit_generation: int = -1
    last_gate_status: str = "not-run"
    last_failure_log: str = ""


def process_hook_event(payload: dict[str, Any], workspace_root: Path, profile: str) -> dict[str, Any]:
    if profile == "session-context":
        return session_context_output(workspace_root)
    if profile == "readonly-guard":
        return readonly_guard_output(payload)
    if profile == "implementation-guard":
        return implementation_guard_output(payload)
    if profile == "track-edits":
        return track_edits_output(payload, workspace_root)
    if profile == "quality-gate":
        return quality_gate_output(payload, workspace_root)
    return {"continue": True}


def session_context_output(workspace_root: Path) -> dict[str, Any]:
    config = load_quality_gate_config(workspace_root)
    branch = current_branch(workspace_root)
    summary = summarize_quality_gates(config)
    return {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": (
                f"Workspace root: {workspace_root.as_posix()} | Branch: {branch}\n"
                "Zed is the primary editor workflow for this repo. In VS Code, prefer the custom agents "
                "for strict plan -> implement -> review flow.\n"
                f"{summary}"
            ),
        }
    }


def readonly_guard_output(payload: dict[str, Any]) -> dict[str, Any]:
    tool_name = str(payload.get("tool_name", ""))
    if is_mutating_tool(tool_name):
        return deny_pre_tool_use("This agent is read-only and must not edit files directly.")

    command = extract_command(payload.get("tool_input"))
    if command and not is_safe_readonly_command(command):
        return deny_pre_tool_use(
            "This read-only agent may inspect or verify, but must not run mutating commands."
        )

    return {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "allow"}}


def implementation_guard_output(payload: dict[str, Any]) -> dict[str, Any]:
    command = extract_command(payload.get("tool_input"))
    if command and is_destructive_command(command):
        return deny_pre_tool_use("Destructive command blocked by repository policy.")

    return {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "allow"}}


def track_edits_output(payload: dict[str, Any], workspace_root: Path) -> dict[str, Any]:
    tool_name = str(payload.get("tool_name", ""))
    if not is_mutating_tool(tool_name):
        return {"continue": True}

    state = load_state(workspace_root, str(payload.get("sessionId", "default")))
    paths = extract_paths(payload.get("tool_input"), workspace_root)
    if paths:
        for path in paths:
            if path not in state.edited_files:
                state.edited_files.append(path)
    state.edit_generation += 1
    save_state(workspace_root, state)
    return {"continue": True}


def quality_gate_output(payload: dict[str, Any], workspace_root: Path) -> dict[str, Any]:
    session_id = str(payload.get("sessionId", "default"))
    state = load_state(workspace_root, session_id)

    if state.edit_generation == 0:
        return {"continue": True}

    if state.last_gate_status == "passed" and state.last_gate_edit_generation == state.edit_generation:
        return {"continue": True}

    if payload.get("stop_hook_active") and state.last_gate_status == "failed":
        return {
            "continue": True,
            "systemMessage": (
                "Quality gate is still failing for the current edits. Either fix the issue or report a concrete blocker."
            ),
        }

    config = load_quality_gate_config(workspace_root)
    result = run_quality_gates(config, changed_paths=state.edited_files, timeout_seconds=300)
    state.last_gate_edit_generation = state.edit_generation

    if result["passed"]:
        state.last_gate_status = "passed"
        state.last_failure_log = ""
        save_state(workspace_root, state)
        return {"continue": True}

    state.last_gate_status = "failed"
    log_path = runtime_root(workspace_root) / f"{session_id}-quality-gate.log"
    log_path.write_text(format_quality_gate_log(result), encoding="utf-8")
    state.last_failure_log = log_path.as_posix()
    save_state(workspace_root, state)

    failing = next(item for item in result["results"] if item["exit_code"] != 0)
    return {
        "hookSpecificOutput": {
            "hookEventName": "Stop",
            "decision": "block",
            "reason": (
                "Quality gate failed after edits. Fix the failure and verify again before stopping. "
                f"Failed command: {failing['command']}"
            ),
        },
        "systemMessage": (
            f"Quality gate log written to {log_path.as_posix()}\n"
            f"Failed command: {failing['command']}\n"
            f"stdout:\n{failing['stdout']}\n"
            f"stderr:\n{failing['stderr']}"
        ),
    }


def current_branch(workspace_root: Path) -> str:
    completed = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=workspace_root,
        capture_output=True,
        text=True,
        check=False,
    )
    branch = completed.stdout.strip()
    return branch or "unknown"


def deny_pre_tool_use(reason: str) -> dict[str, Any]:
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }


def is_mutating_tool(tool_name: str) -> bool:
    lowered = tool_name.lower()
    return any(hint in lowered for hint in MUTATING_TOOL_HINTS)


def is_safe_readonly_command(command: str) -> bool:
    lowered = command.strip().lower()
    return any(lowered.startswith(prefix) for prefix in SAFE_READONLY_COMMANDS)


def is_destructive_command(command: str) -> bool:
    lowered = command.strip().lower()
    return any(hint in lowered for hint in DESTRUCTIVE_COMMAND_HINTS)


def extract_command(tool_input: Any) -> str:
    if isinstance(tool_input, dict):
        for key in ("command", "cmd"):
            value = tool_input.get(key)
            if isinstance(value, str):
                return value
    return ""


def extract_paths(tool_input: Any, workspace_root: Path) -> list[str]:
    collected: list[str] = []

    def walk(value: Any, key: str | None = None) -> None:
        if isinstance(value, dict):
            for child_key, child_value in value.items():
                walk(child_value, child_key.lower())
            return
        if isinstance(value, list):
            for item in value:
                walk(item, key)
            return
        if not isinstance(value, str) or key not in PATH_KEYS:
            return

        normalized = normalize_path(value, workspace_root)
        if normalized and normalized not in collected:
            collected.append(normalized)

    walk(tool_input)
    return collected


def normalize_path(value: str, workspace_root: Path) -> str:
    raw = value.strip()
    if not raw or raw.startswith("http://") or raw.startswith("https://"):
        return ""

    candidate = Path(raw)
    if candidate.is_absolute():
        try:
            return candidate.resolve().relative_to(workspace_root).as_posix()
        except ValueError:
            return ""

    return candidate.as_posix().lstrip("./")


def runtime_root(workspace_root: Path) -> Path:
    target = workspace_root / RUNTIME_DIRNAME
    target.mkdir(parents=True, exist_ok=True)
    return target


def state_path(workspace_root: Path, session_id: str) -> Path:
    safe_id = "".join(ch for ch in session_id if ch.isalnum() or ch in ("-", "_")) or "default"
    return runtime_root(workspace_root) / f"{safe_id}.json"


def load_state(workspace_root: Path, session_id: str) -> HookState:
    target = state_path(workspace_root, session_id)
    if not target.exists():
        return HookState(session_id=session_id)
    payload = json.loads(target.read_text(encoding="utf-8"))
    return HookState(**payload)


def save_state(workspace_root: Path, state: HookState) -> None:
    target = state_path(workspace_root, state.session_id)
    target.write_text(json.dumps(asdict(state), indent=2), encoding="utf-8")


def format_quality_gate_log(result: dict[str, Any]) -> str:
    lines = [
        f"passed: {result['passed']}",
        f"changed_paths: {', '.join(result['changed_paths']) or '(none)'}",
    ]
    for item in result["results"]:
        lines.append("")
        lines.append(f"command: {item['command']}")
        lines.append(f"exit_code: {item['exit_code']}")
        lines.append("stdout:")
        lines.append(str(item["stdout"]))
        lines.append("stderr:")
        lines.append(str(item["stderr"]))
    return "\n".join(lines)
