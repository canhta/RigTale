# Small-Studio 2D Cutout Workflow Evidence

**Evidence owner:** `SPIKE-W001` Part A (`RGT-S009`). Desk research only. All sources accessed 2026-08-02.

## Evidence Labels

Every statement carries one label. An unlabelled statement is a defect.

| Label | Meaning |
|---|---|
| `[FACT]` | Directly stated in a cited primary or official source that was retrieved |
| `[REPORTED]` | A first-hand practitioner account, attributed; one person's experience, not a general truth |
| `[INFERENCE]` | Reasoning from cited facts, with the reasoning stated |
| `[HYPOTHESIS]` | Plausible but unevidenced |
| `[UNKNOWN]` | An open question with no source found |

Desk research establishes what published sources document about tool-supported workflows. **It cannot establish what any specific two-to-five-person team actually does, what it spends time on, or what it would change.** Every claim about user behaviour here is a hypothesis, and stays one permanently: `RGT-S009B`, the only route to testing them, was rejected by owner decision on 2026-08-02.

## Headline Findings

Three results matter more than the rest, and two of them are adverse to RigTale.

1. **There is no published time or cost baseline for small-team 2D cutout production.** The charter's "at least 50% reduction" claim currently has nothing external to be measured against, which makes it not merely unproven but **unfalsifiable**. That is a credibility risk independent of whether the claim is true.
2. **The scene-assembly work RigTale proposes to automate is already largely automated for Toon Boom users**, and cutout as a technique already claims the time-saving RigTale claims. RigTale's 50% must be measured against an already-optimised baseline.
3. **Rig-change propagation is a documented, unsolved failure mode in the dominant cutout tool**, and automating shot production would amplify it. This is a design requirement for RigTale, not an optional feature.

## Source Provenance

An earlier draft cited seven sources that were never retrieved; they were withdrawn and recorded as open tasks. **Five have since been retrieved directly and are now incorporated:**

| Source | Status |
|---|---|
| Blender Manual, Library Overrides and Link/Append | **Retrieved.** Section 5. |
| Blender Studio pipeline and asset-versioning docs | **Retrieved.** The pipeline path redirects rather than being empty; successor pages read. Section 5. |
| Animation Guild / IATSE 839 Master CBA 2024–2027 and wage schedule | **Retrieved**, 215 pages, full-text searched. Section 6. |
| ADADA journal paper | **Retrieved.** The earlier parse failure was a tooling issue. Section 6. |
| YouTube monetization and made-for-kids policy | **Retrieved by direct fetch**, replacing search-index extraction. Section 8. |
| Netflix textless and M&E guidelines | **Retrieved by direct fetch.** Section 8. |
| PBS Distribution technical specifications; Discovery textless guide; AMWA AS-11 UK DPP | **Still not retrieved. Nothing rests on them.** The Netflix material now covers the same architectural question. |

**Remaining limitation:** `helpx.adobe.com` timed out on all fetch attempts, so the Adobe Character Animator and Adobe Animate statements in section 7 come from search-index extraction and are weighted medium. They must be re-verified by direct retrieval before informing any requirement or decision record. No conclusion in this document depends on them alone.

## 1. Source Inventory

| Source | Type | Weight |
|---|---|---|
| Toon Boom LEARN, "Cut-out Animation Workflow" (T-PRIN-003-012) | Vendor training | High — the only end-to-end published cutout workflow map found |
| Toon Boom LEARN, "Job Descriptions" (T-PRIN-003-013) | Vendor training | High, for roles and gates |
| Harmony 25 Premium docs: About, Animating Lip-Sync, Importing Sound, How to Animate a Cut-out Character, About the Master Controller, Importing Templates | Vendor docs | High |
| Harmony 22 Premium docs: About Templates, How to Rig a Cut-out Character | Vendor docs | High / Medium |
| Harmony 25 Advanced, "About the Library & Templates" | Vendor docs | High |
| Storyboard Pro 25, "Exporting Harmony Scenes" | Vendor docs | High |
| Toon Boom Producer 22 and 26, Workflows and Processes | Vendor docs | High, but a large-studio tool |
| Kitsu (CGWire), "Status, publish and review" | Vendor docs | Medium |
| Blender Studio pipeline: Design Principles, Pipeline Usage, Shot Assembly | Published studio pipeline | High, but 3D and 10–20 people |
| Blender Studio: "Task Review", "2D Assets" | Published studio pipeline | **Nil — both are empty stubs marked under edit since October 2023** |
| OpenToonz User Manual | Official docs | Medium-High |
| Moho manual, Tutorial 5.1–5.2; Moho features page | Vendor docs / marketing | Medium / Low |
| Rhubarb Lip Sync README | Project docs | Medium-High |
| Toon Boom interview, Jamie Greene, rigging artist | Vendor-published first-hand account | Medium — `[REPORTED]` |
| Moho Featured Artist: Amblagar Studio; Moho webinar listing for *Bobo English* | Vendor-published studio account | Medium — `[REPORTED]`, the only traceable throughput figure found |
| Moho user forum threads | Practitioner forum | Low-Medium — `[REPORTED]`, individual accounts |
| Purwaningsih, ADADA Vol.21 No.1, "Optimizing 2D Animation Production Time" | Academic | **Nil — PDF could not be parsed; zero content extracted. Do not cite.** |
| Netflix Partner Help Center; YouTube Help monetization and "made for kids" | Distributor / platform policy | Low-Medium — search-index extraction only |
| Lesterbanks write-up of the *Puffin Rock* Moho pipeline talk | Secondary trade write-up | Low — secondary, large studio |

