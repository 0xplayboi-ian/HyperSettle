import { getDb } from '@/db';
import { getRevenueSummary, type RevenueGroupBy } from '@/services/ledger';
import { jsonError, jsonOk, normalizeDateBound } from '../_utils';

export const dynamic = 'force-dynamic';

const VALID_GROUPS = new Set<RevenueGroupBy>(['day', 'week', 'source']);

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const builderCode = searchParams.get('builder_code');
    const from = normalizeDateBound(searchParams.get('from'), false);
    const to = normalizeDateBound(searchParams.get('to'), true);
    const groupParam = (searchParams.get('group') ?? 'day') as RevenueGroupBy;

    if (!VALID_GROUPS.has(groupParam)) {
      return jsonError(new Error('Invalid group parameter; expected day, week, or source'), 400);
    }

    const db = getDb();
    const summary = getRevenueSummary(db, {
      builderCode,
      from,
      to,
      group: groupParam
    });

    return jsonOk(summary);
  } catch (err) {
    return jsonError(err, 400);
  }
}
