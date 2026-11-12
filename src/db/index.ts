import Database from 'better-sqlite3';
import path from 'path';
import fs from 'fs';
import { SCHEMA_SQL } from './schema';

function resolveProjectRoot(): string {
  let dir = process.cwd();
  for (let i = 0; i < 6; i++) {
    if (fs.existsSync(path.join(dir, 'package.json'))) {
      return dir;
    }
    const parent = path.dirname(dir);
    if (parent === dir) break;
    dir = parent;
  }
  return process.cwd();
}

const DATA_DIR = path.join(resolveProjectRoot(), 'data');
if (!fs.existsSync(DATA_DIR)) {
  fs.mkdirSync(DATA_DIR, { recursive: true });
}

const DEFAULT_DB_PATH = process.env.DATABASE_PATH || path.join(DATA_DIR, 'hypersettle.db');

declare global {
  // eslint-disable-next-line no-var
  var __hypersettleDb: Database.Database | undefined;
  // eslint-disable-next-line no-var
  var __hypersettleDbPath: string | undefined;
}

export function getDb(dbPath: string = DEFAULT_DB_PATH): Database.Database {
  if (!globalThis.__hypersettleDb || globalThis.__hypersettleDbPath !== dbPath) {
    if (globalThis.__hypersettleDb) {
      globalThis.__hypersettleDb.close();
    }
    const db = new Database(dbPath);
    db.pragma('journal_mode = WAL');
    db.pragma('foreign_keys = ON');
    db.exec(SCHEMA_SQL);
    globalThis.__hypersettleDb = db;
    globalThis.__hypersettleDbPath = dbPath;
  }
  return globalThis.__hypersettleDb;
}

export function closeDb(): void {
  if (globalThis.__hypersettleDb) {
    globalThis.__hypersettleDb.close();
    globalThis.__hypersettleDb = undefined;
    globalThis.__hypersettleDbPath = undefined;
  }
}
