/**
 * HyperSettle Financial Operations Service Layer
 *
 * Centralizes SQLite queries, BigInt micro-USD aggregations,
 * split rule resolution, cursor pagination, and transactional
 * settlement finalization.
 */

import Database from 'better-sqlite3';
import {
  calculateSplit,
  deserializeSplitConfig,
  formatMicroUsd,
  microUsdToDecimal,
  serializeSplitConfig,
  validateSplitConfig,
  type SplitConfig
} from '../core/splits';
import {
  isValidSolanaAddress,
  type SettlementExportHeader,
  type SettlementExportLine
} from '../export/squads';

const EVM_ADDRESS_REGEX = /^0x[a-fA-F0-9]{40}$/;

export interface BuilderCodeRecord {
  id: number;
  address: string;
  label: string;
  active: boolean;
  createdAt: string;
}

export interface ContributorRecord {
  id: string;
  name: string;
  walletEvm: string | null;
  walletSolana: string | null;
  active: boolean;
  createdAt: string;
}

export interface SplitRuleRecord {
  id: number;
  builderCodeId: number;
  builderAddress?: string;
  builderLabel?: string;
  name: string;
  effectiveFrom: string;
  effectiveTo: string | null;
  type: 'percent' | 'fixed_per_period';
  config: SplitConfig;
  version: number;
  createdAt: string;
}

export type RevenueGroupBy = 'day' | 'week' | 'source';

export interface RevenueBucket {
  key: string;
  fillCount: number;
  notionalMicroUsd: string;
  notionalUsd: string;
  feeMicroUsd: string;
  feeUsd: string;
}

/**
 * Resolve optional builder filter (numeric ID or 0x EVM address) to builder_code_id.
 */
export function resolveBuilderCode(
  db: Database.Database,
  builderCode?: string | number | null
): BuilderCodeRecord | null {
  if (builderCode === undefined || builderCode === null || builderCode === '') {
    return null;
  }

  let row: any;
  if (typeof builderCode === 'number' || /^\d+$/.test(String(builderCode))) {
    row = db
      .prepare('SELECT id, address, label, active, created_at FROM builder_codes WHERE id = ?')
      .get(Number(builderCode));
  } else {
    row = db
      .prepare('SELECT id, address, label, active, created_at FROM builder_codes WHERE lower(address) = lower(?)')
      .get(String(builderCode));
  }

  if (!row) return null;
  return {
    id: row.id,
    address: row.address,
    label: row.label,
    active: Boolean(row.active),
    createdAt: row.created_at
  };
}

export function listBuilderCodes(db: Database.Database): BuilderCodeRecord[] {
  const rows = db
    .prepare('SELECT id, address, label, active, created_at FROM builder_codes ORDER BY id ASC')
    .all() as any[];

  return rows.map(r => ({
    id: r.id,
    address: r.address,
    label: r.label,
    active: Boolean(r.active),
    createdAt: r.created_at
  }));
}

export function createBuilderCode(
  db: Database.Database,
  input: { address: string; label: string }
): BuilderCodeRecord {
  const address = input.address.trim().toLowerCase();
  const label = input.label.trim();

  if (!EVM_ADDRESS_REGEX.test(address)) {
    throw new Error('Builder code address must be a valid 0x-prefixed 20-byte EVM address');
  }
  if (!label) {
    throw new Error('Builder code label is required');
  }

  const res = db
    .prepare('INSERT INTO builder_codes (address, label, active) VALUES (?, ?, 1)')
    .run(address, label);

  return resolveBuilderCode(db, Number(res.lastInsertRowid))!;
}

export function listContributors(db: Database.Database): ContributorRecord[] {
  const rows = db
    .prepare('SELECT id, name, wallet_evm, wallet_solana, active, created_at FROM contributors ORDER BY name ASC')
    .all() as any[];

  return rows.map(r => ({
    id: r.id,
    name: r.name,
    walletEvm: r.wallet_evm,
    walletSolana: r.wallet_solana,
    active: Boolean(r.active),
    createdAt: r.created_at
  }));
}

