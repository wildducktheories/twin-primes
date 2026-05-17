from collections import Counter

from .sieve import prime_sieve
from .sequences import A002822, A067611
from .decompositions import generate_from_seeds, middle_number_pairs


def verify_wagler_mod5(n=10000):
    """Verify the mod-5 congruence constraints on middle number decompositions.

    Confirms:
    - A002822 elements > 1 have residues in {0, 2, 3} mod 5 only.
    - No middle number decomposition m0 + m1 = m2 has (m0 mod 5, m1 mod 5) in {(2,2),(3,3)}.
    - All other residue combinations do occur.
    """
    sieve = prime_sieve(6*n + 1)
    centers = [m for m in range(1, n+1) if sieve[6*m-1] and sieve[6*m+1]]
    center_set = set(centers)

    residues = Counter(m % 5 for m in centers if m > 1)
    print(f"Residues mod 5 for A002822 elements > 1 (n={n}):")
    for r in range(5):
        mark = "  <- forbidden" if r in {1, 4} else ""
        print(f"  r={r}: {residues[r]} elements{mark}")

    pair_counts = Counter()
    forbidden_found = []
    for m2 in centers:
        for m0 in centers:
            if m0 >= m2:
                break
            m1 = m2 - m0
            if m1 in center_set and m1 >= m0:
                r0, r1 = m0 % 5, m1 % 5
                pair_counts[(min(r0,r1), max(r0,r1))] += 1
                if (r0, r1) in {(2, 2), (3, 3)}:
                    forbidden_found.append((m0, m1, m2))

    print(f"\nUnordered residue pairs (r0, r1) in middle number decompositions:")
    for pair in sorted(pair_counts):
        r0, r1 = pair
        status = "FORBIDDEN (never occurs)" if pair in {(2,2),(3,3)} else "ok"
        print(f"  ({r0},{r1}): {pair_counts[pair]} decompositions  [{status}]")

    for pair in [(2,2),(3,3)]:
        if pair not in pair_counts:
            print(f"  {pair}: 0 decompositions  [FORBIDDEN — confirmed absent]")

    if forbidden_found:
        print(f"\nFORBIDDEN PAIRS FOUND: {forbidden_found[:5]}")
    else:
        print(f"\nConfirmed: no (2,2) or (3,3) residue pairs appear in any middle number decomposition.")


def verify_dubner_conjecture3(N=10000):
    """Verify Dubner's Conjecture 3 (set form): the positive integers with no
    representation as a sum i + j with i, j in A002822 are exactly:
      {1, 16, 67, 86, 131, 151, 186, 191, 211, 226, 541, 701}

    Checks all positive integers up to N and reports any exceptions beyond 701.
    """
    A243956 = {1, 16, 67, 86, 131, 151, 186, 191, 211, 226, 541, 701}

    sieve = prime_sieve(6*N + 1)
    a002822 = sorted(A002822(range(1, N+1), sieve))
    a002822_set = set(a002822)

    sumset = set()
    for i in a002822:
        for j in a002822:
            s = i + j
            if s > N:
                break
            sumset.add(s)

    exceptions = sorted(n for n in range(1, N+1) if n not in sumset)

    known = sorted(A243956)
    unexpected = [n for n in exceptions if n not in A243956]
    missing = [n for n in A243956 if n <= N and n not in exceptions]

    print(f"Checked n in [1, {N}]:")
    print(f"  Exceptions (not in sumset of A002822): {exceptions}")
    print(f"  Known A243956:                         {known}")
    print(f"  Unexpected exceptions beyond A243956:  {unexpected if unexpected else 'none'}")
    print(f"  A243956 members missing from exceptions: {missing if missing else 'none'}")
    if not unexpected and not missing:
        print(f"  Conjecture 3 verified up to N={N}.")


def verify_goldbach_twin(N=10000):
    """Verify Dubner's Conjecture 4a: every even n > 4208 is the sum of two t-primes.
    Also check the weaker form: at least one summand is a t-prime.

    Reports all exceptions to each form and example decompositions.
    """
    sieve = prime_sieve(2*N + 10)

    twin_primes = sorted(
        p for p in range(2, 2*N + 1)
        if sieve[p] and (
            (p - 2 >= 2 and sieve[p - 2]) or
            (p + 2 <= 2*N + 10 and sieve[p + 2])
        )
    )
    twin_set = set(twin_primes)

    weak_failures = []
    strong_failures = []

    for n in range(4, 2*N + 1, 2):
        weak_ok = False
        strong_ok = False
        for p in twin_primes:
            if p >= n:
                break
            q = n - p
            if q >= 2 and sieve[q]:
                weak_ok = True
                if q in twin_set:
                    strong_ok = True
                    break
        if not weak_ok:
            weak_failures.append(n)
        if not strong_ok:
            strong_failures.append(n)

    print(f"Checked even numbers from 4 to {2*N}.")
    print(f"t-primes up to {2*N}: {len(twin_primes)}")

    print(f"\nWeak form (>=1 summand a t-prime) failures: {weak_failures if weak_failures else 'none (except n=4)'}")

    strong_above_4208 = [n for n in strong_failures if n > 4208]
    print(f"\nStrong form (both summands t-primes, Dubner Conj. 4a) failures:")
    print(f"  All failures: {strong_failures[:15]}{'...' if len(strong_failures)>15 else ''}")
    print(f"  Failures > 4208: {strong_above_4208[:10] if strong_above_4208 else 'none'}")
    print(f"  Largest failure: {max(strong_failures)}")

    print("\nExample strong-form decompositions:")
    for n in [100, 1000, 4210, 10000, 20000]:
        for p in twin_primes:
            if p >= n:
                break
            q = n - p
            if q >= 2 and sieve[q] and q in twin_set:
                print(f"  {n} = {p} + {q}")
                break


