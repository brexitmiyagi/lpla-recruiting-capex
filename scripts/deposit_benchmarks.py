# What banks pay for LPL's advisory IRA cash, next to what they pay for other deposits, as a share of fed funds.
from common import rows, kv
B = {r["series"]: r for r in rows("deposit_benchmarks.csv")}
ff = {k: float(B["fed_funds_effective_avg_pct"][k]) for k in ("q3_2024", "q3_2025", "q3_2026")}
lpl_bank = {"q3_2024": 4.00 + 0.25, "q3_2025": 4.01 + 0.30, "q3_2026": 3.46 + 0.30}   # DCA fee yield + client rate (dca_economics.py)
lpl_client = {"q3_2024": 0.25, "q3_2025": 0.30, "q3_2026": 0.30}
def line(name, vals):
    print(f"  {name}: " + ", ".join(f"{k[-4:]} {vals[k]:.2f}% ({vals[k]/ff[k]:.0%})" for k in ("q3_2024", "q3_2025", "q3_2026")))
print("rate, and share of the average fed funds rate, Q3 of each year:")
line("banks paying for LPL advisory IRA cash (at least)", lpl_bank)
for k, lab in (("jpm_interest_bearing_deposits_rate_pct", "JPMorgan interest-bearing deposits"), ("wfc_interest_bearing_deposits_rate_pct", "Wells Fargo interest-bearing deposits"),
               ("bac_interest_bearing_deposits_rate_pct", "Bank of America interest-bearing deposits"), ("schw_bank_deposits_rate_pct", "Schwab bank deposits (mostly swept brokerage cash)"),
               ("fdic_national_12m_cd_rate_pct", "FDIC national 12-month CD"), ("fdic_national_savings_rate_pct", "FDIC national savings")):
    line(lab, {q: float(B[k][q]) for q in ff})
line("LPL advisory IRA client rate", lpl_client)
s = kv("sweep.csv")
print(f"Schwab's brokered CDs: weighted-average {s['schw_brokered_cd_weighted_rate_2026_09_30']*100:.2f}% at 30 Sep 2026, against 3.88% effective fed funds then ({s['schw_brokered_cd_weighted_rate_2026_09_30']*100/3.88:.0%})")
print("so in 2026 the banks price LPL's IRA cash like wholesale funding (brokered CDs), about twice what the big banks pay on their deposits overall,")
print("while the client earns less than the FDIC national savings rate")
