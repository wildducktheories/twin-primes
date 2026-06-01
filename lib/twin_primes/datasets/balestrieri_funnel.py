"""
balestrieri_funnel — export witness geometry for the Balestrieri Funnel viewer.

Coordinate system (signed):
  x = sgn_a * a   where sgn_a is the sign of the a-term in the closest defect form
  y = sgn_b * b   where sgn_b is the sign of the b-term
  z = sgn_u * h   where sgn_u encodes which channel the defect form attacks:
                    +1 → 6w+1 is composite (defect types ++ and --)
                    -1 → 6w-1 is composite (defect types +- and -+)
                  and h = height(w) = length of longest ancestral path to seed {1}

The four quadrants of the (x,y) plane correspond to the four sign combinations:
  (+,+) → type ++  : m = 6ab + a + b,  6m+1 = (6a+1)(6b+1)
  (+,-) → type +-  : m = 6ab + a - b,  6m-1 = (6a-1)(6b+1)   [= type -+ in paper]
  (-,-) → type --  : m = 6ab - a - b,  6m+1 = (6a-1)(6b-1)
  (-,+) → type -+  : m = 6ab - a + b,  (symmetric variant — see note)

Each witness escapes all defect forms.  We place it at the coordinates of its
CLOSEST defect form — the one it most narrowly escaped.  This puts witnesses
near the surface of the Balestrieri lattice, with their position encoding
which family nearly claimed them.

Note: the three canonical families in the literature are ++, --, +-  (the fourth
sign combination -+ is equivalent to +- by symmetry a↔b).  We include all four
sign combinations here to populate all quadrants.

z < 0: witness nearly belonged to a family attacking the 6w-1 channel
z > 0: witness nearly belonged to a family attacking the 6w+1 channel

Usage:
    from twin_primes.datasets.balestrieri_funnel import generate
    data = generate(limit=500)

Output JSON schema:
    {
      "limit": int,
      "nodes": [
        {"w": int, "x": float, "y": float, "z": float,
         "a": int, "b": int, "h": int,
         "sgn_a": +1|-1, "sgn_b": +1|-1, "sgn_u": +1|-1,
         "defect_type": str,   // "++", "+-", "--", "-+"
         "miss": float,        // |6ab ± a ± b - w|, closeness of escape
         "generation": int,
         "prog": [u, v] | null}
      ],
      "edges": [
        {"src": int, "dst": int,
         "arc": [[x,y,z], ...]}   // helix sample points for spiral edge
      ],
      "heights": {str(w): int}
    }
"""

import math
import heapq

from ..sieve import prime_sieve


# The four defect families: (sgn_a, sgn_b, sgn_u, label)
# sgn_u: which channel is attacked
#   +1 → 6m+1 is composite  (types ++ and --)
#   -1 → 6m-1 is composite  (types +- and -+)
_DEFECT_FAMILIES = [
    (+1, +1, +1, "++"),   # m = 6ab + a + b,  6m+1 = (6a+1)(6b+1)
    (-1, -1, +1, "--"),   # m = 6ab - a - b,  6m+1 = (6a-1)(6b-1)
    (+1, -1, -1, "+-"),   # m = 6ab + a - b,  6m-1 = (6a-1)(6b+1)
    (-1, +1, -1, "-+"),   # m = 6ab - a + b,  6m-1 = (6a+1)(6b-1)  [symmetric]
]


