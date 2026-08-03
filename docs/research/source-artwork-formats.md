# Source-Artwork Format Screening and the Vector-versus-Raster Determination

**Screened under:** `RGT-S014`. Read-only. No candidate code, dependency, build, or setup script was executed. Repositories were cloned into the ignored `.research/clones/` workspace and read at pinned commits.

**All URLs accessed 2026-08-02.** Package-registry and repository facts were read on the same date.

This document closes defects 1 and 2 recorded in `docs/spikes/SPIKE-C001-competitive-landscape.md` lines 47–51. Defects 3, 4, and 5 are routed elsewhere in `TODO.md` and are out of scope here, except where evidence gathered for defects 1 and 2 bears on defect 4 (colour and alpha), which it does heavily and which is recorded rather than resolved.

## Evidence Rules Applied

Official specifications, vendor reference documentation, and repository source files at exact revisions are treated as primary evidence. Package-registry release records (npm, PyPI, crates.io) are treated as primary for release identity and date. Marketing pages, README positioning, star counts, download counts, and search-index summaries are discovery signals only and are labelled as such. Licences were read from the `LICENSE`/`COPYING` file, not from the GitHub badge, wherever the file was reachable. Where a fact could not be verified from a primary source it is recorded as **not verified** rather than inferred.

The GitHub REST API was rate-limited for this network during the round. Repository facts were therefore established by `git clone --depth 1` plus `git log`/`git ls-remote`, and by the package registries. Where only a tag exists and no dated release record was retrievable, the release *date* is recorded as not verified.

**No technology is selected here.** Every outcome is a screening disposition routed to `SPIKE-A002`, `SPIKE-R001`, or `RGT-D010`.

---

## Part 1 — Q1: Layered Source-Artwork Ingestion Formats

### 1.1 The criterion, applied to the read side

`PR-A003` requires ingestion of "at least one **documented** layered-artwork format" and, from `RGT-S001`, adds the gate: **a program can produce valid content without a graphical interface and without a proprietary tool.**

Applied to source artwork this splits into three independent questions that the round found are answered by *different* formats:

1. **Is it documented?** — is there a published specification a third party can implement from?
2. **Can a program write it headlessly?** — the `PR-A003` gate. RigTale needs this for fixtures, regression assets, round-trip tests, and any agent-generated or agent-repaired artwork.
3. **Is it what the target user actually hands over?** — the ingestion question. A format RigTale can write but nobody exports is a test fixture, not an ingestion path.

**The organising finding of this round: no single format answers all three.** OpenRaster answers 1 and 2 and fails 3. PSD answers 2 and 3 and answers 1 only partially, by a specification whose own text declines to define semantics. Everything the target segment actually paints in — `.procreate`, `.clip`, `.mdp`, `.sai2` — fails 1 and 2 outright and reaches RigTale only by being exported to PSD.

### 1.2 Comparison table

`PR-A003 write gate` = can a program write a valid file with no GUI and no proprietary tool.

| Format | Published spec | Container | Headless write | Layer tree | Blend modes | Masks | Adjustment layers | Text | Vector | ICC | Target users export it? |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **OpenRaster `.ora`** | Yes, v0.0.6, with a RelaxNG schema | ZIP + XML + PNG | **met** | yes (nested `stack`) | 21 `composite-op` values, defined by reference to W3C Compositing-1 | **no** | **no** (proposal only) | **no** (prose refers to a `text` element that does not exist in the schema) | not specified normatively | **no** (proposal only) | Krita, GIMP, MyPaint only |
| **Adobe PSD** | Yes, Nov 2019, self-declared partial | binary, big-endian, 5 sections | **met** (ag-psd, MIT) | yes | 28 blend keys | yes | yes | yes | yes | yes (resource 1039) | **yes — universally** |
| **Adobe PSB** | Same document | same, 64-bit lengths | **met** (ag-psd `psb: true`) | as PSD | as PSD | as PSD | as PSD | as PSD | as PSD | as PSD | Clip Studio, Photoshop, Storyboard Pro |
| **Krita `.kra`** | **None** | ZIP + XML + binary LZF tiles | **not met** — see §1.5 | yes | yes | yes (5 mask types) | yes | via shape layer | yes (`shapelayer`) | yes (`/annotations/icc`) | Krita only |
| **GIMP `.xcf`** | Yes, GPL-2.0+ text, explicitly non-normative | binary, pointer-linked | met, but only via GIMP itself or a partial third-party writer | yes | 62 `PROP_MODE` values | yes | yes (XCF 20+, GEGL ops) | yes (parasites) | yes (XCF 24+) | yes (`icc-profile` parasite) | GIMP only |
| **Procreate `.procreate`** | **None** | ZIP + NSKeyedArchive + LZO/LZ4 tiles | **not met** | yes (read only) | yes (read only) | yes (read only) | not verified | not verified | n/a | not verified | it is a *source* format; users export PSD |
| **Clip Studio `.clip`** | **None** | `CSFCHUNK` chunks + embedded SQLite | **not met** | yes (read only) | yes (read only) | not verified | not verified | yes (rasterised on export) | yes (rasterised or dropped on export) | not verified | it is a *source* format; users export PSD/PSB |
| **MediBang/FireAlpaca `.mdp`** | **None** | not verified | **not met** | not verified | not verified | not verified | not verified | not verified | not verified | not verified | source format; users export PSD |
| **PaintTool SAI `.sai` / `.sai2`** | **None** | v1: encrypted block filesystem. v2: chunked, 256×256 tiles | **not met** | yes (read only) | yes (read only) | not verified | not verified | yes (`text` layer type) | yes (`shap` layer type) | not verified | export set **not verified** from any vendor page |
| **Layered TIFF** | TIFF 6.0 published; the *layers* are a PSD blob in private tag 37724 | TIFF IFD wrapper | **not verified** — see §1.10 | inherits PSD | inherits PSD | inherits PSD | inherits PSD | inherits PSD | inherits PSD | yes | Photoshop, Affinity, Krita |
| **PNG / APNG** | Yes, W3C PNG 3rd ed., 24 June 2025 | chunked binary | met (trivially) | **no layer model at all** | n/a | n/a | n/a | n/a | n/a | yes (`iCCP`) | as a per-layer dump, yes |
| **SVG** | Yes, W3C SVG 2 CR, 4 Oct 2018 | XML text | met (trivially) | `<g>` groups; the word "layer" does not appear in the structure chapter | via CSS `mix-blend-mode` (W3C Compositing-1) | via `<mask>`/`<clipPath>` | filters | yes | native | via CSS colour | vector tools only |
| **Multi-part / multi-layer OpenEXR** | Yes, BSD-3 project docs | binary, multi-part | met (OpenEXR BSD-3, OpenImageIO Apache-2.0) | naming convention only | **none** — spec states the convention "does not describe a back-to-front stacking order or any compositing operations" | no | no | no | no | yes | Harmony multi-layer write, Blender |
| **Aseprite `.ase`/`.aseprite`** | Yes, in-repo, linked from official docs | binary, chunked, zlib | not verified | yes | yes | yes (tilemap/cel) | no | no | no | yes (chunk 0x2007) | pixel-art segment only |

### 1.3 OpenRaster (`.ora`)

**Specification.** `https://www.openraster.org/` — "Open Raster Specification version 0.0.6". Baseline is two documents: `https://www.openraster.org/baseline/file-layout-spec.html` and `https://www.openraster.org/baseline/layer-stack-spec.html`. Canonical source repository `https://invent.kde.org/documentation/openraster-org`, cloned at `e8ef488acf139d67a87f232f080b56dddcad4561` (2025-08-23). A canonical **RelaxNG schema** is published at `openraster-standard/schema.rnc` / `schema.rng` — that is a machine-checkable grammar for the layer stack, which is materially more than most candidate formats offer.

**Governance is weak and says so.** The spec repository's `README.md` records that the format moved from the freedesktop wiki to GitHub after LGM2016, and then "at LGM2018 BOF it appeared that the previous maintainer had dissapeared without giving anyone the ability to make commits. It is therefore moved under the KDE umbrella", followed by "We are yet to decide upon protocols for submitting changes." The older freedesktop wiki page is still live and still labels itself "**Draft Specification**". Version 0.0.6 after roughly twenty years is itself the maintenance signal.

**Container, verbatim from the file-layout spec.** ZIP wrapper; "The first file in the archive must be called `mimetype`, without a file name extension. It must be STORED without compression" and must contain exactly `image/openraster`. Required members: `stack.xml` (UTF-8), `Thumbnails/thumbnail.png` (non-interlaced, 8 bpc, ≤256×256), and `mergedimage.png` (8 or 16 bpc, mandatory since 0.0.2). "Only DEFLATED and STORED should be used." Layer data lives at paths referenced from `stack.xml`, e.g. `data/layer2.png`.

**What the baseline preserves.** The entire schema vocabulary is three elements — `image`, `stack`, `layer` — with `name`, `opacity` (float 0.0–1.0, "multiplied by this opacity before blending"), `visibility`, `composite-op`, `isolation`, `x`, `y`, `src`. Twenty-one `composite-op` values, each defined as a W3C Compositing-1 blend function plus a Porter-Duff operator, with `svg:src-over` the default. Group isolation is explicit: isolated groups render "starting with a fully-transparent 'black' backdrop (rgba={0,0,0,0})"; non-isolated groups ignore their own `composite-op` and multiply opacity into children.

