import { chromium } from 'playwright';
import assert from 'node:assert/strict';
import { createServer } from 'node:http';
import { readFile, mkdir, writeFile } from 'node:fs/promises';
import { resolve, join, dirname } from 'node:path';
import { createHash } from 'node:crypto';
import os from 'node:os';

const app = resolve(process.argv[2] || '../fixtures/tracker');
const output = resolve(process.argv[3] || './runs/current');
await mkdir(dirname(output), { recursive: true });
await mkdir(output); // Never overwrite an earlier observation run.
const files = { '/': ['index.html', 'text/html'], '/app.js': ['app.js', 'text/javascript'], '/style.css': ['style.css', 'text/css'] };
const server = createServer(async (request, response) => {
  const file = files[request.url];
  if (!file) { response.writeHead(404); response.end(); return; }
  response.setHeader('Content-Type', file[1]);
  response.setHeader('Cache-Control', 'no-store');
  response.end(await readFile(join(app, file[0])));
});
await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
const base = `http://127.0.0.1:${server.address().port}`;
const browser = await chromium.launch({ channel: 'chrome', headless: true }).catch(async error => {
  await writeFile(join(output, 'infrastructure.json'), JSON.stringify({
    kind: 'infrastructure_failure', captured_at: new Date().toISOString(), error: String(error),
    limitation: 'Browser did not launch; no application result was observed.'
  }, null, 2) + '\n');
  await new Promise(resolve => server.close(resolve));
  throw error;
});
const KEY = 'task-tracker-v1';
const results = [];
const snapshot = page => page.evaluate(key => ({
  feedback: document.querySelector('#feedback')?.textContent,
  input: document.querySelector('#title')?.value,
  visibleCount: document.querySelectorAll('#tasks li').length,
  storedRaw: localStorage.getItem(key),
  stored: JSON.parse(localStorage.getItem(key) || '[]'),
}), KEY);
const add = async (page, title = 'Plan the next step') => {
  await page.locator('#title').fill(title);
  await page.locator('#add').click();
  await page.waitForFunction(() => document.querySelector('#feedback').textContent !== 'Adding…');
};
const edit = async (page, note = 'Review with the team') => {
  const item = page.locator('#tasks li').first();
  await item.locator('textarea').fill(note);
  await item.locator('input[type=checkbox]').check();
  await item.getByRole('button', { name: 'Save changes' }).click();
  await page.waitForFunction(() => document.querySelector('#feedback').textContent !== 'Saving…');
};
const denyWrites = page => page.evaluate(key => {
  const original = Storage.prototype.setItem;
  Storage.prototype.setItem = function(name, value) {
    if (name === key) throw new DOMException('Test storage unavailable', 'QuotaExceededError');
    return original.call(this, name, value);
  };
}, KEY);
async function scenario(id, criteria, steps, run) {
  const context = await browser.newContext({ viewport: { width: 1000, height: 800 } });
  await context.tracing.start({ screenshots: true, snapshots: true, sources: true });
  const page = await context.newPage();
  const errors = [];
  page.on('pageerror', error => errors.push(String(error)));
  const result = { id, criteria, steps, started_at: new Date().toISOString() };
  try {
    await page.goto(base);
    await run(page, context, result);
    result.status = 'pass';
  } catch (error) {
    result.status = 'fail';
    result.error = String(error);
  } finally {
    const active = context.pages().find(p => !p.isClosed());
    if (active) {
      result.observation = await snapshot(active).catch(error => ({ error: String(error) }));
      await active.screenshot({ path: join(output, `${id}.png`), fullPage: true });
    }
    result.runtime_errors = errors;
    await context.tracing.stop({ path: join(output, `${id}.trace.zip`) });
    await context.close();
    results.push(result);
    console.log(`${id}: ${result.status}`);
  }
}
try {
  await scenario('create-readback', ['F01', 'F04'], ['Submit a trimmed Unicode/punctuation title.', 'Compare visible and stored values.'], async page => {
    await add(page, '  Plan café <draft>  ');
    const state = await snapshot(page);
    assert.equal(state.stored.length, 1);
    assert.equal(state.stored[0].title, 'Plan café <draft>');
    assert.equal(state.visibleCount, 1);
  });
  await scenario('save-readback', ['F01', 'F03'], ['Create one record.', 'Edit note and Completed; save.', 'Read committed values independently of confirmation.'], async page => {
    await add(page);
    await edit(page);
    const state = await snapshot(page);
    assert.equal(state.stored[0].note, 'Review with the team', 'Saved note must match the requested edit');
    assert.equal(state.stored[0].done, true);
  });
  await scenario('refresh', ['F02'], ['Create a uniquely titled record.', 'Read store; refresh same origin/profile.', 'Compare loaded records and identities.'], async page => {
    await add(page, 'Retain across refresh');
    const before = (await snapshot(page)).stored;
    await page.reload();
    const after = await snapshot(page);
    assert.deepEqual(after.stored, before);
    assert.equal(after.visibleCount, 1, 'Refresh must load the committed record');
    assert.equal(await page.locator('h3').first().textContent(), before[0].title);
  });
  await scenario('reopen', ['F02'], ['Create a record.', 'Close app tab; reopen same origin in same browser context.', 'Verify loaded record.'], async (page, context) => {
    await add(page, 'Retain across app reopen');
    await page.close();
    const reopened = await context.newPage();
    await reopened.goto(base);
    assert.equal((await snapshot(reopened)).visibleCount, 1);
  });
  await scenario('rapid-repeat', ['F05'], ['Fill one intention.', 'Invoke form submission twice before pending work settles.', 'Count committed identities.'], async page => {
    await page.locator('#title').fill('One intention');
    await page.evaluate(() => { const form = document.querySelector('form'); form.requestSubmit(); form.requestSubmit(); });
    await page.waitForTimeout(500);
    assert.equal((await snapshot(page)).stored.length, 1, 'Repeated pending submission must create one record');
  });
  await scenario('intentional-repeat', ['F05'], ['Submit a title.', 'After completion, submit the same title as a new intention.', 'Verify two distinct IDs.'], async page => {
    await add(page, 'Repeat intentionally');
    await add(page, 'Repeat intentionally');
    const { stored } = await snapshot(page);
    assert.equal(stored.length, 2);
    assert.equal(new Set(stored.map(task => task.id)).size, 2);
  });
  await scenario('title-boundaries', ['F04'], ['Reject empty/whitespace and programmatic 81-character title.', 'Accept exactly 80 characters.'], async page => {
    for (const title of ['', '   ', 'a'.repeat(81)]) {
      await page.locator('#title').evaluate((input, value) => { input.value = value; }, title);
      assert.equal((await page.locator('#title').inputValue()).length, title.length, 'Probe must actually inject the intended boundary value');
      await page.evaluate(() => document.querySelector('form').requestSubmit());
      await page.waitForTimeout(300);
      assert.equal((await snapshot(page)).stored.length, 0);
    }
    await add(page, 'a'.repeat(80));
    assert.equal((await snapshot(page)).stored.length, 1);
  });
  await scenario('note-boundaries', ['F04'], ['Save exactly 500 note characters.', 'Attempt 501 through a programmatic value.', 'Verify rejection preserves the previous note.'], async page => {
    await add(page);
    await edit(page, 'n'.repeat(500));
    assert.equal((await snapshot(page)).stored[0].note.length, 500);
    await page.locator('textarea').evaluate(el => { el.value = 'n'.repeat(501); });
    await page.getByRole('button', { name: 'Save changes' }).click();
    await page.waitForTimeout(300);
    const state = await snapshot(page);
    assert.equal(state.stored[0].note.length, 500);
    assert.ok(!/^Changes saved/.test(state.feedback));
  });
  await scenario('create-storage-failure', ['F03'], ['Create an existing task.', 'Reject storage writes, then add another task.', 'Verify no false success, no previous-data loss, and retained input.'], async page => {
    await add(page, 'Keep existing');
    const before = (await snapshot(page)).stored;
    await denyWrites(page);
    await add(page, 'Keep this draft');
    const state = await snapshot(page);
    assert.deepEqual(state.stored, before);
    assert.equal(state.input, 'Keep this draft');
    assert.match(state.feedback, /could not|unable|failed|not saved/i);
    assert.equal(state.visibleCount, 1);
  });
  await scenario('save-storage-failure', ['F03'], ['Create a task.', 'Reject storage writes; edit and save.', 'Compare feedback, old committed data and retained draft.'], async page => {
    await add(page);
    const before = (await snapshot(page)).stored;
    await denyWrites(page);
    await edit(page, 'Keep this unsaved note');
    const state = await snapshot(page);
    assert.deepEqual(state.stored, before);
    assert.match(state.feedback, /could not|unable|failed|not saved/i);
    assert.equal(await page.locator('textarea').inputValue(), 'Keep this unsaved note');
  });
  await scenario('feedback-timing', ['F03'], ['Start save.', 'If success is visible, independently confirm the new value already committed.', 'Wait for completion and compare again.'], async page => {
    await add(page);
    await page.locator('textarea').fill('Confirmed only after commit');
    await page.getByRole('button', { name: 'Save changes' }).click();
    let state = await snapshot(page);
    if (/^Changes saved/.test(state.feedback)) assert.equal(state.stored[0].note, 'Confirmed only after commit');
    await page.waitForTimeout(300);
    state = await snapshot(page);
    assert.equal(state.stored[0].note, 'Confirmed only after commit');
  });
  await scenario('save-repeat', ['F01', 'F05'], ['Create and edit one record.', 'Activate save twice rapidly.', 'Verify one record with correct fields.'], async page => {
    await add(page);
    await page.locator('textarea').fill('One final value');
    await page.getByRole('button', { name: 'Save changes' }).evaluate(button => { button.click(); button.click(); });
    await page.waitForTimeout(500);
    const state = await snapshot(page);
    assert.equal(state.stored.length, 1);
    assert.equal(state.stored[0].note, 'One final value');
  });
  const hashes = {};
  for (const name of ['index.html', 'app.js', 'style.css', 'README.md']) hashes[name] = createHash('sha256').update(await readFile(join(app, name))).digest('hex');
  await writeFile(join(output, 'results.json'), JSON.stringify({
    captured_at: new Date().toISOString(), app_hashes: hashes,
    environment: { browser: browser.version(), channel: 'chrome', node: process.version, os: os.platform(), base_url: base, viewport: '1000x800', isolation: 'Fresh context for each scenario; only fixture localStorage key inspected.' },
    results, limitation: 'Executable workflow checks on a seeded local fixture, not a controlled skill effectiveness study. F06 and other groups unassessed.'
  }, null, 2) + '\n');
  process.exitCode = results.some(result => result.status === 'fail') ? 1 : 0;
} finally {
  await browser.close();
  await new Promise(resolve => server.close(resolve));
}
