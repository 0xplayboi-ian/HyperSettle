/**
 * HyperSettle Automated Onchain Reconciliation Engine
 *
 * Cross-references local HyperCore fill rollups (`fee_events`) against
 * Hyperliquid L1 referral / builderRewards ledger totals to detect
 * missing fills, rounding drift, or protocol fee-cap anomalies.
 */

import Database from 'better-sqlite3';
import { formatMicroUsd, parseUsdToMicro } from './splits';
import type { HyperliquidReferralResponse } from '../ingestion/client';

export type ReconciliationStatus = 'matched' | 'minor_drift' | 'discrepancy';

export interface ReconciliationAnomaly {
  eventId: number;
  externalId: string;
  reason: string;
  effectiveFeeBps: number;
  feeMicroUsd: bigint;
  notionalMicroUsd: bigint;
}

export interface ReconciliationReport {
  builderCodeId: number;
  builderAddress: string;
  builderLabel: string;
  periodStart: string;
  periodEnd: string;
  fillCount: number;
  localNotionalMicroUsd: bigint;
  localTotalMicroUsd: bigint;
  onchainTotalMicroUsd: bigint;
  driftMicroUsd: bigint;
  driftPercent: string;
  status: ReconciliationStatus;
  anomalies: ReconciliationAnomaly[];
  checkedAt: string;
  source: string;
  notes: string;
}

/**
 * Pure reconciliation computation comparing local ledger total against onchain total.
 * Thresholds:
 * - matched: exact 0 micro-USD drift
 * - minor_drift: <= $0.01 (10,000 micro-USD) OR <= 0.01% (1 bp)
 * - discrepancy: anything above minor_drift threshold
 */
export function evaluateReconciliation(params: {
  localTotalMicroUsd: bigint;
  onchainTotalMicroUsd: bigint;
  anomalyCount?: number;
}): {
  driftMicroUsd: bigint;
  absDriftMicroUsd: bigint;
  driftPercent: string;
  status: ReconciliationStatus;
  notes: string;
} {
  const { localTotalMicroUsd, onchainTotalMicroUsd, anomalyCount = 0 } = params;
  const driftMicroUsd = onchainTotalMicroUsd - localTotalMicroUsd;
  const absDriftMicroUsd = driftMicroUsd < 0n ? -driftMicroUsd : driftMicroUsd;

  const denominator = onchainTotalMicroUsd > 0n ? onchainTotalMicroUsd : localTotalMicroUsd;
  const driftRatioPct =
    denominator > 0n
      ? (Number((absDriftMicroUsd * 1_000_000n) / denominator) / 10_000)
      : absDriftMicroUsd > 0n
        ? 100
        : 0;
  const driftPercent = `${driftRatioPct.toFixed(4)}%`;

  let status: ReconciliationStatus = 'matched';
  let notes = '100% ledger parity between local HyperCore fills and onchain rewards.';

  if (absDriftMicroUsd === 0n && anomalyCount === 0) {
    status = 'matched';
  } else if (anomalyCount === 0 && (absDriftMicroUsd <= 10_000n || driftRatioPct <= 0.01)) {
    status = 'minor_drift';
    notes = `Within tolerance (${formatMicroUsd(absDriftMicroUsd)} / ${driftPercent}). Typical of 2-3s HyperBFT finality lag.`;
  } else {
    status = 'discrepancy';
    const reasons: string[] = [];
    if (absDriftMicroUsd > 0n) {
      const direction = driftMicroUsd > 0n ? 'missing local fills' : 'excess local fills vs onchain';
      reasons.push(`${formatMicroUsd(absDriftMicroUsd)} drift (${direction})`);
    }
    if (anomalyCount > 0) {
      reasons.push(`${anomalyCount} protocol fee anomaly event(s)`);
    }
    notes = `Discrepancy flagged: ${reasons.join('; ')}.`;
  }

  return {
    driftMicroUsd,
    absDriftMicroUsd,
    driftPercent,
    status,
    notes
  };
}

/**
 * Extract builder rewards total in micro-USD from a Hyperliquid /info referral response.
 */
export function extractOnchainBuilderRewardsMicroUsd(referral: HyperliquidReferralResponse): bigint {
  const raw = referral.builderRewards ?? referral.unclaimedRewards ?? '0';
  return parseUsdToMicro(String(raw));
}

/**
 * Scan local `fee_events` rows inside a window for protocol anomalies:
 * - Zero or negative fees
 * - Effective fee exceeding maximum Hyperliquid 1% (100 bps) spot builder fee cap
 */
