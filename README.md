# lpla-recruiting-capex

This is the data and code behind my Seeking Alpha piece on LPL Financial (LPLA), "The Cash Fee Grew Because The Program Grew, And That's Done". Prices are the November 20, 2026 close.

The short version. The banks holding LPL's advisory IRA cash (the Deposit Cash Account) now pay at least the full fed funds rate for it, about 102% in Q3 2026 against about 81% in Q3 2024, while the client still gets about 0.30%. LPL takes the rest through a flat monthly fee per account set by the fed funds target, and as the average account shrank (about $8,584 to $6,346) its cut of each dollar rose from 76% to 94% of fed funds without the fee schedule changing. Valued at LPLA's own 25th-percentile forward multiple since 2017 (11.54x), four sweep outcomes weighted 25/35/25/15 give $294, 11.3% above the November 20 close, a HOLD under my rules. At the median multiple (13.56x) it's $347.

Later versions changed three things. LPL widened the DCA from IRAs only to IRAs and retirement plan accounts, SEP and SIMPLE included, between July 2024 and October 2025, which fits the late-2025 jump in accounts (the early-2025 rise is most likely Atria). The base case now uses the Fed path in fed funds futures (CME FedWatch, 23 Nov 2026: a December hike, about 61 bp higher on average in 2027), with the cost of equity and the multiple moved with it (9.54% to 10.09%, 11.54x to 10.85x). Higher rates lift EPS and cut the multiple by about the same, so the weighted value stays $294 and the price assumes LPL gives up 57% of the DCA fee. Without the multiple cut it's $313, still a HOLD.

## How to run it

Python 3, standard library only. From any folder:

    python scripts/tieout.py
    python scripts/oct28_decomposition.py
    python scripts/recruiting_unit_economics.py
    python scripts/cash_vs_earnings.py
    python scripts/sweep_sensitivity.py
    python scripts/capital_ladder.py
    python scripts/price_target.py
    python scripts/loan_book.py
    python scripts/big_down_days.py
    python scripts/sweep_reset.py
    python scripts/eps_model.py
    python scripts/three_statement.py
    python scripts/valuation.py
    python scripts/market_beta.py
    python scripts/backtest.py
    python scripts/consensus_bridge.py
    python scripts/multiple_history.py
    python scripts/kpi_and_capital.py
    python scripts/sweep_capture.py
    python scripts/dca_economics.py
    python scripts/deposit_benchmarks.py
    python scripts/dca_fix_costs.py
    python scripts/quarterly_estimates.py
    python scripts/peer_multiples.py
    python scripts/whats_priced.py
    python scripts/fed_path.py
    python scripts/market_path_value.py
    python scripts/dca_eligibility.py
    python scripts/dca_nowcast.py
    python scripts/dca_widening.py
    python scripts/consensus_gap.py
    python scripts/value_bridge.py
    python scripts/adv_clients.py
    python scripts/build_workbook.py
    python scripts/event_study.py
    python scripts/options_term.py
    python scripts/damages.py

My own run is saved in results/.

## What each script backs up

tieout.py checks my quarterly recruited assets add up to the $81 billion and $168 billion TTM figures LPL printed, and that my quarterly advisor-loan numbers match the year-to-date XBRL values. It stops if anything is off.

oct28_decomposition.py is the $3.79 billion lost on October 28 next to the $2.75 billion LPL funded at the Commonwealth closing, and what the $20 million EBITDA cut is worth at LPL's own 8x.

recruiting_unit_economics.py is the 88 bps vs 117 bps per recruited dollar, the 25.9 bps gross profit ROA, the 4.5 year payback and the 20.5% IRR.

cash_vs_earnings.py is advisor-loan cash paid vs the forgiveness charge in the P&L, operating cash flow and free cash flow for 2023, 2024, 2025 and the twelve months to Q3 2026.

sweep_sensitivity.py is the $0.31 a share per 25 bp hike on floating ICA and the $1.26 a share for a 25 bp give-back on bank sweep.

