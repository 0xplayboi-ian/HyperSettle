import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import Database from 'better-sqlite3';
import { SCHEMA_SQL } from '../src/db/schema';
import { HyperCoreClient, WeightRateLimiter } from '../src/ingestion/client';
import {
  createBuilderCode,
  createContributor,
  createSplitRule,
  finalizeSettlement,
  getFeeEvents,
  getRevenueSummary,
  getSettlementExportData,
  previewSettlement
} from '../src/services/ledger';

let activeTestDb: Database.Database;

vi.mock('@/db', () => ({
  getDb: () => activeTestDb,
  closeDb: () => {}
}));

import { GET as getHealth } from '../src/app/api/health/route';
import { GET as getRevenue } from '../src/app/api/revenue/route';
import { GET as getReconciliation } from '../src/app/api/reconciliation/route';
import { POST as postPreview } from '../src/app/api/settlements/preview/route';
import { POST as postFinalize } from '../src/app/api/settlements/finalize/route';
import { GET as getAuditExport } from '../src/app/api/settlements/[id]/export.csv/route';
import { GET as getSquadsExport } from '../src/app/api/settlements/[id]/export.squads.csv/route';

function setupSeededInMemoryDb(): Database.Database {
  const db = new Database(':memory:');
  db.pragma('foreign_keys = ON');
  db.exec(SCHEMA_SQL);

  const builder = createBuilderCode(db, {
    address: '0x1111111111111111111111111111111111111111',
    label: 'HyperDesk Core'
  });

  const alice = createContributor(db, {
    id: 'alice',
    name: 'Alice Founder',
    walletSolana: '7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU'
  });
  const bob = createContributor(db, {
    id: 'bob',
    name: 'Bob Protocol',
    walletSolana: '9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM'
  });

  createSplitRule(db, {
    builderCodeId: builder.id,
    name: '60/40 Split',
    effectiveFrom: '2026-10-01T00:00:00.000Z',
    config: {
      type: 'percent',
      recipients: [
        { contributorId: alice.id, bps: 6000 },
        { contributorId: bob.id, bps: 4000 }
      ]
    }
  });

  const insertFill = db.prepare(
    `INSERT INTO fee_events (
       external_id, builder_code_id, source_label, trader,
       notional_micro_usd, fee_micro_usd, block_time, tx_ref
     ) VALUES (?, ?, ?, '0xtrader', ?, ?, ?, ?)`
  );

  insertFill.run('hl_1', builder.id, 'web_terminal', 100_000_000_000, 1_000_001, '2026-10-10T12:00:00.000Z', '0xtx1');
  insertFill.run('hl_2', builder.id, 'tg_bot_alpha', 200_000_000_000, 2_000_000, '2026-10-11T12:00:00.000Z', '0xtx2');
  insertFill.run('hl_3', builder.id, 'web_terminal', 150_000_000_000, 1_500_000, '2026-10-12T12:00:00.000Z', '0xtx3');

  return db;
}

