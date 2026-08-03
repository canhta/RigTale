#!/usr/bin/env python3
"""Assemble the cast parts into a contact sheet.

This is a posing harness, not a renderer and not an assertion. It exists to show
that the layered parts compose, that the manifest's rig data is sufficient to
place and parent every part without guessing, and that nothing is missing from
the manifest. Visual acceptance belongs to `SPIKE-R002` and the quality rubric,
not here.

No joint offset is written down in this file. Every position comes from
`cast/manifest.json`: a part is placed by putting its own pivot on the named
joint of its parent, then rotating by the recorded `rest_angle`. The only
hardcoded geometry is the contact sheet's own layout.

    python3 fixtures/tools/preview_cast.py [-o path.png]
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from PIL import Image

CAST_DIR = Path(__file__).resolve().parents[1] / "cast"
SUPPORTED_BLEND_MODES = {"normal"}


def load_manifest() -> dict:
    path = CAST_DIR / "manifest.json"
    if not path.exists():
        raise SystemExit("No manifest. Run fixtures/tools/build_cast.py first.")
    return json.loads(path.read_text())


def over(base: Image.Image, img: Image.Image, x: float, y: float) -> None:
    """Alpha-composite `img` onto `base`, clipping anything off the edges."""
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
    base.alpha_composite(img, (x, y))


def rotate_point(p: tuple, origin: tuple, angle_deg: float) -> tuple[float, float]:
    """Rotate `p` about `origin` counter-clockwise on screen, in y-down pixels."""
    t = math.radians(angle_deg)
    dx, dy = p[0] - origin[0], p[1] - origin[1]
    return (origin[0] + dx * math.cos(t) + dy * math.sin(t),
            origin[1] - dx * math.sin(t) + dy * math.cos(t))


class Rig:
    """Evaluates a character's rest pose straight out of the manifest."""

    def __init__(self, doc: dict) -> None:
        self.doc = doc
        self.index = {(p["character"], p["layer"]): p for p in doc["parts"]}
        self.rig = doc["rig"]

    def part(self, character: str, layer: str) -> Image.Image:
        record = self.index[(character, layer)]
        if record["blend_mode"] not in SUPPORTED_BLEND_MODES:
            raise SystemExit(
                f"{character}/{layer} declares blend mode '{record['blend_mode']}', "
                f"which this harness does not implement. Supported: "
                f"{sorted(SUPPORTED_BLEND_MODES)}."
            )
        img = Image.open(CAST_DIR / record["file"]).convert("RGBA")
        opacity = float(record["opacity"])
        if opacity < 1.0:
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
        attach = self.rig[character]["attach"]
        solved: dict[str, tuple[float, tuple[float, float]]] = {}

        def solve(layer: str):
            if layer in solved:
                return solved[layer]
            entry = attach[layer]
            parent = entry["parent"]
            if parent is None:
                solved[layer] = (float(entry["rest_angle"]), (0.0, 0.0))
            else:
                p_angle, p_pivot_char = solve(parent)
                p_record = self.index[(character, parent)]
                joint = p_record["joints"][entry["joint"]]
                where = rotate_point(joint, p_record["pivot"], p_angle)
                solved[layer] = (
                    p_angle + float(entry["rest_angle"]),
                    (p_pivot_char[0] + where[0] - p_record["pivot"][0],
                     p_pivot_char[1] + where[1] - p_record["pivot"][1]),
                )
            return solved[layer]

        for layer in attach:
            solve(layer)
        return solved

    def pose(self, character: str, root: str) -> Image.Image:
        """Render one root and everything parented under it, in z order."""
        solved = self.frames(character)
        placed = []
        for layer, (angle, pivot_char) in solved.items():
            if self.root_of(character, layer) != root or not self.visible(character, layer):
                continue
            record = self.index[(character, layer)]
            img = self.part(character, layer)
            pivot = record["pivot"]
            if angle:
                out = img.rotate(angle, expand=True, resample=Image.BICUBIC)
                centre = ((img.width - 1) / 2, (img.height - 1) / 2)
                moved = rotate_point(pivot, centre, angle)
                anchor = (moved[0] - centre[0] + (out.width - 1) / 2,
                          moved[1] - centre[1] + (out.height - 1) / 2)
            else:
                out, anchor = img, (float(pivot[0]), float(pivot[1]))
            placed.append((record["z"], layer, out,
                           pivot_char[0] - anchor[0], pivot_char[1] - anchor[1]))

        left = min(x for _, _, _, x, _ in placed)
        top = min(y for _, _, _, _, y in placed)
        right = max(x + im.width for _, _, im, x, _ in placed)
        bottom = max(y + im.height for _, _, im, _, y in placed)
        canvas = Image.new("RGBA", (int(math.ceil(right - left)),
                                    int(math.ceil(bottom - top))), (0, 0, 0, 0))
        for _, _, im, x, y in sorted(placed, key=lambda r: (r[0], r[1])):
            over(canvas, im, x - left, y - top)
        return canvas

    def tiles(self, character: str) -> list:
        return [self.pose(character, root) for root in self.rig[character]["roots"]]


def draw_backdrop(rig: Rig, sheet: Image.Image, ground_y: int) -> None:
    """Lay the scene bands onto the sheet in z order, far to near.

    The x positions here are contact-sheet layout. The stacking order and the
    ground line come from the manifest: `z` orders the bands and each band's
    `ground` joint is the point that sits on the ground line.
    """
    bands = sorted((rig.index[("scene", layer)] for layer in rig.rig["scene"]["roots"]),
                   key=lambda r: r["z"])
    for record in bands:
        img = rig.part("scene", record["layer"])
        gx, gy = record["joints"]["ground"]
        if record["layer"] == "grass":
            for x in range(0, sheet.width + img.width, img.width):
                over(sheet, img, x - gx, ground_y - gy)
        elif record["layer"] == "cloud":
            over(sheet, img, 60, 30)
        elif record["layer"] == "tree_large":
            over(sheet, img, sheet.width - img.width - 40, ground_y - gy - 20)
        else:
            over(sheet, img, sheet.width - img.width - 190, ground_y - gy - 10)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--out", default=str(CAST_DIR / "preview.png"))
    args = ap.parse_args()

    rig = Rig(load_manifest())
    tiles = []
    for character in rig.rig:
        if character == "scene":
            continue
        tiles.extend(rig.tiles(character))

    pad = 24
    width = sum(t.width + pad for t in tiles) + pad
    height = max(t.height for t in tiles) + pad * 2 + 90
    sheet = Image.new("RGBA", (width, height), (250, 249, 246, 255))

    baseline = height - 120
    draw_backdrop(rig, sheet, height - 40)

    x = pad
    for tile in tiles:
        over(sheet, tile, x, baseline - tile.height + 60)
        x += tile.width + pad

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    sheet.convert("RGB").save(args.out)
    print(f"{len(tiles)} posed groups -> {args.out}")


if __name__ == "__main__":
    main()
