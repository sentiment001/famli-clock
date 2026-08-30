"""
Maryland FAMLI Clock - reference implementation v2 (Step 2.2, revised)
Written against FAMLI_Rules_v1.md. Deterministic. No I/O.

v2 changes:
  - Phase machine. Site and email content key off today's date.
  - DOI lead times expressed as a range, not a point estimate.
  - Stage-aware remaining path, so a partly-registered employer gets a real answer.
  - Two optional refinement inputs: high earners, first 2027 pay date.
  - Size determination branches on year (2027 quarterly, 2028+ prior-year average).
"""
from dataclasses import dataclass, field
from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP

# ----------------------------------------------------------------------
# CONFIG
# ----------------------------------------------------------------------

CONFIG = {
    "wage_cap": Decimal("184500"),
    "wage_cap_year": 2026,
    "wage_cap_confirmed": False,
    "total_rate": Decimal("0.009"),
    "employee_share_max": Decimal("0.5"),
    "small_employer_threshold": 15,
    "small_employer_share": Decimal("0.5"),
    "self_insure_min_md_employees": 50,
    "quarterly_size_year": 2027,

    "cp_doi_decision": 15,              # COMAR 09.42.03.10A(2). PRIMARY.

    "doi_window_opens": date(2026, 9, 1),
    "doi_deadline_nominal": date(2026, 11, 15),
    "doi_deadline_business": date(2026, 11, 13),
    "contributions_start": date(2027, 1, 1),
    "q1_payment_due": date(2027, 4, 30),
    "q2_payment_due": date(2027, 7, 31),
    "q3_payment_due": date(2027, 10, 31),
    "q4_payment_due": date(2028, 1, 31),
    "six_month_notice_by": date(2027, 7, 3),
    "epip_application_due": date(2027, 10, 1),
    "epip_approval_by": date(2028, 1, 1),
    "benefits_begin": date(2028, 1, 3),
    "notice_safe_date": date(2026, 12, 1),
    "mia_carrier_filing_deadline": date(2026, 9, 30),
}

# DOI stage durations in business days. Only the decision is a primary source.
# Three scenarios, because no agency publishes these and a single number would be
# false precision.
STAGES = [
    ("designate_officer",
     "Designate an Authorized Officer, gather EIN, NAICS and resident agent details",
     {"fast": 2, "typical": 5, "slow": 10}),
    ("verify_identity",
     "Authorized Officer completes Login.gov identity verification",
     {"fast": 1, "typical": 5, "slow": 10}),
    ("register",
     "Register the employer in the FAMLI Portal",
     {"fast": 1, "typical": 3, "slow": 5}),
    ("book_agent",
     "Find an insurance agent and get a consultation booked",
     {"fast": 5, "typical": 15, "slow": 25}),
    ("consult_and_sign",
     "Hold the consultation and get the signed form back",
     {"fast": 1, "typical": 3, "slow": 5}),
]

PROGRESS = {
    "not_started": 0,
    "officer_named": 1,
    "identity_verified": 2,
    "registered": 3,
    "agent_booked": 4,
    "form_in_hand": 5,
}

HOLIDAYS = {
    date(2026, 9, 7):   "Labor Day",
    date(2026, 10, 12): "Columbus Day",
    date(2026, 11, 3):  "General Election Day (MD)",
    date(2026, 11, 11): "Veterans Day",
    date(2026, 11, 26): "Thanksgiving",
    date(2026, 11, 27): "American Indian Heritage Day (MD)",
    date(2026, 12, 25): "Christmas Day",
    date(2027, 1, 1):   "New Year's Day",
    date(2027, 1, 18):  "Martin Luther King Jr. Day",
    date(2027, 5, 31):  "Memorial Day",
    date(2027, 7, 5):   "Independence Day observed",
    date(2027, 9, 6):   "Labor Day",
    date(2027, 11, 11): "Veterans Day",
    date(2027, 11, 25): "Thanksgiving",
    date(2027, 12, 24): "Christmas Day observed",
    date(2027, 12, 31): "New Year's Day observed",
}

PERIODS_PER_YEAR = {"weekly": 52, "biweekly": 26, "semimonthly": 24, "monthly": 12}
PERIOD_DAYS = {"weekly": 7, "biweekly": 14, "semimonthly": 15, "monthly": 30}