describe('Ledger Service, HyperCore Client & Next.js REST APIs', () => {
  beforeEach(() => {
    activeTestDb = setupSeededInMemoryDb();
  });

  afterEach(() => {
    activeTestDb.close();
  });

  it('aggregates revenue by day/week/source with exact BigInt micro-USD totals', () => {
    const bySource = getRevenueSummary(activeTestDb, { group: 'source' });
    expect(bySource.totals.fillCount).toBe(3);
    expect(bySource.totals.feeMicroUsd).toBe('4500001');
    expect(bySource.buckets[0]).toMatchObject({
      key: 'web_terminal',
      fillCount: 2,
      feeMicroUsd: '2500001'
    });
    expect(bySource.buckets[1]).toMatchObject({
      key: 'tg_bot_alpha',
      fillCount: 1,
      feeMicroUsd: '2000000'
    });
  });

  it('paginates fee events deterministically using cursor without gaps', () => {
    const page1 = getFeeEvents(activeTestDb, { limit: 2 });
    expect(page1.events).toHaveLength(2);
    expect(page1.hasMore).toBe(true);
    expect(page1.events.map(e => e.externalId)).toEqual(['hl_3', 'hl_2']);

    const page2 = getFeeEvents(activeTestDb, { limit: 2, cursor: page1.nextCursor });
    expect(page2.events).toHaveLength(1);
    expect(page2.hasMore).toBe(false);
    expect(page2.events[0].externalId).toBe('hl_1');
  });

  it('previews, finalizes, and blocks overlapping settlements', () => {
    const preview = previewSettlement(activeTestDb, {
      builderCodeId: 1,
      periodStart: '2026-10-01T00:00:00.000Z',
      periodEnd: '2026-10-31T23:59:59.999Z'
    });
    expect(preview.invariantPassed).toBe(true);
    expect(preview.totalFeeMicroUsd).toBe('4500001');
    expect(preview.overlappingFinalizedSettlementId).toBeNull();

    const finalized = finalizeSettlement(activeTestDb, {
      builderCodeId: 1,
      periodStart: '2026-10-01T00:00:00.000Z',
      periodEnd: '2026-10-31T23:59:59.999Z'
    });
    expect(finalized.status).toBe('final');
    expect(finalized.settlementId).toBe(1);

    const exportData = getSettlementExportData(activeTestDb, 1);
    expect(exportData?.lines).toHaveLength(2);

    expect(() =>
      finalizeSettlement(activeTestDb, {
        builderCodeId: 1,
        periodStart: '2026-10-15T00:00:00.000Z',
        periodEnd: '2026-11-05T00:00:00.000Z'
      })
    ).toThrow(/overlaps existing finalized settlement/);
  });

  it('enforces WeightRateLimiter budget and retries HyperCore 429 responses', async () => {
    let now = 1_000_000;
    const limiter = new WeightRateLimiter({
      capacity: 10,
      refillPerMs: 0.02, // 20 per second
      nowFn: () => now
    });

    expect(limiter.tryConsume(6)).toEqual({ allowed: true, waitMs: 0 });
    const denied = limiter.tryConsume(6);
    expect(denied.allowed).toBe(false);
    expect(denied.waitMs).toBe(100);

    now += 100; // Refill +2 tokens -> 6 available
    expect(limiter.tryConsume(6)).toEqual({ allowed: true, waitMs: 0 });

    const calls: string[] = [];
    const mockFetch = vi.fn(async (_url: string | URL | Request, init?: RequestInit) => {
      calls.push(String(init?.body ?? ''));
      if (calls.length === 1) {
        return new Response('rate limited', { status: 429 });
      }
      return new Response(JSON.stringify({ builderRewards: '42.125' }), {
        status: 200,
        headers: { 'Content-Type': 'application/json' }
      });
    });

    const client = new HyperCoreClient({
      fetchFn: mockFetch as unknown as typeof fetch,
      maxRetries: 2
    });

    const ref = await client.fetchBuilderReferralState('0x1111111111111111111111111111111111111111');
    expect(ref.builderRewards).toBe('42.125');
    expect(mockFetch).toHaveBeenCalledTimes(2);
  });

  it('handles Next.js App Router API routes end-to-end including Squads V4 CSV download', async () => {
    const healthRes = await getHealth();
    expect(healthRes.status).toBe(200);
    const healthBody = await healthRes.json();
    expect(healthBody.status).toBe('ok');
    expect(healthBody.counts.feeEvents).toBe(3);

    const revBadRes = await getRevenue(new Request('http://localhost/api/revenue?group=invalid'));
    expect(revBadRes.status).toBe(400);

    const revOkRes = await getRevenue(new Request('http://localhost/api/revenue?group=source'));
    expect(revOkRes.status).toBe(200);

    const reconRes = await getReconciliation(
      new Request('http://localhost/api/reconciliation?from=2026-10-01&to=2026-10-31')
    );
    expect(reconRes.status).toBe(200);
    const reconBody = await reconRes.json();
    expect(reconBody.overallStatus).toBe('matched');
    expect(reconBody.reports[0].localTotalMicroUsd).toBe('4500001');

    const previewRes = await postPreview(
      new Request('http://localhost/api/settlements/preview', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          builder_code_id: 1,
          period_start: '2026-10-01',
          period_end: '2026-10-31'
        })
      })
    );
    expect(previewRes.status).toBe(200);

    const finalizeRes = await postFinalize(
      new Request('http://localhost/api/settlements/finalize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          builderCodeId: 1,
          periodStart: '2026-10-01',
          periodEnd: '2026-10-31'
        })
      })
    );
    expect(finalizeRes.status).toBe(201);

    const conflictRes = await postFinalize(
      new Request('http://localhost/api/settlements/finalize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          builderCodeId: 1,
          periodStart: '2026-10-10',
          periodEnd: '2026-10-20'
        })
      })
    );
    expect(conflictRes.status).toBe(409);

    const squadsRes = await getSquadsExport(
      new Request('http://localhost/api/settlements/1/export.squads.csv'),
      { params: Promise.resolve({ id: '1' }) }
    );
    expect(squadsRes.status).toBe(200);
    expect(squadsRes.headers.get('Content-Type')).toContain('text/csv');
    expect(squadsRes.headers.get('X-Squads-Transfer-Count')).toBe('2');
    const squadsCsv = await squadsRes.text();
    expect(squadsCsv.split('\n')[0]).toBe('token_address,receiver,amount');

    const auditRes = await getAuditExport(
      new Request('http://localhost/api/settlements/1/export.csv'),
      { params: Promise.resolve({ id: '1' }) }
    );
    expect(auditRes.status).toBe(200);
    expect(await auditRes.text()).toContain('settlement_id,status,builder_code');

    const notFoundRes = await getSquadsExport(
      new Request('http://localhost/api/settlements/999/export.squads.csv'),
      { params: Promise.resolve({ id: '999' }) }
    );
    expect(notFoundRes.status).toBe(404);
  });
});
