# Fails loudly if my transcriptions stop reconciling to the filings.
from common import rows

q = {r["quarter"]: float(r["recruited_aum_bn"]) for r in rows("recruiting_quarterly.csv")}
ttm26 = q["2025Q4"] + q["2026Q1"] + q["2026Q2"] + q["2026Q3"]
ttm25 = q["2024Q4"] + q["2025Q1"] + q["2025Q2"] + q["2025Q3"]
assert round(ttm26) == 81, ttm26      # release: TTM recruited $81bn
assert round(ttm25) == 168, ttm25     # Q3 2025 release: TTM $168bn
assert round(q["2026Q3"] / q["2025Q3"] - 1, 2) == -0.26  # release: down 26%

ytd = {r["period_end"]: int(r["ytd_cash_out_thousands"]) for r in rows("advisor_loans_ytd_xbrl.csv")}
lo = {r["quarter"]: float(r["advisor_loans_cash_out_m"]) for r in rows("recruiting_quarterly.csv")}
chk = {
    "2026Q3": ytd["2026-09-30"] - ytd["2026-06-30"],
    "2026Q2": ytd["2026-06-30"] - ytd["2026-03-31"],
    "2026Q1": ytd["2026-03-31"],
    "2025Q4": ytd["2025-12-31"] - ytd["2025-09-30"],
    "2025Q3": ytd["2025-09-30"] - ytd["2025-06-30"],
    "2025Q2": ytd["2025-06-30"] - ytd["2025-03-31"],
    "2025Q1": ytd["2025-03-31"],
    "2024Q4": ytd["2024-12-31"] - ytd["2024-09-30"],
    "2024Q3": ytd["2024-09-30"] - ytd["2024-06-30"],
    "2024Q2": ytd["2024-06-30"] - ytd["2024-03-31"],
}
for k, v in chk.items():
    assert abs(v / 1000 - lo[k]) < 0.1, (k, v, lo[k])

cf = {r["period"]: r for r in rows("cash_flow.csv")}
assert cf["9M2026"]["advisor_loans_out_k"] == str(ytd["2026-09-30"])
assert cf["FY2025"]["advisor_loans_out_k"] == str(ytd["2025-12-31"])
print("all tie-outs pass")

# the headline numbers in the article, recomputed from the data so they can't drift
import subprocess, sys, os
out = subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "sweep_reset.py")], capture_output=True, text=True).stdout
for must in ["$4.57 a share", "$5.02 a share", "$2.86 a share", "$280.55", "$310.49", "$254.71", "$197.39", "$243.95", "LPLA -9.7%, MS -6.6%, SF -6.2%"]:
    assert must in out, must
print("article sweep numbers reproduce")

# my own EPS model, the probability tree and the cross-checks, as quoted in the article
here = os.path.dirname(os.path.abspath(__file__))
def run_script(name):
    return subprocess.run([sys.executable, os.path.join(here, name)], capture_output=True, text=True).stdout
checks = {
    "valuation.py": ["$24.35", "$29.56", "$28.25", "11.3x", "$322.01", "$313.76", "$277.08", "$232.16", "$294.41 (+11.3%)", "$346.64 (+31.0%)",
                     "$257.05", "56%", "$302.98", "$151.93", "28.5%", "$19.03", "$5.32", "$193 a share"],
    "consensus_bridge.py": ["2027 $27.04", "(-13.0%)", "(+2.8%)", "(-1.2%)"],
    "backtest.py": ["average EPS error -4.7%"],
    "multiple_history.py": ["median 13.56x", "25th pct 11.54x", "R-squared 0.20", "15.0x", "95% of pre-tax", "92% of pre-tax"],
    "sweep_capture.py": ["DCA 400 (76%)", "DCA 401 (93%)", "DCA 346 (94%)", "ICA 352 (96%)", "2.44m", "$6,194", "2.34% -> 2.18%"],
    "event_study.py": ["abnormal -20.0%", "abnormal -5.3%", "abnormal -15.5%", "+65.6%", "$-81.27"],
    "options_term.py": ["40.8%", "40.9%", "0.9%"],
    "damages.py": ["$1,690m", "$3,166m", "$504m", "$3.95 a share"],
    "dca_economics.py": ["fee -11.6%, implied accounts +2.2%", "371 bps, 96%", "$18.25 at the Dec 2025", "1.04m accounts, $8,584", "2.38m accounts, $6,346", "at least 81% of funds", "at least 102% of funds", "+42%"],
    "deposit_benchmarks.py": ["2026 3.76% (102%)", "2024 4.25% (81%)", "JPMorgan interest-bearing deposits: 2024 2.94% (56%)", "2026 0.23% (6%)", "(102%)"],
    "dca_fix_costs.py": ["$557m", "$5.42 a share, 22%", "$2.43-$3.22", "$4.75 a share"],
    "quarterly_estimates.py": ["adj EPS $5.32 vs consensus $6.02 (-12%)", "adj EPS $6.32 vs consensus $7.64 (-17%)"],
    "peer_multiples.py": ["SCHW: 11.6x", "RJF: 11.0x", "LPLA: 9.0x", "78%"],
    "whats_priced.py": ["$286m a year pre-tax, 51% of the DCA fee", "118% of the DCA fee", "(-40.11 a share)", "(-8.38 a share)", "(-28.46 a share)"],
    "kpi_and_capital.py": ["2.9% (-0.9 pt)", "2.2% (-0.2 pt)", "$50.0bn", "$4,756", "$900m", "+105 bp", "average $319.87", "-17.3%", "2.68x"],
}
for script, musts in checks.items():
    out = run_script(script)
    for must in musts:
        assert must in out, (script, must)
print("model, valuation and capital numbers reproduce")
