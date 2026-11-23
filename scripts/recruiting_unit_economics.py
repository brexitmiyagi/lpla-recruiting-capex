# Recruiting as capex: what LPL pays up front per recruited dollar and what it earns back.
from common import rows, kv

q = rows("recruiting_quarterly.csv")
c = kv("company_q3_2026.csv")
for r in q:
    ra, lo = float(r["recruited_aum_bn"]), float(r["advisor_loans_cash_out_m"])
    print(f"{r['quarter']}: recruited ${ra:.1f}bn, advisor-loan cash out ${lo:.1f}m, {lo/ra*10:.0f} bps")

last4 = q[-4:]
prior4 = q[-8:-4]
ttm_ra = sum(float(r["recruited_aum_bn"]) for r in last4)
prv_ra = sum(float(r["recruited_aum_bn"]) for r in prior4)
print(f"TTM recruited to Q3 2026 ($bn): {ttm_ra:.1f}   prior TTM: {prv_ra:.1f}")
print(f"prior TTM without Q4 2024 ($bn): {prv_ra-78.7:.1f}")
print(f"trough Q4 2025 -> Q3 2026: {24.1/14.5-1:.0%}")

ttm_loans = sum(float(r["advisor_loans_cash_out_m"]) for r in last4)
bps = ttm_loans / ttm_ra * 10
print(f"TTM advisor-loan cash out ($m): {ttm_loans:.1f}")
print(f"upper-bound cost per recruited dollar (bps): {bps:.0f}")

assets = c["advisory_assets_bn"] + c["brokerage_assets_bn"]
roa = c["q3_gross_profit_m"] * 4 / assets * 10
print(f"gross profit ROA, Q3 annualized on end assets (bps): {roa:.1f}")
print(f"simple payback (years of gross profit): {bps/roa:.1f}")


def irr(up, ann, n):
    lo, hi = 0.0, 1.0
    for _ in range(200):
        m = (lo + hi) / 2
        pv = sum(ann / (1 + m) ** k for k in range(1, n + 1))
        lo, hi = (m, hi) if pv > up else (lo, m)
    return m

# 14 years is the useful life LPL itself put on Commonwealth's advisor relationships
for n in (10, 14):
    print(f"pre-opex IRR over {n} years: {irr(bps, roa, n):.1%}")
af = sum(1 / 1.10 ** k for k in range(1, 15))
print(f"NPV per recruited dollar at 10% over 14y, pre-opex (bps): {roa*af-bps:.0f}")

# price per recruited dollar, before vs now. I leave out 2024Q4 (one big institution,
# cheap per dollar) and 2025Q3 (the Commonwealth close quarter) because neither is a normal quarter.
qq = {r["quarter"]: r for r in q}
def blended(keys):
    lo = sum(float(qq[k]["advisor_loans_cash_out_m"]) for k in keys)
    ra = sum(float(qq[k]["recruited_aum_bn"]) for k in keys)
    return lo / ra * 10
before = blended(["2024Q2", "2024Q3", "2025Q1", "2025Q2"])
after = blended(["2025Q4", "2026Q1", "2026Q2", "2026Q3"])
print(f"bps per recruited dollar, 2024Q2-2025Q2 ex 2024Q4: {before:.0f}; last four quarters: {after:.0f}; change {after/before-1:+.0%}")
print(f"pre-opex IRR over 14 years at the old price: {irr(before, roa, 14):.1%}")
print(f"14-year IRR at {after:.0f} bps after a 26% tax haircut, rough: {irr(after, roa, 14)*0.74:.1%}")

# robust version: medians and ranges, no hand-picked windows except the Commonwealth closing quarter
from statistics import median
pre = ["2024Q2", "2024Q3", "2024Q4", "2025Q1", "2025Q2"]
post = ["2025Q4", "2026Q1", "2026Q2", "2026Q3"]
b = lambda k: float(qq[k]["advisor_loans_cash_out_m"]) / float(qq[k]["recruited_aum_bn"]) * 10
pb, ob = [b(k) for k in pre], [b(k) for k in post]
print(f"before Commonwealth close: {min(pb):.0f}-{max(pb):.0f} bps, median {median(pb):.0f}; since: {min(ob):.0f}-{max(ob):.0f} bps, median {median(ob):.0f}")
ex = (c["q3_gross_profit_m"] - 461.471) * 4 / assets * 10
print(f"gross profit ROA ex client cash: {ex:.1f} bps")
for up in (median(pb), median(ob)):
    print(f"at {up:.0f} bps, 14-year pre-opex IRR with sweep {irr(up, roa, 14):.1%}, without sweep {irr(up, ex, 14):.1%}")
