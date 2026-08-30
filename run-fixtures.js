/* Runs the 27 spec fixtures against engine.js and compares, block by block, with
   fixture_table.txt. The expected file was produced by famli_ref.py, which this engine
   was written without reading. Any match is therefore an independent agreement. */
'use strict';
var fs = require('fs');
var F = require('./load-engine.js')();

var TODAY = '2026-08-29';

var FIXTURES = [
  ['F01', '8-employee firm, all wages under the cap',
    { md_employees: 8, ein_employees: 8, md_payroll: 480000, pay_frequency: 'biweekly', considering_private_plan: false, today: TODAY }],
  ['F02', 'Same firm, read the absorb column',
    { md_employees: 8, ein_employees: 8, md_payroll: 480000, pay_frequency: 'biweekly', considering_private_plan: false, today: TODAY }],
  ['F03', '40-employee firm, average wage above the cap',
    { md_employees: 40, ein_employees: 40, md_payroll: 8400000, pay_frequency: 'biweekly', considering_private_plan: false, today: TODAY }],
  ['F04', '200-employee firm, semimonthly',
    { md_employees: 200, ein_employees: 200, md_payroll: 16000000, pay_frequency: 'semimonthly', considering_private_plan: false, today: TODAY }],
  ['F05', '3 Maryland employees, 400 out of state',
    { md_employees: 3, ein_employees: 403, md_payroll: 300000, pay_frequency: 'biweekly', considering_private_plan: false, today: TODAY }],
  ['F06', 'Exactly 15 employees',
    { md_employees: 15, ein_employees: 15, md_payroll: 1050000, pay_frequency: 'biweekly', considering_private_plan: false, today: TODAY }],
  ['F07', '14 employees crossing to 16 mid-year',
    { md_employees: 16, ein_employees: 16, md_payroll: 1050000, pay_frequency: 'biweekly', considering_private_plan: false, today: TODAY,
      quarterly_ein_headcount: [14, 14, 16, 16], quarterly_md_payroll: [245000, 245000, 280000, 280000] }],
  ['F08', 'Private plan, 60 days out, cold start',
    { md_employees: 25, ein_employees: 25, md_payroll: 1750000, pay_frequency: 'biweekly', considering_private_plan: true, today: '2026-09-14' }],
  ['F09', 'Private plan, 10 days out, cold start',
    { md_employees: 25, ein_employees: 25, md_payroll: 1750000, pay_frequency: 'biweekly', considering_private_plan: true, today: '2026-11-03' }],
  ['F10', 'Private plan, past the deadline',
    { md_employees: 25, ein_employees: 25, md_payroll: 1750000, pay_frequency: 'biweekly', considering_private_plan: true, today: '2026-11-20' }],
  ['F11', '48-employee firm wanting to self-insure',
    { md_employees: 48, ein_employees: 48, md_payroll: 3840000, pay_frequency: 'monthly', considering_private_plan: true, today: TODAY }],
  ['F12', 'One Maryland employee, not the sole owner',
    { md_employees: 1, ein_employees: 1, md_payroll: 65000, pay_frequency: 'weekly', considering_private_plan: false, today: TODAY }],
  ['F13', 'Sole owner, only employee of their own entity',
    { md_employees: 1, ein_employees: 1, md_payroll: 120000, pay_frequency: 'monthly', considering_private_plan: false, today: TODAY, sole_owner_only_employee: true }],
  ['F14', 'No Maryland employees',
    { md_employees: 0, ein_employees: 60, md_payroll: 0, pay_frequency: 'biweekly', considering_private_plan: false, today: TODAY }],
  ['F15', 'Wages exactly at the cap',
    { md_employees: 10, ein_employees: 10, md_payroll: 1845000, pay_frequency: 'semimonthly', considering_private_plan: false, today: TODAY }],
  ['F16', 'Small by EIN, staff out of state (the reporting trap)',
    { md_employees: 10, ein_employees: 12, md_payroll: 700000, pay_frequency: 'monthly', considering_private_plan: false, today: TODAY }],
  ['F17', 'One employee paid $2m',
    { md_employees: 1, ein_employees: 1, md_payroll: 2000000, pay_frequency: 'monthly', considering_private_plan: false, today: TODAY }],
  ['F18', 'Skewed payroll, even rule (the A2 error case)',
    { md_employees: 10, ein_employees: 10, md_payroll: 2500000, pay_frequency: 'monthly', considering_private_plan: false, today: TODAY }],
  ['F19', 'Same firm with the high-earner refinement',
    { md_employees: 10, ein_employees: 10, md_payroll: 2500000, pay_frequency: 'monthly', considering_private_plan: false, today: TODAY,
      high_earner_count: 1, high_earner_wages: 1600000 }],
  ['F20', 'Refinement declared as zero high earners',
    { md_employees: 10, ein_employees: 10, md_payroll: 900000, pay_frequency: 'monthly', considering_private_plan: false, today: TODAY,
      high_earner_count: 0 }],
  ['F21', 'Contradictory refinement, must fall back and flag',
    { md_employees: 10, ein_employees: 10, md_payroll: 900000, pay_frequency: 'monthly', considering_private_plan: false, today: TODAY,
      high_earner_count: 3, high_earner_wages: 200000 }],
  ['F22', 'Notice date refinement, biweekly, first pay 8 Jan 2027',
    { md_employees: 30, ein_employees: 30, md_payroll: 2100000, pay_frequency: 'biweekly', considering_private_plan: false, today: TODAY,
      first_2027_pay_date: '2027-01-08' }],
  ['F23', 'Phase 2, already registered, 20 Oct 2026',
    { md_employees: 25, ein_employees: 25, md_payroll: 1750000, pay_frequency: 'biweekly', considering_private_plan: true, today: '2026-10-20',
      doi_progress: 'registered' }],
  ['F24', 'Phase 2, agent already booked, 20 Oct 2026',
    { md_employees: 25, ein_employees: 25, md_payroll: 1750000, pay_frequency: 'biweekly', considering_private_plan: true, today: '2026-10-20',
      doi_progress: 'agent_booked' }],
  ['F25', 'Phase 3, notice urgency, 1 Dec 2026',
    { md_employees: 30, ein_employees: 30, md_payroll: 2100000, pay_frequency: 'biweekly', considering_private_plan: false, today: '2026-12-01' }],
  ['F26', 'Phase 4, contributions live, 15 Feb 2027',
    { md_employees: 30, ein_employees: 30, md_payroll: 2100000, pay_frequency: 'biweekly', considering_private_plan: false, today: '2027-02-15' }],
  ['F28', 'Cap bites while the band changes mid-year',
    { md_employees: 16, ein_employees: 16, md_payroll: 4000000, pay_frequency: 'monthly', considering_private_plan: false, today: TODAY,
      quarterly_ein_headcount: [14, 14, 16, 16] }],
  ['F27', '2028 branch, prior-year average crosses the threshold',
    { md_employees: 20, ein_employees: 20, md_payroll: 1400000, pay_frequency: 'biweekly', considering_private_plan: false, today: '2028-02-01',
      contribution_year: 2028, prior_year_quarterly_headcount: [13, 14, 16, 17] }]
];

