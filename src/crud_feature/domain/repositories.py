from __future__ import annotations

from typing import Protocol

from .entities import CrudFeature


class CrudFeatureRepository(Protocol):
    def save(self, entity: CrudFeature) -> CrudFeature: ...
