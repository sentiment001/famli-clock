/* Real-Chromium QA for the famliclock.com SEO build.

   Serves ../site over http (the pages use root-relative links, and file:// would
   break every one of them), then for each page at four widths:
     - loads it, fails on any page error or console error
     - asserts no horizontal overflow
     - asserts the h1, the nav and the run-the-calculator button are visible
     - measures the rendered height so a collapsed layout shows up as a number
   Then drives the calculator on the patched index.html and asserts the engine
   still produces a result, because that is the only thing on the site that can
   actually break.

   Usage:  node browser_qa.js [siteDir]
*/
'use strict';
const http = require('http');
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const SITE_DIR = path.resolve(process.argv[2] || path.join(__dirname, '..', 'site'));
const WIDTHS = [1280, 1024, 768, 390];
const PAGES = ['/', '/contribution-rate-2027', '/small-employer', '/out-of-state-employees',
  '/employee-notice', '/private-plan-declaration-of-intent', '/deadlines-2027',
  '/registration', '/payroll-providers'];

const TYPES = { '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8',
  '.xml': 'application/xml', '.txt': 'text/plain; charset=utf-8' };

let pass = 0; const fails = [];
function check(label, ok, detail) {
  if (ok) { pass++; } else { fails.push(label + (detail ? '  [' + detail + ']' : '')); }
}

function serve() {
  return new Promise((resolve) => {
    const server = http.createServer((req, res) => {
      let p = decodeURIComponent(req.url.split('?')[0]);
      if (p === '/') { p = '/index.html'; }
      // cleanUrls: true in vercel.json, so /foo serves foo.html
      let file = path.join(SITE_DIR, p);
      if (!fs.existsSync(file) && fs.existsSync(file + '.html')) { file += '.html'; }
      if (!fs.existsSync(file) || fs.statSync(file).isDirectory()) {
        res.writeHead(404); res.end('not found: ' + p); return;
      }
      res.writeHead(200, { 'Content-Type': TYPES[path.extname(file)] || 'application/octet-stream' });
      res.end(fs.readFileSync(file));
    });
    server.listen(0, '127.0.0.1', () => resolve(server));
  });
}

