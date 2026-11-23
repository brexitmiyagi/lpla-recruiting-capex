# 12-month target: today's multiple on 2028 consensus, after a sweep give-back stress.
from statistics import median
from common import rows, kv, shares_out_m, ttm_tax_rate

cons = {r["ticker"]: r for r in rows("consensus.csv")}
c = kv("company_q3_2026.csv")
L = cons["LPLA"]
p = float(L["price_2026_11_20"])
e26, e27, e28 = (float(L[k]) for k in ("eps_2026", "eps_2027", "eps_2028"))
t = ttm_tax_rate()
haircut = c["bank_sweep_bn"] * 1e3 * 0.0025 * (1 - t) / (c["diluted_shares_q3_k"] / 1000)

pe27 = p / e27
print(f"LPLA P/E: {p/e26:.2f}x 2026, {pe27:.2f}x 2027; EPS growth 26->27 {e27/e26-1:.0%}, 27->28 {e28/e27-1:.0%}")
peers = {}
for k in ("SCHW", "RJF", "AMP", "SF"):
    r = cons[k]
    peers[k] = float(r["price_2026_11_20"]) / float(r["eps_2027"])
    g = float(r["eps_2028"]) / float(r["eps_2027"]) - 1
    print(f"{k}: {peers[k]:.2f}x next-year EPS, next growth {g:.0%}")
pm = median(peers.values())
print(f"peer median: {pm:.2f}x")

e28h, e27h = e28 - haircut, e27 - haircut
base = pe27 * e28h
bear = 8.0 * e27h
bull = pm * e28h
print(f"sweep haircut per share: ${haircut:.2f}")
print(f"bear 8.0x x ${e27h:.2f} = ${bear:.2f} ({bear/p-1:+.1%})")
print(f"base {pe27:.2f}x x ${e28h:.2f} = ${base:.2f} ({base/p-1:+.1%})")
print(f"bull {pm:.2f}x x ${e28h:.2f} = ${bull:.2f} ({bull/p-1:+.1%})")
print(f"dividend yield: {c['dividend_annual']/p:.2%}")

rf = 5.04
coe = rf + 5.0
print(f"no-growth value of 2027 EPS at {coe:.2f}% cost of equity: ${e27/(coe/100):.2f}")
sh = shares_out_m()
mcap = p * sh / 1000
ev = mcap + c["total_debt_m"] / 1000 - c["corporate_cash_m"] / 1000
print(f"market cap ${mcap:.2f}bn, EV ${ev:.2f}bn, EV/TTM EBITDA {ev/(c['ttm_ebitda_k']/1e6):.2f}x")
gaap_eps = c["ttm_net_income_k"] / c["diluted_shares_q3_k"]
print(f"TTM GAAP EPS ${gaap_eps:.2f}, GAAP P/E {p/gaap_eps:.1f}x")
base50 = pe27 * (e28 - 2 * haircut)
print(f"base with a 50 bp give-back instead: ${base50:.2f}")
