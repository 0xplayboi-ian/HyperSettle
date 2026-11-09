# HyperSettle: Project Specification

**Target:** Colosseum Eternal (4-Week Sprint)  
**Primary Track:** Payments / Developer Tooling  
**Author / Team:** HyperSettle Team  

---

## 1. Summary
**HyperSettle** is a financial operations web application for teams that earn builder fees on Hyperliquid. It ingests builder-fee activity directly from Hyperliquid's onchain data (HyperCore), reconciles it against official referral and reward state, aggregates revenue by day, week, and source (bots, frontends, API endpoints), calculates contributor revenue shares with deterministic integer math, and exports settlement reports. 

Settlement reports can be exported as standard financial CSVs, direct **Solana SPL USDC batch transactions**, or **Squads Multisig batch transfer files**. HyperSettle is strictly non-custodial and does not hold private keys or custody funds.

---

## 2. Verified Technical Parameters & Hyperliquid Architecture

1. **Builder Fee Identification:**
   - Orders specify builder attribution via the `builder` payload parameter:
     ```json
     { "b": "0xBuilderAddress", "f": 10 }
     ```
   - `b`: Destination address for builder fee collection.
   - `f`: Fee rate in **tenths of a basis point** (decibps). `1` = 0.001%, `10` = 0.01% (1 bp).
2. **Protocol Caps:**
   - Maximum Perp Builder Fee: 0.1% (10 bps).
   - Maximum Spot Builder Fee: 1.0% (100 bps).
3. **Accounting Currency & Precision:**
   - Hyperliquid perps and spot markets settle in **USDC**.
   - All internal values are stored in **integer micro-USD ($10^{-6}$)**, matching native 6-decimal USDC precision. Floating-point arithmetic is forbidden for accounting totals.
   - No external price lookup is required for perp builder fee revenue.
4. **Finality & Consensus:**
   - Consensus Engine: **HyperBFT** (HotStuff-based BFT).
   - Instant, single-slot deterministic finality. No probabilistic chain reorganizations.
   - Ingestion safe window: 2 to 3 seconds (~10 blocks).
5. **Rate Limits & API Weights:**
   - Hyperliquid REST: 1,200 weight budget per minute per IP address.
   - Standard `/info` requests cost 2 points (~600 req/min).

---

## 3. Data Model

### `raw_events`
- `id` (INTEGER, PK)
- `source` (TEXT) - e.g., `"hypercore_fills"`, `"quicknode_stream"`
- `payload` (JSON)
- `external_id` (TEXT, UNIQUE)
- `fetched_at` (TIMESTAMP UTC)

### `fee_events`
- `id` (INTEGER, PK)
- `external_id` (TEXT, UNIQUE)
- `builder_code` (TEXT, Indexed)
- `source_label` (TEXT) - e.g., `"web_terminal"`, `"tg_bot_alpha"`, `"api_client"`
- `trader` (TEXT, Optional)
- `notional_micro_usd` (INTEGER)
- `fee_micro_usd` (INTEGER)
- `block_time` (TIMESTAMP UTC)
- `tx_ref` (TEXT, Optional)
- `inserted_at` (TIMESTAMP UTC)

### `builder_codes`
- `id` (INTEGER, PK)
- `address` (TEXT, UNIQUE)
- `label` (TEXT)
- `active` (BOOLEAN)

### `contributors`
- `id` (INTEGER, PK)
- `name` (TEXT)
- `wallet_evm` (TEXT, Optional)
- `wallet_solana` (TEXT, Optional - Base58)
- `active` (BOOLEAN)

### `split_rules`
- `id` (INTEGER, PK)
- `builder_code_id` (INTEGER, FK)
- `name` (TEXT)
- `effective_from` (TIMESTAMP UTC)
- `effective_to` (TIMESTAMP UTC, Optional)
- `type` (TEXT: `'percent'` | `'fixed_per_period'`)
- `config` (JSON) - e.g. contributor weights, cap thresholds, fallback treasuries
- `version` (INTEGER)

### `settlements`
- `id` (INTEGER, PK)
- `builder_code_id` (INTEGER, FK)
- `period_start` (TIMESTAMP UTC)
- `period_end` (TIMESTAMP UTC)
- `split_rule_version` (INTEGER)
- `status` (TEXT: `'draft'` | `'final'`)
- `total_fee_micro_usd` (INTEGER)
- `created_at` (TIMESTAMP UTC)
- `locked_at` (TIMESTAMP UTC, Optional)

### `settlement_lines`
- `id` (INTEGER, PK)
- `settlement_id` (INTEGER, FK)
- `contributor_id` (INTEGER, FK)
- `amount_micro_usd` (INTEGER)
- `payout_chain` (TEXT: `'solana'` | `'evm'`)
- `payout_address` (TEXT)

---

## 4. Deterministic Split Logic & Rounding Rules

1. **Percent Rule:** Sum of contributor percentages must equal 100%.
2. **Fixed Rule:** Contributor allocated fixed micro-USD amount, capped at period total; any remainder routes to treasury.
3. **Rounding Remainder Allocation:**
   - Any fractional micro-USD rounding residue is deterministically credited to the largest recipient.
   - In case of a tie, the contributor with the lexicographically smaller ID receives the remainder.
   - Invariant: `SUM(settlement_lines.amount_micro_usd) === settlements.total_fee_micro_usd`.

---

## 5. API Endpoints

- `GET  /api/health`
- `GET  /api/builder-codes`
- `POST /api/builder-codes`
- `GET  /api/revenue?builder_code=&from=&to=&group=day|week|source`
- `GET  /api/fee-events?builder_code=&from=&to=&limit=&cursor=`
- `GET  /api/contributors`
- `POST /api/contributors`
- `GET  /api/split-rules?builder_code=`
- `POST /api/split-rules`
- `POST /api/settlements/preview`
- `POST /api/settlements/finalize`
- `GET  /api/settlements/:id/export.csv`
- `GET  /api/settlements/:id/export.squads.csv` (Solana Squads Multisig Batch format)
- `GET  /api/reconciliation?builder_code=&from=&to=`

---

## 6. Sprint Milestones (Nov 6 – Dec 4, 2026)

- **Week 1:** Data ingestion from HyperCore, SQLite schema, unit tests for split math & rounding.
- **Week 2:** Revenue & Attribution REST API, Overview UI, daily/weekly charts, automated reconciliation runner.
- **Week 3:** Contributor & Rule admin UI, Settlement generation & finalization, Squads Solana CSV exporter.
- **Week 4:** UI refinement, end-to-end testing, demo video, pitch deck, final submission.
