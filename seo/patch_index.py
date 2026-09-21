#!/usr/bin/env python3
"""Applies the SEO and GEO changes to the live index.html by string replacement.

    python3 patch_index.py --in ../index.html --out ../site/index.html

It is a PATCHER, not a rewriter. index.html carries the calculator, the engine, the
print report and the email capture, and none of that is touched. Every anchor is
asserted, and an anchor that has moved fails the run loudly rather than half-applying.
Re-run it against a newer index.html and it will either apply cleanly or tell you which
anchor moved.

WHAT IT CHANGES
  1.  <title>
  2.  meta description, keywords, og:title, og:description, twitter:title/description
  3.  the JSON-LD @graph, replaced wholesale with a superset of the original
  4.  a <link> to /famli_pages.css, placed BEFORE the inline <style> so the inline
      rules, including the whole @media print block, still win every tie
  5.  the static <h1>
  6.  the FIVE phase headline strings in the app script  <-- READ THE NEXT PARAGRAPH
  7.  a nav above the masthead
  8.  a Colorado disambiguation line under the sub headline
  9.  a crawlable content block between the CTA card and the email-capture comment

THE SIX H1 COPIES ARE THE TRAP
  There is one <h1> in the markup, and the app then overwrites it on every load from
  a five-entry phase table:  $('h1').textContent = h[0].  The phase moves five times
  between now and 2027, so whatever Googlebot sees depends on the day it crawls.
  Before this patch, three of the five phase headlines did not contain the words
  "Maryland FAMLI" at all. Change only the static one and the new H1 survives until
  the script runs, then the old text paints back over it, for crawlers as well as for
  people. All six now lead with "Maryland FAMLI calculator". The patcher asserts on
  all six and refuses to write a file where any of them is missing.
"""

import argparse
import json
import os
import re
import sys

from build import (S, SITE, VERIFIED, BUILD_DATE, CALENDLY, NAV, DISAMBIG,
                   src, money, money0, esc, nav_html, footmap_html,
                   sources_html, FOOTER, load_examples)
from content_a import wex, basis_nocap

HERE = os.path.dirname(os.path.abspath(__file__))

NEW_TITLE = ("Maryland FAMLI Calculator: 2027 Contribution, Notice Date, "
             "Private Plan Deadline")
NEW_DESC = ("Free Maryland FAMLI calculator for employers. Your 2027 contribution, the "
            "written notice date worked out from your own payroll calendar, and the private "
            "plan deadline. Five questions, no sign up.")
NEW_OG_DESC = ("Free Maryland FAMLI calculator. Your 2027 contribution, your employee notice "
               "date, and whether a private plan Declaration of Intent still fits. No sign up.")

H1_STATIC = ("Maryland FAMLI calculator: what your business owes in 2027 and the dates "
             "you must hit")

# Phase key -> (old headline, new headline). Every new one leads with the same five
# words so that the indexed H1 is stable whichever phase is live on the crawl date.
H1_PHASES = [
    ("P1_runway",
     "What Maryland FAMLI costs you, and the date you cannot miss.",
     "Maryland FAMLI calculator: what your business owes in 2027 and the dates you must hit"),
    ("P2_compressed",
     "The private plan window is closing. Here is what still fits.",
     "Maryland FAMLI calculator: the private plan window is closing, here is what still fits"),
    ("P3_notice",
     "Your employees need this notice in writing before January.",
     "Maryland FAMLI calculator: your employees need this notice in writing before January"),
    ("P4_live",
     "Contributions are live. Here is your first payment and what it is.",
     "Maryland FAMLI calculator: contributions are live, here is your first payment"),
    ("P5_steady",
     "Your Maryland FAMLI cost, quarter by quarter.",
     "Maryland FAMLI calculator: your cost, quarter by quarter"),
]


