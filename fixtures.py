from decimal import Decimal
from datetime import date
from famli_ref import Inputs, compute, CONFIG, doi_block, phase

D = Decimal
TODAY = date(2026, 8, 29)

FIXTURES = [
    # --- money ---
    ("F01", "8-employee firm, all wages under the cap",
     Inputs(8, 8, D("480000"), "biweekly", False, TODAY)),
    ("F02", "Same firm, read the absorb column",
     Inputs(8, 8, D("480000"), "biweekly", False, TODAY)),
    ("F03", "40-employee firm, average wage above the cap",
     Inputs(40, 40, D("8400000"), "biweekly", False, TODAY)),
    ("F04", "200-employee firm, semimonthly",
     Inputs(200, 200, D("16000000"), "semimonthly", False, TODAY)),
    ("F05", "3 Maryland employees, 400 out of state",
     Inputs(3, 403, D("300000"), "biweekly", False, TODAY)),
    ("F06", "Exactly 15 employees",
     Inputs(15, 15, D("1050000"), "biweekly", False, TODAY)),
    ("F07", "14 employees crossing to 16 mid-year",
     Inputs(16, 16, D("1050000"), "biweekly", False, TODAY,
            quarterly_ein_headcount=[14, 14, 16, 16],
            quarterly_md_payroll=[D("245000"), D("245000"), D("280000"), D("280000")])),
    # --- DOI ---
    ("F08", "Private plan, 60 days out, cold start",
     Inputs(25, 25, D("1750000"), "biweekly", True, date(2026, 9, 14))),
    ("F09", "Private plan, 10 days out, cold start",
     Inputs(25, 25, D("1750000"), "biweekly", True, date(2026, 11, 3))),
    ("F10", "Private plan, past the deadline",
     Inputs(25, 25, D("1750000"), "biweekly", True, date(2026, 11, 20))),
    ("F11", "48-employee firm wanting to self-insure",
     Inputs(48, 48, D("3840000"), "monthly", True, TODAY)),
    # --- scope ---
    ("F12", "One Maryland employee, not the sole owner",
     Inputs(1, 1, D("65000"), "weekly", False, TODAY)),
    ("F13", "Sole owner, only employee of their own entity",
     Inputs(1, 1, D("120000"), "monthly", False, TODAY, sole_owner_only_employee=True)),
    ("F14", "No Maryland employees",
     Inputs(0, 60, D("0"), "biweekly", False, TODAY)),
    # --- boundaries ---
    ("F15", "Wages exactly at the cap",
     Inputs(10, 10, D("1845000"), "semimonthly", False, TODAY)),
    ("F16", "Small by EIN, staff out of state (the reporting trap)",
     Inputs(10, 12, D("700000"), "monthly", False, TODAY)),
    ("F17", "One employee paid $2m",
     Inputs(1, 1, D("2000000"), "monthly", False, TODAY)),
    # --- v2 additions ---
    ("F18", "Skewed payroll, even rule (the A2 error case)",
     Inputs(10, 10, D("2500000"), "monthly", False, TODAY)),
    ("F19", "Same firm with the high-earner refinement",
     Inputs(10, 10, D("2500000"), "monthly", False, TODAY,
            high_earner_count=1, high_earner_wages=D("1600000"))),
    ("F20", "Refinement declared as zero high earners",
     Inputs(10, 10, D("900000"), "monthly", False, TODAY, high_earner_count=0)),
    ("F21", "Contradictory refinement, must fall back and flag",
     Inputs(10, 10, D("900000"), "monthly", False, TODAY,
            high_earner_count=3, high_earner_wages=D("200000"))),
    ("F22", "Notice date refinement, biweekly, first pay 8 Jan 2027",
     Inputs(30, 30, D("2100000"), "biweekly", False, TODAY,
            first_2027_pay_date=date(2027, 1, 8))),
    ("F23", "Phase 2, already registered, 20 Oct 2026",
     Inputs(25, 25, D("1750000"), "biweekly", True, date(2026, 10, 20),
            doi_progress="registered")),
    ("F24", "Phase 2, agent already booked, 20 Oct 2026",
     Inputs(25, 25, D("1750000"), "biweekly", True, date(2026, 10, 20),
            doi_progress="agent_booked")),
    ("F25", "Phase 3, notice urgency, 1 Dec 2026",
     Inputs(30, 30, D("2100000"), "biweekly", False, date(2026, 12, 1))),
    ("F26", "Phase 4, contributions live, 15 Feb 2027",
     Inputs(30, 30, D("2100000"), "biweekly", False, date(2027, 2, 15))),
    ("F28", "Cap bites while the band changes mid-year",
     Inputs(16, 16, D("4000000"), "monthly", False, TODAY,
            quarterly_ein_headcount=[14, 14, 16, 16])),
    ("F27", "2028 branch, prior-year average crosses the threshold",
     Inputs(20, 20, D("1400000"), "biweekly", False, date(2028, 2, 1),
            contribution_year=2028, prior_year_quarterly_headcount=[13, 14, 16, 17])),
]


