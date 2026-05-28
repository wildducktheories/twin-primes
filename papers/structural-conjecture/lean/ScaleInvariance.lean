import Mathlib
import Basic

/-!
# Scale Invariance under BC (ch08b)

Formalisation of the scale invariance properties from ch08b of the paper.
-/

open scoped BigOperators Classical

/-! ## Bridging scale bound -/

/-- Under BC, for any threshold V ≥ 1, there exist witnesses u, v, w with
    u + v = w, v ≤ V < w, and w ≤ 2v (the doubling bound). -/
theorem scale_bound (hBC : BC) (V : ℕ) (hV : 1 ≤ V) :
    ∃ u v w, IsWitness u ∧ IsWitness v ∧ IsWitness w ∧
      u + v = w ∧ v ≤ V ∧ V < w ∧ w ≤ 2 * v := by
  obtain ⟨u, v, w, hu, hv, hw, huv, hvV, hVw, hsum⟩ := hBC V hV
  exact ⟨u, v, w, hu, hv, hw, hsum, hvV, hVw, by omega⟩

/-! ## Gap invariance -/

/-- The channel gap H_m - L_m = 2 is invariant across all m ≥ 1. -/
theorem gap_invariance (m : ℕ) (hm : 1 ≤ m) :
    upperChannel m - lowerChannel m = 2 :=
  gap_preserved hm

/-! ## Witness tower -/

/-- Under BC, witnesses are unbounded: for every n there exists a witness w ≥ n.
    This is a direct consequence of `bc_implies_tpc`. -/
theorem witness_tower (hBC : BC) :
    ∀ n : ℕ, ∃ w, IsWitness w ∧ w ≥ n := by
  intro n
  obtain ⟨w, hw1, hw2⟩ := bc_implies_tpc hBC n
  exact ⟨w, hw2, by omega⟩
