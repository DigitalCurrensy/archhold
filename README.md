# ARCHHOLD

The arch is the keep. A radar walk looks like a roof you can trust. Score the span against the overburden.

**Owner:** Digital Currensy Inc.
**Status:** Private. Independent tool. Not a NASA Space Apps 2026 submission.
**License of our code:** Apache-2.0

## One sentence

A published conduit looks like a vault that will hold. Name the arch against span and roof — or say the vault is not a keep.

## Wave freeze

- W0 catalog: Mare Tranquillitatis west Mini-RF arch (Carrer 2024 burial 135–175 m, span 45±7.5 m) and Marius Hills LRS rille (Kaku 2017; span undeclared). arch.py named, not run.
- W1 vault scorer: arch.py ported. MTP scores ok. MHP scores missing. Blair FEM named. Wagner 16 mare pits named, not roofs. ok is not a keep.
- W2 one bad vault: ARCH-MTP-WEST walked. Catalog ok is not a keep. Blair FEM named, not run. Wagner pits named, not roofs. Famous is not a door.
- W3 vault letter: compiled from locked fields. Fail still issues. ok still issues. ok is not a keep. Blair lithostatic named. Carrer inversion is not a roof. Counsel unsigned.
- W4 counsel pass: compiled from locked fields. Unsigned. Hoek-Brown GSI 70 named, not run. Lunar thermal cycling is not a roof. Kapton is MLI, not overburden. Station freeze.

## arch.py

```
if span_m is None or roof_m is None: missing
elif roof_m < 2: thin
elif span_m > 5000: wide
elif tensile_mpa is not None and tensile_mpa < 1: weak
elif crack: crack
else: ok
```

Missing first. Equality sits. FEM unrun. ok is not a keep.

## What it is not

- Not TUBEWALK. A walk is not a ceiling.
- Not BAGHOLD mouth. A collapsed skylight is not the remaining arch.
- Not Blair 2017 FEM run. ABAQUS stays upstream.
- Not an elastic beam. Hörz ~385 m at 65 m roof is not an arch.
- Not GRAIL km-scale as this 45 m vault.
- Not tensile as this score. Theinat named. arch.py skips None.
- Not FEASFRONT lighting. A dark roof is not a keep.
- Not DOSEPATH occupancy. Shelter is a graph box, not this span.

## Run

```
PYTHONPATH=src python -m unittest tests.test_kernel
```
