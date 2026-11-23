# What multiple did LPLA trade at through the last sweep scare (July 2024 to January 2025)?
# Forward P/E = price / the adjusted EPS LPL actually reported over the next four quarters (same method as multiple_history.py).
import csv, os
from common import rows
HERE = os.path.dirname(os.path.abspath(__file__))
eps = {r["quarter"]: float(r["adj_eps"]) for r in rows("lpla_quarterly_pe.csv")}
px = {r["date"]: float(r["close"]) for r in csv.DictReader(open(os.path.join(HERE, "..", "data", "nasdaq", "LPLA.csv")))}
fwd_q3_24 = eps["2024Q3"] + eps["2024Q4"] + eps["2025Q1"] + eps["2025Q2"]
fwd_q1_25 = eps["2025Q1"] + eps["2025Q2"] + eps["2025Q3"] + eps["2025Q4"]
for d, f, lab in (("07/11/2024", fwd_q3_24, "before the Wells Fargo/Morgan Stanley week"), ("07/19/2024", fwd_q3_24, "after it"),
                  ("08/05/2024", fwd_q3_24, "the low"), ("09/30/2024", fwd_q3_24, "quarter end"), ("01/21/2025", fwd_q1_25, "after the recovery")):
    print(f"{d} ({lab}): ${px[d]:.2f} on forward EPS ${f:.2f} = {px[d]/f:.2f}x")
print("my multiples: 11.54x (25th percentile 2017-2025), 10.85x after the cut for rates")