export function createContributor(
  db: Database.Database,
  input: { id?: string; name: string; walletEvm?: string | null; walletSolana?: string | null }
): ContributorRecord {
  const name = input.name.trim();
  if (!name) {
    throw new Error('Contributor name is required');
  }

  const walletEvm = input.walletEvm?.trim() || null;
  const walletSolana = input.walletSolana?.trim() || null;

  if (!walletEvm && !walletSolana) {
    throw new Error('At least one payout wallet (Solana Base58 or EVM) is required');
  }
  if (walletEvm && !EVM_ADDRESS_REGEX.test(walletEvm)) {
    throw new Error(`Invalid EVM wallet address: ${walletEvm}`);
  }
  if (walletSolana && !isValidSolanaAddress(walletSolana)) {
    throw new Error(`Invalid Solana Base58 wallet address: ${walletSolana}`);
  }

  const slug =
    input.id?.trim() ||
    `contributor_${name
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '_')
      .replace(/^_|_$/g, '')
      .slice(0, 32)}`;

  db.prepare(
    'INSERT INTO contributors (id, name, wallet_evm, wallet_solana, active) VALUES (?, ?, ?, ?, 1)'
  ).run(slug, name, walletEvm, walletSolana);

  const row = db
    .prepare('SELECT id, name, wallet_evm, wallet_solana, active, created_at FROM contributors WHERE id = ?')
    .get(slug) as any;

  return {
    id: row.id,
    name: row.name,
    walletEvm: row.wallet_evm,
    walletSolana: row.wallet_solana,
    active: Boolean(row.active),
    createdAt: row.created_at
  };
}

export function listSplitRules(
  db: Database.Database,
  builderFilter?: string | number | null
): SplitRuleRecord[] {
  let builderId: number | null = null;
  if (builderFilter !== undefined && builderFilter !== null && builderFilter !== '') {
    const resolved = resolveBuilderCode(db, builderFilter);
    if (!resolved) return [];
    builderId = resolved.id;
  }

  const query = `
    SELECT sr.id, sr.builder_code_id, bc.address as builder_address, bc.label as builder_label,
           sr.name, sr.effective_from, sr.effective_to, sr.type, sr.config, sr.version, sr.created_at
    FROM split_rules sr
    JOIN builder_codes bc ON bc.id = sr.builder_code_id
    ${builderId !== null ? 'WHERE sr.builder_code_id = ?' : ''}
    ORDER BY sr.builder_code_id ASC, sr.version DESC, sr.id DESC
  `;

  const rows = (builderId !== null
    ? db.prepare(query).all(builderId)
    : db.prepare(query).all()) as any[];

  return rows.map(r => ({
    id: r.id,
    builderCodeId: r.builder_code_id,
    builderAddress: r.builder_address,
    builderLabel: r.builder_label,
    name: r.name,
    effectiveFrom: r.effective_from,
    effectiveTo: r.effective_to,
    type: r.type,
    config: deserializeSplitConfig(r.config),
    version: r.version,
    createdAt: r.created_at
  }));
}

export function createSplitRule(
  db: Database.Database,
  input: {
    builderCodeId: number;
    name: string;
    effectiveFrom?: string;
    config: SplitConfig;
  }
): SplitRuleRecord {
  const builder = resolveBuilderCode(db, input.builderCodeId);
  if (!builder) {
    throw new Error(`Builder code #${input.builderCodeId} not found`);
  }

  const name = input.name.trim();
  if (!name) {
    throw new Error('Split rule name is required');
  }

  const validation = validateSplitConfig(input.config);
  if (!validation.valid) {
    throw new Error(validation.error);
  }

  // Verify all referenced contributors exist
  const referencedIds =
    input.config.type === 'percent'
      ? input.config.recipients.map(r => r.contributorId)
      : [
          ...input.config.fixedRecipients.map(r => r.contributorId),
          input.config.spilloverRecipientId
        ];

  const uniqueIds = Array.from(new Set(referencedIds));
  const checkStmt = db.prepare('SELECT id FROM contributors WHERE id = ?');
  for (const cid of uniqueIds) {
    if (!checkStmt.get(cid)) {
      throw new Error(`Referenced contributor "${cid}" does not exist`);
    }
  }

  const latestVersionRow = db
    .prepare('SELECT COALESCE(MAX(version), 0) as max_v FROM split_rules WHERE builder_code_id = ?')
    .get(builder.id) as { max_v: number };

  const nextVersion = latestVersionRow.max_v + 1;
  const effectiveFrom = input.effectiveFrom || new Date().toISOString();

  const res = db
    .prepare(
      `INSERT INTO split_rules (builder_code_id, name, effective_from, type, config, version)
       VALUES (?, ?, ?, ?, ?, ?)`
    )
    .run(
      builder.id,
      name,
      effectiveFrom,
      input.config.type,
      serializeSplitConfig(input.config),
      nextVersion
    );

  const insertedId = Number(res.lastInsertRowid);
  const list = listSplitRules(db, builder.id);
  return list.find(r => r.id === insertedId)!;
}

