# The same valuation run twice: Fed on hold (my base) and the Fed path the Treasury curve implies (fed_path.py).
# The DCA fee steps with the funds target, so a market that expects hikes is also expecting a bigger DCA fee.
import io, contextlib
from eps_model import run
import fed_path as F
with contextlib.redirect_stdout(io.StringIO()):
    import valuation as V
    import whats_priced as W

price, div, ke, lit = V.price, V.div, V.ke, V.lit

def cases(path):
    # In the wirehouse cases the client rate follows the Fed too, so the give-back grows with the path.
    # Merrill's 3.35% is 86% of 3.88% funds; I move it by 86% of the average change over the valuation year (Q4 27-Q3 28).
    d = 0 if path is None else sum(path[4:8]) / 4 / 1e4
    wire = V.s["merrill_advisory_tier5_apy"] + 0.86 * d
    extra = {} if path is None else dict(fed_path_bp=path)
    return [("A", dict(extra), 0.25),
            ("B", dict(extra, sweep_giveback_pretax_yr=V.gb(0.0058)), 0.35),
            ("C2", dict(extra, sweep_giveback_pretax_yr=V.gb(wire), platform_offset_share=0.5), 0.25),
            ("C", dict(extra, sweep_giveback_pretax_yr=V.gb(wire)), 0.15)]

def report(path, label):
    vals = {k: V.fwd_eps(run(a)) * V.pe_lo - lit for k, a, w in cases(path)}
    ev = sum(w * vals[k] for k, a, w in cases(path))
    evm = sum(w * (V.fwd_eps(run(a)) * V.pe_med - lit) for k, a, w in cases(path))
    r = run({} if path is None else dict(fed_path_bp=path))
    print(f"{label}: 2027 EPS ${r['eps_2027']:.2f}, 2028 ${r['eps_2028']:.2f}; cases at {V.pe_lo}x " + ", ".join(f"{k} ${v:.2f}" for k, v in vals.items()))
    print(f"  weighted ${ev:.2f} ({ev/price-1:+.1%}, {(ev+div)/price-1:+.1%} with the dividend); at {V.pe_med}x ${evm:.2f}; buy below ${(ev+div)/1.15:.2f}; case C {vals['C']/price-1:+.1%}")
    extra = {} if path is None else dict(fed_path_bp=path)
    def value_today(g, pe):
        return (V.fwd_eps(run(dict(extra, sweep_giveback_pretax_yr=g))) * pe - lit + div) / (1 + ke)
    for pe in (V.pe_lo, V.pe_med):
        lo, hi = 0.0, W.dca_fee_rev * 4
        for _ in range(60):
            m = (lo + hi) / 2
            lo, hi = (m, hi) if value_today(m, pe) > price else (lo, m)
        fee_on_path = W.dca_fee_rev * (1 if path is None else (19.50 + sum(path[1:5]) / 4 / 25 * 1.25) / 19.50)
        print(f"  what's priced at {pe}x: give-back ${m:.0f}m a year pre-tax, {m/W.dca_fee_rev:.0%} of today's DCA fee" + ("" if path is None else f", {m/fee_on_path:.0%} of the ${fee_on_path:.0f}m it would earn on this path in 2027"))
    return ev

flat = report(None, "Fed on hold (base)")
for b in (20, 10, 30):
    p = F.path(b)
    report(p, f"market path, bill spread {b} bp ({'+'.join(str(x) for x in p[1:5])} bp in 2027)")
# the DCA fee itself on the path: $60 a year per account per point of target, so 2.4 hikes is about +$36 a year per account
p = F.path(20); d27 = sum(p[1:5]) / 4
print(f"DCA fee on the central path: about ${19.50 + d27/25*1.25:.2f} a month on average in 2027 against $19.50 now ({d27/25:.1f} steps of $1.25)")
with contextlib.redirect_stdout(io.StringIO()):
    mp = report(F.path(20), "central")
print(f"the curve's path adds ${mp-flat:+.2f} a share to the weighted value")

print("chart: value today at 11.54x by share of today's DCA fee given up (Fed on hold / on the curve)")
for pct in (0, 25, 50, 75, 100):
    g = W.dca_fee_rev * pct / 100
    vals_ = [(V.fwd_eps(run(dict(x, sweep_giveback_pretax_yr=g))) * V.pe_lo - lit + div) / (1 + ke) for x in ({}, dict(fed_path_bp=F.path(20)))]
    print(f"  {pct}%: ${vals_[0]:.2f} / ${vals_[1]:.2f}")
