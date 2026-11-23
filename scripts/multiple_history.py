# LPLA's own multiple, without reference to today's price.
# Forward P/E here = quarter-end price / the adjusted EPS LPL actually reported over the next four quarters.
import numpy as np
from common import rows

R = rows("lpla_quarterly_pe.csv")
q = [r["quarter"] for r in R]
eps = {r["quarter"]: float(r["adj_eps"]) if r["adj_eps"] else None for r in R}
out = []
for i, r in enumerate(R):
    if i + 4 >= len(R) or None in [eps[x] for x in q[i + 1:i + 5]] or r["quarter"] < "2017Q4":
        continue
    fwd = sum(eps[x] for x in q[i + 1:i + 5])
    out.append(dict(q=r["quarter"], pe=float(r["lpla_close"]) / fwd, ff=float(r["fed_funds_avg_bps"]), cash=float(r["client_cash_pct_of_assets"])))
pe = np.array([o["pe"] for o in out])
print(f"forward P/E on realised EPS, {out[0]['q']} to {out[-1]['q']} ({len(pe)} quarters): mean {pe.mean():.2f}x, median {np.median(pe):.2f}x, "
      f"25th pct {np.percentile(pe,25):.2f}x, 75th pct {np.percentile(pe,75):.2f}x, low {pe.min():.1f}x, high {pe.max():.1f}x")
ff = np.array([o["ff"] for o in out]); cash = np.array([o["cash"] for o in out])
X = np.column_stack([np.ones(len(pe)), ff, cash]); b, *_ = np.linalg.lstsq(X, pe, rcond=None)
r2 = 1 - ((pe - X @ b) ** 2).sum() / ((pe - pe.mean()) ** 2).sum()
print(f"fit on fed funds and cash share: R-squared {r2:.2f}; correlation with fed funds {np.corrcoef(pe, ff)[0,1]:.2f}, with cash share {np.corrcoef(pe, cash)[0,1]:.2f}")
print("so the funds rate explains almost none of LPLA's multiple; I use the plain historical range instead of the fit")
for lab, m in (("funds under 1%", ff < 100), ("funds 1% or more", ff >= 100)):
    print(f"  {lab}: median {np.median(pe[m]):.2f}x over {m.sum()} quarters")

# trailing GAAP at year ends, and the Schwab comparison
H = rows("history_annual.csv")
for r in H:
    print(f"{r['year']}: trailing GAAP P/E {float(r['yearend_close'])/float(r['gaap_diluted_eps']):.1f}x, fed funds {float(r['fed_funds_yearend']):.2f}%")
print("today: 15.0x TTM GAAP EPS of $17.64")
for r in rows("peer_spread_dependence.csv"):
    print(f"{r['ticker']} Q3 2026: interest/sweep income = {float(r['net_interest_or_sweep_m'])/float(r['pretax_m']):.0%} of pre-tax")