**What the baseline does not have — and this is the finding.** No masks. No clipping. No adjustment or filter layers (the spec's own example carries the comment "filters are syntactically permissible, but not valid for baseline"). No text element in the schema, although the prose says stacks "may contain sub-stacks, layers, or text elements" — a spec inconsistency. **No colour profile:** ICC is a *proposal* at `https://www.openraster.org/proposals/png-data-requirements.html`, not baseline. **Alpha semantics are never stated**; layer data is PNG, and W3C PNG 3rd edition states "The color values in a pixel are not premultiplied by the alpha value assigned to the pixel", so straight alpha is implied by the payload format and not by ORA.

**`PR-A003` write gate: MET, and by the widest margin of any candidate.** The container is a ZIP, the manifest is XML with a published grammar, and the payload is PNG. Any language with a zip library, an XML writer, and a PNG encoder can produce a valid file with nothing installed. Verified writers:

- **pyora** — `https://gitlab.com/inklabapp/pyora`, MIT (`LICENSE`, "Copyright (c) 2019 Paul Jewell"), PyPI 0.3.11 uploaded 2021-03-19, clone `54e16cbea6d0a5ef4a50b429f98c1e03489493d9` (2021-03-18). Writer at `pyora/Project.py:358`. **Unmaintained for five years, and non-conformant in two visible ways**: it declares `ORA_VERSION = "0.0.1"` (`pyora/__init__.py:3`) and emits `src` values with a leading slash — `f'/data/layer{n}.png'` (`Project.py:392`) — where the spec specifies root-relative paths of the form `data/layer2.png`.
- **MyPaint** — `https://github.com/mypaint/mypaint`, GPL-2.0-or-later, clone `35aa9d33cd3deba6cafea6d8fc901b5a1d161ceb` (2026-01-19). `lib/document.py:1770 def save_ora(...)`, ZIP assembly at `:2090-2160`, and `lib/xml.py:23 OPENRASTER_VERSION = "0.0.5"`. Copyleft — readable as a reference, not linkable under `PR-P005` until the distribution model is decided.
- **Krita** and **GIMP** both write it; both are copyleft applications, not libraries.
- **No Rust, Go, or maintained C library was found.** A crates.io search returned only `file-format`, which performs format *detection*. Recorded as not verified rather than absent.

**Every writer degrades the file, verified in source.** GIMP's `plug-ins/python/file-openraster.py` maps roughly sixteen GIMP modes to real `svg:*` values and **collapses thirty-plus others — Dissolve, Divide, Subtract, Grain extract/merge, the LCH modes, Vivid/Pin/Linear light, Hard mix, Exclusion, Linear burn, Luminance, Pass-through — to `svg:src-over`**, with an in-source `# FIXME Determine the closest available layer mode`. Krita's `plugins/impex/ora/kis_open_raster_stack_save_visitor.cpp` writes unmapped ops as `"krita:" + compositeOpId` (non-portable), smuggles alpha-lock as `svg:src-atop` or a non-baseline `alpha-preserve` attribute, writes adjustment layers as a `<filter type="applications:krita:NAME">` element **with no data payload**, rasterises clone/generator/vector layers through `layer->projection()`, never visits masks at all (they are baked into the projection), and declares `<image version="0.0.1">`.

**Licensing.** The spec repository contains **no LICENSE file**; the website footer is a bare `©2018, create@lists.freedesktop.org` with no grant. Implementing the format is unaffected — file formats are not copyrightable — but **redistributing the spec text has no verified licence**. Recorded for `PR-P005`.

**Who exports it.** `openraster.org` states "Applications that support OpenRaster are Krita, GIMP, MyPaint and Scribus." MyPaint's `gui/filehandling.py:593` shows `ext2saveformat` limited to `.ora`, `.png`, `.jpeg`, `.jpg` — **ORA is MyPaint's only layered format; it has no native format of its own.** Krita's own manual calls ORA "an interchange format… designed to replace \*.psd as an interchange format" (`https://docs.krita.org/en/general_concepts/file_formats/file_ora.html`). **No rigging or animation tool screened in §1.12 accepts ORA.**

**Disposition: `adopt` as RigTale's fixture and round-trip authoring format; `reject` as the primary user ingestion path.**

### 1.4 Adobe PSD and PSB

**Specification: published, and the repository's prior characterisation of it is wrong.** `https://www.adobe.com/devnet-apps/photoshop/fileformatashtml/` returns HTTP 200 and is titled "Adobe Photoshop File Formats Specification — November 2019". It states its purpose verbatim: "This document is provided for 3rd parties to read and write the Photoshop native file format." It covers **both PSD and PSB** in one document.

**But the specification defines syntax and explicitly declines to define semantics.** Verbatim: "**This document does not explain how to interpret the data. This document describes the format of the data only.**" It also excludes the Photoshop Cloud Document format ("That format, at this time, is private"), leaves duotone undocumented ("the format of which is not documented"), marks the global layer mask overlay colour space "(undocumented)", marks the `'shmd'` metadata block "Variable — Undocumented data", and carries nine "Obsolete" markers. Its licence line is "The information in this document is furnished for informational use only, is subject to change without notice" — **no open licence grant, and no explicit patent or implementation grant.**

**The practical consequence is the single most important technical fact in this document: Photoshop's blend-mode formulas are not published anywhere.** The spec lists 28 four-character blend keys — extracted directly from the specification page: `norm mul  scrn diss over dark lite hLit sLit diff smud div  idiv lbrn lddg vLit lLit pLit hMix dkCl lgCl fsub fdiv hue  sat  colr lum  pass`. W3C Compositing and Blending Level 1 (`https://www.w3.org/TR/compositing-1/`, Candidate Recommendation Draft, 21 March 2024) defines **sixteen**: twelve separable plus four non-separable. The difference is twelve keys, of which **eleven are blend modes with no W3C or PDF definition at all** — dissolve, linear burn, darker colour, linear dodge, lighter colour, vivid light, linear light, pin light, hard mix, subtract and divide. The twelfth, `pass`, is a group pass-through rather than a blend mode. The key-to-name mapping is read from two independent readers that agree: `ag-psd/src/helpers.ts:9-35` and `psd-tools/src/psd_tools/constants.py`. Note in particular that `smud` is **exclusion**, which W3C does define, and `div`/`idiv` are colour dodge and colour burn — so the difference is not obtainable by eye from the four-character keys. See §2.4 for what this does to the renderer question.

**Container.** Binary, big-endian ("All data is stored in big endian byte order"). Five sections: File Header (`'8BPS'`, version 1 for PSD and "**PSB** version is 2", width/height limit "1 to 30,000. (**PSB** max of 300,000.)"), Color Mode Data, Image Resources (ID 1039 = raw ICC profile bytes), Layer and Mask Information (PSB uses 8-byte lengths and the `'Lr16'`/`'Lr32'` keys), and the flattened composite Image Data. Layer records carry a 1-byte opacity, a 1-byte clipping flag, visibility and transparency-protection flags, mask data, blending ranges, name, and keyed Additional Layer Information blocks.

**`PR-A003` write gate: MET.** The only actively released library verified to both read and write is:

- **ag-psd** — `https://github.com/Agamnentzar/ag-psd`, MIT (`LICENSE` read: "The MIT License (MIT) … Copyright (c) 2016 Agamnentzar"), npm `31.0.2` published 2026-07-02, clone `387049670cb89b88fb8fe1b7c01aeacf98dd2e3b` (2026-07-02). Write API at `src/index.ts:29,35,41` — `writePsd`, `writePsdUint8Array`, `writePsdBuffer`. **PSB is written via `WriteOptions.psb` (`src/psd.ts:1859-1860`, "Saves document as PSB (Large Document Format) file"), with the version word set at `src/psdWriter.ts:260`.** Note that `README.md:15` still claims "Does not support The Large Document Format (8BPB/PSB)" — that line is stale and is contradicted by the project's own `CHANGELOG.md` v12.1.0 entry and by the code; the library is at v31.

  **Headless operation is confirmed by reading the source, not the README.** `src/helpers.ts:385-386` makes `createCanvas` throw unless `initializeCanvas` is called, and `README.md:73` says node-canvas is needed "to read image data and thumbnails". But layer pixels can be supplied as raw `imageData` (`Layer.imageData?: PixelData`, `src/psd.ts:1774`), the writer consumes it directly (`src/psdWriter.ts:211,245`), and the only canvas call on the write path is inside thumbnail generation (`src/psdWriter.ts:585-607`). **With `imageData` and no `generateThumbnail`, ag-psd writes PSD and PSB in plain Node with no canvas, no display, and no Adobe software.**

  Structure it can write, from `src/psd.ts` and the handler tables in `src/additionalInfo.ts`: layer tree and groups (`children`, `'lsct'`), opacity (`opacity`, `'iOpa'`), the full 28-value `BlendMode` union (`src/psd.ts:1-5`), raster masks (`mask`, `realMask`, `'LMsk'`), clipping (`clipping`), adjustment layers (`adjustment`, with handlers for `'brit' 'levl' 'curv' 'expA' 'vibA' 'hue2' 'blnc' 'blwh' 'phfl' 'mixr' 'clrL' 'nvrt' 'post' 'thrs' 'grdm' 'selc' 'CgEd'`), vector fill/stroke/mask, layer effects, and ICC **as an opaque pass-through blob** (`src/imageResources.ts:1229-1237` — read and written as bytes; the library will not construct a profile).

  **Write-side limits, from the README and enforced in the writer: 8 bits per channel only, RGB colour mode only, text layers incomplete** ("files with updated/written text layers will result in a warning prompt when opening the file in Photoshop"), and the library does not regenerate the composite or the thumbnail when layers change.

  **Alpha semantics, verified in source and material to `PR-R003`.** Layer channel data is written verbatim — **straight, unassociated alpha**. Only the flattened composite section is matted against white: `src/psdWriter.ts:322-337` computes `p[i] = p[i] * a + 255 * (1 - a)` under an `// add weird white matte` comment, and `src/psdReader.ts:1010-1025` inverts it. That pair is not lossless for partially transparent pixels. The library additionally documents that reading through an HTML canvas premultiplies and corrupts data, and provides `ReadOptions.useImageData` to avoid it. **The Adobe specification itself makes no statement about premultiplied versus straight layer alpha — not verified.**

- **psd-tools** — `https://github.com/psd-tools/psd-tools`, MIT (`LICENSE`), PyPI 1.17.4 uploaded 2026-06-24, clone `ad89f315777866c832bf82e0377226cb13250c36` (2026-07-21). It does write (`src/psd_tools/psd/document.py:30`, `PSDImage.save` at `src/psd_tools/api/psd_image.py:241`) and supports PSB via a `header.version in_((1, 2))` validator. But `docs/index.rst:52-75` caps it itself: supported is "Read and write of the low-level PSD/PSB file structure"; *not* supported is "Editing of various layers such as type layers, shape layers, smart objects" or "Composition of adjustment layers". **It is a byte-level round-trip editor, not an authoring library.**
- **pytoshop** — BSD-3-Clause, writes PSD and PSB, **last release and last commit both 2018-11-30**. Abandoned.
- **Read-only:** `chinedufn/psd` (Rust, MIT OR Apache-2.0), `oov/psd` (Go, MIT), `TheNicker/libpsd` (**LGPL-2.0**, per `COPYING`; the GitHub badge says NOASSERTION and is wrong).
- **ImageMagick** documents `PSD | RW` and `PSB | RW` at `https://imagemagick.org/formats/`, with `coders/psd.c` containing `WritePSDImage` (:186) and a blend-mode round-trip table (`PSDBlendModeToCompositeOperator`, :858-900). Authoring an arbitrary layer tree from scratch through ImageMagick is **not verified**; the documented write path is oriented toward round-tripping an input PSD.
- **GraphicsMagick lists PSD but states "PSD format is no longer supported since the 1.3.24 release"** (`http://www.graphicsmagick.org/formats.html`). Unusable.

**Who exports it — and this is the decisive evidence for the ingestion path.** Every closed painting application screened writes PSD, and their own manuals name it as the way to move layered data:

- **Clip Studio Paint**, verbatim: "If you want to keep your layers intact and use the data in another application use Save Duplicate and save as a .psd (Photoshop Document) or .psb (Photoshop Big Document)", and "When saving in BMP, JPEG, PNG, TIFF or Targa format, the image will be saved with the layers flattened" (`https://help.clip-studio.com/en-us/manual_en/210_file/Save_file.htm`).
- **Procreate**, verbatim: "Export your artwork as a native .procreate file or a **layered Adobe® Photoshop® PSD**. This preserves your layers, layer names, opacity, visibility, and blend modes" (`https://help.procreate.com/procreate/handbook/actions/actions-share`).
- **FireAlpaca**, verbatim: "Layer data cannot be kept in BMP, JPEG, and PNG formats. To keep layer data, a file needs to be saved in MDP or PSD format" (`https://firealpaca.net/manual/menu/file/`). **MediBang Paint** lists PSD among its save formats with "This file type can preserve text and layer information, but not features specific to MediBang Paint" (`https://medibangpaint.com/en/tutorial/pc/save/`).
- **Photopea**: "You can save your work as a PSD file (to preserve the whole structure of the document)" (`https://www.photopea.com/learn/opening-saving`).
- **Affinity Photo 2** ticks PSD for export; **PSB is import-only**, and the only layer-preservation claim Serif makes on that page is for TIFF (`https://affinity.help/photo2/en-US.lproj/pages/Appendix/fileformat.html`).
- **Krita** and **GIMP** both export PSD.

**Security.** PSD is a length-prefixed binary format with deeply nested variable-length sections and attacker-controlled length fields. `psd-tools` carries three GitHub advisories, verified via OSV on 2026-08-02: `GHSA-22jr-vc7j-g762` (buffer overflow, fixed 1.9.4), `GHSA-24p2-j2jr-386w` (published 2026-02-26, "unguarded zlib decompression, missing dimension validation", fixed 1.12.2), and `GHSA-2rmg-vrx8-9j2f` (published 2026-07-09, **"arbitrary file write via smart-object filename"**, fixed 1.17.1). ImageMagick's `coders/psd.c` has a long CVE history including two on the *write* path, CVE-2014-2030 and CVE-2014-1947, both stack-based buffer overflows in `WritePSDImage`. No advisory was found for `ag-psd`; **absence of an advisory is not evidence of safety** and no public fuzzing corpus was verified for any of these libraries.

**Disposition: `adopt` as the primary ingestion format, subject to `SPIKE-A002` confirming fidelity. `shortlist` ag-psd as the write path.**

### 1.5 Krita `.kra` — the claim in `SPIKE-C001` is half wrong

`SPIKE-C001` line 49 states that "`.kra` and `.ora` are open ZIP+XML containers a program can write". **For `.ora` that is correct. For `.kra` it is not, on both halves of `PR-A003`.**

**There is no published specification.** The only user-facing document is `https://docs.krita.org/en/general_concepts/file_formats/file_kra.html`, whose entire technical content is that `.kra` "is Krita's internal file-format", its "construction is vaguely based on the open document standard, which means that you can rename your `.kra` file to a `.zip`", it contains a `mergedimage.png`, and — verbatim — "**Other applications mostly cannot open `.kra` files.**" An enumeration of the Krita repository (master `57180ec75d8df25073d4dbb99fa5d44b08d3e266`, 2026-08-02) found no layout specification anywhere in the source tree. **The format is defined only by its implementation.** It therefore fails the word "documented" in `PR-A003` before the write gate is even reached.

**What the format holds is genuinely richer than ORA or PSD** — read from `plugins/impex/libkra/kis_kra_tags.h` (LGPL-2.0-or-later, 147 lines): layer types `paintlayer`, `grouplayer`, `adjustmentlayer`, `generatorlayer`, `clonelayer`, `shapelayer`, `filelayer`, `referenceimages`; five mask types (`filtermask`, `transparencymask`, `selectionmask`, `colorizemask`, `transformmask`); per-layer `compositeop`, `opacity`, `visible`, `locked`, `passthrough`, `channelflags`, `keyframes`; an embedded ICC profile at `/annotations/icc` plus a full soft-proofing block; and `/animation/`, `/audio/`, `/storyboard/`, `/palettes/` trees. Container members are `mimetype`, `maindoc.xml`, `documentinfo.xml`, `preview.png`, `mergedimage.png`; layer pixels are **binary LZF-compressed 64×64 tiles**, not PNG. Alpha semantics are undocumented — **not verified**.

**`PR-A003` write gate: NOT MET.** Exactly one third-party writer was found — **kritapy** (`https://github.com/cozy-creator/kra-py`, clone `8362751259016c6c8a5456d9dfb80cd6abe8b1d3`, 2025-02-18). It genuinely implements the container and the tile format (`src/kritapy/document.py:62-64`, `src/kritapy/layers/paint.py:49-105`). It is also: PyPI version literally `0.0.0`, classifier "Development Status :: 3 - Alpha", a single commit day, **no LICENSE file** (MIT asserted only in `pyproject.toml`), no tests, and — concretely — **it writes the mimetype string `application/x-krita` where Krita's own `kis_kra_tags.h:19` defines `application/x-kra`.** Whether Krita opens its output is not verified and cannot be verified under this spike's read-only rule.

**libkra** (`https://github.com/2shady4u/libkra`, MIT verified from `LICENSE.md`, clone `b880e94e8ae43f7cb7746c0216a3998e3bc9f5d8` = tag `v0.3`, 2026-07-19) is actively maintained but **read-only**, and narrow: `libkra/kra_document.cpp:169` — "If it is not a paintlayer nor a grouplayer then we don't support it!" Its own README declares no colour-profile awareness.

**Krita's headless CLI does not close the gap.** `https://docs.krita.org/en/reference_manual/linux_command_line.html` documents `--export`, `--export-filename`, and `--export-sequence`. That reads a `.kra` and exports it elsewhere; it does not let a program author a `.kra` from non-Krita data. It also requires the full Qt GUI binary, and **no offscreen or headless platform mode is documented — viability on a display-less machine is not verified.** This is the same class of unknown as `RGT-S012`'s `tcomposer` question.

**Disposition: `defer` — read support only. Route the reader question to `SPIKE-A002` because Inochi Creator's ingestion path proves KRA is a real second source; route the writer question nowhere, because there is no credible writer.**

### 1.6 GIMP `.xcf`

**Specification: published, GPL-2.0-or-later, and explicitly subordinate to the code.** The file moved out of the GIMP source tree on 2022-11-14 (commit `f7f92b61e1d703ac4bf878b305019c98674c4745`); the `devel-docs/xcf.txt` path used by earlier research now 404s. Current canonical locations: `https://developer.gimp.org/core/standards/xcf/` and `https://gitlab.gnome.org/Infrastructure/gimp-web-devel/-/raw/master/content/core/standards/xcf.md`.

Its `## Status` section is verbatim: "This specification is an official condensation and extrapolation of the XCF-writing and -reading code. Yet we remind that **the ultimate reference is the loading and saving code**… Some of the normative statements made below are enforced by the XCF code in GIMP; others are just the authors' informed guess about 'best practices'."

**Its `## Scope` section is a direct, primary-source argument against using XCF as an ingestion format — and an endorsement of ORA.** Verbatim: "Use of the XCF format by third-party software is recommended **only as a way to get data into and out of GIMP** for which it would be impossible or inconvenient to use a more standard interchange format… The GIMP developers… **make no special efforts to allow reading of XCF files created by other software**. **Interchanging image data with other applications is not the goal of the XCF format.** … **OpenRaster (ORA) in particular is meant to be a generic interchange format** between software, with as few feature loss as possible, though its standardization is still quite slow."

**Structural hazard, quoted from the same document:** "GIMP's own XCF reader will ignore the length word of most properties that it does recognize… some historical versions of GIMP actually stored the wrong length for some properties, so there are XCF files with misleading property length information in circulation."

**Coverage is the widest of any candidate.** 62 `PROP_MODE` values plus `PROP_COMPOSITE_MODE`, `PROP_COMPOSITE_SPACE`, and `PROP_BLEND_SPACE`; layer groups (XCF 3+) and group masks (2.10+); float opacity overriding integer opacity; non-destructive GEGL effect layers (XCF 20+, GIMP 3.0) persisted as `{op, version, property-list, effect mask}`; text as parasites; vector layers (XCF 24+, GIMP 3.2); ICC as an `icc-profile` image parasite with "**If no profile is set, sRGB is assumed**". **Alpha is explicitly straight**: "The color values do not use 'premultiplied alpha' storage. The color information for pixels with alpha 0 *may* be meaningful; GIMP preserves it." That is the only format in this round whose specification states alpha semantics unambiguously.

**Version churn is severe:** versions 14–23 all landed in GIMP 3.0.0 (2025-03-16) and 24–25 in GIMP 3.2. A reader pinned to one version ages fast.

**`PR-A003` write gate: MET, with caveats.** GIMP documents true headless batch operation — `-i, --no-interface` and `-b, --batch=commands`, plus a `gimp-console` binary (`https://docs.gimp.org/3.0/en/gimp-fire-up.html`) — so `gimp-console -i -b '(...)'` writes XCF with no GUI. But that is GPL-3.0-or-later software driving a Scheme PDB, which is an operational dependency, not a library. The one permissive third-party writer is **xcf-rs** (`https://github.com/mothsART/xcf-rs`, `UNLICENSE` file present, crates 0.5.0 2025-06-08, clone `3edb3c98bd20c048b8a278325956622b0bb6d7a5`), whose `src/create.rs:670 pub fn save(...)` is real but whose own README states the reader "supports RGB or RGBA images, but not grayscale or indexed" and that better-compressed XCF is "not supported". **gimpformats** (LGPL-3.0, clone `d3181b81a1accab51f6e892ec019ac0664ec83fc`, 2026-06-21) lists "Saving" under its own README heading "**In progress but results in crashes and tests failing**". **xcftools** is read-only and mixed-licence: Makholm's own code is public domain, but the bundled `gimp/*.h` headers are GPL-3.0-or-later, so the distributed whole is GPL-encumbered.

**Disposition: `reject` as an ingestion format, on the format maintainer's own stated scope. `reference` for two things RigTale needs: the explicit straight-alpha statement, and the effect-layer persistence model.**

### 1.7 Procreate (`.procreate`)

**No published specification.** Nothing on `help.procreate.com` or `procreate.com` describes the container.

**Structure, from credible reverse engineering.** `https://github.com/Avarel/silicate` `README.md` (clone `0e12deb2ae1ffb152fc4a3d09add230590f52f68`, 2026-03-29, MIT): a ZIP holding `{UUID}/{col}~{row}.chunk` tiles (LZO or LZ4, **premultiplied** RGBA or grayscale masks), `QuickLook/Thumbnail.png`, `video/segments/*.mp4`, and `Document.archive` — an Apple **NSKeyedArchive** whose root object is `SilicaDocument` and which holds the layer hierarchy, canvas size, opacity, blend, and visibility. Parsing it therefore requires an Apple plist/keyed-archive decoder in addition to a ZIP reader.

**Readers only.** `silicate` (MIT, active, read-only viewer/compositor); `jaromvogel/ProcreateViewer` (MIT, last commit 2019-10-19, dead); `jaromvogel/prospect` (**GPL-3.0**, 2024-12-20); `naanlizard/procreate2psd` (no licence file). The foundational `git.sr.ht/~redstrate/silica-viewer` that silicate credits **404s as of 2026-08-02**.

**`PR-A003` write gate: NOT MET.** No writer was found in any language.

**It does not need to be met.** Procreate documents "Export your artwork as a native .procreate file or a layered Adobe® Photoshop® PSD. This preserves your layers, layer names, opacity, visibility, and blend modes", and separately "You can also share layers as PNG Files, and Animated PNGs" (`https://help.procreate.com/procreate/handbook/gallery/gallery-file-types`). **The documented layered egress is PSD.**

**Disposition: `reject` as an ingestion format; `reference` as evidence of what the segment paints in. Route to `SPIKE-A002` only as a "user hands us the wrong file" diagnostic case.**

### 1.8 Clip Studio Paint (`.clip`)

**No published specification.** Celsys does publish an open standard — but for exposure sheets, not artwork: XDTS, `https://www.celsys.com/en/clipsolution/xdts/`, "an open format that is not dependent on a specific software and that anyone can develop and implement." XDTS is already in the RigTale index from `RGT-S001` and is unrelated to this question.

**Structure, from two independent clean-room efforts that agree.** `Inochi2D/clip-d` `SPEC.md` (commit `24fe807fa6503f964ed6c19a86bc60d15808d908`, 2023-07-03, BSD-2-Clause): big-endian; "A file always starts with the `CSFCHUNK` chunk, followed by 8 bytes of file length, then 8 bytes of offset info… After which there is a `CHNKHead` chunk… there may be 1 or more `CHNKExta` chunks, followed by a **`CHNKSQLi`** chunk and a `CHNKFoot` footer", with `CHNKExta` holding zlib-compressed image and layer data. `dobrokot/clip_to_psd` (MIT, last commit 2024-07-05) implements the identical header independently (`clip_to_psd.py:92-121`) and confirms the embedded **SQLite** database with `Layer`, `Mipmap`, `MipmapInfo`, and `OffscreenChunks` tables.

**`PR-A003` write gate: NOT MET.** Readers and a `.clip`→`.psd` converter only.

**Egress is PSD/PSB**, quoted in §1.4. One fidelity caveat worth carrying into `SPIKE-A002`, from the `clip_to_psd` README: **CSP rasterises vector, tone, and frame-border layers on PSD export, and newer CSP versions drop the pixel data for vector layers entirely**, making them unrecoverable by third-party converters. That is a real ingestion failure mode with a named cause.

**Disposition: `reject` as an ingestion format; route the vector-layer-loss case to `SPIKE-A002` as a required malformed-input fixture.**

### 1.9 MediBang / FireAlpaca `.mdp`, and PaintTool SAI `.sai` / `.sai2`

These are the "Japanese/Korean production formats" the `TODO.md` gap list said the first round missed entirely.

**`.mdp`.** No published specification. MediBang confirms the format is shared between two products: "MDP is a dedicated format for **two** illustration creation tools, MediBang Paint and Fire Alpaca… it is only recognized by MediBang Paint and Fire Alpaca" (`https://medibangpaint.com/en/use/2020/06/explanation-of-file-extension/`). One GIMP plugin surfaced in search (`weeb-poly/gimp-file-mdp-plugin`); its metadata is **not verified**. Write gate: **not met**. Egress is PSD, per the FireAlpaca manual quoted in §1.4. MediBang states 100 million downloads worldwide (`https://medibang.co.jp/en/news/2024/20240920/`) — a vendor statistic, recorded as primary for the vendor's own claim and not as market share.

**`.sai` and `.sai2`.** No published specification, and **SYSTEMAX publishes no file-format list at all** for either version. The only official format statement located is Japanese-only (`https://www.systemax.jp/ja/sai/devdept.html`), announcing that the SAI2 canvas format is `.sai2` and is not compatible with version 1 except for reading `.sai`. Reverse engineering exists and is unusually detailed: `Wunkolo/libsai` (MIT, last commit 2026-05-19) documents `.sai` as "an archive containing a *file-system-like* structure once decrypted" with **block-level encryption** — 4096-byte blocks, every 512th block a key table, XOR cipher against a 256-entry key atlas; and `photopea/SAI2-specification` (no LICENSE file, commit `9dfeb3729c842f6eb734c5d9f6c629f4ddc550fa`, 2025-03-16) documents `.sai2` as unencrypted with magic `"SAI-CANVAS-TYPE0"`, `layr` chunks carrying layer type (`norm`/`fold`/`text`/`shap`/`liwk`), a four-character blend mode and 0–100 opacity, and 256×256 pixel tiles. **Write gate: not met.** Export options: **not verified** from any vendor source.

**A detail worth carrying to `SPIKE-R001`:** Krita's composite-op registry contains `COMPOSITE_LUMINOSITY_SAI`, a SAI-specific luminosity variant — third-party evidence that SAI's blend maths differs from both Photoshop's and the W3C's.

**Disposition for all three: `reject` as ingestion formats. `reference` for the segment-coverage argument.**

### 1.10 Layered TIFF, PNG/APNG, SVG, and multi-layer OpenEXR

**Layered TIFF is PSD wearing a TIFF wrapper.** libtiff's `libtiff/tiff.h:493` defines `TIFFTAG_IMAGESOURCEDATA 37724` with the in-source comment pointing at the Photoshop file-format specification, and `:474-475` defines `TIFFTAG_PHOTOSHOP 34377` as "private tag registered to Adobe for PhotoShop". **A layered TIFF's layers are a PSD blob in a private tag**, so the format inherits every PSD semantic question and adds a container. TIFF 6.0 itself is published; Adobe's own hosted PDF 404s and a copy is served by ITU at `https://www.itu.int/itudoc/itu-t/com16/tiff-fx/docs/tiff6.pdf` — the current canonical Adobe location is **not verified**. Multi-page TIFF (multiple IFDs) is writable by libtiff and Pillow, but that is pages, not a layer tree with opacity and blend modes. **No open-source library was verified to write a Photoshop-layered TIFF. Write gate: not verified.** Krita's manual recommends TIFF as a layer-preserving format, and Affinity's only explicit layer-preservation claim is for TIFF — both recorded, neither resolving the library question.

**There is no layered PNG standard.** W3C PNG 3rd edition is a Recommendation of 24 June 2025 and incorporates APNG (`acTL`/`fcTL` chunks); "layer" appears once in the whole document, incidentally. **APNG expresses animation frames, not layers.** PNG's value here is different and real: it is the payload format inside ORA, and it is the format Procreate uses for per-layer export. Its alpha semantics are stated normatively — "The color values in a pixel are not premultiplied by the alpha value assigned to the pixel. This rule is sometimes called 'unassociated' or 'non-premultiplied' alpha" — which makes it the reference point for straight alpha in this document.

**SVG is the vector counterpart and has no layer concept.** SVG 2 is a W3C Candidate Recommendation of 4 October 2018. **The word "layer" does not occur anywhere in its structure chapter** (`https://www.w3.org/TR/SVG2/struct.html`); grouping is `<g>`, and "layers" in Inkscape are `<g>` elements carrying vendor attributes. Blending comes from CSS `mix-blend-mode` and `isolation`, i.e. the same W3C Compositing-1 sixteen. Writing SVG headlessly is trivial. **The decisive limitation is in §2.5: SVG 2 contains no mesh or texture-mapping primitive at all** — zero occurrences of "mesh" in the specification index or the paint-servers chapter.

**Multi-part OpenEXR carries layers but no layer semantics.** The technical introduction (`website/TechnicalIntroduction.rst`, AcademySoftwareFoundation/openexr, BSD-3-Clause) documents multi-part files and a nested layer naming convention `L1.L2.C`, then states verbatim: "**Note that this naming convention does not describe a back-to-front stacking order or any compositing operations for combining the layers into a final image.**" Alpha is the opposite of PNG's: "By convention, all color channels are premultiplied by alpha", and "In the visual effects industry premultiplied color channels are the norm." Write gate met (OpenEXR BSD-3-Clause; OpenImageIO Apache-2.0). **EXR is a valid intermediate and render-pass handoff — Toon Boom Harmony's multi-layer write node emits it, and Blender's review record already names multilayer EXR as its layered-compositing handoff — but it is not a source-artwork format, because it carries no opacity, blend mode, mask, or stacking order.**

**Aseprite `.ase`/`.aseprite`.** The specification is published in-repo and linked from the official docs (`https://www.aseprite.org/docs/files/` → `docs/ase-file-specs.md`, HTTP 200, 637 lines): 128-byte header with magic `0xA5E0`, frames with magic `0xF1FA`, chunk types including `0x2004` Layer (with flags, layer type Normal/Group/Tilemap, child level, blend mode, opacity), `0x2005` Cel, `0x2007` Color Profile, `0x2023` Tileset; zlib pixel data; little-endian. **The licence is the trap:** there is no `LICENSE` file; `README.md` states "Source code and official releases/binaries are distributed under our End-User License Agreement for Aseprite (EULA)", and `EULA.txt` states "You may not distribute copies of the SOFTWARE PRODUCT to third parties." Only named sub-libraries are MIT. **A published format specification inside a repository that is not open source** — the mirror image of the Remotion finding in `candidate-screening.md`. Write gate: **not verified** (no permissively licensed writer confirmed). Segment fit is pixel art, not cutout character artwork.

### 1.11 What structure survives ingestion, measured on a real open-source rigging tool

`.research/clones/inochi-creator` at the pinned commit `dba60811` (BSD-2-Clause) is the only open-source 2D character-rigging application in the RigTale corpus that ingests layered artwork, and it is direct evidence of what a rig importer actually keeps.

- **It accepts exactly PSD and KRA.** `dub.sdl` declares `dependency "psd-d" version="~>0.6.1"` and `dependency "kra-d" version="~>0.5.6"`; `source/creator/panels/viewport.d:251-258` routes dropped `.psd` and `.kra` files to `incAskImportPSD` / `incAskImportKRA`; the File ▸ Import menu offers "Photoshop Document", "Krita Document", "Inochi2D Puppet", and an image folder ("Supports PNGs, TGAs and JPEGs"). **No ORA, no XCF, no TIFF.**
- **Blend modes are lossy on the way in.** `source/creator/io/psd.d:112-127` maps fourteen PSD blend keys and sends **everything else to `BlendMode.Normal` via `default:`**. Of the 28 keys Adobe documents, half are silently normalised.
- **Groups collapse unless they carry a blend.** `source/creator/io/kra.d:193-201`: a group whose mode is PassThrough or Normal becomes a plain node (or is dropped when `keepStructure` is false); only a group with a real blend mode becomes a `Composite` node with a framebuffer.
- **Layers are premultiplied at import.** `source/creator/io/kra.d:204-206` calls `inTexPremultiply(...)` on the extracted layer data before creating the texture. The source data is straight alpha; the runtime is premultiplied; the conversion is 8-bit.
- **Opacity, visibility, and position survive** (`kra.d:227-231`), and draw order becomes `zSort = -(index)`.
- Its dependencies: `Inochi2D/psd-d`, BSD-2-Clause, **last commit 2023-07-23** — read-only, no writer; `Inochi2D/kra-d`, BSD-2-Clause, last commit 2025-07-20 — read-only. An actively maintained fork, `nijigenerate/nijigenerate` (BSD-2-Clause, last commit 2026-06-18), keeps the identical ingestion path.
- **An observed defect in `kra-d` worth recording:** `source/kra/layer.d:47` and `:51` both map to the string `"lighter color"` (`Lighten` and `LighterColor`), so a Krita layer whose composite op is `lighten` matches neither and falls through. Observed in source at the pinned commit; behaviour **not tested** — no code was executed.

**The commercial reference point is stricter, not looser.** Live2D Cubism, the most widely used 2D character rigging tool, states verbatim: "**Only [PSD format] image data can be loaded in Cubism Editor**"; "Save format should be [PSD]. Color mode should be [RGB]. The color channel setting should be [8bit/channel]. **If even one of these conditions is not met, import cannot be performed**"; colour profile sRGB; and, on preparation, "**Do not use layer masks**" and "Merge line drawings and clipping masks" (`https://docs.live2d.com/en/cubism-editor-manual/precautions-for-psd-data/`). It further names the writer software it trusts: "Adobe Photoshop / Celsys CLIP STUDIO PAINT… PSDs created with applications other than those listed above may not load properly."

**This is a direct, evidence-backed constraint on `PR-A003`.** `PR-A003` requires preserving "masks, draw order, deformation, expression changes". The market-leading tool in this exact category **requires masks to be removed before import**, and the leading open-source tool discards half the blend modes and premultiplies at 8 bits. `PR-A003`'s preservation clause is more ambitious than any shipped product screened, and `SPIKE-A002` must either justify the ambition with a measurement or narrow the requirement.

**One convenient alignment:** ag-psd writes 8-bit RGB only — which is exactly and only what Live2D Cubism accepts. The library's most-cited limitation is a non-issue for this domain.

### 1.12 Which layered format do rigging and animation tools actually ingest?

Every claim below is from the vendor's own documentation.

| Tool | Documented layered artwork input |
|---|---|
| Live2D Cubism | **PSD only**, RGB/8-bit/sRGB, no masks |
| Esoteric Spine | PSD — built-in `Import PSD`, "saved from Adobe Photoshop or any other graphics software capable of writing a PSD file", naming Affinity, Clip Studio Paint, GIMP, Krita, Paint Tool SAI, Photopea, Procreate |
| Toon Boom Harmony 22 | PSD (16 bits/channel) among bitmap formats; multi-layer PSD import with "Single Layer", "Groups as Layers", "Individual Layers" modes; multi-layer **PSD and EXR** output |
| Toon Boom Storyboard Pro 25 | PSD **and PSB**, with "Click Yes to import each layer in the document as its own layer" |
| OpenToonz | "Photoshop documents (PSD files) can be loaded as a scene element… taking into account the layers"; "Supported formats are RGB or grayscale images, using 8 or 16 bits per channel" |
| TVPaint | "When you load a file in PSD format… the image's layers are all present in the Timeline" |
| Inochi2D / nijigenerate | PSD **and KRA** |
| Blender Grease Pencil | **Neither — SVG only.** Blender's import/export list and its image-format list contain no PSD at all |
| Moho | PSD claimed on vendor marketing pages ("up to 10 layers" for Debut 14); **the only reachable Lost Marble manual lists no PSD at all** — layered import **not verified** from versioned documentation |

**PSD is accepted by every ingesting tool verified. KRA by exactly one. OpenRaster by none.**

A negative worth recording precisely because it contradicts an assumption available elsewhere in this repository: **OpenToonz declares a PSD writer class and it writes nothing.** At the pinned commit `5f6beab3`, `toonz/sources/image/psd/tiio_psd.cpp:189` reads in full:

```cpp
void TLevelWriterPsd::save(const TImageP &img, int frameIndex) {}
```

An empty body. The class, the factory, and the registration all exist. Anyone screening on symbol presence would have recorded OpenToonz as a PSD writer. It is a reader only.

### 1.13 Untrusted-asset ingestion security

`TODO.md` routes the untrusted-ingestion gap to this item, and `docs/architecture/system-design.md` (Security Boundaries) already declares user-supplied layered files untrusted.

**ZIP-based containers — ORA, KRA, `.procreate`.** The ORA specification requires that layer files be "referenced in `stack.xml` by their full path relative to the OpenRaster file's root". A reader that joins that attacker-controlled path onto a temporary directory without normalisation is a path-traversal bug; the same applies to KRA's `maindoc.xml` and to `.procreate`'s UUID chunk paths. Decompression-ratio limits are equally required. **This is analysis of the specification text, not a reported vulnerability, and is labelled as such.** No ZIP-container advisory for these specific readers was located.

**PSD.** Three GitHub advisories against `psd-tools`, quantified in §1.4, one of which is an **arbitrary file write** reachable from a crafted smart-object filename and was published four weeks before this screening. ImageMagick's PSD coder has CVEs on both the read and write paths.

**Comparative exposure of the compositing candidates**, from OSV queries against the Debian 12 source packages on 2026-08-02 — all-time counts across all severities, offered as an order-of-magnitude signal and not as a defect-density metric: `imagemagick` 739 advisory records, `tiff` 271, `vips` 22. Pillow's advisory list is long and current, including two 2026 decompression-bomb-bypass advisories and an OS-command-injection advisory in `WindowsViewer.get_command()`.

**Consequence for screening: parsing untrusted PSD in-process in a memory-unsafe language is the highest-risk single component identified in this round.** ag-psd (TypeScript) and the Rust readers are memory-safe by construction; ImageMagick, libpsd, and libtiff are not. This belongs in `SPIKE-A002`'s malformed-input case list, which currently says only "malformed, flattened, ambiguous, incompatible, and unlicensed inputs".

---

## Part 2 — Q2: The Vector-versus-Raster Determination

### 2.1 Verdict

**The source artwork is layered raster. The determinism shortlist was not screening the wrong universe, but it was screening it on the wrong axis, and the axis it missed is the one that decides the question.**

Three findings, in order of force:

1. **Every tool the target segment paints in is raster-first, and the only layered format they all export is PSD** (§1.4, §1.12). Not one of them exports a vector layered container.
2. **Every 2D cutout rig system screened deforms a raster texture.** This is verified in source, not assumed (§2.3).
3. **The vector shortlist's members are not disqualified — tiny-skia is a raster pixel pipeline with the full W3C blend set and a pattern shader, and Skia has a textured-mesh primitive — but neither implements Photoshop's eleven extra blend modes, and no general 2D graphics library screened does** (§2.4). The real gap is not vector-versus-raster. It is **W3C-blend-set-versus-Photoshop-blend-set**, and it was invisible until the input question was asked.

### 2.2 What the target users produce

Raster, with a vector minority inside otherwise raster documents.

- `[FACT]` **Procreate** is raster-only and iPad-only; its documented layered exports are `.procreate` and PSD, plus per-layer PNG.
- `[FACT]` **Clip Studio Paint** is hybrid: it has vector layers, but its own manual says the way to move layers to another application is PSD/PSB, and `clip_to_psd`'s README records that **CSP rasterises vector layers on PSD export and newer versions drop their pixel data**.
- `[FACT]` **Krita** is raster-first with a vector `shapelayer` type; **MediBang/FireAlpaca** and **PaintTool SAI** are raster with limited vector; **Photoshop** is raster with shape layers.
- `[REPORTED]` Vendor-published usage figures, primary for the vendor's own claim and **not** market share: Clip Studio Paint "exceeded 50 million copies" (2025-04-10); Procreate "over 30 million users" (2023); MediBang Paint 100 million downloads (2024).
- `[UNKNOWN]` Widely repeated survey percentages for tool market share were checked and could not be traced to any primary publication. They are not used here.

`[UNKNOWN]` **Which painting tool RigTale's specific target segment uses is unknowable within this project.** `docs/research/small-studio-workflow.md` covers the segment's *animation* tools and says nothing about its painting tools, and with `RGT-S009B` rejected there will be no interviews. Vendor documentation and vendor-published user counts are the only evidence that will ever exist for this question. **The ingestion decision must therefore rest on format reach rather than on measured tool share** — which is what §1.12 supplies: PSD is accepted by every ingesting tool verified, so choosing it does not require knowing which painting tool the user runs.

### 2.3 What the rig systems consume — verified in source

| System | Rig draw primitive | Evidence |
|---|---|---|
| Inochi2D / Inochi Creator | `ExPart` built from a `Texture` created from decoded PSD/KRA layer pixels | `source/creator/io/kra.d:204-210` at `dba60811` |
| DragonBones | `ImageDisplayData.texture: TextureData` and `MeshDisplayData { geometry: GeometryData; texture: TextureData }` | `DragonBones/src/dragonBones/model/DisplayData.ts:81-145` at `64b6c69a`. There is no vector-path display type; `PathDisplayData` drives constraints |
| Godot 2D skeleton stack | `Polygon2D` carries `Ref<Texture2D> texture` with texture offset/rotation/scale, plus bones and per-vertex weights | `scene/2d/polygon_2d.h:55,122-132` at `eda2a482` |
| Live2D Cubism | PSD layers become deformable textured meshes | vendor documentation, §1.11 |
| Spine | PSD layers become image attachments on slots | vendor documentation, §1.12 |

**2D cutout animation is the deformation of raster texture patches by a mesh.** Every candidate with a real rig model in the RigTale corpus does this. The systems that are vector-native — Synfig, Glaxnimate, Lottie — are also the systems `RGT-S001` recorded as having no bone hierarchy or a weaker one, and their authoring path is the tool itself rather than the artist's painting application.

**Consequence for `PR-R005`.** `PR-R005` records that "no candidate supplies both a reusable character rig system and a deterministic frame-addressable renderer", and `SPIKE-C001` line 51 speculates that this may be because "the search ran across two disjoint universes". **The evidence supports that diagnosis.** The rig candidates were assessed as rig systems and the renderer candidates as vector rasterisers, and the operation that joins them — draw a textured, deformed triangle mesh with a specified blend mode into a layer stack — was never used as a screening criterion for either group.

### 2.4 The blend-mode gap, which is the real finding

**Photoshop defines 28 blend keys and publishes no formulas for any of them.** W3C Compositing-1 defines 16 with normative formulas. **No general-purpose 2D graphics library screened implements the eleven extra Photoshop blend modes.**

Verified blend-mode coverage, each from the enum in the library's own source:

| Library | Porter-Duff | W3C 12 separable | W3C 4 non-separable | PSD-only extras |
|---|---|---|---|---|
| Skia (`include/core/SkBlendMode.h`) | yes | yes | yes | **no** |
| tiny-skia (`src/blend_mode.rs:5-65`) | yes | yes | yes | **no** |
| Cairo (`src/cairo.h`) | yes | yes | yes | **no** |
| pixman (`pixman/pixman.h:431-445`) | yes | yes | yes | **no** |
| libvips (`libvips/include/vips/conversion.h:110-139`) | yes | yes | yes | **no** |
| raqote (`src/draw_target.rs:79-109`) | yes | yes | yes | **no** |
| Aseprite `src/doc` (`blend_mode.h:15-44`) | — | yes | yes | addition/subtract/divide only |
| ImageMagick (`MagickCore/composite.h`) | yes | yes | yes (Hue/Saturate/Colorize/Luminize) | **yes** — LinearBurn, LinearDodge, LinearLight, PinLight, VividLight and HardMix by exact name; Dissolve, DivideSrc/DivideDst and ModulusSubtract under names whose formulas differ from Photoshop's; darker colour and lighter colour absent under any name. PegtopLight, Freeze and Reflect are not Photoshop keys at all |
| Blend2D (`blend2d/core/context.h:242-305`) | yes | yes | **none** | LinearBurn, LinearLight, PinLight |
| GEGL (`operations/generated/`) | yes | yes | **none** | no |
| OpenImageIO (`imagebufalgo.h:1005-1044`) | `over`/`zover` only | **none** | **none** | no |
| Pillow (`src/PIL/ImageChops.py`) | partial | **8 of 12** — no color-dodge, color-burn, exclusion | **none** | no |
| Krita `KoCompositeOpRegistry.h` | yes | yes | yes | **all eleven by name** — dissolve, linear burn, darker color, linear dodge, lighter color, vivid light, linear light, pin light, hard mix, subtract, divide; plus parallel HSV/HSL/HSI families. Read from clone `57180ec7`; 148 composite ids in total. Name equality is not formula equality — the registry ships `COMPOSITE_HARD_MIX_PHOTOSHOP` beside `COMPOSITE_HARD_MIX` |

**And the same mode name is not the same formula.** Krita's registry, read from `libs/pigment/KoCompositeOpRegistry.h` at master `57180ec7` (2026-08-02), ships **four different soft-light implementations** side by side — `COMPOSITE_SOFT_LIGHT_PHOTOSHOP`, `COMPOSITE_SOFT_LIGHT_SVG`, `COMPOSITE_SOFT_LIGHT_PEGTOP_DELPHI`, `COMPOSITE_SOFT_LIGHT_IFS_ILLUSIONS` — plus `COMPOSITE_HARD_MIX_PHOTOSHOP` alongside `COMPOSITE_HARD_MIX` and a SAI-specific `COMPOSITE_LUMINOSITY_SAI`. **That is primary-source proof that "soft light" is ambiguous across the exact ecosystem RigTale ingests from, and that Photoshop's and SVG's definitions differ.**

**This is a `PR-R003` and `PR-R005` problem, not a nice-to-have.** If a user's PSD uses Linear Light on a shadow layer, a Skia, tiny-skia, Cairo, pixman, libvips, or raqote backend has nothing to map it to. The two options are to implement the missing modes against a reverse-engineered reference (Krita's and ImageMagick's implementations are the available oracles, both copyleft or bespoke-licensed for the Krita case), or to declare a **supported blend-mode profile** and fail loudly on anything outside it — which is exactly the `PR-C003` "never silently substitute a visibly incorrect action" posture applied to compositing. Inochi Creator's `default: blendMode = BlendMode.Normal` is the failure mode to avoid, and it is in shipped software.

### 2.5 Does the existing vector shortlist survive? Partly — with a named boundary

**resvg/tiny-skia is not disqualified, and an earlier version of my own reasoning in this task said it was. That is corrected here.** Verified at the already-pinned resvg commit `68b14c4c`:

- resvg maps **all sixteen** W3C blend modes onto tiny-skia (`crates/resvg/src/render.rs:145-165`).
- It decodes **raster images** — PNG, JPEG, GIF, WebP — behind the `raster-images` feature (`crates/usvg/src/tree/mod.rs:1470-1481`, `crates/resvg/src/image.rs`).
- tiny-skia exposes blend modes for **pixmap-on-pixmap compositing with no path involved**: `PixmapPaint { opacity, blend_mode, quality }` (`src/shaders/pattern.rs:32-49`) is the paint argument to `draw_pixmap` (`src/painter.rs:472`). tiny-skia is a **CPU raster compositor**, not merely a vector rasteriser.

Three boundaries are equally verified and are the real constraints:

1. **Blend mode is a group property, not an image property.** `crates/resvg/src/render.rs:38-40` renders `usvg::Node::Image` with no blend parameter; blending happens only when an isolated group is composited (`render_group`). Every blended raster layer must be wrapped in an isolated group, which means a full offscreen pixmap per blended layer.
2. **Raster images are premultiplied into an 8-bit pixmap on load.** `crates/resvg/src/image.rs:157-171` computes `dst = (src * a + 0.5) as u8` per channel. **An 8-bit premultiply is lossy and destroys colour precision under low alpha — which is precisely where cutout edge haloing appears**, and precisely the region that `docs/research/candidate-screening.md` already established resvg's own golden tests never check, because fully transparent pixels are exempt from comparison.
3. **SVG cannot express a textured mesh.** The word "mesh" occurs **zero** times in the SVG 2 specification index and in its paint-servers chapter. Mesh deformation of a raster layer — the core cutout operation — can only be emulated, by one clipped, affinely transformed `<image>` per triangle. That emulation is exact per triangle, because an affine map takes triangles to triangles, but it produces antialiasing seams at shared edges and multiplies node count by the mesh density. **No primary source verifying its visual quality or throughput was found; not verified.** For a 3,600–5,040-frame benchmark with per-frame SVG serialisation and re-parsing — a cost `candidate-screening.md` already flagged — this is the concrete reason the SVG front end is the wrong shape, and tiny-skia *without* resvg is the interesting candidate.

**By contrast, Skia has the primitive natively:** `include/core/SkCanvas.h:2081`, `void drawVertices(const SkVertices*, SkBlendMode, const SkPaint&)`, which is the standard way to draw a textured deformed mesh.

**Answer to the question as posed: the existing shortlist is *partly relevant*, and it was screening the wrong axis.** resvg-as-SVG-front-end is a poor fit for cutout compositing; **tiny-skia as a raster compositing library is a strong fit and was never screened as one**; Skia rises because it has both the mesh primitive and the full W3C blend set; and Vello and ThorVG remain vector-first candidates whose relevance now depends entirely on whether RigTale's pipeline has a vector stage at all.

### 2.6 Layered-raster compositing candidate records

Licences were read from the `LICENSE`/`COPYING` file in each case unless noted. Dates are the clone's HEAD commit date and the newest release tag reachable at that clone.

**Skia** — `https://github.com/google/skia`. BSD-3-Clause (`LICENSE`). HEAD `1c31040989d4813828c88cd43eb94b1bd1690a7f`, 2026-08-02. **No semver releases**; milestone branches only, newest `chrome/m152`, with `SK_MILESTONE 153` on main — release *dates* not verified. Headless CPU rendering is first-class: `SkSurfaces::Raster(...)` "Allocates raster SkSurface. SkCanvas returned by SkSurface draws directly into those allocated pixels" (`include/core/SkSurface.h:78`), plus `WrapPixels` into caller memory. Blend modes complete (W3C 16 + Porter-Duff); **no PSD extras**. Alpha: premultiplied is the working representation (`include/core/SkAlphaType.h`, `kPremul_SkAlphaType`). **`drawVertices` gives it the textured-mesh primitive no other shortlisted candidate has.** No determinism claim found. Build weight and Node/Swift binding cost are the open questions.

**tiny-skia** — `https://github.com/linebender/tiny-skia`. BSD-3-Clause (`LICENSE`; Google 2011 + Yevhenii Reizner 2020). Clone `88c65f6e6dfb31b7ea720e2f1609db7bf154b182`, 2026-07-31; crates.io v0.12.0 published 2026-02-02. "an absolute minimal, **CPU only**, 2D rendering library" — no GPU path exists. Blend modes complete for pixmap compositing, per §2.5. **Alpha is premultiplied and explicitly documented** (`src/pixmap.rs:26,300,317`). No determinism claim found, and a real counter-signal in its own README: "neither Skia or `tiny-skia` are supporting dynamic CPU detection, so by enabling newer instructions you're making the resulting binary non-portable" — **output can vary with the SIMD level the binary was compiled for**, which is directly material to `RGT-S013` and `PR-R007`. Its README also describes it as "more of a research project" (discovery signal). Textured-mesh drawing is available only by per-triangle path fill with a `Pattern` shader — plausible, **not verified**.

**Cairo** — `https://gitlab.freedesktop.org/cairo/cairo`. **LGPL-2.1 OR MPL-1.1** (`COPYING`) — note MPL **1.1**, not 2.0. Clone `bd04e43e201ef9beddcacdf379b610a0e199112e`, 2026-07-11; release 1.18.4, 2025-03-08. Image surfaces are pure in-memory. Blend modes complete (`cairo_operator_t`). Alpha premultiplied (`CAIRO_FORMAT_ARGB32` documented as "Pre-multiplied"). No determinism claim found — a grep of all clone documentation for "deterministic|reproducib" returned zero hits, which **supersedes the "marketing line about consistent output" recorded in `candidate-screening.md`**. This is `node-canvas`'s backend.

**pixman** — `https://gitlab.freedesktop.org/pixman/pixman`. MIT (`COPYING`). Clone `14735ced17e0053abbb925f9cf18c05ed9f52378`, 2026-06-15; release `pixman-0.46.4`, 2025-07-20. Blend modes complete (`pixman_op_t` 0x30–0x3e). **It is one of only two candidates that cites a normative specification inside the compositing source**: `pixman/pixman-combine-float.c:302-342` — "The following blend modes have been taken from the PDF ISO 32000 specification… chapters 11.3.5 and 11.3.6 and a later supplement for Adobe Acrobat 9.1… that clarifies the specifications for blend modes ColorDodge and ColorBurn." Alpha premultiplied, with the conversion stated in-source. No determinism claim found; it ships MMX/SSE2/NEON fast paths and **no per-path numeric-equivalence claim was located** — a structural determinism concern of the same shape as tiny-skia's.

**libvips** — `https://github.com/libvips/libvips`. **LGPL-2.1-or-later** (`LICENSE` plus per-file headers). Clone `362b4920ce58b9054aee1a60757d45d8b5dbf757`, 2026-08-01; release v8.18.4, 2026-07-05. Blend modes complete in the header and implementation; the **published API page omits the four non-separable modes** while the source has them — a documentation defect, recorded so nobody screens it out on the rendered page. `libvips/conversion/composite.cpp:1` — "composite an array of images with PDF operators"; `:466` "Non-separable blend helpers from the Cairo/PDF definitions"; luminosity coefficients 0.3/0.59/0.11 match the PDF definition. **It is the only candidate exposing a caller-facing `premultiplied` switch** (`:1707-1711`), premultiplying incoming pixels itself when unset (`:570`) and round-tripping for operators that need unpremultiplied values (`:893-894`). Constraint at `:1638`: "non-separable blend modes require 3-band images". **No native PSD loader** — PSD only via an ImageMagick delegate. No determinism claim found; its only "reproducibility" hit is a contributor-process line in `CONTRIBUTING.md`.

**ImageMagick** — `https://github.com/ImageMagick/ImageMagick`. **The ImageMagick License**, a bespoke Apache-2.0-derived document, not Apache-2.0 itself. Clone `cc6d9251e7746dcb9ef6b391976c2a334edd0d15`, 2026-08-02; release 7.1.2-29, 2026-07-27, on a roughly weekly cadence. **The only candidate that both composites with the extended Photoshop blend set and reads and writes layered PSD** (`coders/psd.c`, `ReadPSDImage` :2392, `WritePSDImage` :186, blend map :858-900). Alpha: straight in the pixel model, premultiplied internally during compositing (`MagickCore/composite.c:151,1113-1119`). Against it: the largest CVE surface of any candidate (739 Debian advisory records), output that depends on build-time QuantumDepth and HDRI settings, no determinism claim, and an apparent key swap in its own PSD writer table at `coders/psd.c:282-284` (observed; root cause not verified). **Its strongest role is as a reference oracle and a conversion tool, not as the production compositor.**

**GraphicsMagick** — `http://www.graphicsmagick.org/`. MIT-style (`Copyright.html`). Release 1.3.48, 2026-07-23; last commit not verified (Mercurial). Blend modes present by name; formula conformance not verified; alpha semantics not verified. **Dropped PSD support at 1.3.24.** Weakest evidence base of the set.

**OpenImageIO** — `https://github.com/AcademySoftwareFoundation/OpenImageIO`. Apache-2.0 (`LICENSE.md`). Clone `3aab3be78659eceb782b9b823273dc16eac5eae0`, 2026-07-31; release v3.1.16.0, 2026-07-30. **Decisive negative: it has no PDF or Photoshop blend modes at all.** `src/include/OpenImageIO/imagebufalgo.h:1005-1044` offers only `over()` and `zover()`, and a case-insensitive grep across its source for `softlight|colorburn|hardlight|blendmode|overlay` returned zero hits. Alpha is associated/premultiplied with an explicit `premult`/`unpremult`/`repremult` trio. **Excellent as an image I/O and colour-pipeline layer; not a layered-artwork compositor.**

**Blend2D** — `https://github.com/blend2d/blend2d`. zlib (`LICENSE.md`). Clone `6dbc2cefbc996379e07104e34519a440b49b15d7`, **2025-11-29 — roughly eight months without a commit**. **`git ls-remote --tags` returns nothing: the repository has never cut a tagged release**; the in-source version is `BL_VERSION 0.21.2`. All eleven separable modes plus LinearBurn/LinearLight/PinLight, but **no hue, saturation, colour, or luminosity** (`BL_COMP_OP_MAX_VALUE = 28`). Its JIT pipeline has a documented off switch (`BL_CONTEXT_CREATE_FLAG_DISABLE_JIT`), but **no claim that the JIT and reference pipelines agree bit-for-bit** — which sharpens rather than resolves the concern already recorded in `landscape.md`.

**Pillow** — `https://github.com/python-pillow/Pillow`. MIT-CMU (`LICENSE`). Clone `425a038b89afc76f145b522fd5e399385b56b09b`, 2026-08-02; release 12.3.0, 2026-07-01. **Blend coverage is the weakest of any live candidate**: `ImageChops` has eight of the twelve separable modes and **none** of the non-separable ones; color-dodge, color-burn, and exclusion are absent. Its PSD reader explicitly discards blend data — `src/PIL/PsdImagePlugin.py:248`, `# skip over blend flags and extra information`. Large and current advisory list. **Reject as a compositor; retain only as a codec convenience.**

**GEGL** — `https://gitlab.gnome.org/GNOME/gegl`. Split licence: library LGPL-3.0-or-later (`gegl/gegl.h:4-6`), repository `COPYING` GPL-3.0. Clone `2d0e992c970e784ed0fa8331785941ccf859aa32`, 2026-07-31; release `GEGL_0_4_70`, 2026-03-24. All eleven separable modes, generated from `operations/generated/svg-12-blend.rb` citing SVG 1.2; **no hue/saturation/colour/luminosity in GEGL itself** — those live in GIMP's own `app/operations/layer-modes`, outside this repository and **not verified here**. Premultiplied via babl `RaGaBaA`. Copyleft; `reference` only.

**raqote** — `https://github.com/jrmuizel/raqote`. BSD-3-Clause (`LICENSE.md`). Clone `9f1340c8ce3909286601a059a3c2077c3502a059`, **2025-02-11 — roughly eighteen months stale**; release 0.8.5, 2024-09-11. Blend modes complete. CPU-only. Alpha premultiplied (doc statement not verified). Watch-list only, below tiny-skia on every axis.

**image-rs/image** — `https://github.com/image-rs/image`. MIT OR Apache-2.0. Clone `034a1585dfec1b3eb2aa7489cf7d5825a98bf89f`, 2026-07-26; release 0.25.10, 2026-03-10. **No blend modes at all** — `Pixel::blend` is straight-alpha source-over only (`src/color.rs:837-870`). Viable as a codec layer, not as a compositor.

**Aseprite `src/doc`** — the blend implementation specifically is **MIT** (`src/doc/LICENSE.txt`; `src/doc/blend_mode.h:4-5` "This file is released under the terms of the MIT license"), inside a repository whose root `EULA.txt` is proprietary and forbids redistribution. Clone `717ab76b2ed9b814fda4b65eb388f6ad480ca4ee`, 2026-07-30; release v1.3.18.1, 2026-07-23. Complete W3C set in integer arithmetic with the canonical PDF helpers `lum()`, `clip_color()`, `set_lum()` (`src/doc/blend_funcs.cpp:362-481`). **Its value to RigTale is as a compact, permissively licensed cross-check oracle, not as a dependency** — and the licence boundary must be stated precisely if it is ever used, because the surrounding application is not open source.

**Krita `KoCompositeOp`** — the widest blend coverage found anywhere, and the only place the Photoshop-versus-SVG formula divergence is made explicit (§2.4). **Krita is a Qt desktop application; no headless library extraction path was verified.** GPL-family licence, not verified by reading the file. `reference` only, and a strong one.

**OpenColorIO** — **BSD-3-Clause**, read from `main/LICENSE`. Latest tag v2.5.2. **Not a compositing library and contributes zero blend modes** — but blend results are colour-space dependent, so it is the natural home for the working-space half of the `TODO.md` colour-management gap.

**libmypaint** — ISC (`COPYING`). Clone `d5a88fbe6649d5ec776bc42ec8c1f4bb29d7fd7f`, 2026-04-14, but **latest tag `v2.0.0-beta.1` dated 2019-12-31 — no stable release in over six years**. It is a brush-dab library with no PDF blend modes (`brushmodes.c`). Rule out.

### 2.7 The cross-candidate negative

**No candidate in this set makes any output-determinism or reproducibility claim.** Thirteen clones were searched for "deterministic" and "reproducib"; the only hits were contributor-process statements (libvips `CONTRIBUTING.md`) and fuzzing-reproducibility notes (OpenImageIO). This is stated as a search result over the sources inspected, not as a universal claim.

**Determinism will therefore be established by RigTale's integration and measurement, not inherited from a dependency.** That is the same conclusion `RGT-S013` reached for the vector rasterisers, now extended to the raster compositors — and it means `PR-R007`'s "declared raster determinism class" must cover the compositing stage, not only the rasterisation stage.

---

## Dispositions

| Candidate | Disposition | Gating question | Routed to |
|---|---|---|---|
| **Adobe PSD** (ingestion) | `adopt` | Does a real PSD from Procreate, Clip Studio, and Krita survive import with the structure a rig needs, or does it need the Live2D-style "prepare it this way" contract? | `SPIKE-A002` |
| **Adobe PSB** | `adopt` alongside PSD | Does anything in the fixture exceed 30,000 px, or is PSB purely a compatibility surface? | `SPIKE-A002` |
| **ag-psd** (PSD/PSB read+write) | `shortlist` | Can it write a PSD that Photoshop, Clip Studio, Krita, and Live2D all open without a repair warning? Requires execution. | `SPIKE-A002` |
| **OpenRaster `.ora`** | `adopt` as fixture and round-trip format; `reject` as user ingestion path | Is a fixture format with no masks, no adjustment layers and no ICC sufficient to exercise the importer? | `SPIKE-A002`, `SPIKE-F001` |
| **pyora** | `defer` | Five years unmaintained and writes two non-conformant values. Is a from-scratch ORA writer cheaper than adopting it? | `SPIKE-A002` |
| **Krita `.kra`** | `defer`, read-only | Is a second, structurally richer source format worth a second importer, given no specification exists and Inochi is the only precedent? | `SPIKE-A002` |
| **libkra** | `reference` | Paintlayer and grouplayer only, no colour profile. Does that cover a real `.kra` from a working illustrator? | `SPIKE-A002` |
| **kritapy** (`.kra` writer) | `reject` | v0.0.0, no LICENSE file, and writes a mimetype string that disagrees with Krita's own source constant. | — |
| **GIMP `.xcf`** | `reject` as ingestion; `reference` for alpha semantics and effect-layer persistence | none | — |
| **`.procreate`, `.clip`, `.mdp`, `.sai`/`.sai2`** | `reject` as ingestion formats; `reference` for segment coverage | Which of them lose structure on PSD export, and does RigTale need to detect and report that? The CSP vector-layer drop is a confirmed instance. | `SPIKE-A002` |
| **Layered TIFF** | `defer` | Does any permissively licensed library write Photoshop-layered TIFF, or is it PSD-in-a-wrapper only? Currently not verified. | `SPIKE-A002` |
| **PNG / APNG** | `adopt` as the per-layer payload and per-layer export path; `reject` as a layered container | none | — |
| **SVG** | `reference` | Does RigTale have any vector stage at all — backgrounds, effects, UI overlays — or is the pipeline raster end to end? | `SPIKE-A002`, `SPIKE-R001` |
| **Multi-part OpenEXR** | `reference` as an intermediate and render-pass handoff; `reject` as source artwork | Is a multi-layer EXR handoff needed for the deliverables in `PR-F003`? | `SPIKE-R001` |
| **Aseprite `.ase`** | `reject` | Licence forbids redistribution and the segment is pixel art. | — |
| **Skia** | `shortlist` **for raster compositing** | Does `drawVertices` plus the raster surface give deterministic, headless textured-mesh compositing on macOS arm64, and what is the binding cost from Swift or Node? | `SPIKE-R001`, `RGT-S013` |
| **tiny-skia** | `shortlist` **re-scoped from vector rasteriser to raster compositor** | Two questions, both new: does per-triangle `Pattern`-shader fill produce acceptable mesh deformation, and does compiled-in SIMD level change output? | `SPIKE-R001`, `RGT-S013` |
| **resvg** (SVG front end) | `defer`, **role narrowed** | Only relevant if a vector stage exists. The 8-bit premultiply on image load and the per-blended-layer isolated group are the measurable risks. | `SPIKE-R001` |
| **libvips** | `shortlist` | LGPL-2.1+ dynamic linking under an undecided distribution model; and is the demand-driven threaded pipeline bit-reproducible? | `SPIKE-R001`, `PR-P005` |
| **pixman** | `shortlist` | MIT, PDF-spec-cited formulas, but SIMD paths with no stated numeric equivalence. Does it agree with itself across CPU dispatch? | `SPIKE-R001`, `RGT-S013` |
| **Cairo** | `defer` | Retained as `node-canvas`'s backend. The prior "design-intent statement" of consistent output is not supported by anything in the repository. | `SPIKE-R001` |
| **ImageMagick** | `reference` as blend oracle and conversion tool; `defer` as a production dependency | Bespoke licence, build-dependent output, largest CVE surface. Is it acceptable anywhere in a pipeline that ingests untrusted files? | `SPIKE-A002`, `PR-P005` |
| **Aseprite `src/doc` blend functions** | `reference` as a permissively licensed blend oracle | Can the MIT boundary be stated precisely enough to use it? | `SPIKE-R001` |
| **Krita `KoCompositeOp`** | `reference` | The authoritative catalogue of how many formulas hide behind one mode name. | `SPIKE-R001` |
| **Blend2D** | `reject` for this role | No non-separable blend modes, never tagged a release, eight months idle. | — |
| **GEGL** | `reference` | Copyleft, and the non-separable modes are not in this repository. | — |
| **OpenImageIO** | `reference` for image I/O and EXR; `reject` as a compositor | none | — |
| **Pillow, image-rs/image** | `reject` as compositors; `reference` as codecs | none | — |
| **GraphicsMagick, raqote, libmypaint** | `reject` | Dropped PSD / eighteen months stale / not a compositor. | — |
| **OpenColorIO** | `reference` | Owns the working-space half of the colour gap, which has no owner. | `TODO.md` colour gap |

---

## Propagation

Mandatory exit criterion per `docs/README.md`. **All rows were applied on 2026-08-02 by Project Owner instruction.**

| Finding | Target | Proposed edit | Status |
|---|---|---|---|
| PSD is the only layered format every ingesting tool accepts and every painting tool exports (§1.4, §1.12) | `PR-A003` | Name PSD/PSB as the primary candidate source format and record that the `SPIKE-A002` decision now has a named default rather than an empty set | `applied` |
| `PR-A003` requires preserving masks, while Live2D Cubism *requires masks be removed* and Inochi Creator drops half of PSD's blend modes (§1.11) | `PR-A003` | Qualify the preservation clause: state which structures must survive, which may be flattened with a recorded diagnostic, and require `SPIKE-A002` to measure rather than assume | `applied` |
| `.kra` has no published specification and no credible writer, contradicting `SPIKE-C001` line 49 (§1.5) | `docs/spikes/SPIKE-C001-competitive-landscape.md:49` | Correct the sentence: ORA is writable, `.kra` is not, and `.kra` is not documented | `applied` |
| Adobe publishes a PSD/PSB specification; "reverse-engineered" is imprecise (§1.4) | same line | Replace with: the specification is published but defines syntax only and explicitly declines to define semantics | `applied` |
| PSD defines 28 blend keys, publishes no formulas, and no general 2D library implements the extra eleven (§2.4) | `PR-R002`, `PR-R003`, `PR-R005` | Add a required **supported blend-mode profile** with explicit failure on out-of-profile modes, mirroring `PR-C003` | `applied` |
| One mode name is several formulas — Krita ships four soft-lights and a Photoshop/SVG split (§2.4) | `PR-R003` | Record that preview/final parity cannot be asserted across two backends until the blend profile fixes a formula per mode | `applied` |
| Alpha semantics differ by format: PNG and XCF straight, EXR and tiny-skia and Skia premultiplied, PSD straight per layer with a white-matted composite (§1.4, §1.6, §1.10, §2.6) | `TODO.md` colour/alpha gap; `docs/architecture/production-contracts.md` | This gap now has evidence and a named owner-candidate. Draft the one-page colour and alpha contract before `SPIKE-R001`, covering working space, straight-vs-premultiplied at each boundary, blend space, and bit depth | `applied` |
| resvg premultiplies raster images into an 8-bit pixmap on load, in the region its own goldens never check (§2.5) | `PR-R007`, `RGT-S013` | Add 8-bit premultiplication precision to the determinism-class evidence list, alongside the existing font and macOS questions | `applied` |
| tiny-skia's output can vary with the SIMD level the binary was compiled for, by its own README; pixman ships SIMD paths with no equivalence claim (§2.6) | `PR-R007`, `RGT-S013` | Add "compiled-in instruction set" as a determinism variable alongside thread count and architecture | `applied` |
| 2D cutout rigs deform textured meshes; SVG has no mesh primitive; Skia has `drawVertices` (§2.3, §2.5) | `PR-R002`, `PR-R005`, `SPIKE-R001` | Add "textured, deformed triangle mesh with per-layer blend" as an explicit renderer screening criterion. It was not one, and it is the operation the product is made of | `applied` |
| The determinism shortlist was screened on the vector axis; tiny-skia is a raster compositor and was never screened as one (§2.5) | `docs/research/landscape.md`, `TODO.md` shortlist | Re-scope the tiny-skia row from "vector rasteriser" to "CPU raster compositor" and add Skia, libvips, and pixman as raster-compositing rows | `applied` |
| No compositing candidate makes a determinism claim (§2.7) | `PR-R007` | State that the determinism class must be established by measurement at the compositing stage as well as the rasterisation stage | `applied` |
| `psd-tools` has a 2026 arbitrary-file-write advisory; ImageMagick has 739 Debian advisory records; ZIP containers carry attacker-controlled internal paths (§1.13) | `SPIKE-A002` required cases; `docs/architecture/system-design.md` (Security Boundaries) | Expand the malformed-input case list to name path traversal, decompression ratio, nesting depth, and length-field overflow, and require the parser choice to be justified on memory safety | `applied` |
| Licence facts for the new candidate set: ImageMagick is a bespoke licence, Aseprite's repo is proprietary with an MIT sub-module, GEGL is LGPL-3 inside GPL-3, libvips is LGPL-2.1+, the ORA spec text has no licence at all (§1.3, §2.6) | `PR-P005` | Add these to the dependency-licensing evidence set; the ORA spec-text point is new and affects documentation reuse, not code | `applied` |
| Which painting tool the target segment uses is permanently unknowable now that `RGT-S009B` is rejected (§2.2) | `PR-A003`; `docs/research/small-studio-workflow.md` | Record that the ingestion decision rests on **format reach across ingesting tools**, not on measured tool share, and that this is a deliberate substitution forced by the no-interviews constraint | `applied` |
| OpenToonz declares `TLevelWriterPsd` and its `save` body is empty (§1.12) | `docs/research/repository-reviews/opentoonz.md` | Record the empty-writer finding; it is a concrete instance of the screening failure mode this repository has twice had to correct | `applied` |
| Clip Studio rasterises and now drops vector-layer pixel data on PSD export (§1.8) | `SPIKE-A002` required cases | Add "source tool lost data before RigTale saw the file" as a distinct diagnostic class from "malformed input" | `applied` |
| Krita's manual states PSD "doesn't have an official spec online"; Adobe publishes one (§1.4) | none — third-party document | No RigTale edit is possible or needed. Recorded so the Krita page is not cited as evidence for that claim | `none, with reason` |

---

## Contradictions and Self-Corrections

**Contradictions of existing claims in this repository.**

1. **`docs/spikes/SPIKE-C001-competitive-landscape.md:49` — "`.kra` and `.ora` are open ZIP+XML containers a program can write."** Half wrong. ORA has a published specification, a RelaxNG schema, and at least two independent writers; `.kra` has **no published specification anywhere**, is defined only by Krita's implementation, stores pixels as binary LZF tiles rather than XML-referenced PNGs, and has exactly one third-party writer at version 0.0.0 with no LICENSE file that writes a mimetype string disagreeing with Krita's own constant. §1.5.

2. **Same line — "PSD is reverse-engineered."** Imprecise. Adobe publishes "Adobe Photoshop File Formats Specification — November 2019" covering PSD and PSB, explicitly "provided for 3rd parties to read and write the Photoshop native file format". What is genuinely unpublished is *semantics* — the specification states "This document does not explain how to interpret the data" — and, critically, **the blend-mode formulas**. The correct statement is that PSD's syntax is documented and its behaviour is not. §1.4.

3. **`docs/spikes/SPIKE-C001-competitive-landscape.md:51` — "the correct candidate set is a layered-raster compositing set that was never enumerated", implying the vector shortlist answered the wrong question.** The diagnosis of the cause is right and the conclusion about the shortlist is too strong. tiny-skia is a CPU **raster** compositor with the full W3C blend set exposed for pixmap-on-pixmap compositing (`src/shaders/pattern.rs:32-49`), and resvg decodes and composites raster images. The shortlist was not screening a disjoint universe; **it was screening the right libraries against the wrong criterion.** §2.5.

4. **`docs/research/candidate-screening.md` on Cairo — "Its only determinism statement is a marketing line about consistent output."** A grep of the full Cairo clone at `bd04e43e` for "deterministic|reproducib" across all documentation returned **zero hits**. Cairo makes no determinism statement in its repository at all. The record should say there is none rather than that there is a weak one. §2.6.

5. **`docs/research/repository-reviews/mlt-glaxnimate-lottie.md:47` — that a GPL-free MLT build makes PSD and KRA unloadable.** **Verified and confirmed** at the pinned commit `8c092fd1`: `src/modules/core/loader.dict:33` maps `*.kra=qimage` and `:41` maps `*.psd=qimage`, with no fallback producer, while PNG (`:40`) and SVG (`:46`) list `pixbuf` and `glaxnimate` alternatives. Two additions the original record did not make: the Qt image producer yields a **single flattened image**, so even in a GPL build MLT never sees a layer tree; and **whether Qt can decode PSD at all without the KImageFormats plugin set is not verified.**

6. **`docs/research/landscape.md` authoring-path table.** Its "Open — a program can author content without a GUI or a proprietary tool" column lists runtime and animation formats only. On the evidence here, **OpenRaster and PSD/PSB both belong in that column** and neither is in the index at all.

7. **Krita's own manual states that PSD "doesn't have an official spec online" and recommends ORA or TIFF instead.** Contradicted by the live Adobe specification. Recorded because that page is otherwise a good primary source and could be miscited.

**Reasoning errors made during this screening, kept because the error is the transferable lesson.**

8. **"The vector shortlist is the wrong universe" is the intuitive conclusion and it is too strong.** Source refuted it: tiny-skia is a raster compositor. The failure was screening on library category rather than on the operation the product performs. The transferable rule: screen renderers on the primitive the product needs — here, textured deformed mesh with per-layer blend — not on what the project calls itself.

9. **"SVG cannot express mesh deformation" is also too strong.** It is emulable, one clipped affinely transformed `<image>` per triangle, and exact per triangle. The defensible claim is narrower: no mesh primitive exists, the emulation seams at shared edges and multiplies node count, and no primary source verifies its quality or throughput.

10. **Two reported release dates conflicted and were re-verified at the registry.** `psd-tools` 1.17.4 uploaded 2026-06-24 (PyPI); ag-psd `latest` 31.0.2 published 2026-07-02 (npm), ahead of the newest git tag. Registry values are used throughout, because git tags lag publishes.

---

## Open / Not Verified

Everything below was attempted and not established. None of it is inferred in the body of this document.

| Unknown | What it would take |
|---|---|
| **Whether ag-psd's output opens cleanly in Photoshop, Clip Studio, Krita, and Live2D Cubism.** This is the load-bearing assumption of the entire `PR-A003` write gate and cannot be settled by reading source | Execution, in `SPIKE-A002`, against the four target readers |
| **Whether any permissively licensed library writes a Photoshop-layered TIFF** (as opposed to multi-page TIFF) | Source inspection of the write path in libtiff-based writers; currently not verified |
| **PSD blend-mode formulas.** Adobe publishes none. Krita and ImageMagick are the available oracles and are copyleft or bespoke-licensed; Aseprite's `src/doc` is MIT but covers only the W3C set plus three | Either a licensed reference implementation, or a declared blend profile that excludes what cannot be reproduced |
| **Whether Krita's `--export` runs on a machine with no window server**, on macOS in particular. No offscreen mode is documented | The same class of test as `RGT-S012`'s `tcomposer` question |
| **Whether kritapy produces a `.kra` Krita will open.** Its mimetype string disagrees with Krita's own constant | Execution; out of scope here |
| **Whether tiny-skia's per-triangle `Pattern`-shader fill gives acceptable mesh deformation quality and throughput** | An executable spike; no candidate documents this use |
| **Whether tiny-skia, pixman, or libvips produce bit-identical output across SIMD dispatch, thread count, and macOS arm64** | `RGT-S013`, now extended to the compositing stage |
| **Whether Blend2D's JIT and reference pipelines agree bit-for-bit** | Execution; no claim exists either way |
| **Moho's layered PSD import.** Claimed on vendor marketing pages ("up to 10 layers"); the only reachable Lost Marble manual lists no PSD at all | A versioned Moho manual, or a vendor statement outside marketing |
| **PaintTool SAI's export format list.** SYSTEMAX publishes none | A vendor page; none was found in English or Japanese |
| **`.mdp` structure and any open-source reader's licence and maintenance state** | Cloning and reading `weeb-poly/gimp-file-mdp-plugin`; not done |
| **Which painting tool the target segment actually uses.** Vendor user counts exist; tool share within RigTale's specific segment does not | Nothing. `RGT-S009B` was the only route and was rejected by owner decision on 2026-08-02, so this is permanently unknowable. The ingestion argument rests on format reach instead; see §2.2 |
| **Whether Qt can decode PSD without KImageFormats**, which determines whether MLT's `qimage` route works at all in a plain build | Source or packaging inspection of the Qt image-plugin set |
| **GraphicsMagick's alpha semantics, blend formula conformance, and last commit date** | A Mercurial checkout; the git mirror 404s |
| **Skia's release dates.** It has milestone branches and no semver releases | Chromium release metadata; not retrieved |
| **libkra `v0.3` release date**, and licence files for `jsora`, the `krita` crate, `shivshank/xcf-rs`, and `xcfreader` | Non-GitHub hosts or absent files; each needs a direct fetch |
| **Any fuzzing corpus or security audit for ag-psd, psd-d, kra-d, silicate, clip-d, or libsai** | None found. Absence of an advisory is not evidence of safety |
