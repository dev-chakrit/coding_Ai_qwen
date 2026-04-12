from __future__ import annotations

import re
from pathlib import Path

from local_coding_agent.config import Settings
from local_coding_agent.tools.workspace import resolve_workspace_path, to_relative_path


def normalize_feature_name(name: str) -> tuple[str, str, str]:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "_", name).strip("_")
    if not cleaned:
        raise ValueError("feature name must contain letters or numbers")

    snake_case = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", cleaned).lower()
    parts = [part for part in snake_case.split("_") if part]
    kebab_case = "-".join(parts)
    pascal_case = "".join(part.capitalize() for part in parts)
    return snake_case, kebab_case, pascal_case


def python_feature_files(feature_name: str, class_name: str) -> dict[str, str]:
    repository_name = f"{class_name}Repository"
    use_case_name = f"Create{class_name}UseCase"

    return {
        "__init__.py": "",
        "domain/__init__.py": "",
        "domain/entities.py": (
            "from dataclasses import dataclass\n\n\n"
            f"@dataclass(slots=True)\n"
            f"class {class_name}:\n"
            "    id: str\n"
            "    name: str\n"
        ),
        "domain/repositories.py": (
            "from __future__ import annotations\n\n"
            "from typing import Protocol\n\n"
            f"from .entities import {class_name}\n\n\n"
            f"class {repository_name}(Protocol):\n"
            f"    def save(self, entity: {class_name}) -> {class_name}: ...\n"
        ),
        "application/__init__.py": "",
        "application/use_cases.py": (
            "from __future__ import annotations\n\n"
            f"from ..domain.entities import {class_name}\n"
            f"from ..domain.repositories import {repository_name}\n\n\n"
            f"class {use_case_name}:\n"
            f"    def __init__(self, repository: {repository_name}) -> None:\n"
            "        self._repository = repository\n\n"
            f"    def execute(self, entity_id: str, name: str) -> {class_name}:\n"
            f"        entity = {class_name}(id=entity_id, name=name)\n"
            "        return self._repository.save(entity)\n"
        ),
        "infrastructure/__init__.py": "",
        "infrastructure/repositories.py": (
            "from __future__ import annotations\n\n"
            f"from ..domain.entities import {class_name}\n"
            f"from ..domain.repositories import {repository_name}\n\n\n"
            f"class InMemory{repository_name}({repository_name}):\n"
            "    def __init__(self) -> None:\n"
            f"        self._items: dict[str, {class_name}] = {{}}\n\n"
            f"    def save(self, entity: {class_name}) -> {class_name}:\n"
            "        self._items[entity.id] = entity\n"
            "        return entity\n"
        ),
        "presentation/__init__.py": "",
        "presentation/contracts.py": (
            "from dataclasses import dataclass\n\n\n"
            "@dataclass(slots=True)\n"
            f"class Create{class_name}Request:\n"
            "    id: str\n"
            "    name: str\n"
        ),
    }


def python_test_files(feature_name: str, class_name: str) -> dict[str, str]:
    repository_name = f"InMemory{class_name}Repository"
    use_case_name = f"Create{class_name}UseCase"

    return {
        f"tests/{feature_name}/test_use_cases.py": (
            f"from {feature_name}.application.use_cases import {use_case_name}\n"
            f"from {feature_name}.infrastructure.repositories import {repository_name}\n\n\n"
            f"def test_{feature_name}_use_case_saves_entity() -> None:\n"
            f"    use_case = {use_case_name}({repository_name}())\n"
            "    entity = use_case.execute(entity_id='1', name='example')\n\n"
            "    assert entity.id == '1'\n"
            "    assert entity.name == 'example'\n"
        )
    }


