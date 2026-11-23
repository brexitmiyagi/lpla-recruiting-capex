# What the market took off LPL on Oct 28, next to what Commonwealth cost.
import os
from common import rows, kv, shares_out_m

HERE = os.path.dirname(os.path.abspath(__file__))
px = {r["date"]: r for r in rows("prices.csv")}
cw = kv("commonwealth.csv")

pre = float(px["2026-10-27"]["lpla_close"])
post = float(px["2026-10-28"]["lpla_close"])
now = float(px["2026-11-20"]["lpla_close"])
sh = shares_out_m()

print(f"shares outstanding at Sep 30 (m): {sh:.2f}")
print(f"Oct 28 move: {post/pre-1:.1%}  (${pre:.2f} -> ${post:.2f})")
print(f"S&P 500 same day: {float(px['2026-10-28']['sp500_close'])/float(px['2026-10-27']['sp500_close'])-1:.2%}")
lost = (pre - post) * sh / 1000
print(f"market value lost Oct 28 ($bn): {lost:.2f}")
print(f"lost since Oct 27 close to Nov 20 ($bn): {(pre-now)*sh/1000:.2f}")
print(f"Commonwealth cash funded at close ($bn): {cw['cash_funded_at_close_k']/1e6:.2f}")
print(f"Commonwealth all-in cost per deal deck ($bn): {cw['total_cost_m']/1000:.2f}")
print(f"Oct 28 loss / cash at close: {lost/(cw['cash_funded_at_close_k']/1e6):.2f}x")
# the only hard number LPL changed on Commonwealth: run-rate EBITDA 435 -> 415
cut = 435 - 415
print(f"run-rate EBITDA cut ($m): {cut}, at LPL's own ~8.0x deal multiple ($bn): {cut*8/1000:.2f}")
print(f"share of Oct 28 loss explained by the EBITDA cut: {cut*8/1000/lost:.1%}")
print(f"YTD from Dec 31 2025 close: {now/float(px['2025-12-31']['lpla_close'])-1:.1%}")
print(f"from Feb 9 closing high: {now/float(px['2026-02-09']['lpla_close'])-1:.1%}")
sp = {k: float(v['sp500_close']) for k, v in px.items() if v['sp500_close']}
print(f"S&P 500 Dec 31 2024 -> Sep 30 2026: {sp['2026-09-30']/sp['2024-12-31']-1:.1%}")
