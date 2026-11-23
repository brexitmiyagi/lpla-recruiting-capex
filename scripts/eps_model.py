# My own EPS build for 2027-2028, quarterly from Q4 2026, starting from the Q3 2026 run rate.
# Every input is in ASSUMPTIONS so you can change it. Adjusted EPS = LPL's definition
# (excludes amortization of acquired intangibles and acquisition costs).
import os, csv, json

HERE = os.path.dirname(os.path.abspath(__file__))

Q3 = dict(  # Q3 2026, from the earnings release (dollars in millions)
    assets_bn=2564.6, gross_profit=1662.2, client_cash_rev=461.471, third_party_cash_avg_bn=53.2,
    core_ga=532.205, ta_amort=150.009, promo=87.943, share_comp=21.109, regulatory=6.390,
    da=117.287, interest=105.834, adj_pretax=641.119, adj_eps=5.97, diluted_shares_m=78.968,
    advisor_loans=3979.8, adv_plus_comm_rev=2872.928 + 1250.756, total_debt=7836, corp_cash=563)

ASSUMPTIONS = dict(
    market_growth_yr=0.06,        # assets from markets
    organic_growth_yr=0.035,      # Q3 was 4.5% annualized, October "in the zone of 3%"
    cash_share_of_assets=0.0208,  # third-party sweep cash: Q3 avg $53.2bn on ~$2.56tn (October total ~$55.5bn incl. CCA)
    q4_payout_step=0.004,         # Q4 guide: payout rate up ~40 bps
    q4_client_cash_yield_step=0.0014,  # ICA +~20 bps on ~70% of bank sweep
    fed_change_bp=0,              # base: no further Fed moves
    floating_ica_share=0.35, ica_share_of_cash=0.70,
    dca_share_of_cash=16.0 / 54.8,  # DCA fee is a per-account fee indexed to the fed funds target (10-K, ADV brochure); it now moves ~1:1 with funds
    dca_fed_beta=0.94,            # Q3 2026 DCA fee yield 346 bps / fed funds 367 bps
    q4_fed_vs_q3_bp=21,           # effective funds 3.88% (FRED DFF, Nov 2026) vs Q3 average 3.67%; the ICA part is already in LPL's +20 bp guide
    mmf_fee_bps=10,               # what LPL earns on cash that leaves the sweep for purchased money funds (6-20 bps when it last disclosed, 2020-22)
    q4_core_ga=566.0,             # 2026 guide midpoint $2,150m less Q1-Q3 ($1,583.5m)
    core_ga_2026=2150.0, core_ga_growth_yr=0.05,
    core_ga_shape=[532.049/2150, 519.272/2150, 532.205/2150, 566.0/2150],  # 2026 quarterly pattern (Q4 = guide)
    promo_2026=75.888+79.123+87.943+88.0, promo_shape=None,
    ica_fixed_reprice_bp_per_q=0.0,  # sensitivity: fixed ICA contracts rolling to lower (-) or higher (+) rates, bp of ICA yield per quarter
    ta_amort_rate_yr=0.151,       # Q3 TA amortization x4 / loan book
    loan_book_bps_of_assets=15.5, # stable in 2026
    promo_growth_yr=0.05, q4_promo=88.0,
    q4_da=130.0, da_growth_q=0.02,
    q4_interest=117.0, interest_growth_q=0.0,
    share_comp_q=22.0, regulatory_q=7.0,
    tax_rate=0.265,               # Q3 adjusted: 1 - 5.97*78.968/641.1
    buyback_q=300.0, buyback_price_start=264.56, buyback_price_growth_q=0.02, dilution_q_m=0.10,
    commonwealth_synergy_extra_q=[0, 5, 10, 15, 20, 25, 25, 25, 25],  # pre-tax $m by quarter Q4'26..Q4'28, my guess at ramp to "Q4 of 2027"
    sweep_giveback_pretax_yr=0.0, # set by scenarios
    platform_offset_share=0.0,    # share of a give-back recovered through platform fees
    initial_asset_shock=-0.045,   # marked to Nov 20: Oct-end client assets $2,560.9bn (monthly report), then S&P (SPY) -8.7% Oct 30 to Nov 20 at a 0.5 beta
    cash_share_drift_q=0.0,       # e.g. -0.00025 = sweep cash falls 0.1 pt of assets a year (cash sorting / AI tools)
    cash_drift_yr=(0.0, -0.0010, -0.0005),  # cash share of assets change in 2026 Q4, 2027, 2028. Q3 cash share fell 6.4, 3.8, 2.9, 2.4, 2.2% (2022-26); the fall has roughly halved each year, so I carry that on
)

