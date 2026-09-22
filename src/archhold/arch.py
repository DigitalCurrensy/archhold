def hold(
    span_m: float | None,
    roof_m: float | None,
    tensile_mpa: float | None,
    crack: bool,
) -> str:
    if span_m is None or roof_m is None:
        return "missing"
    if roof_m < 2:
        return "thin"
    if span_m > 5000:
        return "wide"
    if tensile_mpa is not None and tensile_mpa < 1:
        return "weak"
    if crack:
        return "crack"
    return "ok"
