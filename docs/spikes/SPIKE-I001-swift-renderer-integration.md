# SPIKE-I001: Swift-to-Renderer Integration

**Tracker:** `RGT-S006`

**Status:** Queued. Do not execute before a qualified renderer and stable job or compiled-shot boundary exist.

## Question

Which integration boundary lets a native Swift macOS studio control compilation, preview, and rendering reliably while preserving UI responsiveness, crash isolation, packaging, diagnostics, reproducibility, and a future headless or cloud execution path?

## Why This Requires a Spike

Direct native binding can reduce latency but couples Swift to renderer ABI and process failures. A child process or local service improves isolation but introduces packaging, IPC, lifecycle, and data-transfer costs. The correct choice must be compared across every qualified backend and measured workload before `RGT-D010` selects the final pairing.

## Preconditions

- `SPIKE-A001` has established the candidate compilation boundary.
- `SPIKE-R001` has qualified renderer backends and recorded integration surfaces.
- `SPIKE-R002` has clarified preview behavior where relevant.
- The representative fixture, job lifecycle, error contract, and render manifest are versioned.

## Approaches to Compare

1. **Native library or C-compatible bridge:** Swift invokes an embedded runtime through a stable ABI.
2. **Supervised child process:** Swift launches a packaged worker and communicates through framed IPC or files plus structured events.
3. **Local service:** Swift connects to a separately managed localhost or socket service using the application API.
4. **Hybrid:** lightweight preview is embedded while final rendering uses an isolated worker, only if parity evidence supports it.

Unsupported approaches may be removed only with source-level evidence. New approaches may be added when a qualified renderer requires them.

## Required Behaviors

- start, health check, version negotiation, and capability discovery;
- submit idempotent preview, frame-range, shot, and episode jobs;
- report progress and structured diagnostics without blocking the main UI thread;
- cancel and terminate work safely;
- isolate renderer crash, hang, excessive memory, and malformed input;
- resume or retry from persisted job state;
- locate artifacts without embedding unstable absolute paths in durable contracts;
- transport or reference review frames efficiently;
- package, sign, notarize, install, update, and uninstall dependencies predictably; and
- reuse the worker or application boundary for CLI and future headless execution where practical.

## Method

1. Inspect every qualified backend's official embedding, headless, extension, and redistribution interfaces.
2. Implement the smallest equivalent control surface for each viable backend/integration approach.
3. Drive the same diagnostic and full-production jobs from a minimal native Swift harness.
4. Measure startup, command latency, progress delivery, frame transport, CPU, GPU, memory, and shutdown.
5. Inject renderer crash, process kill, hang, malformed message, incompatible version, cancellation, disk exhaustion, and application restart.
6. Build and verify signed distribution artifacts in the intended macOS packaging model.
7. Exercise clean installation, upgrade, rollback where supported, and removal without deleting projects.
8. Compare how each approach extends to CLI, CI, and future cloud workers.

## Measurements

- cold and warm startup time;
- preview command and first-frame latency;
- job throughput relative to direct backend execution;
- memory overhead and media-copy cost;
- UI responsiveness during normal and failed jobs;
- crash containment and successful recovery rate;
- cancellation and shutdown latency;
- package size, signing complexity, dependency update surface, and clean-install success;
- diagnostic fidelity across the boundary; and
- implementation size, test burden, and solo-maintenance cost.

## Security Checks

- Validate all IPC messages and artifact references.
- Prevent worker input from escaping its assigned workspace.
- Avoid passing provider secrets to render workers.
- Restrict network access unless the backend demonstrably requires it.
- Verify bundled binary provenance, license, integrity, and update behavior.
- Confirm logs and crash reports do not expose private production content unexpectedly.

## Required Outputs

- Minimal integration harnesses and reproducible commands for every viable approach.
- Failure-injection results, measurements, package artifacts, and clean-install evidence.
- Recommended process and IPC boundary or a documented decision to defer.
- Proposed application API, job, health, version, and diagnostic contract revisions.
- macOS packaging, signing, upgrade, and renderer-dependency policy.
- Updates to system design, operations, quality system, and implementation plan.
- Decision inputs for `RGT-D010`, including qualified and rejected backend/integration combinations plus any binding implementation-language constraints.

## Exit Criteria

- At least two viable integration approaches are executed unless primary evidence proves only one is technically possible.
- The complete fixture can be started, monitored, cancelled, failed, recovered, and rerun from Swift.
- A renderer crash cannot corrupt the project or terminate the studio application under the accepted boundary.
- Clean installation and packaged execution succeed on the supported test environment.
- CLI and future headless implications are documented.
- Every recommended approach is justified by measurements and maintenance cost; final selection remains with `RGT-D010`.
