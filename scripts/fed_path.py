# The Fed path the Treasury bill and note curve implies, quarter by quarter, for the EPS model.
# Two ways: 30-day fed funds futures (CME FedWatch, read 23 Nov 2026), which is the main path, and the Treasury bill and note curve (FRED, 19 Nov 2026) as a cross-check.
# Bills trade above or below fed funds for reasons that have nothing to do with the Fed (supply, tax dates),
# so I take the spread off first. I calibrate it on the 1-month bill, which only spans the December meeting.
import os, csv
HERE = os.path.dirname(os.path.abspath(__file__))
curve = {r["series"]: (float(r["maturity_yrs"]), float(r["yield_pct"])) for r in csv.DictReader(open(os.path.join(HERE, "..", "data", "treasury_curve_2026-11-19.csv")))}
effr = curve["DFF"][1]
pts = [(0.0, effr)] + [curve[s] for s in ("DGS1MO", "DGS3MO", "DGS6MO", "DGS1", "DGS2")]

def path(basis_bp, term_premium_2y_bp=0):
    # average expected funds rate over each quarter from 19 Nov, by differencing cumulative yield x time
    adj = [(t, y if t == 0 else y - basis_bp / 100 - (term_premium_2y_bp / 100 if t == 2.0 else 0)) for t, y in pts]
    def cum(T):  # integral of the forward curve up to T, yields linear in maturity
        for (t0, y0), (t1, y1) in zip(adj, adj[1:]):
            if T <= t1:
                y = y0 + (y1 - y0) * (T - t0) / (t1 - t0); return y * T
        return adj[-1][1] * T
    # quarters Q4 26 .. Q4 28 measured from 19 Nov 2026; Q4 26 is only the last ~6 weeks
    edges = [0, 0.11, 0.36, 0.61, 0.86, 1.11, 1.36, 1.61, 1.86, 2.0]
    out = []
    for a, b in zip(edges, edges[1:]):
        f = (cum(b) - cum(a)) / (b - a)
        out.append(round((f - effr) * 100))
    return out

def futures_path():
    # monthly average effective funds rate = 100 - futures price; quarter averages against today's 3.88%.
    # Q4 2026: October and November sat at 3.88%, December prices the 9 Dec hike. The model applies Q4's number to the
    # last six weeks only (0.11 of a 0.25-year quarter), so I scale the full-quarter average up by 0.25/0.11 here.
    m = {r["month"]: float(r["implied_avg_effr_pct"]) for r in csv.DictReader(open(os.path.join(HERE, "..", "data", "fed_funds_futures_2026-11-23.csv")))}
    q = lambda ms: (sum(m[k] for k in ms) / len(ms) - effr) * 100
    q4_26 = (0 + (m["2026-11"] - effr) * 100 + (m["2026-12"] - effr) * 100) / 3
    p = [q4_26 * 0.25 / 0.11, q(["2027-01", "2027-02", "2027-03"]), q(["2027-04", "2027-05", "2027-06"]),
         q(["2027-07", "2027-08", "2027-09"]), q(["2027-10", "2027-11"])]
    return [round(x) for x in p] + [round(p[-1])] * 4      # contracts stop at November 2027, so 2028 is held at the late-2027 level

# 1-month bill 4.20% against 3.88% effective. A 25 bp hike on 9 Dec would only lift the month's average about 11 bp,
# so the bill sits roughly 20 bp above the funds path. I use 20 bp, and 10 and 30 either side.
if __name__ == "__main__":
    qs = ["Q4 26", "Q1 27", "Q2 27", "Q3 27", "Q4 27", "Q1 28", "Q2 28", "Q3 28", "Q4 28"]
    for b in (10, 20, 30):
        p = path(b)
        print(f"bill-funds spread {b} bp: change in fed funds vs today's 3.88%, by quarter (bp): " + ", ".join(f"{q} {x:+d}" for q, x in zip(qs, p)))
    f = futures_path()
    print("fed funds futures (CME, 23 Nov): change vs 3.88% by quarter (bp): " + ", ".join(f"{q} {x:+d}" for q, x in zip(qs, f)) + " (2028 held flat)")
    print(f"futures: 2027 average {sum(f[1:5])/4:+.0f} bp; FedWatch puts 97.6% on a 25 bp hike on 9 Dec")
    p = path(20)
    print(f"bill curve cross-check, central path: 2027 average {sum(p[1:5])/4:+.0f} bp, about {sum(p[1:5])/4/25:.1f} hikes; 2028 average {sum(p[5:9])/4:+.0f} bp")
    with open(os.path.join(HERE, "..", "results", "fed_path.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["quarter", "futures", "bills_spread_10bp", "bills_spread_20bp", "bills_spread_30bp"])
        for i, q in enumerate(qs): w.writerow([q, futures_path()[i], path(10)[i], path(20)[i], path(30)[i]])
