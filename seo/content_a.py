# -*- coding: utf-8 -*-
"""Content for /contribution-rate-2027, /small-employer, /out-of-state-employees
and /employee-notice.

Every figure in a worked example is read out of examples.json, which comes from
the shipped engine. No number in this file is typed by hand except the rate
percentages and the statutory thresholds, which are quoted from COMAR and the
Labor and Employment Article and are listed in FACTS_REGISTER.md.
"""

import re

from build import S, src, money, money0


def _cell(v):
    """Right-aligned and nowrap for a figure, left-aligned and wrapping for a
    sentence. Measured in Chromium: a nowrap sentence in a value cell pushed the
    sole-proprietor example 822px wide and gave the whole homepage a horizontal
    scrollbar at 390px. The 60-character threshold is the fix, not a guess."""
    plain = re.sub(r"<[^>]+>", "", str(v))
    cls = "num" if len(plain) <= 60 else "txt"
    return '<td class="%s">%s</td>' % (cls, v)


def wex(title, inputs, outputs, basis):
    """One worked example: inputs table, outputs table, basis line.

    Both tables sit in .tblwrap, which scrolls horizontally rather than pushing
    the page wider, so a long row can never break the layout at phone width."""
    irows = "".join("<tr><th>%s</th>%s</tr>" % (k, _cell(v)) for k, v in inputs)
    orows = "".join('<tr%s><th>%s</th>%s</tr>'
                    % (' class="total"' if t else "", k, _cell(v)) for k, v, t in outputs)
    return (
        '<div class="wex"><h3>%s</h3>'
        '<div class="tblwrap"><table class="tbl"><caption>What was entered</caption>'
        '<tbody>%s</tbody></table></div>'
        '<div class="tblwrap"><table class="tbl"><caption>What the calculator returns</caption>'
        '<tbody>%s</tbody></table></div>'
        '<p class="basis">%s</p></div>' % (title, irows, orows, basis))


def basis(meta, verified="21 September 2026"):
    """The one-sentence provenance line under every worked example.

    The wage cap and its year are read out of the engine's own CONFIG, through
    examples.json, and never typed. index.html carries a DOM guard (run-dom.js)
    that fails if a formatted cap literal such as $184,500 survives anywhere in
    its source, precisely because a literal goes stale the day SSA publishes the
    next cap. The same reasoning applies to these pages; the difference is that
    they are generated, so rebuilding them after the October CONFIG change
    updates every figure at once. qa.py fails the build if a page and the engine
    disagree."""
    cap = "$" + "{:,}".format(int(meta["wage_cap"]))
    return ("Computed by famliclock.com from the published 2027 rate of 0.9 percent and the "
            "%d Social Security taxable maximum of %s, on %s. Wages are assumed to be spread "
            "evenly across the headcount, which produces the largest figure the employer "
            "could owe. These are estimates, not a filing." % (meta["wage_cap_year"], cap, verified))


def basis_nocap(verified="21 September 2026"):
    """Provenance line for worked examples where no employee is anywhere near the
    cap, so the figures do not move when the cap does. Used on index.html, whose
    source must carry no cap literal and no "<year> Social Security" phrase."""
    return ("Computed by famliclock.com from the published 2027 rate of 0.9 percent, on %s. "
            "No employee in this example is paid above the Social Security wage base, so "
            "these figures do not change when the cap is updated. Estimates, not a filing."
            % verified)


