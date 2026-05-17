from .sieve import prime_sieve


def A002822(seq, sieve):
    for m in seq:
        if sieve[6*m-1] and sieve[6*m+1]:
            yield m


def A067611(seq, sieve):
    for m in seq:
        if not (sieve[6*m-1] and sieve[6*m+1]):
            yield m


def ab(n):
    for b in range(1, n):
        for a in range(1, b+1):
            if 6*a*b-a-b >= n:
                break
            yield {"a": -a, "b": -b, "c": 0, "m": 6*a*b-a-b}
            yield {"a": +a, "b": -b, "c": 0, "m": 6*a*b+a-b}
            yield {"a": -a, "b": +b, "c": 0, "m": 6*a*b-a+b}
            yield {"a": +a, "b": +b, "c": 0, "m": 6*a*b+a+b}


def ab_dict(n):
    d = {}
    for ab_ in ab(n):
        m = ab_["m"]
        if m not in d:
            d[m] = []
        d[m].append(ab_)
    return d


def a002822_augmented(n):
    sieve = prime_sieve(6*n + 1)
    list_2822 = list(A002822(range(1, n+1), sieve))
    set_67611 = set(A067611(range(1, n+1), sieve))
    d = ab_dict(n+1)

    def augment(e, l, c):
        if c > 0:
            out = e | {"m": l, "c": c, "x": e["a"], "y": e["b"]}
        else:
            out = e | {"m": l, "c": c, "x": e["b"], "y": e["a"]}
        out["l"] = 6*l - 1
        out["u"] = 6*l + 1
        return out

    for l in list_2822:
        if l-1 in set_67611:
            ab_list = d[l-1]
            for e in ab_list:
                yield augment(e, l, 1)
        if l+1 in set_67611:
            ab_list = d[l+1]
            for e in ab_list:
                yield augment(e, l, -1)
