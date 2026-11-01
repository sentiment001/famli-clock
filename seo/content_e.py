# -*- coding: utf-8 -*-
"""Content for /maryland-paid-family-leave, /sick-and-safe-leave-vs-famli and
/social-security-wage-base-2027. Added 31 October 2026 (SEO handoff 30 Oct, Job 1).

Every money figure is read out of examples.json, which comes from the shipped
engine. The numbers typed here are statutory thresholds and SSA's published
contribution and benefit base table, each listed in FACTS_REGISTER.md (F17 to F20)
with the paragraph it came from. qa.py checks the SSA table's current-year row
against the engine's CONFIG and the per-employee maximum against the cap times the
rate, so a stale or mistyped figure fails the build.
"""

from build import S, src, money, money0
from content_a import wex, cap_fig, cap_on

CHECKED = "31 October 2026"

# SSA, Contribution and Benefit Base, https://www.ssa.gov/oact/cola/cbb.html,
# read 31 October 2026. Whole dollars, exactly as SSA's table prints them. The row
# for the engine's own wage_cap_year is NOT typed here: it is read from CONFIG via
# examples.json, so this table can never disagree with the calculator.
SSA_CBB = [
    (2017, 127200), (2018, 128400), (2019, 132900), (2020, 137700),
    (2021, 142800), (2022, 147000), (2023, 160200), (2024, 168600),
    (2025, 176100), (2026, 184500),
]


def ssa_rows(meta):
    rows = [(y, a) for y, a in SSA_CBB if y < meta["wage_cap_year"]]
    rows.append((meta["wage_cap_year"], int(meta["wage_cap"])))
    return rows


def basis_capped(meta):
    """Provenance line for examples where the wage base bites. basis() in
    content_a says wages are spread evenly, which is not true here, so this one
    says what the engine actually assumed."""
    return ("Computed by famliclock.com from the published 2027 rate of 0.9 percent and the "
            "%d Social Security taxable maximum of %s, on %s. Each higher earner is assumed to "
            "be paid evenly through the year, and everyone else shares the rest of the payroll "
            "evenly. These are estimates, not a filing."
            % (meta["wage_cap_year"], cap_fig(meta), CHECKED))


