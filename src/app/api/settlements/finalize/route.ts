import { getDb } from '@/db';
import { finalizeSettlement } from '@/services/ledger';
import { jsonError, jsonOk, normalizeDateBound, readJsonBody } from '../../_utils';

export const dynamic = 'force-dynamic';

export async function POST(request: Request) {
  try {
    const body = await readJsonBody<{
      builderCodeId?: number | string;
      builder_code_id?: number | string;
      builderCode?: string;
      builder_code?: string;
      periodStart?: string;
      period_start?: string;
      periodEnd?: string;
      period_end?: string;
      splitRuleId?: number | string;
      split_rule_id?: number | string;
    }>(request);

    const builderCodeId =
      body.builderCodeId ?? body.builder_code_id ?? body.builderCode ?? body.builder_code;
    const periodStart = normalizeDateBound(body.periodStart ?? body.period_start ?? null, false);
    const periodEnd = normalizeDateBound(body.periodEnd ?? body.period_end ?? null, true);
    const rawSplitRuleId = body.splitRuleId ?? body.split_rule_id;

    if (builderCodeId === undefined || builderCodeId === null || builderCodeId === '') {
      return jsonError(new Error('builderCodeId (or builder_code) is required'), 400);
    }
    if (!periodStart || !periodEnd) {
      return jsonError(new Error('Both periodStart and periodEnd are required'), 400);
    }

    const splitRuleId =
      rawSplitRuleId !== undefined && rawSplitRuleId !== null && rawSplitRuleId !== ''
        ? Number(rawSplitRuleId)
        : undefined;
    if (splitRuleId !== undefined && (!Number.isInteger(splitRuleId) || splitRuleId <= 0)) {
      return jsonError(new Error('splitRuleId must be a positive integer'), 400);
    }

    const db = getDb();
    const settlement = finalizeSettlement(db, {
      builderCodeId,
      periodStart,
      periodEnd,
      splitRuleId
    });

    return jsonOk({ settlement }, 201);
  } catch (err) {
    return jsonError(err, 400);
  }
}
