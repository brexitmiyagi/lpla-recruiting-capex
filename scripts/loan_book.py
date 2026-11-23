# LPL's advisor-loan book against client assets, and what TA is as a share of a year's revenue.
from common import rows

for r in rows("advisor_loan_book.csv"):
    lo = float(r["advisor_loans_net_m"])
    per_adv = lo * 1e6 / float(r["advisors"]) / 1000
    line = f"{r['date']}: loans ${lo:,.1f}m, per advisor ${per_adv:,.0f}k"
    if r["client_assets_bn"]:
        line += f", {lo/float(r['client_assets_bn'])*10:.1f} bps of client assets"
    print(line)
b = {r["date"]: r for r in rows("advisor_loan_book.csv")}
print(f"precise: end-2025 {3681.512/2370.5*10:.2f} bps, Sep 2026 {3979.817/2564.6*10:.2f} bps")
print(f"growth 2018 -> Q3 2026: {float(b['2026-09-30']['advisor_loans_net_m'])/float(b['2018-12-31']['advisor_loans_net_m']):.1f}x")
print(f"loan book / equity at Sep 30 2026 ($5,812.3m): {3979.8/5812.3:.0%}")
for r in rows("advisor_loan_credit.csv"):
    print(f"{r['year']}: net charge-offs ${float(r['net_chargeoffs_k'])/1e3:.1f}m, allowance ${float(r['allowance_end_k'])/1e3:.1f}m")

s = {r["item"]: float(r["value"]) for r in rows("street_and_positioning.csv")}
y26 = s["fees_commissions_per_advisor_k_q3_2026"] / (s["avg_assets_per_advisor_m_q3_2026"] * 1000) * 1e4
y25 = s["fees_commissions_per_advisor_k_q3_2025"] / (s["avg_assets_per_advisor_m_q3_2025"] * 1000) * 1e4
print(f"advisor revenue yield on assets: {y25:.1f} bps (Q3 25), {y26:.1f} bps (Q3 26)")
print(f"TA as % of a year's advisor revenue: 88 bps -> {88/y25:.0%}, 117 bps -> {117/y26:.0%}")
for k, c in (("LPL 2029 notes", 0.0585), ("Osaic secured", s["osaic_secured_notes_coupon"]), ("Osaic unsecured", s["osaic_unsecured_notes_coupon"])):
    carry = 117 * c
    print(f"carry on 117 bps of TA at {k} {c:.2%}: {carry:.1f} bps a year, {carry/25.9:.0%} of the 25.9 bps gross ROA")
print(f"short interest % of shares: {s['short_interest_shares_2026_10_30']/78.311e6:.1%}")
print(f"my $310 vs lowest Street target ${s['low_price_target']:.0f} and average ${s['avg_price_target']:.2f}")
