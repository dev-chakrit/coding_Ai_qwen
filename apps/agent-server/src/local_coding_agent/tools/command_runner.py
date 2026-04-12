from __future__ import annotations

import shlex
import subprocess

from local_coding_agent.config import Settings
from local_coding_agent.tools.workspace import resolve_workspace_path, to_relative_path


def command_is_allowed(settings: Settings, parts: list[str]) -> bool:
    return any(tuple(parts[: len(prefix)]) == prefix for prefix in settings.allowed_command_prefixes)


def run_project_command(
    settings: Settings,
    command: str,
    working_dir: str = ".",
    timeout_seconds: int = 60,
) -> dict:
    if not command:
        raise ValueError("command is required")

    command_parts = shlex.split(command)
    if not command_parts:
        raise ValueError("command is required")
    if not command_is_allowed(settings, command_parts):
        raise ValueError(
            "command is not allowed. Add it to LOCAL_CODING_AGENT_ALLOWED_COMMANDS if you trust it."
        )

    effective_timeout = min(timeout_seconds, settings.max_command_timeout_seconds)
    cwd = resolve_workspace_path(settings, working_dir)
    completed = subprocess.run(
        command_parts,
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=effective_timeout,
        check=False,
    )

    return {
        "command": command,
        "cwd": to_relative_path(settings, cwd) if cwd != settings.workspace_root else ".",
        "exit_code": completed.returncode,
        "stdout": completed.stdout[-12_000:],
        "stderr": completed.stderr[-12_000:],
    }
