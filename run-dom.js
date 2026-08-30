/* Renders the real page in jsdom at several dates and asserts that the required
   outputs are actually on screen. Catches the class of bug the fixtures cannot:
   a correct engine wired to a broken page. */
'use strict';
var fs = require('fs');
var path = require('path');
var { JSDOM } = require('jsdom');

var HTML = fs.readFileSync(path.join(__dirname, 'index.html'), 'utf8');
var pass = 0, fail = 0, out = [];

function check(label, cond, extra) {
  if (cond) { pass++; out.push('PASS  ' + label); }
  else { fail++; out.push('FAIL  ' + label + (extra ? '   ' + extra : '')); }
}

/* The engine is inline in index.html, so jsdom runs the real page as shipped. */
var HTML_INLINED = HTML;

function load(query) {
  var errors = [];
  var dom = new JSDOM(HTML_INLINED, {
    url: 'https://famliclock.com/' + (query || ''),
    runScripts: 'dangerously',
    pretendToBeVisual: true,
    virtualConsole: new (require('jsdom').VirtualConsole)()
      .on('jsdomError', function (e) { errors.push(e.message); })
      .on('error', function (m) { errors.push(m); })
  });
  var w = dom.window;
  w.scrollTo = function () {};
  w.HTMLElement.prototype.scrollIntoView = function () {};
  w.__errors = errors;
  return w;
}

function fill(w, vals) {
  var d = w.document;
  d.getElementById('md').value = vals.md;
  d.getElementById('ein').value = vals.ein;
  d.getElementById('pay').value = vals.pay;
  d.getElementById('freq').value = vals.freq || 'biweekly';
  d.getElementById('priv').checked = !!vals.priv;
  d.getElementById('form').dispatchEvent(new w.Event('submit', { bubbles: true, cancelable: true }));
  return d.getElementById('out').textContent;
}

/* ---- 1. each phase renders its own lead ---- */
out.push('--- phase-specific lead output ---');
[
  ['2026-08-29', 'P1', 'Declaration of Intent', true],
  ['2026-10-20', 'P2', 'Where are you already', true],
  ['2026-12-01', 'P3', 'writing', false],
  ['2027-02-15', 'P4', 'quarterly report', false],
  ['2027-06-01', 'P5', 'quarterly', false]
].forEach(function (t) {
  var w = load('?d=' + t[0]);
  var txt = fill(w, { md: 25, ein: 25, pay: 1750000, priv: t[3] });
  check(t[1] + ' (' + t[0] + ') lead mentions "' + t[2] + '"', txt.indexOf(t[2]) !== -1);
  check(t[1] + ' phase rail shows the right phase',
    w.document.getElementById('phaseline').textContent.indexOf(
      ['DOI runway', 'DOI compressed', 'Notice and withholding', 'Contributions live', 'Steady state'][+t[1][1] - 1]) !== -1);
});

/* ---- 2. the money that must always be on screen ---- */
out.push('--- required result blocks ---');
var w1 = load('?d=2026-08-29');
var t1 = fill(w1, { md: 40, ein: 40, pay: 8400000 });
[
  ['annual total', '$66,420.00'], ['employer withhold', '$33,210.00'],
  ['Q1 payment', '$18,900.00'], ['per period', '$2,907.69'],
  ['payment due date', '30 Apr 2027'], ['safe notice date', '1 Dec 2026'],
  ['withhold vs absorb', 'If you absorb'], ['cost of never withholding', 'deemed to have chosen to pay'],
  ['registration open now', 'Registration is open now'],
  ['not flat warning', 'does not hold all year'],
  ['wage cap disclosure D1', '$184,500'],
  ['date list', 'Your dates']
].forEach(function (p) { check(p[0] + ' present', t1.indexOf(p[1]) !== -1); });

/* ---- 3. flags ---- */
out.push('--- flags ---');
var w2 = load('?d=2026-08-29');
var t2 = fill(w2, { md: 3, ein: 403, pay: 300000 });
check('small in MD but not under EIN flag', t2.indexOf('small in Maryland but not small under your EIN') !== -1);
var w3 = load('?d=2026-08-29');
var t3 = fill(w3, { md: 10, ein: 12, pay: 700000, freq: 'monthly' });
check('out of state reporting trap flag', t3.indexOf('bill doubles') !== -1);
check('trap quotes the right number ($3,150.00)', t3.indexOf('$3,150.00') !== -1);

