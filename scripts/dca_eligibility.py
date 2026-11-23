# Why did implied DCA accounts rise 129% when LPL's total accounts rose 42%?
# 1) the eligibility wording, from LPL's own booklets and SEC filings
# 2) Commonwealth: its clients weren't on LPL's platform until the mid-November 2026 conversion, so none of it is in the DCA through Q3
# 3) which fee schedule was in force (there's a second, lower one in the July 2024 booklet)
# 4) the small-account arithmetic: where the banks' payment stops covering LPL's flat fee
import datetime as dt, io, contextlib
from common import rows
with contextlib.redirect_stdout(io.StringIO()):
    import dca_economics as D
acc0 = {r['quarter']: float(r['total_client_accounts_m']) for r in rows('total_client_accounts.csv')}

print("Commonwealth's advisors converted to LPL's platform over 13-16 November 2026 (InvestmentNews 16 Nov, WealthManagement.com 18 Nov), so none of its accounts were in the DCA through Q3")
print(f"LPL total accounts rose {acc0['2026Q3']/acc0['2024Q1']-1:+.0%}; take out the Q3 2025 step when Commonwealth closed ({acc0['2025Q3']-acc0['2025Q2']:.1f}m, some of it organic) and it's about {(acc0['2026Q3']-(acc0['2025Q3']-acc0['2025Q2']))/acc0['2024Q1']-1:+.0%}, against +129% for implied DCA accounts")
print("eligibility wording over time:")
for r in rows("dca_eligibility_timeline.csv"):
    print(f"  {r['date']} {r['document']}: {r['eligibility_wording']}")
print("so the widening happened between the July 2024 booklet and the October 2025 one; LPL's filings changed between the Q3 2025 10-Q (3 Nov 2025) and the 2025 10-K (23 Feb 2026)")

# implied accounts under the two schedules
s24 = [(float(r["fft_low_bps"]), float(r["fft_high_bps"]), float(r["lpl_monthly_fee_per_account"])) for r in rows("dca_fee_schedule_2024.csv")]
def fee24(mid):
    for lo, hi, f in s24:
        if lo <= mid < hi: return f
    return s24[-1][2]
def qfee(y, q, fn):
    m0 = (q - 1) * 3 + 1; d = dt.date(y, m0, 1); tot = n = 0
    while d.year == y and m0 <= d.month <= m0 + 2:
        k = str(d)
        if k in D.U: tot += fn(round((D.U[k] + D.L[k]) / 2 * 100)); n += 1
        d += dt.timedelta(days=1)
    return tot / n
print("implied accounts (m) under the April 2023 table and under the July 2024 table, with LPL's total accounts:")
acc = {r["quarter"]: float(r["total_client_accounts_m"]) for r in rows("total_client_accounts.csv")}
prev = None
for r in rows("sweep_yields_quarterly.csv"):
    if not r["dca_revenue_k"]: continue
    y, q = int(r["quarter"][:4]), int(r["quarter"][-1])
    rev = float(r["dca_revenue_k"]) * 1000
    a23, a24 = rev / 3 / qfee(y, q, D.fee_for), rev / 3 / qfee(y, q, fee24)
    print(f"  {r['quarter']}: 2023 table {a23/1e6:.2f}m, 2024 table {a24/1e6:.2f}m, LPL total {acc[r['quarter']]:.1f}m")
r3 = {r["quarter"]: r for r in rows("sweep_yields_quarterly.csv")}
a2 = float(r3["2024Q2"]["dca_revenue_k"]) * 1000 / 3 / qfee(2024, 2, D.fee_for)
a3_switch = float(r3["2024Q3"]["dca_revenue_k"]) * 1000 / 3 / qfee(2024, 3, fee24)
print(f"test: if LPL had moved to the 2024 table in Q3 2024, DCA accounts would have jumped {a3_switch/a2-1:+.0%} in a quarter when LPL's total accounts rose {acc['2024Q3']/acc['2024Q2']-1:+.0%} and nothing was acquired. So it wasn't in force then.")
print("and from Q4 2023 to Q2 2024 the funds target sat at 5.25-5.50% and LPL bought nothing, yet the DCA fee yield never fell (379, 378, 399 bps); a switch to the 2024 table would have cut it about 18%")
print(f"the December 2025 rate sheet shows $18.00 at 3.50-3.75%: the 2023 table says ${D.fee_for(362.5):.2f}, the 2024 table ${fee24(362.5):.2f}")
a25q3 = float(r3["2025Q3"]["dca_revenue_k"]) * 1000 / 3 / qfee(2025, 3, fee24); a25q4 = float(r3["2025Q4"]["dca_revenue_k"]) * 1000 / 3 / qfee(2025, 4, D.fee_for)
print(f"if the 2024 table had run from Q4 2024 to Q3 2025 and the old level came back by December, the count would have fallen {a25q4/a25q3-1:+.0%} in Q4 2025, the quarter eligibility widened")
print("the data fit the 2023 table all the way through and don't fit any switch I can build. Both ends of 1.04m -> 2.38m rest on that, and I'm asking LPL to confirm")

# small accounts: the per-account fee against what the banks pay on that account's balance
fee_yr = 19.50 * 12; ff = 3.88
for pct in (1.00, 1.02):
    bank = pct * ff / 100
    print(f"if banks pay {pct:.0%} of fed funds: an account needs ${fee_yr/bank:,.0f} for the bank's payment to cover LPL's ${fee_yr:.0f} a year, ${fee_yr/(bank-0.003):,.0f} once the client's 0.30% is paid")
for bal in (8584, 7936, 6346, 5500, 5000):
    need = (fee_yr / bal + 0.003) / (ff / 100)
    print(f"  average balance ${bal:,}, at today's fee and rates: the banks must pay {need:.0%} of fed funds for LPL's fee and the client's 0.30%")
print("the shortfall clause compares what the banks paid 'for the period' with LPL's fee 'for the same period', so it bites at the program level, not account by account")
print("the posted rate is 0.30% on 'Any value > $0', marked 'Rate net of all fees'. If fees were being taken out of small accounts, their net rate would be below zero, so the sheet says it isn't happening, or at least that LPL doesn't present it that way")