capital_ladder.py is the four prices of capital (4.33% notes after tax, 11.1% buyback earnings yield, 12.4% Commonwealth, 20.5% recruiting).

price_target.py is the peer multiples and an earlier simple bear/base/bull ($224 / $310 / $357) I kept as a cross-check. The target in the article comes from sweep_reset.py.

loan_book.py is the advisor-loan book from every 10-K since 2017 ($298.8m in 2018 to $3,979.8m now, 8.0 to 15.5 bps of client assets), TA as a share of a year's advisor revenue (143% then, 182% now), what carrying TA costs at LPL's 5.85% vs Osaic's 6.75% and 8% notes, and the Street and short interest numbers.

sweep_reset.py is the sweep section: client cash revenue next to adjusted pre-tax income, the implied 2.44m DCA accounts at $18 a month, the cost of paying DCA clients Merrill's 3.35% ($4.57 to $5.02 a share), $2.86 per $10bn of advisory ICA, the June 2026 price moves for LPLA, MS and SF, and the four cases behind the $281 target and $244 buy level, all at today's 9.04x.

eps_model.py is my own quarterly EPS build from Q4 2026 to Q4 2028, starting from the Q3 2026 run rate and LPL's Q4 guidance. All assumptions sit in one dictionary at the top. Costs follow 2026's quarterly pattern, the fixed-rate ICA book is held flat (a parameter lets you roll it up or down), and client cash as a share of assets keeps falling, 0.1 pt in 2027 and 0.05 pt in 2028, because that fall has roughly halved every year since 2022. With no sweep change it gives $26.86 for 2027 and $32.41 for 2028, against consensus of $29.26 and $35.60.

three_statement.py is a small linked income statement, cash flow and balance sheet built on the same model (also saved as results/lpla_model.xlsx).

valuation.py runs the sweep outcomes through the model (A no change, B match Osaic, C2 Merrill-level with half offset by platform fees, C Merrill-level, D C plus an S&P drop), weights them 25/35/25/15 and values each at today's price over my 2027 EPS (9.85x). It prints the probability-weighted value ($295.32), the odds on case C that would make today's price fair, the cash-sorting sensitivities, the sweep/non-sweep split and the decay rate the price implies, a DCF cross-check, and the litigation ceiling.

backtest.py runs the same rules from Q4 2025 and compares them with actual Q1-Q3 2026 EPS (average error -4.7%).

consensus_bridge.py walks my 2027 EPS toward consensus one assumption at a time, and prints the market, Fed and fixed-book sensitivities.

multiple_history.py is LPLA's trailing GAAP P/E at each year end since 2016 next to the funds rate, and how much of LPL's and Schwab's Q3 pre-tax income is interest and sweep income.

kpi_and_capital.py is the cash-sorting history from five Q3 releases, the KPI tracker starting values, debt maturities and the November notes, the buyback average cost, the 13F and options numbers, and leverage in the full-reset case.

market_beta.py estimates how much client assets move with the S&P from LPL's own market-impact lines.

big_down_days.py lists every LPLA day worse than -10% since November 2016 and what happened over the next 12 months.


whats_priced.py solves for the DCA give-back today's price implies (51% of the fee at 11.54x, more than all of it at the 13.56x median) and prints the per-share effect of each risk on the weighted value.

build_workbook.py writes results/LPLA-scenario-model.xlsx. Its first sheet, Start here, has yellow input cells (price, multiple, Fed move, S&P move, fee schedule override, client rate, account count, average balance, extra fee cut, case rates and weights) and live formulas for the DCA economics, the four case values, the weighted value and what the price implies. The sensitivities it uses are taken from eps_model.py.

data/catalysts.csv is the event calendar in the piece.

deposit_benchmarks.py puts the minimum bank payment for LPL's IRA cash next to what JPMorgan, Wells Fargo, Bank of America and Schwab pay on deposits, Schwab's brokered CDs, and the FDIC national savings and CD rates, all as a share of fed funds.

dca_fix_costs.py sizes the DCA fee per share and what a flat cut, a cap as a share of each account's balance, or Merrill's rate would cost. The caps assume a lognormal balance spread around the implied average (sigma 1.0 and 1.5); LPL doesn't disclose the real one.

