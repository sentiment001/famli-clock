# FAMLICLOCK SEO

Nine pages plus the SEO and GEO layer for `famliclock.com`, built 21 September 2026 from
*FAMLI Clock (famliclock.com): SEO + GEO Assessment and Working Plan*.

**Status: built, tested, committed locally, NOT pushed.** The sandbox could clone and read
`sentiment001/famli-clock` but its proxy refused every write, with and without a personal
access token: *"not in this session's authorized repository set"*. The commit exists as a git
bundle in the delivery zip. **Read APPLY.md** for the three ways to land it.

Read **PUSH_ORDER.md** before touching `index.html`. It carries a trap that will silently
undo half the work: six copies of the H1, five of them inside the app script, keyed by
campaign phase.

## What is here

```
FAMLICLOCK SEO/
  HANDOFF_PROMPT.md          paste this into a fresh chat to get it pushed
  README.md                  this file
  APPLY.md                   the three ways to land the commit
  PUSH_ORDER.md              what changed, what to verify, what was deliberately left out
  FACTS_REGISTER.md          every published fact, traced to COMAR, statute or the tool's CONFIG
  site/                      the 15 files that go to the repo root, drop-in
    index.html               PATCHED from 9aa35dc, read PUSH_ORDER.md section 1 first
    (8 content pages, famli_pages.css, sitemap.xml, robots.txt, llms.txt)
    vercel.json              finished, replaces the existing one
    vercelignore             SAVE AS .vercelignore, with the leading dot
  source/                    the generator, the QA, and examples.json
    build.py                 scaffolding, head, nav, sitemap, robots, llms.txt, main()
    content_a.py             rate, small employer
    content_b.py             out-of-state, employee notice
    content_c.py             private plan, deadlines
    content_d.py             registration, payroll providers
    patch_index.py           the homepage patcher, asserts every anchor
    famli_pages.css          shared stylesheet, hand-maintained
    run_examples.js          runs the SHIPPED engine, writes examples.json
    examples.json            every money and date figure published, engine-derived
    qa.py                    499 structural, JSON-LD, link and house-style checks
    browser_qa.js            371 real-Chromium checks at four widths, plus the live tool
  qa-shots/                  screenshots taken during QA (zip only, binary)
  famliclock-seo.bundle      the exact commit, applyable in one command (zip only, binary)
```

`version.txt` is not shipped as a file because it has to be regenerated from whichever
`index.html` actually lands. The command is in APPLY.md and HANDOFF_PROMPT.md.

Rebuild from scratch:

```bash
node source/run_examples.js /path/to/index.html > source/examples.json
python3 source/build.py --out site
python3 source/patch_index.py --in /path/to/index.html --out site/index.html
python3 source/qa.py --dir site
node source/browser_qa.js site
```

## The pages

| URL | Primary target | Semrush volume today |
|---|---|---|
| `/` retitled, plus ~900 crawlable words | maryland famli calculator | 10 |
| `/contribution-rate-2027` | maryland famli contribution rate | 0 |
| `/small-employer` | maryland famli small employer | 0 |
| `/out-of-state-employees` | maryland famli out of state employees | 0 |
| `/employee-notice` | maryland famli employee notice | 0 |
| `/private-plan-declaration-of-intent` | famli declaration of intent | 0 |
| `/deadlines-2027` | maryland famli deadlines | 0 |
| `/registration` | maryland famli registration | 10 |
| `/payroll-providers` | maryland famli payroll setup | 0 |

**Eight of the nine target terms Semrush measures at zero, and that is the entire point of
this build**, so it is worth being blunt about it. Maryland FAMLI has not started. The
employer long tail has not formed. Below-threshold is not the same as nobody searching, and
these are precisely the questions employers will type from November 2026 (Declaration of
Intent), December (the notice), January 2027 (a new line on a pay stub) and April 2027 (the
first remittance). If you judge these pages on Search Console impressions in ninety days they
will look like failures. The measurable demand that exists today, roughly 1,350 a month, is
almost all navigational to `paidleave.maryland.gov` and is not winnable.

Total body copy: about 13,900 words across nine pages, including shared furniture.

## What these pages actually compete on

Not volume. The head terms belong to the state site, to national law firms (Ogletree, Fisher
Phillips) and to national insurers (Hartford, Unum, ShelterPoint, Sun Life), all with domain
authority in the 50s to 80s. Every one of those pages explains the law. **None of them
computes anything.**

