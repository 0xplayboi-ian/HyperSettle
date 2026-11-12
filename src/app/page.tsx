import Link from 'next/link';

const API_ENDPOINTS = [
  { method: 'GET', path: '/api/health', desc: 'SQLite connectivity and ledger table counts' },
  { method: 'GET', path: '/api/builder-codes', desc: 'List registered Hyperliquid builder codes' },
  { method: 'GET', path: '/api/revenue?group=source', desc: 'Micro-USD revenue summary grouped by source/day/week' },
  { method: 'GET', path: '/api/fee-events?limit=25', desc: 'Cursor-paginated attributed HyperCore fills' },
  { method: 'GET', path: '/api/contributors', desc: 'Payee directory with Solana & EVM payout wallets' },
  { method: 'GET', path: '/api/split-rules', desc: 'Versioned deterministic percent & fixed split configs' },
  { method: 'GET', path: '/api/reconciliation', desc: 'Onchain HyperCore vs local SQLite ledger parity checks' },
  { method: 'GET', path: '/api/settlements', desc: 'Finalized & draft period settlements' },
  { method: 'GET', path: '/api/settlements/1/export.squads.csv', desc: 'Solana Squads V4 SPL USDC batch transfer CSV' },
  { method: 'GET', path: '/api/settlements/1/export.csv', desc: 'Full FinOps audit settlement CSV' }
];

export default function HomePage() {
  return (
    <main className="mx-auto max-w-4xl px-6 py-16">
      <div className="mb-8 inline-flex items-center gap-2 rounded-full border border-[#17302a] bg-[#0a1412] px-3 py-1 text-xs font-medium text-[#00f5d4]">
        <span className="h-2 w-2 rounded-full bg-[#00f5d4]" />
        Step 3 Active · REST API, Reconciliation & Squads V4 Exporter
      </div>

      <h1 className="text-4xl font-semibold tracking-tight text-[#eef6f4]">
        HyperSettle <span className="text-[#00f5d4]">Core Engine</span>
      </h1>
      <p className="mt-3 max-w-2xl text-sm leading-relaxed text-[#8ea9a2]">
        Institutional FinOps ledger for Hyperliquid builder codes. All monetary computations execute
        in integer micro-USD (<code className="text-[#00f5d4]">bigint 1e-6</code>) backed by
        deterministic split math and Solana Squads V4 batch payout exports. Step 4 will layer the
        full Executive FinOps UI onto these routes.
      </p>

      <section className="mt-10 rounded-xl border border-[#17302a] bg-[#0a1412] p-6">
        <h2 className="text-sm font-semibold uppercase tracking-wider text-[#8ea9a2]">
          Live API Endpoints
        </h2>
        <div className="mt-4 divide-y divide-[#17302a]">
          {API_ENDPOINTS.map(ep => (
            <div key={ep.path} className="flex flex-col gap-1 py-3 sm:flex-row sm:items-center sm:justify-between">
              <div className="flex items-center gap-3">
                <span className="rounded bg-[#112621] px-2 py-0.5 font-mono text-xs font-semibold text-[#00f5d4]">
                  {ep.method}
                </span>
                <Link
                  href={ep.path}
                  className="font-mono text-xs text-[#eef6f4] underline decoration-[#17302a] underline-offset-4 hover:text-[#00f5d4]"
                >
                  {ep.path}
                </Link>
              </div>
              <span className="text-xs text-[#8ea9a2]">{ep.desc}</span>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}
