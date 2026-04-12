from __future__ import annotations

import fnmatch
import os
import re
from pathlib import Path
from typing import Iterable

from local_coding_agent.config import Settings


def resolve_workspace_path(settings: Settings, raw_path: str) -> Path:
    candidate = Path(raw_path)
    if not candidate.is_absolute():
        candidate = settings.workspace_root / candidate
    resolved = candidate.resolve()

    if resolved != settings.workspace_root and settings.workspace_root not in resolved.parents:
        raise ValueError(f"Path escapes workspace root: {raw_path}")

    return resolved


def to_relative_path(settings: Settings, path: Path) -> str:
    return path.relative_to(settings.workspace_root).as_posix()


def should_skip_directory(settings: Settings, directory_name: str) -> bool:
    return directory_name in settings.excluded_dirs


def iter_workspace_files(settings: Settings, base_dir: Path) -> Iterable[Path]:
    for current_root, dirs, files in os.walk(base_dir):
        dirs[:] = [
            directory
            for directory in dirs
            if not should_skip_directory(settings, directory)
        ]

        current_root_path = Path(current_root)
        for file_name in files:
            yield current_root_path / file_name


def workspace_tree(settings: Settings, max_depth: int = 3, max_entries: int = 200) -> dict:
    root = settings.workspace_root
    lines: list[str] = []
    visited = 0
    truncated = False

    def walk(directory: Path, depth: int) -> None:
        nonlocal visited, truncated
        if truncated or depth > max_depth:
            return

        entries = sorted(
            directory.iterdir(),
            key=lambda item: (item.is_file(), item.name.lower()),
        )

        for entry in entries:
            if entry.is_dir() and should_skip_directory(settings, entry.name):
                continue

            if visited >= max_entries:
                truncated = True
                return

            visited += 1
            indent = "  " * depth
            marker = "/" if entry.is_dir() else ""
            lines.append(f"{indent}{entry.name}{marker}")

            if entry.is_dir():
                walk(entry, depth + 1)

    walk(root, depth=0)
    return {
        "workspace_root": root.as_posix(),
        "max_depth": max_depth,
        "max_entries": max_entries,
        "truncated": truncated,
        "tree": "\n".join(lines),
    }


def find_files(
    settings: Settings,
    pattern: str = "*",
    base_path: str = ".",
    max_results: int = 100,
) -> dict:
    base_dir = resolve_workspace_path(settings, base_path)
    matches: list[str] = []

    for path in iter_workspace_files(settings, base_dir):
        relative_path = path.relative_to(base_dir).as_posix()
        if fnmatch.fnmatch(relative_path, pattern) or fnmatch.fnmatch(path.name, pattern):
            matches.append(to_relative_path(settings, path))
            if len(matches) >= max_results:
                break

    return {
        "pattern": pattern,
        "base_path": to_relative_path(settings, base_dir)
        if base_dir != settings.workspace_root
        else ".",
        "matches": matches,
    }


def read_text_file(
    settings: Settings,
    path: str,
    start_line: int = 1,
    end_line: int = 250,
) -> dict:
    if start_line < 1 or end_line < start_line:
        raise ValueError("start_line and end_line are invalid")

    target = resolve_workspace_path(settings, path)
    if not target.exists():
        raise FileNotFoundError(path)
    if not target.is_file():
        raise ValueError(f"Not a file: {path}")

    collected: list[dict[str, str | int]] = []
    total_lines = 0
    consumed_bytes = 0
    truncated = False

    with target.open("r", encoding="utf-8", errors="replace") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            total_lines = line_number
            consumed_bytes += len(raw_line.encode("utf-8", errors="ignore"))
            if consumed_bytes > settings.max_read_bytes:
                truncated = True
                break
            if line_number < start_line:
                continue
            if line_number > end_line:
                break
            collected.append(
                {
                    "line": line_number,
                    "text": raw_line.rstrip("\n"),
                }
            )

    return {
        "path": to_relative_path(settings, target),
        "start_line": start_line,
        "end_line": end_line,
        "truncated": truncated,
        "total_lines_seen": total_lines,
        "lines": collected,
    }


def search_code(
    settings: Settings,
    query: str,
    base_path: str = ".",
    max_results: int = 50,
    case_sensitive: bool = False,
    use_regex: bool = False,
) -> dict:
    if not query:
        raise ValueError("query is required")

    base_dir = resolve_workspace_path(settings, base_path)
    results: list[dict[str, str | int]] = []
    flags = 0 if case_sensitive else re.IGNORECASE
    matcher = re.compile(query if use_regex else re.escape(query), flags)

    for path in iter_workspace_files(settings, base_dir):
        try:
            with path.open("r", encoding="utf-8", errors="ignore") as handle:
                for line_number, line in enumerate(handle, start=1):
                    if matcher.search(line):
                        results.append(
                            {
                                "path": to_relative_path(settings, path),
                                "line": line_number,
                                "text": line.rstrip("\n"),
                            }
                        )
                        if len(results) >= max_results:
                            return {"query": query, "results": results}
        except OSError:
            continue

    return {"query": query, "results": results}


def write_text_file(
    settings: Settings,
    path: str,
    content: str,
    overwrite: bool = False,
) -> dict:
    target = resolve_workspace_path(settings, path)

    if target.exists() and not overwrite:
        raise FileExistsError(
            f"File already exists: {to_relative_path(settings, target)}. Set overwrite=true to replace it."
        )

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")

    return {
        "path": to_relative_path(settings, target),
        "bytes_written": len(content.encode("utf-8")),
        "overwrite": overwrite,
    }


def replace_in_file(
    settings: Settings,
    path: str,
    search: str,
    replace: str,
    count: int = 1,
) -> dict:
    if not search:
        raise ValueError("search must not be empty")

    target = resolve_workspace_path(settings, path)
    original = target.read_text(encoding="utf-8")
    occurrences = original.count(search)

    if occurrences == 0:
        raise ValueError("search text was not found")

    replacement_count = occurrences if count == 0 else min(count, occurrences)
    updated = original.replace(search, replace, replacement_count)
    target.write_text(updated, encoding="utf-8")

    return {
        "path": to_relative_path(settings, target),
        "replacements": replacement_count,
    }
