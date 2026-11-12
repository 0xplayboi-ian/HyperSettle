import { getDb } from '@/db';
import { createBuilderCode, listBuilderCodes } from '@/services/ledger';
import { jsonError, jsonOk, readJsonBody } from '../_utils';

export const dynamic = 'force-dynamic';

export async function GET() {
  try {
    const db = getDb();
    const builderCodes = listBuilderCodes(db);
    return jsonOk({ builderCodes });
  } catch (err) {
    return jsonError(err, 500);
  }
}

export async function POST(request: Request) {
  try {
    const body = await readJsonBody<{ address?: string; label?: string }>(request);
    if (typeof body.address !== 'string' || typeof body.label !== 'string') {
      return jsonError(new Error('Both address and label strings are required'), 400);
    }

    const db = getDb();
    const created = createBuilderCode(db, {
      address: body.address,
      label: body.label
    });
    return jsonOk({ builderCode: created }, 201);
  } catch (err) {
    return jsonError(err, 400);
  }
}
