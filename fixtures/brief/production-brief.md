# Reference Production Brief

**Owner:** `SPIKE-F001` (`RGT-S003`), method step 3. **Status:** draft, not approved.

Two original preschool cutout music videos built from the published cast in `fixtures/`. Both are inside the charter's 150–210 second window. `creative-intent.json` carries the Gate 1 fields, the stimulation profile and the originality statement as data; this document carries the narrative, the shot lists, the capability boundary and the structured correction, and does not restate them.

## Why two

The matrix asks for two in four places. `RISK-41` requires that a second production differ on the narrative axis rather than in its assets. `RISK-42` requires both to record the same engine revision. `RISK-66` requires one production produced twice — once manually, once through RigTale — for the time comparison. `RISK-35` requires a correction whose blast radius is known before the run.

Production **A** is the benchmark: it is the one produced twice for `RISK-66`, and the one the correction lands in. Production **B** exists to prove the pipeline does not template, and is produced once.

## Rig capability boundary

**This is the load-bearing section.** `RISK-07` fails a production that declares an action its rig cannot perform, so the shot lists below stay inside what `fixtures/cast/manifest.json` actually supports. Read from the manifest:

| Available | How |
|---|---|
| Limb motion | `hip_*`, `knee_*`, `shoulder_*`, `elbow_*` on each biped; four legs plus `rump`, `tail_mid`, `tail_end` on `mochi` |
| Whole-character movement | pose `root` translation and `root_angle`, as `poses.plant` uses |
| Gaze | eye slot swap only — `eye_left`, `eye_left_look_left`, `eye_left_look_right` |
| Expression | mouth slot swap only — `mouth_neutral`, `mouth_smile`, `mouth_open`, `mouth_wide` |
| Speech and song | eight visemes — `ai`, `e`, `o`, `u`, `mbp`, `fv`, `l`, `ws` |
| Hands | `open`, `closed`, `point` |
| Attachment | `ball/grip`, `drum/grip`, `drum/strike`, `cart/hitch`, `cart/cargo`, `cart/axle_front`, `cart/axle_rear`. Each hand slot member carries its own `grip`, so a hand reference names the member — `hand_left_closed/grip` — because no bare hand layer exists to hang one on |

**Not available, and therefore absent from both scripts:** no head turn, no neck, no torso bend or lean — no biped has a spine or neck bone. No facial motion beyond slot swaps. No deformation on `cart` or `props`; both are rigid, so the wheels turn about their axle joints and the ball does not squash.

The consequence is a directing constraint, not a defect: **a character indicates attention with its eyes and its whole body, never by turning its head.** Both scripts are written that way. If a later brief needs a head turn, the cast gains a bone and the fixture takes a new version; the brief does not quietly assume one.

## Production A — *Carry It Together*

One ball, three friends, one cart. Each friend in turn finds the ball awkward to carry alone; each passes it on; at the end all three carry it together onto the cart. The refrain is a travelling one, sung while the group moves, and returns three times with the formation changed.

| Shot | Start–end | Sec | What happens | Exercises |
|---|---|---|---|---|
| A01 | 0:00–0:10 | 10 | Wide. `mochi` alone on the grass, tail sway. Camera pushes in slowly. | Parallax bands, quadruped idle, `tail_mid`/`tail_end` |
| A02 | 0:10–0:22 | 12 | `pim` walks in from frame left carrying the ball at `hand_left_closed/grip`. | Solo biped locomotion, ground contact, prop attachment |
| A03 | 0:22–0:46 | 24 | **Refrain 1.** `pim`, `bo`, `nu` walk abreast, `mochi` alongside. Camera pans with them. | Three simultaneous instances, group choreography, camera pan, parallax |
| A04 | 0:46–1:02 | 16 | `pim` passes the ball to `bo`. `ball/grip` meets `bo`'s `hand_right_closed/grip` on a declared contact frame. | Role-based interaction, visible contact frame, handoff |
| A05 | 1:02–1:14 | 12 | `bo` fumbles; the ball rolls. `nu` reacts — `mouth_open`, gaze `look_left`. `mochi` stops it with a forepaw. | Reaction, expression, gaze, quadruped contact |
| A06 | 1:14–1:38 | 24 | **Refrain 2.** Same motion clip, changed formation: `nu` leads, `mochi` rides on `cart/cargo`. | Controlled variation, cargo attachment, motion-clip reuse |
| A07 | 1:38–1:58 | 20 | `nu` plays the drum. `drum/strike` lands on the beat map's frames. Others clap on the offbeat. | Beat-synchronised prop action, `RISK-52` |
| A08 | 1:58–2:14 | 16 | All three push the cart; the ball rides in `cart/cargo`. Wheels turn about `axle_front` and `axle_rear`. | Vehicle wheel cycle against ground travel, multi-character interaction |
| A09 | 2:14–2:38 | 24 | **Refrain 3.** Camera pulls back to full width; all four and the cart move together. | Repetition with variation, camera move, full-cast composition |
| A10 | 2:38–2:48 | 10 | Wide hold. `mochi` tail sway. Slow fade. | Continuity with A01, resolve |

**168 seconds, 10 shots, 9 cuts.**

## Production B — *Where Did It Go?*

