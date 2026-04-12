from __future__ import annotations

import os

from mcp.server.fastmcp import FastMCP

from local_coding_agent.config import Settings
from local_coding_agent.quality_gates import (
    load_quality_gate_config,
    run_quality_gates as run_quality_gates_impl,
    select_quality_gate_commands,
    summarize_quality_gates,
)
from local_coding_agent.tools.command_runner import run_project_command as run_project_command_impl
from local_coding_agent.tools.scaffolding import (
    create_clean_architecture_feature as create_clean_architecture_feature_impl,
)
from local_coding_agent.tools.workspace import (
    find_files as find_files_impl,
    read_text_file as read_text_file_impl,
    replace_in_file as replace_in_file_impl,
    search_code as search_code_impl,
    workspace_tree as workspace_tree_impl,
    write_text_file as write_text_file_impl,
)

SETTINGS = Settings.from_env()

CLEAN_ARCHITECTURE_GUIDE = """\
Use clean architecture defaults for this workspace:

- Domain is the innermost layer and must not depend on frameworks, transport, storage, or editor APIs.
- Application orchestrates use cases and depends only on domain abstractions.
- Infrastructure implements ports for persistence, LLM access, and external services.
- Presentation owns transport-facing contracts such as CLI payloads, HTTP DTOs, and editor-facing shapes.
- New features should be added as vertical slices under src/<feature>/ with domain, application, infrastructure, and presentation subfolders.
- Prefer explicit names over generic helpers so future agents can navigate the codebase with minimal ambiguity.
"""

DELIVERY_WORKFLOW_GUIDE = """\
Use a quality-first implementation workflow in this workspace:

- Inspect the relevant code before editing.
- For non-trivial changes, identify the narrowest meaningful verification step first.
- Prefer adding or updating regression tests for reproducible bugs.
- After each meaningful change, run the relevant verification step.
- If tests fail, debug the real cause, implement a maintainable fix, rerun, and repeat until green or blocked.
- Never make failures disappear by weakening tests, muting exceptions, or adding vague fallbacks without explicit approval.
- End by stating what was verified and what still could not be verified.
"""

FRONTEND_QUALITY_GUIDE = """\
Treat frontend quality as part of correctness:

- Use consistent spacing and alignment.
- Preserve clear typographic hierarchy with readable line lengths and line heights.
- Make primary actions obvious and keep visual hierarchy intentional.
- Cover relevant interaction states: hover, focus, disabled, loading, error, and empty states.
- Verify responsive behavior for narrow and wide layouts.
- Avoid generic, low-signal UI. Aim for a polished result.
"""

SENIOR_DELIVERY_GUIDE = """\
Work like a disciplined senior engineer in this workspace:

- Read the surrounding code before proposing changes.
- Define verification before implementation, especially for risky changes.
- Prefer regression tests when there is a reproducible failure.
- Keep fixes maintainable and local to the real cause.
- If verification fails, continue the repair loop until it passes or a real blocker is identified.
- For UI work, include spacing, typography, hierarchy, responsive behavior, and state coverage in the acceptance bar.
- Explain tradeoffs and remaining risks clearly when handing work back to the user.
"""

VISION_WORKFLOW_GUIDE = """\
Use a dedicated vision model for image-heavy tasks in this repo:

- Use the vision model for UI references, screenshots, OCR-style extraction, and visible error states.
- Use the coder model for repo edits, refactors, test repair loops, and final implementation.
- For UI references, ask the vision model to extract layout, spacing, typography, hierarchy, and component patterns.
- For screenshot debugging, ask the vision model to extract the exact error text, paths, line numbers, and likely root cause.
- After the visual analysis, switch back to the coder model and use MCP tools plus quality gates to implement or debug the change.
"""

mcp = FastMCP("local-coding-agent", json_response=True)


@mcp.resource("architecture://clean-architecture-guide")
def clean_architecture_guide() -> str:
    """Return the baseline architecture rules for the workspace."""

    return CLEAN_ARCHITECTURE_GUIDE


@mcp.resource("workflow://delivery-quality")
def delivery_workflow_guide() -> str:
    """Return the expected test-first and repair-loop workflow."""

    return DELIVERY_WORKFLOW_GUIDE


@mcp.resource("design://frontend-quality-guide")
def frontend_quality_guide() -> str:
    """Return the frontend UX/UI quality bar."""

    return FRONTEND_QUALITY_GUIDE


