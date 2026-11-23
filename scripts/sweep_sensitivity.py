# Client cash: what a Fed move and a pricing give-back each do to EPS.
from common import kv, ttm_tax_rate

c = kv("company_q3_2026.csv")
t = ttm_tax_rate()
sh = c["diluted_shares_q3_k"] / 1000
floating = c["ica_balance_bn"] * (1 - c["ica_fixed_share"])
print(f"TTM effective tax rate: {t:.1%}")
print(f"floating ICA ($bn): {floating:.1f}")
up = floating * 1e3 * 0.0025
print(f"+25bp on floating ICA, pre-tax ($m/yr): {up:.0f}, per share after tax: ${up*(1-t)/sh:.2f}")
give = c["bank_sweep_bn"] * 1e3 * 0.0025
print(f"25bp give-back on all bank sweep, pre-tax ($m/yr): {give:.1f}, per share after tax: ${give*(1-t)/sh:.2f}")
print(f"ICA yield Q3 (bps): {c['ica_yield_bps_q3']:.0f}, Q4 guided about +20")
