# Where did Commonwealth's client cash go when LPL bought it (closed 1 Aug 2025)?
# LPL's Q3 2025 release: total client cash of $56bn "included $4 billion resulting from the acquisition of Commonwealth",
# and the client cash table has only ICA, DCA, money market sweep and CCA lines. The monthly columns show when each line moved.
from common import rows
r = list(rows("client_cash_monthly_2025q3.csv"))
for a, b in zip(r, r[1:]):
    print(f"{b['month_end']}: DCA {float(b['dca_bn'])-float(a['dca_bn']):+.1f}bn, ICA {float(b['ica_bn'])-float(a['ica_bn']):+.1f}bn, "
          f"money market sweep {float(b['money_market_sweep_bn'])-float(a['money_market_sweep_bn']):+.1f}bn, total {float(b['total_client_cash_bn'])-float(a['total_client_cash_bn']):+.1f}bn")
print("July 2025, the month LPL completed Atria's conversion: DCA flat at $10.8bn")
print("August 2025, the month Commonwealth closed: DCA +$1.4bn, total client cash +$3.2bn")
print("so Commonwealth's client cash has been reported inside LPL's sweep lines, DCA included, since August 2025, well before its accounts converted in November 2026")
