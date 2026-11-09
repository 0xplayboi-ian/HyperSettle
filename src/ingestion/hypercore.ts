/**
 * HyperCore Ingestion & Builder Fee Parser
 * 
 * Ingests fill events from Hyperliquid HyperCore L1, parses builder fee attributes:
 * - b: Destination builder address
 * - f: Fee rate in tenths of a basis point (decibps)
 * 
 * Enforces idempotent insertion using unique fill / trade IDs.
 */

import Database from 'better-sqlite3';

export interface RawHyperCoreFill {
  coin: string;
  px: string;       // Execution price
  sz: string;       // Execution size
  side: 'B' | 'A';  // Buy or Ask/Sell
  time: number;     // Milliseconds epoch
  hash: string;     // Transaction hash
  tid: number | string; // Trade ID
  b?: string;       // Builder address
  f?: number;       // Fee rate in decibps (tenths of a bp: 10 = 1 bp = 0.01%)
  cloid?: string;   // Client order ID (e.g. "web_terminal_abc123" or "tg_bot_456")
  user?: string;    // Trader address
}

export interface ParsedFeeEvent {
  externalId: string;
  builderAddress: string;
  sourceLabel: string;
  trader?: string;
  notionalMicroUsd: bigint;
  feeMicroUsd: bigint;
  blockTime: string; // ISO UTC string
  txRef: string;
  rawJson: string;
}

/**
 * Determine source label (attribution channel) from client order ID or user metadata
 */
export function determineSourceLabel(fill: RawHyperCoreFill): string {
  const cloid = fill.cloid?.toLowerCase() || '';
  if (cloid.startsWith('tg_') || cloid.includes('telegram') || cloid.includes('sniper')) {
    return 'tg_bot_alpha';
  }
  if (cloid.startsWith('api_') || cloid.includes('arb') || cloid.includes('algo')) {
    return 'api_client';
  }
  if (cloid.startsWith('web_') || cloid.includes('terminal') || cloid.includes('app')) {
    return 'web_terminal';
  }
  // Default based on size: large volume tends to be API, small volume web
  const notional = parseFloat(fill.px) * parseFloat(fill.sz);
  if (notional > 50_000) return 'api_client';
  return 'web_terminal';
}

/**
 * Parse raw HyperCore fill into deterministic micro-USD fee event
 */
export function parseHyperCoreFill(fill: RawHyperCoreFill): ParsedFeeEvent | null {
  if (!fill.b || !fill.f || fill.f <= 0) {
    return null; // Not a builder fee order
  }

  const px = parseFloat(fill.px);
  const sz = parseFloat(fill.sz);
  if (isNaN(px) || isNaN(sz) || px <= 0 || sz <= 0) {
    return null;
  }

  // Calculate notional in micro-USD (10^-6)
  // notional = px * sz * 1,000,000
  const notionalFloat = px * sz;
  const notionalMicroUsd = BigInt(Math.round(notionalFloat * 1_000_000));

  // Builder fee in tenths of a basis point:
  // 1 decibp = 0.001% = 1 / 100,000
  // fee = (notional * f) / 100,000
  const feeMicroUsd = (notionalMicroUsd * BigInt(fill.f)) / 100_000n;

  const blockTime = new Date(fill.time).toISOString();
  const externalId = `hl_fill_${fill.hash}_${fill.tid}`;

  return {
    externalId,
    builderAddress: fill.b.toLowerCase(),
    sourceLabel: determineSourceLabel(fill),
    trader: fill.user,
    notionalMicroUsd,
    feeMicroUsd,
    blockTime,
    txRef: fill.hash,
    rawJson: JSON.stringify(fill)
  };
}

/**
 * Idempotently insert parsed fee event into SQLite database
 */
export function ingestFeeEvent(db: Database.Database, event: ParsedFeeEvent): { inserted: boolean; id?: number } {
  // 1. Find or verify builder code exists
  const builder = db.prepare('SELECT id FROM builder_codes WHERE lower(address) = ?').get(event.builderAddress) as { id: number } | undefined;
  if (!builder) {
    return { inserted: false };
  }

  // 2. Insert raw event audit record
  db.prepare(`
    INSERT OR IGNORE INTO raw_events (source, external_id, payload, fetched_at)
    VALUES (?, ?, ?, datetime('now'))
  `).run('hypercore_fills', event.externalId, event.rawJson);

  // 3. Insert parsed fee event
  const result = db.prepare(`
    INSERT OR IGNORE INTO fee_events (
      external_id, builder_code_id, source_label, trader,
      notional_micro_usd, fee_micro_usd, block_time, tx_ref
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
  `).run(
    event.externalId,
    builder.id,
    event.sourceLabel,
    event.trader || null,
    event.notionalMicroUsd.toString(),
    event.feeMicroUsd.toString(),
    event.blockTime,
    event.txRef
  );

  return {
    inserted: result.changes > 0,
    id: Number(result.lastInsertRowid)
  };
}
