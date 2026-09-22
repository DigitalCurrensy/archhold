# Architecture

`arch.py` is the vault kernel. Wave 0 names it. Wave 1 ports it.

Declared caches: SYN-ARCH-MTP and SYN-ARCH-MHP. Mini-RF, SELENE LRS, GRAIL, and ABAQUS stay unfetched.

Fail-closed: missing first, then thin, then wide, then weak, then crack. Equality sits. Span None or roof None is missing. Tensile None skips weak.

Parent walk: TUBEWALK owns the conduit. BAGHOLD owns the mouth. A collapsed skylight is not the remaining arch. A walk is not a ceiling.

Blair 2017 FEM (Icarus 282 47–55): 2 m roof can hold 1 km; 50 m burial up to 3.5 km fully stable; 500 m lithostatic up to 5 km. 3:1 width-to-height. GSI. Lithostatic vs Poisson. ABAQUS named, not run, not vendored. arch.py does not take a mesh.

Elastic beam (Hörz 1985 / prior models Blair cites): ~385 m max at 65 m roof, 2500 kg m⁻³. A beam is not an arch. Not this score.

Theinat: tensile << compressive. Blair ignored tensile. Named. arch.py skips tensile None.

GRAIL GRGM1200A is km-scale. A 45 m span cannot be a GRAIL detection. Gravity is not a roof.

Carrer 2024: west conduit span ~45±7.5 m, burial 135–175 m below surface. Burial is declared overburden, not a live FEM roof.

Kaku 2017: LRS second echo, ε=1 → 225 m, ε=4 → ~100 m. Width undeclared. Missing until a span is named.
