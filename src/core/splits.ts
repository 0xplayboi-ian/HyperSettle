/**
 * HyperSettle Deterministic Micro-USD Split Engine
 * 
 * Strict FinOps rules:
 * 1. Zero floating-point arithmetic for accounting calculations.
 * 2. All currency represented in integer micro-USD (10^-6, matching native USDC 6 decimals).
 *    e.g. 1 USDC = 1,000,000 micro-USD.
 * 3. Rounding residue allocated deterministically to the largest recipient.
 *    Tie-breaker: Lexicographically smaller contributor ID.
 * 4. Invariant: SUM(lines.amountMicroUsd) === totalFeeMicroUsd.
 */

export interface Contributor {
  id: string;
  name: string;
  walletSolana?: string;
  walletEvm?: string;
}

export interface PercentRecipient {
  contributorId: string;
  bps: number; // Basis points: 10,000 bps = 100.00%, 1 bp = 0.01%
}

export interface FixedRecipient {
  contributorId: string;
  amountMicroUsd: bigint;
}

export interface PercentSplitConfig {
  type: 'percent';
  recipients: PercentRecipient[];
}

export interface FixedSplitConfig {
  type: 'fixed_per_period';
  fixedRecipients: FixedRecipient[];
  spilloverRecipientId: string; // Treasury / DAO reserve getting remainder
}

export type SplitConfig = PercentSplitConfig | FixedSplitConfig;

export interface SettlementLine {
  contributorId: string;
  amountMicroUsd: bigint;
  bpsCalculated: number; // Actual basis points of total received
  formattedUsd: string;
}

export interface SplitResult {
  totalFeeMicroUsd: bigint;
  lines: SettlementLine[];
  residueAllocatedMicroUsd: bigint;
  residueRecipientId?: string;
  invariantPassed: boolean;
}

/**
 * Format integer micro-USD into human-readable USD string
 * e.g. 1500000n -> "$1.500000", or "$1.50" with trimZeroes
 */
export function formatMicroUsd(amount: bigint, decimals: number = 6): string {
  const isNegative = amount < 0n;
  const absAmount = isNegative ? -amount : amount;
  const divisor = 1_000_000n;
  const whole = absAmount / divisor;
  const fraction = absAmount % divisor;
  
  const fractionStr = fraction.toString().padStart(6, '0').slice(0, decimals);
  const sign = isNegative ? '-' : '';
  return `${sign}$${whole.toLocaleString('en-US')}.${fractionStr}`;
}

/**
 * Parse USD decimal string to integer micro-USD
 * e.g. "1.50" -> 1500000n, "0.000001" -> 1n
 */
export function parseUsdToMicro(usdStr: string): bigint {
  const clean = usdStr.trim().replace(/^\$/, '');
  const [wholeStr, fracStr = ''] = clean.split('.');
  const whole = BigInt(wholeStr || '0');
  const fracPadded = (fracStr + '000000').slice(0, 6);
  const frac = BigInt(fracPadded);
  return whole * 1_000_000n + frac;
}

/**
 * Validate that PercentSplitConfig adds up to 10,000 basis points (100.00%)
 */
export function validateSplitConfig(config: SplitConfig): { valid: boolean; error?: string } {
  if (config.type === 'percent') {
    if (!config.recipients || config.recipients.length === 0) {
      return { valid: false, error: 'Percent rule must have at least one recipient' };
    }
    const totalBps = config.recipients.reduce((sum, r) => sum + r.bps, 0);
    if (totalBps !== 10_000) {
      return { valid: false, error: `Percent split basis points must total exactly 10,000 bps (got ${totalBps})` };
    }
    return { valid: true };
  } else if (config.type === 'fixed_per_period') {
    if (!config.fixedRecipients || config.fixedRecipients.length === 0) {
      return { valid: false, error: 'Fixed rule must have at least one recipient' };
    }
    if (!config.spilloverRecipientId) {
      return { valid: false, error: 'Fixed rule requires a spillover/treasury recipient ID' };
    }
    return { valid: true };
  }
  return { valid: false, error: 'Unknown split rule type' };
}

/**
 * Calculate deterministic revenue split for a given period total
 */
export function calculateSplit(totalFeeMicroUsd: bigint, config: SplitConfig): SplitResult {
  if (totalFeeMicroUsd < 0n) {
    throw new Error(`Total fee cannot be negative (got ${totalFeeMicroUsd})`);
  }

  const validation = validateSplitConfig(config);
  if (!validation.valid) {
    throw new Error(validation.error);
  }

  // Edge case: Zero revenue period
  if (totalFeeMicroUsd === 0n) {
    const zeroLines: SettlementLine[] = (config.type === 'percent'
      ? config.recipients.map(r => ({
          contributorId: r.contributorId,
          amountMicroUsd: 0n,
          bpsCalculated: r.bps,
          formattedUsd: '$0.000000'
        }))
      : config.fixedRecipients.map(r => ({
          contributorId: r.contributorId,
          amountMicroUsd: 0n,
          bpsCalculated: 0,
          formattedUsd: '$0.000000'
        }))
    );
    return {
      totalFeeMicroUsd: 0n,
      lines: zeroLines,
      residueAllocatedMicroUsd: 0n,
      invariantPassed: true
    };
  }

  if (config.type === 'percent') {
    return calculatePercentSplit(totalFeeMicroUsd, config);
  } else {
    return calculateFixedSplit(totalFeeMicroUsd, config);
  }
}

