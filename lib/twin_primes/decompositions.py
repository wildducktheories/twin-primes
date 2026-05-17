from .sieve import prime_sieve
from .sequences import A002822, A067611


def middle_number_pairs(n):
    """For each twin prime cofactor m in A002822(1..n), find all pairs (a, b)
    of smaller twin prime cofactors such that a + b == m.
    Returns a dict mapping m -> list of (a, b) pairs.
    """
    sieve = prime_sieve(6*n + 1)
    centers = [m for m in range(1, n+1) if sieve[6*m-1] and sieve[6*m+1]]
    center_set = set(centers)

    result = {}
    for m in centers:
        pairs = []
        for a in centers:
            if a >= m:
                break
            b = m - a
            if b in center_set and b >= a:
                pairs.append((a, b))
        result[m] = pairs
    return result


def generate_from_seeds(seeds, N):
    """Starting from a seed set, repeatedly take the largest unprocessed member m_max,
    add it to each smaller member, and admit the sum if its residue mod 5 is in {0,2,3}.
    Continue until all members exceed N.

    Returns the generated set M.
    """
    M = sorted(seeds)
    M_set = set(M)
    processed = set()

    while True:
        remaining = [m for m in M if m not in processed and m <= N]
        if not remaining:
            break
        m_max = max(remaining)
        processed.add(m_max)
        for m_i in [m for m in M if m < m_max]:
            s = m_max + m_i
            if s <= N and s % 5 in {0, 2, 3} and s not in M_set:
                M_set.add(s)
                M = sorted(M_set)

    return M_set


def compare_to_a002822(seeds, N=300):
    sieve = prime_sieve(6*N + 1)
    a002822 = set(A002822(range(1, N+1), sieve))

    M = generate_from_seeds(seeds, N)

    in_M_not_a = sorted(M - a002822)
    in_a_not_M = sorted(a002822 - M)

    print(f"Seeds: {sorted(seeds)},  N={N}")
    print(f"  Generated |M| = {len(M)},  |A002822| = {len(a002822)}")
    print(f"  In M but not A002822 ({len(in_M_not_a)}): {in_M_not_a[:20]}{'...' if len(in_M_not_a)>20 else ''}")
    print(f"  In A002822 but not M ({len(in_a_not_M)}): {in_a_not_M[:20]}{'...' if len(in_a_not_M)>20 else ''}")

    if in_a_not_M:
        print(f"\n  A002822 \\ M — middle number decompositions within A002822:")
        for m in in_a_not_M[:15]:
            decomps = [(a, m-a) for a in sorted(a002822) if a < m and (m-a) in a002822]
            print(f"    m={m} (mod5={m%5}): {decomps[:4]}{'...' if len(decomps)>4 else ''}")
