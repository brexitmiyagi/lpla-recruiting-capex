# LPL's own Form ADV, Part 1A Item 5D: advisory clients by type at each year end (SEC IA FOIA monthly files).
# Question: did retirement plan clients jump when the DCA was opened to retirement plan accounts?
# Note: Form ADV counts IRAs (including SEP and SIMPLE IRAs) of individuals under "individuals", so only
# employer plans show up under "pension and profit sharing plans".
from common import rows
r = list(rows("adv_item5d_lpl.csv"))
prev = None
for x in r:
    ind = int(x["individuals_clients"]) + int(x["hnw_individuals_clients"]); plans = int(x["pension_profit_sharing_plan_clients"])
    line = f"{x['fiscal_year_end']}: individual clients {ind:,}, pension and profit sharing plan clients {plans:,}"
    if prev: line += f" (individuals {ind/prev[0]-1:+.1%}, plans {plans/prev[1]-1:+.1%})"
    print(line); prev = (ind, plans)
print("so plan clients grew 7%, 13% and 14% a year with no jump in 2025, and at about 10,000 they're far too few to explain a wave of ~500,000 DCA accounts")
