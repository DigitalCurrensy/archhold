# Copyright 2026 Digital Currensy Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Plane-stress triangles, then the Hoek-Brown envelope. Not ABAQUS. Not a plastic return map."""

from __future__ import annotations

import math

from archhold.arch import hold
from archhold.hoek import (
    G_MOON,
    RHO,
    envelope_hit,
    lithostatic_mpa,
    return_principals,
    tensile_cutoff_mpa,
    ucs_mass_mpa,
)
from archhold.thermal import POISSON, YOUNG_GPA

THICKNESS_M = 1.0
MAX_NODES = 64
E_MPA = YOUNG_GPA * 1e3


def _finite(value: float) -> None:
    if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value):
        raise ValueError("not a mesh")


def plane_stress_d(young_mpa: float = E_MPA, poisson: float = POISSON) -> list[list[float]]:
    """Isotropic plane-stress matrix. Tension is positive. Units are MPa."""
    _finite(young_mpa)
    _finite(poisson)
    if young_mpa <= 0 or not -1.0 < poisson < 0.5:
        raise ValueError("not a mesh")
    scale = young_mpa / (1.0 - poisson * poisson)
    shear = scale * (1.0 - poisson) / 2.0
    return [
        [scale, scale * poisson, 0.0],
        [scale * poisson, scale, 0.0],
        [0.0, 0.0, shear],
    ]


def _matmul(left: list[list[float]], right: list[list[float]]) -> list[list[float]]:
    out = [[0.0 for _ in right[0]] for _ in left]
    for i, row in enumerate(left):
        for k, value in enumerate(row):
            if value == 0.0:
                continue
            for j in range(len(right[0])):
                out[i][j] += value * right[k][j]
    return out


def _transpose(matrix: list[list[float]]) -> list[list[float]]:
    return [list(column) for column in zip(*matrix)]


def _matvec(matrix: list[list[float]], vector: list[float]) -> list[float]:
    return [sum(value * vector[j] for j, value in enumerate(row)) for row in matrix]


def triangle_geometry(
    corners: list[tuple[float, float]],
) -> tuple[float, list[list[float]]]:
    """Area and the strain-displacement matrix. Corners are counterclockwise."""
    (x1, y1), (x2, y2), (x3, y3) = corners
    twice = x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)
    if twice <= 0.0:
        raise ValueError("not a mesh")
    b = (y2 - y3, y3 - y1, y1 - y2)
    c = (x3 - x2, x1 - x3, x2 - x1)
    scale = 1.0 / twice
    strain = [
        [b[0] * scale, 0.0, b[1] * scale, 0.0, b[2] * scale, 0.0],
        [0.0, c[0] * scale, 0.0, c[1] * scale, 0.0, c[2] * scale],
        [c[0] * scale, b[0] * scale, c[1] * scale, b[1] * scale, c[2] * scale, b[2] * scale],
    ]
    return twice / 2.0, strain


def triangle_stiffness(
    corners: list[tuple[float, float]],
    young_mpa: float = E_MPA,
    poisson: float = POISSON,
    thickness_m: float = THICKNESS_M,
) -> list[list[float]]:
    """K = thickness * area * B^T * D * B. Displacements are meters. Forces are MN."""
    area, strain = triangle_geometry(corners)
    elastic = plane_stress_d(young_mpa, poisson)
    core = _matmul(elastic, strain)
    gram = _matmul(_transpose(strain), core)
    weight = thickness_m * area
    return [[value * weight for value in row] for row in gram]


def triangle_stress(
    corners: list[tuple[float, float]],
    displacement: list[float],
    young_mpa: float = E_MPA,
    poisson: float = POISSON,
) -> tuple[float, float, float]:
    """Tension-positive sxx, syy, txy in MPa."""
    _area, strain = triangle_geometry(corners)
    return tuple(_matvec(_matmul(plane_stress_d(young_mpa, poisson), strain), displacement))  # type: ignore[return-value]


def principals_compression(sxx: float, syy: float, txy: float) -> tuple[float, float]:
    """Return sigma1, sigma3 with compression positive and sigma1 >= sigma3."""
    average = 0.5 * (sxx + syy)
    radius = math.hypot(0.5 * (sxx - syy), txy)
    most_tension = average + radius
    least_tension = average - radius
    return -least_tension, -most_tension


def _solve(matrix: list[list[float]], rhs: list[float]) -> list[float]:
    size = len(rhs)
    rows = [matrix[i][:] + [rhs[i]] for i in range(size)]
    for col in range(size):
        pivot = max(range(col, size), key=lambda row: abs(rows[row][col]))
        if abs(rows[pivot][col]) < 1e-14:
            raise ValueError("not a mesh")
        rows[col], rows[pivot] = rows[pivot], rows[col]
        scale = rows[col][col]
        for j in range(col, size + 1):
            rows[col][j] /= scale
        for row in range(size):
            if row == col:
                continue
            factor = rows[row][col]
            if factor == 0.0:
                continue
            for j in range(col, size + 1):
                rows[row][j] -= factor * rows[col][j]
    return [rows[i][size] for i in range(size)]


def _nodes(span_m: float, roof_m: float, nx: int, nz: int) -> list[tuple[float, float]]:
    nodes: list[tuple[float, float]] = []
    for j in range(nz):
        y = roof_m * j / (nz - 1)
        for i in range(nx):
            nodes.append((span_m * i / (nx - 1), y))
    return nodes


def _triangles(nx: int, nz: int) -> list[tuple[int, int, int]]:
    faces: list[tuple[int, int, int]] = []
    for j in range(nz - 1):
        for i in range(nx - 1):
            a = j * nx + i
            b = a + 1
            c = a + nx
            d = c + 1
            faces.append((a, b, d))
            faces.append((a, d, c))
    return faces