/* ---- formatting helpers that mirror the reference renderer exactly ---- */
function grp(s) { return s.replace(/\B(?=(\d{3})+(?!\d))/g, ','); }
function m(c) { return '$' + grp((c / 100).toFixed(2)); }
function f0(c) { return grp(String(Math.round(c / 100))); }
function f2(c) { return grp((c / 100).toFixed(2)); }
function py(b) { return b ? 'True' : 'False'; }
function pad(s, n) { while (s.length < n) { s += ' '; } return s; }
var DOW = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

function render(fid, name, input) {
  var r = F.compute(input);
  var L = [];
  L.push('### ' + fid + ' - ' + name);
  L.push('IN md=' + input.md_employees + ' ein=' + input.ein_employees
    + ' payroll=$' + grp(String(input.md_payroll))
    + ' freq=' + input.pay_frequency
    + ' private=' + py(!!input.considering_private_plan)
    + ' today=' + input.today
    + ' year=' + (input.contribution_year || 2027));
  L.push('PHASE ' + r.phase + ' (' + r.phase_label + ')');
  if (!r.in_scope) { L.push('OUT: not in scope. ' + r.reason); return L.join('\n'); }

  L.push('size_basis=' + r.size_basis.basis + ' band=' + r.band
    + ' rate=' + (r.rate_bp / 100).toFixed(2) + '%'
    + ' avg_wage=' + m(r.avg_wage_cents)
    + ' base_mode=' + r.base_mode
    + ' valid=' + py(r.base_inputs_valid)
    + ' cap_bites=' + py(r.cap_bites)
    + ' base=' + m(r.base_cents));
  L.push('annual_total=' + m(r.annual_total_cents)
    + ' employer_withhold=' + m(r.annual_employer_if_withholding_cents)
    + ' employee=' + m(r.annual_employee_if_withholding_cents)
    + ' employer_absorb=' + m(r.absorb_annual_employer_cents)
    + ' absorb_delta=' + m(r.absorb_delta_cents));
  L.push('per_period total=' + m(r.per_period_total_cents)
    + ' employer=' + m(r.per_period_employer_cents)
    + ' employee=' + m(r.per_period_employee_cents)
    + ' flat_across_year=' + py(r.flat_across_year));
  L.push('quarters ' + r.quarters.map(function (q) {
    return 'Q' + q.quarter + '[' + q.band.slice(0, 2) + ' base ' + f0(q.base_cents) + ' due ' + f2(q.due_cents) + ']';
  }).join(' '));
  L.push('q1_payment=' + m(r.q1_payment_cents) + ' due ' + r.q1_payment_due
    + ' | never_withhold=' + m(r.cost_of_never_withholding_cents)
    + ' per_missed_period=' + m(r.cost_per_missed_pay_period_cents)
    + ' out_of_state_trap=' + m(r.cost_of_unreported_out_of_state_cents));
  L.push('notice mode=' + r.notice.mode + ' by=' + r.notice.notice_by
    + ' (' + DOW[new Date(F.toDay(r.notice.notice_by) * 86400000).getUTCDay()] + ')');

  var flags = [];
  if (r.small_by_md_but_not_by_ein) flags.push('small in MD but not under EIN');
  if (r.must_report_out_of_state) flags.push('must report out-of-state headcount');
  if (!r.base_inputs_valid) flags.push('high-earner inputs contradictory, fell back to even rule');
  if (flags.length) L.push('FLAGS: ' + flags.join('; '));

  if (r.doi) {
    var d = r.doi;
    L.push('DOI open=' + py(d.window_open) + ' progress=' + d.progress
      + ' bd_left=' + d.business_days_left + ' headline=' + d.headline);
    L.push('  remaining bd fast/typical/slow = ' + d.totals_remaining.fast + '/'
      + d.totals_remaining.typical + '/' + d.totals_remaining.slow);
    ['fast', 'typical', 'slow'].forEach(function (k) {
      var v = d.verdict[k];
      L.push('  ' + pad(k, 8) + ' earliest_submit=' + (v.earliest_submission === null ? 'None' : v.earliest_submission)
        + ' fits=' + py(v.fits_deadline)
        + ' fits_with_buffer=' + py(v.fits_with_resubmit_buffer)
        + ' last_cold_start=' + v.last_cold_start);
    });
    L.push('  self_insure=' + py(d.can_self_insure) + ' epip_fee=$' + d.epip_fee);
  }
  return L.join('\n');
}

