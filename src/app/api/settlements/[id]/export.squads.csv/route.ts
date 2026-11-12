import { NextResponse } from 'next/server';
import { getDb } from '@/db';
import { generateSquadsBatchCsv } from '@/export/squads';
import { getSettlementExportData } from '@/services/ledger';
import { jsonError } from '../../../_utils';

export const dynamic = 'force-dynamic';

export async function GET(
  _request: Request,
  context: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await context.params;
    const settlementId = Number(id);
    if (!Number.isInteger(settlementId) || settlementId <= 0) {
      return jsonError(new Error(`Invalid settlement ID: ${id}`), 400);
    }

    const db = getDb();
    const data = getSettlementExportData(db, settlementId);
    if (!data) {
      return jsonError(new Error(`Settlement #${settlementId} not found`), 404);
    }

    const squads = generateSquadsBatchCsv(data.lines);
    return new NextResponse(squads.csv, {
      status: 200,
      headers: {
        'Content-Type': 'text/csv; charset=utf-8',
        'Content-Disposition': `attachment; filename="hypersettle-settlement-${settlementId}.squads.csv"`,
        'X-Squads-Transfer-Count': String(squads.transferCount),
        'X-Squads-Total-USDC': squads.totalTransferUsdc,
        'X-Squads-Mint': squads.mintAddress,
        'Cache-Control': 'no-store'
      }
    });
  } catch (err) {
    return jsonError(err, 400);
  }
}
