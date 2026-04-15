import type { Crud } from '../domain/entities';
import type { CrudRepository } from '../domain/repositories';

export class CreateCrudUseCase {
  constructor(private readonly repository: CrudRepository) {}

  async execute(id: string, name: string): Promise<Crud> {
    const entity: Crud = { id, name };
    return this.repository.save(entity);
  }
}
