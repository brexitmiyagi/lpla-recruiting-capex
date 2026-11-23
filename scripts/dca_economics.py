# The Deposit Cash Account, rebuilt from LPL's own fee schedule.
# LPL gets a flat monthly fee per account, set by the fed funds target (FFT) midpoint (April 2023 booklet).
# Banks pay a percentage of balances; that covers LPL's fee, the administrator and the client's interest.
import csv, os, datetime as dt
from common import rows, DATA

sched = [(float(r["fft_low_bps"]), float(r["fft_high_bps"]), float(r["lpl_monthly_fee_per_account"])) for r in rows("dca_fee_schedule_2023.csv")]
def fee_for(mid):
    for lo, hi, f in sched:
        if lo <= mid < hi: return f
    return sched[-1][2]

def fred(name, col):
    with open(os.path.join(DATA, name)) as f:
        return {r["observation_date"]: float(r[col]) for r in csv.DictReader(f) if r[col] not in ("", ".")}
U, L = fred("fred_DFEDTARU.csv", "DFEDTARU"), fred("fred_DFEDTARL.csv", "DFEDTARL")

def quarter_fee(y, q):
    m0 = (q - 1) * 3 + 1; d = dt.date(y, m0, 1); tot = n = 0
    while d.year == y and m0 <= d.month <= m0 + 2:
        k = str(d)
        if k in U: tot += fee_for(round((U[k] + L[k]) / 2 * 100)); n += 1
        d += dt.timedelta(days=1)
    return tot / n

print("the schedule is close to linear: about $%.1f a year per account for each 1 point of FFT (e.g. $18.25/month at 350-375 bps, $27.00 at 525-550)" % (18.25 * 12 / 3.625))
print(f"December 2025 sheet: ${float([r for r in rows('sweep.csv') if r['item']=='dca_sheet_fee_dec2025'][0]['value']):.2f} a month; the 2023 schedule gives ${fee_for(362.5):.2f} at the Dec 2025 FFT of 3.50-3.75%")
print("quarter: fed funds, DCA fee yield, schedule fee/month, implied accounts, average balance, implied bank payment as % of fed funds")
out = []
for r in rows("sweep_yields_quarterly.csv"):
    if not r["dca_revenue_k"]: continue
    y, q = int(r["quarter"][:4]), int(r["quarter"][-1])
    f = quarter_fee(y, q); rev = float(r["dca_revenue_k"]) * 1000; avg = float(r["dca_avg_bn"]) * 1e9
    accts = rev / 3 / f; bal = avg / accts
    client = 0.0025 if y < 2025 else 0.0030      # complaint: 0.16-0.35% (2022-Aug 2024); Dec 2025 sheet 0.30%
    ff = float(r["fed_funds_avg_bps"])
    bank = float(r["dca_fee_yield_bps"]) + client * 1e4
    out.append((r["quarter"], ff, bank / ff))
    print(f"  {r['quarter']}: funds {ff:.0f} bps, fee yield {r['dca_fee_yield_bps']} bps ({float(r['dca_fee_yield_bps'])/ff:.0%}), ${f:.2f}/month, "
          f"{accts/1e6:.2f}m accounts, ${bal:,.0f} average, banks pay at least {bank/ff:.0%} of funds")
print("so LPL's share of funds rose because the average account shrank under a flat per-account fee, not because the schedule changed")
print("a 25 bp cut takes the fee down one step (about $1.25 a month), about 7% of DCA revenue at today's level")

acc = {r["quarter"]: float(r["total_client_accounts_m"]) for r in rows("total_client_accounts.csv")}
print(f"LPL total client accounts {acc['2024Q1']}m (Q1 2024) -> {acc['2026Q3']}m (Q3 2026), {acc['2026Q3']/acc['2024Q1']-1:+.0%}, with Atria and Commonwealth; implied DCA accounts rose faster")

# consistency check: if the 2023 schedule weren't in force, implied accounts would jump when the fee steps with each Fed move
print("implied account change quarter to quarter, with the fee change in that quarter:")
prev = None
for r in rows("sweep_yields_quarterly.csv"):
    if not r["dca_revenue_k"]: continue
    y, q = int(r["quarter"][:4]), int(r["quarter"][-1])
    f = quarter_fee(y, q); a = float(r["dca_revenue_k"]) * 1000 / 3 / f
    if prev: print(f"  {r['quarter']}: fee {f/prev[1]-1:+.1%}, implied accounts {a/prev[0]-1:+.1%}")
    prev = (a, f)

# falsifiable call for Q4 2026 (reported late January 2027), assuming no change at the December FOMC
f4 = fee_for(387.5)
for bal in (6000, 6300, 6600):
    print(f"Q4 2026 call: fee ${f4:.2f}/month; at a ${bal:,} average balance the DCA fee yield is {f4*12/bal*1e4:.0f} bps, {f4*12/bal*1e4/388:.0%} of 3.88% fed funds")
