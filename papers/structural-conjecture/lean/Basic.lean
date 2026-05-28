import Mathlib

/-!
# A Structural Conjecture for the Infinitude of Twin Primes

Lean 4 formalization of the definitions and theorems from the paper.
-/

set_option maxHeartbeats 800000

open scoped BigOperators Classical

/-! ## Channel Representation -/

/-- The lower channel value: L_m = 6m - 1 -/
def lowerChannel (m : ℕ) : ℕ := 6 * m - 1

/-- The upper channel value: H_m = 6m + 1 -/
def upperChannel (m : ℕ) : ℕ := 6 * m + 1

/-- A positive integer m is a *witness* if both 6m-1 and 6m+1 are prime. -/
def IsWitness (m : ℕ) : Prop :=
  1 ≤ m ∧ (6 * m - 1 : ℕ).Prime ∧ (6 * m + 1 : ℕ).Prime

/-- The base witness ω = 1, corresponding to twin prime pair (5, 7). -/
def baseWitness : ℕ := 1

/-- The set of all witnesses. -/
def WitnessSet : Set ℕ := { m | IsWitness m }

/-! ## Base witness verification -/

theorem baseWitness_isWitness : IsWitness baseWitness := by
  unfold IsWitness baseWitness
  constructor
  · omega
  constructor <;> decide

/-! ## Primes in channels -/

/-
Every prime p > 3 lies in a channel: there exists m ≥ 1 such that
    p = L_m or p = H_m.
-/
theorem prime_in_channel {p : ℕ} (hp : p.Prime) (hp3 : 3 < p) :
    ∃ m, 1 ≤ m ∧ (p = lowerChannel m ∨ p = upperChannel m) := by
  -- Since p > 3 is prime, gcd(p, 6) = 1, so p % 6 ∈ {1, 5}.
  have h_mod : p % 6 = 1 ∨ p % 6 = 5 := by
    by_contra h_contra;
    have := Nat.Prime.eq_two_or_odd hp; ( have := Nat.dvd_of_mod_eq_zero ( show p % 3 = 0 by omega ) ; simp_all +decide [ Nat.Prime.dvd_iff_eq hp ] ; )
  generalize_proofs at *; simp_all +decide [ lowerChannel, upperChannel ] ; (
  exact ⟨ p / 6 + ( if p % 6 = 1 then 0 else 1 ), by split_ifs <;> omega, by split_ifs <;> omega ⟩)

/-! ## The Multiplexing Identity -/

theorem mux_lower {u v : ℕ} (hu : 1 ≤ u) (_hv : 1 ≤ v) :
    lowerChannel (u + v) = lowerChannel u + lowerChannel v + 1 := by
  simp only [lowerChannel]; omega

theorem mux_upper {u v : ℕ} (_hu : 1 ≤ u) (_hv : 1 ≤ v) :
    upperChannel (u + v) = upperChannel u + upperChannel v - 1 := by
  simp only [upperChannel]; omega

/-! ## Cross-term collapse -/

theorem cross_term {u v : ℕ} (hu : 1 ≤ u) (_hv : 1 ≤ v) :
    lowerChannel u + upperChannel v = 6 * (u + v) := by
  simp only [lowerChannel, upperChannel]; omega

theorem cross_composite {u v : ℕ} (hu : 1 ≤ u) (hv : 1 ≤ v)
    (_huv : 1 < u + v) : ¬ (lowerChannel u + upperChannel v).Prime := by
  rw [cross_term hu hv];
  norm_num [ Nat.prime_mul_iff ]

/-! ## Shift form -/

theorem shift_lower {u v : ℕ} (_hu : 1 ≤ u) :
    lowerChannel (u + v) = lowerChannel u + 6 * v := by
  simp only [lowerChannel]; omega

theorem shift_upper {u v : ℕ} (_hu : 1 ≤ u) :
    upperChannel (u + v) = upperChannel u + 6 * v := by
  simp only [upperChannel]; omega

theorem gap_preserved {m : ℕ} (_hm : 1 ≤ m) :
    upperChannel m - lowerChannel m = 2 := by
  simp only [upperChannel, lowerChannel]; omega

/-! ## Mod-5 structure -/

theorem mod5_lower_defect {m : ℕ} (hm : 1 < m) (hmod : m % 5 = 1) :
    ¬ IsWitness m := by
  exact fun h => by have := Nat.dvd_of_mod_eq_zero ( show ( 6 * m - 1 ) % 5 = 0 by omega ) ; rw [ h.2.1.dvd_iff_eq ] at this <;> omega;