Four things on this site are not available anywhere else, and they are the link ask and the
AI citation hook:

1. **The written notice date.** COMAR 09.42.02.05D requires notice "at least 1 pay period
   prior to the commencement" of withholding. That makes the deadline a function of each
   employer's payroll calendar, and no agency publishes a per-employer answer. The tool
   derives it. The state tells you the rate; this tells you your date.
2. **Whether a Declaration of Intent still fits.** Five stages, three outside the employer's
   control, one hard deadline, modelled at three paces.
3. **The cost of the blank out-of-state headcount field**, which reclassifies a small
   employer from 0.45% to 0.9% with no notice and no letter.
4. **That a private plan saves nothing in 2027.** The same contributions are collected and
   escrowed rather than remitted. Most employers considering one have not been told this.

Every worked example on every page was computed by running the shipped engine out of
`index.html`. Nothing is hand-calculated. That is what makes the figures citable.

## The Colorado problem

Colorado runs a paid leave program with the same acronym, live since 2024. "famli" alone is
14,800 US searches a month and "famli calculator" is 210; those are Colorado's. Every page
leads with "Maryland" in the title, the H1 and the first sentence, and carries a
disambiguation line naming the Maryland Department of Labor. `qa.py` fails the build if any
page is missing it. Watch Search Console: clicks on "famli calculator" without "maryland"
mean the line needs tightening.

## Decisions made in this session, and why

Four were open in section 13 of the assessment. Three were settled by building; one is still
Mash's.

1. **The call to action is aimed at payroll bureaus and CPAs, not single employers.**
   Approved by building it that way. `/payroll-providers` is written to Lane 1 and every
   other page's CTA bullets speak to scale rather than to one employer's arithmetic. The
   assessment's own honest read is the reason: the tool's natural user, a ten-person shop,
   cannot become a $20K client, but a bureau with fifty Maryland clients has a workflow
   problem that is a build.
2. **The "Client FAMLI Register in 48 hours" bridge artifact ships**, on `/payroll-providers`,
   offered free and explicitly without obligation, with the recurring version named as the
   paid engagement. Mirrors the FL structure.
3. **The calculator is not embedded on the eight content pages.** This is the one place the
   build departs from the plan. Reasoning in PUSH_ORDER.md section 7, in short: nine copies
   of the engine is nine chances for one of them to disagree about the wage cap, which is the
   exact failure the repo's own guard exists to prevent.
4. **Still open: defaulting the annual payroll input from headcount.** The assessment
   recommends it, to cut the one input people do not know off hand. It is a change to the
   tool's form rather than to these pages, so it was left alone. It is the highest-leverage
   remaining conversion change on the site.

## Still to do, and the first one matters most

1. **Google Search Console.** Add the property, submit the sitemap. Ten minutes, and nothing
   ranks until it is done.
2. **Check what `famliclock.com/robots.txt` actually serves.** On 21 September 2026 it
   returned Cloudflare's managed content-signals file, not a file from the repo. If Cloudflare
   overrides the pushed `robots.txt`, or has AI crawler control switched on for the zone, the
   whole GEO effort fails regardless of page quality. This was observed, not guessed.
3. **Repurpose `/private-plan-declaration-of-intent` after 15 November 2026** into "you missed
   the Declaration of Intent, here is what now". The section is already written; it needs
   promoting.
4. **The October wage cap update now has two extra steps.** PUSH_ORDER.md section 6.
5. **Confirm the Declaration of Intent upload step** by signing into the FAMLI portal. It sits
   behind Login.gov and no build session has seen it. Two things the private plan page leans
   on are not stated by any primary source and are disclosed as such on the page.

## What this work corrected

**A live SEO defect nobody had noticed.** The homepage H1 is rewritten by the app from a
five-entry phase table. Phase 2 begins 29 September 2026, and its headline was "The private
plan window is closing. Here is what still fits." Phases 3 and 4 were similar. From 29
September the site's own H1 would have stopped containing the words "Maryland FAMLI" at all,
silently, for as long as each phase lasted. All six copies now lead with "Maryland FAMLI
calculator".

**A standing project fact, confirmed and now cited.** "1 December written notice is NOT a
fixed statutory date, it is employer-specific" was carried in project memory as a correction.
The paragraph behind it is COMAR 09.42.02.05D, quoted verbatim on `/employee-notice`, and
1 December is labelled throughout as the calculator's safe default rather than a deadline.
