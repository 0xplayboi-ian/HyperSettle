/**
 * Hyperliquid HyperCore REST /info Client with Weight-Based Rate Limiter
 *
 * Protocol parameters (per SPEC.md):
 * - Endpoint: POST https://api.hyperliquid.xyz/info
 * - Budget: 1,200 weight points per minute per IP
 * - Standard /info request weight: 2 points (~600 req/min sustained)
 * - Consensus finality: HyperBFT (~0.2s deterministic finality; 2-3s safe polling lag)
 */

import type { RawHyperCoreFill } from './hypercore';

export const HYPERLIQUID_INFO_URL =
  process.env.HYPERLIQUID_INFO_URL || 'https://api.hyperliquid.xyz/info';

export const DEFAULT_WEIGHT_BUDGET_PER_MIN = 1200;
export const STANDARD_INFO_WEIGHT = 2;

export interface HyperliquidReferralResponse {
  referredBy?: unknown;
  cumVlm?: string;
  unclaimedRewards?: string;
  claimedRewards?: string;
  builderRewards?: string;
  referrerState?: {
    stage?: string;
    data?: {
      nUsers?: number;
      referralCode?: string;
      cumVlm?: string;
      cumReward?: string;
    };
  };
}

export interface TokenBucketOptions {
  capacity?: number;
  refillPerMs?: number;
  nowFn?: () => number;
}

/**
 * Weight-aware Token Bucket enforcing Hyperliquid's 1,200 weight/minute IP limit.
 */
export class WeightRateLimiter {
  private tokens: number;
  private lastRefillMs: number;
  readonly capacity: number;
  readonly refillPerMs: number;
  private readonly nowFn: () => number;

  constructor(options: TokenBucketOptions = {}) {
    this.capacity = options.capacity ?? DEFAULT_WEIGHT_BUDGET_PER_MIN;
    this.refillPerMs = options.refillPerMs ?? this.capacity / 60_000;
    this.nowFn = options.nowFn ?? (() => Date.now());
    this.tokens = this.capacity;
    this.lastRefillMs = this.nowFn();
  }

  private refill(): void {
    const now = this.nowFn();
    const elapsed = Math.max(0, now - this.lastRefillMs);
    this.tokens = Math.min(this.capacity, this.tokens + elapsed * this.refillPerMs);
    this.lastRefillMs = now;
  }

  availableWeight(): number {
    this.refill();
    return Math.floor(this.tokens);
  }

  /**
   * Reserve weight immediately if sufficient tokens remain; returns delay ms otherwise.
   */
  tryConsume(weight: number = STANDARD_INFO_WEIGHT): { allowed: boolean; waitMs: number } {
    this.refill();
    if (this.tokens >= weight) {
      this.tokens -= weight;
      return { allowed: true, waitMs: 0 };
    }
    const deficit = weight - this.tokens;
    const waitMs = Math.ceil(deficit / this.refillPerMs);
    return { allowed: false, waitMs };
  }

  async acquire(weight: number = STANDARD_INFO_WEIGHT): Promise<void> {
    const check = this.tryConsume(weight);
    if (check.allowed) return;
    await new Promise(resolve => setTimeout(resolve, check.waitMs));
    return this.acquire(weight);
  }
}

export interface HyperCoreClientOptions {
  baseUrl?: string;
  timeoutMs?: number;
  maxRetries?: number;
  fetchFn?: typeof fetch;
  rateLimiter?: WeightRateLimiter;
}

export class HyperCoreClient {
  private readonly baseUrl: string;
  private readonly timeoutMs: number;
  private readonly maxRetries: number;
  private readonly fetchFn: typeof fetch;
  readonly rateLimiter: WeightRateLimiter;

  constructor(options: HyperCoreClientOptions = {}) {
    this.baseUrl = options.baseUrl ?? HYPERLIQUID_INFO_URL;
    this.timeoutMs = options.timeoutMs ?? 8_000;
    this.maxRetries = options.maxRetries ?? 2;
    this.fetchFn = options.fetchFn ?? fetch;
    this.rateLimiter = options.rateLimiter ?? new WeightRateLimiter();
  }

  private async postInfo<T>(payload: Record<string, unknown>, weight: number = STANDARD_INFO_WEIGHT): Promise<T> {
    let lastError: Error | null = null;

    for (let attempt = 0; attempt <= this.maxRetries; attempt++) {
      await this.rateLimiter.acquire(weight);
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), this.timeoutMs);

      try {
        const res = await this.fetchFn(this.baseUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
          signal: controller.signal
        });

        clearTimeout(timer);

        if (res.status === 429 && attempt < this.maxRetries) {
          const backoffMs = 250 * 2 ** attempt;
          await new Promise(r => setTimeout(r, backoffMs));
          continue;
        }

        if (!res.ok) {
          const errText = await res.text().catch(() => '');
          throw new Error(`HyperCore /info error HTTP ${res.status}: ${errText || res.statusText}`);
        }

        return (await res.json()) as T;
      } catch (err) {
        clearTimeout(timer);
        lastError = err instanceof Error ? err : new Error(String(err));
        if (attempt === this.maxRetries) {
          break;
        }
      }
    }

    throw lastError ?? new Error('HyperCore /info request failed');
  }

  /**
   * Query Hyperliquid /info `{ type: "referral", user }` for claimed/unclaimed builderRewards.
   */
  async fetchBuilderReferralState(builderAddress: string): Promise<HyperliquidReferralResponse> {
    return this.postInfo<HyperliquidReferralResponse>({
      type: 'referral',
      user: builderAddress
    });
  }

  /**
   * Query Hyperliquid /info `{ type: "userFillsByTime" }` inside bounded HyperBFT finality windows.
   */
  async fetchUserFillsByTime(
    userAddress: string,
    startTimeMs: number,
    endTimeMs?: number
  ): Promise<RawHyperCoreFill[]> {
    const body: Record<string, unknown> = {
      type: 'userFillsByTime',
      user: userAddress,
      startTime: startTimeMs
    };
    if (typeof endTimeMs === 'number') {
      body.endTime = endTimeMs;
    }
    return this.postInfo<RawHyperCoreFill[]>(body, 20);
  }
}
