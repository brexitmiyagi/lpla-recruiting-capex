# Load the Nasdaq daily closes saved in data/nasdaq (pulled 23 Nov 2026).
import os, csv, datetime as dt
HERE = os.path.dirname(os.path.abspath(__file__))

def closes(sym):
    with open(os.path.join(HERE, "..", "data", "nasdaq", f"{sym}.csv")) as f:
        return {dt.datetime.strptime(r["date"], "%m/%d/%Y").date(): float(r["close"]) for r in csv.DictReader(f)}
