import { NextResponse } from 'next/server';

/**
 * Recursively convert BigInt values to strings for JSON serialization.
 */
export function serializeBigInts<T>(value: T): unknown {
  if (typeof value === 'bigint') {
    return value.toString();
  }
  if (Array.isArray(value)) {
    return value.map(item => serializeBigInts(item));
  }
  if (value !== null && typeof value === 'object') {
    const out: Record<string, unknown> = {};
    for (const [k, v] of Object.entries(value)) {
      out[k] = serializeBigInts(v);
    }
    return out;
  }
  return value;
}

export function jsonOk<T>(data: T, status: number = 200): NextResponse {
  return NextResponse.json(serializeBigInts(data), { status });
}

export function jsonError(err: unknown, defaultStatus: number = 400): NextResponse {
  const message = err instanceof Error ? err.message : String(err);
  const lower = message.toLowerCase();

  let status = defaultStatus;
  if (lower.includes('not found') || lower.includes('unknown builder code')) {
    status = 404;
  } else if (lower.includes('overlaps') || lower.includes('unique constraint')) {
    status = 409;
  } else if (lower.includes('hypercore /info error')) {
    status = 502;
  }

  return NextResponse.json({ error: message }, { status });
}

export function normalizeDateBound(value: string | null, endOfDay: boolean = false): string | null {
  if (!value) return null;
  const trimmed = value.trim();
  if (!trimmed) return null;
  if (/^\d{4}-\d{2}-\d{2}$/.test(trimmed)) {
    return endOfDay ? `${trimmed}T23:59:59.999Z` : `${trimmed}T00:00:00.000Z`;
  }
  return trimmed;
}

export async function readJsonBody<T = Record<string, unknown>>(request: Request): Promise<T> {
  try {
    const body = await request.json();
    if (!body || typeof body !== 'object' || Array.isArray(body)) {
      throw new Error('Request body must be a JSON object');
    }
    return body as T;
  } catch (err) {
    if (err instanceof Error && err.message === 'Request body must be a JSON object') {
      throw err;
    }
    throw new Error('Invalid JSON request body');
  }
}
