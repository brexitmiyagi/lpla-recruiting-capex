# A simple linked model: adjusted income statement, cash flow and balance sheet, 2026E-2028E (no give-back case).
# It is deliberately small. Every line comes from eps_model.py plus the assumptions below.
import os, csv
from eps_model import run, Q3
HERE = os.path.dirname(os.path.abspath(__file__))

A = dict(capex_yr=800.0, intangibles_amort_q=73.0, acquisition_costs_yr=100.0, dividend_per_share=1.20,
         tax=0.265, loan_book_start=Q3["advisor_loans"], debt=7836.0 + 750.0 - 616.0,  # Nov notes repaid the revolver
         corp_cash_start=563.0, equity_start=5812.3)
r = run()
qs = r["quarters"]
years = {"2026E (Q4 only)": qs[0:1], "2027E": qs[1:5], "2028E": qs[5:9]}
rows = []
cash = A["corp_cash_start"]; book = A["loan_book_start"]; equity = A["equity_start"]; debt = A["debt"]
for y, q in years.items():
    n = len(q)
    adj_pretax = sum(x["adj_pretax"] for x in q); adj_ni = sum(x["adj_ni"] for x in q)
    intang = A["intangibles_amort_q"] * n; acq = A["acquisition_costs_yr"] * n / 4
    gaap_ni = adj_ni - (intang + acq) * (1 - A["tax"])
    da = sum(x["da"] for x in q); ta = sum(x["ta"] for x in q); interest = sum(x["interest"] for x in q)
    ebitda = adj_pretax + da + interest
    new_book = q[-1]["assets_bn"] * 15.5 / 10
    loans_out = ta + (new_book - book)              # cash out = forgiveness replaced + book growth
    capex = A["capex_yr"] * n / 4
    buyback = 300.0 * n; divs = A["dividend_per_share"] / 4 * n * q[-1]["shares"]
    cfo = gaap_ni + da + intang + ta - loans_out
    fcf = cfo - capex
    cash = cash + fcf - buyback - divs
    book = new_book
    equity = equity + gaap_ni - buyback - divs
    rows.append(dict(period=y, client_cash_rev=round(sum(x["client_cash"] for x in q)), gross_profit=round(sum(x["gp"] for x in q)),
                     adj_pretax=round(adj_pretax), adj_net_income=round(adj_ni), gaap_net_income=round(gaap_ni),
                     adj_eps=round(sum(x["eps"] for x in q), 2), ebitda=round(ebitda), cfo=round(cfo), capex=round(capex),
                     advisor_loans_paid=round(loans_out), fcf=round(fcf), buybacks=round(buyback), dividends=round(divs),
                     corp_cash_end=round(cash), advisor_loan_book_end=round(book), debt_end=round(debt), equity_end=round(equity),
                     net_debt_to_ebitda_annualized=round((debt - cash) / (ebitda * 4 / n), 2)))
if __name__ == "__main__":
    for x in rows: print(x)
out = os.path.join(HERE, "..", "results", "three_statement.csv")
with open(out, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); [w.writerow(x) for x in rows]
try:
    from openpyxl import Workbook
    wb = Workbook(); ws = wb.active; ws.title = "Model"
    ws.append(["LPLA simple linked model, no sweep give-back, $m except EPS"]); ws.append(["line"] + [x["period"] for x in rows])
    for k in rows[0]:
        if k != "period": ws.append([k] + [x[k] for x in rows])
    ws2 = wb.create_sheet("Quarters")
    ws2.append(list(qs[0].keys())); [ws2.append([round(v, 3) if isinstance(v, float) else v for v in q.values()]) for q in qs]
    wb.save(os.path.join(HERE, "..", "results", "lpla_model.xlsx"))
    print("saved results/lpla_model.xlsx")
except ImportError:
    pass
