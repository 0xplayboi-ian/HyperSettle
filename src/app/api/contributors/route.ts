import { getDb } from '@/db';
import { createContributor, listContributors } from '@/services/ledger';
import { jsonError, jsonOk, readJsonBody } from '../_utils';

export const dynamic = 'force-dynamic';

export async function GET() {
  try {
    const db = getDb();
    const contributors = listContributors(db);
    return jsonOk({ contributors });
  } catch (err) {
    return jsonError(err, 500);
  }
}

export async function POST(request: Request) {
  try {
    const body = await readJsonBody<{
      id?: string;
      name?: string;
      walletEvm?: string | null;
      wallet_evm?: string | null;
      walletSolana?: string | null;
      wallet_solana?: string | null;
    }>(request);

    if (typeof body.name !== 'string') {
      return jsonError(new Error('Contributor name is required'), 400);
    }

    const db = getDb();
    const created = createContributor(db, {
      id: body.id,
      name: body.name,
      walletEvm: body.walletEvm ?? body.wallet_evm ?? null,
      walletSolana: body.walletSolana ?? body.wallet_solana ?? null
    });
    return jsonOk({ contributor: created }, 201);
  } catch (err) {
    return jsonError(err, 400);
  }
}
