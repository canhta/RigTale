# RigTale Fixtures

Versioned, redistributable fixture assets for `SPIKE-F001` (`RGT-S003`).

Everything here derives from the two CC0 sources recorded in `PROVENANCE.json` — Kenney Shape Characters and ambientCG Fabric034. Both are public domain dedications, so nothing here carries a downstream obligation. Nothing derives from the reference-read-only tier, and nothing derives from a video reference.

## Status

**Draft, not approved.** `RGT-S003` is active. `SPIKE-F001` requires a decision record approving the fixture version before comparative spikes may cite it, and that record does not exist yet. Until it does, these assets may be used for development and may not be cited as approval evidence.

## Layout

| Path | Contents |
|---|---|
| `PROVENANCE.json` | Tracked source provenance and licence evidence |
| `cast/` | Layered cutout parts, one PNG per rig layer |
| `cast/manifest.json` | Per-part draw order, size, pivot, joints, blend mode and opacity, plus the rig tree |
| `cast/preview.png` | Generated contact sheet, not an assertion |
| `tools/build_cast.py` | Regenerates `cast/` from the CC0 sources |
| `tools/preview_cast.py` | Poses the parts from the manifest alone, to show the rig data is sufficient |

## Regenerating

The CC0 sources are not vendored. Download the two archives named in `PROVENANCE.json` — each record carries its download URL, SHA-256 and byte size — into `.sandbox/downloads/`, then extract them so that:

- the Kenney part PNGs are at `.sandbox/assets/kenney-shape-characters/PNG/Double/`;
- the Fabric034 colour map is at `.sandbox/assets/fabric034/Fabric034_1K-JPG_Color.jpg`.

Those paths are where the build reads its inputs. They are not the fixture's provenance: the licence evidence is `PROVENANCE.json`, which is tracked in Git. `.sandbox/` is a Git-ignored working area whose rules are set out in `.sandbox/README.md`.

```
python3 fixtures/tools/build_cast.py
python3 fixtures/tools/preview_cast.py
```

The generator verifies every archive against the SHA-256 and byte size in `PROVENANCE.json` before it builds. A missing or mismatched source stops the build with an explicit message rather than producing a partial cast. Two runs produce byte-identical output.

## Cast

132 PNG files across seven groups, 349 KB, plus a 75 KB manifest.

| Group | Archetype | Files | Exercises |
|---|---|---|---|
| `pim`, `bo`, `nu` | biped | 34, 34, 36 | Three simultaneous instances with distinct silhouette, palette, hair and clothing |
| `mochi` | quadruped | 16 | Four-point ground contact, secondary motion on ears and tail |
| `cart` | vehicle | 5 | Wheel cycle against ground travel, character and prop attachment |
| `props` | prop | 3 | Handoff, attachment, beat-synchronised action |
| `scene` | environment | 4 | Parallax bands, draw order |

The three bipeds use three different base silhouettes: `pim` a squircle and `bo` a circle, both recoloured Kenney bases, and `nu` a generated cloud — the third shape in the spike's stated vocabulary, which the Kenney pack does not supply.

Every biped carries separated arms, legs, hands in three grips, eyes with three gaze targets, eyebrows, and twelve mouth states — four expressions plus eight visemes. Parts are separate because the fixture exists to exercise rigging; a flattened character would assert nothing.

### Files against unique images

The 132 files hold **78 unique images**. 54 files are byte-identical to another file, for two reasons:

- **Mirroring a symmetric shape is a no-op.** A capsule limb, a sphere pigtail, a circular wheel, eye and ear shapes are all left-right symmetric, so the left and right copies are identical bytes. This covers each biped's `arm_left`/`arm_right` and `leg_left`/`leg_right`, `nu`'s two pigtails, `mochi`'s four legs and its ears and eyes, and the cart's two wheels.
- **Faces are shared across the cast.** All three bipeds are 160×160, so their eyes, their twelve mouth states and their ground shadow come out at the same size in the same ink, and the files match.

The duplicates are kept rather than deduplicated: each character is a self-contained directory, so a consumer can edit or replace one character's parts without reaching into another's. Consumers that care about payload size should deduplicate on content hash at packaging time.

## Rig data

`cast/manifest.json` carries enough structure to place and parent every part without guessing. `tools/preview_cast.py` contains no joint offsets of its own; it reads all of them from the manifest, which is what demonstrates the data is sufficient.

- **Part space.** A part's `pivot` and each entry in its `joints` are pixels from that part's own top-left.
- **Character space.** A character's space is its root part's pivot, +x right, +y down, in pixels.
- **Attachment.** `rig.<character>.attach` gives every part a `parent`, the named `joint` on that parent it hangs from, and a `rest_angle`. A part is placed by putting its own pivot on that joint, then rotating counter-clockwise by `rest_angle`. A part's pivot is always its anchor, so there is no separate anchor field. `roots` lists the parts with no parent.
- **Slots.** `rig.<character>.slots` groups mutually exclusive alternates — the three hand grips, the three gaze targets per eye, the mouth states — and names the default. Exactly one member of a slot is posed at a time.
- **Draw order.** `z` is unique per part except within a slot and between non-overlapping left-right pairs.
- **Compositing.** Every part carries an explicit `blend_mode` and `opacity`. `blend_profile` at the top of the manifest declares the modes the fixture expects a consumer to support; a consumer that cannot honour a declared mode must fail rather than silently substitute `normal`.
- **Parallax.** `rig.scene.parallax` gives each environment band its depth factor, ordered with `z` from far to near.

Pivots name real joints. A limb's pivot is the centre of its top cap, so it rotates from the shoulder or hip; `mochi`'s head pivot is at the neck, not the skull centre, so a nod is a nod.

## Attribution and provenance

`PROVENANCE.json` is the record: per source, the source page, the final download URL, the retrieval date, the licence, the licence evidence, the archive SHA-256 and byte size, and which generated part groups derive from it.

Kenney Shape Characters ships a `License.txt` inside its archive that states the CC0 dedication verbatim. ambientCG Fabric034 ships no licence file, so its evidence is the source page.

Neither licence requires attribution. Both are credited because it is right, not because it is required.

## Originality

The characters are original compositions. Palette, hair, clothing patterns, limbs, eyes, mouth states, the cloud silhouette, the quadruped, the vehicle and the props were all authored here; Kenney supplies geometric bases and ambientCG supplies a texture.

**No visual identity is copied from any reference channel** — not shape, colour, hair, costume, or naming. Channels studied for art direction were used as visual reference only and supplied no asset. Local or non-commercial use does not by itself permit downloading or reusing video content: the [YouTube Terms of Service](https://www.youtube.com/static?template=terms) restrict it unless a service feature, the rights holder, or law permits it.

## What this fixture does not yet contain

The cast is `SPIKE-F001` method step 3. Still outstanding: the contract and failure corpus, diagnostic-shot manifests with expected evidence, the complete production brief and timeline, the calibration plan, and the approving decision record. `docs/quality/fixture-risk-matrix.md` lists the risks each of those must cover.
