import Mathlib
import Basic
import ScaleInvariance
import Machines
import Corollaries

/-!
# The Complete Proved Implication Chain

This file assembles the full chain of implications proved in the paper
"A Structural Conjecture for the Infinitude of Twin Primes".

All arrows here are unconditional theorems (no conjectures assumed as axioms).
Every statement is conditional on the relevant hypothesis (BC, WDC, etc.)
being passed as an explicit argument.

This file compiles with zero `sorry` and serves as a standalone
machine-verified certificate.
-/

open scoped BigOperators Classical

/-! ## Arrow 1: BC ⟹ TPC -/
#check @bc_implies_tpc    -- BC → TPC

/-! ## Arrow 2: WDC ⟹ GC -/
#check @wdc_implies_gc    -- WDC → GC

/-! ## Arrow 3: BC ⟹ GC -/
#check @bc_implies_gc     -- BC → GC

/-! ## Arrow 4: WDC ∧ TPC ⟹ BC -/
#check @wdc_tpc_implies_bc  -- WDC → TPC → BC

/-! ## Arrow 5: Channel Exhaustion ⟹ (W finite ⟹ Primes bounded) -/
#check @channel_exhaustion_bounded

/-! ## The Euclid veto: primes are infinite (Mathlib) -/
#check @Nat.exists_infinite_primes  -- ∀ n, ∃ p, n ≤ p ∧ Nat.Prime p

/-! ## Assembled: BC ⟹ Primes infinite (via TPC)

Note: `bc_implies_primes_infinite` does not logically require TPC or
channel exhaustion — it simply restates `bc_implies_tpc` in the form
"for every N, there is a prime pair beyond N", which already gives
infinitely many primes (specifically, infinitely many *twin* primes).
-/

/-- Under BC, there are infinitely many primes — in fact, infinitely
    many twin prime pairs (which is strictly stronger). -/
theorem bc_implies_primes_infinite (hBC : BC) :
    ∀ N : ℕ, ∃ p, p > N ∧ Nat.Prime p := by
  intro N
  obtain ⟨m, hm_gt, hm_wit⟩ := bc_implies_tpc hBC N
  exact ⟨6 * m + 1, by omega, hm_wit.2.2⟩

/-! ## Corollaries from ch08 -/

#check @sc_tpc        -- BC → TPC
#check @sc_equiv      -- WDC → (BC ↔ TPC)
#check @sc_bertrand   -- WDC → ... → w₂ ≤ 2 * w₁

/-! ## Scale invariance -/

#check @scale_bound       -- BC → V ≥ 1 → ∃ u v w, ... ∧ w ≤ 2v
#check @gap_invariance    -- m ≥ 1 → H_m - L_m = 2
#check @witness_tower     -- BC → ∀ n, ∃ w ∈ W, w ≥ n

/-! ## Machines -/

#check @bc_implies_bm_runs      -- BC → ∀ V, ∃ w ∈ W, w > V
#check @gc_implies_gm_advances  -- WDC → consecutive w₁ w₂ → ∃ decomposition
#check @gm_loops_if_gc_false    -- w₂ > 2w₁ → no decomposition with v ≤ w₁

/-! ## Axiom audit -/

#print axioms bc_implies_tpc
#print axioms wdc_tpc_implies_bc
#print axioms wdc_implies_gc
#print axioms bc_implies_gc
#print axioms channel_exhaustion_bounded
#print axioms bc_implies_primes_infinite
#print axioms sc_tpc
#print axioms sc_equiv
#print axioms sc_bertrand
