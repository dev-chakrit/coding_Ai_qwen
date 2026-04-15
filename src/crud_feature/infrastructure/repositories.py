from __future__ import annotations

from ..domain.entities import CrudFeature
from ..domain.repositories import CrudFeatureRepository


class InMemoryCrudFeatureRepository(CrudFeatureRepository):
    def __init__(self) -> None:
        self._items: dict[str, CrudFeature] = {}

    def save(self, entity: CrudFeature) -> CrudFeature:
        self._items[entity.id] = entity
        return entity
