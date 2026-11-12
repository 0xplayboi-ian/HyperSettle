import { getDb } from '@/db';
import { getFeeEvents } from '@/services/ledger';
import { jsonError, jsonOk, normalizeDateBound } from '../_utils';

export const dynamic = 'force-dynamic';

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const builderCode = searchParams.get('builder_code');
    const from = normalizeDateBound(searchParams.get('from'), false);
    const to = normalizeDateBound(searchParams.get('to'), true);
    const limitRaw = searchParams.get('limit');
    const cursor = searchParams.get('cursor');

    let limit = 50;
    if (limitRaw !== null && limitRaw !== '') {
      const parsed = Number(limitRaw);
      if (!Number.isInteger(parsed) || parsed < 1) {
        return jsonError(new Error('limit must be a positive integer'), 400);
      }
      limit = parsed;
    }

    const db = getDb();
    const result = getFeeEvents(db, {
      builderCode,
      from,
      to,
      limit,
      cursor
    });

    return jsonOk(result);
  } catch (err) {
    return jsonError(err, 400);
  }
}
