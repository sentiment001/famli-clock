# FAMLI Clock SEO: what was pushed, and what to check

Built 21 September 2026 for `famliclock.com`. Target repo `sentiment001/famli-clock`,
branch `main`, which auto-deploys to Vercel.

**This session did not push it.** It could clone and read the repo, but the sandbox proxy
refused every write, with and without a personal access token: *"sentiment001/famli-clock is
not in this session's authorized repository set"*. The work is committed locally and shipped
as a git bundle; APPLY.md has the three ways to land it.

It is one commit, deliberately, so there is no broken intermediate state: Vercel deploys the
whole thing or none of it.

If you are the session that pushes this, read section 1 first.

---

## 1. index.html is patched, not rewritten

`index.html` carries the calculator, the engine, the print report and the email capture. None
of that was touched. The file in `site/` was produced by `source/patch_index.py` from the
`index.html` live at commit `9aa35dc` (sha256 `68308de5…`, 123,593 bytes).

Nine things changed, all by string replacement, every anchor asserted:

1. `<title>`
2. meta description, keywords, `og:title`, `og:description`, `twitter:title`
3. the JSON-LD `@graph`, replaced with a **superset**: the original `WebApplication` node and
   all four original FAQ entries survive word for word, plus four new FAQ entries, an
   `Organization` and a `WebSite` node. The patcher asserts no original question was dropped.
4. a `<link>` to `/famli_pages.css`
5. the static `<h1>`
6. **the five phase headline strings in the app script**
7. a nav above the masthead
8. a Colorado disambiguation line under the sub headline
9. a crawlable content block between the CTA card and the email-capture comment

### THE SIX H1 COPIES ARE THE TRAP

There is **one** `<h1>` element in the markup. The app then overwrites its text on every load
from a five-entry phase table:

```js
$('h1').textContent = h[0];   // h comes from a { P1_runway: [...], P2_compressed: [...] } map
```

The phase advances five times between now and 2028, so what a crawler indexes depends on the
day it crawls. **Before this work, three of the five phase headlines did not contain the words
"Maryland FAMLI" at all**:

- P2 was "The private plan window is closing. Here is what still fits."
- P3 was "Your employees need this notice in writing before January."
- P4 was "Contributions are live. Here is your first payment and what it is."

P2 begins **29 September 2026**. Left alone, the site's H1 would have stopped naming its own
primary keyword eight days after this build, silently, and the homepage retitle would have
looked like it had been done.

All six now lead with "Maryland FAMLI calculator". `patch_index.py` asserts on all six and
refuses to write a file where any is missing. `browser_qa.js` additionally loads the page,
waits for the app to run, and checks the H1 **after** the script has painted.

### If main has moved since 9aa35dc

Do not paste `site/index.html` over a newer file. Re-run the patcher against the current one:

```bash
python3 source/patch_index.py --in index.html --out index.html
```

It works by string replacement against anchors it asserts, so it either applies cleanly to a
newer file or tells you exactly which anchor moved. It never half-applies.

---

## 2. Files, and where they go

All at repo root, alongside `index.html`.

| File | New or replace | Notes |
|---|---|---|
| `index.html` | Replace | See section 1 |
| `famli_pages.css` | New | Base tokens duplicated from the inline sheet, plus the new page styles |
| `contribution-rate-2027.html` | New | |
| `small-employer.html` | New | |
| `out-of-state-employees.html` | New | |
| `employee-notice.html` | New | |
| `private-plan-declaration-of-intent.html` | New | Time-critical, see section 5 |
| `deadlines-2027.html` | New | |
| `registration.html` | New | |
| `payroll-providers.html` | New | Written to Lane 1 |
| `sitemap.xml` | New | |
| `robots.txt` | New | Check it actually serves, see section 6 |
| `llms.txt` | New | |
| `vercel.json` | Edit, one key | `Cache-Control` added to the catch-all header block |
| `seo/` | New folder | The generator, the QA and these three docs |

`famli_pages.css` duplicates `:root`, the reset, `body`, `.wrap`, headings, `.card`, `.note`,
`.src`, `.flag`, `table.pace`, `details.disc`, `.cta`, `.bookwrap` and `.foot` from the inline
stylesheet in `index.html`. **That is deliberate.** The content pages carry no inline block,
and without `:root` every `var(--ink)` resolves to nothing, which renders the call-to-action
button invisible. Values are identical, so the homepage loading both changes nothing there.
**If the inline stylesheet changes, re-extract the block above the `BASE ENDS` marker.**

### Why the stylesheet link sits BEFORE the inline `<style>`

Because the inline block contains the whole `@media print` section, and the printed CFO report
is measured to the millimetre. A later sheet redefining `.card` at equal specificity would win
the cascade and could reflow a print sheet. Loading `famli_pages.css` first means the inline
rules win every tie and the external sheet only supplies selectors the content pages
introduce. Do not move it.

---

## 3. vercel.json

`cleanUrls: true` and `trailingSlash: false` were already there, which is what the
extensionless canonicals and internal links need. One key was added: `Cache-Control:
public, max-age=300, must-revalidate` on the catch-all `/(.*)` header block, so the October
wage cap change propagates off the new pages as fast as it does off the homepage. The
pre-existing `/`-only cache entry was left alone.

---

## 4. What to verify on the live site

Cache-bust through Cloudflare with `?v=1`.

1. **The tool still works.** Paste 12 / 12 / 780000 / biweekly. It should return a small
   employer at 0.45% and a 2027 total of **$3,510.00**.
2. **The H1 after the app has finished loading** reads "Maryland FAMLI calculator: …". Check
   it a second time after 29 September, when phase 2 starts, because that is a different
   string.