quarterly_estimates.py is my adjusted EPS by quarter, Q4 2026 to Q4 2027, against Nasdaq/Zacks consensus.

peer_multiples.py is forward P/E against sweep or interest dependence for LPLA, SCHW, RJF and AMP (the AMP dependence figure is rough).

dca_economics.py rebuilds the Deposit Cash Account from LPL's April 2023 fee schedule (data/dca_fee_schedule_2023.csv) and the fed funds target history from FRED: the monthly fee each quarter, implied account count and average balance, and the minimum the banks must be paying as a share of fed funds for clients to get 0.30%. It also checks the implied account count across every Fed move (a wrong schedule would make the count jump when the fee steps) and prints the Q4 2026 call: a DCA fee yield of 355-390 bps if nothing has changed.

sweep_capture.py is LPL's fee yield on the ICA and DCA as a share of fed funds, every quarter since Q3 2021, the implied DCA account count at $18 a month, and the monthly cash share from the October 2026 monthly report.

event_study.py is LPLA's abnormal return against a market model around each sweep event in data/sweep_events.csv.

options_term.py backs implied volatility out of the Nasdaq option chain for every expiry, the implied Q4-results move, and January skew.

damages.py builds a damages range for the consolidated sweep case and an expected cost, which valuation.py deducts from every case.

multiple_history.py now also has LPLA's forward P/E on realised adjusted EPS for every quarter from Q4 2017, and a fit against the funds rate and cash share (it explains little).

## Sources

Fed funds futures and meeting odds: CME FedWatch, https://www.cmegroup.com/markets/interest-rates/cme-fedwatch-tool.html (read 23 Nov 2026)
LPL program brochures (March 2026): https://www.lpl.com/content/dam/edam/format/disclosure/progam-brochure/A9.pdf and https://www.lpl.com/content/dam/edam/format/disclosure/progam-brochure/A11.pdf
Atria closing: https://www.investmentnews.com/independent-broker-dealers/lpl-successfully-closes-atria-acquisition/257466
Treasury curve, 19 Nov 2026: FRED DGS1MO, DGS3MO, DGS6MO, DGS1, DGS2, DFF (https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS2 and so on)
DCA booklet July 2024: https://lpl.com/content/dam/lpl-www/documents/disclosures/lpl_dca-disclosure-booklet.pdf
DCA booklet October 2025: https://www.lpl.com/content/dam/edam/product/banking/dca-disclosure-booklet-banking-lending.pdf
LPL 10-Q Q3 2025: https://www.sec.gov/Archives/edgar/data/1397911/000162828025047934/lpla-20250930.htm
LPL 10-K 2025: https://www.sec.gov/Archives/edgar/data/1397911/000162828026010705/lpla-20251231.htm
Commonwealth conversion: https://www.investmentnews.com/independent-broker-dealers/commonwealth-financials-move-or-conversion-to-lpl-a-success-company-declares/269031 and https://wealthmanagement.com/ibd-news/lpl-closes-deal-for-2-7b-commonwealth-team-on-conversion-day

