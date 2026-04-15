from __future__ import annotations

from ..domain.entities import CrudFeature
from ..domain.repositories import CrudFeatureRepository


class CreateCrudFeatureUseCase:
    def __init__(self, repository: CrudFeatureRepository) -> None:
        self._repository = repository

    def execute(self, entity_id: str, name: str) -> CrudFeature:
        entity = CrudFeature(id=entity_id, name=name)
        return self._repository.save(entity)
