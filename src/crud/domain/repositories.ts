import type { Crud } from './entities';

export interface CrudRepository {
  save(entity: Crud): Promise<Crud>;
}
