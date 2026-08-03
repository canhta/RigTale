#!/usr/bin/env python3
"""Assemble the cast parts into contact sheets, at rest and under a named pose.

This is a posing and skinning harness, not a renderer and not an assertion. It
exists to show that the layered parts compose, that the manifest's rig data is
sufficient to place, parent, blend and deform every part without guessing, and
that nothing is missing from the manifest. Visual acceptance belongs to
`SPIKE-R002` and the quality rubric, not here.

No joint offset, weight or blend formula is written down in this file. Every
position comes from `cast/manifest.json`: a part is placed by putting its own
pivot on the named joint of its parent, then rotating by the recorded
`rest_angle`; a meshed part is skinned from its own weights and rasterised
triangle by triangle through its uv; a group stands on its own declared ground
plane. The only hardcoded geometry is the contact sheet's own layout.

    python3 fixtures/tools/preview_cast.py [-o rest.png] [--pose-out posed.png]
    python3 fixtures/tools/preview_cast.py --all      # refuses the out-of-profile part
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw

sys.dont_write_bytecode = True  # keep the fixture tree free of build litter
sys.path.insert(0, str(Path(__file__).resolve().parent))
import rig as rig_eval  # noqa: E402  the attachment rule, shared with the generator

CAST_DIR = Path(__file__).resolve().parents[1] / "cast"

# What this harness can actually composite. The manifest declares the profile it
# expects a consumer to support; these are the modes implemented against it, by
# the W3C Compositing-1 separable formulas the manifest names. A mode the
# manifest declares and this set lacks is a harness gap and stops the run — the
# one thing that must never happen is quietly drawing it as `normal`.
IMPLEMENTED_BLEND_MODES = {
    "normal": lambda cb, cs: cs,
    "multiply": lambda cb, cs: cb * cs,
    "screen": lambda cb, cs: cb + cs - cb * cs,
}


def load_manifest() -> dict:
    path = CAST_DIR / "manifest.json"
    if not path.exists():
        raise SystemExit("No manifest. Run fixtures/tools/build_cast.py first.")
    return json.loads(path.read_text())


def over(base: Image.Image, img: Image.Image, x: float, y: float,
         mode: str = "normal") -> None:
    """Blend `img` onto `base` in place, clipping anything off the edges.

    Source-over with a separable blend function, on straight alpha in the sRGB
    encoding the manifest declares. Opacity is already in the source alpha by the
    time a part reaches here, which is the order `blend_profile.composite_order`
    requires: alpha times opacity first, blend second.
    """
    x, y = int(round(x)), int(round(y))
    sx, sy = max(0, -x), max(0, -y)
    if sx >= img.width or sy >= img.height:
        return
    if sx or sy:
        img = img.crop((sx, sy, img.width, img.height))
        x += sx
        y += sy
    w = min(img.width, base.width - x)
    h = min(img.height, base.height - y)
    if w <= 0 or h <= 0:
        return
    if (w, h) != img.size:
        img = img.crop((0, 0, w, h))

    region = base.crop((x, y, x + w, y + h))
    src = np.asarray(img, dtype=np.float64) / 255.0
    dst = np.asarray(region, dtype=np.float64) / 255.0
    cs, a_s = src[..., :3], src[..., 3:4]
    cb, ab = dst[..., :3], dst[..., 3:4]
    blended = IMPLEMENTED_BLEND_MODES[mode](cb, cs)
    ar = a_s + ab * (1.0 - a_s)
    num = (1.0 - ab) * a_s * cs + ab * a_s * blended + (1.0 - a_s) * ab * cb
    cr = np.divide(num, ar, out=np.zeros_like(num), where=ar > 0.0)
    out = np.concatenate([cr, ar], axis=-1)
    base.paste(Image.fromarray(np.rint(out * 255.0).astype(np.uint8), "RGBA"), (x, y))


def draw_mesh(canvas: Image.Image, img: Image.Image, mesh: dict, posed: list,
              left: float, top: float, mode: str) -> None:
    """Rasterise a deformed part: one affine warp per triangle, uv to posed.

    This is what makes the harness a skinning evaluator rather than a sprite
    placer. Each triangle's uv corners give the source pixels, its skinned
    vertices give the destination, and the affine between them carries the
    texture. Coarse meshes make that legible: a bend is visibly a fan of
    triangles, not a mystery.
    """
    size = img.size
    for tri in mesh["triangles"]:
        src = [(mesh["uv"][i][0] * size[0], mesh["uv"][i][1] * size[1]) for i in tri]
        dst = [(posed[i][0] - left, posed[i][1] - top) for i in tri]
        x0 = max(0, int(math.floor(min(p[0] for p in dst))) - 1)
        y0 = max(0, int(math.floor(min(p[1] for p in dst))) - 1)
        x1 = min(canvas.width, int(math.ceil(max(p[0] for p in dst))) + 1)
        y1 = min(canvas.height, int(math.ceil(max(p[1] for p in dst))) + 1)
        if x1 <= x0 or y1 <= y0:
            continue
        # Solve the affine that maps patch coordinates back to source pixels,
        # which is the direction PIL's AFFINE transform wants.
        a = np.array([[p[0] - x0, p[1] - y0, 1.0] for p in dst], dtype=np.float64)
        if abs(np.linalg.det(a)) < 1e-9:
            continue
        cx = np.linalg.solve(a, np.array([p[0] for p in src], dtype=np.float64))
        cy = np.linalg.solve(a, np.array([p[1] for p in src], dtype=np.float64))
        patch = img.transform((x1 - x0, y1 - y0), Image.AFFINE,
                              (cx[0], cx[1], cx[2], cy[0], cy[1], cy[2]),
                              resample=Image.BILINEAR)
        mask = Image.new("L", patch.size, 0)
        ImageDraw.Draw(mask).polygon([(p[0] - x0, p[1] - y0) for p in dst],
                                     fill=255, outline=255)
        patch.putalpha(ImageChops.multiply(patch.getchannel("A"), mask))
        over(canvas, patch, x0, y0, mode)


rotate_point = rig_eval.rotate_point


class Rig:
    """Evaluates a character's rest pose straight out of the manifest."""

    def __init__(self, doc: dict, demand_all: bool = False) -> None:
        self.doc = doc
        self.index = {(p["character"], p["layer"]): p for p in doc["parts"]}
        self.rig = doc["rig"]
        self.profile = set(doc["blend_profile"]["supported"])
        self.demand_all = demand_all
        self.excluded: list[str] = []

    def honours(self, character: str, layer: str) -> bool:
        """Decide whether this harness may draw a part at all.

        Three outcomes, and none of them is drawing the part as `normal`. In
        profile and implemented: draw it. In profile and not implemented: the
        harness is broken and stops. Outside the profile: refuse it by name, and
        say so — the contact sheet is a profile-honouring consumer, so it leaves
        the part out rather than pretending it composited it.
        """
        mode = self.index[(character, layer)]["blend_mode"]
        if mode in self.profile:
            if mode not in IMPLEMENTED_BLEND_MODES:
                raise SystemExit(
                    f"{character}/{layer} declares '{mode}', which the manifest's "
                    f"blend profile supports and this harness has not implemented. "
                    "Implement it; do not substitute normal."
                )
            return True
        if self.demand_all:
            raise SystemExit(
                f"{character}/{layer} declares blend mode '{mode}', which is outside "
                f"blend_profile.supported {sorted(self.profile)}. This harness "
                "refuses it rather than substituting normal."
            )
        self.excluded.append(f"{character}/{layer} ({mode})")
        return False

    def part(self, character: str, layer: str) -> Image.Image:
        record = self.index[(character, layer)]
        img = Image.open(CAST_DIR / record["file"]).convert("RGBA")
        opacity = float(record["opacity"])
        if opacity < 1.0:
            # Opacity multiplies alpha before the blend, per composite_order.
            alpha = img.getchannel("A").point(lambda v: int(round(v * opacity)))
            img.putalpha(alpha)
        return img

    def root_of(self, character: str, layer: str) -> str:
        attach = self.rig[character]["attach"]
        while attach[layer]["parent"] is not None:
            layer = attach[layer]["parent"]
        return layer

    def visible(self, character: str, layer: str) -> bool:
        """A slot holds mutually exclusive alternates; only its default is posed."""
        for slot in self.rig[character]["slots"].values():
            if layer in slot["members"]:
                return layer == slot["default"]
        return True

    def frames(self, character: str) -> dict:
        """Map every layer to (cumulative angle, its pivot in character space)."""
        return rig_eval.solve_frames(self.rig[character]["attach"],
                                     self.records(character))

    def records(self, character: str) -> dict:
        return rig_eval.records_of(self.doc, character)

    def ground_of(self, character: str, root: str, solved: dict) -> float | None:
        """Character-space y of the floor plane this root stands on."""
        for entry in self.rig[character].get("ground", []):
            if entry["part"] == root:
                return rig_eval.joint_point(self.records(character), solved,
                                            entry["part"], entry["joint"])[1]
        return None

    def skinned(self, character: str, angles: dict) -> tuple:
        """Solve one pose: bone transforms, deformed meshes, and rigid frames.

        A meshed part is drawn from its skinned vertices. A rigid part is placed
        the way the rest pose places it, except that its anchor comes from the
        parent's *deformed* mesh when the parent has one, and it takes the bone
        angles blended at that anchor. That is the rule the manifest states, and
        it is what carries a hand on a bending arm and a contact on a bending leg.
        """
        records = self.records(character)
        rest_solved = self.frames(character)
        transforms = rig_eval.bone_transforms(self.doc, character, angles,
                                              records, rest_solved)
        meshes: dict[str, tuple] = {}

        def mesh_of(layer: str):
            record = records[layer]
            if record["mesh"] is None:
                return None
            if layer not in meshes:
                rest = rig_eval.rest_vertices(records, rest_solved, layer)
                meshes[layer] = (rest, rig_eval.skin(rest, record["mesh"], transforms))
            return meshes[layer]

        attach = self.rig[character]["attach"]
        frames: dict[str, tuple] = {}

        def solve(layer: str):
            if layer in frames:
                return frames[layer]
            entry = attach[layer]
            parent = entry["parent"]
            if parent is None:
                frames[layer] = (rest_solved[layer][0], rest_solved[layer][1], 0.0)
                return frames[layer]
            _, p_pos, p_extra = solve(parent)
            record = records[parent]
            joint = record["joints"][entry["joint"]]
            deformed = mesh_of(parent)
            if deformed is not None:
                where = rig_eval.deform_point(record["mesh"], *deformed, joint)
                weights = rig_eval.point_weights(record["mesh"], joint)
                extra = sum(w * transforms[b][0]
                            for w, b in zip(weights, record["mesh"]["bones"]))
            else:
                rest_where = rig_eval.joint_point(records, rest_solved, parent,
                                                  entry["joint"])
                where = rotate_point(rest_where, p_pos, p_extra)
                extra = p_extra
            frames[layer] = (rest_solved[layer][0] + extra, where, extra)
            return frames[layer]

        for layer in attach:
            solve(layer)
        return records, frames, meshes

    def pose(self, character: str, root: str,
             angles: dict | None = None) -> tuple[Image.Image, float]:
        """Render one root and everything parented under it, in z order.

        Returns the tile and the y inside it that is the character's ground
        plane, so a caller can stand every group on one floor line.
        """
        angles = angles or {}
        records, frames, meshes = self.skinned(character, angles)
        placed = []
        for layer, (angle, anchor_char, _) in frames.items():
            if self.root_of(character, layer) != root or not self.visible(character, layer):
                continue
            if not self.honours(character, layer):
                continue
            record = self.index[(character, layer)]
            img = self.part(character, layer)
            if layer in meshes:
                placed.append((record["z"], layer, "mesh", img,
                               record["blend_mode"], record["mesh"], meshes[layer][1]))
                continue
            pivot = record["pivot"]
            if angle:
                out = img.rotate(angle, expand=True, resample=Image.BICUBIC)
                centre = ((img.width - 1) / 2, (img.height - 1) / 2)
                moved = rotate_point(pivot, centre, angle)
                anchor = (moved[0] - centre[0] + (out.width - 1) / 2,
                          moved[1] - centre[1] + (out.height - 1) / 2)
            else:
                out, anchor = img, (float(pivot[0]), float(pivot[1]))
            placed.append((record["z"], layer, "rigid", out, record["blend_mode"],
                           anchor_char[0] - anchor[0], anchor_char[1] - anchor[1]))

        box = [math.inf, math.inf, -math.inf, -math.inf]
        for item in placed:
            if item[2] == "mesh":
                xs = [p[0] for p in item[6]]
                ys = [p[1] for p in item[6]]
                corners = (min(xs), min(ys), max(xs), max(ys))
            else:
                _, _, _, im, _, x, y = item
                corners = (x, y, x + im.width, y + im.height)
            box = [min(box[0], corners[0]), min(box[1], corners[1]),
                   max(box[2], corners[2]), max(box[3], corners[3])]
        left, top = math.floor(box[0]), math.floor(box[1])
        canvas = Image.new("RGBA", (int(math.ceil(box[2] - left)) + 1,
                                    int(math.ceil(box[3] - top)) + 1), (0, 0, 0, 0))
        for item in sorted(placed, key=lambda r: (r[0], r[1])):
            if item[2] == "mesh":
                _, _, _, img, mode, mesh, posed = item
                draw_mesh(canvas, img, mesh, posed, left, top, mode)
            else:
                _, _, _, im, mode, x, y = item
                over(canvas, im, x - left, y - top, mode)
        plane = self.ground_of(character, root, self.frames(character))
        return canvas, (0.0 if plane is None else plane - top)

    def tiles(self, character: str, angles: dict | None = None) -> list:
        return [self.pose(character, root, angles)
                for root in self.rig[character]["roots"]]


