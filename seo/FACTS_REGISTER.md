# Maryland FAMLI verified fact register for famliclock.com pages

Compiled 21 September 2026. Every line traces to a named paragraph of COMAR or the
Labor and Employment Article, to a named page on paidleave.maryland.gov, or to the tool's
own `CONFIG`. Nothing here came from a law firm summary, an insurer blog or a payroll
vendor page, except where explicitly labelled as such.

**Authority order.** `index.html`'s `CONFIG` block and `famli_ref.py` beat this file. This
file beats the SEO handoff document. Where this file and the repo disagree, the repo wins
and this file gets corrected, not the other way round.

**Status: reconciled 21 September 2026** against `index.html` at commit `9aa35dc`
(sha256 `68308de5…`, 123,593 bytes, built 2026-09-08T17:04:13Z) and against the
Department's live pages fetched the same day. All three repo harnesses
(`run-fixtures.js`, `run-boundaries.js`, `run-dom.js`, 252 checks) pass against the
patched `index.html`.

---

## Primary sources

| ID | Document | URL |
|---|---|---|
| S1 | COMAR Title 09, Subtitle 42, full text | https://regs.maryland.gov/us/md/exec/comar/09.42/index.full.html |
| S2 | MDOL FAMLI, Make Contributions | https://paidleave.maryland.gov/employers/make-contributions/ |
| S3 | MDOL FAMLI, Understand Employer Registration | https://paidleave.maryland.gov/employers/understand-employer-registration/ |
| S4 | MDOL FAMLI, Understand Your Plan (private plans) | https://paidleave.maryland.gov/employers/understand-your-plan/ |
| S5 | Proof of Private Plan Consultation form | https://paidleave.maryland.gov/files/proof-of-private-plan-consultation.pdf |
| S6 | FAMLI private plan FAQs, April 2026 | https://paidleave.maryland.gov/files/famli-faqs-private-plans-april-2026.pdf |
| S7 | LE §8.3-601, contribution rate | https://mgaleg.maryland.gov/mgawebsite/laws/StatuteText?article=gle&section=8.3-601 |
| S8 | LE §8.3-801, notices | https://mgaleg.maryland.gov/mgawebsite/laws/StatuteText?article=gle&section=8.3-801 |
| S9 | LE §8.3-903, penalties | https://mgaleg.maryland.gov/mgawebsite/laws/StatuteText?article=gle&section=8.3-903 |
| S10 | SSA contribution and benefit base (taxable maximum), 2027 row | https://www.ssa.gov/oact/cola/cbb.html |
| S11 | `index.html` `CONFIG`, this repo | engine block, line ~917 |
| S12 | FAMLI FAQs, April 2026 (general, 154 questions) | https://paidleave.maryland.gov/files/famli-faqs-april-2026.pdf |
| S13 | FAMLI contributions FAQ, April 2026 | https://paidleave.maryland.gov/files/famli-faqs-contributions-april-2026.pdf |
| S14 | SSA 2027 COLA fact sheet | https://www.ssa.gov/cola/factsheets/2027.html |
| S15 | LE §3-1304, earned sick and safe leave (2025RS statute text) | https://mgaleg.maryland.gov/2025RS/Statute_Web/gle/3-1304.pdf |
| S16 | MD Labor, Healthy Working Families Act FAQs | https://labor.maryland.gov/paidleave/paidleavefaqs.shtml |
| S17 | MD Labor, sick and safe leave employee notice | https://labor.maryland.gov/paidleave/paidleaveposter.shtml |

---

## F1. The rate, the split and the ceiling

**Cite:** COMAR 09.42.02.05B; LE §8.3-601. **Source:** S2 verbatim, S1, S7, S11.

S2 verbatim: *"0.9% of wages up to the Social Security wage cap"* for 2027, with a statutory
maximum of *"1.2% of wages"*, and *"The contribution amount is split equally between
employers and employees (0.45% each)."*

COMAR 09.42.02.05B verbatim: *"Under Labor and Employment Article, §8.3-601, an employer may
withhold from the pay of an employee an amount up to 50 percent of the total rate of
contribution."*

`CONFIG` holds `total_rate_bp: 90`, `small_rate_bp: 45`. The page and the engine agree.

**Withholding is permitted, not required.** 0.45% is a ceiling on what may be withheld. An
employer may withhold less and fund the rest.

**The Secretary sets each later year's rate by 1 November of the preceding year**, capped at
1.2%. So the 2028 rate is due by 1 November 2027 and **is not knowable today**. Never publish
a 2028 rate.

## F2. The wage base

