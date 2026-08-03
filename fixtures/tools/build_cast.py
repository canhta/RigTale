#!/usr/bin/env python3
"""Build the RigTale reference cast as layered cutout parts.

Sources are CC0 and are NOT vendored. `fixtures/PROVENANCE.json` is the tracked
licence record and names the two archives to fetch; this script verifies each one
by SHA-256 and byte size before it builds, then writes redistributable output
into `fixtures/cast/`.

    python3 fixtures/tools/build_cast.py

Every part is emitted as its own PNG with a recorded pivot, its own joint points,
and a place in the character's rig tree, because the fixture exists to exercise
rigging. A flattened character would assert nothing.
"""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[2]
PROVENANCE = ROOT / "fixtures/PROVENANCE.json"
OUT = ROOT / "fixtures/cast"

# Fetch locations. These are build inputs, not provenance: the licence facts live
# in PROVENANCE.json and nowhere else.
SANDBOX = ROOT / ".sandbox"
KENNEY = SANDBOX / "assets/kenney-shape-characters/PNG/Double"
FABRIC = SANDBOX / "assets/fabric034/Fabric034_1K-JPG_Color.jpg"

TEXTURE_STRENGTH = 0.16  # felt weave, deliberately subtle
INK = (58, 62, 84, 255)  # shared dark for pupils, mouths, brows

# A limb must show at least this many pixels beyond the body silhouette, measured
# from its own joint along its own rest axis. See `check_clearance`.
LIMB_CLEARANCE = 24


# --------------------------------------------------------------------------
# source verification
# --------------------------------------------------------------------------

def verify_sources() -> None:
    """Check every archive named in the tracked provenance record before building.

    Provenance that is never checked decays. Verifying here means a build either
    used exactly the archives the licence record describes, or it did not run.
    """
    if not PROVENANCE.exists():
        raise SystemExit(f"Missing provenance record at {PROVENANCE}.")
    record = json.loads(PROVENANCE.read_text())
    downloads = SANDBOX / "downloads"

    for source in record["sources"]:
        archive = source["archive"]
        found = next(downloads.rglob(archive["file"]), None) if downloads.exists() else None
        if found is None:
            raise SystemExit(
                f"Missing CC0 source archive '{archive['file']}' for {source['name']}.\n"
                f"Download it from {source['download_url']} into {downloads} "
                "and extract it; see fixtures/README.md, Regenerating."
            )
        size = found.stat().st_size
        digest = hashlib.sha256(found.read_bytes()).hexdigest()
        if size != archive["bytes"] or digest != archive["sha256"]:
            raise SystemExit(
                f"{archive['file']} does not match fixtures/PROVENANCE.json.\n"
                f"  expected sha256 {archive['sha256']} ({archive['bytes']} bytes)\n"
                f"  found    sha256 {digest} ({size} bytes)\n"
                "Re-download the recorded archive, or correct the record if the "
                "source genuinely changed."
            )

    for path, what in ((KENNEY, "Kenney part PNGs"), (FABRIC, "the Fabric034 colour map")):
        if not path.exists():
            raise SystemExit(
                f"Missing extracted {what} at {path}.\n"
                "Extract the verified archives; see fixtures/README.md, Regenerating."
            )


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


# --------------------------------------------------------------------------
# rig geometry
# --------------------------------------------------------------------------

def axis(angle_deg: float) -> tuple[float, float]:
    """Unit vector a part points along after `rest_angle` degrees of rotation.

    Every generated limb is drawn pointing straight down from its pivot, and
    rotation is counter-clockwise on screen, so the rest axis of a limb rotated
    by `a` is (sin a, cos a) in image coordinates.
    """
    t = math.radians(angle_deg)
    return math.sin(t), math.cos(t)


