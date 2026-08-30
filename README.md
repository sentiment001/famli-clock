# famliclock.com, Step 2.3 build

One self-contained page. Deploy the folder to Vercel. No build step, no environment
variables, no external files to go missing.

## Files

| File | What it is |
|---|---|
| `index.html` | The whole site. Engine, CSS and app JS all inline. |
| `fixture_table.txt` | The 28 expected outputs, regenerated from `famli_ref.py`. |
| `fixtures.py` | The 28 fixture definitions, F28 added this session. |
| `load-engine.js` | Pulls the engine out of `index.html` so tests run on shipped bytes. |
| `run-fixtures.js` | The 28 spec fixtures, diffed against `fixture_table.txt`. |
| `run-boundaries.js` | Phase edges, notice versus payment direction, holiday and countdown guards. |
| `run-dom.js` | Renders the real page in jsdom and asserts the outputs are on screen. |
| `vercel.json` | Headers and a short cache, so the October wage cap change propagates. |

`index.html` has no dependency on any sibling file. Open it from disk, email it, or
serve it from anywhere and it works. The only external request is the Google Fonts
stylesheet, and if that fails the page falls back to Georgia and the system sans.

## Run the tests

```
npm install jsdom
node run-fixtures.js     # 28 fixtures
node run-boundaries.js   # 42 date and phase checks
node run-dom.js          # 66 render checks
```

All three read `index.html` directly. There is no separate engine file that can drift
out of step with the page.

## Not built, deliberately

**Email capture.** Prompt 2.3 says do not proceed to the capture build without
02Launch's physical postal address. It was not supplied, so nothing collects email.
The slot is marked in `index.html`. Shipping a capture without the address would put a
non-compliant commercial footer into production.

## October, when SSA publishes the 2027 cap

The cap lives in **two** files. Change both or the tests lie to you.

1. `index.html`, engine block: `wage_cap: 184500`. This is the only place the number
   appears in the page. Every visible figure and every piece of cap copy reads from it,
   including the D1 disclosure text and the cap-bites note. Verified by swapping the
   constant and confirming no literal `184,500` survives anywhere in the file.
2. `famli_ref.py` line 21: `"wage_cap": Decimal("184500")`. The reference engine has its
   own copy. **If you skip this you get 5 fixture failures that look like app bugs and
   are not.**
3. Regenerate the 28 fixtures from `famli_ref.py`, overwrite `fixture_table.txt`, then
   run `run-fixtures.js`. Regenerating against the old constant gives false failures.
4. Update the D1 wording only to swap "2026" for "2027" and add the SSA source date. The
   number itself now interpolates.

## Known limitation carried forward

A11. The 2028 branch determines employer size from the prior year's four quarters, but
the payment and notice dates are still the 2027 constants. It does not bite this cycle.
It bites whoever picks this up next year.

## Date override for QA

`?d=YYYY-MM-DD` renders the page as if read on that date. It stays in your address bar
so you can click around, and the copy-link button strips it, so a link you share always
shows the reader the real phase.