@mcp.resource("workflow://senior-delivery-guide")
def senior_delivery_guide() -> str:
    """Return the repo's senior-style delivery checklist."""

    return SENIOR_DELIVERY_GUIDE


@mcp.resource("workflow://quality-gates")
def quality_gates_guide() -> str:
    """Return the configured quality gate summary for this workspace."""

    config = load_quality_gate_config(SETTINGS.workspace_root)
    return summarize_quality_gates(config)


@mcp.resource("workflow://vision-workflow-guide")
def vision_workflow_guide() -> str:
    """Return the repo's recommended dual-model vision workflow."""

    return VISION_WORKFLOW_GUIDE


@mcp.prompt()
def clean_architecture_prompt(feature_name: str, goal: str, constraints: str = "") -> str:
    """Generate a planning prompt that keeps the model inside clean architecture boundaries."""

    return (
        "You are updating a clean architecture codebase.\n"
        f"Feature: {feature_name}\n"
        f"Goal: {goal}\n"
        f"Constraints: {constraints or 'None provided'}\n"
        "Keep dependencies pointing inward, preserve existing feature slices when possible, "
        "and keep infrastructure concerns out of domain code."
    )


@mcp.prompt()
def repair_loop_prompt(task: str, verification_command: str, failure_summary: str = "") -> str:
    """Generate a prompt for implementing work with a test-first repair loop."""

    return (
        "You are working in a quality-first repository.\n"
        f"Task: {task}\n"
        f"Primary verification command: {verification_command}\n"
        f"Known failure summary: {failure_summary or 'No failure summary provided yet.'}\n"
        "Inspect the relevant code before editing. If the bug is reproducible, add or adjust a regression test "
        "first when practical. Make the smallest maintainable fix, run the verification command, and if it fails, "
        "diagnose the root cause and iterate until green or until a concrete blocker remains."
    )


@mcp.prompt()
def frontend_polish_prompt(surface_name: str, goal: str, constraints: str = "") -> str:
    """Generate a prompt for frontend work with an explicit UX/UI quality bar."""

    return (
        "You are refining a frontend surface with a high UX/UI bar.\n"
        f"Surface: {surface_name}\n"
        f"Goal: {goal}\n"
        f"Constraints: {constraints or 'None provided'}\n"
        "Inspect the existing UI before editing. Improve spacing, typography, hierarchy, alignment, responsive "
        "behavior, and relevant states. Treat accessibility and visual polish as part of correctness, then run the "
        "most relevant local verification steps before stopping."
    )


@mcp.prompt()
def senior_delivery_prompt(task: str, touched_areas: str = "", ui_focus: bool = False) -> str:
    """Generate a prompt for senior-style delivery with plan, verification, and clean implementation."""

    frontend_clause = (
        "This task touches UI, so spacing, typography, visual hierarchy, responsive behavior, and interaction states "
        "are part of correctness."
        if ui_focus
        else "This task is not primarily UI-focused, but user-facing regressions should still be considered."
    )

    return (
        "You are working as a disciplined senior engineer in a local coding workflow.\n"
        f"Task: {task}\n"
        f"Touched areas: {touched_areas or 'Not specified'}\n"
        f"{frontend_clause}\n"
        "Read the relevant files first, define the narrowest verification steps, implement cleanly, and keep iterating "
        "until the relevant quality gates pass or a concrete blocker remains."
    )


@mcp.prompt()
def quality_gate_prompt(task: str, changed_paths: str = "", extra_context: str = "") -> str:
    """Generate a prompt that keeps the model focused on verification and quality gates."""

    return (
        "You are about to implement or finalize a change in a repo with explicit quality gates.\n"
        f"Task: {task}\n"
        f"Changed paths: {changed_paths or 'Not specified'}\n"
        f"Extra context: {extra_context or 'None provided'}\n"
        "Inspect quality-gates.json, identify the relevant commands, and do not stop until they pass or you can "
        "describe a concrete blocker."
    )


@mcp.prompt()
def ui_reference_prompt(goal: str, product_context: str = "", constraints: str = "") -> str:
    """Generate a prompt for analyzing a UI reference image before implementation."""

    return (
        "You are analyzing a UI reference image before handing the work to a coding model.\n"
        f"Goal: {goal}\n"
        f"Product context: {product_context or 'Not specified'}\n"
        f"Constraints: {constraints or 'None provided'}\n"
        "Describe the layout structure, spacing rhythm, typography hierarchy, component patterns, visual hierarchy, "
        "responsive implications, and interaction cues. End with a concise build brief that a coding model can use."
    )


