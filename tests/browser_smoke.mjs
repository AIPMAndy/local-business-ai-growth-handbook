#!/usr/bin/env node
/**
 * Browser-level checks of the real generated site (NOT physical mobile devices).
 * Validates local data, calculation, search, export and PDF download.
 */
import assert from 'node:assert/strict';
import { mkdir } from 'node:fs/promises';
import { chromium } from 'playwright';

const base = (process.env.SITE_URL || 'http://127.0.0.1:8766/').replace(/\/?$/, '/');
await mkdir('qa/browser', { recursive: true });
const browser = await chromium.launch({ headless: true });
const results = [];
try {
  for (const width of [360, 390, 1280]) {
    const context = await browser.newContext({ viewport: { width, height: 820 }, locale: 'zh-CN' });
    const page = await context.newPage();
    const errors = [];
    page.on('pageerror', e => errors.push(e.message));
    const response = await page.goto(base, { waitUntil: 'networkidle' });
    assert.equal(response.status(), 200, 'Homepage HTTP 200');
    assert.equal(await page.locator('h1').count(), 1);
    assert.equal(await page.locator('#clearChapterSearch').count(), 1);
    const chapters = await page.locator('.chapter-card').count();
    assert.equal(chapters, 26, 'Keep all 26 chapters');
    await page.locator('#chapterSearch').fill('no-such-chapter-0000');
    assert.equal(await page.locator('.chapter-card:visible').count(), 0);
    await page.locator('#clearChapterSearch').click();
    assert.equal(await page.locator('#chapterSearch').inputValue(), '');
    assert.equal(await page.locator('.chapter-card:visible').count(), 26);

    await page.evaluate(() => {
      Object.defineProperty(navigator, 'clipboard', {
        configurable: true,
        value: { writeText: async t => { window.__copiedInQA = t; } },
      });
    });
    await page.locator('button[data-copy="AIPMAndy"]').first().click();
    assert.equal(await page.evaluate(() => window.__copiedInQA), 'AIPMAndy');
    assert.match(await page.locator('#toast').textContent(), /已复制/);
    const box = await page.evaluate(() => ({
      innerWidth: window.innerWidth,
      maxWidth: Math.max(document.body.scrollWidth, document.documentElement.scrollWidth),
    }));
    assert.ok(box.maxWidth <= box.innerWidth + 1, 'Horizontal overflow at ' + width + ': ' + JSON.stringify(box));
    assert.deepEqual(errors, [], 'No page errors');
    await page.screenshot({ path: 'qa/browser/local-home-' + width + '.png', fullPage: true });
    results.push({ width, chapters, copiedWechat: true, horizontalOverflow: false });
    await context.close();
  }

  const context = await browser.newContext({ viewport: { width: 390, height: 820 }, acceptDownloads: true });
  const page = await context.newPage();
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));

  await page.goto(base + 'plan.html');
  assert.equal(await page.locator('input[data-day]').count(), 30);
  await page.locator('input[data-day="1"]').check();
  await page.reload();
  assert.equal(await page.locator('input[data-day="1"]').isChecked(), true);
  assert.match(await page.locator('#doneCount').textContent(), /1\s*\/\s*30/);
  const progressDownload = page.waitForEvent('download');
  await page.locator('#exportProgress').click();
  assert.match((await progressDownload).suggestedFilename(), /\.json$/);
  page.once('dialog', dialog => dialog.accept());
  await page.locator('#resetProgress').click();
  assert.equal(await page.locator('input[data-day="1"]').isChecked(), false);
  await page.screenshot({ path: 'qa/browser/local-plan-390.png', fullPage: true });

  await page.goto(base + 'tools.html');
  const values = { revenue:'500', variable:'200', cpl:'20', leads:'10', visits:'6',
    orders:'3', fixed:'100', hours:'2', hourly:'50' };
  for (const [field, value] of Object.entries(values)) await page.locator('#' + field).fill(value);
  const model = await page.evaluate(() => window.__localBusinessCalc);
  assert.deepEqual(model.result.error, []);
  assert.equal(model.result.net, 500, 'Net contribution formula regression');
  await page.locator('#visits').fill('11');
  assert.match(await page.locator('#calcErrors').textContent(), /到店数不能大于合格咨询数/);
  await page.locator('#resetCalc').click();
  assert.equal(await page.locator('#revenue').inputValue(), '400');
  assert.equal(await page.locator('#calcErrors').textContent(), '');
  const calcDownload = page.waitForEvent('download');
  await page.locator('#exportCalc').click();
  assert.match((await calcDownload).suggestedFilename(), /\.txt$/);
  await page.screenshot({ path: 'qa/browser/local-tools-390.png', fullPage: true });

  const pdfResponse = await page.request.get(base + 'downloads/local-business-ai-growth-handbook-guide.pdf');
  assert.equal(pdfResponse.status(), 200);
  const pdf = await pdfResponse.body();
  assert.equal(pdf.subarray(0, 4).toString(), '%PDF');
  assert.deepEqual(errors, []);
  console.log(JSON.stringify({ status: 'PASS', results, calculator: '500 yuan from teaching inputs', pdfBytes: pdf.length }, null, 2));
  await context.close();
} finally {
  await browser.close();
}