def m(x): return f"${x:,.2f}"


def render():
    print("Maryland FAMLI - computed fixture output (spec v2)")
    print("Generated from famli_ref.py. Reference date 29 Aug 2026 unless the fixture sets its own.")
    print("=" * 78)
    for fid, name, i in FIXTURES:
        r = compute(i)
        print(f"\n### {fid} - {name}")
        print(f"IN md={i.md_employees} ein={i.ein_employees} payroll=${i.md_payroll:,.0f} "
              f"freq={i.pay_frequency} private={i.considering_private_plan} today={i.today} "
              f"year={i.contribution_year}")
        print(f"PHASE {r['phase']} ({r['phase_label']})")
        if not r["in_scope"]:
            print(f"OUT: not in scope. {r['reason']}"); continue
        print(f"size_basis={r['size_basis']['basis']} band={r['band']} rate={r['rate']*100:.2f}% "
              f"avg_wage={m(r['avg_wage'])} base_mode={r['base_mode']} valid={r['base_inputs_valid']} "
              f"cap_bites={r['cap_bites']} base={m(r['base'])}")
        print(f"annual_total={m(r['annual_total'])} employer_withhold={m(r['annual_employer_if_withholding'])} "
              f"employee={m(r['annual_employee_if_withholding'])} employer_absorb={m(r['absorb_annual_employer'])} "
              f"absorb_delta={m(r['absorb_delta'])}")
        print(f"per_period total={m(r['per_period_total'])} employer={m(r['per_period_employer'])} "
              f"employee={m(r['per_period_employee'])} flat_across_year={r['flat_across_year']}")
        print("quarters " + " ".join(
            f"Q{q['quarter']}[{q['band'][:2]} base {q['base']:,.0f} due {q['due']:,.2f}]"
            for q in r["quarters"]))
        print(f"q1_payment={m(r['q1_payment'])} due {r['q1_payment_due']} | "
              f"never_withhold={m(r['cost_of_never_withholding'])} "
              f"per_missed_period={m(r['cost_per_missed_pay_period'])} "
              f"out_of_state_trap={m(r['cost_of_unreported_out_of_state'])}")
        n = r["notice"]
        print(f"notice mode={n['mode']} by={n['notice_by']} ({n['notice_by'].strftime('%a')})")
        flags = []
        if r["small_by_md_but_not_by_ein"]: flags.append("small in MD but not under EIN")
        if r["must_report_out_of_state"]: flags.append("must report out-of-state headcount")
        if not r["base_inputs_valid"]: flags.append("high-earner inputs contradictory, fell back to even rule")
        if flags: print("FLAGS: " + "; ".join(flags))
        if "doi" in r:
            d = r["doi"]
            print(f"DOI open={d['window_open']} progress={d['progress']} "
                  f"bd_left={d['business_days_left']} headline={d['headline']}")
            print(f"  remaining bd fast/typical/slow = {d['totals_remaining']['fast']}/"
                  f"{d['totals_remaining']['typical']}/{d['totals_remaining']['slow']}")
            for k in ("fast", "typical", "slow"):
                v = d["verdict"][k]
                print(f"  {k:8s} earliest_submit={v['earliest_submission']} "
                      f"fits={v['fits_deadline']} fits_with_buffer={v['fits_with_resubmit_buffer']} "
                      f"last_cold_start={v['last_cold_start']}")
            print(f"  self_insure={d['can_self_insure']} epip_fee=${d['epip_fee']}")


if __name__ == "__main__":
    render()
