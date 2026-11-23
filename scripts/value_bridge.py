# From a Street-style value to mine, one judgement at a time, on the futures path. Each step changes one thing.
# Start: no sweep change (case A), client assets NOT marked down for the S&P's fall, at LPLA's median multiple, no litigation cost.
import io, contextlib
from eps_model import run
with contextlib.redirect_stdout(io.StringIO()):
    import market_path_value as M
    import valuation as V
FUT = M.FUT
ke, pe_cut, pem_cut = M.setup(FUT, True)
A = dict(fed_path_bp=FUT)
f_unmarked = V.fwd_eps(run(dict(A, initial_asset_shock=0.0)))
f_A = V.fwd_eps(run(A))
steps = []
v = f_unmarked * V.pe_med; steps.append(("start: no sweep change, no S&P markdown, median 13.56x", v))
v1 = f_A * V.pe_med; steps.append(("mark client assets to the Nov 20 market", v1 - v)); v = v1
v1 = f_A * V.pe_lo; steps.append(("25th-percentile multiple (13.56x to 11.54x)", v1 - v)); v = v1
v1 = f_A * pe_cut; steps.append(("cut the multiple for the higher cost of equity (to 10.85x)", v1 - v)); v = v1
wtd = sum(w * V.fwd_eps(run(a)) * pe_cut for k, a, w in M.cases(FUT))
steps.append(("weight the four sweep outcomes 25/35/25/15", wtd - v)); v = wtd
steps.append(("expected cost of the sweep lawsuit", -V.lit)); v -= V.lit
print("value bridge, $ a share:")
for lab, x in steps:
    print(f"  {lab}: {x:+.2f}" if not lab.startswith("start") else f"  {lab}: {x:.2f}")
print(f"  my 12-month value: {v:.2f}; today's price {V.price:.2f}")

# trigger levels
g_osaic = V.gb(0.0058)
print(f"Osaic-level fix: give-back ${g_osaic:.0f}m a year pre-tax, {g_osaic/557:.0%} of today's DCA fee")
print(f"SELL threshold under my rule (weighted total return below -5%): value below ${(V.price*0.95 - V.div):.2f}")
vals = {k: V.fwd_eps(run(a)) * pe_cut - V.lit for k, a, w in M.cases(FUT)}
print("cases: " + ", ".join(f"{k} ${x:.2f} ({(x+V.div)/V.price-1:+.1%} with the dividend)" for k, x in vals.items()))
no_a = 0.40 * vals["B"] + 0.35 * vals["C2"] + 0.25 * vals["C"]
print(f"if a Q4 fee cut takes 'no change' off the table (weights 0/40/35/25): ${no_a:.2f} ({(no_a+V.div)/V.price-1:+.1%})")
