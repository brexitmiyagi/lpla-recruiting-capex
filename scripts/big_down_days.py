# Every LPLA day worse than -10% in the Nasdaq history I pulled (Nov 2016 to Nov 2026), and the next 12 months.
from common import rows

for r in rows("big_down_days.csv"):
    nxt = f"{float(r['next_12m_pct']):+.1f}% over the next 12 months" if r["next_12m_pct"] else "n/a yet"
    print(f"{r['date']}: {float(r['one_day_move_pct']):+.1f}% to ${float(r['close']):.2f}, {nxt} ({r['note']})")