def silhouette_exit(body: Image.Image, joint: tuple[float, float], angle_deg: float,
                    limit: float) -> float:
    """Distance from `joint` along a limb's rest axis to the edge of the body."""
    alpha = np.asarray(body)[..., 3]
    h, w = alpha.shape
    ux, uy = axis(angle_deg)
    d = 0.0
    while d <= limit:
        x, y = int(round(joint[0] + ux * d)), int(round(joint[1] + uy * d))
        if not (0 <= x < w and 0 <= y < h) or alpha[y, x] <= 8:
            return d
        d += 1.0
    return limit


def check_clearance(who: str, body: Image.Image, joint: tuple[float, float],
                    angle_deg: float, length: int) -> None:
    """Enforce the rule that makes a limb pivot testable.

    Limbs sit behind the body so the joint is hidden. The joint is inside the
    silhouette, so what matters is not the body radius but the distance from that
    joint to the silhouette edge along the limb's own axis: a limb that does not
    clear that distance by a visible margin is invisible at rest and its pivot
    cannot be observed. Body radius is the wrong yardstick because no joint sits
    at the body centre.
    """
    exit_at = silhouette_exit(body, joint, angle_deg, float(length))
    need = exit_at + LIMB_CLEARANCE
    if length < need:
        raise SystemExit(
            f"{who}: limb length {length} px does not clear the silhouette. "
            f"The joint is {exit_at:.0f} px inside the body along its rest axis, "
            f"so the limb needs at least {need:.0f} px to show {LIMB_CLEARANCE} px."
        )


# --------------------------------------------------------------------------
# generated shapes
# --------------------------------------------------------------------------

def limb(length: int, thickness: int, light: tuple, dark: tuple) -> Image.Image:
    """A rounded capsule drawn pointing down from the centre of its top cap."""
    m = Image.new("L", (thickness, length), 0)
    ImageDraw.Draw(m).rounded_rectangle(
        (0, 0, thickness - 1, length - 1), radius=thickness // 2, fill=255
    )
    return shaped(m, light, dark)


def limb_joints(length: int, thickness: int) -> dict:
    """Far-end joints of a capsule: the far cap centre, and the ground contact."""
    return {
        "tip": [thickness // 2, length - thickness // 2],
        "contact": [thickness // 2, length - 1],
    }


def cloud_body(w: int, h: int, light: tuple, dark: tuple) -> Image.Image:
    """A lobed cloud silhouette, the third shape in the spike's vocabulary.

    Kenney supplies circle and squircle bases. A cloud is not in the pack, so it
    is composed here from the same shape language: a rounded slab with three
    lobes over it.
    """
    m = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(m)
    d.rounded_rectangle((w * 0.06, h * 0.40, w * 0.94, h * 0.98), radius=int(w * 0.26), fill=255)
    for cx, cy, r in ((0.24, 0.42, 0.24), (0.52, 0.30, 0.30), (0.79, 0.45, 0.23)):
        d.ellipse((w * (cx - r), h * (cy - r), w * (cx + r), h * (cy + r)), fill=255)
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
    body_shape: str          # squircle and circle are Kenney bases; cloud is generated
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
    Biped("nu", "cloud", PALETTES["mustard"], "pigtails", "dots", "observer"),
]

# How far each hair style sits down onto the crown, as a fraction of its own
# height. A fringe covers the forehead; a tuft rides on top.
HAIR_SEAT = {"tuft": 0.67, "curls": 0.73, "fringe": 0.96}


@dataclass
class Manifest:
    parts: list = field(default_factory=list)
    rig: dict = field(default_factory=dict)

    def group(self, character: str, roots: list, space: str) -> None:
        self.rig[character] = {"roots": list(roots), "space": space,
                               "attach": {}, "slots": {}}

    def add(self, character: str, layer: str, z: int, img: Image.Image,
            pivot: tuple, note: str = "", joints: dict | None = None,
            parent: str | None = None, joint: str | None = None,
            rest_angle: float = 0.0, slot: str | None = None,
            slot_default: bool = False, blend_mode: str = "normal",
            opacity: float = 1.0) -> None:
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
            "pivot": [int(round(pivot[0])), int(round(pivot[1]))],
            "joints": {k: [int(round(v[0])), int(round(v[1]))]
                       for k, v in (joints or {}).items()},
            "blend_mode": blend_mode,
            "opacity": opacity,
            "note": note,
        })
        rig = self.rig[character]
        rig["attach"][layer] = {"parent": parent, "joint": joint,
                                "rest_angle": round(float(rest_angle), 2)}
        if slot:
            entry = rig["slots"].setdefault(slot, {"members": [], "default": None})
            entry["members"].append(layer)
            if slot_default:
                entry["default"] = layer