Bank deposit rates: JPMorgan, Wells Fargo, Bank of America and Schwab 10-Qs for Q3 2025 and Q3 2026 (EDGAR), average balance tables. Schwab brokered CD rate: Schwab Q3 2026 10-Q. FDIC national rates: FRED SNDR and NDR12MCD. Peer consensus: Nasdaq earnings forecasts, 23 Nov 2026. Raymond James FQ4 2026 and Ameriprise Q3 2026 earnings releases (8-K, EDGAR).
LPL DCA Disclosure Booklet as of April 2023 (fee schedule effective April 30, 2023): https://www.lpl.com/content/dam/lpl-www/documents/disclosures/lpl-dca-disclosure-booklet.pdf
LPL DCA Rate and Fee sheet as of 12/12/2025: https://www.lpl.com/content/dam/edam/product/banking/deposit-cash-acct-rate-fee.pdf
November 20 market close: https://spectrumlocalnews.com/us/snplus/business/2026/11/20/wall-street-nov-20-2026
LPL quarterly earnings releases Q1 2017 to Q3 2026 (EDGAR 8-K exhibit 99.1), saved and parsed for fed funds, ICA and DCA fee yields, cash balances and adjusted EPS.
LPL Form ADV brochures via the SEC's adviser search (firm 6413): consolidated program brochure and firm brochure dated October 8, 2026, SAM brochure dated November 13, 2026. https://adviserinfo.sec.gov/firm/summary/6413
LPL October 2026 monthly metrics (historical file and press release, 19 Nov 2026) on lpl.com, read through a fetch tool.
Daily closes and the option chain: Nasdaq API, pulled 23 Nov 2026 (saved in data/nasdaq).
FRED: SP500, DGS10, DGS2, DFF (to 19 Nov 2026).
Event dates: SEC release 2025-16; InvestmentNews 15 Jul 2024, 16 Jul 2024, 19 Jul 2024, 11 Oct 2024, 29 Jun 2026; Financial Planning 16 Jul 2024.

Q3 releases used for the cash history: https://www.sec.gov/Archives/edgar/data/1397911/000139791122000152/a2022q3earningsrelease.htm , https://www.sec.gov/Archives/edgar/data/1397911/000139791123000156/a2023q3earningsrelease.htm , https://www.sec.gov/Archives/edgar/data/1397911/000139791124000136/a2024q3earningsrelease.htm , https://www.sec.gov/Archives/edgar/data/1397911/000162828025047543/a2025q3earningsrelease.htm
November 2026 notes term sheet: https://www.sec.gov/Archives/edgar/data/1397911/000119312526463863/d170779dfwp.htm
Crane 100 Money Fund Index (3.76% as of 11/22/2026, site header): https://cranedata.com/
Fidelity FCASH: https://www.investmentnews.com/rias/fidelity-to-move-ria-clients-sweep-balances-to-in-house-product/258376
Save on Schwab: https://www.financial-planning.com/news/rias-working-with-schwab-get-higher-yielding-option-for-clients-cash
June 2025 ruling: https://citywire.com/pro-buyer/news/judge-partially-dismisses-cash-sweep-claims-against-lpl/a2469249 and https://www.thewealthadvisor.com/article/partial-legal-victory-lpl-financial
U.S. Bank dismissal and the Oppenheimer settlement: https://www.financial-planning.com/news/cash-sweeps-lawsuits-stumble-with-dismissal-of-u-s-bank-case
Nasdaq institutional holdings, analyst targets and option chain, pulled 23 Nov 2026: https://www.nasdaq.com/market-activity/stocks/lpla

