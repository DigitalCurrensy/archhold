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

"""A rectangular grid of the closed-form lithostatic check. Not a finite-element solve."""

from __future__ import annotations

import math

from archhold.arch import hold
from archhold.hoek import lithostatic_mpa, ucs_mass_mpa


def _finite(value: float) -> None:
    if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value):
        raise ValueError("not a mesh")


def rectangular_mesh(
    span_m: float, depth_m: float, nx: int, nz: int
) -> tuple[list[tuple[float, float]], list[tuple[int, int]]]:
    """Nodes (x, depth) and 4-neighbor edges.

    x runs from 0 to span. Depth runs from 0 to depth_m. nx and nz count
    nodes, not elements, and each must be at least 2. An edge means the
    two nodes share a side. It does not carry stress.
    """
    _finite(span_m)
    _finite(depth_m)
    if span_m < 0 or depth_m < 0:
        raise ValueError("not a mesh")
    if type(nx) is not int or type(nz) is not int or nx < 2 or nz < 2:
        raise ValueError("not a mesh")
    nodes: list[tuple[float, float]] = []
    for j in range(nz):
        depth = depth_m * j / (nz - 1)
        for i in range(nx):
            x = span_m * i / (nx - 1)
            nodes.append((x, depth))
    edges: list[tuple[int, int]] = []
    for j in range(nz):
        for i in range(nx):
            here = j * nx + i
            if i + 1 < nx:
                edges.append((here, here + 1))
            if j + 1 < nz:
                edges.append((here, here + nx))
    return nodes, edges


def _components(edges: list[tuple[int, int]], over: set[int]) -> int:
    neighbors: dict[int, list[int]] = {node: [] for node in over}
    for left, right in edges:
        if left in over and right in over:
            neighbors[left].append(right)
            neighbors[right].append(left)
    seen: set[int] = set()
    components = 0
    for start in over:
        if start in seen:
            continue
        components += 1
        stack = [start]
        seen.add(start)
        while stack:
            node = stack.pop()
            for other in neighbors[node]:
                if other not in seen:
                    seen.add(other)
                    stack.append(other)
    return components


def score_mesh(
    span_m: float,
    roof_m: float,
    depth_m: float,
    nx: int,
    nz: int,
    tensile_mpa: float | None = None,
    crack: bool = False,
) -> dict[str, float | int | str]:
    """Score every node with lithostatic stress against the Hoek-Brown strength.

    The shape word from hold() wins when it is not ok and not load. Otherwise
    the word is load when any node is over strength, else ok. Stress does not
    move along an edge.
    """
    _finite(roof_m)
    nodes, edges = rectangular_mesh(span_m, depth_m, nx, nz)
    strength = ucs_mass_mpa()
    stresses = [lithostatic_mpa(depth) for _x, depth in nodes]
    over = {index for index, stress in enumerate(stresses) if stress > strength}
    shape = hold(span_m, roof_m, tensile_mpa, crack, depth_m)
    if shape in {"ok", "load"}:
        word = "load" if over else "ok"
    else:
        word = shape
    return {
        "word": word,
        "nodes": len(nodes),
        "edges": len(edges),
        "over": len(over),
        "components": _components(edges, over),
        "max": max(stresses),
        "ucs": strength,
    }


def mesh_line(
    span_m: float,
    roof_m: float,
    depth_m: float,
    nx: int,
    nz: int,
) -> str:
    scored = score_mesh(span_m, roof_m, depth_m, nx, nz)
    return (
        f"{scored['word']} nodes={scored['nodes']} edges={scored['edges']} "
        f"over={scored['over']} components={scored['components']} "
        f"max={scored['max']:.10g} ucs={scored['ucs']:.10g} "
        f"span={span_m:.10g} roof={roof_m:.10g} depth={depth_m:.10g}"
    )