`[INFERENCE]` That a single vendor's training material is the only end-to-end published cutout workflow map is itself a finding about how thin this literature is.

## 2. Documented Small-Team Cutout Workflow Map

All from the Toon Boom LEARN cut-out workflow page unless noted.

`[FACT]` Stage sequence: Script → Designs → Colour styling → Audio recording → Storyboard → Animatic reel → Background layout → Background painting → Character and prop rigging → Library → Scene setup → Animation → Compositing → Export/render → Post-production.

`[FACT]` Tool boundary: "Other than scripting and recording, every other step in the cut-out workflow should be done in the animation software."

`[FACT]` Parallelism is documented as a property of cutout specifically: "multiple assignments can be done simultaneously, especially during the design and development stage… it is possible for a team to do both the storyboard and designs at the same time, as compared to a traditional workflow where the storyboard artist must have all the models ready before starting."

`[FACT]` Ordering constraints: designs are authored in-tool because "whatever the breakdown technique chosen, the lines will be the same style, the palette will already be created and it will be less work to break down and rig"; "The colour styling must be done before the animation and character breakdown"; and if there is dialogue, "the final version must be recorded soon enough to import it into the project before the animation."

`[FACT]` Storyboard is not required to be on-model in cutout: "the characters and props used for the animation are puppets, which always remain on model."

`[FACT]` Rigging role and artifact: the rigger takes the final model and "start[s] building the puppet… deciding which parts will be separated and preparing all of the joints and views for the animators", then "stores them in the library as templates to be shared with the rest of the team."

`[FACT]` **Rigging is documented as the highest-consequence step**, warned twice in adjacent paragraphs: "This step must be done with care because these puppets will be distributed among all the animators later and you do not want to duplicate mistakes throughout the project… these puppets will be duplicated over and over throughout the whole project." No other stage receives this treatment.

`[FACT]` The library is a named, staffed role: "Someone should be assigned to manage the library so that it remains well organized… It is essential that this job be done correctly in order for the team to remain efficient throughout production."

`[FACT]` Scene setup is a clean handoff: "the person working on the scene setup will import the assets needed for the scene animation, as well as import the animatic reference and often position the camera. When the scene setup is completed, the scene can be passed on to the animator who can start animating without having to mount the scene."

`[FACT]` Rig and animation technique are coupled: "The animation technique has to conform with the rigging technique. The studio must establish its profile in order to determine which direction to take."

`[FACT]` **Small-team role collapse is documented at three points:** background painting done by one person; "In a small team, the animators will animate their own effects"; "On a small team, the animators will probably do their own compositing."

`[FACT]` OpenToonz documents cutout as a technique — Skeleton tool, pivot points, hierarchical links, Build Skeleton / Animate / Inverse Kinematics modes — but publishes **no** production-workflow map for cutout.

## 3. Documented Time and Revision Hotspots

`[FACT]` Lip sync is named a hotspot by the vendor: "it is also a particularly tedious part of the animation process."

`[FACT]` Compositing is documented as harder in cutout than other 2D forms: "Compositing is generally a bit more advanced and complex for a cut-out production than for a traditional or tradigital one."

`[FACT]` Retakes are a first-class production object: the Animation Director "coordinates the revision and retake process with the animators."

`[REPORTED]` Rig preparation is measured in days to weeks per character. Rigging artist Jamie Greene, in a Toon Boom-published interview: "you might have this assignment for five days to a couple of weeks, at times." He describes rigging as "the bridge between animation and design" and notes that "the design includes certain elements that might actually hinder artists." This is studio TV work with a dedicated specialist, not a two-to-five-person team.

`[INFERENCE]` Rig defects are the most expensive revision class available: discovery is downstream, and the blast radius is every shot using the rig.

`[UNKNOWN]` **No source ranks cutout stages by measured hours.** No vendor, studio, paper, or talk publishes a per-stage time breakdown. Any RigTale claim about which stage costs most is currently unevidenced.

## 4. Approval Gate Evidence

`[FACT]` Two gates are documented in the cutout workflow itself: storyboard "completed, approved and locked" before the animatic, and animation "completed and approved" before compositing. Also: "Only one person is in charge of the animatic production to ensure consistency throughout the whole production."

`[FACT]` Toon Boom Producer models gates formally: "There are 2 main types of processes: Manual and Approval… The Approval Process is used when work created during a manual process needs to be reviewed by a supervisor. The supervisor will then update the status to Approved or Retake."

`[FACT]` Kitsu documents waiting-for-approval → Retake or Approved, with artists setting the request and supervisors setting the outcome.

`[FACT]` Blender Studio documents a concrete render gate: "Approve Render will copy the Image Sequence of your flamenco render to the shot_frames directory", after which approved renders import to the edit.

`[FACT]` **Explicit scope caveat:** Blender Studio states its pipeline is "designed to facilitate a small production unit (10-20 people)."

