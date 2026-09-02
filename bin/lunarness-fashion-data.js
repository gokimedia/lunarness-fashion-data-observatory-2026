#!/usr/bin/env node

import process from 'node:process';
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

const HELP = `lunarness-fashion-data

Query and validate the Lunarness Fashion Data Observatory 2026 dataset.

Usage:
  lunarness-fashion-data list [--topic <topic>] [--json]
  lunarness-fashion-data get <record-id> [--json]
  lunarness-fashion-data search <query> [--json]
  lunarness-fashion-data topics [--json]
  lunarness-fashion-data sources [--json]
  lunarness-fashion-data validate [--json]
  lunarness-fashion-data citation
  lunarness-fashion-data --version

Canonical source:
  https://lunarness.com/pages/fashion-statistics-observatory
`;

function readOption(args, name) {
  const index = args.indexOf(name);
  return index === -1 ? undefined : args[index + 1];
}

function withoutOptions(args) {
  const values = [];
  for (let index = 0; index < args.length; index += 1) {
    if (args[index] === '--json') continue;
    if (args[index] === '--topic') {
      index += 1;
      continue;
    }
    values.push(args[index]);
  }
  return values;
}

function printJson(value) {
  console.log(JSON.stringify(value, null, 2));
}

function printRecords(records) {
  if (records.length === 0) {
    console.log('No records found.');
    return;
  }

  const rows = records.map((record) => ({
    id: record.id,
    topic: record.topic,
    period: record.period,
    entity: record.entity,
    value: formatRecordValue(record),
  }));
  console.table(rows);
}

function printRecord(record) {
  console.log(`ID: ${record.id}`);
  console.log(`Topic: ${record.topic}`);
  console.log(`Entity: ${record.entity}`);
  console.log(`Geography: ${record.geography}`);
  console.log(`Period: ${record.period}`);
  console.log(`Value: ${formatRecordValue(record)}`);
  if (record.derivation) console.log(`Derivation: ${record.derivation}`);
  if (record.caveat) console.log(`Caveat: ${record.caveat}`);
  console.log(`Source: ${record.source}`);
}

function fail(message, exitCode = 1) {
  console.error(message);
  process.exitCode = exitCode;
}

const args = process.argv.slice(2);
const command = args[0];
const json = args.includes('--json');

if (!command || command === '--help' || command === '-h' || command === 'help') {
  console.log(HELP);
} else if (command === '--version' || command === '-v') {
  console.log(getDataset().version);
} else if (command === 'list') {
  const topic = readOption(args, '--topic');
  if (args.includes('--topic') && !topic) {
    fail('--topic requires a value.', 2);
  } else {
    const records = listRecords({ topic });
    json ? printJson(records) : printRecords(records);
  }
} else if (command === 'get') {
  const [id] = withoutOptions(args.slice(1));
  if (!id) {
    fail('get requires a record id.', 2);
  } else {
    const record = getRecord(id);
    if (!record) fail(`Unknown record id: ${id}.`);
    else json ? printJson(record) : printRecord(record);
  }
} else if (command === 'search') {
  const query = withoutOptions(args.slice(1)).join(' ');
  if (!query) fail('search requires a query.', 2);
  else {
    const records = searchRecords(query);
    json ? printJson(records) : printRecords(records);
  }
} else if (command === 'topics') {
  const topics = listTopics();
  json ? printJson(topics) : topics.forEach((topic) => console.log(topic));
} else if (command === 'sources') {
  const sources = listSources();
  if (json) printJson(sources);
  else sources.forEach((source) => console.log(`${source.url}\n  ${source.record_ids.join(', ')}`));
} else if (command === 'validate') {
  const result = validateDataset();
  if (json) printJson(result);
  else {
    console.log(result.valid ? 'Dataset is valid.' : 'Dataset is invalid.');
    console.log(`Records: ${result.stats.records}; topics: ${result.stats.topics}; sources: ${result.stats.sources}.`);
    result.errors.forEach((error) => console.error(`ERROR: ${error}`));
    result.warnings.forEach((warning) => console.warn(`WARNING: ${warning}`));
  }
  if (!result.valid) process.exitCode = 1;
} else if (command === 'citation') {
  console.log(getCitation());
} else {
  fail(`Unknown command: ${command}. Run with --help for usage.`, 2);
}
