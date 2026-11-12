import { describe, it, expect } from 'vitest';
import {
  SOLANA_USDC_MINT,
  generateAuditSettlementCsv,
  generateSquadsBatchCsv,
  isValidSolanaAddress,
  sanitizeCsvCell,
  type SettlementExportHeader,
  type SettlementExportLine
} from '../src/export/squads';

describe('Squads V4 & Audit CSV Exporters', () => {
  const ADDR_ALICE = '7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU';
  const ADDR_BOB = '9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM';

  it('validates Solana Base58 addresses accurately', () => {
    expect(isValidSolanaAddress(SOLANA_USDC_MINT)).toBe(true);
    expect(isValidSolanaAddress(ADDR_ALICE)).toBe(true);
    expect(isValidSolanaAddress('0x742d35cc6634c0532925a3b844bc454e4438f44e')).toBe(false);
    expect(isValidSolanaAddress('short')).toBe(false);
    expect(isValidSolanaAddress('0OIl' + '1'.repeat(35))).toBe(false);
  });

  it('sanitizes spreadsheet formula injection and RFC 4180 characters', () => {
    expect(sanitizeCsvCell('=CMD("calc")')).toBe(`"'=CMD(""calc"")"`);
    expect(sanitizeCsvCell('+100')).toBe("'+100");
    expect(sanitizeCsvCell('-50')).toBe("'-50");
    expect(sanitizeCsvCell('@SUM(A1:A2)')).toBe("'@SUM(A1:A2)");
    expect(sanitizeCsvCell('Alice, Ops')).toBe('"Alice, Ops"');
    expect(sanitizeCsvCell(1_250_000n)).toBe('1250000');
  });

  it('exports Squads V4 CSV consolidating duplicate receivers and skipping EVM/zero rows', () => {
    const lines: SettlementExportLine[] = [
      {
        contributorId: 'c_bob_1',
        contributorName: 'Bob Ops',
        amountMicroUsd: 1_500_000n,
        payoutChain: 'solana',
        payoutAddress: ADDR_BOB
      },
      {
        contributorId: 'c_alice',
        contributorName: 'Alice Founder',
        amountMicroUsd: 2_000_001n,
        payoutChain: 'solana',
        payoutAddress: ADDR_ALICE
      },
      {
        contributorId: 'c_bob_2',
        contributorName: 'Bob Bonus',
        amountMicroUsd: 500_000n,
        payoutChain: 'solana',
        payoutAddress: ADDR_BOB
      },
      {
        contributorId: 'c_evm',
        contributorName: 'EVM Treasury',
        amountMicroUsd: 3_000_000n,
        payoutChain: 'evm',
        payoutAddress: '0x1111111111111111111111111111111111111111'
      },
      {
        contributorId: 'c_zero',
        contributorName: 'Zero Quota',
        amountMicroUsd: 0n,
        payoutChain: 'solana',
        payoutAddress: ADDR_ALICE
      }
    ];

    const res = generateSquadsBatchCsv(lines);
    expect(res.mintAddress).toBe(SOLANA_USDC_MINT);
    expect(res.transferCount).toBe(2);
    expect(res.totalTransferMicroUsd).toBe(4_000_001n);
    expect(res.totalTransferUsdc).toBe('4.000001');
    expect(res.skippedNonSolanaCount).toBe(1);
    expect(res.skippedZeroAmountCount).toBe(1);

    const csvLines = res.csv.trim().split('\n');
    expect(csvLines[0]).toBe('token_address,receiver,amount');
    expect(csvLines[1]).toBe(`${SOLANA_USDC_MINT},${ADDR_ALICE},2.000001`);
    expect(csvLines[2]).toBe(`${SOLANA_USDC_MINT},${ADDR_BOB},2`);
  });

  it('rejects invalid Base58 Solana addresses during Squads export', () => {
    expect(() =>
      generateSquadsBatchCsv([
        {
          contributorId: 'bad_wallet',
          contributorName: 'Bad',
          amountMicroUsd: 100n,
          payoutChain: 'solana',
          payoutAddress: 'not-base58-0x123'
        }
      ])
    ).toThrow(/Invalid Solana Base58/);
  });

  it('generates full FinOps audit CSV with micro-USD precision and deterministic sorting', () => {
    const header: SettlementExportHeader = {
      settlementId: 7,
      builderAddress: '0xbuilder11111111111111111111111111111111',
      builderLabel: '=HyperTest',
      periodStart: '2026-10-01T00:00:00.000Z',
      periodEnd: '2026-10-31T23:59:59.999Z',
      splitRuleVersion: 2,
      status: 'final',
      totalFeeMicroUsd: 10_000_000n,
      lockedAt: '2026-11-01T00:00:00Z'
    };

    const lines: SettlementExportLine[] = [
      {
        contributorId: 'c_small',
        contributorName: 'Small',
        amountMicroUsd: 2_500_000n,
        payoutChain: 'evm',
        payoutAddress: '0x2222222222222222222222222222222222222222'
      },
      {
        contributorId: 'c_large',
        contributorName: 'Large',
        amountMicroUsd: 7_500_000n,
        payoutChain: 'solana',
        payoutAddress: ADDR_ALICE
      }
    ];

    const csv = generateAuditSettlementCsv(header, lines);
    const rows = csv.trim().split('\n');
    expect(rows).toHaveLength(3);
    expect(rows[0]).toContain('settlement_id,status,builder_code,builder_label');
    expect(rows[1]).toContain("'=HyperTest");
    expect(rows[1]).toContain(',c_large,Large,solana,');
    expect(rows[1]).toContain(',7500000,7.5,75.0000');
    expect(rows[2]).toContain(',c_small,Small,evm,');
    expect(rows[2]).toContain(',2500000,2.5,25.0000');
  });
});