theorem mod5_upper_defect {m : ℕ} (hm : 1 < m) (hmod : m % 5 = 4) :
    ¬ IsWitness m := by
  exact fun h => by have := Nat.dvd_of_mod_eq_zero ( show ( 6 * m + 1 ) % 5 = 0 by omega ) ; rw [ h.2.2.dvd_iff_eq ] at this <;> linarith;

theorem witness_mod5 {m : ℕ} (hw : IsWitness m) (hm : m ≠ 1) :
    m % 5 = 0 ∨ m % 5 = 2 ∨ m % 5 = 3 := by
  rcases hw with ⟨ hm₁, hm₂, hm₃ ⟩ ; rcases m with ( _ | _ | _ | m ) <;> simp_all +arith +decide;
  have := Nat.mod_lt m ( by decide : 5 > 0 ) ; interval_cases _ : m % 5 <;> simp_all +arith +decide [ Nat.add_mod ] ;
  · exact absurd ( Nat.dvd_of_mod_eq_zero ( show ( 6 * m + 19 ) % 5 = 0 by norm_num [ *, Nat.add_mod, Nat.mul_mod ] ) ) ( by rw [ hm₃.dvd_iff_eq ] <;> linarith );
  · exact absurd ( Nat.dvd_of_mod_eq_zero ( show ( 6 * m + 17 ) % 5 = 0 by norm_num [ *, Nat.add_mod, Nat.mul_mod ] ) ) ( by rw [ hm₂.dvd_iff_eq ] <;> linarith )

/-! ## The Twin Prime Conjecture and structural conjectures -/

/-- The Twin Prime Conjecture: there are infinitely many witnesses. -/
def TPC : Prop := ∀ N : ℕ, ∃ m, m > N ∧ IsWitness m

/-- The Witness Decomposition Conjecture: every witness beyond the base
    is a sum of two witnesses. -/
def WDC : Prop :=
  ∀ w, IsWitness w → w > baseWitness →
    ∃ u v, IsWitness u ∧ IsWitness v ∧ u ≤ v ∧ u + v = w

/-- The Bridging Conjecture: for every threshold V, some pair of witnesses
    below V sums to a witness above V. -/
def BC : Prop :=
  ∀ V : ℕ, 1 ≤ V → ∃ u v w, IsWitness u ∧ IsWitness v ∧ IsWitness w ∧
    u ≤ v ∧ v ≤ V ∧ V < w ∧ u + v = w

/-- The Gap Conjecture: consecutive witnesses satisfy w_{n+1} ≤ 2w_n. -/
def GC : Prop :=
  ∀ w₁ w₂ : ℕ, IsWitness w₁ → IsWitness w₂ → w₁ < w₂ →
    (∀ m, IsWitness m → m ≤ w₁ ∨ w₂ ≤ m) →
    w₂ ≤ 2 * w₁

/-! ## Proved implications -/

/-
BC ⟹ TPC: the Bridging Conjecture implies the Twin Prime Conjecture.
-/
theorem bc_implies_tpc : BC → TPC := by
  intro hbc
  intro N
  obtain ⟨u, v, w, hw⟩ := hbc (max 1 N) (by norm_num);
  exact ⟨ w, by cases max_cases 1 N <;> linarith, hw.2.2.1 ⟩

/-
WDC + TPC ⟹ BC
-/
theorem wdc_tpc_implies_bc : WDC → TPC → BC := by
  intros hWDC hTPC V hV_pos
  obtain ⟨w_star, hw_star⟩ : ∃ w_star, w_star > V ∧ IsWitness w_star := hTPC V;
  -- By the well-ordering principle, there exists a smallest witness $w^*$ greater than $V$.
  obtain ⟨w_star, hw_star_min⟩ : ∃ w_star, w_star > V ∧ IsWitness w_star ∧ ∀ w', w' > V → IsWitness w' → w_star ≤ w' := by
    exact ⟨ Nat.find ( ⟨ w_star, hw_star.1, hw_star.2 ⟩ : ∃ w_star > V, IsWitness w_star ), Nat.find_spec ( ⟨ w_star, hw_star.1, hw_star.2 ⟩ : ∃ w_star > V, IsWitness w_star ) |>.1, Nat.find_spec ( ⟨ w_star, hw_star.1, hw_star.2 ⟩ : ∃ w_star > V, IsWitness w_star ) |>.2, fun w' hw'_gt hw'_witness => Nat.find_min' ( ⟨ w_star, hw_star.1, hw_star.2 ⟩ : ∃ w_star > V, IsWitness w_star ) ⟨ hw'_gt, hw'_witness ⟩ ⟩;
  -- By WDC, since w* > 1 ≥ baseWitness, w* = u + v with u ≤ v, u,v ∈ W.
  obtain ⟨u, v, hu, hv, huv⟩ : ∃ u v, IsWitness u ∧ IsWitness v ∧ u ≤ v ∧ u + v = w_star := by
    exact hWDC _ hw_star_min.2.1 ( by linarith [ show baseWitness ≤ V from hV_pos ] );
  grind +locals

