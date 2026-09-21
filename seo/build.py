#!/usr/bin/env python3
"""Builds the eight new content pages for famliclock.com, plus the shared
stylesheet, sitemap, robots.txt and llms.txt.

    python3 build.py            writes everything into ../site
    python3 build.py --out DIR  writes into DIR

The homepage is NOT written here. It is patched from the live index.html by
patch_index.py, because index.html carries the calculator and must not be
rewritten from scratch.

Every money and date figure that appears in a worked example comes from
examples.json, which run_examples.js produces by running the shipped engine
inside index.html. Nothing on these pages is hand-calculated.
"""

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

SITE = "https://www.famliclock.com"
VERIFIED = "21 September 2026"
BUILD_DATE = "2026-09-21"
CALENDLY = "https://calendly.com/ahmed-asif1/30min"

# --------------------------------------------------------------- sources ---
# Same URLs the tool itself cites, taken from SOURCES in the engine block.
S = {
    "comar":        "https://regs.maryland.gov/us/md/exec/comar/09.42/index.full.html",
    "contributions": "https://paidleave.maryland.gov/employers/make-contributions/",
    "registration": "https://paidleave.maryland.gov/employers/understand-employer-registration/",
    "register":     "https://paidleave.maryland.gov/register/",
    "privatePlans": "https://paidleave.maryland.gov/employers/understand-your-plan/",
    "consultForm":  "https://paidleave.maryland.gov/files/proof-of-private-plan-consultation.pdf",
    "privateFaq":   "https://paidleave.maryland.gov/files/famli-faqs-private-plans-april-2026.pdf",
    "ssaCap":       "https://www.ssa.gov/faqs/en/questions/KA-02387.html",
    "notices":      "https://mgaleg.maryland.gov/mgawebsite/laws/StatuteText?article=gle&section=8.3-801",
    "rate":         "https://mgaleg.maryland.gov/mgawebsite/laws/StatuteText?article=gle&section=8.3-601",
    "penalties":    "https://mgaleg.maryland.gov/mgawebsite/laws/StatuteText?article=gle&section=8.3-903",
    "employers":    "https://paidleave.maryland.gov/employers/",
    "home":         "https://paidleave.maryland.gov/",
}

# ------------------------------------------------------------------ nav ----
# Order is the reading order a payroll person would want, not the build order.
NAV = [
    ("/",                                  "Calculator"),
    ("/contribution-rate-2027",            "Rate"),
    ("/small-employer",                    "Under 15 staff"),
    ("/out-of-state-employees",            "Out-of-state staff"),
    ("/employee-notice",                   "Employee notice"),
    ("/private-plan-declaration-of-intent", "Private plan"),
    ("/deadlines-2027",                    "Deadlines"),
    ("/registration",                      "Registration"),
    ("/payroll-providers",                 "Payroll providers"),
]

DISAMBIG = (
    "This page is about <b>Maryland</b> FAMLI, administered by the Maryland Department of "
    "Labor, FAMLI Division. Colorado runs a separate paid leave program with the same name "
    "and different rules; nothing here applies to it."
)


# ------------------------------------------------------------- helpers -----
def money(cents):
    """$1,234.56 from an integer number of cents. Never floats for display."""
    neg = cents < 0
    v = abs(int(cents))
    s = "{:,.2f}".format(v / 100.0)
    return ("-$" if neg else "$") + s


def money0(cents):
    """$1,235 from an integer number of cents, whole dollars only."""
    return "$" + "{:,}".format(int(round(int(cents) / 100.0)))


def src(label, url):
    return ('<span class="src"><a href="%s" target="_blank" rel="noopener">%s</a></span>'
            % (url, label))


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def load_examples():
    path = os.path.join(HERE, "examples.json")
    if not os.path.exists(path):
        sys.exit("examples.json is missing. Run:  node run_examples.js > examples.json")
    with open(path) as f:
        return json.load(f)


