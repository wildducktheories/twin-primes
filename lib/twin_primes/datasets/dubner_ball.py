"""
dubner_ball — export BCM witness geometry to JSON for the Dubner Ball Three.js viewer.

Usage (as module):
    from twin_primes.datasets.dubner_ball import generate
    data = generate(limit=500)
    data = generate(limit=500, non_witnesses=True)

Usage (as script):
    python -m twin_primes.datasets.dubner_ball [LIMIT] [--non-witnesses] [--output PATH]
    python -m twin_primes.datasets.dubner_ball 500 > data.json
    python -m twin_primes.datasets.dubner_ball 500 --non-witnesses --output data.json

Output JSON schema:
    {
      "limit": 500,
      "nodes": [
        {"w": int, "x": float, "y": float, "z": float, "t": float,
         "dequeue_idx": int, "prog": [u, v] | null}
      ],
      "edges": [{"src": int, "dst": int}],
      "generations": [{"v": int, "children": [[u, w], ...]}],
      "non_witnesses": [   // only when non_witnesses=True
        {"w": int, "x": float, "y": float, "z": float,
         "prog": [u, v], "kind": "one_prime" | "composite"}
      ]
    }

t is the coolwarm rank in [0,1]: 0=blue (balanced u≈v), 1=red (lopsided u≪v).
"""

import math
import heapq

from ..sieve import prime_sieve


def _plane_to_cart(r, alpha, k):
    psi = 2 * math.pi * k / 5
    e1x, e1y = -math.sin(psi), math.cos(psi)
    return (
        r * math.cos(alpha) * e1x,
        r * math.cos(alpha) * e1y,
        r * math.sin(alpha),
    )


def generate(*, limit=500, non_witnesses=False):
    """
    Run BCM to `limit` and produce geometry data for the Dubner Ball viewer.

    Parameters
    ----------
    limit : int
        Maximum witness value to consider.
    non_witnesses : bool
        If True, also record the first (u,v) pair generating each rejected w.

    Returns
    -------
    dict
        JSON-serialisable result dict (see module docstring for schema).
    """
    N = limit
    sieve_arr = prime_sieve(6 * N + 1)

    def is_witness(w):
        return 1 <= w <= N and bool(sieve_arr[6*w-1]) and bool(sieve_arr[6*w+1])

    def non_witness_kind(w):
        if w < 1 or w > N:
            return None
        lo = bool(sieve_arr[6*w-1])
        hi = bool(sieve_arr[6*w+1])
        if lo and hi:
            return None
        if lo or hi:
            return 'one_prime'
        return 'composite'

    A = [1]
    A_set = {1}
    q = [1]
    dequeue_idx = {}
    progenitor = {1: None}
    pos_polar = {1: (math.log(2), math.pi / 4, 1 % 5)}
    generations = []

    nw_progenitor = {}
    nw_kind = {}

    while q:
        v = heapq.heappop(q)
        dequeue_idx[v] = len(dequeue_idx)
        children = []

        for u in A:
            s = u + v
            if s > N:
                break
            if s in A_set:
                continue
            if is_witness(s):
                A.append(s)
                A_set.add(s)
                pu, pv = min(u, v), max(u, v)
                progenitor[s] = (pu, pv)
                heapq.heappush(q, s)
                ratio = pu / pv
                r_s   = math.log(s - 1 + ratio)
                alpha = 2 * math.pi * ratio
                pos_polar[s] = (r_s, alpha, s % 5)
                children.append([pu, s])
            elif non_witnesses and s not in nw_progenitor:
                kind = non_witness_kind(s)
                if kind is not None:
                    pu, pv = min(u, v), max(u, v)
                    nw_progenitor[s] = (pu, pv)
                    nw_kind[s] = kind

        generations.append({"v": v, "children": children})

    pos_xyz = {}
    for w in dequeue_idx:
        r, alpha, k = pos_polar[w]
        pos_xyz[w] = _plane_to_cart(r, alpha, k)

    delta_uv = {}
    for w in dequeue_idx:
        prog = progenitor[w]
        delta_uv[w] = (prog[1] - prog[0]) / w if prog else None

    ranked = sorted((dv, w) for w, dv in delta_uv.items() if dv is not None)
    n = len(ranked)
    t_colour = {w: 0.5 for w in dequeue_idx}
    for rank, (_, w) in enumerate(ranked):
        t_colour[w] = rank / max(n - 1, 1)

    nodes = []
    for w in sorted(dequeue_idx.keys()):
        x, y, z = pos_xyz[w]
        prog = progenitor[w]
        nodes.append({
            "w": w,
            "x": round(x, 6),
            "y": round(y, 6),
            "z": round(z, 6),
            "t": round(t_colour[w], 6),
            "dequeue_idx": dequeue_idx[w],
            "prog": list(prog) if prog else None,
        })

    edges = []
    for w in sorted(dequeue_idx.keys()):
        prog = progenitor[w]
        if prog:
            u, v = prog
            edges.append({"src": u, "dst": w})
            if u != v:
                edges.append({"src": v, "dst": w})

    result = {
        "limit": N,
        "nodes": nodes,
        "edges": edges,
        "generations": generations,
    }

    if non_witnesses:
        nw_nodes = []
        for w in sorted(nw_progenitor.keys()):
            pu, pv = nw_progenitor[w]
            ratio = pu / pv
            r_w   = math.log(w - 1 + ratio)
            alpha = 2 * math.pi * ratio
            x, y, z = _plane_to_cart(r_w, alpha, w % 5)
            nw_nodes.append({
                "w": w,
                "x": round(x, 6),
                "y": round(y, 6),
                "z": round(z, 6),
                "prog": [pu, pv],
                "kind": nw_kind[w],
            })
        result["non_witnesses"] = nw_nodes

    return result


if __name__ == "__main__":
    import argparse
    import json
    import sys

    p = argparse.ArgumentParser(
        description="Generate Dubner Ball witness geometry JSON"
    )
    p.add_argument("limit", type=int, nargs="?", default=500,
                   help="Maximum witness value (default: 500)")
    p.add_argument("--non-witnesses", action="store_true",
                   help="Include non-witness nodes")
    p.add_argument("--output", default="-",
                   help="Output file path (default: stdout)")
    args = p.parse_args()

    data = generate(limit=args.limit, non_witnesses=args.non_witnesses)
    out = json.dumps(data, separators=(',', ':'))

    if args.output == "-":
        print(out)
    else:
        with open(args.output, "w") as f:
            f.write(out)
        print(f"Wrote {args.output}", file=sys.stderr)