LPL Q3 2026 earnings release: https://www.sec.gov/Archives/edgar/data/1397911/000162828026067590/a2026q3earningsrelease.htm
LPL Q3 2026 10-Q: https://www.sec.gov/Archives/edgar/data/1397911/000162828026068226/lpla-20260930.htm
LPL 2025 10-K: https://www.sec.gov/Archives/edgar/data/1397911/000162828026010705/lpla-20251231.htm
LPL Q3 2025 10-Q (Commonwealth closing): https://www.sec.gov/Archives/edgar/data/1397911/000162828025047934/lpla-20250930.htm
Commonwealth deal deck, March 2025: https://www.sec.gov/Archives/edgar/data/1397911/000119312525067661/d697025dex992.htm
Earnings releases for Q2 2025, Q3 2025, Q4 2025, Q1 2026, Q2 2026 (recruited assets and the EBITDA guidance path):
https://www.sec.gov/Archives/edgar/data/1397911/000139791125000119/a2025q2earningsrelease.htm
https://www.sec.gov/Archives/edgar/data/1397911/000162828025047543/a2025q3earningsrelease.htm
https://www.sec.gov/Archives/edgar/data/1397911/000162828026004112/a2025q4earningsrelease.htm
https://www.sec.gov/Archives/edgar/data/1397911/000162828026028890/a2026q1earningsrelease.htm
https://www.sec.gov/Archives/edgar/data/1397911/000162828026051046/a2026q2earningsrelease.htm
Advisor loans, XBRL (IncreaseDecreaseInOtherLoans): https://data.sec.gov/api/xbrl/companyfacts/CIK0001397911.json
2029 notes prospectus: https://www.sec.gov/Archives/edgar/data/1397911/000119312526465522/d158035d424b5.htm
Q3 2026 call transcript: https://www.fool.com/earnings/call-transcripts/2026/10/28/lpl-financial-lpla-q3-2026-earnings-call-transcript/
Fed funds and Treasury yields: https://fred.stlouisfed.org/series/DFEDTARU and https://fred.stlouisfed.org/series/DGS2
Prices, consensus EPS, analyst targets and short interest: Nasdaq, pulled November 23, 2026.
LPL 10-Ks for 2017 to 2025 (advisor-loan balances, client assets, advisors): https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001397911&type=10-K
TA ranges: https://winthropco.com/insights/what-is-a-financial-advisor-transition-deal-worth-in-2026 (a recruiter, paid by firms, so treat as marketing ranges)
Osaic notes: https://www.wealthmanagement.com/ibd-news/osaic-to-raise-another-750m-in-debt-refinancing
Osaic recapitalization: https://www.lw.com/en/news/2026/05/latham-watkins-advises-ares-as-co-lead-investor-in-reverence-capital-recapitalization-of-osaic
SEC sweep probe closed: https://www.wealthmanagement.com/regulation-compliance/sec-drops-lpl-cash-sweep-investigation
Sweep class action motion to dismiss: https://www.law360.com/articles/2545248
Merrill rate sheet (APY as of 11/20/2026): https://olui2.fs.ml.com/Publish/Content/application/pdf/GWMOL/ICCRateSheet.pdf
SEC charges against Wells Fargo and Merrill, Jan 17 2025: https://www.sec.gov/newsroom/press-releases/2025-16
Osaic rate lists (NFS, Pershing) and Form ADV Part 2A: https://assets.osaic.com/m/64fab5770bd90cd/original/NFS-RateChart.pdf , https://assets.osaic.com/m/5215e99c58707370/original/Pershing-RateChart.pdf , https://assets.osaic.com/m/2e9b66b68b4df36c/original/Form-ADV-Part-2A.pdf
Vu v. LPL Financial complaint (S.D. Cal. 3:24-cv-01484): https://wp.classlawgroup.com/wp-content/uploads/LPL-Financial-Cash-Sweep-Lawsuit-Complaint.pdf
Q1 and Q2 2026 call transcripts: https://seekingalpha.com/article/4897097-lpl-financial-holdings-inc-lpla-q1-2026-earnings-call-transcript , https://seekingalpha.com/article/4928271-lpl-financial-holdings-inc-lpla-q2-2026-earnings-call-transcript
Q3 2026 call transcript, second source: https://seekingalpha.com/article/4958241-lpl-financial-holdings-inc-lpla-q3-2026-earnings-call-transcript
Morgan Stanley advisory sweep to 3.6% (balances over $250,000 per Crane Data): https://www.investmentnews.com/wirehouses/morgan-stanley-boosts-returns-on-client-cash-report/267202
LPL DCA rate and fee sheet, 12/12/2025: https://www.lpl.com/content/dam/edam/product/banking/deposit-cash-acct-rate-fee.pdf

fed_path.py builds the Fed path quarter by quarter from 30-day fed funds futures (data/fed_funds_futures_2026-11-23.csv, read off CME FedWatch), and cross-checks it against the Treasury bill and note curve on 19 November (FRED), after taking a bill-to-fed-funds spread off. The two agree on 2027 within a basis point. data/fedwatch_meeting_probs_2026-11-23.csv has FedWatch's meeting-by-meeting odds.

market_path_value.py is the valuation the post uses: the futures path, with the cost of equity raised by beta times the 2027 rise in fed funds and the multiple cut to match. It also runs the futures path without that cut, the Fed on hold, and the bill-curve path, solves "what's priced" for each, prints the risk table and the quarterly estimates on the base. In the wirehouse cases the client rate rises with the path too.

