# ARCHHOLD

The caller supplies the span and the roof numbers: span, thickness, tensile strength, and a declared crack.

**Owner:** Digital Currensy Inc.
**Copyright:** 2026 Digital Currensy Inc.
**License:** Apache-2.0. The file named LICENSE is the unmodified Apache text. The copyright notice is in NOTICE and at the top of each source file.

## What it decides

Thin, wide, weak, crack, missing, load, or ok. Passing the shape check is not a keep. Ok is not a structural keep and no finite-element model is run. A load result is the closed-form comparison, not a mesh and not a keep.

## The order inside hold()

`hold(span_m, roof_m, tensile_mpa, crack, depth_m=None)` returns the first hit, in this order:

1. **missing** — `span_m` is missing or `roof_m` is missing.
2. **missing** — `span_m` is negative or `roof_m` is negative. A present `tensile_mpa` under 0 is missing, not weak. A present `depth_m` under 0 is missing.
3. **thin** — `roof_m < 2`.
4. **wide** — `span_m > 5000`.
5. **weak** — `tensile_mpa` is present and `tensile_mpa < 1`.
6. **crack** — `crack` is true.
7. **load** — `depth_m` is present and `depth_m >= 0`, and lithostatic stress at that depth is greater than the Hoek-Brown unconfined mass strength. The comparison is density 3100 and gravity 1.62 against the Hoek-Brown unconfined mass strength already in `hoek.py`. That comparison is not a mesh. No finite-element model is run.
8. **ok** — none of the above.

The line prints span, roof, tensile, crack, the Hoek-Brown unconfined strength `ucs`, and lithostatic stress. lithostatic is unset when depth was not supplied. A blank required number is missing. A non-finite number is missing. It takes the same branch `hold()` already uses for `None`. A missing span or a missing thickness is `missing`, not ok. A blank tensile cell is not a weak roof; the weak check runs only when a number is present. A negative tensile is missing, not weak. Every existing four-argument call leaves depth unset. Ok is not a structural keep and no finite-element model is run.

## Closed forms, not a mesh

`thermal.py` is a closed form, not a mesh. Surface swing is noon mid `392` K minus dawn `95` K. Burial damping is that swing times `exp(-depth / skin)`. Skin is `0.07` m in regolith and `0.75` m in rock. A non-positive skin, or a ratio under `1e-12`, returns `0`. Constrained stress in MPa is `(30 GPa × 1000 × 6e-6 × delta) / (1 − 0.25)`. The same file states noon `387`–`397` K, equator mean `215.5` K, equator max `392.3` K, equator min `94.3` K, polar max `202` K, polar min `50` K, and a counsel delta of `300` K. That temperature is not a roof.

`hoek.py` is a closed-form Hoek–Brown envelope, not a mesh. Constants in the file: GSI `70`, disturbance `0`, mi `17` (conservative), `20` (Blair), and `25` (basalt), intact strength `100` MPa, density `3100`, lunar gravity `1.62`, burial `135` m, thin-roof mark `2` m. `mb = mi × exp((GSI − 100) / (28 − 14D))`, `s = exp((GSI − 100) / (9 − 3D))`, `a = 0.5 + (1/6) × (exp(−GSI/15) − exp(−20/3))`. Major principal stress is `sigma3 + 100 × (mb × sigma3 / 100 + s) ^ a` when the inside term is positive, otherwise `sigma3`. Lithostatic stress in MPa is `3100 × 1.62 × depth / 1e6`. `hoek_is_keep` stays false. ABAQUS is not run.

A beam formula is not an arch survey.

## Worked rows

`examples/roof.csv` uses the four `hold()` inputs and nothing else. Worked rows are not a vault a customer asked to keep.

## What it will not do

- Run ABAQUS.
- Run a finite-element model.
- Treat a beam formula as an arch survey.
- Treat ok as a structural keep.

## Run

```
PYTHONPATH=src python -m unittest tests.test_kernel
PYTHONPATH=src python -m archhold examples/roof.csv
```

Copyright 2026 Digital Currensy Inc. Apache-2.0.
