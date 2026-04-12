from pathlib import Path

from local_coding_agent.config import Settings
from local_coding_agent.tools.scaffolding import create_clean_architecture_feature


def test_create_python_feature(tmp_path: Path) -> None:
    settings = Settings(workspace_root=tmp_path)

    result = create_clean_architecture_feature(
        settings,
        feature_name="billing",
        language="python",
        source_dir="src",
        include_tests=True,
    )

    assert result["feature_name"] == "billing"
    assert (tmp_path / "src" / "billing" / "domain" / "entities.py").exists()
    assert (tmp_path / "tests" / "billing" / "test_use_cases.py").exists()


def test_create_typescript_feature(tmp_path: Path) -> None:
    settings = Settings(workspace_root=tmp_path)

    result = create_clean_architecture_feature(
        settings,
        feature_name="order-management",
        language="typescript",
        source_dir="src",
        include_tests=False,
    )

    assert result["feature_name"] == "order_management"
    assert (tmp_path / "src" / "order_management" / "application" / "use-cases.ts").exists()