def build(ex):
    E1 = ex["E1_small"]
    E2 = ex["E2_large"]

    pages = []

    # ================================================== /contribution-rate-2027
    body = """
<h2>The rate, and how it splits</h2>
<p>Maryland FAMLI contributions are due on wages paid from 1 January 2027. The total rate for
2027 is <b>0.9 percent</b> of covered wages. It splits evenly: 0.45 percent employer, 0.45
percent employee. %(src_rate)s</p>
<p>The employer remits the whole 0.9 percent to the Maryland Department of Labor each quarter.
Whether the employee half comes out of the employee's pay or out of the employer's own pocket
is the employer's choice, made pay period by pay period. The Department only ever sees one
payment.</p>

<h2>What wages the rate applies to</h2>
<p>All wages paid for qualified employment are subject to contributions <b>up to the Social
Security wage base each calendar year</b>, per employee. %(src_04A)s The cap is per person
per year, not per employer, so an employee earning above it simply stops accruing
contributions once their year-to-date Maryland wages cross the line.</p>
<p>The Social Security taxable maximum for 2026 is <b>$184,500</b>. %(src_ssa)s The Social
Security Administration publishes the 2027 figure in October 2026, and every number on this
site changes the day it lands. Until then the calculator uses the 2026 cap as a stand-in and
says so on the page.</p>
<p>Independent contractors are not employees for this purpose and their payments are not
subject to contributions.</p>

<h2>Who sets the rate, and when it can change</h2>
<p>The Secretary of Labor sets the rate. The statute caps it at <b>1.2 percent</b> of wages
and requires the rate for each later year to be set by 1 November of the preceding year.
%(src_le601)s So the 2028 rate is due by 1 November 2027, and it can be higher than 0.9
percent, up to that 1.2 percent ceiling. Nobody can tell you the 2028 number yet, and any
page that does is guessing.</p>

<h2>Withholding is a choice, and not choosing is a choice</h2>
<p>An employer may withhold from an employee's pay <b>up to 50 percent of the total rate of
contribution</b>. %(src_05B)s That is the 0.45 percent employee half, and it is a ceiling,
not a requirement. An employer may withhold less, or nothing at all, and fund the difference
itself.</p>
<p>The trap is in what happens if you simply do not get round to it:</p>
<blockquote><p>&ldquo;If an employer fails to make the proper deduction from an employee's
pay, that employer is considered to have elected to pay the employee's portion for each pay
period the employer fails to make the deduction.&rdquo; %(src_07A)s</p></blockquote>
<p>That is not a fine. It is a deemed election, and it is per pay period. You cannot recover
the missed amount out of a later pay cycle. For a 40-person employer on a $3.2m Maryland
payroll that is %(e2_missed)s every month it runs, and %(e2_never)s across a full year.</p>

<h2>Two worked examples</h2>
%(wex1)s
%(wex2)s

<h2>What this rate does not cover</h2>
<ul>
<li><b>Benefits.</b> Contributions start January 2027; employees cannot claim until January
2028. The first year is collection only.</li>
<li><b>A private plan.</b> An approved private plan does not reduce the 2027 cash cost. The
same contributions are collected and held in escrow instead of remitted. See the
<a href="/private-plan-declaration-of-intent">Declaration of Intent page</a>.</li>
<li><b>Employers with fewer than 15 staff.</b> They pay no employer share. See
<a href="/small-employer">the small employer page</a>.</li>
</ul>
""" % {
        "src_rate": src("Maryland Department of Labor, make contributions", S["contributions"]),
        "src_04A": src("COMAR 09.42.02.04A", S["comar"]),
        "src_ssa": src("SSA 2026 taxable maximum", S["ssaCap"]),
        "src_le601": src("LE 8.3-601", S["rate"]),
        "src_05B": src("COMAR 09.42.02.05B", S["comar"]),
        "src_07A": src("COMAR 09.42.02.07A", S["comar"]),
        "e2_missed": money(E2["cost_per_missed_pay_period"]),
        "e2_never": money(E2["cost_of_never_withholding"]),
        "wex1": wex(
            "A 12-person employer, all staff in Maryland",
            [("Employees working in Maryland", "12"),
             ("Total employees under one EIN", "12"),
             ("Annual Maryland payroll", money0(E1["input"]["md_payroll"] * 100)),
             ("Payroll frequency", "Every two weeks")],
            [("Band", "Small employer, under 15", False),
             ("Rate applied", "0.45%", False),
             ("Employer share, full year 2027", money(E1["annual_employer"]), False),
             ("Employee share, full year 2027", money(E1["annual_employee"]), False),
             ("Total, full year 2027", money(E1["annual_total"]), True),
             ("Per pay period, total", money(E1["per_period_total"]), False),
             ("First payment, Q1 wages, due 30 April 2027", money(E1["q1_payment"]), False)],
            basis(ex["_meta"])),
        "wex2": wex(
            "A 40-person employer, all staff in Maryland",
            [("Employees working in Maryland", "40"),
             ("Total employees under one EIN", "40"),
             ("Annual Maryland payroll", money0(E2["input"]["md_payroll"] * 100)),
             ("Payroll frequency", "Monthly")],
            [("Band", "Standard, 15 or more", False),
             ("Rate applied", "0.90%", False),
             ("Employer share, full year 2027", money(E2["annual_employer"]), False),
             ("Employee share, full year 2027", money(E2["annual_employee"]), False),
             ("Total, full year 2027", money(E2["annual_total"]), True),
             ("Per pay period, total", money(E2["per_period_total"]), False),
             ("Cost of absorbing the employee half instead", money(E2["absorb_delta"]) + " more a year", False),
             ("First payment, Q1 wages, due 30 April 2027", money(E2["q1_payment"]), False)],
            basis(ex["_meta"])),
    }

    pages.append(dict(
        path="/contribution-rate-2027",
        title="Maryland FAMLI Contribution Rate 2027: 0.9%, the Split, the Wage Cap",
        description=("The Maryland FAMLI contribution rate for 2027 is 0.9% of wages up to the "
                     "Social Security cap, split 0.45% employer and 0.45% employee. Worked "
                     "examples, the wage cap rule, and who sets the rate."),
        og_desc=("Maryland FAMLI 2027: 0.9% total, 0.45% each side, capped at the Social Security "
                 "wage base. Two worked examples and the rule behind each figure."),
        h1="Maryland FAMLI contribution rate for 2027",
        lede=("The Maryland FAMLI contribution rate for 2027 is <b>0.9 percent</b> of covered "
              "wages up to the Social Security wage base, split evenly between employer and "
              "employee at 0.45 percent each, on wages paid from 1 January 2027."),
        breadcrumb_name="Contribution rate 2027",
        tool_text=("Put your headcount and payroll in and get your own figure, per pay period and "
                   "for the full year, with a printable report for your CFO."),
        body=body,
        faq=[
            ("What is the Maryland FAMLI contribution rate for 2027?",
             "0.9 percent of covered wages, split evenly between employer and employee at 0.45 "
             "percent each. It applies to wages paid from 1 January 2027, up to the Social "
             "Security wage base per employee per year.",
             "0.9 percent of covered wages, split evenly at <b>0.45 percent each</b>. It applies "
             "to wages paid from 1 January 2027, up to the Social Security wage base per employee "
             "per year."),
            ("Is there a cap on Maryland FAMLI contributions?",
             "Yes. Wages are subject to contributions only up to the Social Security wage base "
             "each calendar year, per employee. The 2026 figure is $184,500 and the Social "
             "Security Administration publishes the 2027 figure in October 2026.",
             "Yes. Wages count only up to the Social Security wage base each calendar year, per "
             "employee. The 2026 figure is <b>$184,500</b>; SSA publishes the 2027 figure in "
             "October 2026."),
            ("Can the Maryland FAMLI rate go up?",
             "Yes. The Secretary of Labor sets the rate and the statute caps it at 1.2 percent of "
             "wages. The rate for each later year must be set by 1 November of the preceding "
             "year, so the 2028 rate is due by 1 November 2027.",
             "Yes. The Secretary of Labor sets it and the statute caps it at <b>1.2 percent</b>. "
             "Each later year's rate must be set by 1 November of the preceding year, so the 2028 "
             "rate is due by 1 November 2027."),
            ("Do employers have to withhold the employee share?",
             "No. Withholding up to 50 percent of the total rate is permitted, not required. But "
             "an employer that fails to make the deduction is considered to have elected to pay "
             "the employee's portion for each pay period it missed, and cannot recover it later.",
             "No. Withholding up to half the total rate is permitted, not required. But an "
             "employer that fails to make the deduction is <b>considered to have elected to pay "
             "the employee's portion</b> for each pay period it missed, and cannot recover it "
             "later."),
        ],
        sources=[
            ("Maryland Department of Labor, Make Contributions", S["contributions"]),
            ("COMAR 09.42.02, contributions", S["comar"]),
            ("Labor and Employment Article &sect;8.3-601, rate setting", S["rate"]),
            ("Social Security Administration, taxable maximum", S["ssaCap"]),
        ],
        related=[
            ("/small-employer", "Employers with fewer than 15 staff",
             "why the employer share is zero and the employee share is not"),
            ("/deadlines-2027", "Every 2027 deadline",
             "when withholding starts and when each payment is due"),
            ("/employee-notice", "The written notice",
             "the date depends on your payroll calendar, not the calendar year"),
        ],
        cta_intro="What a 30 minute call with our AI engineers does for you:",
        cta_bullets=[
            "<b>Your actual payroll file, not a typed estimate.</b> Every employee read "
            "individually, so the wage cap lands per person and the number you hand your CFO is "
            "the real one.",
            "<b>The October rate and cap change, applied for you.</b> SSA publishes the 2027 cap "
            "in October and the Secretary sets the 2028 rate by 1 November 2027. Both move every "
            "figure you filed.",
            "<b>The rest of the calendar, not just this deadline.</b> FAMLI is one line on a "
            "compliance calendar you keep by hand. The same build watches the others and tells "
            "you when one moves.",
        ],
    ))

    # ============================================================ /small-employer
    body = """
<h2>What changes if you are under 15</h2>
<p>An employer whose size is below 15 is <b>only responsible for remitting 50 percent of the
total rate of contribution</b>. %(src_06D)s In 2027 that means 0.45 percent rather than 0.9
percent.</p>
<p>The half that disappears is the employer half. The employee half does not. You still
withhold 0.45 percent from your staff and you still remit it to the Maryland Department of
Labor every quarter. What changes is that you are not asked to match it.</p>
<p>Put plainly: a small employer can legally pass its entire FAMLI obligation to its
employees, and pay nothing from its own funds. A 15-person employer cannot.</p>

<h2>How the 15 is counted, and it is not what most people assume</h2>
<p>Employer size is the total headcount under the same federal EIN, <b>counting employees
inside and outside Maryland</b>. %(src_06A)s The Department's own guidance puts it the same
way: employers with fewer than 15 total employees, counting both Maryland and out-of-state
employees. %(src_contrib)s</p>
<p>So a firm with 8 people in Baltimore and 30 in Virginia is not a small employer. It has 38
employees and it pays the full 0.9 percent on its Maryland wages. This is the single most
common way an employer gets its own FAMLI rate wrong, and it is worth its own page:
<a href="/out-of-state-employees">out-of-state employees and your Maryland FAMLI rate</a>.</p>
<p>Independent contractors are not counted.</p>

<h2>Crossing 15 during the year</h2>
<p>Size is not fixed for all time. During <b>2027</b> it is worked out quarter by quarter, so
an employer that crosses 15 in the middle of the year changes band from that quarter forward
and never backwards. From <b>2028</b> size is set by the average of the prior year's four
quarters and then fixed for the whole year.</p>
<p>Practically, that means a growing employer in 2027 should expect its rate to move mid-year,
and should not budget the small-employer figure for twelve months if hiring is planned.</p>

<h2>Exactly 15 is not small</h2>
<p>The regulation says size <b>below</b> 15. Fifteen employees is the standard band and the
full 0.9 percent. There is no rounding and no grace.</p>

<h2>The sole owner who is their own only employee</h2>
<p>If you are the sole owner and the only person your entity employs, you are not an employer
for FAMLI purposes at all. %(src_sole)s No registration, no contribution, no notice. The
calculator returns exactly that and stops.</p>
<p>This is narrow. One employee who is not the owner puts you in scope. Self-employed people
who want coverage can elect into the program separately, which is a different question and
handled by the Department, not by this tool.</p>

<h2>A worked example</h2>
%(wex1)s
<p>Compare the same payroll at a firm that is over the threshold on headcount alone: a 40-person
employer on a $3.2m Maryland payroll pays %(e2_er)s of employer money a year. The small employer
on a $780,000 payroll pays nothing.</p>

<h2>What the small employer still has to do</h2>
<ul>
<li><b>Register.</b> Registration is required for any employer with at least one Maryland
employee. There are no exceptions for size. See <a href="/registration">registration</a>.</li>
<li><b>Send the written notice.</b> The notice before withholding begins is owed by every
employer, small or not. See <a href="/employee-notice">the employee notice</a>.</li>
<li><b>Report out-of-state headcount on the quarterly report.</b> Leave the field blank and
you lose the small-employer rate. See <a href="/out-of-state-employees">the headcount
field</a>.</li>
<li><b>Withhold, or be deemed to have elected to pay.</b> Miss the deduction and the employee
half becomes yours for that pay period, permanently. %(src_07A)s</li>
</ul>
""" % {
        "src_06D": src("COMAR 09.42.02.06D", S["comar"]),
        "src_06A": src("COMAR 09.42.02.06A", S["comar"]),
        "src_contrib": src("Maryland Department of Labor", S["contributions"]),
        "src_sole": src("COMAR 09.42.01.01B(21)(b)", S["comar"]),
        "src_07A": src("COMAR 09.42.02.07A", S["comar"]),
        "e2_er": money(E2["annual_employer"]),
        "wex1": wex(
            "A 12-person employer, all staff in Maryland, paid every two weeks",
            [("Employees working in Maryland", "12"),
             ("Total employees under one EIN", "12"),
             ("Annual Maryland payroll", money0(E1["input"]["md_payroll"] * 100)),
             ("Payroll frequency", "Every two weeks")],
            [("Band", "Small employer, under 15", False),
             ("Rate applied", "0.45%, half the full rate", False),
             ("<b>Employer share, full year 2027</b>", "<b>" + money(E1["annual_employer"]) + "</b>", False),
             ("Employee share, full year 2027", money(E1["annual_employee"]), False),
             ("Total remitted for 2027", money(E1["annual_total"]), True),
             ("Withheld per pay period, per the whole firm", money(E1["per_period_employee"]), False),
             ("Written notice due, if no first 2027 pay date is given", "1 December 2026", False),
             ("First payment, Q1 wages", money(E1["q1_payment"]) + ", due 30 April 2027", False)],
            basis(ex["_meta"])),
    }

    pages.append(dict(
        path="/small-employer",
        title="Maryland FAMLI for Employers Under 15 Staff: What Changes",
        description=("Employers with fewer than 15 employees pay no Maryland FAMLI employer share, "
                     "but still withhold and remit the employee half. How headcount is counted "
                     "across all states, and what still applies."),
        og_desc=("Under 15 staff? No employer share, but you still withhold and remit 0.45%. The "
                 "headcount counts every state under one EIN, and that catches people out."),
        h1="Maryland FAMLI for employers with fewer than 15 employees",
        lede=("An employer with fewer than 15 employees pays <b>no employer share</b> of Maryland "
              "FAMLI. It still withholds the 0.45 percent employee share and still remits it every "
              "quarter. The 15 is counted across every state under one federal EIN, not just "
              "Maryland."),
        breadcrumb_name="Employers under 15 staff",
        tool_text=("Enter your Maryland headcount and your total headcount under one EIN. The "
                   "calculator applies the right band and shows what each side pays."),
        body=body,
        faq=[
            ("Do employers with fewer than 15 employees pay Maryland FAMLI?",
             "They remit only 50 percent of the total rate, which is the employee half. The "
             "employer share is zero. The employee share is still withheld and still remitted to "
             "the Maryland Department of Labor each quarter.",
             "They remit only half the total rate, which is the employee half. The employer share "
             "is <b>zero</b>. The employee share is still withheld and still remitted each quarter."),
            ("How is the 15-employee threshold counted for Maryland FAMLI?",
             "By total headcount under the same federal EIN, counting employees inside and outside "
             "Maryland. Independent contractors are excluded. A firm with 8 employees in Maryland "
             "and 30 elsewhere has 38 employees and is not a small employer.",
             "By total headcount under the same federal EIN, <b>counting employees inside and "
             "outside Maryland</b>. Contractors are excluded. A firm with 8 in Maryland and 30 "
             "elsewhere has 38 employees and is not small."),
            ("What happens if I cross 15 employees during the year?",
             "During 2027 employer size is recalculated quarter by quarter, so the rate changes "
             "from that quarter forward and never backwards. From 2028 size is set by the average "
             "of the prior year's four quarters and fixed for the whole year.",
             "In 2027 size is recalculated quarter by quarter, so the rate changes from that "
             "quarter forward and never backwards. From 2028 it is the prior year's four-quarter "
             "average, fixed for the year."),
            ("Is a sole owner with no other employees covered by Maryland FAMLI?",
             "No. A sole owner who is the only person the entity employs is not an employer for "
             "FAMLI purposes, so there is nothing to register, withhold or remit. One employee who "
             "is not the owner puts the business in scope.",
             "No. A sole owner who is the only person the entity employs is not an employer for "
             "FAMLI purposes. One employee who is not the owner puts the business in scope."),
        ],
        sources=[
            ("COMAR 09.42.02, employer size and contributions", S["comar"]),
            ("Maryland Department of Labor, Make Contributions", S["contributions"]),
            ("Maryland Department of Labor, employer registration", S["registration"]),
        ],
        related=[
            ("/out-of-state-employees", "Out-of-state staff",
             "the blank field on the quarterly report that doubles your rate"),
            ("/contribution-rate-2027", "The 2027 rate",
             "0.9 percent, the split, and the wage cap"),
            ("/registration", "Registration",
             "required at one Maryland employee, whatever your size"),
        ],
        cta_intro="What a 30 minute call with our AI engineers does for you:",
        cta_bullets=[
            "<b>Your real headcount, tracked as it moves.</b> Size is recalculated quarterly in "
            "2027. Crossing 15 doubles your rate from that quarter, and nobody sends you a warning.",
            "<b>The blank field that doubles your rate, caught before you file.</b> Out-of-state "
            "headcount has to be on the quarterly report. Leave it empty and you are reclassified "
            "from 0.45% to 0.9%.",
            "<b>Your actual payroll file, not a typed estimate.</b> Every employee read "
            "individually, so the wage cap lands per person and the number you hand your CFO is "
            "the real one.",
        ],
    ))

    return pages