# ------------------------------------------------------------ scaffolding --
CLARITY = """<script>
(function(){
  if (location.protocol === 'file:') { return; }
  (function(c,l,a,r,i,t,y){
    c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
    t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
    y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
  })(window, document, "clarity", "script", "yatz1z728u");
})();
</script>"""


def nav_html(current):
    out = ['<nav class="topbar" aria-label="FAMLI Clock pages">',
           '<a class="home" href="/">FAMLI Clock &middot; Maryland</a>']
    for href, label in NAV:
        cur = ' aria-current="page"' if href == current else ""
        out.append('<a class="nl" href="%s"%s>%s</a>' % (href, cur, label))
    out.append("</nav>")
    return "\n".join(out)


def footmap_html(current):
    items = "".join(
        '<li><a href="%s">%s</a></li>' % (h, l) for h, l in NAV if h != current)
    return ('<div class="footmap"><div class="fmcap">More on Maryland FAMLI</div>'
            '<ul>%s</ul></div>' % items)


def toolcard_html(text):
    return ('<div class="toolcard"><p>%s</p>'
            '<p><a class="run" href="/">Run the Maryland FAMLI calculator '
            '<span class="arr" aria-hidden="true">&rarr;</span></a></p></div>' % text)


def cta_html(bullets, intro):
    lis = "".join("<li>%s</li>" % b for b in bullets)
    return (
        '<div class="card cta">'
        '<h2>Who made this</h2>'
        '<p>Our team at <b style="color:#fff">02Launch.com</b> finds creative ways to use AI to '
        'drastically reduce your workload. We built this calculator because the FAMLI rules are '
        'spread across five COMAR chapters and nobody had put them in one place.</p>'
        '<p style="margin-bottom:.5rem">%s</p>'
        '<ul>%s</ul>'
        '<p style="margin-bottom:0"><span class="bookwrap">'
        '<a class="book" href="%s" target="_blank" rel="noopener">Book a call with our team '
        '<span class="arr" aria-hidden="true">&rarr;</span></a></span></p>'
        '</div>' % (intro, lis, CALENDLY))


def sources_html(items):
    lis = "".join(
        '<li>%s: <a href="%s" target="_blank" rel="noopener">%s</a></li>'
        % (label, url, url) for label, url in items)
    return ('<div class="card sources"><h2>Sources</h2><ol>%s</ol>'
            '<p class="verified">Rates and dates last verified against these sources on %s. '
            'Where this page and the Maryland Department of Labor disagree, the Department is '
            'right and this page is wrong; tell us at '
            '<a href="mailto:hello@02launch.com?subject=FAMLI%%20Clock%%3A%%20this%%20looks%%20wrong">'
            'hello@02launch.com</a> and a dedicated engineer fixes it within 6 hours.</p></div>'
            % (lis, VERIFIED))


def related_html(items):
    lis = "".join('<li><a href="%s">%s</a>, %s</li>' % (h, t, d)
                  for h, t, d in items)
    return '<div class="card related"><h2>Next</h2><ul>%s</ul></div>' % lis


FOOTER = (
    '<footer class="foot">'
    '<p><b>This is an estimate, not tax, legal or payroll advice.</b> It is built from the '
    'Maryland regulations and the Division\'s own published pages, cited above. Check anything '
    'you are going to rely on with FAMLI Customer Care on '
    '<a href="tel:+14105254010">(410) 525-4010</a> or your own advisers before you act on it.</p>'
    '<p>Questions, or something here looks wrong? Write to '
    '<!--email_off--><a href="mailto:hello@02launch.com?subject=FAMLI%20Clock%3A%20this%20looks%20wrong">'
    'hello@02launch.com</a><!--/email_off--> and tell us what you were looking at. We have a '
    'dedicated engineer who fixes it within 6 hours of you telling us.</p>'
    '<p style="margin-bottom:0"><b>02Launch</b> &middot; Forward deployed AI engineering.</p>'
    '</footer>'
)


def breadcrumb(path, name):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Maryland FAMLI Clock",
             "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": name,
             "item": SITE + path},
        ],
    }


