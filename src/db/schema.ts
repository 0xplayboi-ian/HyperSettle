/**
 * HyperSettle SQLite Schema Definitions
 * Matching SPEC.md Technical Data Model
 */

export const SCHEMA_SQL = `
-- 1. Builder Codes Registered on HyperCore
CREATE TABLE IF NOT EXISTS builder_codes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  address TEXT UNIQUE NOT NULL,
  label TEXT NOT NULL,
  active INTEGER NOT NULL DEFAULT 1,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_builder_codes_address ON builder_codes(address);

-- 2. Team Contributors
CREATE TABLE IF NOT EXISTS contributors (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  wallet_evm TEXT,
  wallet_solana TEXT,
  active INTEGER NOT NULL DEFAULT 1,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- 3. Revenue Split Rules
CREATE TABLE IF NOT EXISTS split_rules (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  builder_code_id INTEGER NOT NULL REFERENCES builder_codes(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  effective_from TEXT NOT NULL,
  effective_to TEXT,
  type TEXT NOT NULL CHECK (type IN ('percent', 'fixed_per_period')),
  config TEXT NOT NULL, -- JSON string matching SplitConfig
  version INTEGER NOT NULL DEFAULT 1,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_split_rules_builder ON split_rules(builder_code_id, effective_from);

-- 4. Raw Ingested Events (Idempotent Ledger Audit)
CREATE TABLE IF NOT EXISTS raw_events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  source TEXT NOT NULL,
  external_id TEXT UNIQUE NOT NULL,
  payload TEXT NOT NULL, -- JSON raw fill event
  fetched_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_raw_events_ext ON raw_events(external_id);

-- 5. Parsed Builder Fee Events
CREATE TABLE IF NOT EXISTS fee_events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  external_id TEXT UNIQUE NOT NULL,
  builder_code_id INTEGER NOT NULL REFERENCES builder_codes(id) ON DELETE CASCADE,
  source_label TEXT NOT NULL, -- e.g. 'web_terminal', 'tg_bot_alpha', 'api_client'
  trader TEXT,
  notional_micro_usd INTEGER NOT NULL,
  fee_micro_usd INTEGER NOT NULL,
  block_time TEXT NOT NULL,
  tx_ref TEXT,
  inserted_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_fee_events_builder_time ON fee_events(builder_code_id, block_time);
CREATE INDEX IF NOT EXISTS idx_fee_events_source ON fee_events(source_label);

-- 6. Settlement Records (Draft or Final)
CREATE TABLE IF NOT EXISTS settlements (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  builder_code_id INTEGER NOT NULL REFERENCES builder_codes(id) ON DELETE CASCADE,
  period_start TEXT NOT NULL,
  period_end TEXT NOT NULL,
  split_rule_version INTEGER NOT NULL,
  status TEXT NOT NULL DEFAULT 'draft' CHECK (status IN ('draft', 'final')),
  total_fee_micro_usd INTEGER NOT NULL,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  locked_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_settlements_builder ON settlements(builder_code_id, period_start);

-- 7. Settlement Payout Lines
CREATE TABLE IF NOT EXISTS settlement_lines (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  settlement_id INTEGER NOT NULL REFERENCES settlements(id) ON DELETE CASCADE,
  contributor_id TEXT NOT NULL REFERENCES contributors(id),
  amount_micro_usd INTEGER NOT NULL,
  payout_chain TEXT NOT NULL CHECK (payout_chain IN ('solana', 'evm')),
  payout_address TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_settlement_lines_parent ON settlement_lines(settlement_id);

-- 8. Onchain HyperCore Reconciliation Snapshots
CREATE TABLE IF NOT EXISTS reconciliation_snapshots (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  builder_code_id INTEGER NOT NULL REFERENCES builder_codes(id) ON DELETE CASCADE,
  period_start TEXT NOT NULL,
  period_end TEXT NOT NULL,
  local_total_micro_usd INTEGER NOT NULL,
  onchain_total_micro_usd INTEGER NOT NULL,
  drift_micro_usd INTEGER NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('matched', 'minor_drift', 'discrepancy')),
  source TEXT NOT NULL DEFAULT 'hypercore_referral_api',
  notes TEXT,
  checked_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_reconciliation_builder ON reconciliation_snapshots(builder_code_id, checked_at);
`;
