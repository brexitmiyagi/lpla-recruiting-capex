import os, csv

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")


def rows(name):
    with open(os.path.join(DATA, name), newline="") as f:
        return list(csv.DictReader(f))


def kv(name):
    out = {}
    for r in rows(name):
        try:
            out[r["item"]] = float(r["value"])
        except ValueError:
            out[r["item"]] = r["value"]  # text rows (ratings, case names)
    return out


def shares_out_m():
    c = kv("company_q3_2026.csv")
    return (c["shares_issued_k"] - c["treasury_shares_k"]) / 1000.0


def ttm_tax_rate():
    c = kv("company_q3_2026.csv")
    return c["ttm_tax_k"] / (c["ttm_net_income_k"] + c["ttm_tax_k"])
