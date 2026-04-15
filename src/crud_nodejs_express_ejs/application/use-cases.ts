import type { CrudNodejsExpressEjs } from '../domain/entities';
import type { CrudNodejsExpressEjsRepository } from '../domain/repositories';

export class CreateCrudNodejsExpressEjsUseCase {
  constructor(private readonly repository: CrudNodejsExpressEjsRepository) {}

  async execute(id: string, name: string): Promise<CrudNodejsExpressEjs> {
    const entity: CrudNodejsExpressEjs = { id, name };
    return this.repository.save(entity);
  }
}
