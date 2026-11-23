# A damages range for the consolidated sweep case, built the way a plaintiff would, then an expected cost.
# Class period here: Q3 2022 (when rates became meaningful) to Q3 2026. End-of-quarter balances.
from common import rows, kv

Q = [r for r in rows("sweep_yields_quarterly.csv") if r["quarter"] >= "2022Q3"]
client = 0.0025            # complaint: DCA paid 0.16%-0.35% from 2022 to Aug 2024; Dec 2025 sheet 0.30%
adv_ica_share = 9.2 / 37.8 # my advisory share of ICA, same as valuation.py

def damages(bench, with_ica):
    tot = 0.0
    for r in Q:
        bal = float(r["dca_end_bn"]) + (float(r["ica_end_bn"]) * adv_ica_share if with_ica else 0)
        tot += bal * 1e9 * max(bench(float(r["fed_funds_avg_bps"]) / 1e4) - client, 0) / 4
    return tot / 1e6

dca_fees = sum(float(r["dca_end_bn"]) * 1e9 * float(r["dca_fee_yield_bps"]) / 1e4 / 4 for r in Q) / 1e6
print(f"{Q[0]['quarter']} to {Q[-1]['quarter']}: DCA fees LPL kept ${dca_fees:,.0f}m (what disgorgement could reach on the DCA)")
for lab, b in (("money fund rate (funds less 15 bp)", lambda f: f - 0.0015), ("wirehouse level (90% of funds)", lambda f: 0.9 * f), ("half of funds", lambda f: 0.5 * f)):
    print(f"  benchmark {lab}: DCA ${damages(b, False):,.0f}m; DCA plus advisory ICA ${damages(b, True):,.0f}m")

plaintiff = damages(lambda f: 0.9 * f, True)
opp_ratio = 70 / 440
tax = 0.265; shares = 78.31
cases = [("dismissed or defence wins", 0.40, 0.0),
         ("settles at Oppenheimer's ratio of its own estimate (16%)", 0.50, plaintiff * opp_ratio),
         ("judgment for full DCA disgorgement", 0.10, dca_fees)]
exp = 0
for lab, p, cost in cases:
    exp += p * cost
    print(f"  {lab} ({p:.0%}): ${cost:,.0f}m pre-tax, ${cost*(1-tax)/shares:.2f} a share")
print(f"expected cost ${exp:,.0f}m pre-tax, ${exp*(1-tax)/shares:.2f} a share after tax; Oppenheimer paid $70m against its own >$440m estimate ({opp_ratio:.0%})")
print(f"old ceiling for comparison: three years of the full DCA gap to Merrill, $13.72 a share")
