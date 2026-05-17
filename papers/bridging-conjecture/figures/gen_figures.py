"""Generate figures for the Bridging Conjecture paper appendix."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'lib'))

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

from twin_primes import prime_sieve, A002822, middle_number_pairs

# ── data ─────────────────────────────────────────────────────────────────────

LIMIT = 5000
D = {1, 16, 67, 86, 131, 151, 186, 191, 211, 226, 541, 701}

sieve = prime_sieve(6 * LIMIT + 1)
a002822 = sorted(m for m in range(1, LIMIT + 1) if sieve[6*m-1] and sieve[6*m+1])
a002822_set = set(a002822)
pairs = middle_number_pairs(LIMIT)

# ── Figure 1: Consecutive gap ratio ─────────────────────────────────────────

GAP_LIMIT = 10_000
gap_sieve = prime_sieve(6 * GAP_LIMIT + 1)
A = list(A002822(range(1, GAP_LIMIT + 1), gap_sieve))

gaps = [A[i+1] - A[i] for i in range(len(A) - 1)]
ratios = [g / A[i+1] for i, g in enumerate(gaps)]

window = 200
rolling_mean = np.convolve(ratios, np.ones(window)/window, mode='valid')
roll_x = A[window//2 : window//2 + len(rolling_mean)]

fig, ax = plt.subplots(figsize=(7, 4))
ax.scatter(A[1:], ratios, s=1, alpha=0.25, color='steelblue', label='gap/m_{n+1}')
ax.plot(roll_x, rolling_mean, color='darkorange', linewidth=1.5,
        label=f'Rolling mean (window={window})')
ax.axhline(y=0.5, color='red', linestyle='--', linewidth=1,
           label='Bridging Conjecture bound (gap/m < 1/2)')
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('$m_{n+1}$')
ax.set_ylabel(r'gap$(n) / m_{n+1}$')
ax.set_title('Gap ratio for consecutive elements of $A002822$')
ax.legend(fontsize=8, markerscale=4)
fig.tight_layout()
fig.savefig('gap_ratio.pdf', dpi=150)
plt.close(fig)
print("gap_ratio.pdf written")

# ── Figure 2: Decomposition gap ratio ────────────────────────────────────────

xs_inner, ys_inner = [], []
xs_largest, ys_largest = [], []
xs_smallest, ys_smallest = [], []
xs_D, ys_D = [], []

for m in a002822:
    decomps = pairs.get(m, [])
    if not decomps:
        xs_D.append(m)
        ys_D.append(1.0)
        continue
    gaps = [(b - a, a, b) for (a, b) in decomps]
    max_gap = max(g for g, _, _ in gaps)
    min_gap = min(g for g, _, _ in gaps)
    for g, a, b in gaps:
        ratio = g / m
        if g == max_gap:
            xs_largest.append(m)
            ys_largest.append(ratio)
        elif g == min_gap:
            xs_smallest.append(m)
            ys_smallest.append(ratio)
        else:
            xs_inner.append(m)
            ys_inner.append(ratio)

for m in D:
    if m not in a002822_set:
        xs_D.append(m)
        ys_D.append(1.0)

fig, ax = plt.subplots(figsize=(7, 4))
ax.scatter(xs_inner, ys_inner, s=1, alpha=0.3, color='steelblue',
           label='Decompositions (inner)')
ax.scatter(xs_largest, ys_largest, s=4, alpha=0.6, color='darkorange',
           label='Largest-gap decomposition')
ax.scatter(xs_smallest, ys_smallest, s=4, alpha=0.6, color='green',
           label='Smallest-gap decomposition')
ax.scatter(xs_D, ys_D, s=12, alpha=0.8, color='red', marker='x',
           label=r'A243956 (trivial: $g/m = 1$)')
ax.axhline(y=1.0, color='red', linestyle='--', linewidth=0.8, alpha=0.5)
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('$m$')
ax.set_ylabel(r'$g / m$,\ \ $g = b - a$')
ax.set_title(r'Decomposition gap ratio for $A002822 \cup A243956$')
ax.legend(fontsize=8, markerscale=3)
fig.tight_layout()
fig.savefig('decomp_gap_ratio.pdf', dpi=150)
plt.close(fig)
print("decomp_gap_ratio.pdf written")

# ── Figure 3: Ratio of smallest to largest decomposition gap ─────────────────
# For each m with at least 2 decompositions, plot g_min/g_max where g = b-a.
# A value approaching 1 means all decompositions have nearly equal gaps —
# the dangerous case where a ≈ b ≈ m/2 for every decomposition, threatening
# the 2K gap bound. Staying well below 1 confirms the spread continues to grow.

xs_ratio, ys_ratio = [], []

for m in a002822:
    decomps = pairs.get(m, [])
    if len(decomps) < 2:
        continue
    gaps = [b - a for (a, b) in decomps]
    max_gap = max(gaps)
    min_gap = min(gaps)
    if max_gap > 0:
        xs_ratio.append(m)
        ys_ratio.append(min_gap / max_gap)

fig3, ax3 = plt.subplots(figsize=(7, 4))
ax3.scatter(xs_ratio, ys_ratio, s=2, alpha=0.4, color='steelblue',
            label=r'$g_{\min} / g_{\max}$')
ax3.axhline(y=1.0, color='red', linestyle='--', linewidth=0.8, alpha=0.6,
            label='ratio = 1 (all decompositions equally balanced)')
ax3.set_xscale('log')
ax3.set_yscale('log')
ax3.set_xlabel('$m$')
ax3.set_ylabel(r'$g_{\min} / g_{\max}$')
ax3.set_title(r'Ratio of Smallest to Largest Decomposition Gap for $A002822$')
ax3.legend(fontsize=8)
fig3.tight_layout()
fig3.savefig('decomp_gap_ratio_spread.pdf', dpi=150)
plt.close(fig3)
print("decomp_gap_ratio_spread.pdf written")
