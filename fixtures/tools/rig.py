#!/usr/bin/env python3
"""Rig evaluation shared by the generator and the preview harness.

The manifest describes one attachment rule: put a part's own pivot on the named
joint of its parent, then rotate counter-clockwise by `rest_angle`. This module
is the only implementation of that rule. The generator uses it to check what it
wrote; `preview_cast.py` uses it to pose. Neither carries joint offsets of its
own — every number comes from `cast/manifest.json`.
"""

from __future__ import annotations

import math

Point = tuple[float, float]


def rotate_point(p, origin, angle_deg: float) -> Point:
    """Rotate `p` about `origin` counter-clockwise on screen, in y-down pixels."""
    t = math.radians(angle_deg)
    dx, dy = p[0] - origin[0], p[1] - origin[1]
    return (origin[0] + dx * math.cos(t) + dy * math.sin(t),
            origin[1] - dx * math.sin(t) + dy * math.cos(t))


def solve_frames(attach: dict, records: dict) -> dict:
    """Map every layer to (cumulative angle, its pivot in character space).

    `attach` is `rig.<character>.attach`; `records` maps layer name to its part
    record. A part whose attachment carries a constraint that drops rotation
    inheritance keeps its own `rest_angle` and nothing of its parent's.

    This is the rest pose. `solve_pose` below is the same tree under a set of
    bone angles and a root placement.
    """
    solved: dict[str, tuple[float, Point]] = {}

    def solve(layer: str):
        if layer in solved:
            return solved[layer]
        entry = attach[layer]
        parent = entry["parent"]
        if parent is None:
            solved[layer] = (float(entry["rest_angle"]), (0.0, 0.0))
            return solved[layer]
        p_angle, p_pivot_char = solve(parent)
        where = joint_point(records, solved, parent, entry["joint"])
        constraint = entry.get("constraint")
        angle = p_angle + float(entry["rest_angle"])
        if constraint and not constraint.get("inherit_rotation", True):
            angle = float(entry["rest_angle"])
        solved[layer] = (angle, where)
        return solved[layer]

    for layer in attach:
        solve(layer)
    return solved


def joint_point(records: dict, solved: dict, layer: str, joint: str) -> Point:
    """Character-space position of a named joint on an already-solved part."""
    record = records[layer]
    angle, pivot_char = solved[layer]
    pivot = record["pivot"]
    where = rotate_point(record["joints"][joint], pivot, angle)
    return (pivot_char[0] + where[0] - pivot[0],
            pivot_char[1] + where[1] - pivot[1])


def part_point(records: dict, solved: dict, layer: str, p) -> Point:
    """Character-space position of any point given in a part's own pixels."""
    record = records[layer]
    angle, pivot_char = solved[layer]
    pivot = record["pivot"]
    where = rotate_point(p, pivot, angle)
    return (pivot_char[0] + where[0] - pivot[0],
            pivot_char[1] + where[1] - pivot[1])


# --------------------------------------------------------------------------
# skinning
# --------------------------------------------------------------------------
#
# A bone is a rotation about a head point that is itself an existing rig joint.
# Rest is identity: at rest every bone's transform is the identity, so a mesh
# vertex sits exactly where the rigid rest pose puts it. A pose supplies an angle
# per bone; a bone's transform is its parent's, composed with a rotation about
# its own rest head. A vertex is then the weighted sum of its bones applied to
# its rest position — linear blend skinning, in character space, on a rest pose
# that is already solved. Every transform below is (angle, tx, ty): p -> R p + t.

def rot_about(head: Point, angle_deg: float) -> tuple:
    """Rotation about a point, as (angle, tx, ty)."""
    turned = rotate_point(head, (0.0, 0.0), angle_deg)
    return (angle_deg, head[0] - turned[0], head[1] - turned[1])


def compose(outer: tuple, inner: tuple) -> tuple:
    """`outer` applied after `inner`."""
    moved = rotate_point((inner[1], inner[2]), (0.0, 0.0), outer[0])
    return (outer[0] + inner[0], moved[0] + outer[1], moved[1] + outer[2])


def apply(transform: tuple, p) -> Point:
    turned = rotate_point(p, (0.0, 0.0), transform[0])
    return (turned[0] + transform[1], turned[1] + transform[2])