def faq_ld(triples):
    """triples are (question, plain-text answer, html answer). The plain text
    goes in the JSON-LD, the HTML goes on the page. They must say the same
    thing; assert_faq_parity in qa.py checks that they do."""
    return {
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a, _h in triples
        ],
    }


def page(path, title, description, h1, lede, body, faq_pairs, sources,
         related, cta_intro, cta_bullets, tool_text, og_desc=None,
         breadcrumb_name=None, extra_ld=None):
    """Assembles one complete, self-contained content page."""
    url = SITE + path
    graph = [
        {
            "@type": "WebPage",
            "@id": url,
            "url": url,
            "name": title,
            "description": description,
            "inLanguage": "en-US",
            "isPartOf": {"@type": "WebSite", "name": "Maryland FAMLI Clock",
                         "url": SITE + "/"},
            "about": {"@type": "GovernmentService", "name": "Maryland Family and Medical "
                      "Leave Insurance (FAMLI)", "provider": {
                          "@type": "GovernmentOrganization",
                          "name": "Maryland Department of Labor, FAMLI Division",
                          "url": S["home"]},
                      "areaServed": {"@type": "State", "name": "Maryland"}},
            "publisher": {"@type": "Organization", "name": "02Launch",
                          "url": "https://02launch.com"},
            "dateModified": BUILD_DATE,
        },
        breadcrumb(path, breadcrumb_name or h1),
    ]
    if faq_pairs:
        graph.append(faq_ld(faq_pairs))
    if extra_ld:
        graph.extend(extra_ld)
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph},
                    separators=(",", ":"))

    faq_html = ""
    if faq_pairs:
        blocks = "".join("<h3>%s</h3><p>%s</p>" % (esc(q), a_html)
                         for q, _a, a_html in faq_pairs)
        faq_html = '<div class="card faq"><h2>Questions</h2>%s</div>' % blocks

    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s</title>
<meta name="description" content="%(description)s">
<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large">
<link rel="canonical" href="%(url)s">
<meta name="author" content="02Launch">
%(clarity)s
<meta property="og:type" content="article">
<meta property="og:site_name" content="FAMLI Clock">
<meta property="og:url" content="%(url)s">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(ogdesc)s">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="%(title)s">
<meta name="twitter:description" content="%(ogdesc)s">
<meta name="theme-color" content="#0E5A5E">
<script type="application/ld+json">%(ld)s</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600&family=Public+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/famli_pages.css">
</head>
<body>
<div class="wrap">
<header class="mast">
%(nav)s
</header>

<h1>%(h1)s</h1>
<p class="lede">%(lede)s</p>
<p class="disambig">%(disambig)s</p>

%(tool)s

<div class="prose">
%(body)s
</div>

%(faq)s

%(sources)s

%(related)s

%(cta)s

%(footer)s

%(footmap)s
</div>
</body>
</html>
""" % {
        "title": esc(title),
        "description": esc(description),
        "ogdesc": esc(og_desc or description),
        "url": url,
        "clarity": CLARITY,
        "ld": ld,
        "nav": nav_html(path),
        "h1": h1,
        "lede": lede,
        "disambig": DISAMBIG,
        "tool": toolcard_html(tool_text),
        "body": body,
        "faq": faq_html,
        "sources": sources_html(sources),
        "related": related_html(related),
        "cta": cta_html(cta_bullets, cta_intro),
        "footer": FOOTER,
        "footmap": footmap_html(path),
    }


# ------------------------------------------------------------- sitemap -----
def sitemap():
    # Priority reflects the campaign, not vanity: the calculator first, then the
    # two pages with a dated deadline in front of them.
    prio = {
        "/": "1.0",
        "/private-plan-declaration-of-intent": "0.9",
        "/employee-notice": "0.9",
        "/contribution-rate-2027": "0.8",
        "/deadlines-2027": "0.8",
        "/small-employer": "0.7",
        "/out-of-state-employees": "0.7",
        "/registration": "0.7",
        "/payroll-providers": "0.7",
    }
    rows = []
    for href, _label in NAV:
        rows.append(
            "  <url>\n"
            "    <loc>%s%s</loc>\n"
            "    <lastmod>%s</lastmod>\n"
            "    <changefreq>monthly</changefreq>\n"
            "    <priority>%s</priority>\n"
            "  </url>" % (SITE, "" if href == "/" else href, BUILD_DATE, prio[href]))
    # The homepage loc has to end in a slash to match its canonical.
    rows[0] = rows[0].replace("<loc>%s</loc>" % SITE, "<loc>%s/</loc>" % SITE)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(rows) + "\n</urlset>\n")


def robots():
    return """# famliclock.com
