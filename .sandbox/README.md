# Local Sandbox — Third-Party Experimental Assets

This directory holds assets downloaded from the Internet for **local technical experimentation only**. Everything in it except this file is Git-ignored.

## Policy

RigTale may download and use Internet resources for technical experiments in this sandbox, provided each resource is obtained and used in accordance with its licence or terms.

**Hard rules. None of them is optional.**

1. Downloaded resources are used **only** inside this sandbox.
2. All sandbox resources are Git-ignored.
3. Output produced from a sandbox asset is Git-ignored. Write it under `output/`; do not write derived artifacts elsewhere in the tree.
4. These files are never committed, packaged, published, or included in a release.
5. **A sandbox asset is never an official fixture and never approval evidence.**
6. Any result intended as official evidence must be reproduced from assets with clearly established redistribution rights.
7. **`.gitignore` does not alter or remove any copyright or licence obligation.** Ignoring a file changes what Git tracks, nothing else. Attribution, share-alike, non-commercial, and no-derivatives terms continue to bind regardless.

## Layout

| Path | Contents |
|---|---|
| `downloads/` | Raw fetches, unmodified, as retrieved |
| `assets/` | Prepared or converted working copies |
| `output/` | Renders and any other derived artifacts |
| `PROVENANCE.md` | Required ledger, see below |

## Required provenance ledger

Before using any downloaded resource, add a row to `.sandbox/PROVENANCE.md`: source URL, retrieval date, stated licence or terms, the licence file or terms page URL, and what the asset is used for. The ledger stays local, like the assets it describes.

Keep it because the obligation outlives the file. If an experiment ever needs promoting to official evidence, the ledger is what tells you whether the asset can make that move or must be replaced.

## What "official evidence" means here

`SPIKE-F001` fixtures, anything cited in a spike result, anything supporting a decision record, and anything in the reference production. If a result matters to a decision, it must stand on redistributable assets — reproduce it before citing it.

Sandbox assets exist to answer questions like "does this renderer composite a textured mesh headlessly on macOS" without waiting for the official cast. That is their whole purpose, and their limit.
