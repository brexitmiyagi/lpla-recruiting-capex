# The advisory sweep: how big it is, what a Merrill-style reset costs, and what the price leaves room for.
from common import rows, kv, ttm_tax_rate

s = kv("sweep.csv")
c = kv("company_q3_2026.csv")
cons = {r["ticker"]: r for r in rows("consensus.csv")}
t = ttm_tax_rate()
sh = c["diluted_shares_q3_k"] / 1000
p = float(cons["LPLA"]["price_2026_11_20"])
e27, e28 = float(cons["LPLA"]["eps_2027"]), float(cons["LPLA"]["eps_2028"])
pe = p / e27

print(f"client cash revenue / adjusted pre-tax income, Q3: {s['q3_client_cash_revenue_k']/s['q3_adj_pretax_income_k']:.0%}")
acc = s["q3_dca_revenue_k"] * 1000 / 3 / s["dca_monthly_fee_per_account"]
print(f"implied DCA accounts at $18/month: {acc/1e6:.2f}m, average DCA balance ${s['q3_dca_avg_balance_bn']*1e9/acc:,.0f}")
print(f"LPL DCA fee yield {s['q3_dca_yield_bps']:.0f} bps vs fed funds effective {s['fed_funds_eff_q3_avg_bps']:.0f} bps: room left for the client at most ~{s['fed_funds_eff_q3_avg_bps']-s['q3_dca_yield_bps']:.0f} bps if banks paid the full funds rate")
m = s["merrill_advisory_tier5_apy"]
for label, client in (("0.30% client rate (Dec 2025 sheet)", s["dca_client_rate"]), ("0% client rate (worst case for my math)", 0.0)):
    cost = s["dca_end_balance_bn"] * 1e3 * (m - client)
    print(f"DCA to Merrill's {m:.2%}, {label}: ${cost:.0f}m pre-tax, ${cost*(1-t)/sh:.2f} a share, {cost*(1-t)/sh/e27:.1%} of 2027 EPS")
dca_eps = s["dca_end_balance_bn"] * 1e3 * (m - s["dca_client_rate"]) * (1 - t) / sh
per10 = 10e3 * (m - s["dca_client_rate"]) * (1 - t) / sh
print(f"each $10bn of advisory ICA moved the same way: ${per10:.2f} a share")
small = c["bank_sweep_bn"] * 1e3 * 0.0025 * (1 - t) / sh

print(f"multiple held at today's {pe:.2f}x in every case")
sc = [("A: 25 bp give-back on all bank sweep", e28 - small),
      ("B: DCA paid Merrill's advisory rate", e28 - dca_eps),
      ("C: B plus $10bn of advisory ICA", e28 - dca_eps - per10),
      ("D: C, and 2028 EPS only matches 2027 consensus", e27 - dca_eps - per10)]
for name, eps in sc:
    v = eps * pe
    print(f"{name}: 2028 EPS ${eps:.2f} -> ${v:.2f} ({v/p-1:+.1%})")
vB = (e28 - dca_eps) * pe
print(f"price that gives a 15% return if B happens: ${vB/1.15:.2f}")
print(f"dividend yield {c['dividend_annual']/p:.2%}")

def ch(a, b): return s[b] / s[a] - 1
print(f"week of Jun 22 (MS advisory hike reported): LPLA {ch('lpla_close_2026_06_22','lpla_close_2026_06_26'):+.1%}, MS {ch('ms_close_2026_06_22','ms_close_2026_06_26'):+.1%}, SF {ch('sf_close_2026_06_22','sf_close_2026_06_26'):+.1%}; Jun 26: LPLA {ch('lpla_close_2026_06_25','lpla_close_2026_06_26'):+.1%}, MS {ch('ms_close_2026_06_25','ms_close_2026_06_26'):+.1%}, SF {ch('sf_close_2026_06_25','sf_close_2026_06_26'):+.1%}")