/* ---- 4. out of scope ---- */
out.push('--- out of scope branches ---');
var w4 = load('?d=2026-08-29');
var t4 = fill(w4, { md: 0, ein: 60, pay: 0 });
check('zero Maryland employees is out of scope', t4.indexOf('No Maryland employees') !== -1);
check('no cost shown when out of scope', t4.indexOf('What it costs') === -1);
var w5 = load('?d=2026-08-29');
w5.document.getElementById('ein').value = '1';
w5.document.getElementById('ein').dispatchEvent(new w5.Event('input', { bubbles: true }));
check('sole owner question appears only when EIN is 1',
  !w5.document.getElementById('soleWrap').classList.contains('hidden'));
w5.document.getElementById('sole').checked = true;
var t5 = fill(w5, { md: 1, ein: 1, pay: 120000, freq: 'monthly' });
check('sole owner is out of scope with the COMAR cite', t5.indexOf('09.42.01.01B(21)(b)') !== -1);

/* ---- 5. refinements ---- */
out.push('--- refinements ---');
var w6 = load('?d=2026-08-29');
fill(w6, { md: 10, ein: 10, pay: 2500000, freq: 'monthly' });
var d6 = w6.document;
check('R1 copy explains what the field is', d6.getElementById('out').textContent.indexOf('assumes your Maryland salaries are broadly similar') !== -1);
check('R2 copy explains what the field is', d6.getElementById('out').textContent.indexOf('one full pay period before you start withholding') !== -1);
d6.getElementById('hc').value = '1';
d6.getElementById('hw').value = '1600000';
d6.getElementById('applyRef').click();
var t6 = d6.getElementById('out').textContent;
check('R1 recomputes to the refined base $1,084,500', t6.indexOf('$1,084,500.00') !== -1);
check('R1 says by how much it moved', t6.indexOf('lower') !== -1 && t6.indexOf('Updated.') !== -1);

var w7 = load('?d=2026-08-29');
fill(w7, { md: 10, ein: 10, pay: 900000, freq: 'monthly' });
var d7 = w7.document;
d7.getElementById('hc').value = '3';
d7.getElementById('hw').value = '200000';
d7.getElementById('applyRef').click();
var t7 = d7.getElementById('out').textContent;
check('contradictory R1 falls back and says so', t7.indexOf('do not fit together') !== -1);
check('contradictory R1 still shows the default answer $4,050.00', t7.indexOf('$4,050.00') !== -1);

var w8 = load('?d=2026-08-29');
fill(w8, { md: 30, ein: 30, pay: 2100000 });
var d8 = w8.document;
d8.getElementById('fp').value = '2027-01-08';
d8.getElementById('applyRef').click();
var t8 = d8.getElementById('out').textContent;
check('R2 replaces the default with Thu 24 Dec 2026', t8.indexOf('24 Dec 2026') !== -1);
check('R2 says which date it is showing', t8.indexOf('Your date.') !== -1);

/* ---- 6. DOI progress branch ---- */
out.push('--- DOI progress branch (P2) ---');
var w9 = load('?d=2026-10-20');
fill(w9, { md: 25, ein: 25, pay: 1750000, priv: true });
var d9 = w9.document;
check('cold start in P2 reads only_if_everything_goes_right',
  d9.getElementById('out').textContent.indexOf('Only if everything goes right') !== -1);
var sel = d9.getElementById('dp');
sel.value = 'agent_booked';
sel.dispatchEvent(new w9.Event('change', { bubbles: true }));
var t9 = d9.getElementById('out').textContent;
check('agent booked moves the verdict to Tight', t9.indexOf('Tight') !== -1);
check('DOI range is shown, not a point estimate', t9.indexOf('business days, typically') !== -1);
check('escrow reality stated', t9.indexOf('does not save you money in 2027') !== -1);

/* ---- 7. shareable URL round trip ---- */
out.push('--- shareable URL ---');
var w10 = load('?d=2026-08-29');
fill(w10, { md: 25, ein: 25, pay: 1750000, priv: true });
var url = w10.location.search;
check('URL carries the inputs', /md=25/.test(url) && /ein=25/.test(url) && /pay=1750000/.test(url) && /pp=1/.test(url), url);
var w11 = load(url);
check('reloading the URL reproduces the result',
  w11.document.getElementById('out').textContent.indexOf('$15,750.00') !== -1);

/* ---- 8. no browser storage was touched ---- */
out.push('--- storage ---');
var w12 = load('?d=2026-08-29');
var touched = false;
['localStorage', 'sessionStorage'].forEach(function (k) {
  try { if (w12[k] && w12[k].length > 0) touched = true; } catch (e) {}
});
fill(w12, { md: 8, ein: 8, pay: 480000 });
['localStorage', 'sessionStorage'].forEach(function (k) {
  try { if (w12[k] && w12[k].length > 0) touched = true; } catch (e) {}
});
check('nothing written to localStorage or sessionStorage', !touched);
check('no cookies set', w12.document.cookie === '');

