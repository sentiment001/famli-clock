/* The spec called the phase machine the weakest thing in the build, because a page that
   renders differently on Tuesday than Monday fails silently. This walks every boundary,
   one day either side, plus the notice-versus-payment direction trap. */
'use strict';
var F = require('./load-engine.js')();

var pass = 0, fail = 0, out = [];
function check(label, got, want) {
  var ok = String(got) === String(want);
  if (ok) { pass++; } else { fail++; }
  out.push((ok ? 'PASS  ' : 'FAIL  ') + label + (ok ? '' : '   want=' + want + '  got=' + got));
}

/* ---- 1. phase boundaries, one day either side ---- */
out.push('--- phase boundaries ---');
[
  ['2026-08-29', 'P1_runway'], ['2026-09-27', 'P1_runway'], ['2026-09-28', 'P1_runway'],
  ['2026-09-29', 'P2_compressed'], ['2026-09-30', 'P2_compressed'],
  ['2026-11-12', 'P2_compressed'], ['2026-11-13', 'P2_compressed'],
  ['2026-11-14', 'P3_notice'], ['2026-11-15', 'P3_notice'],
  ['2026-12-30', 'P3_notice'], ['2026-12-31', 'P3_notice'],
  ['2027-01-01', 'P4_live'], ['2027-01-02', 'P4_live'],
  ['2027-04-29', 'P4_live'], ['2027-04-30', 'P4_live'],
  ['2027-05-01', 'P5_steady'], ['2027-05-02', 'P5_steady'],
  ['2030-01-01', 'P5_steady']
].forEach(function (t) { check('phase on ' + t[0], F.phaseFor(t[0]).key, t[1]); });

/* ---- 2. notices move earlier, payments move later ---- */
out.push('--- notice direction (COMAR 09.42.02.08E gives relief to payments only) ---');
function noticeFor(freq, firstPay) {
  return F.compute({
    md_employees: 10, ein_employees: 10, md_payroll: 800000, pay_frequency: freq,
    considering_private_plan: false, today: '2026-08-29', first_2027_pay_date: firstPay
  }).notice.notice_by;
}
check('weekly, first pay 2027-01-01',      noticeFor('weekly', '2027-01-01'),      '2026-12-24');
check('biweekly, first pay 2027-01-08',    noticeFor('biweekly', '2027-01-08'),    '2026-12-24');
check('semimonthly, first pay 2027-01-15', noticeFor('semimonthly', '2027-01-15'), '2026-12-31');
check('monthly, first pay 2027-01-29',     noticeFor('monthly', '2027-01-29'),     '2026-12-30');

out.push('--- payment dates move later, notice dates move earlier ---');
check('30 Apr 2027 payment (Fri) unchanged', F.fromDay(F.nextBusinessDay(F.toDay('2027-04-30'))), '2027-04-30');
check('31 Jul 2027 payment (Sat) moves later', F.fromDay(F.nextBusinessDay(F.toDay('2027-07-31'))), '2027-08-02');
check('31 Oct 2027 payment (Sun) moves later', F.fromDay(F.nextBusinessDay(F.toDay('2027-10-31'))), '2027-11-01');
check('3 Jul 2027 notice (Sat) moves earlier', F.fromDay(F.prevBusinessDay(F.toDay('2027-07-03'))), '2027-07-02');
check('DOI 15 Nov 2026 (Sun) moves earlier',   F.fromDay(F.prevBusinessDay(F.toDay('2026-11-15'))), '2026-11-13');

/* ---- 3. holidays that the federal list alone would miss ---- */
out.push('--- Maryland state holidays ---');
check('Election Day 3 Nov 2026 is not a business day', F.isBusinessDay(F.toDay('2026-11-03')), 'false');
check('American Indian Heritage Day 27 Nov 2026 is not a business day', F.isBusinessDay(F.toDay('2026-11-27')), 'false');
check('24 Dec 2026 IS a business day', F.isBusinessDay(F.toDay('2026-12-24')), 'true');

/* ---- 4. the DOI countdown never goes negative and never reopens ---- */
out.push('--- DOI countdown across the deadline ---');
['2026-11-12', '2026-11-13', '2026-11-14', '2026-11-20', '2027-06-01'].forEach(function (d) {
  var r = F.compute({
    md_employees: 25, ein_employees: 25, md_payroll: 1750000, pay_frequency: 'biweekly',
    considering_private_plan: true, today: d
  });
  var ok = r.doi.business_days_left >= 0
    && (d <= '2026-11-13' ? r.doi.window_open : !r.doi.window_open)
    && (d <= '2026-11-13' || r.doi.headline === 'closed');
  if (ok) { pass++; } else { fail++; }
  out.push((ok ? 'PASS  ' : 'FAIL  ') + 'DOI on ' + d + '  open=' + r.doi.window_open
    + ' bd_left=' + r.doi.business_days_left + ' headline=' + r.doi.headline);
});

/* ---- 5. every date row is either dated or explicitly undated, and past is marked ---- */
out.push('--- date list on a late date, past items marked not hidden ---');
var late = F.compute({
  md_employees: 30, ein_employees: 30, md_payroll: 2100000, pay_frequency: 'biweekly',
  considering_private_plan: true, today: '2027-02-15'
});
var passedRows = late.dates.filter(function (x) { return x.passed; });
check('some rows are marked passed on 15 Feb 2027', passedRows.length > 0, 'true');
check('no row is silently dropped', late.dates.length >= 8, 'true');
check('notice row still present after it has passed',
  late.dates.some(function (x) { return /Written notice/.test(x.label); }), 'true');

/* ---- 6. validation branches ---- */
out.push('--- validation ---');
var bad = F.compute({ md_employees: 10, ein_employees: 4, md_payroll: 500000, pay_frequency: 'monthly', considering_private_plan: false, today: '2026-08-29' });
check('EIN below Maryland headcount is blocked', bad.in_scope, 'false');
var zero = F.compute({ md_employees: 5, ein_employees: 5, md_payroll: 0, pay_frequency: 'monthly', considering_private_plan: false, today: '2026-08-29' });
check('zero payroll is flagged, not shown as an answer', zero.zero_payroll, 'true');
check('zero payroll stays in scope', zero.in_scope, 'true');

/* ---- 7. there is always a notice, in both withhold and absorb states ---- */
out.push('--- notice always exists ---');
var anyEmployer = F.compute({ md_employees: 8, ein_employees: 8, md_payroll: 480000, pay_frequency: 'biweekly', considering_private_plan: false, today: '2026-08-29' });
check('notice_by is never null', anyEmployer.notice.notice_by !== null, 'true');

console.log(out.join('\n'));
console.log('\n' + pass + ' passed, ' + fail + ' failed');
process.exit(fail ? 1 : 0);
