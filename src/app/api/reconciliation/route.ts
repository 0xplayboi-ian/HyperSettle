import {
  extractOnchainBuilderRewardsMicroUsd,
  reconcileBuilderCode
} from '@/core/reconciliation';
import { formatMicroUsd, microUsdToDecimal } from '@/core/splits';
import { getDb } from '@/db';
import { HyperCoreClient } from '@/ingestion/client';
import { listBuilderCodes, resolveBuilderCode } from '@/services/ledger';
import { jsonError, jsonOk, normalizeDateBound } from '../_utils';

export const dynamic = 'force-dynamic';

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const builderCodeParam = searchParams.get('builder_code');
    const live = searchParams.get('live') === 'true';
    const persist = searchParams.get('persist') === 'true';

    const nowIso = new Date().toISOString();
    const defaultFromIso = new Date(Date.now() - 60 * 24 * 60 * 60 * 1000).toISOString();
    const fromIso = normalizeDateBound(searchParams.get('from'), false) ?? defaultFromIso;
    const toIso = normalizeDateBound(searchParams.get('to'), true) ?? nowIso;

    if (fromIso >= toIso) {
      return jsonError(new Error('from must be earlier than to'), 400);
    }

    const db = getDb();

    const targets = builderCodeParam
      ? (() => {
          const found = resolveBuilderCode(db, builderCodeParam);
          if (!found) {
            throw new Error(`Unknown builder code filter: ${builderCodeParam}`);
          }
          return [found];
        })()
      : listBuilderCodes(db).filter(b => b.active);

    const client = live ? new HyperCoreClient() : null;
    const reports = [];

    for (const builder of targets) {
      let onchainTotalMicroUsd: bigint | undefined;
      let source: string | undefined;

      if (client) {
        const referral = await client.fetchBuilderReferralState(builder.address);
        onchainTotalMicroUsd = extractOnchainBuilderRewardsMicroUsd(referral);
        source = 'hypercore_referral_api_live';
      }

      const report = reconcileBuilderCode(db, {
        builderCodeId: builder.id,
        fromIso,
        toIso,
        onchainTotalMicroUsd,
        persistSnapshot: persist,
        source
      });

      reports.push({
        ...report,
        localNotionalUsd: formatMicroUsd(report.localNotionalMicroUsd, 2),
        localTotalUsdc: microUsdToDecimal(report.localTotalMicroUsd),
        localTotalFormatted: formatMicroUsd(report.localTotalMicroUsd, 6),
        onchainTotalUsdc: microUsdToDecimal(report.onchainTotalMicroUsd),
        onchainTotalFormatted: formatMicroUsd(report.onchainTotalMicroUsd, 6),
        driftFormatted: formatMicroUsd(report.driftMicroUsd, 6)
      });
    }

    const hasDiscrepancy = reports.some(r => r.status === 'discrepancy');
    const hasMinorDrift = reports.some(r => r.status === 'minor_drift');

    return jsonOk({
      overallStatus: hasDiscrepancy
        ? 'discrepancy'
        : hasMinorDrift
          ? 'minor_drift'
          : 'matched',
      mode: live ? 'live_hypercore' : 'ledger_snapshot',
      periodStart: fromIso,
      periodEnd: toIso,
      reports
    });
  } catch (err) {
    return jsonError(err, 400);
  }
}