/**
 * Aggregate revenue grouped by day, week, or attribution source.
 */
export function getRevenueSummary(
  db: Database.Database,
  params: {
    builderCode?: string | null;
    from?: string | null;
    to?: string | null;
    group?: RevenueGroupBy;
  } = {}
) {
  const group: RevenueGroupBy = params.group ?? 'day';
  const whereClauses: string[] = [];
  const bindParams: unknown[] = [];

  if (params.builderCode) {
    const resolved = resolveBuilderCode(db, params.builderCode);
    if (!resolved) {
      throw new Error(`Unknown builder code filter: ${params.builderCode}`);
    }
    whereClauses.push('builder_code_id = ?');
    bindParams.push(resolved.id);
  }

  if (params.from) {
    whereClauses.push('block_time >= ?');
    bindParams.push(params.from);
  }
  if (params.to) {
    whereClauses.push('block_time <= ?');
    bindParams.push(params.to);
  }

  const whereSql = whereClauses.length > 0 ? `WHERE ${whereClauses.join(' AND ')}` : '';

  let groupExpr = `strftime('%Y-%m-%d', block_time)`;
  let orderSql = 'bucket_key ASC';
  if (group === 'week') {
    groupExpr = `strftime('%Y-W%W', block_time)`;
  } else if (group === 'source') {
    groupExpr = `source_label`;
    orderSql = 'fee_sum DESC';
  }

  const rows = db
    .prepare(
      `SELECT ${groupExpr} as bucket_key,
              COUNT(*) as fill_count,
              COALESCE(SUM(notional_micro_usd), 0) as notional_sum,
              COALESCE(SUM(fee_micro_usd), 0) as fee_sum
       FROM fee_events
       ${whereSql}
       GROUP BY bucket_key
       ORDER BY ${orderSql}`
    )
    .all(...bindParams) as Array<{
    bucket_key: string;
    fill_count: number;
    notional_sum: number | string;
    fee_sum: number | string;
  }>;

  let totalFills = 0;
  let totalNotional = 0n;
  let totalFees = 0n;

  const buckets: RevenueBucket[] = rows.map(row => {
    const notional = BigInt(row.notional_sum ?? 0);
    const fee = BigInt(row.fee_sum ?? 0);
    totalFills += row.fill_count;
    totalNotional += notional;
    totalFees += fee;

    return {
      key: row.bucket_key,
      fillCount: row.fill_count,
      notionalMicroUsd: notional.toString(),
      notionalUsd: formatMicroUsd(notional, 2),
      feeMicroUsd: fee.toString(),
      feeUsd: formatMicroUsd(fee, 6)
    };
  });

  return {
    groupBy: group,
    totals: {
      fillCount: totalFills,
      notionalMicroUsd: totalNotional.toString(),
      notionalUsd: formatMicroUsd(totalNotional, 2),
      feeMicroUsd: totalFees.toString(),
      feeUsdc: microUsdToDecimal(totalFees),
      feeUsdFormatted: formatMicroUsd(totalFees, 2)
    },
    buckets
  };
}

/**
 * Cursor-paginated listing of raw attributed fee_events (chronological descending).
 */
