import type { CrudNodejsExpressEjs } from './entities';

export interface CrudNodejsExpressEjsRepository {
  save(entity: CrudNodejsExpressEjs): Promise<CrudNodejsExpressEjs>;
}
