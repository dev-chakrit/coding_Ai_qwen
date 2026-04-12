from local_coding_agent.server import mcp


def test_server_exposes_expected_tools_and_prompts() -> None:
    tool_names = set(mcp._tool_manager._tools.keys())
    prompt_names = set(mcp._prompt_manager._prompts.keys())

    assert {
        "workspace_summary",
        "find_files",
        "search_code",
        "read_text_file",
        "write_text_file",
        "replace_in_file",
        "create_clean_architecture_feature",
        "run_project_command",
        "get_quality_gates",
        "suggest_quality_gate_commands",
        "run_quality_gates",
    }.issubset(tool_names)

    assert {
        "clean_architecture_prompt",
        "repair_loop_prompt",
        "frontend_polish_prompt",
        "senior_delivery_prompt",
        "quality_gate_prompt",
        "ui_reference_prompt",
        "screenshot_debug_prompt",
    }.issubset(prompt_names)
