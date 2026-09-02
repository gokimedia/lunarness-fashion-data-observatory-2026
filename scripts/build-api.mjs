import { createHash } from 'node:crypto';
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const sourcePath = join(root, 'data', 'fashion_observatory_2026.json');
const publicRoot = join(root, 'public');
const apiRoot = join(publicRoot, 'api', 'v1');
const sourceText = await readFile(sourcePath, 'utf8');
const dataset = JSON.parse(sourceText);
const baseUrl = 'https://gokimedia.github.io/lunarness-fashion-data-observatory-2026';
const indexNowKey = 'd28a745db7d24cc6b8040d1145426580';

function json(value) {
  return `${JSON.stringify(value, null, 2)}\n`;
}

async function output(relativePath, value) {
  const destination = join(publicRoot, relativePath);
  await mkdir(dirname(destination), { recursive: true });
  await writeFile(destination, typeof value === 'string' ? value : json(value), 'utf8');
}

const topics = [...new Set(dataset.records.map((record) => record.topic))].sort();
const canonicalSourceText = sourceText.replace(/\r\n/g, '\n');
const checksum = createHash('sha256').update(canonicalSourceText).digest('hex');
const distributions = {
  dataset: `${baseUrl}/api/v1/dataset.json`,
  records: `${baseUrl}/api/v1/records.json`,
  manifest: `${baseUrl}/api/v1/manifest.json`,
  openapi: `${baseUrl}/openapi.yaml`,
  postman: `${baseUrl}/postman/lunarness-fashion-data.postman_collection.json`,
};

await output('api/v1/index.json', {
  name: 'Lunarness Fashion Data API',
  version: 'v1',
  dataset_version: dataset.version,
  canonical_url: dataset.canonical_url,
  license: dataset.license,
  endpoints: {
    ...distributions,
    record_template: `${baseUrl}/api/v1/records/{id}.json`,
    topic_template: `${baseUrl}/api/v1/topics/{topic}.json`,
  },
  topics,
});

await output('api/v1/dataset.json', dataset);
await output('api/v1/records.json', {
  dataset: dataset.name,
  dataset_version: dataset.version,
  count: dataset.records.length,
  records: dataset.records,
});

await output('api/v1/manifest.json', {
  name: dataset.name,
  dataset_version: dataset.version,
  published: dataset.published,
  record_count: dataset.records.length,
  topics,
  sha256: checksum,
  canonical_url: dataset.canonical_url,
  doi: 'https://doi.org/10.5281/zenodo.22131190',
  distributions,
});

for (const record of dataset.records) {
  await output(`api/v1/records/${record.id}.json`, {
    dataset: dataset.name,
    dataset_version: dataset.version,
    record,
  });
}

for (const topic of topics) {
  const records = dataset.records.filter((record) => record.topic === topic);
  await output(`api/v1/topics/${topic}.json`, {
    dataset: dataset.name,
    dataset_version: dataset.version,
    topic,
    count: records.length,
    records,
  });
}

const openapi = `openapi: 3.1.0
info:
  title: Lunarness Fashion Data API
  version: 1.0.0
  description: >-
    Read-only access to the cited Lunarness Fashion Data Observatory 2026
    release. Units, periods, sources, derivations and caveats remain attached.
  license:
    name: CC BY 4.0 for Lunarness original analysis and data structure
    url: https://creativecommons.org/licenses/by/4.0/
  contact:
    name: Lunarness
    url: https://lunarness.com/pages/contact
servers:
  - url: ${baseUrl}/api/v1
security: []
paths:
  /index.json:
    get:
      operationId: getApiIndex
      summary: Get the API directory
      responses:
        '200':
          description: API directory and topic list
          content:
            application/json:
              schema:
                type: object
        '404':
          description: API directory not found
  /manifest.json:
    get:
      operationId: getManifest
      summary: Get the release manifest and checksum
      responses:
        '200':
          description: Dataset release manifest
          content:
            application/json:
              schema:
                type: object
        '404':
          description: Manifest not found
  /dataset.json:
    get:
      operationId: getDataset
      summary: Get the complete dataset
      responses:
        '200':
          description: Complete cited dataset
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Dataset'
        '404':
          description: Dataset not found
  /records.json:
    get:
      operationId: listRecords
      summary: List every record
      responses:
        '200':
          description: All records
          content:
            application/json:
              schema:
                type: object
        '404':
          description: Records collection not found
  /records/{id}.json:
    get:
      operationId: getRecord
      summary: Get one record by its stable ID
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
          examples:
            textileConsumption:
              value: eu_textile_consumption
      responses:
        '200':
          description: A single record with source and caveat
          content:
            application/json:
              schema:
                type: object
        '404':
          description: Record ID not found
  /topics/{topic}.json:
    get:
      operationId: listTopicRecords
      summary: List records in one topic
      parameters:
        - name: topic
          in: path
          required: true
          schema:
            type: string
            enum: [${topics.join(', ')}]
      responses:
        '200':
          description: Topic records
          content:
            application/json:
              schema:
                type: object
        '404':
          description: Topic not found
components:
  schemas:
    Dataset:
      type: object
      required: [name, version, published, canonical_url, license, method, records]
      properties:
        name:
          type: string
        version:
          type: string
        published:
          type: string
          format: date
        canonical_url:
          type: string
          format: uri
        license:
          type: object
        method:
          type: string
        records:
          type: array
          items:
            $ref: '#/components/schemas/Record'
    Record:
      type: object
      required: [id, topic, geography, period, entity, unit, source]
      properties:
        id:
          type: string
        topic:
          type: string
        geography:
          type: string
        period:
          type: string
        entity:
          type: string
        value:
          type: number
        value_min:
          type: number
        value_max:
          type: number
        value_lower_bound:
          type: number
        unit:
          type: string
        derivation:
          type: string
        caveat:
          type: string
        source:
          type: string
          format: uri
`;

