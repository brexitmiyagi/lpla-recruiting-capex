# Four prices of capital at LPL, side by side.
from common import kv, rows, ttm_tax_rate

c = kv("company_q3_2026.csv")
cw = kv("commonwealth.csv")
t = ttm_tax_rate()
cons = {r["ticker"]: r for r in rows("consensus.csv")}
p = float(cons["LPLA"]["price_2026_11_20"])
e27 = float(cons["LPLA"]["eps_2027"])
print(f"new 2029 notes: {c['new_notes_coupon']:.2%} coupon, {c['new_notes_coupon']*(1-t):.2%} after tax")
print(f"buyback at ${p}: {e27/p:.1%} 2027 earnings yield")
avg = c["ytd_buyback_cost_k"] / c["ytd_buyback_shares_k"]
print(f"2026 YTD buyback average price: ${avg:.2f}, 2027 earnings yield at that price {e27/avg:.1%}")
print(f"Commonwealth all-in ${cw['total_cost_m']:.0f}m / $415m run-rate EBITDA = {cw['total_cost_m']/415:.1f}x, pre-tax yield {415/cw['total_cost_m']:.1%}")
print(f"Commonwealth cash at close / 415 = {cw['cash_funded_at_close_k']/1e3/415:.1f}x")