dca_eligibility.py lays out the DCA eligibility wording from LPL's booklets and its 10-K and 10-Qs, tests the second, lower fee table in the July 2024 booklet against the data, and works out where the banks' payment on a small account stops covering LPL's flat fee.

dca_nowcast.py estimates Q4 2026 DCA revenue from LPL's monthly DCA balances before LPL reports. Put November and December in at the top when they come out and rerun. It backtests the same method on Q2 and Q3 2026.

dca_widening.py sizes the two waves in the implied DCA account count against the run-rate since (3.3% a quarter): about 260,000 accounts in Q1-Q2 2025, after Prudential Advisors moved onto LPL's platform in November 2024, and about 540,000 in Q3 2025-Q1 2026. The second starts the quarter Atria converted (July 2025, per LPL's 10-Q) and overlaps the eligibility change, so I can't split it. Both waves together are about 790,000 accounts, $186m a year before tax, $1.73 a share after tax. It also shows the answer at a 2% and 4% trend.

adv_clients.py reads LPL's Form ADV client counts by type (Item 5D) from the SEC's monthly adviser files for four year ends. Pension and profit sharing plan clients grew 13.6% in 2025, the same pace as 2024, and number about 10,000, so employer plans can't explain the 2025 jump in DCA accounts.

dca_widening.py also tests what balance the added accounts brought. It doesn't separate the explanations: every period's new accounts are smaller than the book, and the second wave's were the largest of the four, so I say the attribution rests on timing and documents.

value_bridge.py walks from a Street-style value ($455: no sweep change, no S&P markdown, median multiple) to mine ($294) one judgement at a time, and prints the levels behind the upgrade and downgrade triggers in the post.

consensus_gap.py walks my 2027 EPS on the futures path ($26.00) toward consensus ($29.26) one choice at a time. Undoing my S&P markdown is most of it.

## Things to be careful with

The 117 bps is an upper bound. The advisor-loan line also has loans to existing advisors in it, so the true cost per recruited dollar is a bit lower. I left out Q4 2024 (one big institution, cheap per dollar) and Q3 2025 (the Commonwealth closing quarter) from the before and after comparison. You can argue for other choices and the script makes that easy to change.

The 20.5% IRR is before tax and before the cost of servicing the advisor. It uses LPL's average gross profit ROA, and a recruited advisor won't be exactly average. The 14 years is the useful life LPL put on Commonwealth's advisor relationships, not a number I made up, but it's still an assumption.

The DCA client rate (0.30%) and $18 fee come from a sheet dated December 12, 2025. lpl.com blocked me from the current one, so if LPL has raised the rate since, my reset cost is too high. Morgan Stanley's 3.6% comes from one report of a Wolfe Research note. The probability weights are mine. Change them at the top of valuation.py and the value moves with them. The 25 bp give-back in scenario A is my stress, not anything LPL said.

Consensus EPS is one source (Nasdaq). The 2028 number has six estimates.

The 65% fixed-rate ICA share and the Q4 guidance come from the call transcript, which is AI-assisted. Check them against LPL's replay if they matter to you.

The Osaic carry comparison uses the coupons on two note add-ons as Osaic's marginal cost of debt. I don't know how Osaic actually funds its transition assistance, and it raised more than $2 billion of equity this year too.

The big-down-days list is one non-Covid example. It's context, not evidence.

The EPS model is mine and it's simple: assets grow with a 6% market and 3.5% organic growth, gross profit outside client cash is a fixed rate on assets, costs follow LPL's guidance and then grow 5% a year, and the Commonwealth synergy ramp is my guess. It lands about 8-9% below consensus. The split of advisory cash inside the ICA is unknown; I use half of what a proportional split would give ($9.2bn) and the script shows the range. Charging all costs to the non-sweep side is a choice, and it makes the sweep look as big as it can.

The futures only run to November 2027, so I hold 2028 at the late-2027 level. The multiple cut for rates is my choice and probably counts some of the path twice, since the 10-year already prices much of it; without it the value is $313. The eligibility timing is from documents: I couldn't open the July 2025 booklet, so the change sits somewhere between July 2024 and October 2025. The bank list and the current fee schedule on lpl.com were blocked to me, from a fetch tool and from a browser.

