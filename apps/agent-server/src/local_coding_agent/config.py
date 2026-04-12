from __future__ import annotations

import os
import shlex
from dataclasses import dataclass, field
from pathlib import Path


DEFAULT_ALLOWED_COMMANDS = (
    ("git", "status"),
    ("git", "diff"),
    ("pytest",),
    ("python", "-m", "pytest"),
    ("uv", "run", "pytest"),
    ("npm", "test"),
    ("npm", "run", "lint"),
    ("npm", "run", "build"),
    ("pnpm", "test"),
    ("pnpm", "lint"),
    ("pnpm", "build"),
    ("cargo", "check"),
    ("cargo", "test"),
    ("go", "test", "./..."),
)

DEFAULT_EXCLUDED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
    ".next",
    ".turbo",
    ".mypy_cache",
    ".pytest_cache",
}


@dataclass(slots=True)
class Settings:
    workspace_root: Path
    max_read_bytes: int = 262_144
    max_command_timeout_seconds: int = 180
    excluded_dirs: set[str] = field(default_factory=lambda: set(DEFAULT_EXCLUDED_DIRS))
    allowed_command_prefixes: tuple[tuple[str, ...], ...] = DEFAULT_ALLOWED_COMMANDS

    @classmethod
    def from_env(cls) -> "Settings":
        workspace_root = Path(
            os.getenv("LOCAL_CODING_AGENT_WORKSPACE_ROOT", os.getcwd())
        ).resolve()
        max_read_bytes = int(os.getenv("LOCAL_CODING_AGENT_MAX_READ_BYTES", "262144"))
        timeout = int(os.getenv("LOCAL_CODING_AGENT_MAX_COMMAND_TIMEOUT", "180"))
        allowed = cls._parse_allowed_commands(
            os.getenv("LOCAL_CODING_AGENT_ALLOWED_COMMANDS", "")
        )

        return cls(
            workspace_root=workspace_root,
            max_read_bytes=max_read_bytes,
            max_command_timeout_seconds=timeout,
            allowed_command_prefixes=allowed or DEFAULT_ALLOWED_COMMANDS,
        )

    @staticmethod
    def _parse_allowed_commands(raw_value: str) -> tuple[tuple[str, ...], ...]:
        items: list[tuple[str, ...]] = []
        for command in raw_value.split(";"):
            command = command.strip()
            if not command:
                continue
            parts = tuple(shlex.split(command))
            if parts:
                items.append(parts)
        return tuple(items)
