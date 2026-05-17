"""Generate figures for the Bridging Conjecture paper appendix."""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

# ── helpers ──────────────────────────────────────────────────────────────────

def sieve_primes(n):
    sieve = bytearray([1]) * (n + 1)
    sieve[0] = sieve[1] = 0
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            sieve[i*i::i] = bytearray(len(sieve[i*i::i]))
    return sieve

def build_A002822(limit):
    """Return sorted list of m such that 6m-1 and 6m+1 are both prime."""
    top = 6 * limit + 2
    sieve = sieve_primes(top)
    return [m for m in range(1, limit + 1)
            if sieve[6*m - 1] and sieve[6*m + 1]]

# ── data ─────────────────────────────────────────────────────────────────────

LIMIT = 100_000
A = build_A002822(LIMIT)
A_set = set(A)

# ── Figure 1: Gap ratio ───────────────────────────────────────────────────────

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
ax.set_ylabel('gap$(n) / m_{n+1}$')
ax.set_title('Gap ratio for consecutive elements of $A002822$')
ax.legend(fontsize=8, markerscale=4)
fig.tight_layout()
fig.savefig('gap_ratio.pdf', dpi=150)
plt.close(fig)
print("gap_ratio.pdf written")

# ── Figure 2: Decomposition count ────────────────────────────────────────────

# For each m in A, count pairs (a, b) with a <= b, a+b = m, a,b in A_set
# Only go to 20000 to keep it tractable; pairs is O(|A|^2) naively
DECOMP_LIMIT = 20_000
A_small = [m for m in A if m <= DECOMP_LIMIT]
A_small_set = set(A_small)

decomp_m = []
decomp_count = []
for m in A_small:
    if m <= 1:
        continue
    count = sum(1 for a in A_small if a < m and (m - a) in A_small_set and a <= m - a)
    decomp_m.append(m)
    decomp_count.append(count)

decomp_m = np.array(decomp_m)
decomp_count = np.array(decomp_count)

# reference curve c * m / (log m)^2, scaled to match data mean
mask = decomp_m > 10
ref = decomp_m[mask] / (np.log(decomp_m[mask])**2)
scale = np.mean(decomp_count[mask]) / np.mean(ref)
ref_scaled = scale * ref

window2 = 100
roll2 = np.convolve(decomp_count, np.ones(window2)/window2, mode='valid')
roll2_x = decomp_m[window2//2 : window2//2 + len(roll2)]

fig2, ax2 = plt.subplots(figsize=(7, 4))
ax2.scatter(decomp_m, decomp_count, s=1, alpha=0.25, color='steelblue',
            label='Decomposition count')
ax2.plot(roll2_x, roll2, color='darkorange', linewidth=1.5,
         label=f'Rolling mean (window={window2})')
ax2.plot(decomp_m[mask], ref_scaled, color='green', linestyle='--', linewidth=1,
         label=r'$c \cdot m / (\log m)^2$ reference')
ax2.set_xlabel('$m$')
ax2.set_ylabel('Number of decompositions')
ax2.set_title('Middle number decomposition count for $A002822$')
ax2.legend(fontsize=8, markerscale=4)
fig2.tight_layout()
fig2.savefig('decomp_count.pdf', dpi=150)
plt.close(fig2)
print("decomp_count.pdf written")