def build_ld():
    """Superset of the JSON-LD already on the page. The WebApplication node and all
    four original FAQ entries are preserved word for word; four FAQ entries, an
    Organization and a WebSite node are added."""
    return {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/",
             "name": "Maryland FAMLI Clock", "inLanguage": "en-US",
             "publisher": {"@id": "https://02launch.com/#org"}},
            {"@type": "Organization", "@id": "https://02launch.com/#org",
             "name": "02Launch", "url": "https://02launch.com",
             "description": "Forward deployed AI engineering."},
            {"@type": "WebApplication", "name": "Maryland FAMLI Clock",
             "url": SITE + "/", "applicationCategory": "BusinessApplication",
             "operatingSystem": "Any", "inLanguage": "en-US",
             "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
             "description": "Free calculator for Maryland employers. Works out your 2027 FAMLI "
                            "contribution, your employee notice date, and whether you can still "
                            "file a Declaration of Intent for a private plan before 13 November "
                            "2026.",
             "featureList": [
                 "2027 FAMLI contribution at 0.9 percent, split employer and employee",
                 "Small employer rate for fewer than 15 employees under one EIN",
                 "Written notice date derived from payroll frequency",
                 "Private plan Declaration of Intent fit check",
                 "Printable employer report"],
             "creator": {"@id": "https://02launch.com/#org"}},
            {"@type": "FAQPage", "mainEntity": [
                {"@type": "Question",
                 "name": "What is the Maryland FAMLI contribution rate for 2027?",
                 "acceptedAnswer": {"@type": "Answer", "text":
                     "0.90 percent of covered wages, split evenly between employer and employee "
                     "at 0.45 percent each. Employers with fewer than 15 employees pay no "
                     "employer share but still withhold and remit the employee share."}},
                {"@type": "Question",
                 "name": "When is the Maryland FAMLI Declaration of Intent due?",
                 "acceptedAnswer": {"@type": "Answer", "text":
                     "Sunday 15 November 2026 for a private plan covering 2027. Friday 13 "
                     "November is the last business day before it, which is the practical "
                     "deadline because FAMLI customer care is closed at the weekend. The "
                     "Declaration is a five stage process, not a form, and the insurance agent "
                     "consultation alone typically takes about 15 business days to arrange."}},
                {"@type": "Question",
                 "name": "Do Maryland employers have to give employees written notice?",
                 "acceptedAnswer": {"@type": "Answer", "text":
                     "Yes. Written notice must reach employees at least one full pay period "
                     "before the first withholding, which for most employers means December 2026 "
                     "ahead of contributions starting 1 January 2027."}},
                {"@type": "Question",
                 "name": "How is employer size determined for Maryland FAMLI?",
                 "acceptedAnswer": {"@type": "Answer", "text":
                     "By total headcount under the same federal EIN, counting employees inside "
                     "and outside Maryland. Contractors are excluded. Size is recalculated "
                     "quarterly during 2027 and moves to a four quarter average from 2028."}},
                {"@type": "Question",
                 "name": "When do Maryland FAMLI contributions start?",
                 "acceptedAnswer": {"@type": "Answer", "text":
                     "Contributions are due on wages paid from 1 January 2027. The first "
                     "quarterly report and payment, covering January to March 2027, is due 30 "
                     "April 2027. Benefits do not begin until January 2028, so 2027 is a "
                     "collection year with no claims in it."}},
                {"@type": "Question",
                 "name": "Is Maryland FAMLI the same as Colorado FAMLI?",
                 "acceptedAnswer": {"@type": "Answer", "text":
                     "No. Maryland FAMLI is administered by the Maryland Department of Labor and "
                     "is a separate program from Colorado's paid family and medical leave "
                     "insurance program of the same name. The rates, deadlines and rules are "
                     "different and nothing on this site applies to Colorado."}},
                {"@type": "Question",
                 "name": "Is there a wage cap on Maryland FAMLI contributions?",
                 "acceptedAnswer": {"@type": "Answer", "text":
                     "Yes. Wages are subject to contributions only up to the Social Security wage "
                     "base each calendar year, per employee. The 2026 figure is 184,500 US "
                     "dollars and the Social Security Administration publishes the 2027 figure in "
                     "October 2026."}},
                {"@type": "Question",
                 "name": "Does a private FAMLI plan reduce what a Maryland employer pays in 2027?",
                 "acceptedAnswer": {"@type": "Answer", "text":
                     "No. An employer with an accepted Declaration of Intent still collects the "
                     "same contributions from 1 January 2027 and holds them in escrow instead of "
                     "remitting them to the State. The cash cost is identical; only the "
                     "destination changes."}},
            ]},
        ],
    }


