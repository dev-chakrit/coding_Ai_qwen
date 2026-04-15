import { CreateCrudUseCase } from '../../src/crud/application/use-cases';
import { InMemoryCrudRepository } from '../../src/crud/infrastructure/repositories';

describe('CreateCrudUseCase', () => {
  it('saves an entity', async () => {
    const useCase = new CreateCrudUseCase(new InMemoryCrudRepository());
    const entity = await useCase.execute('1', 'example');

    expect(entity.id).toBe('1');
    expect(entity.name).toBe('example');
  });
});
