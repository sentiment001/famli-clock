# -*- coding: utf-8 -*-
"""Content for /out-of-state-employees and /employee-notice."""

from build import S, src, money, money0
from content_a import wex, basis


def long_date(iso):
    """'2026-12-24' -> 'Thursday 24 December 2026'. Used only for notice dates,
    which the engine produced; the weekday is computed, never typed."""
    import datetime
    d = datetime.date(*[int(x) for x in iso.split("-")])
    return "%s %d %s %d" % (
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][d.weekday()],
        d.day,
        ["January", "February", "March", "April", "May", "June", "July", "August",
         "September", "October", "November", "December"][d.month - 1],
        d.year)


def build(ex):
    E4a = ex["E4_oos_big"]
    E4b = ex["E4b_oos_small"]
    NW, NB, NS, NM = ex["N_weekly"], ex["N_biweekly"], ex["N_semi"], ex["N_monthly"]
    ND = ex["N_default"]
    pages = []

    # ======================================================= /out-of-state-employees
    body = """
<h2>Two different numbers, doing two different jobs</h2>
<p>Maryland FAMLI asks employers for two headcounts, and they are not interchangeable.</p>
<ol>
<li><b>Employees whose work is localized in Maryland.</b> This is the group whose wages
contributions are calculated on.</li>
<li><b>Total employees under the same federal EIN, in every state.</b> This is the number
that decides whether you are a small employer or not. %(src_06A)s</li>
</ol>
<p>Mixing them up costs money in both directions. An employer that reports only its Maryland
staff as its size may claim a small-employer rate it is not entitled to. An employer that
never tells the Department how many people it has outside Maryland loses a small-employer
rate it <em>is</em> entitled to.</p>

<h2>The blank field</h2>
<p>To be classified as small, your quarterly wage report has to state how many of your
employees work outside Maryland. %(src_08CD)s Leave that field empty and you are treated as
not small, and you pay 0.9 percent instead of 0.45 percent.</p>
<p>No penalty, no notice, no correspondence. A blank field, and the rate doubles.</p>
<p>This is the one thing on this site most likely to cost a reader real money, which is why
the calculator raises it as a warning rather than a footnote whenever your EIN headcount is
higher than your Maryland headcount and you are inside the small band.</p>

<h2>What &ldquo;localized in Maryland&rdquo; means in practice</h2>
<p>Contributions are due on wages paid for qualified employment, which is work localized in
Maryland. A fully remote employee living and working in Baltimore for a Denver company is a
Maryland employee. A Maryland-headquartered company's salesperson who lives and works in
Pennsylvania is not. Independent contractors are not employees for this purpose in either
direction.</p>
<p>Edge cases (employees who split their time across state lines, employees seconded for part
of the year, staffing arrangements where two entities could each be the employer) are
genuinely hard, and neither this page nor the calculator resolves them. Ask FAMLI Customer
Care on <a href="tel:+14105254010">(410) 525-4010</a>, and get the answer in writing.</p>

<h2>Two worked examples, same Maryland payroll</h2>
<p>Both firms below employ 10 people in Maryland and pay them $750,000 a year between them.
Only the out-of-state headcount differs.</p>
%(wex1)s
%(wex2)s
<p>The Maryland payroll is identical. The bill is not. The only variable is a headcount in
another state.</p>

<h2>And the third case, which is the expensive one</h2>
<p>Take the second firm, the one entitled to the small-employer rate at %(e4b_total)s a year,
and leave the out-of-state headcount field blank on its quarterly report. It is deemed not
small and pays 0.9 percent: %(e4b_unrep)s more a year, for an empty box.</p>

<h2>What to do about it</h2>
<ul>
<li>Decide, once, which employees are localized in Maryland, and write the reasoning down.
You will be asked again every quarter.</li>
<li>Keep the EIN-wide headcount somewhere your payroll person can see it. It is not a number
most Maryland payroll runs surface.</li>
<li>Check the out-of-state field is populated before each quarterly submission, not after.</li>
<li>If you use a payroll bureau, confirm which of you owns that field. It is a common gap.
See <a href="/payroll-providers">Maryland FAMLI for payroll bureaus</a>.</li>
</ul>
""" % {
        "src_06A": src("COMAR 09.42.02.06A", S["comar"]),
        "src_08CD": src("COMAR 09.42.02.08C and D", S["comar"]),
        "e4b_total": money(E4b["annual_total"]),
        "e4b_unrep": money(E4b["cost_of_unreported_out_of_state"]),
        "wex1": wex(
            "Firm A: 10 in Maryland, 30 elsewhere, 40 under one EIN",
            [("Employees working in Maryland", "10"),
             ("Total employees under one EIN", "40"),
             ("Annual Maryland payroll", money0(E4a["input"]["md_payroll"] * 100)),
             ("Payroll frequency", "Monthly")],
            [("Band", "Standard, 15 or more under the EIN", False),
             ("Rate applied", "0.90%", False),
             ("Employer share, full year 2027", money(E4a["annual_employer"]), False),
             ("Employee share, full year 2027", money(E4a["annual_employee"]), False),
             ("Total for 2027", money(E4a["annual_total"]), True),
             ("Extra cost of the out-of-state headcount", money(E4a["absorb_delta"]) + " a year", False)],
            basis(ex["_meta"])),
        "wex2": wex(
            "Firm B: 10 in Maryland, 2 elsewhere, 12 under one EIN",
            [("Employees working in Maryland", "10"),
             ("Total employees under one EIN", "12"),
             ("Annual Maryland payroll", money0(E4b["input"]["md_payroll"] * 100)),
             ("Payroll frequency", "Monthly")],
            [("Band", "Small employer, under 15", False),
             ("Rate applied", "0.45%", False),
             ("Employer share, full year 2027", money(E4b["annual_employer"]), False),
             ("Employee share, full year 2027", money(E4b["annual_employee"]), False),
             ("Total for 2027", money(E4b["annual_total"]), True),
             ("If the out-of-state headcount field is left blank",
              money(E4b["cost_of_unreported_out_of_state"]) + " more a year", False)],
            basis(ex["_meta"])),
    }

    pages.append(dict(
        path="/out-of-state-employees",
        title="Maryland FAMLI and Out-of-State Employees: Why the Headcount Field Matters",
        description=("Maryland FAMLI counts employer size across every state under one EIN, and the "
                     "quarterly report has to state your out-of-state headcount. Leave it blank and "
                     "your rate doubles."),
        og_desc=("Employer size counts every state under one EIN. The quarterly report needs your "
                 "out-of-state headcount, and a blank field reclassifies you from 0.45% to 0.9%."),
        h1="Out-of-state employees and your Maryland FAMLI rate",
        lede=("Maryland FAMLI counts employer size across <b>every state under one federal EIN</b>, "
              "but calculates contributions only on wages for work localized in Maryland. Your "
              "quarterly report has to state the out-of-state headcount, and leaving that field "
              "blank means you are treated as not small and pay double."),
        breadcrumb_name="Out-of-state employees",
        tool_text=("The calculator asks for both numbers separately, and warns you the moment your "
                   "EIN headcount and your Maryland headcount put you on the wrong side of the line."),
        body=body,
        faq=[
            ("Do out-of-state employees count toward the Maryland FAMLI 15-employee threshold?",
             "Yes. Employer size is total headcount under the same federal EIN, counting employees "
             "inside and outside Maryland. Contributions themselves are calculated only on wages "
             "for work localized in Maryland.",
             "Yes. Employer size is total headcount under the same federal EIN, <b>inside and "
             "outside Maryland</b>. Contributions themselves are calculated only on wages for work "
             "localized in Maryland."),
            ("What happens if I do not report my out-of-state headcount?",
             "To be classified as a small employer your quarterly wage report must state how many "
             "employees work outside Maryland. If it does not, you are deemed not small and pay the "
             "full 0.9 percent instead of 0.45 percent.",
             "To be classified small, your quarterly wage report must state how many employees work "
             "outside Maryland. If it does not, you are <b>deemed not small</b> and pay 0.9 percent "
             "instead of 0.45 percent."),
            ("Are remote employees living in Maryland covered by Maryland FAMLI?",
             "An employee whose work is localized in Maryland is covered, including a remote "
             "employee who lives and works in Maryland for an out-of-state company. Independent "
             "contractors are not employees for this purpose.",
             "An employee whose work is localized in Maryland is covered, including a remote worker "
             "living and working in Maryland for an out-of-state company. Contractors are not "
             "employees for this purpose."),
        ],
        sources=[
            ("COMAR 09.42.02, employer size and quarterly reporting", S["comar"]),
            ("Maryland Department of Labor, Make Contributions", S["contributions"]),
            ("Maryland Department of Labor, for employers", S["employers"]),
        ],
        related=[
            ("/small-employer", "Employers under 15 staff",
             "what the small-employer band actually gives you"),
            ("/deadlines-2027", "Quarterly reporting dates",
             "when the report carrying that field is due"),
            ("/payroll-providers", "Payroll bureaus and bookkeepers",
             "who owns the field when someone else runs your payroll"),
        ],
        cta_intro="What a 30 minute call with our AI engineers does for you:",
        cta_bullets=[
            "<b>The blank field that doubles your rate, caught before you file.</b> Out-of-state "
            "headcount has to be on the quarterly report. Leave it empty and you are reclassified "
            "from 0.45% to 0.9%.",
            "<b>One place where both headcounts live.</b> Maryland-localized staff and EIN-wide "
            "staff are different numbers doing different jobs, and most payroll runs surface only "
            "one of them.",
            "<b>The rest of the calendar, not just this deadline.</b> FAMLI is one line on a "
            "compliance calendar you keep by hand. The same build watches the others and tells you "
            "when one moves.",
        ],
    ))

    # ============================================================ /employee-notice
    notice_rows = "".join(
        '<tr><th>%s</th><td>%s</td><td>%s</td></tr>' % (freq, first_pay, long_date(r["notice"]["notice_by"]))
        for freq, first_pay, r in [
            ("Weekly", "Friday 8 January 2027", NW),
            ("Every two weeks", "Friday 8 January 2027", NB),
            ("Twice a month", "Friday 15 January 2027", NS),
            ("Monthly", "Friday 29 January 2027", NM),
        ])

    body = """
<h2>The rule, in the regulation's own words</h2>
<blockquote><p>&ldquo;An employer shall provide written notice to all of its employees of the
commencement of contribution withholding and any changes to employee contributions at least 1
pay period prior to the commencement or change.&rdquo; %(src_05D)s</p></blockquote>
<p>Read that clause again, because the important phrase is <b>at least 1 pay period prior</b>,
not a date. There is no statutory 1 December. There is no fixed day in the calendar that
applies to everybody. The deadline is derived from the employer's own payroll schedule and it
is different for a weekly payroll and a monthly one.</p>
<p>That is the single most useful thing on this site and it is the thing nobody else computes.
The Department publishes the rule. This tells you your date.</p>

<h2>Your date depends on your first 2027 pay date</h2>
<p>Work backwards from the first pay date in 2027 on which FAMLI is withheld. Step back one
full pay period. That is your latest safe notice date, and if it lands on a weekend or a
holiday it moves <b>earlier</b>, not later: payment dates get next-business-day relief,
notice dates do not. %(src_08E)s</p>
<div class="tblwrap">
<table class="tbl">
<caption>Notice date by payroll frequency, computed by the calculator</caption>
<thead><tr><th>Payroll frequency</th><th>First 2027 pay date</th><th>Written notice due by</th></tr></thead>
<tbody>%(rows)s</tbody>
</table>
</div>
<p class="note">Computed by famliclock.com on 21 September 2026 from the pay dates shown. Change
the first pay date and every answer changes. Notice that weekly comes out <em>later</em> than
every two weeks: a shorter pay period means a shorter run-up.</p>
<p>If you do not yet know your first 2027 pay date, the calculator falls back to
<b>%(safe)s</b>, which is early enough to be safe on every one of the four frequencies. Treat
it as a safe default, not as a legal deadline, and replace it with your real date as soon as
you have it.</p>

<h2>What the notice has to say</h2>
<p>The statute sets out what the employee notice must cover: the right to receive benefits,
how to file a claim, the employee's own responsibilities in notifying the employer and the
penalties for not doing so, the right to file a complaint, job protection, and the prohibited
acts with their penalties and complaint procedures. %(src_801)s</p>
<p><b>The Department has not yet published the templates.</b> The regulations reserve the right
to require approved forms for notices, claims and dispute resolution, and say those forms will
be provided later. Until they land, an employer drafting its own notice is guessing at format,
not at content.</p>
<p>We will not draft the notice for you, and you should be wary of anyone who offers to. Once
MDOL publishes a template, using it is free and using anything else is a risk you took for no
reason. Watch <a href="%(employers)s" target="_blank" rel="noopener">the Department's employer
pages</a>.</p>

<h2>The other notices you owe, which are not one-offs</h2>
<p>The withholding notice is the one with a date in front of it. It is not the only one.</p>
<div class="tblwrap">
<table class="tbl">
<caption>Every FAMLI notice an employer owes</caption>
<thead><tr><th>Notice</th><th>When</th><th>Authority</th></tr></thead>
<tbody>
<tr><th>Before withholding starts, and before any change to employee contributions</th>
<td>At least one full pay period before</td><td>COMAR 09.42.02.05D</td></tr>
<tr><th>Rights and duties under the program</th>
<td>At hire, and annually after that</td><td>LE 8.3-801(a)</td></tr>
<tr><th>Six months before benefits commence</th>
<td>Benefits begin January 2028, so this falls in July 2027</td><td>COMAR 09.42.04.08A(1)(a)</td></tr>
<tr><th>Before a change to your FAMLI procedures or plan takes effect</th>
<td>30 days before</td><td>COMAR 09.42.04.08A(1)(d)</td></tr>
<tr><th>When an employee requests leave, or you learn leave may qualify</th>
<td>Within 5 business days</td><td>LE 8.3-801(b)(1)</td></tr>
</tbody>
</table>
</div>
<p>The six-month pre-benefit notice is the one most employers have not put in a calendar yet.
Its nominal date, 3 July 2027, is a Saturday, and because notices move earlier rather than
later it lands on the preceding business day.</p>

<h2>If you miss it</h2>
<p>Missing the notice does not by itself carry a stated penalty in the contributions chapter.
The adjacent risk is the one that costs money: if you have not told your employees, in
practice you often have not started the deduction either, and an employer that fails to make
the deduction is considered to have elected to pay the employee's portion for each pay period
it missed. %(src_07A)s For a 20-person firm on a $1.3m payroll paid every two weeks, that is
%(nd_missed)s a pay period, unrecoverable.</p>
""" % {
        "src_05D": src("COMAR 09.42.02.05D", S["comar"]),
        "src_08E": src("COMAR 09.42.02.08E", S["comar"]),
        "src_801": src("LE 8.3-801", S["notices"]),
        "src_07A": src("COMAR 09.42.02.07A", S["comar"]),
        "rows": notice_rows,
        "safe": long_date(ND["notice"]["notice_by"]),
        "employers": S["employers"],
        "nd_missed": money(ND["cost_per_missed_pay_period"]),
    }

    pages.append(dict(
        path="/employee-notice",
        title="Maryland FAMLI Employee Notice: When It Must Go Out and What It Must Say",
        description=("Maryland employers must give written notice at least one full pay period "
                     "before FAMLI withholding begins. The date depends on your payroll frequency, "
                     "not the calendar. Worked dates for weekly, biweekly, semimonthly and monthly."),
        og_desc=("Written notice is due at least one full pay period before the first FAMLI "
                 "withholding, so your date depends on your payroll calendar. Four worked dates, "
                 "and the four other notices you owe."),
        h1="The written notice to employees before Maryland FAMLI withholding",
        lede=("Maryland employers must give <b>written notice to all employees at least one full "
              "pay period before FAMLI withholding begins</b>. There is no single statutory date: "
              "the deadline is derived from your own payroll frequency, so a weekly payroll and a "
              "monthly one owe the notice on different days."),
        breadcrumb_name="Employee notice",
        tool_text=("Enter your payroll frequency, and your first 2027 pay date if you know it. The "
                   "calculator returns your exact notice deadline and puts it in a printable report."),
        body=body,
        faq=[
            ("When is the Maryland FAMLI employee notice due?",
             "At least one full pay period before contribution withholding begins. Because "
             "contributions start on wages paid from 1 January 2027, the notice date depends on the "
             "employer's payroll frequency and its first 2027 pay date. There is no single "
             "statutory calendar date that applies to every employer.",
             "At least one full pay period before withholding begins. Contributions start on wages "
             "paid from 1 January 2027, so <b>your date depends on your payroll frequency and your "
             "first 2027 pay date</b>. There is no one date for everybody."),
            ("Is 1 December 2026 the Maryland FAMLI notice deadline?",
             "No. 1 December 2026 is a safe default that works for every payroll frequency, not a "
             "statutory deadline. The regulation requires notice at least one pay period before "
             "withholding commences, which for most employers falls in December 2026.",
             "No. 1 December 2026 is a <b>safe default</b> that works for every payroll frequency, "
             "not a statutory deadline. The rule is one full pay period before withholding starts, "
             "which for most employers lands somewhere in December 2026."),
            ("Has Maryland published a FAMLI employee notice template?",
             "Not as of 21 September 2026. The regulations reserve the right to require approved "
             "templates for notices, claims and dispute resolution and say they will be provided "
             "later. Employers drafting their own notice should check the Department's employer "
             "pages before sending.",
             "Not as of 21 September 2026. The regulations reserve the right to require approved "
             "templates and say they will be provided later. Check the Department's employer pages "
             "before you send your own."),
            ("What other FAMLI notices do Maryland employers have to give?",
             "Notice of rights and duties at hire and annually, notice six months before benefits "
             "commence, notice 30 days before a change to the employer's FAMLI procedures or plan, "
             "and notice within 5 business days of an employee requesting leave or the employer "
             "learning that leave may qualify.",
             "Rights and duties at hire and annually; six months before benefits commence; 30 days "
             "before a change to your FAMLI procedures or plan; and within 5 business days of a "
             "leave request or of learning leave may qualify."),
        ],
        sources=[
            ("COMAR 09.42.02.05D, notice before withholding", S["comar"]),
            ("COMAR 09.42.04.08, employee notices", S["comar"]),
            ("Labor and Employment Article &sect;8.3-801, notice content", S["notices"]),
            ("Maryland Department of Labor, for employers", S["employers"]),
        ],
        related=[
            ("/deadlines-2027", "Every 2027 deadline",
             "the notice sits inside a longer calendar"),
            ("/contribution-rate-2027", "The 2027 rate",
             "what the notice has to tell them is coming out"),
            ("/registration", "Registration",
             "nothing else can happen until this is done"),
        ],
        cta_intro="What a 30 minute call with our AI engineers does for you:",
        cta_bullets=[
            "<b>Every notice date on one calendar, not just this one.</b> Five separate FAMLI "
            "notices with five different triggers, three of which recur forever.",
            "<b>Notice dates that move themselves.</b> Change your pay calendar and the dates "
            "change. A build that reads the calendar beats a reminder someone set once.",
            "<b>The rest of the compliance calendar too.</b> FAMLI is one line on a list you keep "
            "by hand. The same build watches the others and tells you when one moves.",
        ],
    ))

    return pages