def build_biped(c: Biped, m: Manifest) -> None:
    p = c.palette
    m.group(c.name, ["body"], "body pivot, +x right, +y down, pixels")

    if c.body_shape == "cloud":
        body = cloud_body(160, 160, p.light, p.dark)
        body_note = "generated cloud silhouette, three lobes over a rounded slab"
    else:
        body = texturise(recolour(_rgba(KENNEY / f"blue_body_{c.body_shape}.png"),
                                  p.light, p.dark))
        body_note = f"Kenney {c.body_shape} base, recoloured"
    bw, bh = body.size
    cx, cy = bw / 2, bh / 2

    shadow = soft_shadow((int(bw * 0.86), int(bh * 0.22)))
    band = shirt(int(bw * 0.92), int(bh * 0.34), p.cloth_light, p.cloth_dark, c.pattern)
    er = max(10, int(bw * 0.13))
    brow = texturise(recolour(_rgba(KENNEY / "facial_part_eyebrow_a.png"),
                              p.hair_light, p.hair_dark))

    arm_len, arm_th = int(bh * 0.62), int(bw * 0.13)
    leg_len, leg_th = int(bh * 0.44), int(bw * 0.17)
    arm_angle, leg_angle = 32.0, 14.0

    eye_y = cy - bh * 0.20
    joints = {
        "ground": (cx, cy + bh * 0.5 - 6 + shadow.height / 2),
        "shoulder_left": (cx - bw * 0.36, cy - bh * 0.16),
        "shoulder_right": (cx + bw * 0.36, cy - bh * 0.16),
        "hip_left": (cx - bw * 0.24, cy + bh * 0.28),
        "hip_right": (cx + bw * 0.24, cy + bh * 0.28),
        "clothing": (cx, cy + bh * 0.06),
        "eye_left": (cx - bw * 0.20, eye_y),
        "eye_right": (cx + bw * 0.20, eye_y),
        "brow_left": (cx - bw * 0.20, eye_y - er - brow.height / 2 - 6),
        "brow_right": (cx + bw * 0.20, eye_y - er - brow.height / 2 - 6),
        "mouth": (cx, cy + bh * 0.02),
        "crown": (cx, cy - bh * 0.40),
    }
    if c.hair == "pigtails":
        joints["pigtail_left"] = (cx - bw * 0.52, cy - bh * 0.34)
        joints["pigtail_right"] = (cx + bw * 0.52, cy - bh * 0.34)

    # Limbs sit behind the body, so their joints are inside the silhouette. Each
    # one is checked against the distance from its own joint to the silhouette
    # edge, which is what actually decides whether a pose is visible.
    for side, sign in (("left", -1.0), ("right", 1.0)):
        check_clearance(f"{c.name} arm_{side}", body, joints[f"shoulder_{side}"],
                        sign * arm_angle, arm_len)
        check_clearance(f"{c.name} leg_{side}", body, joints[f"hip_{side}"],
                        sign * leg_angle, leg_len)

    m.add(c.name, "body", 10, body, (cx, cy), body_note, joints)

    m.add(c.name, "shadow", 0, shadow, (shadow.width / 2, shadow.height / 2),
          "ground contact, follows body x only", parent="body", joint="ground")

    # Legs occupy z 1-2 and arms z 3-4 so no two limbs share a band.
    for side, sign, leg_z, arm_z in (("left", -1.0, 1, 3), ("right", 1.0, 2, 4)):
        leg = limb(leg_len, leg_th, p.light, p.dark)
        m.add(c.name, f"leg_{side}", leg_z, leg, (leg_th // 2, leg_th // 2),
              "pivot at hip; contact joint is the foot on the ground",
              limb_joints(leg_len, leg_th),
              parent="body", joint=f"hip_{side}", rest_angle=sign * leg_angle)
        arm = limb(arm_len, arm_th, p.light, p.dark)
        m.add(c.name, f"arm_{side}", arm_z, arm, (arm_th // 2, arm_th // 2),
              "pivot at shoulder; tip joint is the wrist",
              limb_joints(arm_len, arm_th),
              parent="body", joint=f"shoulder_{side}", rest_angle=sign * arm_angle)

    m.add(c.name, "clothing", 11, band, (band.width / 2, 0),
          f"{c.pattern}, original pattern", parent="body", joint="clothing")

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
            m.add(c.name, f"hand_{side}_{label}", 12, img, (img.width / 2, 4),
                  "pivot at the wrist; grip joint is where a prop attaches",
                  {"grip": (img.width / 2, img.height * 0.62)},
                  parent=f"arm_{side}", joint="tip",
                  slot=f"hand_{side}", slot_default=(label == "open"))

    for side in ("left", "right"):
        for suffix, look, note in ((("", (0.0, 0.0), "sclera, pupil, highlight")),
                                   ("_look_left", (-0.6, 0.0), "gaze target"),
                                   ("_look_right", (0.6, 0.0), "gaze target")):
            m.add(c.name, f"eye_{side}{suffix}", 20, eye(er, look), (er, er), note,
                  {"pupil": (er + look[0] * (er - int(er * 0.52)), er)},
                  parent="body", joint=f"eye_{side}",
                  slot=f"eye_{side}", slot_default=(suffix == ""))

    for side in ("left", "right"):
        img = brow.transpose(Image.FLIP_LEFT_RIGHT) if side == "right" else brow
        m.add(c.name, f"eyebrow_{side}", 21, img, (img.width / 2, img.height / 2),
              "pivot at the brow centre", parent="body", joint=f"brow_{side}")

    mb = int(bw * 0.34)
    for state in MOUTH_STATES:
        img = mouth(mb, state)
        m.add(c.name, f"mouth_{state}", 22, img, (img.width / 2, 0),
              "viseme" if state.startswith("viseme") else "expression",
              parent="body", joint="mouth",
              slot="mouth", slot_default=(state == "smile"))

    hl, hd = p.hair_light, p.hair_dark
    if c.hair == "tuft":
        hair = hair_tuft(int(bw * 0.52), int(bh * 0.30), hl, hd)
        seat = HAIR_SEAT["tuft"]
    elif c.hair == "curls":
        hair = hair_curls(int(bw * 0.86), int(bh * 0.26), hl, hd)
        seat = HAIR_SEAT["curls"]
    else:
        hair = hair_curls(int(bw * 0.52), int(bh * 0.16), hl, hd)
        seat = HAIR_SEAT["fringe"]
    m.add(c.name, "hair", 30, hair, (hair.width / 2, int(hair.height * seat)),
          "pivot where the hair seats on the crown", parent="body", joint="crown")

    if c.hair == "pigtails":
        pt = pigtail(int(bw * 0.13), hl, hd)
        for side in ("left", "right"):
            m.add(c.name, f"pigtail_{side}", 29, pt, (pt.width / 2, pt.height * 0.18),
                  "pivot at the tie against the skull, secondary motion candidate",
                  {"tip": (pt.width / 2, pt.height)},
                  parent="body", joint=f"pigtail_{side}")


def build_quadruped(m: Manifest) -> None:
    """Mochi. Not in the Kenney pack; composed from the same shape language."""
    p = Palette((236, 222, 208), (196, 174, 158), (120, 96, 84), (86, 66, 58),
                (255, 255, 255), (226, 226, 226))
    name = "mochi"
    m.group(name, ["body"], "body pivot, +x right, +y down, pixels")
    bw, bh = 220, 140
    cx, cy = bw / 2, bh / 2

    mask = Image.new("L", (bw, bh), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, bw - 1, bh - 1), fill=255)
    body = shaped(mask, p.light, p.dark)

    shadow = soft_shadow((int(bw * 0.9), 34))
    leg_len, leg_th = 84, 26
    hd = 118

    # Mochi faces left, so the fore legs are at the left of the body. The near
    # side is `_left`; the far side is `_right` and is drawn first.
    legs = (
        ("fore_left", -0.30, -10.0, 4, "shoulder_fore_left", "pivot at the near shoulder"),
        ("fore_right", -0.36, -6.0, 2, "shoulder_fore_right", "pivot at the far shoulder"),
        ("hind_left", 0.30, 10.0, 3, "hip_hind_left", "pivot at the near hip"),
        ("hind_right", 0.36, 6.0, 1, "hip_hind_right", "pivot at the far hip"),
    )
    joints = {"ground": (cx, cy + bh / 2 - 4 + shadow.height / 2),
              "neck": (bw * 0.30, bh * 0.44),
              "rump": (bw * 0.94, bh * 0.32)}
    for _, dx, _, _, jname, _ in legs:
        joints[jname] = (cx + bw * dx, cy + bh * 0.26)

    for layer, _, angle, _, jname, _ in legs:
        check_clearance(f"{name} leg_{layer}", body, joints[jname], angle, leg_len)

    m.add(name, "body", 10, body, (cx, cy),
          "torso; every limb, the head and the tail hang off this", joints)

    m.add(name, "shadow", 0, shadow, (shadow.width / 2, shadow.height / 2),
          "four-point contact, locomotion critical", parent="body", joint="ground")

    for layer, _, angle, z, jname, note in legs:
        m.add(name, f"leg_{layer}", z, limb(leg_len, leg_th, p.light, p.dark),
              (leg_th // 2, leg_th // 2), f"{note}; contact joint is the ground point",
              limb_joints(leg_len, leg_th),
              parent="body", joint=jname, rest_angle=angle)

    tail = limb(70, 20, p.light, p.dark)
    m.add(name, "tail", 9, tail, (10, 10), "pivot at the rump, secondary motion",
          limb_joints(70, 20), parent="body", joint="rump", rest_angle=130.0)

    hm = Image.new("L", (hd, hd), 0)
    ImageDraw.Draw(hm).ellipse((0, 0, hd - 1, hd - 1), fill=255)
    # The neck is the point on the skull nearest the torso, not the head centre.
    # Rotating a head about its centre swings the skull; rotating it about the
    # neck is what a nod is.
    head_joints = {
        "ear_left": (hd / 2 - hd * 0.22, 28),
        "ear_right": (hd / 2 + hd * 0.18, 28),
        "eye_left": (hd / 2 - hd * 0.20, hd * 0.30 + 17),
        "eye_right": (hd / 2 + hd * 0.16, hd * 0.30 + 17),
        "nose": (hd / 2 - 6, hd * 0.56 + 13),
        "mouth": (hd / 2 - 6, hd * 0.80),
    }
    m.add(name, "head", 20, shaped(hm, p.light, p.dark), (hd * 0.90, hd * 0.58),
          "pivot at the neck, where the skull meets the torso", head_joints,
          parent="body", joint="neck")

    em = Image.new("L", (52, 66), 0)
    ImageDraw.Draw(em).ellipse((0, 0, 51, 65), fill=255)
    ear = shaped(em, p.hair_light, p.hair_dark)
    for side in ("left", "right"):
        m.add(name, f"ear_{side}", 19, ear, (26, 56),
              "pivot at the ear base inside the skull, secondary motion",
              {"tip": (26, 0)}, parent="head", joint=f"ear_{side}")

    for side in ("left", "right"):
        m.add(name, f"eye_{side}", 22, eye(17), (17, 17), "sclera, pupil, highlight",
              {"pupil": (17, 17)}, parent="head", joint=f"eye_{side}")
    nm = Image.new("RGBA", (34, 26), (0, 0, 0, 0))
    ImageDraw.Draw(nm).ellipse((0, 0, 33, 25), fill=INK)
    m.add(name, "nose", 23, nm, (17, 13), "muzzle centre", parent="head", joint="nose")
    for state in ("neutral", "open", "smile"):
        img = mouth(46, state)
        m.add(name, f"mouth_{state}", 24, img, (img.width / 2, 0), "expression",
              parent="head", joint="mouth",
              slot="mouth", slot_default=(state == "smile"))


def build_vehicle(m: Manifest) -> None:
    """A pull-along cart. Wheels are separate so cycles can be asserted."""
    p = Palette((188, 214, 240), (120, 158, 204), (70, 82, 104), (48, 58, 76),
                (255, 255, 255), (226, 226, 226))
    name = "cart"
    m.group(name, ["body"], "body pivot, +x right, +y down, pixels")
    bw, bh = 260, 120
    cx, cy = bw / 2, bh / 2
    wd = 76

    shadow = soft_shadow((int(bw * 0.92), 30))
    mask = Image.new("L", (bw, bh), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, bw - 1, bh - 1), radius=34, fill=255)
    joints = {
        "ground": (cx, cy + bh / 2 + 10 + shadow.height / 2),
        "axle_front": (bw * 0.20, bh * 0.92),
        "axle_rear": (bw * 0.80, bh * 0.92),
        "hitch": (bw * 0.04, bh * 0.30),
        "cargo": (cx, 0),
    }
    m.add(name, "body", 10, shaped(mask, p.light, p.dark), (cx, cy),
          "prop and character attachment surface; cargo joint is the load point", joints)
    m.add(name, "shadow", 0, shadow, (shadow.width / 2, shadow.height / 2),
          "ground contact, follows body x only", parent="body", joint="ground")

    wm = Image.new("L", (wd, wd), 0)
    ImageDraw.Draw(wm).ellipse((0, 0, wd - 1, wd - 1), fill=255)
    wheel = shaped(wm, p.hair_light, p.hair_dark)
    hub = ImageDraw.Draw(wheel)
    hub.ellipse((wd * 0.36, wd * 0.36, wd * 0.64, wd * 0.64), fill=(255, 255, 255, 210))
    hub.rectangle((wd * 0.47, wd * 0.10, wd * 0.53, wd * 0.90), fill=(255, 255, 255, 90))
    for side, z in (("rear", 11), ("front", 12)):
        m.add(name, f"wheel_{side}", z, wheel, (wd // 2, wd // 2),
              "pivot at axle centre, rotation cycle must match ground travel",
              {"contact": (wd // 2, wd - 1)},
              parent="body", joint=f"axle_{side}")

    handle = limb(120, 22, p.light, p.dark)
    m.add(name, "handle", 9, handle, (11, 11), "pivot at the hitch; tip is the pull point",
          limb_joints(120, 22), parent="body", joint="hitch", rest_angle=-118.0)


def build_props(m: Manifest) -> None:
    name = "props"
    m.group(name, ["ball", "drum"], "each prop's own pivot, +x right, +y down, pixels")

    bm = Image.new("L", (96, 96), 0)
    ImageDraw.Draw(bm).ellipse((0, 0, 95, 95), fill=255)
    ball = shaped(bm, (255, 196, 196), (222, 116, 128))
    d = ImageDraw.Draw(ball)
    d.arc((8, 8, 87, 87), start=200, end=340, fill=(255, 255, 255, 150), width=6)
    ball.putalpha(bm)
    m.add(name, "ball", 10, ball, (48, 48),
          "handoff and attachment prop; grip joint meets a hand grip joint",
          {"grip": (48, 48), "ground": (48, 100)})

    dm = Image.new("L", (120, 84), 0)
    ImageDraw.Draw(dm).rounded_rectangle((0, 0, 119, 83), radius=18, fill=255)
    drum = shaped(dm, (250, 226, 190), (214, 172, 122))
    dd = ImageDraw.Draw(drum)
    for x in range(12, 110, 24):
        dd.line((x, 10, x + 12, 74), fill=(255, 255, 255, 90), width=4)
    drum.putalpha(dm)
    m.add(name, "drum", 11, drum, (60, 42),
          "beat-synchronised prop; strike joint is the beat contact point",
          {"grip": (60, 42), "strike": (60, 8), "ground": (60, 88)})

    shadow = soft_shadow((72, 22))
    m.add(name, "shadow_small", 0, shadow, (36, 11),
          "shared prop shadow; reparent under any prop with a ground joint",
          parent="ball", joint="ground")


def build_scene(m: Manifest) -> None:
    """Environment layers, recoloured from the Kenney tile set for parallax.

    z runs far to near and matches the parallax factor: the sky band moves least.
    """
    name = "scene"
    bands = (
        ("tile_cloud", "cloud", 0, 0.10, "sky band, farthest"),
        ("tile_background_tree_large", "tree_large", 1, 0.30, "far band"),
        ("tile_background_tree_small", "tree_small", 2, 0.55, "mid band"),
        ("tile_background_grass", "grass", 3, 1.00, "near band, carries the ground line"),
    )
    m.group(name, [layer for _, layer, _, _, _ in bands],
            "each band's own pivot at the ground line, +x right, +y down, pixels")
    m.rig[name]["parallax"] = {layer: factor for _, layer, _, factor, _ in bands}
    for src, layer, z, factor, note in bands:
        img = texturise(recolour(_rgba(KENNEY / f"{src}.png"),
                                 (214, 234, 214), (140, 182, 152)), 0.10)
        m.add(name, layer, z, img, (img.width / 2, img.height),
              f"{note}; parallax factor {factor}", {"ground": (img.width / 2, img.height)})


def main() -> None:
    verify_sources()
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
        "version": "0.2.0-draft",
        "status": "draft, not approved; RGT-S003 is active and RGT-D-fixture has not been recorded",
        "generator": "fixtures/tools/build_cast.py",
        "provenance_record": "fixtures/PROVENANCE.json",
        "originality": (
            "Characters are original compositions: new palette, new hair, new clothing "
            "patterns, generated limbs, eyes and visemes. No visual identity is copied "
            "from any reference channel, and no reference video supplied any asset."
        ),
        "coordinate_note": (
            "A part's `pivot` and its `joints` are pixels from that part's own top-left. "
            "`rig` places parts in character space: a character's space is its root "
            "part's pivot, +x right, +y down, in pixels. A part is attached by putting "
            "its own pivot on the named joint of its parent, then rotating by "
            "`rest_angle` degrees counter-clockwise about that point. A part's pivot is "
            "always its anchor, so no separate anchor field is needed."
        ),
        "blend_profile": {
            "default": "normal",
            "supported": ["normal", "multiply", "screen"],
            "note": (
                "Every part carries an explicit `blend_mode` and `opacity`. A consumer "
                "that cannot honour a part's declared mode must fail rather than "
                "silently substitute `normal`."
            ),
        },
        "rig": m.rig,
        "parts": sorted(m.parts, key=lambda r: (r["character"], r["z"], r["layer"])),
    }
    (OUT / "manifest.json").write_text(json.dumps(doc, indent=2) + "\n")

    chars = sorted({r["character"] for r in m.parts})
    print(f"{len(m.parts)} parts across {len(chars)} groups: {', '.join(chars)}")
    print(f"manifest: {OUT / 'manifest.json'}")


if __name__ == "__main__":
    main()