/* ---- 9. disclosures are inline and attached, not a site footer ---- */
out.push('--- disclosure component ---');
var w13 = load('?d=2026-08-29');
fill(w13, { md: 48, ein: 48, pay: 3840000, freq: 'monthly', priv: true });
var discs = w13.document.querySelectorAll('#out details.disc');
check('disclosures render inside result blocks', discs.length >= 3, 'found ' + discs.length);
check('no disclosure sits in the page footer',
  w13.document.querySelectorAll('footer details.disc').length === 0);
check('D3 DOI reasoning is visible not hidden',
  w13.document.getElementById('out').textContent.indexOf('open enrolment season') !== -1);
check('cannot self insure at 48 MD employees',
  w13.document.getElementById('out').textContent.indexOf('cannot self insure') !== -1);

/* ---- 10. every result number has a source link ---- */
out.push('--- sources ---');
var links = w13.document.querySelectorAll('#out .src a');
check('source links present on results', links.length >= 6, 'found ' + links.length);
var bad = [];
links.forEach(function (a) { if (!/^https:\/\//.test(a.href)) bad.push(a.href); });
check('all source links are absolute https', bad.length === 0, bad.join(','));

/* ---- 11. validation ---- */
out.push('--- validation ---');
var w14 = load('?d=2026-08-29');
fill(w14, { md: 10, ein: 4, pay: 500000 });
check('EIN below MD headcount is blocked with a message',
  !w14.document.getElementById('err').classList.contains('hidden'));
var w15 = load('?d=2026-08-29');
var t15 = fill(w15, { md: 5, ein: 5, pay: 0 });
check('zero payroll says so rather than showing $0.00 as an answer',
  t15.indexOf('cannot cost this yet') !== -1);

/* ---- 12. email capture: consented, optional, never gating ---- */
out.push('--- email capture ---');
var w16 = load('?d=2026-08-29');
check('no email input before a result is produced',
  w16.document.querySelectorAll('input[type=email]').length === 0);
fill(w16, { md: 8, ein: 8, pay: 480000 });
var capEmail = w16.document.getElementById('capEmail');
var capOk = w16.document.getElementById('capOk');
check('email input appears with the result', !!capEmail);
check('consent box is present', !!capOk);
check('consent box is unchecked by default', capOk && capOk.checked === false);
check('email field is not required', capEmail && !capEmail.required);
check('honeypot field is present', !!w16.document.getElementById('capHp'));
check('results render in full with no email given',
  w16.document.body.textContent.indexOf('Full year 2027') !== -1);
check('capture sits after the results, not before them',
  (w16.document.querySelector('.lead').compareDocumentPosition(
     w16.document.querySelector('.cap')) & 4) !== 0);
check('no form element posts anywhere',
  w16.document.querySelectorAll('form[action]').length === 0);
check('the page still states it does not store what you typed',
  w16.document.body.textContent.indexOf('Nothing you typed above is sent') !== -1);

/* ---- 13. the page must be self-contained: this is the bug Mash hit ---- */
out.push('--- self-contained page (regression guard) ---');
var w17 = load('?d=2026-08-29');
var localScripts = [].filter.call(w17.document.querySelectorAll('script[src]'), function (s) {
  return !/^https?:\/\//.test(s.getAttribute('src'));
});
check('no script depends on a sibling file', localScripts.length === 0,
  localScripts.map(function (s) { return s.getAttribute('src'); }).join(','));
check('engine is defined after load', typeof w17.FAMLI === 'object' && !!w17.FAMLI.CONFIG);
check('no uncaught errors on load', w17.__errors.length === 0, w17.__errors.join(' | '));
check('the load-failure guard did not fire',
  w17.document.getElementById('form').textContent.indexOf('did not load properly') === -1);
var t17 = fill(w17, { md: 8, ein: 8, pay: 480000 });
check('no uncaught errors after a run', w17.__errors.length === 0, w17.__errors.join(' | '));

/* ---- 14. build pack: "what this tool does not do", above the CTA ---- */
out.push('--- what this tool does not do ---');
var lim = w17.document.querySelector('.limits');
check('section exists', !!lim);
check('it sits above the CTA block',
  lim && (lim.compareDocumentPosition(w17.document.querySelector('.cta')) & 4) !== 0);
['It estimates', 'not a filing', 'private plan approved', 'looks wrong'].forEach(function (p) {
  check('covers "' + p + '"', lim && lim.textContent.indexOf(p) !== -1);
});

console.log(out.join('\n'));
console.log('\n' + pass + ' passed, ' + fail + ' failed');
process.exit(fail ? 1 : 0);
