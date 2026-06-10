// Drives the live site through the full journey and saves key frames.
// Requires the server running with VENICE_API_KEY set.
import { chromium } from 'playwright';
import fs from 'fs';

const PORT = process.env.PORT || '3010';
const URL  = `http://localhost:${PORT}`;
const OUT  = 'frames';
fs.rmSync(OUT, { recursive: true, force: true });
fs.mkdirSync(OUT, { recursive: true });

const order = [];
async function snap(page, name) {
  await page.screenshot({ path: `${OUT}/${name}.png` });
  order.push(name);
  console.log('  ✓', name);
}
const top = page => page.evaluate(() => window.scrollTo({ top: 0 }));
const center = (page, sel) => page.evaluate(s => document.querySelector(s)?.scrollIntoView({ block: 'center' }), sel);

const browser = await chromium.launch({ channel: 'chrome', headless: true });
const ctx = await browser.newContext({ viewport: { width: 900, height: 900 }, deviceScaleFactor: 2 });
const page = await ctx.newPage();

console.log('navigating', URL);
await page.goto(URL, { waitUntil: 'networkidle' });
await page.waitForTimeout(1500); // banner + fonts + canvas settle

// ── INTRO ──
await top(page);
await snap(page, '01_intro');

// ── TRIAL I ──
await page.click('button:has-text("Begin the Fable")');
await page.waitForTimeout(900);
await top(page);
await snap(page, '02_trial1');

await page.click('.chip:has-text("What makes you")');
await center(page, '.live-console');
await page.waitForTimeout(500);
await snap(page, '03_console');

await page.click('#s1ask');
await page.waitForTimeout(750);                 // catch the progress bar mid-fill
await center(page, '#s1gen');
await snap(page, '04_generating');

await page.waitForFunction(
  () => { const o = document.querySelector('#s1out'); return o && o.style.display !== 'none' && o.innerText.trim().length > 40; },
  { timeout: 60000 }
);
await page.waitForTimeout(900);
await page.evaluate(() => document.querySelector('#s1out').scrollIntoView({ block: 'start' }));
await snap(page, '05_answer');

await center(page, '#reward1');
await page.waitForTimeout(500);
await snap(page, '06_treasure1');

// ── TRIAL II ──
await page.click('button:has-text("Enter the Second Trial")');
await page.waitForTimeout(900);
await top(page);
await snap(page, '07_trial2');

await page.click('#vbM');                        // lift the veil → Mythos
await page.waitForTimeout(700);
await center(page, '#veilPanel');
await snap(page, '08_mythos');

// ── FINALE ──
await page.click('button:has-text("Unseal the Treasures")');
await page.waitForTimeout(1300);
await top(page);
await snap(page, '09_finale');

await center(page, '.gallery');
await page.waitForTimeout(500);
await snap(page, '10_treasures');

await page.evaluate(() => window.scrollBy(0, 760));
await page.waitForTimeout(400);
await snap(page, '11_treasures2');

await browser.close();
fs.writeFileSync(`${OUT}/order.json`, JSON.stringify(order));
console.log('captured', order.length, 'frames');