EPIP_FEE_BANDS = [(14, 100), (49, 250), (199, 500), (499, 600), (999, 750), (10**9, 1000)]

PHASES = [
    ("P1_runway",     None,               date(2026, 9, 28),  "DOI runway"),
    ("P2_compressed", date(2026, 9, 29),  date(2026, 11, 13), "DOI compressed"),
    ("P3_notice",     date(2026, 11, 14), date(2026, 12, 31), "Notice and withholding"),
    ("P4_live",       date(2027, 1, 1),   date(2027, 4, 30),  "Contributions live"),
    ("P5_steady",     date(2027, 5, 1),   None,               "Steady state"),
]


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------

def money(x) -> Decimal:
    """COMAR 09.42.02.08A: below half a cent dropped, half or more rounds up."""
    return Decimal(x).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def is_business_day(d: date) -> bool:
    return d.weekday() < 5 and d not in HOLIDAYS


def add_business_days(start: date, n: int) -> date:
    d, moved = start, 0
    while moved < n:
        d += timedelta(days=1)
        if is_business_day(d):
            moved += 1
    return d


def sub_business_days(start: date, n: int) -> date:
    d, moved = start, 0
    while moved < n:
        d -= timedelta(days=1)
        if is_business_day(d):
            moved += 1
    return d


def business_days_between(a: date, b: date) -> int:
    if b < a:
        return -business_days_between(b, a)
    n, d = 0, a
    while d < b:
        d += timedelta(days=1)
        if is_business_day(d):
            n += 1
    return n


def previous_business_day(d: date) -> date:
    """Used for NOTICES and the DOI, where there is no next-business-day relief, so a
    weekend or holiday must push the date earlier rather than later."""
    while not is_business_day(d):
        d -= timedelta(days=1)
    return d


def next_business_day(d: date) -> date:
    """COMAR 09.42.02.08E. Contribution PAYMENTS only. Not notices, not the DOI."""
    while not is_business_day(d):
        d += timedelta(days=1)
    return d


def epip_fee(md_employees: int) -> int:
    for ceiling, fee in EPIP_FEE_BANDS:
        if md_employees <= ceiling:
            return fee
    return 1000


def phase(today: date) -> tuple:
    for key, start, end, label in PHASES:
        if (start is None or today >= start) and (end is None or today <= end):
            return key, label
    return "P5_steady", "Steady state"


# ----------------------------------------------------------------------
# Inputs
# ----------------------------------------------------------------------

@dataclass
class Inputs:
    md_employees: int
    ein_employees: int
    md_payroll: Decimal
    pay_frequency: str
    considering_private_plan: bool
    today: date

    sole_owner_only_employee: bool = False

    high_earner_count: int = None
    high_earner_wages: Decimal = None
    first_2027_pay_date: date = None

    doi_progress: str = "not_started"

    contribution_year: int = 2027
    quarterly_ein_headcount: list = field(default_factory=list)
    quarterly_md_payroll: list = field(default_factory=list)
    prior_year_quarterly_headcount: list = field(default_factory=list)


# ----------------------------------------------------------------------
# Rules
# ----------------------------------------------------------------------

def in_scope(i: Inputs):
    if i.md_employees < 1:
        return False, "No Maryland employees. FAMLI does not apply to you."
    if i.ein_employees == 1 and i.sole_owner_only_employee:
        return False, ("You are the sole owner and the only person your entity employs. "
                       "COMAR 09.42.01.01B(21)(b) says you are not an employer for FAMLI.")
    return True, ""


def size_band(headcount) -> str:
    return "small" if headcount < CONFIG["small_employer_threshold"] else "standard"


def determine_size_basis(i: Inputs) -> dict:
    if i.contribution_year <= CONFIG["quarterly_size_year"]:
        return {"basis": "quarterly",
                "note": "In 2027 employer size is determined each quarter."}
    q = i.prior_year_quarterly_headcount or [i.ein_employees] * 4
    avg = Decimal(sum(q)) / Decimal(len(q))
    return {"basis": "prior_year_average", "average": avg, "band": size_band(avg),
            "note": "From 2028, size is the average of the prior year's four quarters, "
                    "fixed for the whole year."}