def content_block(ex):
    E1, E2, E3 = ex["E1_small"], ex["E2_large"], ex["E3_sole"]

    tl = """
<div class="tblwrap">
<table class="tbl">
<caption>The Maryland FAMLI calendar, in order</caption>
<thead><tr><th>Date</th><th>What is due</th></tr></thead>
<tbody>
<tr><th>Open now, no deadline</th><td>Register with FAMLI. Required at one Maryland employee,
and it blocks everything else.</td></tr>
<tr><th>1 Sep to 15 Nov 2026</th><td>Declaration of Intent, private plans only. Friday 13
November is the last business day before the close.</td></tr>
<tr><th>October 2026</th><td>The Social Security Administration sets the wage base for the
contribution year. Every figure on this page moves when it lands.</td></tr>
<tr><th>December 2026, your own date</th><td>Written notice to employees, at least one full
pay period before your first 2027 withholding.</td></tr>
<tr><th>1 January 2027</th><td>Withholding starts, on wages paid from this date.</td></tr>
<tr><th>30 April 2027</th><td>First quarterly report and payment, covering Q1 wages.</td></tr>
<tr><th>2 July 2027</th><td>Six months before benefits commence notice. The nominal 3 July is
a Saturday and notices move earlier.</td></tr>
<tr><th>1 October 2027</th><td>Private plan application due, for private plan employers.</td></tr>
<tr><th>31 December 2027</th><td>All Declarations of Intent expire.</td></tr>
<tr><th>January 2028</th><td>Benefits begin. Employees can start claiming.</td></tr>
</tbody>
</table>
</div>"""

    return """
<div class="prose noprint" id="about-famli">

<h2>What Maryland FAMLI costs an employer in 2027</h2>
<p>Maryland's Family and Medical Leave Insurance program takes <b>0.9 percent of covered
wages</b> from 1 January 2027, split evenly between employer and employee at 0.45 percent
each, on wages up to the Social Security wage base per employee per year. %(src_contrib)s
Employers with <b>fewer than 15 employees</b>, counted across every state under one federal
EIN, pay no employer share at all, but still withhold and remit the employee half.
%(src_06D)s</p>
<p>The program is administered by the <b>Maryland Department of Labor, FAMLI Division</b>.
Contributions run for a full year before anyone can claim anything: benefits begin in January
2028, so 2027 is a collection year. %(disambig)s</p>
<p>This calculator exists because the rules are spread across five COMAR chapters and two
articles of statute, and because one of the answers employers need most, <em>the date the
written notice is due</em>, is not published anywhere as a date. The regulation requires
notice &ldquo;at least 1 pay period prior to the commencement&rdquo; of withholding
%(src_05D)s, which means the deadline is derived from each employer's own payroll calendar. A
weekly payroll and a monthly payroll owe it on different days. The state tells you the rate;
this tells you your date.</p>

<h2>Every date, from now to the first claim</h2>
%(timeline)s
<p>Full detail on <a href="/deadlines-2027">the 2027 deadlines page</a>, including the weekend
rules: a <b>payment</b> date at a weekend moves to the next business day, and a <b>notice</b>
date moves earlier instead. %(src_08E)s</p>

<h2>Three worked examples</h2>
<p>Each of these was computed by the calculator on this page, not worked out by hand. Enter
your own figures above and you get the same treatment plus a printable report.</p>
%(wex1)s
%(wex2)s
%(wex3)s

<h2>The two mistakes that cost the most</h2>
<h3>Leaving the out-of-state headcount field blank</h3>
<p>To be classified as a small employer, your quarterly wage report has to state how many of
your employees work outside Maryland. %(src_08CD)s Leave it empty and you are deemed not
small, and the rate doubles from 0.45 percent to 0.9 percent. No penalty notice, no letter. A
blank box. More on <a href="/out-of-state-employees">the out-of-state headcount page</a>.</p>
<h3>Not getting round to the deduction</h3>
<p>An employer that fails to make the proper deduction from an employee's pay
&ldquo;is considered to have elected to pay the employee's portion for each pay period the
employer fails to make the deduction&rdquo;. %(src_07A)s It is not a fine and it cannot be
recovered from a later pay cycle. For the 40-person employer above that is %(e2_missed)s a
month, every month it runs.</p>

<h2>Where to go next</h2>
<ul>
<li><a href="/contribution-rate-2027">The 2027 contribution rate</a>, 0.9 percent, the
split, the wage cap and who sets the rate.</li>
<li><a href="/small-employer">Employers with fewer than 15 staff</a>, no employer
share, and how the 15 is counted.</li>
<li><a href="/out-of-state-employees">Out-of-state employees</a>, two headcounts doing
two different jobs.</li>
<li><a href="/employee-notice">The written notice to employees</a>, your date, derived
from your payroll frequency.</li>
<li><a href="/private-plan-declaration-of-intent">Private plans and the Declaration of
Intent</a>, five stages, one deadline, and no saving in 2027.</li>
<li><a href="/deadlines-2027">Every 2027 deadline</a>, the whole calendar with the
weekend rules.</li>
<li><a href="/registration">Employer registration</a>, required at one Maryland
employee, no exceptions.</li>
<li><a href="/payroll-providers">For payroll bureaus and bookkeepers</a>, the same
five facts, times fifty clients.</li>
</ul>

</div>

<div class="card sources noprint"><h2>Sources</h2><ol>
<li>Maryland Department of Labor, Make Contributions: <a href="%(u_contrib)s" target="_blank" rel="noopener">%(u_contrib)s</a></li>
<li>Maryland Department of Labor, Understand Employer Registration: <a href="%(u_reg)s" target="_blank" rel="noopener">%(u_reg)s</a></li>
<li>Maryland Department of Labor, Understand Your Plan: <a href="%(u_pp)s" target="_blank" rel="noopener">%(u_pp)s</a></li>
<li>COMAR Title 09, Subtitle 42: <a href="%(u_comar)s" target="_blank" rel="noopener">%(u_comar)s</a></li>
<li>Labor and Employment Article &sect;8.3-601, rate setting: <a href="%(u_rate)s" target="_blank" rel="noopener">%(u_rate)s</a></li>
<li>Labor and Employment Article &sect;8.3-801, notices: <a href="%(u_not)s" target="_blank" rel="noopener">%(u_not)s</a></li>
<li>Social Security Administration, taxable maximum: <a href="%(u_ssa)s" target="_blank" rel="noopener">%(u_ssa)s</a></li>
</ol>
<p class="verified">Rates and dates last verified against these sources on %(verified)s. Where
this page and the Maryland Department of Labor disagree, the Department is right and this page
is wrong; tell us at <a href="mailto:hello@02launch.com?subject=FAMLI%%20Clock%%3A%%20this%%20looks%%20wrong">hello@02launch.com</a>
and a dedicated engineer fixes it within 6 hours.</p></div>

%(footmap)s
""" % {
        "src_contrib": src("Maryland Department of Labor", S["contributions"]),
        "src_06D": src("COMAR 09.42.02.06D", S["comar"]),
        "src_05D": src("COMAR 09.42.02.05D", S["comar"]),
        "src_08E": src("COMAR 09.42.02.08E", S["comar"]),
        "src_08CD": src("COMAR 09.42.02.08C and D", S["comar"]),
        "src_07A": src("COMAR 09.42.02.07A", S["comar"]),
        "disambig": DISAMBIG,
        "timeline": tl,
        "e2_missed": money(E2["cost_per_missed_pay_period"]),
        "wex1": wex(
            "A small employer: 12 staff, all in Maryland, paid every two weeks",
            [("Employees working in Maryland", "12"),
             ("Total employees under one EIN", "12"),
             ("Annual Maryland payroll", money0(E1["input"]["md_payroll"] * 100)),
             ("Payroll frequency", "Every two weeks")],
            [("Band", "Small employer, under 15", False),
             ("Rate applied", "0.45%", False),
             ("Employer share, full year 2027", money(E1["annual_employer"]), False),
             ("Employee share, full year 2027", money(E1["annual_employee"]), False),
             ("Total for 2027", money(E1["annual_total"]), True),
             ("Written notice due, safe default", "1 December 2026", False),
             ("First payment, Q1 wages, due 30 April 2027", money(E1["q1_payment"]), False)],
            basis_nocap()),
        "wex2": wex(
            "A larger employer: 40 staff, all in Maryland, paid monthly",
            [("Employees working in Maryland", "40"),
             ("Total employees under one EIN", "40"),
             ("Annual Maryland payroll", money0(E2["input"]["md_payroll"] * 100)),
             ("Payroll frequency", "Monthly")],
            [("Band", "Standard, 15 or more", False),
             ("Rate applied", "0.90%", False),
             ("Employer share, full year 2027", money(E2["annual_employer"]), False),
             ("Employee share, full year 2027", money(E2["annual_employee"]), False),
             ("Total for 2027", money(E2["annual_total"]), True),
             ("Cost of absorbing the employee half instead",
              money(E2["absorb_delta"]) + " more a year", False),
             ("First payment, Q1 wages, due 30 April 2027", money(E2["q1_payment"]), False)],
            basis_nocap()),
        "wex3": wex(
            "A sole owner who is the only person the business employs",
            [("Employees working in Maryland", "1, the owner"),
             ("Total employees under one EIN", "1"),
             ("Annual Maryland payroll", money0(E3["input"]["md_payroll"] * 100)),
             ("Payroll frequency", "Monthly")],
            [("In scope for FAMLI", "No", True),
             ("Why", "A sole owner who is the only person their entity employs is not an "
                     "employer for FAMLI purposes " + src("COMAR 09.42.01.01B(21)(b)", S["comar"]), False),
             ("Contribution", "None", False),
             ("Registration", "Not required", False),
             ("Written notice", "Not required", False)],
            "Computed by famliclock.com on %s. One employee who is not the owner ends this "
            "exemption and puts the business fully in scope." % VERIFIED),
        "u_contrib": S["contributions"], "u_reg": S["registration"], "u_pp": S["privatePlans"],
        "u_comar": S["comar"], "u_rate": S["rate"], "u_not": S["notices"], "u_ssa": S["ssaCap"],
        "verified": VERIFIED,
        "footmap": footmap_html("/").replace('class="footmap"', 'class="footmap noprint"'),
    }