def verify_no_three_consecutive(n=10000):
    """Verify computationally that no three consecutive integers appear in A002822.

    Also shows, for each consecutive pair (m, m+1), which of the six candidate
    primes 6m-1, 6(m+1)-1, 6(m+2)-1 is divisible by 5 — confirming the
    theoretical argument.
    """
    sieve = prime_sieve(6*n + 1)
    centers = sorted(A002822(range(1, n+1), sieve))
    center_set = set(centers)

    triples = [(m, m+1, m+2) for m in centers if m+1 in center_set and m+2 in center_set]

    print(f"Checked A002822 up to n={n} ({len(centers)} terms).")
    if triples:
        print(f"COUNTEREXAMPLE FOUND: {triples}")
    else:
        print("Confirmed: no three consecutive terms exist.")

    print("\nFor each consecutive pair (m, m+1) in A002822, the six candidate values")
    print("and which is divisible by 5:\n")
    pairs_found = 0
    for m in centers:
        if m + 1 in center_set:
            candidates = [
                (f"6·{m}-1",   6*m - 1),
                (f"6·{m}+1",   6*m + 1),
                (f"6·{m+1}-1", 6*(m+1) - 1),
                (f"6·{m+1}+1", 6*(m+1) + 1),
                (f"6·{m+2}-1", 6*(m+2) - 1),
                (f"6·{m+2}+1", 6*(m+2) + 1),
            ]
            div5 = [(label, v) for label, v in candidates if v % 5 == 0]
            print(f"  m={m}, m+1={m+1}: divisible by 5 -> {div5}")
            pairs_found += 1
            if pairs_found >= 10:
                print("  ...")
                break


def characterise_excess(seeds={1, 2, 3}, N=1000):
    """Show what primes account for the composite 6m+-1 in the excess M \\ A002822."""
    sieve = prime_sieve(6*N + 1)
    a002822 = set(A002822(range(1, N+1), sieve))
    M = generate_from_seeds(seeds, N)
    excess = sorted(M - a002822)

    def smallest_factor(n):
        for p in range(2, int(n**0.5)+1):
            if n % p == 0:
                return p
        return None

    factor_counts = Counter()
    for m in excess:
        for v in (6*m-1, 6*m+1):
            if not sieve[v]:
                f = smallest_factor(v)
                factor_counts[f] += 1

    print(f"Seeds={sorted(seeds)}, N={N}")
    print(f"  |M|={len(M)}, |A002822|={len(a002822)}, |excess|={len(excess)}")
    print()
    print("Smallest prime factor of composite 6m+-1 in excess elements:")
    cumulative = 0
    total = sum(factor_counts.values())
    for p, count in sorted(factor_counts.items()):
        cumulative += count
        inv6 = pow(6, -1, p)
        r_minus = inv6 % p
        r_plus = (-inv6) % p
        print(f"  p={p:>3}: {count:>4} occurrences  "
              f"(forbidden residues mod {p}: {r_minus} and {r_plus})  "
              f"cumulative: {cumulative/total:.1%}")


def analyse_types(N=10000):
    """Classify all m in [1,N] by number of primes in {6m-1, 6m+1}:
      type 0: both composite  (A067611 subset)
      type 1: exactly one prime (A067611 subset)
      type 2: both prime      (A002822)
    Report frequencies, run length distributions, and factor structure for type-0.
    """
    from itertools import groupby

    sieve = prime_sieve(6*N + 1)
    typed = [(m, int(sieve[6*m-1]) + int(sieve[6*m+1])) for m in range(1, N+1)]

    counts_by_type = Counter(c for _, c in typed)
    total = len(typed)
    print(f"All m in [1,{N}]: {total} elements")
    for t in (0, 1, 2):
        n = counts_by_type[t]
        label = ["both composite (A067611)", "one prime (A067611)", "both prime (A002822)"][t]
        print(f"  Type {t} ({label}): {n}  ({n/total:.1%})")

    counts = [c for _, c in typed]
    runs = [(k, len(list(g))) for k, g in groupby(counts)]
    run_lengths = {0: Counter(), 1: Counter(), 2: Counter()}
    for typ, length in runs:
        run_lengths[typ][length] += 1

    max_len = max(max(run_lengths[t]) for t in (0, 1, 2))
    print(f"\nRun length distribution:")
    print(f"{'length':>8}  {'type=0':>10}  {'type=1':>10}  {'type=2':>10}")
    for l in range(1, max_len + 1):
        c0 = run_lengths[0].get(l, 0)
        c1 = run_lengths[1].get(l, 0)
        c2 = run_lengths[2].get(l, 0)
        if c0 or c1 or c2:
            print(f"{l:>8}  {c0:>10}  {c1:>10}  {c2:>10}")

    def smallest_factor(n):
        for p in range(2, int(n**0.5)+1):
            if n % p == 0:
                return p
        return n

    pair_factors = Counter()
    for m, c in typed:
        if c == 0:
            pair_factors[(smallest_factor(6*m-1), smallest_factor(6*m+1))] += 1

    print(f"\nMost common factor pairs (sf(6m-1), sf(6m+1)) for type-0 elements:")
    for pair, cnt in pair_factors.most_common(12):
        print(f"  {pair}: {cnt}")