def root_transform(root: Point = (0.0, 0.0), root_angle: float = 0.0) -> tuple:
    """Where a pose puts the whole character: turn about the origin, then move.

    A character's origin is its root part's pivot, so a root angle is a rotation
    about (0, 0) in character space and `root` is a translation after it. Both
    are zero in a pose that only bends bones.
    """
    return compose((0.0, root[0], root[1]), rot_about((0.0, 0.0), root_angle))


def bone_transforms(doc: dict, character: str, angles: dict,
                    records: dict | None = None, solved: dict | None = None,
                    root: Point = (0.0, 0.0), root_angle: float = 0.0) -> dict:
    """Bone name to its (angle, tx, ty) for one pose.

    A bone with no parent carries the root placement, so a root translation or
    root angle moves the skin as well as the rigid parts.
    """
    group = doc["rig"][character]
    bones = {b["name"]: b for b in group.get("bones", [])}
    if records is None or solved is None:
        records, solved = frames_of(doc, character)
    base = root_transform(root, root_angle)
    out: dict[str, tuple] = {}

    def resolve(name: str) -> tuple:
        if name in out:
            return out[name]
        bone = bones[name]
        layer, joint = bone["head"].split("/")
        head = joint_point(records, solved, layer, joint)
        transform = rot_about(head, float(angles.get(name, 0.0)))
        transform = compose(resolve(bone["parent"]) if bone["parent"] else base,
                            transform)
        out[name] = transform
        return transform

    for name in bones:
        resolve(name)
    return out


def rest_vertices(records: dict, solved: dict, layer: str) -> list:
    """A part's mesh vertices in character space, before any pose."""
    return [part_point(records, solved, layer, v)
            for v in records[layer]["mesh"]["vertices"]]


def skin(rest: list, mesh: dict, transforms: dict) -> list:
    """Linear blend skinning: weighted bone transforms over rest positions."""
    bones = mesh["bones"]
    out = []
    for point, weights in zip(rest, mesh["weights"]):
        x = y = 0.0
        for name, w in zip(bones, weights):
            if not w:
                continue
            px, py = apply(transforms[name], point)
            x += w * px
            y += w * py
        out.append((x, y))
    return out


def barycentric(mesh: dict, p) -> tuple:
    """Locate a part-space point in the mesh: (triangle, (a, b, c)).

    A joint on a meshed part is a point *on the mesh*, not a rigid offset from
    the pivot, so this is how a contact point or a child's attachment point
    survives deformation.
    """
    verts = mesh["vertices"]
    best, best_gap = None, None
    for tri in mesh["triangles"]:
        (x1, y1), (x2, y2), (x3, y3) = (verts[i] for i in tri)
        det = (y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3)
        if det == 0:
            continue
        a = ((y2 - y3) * (p[0] - x3) + (x3 - x2) * (p[1] - y3)) / det
        b = ((y3 - y1) * (p[0] - x3) + (x1 - x3) * (p[1] - y3)) / det
        c = 1.0 - a - b
        gap = -min(a, b, c, 0.0)
        if best_gap is None or gap < best_gap:
            best, best_gap = (tri, (a, b, c)), gap
        if gap == 0.0:
            break
    return best


def deform_point(mesh: dict, rest: list, posed: list, p) -> Point:
    """Where a part-space point lands once the part is deformed."""
    tri, (a, b, c) = barycentric(mesh, p)
    i, j, k = tri
    return (a * posed[i][0] + b * posed[j][0] + c * posed[k][0],
            a * posed[i][1] + b * posed[j][1] + c * posed[k][1])


def point_weights(mesh: dict, p) -> list:
    """Bone weights interpolated at a part-space point."""
    tri, bary = barycentric(mesh, p)
    return [sum(w * mesh["weights"][i][b] for w, i in zip(bary, tri))
            for b in range(len(mesh["bones"]))]


def records_of(doc: dict, character: str) -> dict:
    """Layer name to part record, for one character group."""
    return {p["layer"]: p for p in doc["parts"] if p["character"] == character}


def frames_of(doc: dict, character: str) -> tuple[dict, dict]:
    """(records, solved) for one character group."""
    records = records_of(doc, character)
    return records, solve_frames(doc["rig"][character]["attach"], records)


