# RigTale — Working Rules

This is a documentation and research repository. There is no application code yet.

## Writing docs

- **One version of the truth.** Delete superseded text outright. Never strike it through, never keep an old and a new statement side by side, never add a "retained for the record" or "superseded claim" section. Git history is the record. When enforcing this, grep the phrasing as well as the `~~` markup — the prose form is the common one and searching only for strikethrough misses it.
- **Short and focused.** Every document states what is true now and stops. Do not restate a point in two places, do not add a paragraph explaining that a change was made when the changed text already says it.
- **Correct in place.** When a claim turns out to be wrong, rewrite the claim. Keep a correction note only when the reasoning error itself is the finding worth carrying forward, and keep it to a few lines.
- **No duplication across files.** `TODO.md` tracks status and dependencies. Documents own their content. Do not copy content into `TODO.md` or between documents; link instead.

## Evidence

- Every competitive or technical claim cites primary evidence: an exact commit SHA and file path, a release tag, or an official specification or documentation URL.
- READMEs, marketing pages, and star counts are discovery signals, and must be labelled as such.
- If a fact cannot be verified from a primary source, record it as `not verified`. Never infer, and never assert a superlative from search-index confidence.
- Label statements about user behaviour: `[FACT]`, `[REPORTED]`, `[HYPOTHESIS]`, `[UNKNOWN]`, `[OWNER-STATED]`. These labels are load-bearing.
- Screening is read-only. Clone and read source; do not build, install, or execute candidate code.
- Internet-sourced assets may be downloaded into the ignored `.sandbox/` workspace for local technical experiments, under their own licence or terms. They are never fixtures, approval evidence, or release content, and any result promoted to official evidence must be reproduced on assets with provable redistribution rights. `.gitignore` changes what Git tracks and nothing else; licence obligations are unaffected. Full policy: `.sandbox/README.md`.

## Governance

- Spikes produce dispositions routed to a later spike or decision item. They never select technology. Only a decision record selects.
- Unknowns stay spikes. Do not silently promote one into an architecture decision.
- Closing a spike requires a propagation table: one row per material finding, with the requirement, contract, design, test, or plan it binds, and the edit that landed there. A finding with no target needs a recorded reason.
- The charter is owner-governed. Changing approved business scope requires an explicit revision recorded in `docs/requirements/charter.md` under Charter Revisions, never an evidence-state transition in a spike or in `TODO.md`.
- The Project Owner is the sole decision-maker and implementer. No external participants, interviews, or reviewers.

## Consequences worth remembering

- `RGT-S009B` was rejected, so every user-behaviour claim in `docs/research/small-studio-workflow.md` stays a hypothesis permanently, and `PR-F002` can never be promoted.
- Blind quality review is waived, so the 50% time metric rests on an owner self-assessment. State that limitation wherever the metric is used.
- The largest open risk is output quality: nothing yet shows an agent can write structured direction that yields publishable animation.