3. **The print report is unchanged.** Ctrl-P on a result. Five sheets without a private plan,
   six or seven with one. The nav, the disambiguation line and the new content block must all
   be absent from the print preview.
4. `/contribution-rate-2027` resolves **without** the extension, and renders with styling.
5. `/sitemap.xml`, `/robots.txt` and `/llms.txt` all serve.
6. The nav appears above the masthead and the new content appears below the dark CTA card.

If anything is wrong, reverting `index.html` alone restores the previous behaviour. Every
other file is additive.

---

## 5. Three things to do that are not in this push

**1. Google Search Console.** Not verifiable from a build session. Add the property if it does
not exist and submit `sitemap.xml` on day one. Nothing here ranks until Google knows the pages
exist. This is the single highest-value follow-up and it takes ten minutes.

**2. Cloudflare is serving its own robots.txt.** As of 21 September 2026,
`famliclock.com/robots.txt` returns Cloudflare's managed content-signals file, not a file from
this repo. **The `robots.txt` in this push may never be seen.** After deploying, fetch it and
confirm it is the one from this repo. Then check the Cloudflare dashboard for AI crawler
control on the zone. If a content signal is set to no, or AI crawler blocking is on, the
entire GEO effort fails no matter how good the pages are. This is the same issue flagged for
nycclock.com and it is not theoretical here; it was observed.

**3. Repurpose the private plan page after 15 November 2026.** Until then it reads for an
employer deciding. After the window closes the honest version is "you missed the Declaration
of Intent: here is what that costs and what to do now", pointing at the 1 October 2027
application. The page already carries an *If you miss 15 November 2026* section, which is the
skeleton; promote it and demote the five-stage critical path. Do not leave a live countdown to
a passed date.

---

## 6. The October wage cap update, which now has one more step

The repo README's procedure is unchanged and still correct: four values in two files
(`index.html` `CONFIG` and `famli_ref.py`), regenerate `fixture_table.txt`, regenerate
`version.txt`, run all three harnesses.

**Add these two steps at the end**, or the SEO pages will quietly keep quoting the old cap:

```bash
node seo/run_examples.js index.html > seo/examples.json   # re-read the engine
python3 seo/build.py --out .                              # rebuild the 8 content pages
python3 seo/qa.py --dir .                                 # fails if a page and CONFIG disagree
node seo/browser_qa.js .                                  # layout, in real Chromium
```

`index.html` needs **no** rebuild for the cap: it deliberately carries no cap literal, and its
worked examples use wages nowhere near the cap so the figures do not move. That is enforced by
`run-dom.js`, which already fails if a formatted cap literal appears anywhere in its source.
`qa.py` enforces the equivalent on the content pages by cross-checking every cap figure
against `examples.json`, which is read from the engine.

Every money figure on every page comes from `run_examples.js` running the shipped engine out
of `index.html`. **Nothing on these pages is hand-calculated.** If you find yourself typing a
dollar amount into a content module, stop.

---

## 7. What is deliberately not here

So a later session does not treat a decision as an oversight.

**The calculator is not embedded on the eight content pages.** The SEO plan asked for it. It
was not done, and this is the one place this build departs from the plan.

The engine, the form and the render layer are 123KB of `index.html` and the repo's stated
design principle is that there is exactly one copy of them: *"There is no separate engine file
that can drift out of step with the page."* Embedding the engine on eight more pages creates
nine copies to update every October and nine chances for one of them to quietly disagree with
the others about the wage cap. That is the exact failure mode the repo's own `run-dom.js`
guard exists to prevent. Instead every page carries a styled call-to-action card, above the
fold and again at the end, that links to the calculator. If the click-through from content
pages into the tool turns out to be poor in Search Console, the right fix is a small
iframe-free embed of the form alone that posts to `/`, not nine copies of the engine.

**No employee-side page.** Benefits start in 2028 and the employee side is the Department's
job. Building it now attracts traffic that cannot convert.

**No Colorado comparison page.** It would attract exactly the traffic the disambiguation line
exists to repel.

**No 2028 rate, and no 2027 wage cap.** Neither is published. See FACTS_REGISTER.md.

**No notice template.** MDOL has not released one. The pages say so and say why writing your
own is a risk taken for nothing.

**No countdown to the employee notice date.** It is employer-specific, per the standing
project correction, and the calculator derives it. A site-wide countdown to 1 December would
reintroduce exactly the error the project already fixed once.

---

## 8. QA that ran, and what it caught

| Suite | Checks | Result |
|---|---|---|
| `run-fixtures.js` against the patched index.html | 32 | pass |
| `run-boundaries.js` against the patched index.html | 58 | pass |
| `run-dom.js` against the patched index.html | 162 | pass |
| `seo/qa.py`, structure, JSON-LD, links, sitemap, robots, house style | 499 | pass |
| `seo/browser_qa.js`, real Chromium at 1280/1024/768/390 plus the live tool | 371 | pass |

Three real defects were caught by running these rather than by reading:

1. **`run-dom.js` caught the wage cap literal.** The first draft of the homepage block printed
   `$184,500` and "SSA publishes the 2027 Social Security wage cap" in static HTML. The repo's
   own guard failed the build. Both were removed; the homepage now carries no cap literal at
   all. The guard was right and was not weakened.
2. **Chromium caught a horizontal scrollbar on the homepage at every width.** The
   sole-proprietor worked example put a full sentence in a value cell carrying
   `white-space:nowrap`, which made one table 822px wide and gave the whole page a horizontal
   scroll at 390px. Fixed by class, not by eyeballing: value cells over 60 characters render
   as wrapping text cells, and every worked-example table now sits in a scroll wrapper.
3. **`qa.py` caught a title that did not lead with "Maryland FAMLI"** on the out-of-state page.

The screenshots taken during QA are in `seo/qa-shots/`.