## Rating framework I use

BUY: probability-weighted 12-month total return of at least 15%, and the main downside case no worse than -10%. HOLD: weighted return between -5% and +15%, or a downside case worse than -10%. SELL: weighted return below -5%. Values come from my own EPS times LPLA's 25th-percentile historical forward multiple, so they don't move with the price and don't assume a rerating.

## Corrections

Before publication I had compared LPL's DCA to Morgan Stanley's 3.6% advisory rate, which only applies to balances over $250,000. The average DCA account holds about $6,200, so I switched the benchmark to Merrill's advisory rate, which applies at any balance.

While drafting, my rating went BUY $310 (consensus EPS), BUY $298 (my own EPS), HOLD $281 (Merrill's rate as the base case), BUY $321 (Osaic's rate as the base case) and HOLD $295 (a weighted tree plus the cash drain) and HOLD $294 (historical multiple, marked to the November market, litigation priced). None of those were published. The article explains each step.

The buyback average I first quoted was about $316. From XBRL share counts and cost it's $319.87, which is the number in the post.

The v7 valuation multiplied my EPS by today's price over my EPS, so the upside never changed with the price. It now uses LPLA's own historical forward multiple.

My earlier model started from September 30 and ignored the S&P's fall since then. It's now marked to November 20.

My earlier Fed sensitivity only counted the floating part of the ICA. The DCA fee is indexed to the fed funds target, so a 25 bp move is worth about 2.8% on 2027, not 1.2%.

My earlier versions held the Fed flat while the 2-year was 88 bp over fed funds. Then I ran the curve's path without touching the multiple and got $316, which raised earnings with rates but never the discount rate. The base now uses fed funds futures and moves the cost of equity and the multiple with them: $294.

Earlier versions said the acquisitions explained the jump in DCA accounts. Commonwealth wasn't on LPL's platform until November 2026, so it can't have. One version then said the eligibility change explained all of it; it fits the late-2025 jump, and the early-2025 rise is most likely Atria.

Earlier versions treated the April 2023 fee table as the only one. The July 2024 booklet has a lower one. dca_eligibility.py shows why the data don't fit it.

One version said the first wave was most likely Atria and the second was the eligibility change. LPL's 10-Qs say Atria converted in July 2025, the first quarter of the second wave, and Prudential Advisors moved in November 2024. So both waves come from conversions plus the eligibility change, and I don't split them.

Things I couldn't do: I couldn't get LPL's current DCA fee schedule or the names of its ICA banks (lpl.com refused automated fetches), I couldn't get Raymond James, Ameriprise, Stifel or Cetera advisory rates, and I didn't build advisor-level flows from BrokerCheck. Osaic doesn't publish advisor counts.

## Rating log (drafts, none published)

BUY $310 (consensus EPS at today's multiple), BUY $298 (my own EPS), HOLD $281 (Merrill's rate as the base case), BUY $321 (Osaic's rate as the base case), HOLD $295 (weighted cases plus the cash drain), HOLD $294 (LPLA's historical multiple, marked to the November market, litigation priced), HOLD $294 with the Fed on hold and $316 on the curve's path, HOLD $294 on the futures path with the multiple moved for rates. The published piece is the last one.

## Cautions on inputs

The base-rate table (data/peer_sweep_actions.csv) is six firms. The Nasdaq option quotes were sparse and often one-sided, so options_term.py drops wide and one-sided quotes and the results are indicative only. The October 2026 monthly figures were read from lpl.com through a fetch tool, not from EDGAR. The historical forward P/E uses EPS LPL reported later, which flatters the multiple in years when earnings beat. The DCA fee schedule is from April 2023; the December 2025 sheet shows $18.00 where the schedule gives $18.25, so it isn't applied exactly as printed. The implied bank rate assumes the 0.30% client rate applied to all balances; the booklet lets LPL take its fee from a client account when bank payments fall short.
