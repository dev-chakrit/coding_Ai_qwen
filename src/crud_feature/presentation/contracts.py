from dataclasses import dataclass


@dataclass(slots=True)
class CreateCrudFeatureRequest:
    id: str
    name: str