def pose_slice(pose: dict, character: str) -> dict:
    """One character's share of a recorded pose, ready for `solve_pose`."""
    def part(field, default):
        return (pose.get(field) or {}).get(character) or default

    return {"angles": part("angles", {}),
            "root": tuple(part("root", (0.0, 0.0))),
            "root_angle": float(part("root_angle", 0.0))}


def solve_pose(doc: dict, character: str, angles: dict | None = None,
               root: Point = (0.0, 0.0), root_angle: float = 0.0) -> tuple:
    """Solve one pose for a whole group: (records, frames, meshes).

    `frames[layer]` is (angle in character space, the layer's pivot in character
    space, the pose rotation it inherited). `meshes[layer]` is (rest vertices,
    skinned vertices) for *every* meshed part, whether or not anything hangs off
    it: a meshed part is drawn from its skinned vertices, so a mesh solved only
    when some child needs its deformed joints would leave leaf parts rigid.

    A rigid part is placed the way the rest pose places it, except that its
    anchor comes from the parent's deformed mesh when the parent has one, and it
    takes the bone angles blended at that anchor. That is what carries a hand on
    a bending arm and a contact on a bending leg.

    `attach.constraint` restricts what a part inherits. A constraint that drops
    rotation inheritance takes only the translation axes it names, and one
    pinned to the character ground plane holds its y on that plane, which is the
    rest-pose plane: the floor does not move when the character does.
    """
    angles = angles or {}
    group = doc["rig"][character]
    records, rest_solved = frames_of(doc, character)
    planes = {entry["part"]: joint_point(records, rest_solved,
                                         entry["part"], entry["joint"])[1]
              for entry in group.get("ground", [])}
    transforms = bone_transforms(doc, character, angles, records, rest_solved,
                                 root=root, root_angle=root_angle)

    meshes: dict[str, tuple] = {}
    for layer, record in records.items():
        if record["mesh"] is None:
            continue
        rest = rest_vertices(records, rest_solved, layer)
        meshes[layer] = (rest, skin(rest, record["mesh"], transforms))

    attach = group["attach"]
    frames: dict[str, tuple] = {}

    def root_layer(layer: str) -> str:
        while attach[layer]["parent"] is not None:
            layer = attach[layer]["parent"]
        return layer

    def solve(layer: str) -> tuple:
        if layer in frames:
            return frames[layer]
        entry = attach[layer]
        parent = entry["parent"]
        rest_angle, rest_pivot = rest_solved[layer]
        if parent is None:
            frames[layer] = (rest_angle + root_angle,
                             (rest_pivot[0] + root[0], rest_pivot[1] + root[1]),
                             root_angle)
            return frames[layer]
        _, p_pos, p_extra = solve(parent)
        p_rest = rest_solved[parent][1]
        shift = (p_pos[0] - p_rest[0], p_pos[1] - p_rest[1])
        record = records[parent]
        constraint = entry.get("constraint") or {}
        inherits_rotation = constraint.get("inherit_rotation", True)
        deformed = meshes.get(parent)
        if inherits_rotation and deformed is not None:
            joint = record["joints"][entry["joint"]]
            where = deform_point(record["mesh"], *deformed, joint)
            weights = point_weights(record["mesh"], joint)
            extra = sum(w * transforms[b][0]
                        for w, b in zip(weights, record["mesh"]["bones"]))
        else:
            rest_where = joint_point(records, rest_solved, parent, entry["joint"])
            if inherits_rotation:
                where = rotate_point((rest_where[0] + shift[0], rest_where[1] + shift[1]),
                                     p_pos, p_extra)
                extra = p_extra
            else:
                axes = constraint.get("inherit_translation") or []
                where = (rest_where[0] + (shift[0] if "x" in axes else 0.0),
                         rest_where[1] + (shift[1] if "y" in axes else 0.0))
                extra = 0.0
                if constraint.get("pin") == "character ground plane":
                    where = (where[0], planes[root_layer(layer)])
        frames[layer] = (rest_angle + extra, where, extra)
        return frames[layer]

    for layer in attach:
        solve(layer)
    return records, frames, meshes
