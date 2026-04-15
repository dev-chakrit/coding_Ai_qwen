import os
from pathlib import Path

from local_coding_agent.config import Settings


def test_settings_from_env_discovers_git_root(tmp_path: Path, monkeypatch) -> None:
    workspace_root = tmp_path / "sample-repo"
    nested_dir = workspace_root / "apps" / "web"
    nested_dir.mkdir(parents=True)
    (workspace_root / ".git").mkdir()

    monkeypatch.chdir(nested_dir)
    monkeypatch.delenv("LOCAL_CODING_AGENT_WORKSPACE_ROOT", raising=False)
    monkeypatch.delenv("LOCAL_CODING_AGENT_DISCOVER_ROOT", raising=False)

    settings = Settings.from_env()

    assert settings.workspace_root == workspace_root.resolve()


def test_settings_from_env_can_disable_root_discovery(tmp_path: Path, monkeypatch) -> None:
    workspace_root = tmp_path / "sample-repo"
    nested_dir = workspace_root / "apps" / "api"
    nested_dir.mkdir(parents=True)
    (workspace_root / ".git").mkdir()

    monkeypatch.chdir(nested_dir)
    monkeypatch.delenv("LOCAL_CODING_AGENT_WORKSPACE_ROOT", raising=False)
    monkeypatch.setenv("LOCAL_CODING_AGENT_DISCOVER_ROOT", "0")

    settings = Settings.from_env()

    assert settings.workspace_root == nested_dir.resolve()


def test_settings_from_env_honors_explicit_workspace_root(tmp_path: Path, monkeypatch) -> None:
    explicit_root = tmp_path / "explicit-root"
    explicit_root.mkdir()

    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("LOCAL_CODING_AGENT_WORKSPACE_ROOT", os.fspath(explicit_root))

    settings = Settings.from_env()

    assert settings.workspace_root == explicit_root.resolve()
