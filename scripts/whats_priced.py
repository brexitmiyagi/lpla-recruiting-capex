# What today's price already assumes about LPL's advisory IRA (DCA) fee, and the per-share effect of each risk.
import io, contextlib
from eps_model import run
from common import kv
with contextlib.redirect_stdout(io.StringIO()):
    import valuation as V   # reuses fwd_eps, gb, cases, multiples, litigation, cost of equity

price, div, ke, lit = V.price, V.div, V.ke, V.lit
dca_fee_rev = 557.0            # $m a year at today's target (dca_fix_costs.py)

def value_today(giveback_m, pe):
    v12 = V.fwd_eps(run(dict(sweep_giveback_pretax_yr=giveback_m))) * pe - lit
    return (v12 + div) / (1 + ke)

for pe, lab in ((V.pe_lo, "no rerating"), (V.pe_med, "historical median")):
    lo, hi = 0.0, dca_fee_rev * 3
    if value_today(0, pe) <= price:
        print(f"at {pe}x ({lab}): even no change is worth less than today's price"); continue
    for _ in range(60):
        m = (lo + hi) / 2
        lo, hi = (m, hi) if value_today(m, pe) > price else (lo, m)
    print(f"at {pe}x ({lab}): no change is worth ${value_today(0, pe):.2f} today; the price assumes a give-back of ${m:.0f}m a year pre-tax, "
          f"{m/dca_fee_rev:.0%} of the DCA fee")

# risk table: change in the probability-weighted 12-month value at 11.54x
def weighted(extra):
    return sum(w * (V.fwd_eps(run(dict(a, **extra))) * V.pe_lo - lit) for _, _, a, w in V.cases)
base = weighted({})
print(f"base weighted value ${base:.2f}")
risks = [("S&P 500 -10% (client assets -5%)", dict(initial_asset_shock=-0.045 - 0.05)),
         ("S&P 500 +10%", dict(initial_asset_shock=-0.045 + 0.05)),
         ("Fed -25 bp", dict(fed_change_bp=-25)), ("Fed +25 bp", dict(fed_change_bp=25)),
         ("cash drain at double my pace (0.2 pt in 2027, 0.1 pt in 2028)", dict(cash_drift_yr=(0.0, -0.002, -0.001))),
         ("LPL cuts the DCA fee 25% on top of each case", dict(sweep_giveback_pretax_yr=0)),]
for lab, a in risks[:5]:
    v = weighted(a); print(f"  {lab}: ${v:.2f} ({v-base:+.2f} a share)")
for cut in (0.25, 0.50):
    v = sum(w * (V.fwd_eps(run(dict(a, sweep_giveback_pretax_yr=a.get("sweep_giveback_pretax_yr", 0) + dca_fee_rev * cut))) * V.pe_lo - lit) for _, _, a, w in V.cases)
    print(f"  DCA fee cut {cut:.0%} on top of each case (or a schedule change of that size): ${v:.2f} ({v-base:+.2f} a share)")
for lab, l in (("litigation dismissed", 0.0), ("litigation: full DCA disgorgement", 15.86)):
    v = base + lit - l; print(f"  {lab}: ${v:.2f} ({v-base:+.2f} a share)")

print("value today against the share of the DCA fee given up:")
for pct in (0, 0.25, 0.5, 0.75, 1.0):
    print(f"  {pct:.0%}: at {V.pe_lo}x ${value_today(dca_fee_rev*pct, V.pe_lo):.2f}, at {V.pe_med}x ${value_today(dca_fee_rev*pct, V.pe_med):.2f}")
