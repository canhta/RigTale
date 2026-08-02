# RigTale Deployment and Operations

**Status:** v1 draft; evidence-pending.

## Purpose

This document defines the operational behavior required to install, run, observe, recover, upgrade, and later host RigTale. It separates stable operational requirements from undecided technology choices.

## Deployment Profiles

### Local macOS Studio

The primary profile runs the native Swift studio application, local production services, managed workers, artifact storage, and the selected renderer on a supported creator workstation. Network access is optional for provider-backed creative work and unnecessary for editing or rendering an approved compatible production.

### Local automation

CLI and API operation support tests, scripted production, CI, and headless jobs. Commands and APIs operate on the same artifacts and job model as the studio application.

### Agent-hosted MCP

A local MCP adapter exposes scoped production tools to compatible hosts. It must start, stop, report health, locate projects safely, stream or poll long jobs, and preserve host approval semantics.

### Future web and cloud service

A remote application API, web studio, metadata service, artifact storage, and worker pools run the same logical pipeline. Cloud operation is an adapter and deployment evolution, not a second production implementation.

## Installation and Distribution

Local distribution must provide:

- signed and notarized macOS application artifacts where distribution policy requires them;
- declared supported macOS and hardware ranges based on renderer evidence;
- verified installation of bundled or separately managed engine dependencies;
- a first-run diagnostic for storage, media tools, renderer, permissions, and provider configuration;
- a clean uninstall path that does not delete user projects silently; and
- offline documentation and recovery instructions.

Whether render dependencies are bundled, downloaded, or installed separately is decision-pending and must consider size, licensing, signing, security updates, and reproducibility.

## Process Model

The UI must remain responsive when compilation, media analysis, rendering, or agent work fails or consumes significant resources. Expensive or untrusted tasks should run in supervised processes or workers with:

- explicit input and output directories;
- CPU, GPU, memory, disk, duration, and concurrency limits where supported;
- health, heartbeat, cancellation, and graceful-termination behavior;
- captured structured diagnostics and sanitized logs; and
- atomic publication of completed output.

The final process and IPC architecture depends on renderer and Swift integration spikes.

## Configuration and Secrets

- Project configuration is versioned separately from machine configuration.
- Machine configuration includes paths, resources, cache limits, and installed adapter versions.
- User secrets use system credential storage locally and a managed secret service in hosted deployments.
- Secrets are referenced by logical key and never serialized into production artifacts, archives, logs, or crash reports.
- Environment overrides are documented, namespaced, validated, and visible in diagnostics.
- Provider, renderer, and storage adapters expose non-secret effective configuration for reproducibility.

## Storage Layout and Data Safety

Canonical storage must distinguish:

- immutable published artifacts;
- mutable working state with recoverable history;
- derived previews and caches;
- render attempts and final media;
- indexes that can be rebuilt; and
- backups or exported archives.

Content digests identify immutable data and deduplicate where safe. Garbage collection may remove reproducible caches only after proving no published manifest or active job references them. User source assets, published artifacts, approvals, final deliveries, and audit history are never classified as disposable cache.

## Backup, Restore, and Archive

- A production export includes schemas, exact asset versions, creative artifacts, compiled state where required, review records, delivery manifests, provenance, and checksums.
- Restore validates checksums, schema support, adapter availability, and licenses before opening the project as healthy.
- Backup procedures support local external storage first and future remote targets through adapters.
- Restore is tested, not inferred from successful backup creation.
- Migration creates a new recoverable version or backup boundary before changing canonical data.

Retention and archive-size policies require workload evidence.

## Job Recovery

- Jobs persist state before execution and after every externally visible transition.
- Workers acquire expiring leases; abandoned jobs return to a recoverable state.
- Attempts write isolated output and cannot overwrite approved artifacts.
- Retry policy distinguishes transient failures, resource exhaustion, invalid input, and internal defects.
- Resume uses verified checkpoints only; otherwise the affected shot or stage restarts safely.
- Cancellation preserves diagnostics and removes only uncommitted temporary output.

## Observability

Local users need an inspectable activity view containing:

- current and historical jobs;
- stage, progress, attempt, and affected artifact;
- structured errors and remediation;
- component and adapter versions;
- CPU, GPU, memory, disk, and elapsed-time measurements where available;
- agent calls, budgets, retries, and provider status; and
- render and delivery manifests.

Logs use correlation IDs and structured events. Remote telemetry is opt-in for local deployments unless a hosted service documents otherwise. Sensitive source text, media, credentials, and private paths are redacted or excluded by default.

## Security and Supply Chain

- Imported archives, media, fonts, layered files, scripts, and engine projects are treated as untrusted.
- File extraction prevents path traversal and unsafe links.
- Media parsers and third-party render processes use least privilege and isolated work directories.
- Network access for render workers is disabled unless an adapter explicitly requires it.
- Dependencies, binaries, reference assets, and licenses are inventoried and pinned for reproducible releases.
- Release artifacts include checksums and generated dependency/license notices.
- Vulnerability response defines affected versions, mitigations, upgrade paths, and project compatibility.
- Cloud authorization, tenant isolation, audit retention, and abuse controls are designed before hosted data is accepted.

## Upgrades and Migrations

An upgrade must:

1. inspect current application, contract, project, and adapter versions;
2. report compatibility and required migrations before mutation;
3. create a recoverable backup boundary;
4. migrate through versioned, idempotent steps;
5. validate projects and fixtures after migration; and
6. support documented rollback when formats and security policy permit.

The application must not upgrade a renderer or contract silently when doing so could change visible output.

## Capacity and Cost

The system records preview latency, render throughput, memory, storage growth, cache hit rate, provider usage, and failure retries per workload and environment. Default concurrency and cache limits derive from measured reference-production behavior.

Cloud planning must model storage, egress, render compute, queue time, provider usage, retention, and support cost. Subscription-hosted MCP operation and embedded provider billing remain separate cost paths.

## Cloud Evolution Gates

Cloud work begins only after local production proves:

- stable versioned contracts and migrations;
- renderer execution on a supported headless environment;
- resumable jobs and portable artifacts;
- deterministic validation and delivery manifests;
- measured workload and cost envelopes; and
- security review for uploaded assets and production data.

The first cloud service should reuse local services and adapters. It must not introduce multi-tenant billing, marketplace, or organization features merely because a remote worker exists.

## Operational Qualification

A release is operationally qualified when a clean supported Mac can install the application, restore the reference project, inspect assets, apply one structured shot correction, resume an interrupted render, produce a valid delivery, export an archive, and restore it again using documented procedures.

Exact platform versions, hardware floors, performance thresholds, packaging model, renderer process, server language, storage engine, and cloud providers remain evidence-pending.
