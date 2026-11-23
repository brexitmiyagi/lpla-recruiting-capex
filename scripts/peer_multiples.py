# Forward P/E against how much of pre-tax income comes from cash sweep or net interest income.
from common import rows
for r in rows("peer_multiples.csv"):
    pe = float(r["price_2026_11_20"]) / float(r["next_fy_consensus_eps"])
    dep = float(r["sweep_or_interest_income"]) / float(r["pretax_income"])
    print(f"{r['ticker']}: {pe:.1f}x {r['next_fy']} consensus; {dep:.0%} ({r['dependence_definition']})")
print("LPLA on my next four quarters: 11.3x (valuation.py)")
