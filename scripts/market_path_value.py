# The valuation on the Fed path fed funds futures price (fed_path.py), with the discount rate and the multiple
# moved with it, plus two sensitivities: the same path without that link, and the Fed on hold.
#
# The link: higher policy rates raise LPL's sweep earnings, but they should also raise what investors demand.
# I move the cost of equity up by beta x the 2027 average rise in fed funds, and let the multiple fall to match,
# treating the forward earnings yield as cost of equity less growth (so growth is held where 11.54x implies it is).
# It's conservative: the 10-year at 5.04% already prices much of this path, so some of it is counted twice.
import io, contextlib
from eps_model import run
import fed_path as F
with contextlib.redirect_stdout(io.StringIO()):
    import valuation as V
    import whats_priced as W

price, div, lit = V.price, V.div, V.lit
FUT = F.futures_path()
d27 = sum(FUT[1:5]) / 4 / 1e4

def setup(path, link):
    if path is None or not link:
        return V.ke, V.pe_lo, V.pe_med
    dk = V.beta * d27
    return V.ke + dk, 1 / (1 / V.pe_lo + dk), 1 / (1 / V.pe_med + dk)

def cases(path):
    # in the wirehouse cases the client rate follows the Fed too: Merrill's 3.35% is 86% of 3.88% funds,
    # so I move it by 86% of the average change over the valuation year (Q4 27-Q3 28)
    d = 0 if path is None else sum(path[4:8]) / 4 / 1e4
    wire = V.s["merrill_advisory_tier5_apy"] + 0.86 * d
    extra = {} if path is None else dict(fed_path_bp=path)
    return [("A", dict(extra), 0.25),
            ("B", dict(extra, sweep_giveback_pretax_yr=V.gb(0.0058)), 0.35),
            ("C2", dict(extra, sweep_giveback_pretax_yr=V.gb(wire), platform_offset_share=0.5), 0.25),
            ("C", dict(extra, sweep_giveback_pretax_yr=V.gb(wire)), 0.15)]

def report(path, link, label, quiet=False):
    ke, pe, pem = setup(path, link)
    vals = {k: V.fwd_eps(run(a)) * pe - lit for k, a, w in cases(path)}
    ev = sum(w * vals[k] for k, a, w in cases(path))
    evm = sum(w * (V.fwd_eps(run(a)) * pem - lit) for k, a, w in cases(path))
    extra = {} if path is None else dict(fed_path_bp=path)
    r = run(extra)
    def value_today(g, p):
        return (V.fwd_eps(run(dict(extra, sweep_giveback_pretax_yr=g))) * p - lit + div) / (1 + ke)
    priced = {}
    for p in (pe, pem):
        lo, hi = 0.0, W.dca_fee_rev * 4
        for _ in range(60):
            m = (lo + hi) / 2
            lo, hi = (m, hi) if value_today(m, p) > price else (lo, m)
        priced[p] = m
    if not quiet:
        print(f"{label}: cost of equity {ke:.2%}, multiple {pe:.2f}x (median {pem:.2f}x); 2027 EPS ${r['eps_2027']:.2f}, 2028 ${r['eps_2028']:.2f}")
        print("  cases: " + ", ".join(f"{k} ${v:.2f} ({v/price-1:+.1%})" for k, v in vals.items()))
        print(f"  weighted ${ev:.2f} ({ev/price-1:+.1%}, {(ev+div)/price-1:+.1%} with the dividend); at the median multiple ${evm:.2f}; buy below ${(ev+div)/1.15:.2f}")
        rule = "BUY" if (ev + div) / price - 1 >= 0.15 and vals["C"] / price - 1 >= -0.10 else ("SELL" if (ev + div) / price - 1 < -0.05 else "HOLD")
        print(f"  rating rule: {rule}")
        print(f"  what's priced at {pe:.2f}x: give-back ${priced[pe]:.0f}m a year pre-tax, {priced[pe]/W.dca_fee_rev:.0%} of today's DCA fee; at {pem:.2f}x {priced[pem]/W.dca_fee_rev:.0%}")
    return ev, vals, priced[pe]

print(f"futures path (bp vs 3.88%): {FUT}; 2027 average {d27*1e4:+.0f} bp")
base = report(FUT, True, "BASE: futures path, discount rate and multiple moved with it")
nolink = report(FUT, False, "sensitivity: futures path, multiple and discount rate held")
flat = report(None, False, "sensitivity: Fed on hold")
bills = report(F.path(20), True, "cross-check: bill-curve path (20 bp spread), linked")
print(f"the futures path adds ${base[0]-flat[0]:+.2f} a share to the weighted value after the multiple hit, ${nolink[0]-flat[0]:+.2f} before it")

