import { getDb, closeDb } from './index.js';
import { SCHEMA_SQL } from './schema.js';

export function runMigrations(db = getDb()) {
  console.log('⚡ Running HyperSettle database migrations...');
  db.exec(SCHEMA_SQL);
  console.log('✓ Tables and indexes initialized successfully.');
}

if (process.argv[1] && process.argv[1].endsWith('migrate.ts')) {
  try {
    runMigrations();
    closeDb();
  } catch (err) {
    console.error('Migration failed:', err);
    process.exit(1);
  }
}