def build(ex):
    meta = ex["_meta"]
    E1 = ex["E1_small"]
    E2 = ex["E2_large"]
    E4 = ex["E4_oos_big"]
    WS = ex["W_cap_std"]
    WM = ex["W_cap_small"]
    WE = ex["W_firm_even"]
    WC = ex["W_firm_capped"]

    pages = []

    # ============================================= /maryland-paid-family-leave
    body = """
<h2>One program, three names</h2>
<p>The Maryland Department of Labor's name for it is Family and Medical Leave Insurance, FAMLI
for short. Its own FAQ says people also call it paid family and medical leave, or just paid
leave. %(src_q1)s You will also see PFML, short for paid family and
medical leave. It is one program under one law: Title 8.3 of the Labor and Employment Article, with the details in COMAR
09.42. %(src_comar)s</p>
<p>It is not the paid sick days employers already give under the Healthy Working Families Act.
The Department puts the difference simply: sick days are for an everyday cold, and FAMLI is for
a serious illness. %(src_q15)s The two laws count employees differently too, which we cover in
<a href="/sick-and-safe-leave-vs-famli">sick and safe leave vs FAMLI</a>.</p>

<h2>When it starts</h2>
<p>Employers pay in first. Employees claim a year later.</p>
<div class="tblwrap">
<table class="tbl">
<caption>Maryland paid family leave, the employer calendar</caption>
<thead><tr><th>When</th><th>What happens</th></tr></thead>
<tbody>
<tr><th>15 November 2026</th><td>The private plan Declaration of Intent window closes. It opened 1
September. The date is set by the Secretary of Labor, not by statute.</td></tr>
<tr><th>One pay period before your first deduction</th><td>Written notice to employees that
deductions are starting. The date depends on your payroll calendar.</td></tr>
<tr><th>1 January 2027</th><td>Contributions apply to wages paid from this date.</td></tr>
<tr><th>30 April 2027</th><td>First quarterly wage and hour report and payment, for wages paid
January to March.</td></tr>
<tr><th>July 2027</th><td>Notice to employees six months before benefits begin.</td></tr>
<tr><th>Summer to 1 October 2027</th><td>Private plan applications for employers that want
one.</td></tr>
<tr><th>By 1 November 2027</th><td>The Secretary sets the 2028 rate.</td></tr>
<tr><th>January 2028</th><td>Benefits begin. Employees can file claims.</td></tr>
</tbody>
</table>
</div>
<p class="note">Sources: the April 2026 FAQs %(src_q12)s, private plans %(src_pp)s, COMAR
09.42.02.05D %(src_05D)s and LE 8.3-601 %(src_le601)s. Every date in your own case, including
the notice date, is on <a href="/deadlines-2027">the 2027 deadlines page</a>.</p>

<h2>What it costs</h2>
<p>The 2027 rate is <b>0.9 percent</b> of wages, split 0.45 percent employer and 0.45 percent
employee. %(src_q21)s Employers may take the employee half out of pay. They don't have to, and an
employer can choose to pay it for everyone. Each November from 2027, the Department announces the
next year's rate, and the law caps it at 1.2 percent. %(src_le601)s</p>
<p>In dollars: a 40-person employer with a $3.2 million Maryland payroll owes %(e2_total)s for
2027. If it withholds the full employee half, %(e2_ee)s of that comes out of pay. The
<a href="/contribution-rate-2027">contribution rate page</a> has the full working.</p>

<h2>Small employers are not exempt</h2>
<p>An employer with fewer than 15 employees pays no employer share. It still remits the 0.45
percent employee half, which it can take from pay or cover itself. %(src_q21)s The 15 counts
everyone under the same federal EIN, in Maryland and in every other state. %(src_q26)s Exactly
15 is not small.</p>
<p>A 12-person employer on a $780,000 payroll remits %(e1_total)s for 2027, and none of it is
employer money. In 2027 the Department decides size quarter by quarter, so an employer that
hires past 14 moves to the full rate from that quarter. And yes, a family that employs a nanny
is an employer for FAMLI. %(src_q55)s More on <a href="/small-employer">the small employer
rules</a>.</p>

<h2>Which wages count</h2>
<p>Gross wages, using the same definition Maryland uses for unemployment insurance. Not net pay.
%(src_q31)s Wages count up to the Social Security wage base, per employee, per calendar year.
That base is the %(cap_year)d Social Security taxable maximum of %(cap)s, which SSA
published on %(cap_on)s. The Department applies that cap separately to each job an employee
holds. %(src_q39)s Details on <a href="/social-security-wage-base-2027">the 2027 wage base
page</a>.</p>
<p>Only work done in Maryland counts. Someone who lives in Pennsylvania and works in Baltimore
is covered. Someone who lives in Maryland and works full time in Virginia is not. %(src_q53)s</p>

<h2>What to do before January</h2>
<ol>
<li>Register with the FAMLI Division. Every employer with at least one Maryland employee has
to, whatever its size. %(src_reg)s Here is <a href="/registration">what you need to
register</a>.</li>
<li>Decide about a private plan. The Declaration of Intent closes 15 November 2026. Once that
date passes, the next step is a private plan application, due 1 October 2027. A private plan
won't lower your 2027 cost, because the same contributions go into escrow instead. More on
<a href="/private-plan-declaration-of-intent">the Declaration of Intent page</a>.</li>
<li>Decide whether to withhold. A skipped deduction can't come out of a later paycheck. The one
exception is an employee who earned too little in a pay period to cover it, a tipped worker for
example; then you get up to 6 pay periods. %(src_q40)s</li>
<li>Send the written notice at least one pay period before deductions start. %(src_05D)s So the
date is different for every payroll calendar. The calculator works out yours, and
<a href="/employee-notice">the notice page</a> explains why.</li>
<li>Get ready to report. Each quarter you file gross wages and hours for every Maryland
employee, on the FAMLI website rather than BEACON. The first report and payment are due 30 April
2027. %(src_q35)s</li>
</ol>

<h2>What employees get, from January 2028</h2>
<p>Up to <b>12 weeks</b> of paid leave in a benefit year. An employee who has their own serious
health condition and also welcomes a child in the same year can get up to 24 weeks. %(src_q96)s
Pay is up to 90 percent of wages, with a ceiling of <b>$1,000 a week</b>. %(src_q92)s</p>
<p>To qualify, an employee needs 680 hours of work in Maryland over the four calendar quarters
reported before the claim or the leave, whichever comes first. Hours from more than one employer
count. %(src_q64)s Leave can be used for a new child (birth, adoption or foster care), the
employee's own serious health condition, a family member's serious health condition, or a family
member's military deployment. %(src_q69)s The employer holds the job and keeps health benefits
going during the leave. %(src_q105)s</p>

<div class="flag"><b>Looking for paid maternity or parental leave in Maryland?</b>
FAMLI covers bonding with a new child, including adoption and foster care, from January 2028.
Parents can take it any time in the first year after the birth or placement, and both parents
can be on leave at the same time. A baby born in late 2027 still counts, as long as the leave
is taken after benefits start and within that first year. %(src_q71)s Until then, paid time off
for a new child comes from your employer's own policy, or from earned sick and safe leave,
which Maryland lets you use for maternity or paternity leave. %(src_hwfa_uses)s Employees with
questions can call FAMLI Customer Care on (410) 525-4010.</div>
""" % {
        "src_q1": src("FAMLI FAQ, question 1", S["faq"]),
        "src_comar": src("COMAR 09.42", S["comar"]),
        "src_q15": src("FAMLI FAQ, question 15", S["faq"]),
        "src_q12": src("FAMLI FAQ", S["faq"]),
        "src_pp": src("MD Labor", S["privatePlans"]),
        "src_05D": src("COMAR 09.42.02.05D", S["comar"]),
        "src_le601": src("LE 8.3-601", S["rate"]),
        "src_q21": src("FAMLI FAQ, question 21", S["faq"]),
        "src_q26": src("question 26", S["faq"]),
        "src_q55": src("question 55", S["faq"]),
        "src_q31": src("FAMLI FAQ, questions 31 and 37", S["faq"]),
        "src_q39": src("question 39", S["faq"]),
        "src_q53": src("question 53", S["faq"]),
        "src_reg": src("MD Labor, registration", S["registration"]),
        "src_q40": src("FAMLI FAQ, question 40", S["faq"]),
        "src_q35": src("questions 33 and 35", S["faq"]),
        "src_q96": src("FAMLI FAQ, question 96", S["faq"]),
        "src_q92": src("questions 92 and 93", S["faq"]),
        "src_q64": src("question 64", S["faq"]),
        "src_q69": src("question 69", S["faq"]),
        "src_q105": src("questions 105 and 106", S["faq"]),
        "src_q71": src("FAMLI FAQ, questions 71 and 72", S["faq"]),
        "src_hwfa_uses": src("MD Labor sick and safe leave FAQ", S["hwfaFaq"]),
        "cap_year": meta["wage_cap_year"],
        "cap": cap_fig(meta),
        "cap_on": cap_on(meta),
        "e2_total": money(E2["annual_total"]),
        "e2_ee": money(E2["annual_employee"]),
        "e1_total": money(E1["annual_total"]),
    }

    pages.append(dict(
        path="/maryland-paid-family-leave",
        title="Maryland Paid Family Leave (FAMLI) for Employers: 2027",
        description=("Maryland paid family leave (FAMLI) for employers: contributions from 1 Jan "
                     "2027 at 0.9%, benefits from Jan 2028, small employer rules and what to do "
                     "now."),
        og_desc=("Maryland paid family leave, also called FAMLI: who pays, when it starts, what "
                 "small employers owe, and the five things to do before January 2027."),
        h1="Maryland paid family leave (FAMLI): the employer guide",
        lede=("Maryland paid family leave is the state's <b>FAMLI</b> program. Employers pay in "
              "on wages paid from <b>1 January 2027</b>, at 0.9 percent split between employer "
              "and employee. Employees can claim paid leave from <b>January 2028</b>."),
        breadcrumb_name="Maryland paid family leave",
        tool_text=("The state publishes the rate. It does not publish your notice date or your "
                   "first payment. Five questions get you both, plus a printable report."),
        body=body,
        faq=[
            ("Does Maryland have paid family leave?",
             "Yes. Maryland's Family and Medical Leave Insurance program, FAMLI, is paid family "
             "and medical leave. Employers start contributing on wages paid from 1 January 2027 "
             "and employees can claim benefits from January 2028.",
             "Yes. Maryland's Family and Medical Leave Insurance program, <b>FAMLI</b>, is paid "
             "family and medical leave. Contributions start on wages paid from 1 January 2027 "
             "and benefits start in January 2028."),
            ("When does Maryland paid family leave start?",
             "Contributions apply to wages paid from 1 January 2027, with the first quarterly "
             "payment due 30 April 2027. Benefits begin in January 2028.",
             "Contributions apply to wages paid from <b>1 January 2027</b>, and the first "
             "quarterly payment is due 30 April 2027. Benefits begin in <b>January 2028</b>."),
            ("Is Maryland paid family leave the same as FAMLI?",
             "Yes. FAMLI, Family and Medical Leave Insurance, is the official name of Maryland's "
             "paid family and medical leave program, run by the Maryland Department of Labor. "
             "Colorado has a separate program with the same acronym.",
             "Yes. FAMLI is the official name of Maryland's paid family and medical leave "
             "program, run by the Maryland Department of Labor. Colorado has a separate program "
             "with the same acronym."),
            ("Do small businesses pay Maryland paid family leave?",
             "Yes. An employer with fewer than 15 employees, counting every state under one "
             "federal EIN, pays no employer share but still remits the 0.45 percent employee "
             "share. It can take that from pay or cover it itself.",
             "Yes. With fewer than 15 employees, counting every state under one EIN, there is "
             "no employer share, but the business still remits the <b>0.45 percent</b> employee "
             "share. It can take that from pay or cover it itself."),
            ("Is Maryland paid family leave deducted from paychecks?",
             "It can be. Employers may withhold up to half the 2027 rate, 0.45 percent of wages, "
             "from pay, but they don't have to. A skipped deduction can't be taken from a later "
             "paycheck, except when the employee earned too little that pay period to cover it.",
             "It can be. Employers may withhold up to <b>0.45 percent</b> of wages, but they "
             "don't have to. A skipped deduction can't be taken from a later paycheck, except "
             "when the employee earned too little that pay period to cover it."),
        ],
        sources=[
            ("Maryland Department of Labor, FAMLI FAQs, April 2026", S["faq"]),
            ("FAMLI contributions FAQ, April 2026", S["contribFaq"]),
            ("COMAR 09.42, Family and Medical Leave Insurance", S["comar"]),
            ("Labor and Employment Article &sect;8.3-601, rate", S["rate"]),
            ("Maryland Department of Labor, employer registration", S["registration"]),
            ("Maryland Department of Labor, private plans", S["privatePlans"]),
            ("Social Security Administration, contribution and benefit base", S["ssaCap"]),
        ],
        related=[
            ("/contribution-rate-2027", "The 2027 contribution rate",
             "0.9 percent, the split, and two worked examples"),
            ("/small-employer", "Employers under 15 staff",
             "no employer share, and how the 15 is counted"),
            ("/employee-notice", "The written notice",
             "due one pay period before deductions start"),
            ("/deadlines-2027", "Every 2027 deadline",
             "reports, payments and notices in date order"),
        ],
        cta_intro="What a 30 minute call with our AI engineers does for you:",
        cta_bullets=[
            "<b>Every Maryland client checked at once.</b> For a payroll bureau or CPA firm: one "
            "file of client payrolls in, each client's band, notice date and first payment out.",
            "<b>The headcount trap caught early.</b> Size counts every state under the EIN, and "
            "it is decided quarter by quarter in 2027. We flag clients about to cross 15.",
            "<b>The rest of the calendar, not just FAMLI.</b> The same build watches the other "
            "deadlines you track by hand and tells you when one moves.",
        ],
    ))

    # =========================================== /sick-and-safe-leave-vs-famli
    body = """
<h2>The short version</h2>
<p>Sick and safe leave is time off the employer gives and pays for itself, earned an hour at a
time. FAMLI is insurance. Employers and employees pay into a state fund, and the fund, or an
approved private plan, pays the employee during longer leave. The Department's own example: sick
days are for an everyday cold, and FAMLI is for a serious illness. %(src_q15)s</p>
<p>Both cover almost every employer with Maryland staff, so you will usually owe both. One
doesn't replace the other.</p>

<h2>Side by side</h2>
<div class="tblwrap">
<table class="tbl">
<caption>Maryland sick and safe leave and FAMLI, compared</caption>
<thead><tr><th></th><th>Sick and safe leave</th><th>FAMLI</th></tr></thead>
<tbody>
<tr><th>The law</th><td>Healthy Working Families Act, LE &sect;&sect;3-1301 to 3-1311</td>
<td>LE Title 8.3 and COMAR 09.42</td></tr>
<tr><th>In force</th><td>Since 11 February 2018</td><td>Contributions from 1 January 2027.
Benefits from January 2028.</td></tr>
<tr><th>Who is covered</th><td>Employees whose main work location is Maryland, except those
who regularly work under 12 hours a week and a few other groups</td><td>Every employee in a
position based in Maryland. No job categories are exempt.</td></tr>
<tr><th>The 15-employee line</th><td>15 or more: paid leave. 14 or fewer: unpaid leave is
enough.</td><td>Fewer than 15: no employer share. 15 or more: the employer pays half.</td></tr>
<tr><th>How the 15 is counted</th><td>Average monthly headcount over the previous year. The
Commissioner counts Maryland employees only.</td><td>Everyone under the same federal EIN, in
every state. Quarter by quarter during 2027.</td></tr>
<tr><th>Who pays</th><td>The employer, as normal wages for the hours off</td><td>0.9 percent
of wages into a fund. The employer may take up to half from pay.</td></tr>
<tr><th>How much leave</th><td>1 hour per 30 worked. The employer can cap it at 40 hours earned
and 64 used a year, and 64 banked.</td><td>Up to 12 weeks a year, or 24 when a serious health
condition and a new child fall in the same year</td></tr>
<tr><th>Pay during leave</th><td>The employee's normal rate (paid tier)</td><td>Up to 90
percent of wages, at most $1,000 a week</td></tr>
<tr><th>Before it can be used</th><td>The employer can make new hires wait 106 calendar
days</td><td>680 hours in Maryland over the four reported quarters, with any employers</td></tr>
<tr><th>What it is for</th><td>Own illness or care, preventive care, a family member's
illness, maternity or paternity leave, and absences from domestic violence, sexual assault or
stalking</td><td>A new child, own serious health condition, a family member's serious health
condition, and a family member's military deployment</td></tr>
<tr><th>Protection</th><td>No adverse action for using it</td><td>The job is held and health
benefits continue</td></tr>
<tr><th>Run by</th><td>Commissioner of Labor and Industry, Maryland Department of Labor</td>
<td>FAMLI Division, Maryland Department of Labor</td></tr>
</tbody>
</table>
</div>
<p class="note">Sick and safe leave: LE &sect;3-1304 %(src_law)s, the Department's sick and safe
leave FAQ %(src_hfaq)s and its employee notice %(src_poster)s. FAMLI: the April 2026 FAQs
%(src_faq)s.</p>

<h2>The two 15-employee lines are not the same line</h2>
<p>Both laws split employers at 15, and they count in different ways. For sick and safe leave
the number is the average monthly headcount over the previous year, %(src_law)s and the
Commissioner looks only at people employed in Maryland. %(src_hfaq)s For FAMLI it is everyone
under the federal EIN, inside and outside Maryland, decided each quarter during 2027.
%(src_q26)s</p>
<p>Take a firm with 10 people in its Maryland office and 30 more in Virginia. For sick and safe
leave it is under 15, so unpaid leave meets the law. For FAMLI it has 40 employees and pays the
full 0.9 percent. On a $750,000 Maryland payroll that is %(e4_total)s for 2027, half of it
employer money. An employer that sizes itself once and applies the answer to both laws gets one
of them wrong.</p>

<h2>Can employees use sick days during FAMLI leave?</h2>
<p>The employer can't make them. The law stops employers from requiring employees to use paid
time off, including sick days and vacation, before or alongside FAMLI. An employer can require
unpaid leave, such as federal FMLA leave, to run at the same time. %(src_q117)s</p>
<p>The employee can choose to. If the employer allows it, an employee can use accrued leave to
top up the FAMLI benefit to 100 percent of wages, but only if the employee agrees. %(src_q122)s
An employee can also skip FAMLI entirely for a qualifying event and use their own leave
instead. Nobody has to file a claim. %(src_q118)s</p>
<p>Employer parental leave is treated differently. Leave designed for a FAMLI purpose, which the
Department calls Alternative FAMLI Purpose Leave, can be required to run at the same time as
FAMLI, and those weeks count toward the 12. %(src_q119)s</p>

<h2>What changes on the pay stub in January 2027</h2>
<p>Sick and safe leave already requires a statement of used and available leave with each pay.
%(src_hfaq)s That stays. What's new is a FAMLI deduction, if you choose to withhold, on wages
paid from 1 January 2027. %(src_q8)s Employees must get written notice at least one pay period
before it first appears. %(src_05D)s If you cover the employee half yourself, there is no
deduction to show.</p>
<p>The FAMLI quarterly wage and hour report is new too, and it is separate from your
unemployment insurance filing in BEACON. It reports gross wages. %(src_q33)s</p>

<h2>Which one applies</h2>
<p>A two-day flu is sick and safe leave. Twelve weeks after surgery or a birth, from 2028, is
FAMLI, perhaps with sick days topping up pay if you allow it and the employee agrees. Time off
after domestic violence is sick and safe leave: FAMLI does not cover it. %(src_q70)s</p>
""" % {
        "src_q15": src("FAMLI FAQ, question 15", S["faq"]),
        "src_law": src("LE 3-1304", S["hwfaLaw"]),
        "src_hfaq": src("MD Labor sick and safe leave FAQ", S["hwfaFaq"]),
        "src_poster": src("employee notice", S["hwfaPoster"]),
        "src_faq": src("FAMLI FAQ", S["faq"]),
        "src_q26": src("FAMLI FAQ, question 26", S["faq"]),
        "src_q117": src("FAMLI FAQ, questions 116 and 117", S["faq"]),
        "src_q122": src("question 122", S["faq"]),
        "src_q118": src("question 118", S["faq"]),
        "src_q119": src("questions 119 and 120", S["faq"]),
        "src_q8": src("FAMLI FAQ, question 8", S["faq"]),
        "src_05D": src("COMAR 09.42.02.05D", S["comar"]),
        "src_q33": src("FAMLI FAQ, questions 33 and 37", S["faq"]),
        "src_q70": src("FAMLI FAQ, question 70", S["faq"]),
        "e4_total": money(E4["annual_total"]),
    }

    pages.append(dict(
        path="/sick-and-safe-leave-vs-famli",
        title="Maryland Sick and Safe Leave vs FAMLI: What Employers Owe",
        description=("Maryland sick and safe leave vs FAMLI: two laws, two 15-employee lines "
                     "counted different ways, who pays, and whether sick days can run with "
                     "FAMLI."),
        og_desc=("The Healthy Working Families Act and Maryland FAMLI side by side: coverage, "
                 "the 15-employee lines, who pays, and how sick days and FAMLI interact."),
        h1="Maryland sick and safe leave vs FAMLI",
        lede=("Maryland employers now run two leave laws that sound alike. <b>Sick and safe "
              "leave</b>, under the Healthy Working Families Act, has applied since February "
              "2018 and the employer pays for it. <b>FAMLI</b> is insurance: contributions start "
              "on wages paid from 1 January 2027, and benefits from January 2028."),
        breadcrumb_name="Sick and safe leave vs FAMLI",
        tool_text=("Sick and safe leave you already run. FAMLI is the new one: enter your "
                   "headcount and payroll for your 2027 cost and your notice date."),
        body=body,
        faq=[
            ("Is FAMLI the same as Maryland sick and safe leave?",
             "No. Sick and safe leave, under the Healthy Working Families Act, is leave the "
             "employer provides and pays for directly. FAMLI is an insurance program funded by "
             "contributions from 1 January 2027, paying benefits from January 2028.",
             "No. Sick and safe leave is leave the employer provides and pays for directly. "
             "FAMLI is <b>insurance</b>, funded by contributions from 1 January 2027 and paying "
             "benefits from January 2028."),
            ("Do employers with fewer than 15 employees have to give sick and safe leave?",
             "Yes. Employers with 14 or fewer employees must provide sick and safe leave, but it "
             "can be unpaid. The count is the average monthly number of employees in the "
             "previous year, and the Commissioner counts Maryland employees only.",
             "Yes, but it can be <b>unpaid</b>. The count is the average monthly headcount in "
             "the previous year, and the Commissioner counts Maryland employees only."),
            ("Can an employer require employees to use sick leave during FAMLI leave?",
             "No. Maryland does not let employers require employees to use paid time off, "
             "including sick days, with FAMLI. An employer may allow employees to use accrued "
             "leave to top up the FAMLI benefit to full pay if the employee agrees.",
             "No. Employers can't require employees to use paid time off, sick days included, "
             "with FAMLI. They may <b>allow</b> employees to top up the benefit to full pay with "
             "accrued leave, if the employee agrees."),
            ("Does the 15-employee count work the same way for both laws?",
             "No. Sick and safe leave uses the previous year's average monthly headcount in "
             "Maryland. FAMLI counts every employee under the federal EIN in every state, "
             "quarter by quarter during 2027.",
             "No. Sick and safe leave uses last year's average monthly <b>Maryland</b> "
             "headcount. FAMLI counts everyone under the EIN in <b>every state</b>, quarter by "
             "quarter during 2027."),
        ],
        sources=[
            ("Labor and Employment Article &sect;3-1304, earned sick and safe leave", S["hwfaLaw"]),
            ("Maryland Department of Labor, Healthy Working Families Act FAQs", S["hwfaFaq"]),
            ("Maryland Department of Labor, sick and safe leave employee notice", S["hwfaPoster"]),
            ("Maryland Department of Labor, FAMLI FAQs, April 2026", S["faq"]),
            ("COMAR 09.42, Family and Medical Leave Insurance", S["comar"]),
        ],
        related=[
            ("/maryland-paid-family-leave", "Maryland paid family leave",
             "the employer guide to FAMLI"),
            ("/small-employer", "FAMLI for employers under 15",
             "no employer share, and the EIN-wide count"),
            ("/out-of-state-employees", "Out-of-state staff",
             "why they change your FAMLI rate"),
            ("/payroll-providers", "For payroll providers",
             "setting up FAMLI for a book of Maryland clients"),
        ],
        cta_intro="What a 30 minute call with our AI engineers does for you:",
        cta_bullets=[
            "<b>Both counts, for every client.</b> Sick and safe leave counts Maryland staff "
            "only. FAMLI counts the whole EIN. We run both from one payroll file and show where "
            "they disagree.",
            "<b>One leave policy check.</b> We read your current PTO and parental leave policy "
            "against the FAMLI rules and list what has to change before 2028.",
            "<b>The rest of the calendar, not just FAMLI.</b> The same build watches the other "
            "deadlines you track by hand and tells you when one moves.",
        ],
    ))

    # ========================================= /social-security-wage-base-2027
    trend = "".join(
        '<tr><th>%d</th><td class="num">%s</td></tr>' % (y, "{:,}".format(a))
        for y, a in reversed(ssa_rows(meta)))
    q = WS["quarters"]
    qc = WC["quarters"]
    std_max = money(WS["annual_total"])
    std_er = money(WS["annual_employer"])
    std_ee = money(WS["annual_employee"])
    sm_max = money(WM["annual_total"])

    body = """
<h2>The 2027 figure</h2>
<p>For wages paid in 2027, the Social Security contribution and benefit base, also called the
taxable maximum, is <b>%(cap)s</b>. %(src_cbb)s SSA announced it on %(cap_on)s, with the 2027
cost-of-living adjustment. %(src_fact)s Social Security tax is 6.2 percent each for employee
and employer on wages up to that figure, and nothing above it.</p>

<h2>How the wage base has moved</h2>
<p>SSA sets the base each year from changes in the national average wage index. In a few years it
didn't move at all. These are SSA's own figures, and we don't project future years.</p>
<div class="tblwrap">
<table class="tbl">
<caption>Social Security contribution and benefit base, 2017 to %(cap_year)d</caption>
<thead><tr><th>Year</th><th class="num">Wage base, US dollars</th></tr></thead>
<tbody>%(trend)s</tbody>
</table>
</div>
<p class="note">Source: %(src_cbb_t)s</p>

<h2>What it caps for Maryland FAMLI</h2>
<p>Maryland FAMLI uses SSA's number directly. All wages an employer pays an employee count for
contributions up to the Social Security wage base each calendar year. %(src_04A)s For 2027 that
means FAMLI stops on the same %(cap)s that Social Security does.</p>
<div class="tblwrap">
<table class="tbl">
<caption>The most FAMLI can take for one employee in 2027</caption>
<thead><tr><th>Employer with 15 or more, 0.9 percent</th><th class="num">2027</th></tr></thead>
<tbody>
<tr><th>Employer half</th><td class="num">%(std_er)s</td></tr>
<tr><th>Employee half</th><td class="num">%(std_ee)s</td></tr>
<tr class="total"><th>Total</th><td class="num">%(std_max)s</td></tr>
</tbody>
<thead><tr><th>Employer with fewer than 15, 0.45 percent</th><th class="num">2027</th></tr></thead>
<tbody>
<tr><th>Employer half</th><td class="num">%(sm_er)s</td></tr>
<tr><th>Employee half</th><td class="num">%(sm_ee)s</td></tr>
<tr class="total"><th>Total</th><td class="num">%(sm_max)s</td></tr>
</tbody>
</table>
</div>
<p>Those are the calculator's own figures for one Maryland employee paid $250,000 in 2027. Paid
evenly through the year, that employee reaches the cap in the fourth quarter. The engine counts
%(q4_base)s of their fourth-quarter wages, and nothing after that.</p>
%(wex)s
<p>From the third quarter, contributions drop: the two higher earners cross the cap and stop
counting. That's why spreading the payroll evenly, which is the calculator's default, can
overstate the bill when some people earn above %(cap)s. &ldquo;Make this exact&rdquo; in the
calculator fixes that.</p>

<h2>Two employers, two caps</h2>
<p>The Maryland Department of Labor works the cap out <b>separately for each job</b>.
%(src_q19)s Someone with two Maryland employers can have contributions taken on wages up to
%(cap)s at each one. Each employer counts only the wages it pays, so neither one stops early
because of the other job.</p>
<p>The cap also resets every 1 January. Wages paid in December 2027 count toward 2027. Wages
paid on 1 January 2028 start a new year, under whatever base SSA sets for 2028.</p>

<h2>Where the cap does not apply</h2>
<p>Medicare. Since 1994 there has been no limit on wages taxed for Medicare's hospital insurance,
at 1.45 percent each for employee and employer. %(src_cbb)s So an employee paid $250,000 pays
Medicare on all of it, and Social Security and FAMLI on the first %(cap)s.</p>
<p>The base caps wages, not the FAMLI rate. The 2027 rate is 0.9 percent. The law lets the
Secretary raise it to as much as 1.2 percent of wages up to the base, and the 2028 rate is due
by 1 November 2027. %(src_le601)s</p>

<h2>When it changes next</h2>
<p>SSA sets a new figure each year. The 2027 figure came out on %(cap_on)s. The calculator and
every page on this site use it, and we update them when SSA publishes the 2028 figure.</p>
""" % {
        "cap": cap_fig(meta),
        "cap_on": cap_on(meta),
        "cap_year": meta["wage_cap_year"],
        "src_cbb": src("SSA, contribution and benefit base", S["ssaCap"]),
        "src_fact": src("SSA 2027 COLA fact sheet", S["ssaFact"]),
        "src_cbb_t": src("SSA, contribution and benefit base table", S["ssaCap"]),
        "src_04A": src("COMAR 09.42.02.04A", S["comar"]),
        "src_q19": src("FAMLI contributions FAQ, question 19", S["contribFaq"]),
        "src_le601": src("LE 8.3-601", S["rate"]),
        "trend": trend,
        "std_max": std_max, "std_er": std_er, "std_ee": std_ee,
        "sm_max": sm_max,
        "sm_er": money(WM["annual_employer"]),
        "sm_ee": money(WM["annual_employee"]),
        "q4_base": money0(q[3]["base_cents"]),
        "wex": wex(
            "A 20-person employer with two people above the cap",
            [("Employees working in Maryland", "20"),
             ("Total employees under one EIN", "20"),
             ("Annual Maryland payroll", money0(WC["input"]["md_payroll"] * 100)),
             ("Payroll frequency", "Every two weeks"),
             ("Paid above the wage base", "2 people, %s between them"
              % money0(WC["input"]["high_earner_wages"] * 100))],
            [("Band", "Standard, 15 or more", False),
             ("Wages counted after the cap", money(WC["base_cents"]), False),
             ("Employer share, full year 2027", money(WC["annual_employer"]), False),
             ("Employee share, full year 2027, from pay or paid by you",
              money(WC["annual_employee"]), False),
             ("Total, full year 2027", money(WC["annual_total"]), True),
             ("Quarter 1 and quarter 2, each", money(qc[0]["due_cents"]), False),
             ("Quarter 3", money(qc[2]["due_cents"]), False),
             ("Quarter 4", money(qc[3]["due_cents"]), False),
             ("Same payroll with nobody above the cap", money(WE["annual_total"]), False)],
            basis_capped(meta)),
    }

    pages.append(dict(
        path="/social-security-wage-base-2027",
        title="Social Security Wage Base 2027: %s and Maryland FAMLI" % cap_fig(meta),
        description=("The 2027 Social Security wage base is %s, published by SSA on %s. "
                     "What it caps for Maryland FAMLI, per employee and per job."
                     % (cap_fig(meta), cap_on(meta))),
        og_desc=("The 2027 Social Security wage base is %s. Maryland FAMLI stops at the same "
                 "figure: the most it takes per employee, and why the cap is per job."
                 % cap_fig(meta)),
        h1="Social Security wage base 2027 and the Maryland FAMLI cap",
        lede=("The 2027 Social Security wage base is <b>%s</b>, published by SSA on %s. "
              "Maryland FAMLI uses the same number: contributions stop once an employee's 2027 "
              "wages from one employer pass it." % (cap_fig(meta), cap_on(meta))),
        breadcrumb_name="Social Security wage base 2027",
        tool_text=("Got people paid above the cap? Use \"Make this exact\" in the calculator to "
                   "count them separately and see your real 2027 figure."),
        body=body,
        faq=[
            ("What is the Social Security wage base for 2027?",
             "%s. The Social Security Administration published it on %s. Social Security tax "
             "applies to wages up to that amount, and Maryland FAMLI contributions use the same "
             "cap." % (cap_fig(meta), cap_on(meta)),
             "<b>%s</b>, published by SSA on %s. Social Security tax applies to wages up to that "
             "amount, and Maryland FAMLI uses the same cap." % (cap_fig(meta), cap_on(meta))),
            ("What is the most Maryland FAMLI can take for one employee in 2027?",
             "%s at an employer with 15 or more employees, split %s each side if the employer "
             "withholds the employee half. At an employer with fewer than 15, it is %s, all of "
             "it the employee half." % (std_max, std_er, sm_max),
             "<b>%s</b> at an employer with 15 or more employees, %s each side if the employer "
             "withholds the employee half. With fewer than 15, it is <b>%s</b>, all of it the "
             "employee half." % (std_max, std_er, sm_max)),
            ("Does the FAMLI wage cap apply per employer?",
             "Yes. The Maryland Department of Labor determines the cap separately for each job, "
             "so an employee with two employers can have contributions on wages up to the cap at "
             "each one.",
             "Yes. The Department works out the cap <b>separately for each job</b>, so someone "
             "with two employers can have contributions on wages up to the cap at each."),
            ("Is there a wage base cap on Medicare tax?",
             "No. SSA states there has been no limit on wages taxed for Medicare's hospital "
             "insurance since 1994. The 1.45 percent applies to all wages.",
             "No. There has been no limit on Medicare hospital insurance wages since 1994. The "
             "1.45 percent applies to all wages."),
        ],
        sources=[
            ("Social Security Administration, contribution and benefit base", S["ssaCap"]),
            ("Social Security Administration, 2027 COLA fact sheet", S["ssaFact"]),
            ("COMAR 09.42.02.04A, wages subject to contributions", S["comar"]),
            ("FAMLI contributions FAQ, April 2026", S["contribFaq"]),
            ("Labor and Employment Article &sect;8.3-601, rate", S["rate"]),
        ],
        related=[
            ("/contribution-rate-2027", "The 2027 contribution rate",
             "0.9 percent, the split, and who sets it"),
            ("/maryland-paid-family-leave", "Maryland paid family leave",
             "the employer guide to FAMLI"),
            ("/small-employer", "Employers under 15 staff",
             "why the most you remit per employee is half"),
        ],
        cta_intro="What a 30 minute call with our AI engineers does for you:",
        cta_bullets=[
            "<b>Your payroll file, person by person.</b> The cap lands on each employee "
            "separately. We read every record so the figure you hand your CFO is the real one.",
            "<b>Next year's cap and rate, applied for you.</b> SSA resets the base each year and "
            "the Secretary sets the 2028 rate by 1 November 2027. Both move every figure.",
            "<b>The rest of the calendar, not just FAMLI.</b> The same build watches the other "
            "deadlines you track by hand and tells you when one moves.",
        ],
    ))

    return pages
