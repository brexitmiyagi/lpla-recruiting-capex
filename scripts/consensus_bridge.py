# Walk my 2027 EPS up to consensus one lever at a time, to see what the Street must be assuming.
from eps_model import run
steps = [
    ("my base", {}),
    ("+ two more Fed hikes (+50 bp), which the 2-year at 4.76% roughly prices", dict(fed_change_bp=50)),
    ("+ organic growth 4.5% (Q3's pace) not 3.5%", dict(organic_growth_yr=0.045)),
    ("+ core G&A growth 3% not 5%", dict(core_ga_growth_yr=0.03)),
    ("+ Commonwealth synergies double my ramp", dict(commonwealth_synergy_extra_q=[0, 10, 20, 30, 40, 50, 50, 50, 50])),
    ("+ market 8% a year not 6%", dict(market_growth_yr=0.08)),
]
acc = {}
for name, a in steps:
    acc.update(a); r = run(acc)
    print(f"{name}: 2027 ${r['eps_2027']:.2f}, 2028 ${r['eps_2028']:.2f}")
print("consensus: 2027 $29.26, 2028 $35.60")
for name, a in [("ICA fixed book reprices 5 bp lower each quarter", dict(ica_fixed_reprice_bp_per_q=-5)), ("ICA fixed book reprices 5 bp higher each quarter", dict(ica_fixed_reprice_bp_per_q=5))]:
    r = run(a); b = run(); print(f"sensitivity, {name}: 2027 ${r['eps_2027']:.2f} ({r['eps_2027']/b['eps_2027']-1:+.1%})")
for name, a in [("S&P 500 -10% (client assets -5%)", dict(initial_asset_shock=-0.045 - 0.05)), ("S&P 500 +10% (client assets +5%)", dict(initial_asset_shock=-0.045 + 0.05)),
                ("Fed -25 bp", dict(fed_change_bp=-25)), ("Fed +25 bp", dict(fed_change_bp=25))]:
    r = run(a); b = run(); print(f"sensitivity, {name}: 2027 ${r['eps_2027']:.2f} ({r['eps_2027']/b['eps_2027']-1:+.1%})")
