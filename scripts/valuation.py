# Sweep outcomes off my own EPS, valued two ways that don't use today's price:
# (1) LPLA's own historical forward multiple, (2) a residual-income model on book value.
# Then the probability tree, the market-implied odds, the litigation expected cost and a DCF cross-check.
import math
from eps_model import run
from common import kv

s = kv("sweep.csv")
price, div = 264.56, 1.20
shares_now = 78.31                    # 136,851k issued less 58,540k treasury, Q3 2026 10-Q
book0 = 5812.3                        # stockholders' equity, 30 Sep 2026 ($m)
tax = 0.265
pe_med, pe_lo, pe_hi = 13.56, 11.54, 15.10   # multiple_history.py: forward P/E on realised EPS, 2017Q4-2025Q3
rf, beta, erp = 0.0504, 0.90, 0.05           # 10-year Treasury 19 Nov 2026 (FRED); 5-year weekly beta vs SPY; my equity premium
ke = rf + beta * erp
lit = 3.95                                   # damages.py expected cost, $ a share after tax

dca = s["dca_end_balance_bn"]; adv_share = 1561.0 / 2564.6
pool = dca + (56.6 * adv_share - dca) / 2
def gb(rate): return pool * 1000 * (rate - s["dca_client_rate"])

def fwd_eps(r):  # Q4 2027 to Q3 2028, the four quarters after the 12-month horizon
    return sum(x["eps"] for x in r["quarters"][4:8])

def gaap_ni_by_year(r):
    yrs = {"26": [], "27": [], "28": []}
    for x in r["quarters"]:
        yrs[x["q"][-2:]].append(x["adj_ni"] - (73.0 + 25.0) * (1 - tax))   # intangible amortization $73m a quarter, acquisition costs ~$25m a quarter
    return [sum(v) for v in yrs.values()]

def residual_income(r, k=ke, fade=5, roe_term=0.20, payout=0.85):
    # explicit years from my model (GAAP: adjusted less amortization and acquisition costs), ROE fades to
    # roe_term over `fade` years, then residual income stays flat forever. Book is reduced by $300m a quarter of buybacks and the dividend.
    ni = gaap_ni_by_year(r)
    bv, pv, t = book0, 0.0, 0.0
    for n, dur in zip(ni, [0.25, 1.0, 1.0]):
        t += dur
        pv += (n - k * dur * bv) / (1 + k) ** t
        roe_last = n / dur / bv
        bv += n - (300.0 * 4 * dur + div * shares_now * dur)
    for y in range(1, fade + 1):
        t += 1
        roe = roe_last + (roe_term - roe_last) * y / fade
        n = roe * bv
        pv += (n - k * bv) / (1 + k) ** t
        bv += n * (1 - payout)
    pv += (roe_term - k) * bv / k / (1 + k) ** t
    return ((book0 + pv) / shares_now) * (1 + k) - div      # value 12 months out

base = run()
print(f"cost of equity {ke:.2%} (10-year {rf:.2%} + beta {beta} x {erp:.0%})")
print(f"my 2027 adj EPS ${base['eps_2027']:.2f}, 2028 ${base['eps_2028']:.2f}; forward EPS a year out (Q4 27-Q3 28) ${fwd_eps(base):.2f}")
print(f"today's price on my next four quarters (Q4 26-Q3 27): {price/sum(x['eps'] for x in base['quarters'][0:4]):.1f}x, against LPLA's history median {pe_med}x (25th-75th pct {pe_lo}x-{pe_hi}x)")
print(f"book value ${book0/shares_now:.2f} a share")

cases = [("A", "no change, or a token one", dict(), 0.25),
         ("B", "LPL moves to Osaic's level (0.58%)", dict(sweep_giveback_pretax_yr=gb(0.0058)), 0.35),
         ("C2", "wirehouse level (3.35%), half won back in platform fees", dict(sweep_giveback_pretax_yr=gb(s["merrill_advisory_tier5_apy"]), platform_offset_share=0.5), 0.25),
         ("C", "wirehouse level, nothing offset", dict(sweep_giveback_pretax_yr=gb(s["merrill_advisory_tier5_apy"])), 0.15)]
ev = {"lo": 0, "med": 0}; vals = {}
for k, name, a, w in cases:
    r = run(a); f = fwd_eps(r)
    vlo, vmed = f * pe_lo - lit, f * pe_med - lit
    vals[k] = (vlo, vmed, f)
    ev["lo"] += w * vlo; ev["med"] += w * vmed
    print(f"{k} ({w:.0%}) {name}: give-back ${a.get('sweep_giveback_pretax_yr', 0):.0f}m; forward EPS ${f:.2f}; "
          f"at {pe_lo}x ${vlo:.2f} ({vlo/price-1:+.1%}); at {pe_med}x ${vmed:.2f} ({vmed/price-1:+.1%})")