# A free Maryland FAMLI calculator. Everything here is public and meant to be read,
# by people and by machines. Nothing is disallowed.

User-agent: *
Allow: /

# Named explicitly so that a future default-deny at the CDN does not silently
# switch them off. If this file is not what serves at /robots.txt, Cloudflare is
# overriding it; see PUSH_ORDER.md section 6.
User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Claude-Web
Allow: /

User-agent: Claude-SearchBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Perplexity-User
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Applebot
Allow: /

User-agent: Applebot-Extended
Allow: /

User-agent: CCBot
Allow: /

User-agent: Bingbot
Allow: /

User-agent: Amazonbot
Allow: /

User-agent: meta-externalagent
Allow: /

Sitemap: %s/sitemap.xml
""" % SITE


# ------------------------------------------------------------- llms.txt ---
def llms_txt():
    return """# famliclock.com

> A free calculator for Maryland employers. It works out the Maryland FAMLI (Family
> and Medical Leave Insurance) contribution for 2027, the date the written notice to
> employees is due, and whether the remaining time still fits a private plan
> Declaration of Intent. Five inputs, no sign up, and a printable report.

Maryland FAMLI is administered by the Maryland Department of Labor, FAMLI Division.
Colorado runs a separate paid leave program with the same name; nothing on this site
applies to Colorado.

