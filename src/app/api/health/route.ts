import { getDb } from '@/db';
import { jsonError, jsonOk } from '../_utils';

export const dynamic = 'force-dynamic';

export async function GET() {
  try {
    const db = getDb();
    const ping = db.prepare('SELECT 1 as ok').get() as { ok: number };

    const counts = db
      .prepare(
        `SELECT
           (SELECT COUNT(*) FROM builder_codes) as builderCodes,
           (SELECT COUNT(*) FROM contributors) as contributors,
           (SELECT COUNT(*) FROM split_rules) as splitRules,
           (SELECT COUNT(*) FROM fee_events) as feeEvents,
           (SELECT COUNT(*) FROM settlements) as settlements,
           (SELECT COUNT(*) FROM reconciliation_snapshots) as reconciliationSnapshots`
      )
      .get() as Record<string, number>;

    return jsonOk({
      status: ping?.ok === 1 ? 'ok' : 'degraded',
      service: 'hypersettle-api',
      timestamp: new Date().toISOString(),
      precision: 'micro-usd-bigint-1e-6',
      counts
    });
  } catch (err) {
    return jsonError(err, 500);
  }
}