(async () => {
  const server = await serve();
  const base = 'http://127.0.0.1:' + server.address().port;
  const browser = await chromium.launch({ executablePath: undefined });
  const ctx = await browser.newContext();

  for (const w of WIDTHS) {
    for (const p of PAGES) {
      const page = await ctx.newPage();
      await page.setViewportSize({ width: w, height: 900 });
      const problems = [];
      page.on('pageerror', (e) => problems.push('pageerror: ' + e.message));
      page.on('console', (m) => {
        if (m.type() === 'error' && !/clarity|fonts\.g|net::ERR/i.test(m.text())) {
          problems.push('console: ' + m.text());
        }
      });
      const resp = await page.goto(base + p, { waitUntil: 'load' });
      await page.waitForTimeout(220);

      const tag = p + ' @' + w;
      check(tag + ' responds 200', resp && resp.status() === 200, resp && String(resp.status()));
      check(tag + ' no page or console errors', problems.length === 0, problems.slice(0, 2).join(' | '));

      const m = await page.evaluate(() => ({
        scrollW: document.documentElement.scrollWidth,
        clientW: document.documentElement.clientWidth,
        height: document.body.scrollHeight,
        h1: (document.querySelector('h1') || {}).textContent || '',
        h1count: document.querySelectorAll('h1').length,
        navLinks: document.querySelectorAll('nav.topbar a.nl').length,
        runBtn: !!document.querySelector('a.run') || !!document.querySelector('#form'),
        tables: document.querySelectorAll('table').length,
        overflowing: [].filter.call(document.querySelectorAll('table,pre,img,div'),
          (el) => el.scrollWidth > el.clientWidth + 2 &&
                  getComputedStyle(el).overflowX === 'visible').length,
        /* a.run is a flat colour, a.book is a gradient, so a gradient counts as
           painted too. Either way a transparent button means :root never resolved. */
        capBtnPainted: (function () {
          const a = document.querySelector('a.run') || document.querySelector('a.book');
          if (!a) return false;
          const cs = getComputedStyle(a);
          return cs.backgroundColor !== 'rgba(0, 0, 0, 0)' || cs.backgroundImage !== 'none';
        })()
      }));

      check(tag + ' no horizontal page scroll', m.scrollW <= m.clientW + 1,
        m.scrollW + ' > ' + m.clientW);
      check(tag + ' exactly one h1', m.h1count === 1, String(m.h1count));
      check(tag + ' h1 names Maryland FAMLI', /Maryland FAMLI/.test(m.h1), m.h1.slice(0, 60));
      check(tag + ' nav has 9 links', m.navLinks === 9, String(m.navLinks));
      check(tag + ' calculator entry point present', m.runBtn === true);
      check(tag + ' no element overflows its box', m.overflowing === 0, String(m.overflowing));
      check(tag + ' renders taller than 900px', m.height > 900, String(m.height));
      check(tag + ' CSS variables resolved (button is painted)', m.capBtnPainted === true);

      if (w === 1280 && p === '/') {
        await page.screenshot({ path: path.join(SITE_DIR, '..', 'qa-shots', 'home-1280.png'),
          fullPage: false }).catch(() => {});
      }
      await page.close();
    }
  }

  // ---- the calculator still works on the patched homepage -------------------
  {
    const page = await ctx.newPage();
    await page.setViewportSize({ width: 1280, height: 1000 });
    const errs = [];
    page.on('pageerror', (e) => errs.push(e.message));
    await page.goto(base + '/?d=2026-09-21', { waitUntil: 'load' });
    await page.waitForTimeout(250);

    const h1Before = await page.textContent('h1');
    check('tool: h1 after the app has run still names Maryland FAMLI',
      /Maryland FAMLI/.test(h1Before), h1Before);
    check('tool: h1 after the app has run says calculator',
      /calculator/i.test(h1Before), h1Before);

    await page.fill('#md', '12');
    await page.fill('#ein', '12');
    await page.fill('#pay', '780000');
    await page.selectOption('#freq', 'biweekly');
    await page.click('button.go');
    await page.waitForTimeout(400);

    const res = await page.evaluate(() => {
      const out = document.getElementById('out');
      return { text: out ? out.textContent : '', cards: out ? out.querySelectorAll('.card').length : 0 };
    });
    check('tool: the engine rendered a result', res.cards >= 3, 'cards=' + res.cards);
    check('tool: the small-employer total is $3,510.00',
      res.text.indexOf('$3,510.00') !== -1);
    check('tool: the result names the small employer band',
      /small employer/i.test(res.text));
    check('tool: no page errors while computing', errs.length === 0, errs.slice(0, 2).join(' | '));

    // the new prose block must still be in the DOM after the app re-renders
    const proseAfter = await page.evaluate(() =>
      !!document.getElementById('about-famli') &&
      document.querySelectorAll('nav.topbar a.nl').length);
    check('tool: the crawlable block and nav survive a re-render', proseAfter === 9,
      String(proseAfter));

    // print stylesheet still hides the new furniture
    await page.emulateMedia({ media: 'print' });
    await page.waitForTimeout(120);
    const printed = await page.evaluate(() => {
      const vis = (sel) => {
        const el = document.querySelector(sel);
        if (!el) return 'missing';
        return getComputedStyle(el).display;
      };
      return { nav: vis('nav.topbar'), prose: vis('#about-famli'),
               disambig: vis('p.disambig'), cover: vis('.cover') };
    });
    check('print: nav is hidden', printed.nav === 'none', printed.nav);
    check('print: the crawlable block is hidden', printed.prose === 'none', printed.prose);
    check('print: the disambiguation line is hidden', printed.disambig === 'none', printed.disambig);
    check('print: the report cover still renders', printed.cover !== 'none', printed.cover);
    await page.close();
  }

  await browser.close();
  server.close();

  console.log('\n%d passed, %d failed', pass, fails.length);
  fails.forEach((f) => console.log('  FAILED: ' + f));
  process.exit(fails.length ? 1 : 0);
})();
