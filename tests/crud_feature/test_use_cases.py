from crud_feature.application.use_cases import CreateCrudFeatureUseCase
from crud_feature.infrastructure.repositories import InMemoryCrudFeatureRepository


def test_crud_feature_use_case_saves_entity() -> None:
    use_case = CreateCrudFeatureUseCase(InMemoryCrudFeatureRepository())
    entity = use_case.execute(entity_id='1', name='example')

    assert entity.id == '1'
    assert entity.name == 'example'
