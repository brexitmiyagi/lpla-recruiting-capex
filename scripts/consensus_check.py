# Has consensus moved since the November 20 sell-off?
from common import kv
c = kv("consensus_momentum_2026-11-23.csv")
print(f"2027 consensus ${c['fy2027_consensus']:.2f}: over the last four weeks {int(c['fy2027_revisions_down_4wk'])} of {int(c['fy2027_estimates'])} estimates went down, {int(c['fy2027_revisions_up_4wk'])} up (mostly after the Oct 27 Q3 report)")
print(f"Q4 2026 consensus ${c['q4_2026_consensus_1mo_ago']:.2f} a month ago, ${c['q4_2026_consensus_1wk_ago']:.2f} a week ago, ${c['q4_2026_consensus_now']:.2f} now")
print(f"2026 consensus ${c['fy2026_consensus_1mo_ago']:.2f} a month ago, ${c['fy2026_consensus_1wk_ago']:.2f} a week ago, ${c['fy2026_consensus_now']:.2f} now")
print("so analysts cut after the Q3 report, but nothing has moved in the week that includes the November 20 drop")