export function getFeeEvents(
  db: Database.Database,
  params: {
    builderCode?: string | null;
    from?: string | null;
    to?: string | null;
    limit?: number;
    cursor?: string | null;
  } = {}
) {
  const limit = Math.min(Math.max(params.limit ?? 50, 1), 250);
  const whereClauses: string[] = [];
  const bindParams: unknown[] = [];

  if (params.builderCode) {
    const resolved = resolveBuilderCode(db, params.builderCode);
    if (!resolved) {
      throw new Error(`Unknown builder code filter: ${params.builderCode}`);
    }
    whereClauses.push('fe.builder_code_id = ?');
    bindParams.push(resolved.id);
  }
  if (params.from) {
    whereClauses.push('fe.block_time >= ?');
    bindParams.push(params.from);
  }
  if (params.to) {
    whereClauses.push('fe.block_time <= ?');
    bindParams.push(params.to);
  }

  if (params.cursor) {
    try {
      const decoded = JSON.parse(Buffer.from(params.cursor, 'base64url').toString('utf8'));
      if (decoded?.blockTime && typeof decoded?.id === 'number') {
        whereClauses.push('(fe.block_time < ? OR (fe.block_time = ? AND fe.id < ?))');
        bindParams.push(decoded.blockTime, decoded.blockTime, decoded.id);
      }
    } catch {
      throw new Error('Invalid pagination cursor');
    }
  }

  const whereSql = whereClauses.length > 0 ? `WHERE ${whereClauses.join(' AND ')}` : '';

  const rows = db
    .prepare(
      `SELECT fe.id, fe.external_id, fe.builder_code_id, bc.address as builder_address,
              bc.label as builder_label, fe.source_label, fe.trader,
              fe.notional_micro_usd, fe.fee_micro_usd, fe.block_time, fe.tx_ref
       FROM fee_events fe
       JOIN builder_codes bc ON bc.id = fe.builder_code_id
       ${whereSql}
       ORDER BY fe.block_time DESC, fe.id DESC
       LIMIT ?`
    )
    .all(...bindParams, limit + 1) as any[];

  const hasMore = rows.length > limit;
  const pageRows = hasMore ? rows.slice(0, limit) : rows;
  const lastRow = pageRows[pageRows.length - 1];
  const nextCursor =
    hasMore && lastRow
      ? Buffer.from(JSON.stringify({ blockTime: lastRow.block_time, id: lastRow.id })).toString('base64url')
      : null;

  return {
    events: pageRows.map(r => {
      const notional = BigInt(r.notional_micro_usd);
      const fee = BigInt(r.fee_micro_usd);
      return {
        id: r.id,
        externalId: r.external_id,
        builderCodeId: r.builder_code_id,
        builderAddress: r.builder_address,
        builderLabel: r.builder_label,
        sourceLabel: r.source_label,
        trader: r.trader,
        notionalMicroUsd: notional.toString(),
        notionalUsd: formatMicroUsd(notional, 2),
        feeMicroUsd: fee.toString(),
        feeUsd: formatMicroUsd(fee, 6),
        blockTime: r.block_time,
        txRef: r.tx_ref
      };
    }),
    nextCursor,
    hasMore
  };
}

export interface SettlementPreviewLine {
  contributorId: string;
  contributorName: string;
  payoutChain: 'solana' | 'evm';
  payoutAddress: string;
  amountMicroUsd: string;
  amountUsdc: string;
  formattedUsd: string;
  bpsCalculated: number;
}

export interface SettlementPreviewResult {
  builderCodeId: number;
  builderAddress: string;
  builderLabel: string;
  periodStart: string;
  periodEnd: string;
  fillCount: number;
  splitRuleId: number;
  splitRuleName: string;
  splitRuleVersion: number;
  totalFeeMicroUsd: string;
  totalFeeUsdc: string;
  totalFeeFormatted: string;
  residueAllocatedMicroUsd: string;
  residueRecipientId: string | null;
  invariantPassed: boolean;
  overlappingFinalizedSettlementId: number | null;
  lines: SettlementPreviewLine[];
}

/**
 * Preview a deterministic settlement distribution for a builder code and time window.
 */
