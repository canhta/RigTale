# SPIKE-CS001: Contract Tooling and Local Artifact Storage

**Tracker:** `RGT-S011`

**Status:** Queued. Execute after the contract, migration, corruption, dependency, and archive fixture cases are approved.

## Question

Which schema, serialization, content-identity, migration, and local-storage approach can preserve RigTale's versioned production artifacts safely across Swift, shortlisted core-language boundaries, CLI automation, and future cloud adapters?

## Why This Requires Evidence

Readable example objects do not prove forward compatibility, exact time handling, unknown-field preservation, deterministic digests, atomic publication, index rebuildability, corruption recovery, or archive restoration. A convenient schema or embedded database may also create unacceptable cross-language or migration cost.

## Preconditions

- `SPIKE-C001` has screened relevant production and storage patterns.
- `SPIKE-F001` has published contract, invalid-input, migration, corruption, dependency, invalidation, backup, and archive cases.
- The common envelope and canonical object responsibilities are coherent v1 drafts.
- No schema language, serialization, ID format, digest algorithm, embedded database, or cloud database is selected.

## Candidate Dimensions

The spike compares compatible combinations rather than isolated popularity:

- schema definition and code-generation model;
- human-readable authoring representation versus canonical stored representation;
- stable IDs, content digests, canonicalization, and exact time encoding;
- unknown-field and extension preservation;
- migration tooling and version negotiation;
- filesystem object layout and atomic publication;
- embedded metadata index, index rebuild, and dependency queries;
- backup, archive export, restore, corruption detection, and garbage collection; and
- Swift, each shortlisted core-language boundary, CLI, and future service interoperability.

Cloud databases and distributed queues are not selected here. The local interfaces and evidence must remain portable to later adapters.

## Method

1. Inspect official specifications, compatibility guarantees, exact implementations, licenses, and maintenance state for qualified candidates.
2. Encode every canonical contract plus valid, invalid, previous-version, and extension-bearing fixtures.
3. Verify deterministic round trips, unknown-field behavior, exact time, canonical digest, and structured validation errors.
4. Implement representative migrations, including interrupted and repeated migration attempts.
5. Publish immutable artifacts atomically while concurrent readers inspect the previous version.
6. Build and rebuild a local dependency index from canonical manifests.
7. Apply a source change and verify stale-artifact explanation plus the expected invalidation set.
8. Inject truncated files, digest mismatch, missing objects, corrupt index, interrupted write, incompatible schema, and insufficient disk.
9. Export, restore, verify, and rerender-address the fixture archive on a clean environment.
10. Measure cross-language integration, generated-code burden, storage growth, query behavior, migration complexity, and solo-maintenance cost.

## Measurements

- round-trip and migration correctness;
- deterministic content identity across supported languages and machines;
- validation precision and corrupt-data detection;
- publication atomicity and recovery behavior;
- index rebuild time and dependency-query correctness;
- archive size, export and restore time, and checksum coverage;
- schema evolution and generated-code churn;
- Swift and shortlisted core-language integration complexity;
- license, packaging, and long-term maintenance risk; and
- clear separation between canonical artifacts and disposable indexes or caches.

## Required Outputs

- Exact candidate versions, source references, fixtures, commands, and results.
- Recommended contract tooling, serialization, canonicalization, ID and digest policy, migration approach, local object layout, and metadata-index approach, or a documented reason to defer.
- Failure catalogue for corruption, migration, publication, rebuild, backup, and restore.
- Proposed revisions to production contracts, system design, operations, quality system, implementation plan, and traceability matrix.
- Decision inputs for `RGT-D012`; accepted choices are recorded only by that decision.

## Exit Criteria

- At least two viable contract/storage combinations are evaluated unless primary evidence proves only one satisfies a mandatory constraint.
- Every approved contract, migration, corruption, dependency, invalidation, and archive fixture has a reproducible result.
- Canonical digests and exact time behave consistently across every evaluated language boundary.
- A corrupt or missing local index can be rebuilt without losing canonical production state.
- Interrupted publication or migration cannot present partial data as approved.
- Export and clean restore reproduce all required artifact identities and dependency relationships.
- D012 receives enough evidence to accept, reject, or defer each material choice independently.
- D012 may select only a language/tooling/storage combination exercised by this spike; a materially different combination requires a confirmatory rerun of the affected fixtures.