`[INFERENCE]` That is two to four times RigTale's target team size and it is 3D. It is the best-documented pipeline available and it is still **not** evidence about a two-to-five-person 2D team.

`[INFERENCE]` Producer, Harmony Database, and Kitsu all presuppose a supervisor role distinct from the artist, and all are multi-user server systems. A team where "the animators will probably do their own compositing" plausibly has no such separation — but no source confirms or denies this.

`[UNKNOWN]` **No primary source and no first-hand account was found documenting the approval-gate model actually used by a two-to-five-person 2D cutout team.** Targeted searches returned only vendor marketing and content-farm output.

**This is the largest single evidence gap in the spike, and it sits directly on a core RigTale design decision: where the human approves.** `PR-F002` in the product requirements is classified `hypothesis` for exactly this reason, and now stays that way permanently.

## 5. Rig Reuse and Versioning — A Documented Unsolved Failure Mode

`[FACT]` Harmony master templates store "the entire rig, structure, drawings, and keyframes of the different poses of your puppet into a single asset", and should be created from the Node view because "Templates created from the Timeline view may lose the extra connections, effects and groupings."

`[FACT]` Action templates store reusable motion — "you can reuse head positions or a leg animation from a walk-cycle and place them inside other animations" — but "cannot be used on [their] own since [they do] not contain all the information required to rebuild the puppet skeleton and advanced connections."

`[FACT]` **Structural fragility:** "The combination of master and action templates will function as long as the layer order and connections are the same."

`[FACT]` **Templates are copies, not links**, verified verbatim: "Dragging a template into your scene copies the content in your Timeline and does not link it to the original." And: "A template is an individual copy of the artwork stored in the library which you can reuse in different scenes."

`[INFERENCE]` **Fixing a rig in the library therefore does not propagate to shots already built.** Rig-revision cost scales with the number of shots already produced. This is a documented structural failure mode for episodic reuse in the dominant cutout tool.

`[INFERENCE]` **This is adverse to RigTale in a specific and actionable way.** Automating shot production increases the number of shots invalidated by any subsequent rig change. RigTale would amplify this failure mode unless shots pin explicit asset versions and a dependency graph identifies exactly what a rig change invalidates. That is a design requirement, and it is already expressed in `PR-O03` and `PR-Q004` — this evidence raises its priority rather than adding a new one.

`[REPORTED]` The one first-hand account of cross-episode rig evolution retrieved, from Amblagar Studio: "By using character rigs that were being improved along the way, storing them in a server for all animators to be updated with the latest version, and with an ever-increasing actions library we were able to gain production speed and animation quality week by week."

`[INFERENCE]` That describes solving rig-version propagation **socially** — a shared server plus a convention that animators pull the latest — not through tooling.

`[UNKNOWN]` **Style drift across episodes:** no vendor documentation treats model sheets or style guides as an enforceable cross-episode consistency control. Toon Boom documents the Art Director as the human who "ensures the consistency of that look" — a person, not a mechanism.

### The opposite architecture, and what it costs — now retrieved

Blender's linked-library system is the live-link counterpart to Harmony's copy model, and Blender Studio runs a real production on it. Retrieved directly on 2026-08-02.

`[FACT]` Link "creates a reference to data in a source file such that changes made there will be reflected in the current file the next time it is reloaded." Append "copies data-blocks into your blend-file without keeping any reference to the original ones… changes in the external source file will not be reflected."

`[INFERENCE]` Blender's Append is functionally the same architecture as Harmony templates. Link is the opposite.

`[FACT]` Library Overrides is "designed to allow editing linked data, while keeping it in sync with the original library data… **When the library data changes, unmodified properties of the overridden one will be updated accordingly.**"

`[INFERENCE]` **That is the operative rule: unmodified properties keep tracking the library; modified ones stop tracking.** It is the mechanism RigTale needs for per-shot deviation without mutating a published rig.

`[FACT]` Blender Studio's stated design principle is explicit: "When working on Blender-centric pipeline, we rely on Blender's linking system, limit the usage of caching as much as possible." Its animation guide treats rig churn as normal — "Assets are continuously updated during production so it is important to keep rigs and props up to date" — and names "Asset updates" as a budgeted stage between blocking and polishing.

#### The failure mode this trades into

`[FACT]` **The central documented risk**, verbatim: "While resyncing a library override it is possible that **edited overrides get deleted** if they are changed in the original library. If this is the case, a warning message will be displayed stating how many overrides were deleted, if the deletion is undesirable **the resync can be undone before saving** the blend-file."

`[FACT]` Resync "are automatically resynced if needed on blend-files opening."

`[INFERENCE]` **Live-link does not remove the rig-propagation problem; it converts a *staleness* failure into a *reconciliation* failure.** Harmony fails silently by leaving shots stale. Blender fails by deleting a shot's hand-made overrides when the library changes the same data.

`[INFERENCE]` **This is the sharpest risk for an agent-operated studio specifically.** The documented recovery is undo-before-save, and resync runs automatically on file open. **A pipeline that opens, processes, and saves a shot non-interactively consumes that recovery window without any human seeing the warning.** RigTale must therefore treat resync as an explicit, inspected step with a machine-readable diff, never as an implicit side effect of loading.

