# Who else charges a flat monthly fee per account on swept IRA cash, at what level, and who lets SEP and SIMPLE IRAs in.
# Fees are at a fed funds target of 3.75-4.00% (the range since the last cut, FRED DFEDTARL/DFEDTARU on 23 Nov 2026).
import os, csv
HERE = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(HERE, "..", "data", "per_account_sweep_fees_2026-11-23.csv"))))
FF_TOP = 4.00
for bal in (6346, 5000):
    print(f"\naverage account ${bal:,}: annual fee as % of balance and as share of the 4.00% top of the target range")
    for r in rows:
        if not r["monthly_fee_at_375_400bp"]: continue
        f = float(r["monthly_fee_at_375_400bp"]); pct = f * 12 / bal * 100
        print(f"  {r['firm']:<32} ${f:5.2f}/mo  {pct:4.2f}% of balance  {pct/FF_TOP:5.0%} of fed funds")
fees = sorted(float(r["monthly_fee_at_375_400bp"]) for r in rows if r["monthly_fee_at_375_400bp"])
print(f"\nfee range across the {len(fees)} with a printed level: ${fees[0]:.2f}-${fees[-1]:.2f}; LPL ranks {sorted(fees, reverse=True).index(19.50)+1} of {len(fees)}")
print("SEP/SIMPLE eligible:", ", ".join(f"{r['firm']}={r['sep_simple_eligible']}" for r in rows))