def _closest_defect(w):
    """
    Find the (a, b, sgn_a, sgn_b, sgn_u, type, miss) of the closest Balestrieri
    defect form to w.

    For each family, we solve 6ab + sgn_a*a + sgn_b*b = w for a,b >= 1.
    The product term dominates: 6ab ≈ w, so a ≈ sqrt(w/6).
    We search a small neighbourhood of a = round(sqrt(w/6)) and for each a
    compute b = round((w - sgn_a*a) / (6*a + sgn_b)).

    Returns the candidate (a, b, sgn_a, sgn_b, sgn_u, label, miss) with
    smallest |defect_value - w|.
    """
    best = None
    best_miss = math.inf

    a_centre = max(1, round(math.sqrt(w / 6)))

    for sgn_a, sgn_b, sgn_u, label in _DEFECT_FAMILIES:
        for da in range(-3, 4):
            a = a_centre + da
            if a < 1:
                continue
            # Solve: 6ab + sgn_a*a + sgn_b*b = w
            # b*(6a + sgn_b) = w - sgn_a*a
            denom = 6 * a + sgn_b
            if denom <= 0:
                continue
            b_raw = (w - sgn_a * a) / denom
            for b in (max(1, math.floor(b_raw)), max(1, math.ceil(b_raw))):
                val = 6 * a * b + sgn_a * a + sgn_b * b
                miss = abs(val - w)
                if miss < best_miss:
                    best_miss = miss
                    best = (a, b, sgn_a, sgn_b, sgn_u, label, miss)

    return best


def _helix_arc(x0, y0, z0, x1, y1, z1, turns=0.4, n_points=10):
    """
    Generate a helical arc from (x0,y0,z0) to (x1,y1,z1).
    The helix winds `turns` full rotations around the z-axis.
    Handles z0 == z1 (same height) by falling back to straight line.
    """
    pts = []
    r0 = math.sqrt(x0**2 + y0**2)
    r1 = math.sqrt(x1**2 + y1**2)
    theta0 = math.atan2(y0, x0)
    theta1 = math.atan2(y1, x1)

    dtheta = theta1 - theta0
    while dtheta > math.pi:
        dtheta -= 2 * math.pi
    while dtheta < -math.pi:
        dtheta += 2 * math.pi
    dtheta += 2 * math.pi * turns

    for i in range(n_points + 1):
        t = i / n_points
        r = r0 + (r1 - r0) * t
        theta = theta0 + dtheta * t
        z = z0 + (z1 - z0) * t
        pts.append([round(r * math.cos(theta), 5),
                    round(r * math.sin(theta), 5),
                    round(z, 5)])
    return pts