`[FACT]` A harsher variant exists for hierarchy-mismatched files: Resync Enforce "is more forceful, aggressive, at the cost of a potential loss of some overrides on ID pointers properties."

`[FACT]` Overrides also constrain *where* deviation may live: "most notably Edit Mode is not allowed for overrides"; overridden actions "only support a very limited amount of editing… an existing F-Curve can be muted, but its keyframes cannot be edited, and no new F-Curve can be added"; and replacing an action "will completely replace the keyframed animation from the linked data… not override it in any way."

`[INFERENCE]` Any shot-level change that is topological, or that edits keyframes on animation authored in the library, cannot be expressed as an override. It forces either a library change affecting all shots, or Make Local — which drops straight back to the copy architecture.

#### Two mitigations, both documented rather than invented

`[FACT]` **Keep authored animation out of the library rig.** "In general, an override can do much more with its animation data if no animation data exists in its linked reference data-block."

`[FACT]` **Pin shots to versions.** Blender Studio's Active publish class allows "multiple version can be published if some shots require an older version of the current asset."

`[INFERENCE]` **Version pinning is the escape valve that makes live-link survivable — shots are not forced onto the latest rig.** This directly corroborates the `PR-O03` requirement change recorded in the product requirements: pinning plus dependency invalidation is not a convenience, it is what makes either architecture workable.

`[FACT]` Hierarchy stability is a hard constraint, not a style preference: "For library overrides to work well, it is much better if all the collections needed by the character are children of the root… Otherwise, some data may not be properly automatically overridden."

`[INFERENCE]` A fixed-cast rig standard would need hierarchy stability enforced as a validation gate.

`[UNKNOWN]` No retrieved page quantifies how often resync deletes overrides in practice, or gives a measured cost for asset-update stages per shot.

## 6. Time and Cost Data — A Null Result

Stated plainly: **there is essentially no citable published data on production time or cost per finished minute for short 2D cutout work at small-team scale.** This is recorded as a finding.

`[REPORTED]` The only traceable throughput figure is a vendor-published studio account. Amblagar Studio on *Bobo English* (396 episodes × 4 minutes): the webinar page states "an ambitious target of 80 minutes of completed animation each month", and the studio states "in the end we achieved a total of +1100 minutes in 19 months."

`[INFERENCE]` That is roughly 58 finished minutes per month sustained over 19 months. **Team size is stated nowhere.** Without a headcount it cannot be converted to minutes per person-week, which is precisely the metric RigTale needs. As a baseline it is unusable in its current form.

`[FACT]` **The one academic candidate has now been retrieved and read.** Purwaningsih, "Optimizing 2D Animation Production Time in Creating Traditional Watercolor Looks by Integrating Traditional and Digital Media", ADADA Vol.21 No.1, pages 57–62.

`[FACT]` Methodology is a single practice-based case study, **n = 1**, produced by one person: one animated short combining hand-painted watercolour backgrounds with digital frame-by-frame character animation. Evaluation was a screening with qualitative feedback on pacing and look.

`[FACT]` Reported figures: runtime "3 minutes and 9 seconds"; production "done individually and completed in around 3 months of work"; "12 different backgrounds"; "The process to finalize all of the backgrounds and foregrounds took 3 weeks to complete."

`[FACT]` **There is no baseline, no control condition, no comparison against an all-digital pipeline, no time logs, and no per-shot timing data.** The conclusion is asserted, not measured: "it is safe to assume that this strategy has optimized the production time".

`[FACT]` The published PDF's first page contains unedited journal-template placeholder material, including a lorem ipsum abstract and a placeholder author affiliation.

`[INFERENCE]` The only derivable ratio is roughly **one finished minute per person-month**, from a single uncontrolled observation. It is also poor transfer to RigTale: hand-drawn frame-by-frame animation with hand-painted backgrounds for a one-off short — **not cutout rigging, not a recurring cast, not multi-episode reuse, not team production.** Citing it as evidence for RigTale's throughput claims would not be defensible, and the leftover template text indicates weak editorial control at the venue.

**The null result therefore stands, now on a retrieved rather than an unavailable source.**

`[FACT]` Every general search for cutout production time or per-minute cost returned animation-studio marketing pages quoting their own numbers.

`[INFERENCE]` Those vendors have a direct commercial interest in the figures and publish no methodology. They are unusable as evidence.

`[FACT]` Academic index searches surfaced only generative-AI-for-animation papers and AI-adoption surveys — none measuring baseline human cutout production time.

`[UNKNOWN]` **Minutes of finished 2D cutout animation per person-week at two-to-five-person scale: no citable source exists.**

### The union agreement: a price of labour, but no sanctioned rate of output

Retrieved directly on 2026-08-02: the Animation Guild / IATSE Local 839 Master CBA for 2024–2027, 215 pages, and the master wage schedule.

`[FACT]` The agreement is in force, and the wage period beginning 2026-08-02 is current. Rates are published per classification. For the current period, hourly and weekly journey rates include Animator at $64.94 / $2,597.60; Digital Animator I at the same; Digital Animator II and Animation Checker at $55.58 / $2,223.20; Animation Timer at $61.01 / $2,440.40; Breakdown at $48.80; Inbetweener at $47.01; Painter at $46.18. Daily employees receive 118.583% inclusive of vacation and holiday pay, and pension contributions assume a 60-hour on-call week.

