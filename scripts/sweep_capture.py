# How much of the fed funds rate LPL keeps on each sweep program, quarter by quarter, and what the
# monthly cash numbers say about the drain.
from common import rows

print("quarter: fed funds avg, ICA fee yield (share of funds), DCA fee yield (share of funds)")
for r in rows("sweep_yields_quarterly.csv"):
    ff, ica, dca = float(r["fed_funds_avg_bps"]), float(r["ica_fee_yield_bps"]), float(r["dca_fee_yield_bps"])
    if ff < 50:
        print(f"  {r['quarter']}: funds {ff:.0f} bps, ICA {ica:.0f}, DCA {dca:.0f} (rates near zero, ratio meaningless)")
    else:
        print(f"  {r['quarter']}: funds {ff:.0f} bps, ICA {ica:.0f} ({ica/ff:.0%}), DCA {dca:.0f} ({dca/ff:.0%})")

q = {r["quarter"]: r for r in rows("sweep_yields_quarterly.csv")}
for a, b in (("2025Q1", "2025Q3"),):
    print(f"{a} to {b}: funds {q[a]['fed_funds_avg_bps']} -> {q[b]['fed_funds_avg_bps']} bps, DCA fee yield {q[a]['dca_fee_yield_bps']} -> {q[b]['dca_fee_yield_bps']} bps")
print("2024Q3 to 2026Q3: funds 527 -> 367 bps (-160), DCA fee yield 400 -> 346 bps (-54)")

# DCA economics: a flat monthly fee per account, indexed to the fed funds target (ADV program brochure, Oct 2026)
q3_rev_k, fee = 131642, 18.00
accts = q3_rev_k * 1000 / 3 / fee
print(f"implied DCA accounts at $18 a month: {accts/1e6:.2f}m; average balance ${15.1e9/accts:,.0f}")
print(f"a $5,000 DCA balance pays ${fee*12:.0f} a year in fee, {fee*12/5000:.1%} of the balance")

m = rows("monthly_cash_2025_2026.csv")
print("monthly client cash as % of client assets:")
for r in m:
    print(f"  {r['month']}: {float(r['total_client_cash_bn'])/float(r['total_client_assets_bn']):.2%}")
o25, o26 = m[0], m[-1]
print(f"Oct 2025 -> Oct 2026: {float(o25['total_client_cash_bn'])/float(o25['total_client_assets_bn']):.2%} -> {float(o26['total_client_cash_bn'])/float(o26['total_client_assets_bn']):.2%}")
print("money market sweep fell from $4.1bn to $0.9bn, partly a reclassification: $1.6bn moved to purchased money funds in Nov 2025 and $0.5bn in Feb 2026 (LPL footnote)")
print("what LPL earns on purchased money funds: 6 to 9 bps a quarter in 2021-22 and 20 bps in Q3 2020, the last periods it disclosed (Q3 2021-Q1 2022 releases). I use 10 bps.")
