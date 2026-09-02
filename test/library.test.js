import test from 'node:test';
import assert from 'node:assert/strict';

import {
  formatRecordValue,
  getCitation,
  getDataset,
  getRecord,
  listRecords,
  listSources,
  listTopics,
  searchRecords,
  validateDataset,
} from '../src/index.js';

test('loads the complete versioned dataset', () => {
  const dataset = getDataset();
  assert.equal(dataset.name, 'Lunarness Fashion Data Observatory 2026');
  assert.equal(dataset.version, '1.0');
  assert.equal(dataset.records.length, 10);
});

test('returns defensive copies', () => {
  const first = getDataset();
  first.records.length = 0;
  assert.equal(getDataset().records.length, 10);
});

test('filters, finds, and searches records', () => {
  assert.equal(listRecords({ topic: 'ECOMMERCE' }).length, 2);
  assert.equal(getRecord('eu_textile_waste').value, 16);
  assert.equal(getRecord('missing'), undefined);
  assert.ok(searchRecords('London').some((record) => record.id === 'fw_london_top3_total'));
  assert.ok(searchRecords('percentage points').some((record) => record.id === 'eu_online_apparel_age_gap'));
});

test('lists unique topics and sources', () => {
  assert.deepEqual(listTopics(), ['circularity', 'climate', 'digital_demand', 'ecommerce', 'media_attention']);
  assert.equal(listSources().length, 9);
});

test('formats scalar, lower-bound, and range values without changing their meaning', () => {
  assert.equal(formatRecordValue(getRecord('eu_textile_waste')), '16 kg per capita');
  assert.equal(formatRecordValue(getRecord('fashion_site_visits')), '184+ monthly visits in millions');
  assert.equal(formatRecordValue(getRecord('global_textile_ghg_range')), '2–8 percent of global GHG emissions');
});

test('validates the bundled dataset', () => {
  const result = validateDataset();
  assert.equal(result.valid, true);
  assert.deepEqual(result.errors, []);
  assert.equal(result.stats.records, 10);
});

test('rejects duplicate ids and incomplete ranges', () => {
  const dataset = getDataset();
  dataset.records[1].id = dataset.records[0].id;
  delete dataset.records[2].value;
  dataset.records[2].value_min = 10;
  const result = validateDataset(dataset);
  assert.equal(result.valid, false);
  assert.ok(result.errors.some((error) => error.includes('Duplicate record id')));
  assert.ok(result.errors.some((error) => error.includes('value_min and value_max together')));
});

test('returns the stable DOI citation', () => {
  assert.match(getCitation(), /10\.5281\/zenodo\.22131190/);
});
