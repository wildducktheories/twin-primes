"""Generate figures for the Bridging Conjecture paper appendix."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'lib'))

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

from twin_primes import prime_sieve, A002822, middle_number_pairs
from twin_primes.terminology import COLOURS

# ── data ─────────────────────────────────────────────────────────────────────

LIMIT = 5000
D = {1, 16, 67, 86, 131, 151, 186, 191, 211, 226, 541, 701}

sieve = prime_sieve(6 * LIMIT + 1)
a002822 = sorted(w for w in range(1, LIMIT + 1) if sieve[6*w-1] and sieve[6*w+1])
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
ax.scatter(A[1:], ratios, s=1, alpha=0.25, color=COLOURS['primary'],
           label=r'gap$(n)/w_{n+1}$')
ax.plot(roll_x, rolling_mean, color=COLOURS['prediction'], linewidth=1.5,
        label=f'Rolling mean (window={window})')
ax.axhline(y=0.5, color=COLOURS['anomaly'], linestyle='--', linewidth=1,
           label='bridging conjecture bound (gap$/w < 1/2$)')
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('$w_{n+1}$')
ax.set_ylabel(r'gap$(n) / w_{n+1}$')
ax.set_title('Gap ratio for consecutive elements of $A002822$')
ax.legend(fontsize=8, markerscale=4)
fig.tight_layout()
fig.savefig('gap_ratio.pdf', dpi=150)
plt.close(fig)
print("gap_ratio.pdf written")

# ── Figure 2: Decomposition gap ratio ────────────────────────────────────────

import matplotlib.colors as mcolors

# Build a linear red→blue colourmap matching the terminology scheme
cmap_rb = mcolors.LinearSegmentedColormap.from_list(
    'rb', [COLOURS['anomaly'], COLOURS['surface']]
)

xs_all, ys_all, cs_all = [], [], []
xs_D, ys_D = [], []

for w in a002822:
    decomps = pairs.get(w, [])
    if not decomps:
        xs_D.append(w)
        ys_D.append(1.0)
        continue
    for (u, v) in decomps:
        ratio = (v - u) / w
        xs_all.append(w)
        ys_all.append(ratio)
        cs_all.append(ratio)   # colour by own g/w: high→red, low→blue

for w in D:
    if w not in a002822_set:
        xs_D.append(w)
        ys_D.append(1.0)

fig, ax = plt.subplots(figsize=(7, 4))
sc = ax.scatter(xs_all, ys_all, s=2, alpha=0.5, c=cs_all,
                cmap=cmap_rb, vmin=0, vmax=1)
ax.scatter(xs_D, ys_D, s=20, alpha=0.9, color=COLOURS['satellite'],
           marker='x', linewidths=0.8, label=r'$\mathcal{X}$ (A243956, $r = 1$)')
ax.axhline(y=1.0, color=COLOURS['anomaly'], linestyle='--', linewidth=0.8, alpha=0.5)
cbar = fig.colorbar(sc, ax=ax, pad=0.02)
cbar.set_label(r'$r$ (lopsided $\to$ balanced)', fontsize=8)
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('$w$')
ax.set_ylabel(r'$r = (v-u)/w$')
ax.set_title(r'Decomposition gap ratio $r$ for $A002822 \cup \mathcal{X}$')
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig('decomp_gap_ratio.pdf', dpi=150)
plt.close(fig)
print("decomp_gap_ratio.pdf written")

# ── Figure 3: Ratio of smallest to largest gap ratio ─────────────────────────
# For each w with at least 2 decompositions, plot r_min/r_max where r = (v-u)/w.
# A value approaching 1 means all decompositions have nearly equal gap ratios —
# the dangerous case where u ≈ v ≈ w/2 for every decomposition, threatening
# the 2V gap bound. Staying well below 1 confirms the spread continues to grow.

xs_ratio, ys_ratio = [], []

for w in a002822:
    decomps = pairs.get(w, [])
    if len(decomps) < 2:
        continue
    raw_gaps = [v - u for (u, v) in decomps]
    max_gap = max(raw_gaps)
    min_gap = min(raw_gaps)
    if max_gap > 0:
        xs_ratio.append(w)
        ys_ratio.append(min_gap / max_gap)

fig3, ax3 = plt.subplots(figsize=(7, 4))
ax3.scatter(xs_ratio, ys_ratio, s=2, alpha=0.4, color=COLOURS['primary'],
            label=r'$r_{\min} / r_{\max}$')
ax3.axhline(y=1.0, color=COLOURS['anomaly'], linestyle='--', linewidth=0.8, alpha=0.6,
            label='ratio = 1 (all decompositions equally balanced)')
ax3.set_xscale('log')
ax3.set_yscale('log')
ax3.set_xlabel('$w$')
ax3.set_ylabel(r'$r_{\min} / r_{\max}$')
ax3.set_title(r'Ratio of smallest to largest gap ratio $r$ for $A002822$')
ax3.legend(fontsize=8)
fig3.tight_layout()
fig3.savefig('decomp_gap_ratio_spread.pdf', dpi=150)
plt.close(fig3)
print("decomp_gap_ratio_spread.pdf written")