def replace_once(html, old, new, label):
    n = html.count(old)
    if n != 1:
        sys.exit("ANCHOR FAILED [%s]: found %d occurrences, expected exactly 1.\n"
                 "index.html has moved. Re-read the anchor and update patch_index.py.\n"
                 "  looking for: %r" % (label, n, old[:120]))
    return html.replace(old, new)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="src", default=os.path.join(HERE, "..", "index.html"))
    ap.add_argument("--out", dest="dst", default=os.path.join(HERE, "..", "site", "index.html"))
    args = ap.parse_args()

    with open(args.src) as f:
        html = f.read()
    before = len(html)
    ex = load_examples()

    # 1. title
    html = replace_once(
        html,
        "<title>Maryland FAMLI Clock: what you owe, and by when</title>",
        "<title>%s</title>" % esc(NEW_TITLE), "title")

    # 2. meta description
    html = replace_once(
        html,
        '<meta name="description" content="A free calculator for Maryland employers. Your '
        'FAMLI contribution, your written notice date, and your private plan deadline, worked '
        'out from five questions.">',
        '<meta name="description" content="%s">' % esc(NEW_DESC), "meta description")

    # 2b. keywords, lead with the query as it will be typed
    html = replace_once(
        html,
        '<meta name="keywords" content="Maryland FAMLI, Maryland paid family leave, FAMLI '
        'calculator, FAMLI contribution rate, Declaration of Intent, Maryland private plan, '
        'FAMLI employer registration, Maryland paid leave 2027, FAMLI employee notice, '
        'COMAR 09.42">',
        '<meta name="keywords" content="Maryland FAMLI calculator, Maryland FAMLI, Maryland '
        'paid family leave calculator, Maryland FAMLI contribution rate, Maryland FAMLI 2027, '
        'Declaration of Intent, Maryland private plan, FAMLI employer registration, Maryland '
        'FAMLI employee notice, Maryland FAMLI small employer, COMAR 09.42">', "keywords")

    # 2c. social titles and descriptions
    html = replace_once(
        html,
        '<meta property="og:title" content="Maryland FAMLI Clock: what you owe, and by when">',
        '<meta property="og:title" content="%s">' % esc(NEW_TITLE), "og:title")
    html = replace_once(
        html,
        '<meta name="twitter:title" content="Maryland FAMLI Clock: what you owe, and by when">',
        '<meta name="twitter:title" content="%s">' % esc(NEW_TITLE), "twitter:title")
    html = replace_once(
        html,
        '<meta property="og:description" content="Free calculator for Maryland employers. Your '
        'FAMLI contribution, your employee notice date, and the 15 November private plan '
        'deadline, from five questions. No sign up.">',
        '<meta property="og:description" content="%s">' % esc(NEW_OG_DESC), "og:description")

    # 3. JSON-LD, replaced wholesale with a superset
    m = re.search(r'<script type="application/ld\+json">\n(\{.*?\})\n</script>',
                  html, re.S)
    if not m:
        sys.exit("ANCHOR FAILED [json-ld]: the ld+json block did not match.")
    old_ld = json.loads(m.group(1))
    old_q = [q["name"] for q in old_ld["@graph"][1]["mainEntity"]]
    new_ld = build_ld()
    new_q = [q["name"] for n in new_ld["@graph"] if n["@type"] == "FAQPage"
             for q in n["mainEntity"]]
    for q in old_q:
        assert q in new_q, "the new JSON-LD dropped an existing FAQ question: %r" % q
    html = (html[:m.start()]
            + '<script type="application/ld+json">\n'
            + json.dumps(new_ld, separators=(",", ":"))
            + '\n</script>'
            + html[m.end():])

    # 4. stylesheet, BEFORE the inline <style> so the inline print rules still win
    html = replace_once(
        html,
        'family=Fraunces:opsz,wght@9..144,400;9..144,600&family=Public+Sans:wght@400;500;600;700'
        '&display=swap" rel="stylesheet">\n<style>',
        'family=Fraunces:opsz,wght@9..144,400;9..144,600&family=Public+Sans:wght@400;500;600;700'
        '&display=swap" rel="stylesheet">\n'
        '<!-- Loaded BEFORE the inline block on purpose: the inline stylesheet, including the\n'
        '     whole @media print section, must win every tie. This file only needs to supply\n'
        '     the selectors the content pages introduce. -->\n'
        '<link rel="stylesheet" href="/famli_pages.css">\n<style>', "css link")

    # 5. nav above the masthead
    html = replace_once(
        html, '<header class="mast">',
        nav_html("/").replace('class="topbar"', 'class="topbar noprint"')
        + '\n<header class="mast">', "nav insert")

    # 6. static h1
    html = replace_once(
        html,
        '<h1 id="h1">What Maryland FAMLI costs you, and the date you cannot miss.</h1>',
        '<h1 id="h1">%s</h1>' % esc(H1_STATIC), "static h1")

    # 7. the five phase headlines
    for key, old, new in H1_PHASES:
        html = replace_once(html, "'" + old + "'", "'" + new + "'", "phase h1 " + key)

    # 8. Colorado disambiguation, in an element the app never rewrites
    html = replace_once(
        html, '<form class="card" id="form" novalidate>',
        '<p class="disambig noprint">%s</p>\n\n<form class="card" id="form" novalidate>'
        % DISAMBIG, "disambiguation insert")

    # 9. the crawlable content block, after the CTA card, before the capture comment
    html = replace_once(
        html,
        '<!-- =====================================================================\n'
        '     EMAIL CAPTURE: NOT BUILT. BLOCKED, DELIBERATELY.',
        content_block(ex).strip() + '\n\n'
        '<!-- =====================================================================\n'
        '     EMAIL CAPTURE: NOT BUILT. BLOCKED, DELIBERATELY.', "content block insert")

    # ------------------------------------------------------------- assertions
    assert html.count('<h1') == 1, "there must still be exactly one <h1> element"
    assert html.count("Maryland FAMLI calculator") >= 6, \
        "expected the static h1 plus five phase headlines to carry the phrase"
    for key, old, _new in H1_PHASES:
        assert old not in html, "old phase headline survived: %s" % key
    assert "What Maryland FAMLI costs you, and the date you cannot miss." not in html
    assert html.count("famli_pages.css") == 1
    assert html.count('id="about-famli"') == 1
    assert html.count('class="topbar noprint"') == 1
    for path, _label in NAV:
        if path != "/":
            assert 'href="%s"' % path in html, "nav link missing: %s" % path
    assert "<script id=\"famli-engine\">" in html, "the engine block was damaged"
    assert "W3_KEY" in html, "the email capture key was damaged"
    assert "@media print{" in html, "the print stylesheet was damaged"
    assert len(html) > before, "the patch removed more than it added, which is wrong"

    os.makedirs(os.path.dirname(os.path.abspath(args.dst)), exist_ok=True)
    with open(args.dst, "w") as f:
        f.write(html)
    print("index.html patched: %d -> %d bytes (+%d)" % (before, len(html), len(html) - before))
    print("  written to %s" % os.path.abspath(args.dst))


if __name__ == "__main__":
    main()
