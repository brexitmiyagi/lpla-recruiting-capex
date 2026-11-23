# Builds results/LPLA-scenario-model.xlsx: a front sheet with toggles (yellow cells) and live formulas,
# plus the fee schedule, my quarterly model, the DCA history and the deposit benchmarks.
import os, io, contextlib
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from common import rows
with contextlib.redirect_stdout(io.StringIO()):
    import valuation as V
from eps_model import run
HERE = os.path.dirname(os.path.abspath(__file__))

base = run()
fwd0 = V.fwd_eps(base)
per100 = fwd0 - V.fwd_eps(run(dict(sweep_giveback_pretax_yr=100)))
fed25 = V.fwd_eps(run(dict(fed_change_bp=25))) - fwd0
sp10 = V.fwd_eps(run(dict(initial_asset_shock=-0.045 + 0.05))) - fwd0
sh27 = sum(q["shares"] for q in base["quarters"][1:5]) / 4

wb = Workbook(); ws = wb.active; ws.title = "Start here"
IN = PatternFill("solid", fgColor="FFF2CC"); B = Font(bold=True); BL = Font(color="0000FF"); H = Font(bold=True, size=13)
ws.column_dimensions["A"].width = 62; ws.column_dimensions["B"].width = 16; ws.column_dimensions["C"].width = 60
ws["A1"] = "LPLA scenario model (Sameer Shahzad). Change the yellow cells; everything else recalculates."; ws["A1"].font = H
ws["A2"] = "Prices: Nov 20, 2026 close. Base EPS sensitivities come from scripts/eps_model.py; see the repo for the full quarterly build."

r = 4
def section(t):
    global r; ws.cell(r, 1, t).font = B; r += 1
def inp(label, val, note="", fmt=None):
    global r; c = ws.cell(r, 2, val); c.fill = IN; c.font = BL
    if fmt: c.number_format = fmt
    ws.cell(r, 1, label); ws.cell(r, 3, note); r += 1; return f"B{r-1}"
def out(label, formula, note="", fmt=None, bold=False):
    global r; c = ws.cell(r, 2, formula)
    if fmt: c.number_format = fmt
    ws.cell(r, 1, label).font = B if bold else Font(); c.font = B if bold else Font(); ws.cell(r, 3, note); r += 1; return f"B{r-1}"

section("Market and valuation inputs")
price = inp("LPLA price ($)", 264.56, "Nov 20, 2026 close (Nasdaq)", "0.00")
div = inp("Dividend, next 12 months ($)", 1.20, "$0.30 a quarter", "0.00")
ke = inp("Cost of equity", round(V.ke, 4), "10-year 5.04% + 0.90 beta x 5% premium", "0.00%")
pe = inp("Forward P/E used for value a year out", 11.54, "LPLA 25th percentile since 2017; median is 13.56", "0.00")
lit = inp("Expected litigation cost ($ a share, after tax)", 3.95, "scripts/damages.py", "0.00")
fed = inp("Fed funds change from today (bp)", 0, "+ or -; feeds both the EPS and the DCA fee", "0")
sp = inp("S&P 500 move from Nov 20 (%)", 0, "client assets move about half as much", "0%")

section("DCA (advisory IRA cash) inputs")
fft = inp("Fed funds target midpoint today (bp)", 387.5, "3.75%-4.00% range", "0.0")
accts = inp("DCA accounts (millions)", 2.38, "derived from LPL revenue and the 2023 fee schedule; not reported", "0.00")
bal = inp("Average DCA balance per account ($)", 6346, "derived; Q3 2026", "#,##0")
client = inp("Client rate on DCA", 0.003, "Dec 12, 2025 rate sheet (still posted)", "0.00%")
tax = inp("Tax rate", 0.265, "Q3 2026 adjusted", "0.0%")
shares = inp("Diluted shares, 2027 average (m)", round(sh27, 2), "after $300m a quarter of buybacks", "0.00")
cut = inp("Extra DCA fee cut applied in every case (%)", 0, "e.g. 25% or 50%; 0% = schedule as is", "0%")
sched_shift = inp("Fee schedule override ($/month, blank = use schedule)", None, "leave empty to use the 2023 schedule")

section("Sweep outcome inputs")
pool = inp("Advisory cash pool ($bn)", 25.2, "DCA $16.0bn + half of a proportional advisory ICA share", "0.0")
lplr = inp("LPL advisory client rate today", 0.003, "", "0.00%")
osaic = inp("Osaic advisory IRA rate (case B)", 0.0058, "NFS sheet Nov 1, 2026", "0.00%")
merrill = inp("Merrill advisory rate (cases C2 and C)", 0.0335, "rate sheet Nov 20, 2026", "0.00%")
offset = inp("Share of give-back won back in platform fees (C2)", 0.5, "", "0%")
wA = inp("Weight A: no change", 0.25, "", "0%"); wB = inp("Weight B: Osaic level", 0.35, "", "0%")
wC2 = inp("Weight C2: wirehouse, half offset", 0.25, "", "0%"); wC = inp("Weight C: wirehouse, nothing offset", 0.15, "", "0%")

