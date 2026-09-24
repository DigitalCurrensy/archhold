# ARCHHOLD

[![check](https://github.com/DigitalCurrensy/archhold/actions/workflows/check.yml/badge.svg)](https://github.com/DigitalCurrensy/archhold/actions/workflows/check.yml)

For a structural check of one small rectangular roof, from the span, the thickness, and the rock numbers you supply.

The mesh is plane stress. It names the load factor the returned stress can carry. Full burial does not balance. `verify` checks an Ed25519 signature of that line. The public key is in the repository. The private key is not. The signature is of the bytes. It is not a stamp.

This is not ABAQUS and it is not UDEC. Ok is not a keep.

## Install

```bash
pip install -e .
PYTHONPATH=src python -m unittest tests.test_kernel
```

## First command

```bash
PYTHONPATH=src python -m archhold examples/roof.csv
```

The rest of this file is the rule that command prints.

## Record

`--json` prints one object. The process exit code is that object's `exit`. 0 is a pass word (`ok`, `pass`, `scored`, `path`). 1 is a refusal. 2 means the file could not be read. `keep` is false. `absent` is what this output does not contain: a stamp, measured basin months, and the points inside a `.laz` file.

This object is not WaterML and it is not a USGS response.

```json
{
  "absent": [
    "stamp",
    "measured_months",
    "laz_points"
  ],
  "desk": "archhold",
  "exit": 1,
  "formula": "Ok is not a keep. Full burial does not balance.",
  "keep": false,
  "rows": [
    {
      "line": "ok span=45 roof=135 tensile=missing crack=false ucs=18.80243413 lithostatic=unset",
      "word": "ok"
    },
    {
      "line": "missing span=missing roof=100 tensile=missing crack=false ucs=18.80243413 lithostatic=unset",
      "word": "missing"
    },
    {
      "line": "missing span=45 roof=missing tensile=missing crack=false ucs=18.80243413 lithostatic=unset",
      "word": "missing"
    },
    {
      "line": "thin span=45 roof=1 tensile=missing crack=false ucs=18.80243413 lithostatic=unset",
      "word": "thin"
    },
    {
      "line": "wide span=5001 roof=135 tensile=missing crack=false ucs=18.80243413 lithostatic=unset",
      "word": "wide"
    },
    {
      "line": "weak span=45 roof=135 tensile=0.5 crack=false ucs=18.80243413 lithostatic=unset",
      "word": "weak"
    },
    {
      "line": "crack span=45 roof=135 tensile=missing crack=true ucs=18.80243413 lithostatic=unset",
      "word": "crack"
    },
    {
      "line": "ok span=5000 roof=2 tensile=1 crack=false ucs=18.80243413 lithostatic=unset",
      "word": "ok"
    },
    {
      "line": "missing span=missing roof=1 tensile=0.5 crack=true ucs=18.80243413 lithostatic=unset",
      "word": "missing"
    }
  ],
  "word": "missing"
}
```


The caller supplies the span and the roof numbers: span, thickness, tensile strength, and a declared crack.

**Owner:** Digital Currensy Inc.
**Copyright:** 2026 Digital Currensy Inc.
**License:** Apache-2.0. The file named LICENSE is the unmodified Apache text. The copyright notice is in NOTICE and at the top of each source file.

## What it decides

Thin, wide, weak, crack, missing, load, or ok. Passing the shape check is not a keep. Ok is not a structural keep. `python -m archhold verify` checks an Ed25519 signature of the worked line. The public key is in the repo. The private key is not. That signature is of the bytes. It is not a stamp. A dilation other than 0 is refused. An outline that is not this rectangle is refused. The burial load still stops at 5.911552654. The single-depth comparison is one number. The mesh command repeats that number on a grid whose edges do not carry load. The fea command solves plane-stress triangles, cuts principals that leave the Hoek-Brown envelope, then line-searches that elastic stiffness. The returned stress balances only up to the printed limit. It is not ABAQUS and it is not UDEC.

## The order inside hold()

`hold(span_m, roof_m, tensile_mpa, crack, depth_m=None)` returns the first hit, in this order:

1. **missing** — `span_m` is missing or `roof_m` is missing.
2. **missing** — `span_m` is negative or `roof_m` is negative. A present `tensile_mpa` under 0 is missing, not weak. A present `depth_m` under 0 is missing.
3. **thin** — `roof_m < 2`.
4. **wide** — `span_m > 5000`.
5. **weak** — `tensile_mpa` is present and `tensile_mpa < 1`.
6. **crack** — `crack` is true.
7. **load** — `depth_m` is present and `depth_m >= 0`, and lithostatic stress at that depth is greater than the Hoek-Brown unconfined mass strength. The comparison is density 3100 and gravity 1.62 against the Hoek-Brown unconfined mass strength already in `hoek.py`. One depth is one node. The mesh command places that comparison on a grid whose edges do not carry load.
8. **ok** — none of the above.

The line prints span, roof, tensile, crack, the Hoek-Brown unconfined strength `ucs`, and lithostatic stress. lithostatic is unset when depth was not supplied. A blank required number is missing. A non-finite number is missing. It takes the same branch `hold()` already uses for `None`. A missing span or a missing thickness is `missing`, not ok. A blank tensile cell is not a weak roof; the weak check runs only when a number is present. A negative tensile is missing, not weak. Every existing four-argument call leaves depth unset. Ok is not a structural keep.

## Closed forms, not a mesh

`thermal.py` is a closed form, not a mesh. Surface swing is noon mid `392` K minus dawn `95` K. Burial damping is that swing times `exp(-depth / skin)`. Skin is `0.07` m in regolith and `0.75` m in rock. A non-positive skin, or a ratio under `1e-12`, returns `0`. Constrained stress in MPa is `(30 GPa × 1000 × 6e-6 × delta) / (1 − 0.25)`. The same file states noon `387`–`397` K, equator mean `215.5` K, equator max `392.3` K, equator min `94.3` K, polar max `202` K, polar min `50` K, and a counsel delta of `300` K. That temperature is not a roof.

`hoek.py` is a closed-form Hoek–Brown envelope. Constants in the file: GSI `70`, disturbance `0`, mi `17` (conservative), `20` (Blair), and `25` (basalt), intact strength `100` MPa, density `3100`, lunar gravity `1.62`, burial `135` m, thin-roof mark `2` m. `mb = mi × exp((GSI − 100) / (28 − 14D))`, `s = exp((GSI − 100) / (9 − 3D))`, `a = 0.5 + (1/6) × (exp(−GSI/15) − exp(−20/3))`. Major principal stress is `sigma3 + 100 × (mb × sigma3 / 100 + s) ^ a` when the inside term is positive, otherwise `sigma3`. Lithostatic stress in MPa is `3100 × 1.62 × depth / 1e6`. The tensile cutoff is `s × 100 / mb`, a positive number. Compression is positive. If the smaller principal is tension beyond that cutoff, the hit is `tension`. A smaller tension gets no confinement credit and is checked against the envelope at zero confinement. A point above the envelope is `envelope`. `hoek_is_keep` stays false. ABAQUS is not run.

`mesh.py` places that same lithostatic stress on a rectangular grid. `x` runs from 0 to the span. Depth runs from 0 to the depth you pass. `nx` and `nz` are node counts, each at least 2. A 4-neighbor edge means two nodes share a side. The edge does not carry stress, and there is no stiffness matrix. A node is over strength when its own `3100 × 1.62 × depth / 1e6` is greater than the Hoek–Brown unconfined mass strength. `components` counts how many connected groups those over-strength nodes form. The shape word still wins when the roof is thin, wide, weak, cracked, or missing.

```bash
PYTHONPATH=src python -m archhold mesh 45 135 4000 3 3
```

```text
load nodes=9 edges=12 over=3 components=1 max=20.088 ucs=18.80243413 span=45 roof=135 depth=4000
```

The three deep nodes are the bottom row. They share sides, so they are one component. A node count under 2, a negative span or depth, or a non-finite number is `not a mesh`.

`fea.py` is the mesh whose edges carry load. Each rectangle splits into two constant-strain triangles. `K = 1 m × area × Bᵀ × D × B`. `D` is plane stress with Young's modulus `30 GPa` and Poisson's ratio `0.25`. A unit horizontal strain on the triangle `(0,0), (2,0), (0,2)` returns stress `(32000, 8000, 0)` MPa. Tension is positive inside the element. The envelope uses compression as positive.

The strip runs from `y = 0` at the opening to `y = roof` at the extrados. Side nodes cannot move vertically. The lower-left node cannot move horizontally. The top edge is loaded with the lithostatic pressure `3100 × 1.62 × depth / 1e6`, downward. Each triangle also carries self-weight `3100 × 1.62`, split across its three nodes. Forces are meganewtons when stress is MPa and lengths are meters. The dense solve stops above 64 nodes. The first solve is elastic. `return_principals` then cuts each triangle. The stress used for the correction keeps that trial's principal frame: the deviator is scaled so the principals match the returned pair, and the hydrostatic part is the mean of that pair, tension positive. If the trial deviator radius is zero, the frame is ambiguous and the trial-major scale rule is used. The returned stress used for the correction is the elastic stress scaled by `returned_sigma1 / trial_sigma1` when `trial_sigma1` is nonzero, and unchanged when the element was elastic. Elements that returned to the apex use a zero stress for the correction only. Internal force is `1 m × area × Bᵀ × stress`, with the same `B` as `K`. Unbalanced force is the applied load minus those internal forces. Fixed degrees of freedom stay 0. One solve, `K du = unbalanced`, is added to the displacement. `iterations=1` means that single correction. It does not mean the plastic return converged, and it does not mean the updated elastic stress is in equilibrium. `max_sig1` and `min_sig3` are principals of the elastic stress recomputed from the updated displacement. The envelope check and the local return run on that new stress and set the word, `plastic`, and `back_sig1`. A thin, wide, weak, cracked, or missing roof keeps that shape word. Otherwise the word is `hoek` when any new triangle is outside the envelope, else `ok`. Ok is not a structural keep. The vertical reactions still balance the applied load of the elastic trial. `residual` is the max absolute unbalanced force of the returned stress before the correction, on free degrees of freedom. `residual_after` is that imbalance again after one correction, using the returned stress of the updated displacement. Each triangle stores a plastic strain. The trial stress is the elastic matrix times the strain minus that plastic strain. The return cuts the trial. The plastic strain then grows by the compliance times the stress that was cut off. The imbalance is solved with the original elastic stiffness. A step is kept only when it cuts the opening imbalance by at least 1%. The same solve is repeated at a scaled load. `limit` is the largest scale, found by bisection, whose imbalance falls under `1e-9`. On the worked roof that scale is 0.3608335853. At the full burial load the imbalance goes from 15.11887723 to 5.911552654 in 5 steps and stops. The yielded tangent of this return is singular, so a numerical Newton step is unbounded and is not used. A dilation angle is not in this file. `digest` is the first 16 hex characters of SHA-256 of the line before that word. A person can sign that digest. Choosing GSI, mi, the intact strength, and a real outline is also a person. A residual under `1e-9` prints as `0`. If the full load stays elastic, `limit` is 1 and both residuals print `0`. The local return is not an associated flow rule. UDEC is Itasca's distinct-element program. This file does not call it.

```bash
PYTHONPATH=src python -m archhold fea 45 10 135 3 3
```

```text
hoek elements=8 nodes=9 over=1 plastic=1 fail=tension max_sig1=2.10956222 back_sig1=2.10956222 min_sig3=-0.6141579063 ucs=18.80243413 cutoff=0.6126583006 pressure=0.67797 reaction=32.76855 applied=-32.76855 residual=15.11887723 residual_after=5.911552654 iterations=5 limit=0.3608335853 e=30000 nu=0.25 digest=b5a7c9ea7dc5398b
```

A beam formula is not an arch survey.

## Worked rows

`examples/roof.csv` uses the four `hold()` inputs and nothing else. Worked rows are not a vault a customer asked to keep.

## What it will not do

- Run ABAQUS.
- Call UDEC. That is Itasca's distinct-element program. This repository is continuum triangles, not blocks and contacts.
- Treat the full-load imbalance as zero. Plastic strain is stored, and the returned stress is in equilibrium at `limit=0.3608335853`. At the burial load it stops at 5.911552654. A dilation angle is not in this file. It is not UDEC.
- Treat ok as a structural keep.

## Run

```
PYTHONPATH=src python -m unittest tests.test_kernel
PYTHONPATH=src python -m archhold examples/roof.csv
```

Copyright 2026 Digital Currensy Inc. Apache-2.0.
