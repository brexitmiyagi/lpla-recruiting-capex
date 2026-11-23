# How many DCA accounts the 2025 waves added, what they're worth to LPL, and whether it's over.
# Three things overlap: Prudential's move onto LPL's platform (Nov 2024), Atria's conversion (July 2025, per LPL's 10-Q)
# and the wider DCA eligibility (between the July 2024 and October 2025 booklets). Public data can't split them.
# Method: implied accounts each quarter (dca_economics.py); take the recent run-rate (Q2-Q3 2026) as trend;
# anything above trend in the waves is "extra".
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
w1 = wave("2024Q3", "2025Q2", 3, "wave 1 (after Prudential Advisors moved onto LPL's platform in Nov 2024)")
w2 = wave("2025Q2", "2026Q1", 3, "wave 2 (starts the quarter Atria converted, July 2025; overlaps the wider eligibility)")
both = w1[0] + w2[0]
print(f"both waves: about {both/1e6:.2f}m accounts, ${both*fee_yr/1e6:.0f}m a year before tax, ${both*fee_yr*(1-tax)/shares/1e6:.2f} a share after tax")
acc_tot = {r['quarter']: float(r['total_client_accounts_m']) for r in rows('total_client_accounts.csv')}
print(f"DCA accounts as a share of all LPL client accounts: {acc['2024Q1']/1e6/acc_tot['2024Q1']:.1%} in Q1 2024, {acc['2026Q3']/1e6/acc_tot['2026Q3']:.1%} in Q3 2026, {acc['2026Q3']/1e6/(acc_tot['2026Q3']-0.9):.1%} without Commonwealth's ~0.9m (not converted until Nov 2026)")
tot = acc["2026Q3"]
print(f"wave 2 accounts are about {w2[0]/tot:.0%} of today's {tot/1e6:.2f}m; both waves {both/tot:.0%}")
print(f"is it over? the last two quarters grew {g['2026Q2']:+.1%} and {g['2026Q3']:+.1%}, against {g['2025Q3']:+.1%}, {g['2025Q4']:+.1%} and {g['2026Q1']:+.1%} in the wave")
print("caveat: 'extra' depends on the trend I take out; at 2% a quarter instead the extra is larger, at 4% smaller")
for t in (0.02, 0.04):
    e = acc["2026Q1"] - acc["2025Q2"] * (1 + t) ** 3
    print(f"  trend {t:.0%}: wave 2 about {e/1e6:.2f}m accounts, ${e*fee_yr*(1-tax)/shares/1e6:.2f} a share after tax")

# test: what average balance did the added accounts bring? SEP and SIMPLE IRAs should be smaller than the book.
bal = {r["quarter"]: float(r["dca_avg_bn"]) * 1e9 for r in rows("sweep_yields_quarterly.csv") if r["dca_avg_bn"]}
def marginal(a, b, label):
    m = (bal[b] - bal[a]) / (acc[b] - acc[a])
    print(f"{label} ({a} to {b}): added {(acc[b]-acc[a])/1e6:.2f}m accounts and ${(bal[b]-bal[a])/1e9:.1f}bn, about ${m:,.0f} each, "
          f"against ${bal[a]/acc[a]:,.0f} for accounts already there")
    return m
marginal("2024Q1", "2024Q3", "before either wave")
marginal("2024Q3", "2025Q2", "wave 1")
m2 = marginal("2025Q2", "2026Q1", "wave 2")
marginal("2026Q1", "2026Q3", "since")
print("result: in every period the added accounts are smaller than the book, and wave 2's were the LARGEST of the four,"
      " so the balance test doesn't single out SEP/SIMPLE-sized accounts. It neither confirms nor rules out the eligibility story."
      " (Balances also move with markets and cash sorting.)")
print("ICA balances rose in Q3 and Q4 2025 (36.9bn, 41.0bn at quarter end), so there's no sign of accounts leaving the ICA for the DCA either")

# would moving an account from the ICA (LPL earns a % of balance) to the DCA (flat fee) pay LPL?
ica_bps = 352; fee = 19.50 * 12
for b in (3000, 5600, 6650, 10000):
    print(f"  a ${b:,} account earns LPL about ${b*ica_bps/1e4:.0f} a year in the ICA and ${fee:.0f} in the DCA ({fee - b*ica_bps/1e4:+.0f})")
print(f"  break-even balance: ${fee/(ica_bps/1e4):,.0f}. Below it, the DCA pays LPL more")
