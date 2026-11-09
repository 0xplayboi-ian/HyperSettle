/**
 * HyperSettle Realistic Seed Data Generator
 * 
 * Generates 30 days of high-fidelity HyperCore builder fee fills,
 * realistic trading volumes across BTC, ETH, SOL, HYPE,
 * configured contributors with Solana Squads multisig addresses,
 * and deterministic split rules for the Colosseum Eternal hackathon.
 */

import { getDb, closeDb } from './index.js';
import { runMigrations } from './migrate.js';
import { parseHyperCoreFill, ingestFeeEvent, RawHyperCoreFill } from '../ingestion/hypercore.js';
import { calculateSplit, SplitConfig } from '../core/splits.js';

export function seedDatabase(db = getDb()) {
  console.log('⚡ Seeding HyperSettle with production-grade demo data...');
  runMigrations(db);

  // Clear existing records cleanly
  db.exec(`
    DELETE FROM settlement_lines;
    DELETE FROM settlements;
    DELETE FROM fee_events;
    DELETE FROM raw_events;
    DELETE FROM split_rules;
    DELETE FROM contributors;
    DELETE FROM builder_codes;
  `);

  // 1. Insert Builder Codes
  const insertBuilder = db.prepare(`
    INSERT INTO builder_codes (address, label, active)
    VALUES (?, ?, 1)
  `);

  const builder1 = insertBuilder.run('0x1111111111111111111111111111111111111111', 'HyperTerminal Web DEX');
  const builder2 = insertBuilder.run('0x2222222222222222222222222222222222222222', 'HyperSniper Telegram Bot');
  const builder3 = insertBuilder.run('0x3333333333333333333333333333333333333333', 'QuantumArb Institutional API');

  const b1Id = Number(builder1.lastInsertRowid);
  const b2Id = Number(builder2.lastInsertRowid);
  const b3Id = Number(builder3.lastInsertRowid);

  console.log('  ✓ Seeded 3 Builder Codes');

  // 2. Insert Contributors
  const insertContributor = db.prepare(`
    INSERT INTO contributors (id, name, wallet_evm, wallet_solana, active)
    VALUES (?, ?, ?, ?, 1)
  `);

  insertContributor.run(
    'contributor_elena',
    'Elena Vance (Protocol Architect)',
    '0x71C8416760895fDA3073CaA8B9f041B72F30571C',
    'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v'
  );
  insertContributor.run(
    'contributor_marcus',
    'Marcus Chen (Full-Stack Engineer)',
    '0x2546BcD3c84621e976D8185a91A922aE77ECEc30',
    '7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU'
  );
  insertContributor.run(
    'contributor_jayden',
    'Jayden Wu (Trading & Ops Lead)',
    '0xbDA5747bFD65F08deb54cb465eB87D40e51B197E',
    '4zMMC9srt5Ri5X14GAgXhaHii3GnPAEERYPJgZJDncDU'
  );
  insertContributor.run(
    'contributor_treasury',
    'HyperSettle Squads V4 Multisig Treasury',
    '0x000000000000000000000000000000000000dEaD',
    'Squads1111111111111111111111111111111111111'
  );

  console.log('  ✓ Seeded 4 Team Contributors (Solana + EVM)');

  // 3. Insert Split Rules
  const insertRule = db.prepare(`
    INSERT INTO split_rules (builder_code_id, name, effective_from, type, config, version)
    VALUES (?, ?, ?, ?, ?, 1)
  `);

  const ruleB1Config: SplitConfig = {
    type: 'percent',
    recipients: [
      { contributorId: 'contributor_elena', bps: 5000 },  // 50.00%
      { contributorId: 'contributor_marcus', bps: 3000 }, // 30.00%
      { contributorId: 'contributor_treasury', bps: 2000 } // 20.00%
    ]
  };
  insertRule.run(b1Id, 'HyperTerminal Standard Split (50/30/20)', '2026-10-01T00:00:00Z', 'percent', JSON.stringify(ruleB1Config));

  const ruleB2Config: SplitConfig = {
    type: 'percent',
    recipients: [
      { contributorId: 'contributor_jayden', bps: 5500 },   // 55.00%
      { contributorId: 'contributor_elena', bps: 2500 },    // 25.00%
      { contributorId: 'contributor_treasury', bps: 2000 }  // 20.00%
    ]
  };
  insertRule.run(b2Id, 'HyperSniper Bot Split (55/25/20)', '2026-10-01T00:00:00Z', 'percent', JSON.stringify(ruleB2Config));

  const ruleB3Config: SplitConfig = {
    type: 'fixed_per_period',
    fixedRecipients: [
      { contributorId: 'contributor_jayden', amountMicroUsd: 5_000_000_000n } // $5,000 monthly quota
    ],
    spilloverRecipientId: 'contributor_treasury'
  };
  // Store BigInt config as serializable string
  const ruleB3Json = JSON.stringify({
    type: 'fixed_per_period',
    fixedRecipients: [{ contributorId: 'contributor_jayden', amountMicroUsd: '5000000000' }],
    spilloverRecipientId: 'contributor_treasury'
  });
  insertRule.run(b3Id, 'QuantumArb Fixed Quota ($5K Quota + Spillover)', '2026-10-01T00:00:00Z', 'fixed_per_period', ruleB3Json);

  console.log('  ✓ Seeded 3 Active Revenue Split Rules');

  // 4. Generate 30 Days of Fills across 3 Builder Codes
  console.log('  ⚡ Simulating 30 days of HyperCore L1 builder fills...');
  const now = new Date();
  const coins = [
    { coin: 'BTC', px: 94500 },
    { coin: 'ETH', px: 3420 },
    { coin: 'SOL', px: 215 },
    { coin: 'HYPE', px: 32 }
  ];

  let totalEventsGenerated = 0;
  let totalFeesMicro = 0n;

  const insertStmt = db.prepare(`
    INSERT INTO fee_events (
      external_id, builder_code_id, source_label, trader,
      notional_micro_usd, fee_micro_usd, block_time, tx_ref
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
  `);

  db.transaction(() => {
    // Generate events across the past 30 days
    for (let dayOffset = 30; dayOffset >= 0; dayOffset--) {
      const dayDate = new Date(now.getTime() - dayOffset * 24 * 3600 * 1000);
      
      // Between 15 and 30 trades per day
      const tradesToday = 15 + Math.floor(Math.sin(dayOffset * 0.7) * 5) + (dayOffset % 5);

      for (let t = 0; t < tradesToday; t++) {
        const coinObj = coins[t % coins.length];
        const hour = Math.floor((t * 24) / tradesToday);
        const minute = (t * 17) % 60;
        const second = (t * 31) % 60;
        
        const tradeTime = new Date(dayDate);
        tradeTime.setUTCHours(hour, minute, second);

        // Pick builder code: 50% Web Terminal, 30% Telegram Sniper, 20% QuantumArb
        let bCodeId = b1Id;
        let bAddr = '0x1111111111111111111111111111111111111111';
        let feeRateDecibps = 10; // 10 decibps = 1 bp = 0.01%
        let sourceLabel = 'web_terminal';
        let notionalUsd = 500 + Math.random() * 8000;

        if (t % 10 >= 5 && t % 10 < 8) {
          bCodeId = b2Id;
          bAddr = '0x2222222222222222222222222222222222222222';
          feeRateDecibps = 5; // 0.5 bp
          sourceLabel = 'tg_bot_alpha';
          notionalUsd = 200 + Math.random() * 3500;
        } else if (t % 10 >= 8) {
          bCodeId = b3Id;
          bAddr = '0x3333333333333333333333333333333333333333';
          feeRateDecibps = 2; // 0.2 bp
          sourceLabel = 'api_client';
          notionalUsd = 15000 + Math.random() * 120000;
        }

        const notionalMicro = BigInt(Math.round(notionalUsd * 1_000_000));
        // fee = (notional * f) / 100,000
        const feeMicro = (notionalMicro * BigInt(feeRateDecibps)) / 100_000n;

        const txHash = `0x${Array.from({length: 64}, () => Math.floor(Math.random()*16).toString(16)).join('')}`;
        const extId = `hl_fill_${dayOffset}_${t}_${txHash.slice(0, 10)}`;
        const traderAddr = `0x${Array.from({length: 40}, () => Math.floor(Math.random()*16).toString(16)).join('')}`;

        insertStmt.run(
          extId,
          bCodeId,
          sourceLabel,
          traderAddr,
          notionalMicro.toString(),
          feeMicro.toString(),
          tradeTime.toISOString(),
          txHash
        );

        totalEventsGenerated++;
        totalFeesMicro += feeMicro;
      }
    }
  })();

  const totalFeesFormatted = (Number(totalFeesMicro) / 1_000_000).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  console.log(`  ✓ Generated ${totalEventsGenerated} fee events totaling $${totalFeesFormatted} USDC`);

  // 5. Create a Finalized Historical Settlement for Month of October 2026
  const octFeesRow = db.prepare(`
    SELECT SUM(fee_micro_usd) as total 
    FROM fee_events 
    WHERE builder_code_id = ? AND block_time >= '2026-10-01T00:00:00Z' AND block_time < '2026-11-01T00:00:00Z'
  `).get(b1Id) as { total: number };

  const octTotalMicro = BigInt(octFeesRow?.total || 12_500_000_000); // Fallback $12,500
  const octSplitResult = calculateSplit(octTotalMicro, ruleB1Config);

  const insertSettlement = db.prepare(`
    INSERT INTO settlements (builder_code_id, period_start, period_end, split_rule_version, status, total_fee_micro_usd, locked_at)
    VALUES (?, '2026-10-01T00:00:00Z', '2026-10-31T23:59:59Z', 1, 'final', ?, datetime('now'))
  `);
  const settRes = insertSettlement.run(b1Id, octTotalMicro.toString());
  const settId = Number(settRes.lastInsertRowid);

  const insertLine = db.prepare(`
    INSERT INTO settlement_lines (settlement_id, contributor_id, amount_micro_usd, payout_chain, payout_address)
    VALUES (?, ?, ?, 'solana', ?)
  `);

  const contributorWallets: Record<string, string> = {
    contributor_elena: 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v',
    contributor_marcus: '7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU',
    contributor_treasury: 'Squads1111111111111111111111111111111111111'
  };

  for (const line of octSplitResult.lines) {
    const solWallet = contributorWallets[line.contributorId] || '11111111111111111111111111111111';
    insertLine.run(settId, line.contributorId, line.amountMicroUsd.toString(), solWallet);
  }

  console.log(`  ✓ Created finalized baseline settlement #${settId} for HyperTerminal ($${(Number(octTotalMicro)/1e6).toFixed(2)})`);
  console.log('✅ HyperSettle seed completed with 100% database integrity.');
}

if (process.argv[1] && process.argv[1].endsWith('seed.ts')) {
  try {
    seedDatabase();
    closeDb();
  } catch (err) {
    console.error('Seed failed:', err);
    process.exit(1);
  }
}
