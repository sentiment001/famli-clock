#!/usr/bin/env python3
"""QA for the famliclock.com SEO build. Structural and factual checks that do not
need a browser; browser_qa.py does the layout work in real Chromium.

    python3 qa.py            checks ../site
    python3 qa.py --dir DIR

Exits non-zero on any failure. Run it after every build and before every push.
"""

import argparse
import json
import os
import re
import sys
from html.parser import HTMLParser

from build import NAV, SITE, VERIFIED, load_examples

FAILURES = []
CHECKS = [0]


def check(label, ok, detail=""):
    CHECKS[0] += 1
    if ok:
        print("PASS  %s" % label)
    else:
        print("FAIL  %s%s" % (label, ("   [" + detail + "]") if detail else ""))
        FAILURES.append(label)


class Collector(HTMLParser):
    """Minimal DOM facts, and a strict-ish well-formedness check for the tags that
    matter. Not a validator; it catches unclosed block elements, which is the
    failure mode a generator actually produces."""
    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
            "meta", "param", "source", "track", "wbr"}
    TRACK = {"div", "table", "thead", "tbody", "tr", "td", "th", "ul", "ol", "li",
             "p", "h1", "h2", "h3", "section", "nav", "header", "footer",
             "details", "blockquote", "span", "a", "caption", "main", "form"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.imbalance = []
        self.h1 = []
        self.h2 = []
        self.h3 = []
        self.links = []
        self.text = []
        self._cap = None

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "a" and d.get("href"):
            self.links.append(d["href"])
        if tag in ("h1", "h2", "h3"):
            self._cap = tag
        if tag in self.TRACK and tag not in self.VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in ("h1", "h2", "h3"):
            self._cap = None
        if tag in self.TRACK and tag not in self.VOID:
            if not self.stack:
                self.imbalance.append("closing </%s> with empty stack" % tag)
            elif self.stack[-1] != tag:
                self.imbalance.append("closing </%s> but innermost open is <%s>"
                                      % (tag, self.stack[-1]))
                if tag in self.stack:
                    while self.stack and self.stack.pop() != tag:
                        pass
            else:
                self.stack.pop()

    def handle_data(self, data):
        self.text.append(data)
        if self._cap == "h1":
            self.h1.append(data)
        elif self._cap == "h2":
            self.h2.append(data)
        elif self._cap == "h3":
            self.h3.append(data)


def words(text):
    return len(re.findall(r"[A-Za-z0-9$%,.']+", text))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                  "..", "site"))
    args = ap.parse_args()
    d = os.path.abspath(args.dir)
    ex = load_examples()
    meta = ex["_meta"]
    cap_literal = "$" + "{:,}".format(int(meta["wage_cap"]))

    expected = [("/", "index.html")] + [(p, p.lstrip("/") + ".html")
                                        for p, _l in NAV if p != "/"]

    # ------------------------------------------------------------- files exist
    for path, fname in expected:
        check("file exists: %s" % fname, os.path.exists(os.path.join(d, fname)))
    for extra in ("famli_pages.css", "sitemap.xml", "robots.txt", "llms.txt"):
        check("file exists: %s" % extra, os.path.exists(os.path.join(d, extra)))
    if FAILURES:
        print("\nmissing files, stopping early")
        sys.exit(1)

    pages = {}
    for path, fname in expected:
        with open(os.path.join(d, fname)) as f:
            pages[path] = f.read()

    # ------------------------------------------------- per page, structural
    for path, fname in expected:
        html = pages[path]
        tag = fname
        c = Collector()
        c.feed(html)
        body = "".join(c.text)

        check("%s: tags balance" % tag, not c.imbalance and not c.stack,
              "; ".join(c.imbalance[:3]) or ("unclosed: " + ",".join(c.stack[:5])))
        check("%s: exactly one <h1>" % tag, html.count("<h1") == 1,
              "found %d" % html.count("<h1"))
        h1text = " ".join(c.h1)
        check("%s: h1 names Maryland FAMLI" % tag, "Maryland FAMLI" in h1text, h1text[:70])

        m = re.search(r"<title>(.*?)</title>", html, re.S)
        check("%s: has a title" % tag, bool(m))
        title = m.group(1) if m else ""
        check("%s: title leads with Maryland FAMLI" % tag,
              title.startswith("Maryland FAMLI"), title[:80])
        check("%s: title is 40 to 95 chars" % tag, 40 <= len(title) <= 95,
              "%d chars" % len(title))

        m = re.search(r'<meta name="description" content="(.*?)">', html, re.S)
        check("%s: has a meta description" % tag, bool(m))
        if m:
            check("%s: description is 80 to 260 chars" % tag,
                  80 <= len(m.group(1)) <= 260, "%d chars" % len(m.group(1)))

        want_canon = SITE + ("/" if path == "/" else path)
        check("%s: canonical is self-referencing" % tag,
              ('<link rel="canonical" href="%s">' % want_canon) in html, want_canon)

        check("%s: robots meta allows indexing" % tag,
              re.search(r'<meta name="robots" content="index,follow', html) is not None)
        check("%s: Colorado disambiguation present" % tag,
              "Colorado runs a separate" in html)
        check("%s: names the administering agency" % tag,
              "Maryland Department of Labor" in body)
        check("%s: carries the last-verified line" % tag,
              VERIFIED in body, VERIFIED)
        check("%s: loads the shared stylesheet" % tag,
              'href="/famli_pages.css"' in html)
        check("%s: links to the calculator" % tag,
              'href="/"' in html)

        # JSON-LD
        blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>',
                            html, re.S)
        check("%s: exactly one JSON-LD block" % tag, len(blocks) == 1,
              "found %d" % len(blocks))
        if len(blocks) == 1:
            try:
                ld = json.loads(blocks[0])
                ok = True
            except Exception as e:                       # noqa: BLE001
                ld, ok = None, False
                check("%s: JSON-LD parses" % tag, False, str(e)[:80])
            if ok:
                check("%s: JSON-LD parses" % tag, True)
                types = [n.get("@type") for n in ld["@graph"]]
                check("%s: JSON-LD has a FAQPage" % tag, "FAQPage" in types, str(types))
                if path != "/":
                    check("%s: JSON-LD has a BreadcrumbList" % tag,
                          "BreadcrumbList" in types, str(types))
                # every FAQ answer must also be on the page in some form
                for n in ld["@graph"]:
                    if n.get("@type") != "FAQPage":
                        continue
                    for q in n["mainEntity"]:
                        name = q["name"]
                        on_page = name in body
                        if path == "/":
                            # the homepage FAQ lives only in JSON-LD; the prose covers
                            # the same ground but not verbatim, so only check the answer
                            # is not empty
                            check("%s: FAQ answer is non-trivial: %s" % (tag, name[:40]),
                                  len(q["acceptedAnswer"]["text"]) > 60)
                        else:
                            check("%s: FAQ question is also visible on the page: %s"
                                  % (tag, name[:44]), on_page)

        # word count
        prose = re.search(r'<div class="prose[^"]*"[^>]*>(.*?)</div>\s*(?:<div class="card faq|'
                          r'<div class="card sources)', html, re.S)
        n = words(body)
        check("%s: at least 500 words of readable text" % tag, n >= 500, "%d words" % n)

        # house style
        check("%s: no em dashes" % tag, "&mdash;" not in html and "—" not in html)
        check("%s: no unrendered template markers" % tag,
              "%(" not in body and "{{" not in body)

    # --------------------------------------------------------- the cap literal
    check("index.html carries no formatted cap literal",
          cap_literal not in pages["/"], cap_literal)
    check("index.html has no hard-coded '<year> Social Security' outside CONSENT_TEXT",
          len(re.findall(r"\b20\d\d Social Security", pages["/"])) == 1)
    check("index.html has no hard-coded 'SSA publishes/confirms the <year>'",
          not re.search(r"SSA (confirms|publishes) the 20\d\d", pages["/"]))
    for path, fname in expected:
        if path == "/":
            continue
        html = pages[path]
        if cap_literal in html:
            check("%s: every cap literal matches the engine CONFIG (%s)" % (fname, cap_literal),
                  len(re.findall(r"\$1[0-9]{2},[0-9]{3}", html)) ==
                  html.count(cap_literal),
                  "a cap-shaped figure on the page is not %s" % cap_literal)
            check("%s: the cap literal is paired with its year (%d)"
                  % (fname, meta["wage_cap_year"]),
                  ("%d Social Security taxable maximum of %s"
                   % (meta["wage_cap_year"], cap_literal)) in html)

    # ------------------------------------------------------- internal links
    have = {"/" + f for _p, f in expected}
    have |= {p for p, _f in expected}
    have |= {"/famli_pages.css", "/sitemap.xml", "/robots.txt", "/llms.txt"}
    for path, fname in expected:
        for href in Collector_links(pages[path]):
            if href.startswith(("http://", "https://", "mailto:", "tel:", "#")):
                continue
            check("%s: internal link resolves: %s" % (fname, href), href in have, href)

    # --------------------------------------------------------------- sitemap
    with open(os.path.join(d, "sitemap.xml")) as f:
        sm = f.read()
    locs = re.findall(r"<loc>(.*?)</loc>", sm)
    want = [SITE + ("/" if p == "/" else p) for p, _l in NAV]
    check("sitemap lists every page exactly once", sorted(locs) == sorted(want),
          "missing=%s extra=%s" % (sorted(set(want) - set(locs)), sorted(set(locs) - set(want))))
    check("sitemap is well formed XML", _xml_ok(sm))

    # --------------------------------------------------------------- robots
    with open(os.path.join(d, "robots.txt")) as f:
        rb = f.read()
    for bot in ("GPTBot", "ClaudeBot", "PerplexityBot", "Google-Extended", "CCBot",
                "OAI-SearchBot", "Applebot-Extended"):
        check("robots.txt allows %s" % bot,
              re.search(r"User-agent: %s\nAllow: /" % re.escape(bot), rb) is not None)
    check("robots.txt points at the sitemap", "Sitemap: %s/sitemap.xml" % SITE in rb)
    check("robots.txt disallows nothing", "Disallow: /" not in rb)

    # --------------------------------------------------------------- llms.txt
    with open(os.path.join(d, "llms.txt")) as f:
        lt = f.read()
    for p, _l in NAV:
        check("llms.txt lists %s" % p, (SITE + ("/" if p == "/" else p)) in lt)
    check("llms.txt states the Colorado distinction", "Colorado runs a separate" in lt)
    check("llms.txt has no unrendered markers", "%(" not in lt)

    print("\n%d checks, %d failed" % (CHECKS[0], len(FAILURES)))
    if FAILURES:
        for f_ in FAILURES:
            print("  FAILED: %s" % f_)
        sys.exit(1)


def Collector_links(html):
    c = Collector()
    c.feed(html)
    return c.links


def _xml_ok(text):
    try:
        import xml.etree.ElementTree as ET
        ET.fromstring(text)
        return True
    except Exception:                                    # noqa: BLE001
        return False


if __name__ == "__main__":
    main()
