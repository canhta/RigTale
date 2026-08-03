#!/usr/bin/env python3
"""Build the RigTale reference cast as layered cutout parts.

Sources are CC0 and are NOT vendored. `fixtures/PROVENANCE.json` is the tracked
licence record and names the two archives to fetch. Every input is read from
inside one of those archives, after the archive has matched its recorded SHA-256
and byte size and the member itself has matched the digest recorded for it, so
the record is bound to the bytes this build actually consumed.

    python3 fixtures/tools/build_cast.py
    python3 fixtures/tools/build_cast.py --update-provenance

Every part is emitted as its own PNG with a recorded pivot, its own joint points,
a place in the character's rig tree and, where it deforms, a mesh bound to that
tree's bones, because the fixture exists to exercise rigging. A flattened
character would assert nothing.

Nothing here is asserted that is not also checked: the manifest against the files
on disk, the colour block against the emitted PNG bytes, the blend profile
against the modes in use, shared `z` against real overlap, every declared ground
plane against its own contacts, and the reference pose against the seam, the
contacts and the ground.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import math
import platform
import re
import sys
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import PIL
from PIL import Image, ImageDraw, ImageFilter

sys.dont_write_bytecode = True  # keep the fixture tree free of build litter
sys.path.insert(0, str(Path(__file__).resolve().parent))
import rig as rig_eval  # noqa: E402  the shared attachment rule, used to check output

ROOT = Path(__file__).resolve().parents[2]
PROVENANCE = ROOT / "fixtures/PROVENANCE.json"
README = ROOT / "fixtures/README.md"
OUT = ROOT / "fixtures/cast"

# Fetch location. This is a build input, not provenance: the licence facts live
# in PROVENANCE.json and nowhere else. Nothing is read from the sandbox except
# the two archives named there, and nothing is read from them unverified.
SANDBOX = ROOT / ".sandbox"
DOWNLOADS = SANDBOX / "downloads"

KENNEY = "kenney-shape-characters"
FABRIC = "ambientcg-fabric034"
FABRIC_COLOR = "Fabric034_1K-JPG_Color.jpg"

TEXTURE_STRENGTH = 0.16  # felt weave, deliberately subtle
INK = (58, 62, 84, 255)  # shared dark for pupils, mouths, brows

# A limb must show at least this many pixels beyond the body silhouette, measured
# from its own joint along its own rest axis. See `check_clearance`.
LIMB_CLEARANCE = 24


# --------------------------------------------------------------------------
# source verification
# --------------------------------------------------------------------------

def tag(img: Image.Image, *sources: str) -> Image.Image:
    """Record which source members an image's pixels came from."""
    img.rigtale_sources = set(sources) | set(getattr(img, "rigtale_sources", ()))
    return img


def inherit(new: Image.Image, *older: Image.Image) -> Image.Image:
    """Carry source attribution across a transform."""
    return tag(new, *(s for o in older for s in getattr(o, "rigtale_sources", ())))


class Sources:
    """The only door to source bytes.

    The build reads every input out of an archive that has already matched the
    SHA-256 and byte size recorded in `fixtures/PROVENANCE.json`, and checks each
    member it decompresses against the digest recorded for that member. There is
    no extracted tree in the path, so no file on disk outside a verified archive
    can reach the output, and the record is bound to the bytes actually consumed
    rather than to a container beside them.
    """

    def __init__(self, record: dict, update: bool = False) -> None:
        self.record = record
        self.update = update
        self.by_key = {s["key"]: s for s in record["sources"]}
        self.zips: dict[str, zipfile.ZipFile] = {}
        # (key, member) -> {"sha256", "bytes", "treatment", "parts"}
        self.used: dict[tuple[str, str], dict] = {}

    def verify(self) -> None:
        """Verify every archive, then its shipped licence evidence."""
        for source in self.record["sources"]:
            archive = source["archive"]
            found = (next(DOWNLOADS.rglob(archive["file"]), None)
                     if DOWNLOADS.exists() else None)
            if found is None:
                raise SystemExit(
                    f"Missing CC0 source archive '{archive['file']}' for "
                    f"{source['name']}.\nDownload it from {source['download_url']} "
                    f"into {DOWNLOADS}; see fixtures/README.md, Regenerating."
                )
            data = found.read_bytes()
            digest = hashlib.sha256(data).hexdigest()
            if len(data) != archive["bytes"] or digest != archive["sha256"]:
                raise SystemExit(
                    f"{archive['file']} does not match fixtures/PROVENANCE.json.\n"
                    f"  expected sha256 {archive['sha256']} ({archive['bytes']} bytes)\n"
                    f"  found    sha256 {digest} ({len(data)} bytes)\n"
                    "Re-download the recorded archive, or correct the record if the "
                    "source genuinely changed."
                )
            self.zips[source["key"]] = zipfile.ZipFile(found)
            self._check_licence(source)
            names = set(self.zips[source["key"]].namelist())
            missing = sorted(d["member"] for d in source.get("derives", [])
                             if d["member"] not in names)
            if missing:
                raise SystemExit(
                    f"{source['name']}: fixtures/PROVENANCE.json records inputs the "
                    f"verified archive does not contain: {missing}."
                )

    def _check_licence(self, source: dict) -> None:
        """A licence file quoted in the record must still say what we quote."""
        evidence = source["licence_evidence"]
        member = evidence.get("member")
        if not member:
            return
        text = self.raw(source["key"], member).decode("utf-8", "replace")
        if evidence["verbatim"] not in text:
            raise SystemExit(
                f"{source['name']}: {member} in the archive no longer contains the "
                f"licence text quoted in fixtures/PROVENANCE.json:\n"
                f"  {evidence['verbatim']!r}"
            )

    def raw(self, key: str, member: str) -> bytes:
        archive = self.by_key[key]["archive"]["file"]
        try:
            return self.zips[key].read(member)
        except KeyError:
            raise SystemExit(
                f"'{member}' is not in {archive}. fixtures/PROVENANCE.json names an "
                "input the verified archive does not contain."
            ) from None

    def read(self, key: str, member: str, treatment: str) -> bytes:
        """Bytes of one recorded member, checked against its recorded digest."""
        data = self.raw(key, member)
        digest = hashlib.sha256(data).hexdigest()
        entry = self.used.setdefault((key, member), {
            "sha256": digest, "bytes": len(data),
            "treatment": treatment, "parts": set()})
        recorded = {d["member"]: d for d in self.by_key[key].get("derives", [])}
        expected = recorded.get(member)
        if expected is None and self.update:
            return data
        if expected is None:
            raise SystemExit(
                f"{member} is read from {key} but is not recorded in "
                "fixtures/PROVENANCE.json. Run build_cast.py --update-provenance "
                "and review the diff."
            )
        if expected["sha256"] != digest or expected["bytes"] != len(data):
            raise SystemExit(
                f"{key}:{member} does not match fixtures/PROVENANCE.json.\n"
                f"  expected sha256 {expected['sha256']} ({expected['bytes']} bytes)\n"
                f"  found    sha256 {digest} ({len(data)} bytes)\n"
                "The archive matched but the member did not, which means the record "
                "and the bytes this build consumed disagree."
            )
        return data

    def image(self, key: str, member: str, treatment: str) -> Image.Image:
        img = Image.open(io.BytesIO(self.read(key, member, treatment)))
        return tag(img.convert("RGBA"), f"{key}:{member}")

    def attribute(self, part: str, img: Image.Image) -> list:
        """Credit a finished part to every source member its pixels came from."""
        names = sorted(getattr(img, "rigtale_sources", ()))
        for name in names:
            key, member = name.split(":", 1)
            self.used[(key, member)]["parts"].add(part)
        return names


SOURCES: Sources | None = None


# --------------------------------------------------------------------------
# colour and texture helpers
# --------------------------------------------------------------------------

def kenney(member: str, treatment: str) -> Image.Image:
    """One Kenney part PNG, straight out of the verified archive."""
    return SOURCES.image(KENNEY, f"PNG/Double/{member}.png", treatment)


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
    return inherit(
        Image.fromarray(np.concatenate([out, alpha], axis=-1).astype(np.uint8), "RGBA"),
        src)


_fabric_cache: dict[tuple[int, int], np.ndarray] = {}

FABRIC_TREATMENT = (
    "converted to luminance, tiled to the part size, mean-centred and added to "
    "the part's RGB at 0.16 strength, 0.10 on the scene tiles. Alpha is never touched."
)


def _fabric(size: tuple[int, int]) -> np.ndarray:
    """Tileable fabric luminance, centred on zero, cached per size."""
    if size not in _fabric_cache:
        tex = Image.open(io.BytesIO(
            SOURCES.read(FABRIC, FABRIC_COLOR, FABRIC_TREATMENT))).convert("L")
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
    out = Image.fromarray(
        np.concatenate([np.clip(rgb + weave, 0, 255), alpha], axis=-1).astype(np.uint8), "RGBA"
    )
    return tag(inherit(out, img), f"{FABRIC}:{FABRIC_COLOR}")


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


def tint(img: Image.Image, decorate, mask: Image.Image | None = None) -> Image.Image:
    """Composite a translucent decoration into a part instead of stamping its alpha.

    `ImageDraw` writes a fill's alpha straight into the target, so a translucent
    fill drawn onto a part either punches a hole in an opaque region or is thrown
    away by a later `putalpha`. Every decoration in this cast — a clothing
    pattern, a wheel hub, an eye highlight — is a colour tint, not a hole. It is
    drawn on its own transparent layer and composited, so the tint lands at the
    strength it was authored with and the part's alpha stays exactly its
    silhouette mask.
    """
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    decorate(ImageDraw.Draw(layer))
    out = inherit(Image.alpha_composite(img, layer), img)
    if mask is not None:
        out.putalpha(mask)
    return out


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

def limb(length: int, thickness: int, light: tuple, dark: tuple,
         cap_top: bool = True, cap_bottom: bool = True) -> Image.Image:
    """A rounded capsule drawn pointing down from the centre of its top cap.

    An end can be squared off instead. That is what makes a shared-edge seam
    possible: a thigh with a flat bottom and a shin with a flat top meet along
    one straight line, so a backend that deforms the two sides inconsistently
    opens a visible gap instead of hiding it under a rounded overlap.
    """
    m = Image.new("L", (thickness, length), 0)
    d = ImageDraw.Draw(m)
    r = thickness // 2
    d.rounded_rectangle((0, 0, thickness - 1, length - 1), radius=r, fill=255)
    if not cap_top:
        d.rectangle((0, 0, thickness - 1, r), fill=255)
    if not cap_bottom:
        d.rectangle((0, length - 1 - r, thickness - 1, length - 1), fill=255)
    return shaped(m, light, dark)