def effective_rate(band: str) -> Decimal:
    if band == "small":
        return CONFIG["total_rate"] * CONFIG["small_employer_share"]
    return CONFIG["total_rate"]


def _default_base(i: Inputs) -> dict:
    cap = CONFIG["wage_cap"]
    avg = i.md_payroll / i.md_employees
    if avg > cap:
        return {"base": cap * i.md_employees, "avg_wage": avg, "cap_bites": True,
                "high_earners": None}
    return {"base": i.md_payroll, "avg_wage": avg, "cap_bites": False,
            "high_earners": None}


def capped_base(i: Inputs) -> dict:
    """Default (rule B) assumes wages are broadly even, so the cap bites only when the
    average exceeds it. Refined mode uses the user's own high-earner figures and is
    exact."""
    cap = CONFIG["wage_cap"]
    if i.high_earner_count is not None:
        h = min(int(i.high_earner_count), i.md_employees)
        if h == 0:
            return {"base": i.md_payroll, "mode": "refined", "high_earners": 0,
                    "avg_wage": i.md_payroll / i.md_employees,
                    "cap_bites": False, "valid": True}
        if i.high_earner_wages is not None:
            wh = Decimal(i.high_earner_wages)
            if h * cap <= wh <= i.md_payroll:
                return {"base": h * cap + (i.md_payroll - wh), "mode": "refined",
                        "high_earners": h, "avg_wage": i.md_payroll / i.md_employees,
                        "cap_bites": True, "valid": True}
            return dict(_default_base(i), mode="refined_invalid", valid=False)
    return dict(_default_base(i), mode="even", valid=True)


def ytd_quarter_bases(i: Inputs, base_info: dict) -> list:
    """Per-quarter base, applying the annual per-employee cap year to date. High earners
    and everyone else are modelled separately when the refinement is supplied, because
    they hit the cap at different points in the year."""
    cap = CONFIG["wage_cap"]
    if base_info.get("mode") == "refined" and base_info.get("high_earners"):
        h = base_info["high_earners"]
        wh = Decimal(i.high_earner_wages)
        n_low = i.md_employees - h
        low_payroll = i.md_payroll - wh
        w_high = wh / h
        w_low = (low_payroll / n_low) if n_low else Decimal(0)
        out, prev_h, prev_l = [], Decimal(0), Decimal(0)
        for q in range(1, 5):
            cum_h = min(w_high * q / 4, cap)
            cum_l = min(w_low * q / 4, cap) if n_low else Decimal(0)
            out.append((cum_h - prev_h) * h + (cum_l - prev_l) * n_low)
            prev_h, prev_l = cum_h, cum_l
        return out

    w = i.md_payroll / i.md_employees
    out, prev = [], Decimal(0)
    for q in range(1, 5):
        cum = min(w * Decimal(q) / Decimal(4), cap)
        out.append((cum - prev) * i.md_employees)
        prev = cum
    return out


def notice_dates(i: Inputs) -> dict:
    """Pre-withholding notice, COMAR 09.42.02.05D. At least one full pay period before
    the first 2027 withholding."""
    safe = CONFIG["notice_safe_date"]
    if i.first_2027_pay_date:
        raw = i.first_2027_pay_date - timedelta(days=PERIOD_DAYS[i.pay_frequency])
        exact = previous_business_day(raw)
        return {"mode": "exact", "notice_by": exact, "notice_by_raw": raw, "safe_for_everyone": safe,
                "first_pay_date": i.first_2027_pay_date,
                "note": "One full pay period before your first 2027 pay date."}
    return {"mode": "safe_default", "notice_by": safe, "safe_for_everyone": safe,
            "first_pay_date": None,
            "note": "Safe at every pay frequency. Tell us your first 2027 pay date and "
                    "we will give you the exact one."}


def _doi_headline(verdict: dict, open_: bool) -> str:
    if not open_:
        return "closed"
    if verdict["slow"]["fits_with_resubmit_buffer"]:
        return "comfortable"
    if verdict["typical"]["fits_with_resubmit_buffer"]:
        return "on_track"
    if verdict["typical"]["fits_deadline"]:
        return "tight"
    if verdict["fast"]["fits_deadline"]:
        return "only_if_everything_goes_right"
    return "does_not_fit"