await output('openapi.yaml', openapi);

const postman = {
  info: {
    _postman_id: '318e922c-1375-4c95-88ec-60fb2f0a2c74',
    name: 'Lunarness Fashion Data API',
    description: 'Source-aware requests for the Lunarness Fashion Data Observatory 2026 public API. No API key is required.',
    schema: 'https://schema.getpostman.com/json/collection/v2.1.0/collection.json',
  },
  variable: [
    { key: 'baseUrl', value: `${baseUrl}/api/v1`, type: 'string' },
    { key: 'recordId', value: 'eu_textile_consumption', type: 'string' },
    { key: 'topic', value: 'circularity', type: 'string' },
  ],
  item: [
    ['API directory', '/index.json'],
    ['Release manifest', '/manifest.json'],
    ['Complete dataset', '/dataset.json'],
    ['All records', '/records.json'],
    ['Record by ID', '/records/{{recordId}}.json'],
    ['Records by topic', '/topics/{{topic}}.json'],
  ].map(([name, path]) => ({
    name,
    request: {
      method: 'GET',
      header: [{ key: 'Accept', value: 'application/json' }],
      url: { raw: `{{baseUrl}}${path}`, host: ['{{baseUrl}}'], path: path.slice(1).split('/') },
      description: 'Returns a versioned, read-only JSON representation with source and interpretation fields intact.',
    },
    response: [],
  })),
};

await output('postman/lunarness-fashion-data.postman_collection.json', postman);
await output(`${indexNowKey}.txt`, `${indexNowKey}\n`);

const html = `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Lunarness Fashion Data API</title>
  <meta name="description" content="Public, source-aware JSON endpoints for the Lunarness Fashion Data Observatory 2026.">
  <link rel="canonical" href="${baseUrl}/">
  <style>body{max-width:760px;margin:0 auto;padding:64px 24px;background:#f5f1e8;color:#171714;font:18px/1.6 system-ui,sans-serif}h1{font-size:clamp(42px,8vw,76px);line-height:.95;letter-spacing:-.05em}a{color:#315900;text-underline-offset:4px}code{overflow-wrap:anywhere}li{margin:12px 0}.note{margin:36px 0;padding:22px;border-left:4px solid #5b8c00;background:#fff}</style>
</head>
<body>
  <p>Lunarness Research · Public API v1</p>
  <h1>Fashion data with its sources still attached.</h1>
  <p>This read-only API distributes the Lunarness Fashion Data Observatory 2026 dataset without removing units, periods, derivations or caveats. No API key is required.</p>
  <ul>
    <li><a href="api/v1/index.json">API directory</a></li>
    <li><a href="api/v1/dataset.json">Complete dataset</a></li>
    <li><a href="api/v1/manifest.json">Version and SHA-256 manifest</a></li>
    <li><a href="openapi.yaml">OpenAPI 3.1 specification</a></li>
    <li><a href="postman/lunarness-fashion-data.postman_collection.json">Postman collection</a></li>
  </ul>
  <div class="note"><strong>Canonical research page</strong><br><a href="${dataset.canonical_url}">${dataset.canonical_url}</a><br>DOI: <a href="https://doi.org/10.5281/zenodo.22131190">10.5281/zenodo.22131190</a></div>
  <p>Third-party facts remain subject to their source terms. Cite the linked source for each metric.</p>
</body>
</html>
`;

await output('index.html', html);
await output('robots.txt', `User-agent: *\nAllow: /\nSitemap: ${baseUrl}/sitemap.xml\n`);
await output('sitemap.xml', `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n  <url><loc>${baseUrl}/</loc></url>\n  <url><loc>${baseUrl}/api/v1/index.json</loc></url>\n  <url><loc>${baseUrl}/api/v1/dataset.json</loc></url>\n  <url><loc>${baseUrl}/api/v1/manifest.json</loc></url>\n</urlset>\n`);

console.log(`Built ${dataset.records.length} record endpoints across ${topics.length} topics.`);