/**
 * Execute Percentage-based Split with Deterministic Rounding Allocation
 */
function calculatePercentSplit(totalFee: bigint, config: PercentSplitConfig): SplitResult {
  const rawLines: { contributorId: string; amount: bigint; bps: number }[] = [];
  let allocatedSum = 0n;

  // 1. Compute truncated integer amounts
  for (const recipient of config.recipients) {
    const rawAmount = (totalFee * BigInt(recipient.bps)) / 10_000n;
    rawLines.push({
      contributorId: recipient.contributorId,
      amount: rawAmount,
      bps: recipient.bps
    });
    allocatedSum += rawAmount;
  }

  // 2. Compute rounding residue
  const residue = totalFee - allocatedSum;
  let residueRecipientId: string | undefined;

  // 3. Allocate residue to largest recipient (tie-breaker: lexicographical contributor ID)
  if (residue > 0n) {
    // Sort copy to find primary recipient
    const sorted = [...rawLines].sort((a, b) => {
      if (b.amount !== a.amount) {
        return b.amount > a.amount ? 1 : -1;
      }
      return a.contributorId.localeCompare(b.contributorId);
    });

    residueRecipientId = sorted[0].contributorId;
    const targetIdx = rawLines.findIndex(l => l.contributorId === residueRecipientId);
    rawLines[targetIdx].amount += residue;
  }

  // 4. Construct final settlement lines
  const lines: SettlementLine[] = rawLines.map(l => {
    const actualBps = totalFee > 0n ? Number((l.amount * 10_000n) / totalFee) : l.bps;
    return {
      contributorId: l.contributorId,
      amountMicroUsd: l.amount,
      bpsCalculated: actualBps,
      formattedUsd: formatMicroUsd(l.amount)
    };
  });

  // 5. Invariant check
  const totalAllocated = lines.reduce((sum, l) => sum + l.amountMicroUsd, 0n);
  const invariantPassed = totalAllocated === totalFee;

  return {
    totalFeeMicroUsd: totalFee,
    lines,
    residueAllocatedMicroUsd: residue,
    residueRecipientId,
    invariantPassed
  };
}

/**
 * Execute Fixed Quota Split with Spillover/Treasury Fallback
 */
function calculateFixedSplit(totalFee: bigint, config: FixedSplitConfig): SplitResult {
  const fixedTotal = config.fixedRecipients.reduce((sum, r) => sum + r.amountMicroUsd, 0n);

  if (totalFee >= fixedTotal) {
    // Normal case: Full fixed quotas satisfied, surplus goes to spillover / treasury
    const spilloverAmount = totalFee - fixedTotal;
    const lines: SettlementLine[] = config.fixedRecipients.map(r => ({
      contributorId: r.contributorId,
      amountMicroUsd: r.amountMicroUsd,
      bpsCalculated: Number((r.amountMicroUsd * 10_000n) / totalFee),
      formattedUsd: formatMicroUsd(r.amountMicroUsd)
    }));

    if (spilloverAmount > 0n || !lines.some(l => l.contributorId === config.spilloverRecipientId)) {
      lines.push({
        contributorId: config.spilloverRecipientId,
        amountMicroUsd: spilloverAmount,
        bpsCalculated: Number((spilloverAmount * 10_000n) / totalFee),
        formattedUsd: formatMicroUsd(spilloverAmount)
      });
    }

    const totalAllocated = lines.reduce((sum, l) => sum + l.amountMicroUsd, 0n);
    return {
      totalFeeMicroUsd: totalFee,
      lines,
      residueAllocatedMicroUsd: 0n,
      invariantPassed: totalAllocated === totalFee
    };
  } else {
    // Under-run case: Total earned was less than sum of fixed quotas.
    // Prorate fixed quotas proportionally with deterministic residue allocation.
    const rawLines: { contributorId: string; amount: bigint }[] = [];
    let allocatedSum = 0n;

    for (const recipient of config.fixedRecipients) {
      const rawAmount = (totalFee * recipient.amountMicroUsd) / fixedTotal;
      rawLines.push({
        contributorId: recipient.contributorId,
        amount: rawAmount
      });
      allocatedSum += rawAmount;
    }

    const residue = totalFee - allocatedSum;
    let residueRecipientId: string | undefined;

    if (residue > 0n) {
      const sorted = [...rawLines].sort((a, b) => {
        if (b.amount !== a.amount) {
          return b.amount > a.amount ? 1 : -1;
        }
        return a.contributorId.localeCompare(b.contributorId);
      });

      residueRecipientId = sorted[0].contributorId;
      const targetIdx = rawLines.findIndex(l => l.contributorId === residueRecipientId);
      rawLines[targetIdx].amount += residue;
    }

    const lines: SettlementLine[] = rawLines.map(l => {
      const actualBps = totalFee > 0n ? Number((l.amount * 10_000n) / totalFee) : 0;
      return {
        contributorId: l.contributorId,
        amountMicroUsd: l.amount,
        bpsCalculated: actualBps,
        formattedUsd: formatMicroUsd(l.amount)
      };
    });

    const totalAllocated = lines.reduce((sum, l) => sum + l.amountMicroUsd, 0n);
    return {
      totalFeeMicroUsd: totalFee,
      lines,
      residueAllocatedMicroUsd: residue,
      residueRecipientId,
      invariantPassed: totalAllocated === totalFee
    };
  }
}
