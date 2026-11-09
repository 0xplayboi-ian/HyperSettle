import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import Database from 'better-sqlite3';
import { SCHEMA_SQL } from '../src/db/schema';
import { parseHyperCoreFill, ingestFeeEvent, type RawHyperCoreFill } from '../src/ingestion/hypercore';

describe('HyperCore Ingestion & Database Operations', () => {
  let db: Database.Database;

  beforeEach(() => {
    // In-memory isolated database for each test
    db = new Database(':memory:');
    db.pragma('foreign_keys = ON');
    db.exec(SCHEMA_SQL);

    // Register a test builder code
    db.prepare(`
      INSERT INTO builder_codes (id, address, label, active)
      VALUES (1, '0xbuilder11111111111111111111111111111111', 'Test Builder', 1)
    `).run();
  });

  afterEach(() => {
    db.close();
  });

  it('parses raw HyperCore fill correctly with micro-USD precision', () => {
    const rawFill: RawHyperCoreFill = {
      coin: 'BTC',
      px: '90000.0', // $90,000 / BTC
      sz: '0.5',     // 0.5 BTC -> Notional = $45,000.00
      side: 'B',
      time: 1731100000000,
      hash: '0xabc123',
      tid: 999,
      b: '0xbuilder11111111111111111111111111111111',
      f: 10, // 10 decibps = 1 bp (0.01%)
      cloid: 'web_terminal_order_1'
    };

    const parsed = parseHyperCoreFill(rawFill);
    expect(parsed).not.toBeNull();
    // 45,000 USD = 45,000,000,000 micro-USD
    expect(parsed!.notionalMicroUsd).toBe(45_000_000_000n);
    // 0.01% of $45,000 = $4.50 = 4,500,000 micro-USD
    expect(parsed!.feeMicroUsd).toBe(4_500_000n);
    expect(parsed!.sourceLabel).toBe('web_terminal');
    expect(parsed!.externalId).toBe('hl_fill_0xabc123_999');
  });

  it('enforces idempotent ingestion (no double-counting)', () => {
    const rawFill: RawHyperCoreFill = {
      coin: 'ETH',
      px: '3000.0',
      sz: '10.0', // $30,000
      side: 'A',
      time: 1731105000000,
      hash: '0xdeadbeef',
      tid: 101,
      b: '0xbuilder11111111111111111111111111111111',
      f: 10,
      cloid: 'tg_sniper_bot'
    };

    const parsed = parseHyperCoreFill(rawFill)!;

    // First ingestion should succeed
    const first = ingestFeeEvent(db, parsed);
    expect(first.inserted).toBe(true);

    // Duplicate ingestion must NOT insert duplicate row
    const second = ingestFeeEvent(db, parsed);
    expect(second.inserted).toBe(false);

    // Verify row count is strictly 1
    const count = db.prepare('SELECT COUNT(*) as c FROM fee_events').get() as { c: number };
    expect(count.c).toBe(1);
  });

  it('correctly attributes different source labels', () => {
    const fillWeb: RawHyperCoreFill = {
      coin: 'SOL', px: '200', sz: '5', side: 'B', time: 1731100000000,
      hash: '0x1', tid: 1, b: '0xbuilder11111111111111111111111111111111', f: 10,
      cloid: 'web_terminal_trade'
    };
    const fillTg: RawHyperCoreFill = {
      coin: 'SOL', px: '200', sz: '5', side: 'B', time: 1731100000000,
      hash: '0x2', tid: 2, b: '0xbuilder11111111111111111111111111111111', f: 10,
      cloid: 'tg_bot_fast'
    };
    const fillApi: RawHyperCoreFill = {
      coin: 'SOL', px: '200', sz: '500', side: 'B', time: 1731100000000, // Large order $100k
      hash: '0x3', tid: 3, b: '0xbuilder11111111111111111111111111111111', f: 10,
      cloid: 'api_arb_hft'
    };

    expect(parseHyperCoreFill(fillWeb)!.sourceLabel).toBe('web_terminal');
    expect(parseHyperCoreFill(fillTg)!.sourceLabel).toBe('tg_bot_alpha');
    expect(parseHyperCoreFill(fillApi)!.sourceLabel).toBe('api_client');
  });
});
