# -*- coding: utf-8 -*-
"""Content for /private-plan-declaration-of-intent and /deadlines-2027."""

from build import S, src, money, money0
from content_a import wex, basis


def build(ex):
    E5 = ex["E5_doi"]
    E1 = ex["E1_small"]
    pages = []

    # ======================================= /private-plan-declaration-of-intent
    body = """
<h2>What the Declaration of Intent is</h2>
<p>An employer that wants to meet its FAMLI obligation through a private plan rather than the
State Plan has to tell the Maryland Department of Labor first, during a window that opened on
Tuesday 1 September 2026 and closes on Sunday 15 November 2026. %(src_pp)s That notice is the
Declaration of Intent.</p>
<p>The Declaration is not the application. It is the statement that you intend to apply, and
it is what keeps the door open. The private plan application itself comes later: applications
open in summer 2027 and are due 1 October 2027.</p>
<p><b>15 November 2026 is a Sunday.</b> Nobody is on the phone at FAMLI Customer Care that day,
and a portal problem on the Saturday has nowhere to go. The last business day before the close
is <b>Friday 13 November 2026</b>, and that is the date the calculator plans to. Treat the 15th
as the legal fact and the 13th as the operational one.</p>

<h2>It is five stages, not a form</h2>
<p>The submission itself takes minutes. Everything in front of it does not.</p>
<ol>
<li>Designate an Authorized Officer and gather the EIN, NAICS code and resident agent
details.</li>
<li>The Authorized Officer clears Login.gov identity verification, which needs a Social
Security number and a driver's licence or state ID.</li>
<li>Register the employer in the FAMLI portal.</li>
<li>Find a licensed Maryland insurance agent and get a consultation booked.</li>
<li>Hold the consultation and get the signed <a href="%(consult)s" target="_blank"
rel="noopener">Proof of Private Plan Consultation</a> form back.</li>
</ol>
<p>Then upload the signed form in the FAMLI account and attest. %(src_pp2)s</p>
<p>In our planning estimates the agent consultation is the long pole: roughly 15 business days
typically, and up to 25 if the agent is unfamiliar with the product. A cold start is a
multi-week project, not an afternoon. Those durations are ours, not the Department's, and are
marked as estimates wherever the calculator shows them. The only stage duration that is set by
regulation is the decision itself.</p>

<h2>The decision clock</h2>
<p>FAMLI has <b>15 business days</b> from submittal to approve or deny. %(src_310A2)s That
clock is the reason the calculator treats <b>Wednesday 21 October 2026</b> as the
submit-early-enough-to-survive-a-rejection date: 15 business days before the deadline. Submit
after that and your first attempt is effectively your only attempt.</p>
<p>An approved Declaration takes effect on the first day of the next quarter, so a December
approval still starts on 1 January 2027. %(src_310A3)s</p>
<p class="note">Two things this page leans on that no primary source states outright: that a
rejected Declaration can be corrected and resubmitted before 15 November, and that the 15
business days start the business day after submittal. Both are reasonable readings and both
are how the calculator models it. Neither is written down by the Department. If either matters
to your plan, get it confirmed on (410) 525-4010 before you rely on it.</p>

<h2>A private plan does not save you money in 2027</h2>
<p>This is the sentence most employers have not heard, and it changes the decision.</p>
<p>If your Declaration is accepted you still collect the same contributions from 1 January
2027. You hold them in escrow instead of remitting them to the State. The cash cost is
identical; only the destination changes. %(src_310A1d)s</p>
<p>A 25-person employer on a $1.75m Maryland payroll collects %(e5_total)s during 2027 either
way. With a private plan that money sits in escrow rather than going to Annapolis.</p>
<p>And the escrow has an expiry on it: all Declarations of Intent lapse on <b>31 December
2027</b>. Your plan has to be approved before 1 January 2028 or the escrowed money is remitted
to the State with interest.</p>

<h2>What a private plan has to be</h2>
<p>A private plan must provide <b>the same level of benefits and service as the State Plan, or
better</b>. %(src_pp)s Carriers set their own premiums and may charge an employer more than
the State Plan would have. Two things are fixed: a carrier cannot cause more than 0.45 percent
to be withheld from employees, and the annual application fee runs from $100 to $1,000 by
headcount. %(src_305F)s Approval lasts one year and the fee is annual.</p>
<div class="tblwrap">
<table class="tbl">
<caption>Annual private plan application fee, by employer size</caption>
<thead><tr><th>Employees</th><th class="num">Fee</th></tr></thead>
<tbody>
<tr><th>1 to 14</th><td class="num">$100</td></tr>
<tr><th>15 to 49</th><td class="num">$250</td></tr>
<tr><th>50 to 199</th><td class="num">$500</td></tr>
<tr><th>200 to 499</th><td class="num">$600</td></tr>
<tr><th>500 to 999</th><td class="num">$750</td></tr>
<tr><th>1,000 or more</th><td class="num">$1,000</td></tr>
<tr class="total"><th>Self-insured plan</th><td class="num">$1,000</td></tr>
</tbody>
</table>
</div>

<h2>Self-insuring, and the door that has already closed</h2>
<p>Self-insurance requires <b>50 or more employees localized in Maryland</b>. There was an
exception for smaller employers, but it needed a FAMLI-compliant plan already in effect by
<b>31 July 2026</b>, and that date has passed. %(src_305K)s If you have fewer than 50 Maryland
employees and did not already have a compliant plan in place by the end of July, a commercial
plan through a carrier is the route open to you.</p>

<h2>If you miss 15 November 2026</h2>
<p>Nothing breaks. You are on the State Plan for 2027, your contributions start on 1 January
2027 exactly as they would have anyway, and your 2027 cash cost is unchanged. You apply for a
private plan for 2028 when applications open in summer 2027.</p>
<p>The thing you lose is a year of holding your own money and a year of setting your own plan
terms. For most employers under 50 staff that is not the emergency it sounds like. For an
employer that was going to buy a carrier plan regardless, it is a real cost of a missed
deadline.</p>
""" % {
        "src_pp": src("Maryland Department of Labor, private plans", S["privatePlans"]),
        "src_pp2": src("Private plan FAQs", S["privateFaq"]),
        "consult": S["consultForm"],
        "src_310A2": src("COMAR 09.42.03.10A(2)", S["comar"]),
        "src_310A3": src("COMAR 09.42.03.10A(3)", S["comar"]),
        "src_310A1d": src("COMAR 09.42.03.10A(1)(d)", S["comar"]),
        "src_305F": src("COMAR 09.42.03.05F", S["comar"]),
        "src_305K": src("COMAR 09.42.03.05K", S["comar"]),
        "e5_total": money(E5["annual_total"]),
    }

    pages.append(dict(
        path="/private-plan-declaration-of-intent",
        title="Maryland FAMLI Private Plan: The Declaration of Intent and the 15 November Deadline",
        description=("Maryland employers intending to use a private FAMLI plan must file a "
                     "Declaration of Intent between 1 September and 15 November 2026. What it "
                     "takes, how long each stage runs, and why it does not cut your 2027 cost."),
        og_desc=("The Declaration of Intent window runs 1 September to 15 November 2026. It is five "
                 "stages, not a form, and an approved private plan does not reduce your 2027 cash "
                 "cost."),
        h1="Maryland FAMLI private plans and the Declaration of Intent",
        lede=("An employer intending to meet Maryland FAMLI through a private plan must submit a "
              "<b>Declaration of Intent between 1 September and 15 November 2026</b>. The 15th is "
              "a Sunday, so Friday 13 November is the practical deadline, and the work behind the "
              "submission takes weeks, not hours."),
        breadcrumb_name="Private plan and Declaration of Intent",
        tool_text=("Tell the calculator how far you have already got and it works out whether the "
                   "remaining stages still fit before 13 November, at three different paces."),
        body=body,
        faq=[
            ("When is the Maryland FAMLI Declaration of Intent due?",
             "Between 1 September and 15 November 2026 for a private plan covering 2027. 15 "
             "November 2026 is a Sunday, so Friday 13 November is the last business day before the "
             "close and the practical deadline.",
             "Between <b>1 September and 15 November 2026</b> for a private plan covering 2027. The "
             "15th is a Sunday, so Friday 13 November is the last business day and the practical "
             "deadline."),
            ("Does a private FAMLI plan save money in 2027?",
             "No. If the Declaration is accepted the employer still collects the same contributions "
             "from 1 January 2027 and holds them in escrow instead of remitting them to the State. "
             "The cash cost is identical; only the destination changes.",
             "No. You still collect the same contributions from 1 January 2027 and hold them in "
             "<b>escrow</b> instead of remitting them. The cash cost is identical; only the "
             "destination changes."),
            ("How long does FAMLI take to decide on a Declaration of Intent?",
             "15 business days from submittal, set by regulation. Submitting 15 business days "
             "before the deadline, which is 21 October 2026, leaves room to correct and resubmit "
             "if the first attempt is rejected.",
             "<b>15 business days</b> from submittal, set by regulation. Submitting by 21 October "
             "2026 leaves room to correct and resubmit if the first attempt is rejected."),
            ("Can a small Maryland employer self-insure its FAMLI plan?",
             "Self-insurance requires 50 or more employees localized in Maryland. An exception for "
             "smaller employers required a FAMLI-compliant plan already in effect by 31 July 2026, "
             "which has passed. A commercial plan through a carrier is the remaining route.",
             "Only with 50 or more employees localized in Maryland. The exception for smaller "
             "employers needed a compliant plan already in effect by <b>31 July 2026</b>, which has "
             "passed. A carrier plan is the remaining route."),
            ("What happens if I miss the 15 November 2026 Declaration of Intent deadline?",
             "You are on the State Plan for 2027. Contributions start 1 January 2027 either way and "
             "the 2027 cash cost is unchanged. You apply for a private plan for 2028 when "
             "applications open in summer 2027, due 1 October 2027.",
             "You are on the State Plan for 2027. Contributions start 1 January 2027 either way and "
             "your 2027 cash cost is unchanged. You apply for 2028 when applications open in summer "
             "2027, due 1 October 2027."),
        ],
        sources=[
            ("Maryland Department of Labor, Understand Your Plan", S["privatePlans"]),
            ("Proof of Private Plan Consultation form", S["consultForm"]),
            ("FAMLI private plan FAQs", S["privateFaq"]),
            ("COMAR 09.42.03, private employer plans", S["comar"]),
        ],
        related=[
            ("/deadlines-2027", "Every 2027 deadline",
             "where the Declaration sits in the wider calendar"),
            ("/registration", "Registration",
             "stage three of five, and nothing moves until it is done"),
            ("/contribution-rate-2027", "The 2027 rate",
             "the amount you escrow is the amount you would have remitted"),
        ],
        cta_intro="What a 30 minute call with our AI engineers does for you:",
        cta_bullets=[
            "<b>A real critical path, not a deadline.</b> Five stages, three of them outside your "
            "control, with one hard date at the end. We map it against your actual start point.",
            "<b>Escrow you can actually account for.</b> An approved plan means holding contributions "
            "rather than remitting them, every pay period, reconciled every quarter.",
            "<b>The rest of the calendar, not just this deadline.</b> The Declaration expires 31 "
            "December 2027 and the plan application is due 1 October 2027. Both are easy to lose.",
        ],
    ))

    # ============================================================ /deadlines-2027
    body = """
<h2>The whole calendar, in order</h2>
<p>Registration has no deadline and everything else waits on it, so it sits at the top of the
list rather than in a date slot.</p>
<div class="tblwrap">
<table class="tbl">
<caption>Maryland FAMLI dates, from now to the first benefit claims</caption>
<thead><tr><th>Date</th><th>What is due</th><th>Notes</th></tr></thead>
<tbody>
<tr><th>Open now, no deadline</th><td>Register the employer with FAMLI</td>
<td>Required at one Maryland employee. Nothing else can happen until it is done.</td></tr>
<tr><th>Tue 1 Sep to Sun 15 Nov 2026</th><td>Declaration of Intent, private plans only</td>
<td>Friday 13 November is the last business day before the close.</td></tr>
<tr><th>Wed 21 Oct 2026</th><td>Submit the Declaration early enough to survive a rejection</td>
<td>15 business days before the deadline, which is FAMLI's decision window.</td></tr>
<tr><th>October 2026</th><td>SSA publishes the 2027 Social Security wage cap</td>
<td>Not a duty. Every contribution figure changes when it lands.</td></tr>
<tr><th>December 2026, employer-specific</th><td>Written notice to employees before withholding</td>
<td>At least one full pay period before your first 2027 pay date. Your date depends on your
payroll frequency.</td></tr>
<tr><th>Fri 1 Jan 2027</th><td>Withholding starts</td>
<td>Contributions are due on wages <em>paid</em> from this date.</td></tr>
<tr><th>Fri 30 Apr 2027</th><td>First quarterly report and payment, Q1 wages</td>
<td>Covers wages paid 1 January to 31 March 2027.</td></tr>
<tr><th>Fri 2 Jul 2027</th><td>Six months before benefits commence notice</td>
<td>The nominal date, 3 July 2027, is a Saturday. Notices move earlier, not later.</td></tr>
<tr><th>Sat 31 Jul 2027</th><td>Q2 report and payment</td>
<td>A Saturday, so the payment moves to the next business day, Monday 2 August 2027.</td></tr>
<tr><th>Fri 1 Oct 2027</th><td>Private plan application due</td>
<td>Applications open in summer 2027. Private plan employers only.</td></tr>
<tr><th>Sun 31 Oct 2027</th><td>Q3 report and payment</td>
<td>A Sunday, so the payment moves to Monday 1 November 2027.</td></tr>
<tr><th>Mon 1 Nov 2027</th><td>The Secretary must set the 2028 contribution rate</td>
<td>Not a duty. The statute caps the rate at 1.2 percent.</td></tr>
<tr><th>Fri 31 Dec 2027</th><td>All Declarations of Intent expire</td>
<td>The plan must be approved before 1 January 2028 or the escrow is remitted with interest.</td></tr>
<tr><th>January 2028</th><td>Benefits begin</td>
<td>Employees can start claiming. The first claims land Monday 3 January 2028.</td></tr>
<tr><th>Mon 31 Jan 2028</th><td>Q4 2027 report and payment</td>
<td>Covers wages paid 1 October to 31 December 2027.</td></tr>
</tbody>
</table>
</div>

<h2>The quarterly rhythm, once it starts</h2>
<p>Reports and payments are quarterly, due at the end of the month following each quarter.
%(src_08)s</p>
<div class="tblwrap">
<table class="tbl">
<caption>Quarterly wage report and contribution payment dates</caption>
<thead><tr><th>Wages paid</th><th>Report and payment due</th><th>Falls on</th></tr></thead>
<tbody>
<tr><th>1 January to 31 March</th><td>30 April</td><td>Friday in 2027</td></tr>
<tr><th>1 April to 30 June</th><td>31 July</td><td>Saturday in 2027, so Monday 2 August</td></tr>
<tr><th>1 July to 30 September</th><td>31 October</td><td>Sunday in 2027, so Monday 1 November</td></tr>
<tr><th>1 October to 31 December</th><td>31 January</td><td>Monday in 2028</td></tr>
</tbody>
</table>
</div>
<p>Where a <b>payment</b> date falls at a weekend it moves to the next business day. <b>Notice</b>
dates get no such relief and move earlier instead. %(src_08E)s That asymmetry is small and it
catches people, which is why the calculator computes both rather than printing a generic
calendar.</p>

<h2>What happens if you pay late</h2>
<p>Interest runs at <b>1.5 percent a month, or part of a month</b>, on the unpaid amount.
%(src_09A)s The Secretary may also assess a penalty of up to <b>twice the contributions</b>
owed and order an audit of your next fiscal year. %(src_903)s</p>
<p>The bigger exposure is usually not the late payment. It is the deemed election: an employer
that fails to make the deduction is considered to have elected to pay the employee's portion
for each pay period it missed, and cannot recover it from a later cycle. %(src_07A)s</p>

<h2>2027 is a collection year, not a benefits year</h2>
<p>Contributions run for a full twelve months before any employee can claim anything. That gap
is deliberate, and it means the first year of FAMLI is, from an employer's point of view,
entirely administrative: register, notify, withhold, report, pay, four times.</p>
<p>The employee-facing half of the program starts in January 2028, and that is when the
questions change from &ldquo;what does this cost&rdquo; to &ldquo;how do I handle a claim&rdquo;.</p>

<h2>A worked example, so the dates carry a number</h2>
%(wex1)s
""" % {
        "src_08": src("COMAR 09.42.02.08", S["comar"]),
        "src_08E": src("COMAR 09.42.02.08E", S["comar"]),
        "src_09A": src("COMAR 09.42.02.09A", S["comar"]),
        "src_903": src("LE 8.3-903", S["penalties"]),
        "src_07A": src("COMAR 09.42.02.07A", S["comar"]),
        "wex1": wex(
            "A 12-person Maryland employer through the 2027 calendar",
            [("Employees working in Maryland", "12"),
             ("Total employees under one EIN", "12"),
             ("Annual Maryland payroll", money0(E1["input"]["md_payroll"] * 100)),
             ("Payroll frequency", "Every two weeks")],
            [("Notice due, safe default with no first pay date given", "1 December 2026", False),
             ("Withholding starts", "Friday 1 January 2027", False),
             ("Q1 payment, due Friday 30 April 2027", money(E1["q1_payment"]), False),
             ("Q2 payment, due Monday 2 August 2027", money(E1["quarters"][1]["due_cents"]), False),
             ("Q3 payment, due Monday 1 November 2027", money(E1["quarters"][2]["due_cents"]), False),
             ("Q4 payment, due Monday 31 January 2028", money(E1["quarters"][3]["due_cents"]), False),
             ("Total remitted for 2027", money(E1["annual_total"]), True)],
            basis(ex["_meta"])),
    }

    pages.append(dict(
        path="/deadlines-2027",
        title="Maryland FAMLI Deadlines 2027: Withholding, Quarterly Filing, First Payment",
        description=("Every Maryland FAMLI date from the 15 November 2026 Declaration of Intent to "
                     "the first benefit claims in January 2028, with the quarterly report and "
                     "payment dates and what late payment costs."),
        og_desc=("Withholding starts 1 January 2027, the first payment is due 30 April 2027, and "
                 "benefits begin January 2028. Every date in between, with the weekend rules."),
        h1="Every Maryland FAMLI deadline for 2027",
        lede=("Maryland FAMLI withholding starts on wages paid from <b>1 January 2027</b>. The "
              "first quarterly report and payment, covering January to March, is due <b>30 April "
              "2027</b>. Benefits begin in January 2028, so 2027 is a collection year with no "
              "claims in it."),
        breadcrumb_name="Deadlines 2027",
        tool_text=("The calculator returns your own dated list, including the notice date derived "
                   "from your payroll frequency, and marks which one is next."),
        body=body,
        faq=[
            ("When do Maryland FAMLI contributions start?",
             "Contributions are due on wages paid from 1 January 2027. Benefits do not begin until "
             "January 2028, so the first year is collection only.",
             "On wages <b>paid from 1 January 2027</b>. Benefits do not begin until January 2028, "
             "so the first year is collection only."),
            ("When is the first Maryland FAMLI payment due?",
             "30 April 2027, covering wages paid 1 January to 31 March 2027. Reports and payments "
             "are quarterly after that: 31 July, 31 October and 31 January.",
             "<b>30 April 2027</b>, covering wages paid 1 January to 31 March 2027. Quarterly after "
             "that: 31 July, 31 October and 31 January."),
            ("What if a Maryland FAMLI payment date falls on a weekend?",
             "A payment date that falls at a weekend moves to the next business day. Notice dates "
             "get no such relief and move earlier instead. In 2027 that puts the Q2 payment on 2 "
             "August and the Q3 payment on 1 November.",
             "A <b>payment</b> date at a weekend moves to the next business day. A <b>notice</b> "
             "date moves earlier instead. In 2027 that puts Q2 on 2 August and Q3 on 1 November."),
            ("What happens if a Maryland employer pays FAMLI contributions late?",
             "Interest runs at 1.5 percent a month or part of a month on the unpaid amount, and the "
             "Secretary may assess a penalty of up to twice the contributions owed and order an "
             "audit of the next fiscal year.",
             "Interest runs at <b>1.5 percent a month or part of a month</b> on the unpaid amount, "
             "and the Secretary may assess a penalty of up to twice the contributions owed and "
             "order an audit of your next fiscal year."),
        ],
        sources=[
            ("COMAR 09.42.02, contributions, reporting and delinquency", S["comar"]),
            ("Maryland Department of Labor, Make Contributions", S["contributions"]),
            ("Labor and Employment Article &sect;8.3-903, penalties", S["penalties"]),
            ("Maryland Department of Labor, private plans", S["privatePlans"]),
        ],
        related=[
            ("/employee-notice", "The written notice",
             "the one date on this list that is yours alone"),
            ("/private-plan-declaration-of-intent", "The Declaration of Intent",
             "the first hard deadline, and it is in November"),
            ("/payroll-providers", "Payroll bureaus and bookkeepers",
             "the same calendar, multiplied by every client"),
        ],
        cta_intro="What a 30 minute call with our AI engineers does for you:",
        cta_bullets=[
            "<b>The rest of the calendar, not just this deadline.</b> FAMLI is one line on a "
            "compliance calendar you keep by hand. The same build watches the others and tells you "
            "when one moves.",
            "<b>Dates that recompute themselves.</b> Weekend shifts, notice dates that move earlier, "
            "a wage cap that changes every October. Static reminders go stale; a build does not.",
            "<b>Your actual payroll file, not a typed estimate.</b> Every employee read "
            "individually, so the wage cap lands per person and the number you hand your CFO is the "
            "real one.",
        ],
    ))

    return pages
