import test from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const cli = fileURLToPath(new URL('../bin/lunarness-fashion-data.js', import.meta.url));

function run(...args) {
  return spawnSync(process.execPath, [cli, ...args], { encoding: 'utf8' });
}

test('validate command succeeds', () => {
  const result = run('validate');
  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /Dataset is valid/);
  assert.match(result.stdout, /Records: 10/);
});

test('get command returns a metric with its caveat and source', () => {
  const result = run('get', 'fw_paris_top3_total');
  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /97\.7 USD millions/);
  assert.match(result.stdout, /Top-three brand MIV only/);
  assert.match(result.stdout, /https:\/\//);
});

test('search command emits machine-readable JSON', () => {
  const result = run('search', 'circularity', '--json');
  assert.equal(result.status, 0, result.stderr);
  const records = JSON.parse(result.stdout);
  assert.equal(records.length, 2);
});

test('unknown record exits non-zero', () => {
  const result = run('get', 'does-not-exist');
  assert.equal(result.status, 1);
  assert.match(result.stderr, /Unknown record id/);
});
