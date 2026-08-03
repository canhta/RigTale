#!/usr/bin/env python3
"""Check the production brief against the cast it directs.

`RISK-07` fails a production that declares an action its rig cannot perform.
A brief written in prose can drift from the manifest silently: a joint gets
renamed, a slot member is dropped, and the brief still reads correctly. This
refuses that.

What it checks:

  1. Every backtick-quoted rig reference in the brief resolves to a real
     layer, joint, slot member or bone in `cast/manifest.json`.
  2. Every shot list sums to its declared duration, and each duration is
     inside the charter's 150-210 second window.
  3. The cut rate recorded in `creative-intent.json` matches the shot list.
  4. `creative-intent.json` carries all six Gate 1 fields for both
     productions, and a stimulation profile whose fields are all present.
  5. The two productions declare a different storyline, focus and concept,
     which is what `RISK-41` asserts.

    python3 fixtures/tools/check_brief.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "fixtures/cast/manifest.json"
BRIEF = ROOT / "fixtures/brief/production-brief.md"
INTENT = ROOT / "fixtures/brief/creative-intent.json"

# The charter's reference-production window, Objective 1.
MIN_SECONDS, MAX_SECONDS = 150, 210


def fail(message: str) -> None:
    raise SystemExit(f"brief: {message}")


def vocabulary(manifest: dict) -> tuple[set, set, set, set, set]:
    """Everything the brief is allowed to name, read from the manifest."""
    parts = {(p["character"], p["layer"]): p for p in manifest["parts"]}
    layers = {layer for _, layer in parts}
    joints = {f"{layer}/{joint}"
              for (_, layer), record in parts.items() for joint in record["joints"]}
    slots, bones = set(), set()
    for character in manifest["rig"]:
        for slot in manifest["rig"][character].get("slots", {}).values():
            slots.update(slot["members"])
        for bone in manifest["rig"][character].get("bones", []):
            bones.add(bone["name"] if isinstance(bone, dict) else bone)
    return layers, joints, slots, bones, set(manifest["rig"])


def check_references(text: str, manifest: dict) -> int:
    layers, joints, slots, bones, characters = vocabulary(manifest)
    refs = set(re.findall(r"`([a-z_]+/[a-z_]+)`", text))
    refs |= set(re.findall(r"`(mouth_[a-z_]+|eye_[a-z_]+|hand_[a-z_]+|tail_[a-z]+|rump)`", text))

    unresolved = []
    for ref in sorted(refs):
        if ref in slots or ref in bones or ref in layers or ref in joints:
            continue
        if ref.startswith(("fixtures/", "docs/", ".sandbox/")):
            continue  # a repository path, not a rig reference
        if "/" in ref:
            head, tail = ref.split("/", 1)
            if head in characters and (head, tail) in {
                    (c, l) for c, l in [(p["character"], p["layer"]) for p in manifest["parts"]]}:
                continue  # character/layer
            if any(j.split("/", 1)[1] == tail for j in joints if j.startswith(head + "/")):
                continue  # layer/joint
            if head in characters:
                # character/joint: the brief's shorthand for "this character's joint",
                # which may sit on any of its layers.
                owned = {f"{p['layer']}/{j}" for p in manifest["parts"]
                         if p["character"] == head for j in p["joints"]}
                if any(o.split("/", 1)[1] == tail for o in owned):
                    continue
        unresolved.append(ref)

    if unresolved:
        fail("these rig references do not exist in cast/manifest.json, so the brief "
             f"directs an action the cast cannot perform: {unresolved}")
    return len(refs)


def parse_shots(text: str) -> dict:
    """Read each shot table back out of the brief."""
    runs: dict[str, list] = {}
    for match in re.finditer(
            r"^\|\s*([AB])(\d\d)\s*\|\s*(\d+):(\d\d)[–-](\d+):(\d\d)\s*\|\s*(\d+)\s*\|",
            text, re.M):
        production, _, m0, s0, m1, s1, dur = match.groups()
        start, end, dur = int(m0) * 60 + int(s0), int(m1) * 60 + int(s1), int(dur)
        if end - start != dur:
            fail(f"shot {production}{_} spans {end - start}s but its table says {dur}s")
        runs.setdefault(production, []).append((start, end, dur))
    if not runs:
        fail("no shot tables found; the brief must carry them in the documented format")
    return runs


def check_shots(runs: dict, intent: dict) -> None:
    declared = {p["id"]: p for p in intent["productions"]}
    profile = intent["shared"]["stimulation_profile"]["cut_rate"]

    for production, shots in sorted(runs.items()):
        shots.sort()
        total = sum(d for _, _, d in shots)
        if production not in declared:
            fail(f"production {production} has a shot list but no entry in creative-intent.json")
        stated = declared[production]["duration_seconds"]
        if total != stated:
            fail(f"production {production} shots sum to {total}s; creative-intent.json "
                 f"declares {stated}s")
        if not MIN_SECONDS <= total <= MAX_SECONDS:
            fail(f"production {production} is {total}s, outside the charter window "
                 f"{MIN_SECONDS}-{MAX_SECONDS}s")
        for (a_start, a_end, _), (b_start, _, _) in zip(shots, shots[1:]):
            if a_end != b_start:
                fail(f"production {production} has a gap or overlap at {a_end}s")

        cuts = len(shots) - 1
        rate = round(cuts / (total / 60.0), 2)
        recorded = profile.get(f"measured_production_{production.lower()}")
        if recorded is None:
            fail(f"creative-intent.json records no measured cut rate for production {production}")
        if abs(rate - float(recorded)) > 0.01:
            fail(f"production {production} cut rate is {rate}/min; creative-intent.json "
                 f"records {recorded}")
        print(f"production {production}: {total}s, {len(shots)} shots, {cuts} cuts, "
              f"{rate}/min")


def check_intent(intent: dict) -> None:
    shared = intent["shared"]
    # Two Gate 1 fields differ per production; the rest are shared by both.
    per_production = {"duration_seconds", "purpose"}
    for field in intent["gate1_fields"]:
        if field in per_production:
            for production in intent["productions"]:
                if field not in production:
                    fail(f"Gate 1 field '{field}' is missing from production "
                         f"{production['id']}")
            continue
        if field not in shared:
            fail(f"Gate 1 field '{field}' is missing from creative-intent.json")
    for production in intent["productions"]:
        if "duration_seconds" not in production:
            fail(f"production {production['id']} declares no duration")
        if "purpose" not in production:
            fail(f"production {production['id']} declares no purpose")

    for field in ("cut_rate", "motion_amplitude", "colour_intensity", "audio_level_range"):
        if field not in shared["stimulation_profile"]:
            fail(f"stimulation profile is missing '{field}', which RISK-58 requires")

    # RISK-41: the two productions must differ on the narrative axis, not in assets.
    a, b = intent["productions"]
    for axis in ("declared_storyline", "declared_focus", "declared_concept"):
        if a[axis].strip().lower() == b[axis].strip().lower():
            fail(f"both productions declare the same {axis}; RISK-41 requires them to differ")
    print("creative-intent: 6 Gate 1 fields, 4 stimulation fields, "
          "3 narrative axes distinct")


def main() -> None:
    manifest = json.loads(MANIFEST.read_text())
    text = BRIEF.read_text()
    intent = json.loads(INTENT.read_text())

    checked = check_references(text, manifest)
    check_intent(intent)
    check_shots(parse_shots(text), intent)
    print(f"brief: {checked} rig references resolve against cast/manifest.json")


if __name__ == "__main__":
    main()
