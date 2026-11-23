# Cash spent on advisor loans vs the forgiveness charge that runs through earnings.
from common import rows

cf = {r["period"]: {k: float(v) for k, v in r.items() if k not in ("period", "source")} for r in rows("cash_flow.csv")}
ttm = {k: cf["FY2025"][k] - cf["9M2025"][k] + cf["9M2026"][k] for k in cf["FY2025"]}
cf["TTM Q3 2026"] = ttm
for p in ("FY2023", "FY2024", "FY2025", "TTM Q3 2026"):
    d = cf[p]
    gap = d["advisor_loans_out_k"] - d["loan_forgiveness_k"]
    fcf = d["operating_cash_flow_k"] - d["capex_k"]
    print(f"{p}: loans out ${d['advisor_loans_out_k']/1e3:,.1f}m, forgiveness charge ${d['loan_forgiveness_k']/1e3:,.1f}m, "
          f"cash ahead of P&L ${gap/1e3:,.1f}m, OCF ${d['operating_cash_flow_k']/1e3:,.1f}m, capex ${d['capex_k']/1e3:,.1f}m, FCF ${fcf/1e3:,.1f}m")
print(f"9M loans out 2026 vs 2025 ($m): {cf['9M2026']['advisor_loans_out_k']/1e3:,.1f} vs {cf['9M2025']['advisor_loans_out_k']/1e3:,.1f}")
q3_25_alone = 1565992 - 449518
print(f"Q3 2025 alone, the Commonwealth close quarter ($m): {q3_25_alone/1e3:,.1f}")