/* ---- expected blocks ---- */
var expectedRaw = fs.readFileSync(require('path').join(__dirname, 'fixture_table.txt'), 'utf8');
var expected = {};
expectedRaw.split(/\n(?=### )/).forEach(function (blk) {
  var mm = blk.match(/^### (F\d+)/);
  if (mm) expected[mm[1]] = blk.replace(/\s+$/, '');
});

/* ---- run ---- */
var pass = 0, fail = 0, lines = [];
FIXTURES.forEach(function (fx) {
  var fid = fx[0];
  var got, err = null;
  try { got = render(fx[0], fx[1], fx[2]).replace(/\s+$/, ''); }
  catch (e) { got = ''; err = e.message + '\n' + e.stack; }
  var want = expected[fid];
  if (want === undefined) { lines.push('MISSING EXPECTED  ' + fid); fail++; return; }
  if (got === want) { pass++; lines.push('PASS  ' + fid + '  ' + fx[1]); }
  else {
    fail++;
    lines.push('FAIL  ' + fid + '  ' + fx[1]);
    if (err) { lines.push('      threw: ' + err); }
    var g = got.split('\n'), w = want.split('\n');
    for (var i = 0; i < Math.max(g.length, w.length); i++) {
      if (g[i] !== w[i]) {
        lines.push('      want: ' + (w[i] === undefined ? '<none>' : w[i]));
        lines.push('      got : ' + (g[i] === undefined ? '<none>' : g[i]));
      }
    }
  }
});

console.log(lines.join('\n'));
console.log('\n' + pass + ' passed, ' + fail + ' failed, of ' + FIXTURES.length);
process.exit(fail ? 1 : 0);
