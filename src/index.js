import { readFileSync } from 'node:fs';

const datasetUrl = new URL('../data/fashion_observatory_2026.json', import.meta.url);
const bundledDataset = Object.freeze(JSON.parse(readFileSync(datasetUrl, 'utf8')));

const REQUIRED_DATASET_FIELDS = ['name', 'version', 'published', 'canonical_url', 'license', 'records'];
const REQUIRED_RECORD_FIELDS = ['id', 'topic', 'geography', 'period', 'entity', 'unit', 'source'];
const VALUE_FIELDS = ['value', 'value_lower_bound', 'value_min', 'value_max'];

function clone(value) {
  return structuredClone(value);
}

function normalize(value) {
  return String(value ?? '').trim().toLocaleLowerCase('en-US');
}

function isHttpsUrl(value) {
  try {
    return new URL(value).protocol === 'https:';
  } catch {
    return false;
  }
}

export function getDataset() {
  return clone(bundledDataset);
}

export function listRecords({ topic } = {}) {
  const records = topic
    ? bundledDataset.records.filter((record) => normalize(record.topic) === normalize(topic))
    : bundledDataset.records;
  return clone(records);
}

export function getRecord(id) {
  const record = bundledDataset.records.find((candidate) => candidate.id === id);
  return record ? clone(record) : undefined;
}

export function searchRecords(query) {
  const needle = normalize(query);
  if (!needle) return [];

  return clone(
    bundledDataset.records.filter((record) =>
      [record.id, record.topic, record.geography, record.period, record.entity, record.unit, record.caveat]
        .some((value) => normalize(value).includes(needle)),
    ),
  );
}

export function listTopics() {
  return [...new Set(bundledDataset.records.map((record) => record.topic))].sort();
}

export function listSources() {
  const sources = new Map();
  for (const record of bundledDataset.records) {
    const item = sources.get(record.source) ?? { url: record.source, record_ids: [] };
    item.record_ids.push(record.id);
    sources.set(record.source, item);
  }
  return clone([...sources.values()].sort((a, b) => a.url.localeCompare(b.url)));
}

export function formatRecordValue(record) {
  if (typeof record.value === 'number') return `${record.value} ${record.unit}`;
  if (typeof record.value_lower_bound === 'number') return `${record.value_lower_bound}+ ${record.unit}`;
  if (typeof record.value_min === 'number' && typeof record.value_max === 'number') {
    return `${record.value_min}–${record.value_max} ${record.unit}`;
  }
  return `Unspecified ${record.unit ?? ''}`.trim();
}

export function getCitation() {
  return `Lunarness Editorial Team (${bundledDataset.published.slice(0, 4)}). ${bundledDataset.name} (Version ${bundledDataset.version}). https://doi.org/10.5281/zenodo.22131190`;
}

export function validateDataset(dataset = bundledDataset) {
  const errors = [];
  const warnings = [];

  if (!dataset || typeof dataset !== 'object' || Array.isArray(dataset)) {
    return { valid: false, errors: ['Dataset must be a JSON object.'], warnings, stats: { records: 0, topics: 0, sources: 0 } };
  }

  for (const field of REQUIRED_DATASET_FIELDS) {
    if (dataset[field] === undefined || dataset[field] === null || dataset[field] === '') {
      errors.push(`Dataset is missing required field: ${field}.`);
    }
  }

  if (!isHttpsUrl(dataset.canonical_url)) {
    errors.push('Dataset canonical_url must be a valid HTTPS URL.');
  }

  const records = Array.isArray(dataset.records) ? dataset.records : [];
  if (!Array.isArray(dataset.records)) errors.push('Dataset records must be an array.');
  if (records.length === 0) errors.push('Dataset must contain at least one record.');

  const ids = new Set();
  for (const [index, record] of records.entries()) {
    const label = record?.id || `record[${index}]`;
    if (!record || typeof record !== 'object' || Array.isArray(record)) {
      errors.push(`record[${index}] must be an object.`);
      continue;
    }

    for (const field of REQUIRED_RECORD_FIELDS) {
      if (record[field] === undefined || record[field] === null || record[field] === '') {
        errors.push(`${label} is missing required field: ${field}.`);
      }
    }

    if (record.id) {
      if (ids.has(record.id)) errors.push(`Duplicate record id: ${record.id}.`);
      ids.add(record.id);
    }

    if (!isHttpsUrl(record.source)) errors.push(`${label} source must be a valid HTTPS URL.`);

    const presentValues = VALUE_FIELDS.filter((field) => record[field] !== undefined);
    const hasScalar = presentValues.includes('value');
    const hasLowerBound = presentValues.includes('value_lower_bound');
    const hasMin = presentValues.includes('value_min');
    const hasMax = presentValues.includes('value_max');
    const validValueShape = hasScalar || hasLowerBound || (hasMin && hasMax);

    if (!validValueShape) errors.push(`${label} must define value, value_lower_bound, or both value_min and value_max.`);
    if ((hasMin && !hasMax) || (!hasMin && hasMax)) errors.push(`${label} must define value_min and value_max together.`);
    if ((hasScalar && presentValues.length > 1) || (hasLowerBound && presentValues.length > 1)) {
      errors.push(`${label} mixes incompatible value representations.`);
    }

    for (const field of presentValues) {
      if (typeof record[field] !== 'number' || !Number.isFinite(record[field])) {
        errors.push(`${label} ${field} must be a finite number.`);
      }
    }

    if (hasMin && hasMax && record.value_min > record.value_max) {
      errors.push(`${label} value_min cannot exceed value_max.`);
    }
    if (!record.caveat) warnings.push(`${label} has no caveat; confirm that the metric cannot be misread.`);
  }

  const topics = new Set(records.map((record) => record?.topic).filter(Boolean));
  const sources = new Set(records.map((record) => record?.source).filter(Boolean));
  return {
    valid: errors.length === 0,
    errors,
    warnings,
    stats: { records: records.length, topics: topics.size, sources: sources.size },
  };
}
