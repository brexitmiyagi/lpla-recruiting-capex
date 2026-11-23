# LPLA's abnormal return around each sweep event, against the S&P (SPY) with a market model
# fitted on the 250 trading days ending 10 days before the event.
import datetime as dt, numpy as np
from common import rows
from nasdaq_prices import closes

P = {s: closes(s) for s in ["LPLA", "SPY", "SCHW", "RJF", "AMP"]}
dates = sorted(set.intersection(*[set(v) for v in P.values()]))
idx = {d: i for i, d in enumerate(dates)}

def on_or_before(d):
    while d not in idx:
        d -= dt.timedelta(days=1)
    return d

def ret(s, a, b): return P[s][b] / P[s][a] - 1

results = []
for e in rows("sweep_events.csv"):
    d0 = on_or_before(dt.date.fromisoformat(e["start_close"])); d1 = on_or_before(dt.date.fromisoformat(e["end_close"]))
    i0 = idx[d0]; est = dates[max(0, i0 - 260):i0 - 10]
    l = np.array([P["LPLA"][est[k + 1]] / P["LPLA"][est[k]] - 1 for k in range(len(est) - 1)])
    m = np.array([P["SPY"][est[k + 1]] / P["SPY"][est[k]] - 1 for k in range(len(est) - 1)])
    beta = np.cov(l, m)[0, 1] / m.var(ddof=1); alpha = l.mean() - beta * m.mean()
    n = idx[d1] - i0
    ar = ret("LPLA", d0, d1) - (alpha * n + beta * ret("SPY", d0, d1))
    peers = np.mean([ret(s, d0, d1) for s in ("SCHW", "RJF", "AMP")])
    usd = ar * P["LPLA"][d0]
    results.append((e["event"], d0, d1, ar, usd))
    print(f"{e['event']}: {d0} to {d1}, LPLA {ret('LPLA', d0, d1):+.1%}, S&P {ret('SPY', d0, d1):+.1%}, abnormal {ar:+.1%} (${usd:+.2f} a share); SCHW/RJF/AMP {peers:+.1%}")

d_jul24, d_jan25 = on_or_before(dt.date(2024, 7, 19)), on_or_before(dt.date(2025, 1, 21))
print(f"after the July 2024 drop LPLA went from ${P['LPLA'][d_jul24]:.2f} (19 Jul 2024) to ${P['LPLA'][d_jan25]:.2f} (21 Jan 2025): {ret('LPLA', d_jul24, d_jan25):+.1%}, S&P {ret('SPY', d_jul24, d_jan25):+.1%}")
since = [r for r in results if r[1] >= dt.date(2026, 1, 1)]
print(f"2026 sweep events, abnormal $ a share added up: ${sum(r[4] for r in since):+.2f}")
