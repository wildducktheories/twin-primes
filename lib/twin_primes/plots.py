import matplotlib.pyplot as plt
import numpy as np

from .sieve import prime_sieve
from .sequences import A002822, a002822_augmented
from .decompositions import middle_number_pairs


def plot_gap_ratio_bound(N=5000):
    """Plot m_{n+1}/m_n for A002822 elements to verify the gap bound m_{n+1} < 2*m_n
    implied by the Bridging Conjecture. All ratios should be strictly less than 2.
    """
    sieve = prime_sieve(6*N + 1)
    seq = [m for m in range(1, N+1) if sieve[6*m-1] and sieve[6*m+1]]

    ratios = [seq[i+1] / seq[i] for i in range(len(seq)-1)]
    indices = list(range(1, len(ratios)+1))

    window = max(1, len(ratios) // 50)
    trend = np.convolve(ratios, np.ones(window)/window, mode='valid')
    trend_x = indices[window//2: window//2 + len(trend)]

    fig, ax = plt.subplots(figsize=(12, 4))
    ax.scatter(indices, ratios, s=1, color='steelblue', alpha=0.3, label='m_{n+1}/m_n')
    ax.plot(trend_x, trend, color='navy', linewidth=1.2, label=f'Rolling mean (window={window})')
    ax.axhline(y=2.0, color='red', linestyle='--', linewidth=1, label='Bound: ratio = 2')
    ax.axhline(y=1.0, color='gray', linestyle=':', linewidth=0.8)
    ax.set_xlabel('n')
    ax.set_ylabel('m_{n+1} / m_n')
    ax.set_title(f'Consecutive ratio m_{{n+1}}/m_n for A002822 (up to m={seq[-1]})')
    ax.legend()
    ax.set_ylim(0.9, 2.1)
    plt.tight_layout()
    plt.show()

    max_ratio = max(ratios)
    print(f"Maximum consecutive ratio: {max_ratio:.6f}  (bound: < 2.0)")
    print(f"All ratios < 2: {all(r < 2 for r in ratios)}")
    print(f"Elements checked: {len(seq)}, largest: {seq[-1]}")


def plot_gap_ratio(n=10000):
    """Plot the ratio of the gap between successive A002822 elements
    to the second (larger) element, on a logarithmic y-scale.
    The dashed line at 1/2 marks the bound implied by the Bridging Conjecture:
    m_{n+1} < 2*m_n is equivalent to gap/m_{n+1} < 1/2.
    """
    sieve = prime_sieve(6*n + 1)
    centers = sorted(A002822(range(1, n+1), sieve))

    second = centers[1:]
    gaps = [b - a for a, b in zip(centers, second)]
    ratios = [g / b for g, b in zip(gaps, second)]

    window = max(1, len(ratios) // 25)
    trend = np.convolve(ratios, np.ones(window)/window, mode='valid')
    trend_x = [second[i] for i in range(window//2, window//2 + len(trend))]

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(second, ratios, lw=0.4, color='steelblue', alpha=0.6, label='gap / m')
    ax.plot(trend_x, trend, color='navy', lw=1.5, label=f'Rolling mean (window={window})')
    ax.axhline(y=0.5, color='red', linestyle='--', linewidth=1,
               label='Bridging Conjecture bound (gap/m < 1/2)')
    ax.set_yscale('log')
    ax.set_xlabel('m (second element)')
    ax.set_ylabel('gap / m  (log scale)')
    ax.set_title(f'Gap ratio between successive A002822 elements (n={n})')
    ax.legend()
    plt.tight_layout()
    plt.show()


def plot_decomposition_count(n=10000):
    """Plot the number of ways each A002822 element m can be decomposed
    as a sum of two smaller A002822 elements, as a function of m.
    """
    pairs = middle_number_pairs(n)
    ms = sorted(pairs.keys())
    counts = [len(pairs[m]) for m in ms]

    window = max(1, len(ms) // 25)
    trend = np.convolve(counts, np.ones(window)/window, mode='valid')
    trend_x = [ms[i] for i in range(window//2, window//2 + len(trend))]

    ms_arr = np.array(ms, dtype=float)
    ref = ms_arr / np.log(ms_arr)**2
    mid = len(trend) // 2
    scale = trend[mid] / (trend_x[mid] / np.log(trend_x[mid])**2) if trend_x[mid] > 1 else 1.0
    ref_scaled = scale * ref

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(ms, counts, lw=0.4, color='purple', alpha=0.5, label='decomposition count')
    ax.plot(trend_x, trend, color='indigo', lw=1.5, label=f'Rolling mean (window={window})')
    ax.plot(ms, ref_scaled, color='orange', lw=1.2, linestyle='--',
            label=r'$c \cdot m / \log^2 m$ (Goldbach analogy)')
    ax.set_xlabel('m')
    ax.set_ylabel('number of decompositions')
    ax.set_title(f'Number of ways to write m as a sum of two A002822 elements (n={n})')
    ax.legend()
    plt.tight_layout()
    plt.show()


def plot_xy_for_m(m, n=None):
    """Plot the x-y plane for all tuples with the given twin prime cofactor m,
    and overlay the witness (x,y) coordinates for each member of every
    middle-number decomposition (p, q) where p + q == m.

    Green stars:    c > 0 (witness from m-1 neighbour).
    Red stars:      c < 0 (witness from m+1 neighbour).
    Teal/salmon dots: witnesses for p or q, coloured by their own c value.
    """
    if n is None:
        n = m + 1
    all_tuples = list(a002822_augmented(n))
    tuples_for = {}
    for t in all_tuples:
        tuples_for.setdefault(t["m"], []).append(t)

    tuples = tuples_for.get(m, [])
    if not tuples:
        print(f"No tuples found for m={m} (is {6*m-1},{6*m+1} a twin prime pair?)")
        return

    pairs = middle_number_pairs(n).get(m, [])

    cx = sum(t["x"] for t in tuples) / len(tuples)
    cy = sum(t["y"] for t in tuples) / len(tuples)

    fig, ax = plt.subplots(figsize=(6, 6))

    for t in tuples:
        color = "green" if t["c"] > 0 else "red"
        ax.scatter(t["x"], t["y"], color=color, marker="*", s=80, zorder=2)
        ax.annotate(f'({t["x"]},{t["y"]})', (t["x"], t["y"]),
                    textcoords="offset points", xytext=(4, 4), fontsize=7)

    for (p, q) in pairs:
        p_tuples = tuples_for.get(p, [])
        q_tuples = tuples_for.get(q, [])
        for member, member_tuples in ((p, p_tuples), (q, q_tuples)):
            for t in member_tuples:
                color = "teal" if t["c"] > 0 else "salmon"
                ax.scatter(t["x"], t["y"], color=color, marker=".", s=15, zorder=3)
                ax.annotate(f'{member}:({t["x"]},{t["y"]})', (t["x"], t["y"]),
                            textcoords="offset points", xytext=(4, -10), fontsize=7, color=color)
        for tp in p_tuples:
            for tq in q_tuples:
                ax.plot([tp["x"], tq["x"]], [tp["y"], tq["y"]],
                        color="blue", lw=0.4, alpha=0.5, zorder=1)

    ax.axhline(0, color="grey", linewidth=0.5)
    ax.axvline(0, color="grey", linewidth=0.5)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(f"Witnesses for m={m}  ({6*m-1}, {6*m+1})\n"
                 f"star green=c>0, red=c<0  ·  dot teal=summand c>0, salmon=summand c<0")
    ax.legend(handles=[
        plt.Line2D([0],[0], marker='*', color='w', markerfacecolor='green',  markersize=8, label='m: c>0'),
        plt.Line2D([0],[0], marker='*', color='w', markerfacecolor='red',    markersize=8, label='m: c<0'),
        plt.Line2D([0],[0], marker='.', color='w', markerfacecolor='teal',   markersize=8, label='summand: c>0'),
        plt.Line2D([0],[0], marker='.', color='w', markerfacecolor='salmon', markersize=8, label='summand: c<0'),
    ])
    plt.tight_layout()
    plt.show()
