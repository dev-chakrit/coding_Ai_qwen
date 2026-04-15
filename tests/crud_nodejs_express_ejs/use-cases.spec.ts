import { CreateCrudNodejsExpressEjsUseCase } from '../../src/crud_nodejs_express_ejs/application/use-cases';
import { InMemoryCrudNodejsExpressEjsRepository } from '../../src/crud_nodejs_express_ejs/infrastructure/repositories';

describe('CreateCrudNodejsExpressEjsUseCase', () => {
  it('saves an entity', async () => {
    const useCase = new CreateCrudNodejsExpressEjsUseCase(new InMemoryCrudNodejsExpressEjsRepository());
    const entity = await useCase.execute('1', 'example');

    expect(entity.id).toBe('1');
    expect(entity.name).toBe('example');
  });
});
