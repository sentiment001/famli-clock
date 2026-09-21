/* Produces examples.json: every money and date figure published in a worked example
   on the famliclock.com content pages.

   It runs the engine out of the shipped index.html, the same way the repo's own test
   harnesses do, so a published figure can never disagree with what a visitor sees.

   Usage, from the repo root or anywhere:
       node source/run_examples.js path/to/index.html > source/examples.json

   Defaults to ../index.html relative to this file, which is the repo root when this
   folder sits inside the repo. Re-run after ANY change to CONFIG, and in particular
   after the October wage cap update, then rebuild the pages. */
'use strict';
var fs = require('fs');
var path = require('path');
var vm = require('vm');

var htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
var html = fs.readFileSync(htmlPath, 'utf8');
var m = html.match(/<script id="famli-engine">([\s\S]*?)<\/script>/);
if (!m) { throw new Error('No <script id="famli-engine"> block in ' + htmlPath); }
var sandbox = {};
sandbox.self = sandbox;
vm.createContext(sandbox);
vm.runInContext(m[1], sandbox, { filename: htmlPath + '#famli-engine' });
var F = sandbox.FAMLI;
if (!F) { throw new Error('Engine block did not define FAMLI'); }

var TODAY = '2026-09-21';

var CASES = {
  E1_small:      {md_employees:12, ein_employees:12, md_payroll:780000,  pay_frequency:'biweekly',    considering_private_plan:false, today:TODAY},
  E2_large:      {md_employees:40, ein_employees:40, md_payroll:3200000, pay_frequency:'monthly',     considering_private_plan:false, today:TODAY},
  E3_sole:       {md_employees:1,  ein_employees:1,  md_payroll:120000,  pay_frequency:'monthly',     considering_private_plan:false, today:TODAY, sole_owner_only_employee:true},
  E4_oos_big:    {md_employees:10, ein_employees:40, md_payroll:750000,  pay_frequency:'monthly',     considering_private_plan:false, today:TODAY},
  E4b_oos_small: {md_employees:10, ein_employees:12, md_payroll:750000,  pay_frequency:'monthly',     considering_private_plan:false, today:TODAY},
  E5_doi:        {md_employees:25, ein_employees:25, md_payroll:1750000, pay_frequency:'biweekly',    considering_private_plan:true,  today:TODAY},
  N_weekly:      {md_employees:20, ein_employees:20, md_payroll:1300000, pay_frequency:'weekly',      considering_private_plan:false, today:TODAY, first_2027_pay_date:'2027-01-08'},
  N_biweekly:    {md_employees:20, ein_employees:20, md_payroll:1300000, pay_frequency:'biweekly',    considering_private_plan:false, today:TODAY, first_2027_pay_date:'2027-01-08'},
  N_semi:        {md_employees:20, ein_employees:20, md_payroll:1300000, pay_frequency:'semimonthly', considering_private_plan:false, today:TODAY, first_2027_pay_date:'2027-01-15'},
  N_monthly:     {md_employees:20, ein_employees:20, md_payroll:1300000, pay_frequency:'monthly',     considering_private_plan:false, today:TODAY, first_2027_pay_date:'2027-01-29'},
  N_default:     {md_employees:20, ein_employees:20, md_payroll:1300000, pay_frequency:'biweekly',    considering_private_plan:false, today:TODAY}
};

var out = {_meta: {engine: htmlPath + ' #famli-engine', today: TODAY,
                   wage_cap: null, wage_cap_year: null, wage_cap_confirmed: null}};

Object.keys(CASES).forEach(function (k) {
  var r = F.compute(CASES[k]);
  if (r.config) {
    out._meta.wage_cap = r.config.wage_cap;
    out._meta.wage_cap_year = r.config.wage_cap_year;
    out._meta.wage_cap_confirmed = r.config.wage_cap_confirmed;
  }
  function n(v) { return v == null ? null : v; }
  out[k] = {
    input: CASES[k],
    in_scope: r.in_scope, reason: r.reason || null, band: r.band || null,
    rate_bp: n(r.rate_bp), periods_per_year: n(r.periods_per_year),
    base_cents: n(r.base_cents), base_mode: r.base_mode || null, cap_bites: !!r.cap_bites,
    avg_wage_cents: n(r.avg_wage_cents),
    annual_total: n(r.annual_total_cents),
    annual_employer: n(r.annual_employer_if_withholding_cents),
    annual_employee: n(r.annual_employee_if_withholding_cents),
    absorb_annual_employer: n(r.absorb_annual_employer_cents),
    absorb_delta: n(r.absorb_delta_cents),
    per_period_total: n(r.per_period_total_cents),
    per_period_employer: n(r.per_period_employer_cents),
    per_period_employee: n(r.per_period_employee_cents),
    flat_across_year: r.flat_across_year,
    q1_payment: n(r.q1_payment_cents), q1_payment_due: r.q1_payment_due || null,
    quarters: r.quarters || null,
    cost_of_never_withholding: n(r.cost_of_never_withholding_cents),
    cost_per_missed_pay_period: n(r.cost_per_missed_pay_period_cents),
    cost_of_unreported_out_of_state: n(r.cost_of_unreported_out_of_state_cents),
    small_by_md_but_not_by_ein: !!r.small_by_md_but_not_by_ein,
    must_report_out_of_state: !!r.must_report_out_of_state,
    notice: r.notice || null,
    dates: (r.dates || []).map(function (d) { return {label: d.label, date: d.date, kind: d.kind}; })
  };
});

console.log(JSON.stringify(out, null, 1));
