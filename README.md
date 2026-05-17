# Twin Primes

An exploration of the Twin Prime Conjecture and related additive properties of the set
A002822 — the positive integers $m$ such that $6m-1$ and $6m+1$ are both prime (twin
prime cofactors).

---

## Papers

### Bridging the Gap: Additive Structure in the Twin Prime Cofactors

`papers/bridging-conjecture/`

Introduces the **Bridging Conjecture**: for every $K$, there exist $a, b, k \in A002822$
with $a < K$, $b < K$, and $k = a + b > K$. The paper establishes that the Bridging
Conjecture is equivalent to the Twin Prime Conjecture assuming Dubner's Conjecture 1, and
that it follows unconditionally from Dubner's Conjecture 3. As a corollary, the Bridging
Conjecture implies a conditional lower bound $\pi_2(x) \gg \log x$ on the twin prime
counting function, derived purely from the additive structure of A002822.

The paper also re-expresses Dubner's exception set A243956 in set-theoretic terms as the
complement of the self-sumset of A002822 in $\mathbb{N}$, which explains the additive
origin of its elements rather than merely listing them, and reformulates Dubner's
Conjecture 3 as the assertion that this complement is finite. An appendix provides
heuristic evidence for both conjectures, including a gap ratio plot and a decomposition
count plot with Hardy--Littlewood reference curves.

Read the paper:
[wildducktheories-bridging-conjecture.pdf](https://github.com/wildducktheories/twin-primes/blob/master/papers/bridging-conjecture/wildducktheories-bridging-conjecture.pdf)

Build the PDF with:

```
task pdf
```

---

## Notebook

`notebook/twin-primes.ipynb`

An interactive Jupyter notebook exploring the conjectures computationally. Topics covered
include:

- Definitions and verification of A002822, A067611, A243956
- Middle number decompositions and Dubner's Conjecture 1
- The Bridging Conjecture, its gap bound, and density implications
- Verification of Dubner's Conjecture 3 (sumset form) up to large limits
- Congruence constraints on middle number decompositions
- The Goldbach-twin conjecture (Dubner's Conjecture 4a)
- Visualisations: gap ratios, decomposition counts, twin prime witnesses

Open with:

```
task edit
```

---

## Animations

`animations/6ab-a-b-1/`

A 3D animation of the twin prime witness structure, rendered with
[Manim](https://www.manim.community/). Each point represents a witness $(a, b)$ for a
twin prime cofactor $m \in A002822$, plotted in three dimensions with $m$ on the vertical
axis. Green points are witnesses via the $6m-1$ neighbour; red via $6m+1$.

Render with:

```
task animate
```

---

## References

- H. Dubner, *Twin prime conjectures*, Journal of Recreational Mathematics **30**(3),
  1999–2000. ([PDF](papers/bridging-conjecture/sources/a007534.pdf))
- OEIS [A002822](https://oeis.org/A002822): Numbers $m$ such that $6m-1$ and $6m+1$ are both prime.
- OEIS [A243956](https://oeis.org/A243956): Positive integers with no representation as $i+j$ with $i,j \in A002822$.
- OEIS [A007534](https://oeis.org/A007534): Even numbers not the sum of two primes both having a twin prime.