The ball goes missing. Each friend searches one named place and reports back. The refrain is the same question asked three times, sung standing still. `mochi` had it the whole time.

| Shot | Start–end | Sec | What happens | Exercises |
|---|---|---|---|---|
| B01 | 0:00–0:12 | 12 | Wide. `mochi` noses the ball out of frame. Nobody sees. | Establishing, quadruped action, prop displacement |
| B02 | 0:12–0:26 | 14 | `pim` finds the spot empty. `mouth_open`, gaze sweeps `look_left` then `look_right`. | Expression, gaze-only attention — no head turn exists |
| B03 | 0:26–0:44 | 18 | **Refrain 1.** All three ask the question together, standing. Static camera. | Three instances, synchronised singing, viseme track |
| B04 | 0:44–1:00 | 16 | `bo` looks behind `scene/tree_large`. Not there. | Occlusion, draw-order change, safe-area edge |
| B05 | 1:00–1:18 | 18 | **Refrain 2.** Same clip, gaze directions changed, `mochi` now in frame behind them. | Controlled variation, continuity |
| B06 | 1:18–1:34 | 16 | `nu` looks under the cart. Not there. `hand_right_point`. | Occlusion by the vehicle, hand slot |
| B07 | 1:34–1:52 | 18 | **Refrain 3.** Slower, lower. All three `mouth_neutral` between lines. | Repetition with tempo variation |
| B08 | 1:52–2:10 | 18 | `mochi` rolls the ball out. All three to `mouth_smile`. | Reveal, group reaction, contact frame |
| B09 | 2:10–2:24 | 14 | Drum celebration; `drum/strike` on the beat. | Beat sync in a second context |
| B10 | 2:24–2:36 | 12 | Wide resolve. | Continuity with B01 |

**156 seconds, 10 shots, 9 cuts.**

## Repetition and controlled variation

Each production repeats one section three times from **one published motion clip**, varying only declared parameters: formation and cast membership in A, gaze direction and tempo in B. This is what `RISK-20` tests — publishing a corrected clip must invalidate all three refrains through the dependency graph, and no compiled refrain may retain an embedded copy that survives the correction.

The refrains are deliberately the longest shots. If reuse is baked rather than linked, this is where it shows.

## Continuity

`RISK-40` holds across every cut: cast membership, placement, prop state, expression and camera relationship. Two continuity chains are deliberately long-range and cross the repeated sections, so a break is visible rather than plausible:

- **A:** the ball's holder changes exactly twice — `pim` → `bo` at A04, `bo` → the cart at A08 — and is otherwise constant. Any shot showing the ball with the wrong holder fails.
- **B:** `mochi` has the ball from B01 to B08. It must be off-frame or visibly concealed in every shot between, and the reveal must be its first visible appearance.

## The structured correction

`RISK-35` requires the invalidation set to be recorded **before** the run. The correction is applied to Production A.

**Correction:** rewrite one lyric line in A04.

**Must invalidate, and nothing else:**

- A04's compiled shot
- A04's viseme track
- the caption cue covering 0:46–1:02
- the textless render for that range
- the vocal stem segment for that range

**Must not invalidate:** A03, A06 and A09, which reuse a different motion clip and different lyrics; any other shot; the cast; the rig; the asset lock.

**Contrast case, recorded but not applied:** changing `mochi`'s `tail_mid` rest angle would invalidate every shot `mochi` appears in — A01, A03, A05, A06, A09, A10. The two blast radii are disjoint in shape, one narrow and time-bounded, one broad and asset-bounded. A dependency graph that cannot tell them apart fails the assertion regardless of which one it over-invalidates.

## Audio dependency

**Neither production can be produced yet, and this is the brief's blocking gap.**

Charter Objective 1 requires the benchmark to be generated "from locked audio, timed lyrics, and versioned asset packs". Both productions are music videos with sung vocals, which pulls in the full `RISK-49` set. Each requires:

- an **original** song — `RISK-10` forbids copying protected music, and the YouTube rule in `.sandbox/README.md` forbids taking audio from a reference channel;
- vocals and instrumental **split from the session onward**, because `RGT-S009` section 8 establishes that a stereo bounce cannot be separated afterwards;
- timed lyrics, and phoneme intervals that resolve to the eight visemes the cast carries and to no others;
- a beat map for A07 and B09.

None of this exists, and the cast build does not produce it. A sandbox-sourced track cannot stand in even temporarily: `RISK-09` fails any fixture that resolves to a `.sandbox/` path, and a track used once tends to stay.

**Route:** original composition with stems, provenance recorded in `PROVENANCE.json` before any shot is compiled. Until then the shot lists above are timed against intended musical structure rather than against a real waveform, and every timing in this document is provisional.

## What this brief does not settle

- **Shot-plan representation.** `PR-C004` is a hypothesis and `SPIKE-A001` owns where direction ends and rig control begins. This brief states direction in semantic actions — walk, pass, react, play the beat — and names joints only where a contact must be asserted. It does not propose a shot-plan schema.
- **Every stimulation limit.** The profile fields are fixed; the values are evidence-pending and belong to the calibration plan.
- **Whether the story is any good.** `RISK-60` records that as a review judgement no fixture makes, and blind review is waived.
