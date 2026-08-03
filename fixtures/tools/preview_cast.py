#!/usr/bin/env python3
"""Assemble the cast parts into a contact sheet.

This is a posing harness, not a renderer and not an assertion. It exists to show
that the layered parts compose, that pivots are usable, and that nothing is
missing from the manifest. Visual acceptance belongs to `SPIKE-R002` and the
quality rubric, not here.

    python3 fixtures/tools/preview_cast.py [-o path.png]
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from PIL import Image

CAST_DIR = Path(__file__).resolve().parents[1] / "cast"
BIPEDS = ("pim", "bo", "nu")


def load_manifest() -> dict:
    path = CAST_DIR / "manifest.json"
    if not path.exists():
        raise SystemExit("No manifest. Run fixtures/tools/build_cast.py first.")
    doc = json.loads(path.read_text())
    return {(p["character"], p["layer"]): p for p in doc["parts"]}


class Rig:
    def __init__(self, index: dict) -> None:
        self.index = index

    def has(self, character: str, layer: str) -> bool:
        return (character, layer) in self.index

    def part(self, character: str, layer: str) -> Image.Image:
        return Image.open(CAST_DIR / self.index[(character, layer)]["file"]).convert("RGBA")

    def limb(self, canvas: Image.Image, character: str, layer: str,
             joint: tuple[int, int], angle: float) -> tuple[int, int]:
        """Draw a limb rotated about its pivot; return the far tip."""
        img = self.part(character, layer)
        length = img.height
        rotated = img.rotate(angle, expand=True, resample=Image.BICUBIC)
        canvas.alpha_composite(rotated, (joint[0] - rotated.width // 2, joint[1]))
        a = math.radians(angle)
        return joint[0] + int(math.sin(a) * length * 0.92), joint[1] + int(math.cos(a) * length * 0.92)


def pose_biped(rig: Rig, name: str) -> Image.Image:
    body = rig.part(name, "body")
    bw, bh = body.size
    canvas = Image.new("RGBA", (int(bw * 2.2), int(bh * 2.4)), (0, 0, 0, 0))
    cx, cy = canvas.width // 2, int(canvas.height * 0.56)

    shadow = rig.part(name, "shadow")
    canvas.alpha_composite(shadow, (cx - shadow.width // 2, cy + bh // 2 - 6))

    for side, dx, angle in (("left", -0.26, 16), ("right", 0.26, -16)):
        rig.limb(canvas, name, f"leg_{side}", (int(cx + bw * dx), cy + int(bh * 0.30)), angle)

    tips = {}
    for side, dx, angle in (("left", -0.40, 34), ("right", 0.40, -34)):
        tips[side] = rig.limb(canvas, name, f"arm_{side}",
                              (int(cx + bw * dx), cy - int(bh * 0.16)), angle)

    canvas.alpha_composite(body, (cx - bw // 2, cy - bh // 2))

    cloth = rig.part(name, "clothing")
    canvas.alpha_composite(cloth, (cx - cloth.width // 2, cy + int(bh * 0.06)))

    for side in ("left", "right"):
        hand = rig.part(name, f"hand_{side}_open")
        canvas.alpha_composite(hand, (tips[side][0] - hand.width // 2, tips[side][1] - 6))

    radius = rig.part(name, "eye_left").width // 2
    for side, dx in (("left", -0.20), ("right", 0.20)):
        eye = rig.part(name, f"eye_{side}")
        ex, ey = int(cx + bw * dx) - radius, cy - int(bh * 0.20) - radius
        canvas.alpha_composite(eye, (ex, ey))
        brow = rig.part(name, f"eyebrow_{side}")
        canvas.alpha_composite(brow, (ex + radius - brow.width // 2, ey - brow.height - 6))

    mouth = rig.part(name, "mouth_smile")
    canvas.alpha_composite(mouth, (cx - mouth.width // 2, cy + int(bh * 0.02)))

    if rig.has(name, "pigtail_left"):
        for side, dx in (("left", -0.52), ("right", 0.52)):
            pt = rig.part(name, f"pigtail_{side}")
            canvas.alpha_composite(pt, (int(cx + bw * dx) - pt.width // 2, cy - int(bh * 0.42)))

    hair = rig.part(name, "hair")
    canvas.alpha_composite(hair, (cx - hair.width // 2, cy - int(bh * 0.50) - hair.height // 3))
    return canvas


def pose_quadruped(rig: Rig) -> Image.Image:
    name = "mochi"
    body = rig.part(name, "body")
    bw, bh = body.size
    canvas = Image.new("RGBA", (int(bw * 1.7), int(bh * 2.6)), (0, 0, 0, 0))
    cx, cy = canvas.width // 2, int(canvas.height * 0.60)

    shadow = rig.part(name, "shadow")
    canvas.alpha_composite(shadow, (cx - shadow.width // 2, cy + bh // 2 - 4))

    for side, dx, angle in (("fore_left", -0.30, 10), ("fore_right", -0.36, -8),
                            ("hind_left", 0.30, -10), ("hind_right", 0.36, 8)):
        rig.limb(canvas, name, f"leg_{side}", (int(cx + bw * dx), cy + int(bh * 0.26)), angle)

    rig.limb(canvas, name, "tail", (cx + int(bw * 0.44), cy - int(bh * 0.18)), -50)
    canvas.alpha_composite(body, (cx - bw // 2, cy - bh // 2))

    head = rig.part(name, "head")
    hx, hy = cx - int(bw * 0.42) - head.width // 2, cy - int(bh * 0.55)
    for side, dx in (("left", -0.22), ("right", 0.18)):
        ear = rig.part(name, f"ear_{side}")
        canvas.alpha_composite(ear, (hx + head.width // 2 + int(head.width * dx) - ear.width // 2,
                                     hy - int(ear.height * 0.42)))
    canvas.alpha_composite(head, (hx, hy))
    for side, dx in (("left", -0.20), ("right", 0.16)):
        eye = rig.part(name, f"eye_{side}")
        canvas.alpha_composite(eye, (hx + head.width // 2 + int(head.width * dx) - eye.width // 2,
                                     hy + int(head.height * 0.30)))
    nose = rig.part(name, "nose")
    canvas.alpha_composite(nose, (hx + head.width // 2 - nose.width // 2 - 6,
                                  hy + int(head.height * 0.56)))
    mouth = rig.part(name, "mouth_smile")
    canvas.alpha_composite(mouth, (hx + head.width // 2 - mouth.width // 2 - 6,
                                   hy + int(head.height * 0.70)))
    return canvas


def pose_vehicle(rig: Rig) -> Image.Image:
    name = "cart"
    body = rig.part(name, "body")
    bw, bh = body.size
    canvas = Image.new("RGBA", (int(bw * 1.6), int(bh * 2.6)), (0, 0, 0, 0))
    cx, cy = canvas.width // 2, int(canvas.height * 0.52)

    shadow = rig.part(name, "shadow")
    canvas.alpha_composite(shadow, (cx - shadow.width // 2, cy + bh // 2 + 10))
    rig.limb(canvas, name, "handle", (cx - int(bw * 0.46), cy - int(bh * 0.20)), 118)
    canvas.alpha_composite(body, (cx - bw // 2, cy - bh // 2))
    wheel = rig.part(name, "wheel_front")
    for dx in (-0.30, 0.30):
        canvas.alpha_composite(wheel, (int(cx + bw * dx) - wheel.width // 2, cy + int(bh * 0.34)))
    return canvas


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--out", default=str(CAST_DIR / "preview.png"))
    args = ap.parse_args()

    rig = Rig(load_manifest())
    tiles = [pose_biped(rig, n) for n in BIPEDS]
    tiles += [pose_quadruped(rig), pose_vehicle(rig)]
    tiles += [rig.part("props", "ball"), rig.part("props", "drum")]

    pad = 24
    width = sum(t.width + pad for t in tiles) + pad
    height = max(t.height for t in tiles) + pad * 2 + 90
    sheet = Image.new("RGBA", (width, height), (250, 249, 246, 255))

    grass = rig.part("scene", "grass")
    for x in range(0, width, grass.width):
        sheet.alpha_composite(grass, (x, height - grass.height - 10))
    tree = rig.part("scene", "tree_large")
    sheet.alpha_composite(tree, (width - tree.width - 40, height - tree.height - 30))
    cloud = rig.part("scene", "cloud")
    sheet.alpha_composite(cloud, (60, 30))

    x, baseline = pad, height - 120
    for tile in tiles:
        sheet.alpha_composite(tile, (x, baseline - tile.height + 60))
        x += tile.width + pad

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    sheet.convert("RGB").save(args.out)
    print(f"{len(tiles)} posed groups -> {args.out}")


if __name__ == "__main__":
    main()