@mcp.prompt()
def screenshot_debug_prompt(task: str, extra_context: str = "") -> str:
    """Generate a prompt for extracting debugging clues from a screenshot."""

    return (
        "You are reading a screenshot to support a repository debugging workflow.\n"
        f"Task: {task}\n"
        f"Extra context: {extra_context or 'None provided'}\n"
        "Extract the exact visible error text, paths, line numbers, UI state clues, and likely root cause. "
        "Then produce a minimal debugging plan for a coding model that has direct repository access."
    )


@mcp.tool()
def workspace_summary(max_depth: int = 3, max_entries: int = 200) -> dict:
    """Summarize the workspace as a tree so the model can reason about project structure."""

    return workspace_tree_impl(SETTINGS, max_depth=max_depth, max_entries=max_entries)


@mcp.tool()
def find_files(pattern: str = "*", base_path: str = ".", max_results: int = 100) -> dict:
    """Find files in the workspace by glob pattern."""

    return find_files_impl(
        SETTINGS,
        pattern=pattern,
        base_path=base_path,
        max_results=max_results,
    )


@mcp.tool()
def search_code(
    query: str,
    base_path: str = ".",
    max_results: int = 50,
    case_sensitive: bool = False,
    use_regex: bool = False,
) -> dict:
    """Search code across the workspace."""

    return search_code_impl(
        SETTINGS,
        query=query,
        base_path=base_path,
        max_results=max_results,
        case_sensitive=case_sensitive,
        use_regex=use_regex,
    )


@mcp.tool()
def read_text_file(path: str, start_line: int = 1, end_line: int = 250) -> dict:
    """Read a text file from the workspace by line range."""

    return read_text_file_impl(
        SETTINGS,
        path=path,
        start_line=start_line,
        end_line=end_line,
    )


@mcp.tool()
def write_text_file(path: str, content: str, overwrite: bool = False) -> dict:
    """Create or overwrite a text file in the workspace."""

    return write_text_file_impl(SETTINGS, path=path, content=content, overwrite=overwrite)


@mcp.tool()
def replace_in_file(path: str, search: str, replace: str, count: int = 1) -> dict:
    """Replace text in a workspace file."""

    return replace_in_file_impl(
        SETTINGS,
        path=path,
        search=search,
        replace=replace,
        count=count,
    )


@mcp.tool()
def create_clean_architecture_feature(
    feature_name: str,
    language: str = "python",
    source_dir: str = "src",
    include_tests: bool = True,
) -> dict:
    """Scaffold a new feature slice using clean architecture defaults."""

    return create_clean_architecture_feature_impl(
        SETTINGS,
        feature_name=feature_name,
        language=language,
        source_dir=source_dir,
        include_tests=include_tests,
    )


@mcp.tool()
def run_project_command(command: str, working_dir: str = ".", timeout_seconds: int = 60) -> dict:
    """Run a non-destructive workspace command if it is allowlisted."""

    return run_project_command_impl(
        SETTINGS,
        command=command,
        working_dir=working_dir,
        timeout_seconds=timeout_seconds,
    )


@mcp.tool()
def get_quality_gates() -> dict:
    """Return the configured quality gate summary for the workspace."""

    config = load_quality_gate_config(SETTINGS.workspace_root)
    selection = select_quality_gate_commands(config, changed_paths=[])
    return {
        "config_path": config.source_path.as_posix(),
        "default_commands": list(config.default_commands),
        "groups": selection["matched_groups"],
        "summary": summarize_quality_gates(config),
    }


@mcp.tool()
def suggest_quality_gate_commands(
    changed_paths: list[str] | None = None,
    include_default: bool = True,
) -> dict:
    """Suggest verification commands based on changed workspace paths and quality-gates.json."""

    config = load_quality_gate_config(SETTINGS.workspace_root)
    return select_quality_gate_commands(
        config,
        changed_paths=changed_paths or [],
        include_default=include_default,
    )


@mcp.tool()
def run_quality_gates(
    changed_paths: list[str] | None = None,
    include_default: bool = True,
    timeout_seconds: int = 300,
) -> dict:
    """Run the configured quality gate commands for the given paths."""

    config = load_quality_gate_config(SETTINGS.workspace_root)
    return run_quality_gates_impl(
        config,
        changed_paths=changed_paths or [],
        include_default=include_default,
        timeout_seconds=timeout_seconds,
    )


def main() -> None:
    transport = os.getenv("LOCAL_CODING_AGENT_TRANSPORT", "stdio")
    mcp.run(transport=transport)