def typescript_feature_files(feature_name: str, class_name: str) -> dict[str, str]:
    repository_name = f"{class_name}Repository"
    use_case_name = f"Create{class_name}UseCase"

    return {
        "index.ts": f"export * from './application/use-cases';\n",
        "domain/entities.ts": (
            f"export interface {class_name} {{\n"
            "  id: string;\n"
            "  name: string;\n"
            "}\n"
        ),
        "domain/repositories.ts": (
            f"import type {{ {class_name} }} from './entities';\n\n"
            f"export interface {repository_name} {{\n"
            f"  save(entity: {class_name}): Promise<{class_name}>;\n"
            "}\n"
        ),
        "application/use-cases.ts": (
            f"import type {{ {class_name} }} from '../domain/entities';\n"
            f"import type {{ {repository_name} }} from '../domain/repositories';\n\n"
            f"export class {use_case_name} {{\n"
            f"  constructor(private readonly repository: {repository_name}) {{}}\n\n"
            f"  async execute(id: string, name: string): Promise<{class_name}> {{\n"
            f"    const entity: {class_name} = {{ id, name }};\n"
            "    return this.repository.save(entity);\n"
            "  }\n"
            "}\n"
        ),
        "infrastructure/repositories.ts": (
            f"import type {{ {class_name} }} from '../domain/entities';\n"
            f"import type {{ {repository_name} }} from '../domain/repositories';\n\n"
            f"export class InMemory{repository_name} implements {repository_name} {{\n"
            f"  private readonly items = new Map<string, {class_name}>();\n\n"
            f"  async save(entity: {class_name}): Promise<{class_name}> {{\n"
            "    this.items.set(entity.id, entity);\n"
            "    return entity;\n"
            "  }\n"
            "}\n"
        ),
        "presentation/contracts.ts": (
            f"export interface Create{class_name}Request {{\n"
            "  id: string;\n"
            "  name: string;\n"
            "}\n"
        ),
    }


def typescript_test_files(feature_name: str, class_name: str) -> dict[str, str]:
    repository_name = f"InMemory{class_name}Repository"
    use_case_name = f"Create{class_name}UseCase"

    return {
        f"tests/{feature_name}/use-cases.spec.ts": (
            f"import {{ {use_case_name} }} from '../../src/{feature_name}/application/use-cases';\n"
            f"import {{ {repository_name} }} from '../../src/{feature_name}/infrastructure/repositories';\n\n"
            f"describe('{use_case_name}', () => {{\n"
            "  it('saves an entity', async () => {\n"
            f"    const useCase = new {use_case_name}(new {repository_name}());\n"
            "    const entity = await useCase.execute('1', 'example');\n\n"
            "    expect(entity.id).toBe('1');\n"
            "    expect(entity.name).toBe('example');\n"
            "  });\n"
            "});\n"
        )
    }


def create_clean_architecture_feature(
    settings: Settings,
    feature_name: str,
    language: str = "python",
    source_dir: str = "src",
    include_tests: bool = True,
) -> dict:
    snake_case, _, pascal_case = normalize_feature_name(feature_name)
    source_root = resolve_workspace_path(settings, source_dir)
    feature_root = source_root / snake_case

    if language not in {"python", "typescript"}:
        raise ValueError("language must be 'python' or 'typescript'")

    files = (
        python_feature_files(snake_case, pascal_case)
        if language == "python"
        else typescript_feature_files(snake_case, pascal_case)
    )

    if include_tests:
        test_files = (
            python_test_files(snake_case, pascal_case)
            if language == "python"
            else typescript_test_files(snake_case, pascal_case)
        )
    else:
        test_files = {}

    created: list[str] = []
    skipped: list[str] = []

    for relative_path, content in files.items():
        target = feature_root / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            skipped.append(to_relative_path(settings, target))
            continue
        target.write_text(content, encoding="utf-8")
        created.append(to_relative_path(settings, target))

    for relative_path, content in test_files.items():
        target = settings.workspace_root / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            skipped.append(to_relative_path(settings, target))
            continue
        target.write_text(content, encoding="utf-8")
        created.append(to_relative_path(settings, target))

    return {
        "feature_name": snake_case,
        "language": language,
        "source_dir": to_relative_path(settings, source_root),
        "feature_root": to_relative_path(settings, feature_root),
        "created": created,
        "skipped": skipped,
    }
