# How much LPL's client assets move with the S&P 500, from LPL's own "market impact" lines.
from common import rows
# (market impact advisory + brokerage, beginning assets, S&P start, S&P end), from the 10-Qs and FRED
obs = {
    "9M 2026": ((78.7 + 41.2), (1392.7 + 977.9), 6845.50, 7651.54),
    "Q3 2025": ((57.2 + 30.5), (1060.7 + 858.5), 6204.95, 6688.46),
    "Q3 2026": ((-20.5 - 6.7), (1548.4 + 1014.3), 7499.36, 7651.54),
}
for k, (mi, beg, s0, s1) in obs.items():
    a = mi / beg; s = s1 / s0 - 1
    print(f"{k}: client assets from markets {a:+.2%}, S&P 500 {s:+.2%}, ratio {a/s:.2f}")
print("I use 0.5: an S&P drop of 10% takes about 5% off client assets.")
