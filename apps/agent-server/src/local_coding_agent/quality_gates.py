from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from fnmatch import fnmatch
from pathlib import Path, PurePosixPath


QUALITY_GATES_FILENAME = "quality-gates.json"
OUTPUT_LIMIT = 12_000


@dataclass(slots=True)
class GateGroup:
    name: str
    description: str
    patterns: tuple[str, ...]
    commands: tuple[str, ...]


@dataclass(slots=True)
class QualityGateConfig:
    workspace_root: Path
    source_path: Path
    default_commands: tuple[str, ...]
    groups: tuple[GateGroup, ...]


def load_quality_gate_config(workspace_root: Path) -> QualityGateConfig:
    source_path = workspace_root / QUALITY_GATES_FILENAME
    if not source_path.exists():
        return QualityGateConfig(
            workspace_root=workspace_root,
            source_path=source_path,
            default_commands=(),
            groups=(),
        )

    payload = json.loads(source_path.read_text(encoding="utf-8"))
    groups = tuple(
        GateGroup(
            name=item["name"],
            description=item.get("description", ""),
            patterns=tuple(item.get("patterns", [])),
            commands=tuple(item.get("commands", [])),
        )
        for item in payload.get("groups", [])
    )
    return QualityGateConfig(
        workspace_root=workspace_root,
        source_path=source_path,
        default_commands=tuple(payload.get("default", [])),
        groups=groups,
    )


def path_matches_pattern(path: str, pattern: str) -> bool:
    candidates = [pattern]
    if "**/" in pattern:
        candidates.append(pattern.replace("**/", ""))

    posix_path = PurePosixPath(path)
    return any(
        posix_path.match(candidate) or fnmatch(path, candidate) or path == candidate
        for candidate in candidates
    )


def select_quality_gate_commands(
    config: QualityGateConfig,
    changed_paths: list[str] | None = None,
    include_default: bool = True,
) -> dict:
    normalized_paths = [path.replace("\\", "/").lstrip("./") for path in (changed_paths or [])]
    commands: list[str] = list(config.default_commands if include_default else ())
    matched_groups: list[dict[str, object]] = []

    for group in config.groups:
        matched_paths = [
            path
            for path in normalized_paths
            if any(path_matches_pattern(path, pattern) for pattern in group.patterns)
        ]
        if normalized_paths and not matched_paths:
            continue

        matched_groups.append(
            {
                "name": group.name,
                "description": group.description,
                "matched_paths": matched_paths,
                "commands": list(group.commands),
            }
        )
        for command in group.commands:
            if command not in commands:
                commands.append(command)

    return {
        "config_path": config.source_path.as_posix(),
        "changed_paths": normalized_paths,
        "commands": commands,
        "matched_groups": matched_groups,
    }


def run_quality_gates(
    config: QualityGateConfig,
    changed_paths: list[str] | None = None,
    include_default: bool = True,
    timeout_seconds: int = 300,
) -> dict:
    selection = select_quality_gate_commands(
        config,
        changed_paths=changed_paths,
        include_default=include_default,
    )
    results: list[dict[str, object]] = []
    passed = True

    for command in selection["commands"]:
        completed = subprocess.run(
            ["/bin/bash", "-lc", command],
            cwd=config.workspace_root,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
        item = {
            "command": command,
            "exit_code": completed.returncode,
            "stdout": completed.stdout[-OUTPUT_LIMIT:],
            "stderr": completed.stderr[-OUTPUT_LIMIT:],
        }
        results.append(item)
        if completed.returncode != 0:
            passed = False

    return {
        **selection,
        "passed": passed,
        "results": results,
    }


def summarize_quality_gates(config: QualityGateConfig) -> str:
    lines = [
        f"Config: {config.source_path.as_posix()}",
        f"Default commands: {len(config.default_commands)}",
    ]
    for group in config.groups:
        lines.append(
            f"- {group.name}: patterns={len(group.patterns)} commands={len(group.commands)}"
        )
        if group.description:
            lines.append(f"  {group.description}")
    return "\n".join(lines)