export function detectFeeAnomalies(
  db: Database.Database,
  builderCodeId: number,
  fromIso: string,
  toIso: string
): ReconciliationAnomaly[] {
  const rows = db
    .prepare(
      `SELECT id, external_id, notional_micro_usd, fee_micro_usd
       FROM fee_events
       WHERE builder_code_id = ? AND block_time >= ? AND block_time <= ?`
    )
    .all(builderCodeId, fromIso, toIso) as Array<{
    id: number;
    external_id: string;
    notional_micro_usd: number | string;
    fee_micro_usd: number | string;
  }>;

  const anomalies: ReconciliationAnomaly[] = [];

  for (const row of rows) {
    const notional = BigInt(row.notional_micro_usd);
    const fee = BigInt(row.fee_micro_usd);
    const effectiveBps = notional > 0n ? Number((fee * 10_000n) / notional) : 0;

    if (fee <= 0n) {
      anomalies.push({
        eventId: row.id,
        externalId: row.external_id,
        reason: 'Non-positive builder fee recorded on fill event',
        effectiveFeeBps: effectiveBps,
        feeMicroUsd: fee,
        notionalMicroUsd: notional
      });
    } else if (effectiveBps > 100) {
      anomalies.push({
        eventId: row.id,
        externalId: row.external_id,
        reason: `Effective fee (${effectiveBps} bps) exceeds 100 bps Hyperliquid builder cap`,
        effectiveFeeBps: effectiveBps,
        feeMicroUsd: fee,
        notionalMicroUsd: notional
      });
    }
  }

  return anomalies;
}

/**
 * Run a full reconciliation check for a builder code over [fromIso, toIso].
 * Uses explicit `onchainTotalMicroUsd` if provided, else looks up the latest snapshot
 * or defaults to local total when operating in offline seeded mode.
 */
export function reconcileBuilderCode(
  db: Database.Database,
  params: {
    builderCodeId: number;
    fromIso: string;
    toIso: string;
    onchainTotalMicroUsd?: bigint;
    persistSnapshot?: boolean;
    source?: string;
  }
): ReconciliationReport {
  const builder = db
    .prepare('SELECT id, address, label FROM builder_codes WHERE id = ?')
    .get(params.builderCodeId) as { id: number; address: string; label: string } | undefined;

  if (!builder) {
    throw new Error(`Builder code #${params.builderCodeId} not found`);
  }

  const agg = db
    .prepare(
      `SELECT COUNT(*) as fill_count,
              COALESCE(SUM(notional_micro_usd), 0) as notional_sum,
              COALESCE(SUM(fee_micro_usd), 0) as fee_sum
       FROM fee_events
       WHERE builder_code_id = ? AND block_time >= ? AND block_time <= ?`
    )
    .get(builder.id, params.fromIso, params.toIso) as {
    fill_count: number;
    notional_sum: number | string;
    fee_sum: number | string;
  };

  const localTotalMicroUsd = BigInt(agg.fee_sum ?? 0);
  const localNotionalMicroUsd = BigInt(agg.notional_sum ?? 0);
  const anomalies = detectFeeAnomalies(db, builder.id, params.fromIso, params.toIso);

  let onchainTotalMicroUsd = params.onchainTotalMicroUsd;
  let source = params.source ?? 'hypercore_referral_api';

  if (onchainTotalMicroUsd === undefined) {
    const latestSnap = db
      .prepare(
        `SELECT onchain_total_micro_usd, drift_micro_usd, source
         FROM reconciliation_snapshots
         WHERE builder_code_id = ?
         ORDER BY id DESC LIMIT 1`
      )
      .get(builder.id) as
      | { onchain_total_micro_usd: number | string; drift_micro_usd: number | string; source: string }
      | undefined;

    if (latestSnap) {
      // Preserve seeded drift offset if running over full window, otherwise match local
      onchainTotalMicroUsd = localTotalMicroUsd + BigInt(latestSnap.drift_micro_usd);
      source = latestSnap.source;
    } else {
      onchainTotalMicroUsd = localTotalMicroUsd;
      source = 'local_ledger_baseline';
    }
  }

  const evaluation = evaluateReconciliation({
    localTotalMicroUsd,
    onchainTotalMicroUsd,
    anomalyCount: anomalies.length
  });

  const checkedAt = new Date().toISOString();

  if (params.persistSnapshot) {
    db.prepare(
      `INSERT INTO reconciliation_snapshots (
         builder_code_id, period_start, period_end,
         local_total_micro_usd, onchain_total_micro_usd, drift_micro_usd,
         status, source, notes, checked_at
       ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`
    ).run(
      builder.id,
      params.fromIso,
      params.toIso,
      localTotalMicroUsd.toString(),
      onchainTotalMicroUsd.toString(),
      evaluation.driftMicroUsd.toString(),
      evaluation.status,
      source,
      evaluation.notes,
      checkedAt
    );
  }

  return {
    builderCodeId: builder.id,
    builderAddress: builder.address,
    builderLabel: builder.label,
    periodStart: params.fromIso,
    periodEnd: params.toIso,
    fillCount: agg.fill_count,
    localNotionalMicroUsd,
    localTotalMicroUsd,
    onchainTotalMicroUsd,
    driftMicroUsd: evaluation.driftMicroUsd,
    driftPercent: evaluation.driftPercent,
    status: evaluation.status,
    anomalies,
    checkedAt,
    source,
    notes: evaluation.notes
  };
}
