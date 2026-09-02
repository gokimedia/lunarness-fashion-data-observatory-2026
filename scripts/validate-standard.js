#!/usr/bin/env node

import { readdir, readFile } from 'node:fs/promises';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('..', import.meta.url));
const standardRoot = join(root, 'standard');
const requiredCriteria = ['S1', 'M1', 'C1', 'C2', 'A1', 'V1', 'G1', 'I1'];
const allowedStatuses = new Set(['verified', 'self-assessed', 'expired', 'revoked']);

const loadJson = async (path) => JSON.parse(await readFile(path, 'utf8'));
const fail = (message) => {
  throw new Error(message);
};

const index = await loadJson(join(standardRoot, 'registry.json'));
const schema = await loadJson(join(standardRoot, 'registry-entry.schema.json'));
const registryFiles = (await readdir(join(standardRoot, 'registry'))).filter((name) => name.endsWith('.json'));
const badgeFiles = new Set((await readdir(join(standardRoot, 'badges'))).filter((name) => name.endsWith('.json')));

if (index.standard_version !== '1.0' || schema.properties?.standard_version?.const !== '1.0') {
  fail('Standard version mismatch');
}
if (index.entries.length !== registryFiles.length) {
  fail(`Registry index has ${index.entries.length} entries but ${registryFiles.length} detail files exist`);
}

const ids = new Set();
for (const summary of index.entries) {
  const detail = await loadJson(join(standardRoot, summary.record_file));
  const badgeName = summary.badge_file.replace(/^badges\//, '');
  const badge = await loadJson(join(standardRoot, summary.badge_file));

  if (ids.has(detail.record_id)) fail(`Duplicate record ID: ${detail.record_id}`);
  ids.add(detail.record_id);
  if (detail.record_id !== summary.record_id) fail(`Record ID mismatch in ${summary.record_file}`);
  if (detail.domain !== summary.domain || detail.status !== summary.status) fail(`Index mismatch for ${detail.record_id}`);
  if (!allowedStatuses.has(detail.status)) fail(`Unsupported status for ${detail.record_id}`);
  if (detail.status === 'verified' && detail.independent_review !== true) fail(`Verified record lacks independent review: ${detail.record_id}`);
  if (detail.status === 'self-assessed' && detail.independent_review !== false) fail(`Self-assessed record has invalid review flag: ${detail.record_id}`);
  if (!/^lfdts-\d{4}-\d{4}$/.test(detail.record_id)) fail(`Invalid record ID: ${detail.record_id}`);
  if (!/^[a-f0-9]{64}$/.test(detail.artifact_sha256)) fail(`Invalid SHA-256 digest: ${detail.record_id}`);
  if (Date.parse(detail.issued_at) >= Date.parse(detail.expires_at)) fail(`Invalid date range: ${detail.record_id}`);
  if (Object.keys(detail.criteria).sort().join(',') !== [...requiredCriteria].sort().join(',')) fail(`Criterion set mismatch: ${detail.record_id}`);
  if (requiredCriteria.some((key) => detail.criteria[key] !== 'pass')) fail(`Criterion failure in active record: ${detail.record_id}`);
  if (!badgeFiles.has(badgeName)) fail(`Badge status file missing: ${badgeName}`);
  if (badge.schemaVersion !== 1 || badge.message !== detail.status) fail(`Badge mismatch: ${detail.record_id}`);
}

console.log(JSON.stringify({ valid: true, version: index.standard_version, records: ids.size, criteria: requiredCriteria.length }));