# --------------------------------------------------------------------------
# deformation
# --------------------------------------------------------------------------

def weight_row(t: float, heads: list) -> list:
    """Bone weights at position `t` along a strip, from the bone head positions.

    One rule covers every weight in this cast: a bone's weight ramps linearly
    from 0 at the previous bone's head to 1 at its own head, and stays 1 beyond
    it; the previous bone takes the remainder. Above the first head the first
    bone owns the vertex outright.
    """
    w = [0.0] * len(heads)
    if t <= heads[0]:
        w[0] = 1.0
        return w
    for i in range(1, len(heads)):
        if t <= heads[i]:
            share = round((t - heads[i - 1]) / (heads[i] - heads[i - 1]), 4)
            w[i] = share
            w[i - 1] = round(1.0 - share, 4)
            return w
    w[-1] = 1.0
    return w


def strip_mesh(size: tuple, bones: list, heads: list, steps: int,
               axis: str = "y") -> dict:
    """A two-rail strip over the part's rectangle, bound to a bone chain.

    Coarse on purpose. A limb is two rails of `steps + 1` rungs, so it carries
    2*steps triangles: enough to show a bend, few enough that a reviewer can
    check the weights by reading them.
    """
    w, h = size
    span = h if axis == "y" else w
    cuts = [round(span * i / steps, 2) for i in range(steps + 1)]
    verts, uvs, weights = [], [], []
    for t in cuts:
        pair = ((0.0, t), (float(w), t)) if axis == "y" else ((t, 0.0), (t, float(h)))
        row = weight_row(t, heads)
        for x, y in pair:
            verts.append([x, y])
            uvs.append([round(x / w, 5), round(y / h, 5)])
            weights.append(list(row))
    triangles = []
    for i in range(steps):
        a, b, c, d = 2 * i, 2 * i + 1, 2 * i + 2, 2 * i + 3
        triangles.append([a, b, d])
        triangles.append([a, d, c])
    return {"bones": list(bones), "heads": list(heads), "axis": axis,
            "vertices": verts, "uv": uvs, "triangles": triangles,
            "weights": weights}


