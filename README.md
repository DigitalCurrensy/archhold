# ARCHHOLD

For a reviewer deciding whether a lava-tube roof will hold a span.

**Owner:** Digital Currensy Inc.
**Copyright:** 2026 Digital Currensy Inc.
**License:** Apache-2.0. The file named LICENSE is the standard license and is not edited. The copyright notice is in NOTICE and at the top of each source file. Cited data and papers stay with their authors.
## What it decides

Thin, wide, weak, crack, missing, or ok. Ok means the shape check passed. It does not mean the roof will hold.

## The rule

Missing span or thickness is missing. A roof under the thickness gate is thin. A span over the width gate is wide. A declared strength under the gate is weak. A declared crack is a crack. Otherwise ok, and ok is not a keep. A closed-form envelope is not a mesh. No finite-element model is run.

## Worked cases

The Mare Tranquillitatis west arch and the Marius Hills rille arch are named. The synthetic arches each force one gate. They are not a vault a customer asked to keep.

## What it will not do

- Call a radar walk a roof.
- Run ABAQUS, or treat a yield envelope as a keep.
- Sign a structural letter.

## Run

```
git clone <this repo>
cd archhold
PYTHONPATH=src python -m unittest tests.test_kernel
```

Python 3.12. No third-party packages. The test is the demo.