Built and maintained by 02Launch (https://02launch.com), an AI engineering firm.
Rates and dates last verified against primary sources on %(verified)s.

## What the calculator computes that published guidance does not

- The written notice date. The rule is "at least 1 pay period prior to the
  commencement" of withholding (COMAR 09.42.02.05D), so the deadline is derived from
  each employer's payroll frequency and first 2027 pay date. It is not a fixed
  calendar date and no agency publishes a per-employer answer.
- Whether the remaining stages of a private plan Declaration of Intent still fit
  before the window closes, at three different paces.
- The cost of leaving the out-of-state headcount field blank on the quarterly wage
  report, which reclassifies a small employer from 0.45%% to 0.9%%.

## Key facts, each traceable to a cited paragraph

- Contributions are due on wages paid from 1 January 2027 at a total rate of 0.9
  percent of wages up to the Social Security wage base, split evenly between employer
  and employee at 0.45 percent each.
- Employers with fewer than 15 employees, counted across all states under one federal
  EIN, remit only 50 percent of the total rate. The employee share is still withheld.
  (COMAR 09.42.02.06A and .06D)
- Written notice to employees is due at least one full pay period before withholding
  commences, so the date depends on the employer's payroll schedule.
  (COMAR 09.42.02.05D)
- An employer that fails to make the deduction is considered to have elected to pay
  the employee's portion for each pay period missed, and cannot recover it.
  (COMAR 09.42.02.07A)
- Employers intending to use a private plan submit a Declaration of Intent to the
  FAMLI Division between 1 September and 15 November 2026. FAMLI decides within 15
  business days. (COMAR 09.42.03.10A(2))
- An approved private plan does not reduce the 2027 cash cost. The same contributions
  are collected and held in escrow rather than remitted. (COMAR 09.42.03.10A(1)(d))
- The first quarterly wage report and contribution payment, covering January to March
  2027, is due 30 April 2027.
- Benefits become available in January 2028. 2027 is a collection year with no claims.
- The Secretary of Labor sets each later year's rate by 1 November of the preceding
  year, and the statute caps it at 1.2 percent. (LE 8.3-601)

## Pages

%(pages)s

## Primary sources cited across the site

- Maryland Department of Labor, FAMLI: https://paidleave.maryland.gov/
- Make contributions: %(contributions)s
- Employer registration: %(registration)s
- Private plans and the Declaration of Intent: %(privatePlans)s
- COMAR Title 09, Subtitle 42: %(comar)s
- Labor and Employment Article 8.3-601, rate: %(rate)s
- Labor and Employment Article 8.3-801, notices: %(notices)s
- Labor and Employment Article 8.3-903, penalties: %(penalties)s
- Social Security taxable maximum: %(ssaCap)s

## Limits, stated plainly

- It estimates. Figures come from the numbers typed in and the published rates, not
  from payroll records.
- It is not a filing. Nothing reaches Maryland. Employers still register, report and
  pay through the FAMLI portal themselves.
- It cannot get a private plan approved. It says what the Declaration of Intent
  involves and whether the time still fits. FAMLI decides.
- The 2027 Social Security wage cap has not been published yet. Until SSA publishes it
  in October 2026 the calculator uses the 2026 figure of $184,500 as a stand-in and
  labels it as one.
""" % {
        "verified": VERIFIED,
        "pages": "\n".join(
            "- [%s](%s%s)" % (label, SITE, "/" if href == "/" else href)
            for href, label in NAV),
        "contributions": S["contributions"],
        "registration": S["registration"],
        "privatePlans": S["privatePlans"],
        "comar": S["comar"],
        "rate": S["rate"],
        "notices": S["notices"],
        "penalties": S["penalties"],
        "ssaCap": S["ssaCap"],
    }


# ------------------------------------------------------------------ main ---
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(HERE, "..", "site"))
    args = ap.parse_args()
    out = os.path.abspath(args.out)
    os.makedirs(out, exist_ok=True)

    ex = load_examples()

    import content_a, content_b, content_c, content_d
    specs = []
    for mod in (content_a, content_b, content_c, content_d):
        specs.extend(mod.build(ex))

    paths = [p for p, _l in NAV if p != "/"]
    got = [s["path"] for s in specs]
    missing = [p for p in paths if p not in got]
    extra = [p for p in got if p not in paths]
    assert not missing, "content modules did not produce: %s" % missing
    assert not extra, "content modules produced pages not in NAV: %s" % extra
    assert len(set(got)) == len(got), "duplicate page path"

    written = []
    for s in specs:
        html = page(
            path=s["path"], title=s["title"], description=s["description"],
            h1=s["h1"], lede=s["lede"], body=s["body"], faq_pairs=s["faq"],
            sources=s["sources"], related=s["related"],
            cta_intro=s["cta_intro"], cta_bullets=s["cta_bullets"],
            tool_text=s["tool_text"], og_desc=s.get("og_desc"),
            breadcrumb_name=s.get("breadcrumb_name"))
        name = s["path"].lstrip("/") + ".html"
        with open(os.path.join(out, name), "w") as f:
            f.write(html)
        written.append((name, len(html)))

    # Stylesheet is maintained by hand; copy it alongside.
    css_src = os.path.join(HERE, "famli_pages.css")
    with open(css_src) as f:
        css = f.read()
    with open(os.path.join(out, "famli_pages.css"), "w") as f:
        f.write(css)
    written.append(("famli_pages.css", len(css)))

    for name, text in (("sitemap.xml", sitemap()),
                       ("robots.txt", robots()),
                       ("llms.txt", llms_txt())):
        with open(os.path.join(out, name), "w") as f:
            f.write(text)
        written.append((name, len(text)))

    for name, n in written:
        print("  %-42s %7d bytes" % (name, n))
    print("\n%d files written to %s" % (len(written), out))


if __name__ == "__main__":
    main()