**Cite:** COMAR 09.42.02.04A. **Source:** S1 verbatim, S10, S11.

Verbatim: *"All wages paid by each employer to an employee for performing qualified employment
are subject to contributions up to the amount of the social security wage base each calendar
year."*

Per employee, per calendar year. The 2027 Social Security taxable maximum is **$192,300**
(S10 verbatim, read 14 October 2026: *"For earnings in 2027, this base is $192,300."* The
table's 2027 row reads 192,300). SSA published it on **14 October 2026**, with the 2027 COLA.
`CONFIG` carries `wage_cap: 192300`, `wage_cap_year: 2027`, `wage_cap_confirmed: true`,
`wage_cap_confirmed_on: '2026-10-14'`. The 2026 figure it replaced was $184,500; it stays in
this record only.

Per-employee maximum contribution for 2027: 0.9% of $192,300 is $1,730.70 (standard
employers); 0.45% is $865.35 (the employee half, and the whole bill for an employer under 15).

**Handling rule, and it is load-bearing.** `run-dom.js` fails the build if the formatted
cap literal (`$192,300` from 14 October 2026) survives anywhere in `index.html`, or if a hard-coded `<year> Social
Security` phrase appears outside `CONSENT_TEXT`, because a literal goes stale the day SSA
publishes. The SEO pages follow the same discipline by a different route: they are generated,
and the cap is read out of the engine's own `CONFIG` through `examples.json`, never typed.
`qa.py` fails if a page and the engine disagree. **`index.html` itself carries no cap
literal at all**; its worked examples are chosen so that no employee is near the cap, so the
figures do not move when the cap does, and the page says so.

## F3. Employer size, and the 15

**Cite:** COMAR 09.42.02.06A and .06D. **Source:** S1 verbatim, S2.

.06D verbatim: *"The employer is only responsible for remitting 50 percent of the total rate
of contribution if the employer size … is below 15."*

S2 verbatim: *"Employers with fewer than 15 total employees, counting both Maryland and
out-of-state employees are only responsible for remitting 50% of the contribution rate."*

- The half that disappears is the **employer** half. The employee half is still **remitted**.
  Withholding it from pay is the employer's choice (F1, COMAR 09.42.02.05B and .05C), and a
  skipped deduction is the employer's own cost (F5). Never write that a small employer "still
  withholds" or "must withhold". Corrected 14 October 2026: this line used to say "still
  withheld and still remitted", and the site copied it onto three pages. `qa.py` now fails on
  that phrasing.
- Headcount is **EIN-wide, all states**. Independent contractors excluded.
- **Below** 15. Exactly 15 is the standard band.
- 2027: recalculated quarter by quarter, changes apply forward only. From 2028: prior year's
  four-quarter average, fixed for the year. (`CONFIG.quarterly_size_year: 2027`.)

## F4. The out-of-state reporting trap

**Cite:** COMAR 09.42.02.08C and D. **Source:** S1, S11 (the tool raises it as a warning).

To be classified small, the quarterly wage report must state how many employees work outside
Maryland. Leave the field blank and the employer is deemed not small and pays 0.9% rather
than 0.45%.

This is the single most expensive reader error on the site and it gets its own page.

## F5. The deemed election. Not a fine.

**Cite:** COMAR 09.42.02.07A. **Source:** S1 verbatim.

Verbatim: *"If an employer fails to make the proper deduction from an employee's pay, that
employer is considered to have elected to pay the employee's portion for each pay period the
employer fails to make the deduction."*

Per pay period. Unrecoverable from a later cycle. Not a penalty, which is why it never appears
on a penalties list and why employers have not heard of it.

## F6. The written notice date. The site's whole differentiator.

**Cite:** COMAR 09.42.02.05D. **Source:** S1 verbatim.

Verbatim: *"An employer shall provide written notice to all of its employees of the
commencement of contribution withholding and any changes to employee contributions at least 1
pay period prior to the commencement or change."*

**There is no statutory 1 December.** The deadline is derived from the employer's own payroll
schedule. `CONFIG.safe_notice_date: '2026-12-01'` is an internal safe default that clears
every pay frequency, and the pages label it as exactly that. This matches the standing project
correction: *1 Dec written notice is NOT a fixed statutory date, it is employer-specific.*

Computed by the shipped engine for a first 2027 pay date, at 21 September 2026:

| Frequency | First 2027 pay date | Notice due |
|---|---|---|
| Weekly | Fri 8 Jan 2027 | Thursday 31 December 2026 |
| Every two weeks | Fri 8 Jan 2027 | Thursday 24 December 2026 |
| Twice a month | Fri 15 Jan 2027 | Thursday 31 December 2026 |
| Monthly | Fri 29 Jan 2027 | Wednesday 30 December 2026 |
| No first pay date given | n/a | Tuesday 1 December 2026, safe default |

Weekly is **later** than biweekly. A shorter pay period means a shorter run-up. That is
counter-intuitive and it is correct.

## F7. Notice dates move earlier, payment dates move later

**Cite:** COMAR 09.42.02.08E. **Source:** S1, S11.

A payment date at a weekend moves to the next business day. A notice date gets no such relief
and moves earlier. The asymmetry is small, real, and nobody else prints it.

## F8. The other notices

**Cite:** LE §8.3-801(a) and (b)(1); COMAR 09.42.04.08A(1). **Source:** S8 verbatim, S1.

- Rights and duties **at hire and annually** (§8.3-801(a)).
- Within **5 business days** of a leave request, or of the employer learning leave may qualify
  (§8.3-801(b)(1)).
- **6 months before benefits commence** (COMAR 09.42.04.08A(1)(a)). Benefits begin Jan 2028,
  so the nominal date is 3 July 2027, a Saturday; notices move earlier, to Friday 2 July 2027.
- **30 days before** a change to the employer's FAMLI procedures or plan
  (COMAR 09.42.04.08A(1)(d)).

**MDOL has not published the notice templates.** The regulations reserve the right to require
approved forms and say they will be provided later. **Do not draft notice language for
readers.** The pages say so and say why.

## F9. Quarterly reporting and payment

**Cite:** COMAR 09.42.02.08. **Source:** S2 verbatim.

| Wages paid | Due | 2027 weekday |
|---|---|---|
| 1 Jan to 31 Mar | 30 April | Friday |
| 1 Apr to 30 Jun | 31 July | Saturday, so Monday 2 August |
| 1 Jul to 30 Sep | 31 October | Sunday, so Monday 1 November |
| 1 Oct to 31 Dec | 31 January | Monday, in 2028 |

S2 verbatim: *"The first contribution payment, covering wages paid January 1 – March 31, 2027,
will be due April 30, 2027."*

## F10. Late payment

**Cite:** COMAR 09.42.02.09A; LE §8.3-903. **Source:** S1, S9, S11.

Interest at **1.5% a month or part of a month** on the unpaid amount. The Secretary may assess
a penalty of **up to twice the contributions** and order an audit of the next fiscal year.

## F11. The Declaration of Intent

**Cite:** COMAR 09.42.03.10A(1)(d), (2) and (3). **Source:** S4 verbatim, S1, S5, S6, S11.

- Window **1 September to 15 November 2026** (S4 verbatim: *"between September 1-November 15,
  2026"*). 15 November is a **Sunday**; Friday 13 November is the last business day and is
  `CONFIG.doi_deadline`.
- FAMLI decides **within 15 business days** (COMAR 09.42.03.10A(2); S4 verbatim: *"FAMLI will
  notify the Authorized Officer of the outcome of the DOI submission within 15 business
  days."*).
- An approved Declaration **takes effect on the first day of the next quarter**
  (COMAR 09.42.03.10A(3)).
- **Contributions are still collected and held in escrow**, not remitted
  (COMAR 09.42.03.10A(1)(d)). *A private plan does not reduce the 2027 cash cost.*
- `CONFIG.doi_resubmit_safe: '2026-10-21'`, 15 business days before the deadline.
- All Declarations expire **31 December 2027** (`CONFIG.doi_expiry`).
- Three steps: Authorized Officer registers the employer; a licensed Maryland insurance agent
  signs the Proof of Private Plan Consultation; the officer uploads and attests in the FAMLI
  account.

**Two things the pages lean on that no primary source states.** Carried forward verbatim from
the repo README so they are not silently dropped:
1. That a **rejected DOI can be corrected and resubmitted before 15 November**.
2. That the **15 business days start the business day after submittal**.
Both are reasonable readings and both are how the engine models it. Neither is written down.
The private plan page discloses both in a note. Do not upgrade either to a stated rule.

**Also not verified from this session:** the upload step itself. The portal sits behind
Login.gov and no one has signed in from a build session. Someone with a registered account
should confirm before the 13 November plan is relied on.

## F12. Private plan mechanics

**Cite:** COMAR 09.42.03.05F and .05K. **Source:** S4 verbatim, S1, S11.

- Equivalence: *"Private plans must provide the same level of benefits and service as the
  State Plan, or better."* (S4)
- Annual application fee by headcount: $100 (1–14), $250 (15–49), $500 (50–199), $600
  (200–499), $750 (500–999), $1,000 (1,000+). Self-insured: $1,000. Approval lasts one year;
  the fee is annual. (COMAR 09.42.03.05F, S4)
- **Self-insurance needs 50+ employees localized in Maryland.** The under-50 exception
  required a FAMLI-compliant plan already in effect by **31 July 2026**, which has passed.
  (COMAR 09.42.03.05K, S4)
- Private plan applications open **summer 2027**, due **1 October 2027** (S4 verbatim).
- A carrier cannot cause more than 0.45% to be withheld from employees.

## F13. Registration

**Cite:** none needed, agency statement. **Source:** S3 verbatim.

Verbatim: *"If you have at least one employee in Maryland, you are required to register
online. There are no exceptions under state law."*

Required: EIN, legal name, d/b/a, NAICS code, physical and mailing addresses, business email;
Authorized Officer name, title, work email, work phone; resident agent name, address, email,
phone. Account creation needs an email and phone or an existing Login.gov account; **identity
verification additionally needs a Social Security number and a driver's licence or state ID**.

**No published registration deadline.** It nonetheless blocks the Declaration of Intent, the
quarterly report and the payment.

## F14. The sole owner exemption

**Cite:** COMAR 09.42.01.01B(21)(b). **Source:** S1, S11 (the engine returns this and stops).

A sole owner who is the only person their entity employs is not an employer for FAMLI
purposes. Narrow: one employee who is not the owner ends it.

## F15. Program dates

**Source:** S2, S4, S11.

- Contributions on wages **paid from 1 January 2027**.
- Benefits begin **January 2028** (`CONFIG.benefits_begin: '2028-01-03'`).
- 2027 is a collection year with no claims in it.

## F16. Maryland is not Colorado

Colorado runs a paid family and medical leave insurance program with the **same acronym**,
live since 2024. Semrush shows "famli" at 14,800 US searches a month and "famli calculator"
at 210, and those are Colorado's. Every page on this site therefore says "Maryland" in the
title, the H1 and the first sentence, and carries one disambiguation line naming the Maryland
Department of Labor and stating that Colorado's program is separate. `qa.py` fails the build
if any page is missing it.

---

## Added 31 October 2026 (SEO handoff 30 Oct, Job 1)

All read on 31 October 2026 from the sources named. Every row below is **full**: read in
the primary source itself, not a search snippet.

## F17. The wage cap is per job. CORRECTION.

**Source:** S13 verbatim, question 19: *"The cap on wages is determined separately for each
job."* (Same text as S12 question 39.) Consistent with COMAR 09.42.02.04A, *"All wages paid by
each employer to an employee"* (F2).

`/contribution-rate-2027` said from 21 September to 31 October 2026: *"The cap is per person per
year, not per employer"*. That was wrong for anyone with two jobs, and it was fixed in
`content_a.py` on 31 October 2026. `llms.txt` now states the per-job rule.

## F18. Program names, dates and benefits (hub page)

**Source:** S12.

- Q1: up to 12 weeks, up to $1,000 a week; *"often referred to as 'paid family and medical
  leave' or simply 'paid leave'"*.
- Q8, Q10, Q12: contributions from 1 January 2027; benefits January 2028; the 2025 delay bill.
- Q16: notices one pay period before deductions, July 2027, at hire, yearly, on request.
- Q21, Q24: 0.9%, 0.45% each side; withholding optional; employers may pay the full amount.
- Q26: size counts employees within and outside Maryland, quarterly until a full year of reports.
- Q31, Q37: wages as defined for UI (LE §8.3-101(r)); gross wages reported.
- Q33, Q35: FAMLI website, not BEACON; first payment 30 April 2027.
- Q40: no recovery of a missed deduction from a later pay cycle, except an employee who earned
  too little that cycle (up to 6 pay periods).
- Q53: localization examples (lives MD works VA: not covered; lives PA works MD: covered).
- Q55: a family employing a nanny is an employer.
- Q64: 680 hours in Maryland in the 4 reported quarters before claim or leave, whichever is
  earlier; hours from more than one employer count.
- Q69, Q71, Q72: qualifying reasons; leave within the first year after birth or placement,
  including births before benefits start; both parents at once.
- Q92, Q93: up to 90% of wages, $1,000 a week maximum. (No claim is made about indexing.)
- Q96: 12 weeks; up to 24 when own serious health condition and a new child fall in the same year.
- Q105, Q106: job held, health benefits maintained.

## F19. Sick and safe leave, and how it meets FAMLI

**Sources:** S15 verbatim, S16, S17, S12.

- LE §3-1304(a)(1): 15 or more employees, paid at the normal rate; 14 or fewer, at least unpaid.
- §3-1304(a)(2): average monthly employees in the immediately preceding year, all employee
  types counted. S16 II.3: *"The Commissioner will consider only those employees employed in
  Maryland."* (The Commissioner's reading, attributed as such on the page.)
- §3-1304(b), (c): 1 hour per 30 worked; employer need not allow more than 40 earned a year,
  64 used a year, 64 accrued at any time, or use in the first 106 calendar days; carryover 40
  (§3-1304(g)). The 2023 bill to make it 120 days (HB 1015) is not in the 2025RS text.
- S16 I.1, I.4, I.7: in force 11 February 2018; primary work location Maryland; exemptions
  including employees who regularly work under 12 hours a week.
- S16 III.12: a statement of used and available leave each pay period.
- S16 IV.3: uses, including maternity or paternity leave and domestic violence, sexual assault
  or stalking.
- S17: no adverse action for exercising the right.
- S12 Q15 (colds vs serious illness), Q70 (domestic violence is not a FAMLI qualifying event),
  Q113, Q116 to Q122 (FMLA runs concurrently; employers can't require PTO; can require unpaid
  leave; accrued leave may top up to 100% with the employee's agreement; employee may choose
  not to claim; AFPL can be required concurrently and counts toward the 12 weeks).

## F20. The Social Security wage base page

**Sources:** S10, S14, S13, F2.

- S10: 2027 base $192,300; OASDI 6.2% each; *"After 1993, there has been no limitation on
  HI-taxable earnings"*, 1.45% each; the 1937 to 2027 table. Rows 2017 to 2026 are stored in
  `content_e.SSA_CBB`; the 2027 row is read from CONFIG. The table prints amounts **without a
  dollar sign**, as SSA's own table does after its first row, so the cap-literal guard in
  `qa.py` still fails on any stray `$1xx,xxx` figure. `qa.py` checks every row against
  `SSA_CBB` and the engine.
- S14: Maximum Taxable Earnings (OASDI) $192,300 for 2027; Medicare (HI) no limit.
- Per-employee maxima, from the engine (`W_cap_std`, `W_cap_small` in `run_examples.js`):
  $1,730.70 at 0.9% ($865.35 each side); $865.35 at 0.45%. `qa.py` also recomputes cap x rate
  independently and fails if the engine and the arithmetic disagree.

Mutation-tested 31 October 2026: a stale cap typed onto the page, a mistyped SSA row, a bogus
engine figure, and "must withhold" on a new page each fail `qa.py`.

---

## Things deliberately NOT published

Listed so a future session does not treat a gap as an oversight.

1. **A 2028 contribution rate.** The Secretary sets it by 1 November 2027. Unknowable.
2. **A 2028 Social Security wage cap.** SSA sets it in October 2027. (The 2027 cap, $192,300,
   was published 14 October 2026 and is live; see F2. Earlier years appear only in SSA's own
   history table on `/social-security-wage-base-2027`; see F20.)
3. **Notice language.** MDOL's templates are not out. Drafting one for readers would be
   guessing at format for no benefit.
4. **What a private plan costs.** Carriers set their own rates. Only the fee schedule and the
   0.45% withholding ceiling are knowable.
5. **Anything about employee claims, eligibility or benefit amounts.** Reversed in part on
   31 October 2026 by the SEO handoff of 30 October (approved by Mash):
   `/maryland-paid-family-leave` now carries one section on benefits and a short box for
   parental leave searches, all from S12 (F18). There is still no employee-side page and no
   claims guidance.
6. **A Colorado comparison page.** Would attract exactly the traffic the disambiguation line
   exists to repel.
7. **Any penalty figure for a missed notice.** The contributions chapter states none. The
   adjacent exposure, the deemed election, is stated instead and is cited.
8. **Employer-size edge cases**: employees splitting time across state lines, secondments,
   joint-employer staffing. Genuinely unresolved; the pages say so and point at
   (410) 525-4010.
9. **The claim that the calculator is embedded on every page.** It is not, by decision. See
   PUSH_ORDER.md section 7.

## One correction to the SEO handoff

The handoff's section 6 says *"No `HowTo` on the notice page; drafting the notice is the
employer's act."* Followed. It also specifies `WebApplication`, `Organization`, `FAQPage` and
`BreadcrumbList`. All four ship. The handoff's section 5 word targets (500 to 1,000) are
exceeded on every page; body prose runs roughly 800 to 1,300 words plus shared furniture.
