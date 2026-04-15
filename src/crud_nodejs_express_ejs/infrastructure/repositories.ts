import type { CrudNodejsExpressEjs } from '../domain/entities';
import type { CrudNodejsExpressEjsRepository } from '../domain/repositories';

export class InMemoryCrudNodejsExpressEjsRepository implements CrudNodejsExpressEjsRepository {
  private readonly items = new Map<string, CrudNodejsExpressEjs>();

  async save(entity: CrudNodejsExpressEjs): Promise<CrudNodejsExpressEjs> {
    this.items.set(entity.id, entity);
    return entity;
  }
}