def doi_block(i: Inputs) -> dict:
    deadline = CONFIG["doi_deadline_business"]
    today = i.today
    done = PROGRESS.get(i.doi_progress, 0)
    remaining = STAGES[done:]

    totals = {k: sum(s[2][k] for s in remaining) for k in ("fast", "typical", "slow")}
    full = {k: sum(s[2][k] for s in STAGES) for k in ("fast", "typical", "slow")}

    open_ = today <= deadline
    bd_left = business_days_between(today, deadline) if open_ else 0
    decision = CONFIG["cp_doi_decision"]

    def backward(target, scenario):
        d, out = target, {}
        for key, label, dur in reversed(STAGES):
            out[key] = d
            d = sub_business_days(d, dur[scenario])
        out["start_by"] = d
        out["submit_by"] = target
        return out

    safe_submit = sub_business_days(deadline, decision)

    verdict = {}
    for k in ("fast", "typical", "slow"):
        verdict[k] = {
            "business_days_needed": totals[k],
            "earliest_submission": add_business_days(today, totals[k]) if open_ else None,
            "fits_deadline": open_ and bd_left >= totals[k],
            "fits_with_resubmit_buffer": open_ and bd_left >= totals[k] + decision,
            "last_cold_start": sub_business_days(deadline, full[k]),
        }

    return {
        "window_open": open_,
        "window_opens": CONFIG["doi_window_opens"],
        "deadline_business": deadline,
        "deadline_nominal": CONFIG["doi_deadline_nominal"],
        "calendar_days_left": (deadline - today).days,
        "business_days_left": bd_left,
        "progress": i.doi_progress,
        "stages_remaining": [(s[0], s[1], s[2]) for s in remaining],
        "totals_remaining": totals,
        "totals_full_path": full,
        "decision_business_days": decision,
        "safe_submit_by": safe_submit,
        "verdict": verdict,
        "headline": _doi_headline(verdict, open_),
        "safe_path": backward(safe_submit, "typical"),
        "deadline_path": backward(deadline, "typical"),
        "can_self_insure": i.md_employees >= CONFIG["self_insure_min_md_employees"],
        "epip_fee": epip_fee(i.md_employees),
        "epip_application_due": CONFIG["epip_application_due"],
        "mia_carrier_filing_deadline": CONFIG["mia_carrier_filing_deadline"],
    }


def date_list(i: Inputs) -> list:
    t = i.today
    nd = notice_dates(i)
    items = [
        ("Register with FAMLI", None,
         "Registration is open. No approval step, no queue."),
        ("Written notice to employees before you withhold", nd["notice_by"], nd["note"]),
        ("Start withholding", CONFIG["contributions_start"], "First 2027 pay period."),
        ("First report and payment (Q1 wages)", next_business_day(CONFIG["q1_payment_due"]),
         "Covers January to March 2027."),
        ("Six-month notice before benefits", CONFIG["six_month_notice_by"],
         "3 Jul 2027 is a Saturday. The next-business-day rule covers payments, not "
         "notices, so treat Friday 2 Jul as the date."),
        ("Q2 report and payment", next_business_day(CONFIG["q2_payment_due"]),
         "31 Jul 2027 is a Saturday."),
        ("Q3 report and payment", next_business_day(CONFIG["q3_payment_due"]),
         "31 Oct 2027 is a Sunday."),
        ("Q4 report and payment", next_business_day(CONFIG["q4_payment_due"]), ""),
        ("Benefits begin", CONFIG["benefits_begin"], "Your employees can claim."),
    ]
    if i.considering_private_plan:
        items += [
            ("Submit your Declaration of Intent", CONFIG["doi_deadline_business"],
             "15 Nov 2026 is a Sunday. Friday 13 Nov is the last business day."),
            ("Submit by here to survive a rejection",
             sub_business_days(CONFIG["doi_deadline_business"], CONFIG["cp_doi_decision"]),
             "FAMLI has 15 business days to decide. Submit by this date and a rejected "
             "form can still be fixed and resubmitted."),
            ("Apply for the private plan itself (EPIP)", CONFIG["epip_application_due"],
             "The DOI is not the application."),
            ("Private plan must be approved", CONFIG["epip_approval_by"],
             "If it is not, the escrow is remitted with interest and penalties."),
        ]
    out = [{"label": l, "date": d, "note": n,
            "days_remaining": (d - t).days if d else None,
            "passed": bool(d and d < t)} for l, d, n in items]
    out.sort(key=lambda x: (x["date"] is not None, x["date"] or t))
    return out


