/**
 * HyperSettle Settlement CSV & Solana Squads V4 Batch Transfer Exporter
 *
 * Non-custodial payout formatting for:
 * 1. Squads V4 Multisig Batch Transfer CSV (`token_address,receiver,amount`)
 *    targeting Solana Mainnet SPL USDC (`EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v`).
 * 2. Standard FinOps Audit CSV with micro-USD integer precision and wallet provenance.
 */

import { microUsdToDecimal } from '../core/splits';

export const SOLANA_USDC_MINT = 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v';

const BASE58_REGEX = /^[1-9A-HJ-NP-Za-km-z]{32,44}$/;

export interface SettlementExportLine {
  contributorId: string;
  contributorName: string;
  amountMicroUsd: bigint;
  payoutChain: 'solana' | 'evm';
  payoutAddress: string;
}

export interface SettlementExportHeader {
  settlementId: number;
  builderAddress: string;
  builderLabel: string;
  periodStart: string;
  periodEnd: string;
  splitRuleVersion: number;
  status: 'draft' | 'final';
  totalFeeMicroUsd: bigint;
  lockedAt: string | null;
}

export interface SquadsExportResult {
  csv: string;
  mintAddress: string;
  transferCount: number;
  totalTransferMicroUsd: bigint;
  totalTransferUsdc: string;
  skippedZeroAmountCount: number;
  skippedNonSolanaCount: number;
}

/**
 * Validate Base58 format for a Solana public key / SPL token account.
 */
export function isValidSolanaAddress(address: string): boolean {
  return typeof address === 'string' && BASE58_REGEX.test(address.trim());
}

/**
 * Neutralize spreadsheet formula injection (=, +, -, @, tab, CR) and quote RFC 4180 CSV cells.
 */
export function sanitizeCsvCell(value: string | number | bigint): string {
  let str = typeof value === 'bigint' ? value.toString() : String(value ?? '');
  if (/^[=+\-@\t\r]/.test(str)) {
    str = `'${str}`;
  }
  if (/[",\n\r]/.test(str)) {
    return `"${str.replace(/"/g, '""')}"`;
  }
  return str;
}

/**
 * Export Solana Squads V4 Multisig Batch Transfer CSV (`token_address,receiver,amount`).
 * Consolidates duplicate receiver addresses deterministically in ascending Base58 order
 * and excludes zero-value SPL transfers.
 */
export function generateSquadsBatchCsv(
  lines: SettlementExportLine[],
  options: { mintAddress?: string; validateAddresses?: boolean } = {}
): SquadsExportResult {
  const mintAddress = options.mintAddress ?? SOLANA_USDC_MINT;
  const validateAddresses = options.validateAddresses ?? true;

  if (validateAddresses && !isValidSolanaAddress(mintAddress)) {
    throw new Error(`Invalid Solana SPL token mint address: ${mintAddress}`);
  }

  let skippedZeroAmountCount = 0;
  let skippedNonSolanaCount = 0;

  // Consolidate payouts per unique Solana receiver so Squads executes 1 instruction per wallet
  const consolidated = new Map<string, bigint>();

  for (const line of lines) {
    if (line.payoutChain !== 'solana') {
      skippedNonSolanaCount++;
      continue;
    }
    if (line.amountMicroUsd <= 0n) {
      skippedZeroAmountCount++;
      continue;
    }

    const receiver = line.payoutAddress.trim();
    if (validateAddresses && !isValidSolanaAddress(receiver)) {
      throw new Error(
        `Invalid Solana Base58 payout address for contributor "${line.contributorId}": ${line.payoutAddress}`
      );
    }

    consolidated.set(receiver, (consolidated.get(receiver) ?? 0n) + line.amountMicroUsd);
  }

  const sortedReceivers = Array.from(consolidated.entries()).sort(([a], [b]) =>
    a.localeCompare(b)
  );

  const rows: string[] = ['token_address,receiver,amount'];
  let totalTransferMicroUsd = 0n;

  for (const [receiver, amountMicro] of sortedReceivers) {
    const decimalUsdc = microUsdToDecimal(amountMicro);
    rows.push(`${sanitizeCsvCell(mintAddress)},${sanitizeCsvCell(receiver)},${decimalUsdc}`);
    totalTransferMicroUsd += amountMicro;
  }

  return {
    csv: rows.join('\n') + '\n',
    mintAddress,
    transferCount: sortedReceivers.length,
    totalTransferMicroUsd,
    totalTransferUsdc: microUsdToDecimal(totalTransferMicroUsd),
    skippedZeroAmountCount,
    skippedNonSolanaCount
  };
}

/**
 * Export full auditable settlement breakdown CSV with both micro-USD integers and decimal USDC.
 */
export function generateAuditSettlementCsv(
  header: SettlementExportHeader,
  lines: SettlementExportLine[]
): string {
  const columns = [
    'settlement_id',
    'status',
    'builder_code',
    'builder_label',
    'period_start',
    'period_end',
    'split_rule_version',
    'locked_at',
    'contributor_id',
    'contributor_name',
    'payout_chain',
    'payout_address',
    'amount_micro_usd',
    'amount_usdc',
    'share_pct'
  ];

  const sortedLines = [...lines].sort((a, b) => {
    if (b.amountMicroUsd !== a.amountMicroUsd) {
      return b.amountMicroUsd > a.amountMicroUsd ? 1 : -1;
    }
    return a.contributorId.localeCompare(b.contributorId);
  });

  const rows: string[] = [columns.join(',')];

  for (const line of sortedLines) {
    const sharePct =
      header.totalFeeMicroUsd > 0n
        ? (Number((line.amountMicroUsd * 1_000_000n) / header.totalFeeMicroUsd) / 10_000).toFixed(4)
        : '0.0000';

    const row = [
      header.settlementId,
      header.status,
      header.builderAddress,
      header.builderLabel,
      header.periodStart,
      header.periodEnd,
      header.splitRuleVersion,
      header.lockedAt ?? '',
      line.contributorId,
      line.contributorName,
      line.payoutChain,
      line.payoutAddress,
      line.amountMicroUsd,
      microUsdToDecimal(line.amountMicroUsd),
      sharePct
    ].map(sanitizeCsvCell);

    rows.push(row.join(','));
  }

  return rows.join('\n') + '\n';
}