section("Model sensitivities (from eps_model.py, fixed)")
f0 = out("Forward adj EPS a year out, no change (Q4 27-Q3 28)", round(fwd0, 4), "", "0.00")
p100 = out("Forward EPS lost per $100m a year of pre-tax give-back", round(per100, 4), "", "0.000")
f25 = out("Forward EPS change per +25 bp Fed move", round(fed25, 4), "", "0.000")
s10 = out("Forward EPS change per +10% S&P move", round(sp10, 4), "", "0.000")

section("DCA economics (live)")
fee = out("LPL monthly fee per account ($)", f"=IF(ISBLANK({sched_shift}),VLOOKUP({fft}+{fed},'Fee schedule'!A2:C25,3,TRUE),{sched_shift})", "2023 schedule, looked up at today's target plus the Fed change", "0.00")
rev = out("DCA fee revenue ($m a year, pre-tax)", f"={accts}*{fee}*12", "", "#,##0")
ps = out("DCA fee, $ a share after tax", f"={rev}*(1-{tax})/{shares}", "", "0.00")
pct = out("Fee as % of average balance", f"={fee}*12/{bal}", "", "0.00%")
bank = out("Minimum banks must pay (fee + client rate)", f"={pct}+{client}", "", "0.00%")
out("... as % of fed funds", f"={bank}/(({fft}+{fed})/10000)", "", "0%", True)

section("Values a year out (live)")
gbB = out("Give-back B ($m pre-tax)", f"={pool}*1000*({osaic}-{lplr})", "", "#,##0")
gbC = out("Give-back C ($m pre-tax)", f"={pool}*1000*({merrill}-{lplr})", "", "#,##0")
extra = out("Extra fee cut ($m pre-tax, all cases)", f"={rev}*{cut}", "", "#,##0")
adj = out("Forward EPS, no change, after Fed and S&P toggles", f"={f0}+{f25}*{fed}/25+{s10}*{sp}/0.1", "", "0.00")
def case(label, gbexpr):
    return out(label, f"=({adj}-{p100}*({gbexpr}+{extra})/100)*{pe}-{lit}", "", "$0.00")
vA = case("A: no change", "0"); vB = case("B: Osaic level", gbB)
vC2 = case("C2: wirehouse level, part offset", f"{gbC}*(1-{offset})"); vC = case("C: wirehouse level, nothing offset", gbC)
w = out("Probability-weighted value", f"={wA}*{vA}+{wB}*{vB}+{wC2}*{vC2}+{wC}*{vC}", "", "$0.00", True)
out("Total return vs price, with dividend", f"=({w}+{div})/{price}-1", "BUY needs 15% and case C no worse than -10%", "0.0%", True)
out("Case C vs price", f"={vC}/{price}-1", "", "0.0%")
out("Buy below (15% total return)", f"=({w}+{div})/1.15", "", "$0.00")

section("What today's price assumes (live)")
gimp = out("Give-back the price implies ($m a year, pre-tax)", f"=(({adj}-{p100}*{extra}/100)*{pe}-{lit}-({price}*(1+{ke})-{div}))/({pe}*{p100}/100)", "solves value today = price", "#,##0")
out("... as a share of the DCA fee", f"={gimp}/{rev}", "", "0%", True)

# fee schedule sheet
fs = wb.create_sheet("Fee schedule"); fs.append(["FFT low (bp)", "FFT high (bp)", "LPL monthly fee per account ($)", "Source"])
for x in rows("dca_fee_schedule_2023.csv"):
    fs.append([float(x["fft_low_bps"]), float(x["fft_high_bps"]), float(x["lpl_monthly_fee_per_account"]), x["source"]])
# quarterly model
qs = wb.create_sheet("My quarters")
keys = ["q", "assets_bn", "client_cash", "gp", "core_ga", "ta", "promo", "da", "interest", "adj_pretax", "adj_ni", "shares", "eps"]
qs.append(keys)
for q in base["quarters"]: qs.append([round(q[k], 3) if isinstance(q[k], float) else q[k] for k in keys])
cons = rows("consensus_quarterly.csv"); qs.append([]); qs.append(["Consensus (Nasdaq/Zacks, Nov 23)"]); [qs.append([c["quarter"], float(c["consensus_adj_eps"])]) for c in cons]
# DCA history and benchmarks
dh = wb.create_sheet("Sweep history"); src = rows("sweep_yields_quarterly.csv"); k=[c for c in src[0].keys() if c]; dh.append(k); [dh.append([x[c] for c in k]) for x in src]
bm = wb.create_sheet("Deposit benchmarks"); src = rows("deposit_benchmarks.csv"); k=[c for c in src[0].keys() if c]; bm.append(k); [bm.append([x[c] for c in k]) for x in src]
pm = wb.create_sheet("Peers"); src = rows("peer_multiples.csv"); k=[c for c in src[0].keys() if c]; pm.append(k); [pm.append([x[c] for c in k]) for x in src]
out_path = os.path.join(HERE, "..", "results", "LPLA-scenario-model.xlsx"); wb.save(out_path); print("saved results/LPLA-scenario-model.xlsx")
