# Why my 2027 EPS on the futures path ($26.00) sits below consensus ($29.26): undo my choices one at a time.
from eps_model import run
import fed_path as F
from common import rows
FUT = F.futures_path()
cons = 29.26  # data/consensus.csv (Nasdaq, 23 Nov 2026)
steps = [("my base (futures path)", {}),
         ("undo my S&P markdown (client assets back to the Sep 30 level)", dict(initial_asset_shock=0.0)),
         ("stop the cash drain (cash share of assets flat)", dict(cash_drift_yr=(0.0, 0.0, 0.0))),
         ("costs: core G&A growth 3% not 5%", dict(core_ga_growth_yr=0.03)),
         ("organic growth 4.5% (Q3's pace) not 3.5%", dict(organic_growth_yr=0.045)),
         ("Commonwealth synergies at twice my ramp", dict(commonwealth_synergy_extra_q=[0, 10, 20, 30, 40, 50, 50, 50, 50]))]
acc = dict(fed_path_bp=FUT); prev = None
for name, a in steps:
    acc.update(a); e = run(acc)["eps_2027"]
    print(f"{name}: 2027 ${e:.2f}" + ("" if prev is None else f" ({e-prev:+.2f})"))
    prev = e
gap = cons - run(dict(fed_path_bp=FUT))["eps_2027"]
print(f"consensus 2027 ${cons:.2f}; total gap ${gap:.2f}; what's left after these steps ${cons-prev:+.2f}")