`[FACT]` **A full-text search of the 215-page agreement and the wage schedule found: quota 0 hits, footage 0, productivity 0, piece rate 0, piecework 0, workload 0, incentive 0.** The four "output" hits are all in the article on AI systems and refer to AI output, not worker output. Extraction covered 214 of 215 pages; the one image-only page was inspected visually and is the signature page.

`[FACT]` One genuine footage-based norm does exist, for freelance timing: "$4.63/foot… 8 hours/70 feet". `[INFERENCE]` At 16 frames per foot and 24 frames per second that is roughly 46.7 seconds of timed footage per eight-hour day. But it is a **benefits-accrual conversion**, not a required minimum output, and it is explicitly sunset — "not applicable on or after January 1, 2025."

`[FACT]` The one true minimum-staffing article is a **headcount** minimum for writers, not an output minimum.

`[INFERENCE]` **The CBA gives a defensible price of labour and no sanctioned rate of output.** Since January 2025 the agreement contains no footage-per-day standard at all. Any minutes-per-artist-week denominator RigTale uses must be sourced elsewhere and **cannot be attributed to the CBA**.

`[UNKNOWN]` The union site also lists roughly forty employer-specific memoranda and legacy agreements that were not opened. A footage quota in a studio-specific sideletter would not be covered by this null result.

**Consequence.** RigTale's 50% reduction claim has no published baseline. Both candidate external sources have now been retrieved and both fail to supply one: the academic paper is an uncontrolled single case in a different technique, and the union agreement prices labour without rating output. The baseline must be generated in-house, which is exactly what `docs/research/manual-baseline-protocol.md` specifies. Until that protocol runs, the claim is unfalsifiable — a business risk regardless of its truth, and the reason the protocol's bias controls matter.

## 7. Lip Sync and Audio Synchronisation

### Settled position

`[FACT]` Automatic phoneme-to-mouth assignment is a commodity, present in Harmony, Moho, OpenToonz, Cartoon Animator, Adobe Character Animator, and Adobe Animate. It is not a differentiator.

`[INFERENCE]` But in every tool it is a populate-then-correct pattern, and the vendors treat automatic output as a draft.

`[FACT]` Every one of the five commercial tools ships a dedicated manual-correction interface: Harmony's "Modifying the Lip-sync Detection", Moho's Switch Selection window, Cartoon Animator's Lips Editor, Character Animator's viseme timeline, Adobe Animate's Frame Picker.

`[FACT]` **Harmony's automation performs exposure-sheet assignment only.** It "does not create mouth drawings" and requires a pre-existing, correctly named A–X mouth set.

`[INFERENCE]` That matters more than it appears: the automated step presupposes the manual asset-preparation step. The tool automates the cheap half and requires the expensive half as input.

`[FACT]` Lost Marble's own manual calls the method "quick and easy, though not always super-accurate" and requires audio "without background noise or music", recommending external tools for better results.

`[FACT]` Rhubarb, the engine behind Moho's and OpenToonz's automatic lip sync, documents its limits: PocketSphinx "only recognizes English dialog"; the language-independent recogniser is "less precise"; "It is always a good idea to specify the dialog text."

`[FACT]` Adobe's framing implies audio-only detection is weaker: computing lip sync from audio *and* transcript "should produce more accurate visemes… than if no transcript was used."

`[FACT]` OpenToonz requires an external Rhubarb binary, supports only Preston Blair mouth-shape names, and its documentation is explicitly work-in-progress with no accuracy guidance. Adobe Animate's Auto Lip-Sync uses 12 visemes, requires poses on a single Graphic symbol, and the mapping is manual. Cartoon Animator caps audio import at 30 minutes and preserves manual keys. "AccuLips" is documented for iClone, a 3D product, **not** for Cartoon Animator.

### Practitioner accounts conflict

`[REPORTED]` A Moho user states the built-in automatic lip sync picks wrong phonemes "at least 70% of the time" even with clean isolated voice-over. A forum moderator states: "Usually you will need to adjust those a bit." A Character Animator practitioner blog states that editing visemes "can add many tedious hours (or days) to the process."

`[REPORTED]` **Directly contradicting these**, another practitioner in the same forum states that manual keyframing "only takes me a few minutes to get through each scene, and it's way more accurate than any audio-based lip-sync system I've tried", adding: "lip-sync is the easy part… the challenging part is selling the performance, which is everything else happening with the character."

`[UNKNOWN]` No vendor and no published postmortem quantifies the cleanup rate. The 70% figure is a single unverified forum claim.

`[INFERENCE]` Lip sync is a **weaker counter-argument against RigTale than it first appeared, but for an uncomfortable reason.** If manual lip sync genuinely takes minutes per scene, it is neither a bottleneck nor a differentiator, and automating it buys little either way. The more interesting claim is that the cost is body performance and staging — precisely the harder half of what RigTale proposes to automate, and the half with no evidence that structured direction reaches publishable quality.

`[FACT]` Harmony documents the audio hygiene that makes localisation possible: "keep your soundtrack separated in tracks for music, sound effects and characters."

## 8. Platform Policy and Localisation — Now Directly Retrieved

All pages in this section were retrieved by direct fetch on 2026-08-02, replacing the earlier search-index extraction.