ke, pe, _ = setup(FUT, True)
print(f"chart: value today at {pe:.2f}x on the futures path vs {V.pe_lo}x with the Fed on hold, by share of today's DCA fee given up")
for pct in (0, 25, 50, 75, 100):
    g = W.dca_fee_rev * pct / 100
    v_f = (V.fwd_eps(run(dict(fed_path_bp=FUT, sweep_giveback_pretax_yr=g))) * pe - lit + div) / (1 + ke)
    v_h = (V.fwd_eps(run(dict(sweep_giveback_pretax_yr=g))) * V.pe_lo - lit + div) / (1 + V.ke)
    print(f"  {pct}%: ${v_h:.2f} / ${v_f:.2f}")

# risk table on the base (futures path, linked multiple): change in the probability-weighted 12-month value
def weighted_base(extra=None, shift_bp=0, lit_=None):
    p = [x + shift_bp for x in FUT]
    dk = V.beta * (sum(p[1:5]) / 4 / 1e4)
    pe = 1 / (1 / V.pe_lo + dk)
    l = lit if lit_ is None else lit_
    tot = 0
    for k, a, w in cases(p):
        a = dict(a, fed_path_bp=p, **(extra or {}))
        if extra and "sweep_giveback_extra" in extra:
            a = dict(a); g = a.pop("sweep_giveback_extra"); a["sweep_giveback_pretax_yr"] = a.get("sweep_giveback_pretax_yr", 0) + g
        tot += w * (V.fwd_eps(run(a)) * pe - l)
    return tot
b0 = weighted_base()
print(f"risk table on the base, weighted ${b0:.2f}:")
rows = [("S&P 500 -10% (client assets -5%)", dict(initial_asset_shock=-0.045 - 0.05), 0),
        ("S&P 500 +10%", dict(initial_asset_shock=-0.045 + 0.05), 0),
        ("Fed 25 bp below the futures path, all quarters", None, -25),
        ("Fed 25 bp above the futures path", None, 25),
        ("cash drain at twice my pace", dict(cash_drift_yr=(0.0, -0.002, -0.001)), 0),
        ("DCA fee cut 25% on top of each case", dict(sweep_giveback_extra=W.dca_fee_rev * 0.25), 0),
        ("DCA fee cut 50% on top of each case", dict(sweep_giveback_extra=W.dca_fee_rev * 0.50), 0)]
for lab, ex, sh in rows:
    v = weighted_base(ex, sh); print(f"  {lab}: ${v:.2f} ({v-b0:+.2f} a share)")
for lab, l in (("lawsuit dismissed", 0.0), ("lawsuit ends in full DCA disgorgement", 15.86)):
    v = weighted_base(lit_=l); print(f"  {lab}: ${v:.2f} ({v-b0:+.2f} a share)")
v = sum(w * (V.fwd_eps(run(a)) * V.pe_lo - lit) for k, a, w in cases(FUT))
print(f"  futures path without the multiple hit: ${v:.2f} ({v-b0:+.2f} a share)")

# quarterly estimates on the base, against consensus (data/consensus_quarterly.csv)
from common import rows as _rows
_c = {r["quarter"]: float(r["consensus_adj_eps"]) for r in _rows("consensus_quarterly.csv")}
cons = [_c[n] for n in ("Q4 2026", "Q1 2027", "Q2 2027", "Q3 2027", "Q4 2027")]
r = run(dict(fed_path_bp=FUT))
print("quarterly estimates on the futures path:")
for x, c in zip(r["quarters"][:5], cons):
    print(f"  {x['q']}: client cash ${x['client_cash']:.0f}m, gross profit ${x['gp']:.0f}m, adj pre-tax ${x['adj_pretax']:.0f}m, EPS ${x['eps']:.2f} vs ${c:.2f} ({x['eps']/c-1:+.0%})")
q27 = r["quarters"][1:5]
print(f"  2027: client cash ${sum(x['client_cash'] for x in q27):.0f}m, gross profit ${sum(x['gp'] for x in q27):.0f}m, adj pre-tax ${sum(x['adj_pretax'] for x in q27):.0f}m, EPS ${sum(x['eps'] for x in q27):.2f} vs $29.26 ({sum(x['eps'] for x in q27)/29.26-1:+.0%})")
ke_, pe_, pem_ = setup(FUT, True)
print("cases on the base at both multiples:")
for k, a, w in cases(FUT):
    f = V.fwd_eps(run(a)); print(f"  {k} ({w:.0%}): ${f*pe_-lit:.0f} at {pe_:.2f}x, ${f*pem_-lit:.0f} at {pem_:.2f}x")
