# How many DCA accounts the wider eligibility added, what they're worth to LPL, and whether the wave is over.
# Method: implied accounts each quarter (dca_economics.py); take the recent run-rate (Q2-Q3 2026) as trend;
# anything above trend in the waves is "extra". Two waves: Q4 2024-Q2 2025 (most likely Atria) and Q3 2025-Q1 2026 (eligibility).
import io, contextlib
from common import rows
with contextlib.redirect_stdout(io.StringIO()):
    import dca_economics as D

acc = {}
for r in rows("sweep_yields_quarterly.csv"):
    if not r["dca_revenue_k"]: continue
    y, q = int(r["quarter"][:4]), int(r["quarter"][-1])
    acc[r["quarter"]] = float(r["dca_revenue_k"]) * 1000 / 3 / D.quarter_fee(y, q)
g = {k: acc[k] / acc[p] - 1 for p, k in zip(list(acc)[:-1], list(acc)[1:])}
trend = (g["2026Q2"] + g["2026Q3"]) / 2
print(f"quarterly growth in implied accounts: " + ", ".join(f"{k} {v:+.1%}" for k, v in g.items()))
print(f"trend since the wave (Q2-Q3 2026 average): {trend:+.1%} a quarter")
pre = (g["2024Q2"] + g["2024Q3"]) / 2
print(f"before any of it (Q2-Q3 2024 average): {pre:+.1%} a quarter")

fee_yr = 19.50 * 12; tax = 0.265; shares = 78.968; pe = 10.85
def wave(a, b, n, label):
    extra = acc[b] - acc[a] * (1 + trend) ** n
    pre_tax = extra * fee_yr / 1e6
    ps = pre_tax * (1 - tax) / shares
    print(f"{label}: {acc[a]/1e6:.2f}m ({a}) to {acc[b]/1e6:.2f}m ({b}); trend alone would give {acc[a]*(1+trend)**n/1e6:.2f}m, "
          f"so about {extra/1e6:.2f}m extra accounts, ${pre_tax:.0f}m a year before tax at $19.50 a month, ${ps:.2f} a share after tax, about ${ps*pe:.0f} a share at {pe}x")
    return extra, ps
w1 = wave("2024Q3", "2025Q2", 3, "wave 1 (Atria's move onto LPL's platform, most likely)")
w2 = wave("2025Q2", "2026Q1", 3, "wave 2 (wider eligibility)")
tot = acc["2026Q3"]
print(f"wave 2 accounts are about {w2[0]/tot:.0%} of today's {tot/1e6:.2f}m")
print(f"is it over? the last two quarters grew {g['2026Q2']:+.1%} and {g['2026Q3']:+.1%}, against {g['2025Q3']:+.1%}, {g['2025Q4']:+.1%} and {g['2026Q1']:+.1%} in the wave")
print("caveat: 'extra' depends on the trend I take out; at 2% a quarter instead the extra is larger, at 4% smaller")
for t in (0.02, 0.04):
    e = acc["2026Q1"] - acc["2025Q2"] * (1 + t) ** 3
    print(f"  trend {t:.0%}: wave 2 about {e/1e6:.2f}m accounts, ${e*fee_yr*(1-tax)/shares/1e6:.2f} a share after tax")
