#!/usr/bin/env python3
"""Build the RigTale reference cast as layered cutout parts.

Sources are CC0 and are NOT vendored. Fetch them into the ignored sandbox first;
see `.sandbox/README.md`. This script reads from there and writes redistributable
output into `fixtures/cast/`.

    python3 fixtures/tools/build_cast.py

Every part is emitted as its own PNG with a recorded pivot, because the fixture
exists to exercise rigging. A flattened character would assert nothing.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[2]
KENNEY = ROOT / ".sandbox/assets/kenney-shape-characters/PNG/Double"
FABRIC = ROOT / ".sandbox/assets/fabric034/Fabric034_1K-JPG_Color.jpg"
OUT = ROOT / "fixtures/cast"

TEXTURE_STRENGTH = 0.16  # felt weave, deliberately subtle
INK = (58, 62, 84, 255)  # shared dark for pupils, mouths, brows


# --------------------------------------------------------------------------
# colour and texture helpers
# --------------------------------------------------------------------------

def _rgba(path: Path) -> Image.Image:
    return Image.open(path).convert("RGBA")


def recolour(src: Image.Image, light: tuple, dark: tuple) -> Image.Image:
    """Re-map a part onto a new two-stop ramp, preserving its original shading.

    Kenney's parts carry a vertical gradient. Flat-filling would throw away the
    form, so luminance is normalised across the opaque pixels and used as the
    ramp position.
    """
    a = np.asarray(src, dtype=np.float32)
    rgb, alpha = a[..., :3], a[..., 3:4]
    lum = rgb @ np.array([0.299, 0.587, 0.114], dtype=np.float32)
    opaque = alpha[..., 0] > 8
    if opaque.any():
        lo, hi = np.percentile(lum[opaque], [2, 98])
    else:
        lo, hi = 0.0, 255.0
    t = np.clip((lum - lo) / max(hi - lo, 1e-5), 0.0, 1.0)[..., None]
    out = np.array(dark, dtype=np.float32)[:3] * (1 - t) + np.array(light, dtype=np.float32)[:3] * t
    return Image.fromarray(np.concatenate([out, alpha], axis=-1).astype(np.uint8), "RGBA")


_fabric_cache: dict[tuple[int, int], np.ndarray] = {}


def _fabric(size: tuple[int, int]) -> np.ndarray:
    """Tileable fabric luminance, centred on zero, cached per size."""
    if size not in _fabric_cache:
        tex = Image.open(FABRIC).convert("L")
        w, h = size
        tile = Image.new("L", size)
        for y in range(0, h, tex.height):
            for x in range(0, w, tex.width):
                tile.paste(tex, (x, y))
        arr = np.asarray(tile, dtype=np.float32) / 255.0
        _fabric_cache[size] = arr - arr.mean()
    return _fabric_cache[size]


def texturise(img: Image.Image, strength: float = TEXTURE_STRENGTH) -> Image.Image:
    """Modulate luminance with the felt weave, leaving alpha untouched."""
    a = np.asarray(img, dtype=np.float32)
    rgb, alpha = a[..., :3], a[..., 3:4]
    weave = _fabric(img.size)[..., None] * (strength * 255.0)
    return Image.fromarray(
        np.concatenate([np.clip(rgb + weave, 0, 255), alpha], axis=-1).astype(np.uint8), "RGBA"
    )


def vertical_ramp(size: tuple[int, int], light: tuple, dark: tuple) -> Image.Image:
    """Solid vertical gradient, used as fill for generated shapes."""
    w, h = size
    t = np.linspace(1.0, 0.0, h, dtype=np.float32)[:, None, None]
    rgb = np.array(light, np.float32)[:3] * t + np.array(dark, np.float32)[:3] * (1 - t)
    rgb = np.repeat(rgb, w, axis=1)
    a = np.full((h, w, 1), 255, np.float32)
    return Image.fromarray(np.concatenate([rgb, a], -1).astype(np.uint8), "RGBA")


def shaped(mask: Image.Image, light: tuple, dark: tuple, texture: bool = True) -> Image.Image:
    """Fill a mask with a gradient, then optionally texturise."""
    img = vertical_ramp(mask.size, light, dark)
    img.putalpha(mask)
    return texturise(img) if texture else img


def soft_shadow(size: tuple[int, int], blur: float = 6.0, alpha: int = 46) -> Image.Image:
    """The very small soft blur that makes a part read as cut paper."""
    w, h = size
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).ellipse((0, 0, w - 1, h - 1), fill=alpha)
    m = m.filter(ImageFilter.GaussianBlur(blur))
    img = Image.new("RGBA", (w, h), (40, 44, 66, 0))
    img.putalpha(m)
    return img


def trimmed(img: Image.Image) -> tuple[Image.Image, tuple[int, int]]:
    """Crop to the alpha bounding box, returning the offset that was removed."""
    box = img.getbbox()
    if box is None:
        return img, (0, 0)
    return img.crop(box), (box[0], box[1])


# --------------------------------------------------------------------------
# generated shapes
# --------------------------------------------------------------------------

def limb(length: int, thickness: int, light: tuple, dark: tuple) -> Image.Image:
    """A rounded capsule. Pivot is the top centre, so it rotates from the joint."""
    m = Image.new("L", (thickness, length), 0)
    ImageDraw.Draw(m).rounded_rectangle(
        (0, 0, thickness - 1, length - 1), radius=thickness // 2, fill=255
    )
    return shaped(m, light, dark)


def eye(radius: int, look: tuple[float, float] = (0.0, 0.0)) -> Image.Image:
    """White sclera, dark pupil, offset highlight. `look` shifts the pupil."""
    d = radius * 2
    img = Image.new("RGBA", (d, d), (0, 0, 0, 0))
    dr = ImageDraw.Draw(img)
    dr.ellipse((0, 0, d - 1, d - 1), fill=(255, 255, 255, 255))
    pr = int(radius * 0.52)
    cx = radius + look[0] * (radius - pr)
    cy = radius + look[1] * (radius - pr)
    dr.ellipse((cx - pr, cy - pr, cx + pr, cy + pr), fill=INK)
    hr = max(2, int(radius * 0.18))
    dr.ellipse(
        (cx - pr * 0.45 - hr, cy - pr * 0.5 - hr, cx - pr * 0.45 + hr, cy - pr * 0.5 + hr),
        fill=(255, 255, 255, 235),
    )
    return img


MOUTH_STATES = {
    # name: (width factor, height factor, kind)
    "neutral": (0.62, 0.10, "line"),
    "smile": (0.80, 0.34, "arc"),
    "open": (0.58, 0.62, "oval"),
    "wide": (0.86, 0.46, "oval"),
    "viseme_ai": (0.66, 0.54, "oval"),
    "viseme_e": (0.74, 0.28, "oval"),
    "viseme_o": (0.44, 0.56, "oval"),
    "viseme_u": (0.34, 0.42, "oval"),
    "viseme_mbp": (0.62, 0.08, "line"),
    "viseme_fv": (0.60, 0.20, "arc"),
    "viseme_l": (0.56, 0.44, "oval"),
    "viseme_ws": (0.48, 0.30, "oval"),
}


def mouth(base: int, state: str) -> Image.Image:
    wf, hf, kind = MOUTH_STATES[state]
    w, h = max(6, int(base * wf)), max(4, int(base * hf))
    img = Image.new("RGBA", (w, h + 4), (0, 0, 0, 0))
    dr = ImageDraw.Draw(img)
    if kind == "line":
        dr.rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=INK)
    elif kind == "arc":
        dr.pieslice((0, -h, w - 1, h - 1), start=0, end=180, fill=INK)
    else:
        dr.ellipse((0, 0, w - 1, h - 1), fill=INK)
    return img


def hair_tuft(w: int, h: int, light: tuple, dark: tuple) -> Image.Image:
    """Symmetric three-lobe tuft. An off-centre version reads as a beret."""
    m = Image.new("L", (w, h), 0)
    dr = ImageDraw.Draw(m)
    dr.ellipse((0, h * 0.28, w * 0.46, h), fill=255)
    dr.ellipse((w * 0.54, h * 0.28, w, h), fill=255)
    dr.ellipse((w * 0.22, 0, w * 0.78, h * 0.86), fill=255)
    return shaped(m, light, dark)


def hair_curls(w: int, h: int, light: tuple, dark: tuple) -> Image.Image:
    m = Image.new("L", (w, h), 0)
    dr = ImageDraw.Draw(m)
    for i in range(5):
        r = h * (0.42 if i % 2 else 0.52)
        cx = w * (0.12 + i * 0.19)
        dr.ellipse((cx - r, h * 0.5 - r, cx + r, h * 0.5 + r), fill=255)
    return shaped(m, light, dark)


def pigtail(r: int, light: tuple, dark: tuple) -> Image.Image:
    m = Image.new("L", (r * 2, r * 2), 0)
    ImageDraw.Draw(m).ellipse((0, 0, r * 2 - 1, r * 2 - 1), fill=255)
    return shaped(m, light, dark)


def shirt(w: int, h: int, light: tuple, dark: tuple, pattern: str) -> Image.Image:
    """A clothing band across the body, with an original pattern."""
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=int(h * 0.34), fill=255)
    img = shaped(m, light, dark)
    dr = ImageDraw.Draw(img)
    ink = (255, 255, 255, 64)
    if pattern == "stripes":
        for y in range(0, h, max(6, h // 6)):
            dr.rectangle((0, y, w, y + max(2, h // 18)), fill=ink)
    elif pattern == "checks":
        step = max(8, w // 8)
        for y in range(0, h, step):
            for x in range((y // step % 2) * step, w, step * 2):
                dr.rectangle((x, y, x + step - 1, y + step - 1), fill=ink)
    elif pattern == "dots":
        step = max(10, w // 6)
        for y in range(step // 2, h, step):
            for x in range(step // 2 + (y // step % 2) * step // 2, w, step):
                dr.ellipse((x - 3, y - 3, x + 3, y + 3), fill=ink)
    img.putalpha(m)
    return img


# --------------------------------------------------------------------------
# cast definition
# --------------------------------------------------------------------------

@dataclass
class Palette:
    light: tuple
    dark: tuple
    hair_light: tuple
    hair_dark: tuple
    cloth_light: tuple
    cloth_dark: tuple


@dataclass
class Biped:
    name: str
    body_shape: str          # Kenney base: squircle or circle
    palette: Palette
    hair: str                # tuft | curls | pigtails
    pattern: str             # stripes | checks | dots
    role: str


PALETTES = {
    "coral": Palette((255, 173, 149), (226, 106, 92), (92, 66, 74), (58, 42, 52),
                     (255, 246, 232), (238, 214, 186)),
    "teal": Palette((150, 223, 214), (58, 158, 158), (74, 62, 96), (44, 36, 62),
                    (255, 236, 210), (240, 199, 160)),
    "mustard": Palette((255, 214, 130), (232, 168, 60), (120, 78, 54), (82, 50, 34),
                       (214, 235, 255), (166, 200, 240)),
}

CAST = [
    Biped("pim", "squircle", PALETTES["coral"], "tuft", "stripes", "leader"),
    Biped("bo", "circle", PALETTES["teal"], "curls", "checks", "follower"),
    Biped("nu", "squircle", PALETTES["mustard"], "pigtails", "dots", "observer"),
]


@dataclass
class Manifest:
    parts: list = field(default_factory=list)

    def add(self, character: str, layer: str, z: int, img: Image.Image,
            pivot: tuple[int, int], note: str = "") -> None:
        rel = f"{character}/{layer}.png"
        path = OUT / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        img.save(path)
        self.parts.append({
            "character": character,
            "layer": layer,
            "file": rel,
            "z": z,
            "size": list(img.size),
            "pivot": list(pivot),
            "note": note,
        })


def build_biped(c: Biped, m: Manifest) -> None:
    p = c.palette
    base = _rgba(KENNEY / f"blue_body_{c.body_shape}.png")
    body = texturise(recolour(base, p.light, p.dark))
    bw, bh = body.size

    m.add(c.name, "shadow", 0, soft_shadow((int(bw * 0.86), int(bh * 0.22))),
          (int(bw * 0.43), int(bh * 0.11)), "ground contact, follows body x only")

    # Limbs sit behind the body so the joint is hidden, but they must still
    # clear the silhouette — a limb shorter than the body radius is invisible
    # in every pose and makes its pivot untestable.
    arm_len, arm_th = int(bh * 0.62), int(bw * 0.13)
    leg_len, leg_th = int(bh * 0.44), int(bw * 0.17)
    for side, z in (("left", 1), ("right", 2)):
        a = limb(arm_len, arm_th, p.light, p.dark)
        m.add(c.name, f"arm_{side}", z, a, (arm_th // 2, arm_th // 2), "pivot at shoulder")
        l = limb(leg_len, leg_th, p.light, p.dark)
        m.add(c.name, f"leg_{side}", z, l, (leg_th // 2, leg_th // 2), "pivot at hip")

    m.add(c.name, "body", 10, body, (bw // 2, bh // 2), f"Kenney {c.body_shape} base, recoloured")

    band = shirt(int(bw * 0.92), int(bh * 0.34), p.cloth_light, p.cloth_dark, c.pattern)
    m.add(c.name, "clothing", 11, band, (band.width // 2, 0), f"{c.pattern}, original pattern")

    # Kenney's hands are drawn for a larger figure. At cast scale the splayed
    # open hand reads as a frond, so every hand is scaled down to sit against
    # the arm rather than compete with the body.
    HAND_SCALE = 0.55
    hands = {}
    for label, src in (("open", "blue_hand_open"), ("closed", "blue_hand_closed"),
                       ("point", "blue_hand_point")):
        im = texturise(recolour(_rgba(KENNEY / f"{src}.png"), p.light, p.dark))
        hands[label] = im.resize(
            (max(8, int(im.width * HAND_SCALE)), max(8, int(im.height * HAND_SCALE))),
            Image.LANCZOS,
        )
    for side in ("left", "right"):
        flip = side == "right"
        for label, im in hands.items():
            img = im.transpose(Image.FLIP_LEFT_RIGHT) if flip else im
            m.add(c.name, f"hand_{side}_{label}", 12, img,
                  (img.width // 2, 4), "attaches at arm tip; anchor for props")

    er = max(10, int(bw * 0.13))
    for side, look in (("left", (0.0, 0.0)), ("right", (0.0, 0.0))):
        m.add(c.name, f"eye_{side}", 20, eye(er), (er, er), "sclera, pupil, highlight")
    for side, look in (("left", (-0.6, 0.0)), ("right", (-0.6, 0.0))):
        m.add(c.name, f"eye_{side}_look_left", 20, eye(er, look), (er, er), "gaze target")
    for side, look in (("left", (0.6, 0.0)), ("right", (0.6, 0.0))):
        m.add(c.name, f"eye_{side}_look_right", 20, eye(er, look), (er, er), "gaze target")

    brow = texturise(recolour(_rgba(KENNEY / "facial_part_eyebrow_a.png"),
                              p.hair_light, p.hair_dark))
    for side in ("left", "right"):
        img = brow.transpose(Image.FLIP_LEFT_RIGHT) if side == "right" else brow
        m.add(c.name, f"eyebrow_{side}", 21, img, (img.width // 2, img.height // 2), "")

    mb = int(bw * 0.34)
    for state in MOUTH_STATES:
        img = mouth(mb, state)
        m.add(c.name, f"mouth_{state}", 22, img, (img.width // 2, 0),
              "viseme" if state.startswith("viseme") else "expression")

    hl, hd = p.hair_light, p.hair_dark
    if c.hair == "tuft":
        m.add(c.name, "hair", 30, hair_tuft(int(bw * 0.52), int(bh * 0.30), hl, hd),
              (int(bw * 0.26), int(bh * 0.28)), "")
    elif c.hair == "curls":
        m.add(c.name, "hair", 30, hair_curls(int(bw * 0.86), int(bh * 0.26), hl, hd),
              (int(bw * 0.43), int(bh * 0.24)), "")
    else:
        m.add(c.name, "hair", 30, hair_curls(int(bw * 0.52), int(bh * 0.16), hl, hd),
              (int(bw * 0.26), int(bh * 0.14)), "fringe, narrower so the pigtails read")
        pt = pigtail(int(bw * 0.13), hl, hd)
        for side in ("left", "right"):
            m.add(c.name, f"pigtail_{side}", 29, pt, (pt.width // 2, int(pt.height * 0.18)),
                  "pivot near the skull, secondary motion candidate")


def build_quadruped(m: Manifest) -> None:
    """Mochi. Not in the Kenney pack; composed from the same shape language."""
    p = Palette((236, 222, 208), (196, 174, 158), (120, 96, 84), (86, 66, 58),
                (255, 255, 255), (226, 226, 226))
    name = "mochi"
    bw, bh = 220, 140
    m.add(name, "shadow", 0, soft_shadow((int(bw * 0.9), 34)), (int(bw * 0.45), 17),
          "four-point contact, locomotion critical")

    leg_len, leg_th = 84, 26
    for i, side in enumerate(("fore_left", "fore_right", "hind_left", "hind_right")):
        m.add(name, f"leg_{side}", 1 + (i % 2), limb(leg_len, leg_th, p.light, p.dark),
              (leg_th // 2, leg_th // 2), "pivot at hip or shoulder, ground contact at tip")

    mask = Image.new("L", (bw, bh), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, bw - 1, bh - 1), fill=255)
    m.add(name, "body", 10, shaped(mask, p.light, p.dark), (bw // 2, bh // 2), "")

    tail = limb(70, 20, p.light, p.dark)
    m.add(name, "tail", 9, tail, (10, 10), "pivot at rump, secondary motion")

    hd = 118
    hm = Image.new("L", (hd, hd), 0)
    ImageDraw.Draw(hm).ellipse((0, 0, hd - 1, hd - 1), fill=255)
    m.add(name, "head", 20, shaped(hm, p.light, p.dark), (hd // 2, hd // 2), "pivot at neck")

    em = Image.new("L", (52, 66), 0)
    ImageDraw.Draw(em).ellipse((0, 0, 51, 65), fill=255)
    ear = shaped(em, p.hair_light, p.hair_dark)
    for side in ("left", "right"):
        m.add(name, f"ear_{side}", 19, ear, (26, 8), "pivot at skull, secondary motion")

    for side in ("left", "right"):
        m.add(name, f"eye_{side}", 22, eye(17), (17, 17), "")
    nm = Image.new("RGBA", (34, 26), (0, 0, 0, 0))
    ImageDraw.Draw(nm).ellipse((0, 0, 33, 25), fill=INK)
    m.add(name, "nose", 23, nm, (17, 13), "")
    for state in ("neutral", "open", "smile"):
        img = mouth(46, state)
        m.add(name, f"mouth_{state}", 23, img, (img.width // 2, 0), "expression")


def build_vehicle(m: Manifest) -> None:
    """A pull-along cart. Wheels are separate so cycles can be asserted."""
    p = Palette((188, 214, 240), (120, 158, 204), (70, 82, 104), (48, 58, 76),
                (255, 255, 255), (226, 226, 226))
    name = "cart"
    bw, bh = 260, 120
    m.add(name, "shadow", 0, soft_shadow((int(bw * 0.92), 30)), (int(bw * 0.46), 15), "")

    mask = Image.new("L", (bw, bh), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, bw - 1, bh - 1), radius=34, fill=255)
    m.add(name, "body", 10, shaped(mask, p.light, p.dark), (bw // 2, bh // 2),
          "prop and character attachment surface")

    wd = 76
    wm = Image.new("L", (wd, wd), 0)
    ImageDraw.Draw(wm).ellipse((0, 0, wd - 1, wd - 1), fill=255)
    wheel = shaped(wm, p.hair_light, p.hair_dark)
    hub = ImageDraw.Draw(wheel)
    hub.ellipse((wd * 0.36, wd * 0.36, wd * 0.64, wd * 0.64), fill=(255, 255, 255, 210))
    hub.rectangle((wd * 0.47, wd * 0.10, wd * 0.53, wd * 0.90), fill=(255, 255, 255, 90))
    for side in ("front", "rear"):
        m.add(name, f"wheel_{side}", 12, wheel, (wd // 2, wd // 2),
              "pivot at axle centre, rotation cycle must match ground travel")

    handle = limb(120, 22, p.light, p.dark)
    m.add(name, "handle", 9, handle, (11, 11), "pivot at hitch")


def build_props(m: Manifest) -> None:
    name = "props"
    bm = Image.new("L", (96, 96), 0)
    ImageDraw.Draw(bm).ellipse((0, 0, 95, 95), fill=255)
    ball = shaped(bm, (255, 196, 196), (222, 116, 128))
    d = ImageDraw.Draw(ball)
    d.arc((8, 8, 87, 87), start=200, end=340, fill=(255, 255, 255, 150), width=6)
    ball.putalpha(bm)
    m.add(name, "ball", 10, ball, (48, 48), "handoff and attachment prop")

    dm = Image.new("L", (120, 84), 0)
    ImageDraw.Draw(dm).rounded_rectangle((0, 0, 119, 83), radius=18, fill=255)
    drum = shaped(dm, (250, 226, 190), (214, 172, 122))
    dd = ImageDraw.Draw(drum)
    for x in range(12, 110, 24):
        dd.line((x, 10, x + 12, 74), fill=(255, 255, 255, 90), width=4)
    drum.putalpha(dm)
    m.add(name, "drum", 10, drum, (60, 42), "beat-synchronised prop")

    m.add(name, "shadow_small", 0, soft_shadow((72, 22)), (36, 11), "shared prop shadow")


def build_scene(m: Manifest) -> None:
    """Environment layers, recoloured from the Kenney tile set for parallax."""
    name = "scene"
    for src, layer, note in (
        ("tile_background_tree_large", "tree_large", "far parallax band"),
        ("tile_background_tree_small", "tree_small", "mid parallax band"),
        ("tile_cloud", "cloud", "far parallax band"),
        ("tile_background_grass", "grass", "near parallax band"),
    ):
        img = texturise(recolour(_rgba(KENNEY / f"{src}.png"),
                                 (214, 234, 214), (140, 182, 152)), 0.10)
        m.add(name, layer, 0, img, (img.width // 2, img.height), note)


def main() -> None:
    if not KENNEY.exists():
        raise SystemExit(
            f"Missing CC0 sources at {KENNEY}.\n"
            "Fetch them into the sandbox first; see .sandbox/README.md."
        )
    OUT.mkdir(parents=True, exist_ok=True)
    m = Manifest()
    for c in CAST:
        build_biped(c, m)
    build_quadruped(m)
    build_vehicle(m)
    build_props(m)
    build_scene(m)

    doc = {
        "fixture": "rigtale-reference-cast",
        "version": "0.1.0-draft",
        "status": "draft, not approved; RGT-S003 is active and RGT-D-fixture has not been recorded",
        "generator": "fixtures/tools/build_cast.py",
        "sources": [
            {"name": "Kenney Shape Characters", "licence": "CC0 1.0",
             "url": "https://kenney.nl/assets/shape-characters",
             "used_for": "body, hand, eyebrow and environment tile bases"},
            {"name": "ambientCG Fabric034", "licence": "CC0 1.0",
             "url": "https://ambientcg.com/view?id=Fabric034",
             "used_for": "felt weave overlay"},
        ],
        "originality": (
            "Characters are original compositions: new palette, new hair, new clothing "
            "patterns, generated limbs, eyes and visemes. No visual identity is copied "
            "from any reference channel, and no reference video supplied any asset."
        ),
        "coordinate_note": (
            "Pivot is in pixels from each part's own top-left. Placement in character "
            "space is the rig's responsibility and is deliberately not baked in."
        ),
        "parts": sorted(m.parts, key=lambda r: (r["character"], r["z"], r["layer"])),
    }
    (OUT / "manifest.json").write_text(json.dumps(doc, indent=2) + "\n")

    chars = sorted({r["character"] for r in m.parts})
    print(f"{len(m.parts)} parts across {len(chars)} groups: {', '.join(chars)}")
    print(f"manifest: {OUT / 'manifest.json'}")


if __name__ == "__main__":
    main()