def compute(i: Inputs) -> dict:
    ok, reason = in_scope(i)
    ph, ph_label = phase(i.today)
    if not ok:
        return {"in_scope": False, "reason": reason, "phase": ph, "phase_label": ph_label}

    size = determine_size_basis(i)
    band = (size.get("band") if size["basis"] == "prior_year_average"
            else size_band(i.ein_employees))
    rate = effective_rate(band)
    bi = capped_base(i)

    if i.quarterly_ein_headcount and size["basis"] == "quarterly":
        q_bases = i.quarterly_md_payroll or ytd_quarter_bases(i, bi)
        q_bands = [size_band(hc) for hc in i.quarterly_ein_headcount]
        q_heads = i.quarterly_ein_headcount
    else:
        q_bases = ytd_quarter_bases(i, bi)
        q_bands = [band] * 4
        q_heads = [i.ein_employees] * 4

    quarters = []
    for n, (qb, qband, qhc) in enumerate(zip(q_bases, q_bands, q_heads), start=1):
        qrate = effective_rate(qband)
        total_q = money(Decimal(qb) * qrate)
        emp_max_q = money(Decimal(qb) * CONFIG["total_rate"] * CONFIG["employee_share_max"])
        employee_q = min(total_q, emp_max_q)
        quarters.append({"quarter": n, "headcount": qhc, "band": qband, "rate": qrate,
                         "base": money(qb), "due": total_q,
                         "employee": employee_q, "employer": money(total_q - employee_q)})

    annual_total = money(sum(q["due"] for q in quarters))
    employee_if_withholding = money(sum(q["employee"] for q in quarters))
    employer_if_withholding = money(sum(q["employer"] for q in quarters))

    ppy = PERIODS_PER_YEAR[i.pay_frequency]
    pp_q = Decimal(ppy) / 4
    trap = (i.ein_employees < CONFIG["small_employer_threshold"]
            and i.ein_employees > i.md_employees)

    out = {
        "in_scope": True,
        "phase": ph,
        "phase_label": ph_label,
        "contribution_year": i.contribution_year,
        "size_basis": size,
        "band": band,
        "rate": rate,
        "avg_wage": money(bi["avg_wage"]),
        "cap_bites": bi["cap_bites"],
        "base_mode": bi["mode"],
        "base_inputs_valid": bi["valid"],
        "base": money(bi["base"]),
        "annual_total": annual_total,
        "annual_employer_if_withholding": employer_if_withholding,
        "annual_employee_if_withholding": employee_if_withholding,
        "per_period_total": money(quarters[0]["due"] / pp_q),
        "per_period_employer": money(quarters[0]["employer"] / pp_q),
        "per_period_employee": money(quarters[0]["employee"] / pp_q),
        "flat_across_year": len({q["due"] for q in quarters}) == 1,
        "absorb_annual_employer": annual_total,
        "withhold_annual_employer": employer_if_withholding,
        "absorb_delta": money(annual_total - employer_if_withholding),
        "cost_per_missed_pay_period": money(quarters[0]["employee"] / pp_q),
        "cost_of_never_withholding": employee_if_withholding,
        "quarters": quarters,
        "q1_payment": quarters[0]["due"],
        "q1_payment_due": next_business_day(CONFIG["q1_payment_due"]),
        "notice": notice_dates(i),
        "must_report_out_of_state": trap,
        "cost_of_unreported_out_of_state": annual_total if trap else money(0),
        "small_by_md_but_not_by_ein": (i.md_employees < CONFIG["small_employer_threshold"]
                                       <= i.ein_employees),
        "dates": date_list(i),
    }
    if i.considering_private_plan:
        out["doi"] = doi_block(i)
    return out