def run(a=None, verbose=False):
    a = dict(ASSUMPTIONS, **(a or {}))
    qs = ["Q4 26", "Q1 27", "Q2 27", "Q3 27", "Q4 27", "Q1 28", "Q2 28", "Q3 28", "Q4 28"]
    g = (1 + a["market_growth_yr"] + a["organic_growth_yr"]) ** 0.25 - 1
    assets = Q3["assets_bn"] * (1 + a["initial_asset_shock"]); shares = Q3["diluted_shares_m"]; price = a["buyback_price_start"]
    gp_ex_cash_rate = (Q3["gross_profit"] - Q3["client_cash_rev"]) / Q3["assets_bn"]
    cash_yield = Q3["client_cash_rev"] * 4 / Q3["third_party_cash_avg_bn"] / 1000
    payout_drag_rate = a["q4_payout_step"] * Q3["adv_plus_comm_rev"] / Q3["assets_bn"]
    core = a["q4_core_ga"]; promo = a["q4_promo"]; da = a["q4_da"]; intr = a["q4_interest"]
    out = []; drift_acc = 0.0
    for i, q in enumerate(qs):
        assets_prev = assets; assets = assets * (1 + g); avg = (assets + assets_prev) / 2
        if i == 0: avg *= (1 + a["initial_asset_shock"] / 2) / (1 + a["initial_asset_shock"])  # October was flat, so Q4 only carries about half the drop
        if i == 0: cash_yield += a["q4_client_cash_yield_step"] + a["q4_fed_vs_q3_bp"] / 1e4 * a["dca_fed_beta"] * a["dca_share_of_cash"]
        cy = cash_yield + a["fed_change_bp"] / 1e4 * (a["floating_ica_share"] * a["ica_share_of_cash"] + a["dca_fed_beta"] * a["dca_share_of_cash"]) + a["ica_fixed_reprice_bp_per_q"] * i / 1e4 * (1 - a["floating_ica_share"]) * a["ica_share_of_cash"]
        yr_n = 0 if q.endswith("26") else (1 if q.endswith("27") else 2)
        drift_acc += a["cash_drift_yr"][yr_n] / 4
        cash_bal = avg * max(a["cash_share_of_assets"] + drift_acc - a["cash_drift_yr"][yr_n] / 8 + a["cash_share_drift_q"] * (i + 1), 0.0)
        client_cash = cash_bal * 1000 * cy / 4
        lost = avg * max(-(drift_acc - a["cash_drift_yr"][yr_n] / 8 + a["cash_share_drift_q"] * (i + 1)), 0.0)
        client_cash += lost * 1000 * a["mmf_fee_bps"] / 1e4 / 4   # some revenue follows the cash into money funds
        giveback = a["sweep_giveback_pretax_yr"] / 4 * (1 - a["platform_offset_share"])
        gp_ex = avg * (gp_ex_cash_rate - payout_drag_rate)
        gp = gp_ex + client_cash - giveback
        yr_n = 0 if q.endswith("26") else (1 if q.endswith("27") else 2)
        qi = int(q[1]) - 1
        core = a["core_ga_2026"] * (1 + a["core_ga_growth_yr"]) ** yr_n * a["core_ga_shape"][qi]
        pshape = a["promo_shape"] or [75.888 / a["promo_2026"], 79.123 / a["promo_2026"], 87.943 / a["promo_2026"], 88.0 / a["promo_2026"]]
        promo = a["promo_2026"] * (1 + a["promo_growth_yr"]) ** yr_n * pshape[qi]
        book = avg * a["loan_book_bps_of_assets"] / 10  # $m
        ta = book * a["ta_amort_rate_yr"] / 4 if i > 0 else 160.0
        if i > 0: da *= 1 + a["da_growth_q"]; intr *= 1 + a["interest_growth_q"]
        syn = a["commonwealth_synergy_extra_q"][i]
        pretax = gp - core - ta - promo - a["share_comp_q"] - a["regulatory_q"] - da - intr + syn
        ni = pretax * (1 - a["tax_rate"])
        shares_bought = a["buyback_q"] / price
        shares = shares - shares_bought + a["dilution_q_m"]; price *= 1 + a["buyback_price_growth_q"]
        out.append(dict(q=q, assets_bn=assets, client_cash=client_cash, giveback=giveback, gp=gp, core_ga=core, ta=ta,
                        promo=promo, da=da, interest=intr, synergy=syn, adj_pretax=pretax, adj_ni=ni, shares=shares, eps=ni / shares,
                        client_cash_after_tax_per_share=(client_cash - giveback) * (1 - a["tax_rate"]) / shares))
    yr = lambda y: [r for r in out if r["q"].endswith(y)]
    res = dict(q4_26=out[0]["eps"], eps_2027=sum(r["eps"] for r in yr("27")), eps_2028=sum(r["eps"] for r in yr("28")),
               cash_eps_2027=sum(r["client_cash_after_tax_per_share"] for r in yr("27")),
               cash_eps_2028=sum(r["client_cash_after_tax_per_share"] for r in yr("28")), quarters=out)
    if verbose:
        for r in out:
            print(f"{r['q']}: assets ${r['assets_bn']:,.0f}bn, client cash ${r['client_cash']:.0f}m, GP ${r['gp']:.0f}m, adj pretax ${r['adj_pretax']:.0f}m, shares {r['shares']:.2f}m, adj EPS ${r['eps']:.2f}")
    return res

if __name__ == "__main__":
    base = run(verbose=True)
    print(f"2026E adj EPS: Q1-Q3 actual $17.41 + my Q4 ${base['q4_26']:.2f} = ${17.41+base['q4_26']:.2f} (consensus $23.52)")
    print(f"my 2027 adj EPS ${base['eps_2027']:.2f} (consensus $29.26); 2028 ${base['eps_2028']:.2f} (consensus $35.60)")
    print(f"client cash after tax per share: 2027 ${base['cash_eps_2027']:.2f}, 2028 ${base['cash_eps_2028']:.2f}")
    with open(os.path.join(HERE, "..", "results", "eps_model_quarters.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(base["quarters"][0].keys())); w.writeheader(); [w.writerow(r) for r in base["quarters"]]
