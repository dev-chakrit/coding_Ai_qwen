import type { Crud } from '../domain/entities';
import type { CrudRepository } from '../domain/repositories';

export class InMemoryCrudRepository implements CrudRepository {
  private readonly items = new Map<string, Crud>();

  async save(entity: Crud): Promise<Crud> {
    this.items.set(entity.id, entity);
    return entity;
  }
}
