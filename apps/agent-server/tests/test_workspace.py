from pathlib import Path

from local_coding_agent.config import Settings
from local_coding_agent.tools.workspace import read_text_file, replace_in_file, write_text_file


def test_write_and_read_file(tmp_path: Path) -> None:
    settings = Settings(workspace_root=tmp_path)

    write_text_file(settings, "src/example.txt", "alpha\nbeta\ngamma\n", overwrite=False)
    result = read_text_file(settings, "src/example.txt", start_line=2, end_line=3)

    assert result["path"] == "src/example.txt"
    assert result["lines"] == [
        {"line": 2, "text": "beta"},
        {"line": 3, "text": "gamma"},
    ]


def test_replace_in_file(tmp_path: Path) -> None:
    settings = Settings(workspace_root=tmp_path)
    target = tmp_path / "README.md"
    target.write_text("hello local agent\n", encoding="utf-8")

    result = replace_in_file(settings, "README.md", "local", "repo-aware", count=1)

    assert result["replacements"] == 1
    assert target.read_text(encoding="utf-8") == "hello repo-aware agent\n"