### YouTube: the repetitive-content claim is CONFIRMED — and narrower than first framed

`[FACT]` The section "Generic or repetitive content" on `support.google.com/youtube/answer/1311392` lists these violations verbatim:

1. "Similar or repetitive content with low educational value, commentary, narratives, or minimal variation across videos"
2. "Videos where characters are put in the same situation over and over again with the same outcome (i.e., using a highly similar storyline template across multiple videos)"
3. "Image slideshows, templated storylines, or scrolling text with minimal or no narrative, commentary, or educational value"
4. "AI-generated content made with generic or unoriginal templates giving the impression of mass production without adding the creator's original, authentic insights or perspective"

The earlier unverified extraction merged bullets 1 and 2 into one quote. That was the only inaccuracy; the language exists.

`[FACT]` **The "What is allowed" bullets in the same section were missing from the earlier extraction and change the reading materially:**

- "The same intro and outro for your videos, but the bulk of your content is different"
- "Similar content, like a series following a set of characters across episodes or a channel that does product reviews, but in which each video has a distinct storyline, focus or concept"

`[INFERENCE]` **The policy does not prohibit a recurring cast, an episodic series, or reusable production templates.** A series following a set of characters across episodes is expressly named as allowed, and reusable *production* templates — rigs, layouts, pipelines — are nowhere addressed; the policy governs the viewer-visible artifact, not the toolchain.

The prohibition is scoped to **narrative** sameness: same situation, same outcome, same storyline template, minimal variation. The test the page applies is whether "each video has a distinct storyline, focus or concept".

`[INFERENCE]` **The adverse part is real but narrower than first stated, and it is quotable by an adjudicator.** It constrains the narrative axis specifically, and it bites hardest on exactly the genre RigTale targets, because children's music formats are conventionally repetitive by design — same song structure, same lesson shape, same resolution. Bullet 1's "low educational value" qualifier cuts the other way for genuinely educational content, but that is a judgement call at review time, not a bright line.

`[INFERENCE]` **Bullet 4 compounds it.** An agent-operated studio sits squarely in the category YouTube singled out, so RigTale's output plausibly attracts scrutiny that a human studio producing identical episodes would not.

**Correction to the earlier framing in this document:** the claim was not "directly adverse to a generate-many-similar-episodes-from-templates strategy" without qualification. Templates and recurring casts are fine; **narratively interchangeable episodes are not.**

### YouTube: made-for-kids is a structural revenue constraint

`[FACT]` Designation is mandatory and legally consequential: "Failure to set your content appropriately may result in consequences on YouTube or have legal consequences under COPPA and other laws."

`[FACT]` Content is made for kids where children are the primary audience, or where it has "actors, characters, activities, games, songs, stories, or other subject matter that reflect an intent to target children". Stated factors include child-oriented activities "including games, songs, early education".

`[FACT]` Features unavailable on made-for-kids content include personalised advertising, comments, the notification bell, cards and end screens, channel memberships, Super Chat, merchandise and ticketing, the donate button, live chat, save-to-playlist, and autoplay on home.

`[INFERENCE]` For RigTale's target segment this status is **unavoidable** — children's music and educational animation with songs and characters is squarely inside the definition. It removes personalised advertising and every direct-monetisation and audience-retention surface except ads and off-platform channels. **This is a structural constraint on the positioning, independent of the templating question**, and it was not previously recorded anywhere in RigTale's documentation.

### Netflix: split stems are a hard architectural constraint

`[FACT]` Music and effects delivery is required: "Please deliver a fully-filled Music & Effects Package as long-play, discrete channels". Required assets include an M&E track, optional tracks, a dialogue guide, and a print master. "Do not modify Music levels at all".

`[FACT]` **Directly on point for a music show, sung vocals do not stay in the M&E.** Optional tracks must carry "Vocals from a character singing on-screen" and "Vocals from performances original to or produced for show", while the M&E body carries "Background music exactly as it is represented in the original language mix".

`[FACT]` Textless picture is required for IMF and servicing packages, covering "any graphic and/or animated text that occurs over picture" — with carve-outs for text over pure black or white frames, text that was part of visual-effects composites, and in-story brands.

`[INFERENCE]` **This is the sharpest architectural constraint found in the entire spike.** For a children's music show the instrumental bed belongs in the M&E, but **every sung vocal — including character songs, which are the core of the format — must be deliverable as a separate optional track and again as a dialogue stem.** That is achievable only if songs are produced with vocals and instrumental permanently split from the session onward; **it cannot be reconstructed from a stereo song bounce.**

The same applies to picture: on-screen lyric text and animated word overlays need removable layers. The visual-effects-composite carve-out is a plausible route for stylised in-world text.

`[INFERENCE]` **Retrofitting either is impractical, so both must be designed into RigTale's audio and text contracts now, not deferred.** This affects `PR-F003` and the `AudioTimeline` contract directly.

`[UNKNOWN]` How YouTube actually enforces the narrative-sameness bullet against educational children's series — enforcement rates, appeal outcomes, or whether "distinct storyline" is read generously for preschool formats — is not addressed by any retrieved page.

`[UNKNOWN]` **No animation tool vendor documents a multi-language project-versioning workflow.** Not Toon Boom, not Moho, not Reallusion, not Adobe.

