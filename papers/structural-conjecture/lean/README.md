# Lean 4 Formalisation — A Structural Conjecture for the Infinitude of Twin Primes

Machine-verified proofs of the core implication chain from the paper.
All files compile with **zero `sorry`** against Lean 4 / Mathlib v4.28.0.

## Files

| File | Contents |
|---|---|
| `Basic.lean` | Channel definitions, Mux Identity, mod-5 constraints, BC/WDC/GC/TPC definitions, core implication chain |
| `ScaleInvariance.lean` | Scale bound, gap invariance, witness tower (ch08b) |
| `Machines.lean` | Bridging Machine structure and consequences, Gap Machine halting theorem (ch08c–d) |

## Key theorems (all sorry-free)

- `bc_implies_tpc` — BC ⟹ TPC
- `wdc_tpc_implies_bc` — WDC ∧ TPC ⟹ BC
- `wdc_implies_gc` — WDC ⟹ GC
- `bc_implies_gc` — BC ⟹ GC
- `channel_exhaustion_bounded` — Channel Exhaustion ⟹ primes bounded
- `scale_bound` — BC gives witnesses with doubling bound w ≤ 2v
- `gc_implies_gm_advances` — Under WDC, Gap Machine always advances
- `gm_loops_if_gc_false` — GC false ⟹ Gap Machine loops (unconditional)
- `BM_Converse` — stated as open proposition, not proved (deferred)

## Building

Requires Lean 4 and Lake. With `elan` installed:

```
cd papers/structural-conjecture/lean
lake build
```
