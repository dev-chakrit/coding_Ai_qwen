from dataclasses import dataclass


@dataclass(slots=True)
class CrudFeature:
    id: str
    name: str
