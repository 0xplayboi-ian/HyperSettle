import { describe, it, expect } from 'vitest';
import {
  calculateSplit,
  formatMicroUsd,
  parseUsdToMicro,
  validateSplitConfig,
  type SplitConfig
} from '../src/core/splits';

describe('Deterministic Micro-USD Split Engine', () => {

  describe('USD and Micro-USD Formatter & Parser', () => {
    it('formats integer micro-USD correctly', () => {
      expect(formatMicroUsd(1_000_000n)).toBe('$1.000000');
      expect(formatMicroUsd(500_000n)).toBe('$0.500000');
      expect(formatMicroUsd(1n)).toBe('$0.000001');
      expect(formatMicroUsd(0n)).toBe('$0.000000');
      expect(formatMicroUsd(123_456_789n)).toBe('$123.456789');
    });

    it('parses USD string to micro-USD integer', () => {
      expect(parseUsdToMicro('1.00')).toBe(1_000_000n);
      expect(parseUsdToMicro('$1.50')).toBe(1_500_000n);
      expect(parseUsdToMicro('0.000001')).toBe(1n);
      expect(parseUsdToMicro('125.45')).toBe(125_450_000n);
    });
  });

  describe('Config Validation', () => {
    it('passes when percentage bps equals 10,000', () => {
      const config: SplitConfig = {
        type: 'percent',
        recipients: [
          { contributorId: 'alice', bps: 6000 },
          { contributorId: 'bob', bps: 4000 }
        ]
      };
      expect(validateSplitConfig(config).valid).toBe(true);
    });

    it('rejects percentage config when bps sum is not 10,000', () => {
      const config: SplitConfig = {
        type: 'percent',
        recipients: [
          { contributorId: 'alice', bps: 6000 },
          { contributorId: 'bob', bps: 3999 } // 9999
        ]
      };
      const res = validateSplitConfig(config);
      expect(res.valid).toBe(false);
      expect(res.error).toContain('must total exactly 10,000 bps');
    });
  });

  describe('Percentage Splits & Deterministic Rounding', () => {
    it('splits evenly when divisibility is exact', () => {
      const config: SplitConfig = {
        type: 'percent',
        recipients: [
          { contributorId: 'alice', bps: 5000 },
          { contributorId: 'bob', bps: 5000 }
        ]
      };
      const result = calculateSplit(1_000_000n, config);
      expect(result.invariantPassed).toBe(true);
      expect(result.residueAllocatedMicroUsd).toBe(0n);
      expect(result.lines[0].amountMicroUsd).toBe(500_000n);
      expect(result.lines[1].amountMicroUsd).toBe(500_000n);
    });

    it('allocates rounding residue to the largest recipient', () => {
      // Total 100 micro-USD split 70% / 30% -> raw: 70 and 30, no residue
      // What about total 101 micro-USD:
      // 70% of 101 = 70.7 -> truncated to 70
      // 30% of 101 = 30.3 -> truncated to 30
      // Sum = 100, Residue = 1 micro-USD
      // Largest recipient is alice (70 > 30), so alice gets +1 = 71
      const config: SplitConfig = {
        type: 'percent',
        recipients: [
          { contributorId: 'alice', bps: 7000 },
          { contributorId: 'bob', bps: 3000 }
        ]
      };
      const result = calculateSplit(101n, config);
      expect(result.invariantPassed).toBe(true);
      expect(result.residueAllocatedMicroUsd).toBe(1n);
      expect(result.residueRecipientId).toBe('alice');
      expect(result.lines.find(l => l.contributorId === 'alice')?.amountMicroUsd).toBe(71n);
      expect(result.lines.find(l => l.contributorId === 'bob')?.amountMicroUsd).toBe(30n);
      expect(result.lines.reduce((s, l) => s + l.amountMicroUsd, 0n)).toBe(101n);
    });

    it('breaks ties using lexicographically smaller contributor ID', () => {
      // 3 equal partners with 3333 bps + 3333 bps + 3334 bps on 100 micro-USD
      // Raw:
      // alice (3333 bps): 100 * 3333 / 10000 = 33
      // bob   (3333 bps): 100 * 3333 / 10000 = 33
      // carol (3334 bps): 100 * 3334 / 10000 = 33
      // All three have amount = 33. Total = 99, Residue = 1.
      // Tie breaker among [alice, bob, carol] -> 'alice' is lexicographically first.
      const config: SplitConfig = {
        type: 'percent',
        recipients: [
          { contributorId: 'carol', bps: 3334 },
          { contributorId: 'bob', bps: 3333 },
          { contributorId: 'alice', bps: 3333 }
        ]
      };
      const result = calculateSplit(100n, config);
      expect(result.invariantPassed).toBe(true);
      expect(result.residueAllocatedMicroUsd).toBe(1n);
      expect(result.residueRecipientId).toBe('alice');
      expect(result.lines.find(l => l.contributorId === 'alice')?.amountMicroUsd).toBe(34n);
      expect(result.lines.find(l => l.contributorId === 'bob')?.amountMicroUsd).toBe(33n);
      expect(result.lines.find(l => l.contributorId === 'carol')?.amountMicroUsd).toBe(33n);
      expect(result.lines.reduce((s, l) => s + l.amountMicroUsd, 0n)).toBe(100n);
    });

    it('handles zero revenue period cleanly', () => {
      const config: SplitConfig = {
        type: 'percent',
        recipients: [
          { contributorId: 'alice', bps: 6000 },
          { contributorId: 'bob', bps: 4000 }
        ]
      };
      const result = calculateSplit(0n, config);
      expect(result.invariantPassed).toBe(true);
      expect(result.lines[0].amountMicroUsd).toBe(0n);
      expect(result.lines[1].amountMicroUsd).toBe(0n);
    });
  });

  describe('Fixed Quota Splits with Spillover', () => {
    it('allocates fixed quotas and sends surplus to spillover treasury', () => {
      const config: SplitConfig = {
        type: 'fixed_per_period',
        fixedRecipients: [
          { contributorId: 'dev_lead', amountMicroUsd: 2_000_000n }, // $2.00
          { contributorId: 'mod_ops', amountMicroUsd: 1_000_000n }   // $1.00
        ],
        spilloverRecipientId: 'treasury'
      };
      // Total earned: $5.00 (5_000_000 micro-USD)
      const result = calculateSplit(5_000_000n, config);
      expect(result.invariantPassed).toBe(true);
      expect(result.lines.find(l => l.contributorId === 'dev_lead')?.amountMicroUsd).toBe(2_000_000n);
      expect(result.lines.find(l => l.contributorId === 'mod_ops')?.amountMicroUsd).toBe(1_000_000n);
      expect(result.lines.find(l => l.contributorId === 'treasury')?.amountMicroUsd).toBe(2_000_000n);
    });

    it('prorates fixed quotas during an under-run period', () => {
      const config: SplitConfig = {
        type: 'fixed_per_period',
        fixedRecipients: [
          { contributorId: 'dev_lead', amountMicroUsd: 2_000_000n }, // 66.67%
          { contributorId: 'mod_ops', amountMicroUsd: 1_000_000n }   // 33.33%
        ],
        spilloverRecipientId: 'treasury'
      };
      // Total earned: only $1.50 (1_500_000 micro-USD)
      const result = calculateSplit(1_500_000n, config);
      expect(result.invariantPassed).toBe(true);
      const total = result.lines.reduce((s, l) => s + l.amountMicroUsd, 0n);
      expect(total).toBe(1_500_000n);
      // dev_lead gets 2/3 of 1.50 = 1.00
      expect(result.lines.find(l => l.contributorId === 'dev_lead')?.amountMicroUsd).toBe(1_000_000n);
      // mod_ops gets 1/3 of 1.50 = 0.50
      expect(result.lines.find(l => l.contributorId === 'mod_ops')?.amountMicroUsd).toBe(500_000n);
    });
  });

  describe('Invariant Property-Based Testing (1,000 Iterations)', () => {
    it('guarantees SUM(lines) === total across 1,000 randomized micro-USD amounts', () => {
      const syndicates: SplitConfig[] = [
        {
          type: 'percent',
          recipients: [
            { contributorId: 'alice', bps: 5000 },
            { contributorId: 'bob', bps: 5000 }
          ]
        },
        {
          type: 'percent',
          recipients: [
            { contributorId: 'core_team', bps: 6000 },
            { contributorId: 'marketing', bps: 2500 },
            { contributorId: 'liquidity', bps: 1500 }
          ]
        },
        {
          type: 'percent',
          recipients: [
            { contributorId: 'member_01', bps: 1428 },
            { contributorId: 'member_02', bps: 1428 },
            { contributorId: 'member_03', bps: 1428 },
            { contributorId: 'member_04', bps: 1428 },
            { contributorId: 'member_05', bps: 1428 },
            { contributorId: 'member_06', bps: 1428 },
            { contributorId: 'member_07', bps: 1432 } // sums to 10,000
          ]
        }
      ];

      for (let i = 1; i <= 1000; i++) {
        // Pseudo-random micro-USD amounts from 1 micro-USD to $50,000.00
        const randomAmount = BigInt(Math.floor(Math.random() * 50_000_000_000) + 1);
        const config = syndicates[i % syndicates.length];

        const result = calculateSplit(randomAmount, config);
        expect(result.invariantPassed).toBe(true);

        const sum = result.lines.reduce((s, l) => s + l.amountMicroUsd, 0n);
        expect(sum).toBe(randomAmount);
      }
    });
  });

});
