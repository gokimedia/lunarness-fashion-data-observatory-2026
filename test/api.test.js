import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFile } from 'node:fs/promises';
import { join } from 'node:path';
import test from 'node:test';

const root = process.cwd();

async function readJson(path) {
  return JSON.parse(await readFile(join(root, path), 'utf8'));
}

test('generated API exposes every source record', async () => {
  const sourceText = await readFile(join(root, 'data/fashion_observatory_2026.json'), 'utf8');
  const source = await readJson('data/fashion_observatory_2026.json');
  const listing = await readJson('public/api/v1/records.json');
  const manifest = await readJson('public/api/v1/manifest.json');
  assert.equal(listing.count, source.records.length);
  assert.equal(manifest.record_count, source.records.length);
  const expectedChecksum = createHash('sha256').update(sourceText.replace(/\r\n/g, '\n')).digest('hex');
  assert.equal(manifest.sha256, expectedChecksum);

  for (const record of source.records) {
    const endpoint = await readJson(`public/api/v1/records/${record.id}.json`);
    assert.deepEqual(endpoint.record, record);
  }
});

test('topic endpoints partition records without loss', async () => {
  const source = await readJson('data/fashion_observatory_2026.json');
  const index = await readJson('public/api/v1/index.json');
  const records = [];

  for (const topic of index.topics) {
    const endpoint = await readJson(`public/api/v1/topics/${topic}.json`);
    assert.equal(endpoint.topic, topic);
    assert.equal(endpoint.count, endpoint.records.length);
    assert.ok(endpoint.records.every((record) => record.topic === topic));
    records.push(...endpoint.records);
  }

  assert.deepEqual(records.map(({ id }) => id).sort(), source.records.map(({ id }) => id).sort());
});

test('OpenAPI and Postman artifacts use the public API base URL', async () => {
  const baseUrl = 'https://gokimedia.github.io/lunarness-fashion-data-observatory-2026/api/v1';
  const openapi = await readFile(join(root, 'public/openapi.yaml'), 'utf8');
  const postman = await readJson('public/postman/lunarness-fashion-data.postman_collection.json');
  assert.match(openapi, /openapi: 3\.1\.0/);
  assert.match(openapi, new RegExp(baseUrl.replaceAll('.', '\\.')));
  assert.equal(postman.variable.find(({ key }) => key === 'baseUrl').value, baseUrl);
  assert.equal(postman.item.length, 6);
});

test('IndexNow key is available at the site root', async () => {
  const key = 'd28a745db7d24cc6b8040d1145426580';
  assert.equal((await readFile(join(root, 'public', `${key}.txt`), 'utf8')).trim(), key);
});
