import { getDb } from '@/db';
import { listSettlements } from '@/services/ledger';
import { jsonError, jsonOk } from '../_utils';

export const dynamic = 'force-dynamic';

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const builderCode = searchParams.get('builder_code');

    const db = getDb();
    const settlements = listSettlements(db, builderCode);
    return jsonOk({ settlements });
  } catch (err) {
    return jsonError(err, 500);
  }
}