`[INFERENCE]` This cuts both ways: it may be unclaimed opportunity, or it may be unclaimed because small teams simply do not localise.

## 9. Evidence Against RigTale's Premise

Recorded in full, because a red-team that only confirms is not a red-team.

1. `[FACT]` **The time-saving claim already belongs to the vendors.** Toon Boom: "A cut-out production (digital puppet animation) reuses a lot of assets, saves time, keeps a maximum amount of work in the same studio and reduces the amount of resources and budget needed." `[INFERENCE]` RigTale's 50% must be measured against an already-optimised cutout baseline. If the comparison drifts toward frame-by-frame animation, the claim becomes trivially true and commercially meaningless. The baseline protocol's fairness rules exist to prevent exactly this.
2. `[FACT]` **In-betweening is already automatic:** "you can move your character's parts to make your key poses, and let Harmony create the in-betweens."
3. `[FACT]` **Motion and pose reuse already ship:** Harmony action templates, the library system, Moho Actions, Cartoon Animator motion templates.
4. `[FACT]` **Pose authoring is already automatable in Harmony.** Master Controllers exist so that "For complex characters with many deformations, this removes the need for the animator to create poses manually." `[FACT, mitigating]` But they are "created and configured entirely through the scripting interface", and Toon Boom recommends that route "only… if you have solid bases in scripting." `[INFERENCE]` Realistically out of reach for a two-to-five-person team without a technical director — so this is weaker counter-evidence than it appears, and a genuine RigTale opportunity.
5. `[FACT]` **Scene setup is already substantially automated for Toon Boom users.** Storyboard Pro "can automatically export each scene in your project into a scene that can be opened in Harmony… they will contain each of their panels so that you may animate over them, and they will contain their respective part of the animatic's soundtrack", including "drawings, 3D objects, images, videos and camera movements." `[INFERENCE]` For teams on the Toon Boom stack, much of the scene-assembly work RigTale proposes to automate is already done. **This does not apply to Moho or Cartoon Animator users, which may define RigTale's real addressable segment.**
6. `[FACT]` Automatic lip sync exists everywhere and is not a differentiator.
7. `[INFERENCE]` Items 2, 3, 5, and 6 together cover a substantial share of the repetitive work RigTale targets. **The unautomated residue is smaller than a naive reading of "manual 2D cutout workflow" implies.**
8. `[FACT + REPORTED]` The bottleneck evidence points at asset and rig preparation rather than animation — see the assessment below.
9. `[FACT]` Rig-change propagation is unsolved in the dominant tool, and automation amplifies it (section 5).
10. `[UNKNOWN]` No published baseline exists, so the 50% claim cannot currently be falsified.

### Assessment: is asset and rig preparation the dominant cost?

**The available evidence leans yes, but it is thin and cannot be settled by desk research.** Recorded as a live threat to the value hypothesis, not as a proven fact.

**Supporting.** `[FACT]` Toon Boom singles out rigging as the step that "must be done with care" because errors propagate to every animator and shot, and repeats the warning twice; no other stage gets this. `[FACT]` The library holding rigs requires a dedicated owner. `[FACT]` Designs must be authored in-tool specifically to reduce downstream rig work, and colour styling must precede breakdown — two upstream stages whose stated purpose is serving the rig. `[REPORTED]` One rig takes "five days to a couple of weeks." `[REPORTED]` Amblagar attributes throughput to rigs "being improved along the way" plus a growing actions library — asset infrastructure, not per-shot animation speed.

**Undercutting.** `[FACT]` The rig-time figure is studio TV work with a dedicated specialist, vendor-published. `[INFERENCE]` Rig cost is a **fixed** cost amortised across a series with a recurring cast — exactly RigTale's scenario — so its share of per-episode effort could be small after the first episode or two. Nobody has measured the amortisation curve. `[FACT]` Compositing is flagged as more complex in cutout and lands on animators in small teams, so per-episode effort may concentrate there instead.

**Consequence.** `[INFERENCE]` RigTale's hypothesis assumes assets are already published — it begins *after* the stage with the strongest documented evidence of cost and risk. If rig preparation dominates even after amortisation, RigTale targets the wrong bottleneck. If it amortises to near zero by episode three, the hypothesis is sound. **This question should gate go, revise, or stop.** It is question 2 in section 11.

## 10. Ranked Candidate User Problems

Each carries the evidence that would confirm or refute it. None is established.

