# ARCHHOLD

ARCHHOLD scores a roof against its span. A walk is not a ceiling. A beam is not an arch. An `ok` is not a keep.

**Owner:** Digital Currensy Inc.
**License:** Apache-2.0. Our code only. Cited papers stay with their authors.

## What it decides

Thin, wide, weak, crack, missing, or ok. Ok means the shape check passed. It does not mean the roof will hold.

## The rule

If span or roof thickness is missing, the result is missing. A roof under the thickness gate is thin. A span over the width gate is wide. A declared tensile strength under the gate is weak. A declared crack is a crack. Anything else is ok, and ok is still not a keep. A closed-form envelope is not a mesh. A finite-element model is not run here.

## Worked cases

The Mare Tranquillitatis west arch, the Marius Hills rille arch, and synthetic arches in this repository. The synthetic cases each force one gate, including a missing identity and missing inputs. They are the desk’s cases, not a vault a customer asked to keep.

## What it will not do

- Call a radar walk a roof.
- Call a collapsed skylight the remaining arch.
- Run ABAQUS, or treat a yield envelope as a keep.
- Sign a structural letter.

## Run

```
PYTHONPATH=src python -m unittest tests.test_kernel
```

Notes under `docs/` are the build record. This page is the description.
