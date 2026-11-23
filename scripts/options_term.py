# Implied volatility by expiry from the Nasdaq option chain (composite quotes, 20 Nov 2026 close),
# to see whether the market prices a Q4-results jump and whether downside puts are rich.
import os, json, math, datetime as dt
from statistics import median
HERE = os.path.dirname(os.path.abspath(__file__))
S, r, q, t0 = 264.56, 0.0388, 0.0045, dt.date(2026, 11, 20)
N = lambda x: 0.5 * (1 + math.erf(x / math.sqrt(2)))

def bs(cp, K, T, s):
    d1 = (math.log(S / K) + (r - q + s * s / 2) * T) / (s * math.sqrt(T)); d2 = d1 - s * math.sqrt(T)
    return S * math.exp(-q * T) * N(d1) - K * math.exp(-r * T) * N(d2) if cp == "c" else K * math.exp(-r * T) * N(-d2) - S * math.exp(-q * T) * N(-d1)

def iv(cp, K, T, p):
    lo, hi = 0.01, 3.0
    if p <= bs(cp, K, T, lo): return None
    for _ in range(100):
        m = (lo + hi) / 2
        lo, hi = (lo, m) if bs(cp, K, T, m) > p else (m, hi)
    return m

rows = json.load(open(os.path.join(HERE, "..", "data", "nasdaq", "opt.json")))["data"]["table"]["rows"]
exp, vols = None, {}
for o in rows:
    if o.get("expirygroup"): exp = o["expirygroup"]; continue
    T = (dt.datetime.strptime(exp, "%B %d, %Y").date() - t0).days / 365
    for cp, b, a in (("c", o["c_Bid"], o["c_Ask"]), ("p", o["p_Bid"], o["p_Ask"])):
        try: b, a = float(b), float(a)
        except ValueError: continue
        if b <= 0 or (a - b) / ((a + b) / 2) > 0.5: continue   # skip one-sided or very wide quotes
        v = iv(cp, float(o["strike"]), T, (a + b) / 2)
        if v: vols.setdefault(exp, []).append((float(o["strike"]), cp, v, T))
atm = {}
for e, v in vols.items():
    near = [x[2] for x in v if 245 <= x[0] <= 285]
    if near: atm[e] = (median(near), v[0][3]); print(f"{e}: at-the-money implied vol {median(near):.1%}")
(sj, tj), (sa, ta) = atm["January 15, 2027"], atm["April 16, 2027"]
ev = sa ** 2 * ta - sj ** 2 * tj - sj ** 2 * (ta - tj)
print(f"implied Q4-results move (April variance less January's run rate): {math.sqrt(max(ev, 0)):.1%}")
jan = {(k, cp): v for k, cp, v, _ in vols["January 15, 2027"]}
print(f"January skew: $230 put {jan[(230.0,'p')]:.1%}, at the money {sj:.1%}, $290 call {jan[(290.0,'c')]:.1%}")
