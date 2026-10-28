// Evaluator-only: real HTTP boundaries and actual Chrome behavior, never agent input.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
import { spawn, execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';
import { mkdir, mkdtemp, readFile, writeFile, rm, copyFile } from 'node:fs/promises';
import { resolve, join, dirname } from 'node:path';
import os from 'node:os';

const [kind, appArgument, outputArgument] = process.argv.slice(2);
if (!['owner-notes', 'dashboard'].includes(kind) || !appArgument || !outputArgument) throw Error('Use: node expansion-check.mjs <owner-notes|dashboard> <app-directory> <new-output-directory>');
const app = resolve(appArgument), output = resolve(outputArgument);
const evaluatorRoot = dirname(fileURLToPath(import.meta.url));
if (!output.startsWith(evaluatorRoot + '/')) throw Error('Evaluator output must be under the evaluation directory.');
await mkdir(dirname(output), { recursive: true }); await mkdir(output);
const dataDir = await mkdtemp(join(os.tmpdir(), 'toy-fixture-data-'));
const executionApp = join(dataDir, 'clean-app');
await mkdir(executionApp);
for (const name of ['README.md', 'server.py', 'index.html', 'app.js', 'style.css']) await copyFile(join(app, name), join(executionApp, name));
const logs = [], results = [], children = [];
let browser;
async function start(extra = []) {
  const child = spawn('python3', [join(executionApp, 'server.py'), '--port', '0', ...(kind === 'owner-notes' ? ['--data-dir', dataDir] : []), ...extra], { cwd: executionApp });
  children.push(child);
  child.stderr.on('data', data => logs.push(data.toString()));
  const port = await new Promise((resolve, reject) => {
    let text = '';
    const timeout = setTimeout(() => reject(Error('Server startup timeout')), 10000);
    child.on('error', error => { clearTimeout(timeout); reject(error); });
    child.on('exit', code => { if (!text.includes('\n')) { clearTimeout(timeout); reject(Error('Server failed to start: ' + code)); } });
    child.stdout.on('data', data => {
      text += data.toString();
      if (text.includes('\n')) { clearTimeout(timeout); try { resolve(JSON.parse(text.split('\n')[0]).port); } catch (error) { reject(error); } }
    });
  });
  return `http://127.0.0.1:${port}`;
}
async function check(id, criteria, steps, fn) {
  const result = { id, criteria, steps, captured_at: new Date().toISOString(), details: {} };
  try { await fn(result.details); result.status = 'pass'; }
  catch (error) { result.status = String(error).startsWith('AssertionError') ? 'fail' : 'unknown'; result.error = String(error); }
  results.push(result); console.log(`${id}: ${result.status}`);
}
async function browserCheck(id, criteria, steps, base, viewport, fn) {
  await check(id, criteria, steps, async details => {
    const context = await browser.newContext({ viewport });
    await context.tracing.start({ screenshots: true, snapshots: true, sources: true });
    const page = await context.newPage();
    details.runtime_errors = []; page.on('pageerror', error => details.runtime_errors.push(String(error)));
    try { await page.goto(base); await fn(page, details); }
    finally { await page.screenshot({ path: join(output, id + '.png'), fullPage: true }); await context.tracing.stop({ path: join(output, id + '.trace.zip') });
      details.trace_redaction = JSON.parse(execFileSync('python3', [join(evaluatorRoot, 'redact_trace.py'), join(output, id + '.trace.zip')], { encoding: 'utf8' }));
      await context.close(); }
  });
}
async function api(base, path, method = 'GET', cookie, payload) {
  const response = await fetch(base + path, { method, headers: { ...(cookie ? { Cookie: cookie } : {}), ...(payload ? { 'Content-Type': 'application/json' } : {}) }, ...(payload ? { body: JSON.stringify(payload) } : {}) });
  return { status: response.status, data: await response.json() };
}
async function login(base, user) {
  const response = await fetch(base + '/api/login', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ username: user, password: user + '-demo' }) });
  const header = response.headers.get('set-cookie') || '';
  return { status: response.status, cookie: header.split(';')[0], flags: { httpOnly: /httponly/i.test(header), sameSiteStrict: /samesite=strict/i.test(header) } };
}
try {
  browser = await chromium.launch({ channel: 'chrome', headless: true });
  const base = await start();
  if (kind === 'owner-notes') {
    const a = await login(base, 'alice'), b = await login(base, 'bob');
    await check('owner-positive-controls', ['S02'], 'A/B list and read owned resources; anonymous is denied.', async d => {
      d.aList = await api(base, '/api/notes', 'GET', a.cookie); d.bList = await api(base, '/api/notes', 'GET', b.cookie);
      d.aRead = await api(base, '/api/notes/note-a', 'GET', a.cookie); d.anonymous = await api(base, '/api/notes/note-a');
      d.anonymousWrite = await api(base, '/api/notes/note-a', 'PATCH', undefined, { text: 'Anonymous marker' });
      assert.equal(d.aRead.status, 200); assert.equal(d.anonymous.status, 401); assert.equal(d.anonymousWrite.status, 401);
      assert.deepEqual(d.aList.data.map(n => n.owner), ['alice']); assert.deepEqual(d.bList.data.map(n => n.owner), ['bob']);
    });
    await check('cross-owner-read', ['S02'], 'Direct request by A for B resource; no UI guard is involved.', async d => {
      d.response = await api(base, '/api/notes/note-b', 'GET', a.cookie);
      assert.ok([403, 404].includes(d.response.status), 'Another owner must not read this resource');
    });
    await check('cross-owner-write', ['S02'], 'Direct A->B mutation, then B independently reads its data.', async d => {
      d.before = await api(base, '/api/notes/note-b', 'GET', b.cookie);
      d.mutation = await api(base, '/api/notes/note-b', 'PATCH', a.cookie, { text: 'Unauthorized disposable marker' });
      d.after = await api(base, '/api/notes/note-b', 'GET', b.cookie);
      assert.ok([403, 404].includes(d.mutation.status), 'Another owner must not mutate this resource');
      assert.deepEqual(d.after.data, d.before.data);
    });
    await check('owned-edit-and-validation', ['S02', 'S03'], 'Owned quotes/Unicode/plain markup persist; extra ownership fields are rejected.', async d => {
      const text = "Owner's café <b>plain text</b>";
      d.write = await api(base, '/api/notes/note-a', 'PATCH', a.cookie, { text });
      d.read = await api(base, '/api/notes/note-a', 'GET', a.cookie);
      d.transfer = await api(base, '/api/notes/note-a', 'PATCH', a.cookie, { text, owner: 'bob' });
      assert.equal(d.write.status, 200); assert.equal(d.read.data.text, text); assert.equal(d.transfer.status, 422);
    });
    await check('session-lifecycle', ['S04'], 'Verify local cookie flags, invalid login, logout and old-session replay.', async d => {
      d.flags = a.flags; d.invalid = (await login(base, 'invalid')).status;
      d.logout = await api(base, '/api/logout', 'POST', a.cookie, {});
      d.replay = await api(base, '/api/notes', 'GET', a.cookie);
      assert.ok(d.flags.httpOnly && d.flags.sameSiteStrict); assert.equal(d.invalid, 401); assert.equal(d.logout.status, 200); assert.equal(d.replay.status, 401);
    });
    await check('session-expiry', ['S04'], 'Actual one-second test-session expiry; no fake clock.', async d => {
      const expiring = await start(['--session-seconds', '1']); const session = await login(expiring, 'alice');
      d.initial = (await api(expiring, '/api/notes', 'GET', session.cookie)).status;
      await new Promise(resolve => setTimeout(resolve, 1200));
      d.expired = (await api(expiring, '/api/notes', 'GET', session.cookie)).status;
      assert.equal(d.initial, 200); assert.equal(d.expired, 401);
    });
    await browserCheck('login-desktop-preserve', ['S03', 'S04'], 'Capture unchanged login UI, then use owned note UI and logout.', base, { width: 1000, height: 800 }, async (page, d) => {
      await page.screenshot({ path: join(output, 'approved-login.png'), fullPage: true });
      await page.locator('#username').fill('alice'); await page.locator('#password').fill('alice-demo');
      await page.getByRole('button', { name: 'Sign in' }).click(); await page.locator('#notes textarea').waitFor();
      d.literalValue = await page.locator('#notes textarea').inputValue(); d.markupElements = await page.locator('#notes b').count();
      assert.equal(d.literalValue, "Owner's café <b>plain text</b>"); assert.equal(d.markupElements, 0);
      await page.locator('#logout').click(); await page.getByRole('button', { name: 'Sign in' }).waitFor();
      assert.match(await page.locator('#status').textContent(), /signed out/i);
    });
  } else {
    for (const width of [320, 390, 768, 1440]) {
      await browserCheck('layout-' + width, ['U03', 'A04'], 'Load at actual CSS viewport; verify essential Refresh and metric text fit without horizontal task obstruction.', base, { width, height: 900 }, async (page, d) => {
        await page.locator('article').first().waitFor();
        d.geometry = await page.locator('#refresh').evaluate(el => { const r = el.getBoundingClientRect(); return { x: r.x, right: r.right, width: innerWidth, scrollWidth: document.documentElement.scrollWidth }; });
        d.values = await page.locator('.value').allTextContents();
        assert.ok(d.geometry.x >= 0 && d.geometry.right <= width, 'Refresh action must be reachable inside viewport');
        assert.ok(d.geometry.scrollWidth <= width, 'Page must not require horizontal scrolling for these tasks');
        assert.deepEqual(d.values, ['$24,500', '182', '96', '4.2%']);
      });
    }
    await browserCheck('desktop-approved', ['U01', 'U05', 'A02'], 'Capture approved successful desktop screen and native labels/control behavior.', base, { width: 1440, height: 900 }, async (page, d) => {
      await page.locator('article').first().waitFor();
      d.title = await page.locator('h1').textContent(); d.filterName = await page.getByLabel('Filter metrics').count();
      assert.equal(d.title, 'Metrics dashboard'); assert.equal(d.filterName, 1); assert.equal(await page.getByRole('button', { name: 'Refresh data' }).count(), 1);
    });
    await browserCheck('error-recovery', ['U02', 'U04', 'P02'], 'After successful data, induce 503; retain values, explain error, then retry successfully.', base, { width: 1440, height: 900 }, async (page, d) => {
      await page.locator('article').first().waitFor(); const before = await page.locator('.value').allTextContents();
      await page.route('**/api/metrics', route => route.fulfill({ status: 503, contentType: 'application/json', body: '{"error":"Controlled outage"}' }));
      await page.locator('#refresh').click(); await page.waitForFunction(() => !document.querySelector('#refresh').disabled);
      d.errorText = await page.locator('#status').textContent(); d.retainedValues = await page.locator('.value').allTextContents();
      assert.match(d.errorText, /unavailable|failed|could not|unable|error/i); assert.deepEqual(d.retainedValues, before);
      await page.unroute('**/api/metrics'); await page.locator('#refresh').click(); await page.waitForFunction(() => !document.querySelector('#refresh').disabled);
      d.recovered = await page.locator('.value').allTextContents(); assert.deepEqual(d.recovered, before);
    });
    await browserCheck('loading-empty-correction', ['U02', 'U04'], 'Enter a nonmatching query, clear it, then observe a controlled slow refresh and successful completion.', base, { width: 1440, height: 900 }, async (page, d) => {
      await page.locator('article').first().waitFor();
      await page.locator('#filter').fill('no-such-metric'); d.empty = await page.locator('#status').textContent();
      assert.match(d.empty, /no matching/i); assert.equal(await page.locator('article').count(), 0);
      await page.locator('#filter').fill(''); assert.equal(await page.locator('article').count(), 4);
      await page.route('**/api/metrics', async route => { await new Promise(resolve => setTimeout(resolve, 200)); await route.continue(); });
      await page.locator('#refresh').click(); d.pending = await page.locator('#status').textContent(); assert.match(d.pending, /loading/i);
      await page.waitForFunction(() => !document.querySelector('#refresh').disabled); d.finished = await page.locator('#status').textContent(); assert.match(d.finished, /4 metrics/i);
    });
    await browserCheck('local-filter-budget', ['P03'], 'Warm filter; measure five actual input-dispatch-to-next-frame samples at 1440x900, no throttling; p95<=100ms. Verify values.', base, { width: 1440, height: 900 }, async (page, d) => {
      await page.locator('article').first().waitFor();
      d.timing = await page.evaluate(async () => {
        const input = document.querySelector('#filter'); const samples = [];
        for (let i = 0; i < 6; i++) {
          input.value = i % 2 ? '' : 'rev'; const start = performance.now(); input.dispatchEvent(new Event('input', { bubbles: true }));
          await new Promise(requestAnimationFrame); if (i) samples.push(performance.now() - start);
        }
        const sorted = [...samples].sort((a, b) => a - b);
        return { samples_ms: samples, p95_ms: sorted[Math.ceil(0.95 * sorted.length) - 1], calculation: 'Nearest-rank p95 of five post-warmup samples', query: input.value };
      });
      d.values = await page.locator('.value').allTextContents(); assert.deepEqual(d.values, ['$24,500', '182', '96', '4.2%']);
      assert.ok(d.timing.p95_ms <= 100, 'Agreed local task budget exceeded; this is not field CWV');
    });
    await browserCheck('keyboard-focus-targets', ['A01', 'A02', 'A05', 'A06'], 'Tab to Refresh and Filter, inspect focus visibility/geometry, activate refresh using Enter.', base, { width: 1440, height: 900 }, async (page, d) => {
      await page.locator('article').first().waitFor(); await page.keyboard.press('Tab');
      d.focus = await page.evaluate(() => { const el = document.activeElement, r = el.getBoundingClientRect(), css = getComputedStyle(el); return { id: el.id, width: r.width, height: r.height, outlineWidth: css.outlineWidth, outlineStyle: css.outlineStyle, visible: r.top >= 0 && r.bottom <= innerHeight && r.right <= innerWidth }; });
      assert.equal(d.focus.id, 'refresh'); assert.ok(d.focus.visible); assert.notEqual(d.focus.outlineStyle, 'none'); assert.ok(parseFloat(d.focus.outlineWidth) > 0); assert.ok(d.focus.width >= 24 && d.focus.height >= 24);
      await page.screenshot({ path: join(output, 'visible-focus.png'), fullPage: true });
      await page.keyboard.press('Enter'); await page.waitForFunction(() => !document.querySelector('#refresh').disabled); await page.keyboard.press('Tab');
      assert.equal(await page.evaluate(() => document.activeElement.id), 'filter'); d.filter_box = await page.locator('#filter').boundingBox(); assert.ok(d.filter_box.width >= 24 && d.filter_box.height >= 24); await page.keyboard.type('Revenue');
      d.matching = await page.locator('h2').allTextContents(); assert.deepEqual(d.matching, ['Revenue']);
    });
    await browserCheck('text-contrast', ['A03'], 'Measure actual computed text/background colors and unrounded WCAG sRGB ratios for every distinct text style in the normal state.', base, { width: 1440, height: 900 }, async (page, d) => {
      await page.locator('article').first().waitFor();
      d.pairs = await page.evaluate(() => {
        function rgb(value) { return value.match(/[\d.]+/g).slice(0,3).map(Number); }
        function luminance(color) { return rgb(color).map(x => { x /= 255; return x <= .04045 ? x / 12.92 : ((x + .055) / 1.055) ** 2.4; }).reduce((sum,x,i) => sum+x*[.2126,.7152,.0722][i],0); }
        return ['h1', '.eyebrow', 'header p:last-child', 'label', '#filter', '#filter::placeholder', '#refresh', '#status', 'h2', '.value', 'footer'].map(selector => {
          const pseudo = selector.endsWith('::placeholder'); const el = document.querySelector(selector.replace('::placeholder', '')), css = getComputedStyle(el, pseudo ? '::placeholder' : null); let parent = el, background;
          while (parent) { background = getComputedStyle(parent).backgroundColor; if (background !== 'rgba(0, 0, 0, 0)' && background !== 'transparent') break; parent = parent.parentElement; }
          const l = [luminance(css.color), luminance(background)].sort((a,b)=>b-a); const size = parseFloat(css.fontSize); const large = size >= 24 || (size >= 18.6666667 && parseInt(css.fontWeight) >= 700);
          return { selector, foreground: css.color, background, size_px: size, weight: css.fontWeight, ratio: (l[0]+.05)/(l[1]+.05), minimum: large ? 3 : 4.5 };
        });
      });
      assert.ok(d.pairs.every(pair => pair.ratio >= pair.minimum), 'Measured normal-state contrast minimum');
    });
    await browserCheck('resize-text', ['A04'], 'Increase actual root text scale to 200%; inspect that essential action remains reachable. This is supplemental text-resize evidence, not a complete browser zoom conformance test.', base, { width: 1440, height: 900 }, async (page, d) => {
      await page.locator('article').first().waitFor(); await page.addStyleTag({ content: 'html { font-size: 200%; }' });
      d.box = await page.locator('#refresh').boundingBox(); d.title = await page.locator('h1').textContent();
      assert.ok(d.box.x >= 0 && d.box.x + d.box.width <= 1440); assert.equal(d.title, 'Metrics dashboard');
    });
    await browserCheck('repeat-refresh-resources', ['P01', 'P04'], 'Warm up then perform five refresh/filter cycles; inspect request count, final data and runtime exceptions.', base, { width: 1440, height: 900 }, async (page, d) => {
      await page.locator('article').first().waitFor(); let requests = 0;
      page.on('request', request => { if (request.url().endsWith('/api/metrics')) requests++; });
      for (let i = 0; i < 5; i++) { await page.locator('#refresh').click(); await page.waitForFunction(() => !document.querySelector('#refresh').disabled); await page.locator('#filter').fill('Revenue'); await page.locator('#filter').fill(''); }
      d.requests = requests; d.values = await page.locator('.value').allTextContents(); assert.equal(requests, 5); assert.equal(d.runtime_errors.length, 0); assert.equal(d.values.length, 4);
    });
    await check('operator-diagnostics', ['O04'], 'Inject a real safe service failure; correlate response ID with redacted operator stderr event.', async d => {
      const response = await fetch(base + '/api/metrics?unavailable=1'); const id = response.headers.get('x-request-id');
      await new Promise(resolve => setTimeout(resolve, 100));
      d.status = response.status; d.request_id = id; d.logged = logs.some(line => line.includes(id) && line.includes('metrics_unavailable'));
      assert.equal(d.status, 503); assert.ok(d.logged);
    });
    await check('clean-startup-smoke', ['O01'], 'A fresh Python process started from declared source files; GET page and deterministic metrics succeed without extra dependencies.', async d => {
      d.page_status = (await fetch(base)).status; d.api = await api(base, '/api/metrics');
      assert.equal(d.page_status, 200); assert.equal(d.api.status, 200); assert.equal(d.api.data.length, 4);
    });
  }
} catch (error) { results.push({ id: 'infrastructure', criteria: [], status: 'unknown', error: String(error) }); process.exitCode = 2; }
finally {
  if (browser) await browser.close();
  for (const child of children) child.kill();
  const hashes = {};
  for (const name of ['README.md', 'server.py', 'index.html', 'app.js', 'style.css']) hashes[name] = createHash('sha256').update(await readFile(join(app, name))).digest('hex');
  await writeFile(join(output, 'results.json'), JSON.stringify({ fixture: kind, captured_at: new Date().toISOString(), app_hashes: hashes,
    environment: { node: process.version, os: os.platform(), cpu: os.cpus()[0]?.model, browser: browser?.version(), channel: 'chrome', throttling: 'none', execution_isolation: 'Fresh temporary copy of five declared fixture files; fresh process, empty data directory.', task_budget: 'dashboard filter local p95 of five post-warmup samples <=100ms; no field data' }, results, logs,
    limitations: 'Evaluator-led observations on seeded local fixtures. Not a skill-effectiveness comparison, full security assessment, field CWV or WCAG conformance claim.' }, null, 2) + '\n');
  await rm(dataDir, { recursive: true, force: true });
}
if (!process.exitCode) process.exitCode = results.some(r => r.status === 'fail') ? 1 : results.some(r => r.status === 'unknown') ? 2 : 0;
