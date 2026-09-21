# -*- coding: utf-8 -*-
"""Content for /registration and /payroll-providers."""

from build import S, src, money, money0, CALENDLY
from content_a import wex, basis


def build(ex):
    E1 = ex["E1_small"]
    E2 = ex["E2_large"]
    E4b = ex["E4b_oos_small"]
    pages = []

    # ================================================================ /registration
    body = """
<h2>Who has to register</h2>
<p>The Maryland Department of Labor puts it about as plainly as an agency ever does:</p>
<blockquote><p>&ldquo;If you have at least one employee in Maryland, you are required to
register online. There are no exceptions under state law.&rdquo; %(src_reg)s</p></blockquote>
<p>One employee. No size threshold, no industry carve-out, no exemption for employers who
intend to use a private plan. A small employer that pays no employer share still registers. An
employer that has filed a Declaration of Intent still registers, because registration is a
prerequisite for filing one.</p>
<p>The one case that falls outside the program entirely is the sole owner who is the only
person their entity employs. They are not an employer for FAMLI purposes and have nothing to
register. %(src_sole)s One employee who is not the owner ends that.</p>

<h2>There is no registration deadline, and that is the problem</h2>
<p>Registration is open and carries no stated deadline. It is therefore the easiest thing on
the whole calendar to leave until later, and it is the one thing that blocks everything else:
the Declaration of Intent, the quarterly wage report, the contribution payment, all of it runs
through the FAMLI account.</p>
<p>Two of the five Declaration of Intent stages are registration and the Login.gov identity
check that precedes it. An employer that starts registering in November has already lost the
private plan window.</p>

<h2>What you need in front of you</h2>
<div class="tblwrap">
<table class="tbl">
<caption>Information required to register an employer with FAMLI</caption>
<thead><tr><th>Group</th><th>What is asked for</th></tr></thead>
<tbody>
<tr><th>Employer details</th><td>Federal EIN, legal name, any doing-business-as name, NAICS
code, physical address, mailing address, business email</td></tr>
<tr><th>Authorized Officer</th><td>Full name, job title, work email, work phone number</td></tr>
<tr><th>Resident agent</th><td>Name, physical address, email, phone number</td></tr>
</tbody>
</table>
</div>
<p class="note">Source: Maryland Department of Labor, employer registration guidance. %(src_reg2)s</p>

<h2>The Authorized Officer, and Login.gov</h2>
<p>An Authorized Officer is a person legally permitted to act in an official capacity for the
employer. They complete the initial registration, they can see and manage everything in the
FAMLI account, and they sign Power of Attorney documents.</p>
<p>Creating the account needs an email and phone number, or an existing Login.gov account.
<b>Identity verification needs more</b>: a Social Security number and a driver's licence or
state ID card. That step is the one that surprises people, because the officer named on the
form is often a finance director or an owner who is not expecting to hand over personal
identity documents to a state portal.</p>
<p>Decide who that person is before you start, not during. If the online identity check fails,
the fallback is in-person verification at a Post Office, and that turns a same-day step into a
multi-day one.</p>

<h2>Register first, then everything else</h2>
<ol>
<li><b>Register.</b> Open now, no deadline, blocks everything.</li>
<li><b>Decide on a private plan, if you want one.</b> The Declaration of Intent closes 15
November 2026. See <a href="/private-plan-declaration-of-intent">the Declaration of
Intent</a>.</li>
<li><b>Send the written notice.</b> At least one full pay period before your first 2027
withholding. See <a href="/employee-notice">the employee notice</a>.</li>
<li><b>Start withholding</b> on wages paid from 1 January 2027.</li>
<li><b>Report and pay quarterly</b>, first due 30 April 2027. See
<a href="/deadlines-2027">the 2027 deadlines</a>.</li>
</ol>

<h2>Two things registration does not do</h2>
<ul>
<li><b>It does not set your rate.</b> Your band comes from your headcount under the EIN,
recalculated quarterly in 2027. See <a href="/small-employer">employers under 15 staff</a>.</li>
<li><b>It does not file your Declaration of Intent.</b> Registration is stage three of five.
The consultation with a licensed Maryland insurance agent, and the signed form that comes out
of it, still have to happen.</li>
</ul>
""" % {
        "src_reg": src("Maryland Department of Labor, employer registration", S["registration"]),
        "src_reg2": src("Employer registration", S["registration"]),
        "src_sole": src("COMAR 09.42.01.01B(21)(b)", S["comar"]),
    }

    pages.append(dict(
        path="/registration",
        title="Maryland FAMLI Employer Registration: Who Must Register and How",
        description=("Every Maryland employer with at least one employee must register for FAMLI, "
                     "with no exceptions under state law. What information you need, who the "
                     "Authorized Officer is, and why the Login.gov step catches people out."),
        og_desc=("One Maryland employee means you register. No size threshold, no exceptions. What "
                 "to have ready, and the identity check that turns a same-day job into a week."),
        h1="Registering your business for Maryland FAMLI",
        lede=("Any employer with <b>at least one employee in Maryland</b> must register online for "
              "FAMLI. There are no exceptions under state law and there is no size threshold. "
              "Registration is open now, has no deadline, and blocks everything else you have to "
              "do."),
        breadcrumb_name="Employer registration",
        tool_text=("Before you register, find out what the program is going to cost you and which "
                   "dates you are working to. Five questions, under a minute."),
        body=body,
        faq=[
            ("Who has to register for Maryland FAMLI?",
             "Any employer with at least one employee in Maryland. The Maryland Department of Labor "
             "states there are no exceptions under state law. Employers with fewer than 15 staff "
             "register too, even though they pay no employer share.",
             "Any employer with at least one employee in Maryland. The Department states there are "
             "<b>no exceptions under state law</b>. Employers under 15 staff register too, even "
             "though they pay no employer share."),
            ("Is there a deadline to register for Maryland FAMLI?",
             "No deadline is published. Registration is open now. In practice it blocks everything "
             "else, including the Declaration of Intent for a private plan and the quarterly wage "
             "report, so leaving it late has consequences even without a stated deadline.",
             "No published deadline; registration is open now. It <b>blocks everything else</b>, "
             "including the Declaration of Intent and the quarterly wage report, so leaving it late "
             "still costs you."),
            ("What is a FAMLI Authorized Officer?",
             "A person legally permitted to act in an official capacity on behalf of the employer. "
             "They complete registration, can view and manage all aspects of the FAMLI account and "
             "sign Power of Attorney documents. Identity verification through Login.gov requires a "
             "Social Security number and a driver's licence or state ID.",
             "A person legally permitted to act in an official capacity for the employer. They "
             "complete registration and manage the account. Login.gov identity verification needs "
             "a Social Security number and a driver's licence or state ID."),
        ],
        sources=[
            ("Maryland Department of Labor, Understand Employer Registration", S["registration"]),
            ("Maryland FAMLI registration portal", S["register"]),
            ("COMAR 09.42.01, definitions", S["comar"]),
            ("Maryland Department of Labor, for employers", S["employers"]),
        ],
        related=[
            ("/private-plan-declaration-of-intent", "The Declaration of Intent",
             "registration is stage three of five, and the window closes 15 November"),
            ("/small-employer", "Employers under 15 staff",
             "you register either way; the rate is what differs"),
            ("/deadlines-2027", "Every 2027 deadline",
             "what registration unlocks, in order"),
        ],
        cta_intro="What a 30 minute call with our AI engineers does for you:",
        cta_bullets=[
            "<b>Registration data you only assemble once.</b> EIN, NAICS, resident agent, Authorized "
            "Officer. The same fields come back for every state program you are about to join.",
            "<b>The critical path after registration.</b> Declaration of Intent, notice date, first "
            "withholding, first payment. Four dates, three of which move with your payroll calendar.",
            "<b>The rest of the compliance calendar too.</b> FAMLI is one line on a list you keep by "
            "hand. The same build watches the others and tells you when one moves.",
        ],
    ))

    # ========================================================== /payroll-providers
    body = """
<h2>The problem is not the arithmetic. It is the multiplication.</h2>
<p>For one employer, Maryland FAMLI is five facts: a headcount band, a rate, a wage cap, a
notice date and a Declaration of Intent decision. Any competent bookkeeper can work that out
in ten minutes.</p>
<p>For a bureau with fifty Maryland clients it is five facts times fifty, most of them
different, three of them changing during the year, and one of them (the notice date) derived
from each client's own payroll calendar rather than from the statute. That is not a ten minute
job fifty times. It is a register you have to build and then keep.</p>

<h2>The per-client checklist</h2>
<div class="tblwrap">
<table class="tbl">
<caption>What you need to hold for every Maryland client</caption>
<thead><tr><th>Field</th><th>Why it moves</th></tr></thead>
<tbody>
<tr><th>Maryland-localized headcount</th><td>Sets whose wages are subject to contributions.</td></tr>
<tr><th>Total headcount under the EIN, all states</th><td>Sets the rate band. Recalculated
quarterly through 2027, then a prior-year four-quarter average from 2028.</td></tr>
<tr><th>Rate band, small or standard</th><td>0.45 percent under 15, 0.9 percent at 15 and
above. Can change mid-year in 2027.</td></tr>
<tr><th>Withhold or absorb</th><td>Client decision, per pay period, and the default if nobody
decides is expensive.</td></tr>
<tr><th>First 2027 pay date and pay frequency</th><td>Derives the written notice date. Every
client with a different pay calendar has a different deadline.</td></tr>
<tr><th>Declaration of Intent status</th><td>Closes 15 November 2026. After that the answer is
fixed for a year.</td></tr>
<tr><th>Registration status and Authorized Officer</th><td>Blocks everything. The Login.gov
identity step is client-side and you cannot do it for them.</td></tr>
<tr><th>Wage cap in force</th><td>SSA resets it every October and it changes every client's
figures at once.</td></tr>
</tbody>
</table>
</div>

<h2>The four that will actually bite you</h2>
<h3>1. Every client's notice date is different</h3>
<p>The rule is written notice at least one full pay period before withholding commences.
%(src_05D)s There is no single date. A weekly client and a monthly client with the same first
January pay date owe the notice a week apart, and a semimonthly client is different again. Our
<a href="/employee-notice">employee notice page</a> works four of them through.</p>

<h3>2. The out-of-state headcount field</h3>
<p>To be classified small, a client's quarterly wage report has to state how many of its
employees work outside Maryland. %(src_08CD)s Leave it blank and the client is deemed not
small and pays 0.9 percent. For a ten-person Maryland client with two staff elsewhere that is
%(e4b_extra)s a year, for an empty box on a form your team filed. Agree now, in writing, who
owns that field.</p>

<h3>3. The deemed election</h3>
<p>If the deduction does not get made, the employer is considered to have elected to pay the
employee's portion, per pay period, unrecoverable. %(src_07A)s A setup that goes in late, or a
client who says &ldquo;hold off until I decide&rdquo;, turns into the client's money and then
into a conversation about whose fault it was.</p>

<h3>4. Mid-year band changes in 2027</h3>
<p>Size is recalculated quarter by quarter during 2027. A client hiring through the year can
cross 15 and double its rate from that quarter forward. Nobody sends a warning. If your
register holds the EIN-wide headcount you will see it coming; if it holds only the Maryland
number you will not.</p>

<h2>Two clients, side by side</h2>
%(wex1)s
%(wex2)s
<p>Same program, same quarter, two entirely different answers, and the difference is headcount
rather than payroll.</p>

<h2>What we can do about the multiplication</h2>
<p>We are 02Launch, an AI engineering firm out of Google and Microsoft. We built this
calculator, and we build the thing behind it for firms that have this problem at scale.</p>
<p><b>A Client FAMLI Register, free, within 48 hours of a call:</b> every Maryland client on
one sheet, with headcount tier, rate, wage cap, derived notice date, Declaration of Intent
status and first remittance date. Built from whatever you already have, a client list and a
payroll export is enough. No charge and no obligation, because the fastest way to show you
what a build looks like is to hand you one.</p>
<p>If it is useful, the same work extends: the register recomputes itself each quarter, flags
the clients who crossed a band, and reprices everything the day SSA publishes the wage cap in
October. That is an engagement. The register is not.</p>
""" % {
        "src_05D": src("COMAR 09.42.02.05D", S["comar"]),
        "src_08CD": src("COMAR 09.42.02.08C and D", S["comar"]),
        "src_07A": src("COMAR 09.42.02.07A", S["comar"]),
        "e4b_extra": money(E4b["cost_of_unreported_out_of_state"]),
        "wex1": wex(
            "Client A: 12 staff, all in Maryland, paid every two weeks",
            [("Maryland headcount", "12"), ("EIN headcount, all states", "12"),
             ("Annual Maryland payroll", money0(E1["input"]["md_payroll"] * 100)),
             ("Pay frequency", "Every two weeks")],
            [("Band", "Small, under 15", False),
             ("Rate", "0.45%", False),
             ("Employer share for 2027", money(E1["annual_employer"]), False),
             ("Withheld from staff for 2027", money(E1["annual_employee"]), False),
             ("Total remitted for 2027", money(E1["annual_total"]), True),
             ("Q1 payment due 30 April 2027", money(E1["q1_payment"]), False)],
            basis(ex["_meta"])),
        "wex2": wex(
            "Client B: 40 staff, all in Maryland, paid monthly",
            [("Maryland headcount", "40"), ("EIN headcount, all states", "40"),
             ("Annual Maryland payroll", money0(E2["input"]["md_payroll"] * 100)),
             ("Pay frequency", "Monthly")],
            [("Band", "Standard, 15 or more", False),
             ("Rate", "0.90%", False),
             ("Employer share for 2027", money(E2["annual_employer"]), False),
             ("Withheld from staff for 2027", money(E2["annual_employee"]), False),
             ("Total remitted for 2027", money(E2["annual_total"]), True),
             ("Q1 payment due 30 April 2027", money(E2["q1_payment"]), False)],
            basis(ex["_meta"])),
    }

    pages.append(dict(
        path="/payroll-providers",
        title="Maryland FAMLI for Payroll Providers and Bookkeepers: Setting Up Every Client",
        description=("A per-client checklist for Maryland FAMLI: headcount tier, rate, wage cap, "
                     "notice date and Declaration of Intent status. Plus the four things that bite "
                     "a bureau running fifty clients rather than one."),
        og_desc=("Fifty clients, fifty headcounts, fifty notice dates, every quarter. The per-client "
                 "checklist, the four traps, and a free Client FAMLI Register."),
        h1="Maryland FAMLI for payroll bureaus and bookkeepers",
        lede=("For one employer, Maryland FAMLI is five facts. For a bureau with fifty Maryland "
              "clients it is five facts times fifty, three of which change during the year and one "
              "of which (<b>the written notice date</b>) is derived from each client's own payroll "
              "calendar rather than from the statute."),
        breadcrumb_name="Payroll providers and bookkeepers",
        tool_text=("Run a client through it in under a minute and hand them the printable report. "
                   "Free, no sign up, and nothing you enter leaves the page."),
        body=body,
        faq=[
            ("What do payroll providers need to set up for Maryland FAMLI?",
             "For each Maryland client: the Maryland-localized headcount, the total headcount under "
             "the EIN across all states, the resulting rate band, the withhold-or-absorb decision, "
             "the first 2027 pay date and frequency that derive the notice date, the Declaration of "
             "Intent status, and the registration status.",
             "Per client: Maryland headcount, EIN-wide headcount, the resulting rate band, the "
             "withhold-or-absorb decision, the first 2027 pay date and frequency that derive the "
             "notice date, Declaration of Intent status, and registration status."),
            ("Is the Maryland FAMLI notice date the same for every client?",
             "No. The notice is due at least one full pay period before withholding begins, so a "
             "weekly client, a biweekly client and a monthly client with the same first January pay "
             "date each owe the notice on a different day.",
             "No. It is due at least one full pay period before withholding begins, so weekly, "
             "biweekly, semimonthly and monthly clients with the same first January pay date each "
             "owe it on a different day."),
            ("Who is responsible for the out-of-state headcount field on the quarterly report?",
             "Maryland does not assign it between the employer and its payroll provider, which is "
             "why it gets missed. If the field is blank the client is deemed not to be a small "
             "employer and pays 0.9 percent instead of 0.45 percent, so agree ownership in writing "
             "before the first filing.",
             "Maryland does not assign it between employer and provider, which is why it gets "
             "missed. A blank field means the client is deemed not small and pays 0.9 percent. "
             "Agree ownership in writing before the first filing."),
        ],
        sources=[
            ("COMAR 09.42.02, contributions, size and reporting", S["comar"]),
            ("Maryland Department of Labor, Make Contributions", S["contributions"]),
            ("Maryland Department of Labor, employer registration", S["registration"]),
            ("Maryland Department of Labor, private plans", S["privatePlans"]),
        ],
        related=[
            ("/out-of-state-employees", "The out-of-state headcount field",
             "the one that doubles a client's rate silently"),
            ("/employee-notice", "The written notice",
             "a different date for every client, derived not published"),
            ("/deadlines-2027", "Every 2027 deadline",
             "the calendar you will be running fifty times"),
        ],
        cta_intro="What a 30 minute call with our AI engineers gets you, free, within 48 hours:",
        cta_bullets=[
            "<b>Your Client FAMLI Register.</b> Every Maryland client on one sheet: headcount tier, "
            "rate, wage cap, notice date, Declaration of Intent status, first remittance date. "
            "Free, no obligation.",
            "<b>Built from what you already have.</b> A client list and a payroll export is enough. "
            "We do not need access to your systems to build the first one.",
            "<b>Then it recomputes itself.</b> Quarterly band changes flagged, and everything "
            "repriced the day SSA publishes the wage cap in October. That part is an engagement; "
            "the register is not.",
        ],
    ))

    return pages
