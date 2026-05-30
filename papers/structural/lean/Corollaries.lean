import Mathlib
import Basic

/-!
# Corollaries of the Structural Conjecture (ch08)

These corollaries follow directly from the theorems proved in `Basic.lean`.
-/

open scoped BigOperators Classical

/-! ## SC ⟹ TPC -/

/-- Under the Structural Conjecture (PNT ⟹ WDC ∧ BC), TPC follows.
    Here we just record that BC ⟹ TPC is already proved. -/
theorem sc_tpc (hBC : BC) : TPC :=
  bc_implies_tpc hBC

/-! ## Equivalence under SC: WDC ∧ TPC ⟺ BC -/

/-- Under WDC: BC ⟺ TPC (both directions proved). -/
theorem sc_equiv (hWDC : WDC) : BC ↔ TPC :=
  ⟨bc_implies_tpc, wdc_tpc_implies_bc hWDC⟩

/-! ## Bertrand for twin prime pairs -/

/-- Under WDC (which follows from SC), consecutive witnesses satisfy
    w₂ ≤ 2 * w₁. This is the content of GC, extracted from `wdc_implies_gc`. -/
theorem sc_bertrand (hWDC : WDC) (w1 w2 : ℕ)
    (hw1 : IsWitness w1) (hw2 : IsWitness w2)
    (hlt : w1 < w2)
    (hcons : ∀ m, IsWitness m → m ≤ w1 ∨ w2 ≤ m) :
    w2 ≤ 2 * w1 :=
  wdc_implies_gc hWDC w1 w2 hw1 hw2 hlt hcons
