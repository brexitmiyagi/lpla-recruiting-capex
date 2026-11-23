# Can the model's rules, started from Q4 2025, reproduce Q1-Q3 2026? Assets and share count are the actuals;
# everything else follows the same rules eps_model.py uses for 2027-2028.
from common import rows
q = {r["quarter"]: {k: (float(v) if k not in ("quarter", "source") else v) for k, v in r.items()} for r in rows("quarters_2025q3_2026q3.csv")}
def costs(r): return r["core_ga_m"] + r["ta_amort_m"] + r["promo_m"] + r["share_comp_m"] + r["regulatory_m"] + r["da_m"] + r["interest_m"]
for k in q: q[k]["gp"] = q[k]["adj_pretax_m"] + costs(q[k])
b = q["2025Q4"]; avg_b = (q["2025Q3"]["client_assets_end_bn"] + b["client_assets_end_bn"]) / 2
gp_ex_rate = (b["gp"] - b["client_cash_rev_m"]) / avg_b
cash_rate = b["client_cash_rev_m"] / avg_b
tax = 0.265
prev = b["client_assets_end_bn"]
print(f"Q4 2025 base: gross profit ${b['gp']:.1f}m (derived), ex-cash {gp_ex_rate:.4f} $m per $bn a quarter")
errs = []
for i, k in enumerate(["2026Q1", "2026Q2", "2026Q3"], start=1):
    a = q[k]; avg = (prev + a["client_assets_end_bn"]) / 2; prev = a["client_assets_end_bn"]
    gp = gp_ex_rate * avg + cash_rate * avg
    core = b["core_ga_m"] * 1.05 ** (i / 4)
    ta = avg * 15.5 / 10 * 0.151 / 4
    promo = b["promo_m"] * 1.05 ** (i / 4)
    da = b["da_m"] * 1.02 ** i
    pt = gp - core - ta - promo - 22 - 7 - da - b["interest_m"]
    eps = pt * (1 - tax) / (a["diluted_shares_k"] / 1000)
    err = eps / a["adj_eps"] - 1; errs.append(err)
    print(f"{k}: predicted gross profit ${gp:.0f}m vs actual ${a['gp']:.0f}m ({gp/a['gp']-1:+.1%}); adj EPS ${eps:.2f} vs actual ${a['adj_eps']:.2f} ({err:+.1%})")
print(f"average EPS error {sum(errs)/len(errs):+.1%}")