export function previewSettlement(
  db: Database.Database,
  params: {
    builderCodeId: number | string;
    periodStart: string;
    periodEnd: string;
    splitRuleId?: number;
  }
): SettlementPreviewResult {
  const builder = resolveBuilderCode(db, params.builderCodeId);
  if (!builder) {
    throw new Error(`Builder code "${params.builderCodeId}" not found`);
  }

  if (params.periodStart >= params.periodEnd) {
    throw new Error('periodStart must be strictly earlier than periodEnd');
  }

  // Pick split rule (explicit or latest version effective by periodEnd)
  const ruleRow = params.splitRuleId
    ? (db
        .prepare(
          'SELECT id, name, type, config, version FROM split_rules WHERE id = ? AND builder_code_id = ?'
        )
        .get(params.splitRuleId, builder.id) as any)
    : (db
        .prepare(
          `SELECT id, name, type, config, version
           FROM split_rules
           WHERE builder_code_id = ? AND effective_from <= ?
           ORDER BY version DESC, id DESC LIMIT 1`
        )
        .get(builder.id, params.periodEnd) as any);

  if (!ruleRow) {
    throw new Error(`No active split rule found for builder "${builder.label}"`);
  }

  const agg = db
    .prepare(
      `SELECT COUNT(*) as fill_count, COALESCE(SUM(fee_micro_usd), 0) as fee_sum
       FROM fee_events
       WHERE builder_code_id = ? AND block_time >= ? AND block_time <= ?`
    )
    .get(builder.id, params.periodStart, params.periodEnd) as {
    fill_count: number;
    fee_sum: number | string;
  };

  const totalFee = BigInt(agg.fee_sum ?? 0);
  const config = deserializeSplitConfig(ruleRow.config);
  const split = calculateSplit(totalFee, config);

  const contributors = listContributors(db);
  const contribMap = new Map(contributors.map(c => [c.id, c]));

  const lines: SettlementPreviewLine[] = split.lines.map(l => {
    const contributor = contribMap.get(l.contributorId);
    const payoutChain: 'solana' | 'evm' = contributor?.walletSolana ? 'solana' : 'evm';
    const payoutAddress =
      payoutChain === 'solana'
        ? contributor?.walletSolana ?? ''
        : contributor?.walletEvm ?? '';

    return {
      contributorId: l.contributorId,
      contributorName: contributor?.name ?? l.contributorId,
      payoutChain,
      payoutAddress,
      amountMicroUsd: l.amountMicroUsd.toString(),
      amountUsdc: microUsdToDecimal(l.amountMicroUsd),
      formattedUsd: l.formattedUsd,
      bpsCalculated: l.bpsCalculated
    };
  });

  const overlap = db
    .prepare(
      `SELECT id FROM settlements
       WHERE builder_code_id = ? AND status = 'final'
         AND period_start <= ? AND period_end >= ?
       LIMIT 1`
    )
    .get(builder.id, params.periodEnd, params.periodStart) as { id: number } | undefined;

  return {
    builderCodeId: builder.id,
    builderAddress: builder.address,
    builderLabel: builder.label,
    periodStart: params.periodStart,
    periodEnd: params.periodEnd,
    fillCount: agg.fill_count,
    splitRuleId: ruleRow.id,
    splitRuleName: ruleRow.name,
    splitRuleVersion: ruleRow.version,
    totalFeeMicroUsd: split.totalFeeMicroUsd.toString(),
    totalFeeUsdc: microUsdToDecimal(split.totalFeeMicroUsd),
    totalFeeFormatted: formatMicroUsd(split.totalFeeMicroUsd, 6),
    residueAllocatedMicroUsd: split.residueAllocatedMicroUsd.toString(),
    residueRecipientId: split.residueRecipientId ?? null,
    invariantPassed: split.invariantPassed,
    overlappingFinalizedSettlementId: overlap?.id ?? null,
    lines
  };
}

/**
 * Transactionally lock and persist a finalized settlement + payout lines.
 * Guards against overlapping finalized periods and enforces SUM(lines) === total.
 */