| # | Problem | Label | Confirm | Refute |
|---|---|---|---|---|
| 1 | Rig and asset preparation is the dominant up-front cost and highest-risk defect source | `[REPORTED]` | Time logs from 3+ small teams separating one-time rig hours from per-episode hours, rig prep still >25% by episode 5 | Rig prep amortises below ~10% of per-episode effort after episodes 2–3 |
| 2 | A rig change after shots exist invalidates finished work, and no cutout tool solves it | `[FACT]` | Practitioners report re-doing or abandoning shots after rig fixes | Teams freeze rigs after episode 1 and it never materialises |
| 3 | Scene setup is repetitive but already automated for Toon Boom users and not for others | `[FACT]` | Moho and Cartoon Animator teams rank manual scene assembly top-3 by time; Toon Boom teams do not | Scene setup is under 10% of effort for everyone |
| 4 | Compositing is disproportionately complex in cutout and lands on the animator in small teams | `[FACT]` | Small teams rank compositing and render in their top two time sinks | Compositing is templated per series and near zero after setup |
| 5 | Lip-sync residual correction cost is unmeasured and may be near zero | `[UNKNOWN]` | Measured cleanup minutes per minute of dialogue | Practitioners accept automatic output as-is, or skip it because manual is quicker |
| 6 | Localisation is blocked at authoring time by baked-in text and mixed-down music | `[UNKNOWN]` | Teams report re-opening finished scenes to build language versions | Teams publish in one language and never localise |
| 7 | Approval and review in a two-to-five-person team is informal and unmodelled | `[HYPOTHESIS]` | — zero primary evidence in either direction | — |
| 8 | Style drift across episodes is a real recurring-cast problem | `[HYPOTHESIS]` | — zero documentation found in any vendor or distributor source | — |

## 11. What This Document Cannot Establish

Desk research produced no measured time data, no small-team gate model, no cutout-specific stage ranking, and no localisation workflow. These were routed to `RGT-S009B`, which was **rejected by Project Owner decision on 2026-08-02** (`docs/requirements/charter.md`, Charter Revision 1).

**Every `[UNKNOWN]` and `[HYPOTHESIS]` label in sections 9 and 10 is therefore final.** No later work in this project promotes them.

**One question is answered by substitution rather than left open.** This document covers the segment's *animation* tools and says nothing about its *painting* tools, and `RGT-S014` needed that fact to choose an ingestion format. It could not be measured, so the ingestion decision was rested on **format reach across ingesting tools** instead: PSD is accepted by every ingesting tool verified, so choosing it does not require knowing which painting tool a user runs. The substitution is deliberate and is recorded in `PR-A003`.

The one question that carried the project's go/revise/stop test — how many finished seconds one person produces per week on an established series versus on episode 1, and after how many episodes rig-preparation cost stops mattering — is now answered by the owner-operated reference production instead, after implementation rather than before it.

## 12. Follow-Up Retrieval Tasks — Closed

All four tasks recorded when this document was first written have been completed. Their results are incorporated in sections 5, 6, and 8, and the provenance table above records what was and was not retrieved.

One task remains open and is **not** blocking: direct retrieval of the Adobe Character Animator and Adobe Animate documentation, currently held at search-index confidence.

## 13. Constraints This Spike Adds to Downstream Design

Recorded here because they change work that has not started yet. **Every constraint below is a design consequence, and the `Basis` column carries the label of what it rests on** — the constraint is never stronger evidence than its source. Where the basis is `[INFERENCE]`, the vendor or platform states the fact; the obligation is this spike's reading of it.

| Constraint | Basis | Source | Affects |
|---|---|---|---|
| Shots must pin explicit asset versions, and a dependency graph must identify what a rig change invalidates | `[INFERENCE]` from a `[FACT]` (§5) | Harmony templates are copies, verbatim: "Dragging a template into your scene copies the content in your Timeline and does not link it to the original". OpenToonz and Synfig reproduce the unlinked-reuse problem by different mechanisms; Blender's live-link alternative trades it for override deletion. That rig-revision cost therefore scales with shots already produced is the reading | `PR-O03`, `PR-Q004`, `SPIKE-CS001` |
| Any resync or reconciliation step must be explicit and inspected, never an implicit side effect of loading | `[INFERENCE]` from a `[FACT]` (§5) | Blender resync runs automatically on open, verbatim: overrides "are automatically resynced if needed on blend-files opening". Its documented recovery is undo-before-save. That this is a window an automated pipeline consumes silently is the reading | `SPIKE-A001`, agent-system design |
| Rig hierarchy stability must be a validation gate | `[INFERENCE]` from a `[FACT]` (§5) | Hierarchy stability is documented as a hard constraint, not a style preference; mismatch degrades to a lossy enforced resync. That a fixed-cast rig standard would need it enforced as a validation gate is stated as an inference at §5 | `SPIKE-A002` |
| Song vocals and instrumental must be split from the session onward, and on-screen lyric text must live on removable layers | `[INFERENCE]` from `[FACT]`s (§8) | Netflix requires sung vocals on separate optional tracks, and textless picture for IMF and servicing packages. That the split must exist from the session onward, because it cannot be reconstructed from a stereo bounce, is the reading | `PR-F003`, `AudioTimeline` contract |
| Episodes must differ on the narrative axis, not merely in assets | `[FACT]` (§8) | YouTube prohibits "a highly similar storyline template across multiple videos" while expressly allowing a recurring cast across episodes. The constraint restates the prohibition | Charter positioning, `SPIKE-F001` brief design |
| Made-for-kids status removes personalised advertising, comments, cards and end screens, memberships, Super Chat, merchandise, the donate button, live chat, save-to-playlist and autoplay on home | `[FACT]` (§8); that this leaves no direct-monetisation or audience-retention surface except ads and off-platform channels is `[INFERENCE]` | YouTube made-for-kids feature restrictions | Charter business case |

The last two are business constraints rather than technical ones and are raised for the Project Owner. They do not change the approved charter and no charter revision is proposed here. How YouTube actually enforces the narrative-sameness bullet against educational children's series is recorded `[UNKNOWN]` in §8.