def generate(*, limit=500):
    """
    Run BM to `limit`, compute heights, and produce Balestrieri Funnel geometry.
    """
    N = limit
    sieve_arr = prime_sieve(6 * N + 2)

    def is_witness(w):
        hi = 6 * w + 1
        return 1 <= w <= N and hi < len(sieve_arr) and \
               bool(sieve_arr[6*w - 1]) and bool(sieve_arr[hi])

    # --- BM run ---
    A = [1]
    A_set = {1}
    q = [1]
    bm_generation = {}
    progenitor = {1: None}

    while q:
        v = heapq.heappop(q)
        bm_generation[v] = len(bm_generation)
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

    # --- Compute height (longest path back to seed) ---
    height = {1: 0}
    for w in sorted(A_set):
        if w == 1:
            continue
        prog = progenitor.get(w)
        if prog is None:
            height[w] = 0
        else:
            u, v = prog   # u <= v; v is the canonical (larger) parent
            height[w] = height.get(v, 0) + 1

    # --- Compute signed (x, y, z) for each witness ---
    # Scale factors: log for (a,b) so small values are readable; linear for h
    XY_SCALE = 1.4
    Z_SCALE  = 0.9

    def witness_xyz(w, a, b, sgn_a, sgn_b, sgn_u, h):
        # When sgn_u=-1 (+-/-+ families, 6m-1 channel), swap a↔b before
        # applying signs — this separates the four families into distinct
        # clusters and produces the funnel shape.
        ax, bx = (b, a) if sgn_u < 0 else (a, b)
        x = sgn_a * XY_SCALE * math.log(ax + 0.5)
        y = sgn_b * XY_SCALE * math.log(bx + 0.5)
        # z = log(w) — spreads witnesses by magnitude rather than branch depth
        z = math.log(w + 0.5) * Z_SCALE
        return x, y, z

    # --- Jitter witnesses that share the same signed (a,b,sgn_a,sgn_b,sgn_u) cell ---
    cell_count = {}
    cell_order = {}
    for w in sorted(A_set):
        if w == 1:
            cell_order[w] = (1, 1, +1, +1, +1, 0)
            continue
        a, b, sgn_a, sgn_b, sgn_u, label, miss = _closest_defect(w)
        key = (a, b, sgn_a, sgn_b, sgn_u)
        idx = cell_count.get(key, 0)
        cell_count[key] = idx + 1
        cell_order[w] = (a, b, sgn_a, sgn_b, sgn_u, idx)

    # --- Build node list ---
    nodes = []
    node_xyz = {}
    node_meta = {}

    for w in sorted(A_set):
        prog = progenitor.get(w)
        h = height[w]

        if w == 1:
            # Seed: place at origin-ish, no defect family
            a, b, sgn_a, sgn_b, sgn_u = 1, 1, +1, +1, +1
            label, miss, idx = "seed", 0.0, 0
        else:
            a, b, sgn_a, sgn_b, sgn_u, idx = cell_order[w]
            a2, b2, sa2, sb2, su2, lbl, miss = _closest_defect(w)
            label = lbl

        x, y, z = witness_xyz(w, a, b, sgn_a, sgn_b, sgn_u, h)

        # Apply jitter within cell to separate collisions
        if idx > 0:
            jitter_r = 0.15 * idx
            jitter_theta = 2 * math.pi * (w % 11) / 11
            x += jitter_r * math.cos(jitter_theta)
            y += jitter_r * math.sin(jitter_theta)

        node_xyz[w] = (x, y, z)
        node_meta[w] = (a, b, sgn_a, sgn_b, sgn_u, label, miss)

        nodes.append({
            "w": w,
            "x": round(x, 5),
            "y": round(y, 5),
            "z": round(z, 5),
            "a": a,
            "b": b,
            "sgn_a": sgn_a,
            "sgn_b": sgn_b,
            "sgn_u": sgn_u,
            "defect_type": label,
            "miss": round(miss, 4),
            "h": h,
            "generation": bm_generation.get(w, 0),
            "prog": list(prog) if prog else None,
        })

    # --- Build edges with helix arcs ---
    edges = []
    for w in sorted(A_set):
        prog = progenitor.get(w)
        if not prog:
            continue
        u, v = prog   # u <= v; v is canonical parent

        if v not in node_xyz or w not in node_xyz:
            continue

        vx, vy, vz = node_xyz[v]
        wx, wy, wz = node_xyz[w]
        arc = _helix_arc(vx, vy, vz, wx, wy, wz, turns=0.4, n_points=10)
        edges.append({"src": v, "dst": w, "arc": arc})

        if u != v and u in node_xyz:
            ux, uy, uz = node_xyz[u]
            arc_u = _helix_arc(ux, uy, uz, wx, wy, wz, turns=0.2, n_points=8)
            edges.append({"src": u, "dst": w, "arc": arc_u})

    return {
        "limit": N,
        "nodes": nodes,
        "edges": edges,
        "heights": {str(w): height[w] for w in sorted(A_set)},
    }


if __name__ == "__main__":
    import argparse
    import json
    import sys

    p = argparse.ArgumentParser(
        description="Generate Balestrieri Funnel witness geometry JSON"
    )
    p.add_argument("limit", type=int, nargs="?", default=300,
                   help="Maximum witness value (default: 300)")
    p.add_argument("--output", default="-",
                   help="Output file path (default: stdout)")
    args = p.parse_args()

    data = generate(limit=args.limit)
    out = json.dumps(data, separators=(',', ':'))

    if args.output == "-":
        print(out)
    else:
        with open(args.output, "w") as f:
            f.write(out)
        print(f"Wrote {args.output} ({len(data['nodes'])} nodes, "
              f"{len(data['edges'])} edges, "
              f"height range 0-{max(data['heights'].values())})",
              file=sys.stderr)
