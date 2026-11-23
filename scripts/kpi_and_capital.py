# Cash sorting history, the KPI tracker I'll update each quarter, credit and buybacks.
from common import kv, rows

cs = rows("cash_sorting_q3.csv")
print("Q3 client cash as a share of client assets, and purchased money funds:")
prev = None
for r in cs:
    pct = float(r["cash_pct_of_assets"]) * 100
    ch = f" ({pct-prev:+.1f} pt)" if prev is not None else ""
    print(f"  {r['year']}: {pct:.1f}%{ch}, purchased money market funds ${float(r['purchased_mmf_bn']):.1f}bn")
    prev = pct
for r in cs:
    if r["client_accounts_m"]:
        print(f"  {r['year']}: client cash per account ${float(r['client_cash_bn'])/float(r['client_accounts_m'])*1000:,.0f}")

s = kv("sweep.csv")
print("KPI tracker, Q3 2026 starting values:")
print(f"  DCA fee yield {s['q3_dca_yield_bps']:.0f} bps (Q3 2025 {s['q3_2025_dca_yield_bps']:.0f}); fed funds avg {s['fed_funds_eff_q3_avg_bps']:.0f} bps")
print(f"  client cash per account ${56.6/11.9*1000:,.0f}")
print("  recruiting cost (advisor loans / recruited assets): see recruiting_unit_economics.py, four quarters since Commonwealth median 119 bps")
print("  advisor loan book 15.52 bps of client assets (loan_book.py)")
print("  organic growth 4.5% annualized in Q3 (Q3 2026 10-Q)")

c = kv("credit_capital.csv")
print(f"2027 maturities ${c['notes_2027_may_m']+c['notes_2027_nov_m']:.0f}m; new 2029 notes ${c['new_notes_2029_m']:.0f}m at +{c['new_notes_spread_bp']:.0f} bp, yield {c['new_notes_ytm']*100:.3f}%")
sh = c["buyback_2025q1_shares"] + c["buyback_2026q2_shares"] + c["buyback_2026q3_shares"]
cost = c["buyback_2025q1_cost_m"] + c["buyback_2026q2_cost_m"] + c["buyback_2026q3_cost_m"]
avg = cost * 1e6 / sh
print(f"buybacks since 2025: {sh/1e6:.2f}m shares for ${cost:.0f}m, average ${avg:.2f}; at $264.56 that's {264.56/avg-1:+.1%}, ${(264.56-avg)*sh/1e6:.0f}m")

p = kv("street_and_positioning.csv")
strad = (p["apr16_2027_260_call_bid"] + p["apr16_2027_260_call_ask"]) / 2 + (p["apr16_2027_260_put_bid"] + p["apr16_2027_260_put_ask"]) / 2
print(f"April 16 2027 $260 straddle mid ${strad:.2f}, {strad/264.56:.1%} of the price")
print(f"13F: {p['inst_increased_holders']:.0f} holders added {p['inst_increased_shares']/1e6:.2f}m shares, {p['inst_decreased_holders']:.0f} cut {p['inst_decreased_shares']/1e6:.2f}m; "
      f"{p['inst_new_holders']:.0f} new ({p['inst_new_shares']/1e6:.2f}m), {p['inst_soldout_holders']:.0f} sold out ({p['inst_soldout_shares']/1e6:.2f}m)")

# leverage if the full wirehouse reset (case C, $769m pre-tax a year) hit 2027 EBITDA
from three_statement import rows as ts
y = [x for x in ts if x["period"] == "2027E"][0]
net_debt = y["debt_end"] - y["corp_cash_end"]
print(f"2027 net debt / EBITDA: base {net_debt / y['ebitda']:.2f}x; with case C's $769m give-back {net_debt / (y['ebitda'] - 769):.2f}x (covenant max {4.0:.1f}x)")