def score_fea(span_m: float, roof_m: float, depth_m: float, nx: int, nz: int) -> dict[str, float | int | str]:
    """Elastic roof strip, then the Hoek-Brown check on each triangle.

    y = 0 is the opening. y = roof is the extrados. Side nodes cannot move
    vertically. The lower-left node cannot move horizontally. The top edge
    carries lithostatic pressure downward. Every triangle also carries its
    own weight, 3100 * 1.62. Thickness out of plane is 1 m. Young's modulus
    is 30 GPa and Poisson's ratio is 0.25, the pair already used for the
    thermal stress. More than 64 nodes is refused. Principals outside the
    envelope are cut back onto it locally. The mesh is not solved again.
    This does not call a named solver.
    """
    _finite(span_m)
    _finite(roof_m)
    _finite(depth_m)
    if span_m <= 0 or roof_m <= 0 or depth_m < 0:
        raise ValueError("not a mesh")
    if type(nx) is not int or type(nz) is not int or nx < 2 or nz < 2 or nx * nz > MAX_NODES:
        raise ValueError("not a mesh")
    nodes = _nodes(span_m, roof_m, nx, nz)
    faces = _triangles(nx, nz)
    dofs = 2 * len(nodes)
    stiffness = [[0.0 for _ in range(dofs)] for _ in range(dofs)]
    force = [0.0 for _ in range(dofs)]
    weight = RHO * G_MOON / 1e6
    for face in faces:
        corners = [nodes[index] for index in face]
        local = triangle_stiffness(corners)
        area, _strain = triangle_geometry(corners)
        share = weight * area * THICKNESS_M / 3.0
        for local_i, node in enumerate(face):
            force[2 * node + 1] -= share
            for local_j, other in enumerate(face):
                for a in range(2):
                    for b in range(2):
                        stiffness[2 * node + a][2 * other + b] += local[2 * local_i + a][2 * local_j + b]
    pressure = lithostatic_mpa(depth_m)
    dx = span_m / (nx - 1)
    edge_force = pressure * THICKNESS_M * dx / 2.0
    for i in range(nx - 1):
        left = (nz - 1) * nx + i
        right = left + 1
        force[2 * left + 1] -= edge_force
        force[2 * right + 1] -= edge_force
    fixed: set[int] = set()
    for j in range(nz):
        fixed.add(2 * (j * nx) + 1)
        fixed.add(2 * (j * nx + nx - 1) + 1)
    fixed.add(0)
    free = [dof for dof in range(dofs) if dof not in fixed]
    reduced = [[stiffness[i][j] for j in free] for i in free]
    displacement = [0.0 for _ in range(dofs)]
    solved = _solve(reduced, [force[i] for i in free])
    for dof, value in zip(free, solved):
        displacement[dof] = value
    internal = _matvec(stiffness, displacement)
    residual = 0.0
    reaction_y = 0.0
    applied_y = 0.0
    for dof in range(1, dofs, 2):
        applied_y += force[dof]
        imbalance = internal[dof] - force[dof]
        if dof in fixed:
            reaction_y += imbalance
        else:
            residual = max(residual, abs(imbalance))
    sigma1 = -math.inf
    sigma3 = math.inf
    over = 0
    plastic = 0
    fail = "none"
    back = -math.inf
    for face in faces:
        corners = [nodes[index] for index in face]
        local_u = []
        for index in face:
            local_u.extend(displacement[2 * index : 2 * index + 2])
        sxx, syy, txy = triangle_stress(corners, local_u)
        major, minor = principals_compression(sxx, syy, txy)
        sigma1 = max(sigma1, major)
        sigma3 = min(sigma3, minor)
        hit = envelope_hit(major, minor)
        returned1, _returned3, mode = return_principals(major, minor)
        back = max(back, returned1)
        if mode != "elastic":
            plastic += 1
        if hit == "inside":
            continue
        over += 1
        if fail == "none" or hit == "tension":
            fail = hit
    shape = hold(span_m, roof_m, None, False, None)
    if shape == "ok":
        word = "hoek" if over else "ok"
    else:
        word = shape
    return {
        "word": word,
        "elements": len(faces),
        "nodes": len(nodes),
        "over": over,
        "plastic": plastic,
        "fail": fail,
        "back_sig1": back,
        "max_sig1": sigma1,
        "min_sig3": sigma3,
        "ucs": ucs_mass_mpa(),
        "cutoff": tensile_cutoff_mpa(),
        "pressure": pressure,
        "reaction": reaction_y,
        "applied": applied_y,
        "residual": residual,
        "young": E_MPA,
        "poisson": POISSON,
    }


def fea_line(span_m: float, roof_m: float, depth_m: float, nx: int, nz: int) -> str:
    scored = score_fea(span_m, roof_m, depth_m, nx, nz)
    residual = scored["residual"]
    residual_text = "0" if isinstance(residual, float) and residual < 1e-9 else f"{residual:.10g}"
    return (
        f"{scored['word']} elements={scored['elements']} nodes={scored['nodes']} "
        f"over={scored['over']} plastic={scored['plastic']} fail={scored['fail']} "
        f"max_sig1={scored['max_sig1']:.10g} back_sig1={scored['back_sig1']:.10g} min_sig3={scored['min_sig3']:.10g} "
        f"ucs={scored['ucs']:.10g} cutoff={scored['cutoff']:.10g} "
        f"pressure={scored['pressure']:.10g} reaction={scored['reaction']:.10g} "
        f"applied={scored['applied']:.10g} residual={residual_text} "
        f"e={scored['young']:.10g} nu={scored['poisson']:.10g}"
    )
