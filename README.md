# Twin Primes

An exploration of the Twin Prime Conjecture via the additive structure of twin prime
witnesses — the positive integers $m$ such that $6m-1$ and $6m+1$ are both prime
(OEIS [A002822](https://oeis.org/A002822)).

**Website**: [wildducktheories.github.io/twin-primes](https://wildducktheories.github.io/twin-primes/)

---

## Primary Paper

### A Structural Conjecture for the Infinitude of Twin Primes

`papers/structural-conjecture/`

The central thesis: **PNT ⟹ (WDC ∧ BC) ⟹ TPC**. Introduces the Bridging Conjecture
(BC) and Witness Decomposition Conjecture (WDC), and proves BC ⟹ TPC unconditionally.
Proposes that the Prime Number Theorem alone forces the additive closure of the set of
twin prime witnesses — bypassing the parity obstruction that limits sieve theory.

Includes the Bridging Machine, the Gap Machine, scale invariance theorems, and Lean 4
machine-verified proofs of the core implication chain.

[wdt-structural-conjecture.pdf](papers/structural-conjecture/wdt-structural-conjecture.pdf)

---

## Earlier Papers

### Logical Implications of a Bridging Conjecture for the Twin Prime Conjecture

`papers/bridging-conjecture/`

Introduces the Bridging Conjecture and establishes its equivalence to TPC under
Dubner's Middle Number Conjecture. Derives a conditional lower bound
$\pi_2(x) \gg \log x$ from additive structure alone.

[wdt-bridging-conjecture.pdf](papers/bridging-conjecture/wdt-bridging-conjecture.pdf)

### The Mathematics of Dubner's Ball

`papers/dubners-ball/`

The 3D visualisation of the witness set and its progenitor structure. Each node is a
twin prime witness; each filament connects a witness to its decomposition pair. The ball
grows to infinity if and only if BC holds.

[wdt-dubners-ball.pdf](papers/dubners-ball/wdt-dubners-ball.pdf)

### Heuristic Evidence for the Bridging Conjecture

`papers/heuristics/`

Decomposition gap analysis, cluster structure, and probabilistic estimates for
simultaneous bridging failure. Empirical and analytic evidence that BC is
overwhelmingly likely to be true.

[wdt-heuristics.pdf](papers/heuristics/wdt-heuristics.pdf)

### How AI Was Used

`papers/ai-usage/`

A full transparency statement documenting the role of AI systems (Claude, Aristotle,
ChatGPT, Gemini) in the development of this research. Describes what each system
contributed, what the author contributed, the ticket loop review methodology, and
its limitations. Canonical reference for AI attribution across the programme.

[wdt-ai-usage.pdf](papers/ai-usage/wdt-ai-usage.pdf)

### Fiction

`papers/gemima/`

A long-form narrative by Gemima — a journalist who came to this story expecting a sidebar
and found something stranger. The git log, the AI collaborators, Harvey Dubner's ghost,
and a question addressed to a woman called Sonia on which everything depends.

[wdt-gemima.pdf](papers/gemima/wdt-gemima.pdf)

---

## Interactive

### Dubner's Ball — 3D Viewer

`3d/dubner-ball/`

Interactive three-dimensional visualisation of the twin prime witness progenitor tree.
Rotate, zoom, and explore the self-similar structure of the witness set.

[Open viewer](https://wildducktheories.github.io/twin-primes/3d/dubner-ball/index.html)

---

## References

- H. Dubner, *Twin Prime Conjectures*, Journal of Recreational Mathematics **30**(3), 1999–2000.
- F. Balestrieri, *An Equivalent Problem to the Twin Prime Conjecture*, [arXiv:1106.6050](https://arxiv.org/abs/1106.6050), 2011.
- OEIS [A002822](https://oeis.org/A002822): Twin prime cofactors.
- OEIS [A243956](https://oeis.org/A243956): Integers with no witness decomposition.
