import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import Database from 'better-sqlite3';
import { SCHEMA_SQL } from '../src/db/schema';
import {
  detectFeeAnomalies,
  evaluateReconciliation,
  extractOnchainBuilderRewardsMicroUsd,
  reconcileBuilderCode
} from '../src/core/reconciliation';

describe('Onchain Reconciliation Engine', () => {
  let db: Database.Database;

  beforeEach(() => {
    db = new Database(':memory:');
    db.pragma('foreign_keys = ON');
    db.exec(SCHEMA_SQL);

    db.prepare(
      `INSERT INTO builder_codes (id, address, label, active)
       VALUES (1, '0xbuilder11111111111111111111111111111111', 'Alpha Desk', 1)`
    ).run();
  });

  afterEach(() => {
    db.close();
  });

  it('classifies matched, minor_drift, and discrepancy thresholds accurately', () => {
    const exact = evaluateReconciliation({
      localTotalMicroUsd: 1_000_000n,
      onchainTotalMicroUsd: 1_000_000n
    });
    expect(exact.status).toBe('matched');
    expect(exact.driftMicroUsd).toBe(0n);

    const minorFlat = evaluateReconciliation({
      localTotalMicroUsd: 1_000_000n,
      onchainTotalMicroUsd: 1_005_000n // $0.005 <= $0.01 threshold
    });
    expect(minorFlat.status).toBe('minor_drift');

    const minorRatio = evaluateReconciliation({
      localTotalMicroUsd: 1_000_000_000n, // $1,000
      onchainTotalMicroUsd: 1_000_050_000n // $0.05 (0.005% <= 0.01%)
    });
    expect(minorRatio.status).toBe('minor_drift');

    const bigDrift = evaluateReconciliation({
      localTotalMicroUsd: 1_000_000n,
      onchainTotalMicroUsd: 1_500_000n
    });
    expect(bigDrift.status).toBe('discrepancy');
    expect(bigDrift.notes).toContain('missing local fills');

    const zeroDriftWithAnomaly = evaluateReconciliation({
      localTotalMicroUsd: 1_000_000n,
      onchainTotalMicroUsd: 1_000_000n,
      anomalyCount: 1
    });
    expect(zeroDriftWithAnomaly.status).toBe('discrepancy');
    expect(zeroDriftWithAnomaly.notes).toContain('1 protocol fee anomaly');
  });

  it('extracts micro-USD builder rewards from Hyperliquid referral payload', () => {
    expect(
      extractOnchainBuilderRewardsMicroUsd({
        builderRewards: '1234.567891',
        unclaimedRewards: '99.0'
      })
    ).toBe(1_234_567_891n);

    expect(
      extractOnchainBuilderRewardsMicroUsd({
        unclaimedRewards: '42.5'
      })
    ).toBe(42_500_000n);
  });

  it('detects non-positive and >100 bps protocol fee cap anomalies', () => {
    const insert = db.prepare(
      `INSERT INTO fee_events (
         external_id, builder_code_id, source_label, trader,
         notional_micro_usd, fee_micro_usd, block_time
       ) VALUES (?, 1, ?, '0xtrader', ?, ?, ?)`
    );

    // Valid: 5 bps ($50 on $100,000)
    insert.run('fill_ok', 'web_terminal', 100_000_000_000, 50_000_000, '2026-10-15T10:00:00Z');
    // Anomaly 1: 0 fee
    insert.run('fill_zero', 'web_terminal', 10_000_000_000, 0, '2026-10-15T11:00:00Z');
    // Anomaly 2: 150 bps ($150 on $10,000) > 100 bps spot cap
    insert.run('fill_overcap', 'api_client', 10_000_000_000, 150_000_000, '2026-10-15T12:00:00Z');

    const anomalies = detectFeeAnomalies(db, 1, '2026-10-01T00:00:00Z', '2026-10-31T23:59:59Z');
    expect(anomalies).toHaveLength(2);
    expect(anomalies[0].externalId).toBe('fill_zero');
    expect(anomalies[1].externalId).toBe('fill_overcap');
    expect(anomalies[1].effectiveFeeBps).toBe(150);
  });

  it('reconciles builder code and optionally persists audit snapshot', () => {
    db.prepare(
      `INSERT INTO fee_events (
         external_id, builder_code_id, source_label, trader,
         notional_micro_usd, fee_micro_usd, block_time
       ) VALUES ('fill_1', 1, 'tg_bot_alpha', '0xtrader', 50000000000, 25000000, '2026-10-20T09:00:00Z')`
    ).run();

    const report = reconcileBuilderCode(db, {
      builderCodeId: 1,
      fromIso: '2026-10-01T00:00:00Z',
      toIso: '2026-10-31T23:59:59Z',
      onchainTotalMicroUsd: 25_000_000n,
      persistSnapshot: true,
      source: 'unit_test_mock'
    });

    expect(report.fillCount).toBe(1);
    expect(report.localTotalMicroUsd).toBe(25_000_000n);
    expect(report.driftMicroUsd).toBe(0n);
    expect(report.status).toBe('matched');
    expect(report.anomalies).toHaveLength(0);

    const saved = db.prepare('SELECT * FROM reconciliation_snapshots WHERE builder_code_id = 1').all() as any[];
    expect(saved).toHaveLength(1);
    expect(saved[0].status).toBe('matched');
    expect(saved[0].source).toBe('unit_test_mock');
  });
});