print(f"probability-weighted value, no rerating ({pe_lo}x, LPLA's 25th percentile, about where it trades now): ${ev['lo']:.2f} ({ev['lo']/price-1:+.1%}); with the dividend {(ev['lo']+div)/price-1:+.1%}")
print(f"probability-weighted value if the multiple goes back to its median ({pe_med}x): ${ev['med']:.2f} ({ev['med']/price-1:+.1%})")
for lab, ws in (("weights leaning on the peer base rates (no bank, no move: 35/40/15/10)", (0.35, 0.40, 0.15, 0.10)), ("bearish weights (10/30/30/30)", (0.10, 0.30, 0.30, 0.30))):
    e = sum(w * vals[k][0] for (k, _, _, _), w in zip(cases, ws))
    print(f"  {lab}: ${e:.2f} ({e/price-1:+.1%})")
print(f"buy level for a 15% total return on the no-rerating basis: ${(ev['lo']+div)/1.15:.2f}")
rest = {k: w for k, _, _, w in cases if k != "C"}; tot = sum(rest.values())
v_rest = sum(vals[k][0] * w / tot for k, w in rest.items())
print(f"odds on C that make today's price fair (no-rerating basis): {(v_rest - price) / (v_rest - vals['C'][0]):.0%}")
gap = vals["A"][0] - vals["C"][0]
print(f"A minus C on that basis: ${gap:.2f} a share. The 2026 sweep-event abnormal returns add up to $81.27, but the Oct 28 move mixed in recruiting and Commonwealth news")
rD = run(dict(sweep_giveback_pretax_yr=gb(s["merrill_advisory_tier5_apy"]), initial_asset_shock=-0.045 - 0.10))
print(f"stress D (C plus another S&P -20%): ${fwd_eps(rD)*pe_lo - lit:.2f}")
print("residual income cross-check (cost of equity as above), probability-weighted, by long-run ROE:")
for rt in (0.20, 0.25, 0.30):
    e = sum(w * (residual_income(run(a), roe_term=rt) - lit) for _, _, a, w in cases)
    print(f"  ROE settling at {rt:.0%}: ${e:.2f} ({e/price-1:+.1%})")
b0 = run()
lo_, hi_ = 0.10, 0.40
for _ in range(60):
    m = (lo_ + hi_) / 2
    lo_, hi_ = (m, hi_) if residual_income(b0, roe_term=m) < price * (1 + ke) - div else (lo_, m)
print(f"  long-run ROE today's price implies (no sweep change): {m:.1%}; GAAP ROE on my 2028 numbers is {gaap_ni_by_year(b0)[2]/6624:.0%}")
print("ICA fixed book: Q3 ICA yield 352 bps = 65% fixed + 35% floating; if floating earns what the DCA does (94% of 367 = 345 bps), fixed runs at about 356 bps, so the fixed book is priced close to today's rates and roll-offs move little either way; the 2-year at 4.76% (FRED, 19 Nov) says new fixed contracts would price higher, not lower")
print("cash sorting: base has cash share falling 0.1 pt in 2027 and 0.05 pt in 2028")
r0 = run(dict(cash_drift_yr=(0.0, 0.0, 0.0))); print(f"  if it stops falling now: 2027 ${r0['eps_2027']:.2f}, 2028 ${r0['eps_2028']:.2f}")
for d, lab in ((-0.00025, "a further 0.1 pt a year"), (-0.0005, "a further 0.2 pt a year")):
    r = run(dict(cash_share_drift_q=d)); print(f"  {lab}: 2028 EPS ${r['eps_2028']:.2f} ({r['eps_2028']/base['eps_2028']-1:+.1%})")

cash = base["cash_eps_2027"]; core = base["eps_2027"] - cash
print(f"2027 split: client cash after tax ${cash:.2f}, everything else ${core:.2f}")
for cpe in (12, 15, 18):
    resid = price - core * cpe
    g = 0.10 - cash / resid if resid > 0 else float("nan")
    print(f"  core at {cpe}x: price implies sweep earnings changing {g:+.1%} a year forever (10% discount rate)")

try:
    import three_statement as ts
    fcf28 = [x for x in ts.rows if x["period"] == "2028E"][0]["fcf"]
    def dcf(g1, g2, r):
        v, f = 0, fcf28
        for t in range(1, 6): f *= 1 + g1; v += f / (1 + r) ** t
        v += f * (1 + g2) / (r - g2) / (1 + r) ** 5
        return (v / (1 + r) ** 1.2 - (7970 - 600)) / shares_now
    for g1, g2, r in ((0.06, 0.03, 0.10), (0.04, 0.02, 0.10), (0.06, 0.03, 0.09)):
        print(f"  DCF: FCF 2028 ${fcf28:.0f}m growing {g1:.0%} to 2033 then {g2:.0%}, at {r:.0%}: ${dcf(g1, g2, r):.0f} a share")
except Exception as e:
    print("DCF skipped:", e)
print(f"rating rule: BUY needs a weighted total return of 15% and case C no worse than -10%; case C here {vals['C'][0]/price-1:+.1%}")
