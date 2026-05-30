import Mathlib
import Basic

/-!
# The Bridging Machine and the Gap Machine (ch08c, ch08d)

Formalisation of the Bridging Machine (BM) and Gap Machine (GM) from the paper.
-/

open scoped BigOperators Classical

/-! ## The Bridging Machine (ch08c) -/

/-- State of the Bridging Machine. -/
structure BMState where
  /-- Witnesses discovered so far -/
  A : Finset ℕ
  /-- Witnesses waiting to be processed (Q ⊆ A) -/
  queue : Finset ℕ
  /-- Sweep frontier -/
  sigma : ℕ

/-!
### BM key consequences

The full BM partition invariant (A ∪ B ∪ X = {1..σ}, pairwise disjoint)
requires a detailed state-machine simulation that is beyond the scope of
this formalisation. Instead, we prove the key consequences:

1. BC forces the BM to produce unbounded witnesses.
2. BC forces the BM to run forever (never halt).

Both are essentially restatements of `bc_implies_tpc`.
-/

/-- Under BC, the BM labels all of ℕ in the sense that witnesses are unbounded. -/
theorem bm_labels_all (hBC : BC) :
    ∀ N : ℕ, ∃ w, IsWitness w ∧ w ≥ N := by
  intro N
  obtain ⟨w, hw1, hw2⟩ := bc_implies_tpc hBC N
  exact ⟨w, hw2, by omega⟩

/-- Under BC, the BM runs forever: for every V there exists a witness beyond V. -/
theorem bc_implies_bm_runs (hBC : BC) :
    ∀ V : ℕ, ∃ w, IsWitness w ∧ w > V := by
  intro V
  obtain ⟨w, hw1, hw2⟩ := bc_implies_tpc hBC V
  exact ⟨w, hw2, hw1⟩

/-- The converse (BM running forever implies BC) is an open claim,
    deferred to future work. Stated as an explicit hypothesis, not proved. -/
def BM_Converse : Prop :=
  (∀ V : ℕ, ∃ w, IsWitness w ∧ w > V) → BC

/-! ## The Gap Machine (ch08d) -/

/-!
### Direction 1: GC (+ WDC) implies GM advances

**Important note on the formalisation vs. the paper:**

The paper states that under GC, for consecutive witnesses w₁ < w₂ with
w₂ ≤ 2w₁, the GM always finds a decomposition w₂ = u + v with u, v
witnesses and v ≤ w₁. However, GC alone only provides the *bound*
w₂ ≤ 2w₁ — it does not produce a *decomposition*.

The decomposition w₂ = u + v with u, v ∈ W requires WDC. Therefore
we state this theorem conditionally on both WDC and GC.

If w₂ = baseWitness = 1 then w₁ < w₂ = 1 is impossible (since w₁ ≥ 1).
If w₂ > baseWitness, WDC gives u + v = w₂ with u ≤ v. Since u, v are
witnesses and w₁, w₂ are consecutive, and u ≤ v < w₂, we must have
u ≤ v ≤ w₁. Combined with GC's bound w₂ ≤ 2w₁, this gives the result.
-/

/-- Under WDC, for consecutive witnesses w₁ < w₂, we can decompose w₂ = u + v
    with u, v witnesses and u ≤ v ≤ w₁. (GC is not needed for the decomposition
    itself, only for bounding the gap.) -/
theorem gc_implies_gm_advances (hWDC : WDC) (w1 w2 : ℕ)
    (hw1 : IsWitness w1) (hw2 : IsWitness w2)
    (hlt : w1 < w2)
    (hcons : ∀ m, IsWitness m → m ≤ w1 ∨ w2 ≤ m) :
    ∃ u v, IsWitness u ∧ IsWitness v ∧ u ≤ v ∧ v ≤ w1 ∧ u + v = w2 := by
  have hw1_pos := hw1.1
  have hw2_gt : w2 > baseWitness := by
    unfold baseWitness; omega
  obtain ⟨u, v, hu, hv, huv_le, huv_eq⟩ := hWDC w2 hw2 hw2_gt
  have hu_pos := hu.1
  have hv_pos := hv.1
  have hv_lt_w2 : v < w2 := by omega
  have hu_lt_w2 : u < w2 := by omega
  have hv_bound : v ≤ w1 := by
    rcases hcons v hv with h | h
    · exact h
    · omega
  have hu_bound : u ≤ w1 := by
    rcases hcons u hu with h | h
    · exact h
    · omega
  exact ⟨u, v, hu, hv, huv_le, hv_bound, huv_eq⟩

/-!
### Direction 2: GM loops when the gap is too large

If w₂ > 2w₁, then any decomposition w₂ = u + v with u ≤ v requires
v ≥ w₂/2 > w₁, so no valid decomposition with v ≤ w₁ exists.
This direction is unconditional.
-/

/-- If w₂ > 2w₁, there is no decomposition w₂ = u + v with u ≤ v ≤ w₁. -/
theorem gm_loops_if_gc_false (w1 w2 : ℕ)
    (_hw1 : IsWitness w1) (_hw2 : IsWitness w2)
    (hlt : w1 < w2)
    (hgap : w2 > 2 * w1) :
    ¬ ∃ u v, IsWitness u ∧ IsWitness v ∧ u ≤ v ∧ v ≤ w1 ∧ u + v = w2 := by
  rintro ⟨u, v, _, _, huv, hv, rfl⟩
  omega