def limb_joints(length: int, thickness: int) -> dict:
    """Far-end joints of a capsule: the far cap centre, and the ground contact."""
    return {
        "tip": [thickness // 2, length - thickness // 2],
        "contact": [thickness // 2, length - 1],
    }


def foot_reach(length: int, thickness: int) -> float:
    """Distance from a capsule's pivot to its contact joint, along the capsule."""
    return float((length - 1) - thickness // 2)


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
    box = (cx - pr * 0.45 - hr, cy - pr * 0.5 - hr, cx - pr * 0.45 + hr, cy - pr * 0.5 + hr)
    # The highlight is a bright tint on the pupil, not a hole through the eye.
    return tint(img, lambda dr2: dr2.ellipse(box, fill=(255, 255, 255, 235)))


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
    ink = (255, 255, 255, 64)  # a quarter-strength white, tinted into the weave

    def decorate(dr: ImageDraw.ImageDraw) -> None:
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

    # The mask clips the pattern back to the band; without it a stripe that runs
    # past the rounded corner would leave the silhouette.
    return tint(img, decorate, m)


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


# A part that hangs off a parent but must not turn or lift with it. The shadow
# is the case: it tracks the body along the floor and nothing else.
GROUND_PROJECTED = {
    "kind": "ground_projected",
    "inherit_rotation": False,
    "inherit_translation": ["x"],
    "pin": "character ground plane",
}

# A highlight belongs to the light, not to the surface. It follows the ball
# around but must not spin with it.
LIGHT_LOCKED = {
    "kind": "light_locked",
    "inherit_rotation": False,
    "inherit_translation": ["x", "y"],
    "pin": "the key light's direction in character space",
}

# A ground shadow darkens what is under it; that is multiply, not normal. It is
# also the part that carries reduced opacity, so one part exercises both and the
# order they are applied in is observable.
SHADOW_BLEND = {"blend_mode": "multiply", "opacity": 0.8}


@dataclass
class Manifest:
    parts: list = field(default_factory=list)
    rig: dict = field(default_factory=dict)
    images: dict = field(default_factory=dict)

    def group(self, character: str, roots: list, space: str) -> None:
        self.rig[character] = {"roots": list(roots), "space": space,
                               "attach": {}, "slots": {}, "bones": [], "ground": []}

    def bone(self, character: str, name: str, head: str,
             parent: str | None = None) -> str:
        """Declare a deform bone: a rotation about an existing rig joint."""
        self.rig[character]["bones"].append(
            {"name": name, "parent": parent, "head": head})
        return name

    def ground(self, character: str, part: str, joint: str, contacts: list) -> None:
        """Declare where this root stands: one joint, and the contacts it holds."""
        self.rig[character]["ground"].append(
            {"part": part, "joint": joint, "contacts": list(contacts)})

    def add(self, character: str, layer: str, z: int, img: Image.Image,
            pivot: tuple, note: str = "", joints: dict | None = None,
            parent: str | None = None, joint: str | None = None,
            rest_angle: float = 0.0, slot: str | None = None,
            slot_default: bool = False, blend_mode: str = "normal",
            opacity: float = 1.0, constraint: dict | None = None,
            mesh: dict | None = None) -> None:
        rel = f"{character}/{layer}.png"
        path = OUT / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        img.save(path)
        self.images[(character, layer)] = img
        self.parts.append({
            "character": character,
            "layer": layer,
            "file": rel,
            "z": z,
            "size": list(img.size),
            "pivot": [int(round(pivot[0])), int(round(pivot[1]))],
            "joints": {k: [int(round(v[0])), int(round(v[1]))]
                       for k, v in (joints or {}).items()},
            "sources": SOURCES.attribute(f"{character}/{layer}", img),
            "blend_mode": blend_mode,
            "opacity": opacity,
            "mesh": mesh,
            "note": note,
        })
        rig = self.rig[character]
        rig["attach"][layer] = {"parent": parent, "joint": joint,
                                "rest_angle": round(float(rest_angle), 2),
                                "constraint": constraint}
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
        body = texturise(recolour(
            kenney(f"blue_body_{c.body_shape}",
                   "recoloured onto the character's two-stop ramp, keeping the "
                   "original vertical shading as the ramp position"),
            p.light, p.dark))
        body_note = f"Kenney {c.body_shape} base, recoloured"
    bw, bh = body.size
    cx, cy = bw / 2, bh / 2

    shadow = soft_shadow((int(bw * 0.86), int(bh * 0.22)))
    band = shirt(int(bw * 0.92), int(bh * 0.34), p.cloth_light, p.cloth_dark, c.pattern)
    er = max(10, int(bw * 0.13))
    brow = texturise(recolour(
        kenney("facial_part_eyebrow_a",
               "recoloured onto the hair ramp, mirrored for the right side"),
        p.hair_light, p.hair_dark))

    arm_len, arm_th = int(bh * 0.62), int(bw * 0.13)
    leg_len, leg_th = int(bh * 0.52), int(bw * 0.17)
    arm_angle, leg_angle = 32.0, 14.0

    # The leg is two parts meeting along a straight knee line. The thigh's flat
    # bottom edge and the shin's flat top edge are the same edge in character
    # space, so the seam is a real one: get the two sides' deformation out of
    # step and it opens. The split is below the body silhouette on every biped,
    # because a seam hidden behind the torso would assert nothing.
    thigh_len = int(leg_len * 0.60)
    shin_len = leg_len - thigh_len

    # The ground plane is where the feet actually land, not where the body
    # silhouette ends: hip, leg reach and rest angle decide it. Solving it from
    # the silhouette is what put the three archetypes on three different floors.
    hip_y = round(cy + bh * 0.28)
    leg_reach = (thigh_len - leg_th // 2) + (shin_len - 1)
    ground_y = hip_y + leg_reach * math.cos(math.radians(leg_angle))

    eye_y = cy - bh * 0.20
    joints = {
        "ground": (cx, ground_y),
        "shoulder_left": (cx - bw * 0.36, cy - bh * 0.16),
        "shoulder_right": (cx + bw * 0.36, cy - bh * 0.16),
        "hip_left": (cx - bw * 0.24, hip_y),
        "hip_right": (cx + bw * 0.24, hip_y),
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
        # The knee seam must clear the body too, or nothing can see it split.
        exit_at = silhouette_exit(body, joints[f"hip_{side}"], sign * leg_angle,
                                  float(leg_len))
        knee_at = thigh_len - leg_th // 2
        if knee_at <= exit_at:
            raise SystemExit(
                f"{c.name} leg_{side}: the knee seam is {knee_at} px from the hip but "
                f"the body silhouette ends at {exit_at:.0f} px, so the seam is hidden "
                "behind the torso and a split in it would be invisible."
            )

    m.add(c.name, "body", 10, body, (cx, cy), body_note, joints)

    m.add(c.name, "shadow", 0, shadow, (shadow.width / 2, shadow.height / 2),
          "ground shadow; its centre is the ground plane the feet stand on",
          parent="body", joint="ground", constraint=GROUND_PROJECTED, **SHADOW_BLEND)
    m.ground(c.name, "body", "ground",
             ["leg_left_lower/contact", "leg_right_lower/contact"])

    # Legs occupy z 1-4 and arms 5-6, so no two limbs share a band.
    for side, sign, thigh_z, shin_z, arm_z in (("left", -1.0, 1, 2, 5),
                                               ("right", 1.0, 3, 4, 6)):
        hip = m.bone(c.name, f"hip_{side}", f"body/hip_{side}")
        knee = m.bone(c.name, f"knee_{side}", f"leg_{side}_upper/knee", parent=hip)
        shoulder = m.bone(c.name, f"shoulder_{side}", f"body/shoulder_{side}")
        elbow = m.bone(c.name, f"elbow_{side}", f"arm_{side}/elbow", parent=shoulder)

        thigh = limb(thigh_len, leg_th, p.light, p.dark, cap_bottom=False)
        m.add(c.name, f"leg_{side}_upper", thigh_z, thigh, (leg_th // 2, leg_th // 2),
              "thigh; pivot at the hip, knee joint on its flat bottom edge, which "
              f"is the seam it shares with leg_{side}_lower",
              {"knee": (leg_th // 2, thigh_len)},
              parent="body", joint=f"hip_{side}", rest_angle=sign * leg_angle,
              mesh=strip_mesh(thigh.size, [hip, knee],
                              [leg_th / 2, float(thigh_len)], 3))

        shin = limb(shin_len, leg_th, p.light, p.dark, cap_top=False)
        m.add(c.name, f"leg_{side}_lower", shin_z, shin, (leg_th // 2, 0),
              "shin; pivot on its flat top edge, on the knee. The contact joint "
              "rides this part's mesh, so a bent knee moves the foot",
              limb_joints(shin_len, leg_th),
              parent=f"leg_{side}_upper", joint="knee",
              # The hip head sits above this part entirely, so every shin vertex
              # is the knee bone's outright and the shared edge agrees with the
              # thigh's last row by construction.
              mesh=strip_mesh(shin.size, [hip, knee],
                              [-(thigh_len - leg_th // 2), 0.0], 3))

        arm = limb(arm_len, arm_th, p.light, p.dark)
        arm_joints = limb_joints(arm_len, arm_th)
        arm_joints["elbow"] = [arm_th // 2, arm_len // 2]
        m.add(c.name, f"arm_{side}", arm_z, arm, (arm_th // 2, arm_th // 2),
              "pivot at shoulder; elbow joint bends it, tip joint is the wrist",
              arm_joints,
              parent="body", joint=f"shoulder_{side}", rest_angle=sign * arm_angle,
              mesh=strip_mesh(arm.size, [shoulder, elbow],
                              [arm_th / 2, float(arm_len // 2)], 4))

    m.add(c.name, "clothing", 11, band, (band.width / 2, 0),
          f"{c.pattern}, original pattern", parent="body", joint="clothing")

    # Kenney's hands are drawn for a larger figure. At cast scale the splayed
    # open hand reads as a frond, so every hand is scaled down to sit against
    # the arm rather than compete with the body.
    HAND_SCALE = 0.55
    hands = {}
    for label, src in (("open", "blue_hand_open"), ("closed", "blue_hand_closed"),
                       ("point", "blue_hand_point")):
        im = texturise(recolour(
            kenney(src, "recoloured onto the character's ramp, scaled to 0.55 and "
                        "mirrored for the right side"),
            p.light, p.dark))
        hands[label] = inherit(im.resize(
            (max(8, int(im.width * HAND_SCALE)), max(8, int(im.height * HAND_SCALE))),
            Image.LANCZOS,
        ), im)
    for side in ("left", "right"):
        flip = side == "right"
        for label, im in hands.items():
            img = inherit(im.transpose(Image.FLIP_LEFT_RIGHT), im) if flip else im
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
        img = inherit(brow.transpose(Image.FLIP_LEFT_RIGHT), brow) if side == "right" else brow
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
                  "pivot at the tie, set outboard of the cloud silhouette so the "
                  "sphere reads clear of the head; secondary motion candidate",
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
    # side is `_left`; the far side is `_right` and is drawn first. Near and far
    # are told apart by their x offset and their z, not by their angle: all four
    # legs splay by the same angle so all four feet land on one plane.
    splay = 8.0
    legs = (
        ("fore_left", -0.30, -splay, 4, "shoulder_fore_left", "pivot at the near shoulder"),
        ("fore_right", -0.36, -splay, 2, "shoulder_fore_right", "pivot at the far shoulder"),
        ("hind_left", 0.30, splay, 3, "hip_hind_left", "pivot at the near hip"),
        ("hind_right", 0.36, splay, 1, "hip_hind_right", "pivot at the far hip"),
    )
    hip_y = round(cy + bh * 0.26)
    joints = {"ground": (cx, hip_y + foot_reach(leg_len, leg_th)
                         * math.cos(math.radians(splay))),
              "neck": (bw * 0.30, bh * 0.44),
              "belly": (cx, cy + bh * 0.30),
              "rump": (bw * 0.94, bh * 0.32)}
    for _, dx, _, _, jname, _ in legs:
        joints[jname] = (cx + bw * dx, hip_y)

    for layer, _, angle, _, jname, _ in legs:
        check_clearance(f"{name} leg_{layer}", body, joints[jname], angle, leg_len)

    m.add(name, "body", 10, body, (cx, cy),
          "torso; every limb, the head and the tail hang off this", joints)

    m.add(name, "shadow", 0, shadow, (shadow.width / 2, shadow.height / 2),
          "four-point contact, locomotion critical; its centre is the ground plane",
          parent="body", joint="ground", constraint=GROUND_PROJECTED, **SHADOW_BLEND)
    m.ground(name, "body", "ground", [f"leg_{layer}/contact" for layer, *_ in legs])

    for layer, _, angle, z, jname, note in legs:
        # The quadruped bends inside one part rather than across a seam: the
        # knee bone's head is a joint on the leg itself.
        upper = m.bone(name, jname, f"body/{jname}")
        knee = m.bone(name, f"knee_{layer}", f"leg_{layer}/knee", parent=upper)
        leg_joints = limb_joints(leg_len, leg_th)
        leg_joints["knee"] = [leg_th // 2, leg_len // 2]
        m.add(name, f"leg_{layer}", z, limb(leg_len, leg_th, p.light, p.dark),
              (leg_th // 2, leg_th // 2), f"{note}; contact joint is the ground point",
              leg_joints, parent="body", joint=jname, rest_angle=angle,
              mesh=strip_mesh((leg_th, leg_len), [upper, knee],
                              [leg_th / 2, float(leg_len // 2)], 4))

    # A three-bone tail: the longest chain in the cast, and the clearest case of
    # deformation running down a chain rather than sitting in one joint.
    tail_len, tail_th = 70, 20
    rump = m.bone(name, "rump", "body/rump")
    tail_mid = m.bone(name, "tail_mid", "tail/knuckle_1", parent=rump)
    tail_end = m.bone(name, "tail_end", "tail/knuckle_2", parent=tail_mid)
    tail = limb(tail_len, tail_th, p.light, p.dark)
    tail_joints = limb_joints(tail_len, tail_th)
    tail_joints["knuckle_1"] = [tail_th // 2, 26]
    tail_joints["knuckle_2"] = [tail_th // 2, 46]
    m.add(name, "tail", 9, tail, (10, 10), "pivot at the rump, secondary motion",
          tail_joints, parent="body", joint="rump", rest_angle=130.0,
          mesh=strip_mesh(tail.size, [rump, tail_mid, tail_end],
                          [tail_th / 2, 26.0, 46.0], 6))

    # Contact shade under the belly. It multiplies onto the torso at reduced
    # opacity and it is a mesh, so one part carries the whole adapter surface
    # that PR-R005 names: textured deformed mesh plus a blend mode. Its bones are
    # the fore and hind legs', not its own parent's, which is the ordinary case
    # of a part skinned to bones outside its attachment chain.
    sw, sh = int(bw * 0.62), 30
    shade = np.zeros((sh, sw, 4), np.float32)
    shade[..., 0], shade[..., 1], shade[..., 2] = 150.0, 132.0, 126.0
    fall = np.sin(np.linspace(0.0, math.pi, sw, dtype=np.float32))[None, :]
    drop = np.sin(np.linspace(0.0, math.pi, sh, dtype=np.float32))[:, None]
    shade[..., 3] = fall * drop * 118.0
    belly = Image.fromarray(np.rint(shade).astype(np.uint8), "RGBA")
    fore_x = (cx + bw * -0.30) - (cx - sw / 2)
    hind_x = (cx + bw * 0.30) - (cx - sw / 2)
    m.add(name, "belly_shade", 11, belly, (sw / 2, sh / 2),
          "contact shade under the belly; multiply at 0.7, and a mesh bound to "
          "the near fore and hind leg bones so it follows the stride",
          {"fore": (fore_x, sh / 2), "hind": (hind_x, sh / 2)},
          parent="body", joint="belly", blend_mode="multiply", opacity=0.7,
          mesh=strip_mesh(belly.size, ["shoulder_fore_left", "hip_hind_left"],
                          [fore_x, hind_x], 4, axis="x"))

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
    # The ears overlap in head space, so they cannot share a z. The far ear is
    # drawn first, matching the near-and-far convention the legs use.
    for side, z in (("right", 18), ("left", 19)):
        m.add(name, f"ear_{side}", z, ear, (26, 56),
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
    axle_y = round(bh * 0.92)
    joints = {
        # The cart stands on its wheels: the ground plane is the axle height plus
        # the wheel radius to its contact joint.
        "ground": (cx, axle_y + (wd - 1 - wd // 2)),
        "axle_front": (bw * 0.20, axle_y),
        "axle_rear": (bw * 0.80, axle_y),
        "hitch": (bw * 0.04, bh * 0.30),
        "cargo": (cx, 0),
    }
    m.add(name, "body", 10, shaped(mask, p.light, p.dark), (cx, cy),
          "prop and character attachment surface; cargo joint is the load point", joints)
    m.add(name, "shadow", 0, shadow, (shadow.width / 2, shadow.height / 2),
          "ground shadow; its centre is the plane the wheels roll on",
          parent="body", joint="ground", constraint=GROUND_PROJECTED, **SHADOW_BLEND)
    m.ground(name, "body", "ground", ["wheel_front/contact", "wheel_rear/contact"])

    wm = Image.new("L", (wd, wd), 0)
    ImageDraw.Draw(wm).ellipse((0, 0, wd - 1, wd - 1), fill=255)
    def hub(dr: ImageDraw.ImageDraw) -> None:
        dr.ellipse((wd * 0.36, wd * 0.36, wd * 0.64, wd * 0.64), fill=(255, 255, 255, 210))
        dr.rectangle((wd * 0.47, wd * 0.10, wd * 0.53, wd * 0.90), fill=(255, 255, 255, 90))

    # Hub and spoke are markings on a solid wheel: tinted in, never punched out.
    wheel = tint(shaped(wm, p.hair_light, p.hair_dark), hub, wm)
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
    m.add(name, "ball", 10, ball, (48, 48),
          "handoff and attachment prop; grip joint meets a hand grip joint",
          {"grip": (48, 48), "ground": (48, 95), "highlight": (48, 48)})
    m.ground(name, "ball", "ground", ["ball/ground"])

    # The specular is its own part because it belongs to the light: it screens
    # over the ball, and it must not turn when the ball rolls.
    hm = Image.new("L", (96, 96), 0)
    ImageDraw.Draw(hm).arc((8, 8, 87, 87), start=200, end=340, fill=190, width=6)
    hm = hm.filter(ImageFilter.GaussianBlur(2.0))
    hm = Image.fromarray(np.minimum(np.asarray(hm), np.asarray(bm)), "L")
    highlight = Image.new("RGBA", (96, 96), (255, 250, 238, 0))
    highlight.putalpha(hm)
    m.add(name, "ball_highlight", 12, highlight, (48, 48),
          "specular highlight, screened over the ball; pivot coincides with the "
          "ball's own pivot so the two are aligned by construction",
          parent="ball", joint="highlight", blend_mode="screen",
          constraint=LIGHT_LOCKED)

    dm = Image.new("L", (120, 84), 0)
    ImageDraw.Draw(dm).rounded_rectangle((0, 0, 119, 83), radius=18, fill=255)
    def lacing(dr: ImageDraw.ImageDraw) -> None:
        for x in range(12, 110, 24):
            dr.line((x, 10, x + 12, 74), fill=(255, 255, 255, 90), width=4)

    drum = tint(shaped(dm, (250, 226, 190), (214, 172, 122)), lacing, dm)
    m.add(name, "drum", 11, drum, (60, 42),
          "beat-synchronised prop; strike joint is the beat contact point",
          {"grip": (60, 42), "strike": (60, 8), "ground": (60, 83)})
    m.ground(name, "drum", "ground", ["drum/ground"])

    shadow = soft_shadow((72, 22))
    m.add(name, "shadow_small", 0, shadow, (36, 11),
          "shared prop shadow; reparent under any prop with a ground joint",
          parent="ball", joint="ground", constraint=GROUND_PROJECTED, **SHADOW_BLEND)


def build_scene(m: Manifest) -> None:
    """Environment layers, recoloured from the Kenney tile set for parallax.

    z runs far to near and matches the parallax factor: the sky band moves least.
    """
    name = "scene"
    bands = (
        ("tile_cloud", "cloud", 1, 0.10, "sky band, farthest"),
        ("tile_background_tree_large", "tree_large", 2, 0.30, "far band"),
        ("tile_background_tree_small", "tree_small", 3, 0.55, "mid band"),
        ("tile_background_grass", "grass", 4, 1.00, "near band, carries the ground line"),
    )
    haze_factor = 0.05
    m.group(name, ["haze"] + [layer for _, layer, _, _, _ in bands],
            "each band's own pivot at the ground line, +x right, +y down, pixels")
    m.rig[name]["parallax"] = dict(
        [("haze", haze_factor)] + [(layer, factor) for _, layer, _, factor, _ in bands])

    # Atmospheric haze at the horizon, authored here. It is the fixture's
    # out-of-profile case: `linear_light` is a Photoshop key with no published
    # formula and no implementation in any 2D library screened, so a consumer
    # honouring the declared profile has to refuse this part by name.
    hw, hh = 256, 56
    ramp = np.linspace(0.0, 1.0, hh, dtype=np.float32)[:, None] ** 1.4
    haze = np.zeros((hh, hw, 4), np.float32)
    haze[..., 0], haze[..., 1], haze[..., 2] = 255.0, 244.0, 214.0
    haze[..., 3] = np.repeat(ramp * 130.0, hw, axis=1)
    haze_img = Image.fromarray(np.rint(haze).astype(np.uint8), "RGBA")
    m.add(name, "haze", 0, haze_img, (hw / 2, hh - 1),
          f"horizon haze, farthest band; parallax factor {haze_factor}. Declares "
          "`linear_light`, which is outside `blend_profile.supported` on purpose",
          {"ground": (hw / 2, hh - 1)}, blend_mode="linear_light", opacity=0.6)
    m.ground(name, "haze", "ground", ["haze/ground"])

    for src, layer, z, factor, note in bands:
        img = texturise(recolour(
            kenney(src, "recoloured onto the scene ramp"),
            (214, 234, 214), (140, 182, 152)), 0.10)
        # The ground joint is the tile's last opaque row, the same convention a
        # foot and a wheel contact use, so a band placed by it meets the same floor.
        base = int(np.nonzero((np.asarray(img)[..., 3] > 8).any(axis=1))[0].max())
        m.add(name, layer, z, img, (img.width / 2, base),
              f"{note}; parallax factor {factor}", {"ground": (img.width / 2, base)})
        m.ground(name, layer, "ground", [f"{layer}/ground"])


# --------------------------------------------------------------------------
# checks on the emitted manifest
# --------------------------------------------------------------------------

# A joint is written as whole pixels, so a contact solved in floating point can
# miss its declared plane by at most half a pixel. Nothing may miss it by more.
GROUND_TOLERANCE = 0.5


def check_ground(doc: dict, images: dict) -> list:
    """Every declared ground joint must sit on what it says it stands on.

    A character stands on contacts that belong to other parts — feet, wheels —
    and the plane is checked against them. A prop and a scene band stand on
    themselves: the sole declared contact is the plane joint, so comparing the
    two would be comparing a number with itself. Those are checked against the
    emitted alpha instead, because a part resting on its own footprint rests on
    its last opaque row, and a resting point anywhere else is wrong.

    Returns one row per declaration for the build log.
    """
    rows = []
    for character, group in doc["rig"].items():
        records, solved = rig_eval.frames_of(doc, character)
        for entry in group["ground"]:
            plane = rig_eval.joint_point(records, solved, entry["part"], entry["joint"])
            if entry["contacts"] == [f"{entry['part']}/{entry['joint']}"]:
                alpha = np.asarray(
                    images[(character, entry["part"])].getchannel("A")) > 8
                base = float(np.nonzero(alpha.any(axis=1))[0].max())
                declared = float(records[entry["part"]]["joints"][entry["joint"]][1])
                worst = abs(declared - base)
                if worst > GROUND_TOLERANCE:
                    raise SystemExit(
                        f"{character}/{entry['part']}: this part is its own only "
                        f"contact, so its resting point is its footprint. The "
                        f"declared '{entry['joint']}' joint is at row {declared:.2f} "
                        f"but the last opaque row of the emitted image is {base:.0f}, "
                        f"{worst:.2f} px away (tolerance {GROUND_TOLERANCE} px)."
                    )
                rows.append((character, entry["part"], plane[1], worst, "footprint"))
                continue
            worst = 0.0
            for ref in entry["contacts"]:
                layer, joint = ref.split("/")
                point = rig_eval.joint_point(records, solved, layer, joint)
                worst = max(worst, abs(point[1] - plane[1]))
            if worst > GROUND_TOLERANCE:
                raise SystemExit(
                    f"{character}/{entry['part']}: the declared ground plane is "
                    f"{plane[1]:.2f} in character space, but a contact in "
                    f"{entry['contacts']} misses it by {worst:.2f} px "
                    f"(tolerance {GROUND_TOLERANCE} px). Derive `ground` from the "
                    "contact joints, not from the silhouette."
                )
            rows.append((character, entry["part"], plane[1], worst, "contacts"))
    return rows


def placed_mask(image: Image.Image, record: dict, angle: float,
                pivot_char: tuple) -> tuple:
    """A part's opaque mask and its top-left in character space, after rotation."""
    alpha = image.getchannel("A")
    pivot = record["pivot"]
    if angle:
        out = alpha.rotate(angle, expand=True, resample=Image.BICUBIC)
        centre = ((alpha.width - 1) / 2, (alpha.height - 1) / 2)
        moved = rig_eval.rotate_point(pivot, centre, angle)
        anchor = (moved[0] - centre[0] + (out.width - 1) / 2,
                  moved[1] - centre[1] + (out.height - 1) / 2)
    else:
        out, anchor = alpha, (float(pivot[0]), float(pivot[1]))
    return (np.asarray(out) > 8,
            int(round(pivot_char[0] - anchor[0])), int(round(pivot_char[1] - anchor[1])))


def check_draw_order(doc: dict, images: dict, poses: list) -> int:
    """`z` must decide the order of any two parts that can be seen at once.

    Two parts share a `z` only when they can never be composited over each other:
    either they are alternates in the same slot, so one is posed at a time, or
    their opaque pixels do not meet in character space. Anything else leaves the
    result up to whichever order the consumer happens to iterate in.

    A pair that misses at rest can meet once the rig moves, so this runs over
    every recorded pose rather than over rest alone. It places a part rigidly, so
    a meshed part sharing a `z` is refused outright: this check could not decide
    the overlap of a deformed silhouette, and a check that cannot decide must not
    pass.
    """
    checked = 0
    for pose in poses:
        for character, group in doc["rig"].items():
            records, frames, _ = rig_eval.solve_pose(
                doc, character, **rig_eval.pose_slice(pose, character))
            exclusive = {frozenset(slot["members"]) for slot in group["slots"].values()}
            by_z: dict[int, list] = {}
            for layer, record in records.items():
                by_z.setdefault(record["z"], []).append(layer)
            cache: dict[str, tuple] = {}
            for z, layers in sorted(by_z.items()):
                for i, a in enumerate(sorted(layers)):
                    for b in sorted(layers)[i + 1:]:
                        if any({a, b} <= members for members in exclusive):
                            continue
                        checked += 1
                        for layer in (a, b):
                            if records[layer]["mesh"] is not None:
                                raise SystemExit(
                                    f"{character}/{layer} carries a mesh and shares "
                                    f"z={z}. This check places a part rigidly, so it "
                                    "cannot decide whether a deformed silhouette "
                                    "overlaps. Give the meshed part a distinct z."
                                )
                            if layer not in cache:
                                angle, pivot_char, _ = frames[layer]
                                cache[layer] = placed_mask(
                                    images[(character, layer)], records[layer],
                                    angle, pivot_char)
                        (ma, ax, ay), (mb, bx, by) = cache[a], cache[b]
                        overlap = _overlap(ma, ax, ay, mb, bx, by)
                        if overlap:
                            raise SystemExit(
                                f"{character}: under pose '{pose['name']}', {a} and "
                                f"{b} both declare z={z} and their opaque pixels "
                                f"overlap by {overlap} px in character space, so "
                                "their order is undefined. Give one a distinct z."
                            )
    return checked


def _overlap(ma, ax, ay, mb, bx, by) -> int:
    """Opaque pixels shared by two placed masks."""
    x0, y0 = max(ax, bx), max(ay, by)
    x1 = min(ax + ma.shape[1], bx + mb.shape[1])
    y1 = min(ay + ma.shape[0], by + mb.shape[0])
    if x1 <= x0 or y1 <= y0:
        return 0
    sa = ma[y0 - ay:y1 - ay, x0 - ax:x1 - ax]
    sb = mb[y0 - by:y1 - by, x0 - bx:x1 - bx]
    return int(np.count_nonzero(sa & sb))


# The named poses in this fixture. Angles are degrees, counter-clockwise on
# screen, exactly as `rest_angle`. `root` moves a group's origin in character
# space and `root_angle` turns it about that origin; the ground plane does not
# move with either, because the floor belongs to the shot and not to the
# character. Each biped takes the same angles because their limbs are
# vertex-identical, which makes their deformed vertices comparable.
BIPED_STEP = {
    "hip_right": 22.0, "knee_right": -30.0,
    "shoulder_left": -28.0, "elbow_left": 20.0,
    "shoulder_right": 16.0, "elbow_right": -12.0,
}
MOCHI_STEP = {
    "shoulder_fore_right": 18.0, "knee_fore_right": -26.0,
    "hip_hind_left": -16.0, "knee_hind_left": 22.0,
    "rump": -20.0, "tail_mid": -24.0, "tail_end": -28.0,
}
REST_POSE = {
    "name": "rest",
    "note": ("Every bone at 0, no root placement. Deformed vertices equal the rest "
             "positions exactly; the build refuses if skinning moves anything."),
    "angles": {},
    "root": {},
    "root_angle": {},
    "planted": {},
}
REFERENCE_POSE = {
    "name": "step",
    "note": (
        "One leg planted, the opposite leg lifted and bent, arms swinging in "
        "opposition. Every bone not named is at 0. The bipeds keep their left leg "
        "at 0 and mochi keeps its fore left and hind right legs at 0, so those "
        "contacts stay on the declared ground plane while the rest of the rig "
        "deforms. The planted chains are at rest here, so this pose shows the "
        "floor is not moved by a limb that is not deforming; `plant` is the pose "
        "that puts a deforming chain under a planted foot."
    ),
    "angles": {c.name: dict(BIPED_STEP) for c in CAST} | {"mochi": dict(MOCHI_STEP)},
    "root": {},
    "root_angle": {},
    "planted": {c.name: ["leg_left_lower/contact"] for c in CAST}
    | {"mochi": ["leg_fore_left/contact", "leg_hind_right/contact"]},
}

# The planted chain itself deforms here, and the root drops by the amount that
# brings the contact back to the plane. Those drops are recorded numbers, not
# solved ones: the build reads them and measures where the contact lands, so an
# evaluator that skins, translates or anchors differently misses the plane and
# the build refuses. Every root also travels in x, the cart tilts and the ball
# rolls, which is what gives the two constraint kinds something to refuse.
BIPED_PLANT = {
    "hip_left": 20.0, "knee_left": 40.0,
    "hip_right": -30.0, "knee_right": 34.0,
    "shoulder_left": 24.0, "elbow_left": -20.0,
    "shoulder_right": -22.0, "elbow_right": 28.0,
}
MOCHI_PLANT = {
    "shoulder_fore_left": -12.0, "knee_fore_left": -28.0,
    "shoulder_fore_right": 10.0, "knee_fore_right": -14.0,
    "hip_hind_left": 18.0, "knee_hind_left": -24.0,
    "rump": 16.0, "tail_mid": 20.0, "tail_end": 24.0,
}
PLANT_POSE = {
    "name": "plant",
    "note": (
        "Weight on the planted leg. Each biped bends the left hip and knee it "
        "stands on and drops its root 8.27 px so the left contact lands back on "
        "the declared plane; mochi does the same on its fore left leg with a "
        "14.31 px drop. The planted contact is carried by a chain that is "
        "deforming, so 'deformation must not move the floor' is measured on a "
        "limb that is actually moving. Every group also travels 10 to 18 px in x, "
        "the cart tilts 5 degrees and the ball rolls 34 degrees: a ground "
        "projected shadow must take that x, hold its y on the plane the body left, "
        "and not tilt with the cart, and the light locked highlight must travel "
        "with the ball without turning."
    ),
    "angles": {c.name: dict(BIPED_PLANT) for c in CAST} | {"mochi": dict(MOCHI_PLANT)},
    "root": {c.name: [10.0, 8.27] for c in CAST}
    | {"mochi": [10.0, 14.31], "cart": [18.0, 0.0], "props": [12.0, 0.0]},
    "root_angle": {"cart": -5.0, "props": 34.0},
    "planted": {c.name: ["leg_left_lower/contact"] for c in CAST}
    | {"mochi": ["leg_fore_left/contact"]},
}
RECORDED_POSES = [REST_POSE, REFERENCE_POSE, PLANT_POSE]


def check_meshes(doc: dict) -> int:
    """A mesh must be internally consistent before anything is skinned with it."""
    count = 0
    for record in doc["parts"]:
        mesh = record["mesh"]
        if mesh is None:
            continue
        count += 1
        who = f"{record['character']}/{record['layer']}"
        w, h = record["size"]
        bones = {b["name"] for b in doc["rig"][record["character"]]["bones"]}
        unknown = [b for b in mesh["bones"] if b not in bones]
        if unknown:
            raise SystemExit(f"{who}: mesh binds to bones that do not exist: {unknown}")
        n = len(mesh["vertices"])
        if len(mesh["uv"]) != n or len(mesh["weights"]) != n:
            raise SystemExit(f"{who}: vertices, uv and weights disagree in length.")
        for i, ((x, y), (u, v), weights) in enumerate(
                zip(mesh["vertices"], mesh["uv"], mesh["weights"])):
            if not (0.0 <= x <= w and 0.0 <= y <= h):
                raise SystemExit(f"{who}: vertex {i} at ({x}, {y}) leaves the part.")
            if abs(u - x / w) > 1e-4 or abs(v - y / h) > 1e-4:
                raise SystemExit(f"{who}: uv {i} is not the vertex over the part size.")
            if len(weights) != len(mesh["bones"]) or abs(sum(weights) - 1.0) > 1e-6:
                raise SystemExit(f"{who}: weights at vertex {i} do not sum to 1.")
        for tri in mesh["triangles"]:
            if len(tri) != 3 or any(not 0 <= i < n for i in tri):
                raise SystemExit(f"{who}: triangle {tri} is out of range.")
    return count


PROBE_ANGLE = 30.0


def check_skinning(doc: dict) -> int:
    """Skinning must reproduce a rotation constructed without the skinning code.

    Posing one bone at a time and comparing the result against `rotate_point`
    about that bone's own head, blended by the same weights, shares no transform
    algebra, no composition and no traversal with the evaluator. It fails on a
    head resolved in the wrong space, a chain composed in the wrong order, a
    rotation taken the wrong way round, or a descendant that does not follow its
    parent. Rest is the same comparison at 0 degrees, so 'rest is the identity'
    is a case of a check that can fail rather than a restatement of
    `rot_about(head, 0)`.

    A joint on a meshed part is checked here too: read off the mesh at rest it
    must land where reading it rigidly lands, or every deformed contact in the
    manifest is measured from the wrong place.
    """
    checked = 0
    for character, group in doc["rig"].items():
        bones = group.get("bones", [])
        if not bones:
            continue
        records, solved = rig_eval.frames_of(doc, character)
        children: dict[str | None, list] = {}
        heads: dict[str, tuple] = {}
        for bone in bones:
            children.setdefault(bone["parent"], []).append(bone["name"])
            layer, joint = bone["head"].split("/")
            heads[bone["name"]] = rig_eval.joint_point(records, solved, layer, joint)
        meshed = {layer: r for layer, r in records.items() if r["mesh"]}
        rest_of = {layer: rig_eval.rest_vertices(records, solved, layer)
                   for layer in meshed}

        for layer, record in meshed.items():
            for joint, point in record["joints"].items():
                rigid = rig_eval.joint_point(records, solved, layer, joint)
                on_mesh = rig_eval.deform_point(record["mesh"], rest_of[layer],
                                                rest_of[layer], point)
                if math.dist(rigid, on_mesh) > 1e-9:
                    raise SystemExit(
                        f"{character}/{layer}: joint '{joint}' is at {rigid} rigidly "
                        f"but {on_mesh} on its own mesh at rest. A joint on a meshed "
                        "part must be a point on that mesh."
                    )

        for bone in bones:
            name = bone["name"]
            moved_by, stack = set(), [name]
            while stack:
                current = stack.pop()
                moved_by.add(current)
                stack.extend(children.get(current, []))
            for probe in (0.0, PROBE_ANGLE):
                transforms = rig_eval.bone_transforms(doc, character, {name: probe},
                                                      records, solved)
                for layer, record in meshed.items():
                    mesh = record["mesh"]
                    rest = rest_of[layer]
                    for vertex, weights, got in zip(rest, mesh["weights"],
                                                    rig_eval.skin(rest, mesh, transforms)):
                        turned = rig_eval.rotate_point(vertex, heads[name], probe)
                        want = [0.0, 0.0]
                        for weight, other in zip(weights, mesh["bones"]):
                            point = turned if other in moved_by else vertex
                            want[0] += weight * point[0]
                            want[1] += weight * point[1]
                        if math.dist(want, got) > 1e-9:
                            raise SystemExit(
                                f"{character}/{layer}: with only bone '{name}' at "
                                f"{probe} degrees, skinning puts a vertex at {got}, "
                                f"but rotating it about that bone's head puts it at "
                                f"{tuple(want)}."
                            )
                    checked += 1
    return checked


def without_constraints(doc: dict, character: str) -> dict:
    """The same group with every attachment inheriting its parent whole."""
    group = dict(doc["rig"][character])
    group["attach"] = {layer: dict(entry, constraint=None)
                       for layer, entry in group["attach"].items()}
    return dict(doc, rig=dict(doc["rig"], **{character: group}))


def check_constraints(doc: dict, poses: list) -> list:
    """Every declared constraint must be documented and must change a result.

    The manifest says a consumer that ignores a constraint renders the part
    wrongly. That is only true of this cast if some recorded pose separates the
    two, so each constrained part is solved twice — once as declared, once with
    the constraint stripped — and the build refuses unless a pose puts the two
    somewhere different. A constraint no pose distinguishes is decorative, and
    the manifest would be imposing a duty nothing here could catch a consumer
    shirking.
    """
    documented = doc["constraints"]["kinds"]
    rows = []
    for character, group in doc["rig"].items():
        constrained = {layer: entry for layer, entry in group["attach"].items()
                       if entry.get("constraint")}
        if not constrained:
            continue
        free_doc = without_constraints(doc, character)
        solved = [(rig_eval.solve_pose(doc, character,
                                       **rig_eval.pose_slice(pose, character))[1],
                   rig_eval.solve_pose(free_doc, character,
                                       **rig_eval.pose_slice(pose, character))[1],
                   pose["name"])
                  for pose in poses]
        for layer, entry in constrained.items():
            kind = entry["constraint"].get("kind")
            if kind not in documented:
                raise SystemExit(
                    f"{character}/{layer} carries constraint '{kind}', which "
                    "`constraints.kinds` does not define. A manifest that requires a "
                    "consumer to honour a constraint has to say what honouring it "
                    "means."
                )
            shown = [name for held, free, name in solved
                     if math.dist(held[layer][1], free[layer][1]) > 1e-9
                     or abs(held[layer][0] - free[layer][0]) > 1e-9]
            if not shown:
                raise SystemExit(
                    f"{character}/{layer} declares '{kind}', but every recorded pose "
                    "puts it exactly where plain inheritance would. Nothing here "
                    "separates a consumer that honours the constraint from one that "
                    "ignores it. Record a pose that does."
                )
            rows.append((f"{character}/{layer}", kind, shown))
    return rows


def check_deformation(doc: dict, pose: dict) -> dict:
    """Evaluate one pose, check it, and record what it produced.

    Three things have to hold, and each is a defect this fixture exists to catch:
    a contact joint must ride the deformed mesh; the two sides of the knee seam
    must land on the same points; and a planted foot must stay on its declared
    ground plane while everything else deforms and the root moves under it.
    """
    vertices, joints, seams = {}, {}, []
    for character in pose["angles"]:
        records, solved = rig_eval.frames_of(doc, character)
        _, _, meshes = rig_eval.solve_pose(doc, character,
                                           **rig_eval.pose_slice(pose, character))

        for layer, (rest, posed) in meshes.items():
            record = records[layer]
            mesh = record["mesh"]
            vertices[f"{character}/{layer}"] = [[round(x, 2), round(y, 2)]
                                                for x, y in posed]
            for joint, point in record["joints"].items():
                moved = rig_eval.deform_point(mesh, rest, posed, point)
                joints[f"{character}/{layer}/{joint}"] = [round(moved[0], 2),
                                                          round(moved[1], 2)]

        # The knee seam: the thigh's last rung and the shin's first rung are the
        # same two points, and must stay the same two points under the pose.
        for layer in meshes:
            if not layer.endswith("_upper"):
                continue
            lower = layer.replace("_upper", "_lower")
            top = meshes[lower][1][:2]
            bottom = meshes[layer][1][-2:]
            gap = max(math.dist(a, b) for a, b in zip(top, bottom))
            if gap > 1e-9:
                raise SystemExit(
                    f"{character}: the seam between {layer} and {lower} opens by "
                    f"{gap:.3g} px under pose '{pose['name']}'. The shared edge must "
                    "be the same points on both sides."
                )
            seams.append(f"{character}/{layer}|{lower}")

        # A planted contact must still be on the declared ground plane.
        entry = next(e for e in doc["rig"][character]["ground"] if e["part"] == "body")
        plane = rig_eval.joint_point(records, solved, entry["part"], entry["joint"])[1]
        for ref in pose["planted"][character]:
            moved = joints[f"{character}/{ref}"]
            if abs(moved[1] - plane) > GROUND_TOLERANCE:
                raise SystemExit(
                    f"{character}/{ref} is planted but pose '{pose['name']}' puts it "
                    f"at y={moved[1]}, {abs(moved[1] - plane):.2f} px off the declared "
                    f"ground plane y={plane}."
                )

    # The three bipeds share limb geometry exactly, so the same pose must give
    # them the same deformed vertices. If it does not, the topology is not shared.
    for c in CAST[1:]:
        for layer in ("arm_left", "leg_right_upper", "leg_right_lower"):
            a = vertices[f"{CAST[0].name}/{layer}"]
            b = [[round(x - 0.0, 2), round(y, 2)] for x, y in vertices[f"{c.name}/{layer}"]]
            if a != b:
                raise SystemExit(
                    f"{c.name}/{layer} does not deform identically to "
                    f"{CAST[0].name}/{layer}, so the shared topology claim is false."
                )

    return {"name": pose["name"], "note": pose["note"], "angles": pose["angles"],
            "root": pose["root"], "root_angle": pose["root_angle"],
            "planted": pose["planted"], "seams_checked": sorted(seams),
            "vertices": dict(sorted(vertices.items())),
            "joints": dict(sorted(joints.items()))}


def compact_json(doc: dict) -> str:
    """Pretty JSON, but with numeric leaf arrays kept on one line.

    A vertex over four lines is unreadable, and this manifest is meant to be read.
    Only innermost all-numeric arrays are collapsed, so structure is untouched.
    """
    def collapse(match: "re.Match") -> str:
        inner = match.group(0)[1:-1]
        if not re.fullmatch(r"[\s\-+0-9.eE,]*", inner):
            return match.group(0)
        return "[" + ", ".join(t for t in re.split(r"[\s,]+", inner) if t) + "]"

    return re.sub(r"\[[^\[\]]*\]", collapse, json.dumps(doc, indent=2)) + "\n"


def png_chunks(data: bytes) -> list:
    """Chunk types in a PNG, in file order."""
    out, i = [], 8
    while i + 8 <= len(data):
        length = int.from_bytes(data[i:i + 4], "big")
        out.append(data[i + 4:i + 8].decode("ascii", "replace"))
        i += 12 + length
    return out


def check_colour(doc: dict) -> dict:
    """The declared colour block must be true of the bytes on disk.

    Bit depth, channel layout and the absence of an embedded profile are read out
    of the PNG headers. Alpha association is decided by evidence, not assumption:
    under premultiplied alpha no channel can exceed the alpha it is multiplied
    by, so a single pixel where one does settles it.
    """
    colour = doc["colour"]
    witness = None
    for record in doc["parts"]:
        path = OUT / record["file"]
        data = path.read_bytes()
        depth, kind = data[24], data[25]
        if depth != colour["bit_depth"] or kind != 6:
            raise SystemExit(
                f"{record['file']}: PNG bit depth {depth}, colour type {kind}, but the "
                f"manifest declares {colour['bit_depth']}-bit RGBA (colour type 6)."
            )
        profiles = {c for c in png_chunks(data)} & {"iCCP", "sRGB", "gAMA", "cHRM"}
        if profiles:
            raise SystemExit(
                f"{record['file']} carries colour chunks {sorted(profiles)}; the "
                "manifest declares that no part embeds a profile."
            )
        if witness is None:
            a = np.asarray(Image.open(path).convert("RGBA"), dtype=np.int16)
            over = (a[..., 3] > 0) & (a[..., 3] < 255) & (a[..., :3].max(-1) > a[..., 3])
            if over.any():
                y, x = (int(np.nonzero(over)[0][0]), int(np.nonzero(over)[1][0]))
                px = a[y, x]
                witness = (f"{record['file']} at ({x}, {y}) is RGBA "
                           f"({px[0]}, {px[1]}, {px[2]}, {px[3]}); a premultiplied "
                           "pixel cannot carry a channel above its alpha")
    if witness is None:
        raise SystemExit(
            "No part carries a colour channel above its own alpha, so the cast "
            "supplies no evidence for the declared straight-alpha association."
        )
    colour["alpha_evidence"] = witness
    return colour


def check_blend(doc: dict) -> dict:
    """The blend profile must have something to test, in profile and out."""
    profile = set(doc["blend_profile"]["supported"])
    used = {p["blend_mode"] for p in doc["parts"]}
    missing = profile - used
    if missing:
        raise SystemExit(
            f"blend_profile declares {sorted(missing)} but no part uses "
            "them, so the profile is untestable. Either use each declared mode or "
            "stop declaring it."
        )
    out = sorted(f"{p['character']}/{p['layer']}" for p in doc["parts"]
                 if p["blend_mode"] not in profile)
    if not out:
        raise SystemExit(
            "No part declares a mode outside the profile, so the failure path "
            "'refuse rather than substitute normal' has no artifact."
        )
    if not any(p["opacity"] < 1.0 for p in doc["parts"]):
        raise SystemExit("No part carries opacity below 1.0.")
    # The out-of-profile part carries both a blend mode and reduced opacity, but a
    # consumer honouring the profile refuses it, so it cannot be what exercises
    # the order the two are applied in. Only a part a consumer must actually
    # composite counts here.
    both = sorted(f"{p['character']}/{p['layer']}" for p in doc["parts"]
                  if p["opacity"] < 1.0 and p["blend_mode"] != "normal"
                  and p["blend_mode"] in profile)
    if not both:
        raise SystemExit(
            "No part inside the blend profile carries both a non-normal blend mode "
            "and reduced opacity, so the order the two are applied in is not "
            "exercised by any part a consumer is required to draw."
        )
    return {"used": sorted(used), "out_of_profile": out, "blend_and_opacity": both}


def check_files(doc: dict) -> None:
    """Every part on disk is in the manifest and every manifest part is on disk."""
    declared = {(OUT / p["file"]).resolve() for p in doc["parts"]}
    on_disk = {p.resolve() for p in OUT.rglob("*.png")
               if not p.name.startswith("preview")}
    if declared != on_disk:
        missing = sorted(str(p.relative_to(OUT)) for p in declared - on_disk)
        extra = sorted(str(p.relative_to(OUT)) for p in on_disk - declared)
        raise SystemExit(
            "The manifest and the emitted files disagree.\n"
            f"  in the manifest, not on disk: {missing}\n"
            f"  on disk, not in the manifest: {extra}\n"
            "Delete fixtures/cast/ and rebuild."
        )


# How a set of parts is described in prose. Both the authored and the derived
# accounts are generated from `parts[].sources` through this table, so neither
# enumeration can drift from the parts the build emitted — hand-maintained
# enumerations are exactly what `sync_provenance` exists to stop.
PART_GROUPS = (
    ("ground shadows", lambda layer: layer.startswith("shadow")),
    ("hands", lambda layer: layer.startswith("hand_")),
    ("eyebrows", lambda layer: layer.startswith("eyebrow_")),
    ("eyes and gaze targets", lambda layer: layer.startswith("eye_")),
    ("mouth states and visemes", lambda layer: layer.startswith("mouth_")),
)


def enumerate_parts(parts: list) -> str:
    """Describe a set of parts: counted families first, then the rest by name."""
    counts = dict.fromkeys((label for label, _ in PART_GROUPS), 0)
    named = []
    for record in parts:
        for label, match in PART_GROUPS:
            if match(record["layer"]):
                counts[label] += 1
                break
        else:
            named.append(f"{record['character']}/{record['layer']}")
    items = [f"{counts[label]} {label}" for label, _ in PART_GROUPS if counts[label]]
    items += sorted(named)
    if len(items) == 1:
        return items[0]
    return ", ".join(items[:-1]) + " and " + items[-1]


def authored_note(doc: dict) -> str:
    """The generated account of the parts that derive from no source."""
    authored = [p for p in doc["parts"] if not p["sources"]]
    return (f"{len(authored)} parts are authored here: {enumerate_parts(authored)}. "
            "They are drawn by fixtures/tools/build_cast.py from primitives, derive "
            "from no source in this record, and need no source in this record to be "
            "redistributed.")


def derived_note(doc: dict) -> str:
    """The generated account of the parts that carry source pixels."""
    derived = [p for p in doc["parts"] if p["sources"]]
    kenney = [p for p in derived
              if any(s.startswith(f"{KENNEY}:") for s in p["sources"])]
    return (f"{len(derived)} parts carry source pixels. {len(kenney)} take their "
            f"geometry from a Kenney member: {enumerate_parts(kenney)}. The other "
            f"{len(derived) - len(kenney)} are shapes generated here, and are "
            "recorded as derived because texturise() adds the ambientCG Fabric034 "
            "weave to their pixels.")


def toolchain() -> dict:
    """The interpreter and libraries the committed bytes were encoded by."""
    return {
        "python": platform.python_version(),
        "numpy": np.__version__,
        "pillow": PIL.__version__,
        "why": (
            "The emitted PNG bytes depend on Pillow's PNG encoder defaults, its "
            "LANCZOS and BICUBIC resampling and its GaussianBlur, and on numpy's "
            "percentile. Two runs on this toolchain are byte-identical; another "
            "toolchain may encode different bytes, so 'the cast regenerates from "
            "the recorded archives' is a claim about this row and not about every "
            "Python. The build refuses on any other toolchain until this row is "
            "updated for it, which is the point at which the emitted bytes have to "
            "be re-reviewed. fixtures/tools/preview_cast.py encodes the two preview "
            "sheets with the same libraries and is covered by the same row."
        ),
    }


def check_readme(notes: list) -> None:
    """The README's account of the split is the generated one, or nothing ships.

    The prose in fixtures/README.md is the part of this record a reader meets
    first, and it is the part with no mechanism holding it to the data. These two
    sentences are generated from `parts[].sources`, so requiring them verbatim
    holds the README to the parts the build emitted.
    """
    text = README.read_text()
    missing = [note for note in notes if note not in text]
    if missing:
        raise SystemExit(
            "fixtures/README.md no longer carries the generated account of the "
            "authored and derived split. Paste these sentences into it verbatim:\n\n"
            + "\n\n".join(missing)
        )


def sync_provenance(record: dict, sources: Sources, doc: dict, update: bool) -> tuple:
    """Hold the licence record to what this build actually read.

    The `derives` lists, the part counts, the prose that describes them and the
    toolchain that encoded the bytes are all facts about the code, so they are
    generated from the code's own execution: which members it opened, which
    emitted parts their pixels reached, and what encoded them. A hand-maintained
    list drifts — that is how the biped eyebrows and `mochi/tail` came to be
    missing from it, and how the authored enumeration came to name limbs, hair,
    clothing and the quadruped that the manifest records as derived.
    """
    generated: dict[str, list] = {}
    for (key, member), use in sources.used.items():
        generated.setdefault(key, []).append({
            "member": member,
            "sha256": use["sha256"],
            "bytes": use["bytes"],
            "treatment": use["treatment"],
            "parts": sorted(use["parts"]),
        })
    authored = sorted(f"{p['character']}/{p['layer']}"
                      for p in doc["parts"] if not p["sources"])

    notes = [authored_note(doc), derived_note(doc)]
    stale = []
    for source in record["sources"]:
        want = sorted(generated.get(source["key"], []), key=lambda d: d["member"])
        if source.get("derives") != want:
            stale.append(f"sources[{source['key']}].derives")
            source["derives"] = want
    fields = {
        ("authored_here", "parts"): len(authored),
        ("authored_here", "note"): notes[0],
        ("derived", "parts"): len(doc["parts"]) - len(authored),
        ("derived", "note"): notes[1],
    }
    for (block, key), value in fields.items():
        if record[block].get(key) != value:
            stale.append(f"{block}.{key}")
            record[block][key] = value
    if record.get("toolchain") != toolchain():
        stale.append("toolchain")
        record["toolchain"] = toolchain()

    if stale:
        if not update:
            raise SystemExit(
                "fixtures/PROVENANCE.json no longer describes what this build reads: "
                + ", ".join(stale) + ".\nRun `python3 fixtures/tools/build_cast.py "
                "--update-provenance` and review the diff."
            )
        PROVENANCE.write_text(json.dumps(record, indent=2) + "\n")
        print(f"provenance updated: {', '.join(stale)}")
    return len(authored), notes


def main() -> None:
    ap = argparse.ArgumentParser(description="Build the RigTale reference cast.")
    ap.add_argument("--update-provenance", action="store_true",
                    help="rewrite the generated sections of fixtures/PROVENANCE.json "
                         "from what this build actually read")
    args = ap.parse_args()

    global SOURCES
    if not PROVENANCE.exists():
        raise SystemExit(f"Missing provenance record at {PROVENANCE}.")
    record = json.loads(PROVENANCE.read_text())
    SOURCES = Sources(record, update=args.update_provenance)
    SOURCES.verify()

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
        "draw_order": {
            "scope": "character group",
            "note": (
                "`z` orders parts within one character group and says nothing across "
                "groups: `pim/body` and `cart/body` both sit at z 10 and never compete, "
                "because a shot decides which group is in front. Inside a group, `z` is "
                "unique per part except where two parts can never be composited over "
                "each other — alternates in one slot, of which exactly one is posed, and "
                "parts whose opaque pixels do not meet in character space. "
                "`build_cast.py` proves the exception rather than asserting it: under "
                "every pose in `poses`, every pair sharing a `z` is rasterised in "
                "character space and refused if it overlaps by a single pixel. A pair "
                "that misses at rest can meet once the rig moves, so rest alone would "
                "not settle it. That check places a part rigidly and therefore refuses "
                "any meshed part that shares a `z`, because it could not decide the "
                "overlap of a deformed silhouette."
            ),
        },
        "constraints": {
            "note": (
                "`attach.constraint` is null when a part inherits its parent's "
                "transform whole. A non-null constraint restricts that inheritance, and "
                "a consumer that ignores it renders the part wrongly. `rig.py` "
                "implements both kinds below, and the build refuses to ship a "
                "constraint that no recorded pose separates from plain inheritance: "
                "`poses.plant` moves and turns the roots the constrained parts hang "
                "off, so honouring a constraint and ignoring it give different answers "
                "there."
            ),
            "kinds": {
                "ground_projected": (
                    "The part takes the parent's x translation only. Its y stays on the "
                    "character's ground plane and its angle stays fixed in character "
                    "space, so a body that leans, turns or leaves the floor neither "
                    "rotates nor lifts its shadow. Carried by every ground shadow. "
                    "Under `poses.plant` each biped root drops 8.27 px and travels "
                    "10 px: the shadow takes the 10 and stays on the plane, and the "
                    "cart's shadow keeps its angle while the cart tilts 5 degrees."
                ),
                "light_locked": (
                    "The part takes the parent's x and y translation and none of its "
                    "rotation, because it belongs to the key light rather than to the "
                    "surface under it. Carried by props/ball_highlight: a specular sits "
                    "where the light puts it, so it travels with the ball and does not "
                    "turn with it. Under `poses.plant` the ball rolls 34 degrees and "
                    "travels 12 px, and the highlight takes the 12 px only."
                ),
            },
        },
        "ground": {
            "note": (
                "`rig.<group>.ground` lists, per root, the joint that is that root's "
                "floor plane and the contact joints standing on it. Place a group by "
                "putting that joint on the shot's floor line and every character in the "
                "cast stands on the same floor. A character stands on contacts that "
                "belong to other parts — feet, wheels — and its plane is derived from "
                "them and not from its silhouette. A prop and a scene band stand on "
                "themselves: the plane joint is the sole contact, so there the plane is "
                "the part's own resting point, and the build holds it to the last "
                "opaque row of the emitted image rather than to itself. The plane does "
                "not move with a pose: `poses.<name>.root` moves the character, and the "
                "floor stays where the rest pose put it."
            ),
            "tolerance_px": GROUND_TOLERANCE,
            "tolerance_reason": (
                "Joints are written as whole pixels, so a contact solved in floating "
                "point can miss its plane by up to half a pixel. The build refuses any "
                "larger deviation."
            ),
        },
        "deformation": {
            "space": (
                "A mesh's `vertices` are in the part's own pixels, the same space as "
                "`pivot` and `joints`. The part's image occupies [0, size[0]] x "
                "[0, size[1]], and `uv` is the vertex divided by `size`."
            ),
            "triangles": (
                "Indices into `vertices`, wound v(r,c) -> v(r,c+1) -> v(r+1,c+1) and "
                "then v(r,c) -> v(r+1,c+1) -> v(r+1,c). With +y down that is clockwise "
                "on screen. No backface culling is implied."
            ),
            "bones": (
                "`rig.<group>.bones` is the deform skeleton. A bone is a rotation "
                "about its `head`, which is always an existing rig joint named "
                "`part/joint`, resolved to character space through the attachment "
                "tree. Rest is the identity: with every angle at 0 a skinned vertex "
                "sits exactly where the rigid rest pose puts it. On its own that is "
                "not evidence — a rotation of 0 about any point is the identity "
                "whatever the head is — so the build poses one bone at a time and "
                "compares the skinned vertices against that bone's head rotation "
                "applied directly and blended by the same weights, at 0 degrees and "
                "at 30. A wrong head, a chain composed in the wrong order, a rotation "
                "taken the wrong way round or a descendant that does not follow its "
                "parent fails that comparison."
            ),
            "weights": (
                "One rule covers every weight in this cast: a bone's weight ramps "
                "linearly from 0 at the previous bone's head to 1 at its own head, and "
                "stays 1 beyond it; the previous bone takes the remainder. `heads` on "
                "each mesh records those head positions along the strip, so a reviewer "
                "can recompute every weight from two numbers."
            ),
            "skinning": (
                "Linear blend skinning in character space. Solve the rest pose from "
                "`attach`, map each mesh vertex into character space with its part's "
                "rest transform, then take the weighted sum of the bone transforms "
                "applied to that rest position. A bone's transform is its parent's "
                "composed with a rotation about its own rest head."
            ),
            "joints_on_meshes": (
                "A joint on a meshed part is a point on the mesh, not a rigid offset "
                "from the pivot. Find the triangle that contains it in rest part "
                "space, take its barycentric coordinates there, and apply them to that "
                "triangle's deformed vertices. This is how a contact point on a "
                "deformed limb is computed, and how a rigid child — a hand on an arm's "
                "`tip` — finds its anchor: the anchor comes from the deformed mesh, "
                "and its rotation is the bone angles blended by the weights "
                "interpolated at that same point. At rest the rule reproduces the "
                "rigid position exactly, so the ground plane declared in "
                "`rig.<group>.ground` is unaffected; under a pose the contact moves "
                "with the geometry, and each pose's `joints` records where to."
            ),
            "topology": (
                "Limbs are two-rail strips, 6 to 14 triangles each. The three bipeds "
                "have identical body dimensions, so their arms and legs are not merely "
                "the same topology but the same vertices, and the build checks that "
                "every recorded pose deforms them identically."
            ),
            "seam": (
                "leg_<side>_upper and leg_<side>_lower meet along the knee: the "
                "thigh's flat bottom edge and the shin's flat top edge are the same "
                "two points in character space, carried by both meshes. A consumer "
                "that places the shin from the undeformed joint, or interpolates the "
                "two sides differently, opens a visible gap. The build measures the "
                "gap under every recorded pose and refuses anything but zero."
            ),
        },
        "colour": {
            "working_space": "sRGB IEC 61966-2-1, D65 white point",
            "transfer": (
                "sRGB transfer function. Every value in every part is non-linear, "
                "gamma-encoded sRGB; nothing here is linear light."
            ),
            "embedded_profile": (
                "none. No part PNG carries an iCCP, sRGB, gAMA or cHRM chunk, so the "
                "files themselves declare no space and this manifest is the "
                "declaration. Checked against the emitted bytes on every build."
            ),
            "alpha": "straight (unassociated)",
            "alpha_evidence": "filled in by the build from the emitted pixels",
            "blend_space": (
                "sRGB non-linear, the same encoding the parts are stored in. The "
                "generator composites its own decorations in that space, so a "
                "consumer that blends in linear light will not reproduce this cast."
            ),
            "bit_depth": 8,
            "channels": "RGBA, PNG colour type 6, 8 bits per channel, no palette",
            "boundary": (
                "This cast is a published pack, and production-contracts.md requires "
                "alpha association to be fixed at that boundary. It is fixed here as "
                "straight. A consumer that premultiplies for compositing does so after "
                "reading and must not write premultiplied values back into this pack: "
                "an 8-bit premultiply is lossy under low alpha, which is exactly where "
                "the shadows and the horizon haze live."
            ),
            "verification": (
                "Four of these fields are read back out of the emitted bytes on every "
                "build and the build refuses if they disagree: `bit_depth` and "
                "`channels` from every PNG header, `embedded_profile` from the chunk "
                "list of every PNG, and `alpha` from a pixel carrying a colour channel "
                "above its own alpha, which a premultiplied encoding could not hold. "
                "`working_space`, `transfer` and `blend_space` are declarations and "
                "cannot be checked here: a PNG with no profile carries no byte that "
                "records them, which is why this manifest has to state them. They are "
                "true of how build_cast.py composited these pixels; nothing in the "
                "files themselves could refute a different claim."
            ),
            "part_override": (
                "A part record may carry its own `colour` object overriding any field "
                "here. No part does, so this header describes every part."
            ),
        },
        "blend_profile": {
            "default": "normal",
            "supported": ["normal", "multiply", "screen"],
            "formulas": (
                "W3C Compositing and Blending Level 1, separable blend functions, "
                "over unpremultiplied colour: normal B(Cb,Cs)=Cs, multiply "
                "B(Cb,Cs)=Cb*Cs, screen B(Cb,Cs)=Cb+Cs-Cb*Cs. A mode name is not a "
                "formula, so the profile names both."
            ),
            "composite_order": (
                "Opacity first, then blend. A part's alpha is multiplied by its "
                "`opacity`, and only then is the part blended with `blend_mode` and "
                "composited over the backdrop. This is the OpenRaster rule — a layer's "
                "alpha is multiplied by its opacity before blending, and a "
                "non-isolated group multiplies its opacity into its children — and it "
                "is what the shadows test: they carry multiply at opacity 0.8, so a "
                "consumer that blends first and attenuates afterwards lands on a "
                "different pixel."
            ),
            "note": (
                "Every part carries an explicit `blend_mode` and `opacity`. A consumer "
                "that cannot honour a part's declared mode must fail rather than "
                "silently substitute `normal`."
            ),
            "in_profile": {
                "multiply": ("every ground shadow at opacity 0.8, and "
                             "mochi/belly_shade, a deformed mesh, at 0.7"),
                "screen": "props/ball_highlight",
                "normal": "everything else",
            },
            "out_of_profile": {
                "parts": ["scene/haze"],
                "mode": "linear_light",
                "note": (
                    "Photoshop defines Linear Light and publishes no formula for it, "
                    "and no general-purpose 2D library screened implements it. The "
                    "part exists so the refusal path has an artifact: a consumer "
                    "honouring this profile must refuse scene/haze by name. "
                    "preview_cast.py excludes it from the contact sheet and names it "
                    "when it does; `--all` asks for it and the harness refuses."
                ),
            },
        },
        "rig": m.rig,
        "parts": sorted(m.parts, key=lambda r: (r["character"], r["z"], r["layer"])),
    }

    check_files(doc)
    colour = check_colour(doc)
    blend = check_blend(doc)
    meshes = check_meshes(doc)
    probes = check_skinning(doc)
    planes = check_ground(doc, m.images)
    pairs = check_draw_order(doc, m.images, RECORDED_POSES)
    held = check_constraints(doc, RECORDED_POSES)
    doc["poses"] = {
        "note": (
            "Angles are degrees, counter-clockwise on screen, the same convention as "
            "`rest_angle`. A bone absent from a pose is at 0. `root` moves a group's "
            "origin in character space and `root_angle` turns the group about that "
            "origin; both are absent from a pose that only bends bones, and neither "
            "moves the ground plane. `vertices` are the deformed positions in "
            "character space and `joints` are the deformed joints of every meshed "
            "part, both to two decimals, so a consumer can check its own evaluation "
            "against this one rather than only look at it."
        ),
        "rest": {k: REST_POSE[k] for k in ("name", "note", "angles")},
        "reference": check_deformation(doc, REFERENCE_POSE),
        "plant": check_deformation(doc, PLANT_POSE),
    }
    authored, notes = sync_provenance(record, SOURCES, doc, args.update_provenance)
    check_readme(notes)
    (OUT / "manifest.json").write_text(compact_json(doc))

    chars = sorted({r["character"] for r in m.parts})
    print(f"{len(m.parts)} parts across {len(chars)} groups: {', '.join(chars)}")
    print(f"sources: {len(SOURCES.used)} verified archive members read, "
          f"{len(m.parts) - authored} parts derived from them, {authored} authored here")
    print(f"colour: {colour['bit_depth']}-bit RGBA, {colour['alpha']}, "
          f"no embedded profile; evidence {colour['alpha_evidence']}")
    print(f"blend: modes used {blend['used']}, out of profile "
          f"{blend['out_of_profile']}, blend with opacity {blend['blend_and_opacity']}")
    print(f"deformation: {meshes} meshed parts, "
          f"{sum(len(r['mesh']['triangles']) for r in doc['parts'] if r['mesh'])} "
          f"triangles, seams checked {doc['poses']['reference']['seams_checked']}")
    print(f"skinning: {probes} single-bone probes agree with a rotation about the "
          "bone's own head")
    print(f"draw order: {pairs} shared-z pairs checked for overlap across "
          f"{len(RECORDED_POSES)} poses, none overlap")
    for character, part, plane, worst, kind in planes:
        print(f"ground: {character}/{part} plane y={plane:.2f}, "
              f"worst deviation {worst:.2f} px against its {kind}")
    for who, kind, shown in held:
        print(f"constraint: {who} '{kind}' differs from plain inheritance "
              f"under {shown}")
    print(f"toolchain: {', '.join(f'{k} {v}' for k, v in toolchain().items() if k != 'why')}")
    print(f"manifest: {OUT / 'manifest.json'}")


if __name__ == "__main__":
    main()