def draw_backdrop(rig: Rig, sheet: Image.Image, ground_y: int) -> None:
    """Lay the scene bands onto the sheet in z order, far to near.

    The x positions here are contact-sheet layout. The stacking order and the
    ground line come from the manifest: `z` orders the bands and each band's
    `ground` joint is the point that sits on the ground line.
    """
    bands = sorted((rig.index[("scene", layer)] for layer in rig.rig["scene"]["roots"]),
                   key=lambda r: r["z"])
    for record in bands:
        layer = record["layer"]
        if not rig.honours("scene", layer):
            continue
        img = rig.part("scene", layer)
        mode = record["blend_mode"]
        gx, gy = record["joints"]["ground"]
        if layer in ("grass", "haze"):
            for x in range(0, sheet.width + img.width, img.width):
                over(sheet, img, x - gx, ground_y - gy, mode)
        elif layer == "cloud":
            over(sheet, img, 60, 30, mode)
        elif layer == "tree_large":
            over(sheet, img, sheet.width - img.width - 40, ground_y - gy - 20, mode)
        else:
            over(sheet, img, sheet.width - img.width - 190, ground_y - gy - 10, mode)


def contact_sheet(rig: Rig, pose: dict) -> Image.Image:
    """One sheet: every group posed by `pose`, standing on one floor line."""
    tiles = []
    for character in rig.rig:
        if character == "scene":
            continue
        tiles.extend(rig.tiles(character, pose.get("angles", {}).get(character)))

    # Every group is placed by its own declared ground plane onto one floor line.
    # Nothing here knows how tall a character is; if two groups did not agree on
    # where their floor is, the sheet would show it.
    pad = 24
    width = sum(t.width + pad for t, _ in tiles) + pad
    above = max(g for _, g in tiles)
    below = max(t.height - g for t, g in tiles)
    floor = int(round(pad + 60 + above))
    height = int(round(floor + below + pad + 40))
    sheet = Image.new("RGBA", (width, height), (250, 249, 246, 255))

    draw_backdrop(rig, sheet, floor)

    x = pad
    for tile, ground in tiles:
        over(sheet, tile, x, floor - ground)
        x += tile.width + pad
    return sheet


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("-o", "--out", default=str(CAST_DIR / "preview.png"))
    ap.add_argument("--pose-out", default=str(CAST_DIR / "preview_pose.png"))
    ap.add_argument("--all", action="store_true",
                    help="demand every part, including any declaring a mode outside "
                         "the manifest's blend profile. The harness then refuses, "
                         "which is the behaviour the profile requires.")
    args = ap.parse_args()

    doc = load_manifest()
    rig = Rig(doc, demand_all=args.all)
    for path, pose in ((args.out, doc["poses"]["rest"]),
                       (args.pose_out, doc["poses"]["reference"])):
        sheet = contact_sheet(rig, pose)
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        sheet.convert("RGB").save(path)
        print(f"pose '{pose['name']}' -> {path}")
    for excluded in sorted(set(rig.excluded)):
        print(f"refused, outside blend_profile.supported: {excluded}. "
              "Not drawn, not substituted with normal. Run with --all to see the "
              "harness fail on it.")


if __name__ == "__main__":
    main()