export function finalizeSettlement(
  db: Database.Database,
  params: {
    builderCodeId: number | string;
    periodStart: string;
    periodEnd: string;
    splitRuleId?: number;
  }
) {
  return db.transaction(() => {
    const preview = previewSettlement(db, params);

    if (preview.overlappingFinalizedSettlementId !== null) {
      throw new Error(
        `Period overlaps existing finalized settlement #${preview.overlappingFinalizedSettlementId}`
      );
    }

    if (BigInt(preview.totalFeeMicroUsd) <= 0n) {
      throw new Error('Cannot finalize a settlement with zero builder fees in the selected period');
    }

    if (!preview.invariantPassed) {
      throw new Error('Split invariant check failed: SUM(lines) !== totalFeeMicroUsd');
    }

    for (const line of preview.lines) {
      if (!line.payoutAddress) {
        throw new Error(`Missing payout address for contributor "${line.contributorId}"`);
      }
    }

    const res = db
      .prepare(
        `INSERT INTO settlements (
           builder_code_id, period_start, period_end, split_rule_version,
           status, total_fee_micro_usd, locked_at
         ) VALUES (?, ?, ?, ?, 'final', ?, datetime('now'))`
      )
      .run(
        preview.builderCodeId,
        preview.periodStart,
        preview.periodEnd,
        preview.splitRuleVersion,
        preview.totalFeeMicroUsd
      );

    const settlementId = Number(res.lastInsertRowid);
    const insertLine = db.prepare(
      `INSERT INTO settlement_lines (
         settlement_id, contributor_id, amount_micro_usd, payout_chain, payout_address
       ) VALUES (?, ?, ?, ?, ?)`
    );

    for (const line of preview.lines) {
      insertLine.run(
        settlementId,
        line.contributorId,
        line.amountMicroUsd,
        line.payoutChain,
        line.payoutAddress
      );
    }

    return {
      settlementId,
      status: 'final' as const,
      ...preview
    };
  })();
}

export function listSettlements(db: Database.Database, builderFilter?: string | number | null) {
  let builderId: number | null = null;
  if (builderFilter) {
    const resolved = resolveBuilderCode(db, builderFilter);
    if (!resolved) return [];
    builderId = resolved.id;
  }

  const rows = (builderId !== null
    ? db
        .prepare(
          `SELECT s.*, bc.address as builder_address, bc.label as builder_label
           FROM settlements s
           JOIN builder_codes bc ON bc.id = s.builder_code_id
           WHERE s.builder_code_id = ?
           ORDER BY s.id DESC`
        )
        .all(builderId)
    : db
        .prepare(
          `SELECT s.*, bc.address as builder_address, bc.label as builder_label
           FROM settlements s
           JOIN builder_codes bc ON bc.id = s.builder_code_id
           ORDER BY s.id DESC`
        )
        .all()) as any[];

  return rows.map(r => {
    const total = BigInt(r.total_fee_micro_usd);
    return {
      id: r.id,
      builderCodeId: r.builder_code_id,
      builderAddress: r.builder_address,
      builderLabel: r.builder_label,
      periodStart: r.period_start,
      periodEnd: r.period_end,
      splitRuleVersion: r.split_rule_version,
      status: r.status,
      totalFeeMicroUsd: total.toString(),
      totalFeeUsdc: microUsdToDecimal(total),
      totalFeeFormatted: formatMicroUsd(total, 6),
      createdAt: r.created_at,
      lockedAt: r.locked_at
    };
  });
}

export function getSettlementExportData(
  db: Database.Database,
  settlementId: number
): { header: SettlementExportHeader; lines: SettlementExportLine[] } | null {
  const sRow = db
    .prepare(
      `SELECT s.*, bc.address as builder_address, bc.label as builder_label
       FROM settlements s
       JOIN builder_codes bc ON bc.id = s.builder_code_id
       WHERE s.id = ?`
    )
    .get(settlementId) as any;

  if (!sRow) return null;

  const lineRows = db
    .prepare(
      `SELECT sl.*, COALESCE(c.name, sl.contributor_id) as contributor_name
       FROM settlement_lines sl
       LEFT JOIN contributors c ON c.id = sl.contributor_id
       WHERE sl.settlement_id = ?
       ORDER BY sl.id ASC`
    )
    .all(settlementId) as any[];

  const header: SettlementExportHeader = {
    settlementId: sRow.id,
    builderAddress: sRow.builder_address,
    builderLabel: sRow.builder_label,
    periodStart: sRow.period_start,
    periodEnd: sRow.period_end,
    splitRuleVersion: sRow.split_rule_version,
    status: sRow.status,
    totalFeeMicroUsd: BigInt(sRow.total_fee_micro_usd),
    lockedAt: sRow.locked_at
  };

  const lines: SettlementExportLine[] = lineRows.map(l => ({
    contributorId: l.contributor_id,
    contributorName: l.contributor_name,
    amountMicroUsd: BigInt(l.amount_micro_usd),
    payoutChain: l.payout_chain,
    payoutAddress: l.payout_address
  }));

  return { header, lines };
}
