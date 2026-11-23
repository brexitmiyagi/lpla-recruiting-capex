# Q4 2026 DCA revenue, estimated from LPL's monthly reports before the quarter is reported.
# Revenue = accounts x fee x months. Accounts = DCA balance / average balance per account.
# The average account has shrunk about 1.5% a quarter (Q1-Q3 2026: $6,548, $6,445, $6,346), so I carry that on.
# Month-end balances run a little above the quarter's daily average LPL reports; I scale them by the 2026 ratio.
# Fill in November and December from LPL's monthly reports (November's is due mid-December) and rerun.
import io, contextlib
from common import rows
with contextlib.redirect_stdout(io.StringIO()):
    import dca_economics as D

MONTH_END_DCA_BN = {"2026-10": 15.6, "2026-11": None, "2026-12": None}   # None = not out yet; carried at the last known month
FEE = {"hold": (19.50, 19.50, 19.50), "hike 9 Dec": (19.50, 19.50, 19.50 * 9 / 31 + 20.75 * 22 / 31)}  # a hike takes effect 10 Dec

q = {r["quarter"]: r for r in rows("sweep_yields_quarterly.csv")}
m = {r["month"]: float(r["dca_bn"]) for r in rows("monthly_cash_2025_2026.csv")}
ratios = []
for qq, ms in (("2026Q1", ("2026-01", "2026-02", "2026-03")), ("2026Q2", ("2026-04", "2026-05", "2026-06")), ("2026Q3", ("2026-07", "2026-08", "2026-09"))):
    ratios.append(float(q[qq]["dca_avg_bn"]) / (sum(m[x] for x in ms) / 3))
ratio = sum(ratios) / 3
print("reported quarterly average / mean of month-ends: " + ", ".join(f"{x:.3f}" for x in ratios) + f"; I use {ratio:.3f}")

avg_q3 = float(q["2026Q3"]["dca_avg_bn"]) * 1e9 / (float(q["2026Q3"]["dca_revenue_k"]) * 1000 / 3 / D.quarter_fee(2026, 3))
avg_q4 = avg_q3 * (1 - 0.015)
last = None; bals = []
for k, v in MONTH_END_DCA_BN.items():
    last = v if v is not None else last; bals.append(last)
known = sum(v is not None for v in MONTH_END_DCA_BN.values())
print(f"Q3 average account ${avg_q3:,.0f}; Q4 assumed ${avg_q4:,.0f}; months known: {known} of 3")
for lab, fees in FEE.items():
    rev = sum(b * ratio * 1e9 / avg_q4 * f for b, f in zip(bals, fees))
    avg_bal = sum(bals) / 3 * ratio * 1e9
    print(f"  {lab}: Q4 DCA revenue ${rev/1e6:.1f}m (range ${rev/1e6*0.97:.0f}m-${rev/1e6*1.03:.0f}m), fee yield {rev*4/avg_bal*1e4:.0f} bps; Q3 was ${float(q['2026Q3']['dca_revenue_k'])/1000:.1f}m")
print("not in this: Commonwealth's accounts, which moved onto LPL's platform in mid-November. If its advisory IRA cash lands in the DCA, November's balance will jump.")
print("the November balance then counts at the same average account size; if Commonwealth's accounts are bigger than LPL's, I overstate the account count and revenue")

# backtest: the same method on Q2 and Q3 2026, using only what was known before each quarter was reported
def back(qq, ms, prev, fees, rat):
    avg = float(q[prev]["dca_avg_bn"]) * 1e9 / (float(q[prev]["dca_revenue_k"]) * 1000 / 3 / D.quarter_fee(int(prev[:4]), int(prev[-1]))) * (1 - 0.015)
    est = sum(m[x] * rat * 1e9 / avg * f for x, f in zip(ms, fees))
    act = float(q[qq]["dca_revenue_k"]) * 1000
    print(f"  backtest {qq}: estimate ${est/1e6:.1f}m, reported ${act/1e6:.1f}m ({est/act-1:+.1%})")
print("backtest with all three month-ends known:")
back("2026Q2", ("2026-04", "2026-05", "2026-06"), "2026Q1", (18.25, 18.25, 18.25), ratios[0])
back("2026Q3", ("2026-07", "2026-08", "2026-09"), "2026Q2", (18.25, 18.25, 18.25 * 16 / 30 + 19.50 * 14 / 30), (ratios[0] + ratios[1]) / 2)
