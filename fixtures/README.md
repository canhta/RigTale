# RigTale Fixtures

Versioned, redistributable fixture assets for `SPIKE-F001` (`RGT-S003`).

Everything here is derived from CC0 sources and carries no downstream obligation. Nothing here came from the `.sandbox/` reference-read-only tier, and nothing here came from a video reference.

## Status

**Draft, not approved.** `RGT-S003` is active. `SPIKE-F001` requires a decision record approving the fixture version before comparative spikes may cite it, and that record does not exist yet. Until it does, these assets may be used for development and may not be cited as approval evidence.

## Layout

| Path | Contents |
|---|---|
| `cast/` | Layered cutout parts, one PNG per rig layer |
| `cast/manifest.json` | Per-part z-order, size, pivot, and note |
| `cast/preview.png` | Generated contact sheet, not an assertion |
| `tools/build_cast.py` | Regenerates `cast/` from CC0 sources |
| `tools/preview_cast.py` | Poses the parts to show they compose |

## Regenerating

The CC0 sources are not vendored. Fetch them into the ignored sandbox first — see `.sandbox/README.md` — then:

```
python3 fixtures/tools/build_cast.py
python3 fixtures/tools/preview_cast.py
```

The generator fails with an explicit message if the sources are absent rather than producing a partial cast.

## Cast

132 parts across seven groups, 562 KB.

| Group | Archetype | Parts | Exercises |
|---|---|---|---|
| `pim`, `bo`, `nu` | biped | 34–36 each | Three simultaneous instances with distinct silhouette, palette, hair and clothing |
| `mochi` | quadruped | 16 | Four-point ground contact, secondary motion on ears and tail |
| `cart` | vehicle | 5 | Wheel cycle against ground travel, character and prop attachment |
| `props` | prop | 3 | Handoff, attachment, beat-synchronised action |
| `scene` | environment | 4 | Parallax bands, draw order |

Every biped carries separated arms, legs, hands in three grips, eyes with three gaze targets, eyebrows, and twelve mouth states — four expressions plus eight visemes. Parts are separate because the fixture exists to exercise rigging; a flattened character would assert nothing.

Pivots are in pixels from each part's own top-left. Placement in character space is the rig's responsibility and is deliberately not baked in.

## Attribution and Provenance

| Source | Licence | Evidence | Used for |
|---|---|---|---|
| [Kenney Shape Characters](https://kenney.nl/assets/shape-characters) | CC0 1.0 | `License.txt` inside the archive: "License: (Creative Commons Zero, CC0)" | Body, hand, eyebrow and environment tile bases |
| [ambientCG Fabric034](https://ambientcg.com/view?id=Fabric034) | CC0 1.0 | Source page; the archive carries no licence file | Felt weave overlay |

Both are public domain dedications, so redistribution here is unrestricted. Attribution is given because it is right, not because it is required.

Retrieval dates, download URLs, and checksums are recorded in `.sandbox/provenance.local.json`.

## Originality

The characters are original compositions. Palette, hair, clothing patterns, limbs, eyes, mouth states, the quadruped, the vehicle and the props were all authored here; Kenney supplies geometric bases and ambientCG supplies a texture.

**No visual identity is copied from any reference channel** — not shape, colour, hair, costume, or naming. Channels studied for art direction were used as visual reference only and supplied no asset. `.sandbox/README.md` records why: local or non-commercial use does not by itself permit downloading or reusing video content.

## What This Fixture Does Not Yet Contain

The cast is `SPIKE-F001` method step 3. Still outstanding: the contract and failure corpus, diagnostic-shot manifests with expected evidence, the complete production brief and timeline, the calibration plan, and the approving decision record. `docs/quality/fixture-risk-matrix.md` lists the 31 risks each of those must cover.
