# My quarterly adjusted EPS against consensus, Q4 2026 to Q4 2027.
from eps_model import run
from common import rows
base = run()
cons = {r["quarter"]: float(r["consensus_adj_eps"]) for r in rows("consensus_quarterly.csv")}
names = ["Q4 2026", "Q1 2027", "Q2 2027", "Q3 2027", "Q4 2027"]
for n, q in zip(names, base["quarters"][:5]):
    print(f"{n}: client cash revenue ${q['client_cash']:.0f}m, gross profit ${q['gp']:.0f}m, adj pre-tax ${q['adj_pretax']:.0f}m, adj EPS ${q['eps']:.2f} vs consensus ${cons[n]:.2f} ({q['eps']/cons[n]-1:+.0%})")