/-
WDC ⟹ GC
-/
theorem wdc_implies_gc : WDC → GC := by
  intro hdc
  intro w₁ w₂ hw₁ hw₂ hw₁w₂ hw_consecutive
  by_cases hw₂_base : w₂ > 1;
  · obtain ⟨ u, v, hu, hv, huv, rfl ⟩ := hdc w₂ hw₂ hw₂_base;
    cases hw_consecutive u hu <;> cases hw_consecutive v hv <;> linarith [ hu.1, hv.1 ];
  · linarith [ hw₁.1 ]

/-
BC ⟹ GC
-/
theorem bc_implies_gc : BC → GC := by
  intro hBC;
  intro w₁ w₂ hw₁ hw₂ hw₁w₂ hw₁w₂';
  obtain ⟨ u, v, w, hu, hv, hw, huv, hvw, hwv, h ⟩ := hBC w₁ ( by linarith [ hw₁.1 ] );
  grind +revert

/-- GC is a corollary of both structural conjectures. -/
theorem gc_is_corollary : (WDC → GC) ∧ (BC → GC) :=
  ⟨wdc_implies_gc, bc_implies_gc⟩

/-! ## Channel exhaustion -/

/-- Channel Exhaustion conjecture: if W is finite (contained in a finite set S),
    then for every m beyond S, both channel values are composite. -/
def ChannelExhaustion : Prop :=
  ∀ (S : Finset ℕ), (∀ m, IsWitness m → m ∈ S) →
    ∀ m, (∀ s ∈ S, s < m) →
      ¬ (6 * m - 1 : ℕ).Prime ∧ ¬ (6 * m + 1 : ℕ).Prime

/-
Channel exhaustion implies: if W is finite, primes are bounded.
-/
theorem channel_exhaustion_bounded (hce : ChannelExhaustion)
    (S : Finset ℕ) (hS : ∀ m, IsWitness m → m ∈ S) :
    ∃ N, ∀ p, Nat.Prime p → p ≤ N := by
  contrapose! hce;
  -- By contradiction, assume there are infinitely many primes.
  by_contra h_inf_primes;
  obtain ⟨m, hm⟩ : ∃ m, 1 ≤ m ∧ (∀ s ∈ S, s < m) ∧ ((6 * m - 1 : ℕ).Prime ∨ (6 * m + 1 : ℕ).Prime) := by
    obtain ⟨ p, hp₁, hp₂ ⟩ := hce ( 6 * ( S.sup id + 1 ) + 1 );
    obtain ⟨ m, hm₁, hm₂ ⟩ := prime_in_channel hp₁ ( by linarith );
    refine' ⟨ m, hm₁, _, _ ⟩ <;> rcases hm₂ with ( rfl | rfl ) <;> simp_all +decide [ lowerChannel, upperChannel ];
    · exact fun s hs => by linarith! [ Finset.le_sup ( f := id ) hs, Nat.sub_add_cancel ( by linarith : 1 ≤ 6 * m ) ] ;
    · exact fun s hs => lt_of_le_of_lt ( Finset.le_sup ( f := id ) hs ) ( Nat.lt_of_succ_lt hp₂ );
  cases hm.2.2 <;> have := h_inf_primes S hS m hm.2.1 <;> simp_all +decide [ IsWitness ]

/-! ## Mod-5 partition constraint -/

theorem mod5_partition_constraint {u v : ℕ}
    (hu : IsWitness u) (_hv : IsWitness v) (huv : IsWitness (u + v))
    (hu1 : u ≠ 1) (_hv1 : v ≠ 1) (huv1 : u + v ≠ 1) :
    ¬(u % 5 = 2 ∧ v % 5 = 2) ∧ ¬(u % 5 = 3 ∧ v % 5 = 3) := by
  constructor <;> intro h <;> have := mod5_upper_defect ( show 1 < u + v from lt_of_le_of_ne ( Nat.pos_of_ne_zero <| by aesop ) ( Ne.symm huv1 ) ) <;> simp_all +decide [ Nat.add_mod ];
  exact absurd ( mod5_lower_defect ( show 1 < u + v from lt_of_le_of_ne ( Nat.pos_of_ne_zero <| by aesop ) ( Ne.symm huv1 ) ) ( by omega ) ) ( by aesop )