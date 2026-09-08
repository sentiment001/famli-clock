# famliclock.com

One self-contained page. Deploy the folder to Vercel. No build step, no environment
variables, no external files to go missing.

## Files

| File | What it is |
|---|---|
| `index.html` | The whole site. Engine, CSS and app JS all inline. |
| `version.txt` | sha256, byte count and build stamp of the deployed `index.html`. Fetch it to confirm which build is live. Regenerate on every push. |
| `fixture_table.txt` | The 28 expected outputs, regenerated from `famli_ref.py`. |
| `fixtures.py` | The 28 fixture definitions. |
| `famli_ref.py` | Independent reference engine. Written from the spec without reading `index.html`. |
| `load-engine.js` | Pulls the engine out of `index.html` so tests run on shipped bytes. |
| `run-fixtures.js` | The 28 spec fixtures, diffed against `fixture_table.txt`. |
| `run-boundaries.js` | Phase edges, notice versus payment direction, holiday and countdown guards. |
| `run-dom.js` | Renders the real page in jsdom and asserts the outputs are on screen. |
| `vercel.json` | Headers and a short cache, so the October wage cap change propagates. |

`index.html` has no dependency on any sibling file. Open it from disk, email it, or
serve it from anywhere and it works.

**Two external requests, both non-blocking.** The Google Fonts stylesheet, and if that
fails the page falls back to Georgia and the system sans. And Microsoft Clarity, which
is skipped entirely on `file://` so the page still opens from disk with no network at
all. Nothing in the calculation depends on either.

## Run the tests

```
npm install jsdom
node run-fixtures.js     # 28 fixtures
node run-boundaries.js   # 42 date and phase checks
node run-dom.js          # 120 render checks
```

All three read `index.html` directly. There is no separate engine file that can drift
out of step with the page.

## Email capture

**It is built and it is live.** Web3Forms, access key in `index.html`, delivery to
mash@hirecmo.io. It fires only on an explicit click with a valid address and the
consent box ticked, and it carries a versioned consent string (`CONSENT-v1.0`).

The payload sends the address, the consent string, the figures entered, the derived
result, any refinement values, and the share URL that reproduces their exact result.
The capture block on the page states this in full before they submit. If you change
what is sent, change that copy in the same commit.

Free-tier Web3Forms keeps submissions for 30 days with no CSV export. The reminder
promise runs to October 2027, so the list has to be exported or the plan upgraded
before the first 30 days lapse.

Still outstanding: the CAN-SPAM postal address for the commercial mail that goes to
this list. That is a sending blocker, not a capture blocker.

## October, when SSA publishes the 2027 cap

The cap is one setting in each of two files. Every sentence that names the cap, its
year or "October" is built from that setting, so the copy cannot drift from the
number. No string edits.

### Change four values in two files

1. `index.html`, engine block, `CONFIG` at line ~899:
   - `wage_cap`: the 2027 taxable maximum SSA publishes.
   - `wage_cap_year`: `2027`.
   - `wage_cap_confirmed`: `true`.
   - `wage_cap_confirmed_on`: the SSA announcement date as `'YYYY-MM-DD'`.
2. `famli_ref.py`, `CONFIG` at line ~21: the same four keys (`wage_cap` as a `Decimal`,
   `wage_cap_confirmed` as `True`, `wage_cap_confirmed_on` as `date(YYYY, M, D)`).

**Skip the second file and `run-fixtures.js` fails the parity check and 5 fixtures
(F03, F17, F18, F19, F28) that look like app bugs and are not.** Skip the first and
the parity check fails alone.

3. Regenerate the fixture table: `python3 fixtures.py > fixture_table.txt`.
4. Regenerate `version.txt` (sha256, byte count and build stamp of `index.html`).
5. Run all three harnesses. `run-dom.js` derives its cap-dependent expectations from
   the engine's own `CONFIG`, so it needs no edits.

### What the setting drives

Seven places used to say "2026" or "October" by hand: the `CONFIG` comment and six
rendered sentences. `wage_cap_confirmed` now switches the six sentences from the
placeholder wording ("SSA publishes the 2027 cap in October") to the confirmed wording
("confirmed by SSA on ..."): `D1`, the cap note in "What it costs", the
`src('SSA ... taxable maximum')` label, the print cover `cv-note`, the closing page,
and the capture card sentence, which drops out once confirmed. All six live in the
`CAPW` object near the top of the app script. The comment carries no year.

`run-dom.js` fails if a formatted cap literal such as `184,500` survives anywhere in
the source, if the raw figure appears anywhere but the `CONFIG` line, if any rendered
"<year> Social Security" phrase disagrees with `wage_cap_year`, or if any rendered
"SSA confirms/publishes the <year>" phrase disagrees with `wage_cap_year + 1` (or
survives at all once confirmed).

`CONSENT_TEXT` also references the October confirmation. Do not edit it. It is the
consent string people already agreed to, and it is versioned. If it has to change,
bump the version. The guards skip it for that reason.

## Print report

Six sheets. Cover, report head, costs, dates, private plan, closing.

Two things that will bite whoever edits the print CSS:

- **Chrome clips all printed content to the `@page` margin box.** The cover band is
  positioned at `left:-15mm` to bleed, and it cannot. It renders inset 15mm each side.
  `.cv-head` carries its own left padding for that reason. Real full bleed needs
  `@page{margin:0}` with the margins reapplied as content padding on every page.
- **`.foot` is hidden in print.** It is the site footer, not a report component, and
  it used to land alone on its own sheet carrying only the basis note. Page 5 ends at
  227mm with 35mm free and the block needs 43mm, so it could never pull back. Its
  content now lives in the closing page notice. Do not un-hide it without moving that
  content back.

## Analytics

Microsoft Clarity, project `yatz1z728u`. Two settings live in the Clarity dashboard,
not in this repo:

- Masking mode **Balanced**. Input boxes and dropdowns are masked in every mode, and
  Balanced also masks numbers, which covers every figure on the page.
- Bing data sharing **off**.

The one value Balanced would capture is the business name, so it carries
`data-clarity-mask` where it renders. Note the print cover exists in the screen DOM at
`display:none`, so it is captured despite never being visible.

## Known limitation carried forward

A11. The 2028 branch determines employer size from the prior year's four quarters, but
the payment and notice dates are still the 2027 constants. It does not bite this cycle.
It bites whoever picks this up next year.

## Date override for QA

`?d=YYYY-MM-DD` renders the page as if read on that date. It stays in your address bar
so you can click around, and the copy-link button strips it, so a link you share always
shows the reader the real phase.
