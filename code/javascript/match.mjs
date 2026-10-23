// Node 22+: node --env-file=.env code/javascript/match.mjs
// Native fetch + REST, no npm packages. One paid Actor run.
import {mkdir, writeFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import {join} from 'node:path';

const root = fileURLToPath(new URL('../../', import.meta.url));
const api = 'https://api.apify.com/v2';
const token = process.env.APIFY_TOKEN;
const maxCharge = Number(process.env.APIFY_MAX_CHARGE_USD || '0.50');
const timeout = Number(process.env.APIFY_TIMEOUT_SECONDS || '180');
const input = {
  mode: 'matchIds', matchIds: [process.env.MATCH_ID || 'Sf0bExdB'],
  includeOdds: false, includeH2H: false, maxItems: 2,
};

async function request(path, method = 'GET', body) {
  const response = await fetch(api + path, {
    method, headers: {Authorization: `Bearer ${token}`, 'Content-Type': 'application/json'},
    ...(body ? {body: JSON.stringify(body)} : {}), signal: AbortSignal.timeout(90000),
  });
  if (!response.ok) throw new Error(`Apify HTTP ${response.status}; inspect Console before retrying.`);
  return response.json();
}

async function main() {
  if (process.argv.includes('--dry-run')) {
    console.log(JSON.stringify(input, null, 2));
    return;
  }
  if (!token) throw new Error('Set APIFY_TOKEN in .env');
  if (!Number.isFinite(maxCharge) || maxCharge <= 0 || !Number.isInteger(timeout) || timeout < 1)
    throw new Error('Invalid charge limit or timeout');
  const folder = join(root, 'output/direct-javascript-match');
  await mkdir(folder, {recursive: true});
  // Do not retry POST: an uncertain response may already have started a paid run.
  let {data: run} = await request(`/acts/crawlplant~flashscore-tennis/runs?waitForFinish=60&timeout=${timeout}&maxTotalChargeUsd=${maxCharge}`, 'POST', input);
  const saveRun = () => writeFile(join(folder, 'run.json'), JSON.stringify({
    actor: 'crawlplant/flashscore-tennis', input, run_id: run.id,
    dataset_id: run.defaultDatasetId, status: run.status,
    requested_max_charge_usd: maxCharge, retrieved_at: new Date().toISOString(),
  }, null, 2));
  await saveRun();
  const deadline = Date.now() + (timeout + 120) * 1000;
  while (['READY', 'RUNNING', 'TIMING-OUT', 'ABORTING'].includes(run.status)) {
    if (Date.now() > deadline) throw new Error(`Stop waiting for ${run.id}; inspect Console before retrying.`);
    await new Promise(resolve => setTimeout(resolve, 2000));
    ({data: run} = await request(`/actor-runs/${run.id}?waitForFinish=30`));
    await saveRun();
  }
  if (run.status !== 'SUCCEEDED') throw new Error(`Run ${run.id}: ${run.status}`);
  const rows = [];
  for (let offset = 0; ; offset += 1000) {
    const page = await request(`/datasets/${run.defaultDatasetId}/items?format=json&offset=${offset}&limit=1000`);
    if (!Array.isArray(page)) throw new Error('Expected a dataset array');
    rows.push(...page);
    if (page.length < 1000) break;
  }
  await writeFile(join(folder, 'data.json'), JSON.stringify(rows, null, 2));
  console.log(`Saved ${rows.length} records to ${folder}. Bounded sample; no completeness claim.`);
}

main().catch(error => {
  console.error(token ? String(error.message).split(token).join('[REDACTED]') : error.message);
  process.exitCode = 1;
});
