# What the DCA is worth to LPL per share, and what each possible fix would cost.
# Account balances aren't disclosed, so the per-account caps use a lognormal spread with the implied average
# balance ($6,346, Q3 2026). The two spreads bracket a lot of uncertainty; treat the cap costs as ranges.
import math, random
from common import kv
from eps_model import run

s = kv("sweep.csv"); tax = 0.265
base = run(); shares_27 = sum(x["shares"] for x in base["quarters"][1:5]) / 4
rev_q3 = s["q3_dca_revenue_k"] / 1000
fee_now = 19.50                                   # $/month at a 3.75-4.00% target (2023 schedule)
accts = 2.38e6; avg_bal = 6346.0
dca_rev = accts * fee_now * 12 / 1e6
print(f"DCA revenue: Q3 2026 ${rev_q3:.1f}m (${rev_q3*4:.0f}m a year); at today's target, ${dca_rev:.0f}m a year on 2.38m accounts")
per_sh = dca_rev * (1 - tax) / shares_27
print(f"after tax that's ${per_sh:.2f} a share, {per_sh/base['eps_2027']:.0%} of my 2027 adjusted EPS of ${base['eps_2027']:.2f}")

def cap_cost(cap, sigma, n=200000, seed=7):
    random.seed(seed); mu = math.log(avg_bal) - sigma ** 2 / 2
    lost = 0.0
    for _ in range(n):
        b = random.lognormvariate(mu, sigma)
        lost += max(fee_now * 12 - cap * b, 0)
    return lost / n * accts / 1e6

print("cost of each fix, pre-tax $m a year and $ a share after tax (lognormal sigma 1.0 / 1.5):")
rows = []
for cap in (0.01, 0.02, 0.03):
    lo, hi = cap_cost(cap, 1.0), cap_cost(cap, 1.5)
    print(f"  cap LPL's fee at {cap:.0%} of each account's balance: ${lo:.0f}m-${hi:.0f}m, ${lo*(1-tax)/shares_27:.2f}-${hi*(1-tax)/shares_27:.2f} a share")
for cut in (0.25, 0.50):
    c = dca_rev * cut
    print(f"  cut the fee {cut:.0%} for everyone: ${c:.0f}m, ${c*(1-tax)/shares_27:.2f} a share")
gb = (s["merrill_advisory_tier5_apy"] - s["dca_client_rate"]) * s["dca_end_balance_bn"] * 1000
print(f"  pay DCA clients Merrill's 3.35% (DCA only): ${gb:.0f}m, ${gb*(1-tax)/shares_27:.2f} a share")
