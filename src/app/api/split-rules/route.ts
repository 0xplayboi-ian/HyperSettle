import { deserializeSplitConfig } from '@/core/splits';
import { getDb } from '@/db';
import { createSplitRule, listSplitRules, resolveBuilderCode } from '@/services/ledger';
import { jsonError, jsonOk, readJsonBody } from '../_utils';

export const dynamic = 'force-dynamic';

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const builderCode = searchParams.get('builder_code');

    const db = getDb();
    const splitRules = listSplitRules(db, builderCode);
    return jsonOk({ splitRules });
  } catch (err) {
    return jsonError(err, 500);
  }
}

export async function POST(request: Request) {
  try {
    const body = await readJsonBody<{
      builderCodeId?: number | string;
      builder_code_id?: number | string;
      builderCode?: string;
      builder_code?: string;
      name?: string;
      effectiveFrom?: string;
      effective_from?: string;
      config?: unknown;
    }>(request);

    const builderInput =
      body.builderCodeId ?? body.builder_code_id ?? body.builderCode ?? body.builder_code;
    if (builderInput === undefined || builderInput === null || builderInput === '') {
      return jsonError(new Error('builderCodeId (or builder_code) is required'), 400);
    }
    if (typeof body.name !== 'string') {
      return jsonError(new Error('Split rule name is required'), 400);
    }
    if (!body.config || (typeof body.config !== 'object' && typeof body.config !== 'string')) {
      return jsonError(new Error('Split rule config is required'), 400);
    }

    const rawConfigStr =
      typeof body.config === 'string' ? body.config : JSON.stringify(body.config);
    const parsedRaw = JSON.parse(rawConfigStr) as { type?: string };
    if (parsedRaw?.type !== 'percent' && parsedRaw?.type !== 'fixed_per_period') {
      return jsonError(
        new Error('Split config type must be either "percent" or "fixed_per_period"'),
        400
      );
    }

    const config = deserializeSplitConfig(rawConfigStr);
    const db = getDb();
    const resolvedBuilder = resolveBuilderCode(db, builderInput);
    if (!resolvedBuilder) {
      return jsonError(new Error(`Builder code "${builderInput}" not found`), 404);
    }

    const created = createSplitRule(db, {
      builderCodeId: resolvedBuilder.id,
      name: body.name,
      effectiveFrom: body.effectiveFrom ?? body.effective_from,
      config
    });

    return jsonOk({ splitRule: created }, 201);
  } catch (err) {
    return jsonError(err, 400);
  }
}
